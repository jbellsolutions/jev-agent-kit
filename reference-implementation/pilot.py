"""Offline pilot foundation. No HTTP, browser, credentials, or email transport."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import csv
from decimal import Decimal, ROUND_CEILING
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import time
import uuid

JEV = "jev-1.13.0"
GLM = "z-ai/glm-5.3-flash"
LUNA_BATCH = "openai/gpt-5.6-luna:batch"
MODELS = {JEV, GLM, LUNA_BATCH}
TARGET = 10_000_000_000
CEILING = 20_000_000_000


class Conflict(ValueError):
    pass


class BudgetExceeded(ValueError):
    pass


def money(usd):
    number = Decimal(str(usd))
    if not number.is_finite() or number < 0:
        raise ValueError("Cost must be finite and nonnegative")
    return int((number * 1_000_000_000).to_integral_value(rounding=ROUND_CEILING))


def encoded(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(encoded(value).encode()).hexdigest()


def route(kind, *, fallback_reason=None):
    if kind not in {"decision", "reasoning", "writing"}:
        raise ValueError("Unknown model task")
    if fallback_reason is not None and fallback_reason not in {"unavailable", "quality_failed"}:
        raise ValueError("Unknown fallback reason")
    if kind == "decision":
        if fallback_reason:
            raise ValueError("Escalate as a reasoning job before using a text model")
        return {"model": JEV, "mode": "hosted_guarded", "fallback_reason": None}
    return {"model": LUNA_BATCH if fallback_reason else GLM,
            "mode": "batch" if fallback_reason else "synchronous",
            "fallback_reason": fallback_reason}


class Pilot:
    def __init__(self, path):
        self.path = str(path)
        if self.path == ":memory:":
            raise ValueError("Use a persistent database path")
        with self.db() as db:
            db.executescript("""
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS config(id INTEGER PRIMARY KEY CHECK(id=1), target INTEGER, ceiling INTEGER);
                CREATE TABLE IF NOT EXISTS calls(
                    id TEXT PRIMARY KEY, model TEXT NOT NULL, fingerprint TEXT NOT NULL,
                    reserved INTEGER NOT NULL, charged INTEGER, state TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS rows(
                    dataset TEXT, row_number INTEGER, original TEXT NOT NULL,
                    PRIMARY KEY(dataset,row_number));
                CREATE TABLE IF NOT EXISTS jobs(
                    id TEXT PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL,
                    state TEXT NOT NULL, lease TEXT, worker TEXT, expires REAL, result TEXT);
                CREATE TABLE IF NOT EXISTS profiles(
                    id TEXT PRIMARY KEY, sender TEXT NOT NULL UNIQUE);
                CREATE TABLE IF NOT EXISTS suppressed(recipient TEXT PRIMARY KEY);
                CREATE TABLE IF NOT EXISTS messages(
                    id TEXT PRIMARY KEY, campaign TEXT NOT NULL, recipient TEXT NOT NULL,
                    profile TEXT NOT NULL, body TEXT NOT NULL, state TEXT NOT NULL,
                    attempt TEXT, started REAL, evidence TEXT,
                    UNIQUE(campaign,recipient));
            """)
            db.execute("INSERT OR IGNORE INTO config VALUES(1,?,?)", (TARGET, CEILING))
            values = db.execute("SELECT target,ceiling FROM config WHERE id=1").fetchone()
            if tuple(values) != (TARGET, CEILING):
                raise Conflict("Existing pilot budget differs; do not reset it on startup")

    @contextmanager
    def db(self):
        connection = sqlite3.connect(self.path, timeout=15)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def budget(self):
        with self.db() as db:
            totals = db.execute("""SELECT COALESCE(SUM(COALESCE(charged,reserved)),0),
                COALESCE(SUM(charged),0) FROM calls""").fetchone()
        used, settled = totals
        return {"target_usd": TARGET / 1e9, "ceiling_usd": CEILING / 1e9,
                "spent_and_reserved_usd": used / 1e9, "settled_usd": settled / 1e9,
                "target_reached": used >= TARGET, "remaining_usd": max(0, CEILING-used) / 1e9,
                "over_ceiling": used > CEILING}

    def reserve(self, call_id, model, request, max_usd):
        if model not in MODELS or not call_id:
            raise ValueError("A known model and stable call ID are required")
        maximum, fingerprint = money(max_usd), digest(request)
        if maximum <= 0:
            raise ValueError("A positive cost reservation is required")
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT * FROM calls WHERE id=?", (call_id,)).fetchone()
            if old:
                if (old["model"], old["fingerprint"], old["reserved"]) != (model, fingerprint, maximum):
                    raise Conflict("Call ID reused with different model, input, or maximum")
                return {"dispatch": False, "state": old["state"]}
            used = db.execute("SELECT COALESCE(SUM(COALESCE(charged,reserved)),0) FROM calls").fetchone()[0]
            if used + maximum > CEILING:
                raise BudgetExceeded("Pilot model ceiling would be exceeded")
            db.execute("INSERT INTO calls VALUES(?,?,?,?,NULL,'pending')", (call_id, model, fingerprint, maximum))
        return {"dispatch": True, "state": "pending"}

    def uncertain(self, call_id):
        with self.db() as db:
            if not db.execute("UPDATE calls SET state='uncertain' WHERE id=? AND state='pending'", (call_id,)).rowcount:
                raise Conflict("Call is missing or already resolved")

    def settle(self, call_id, actual_usd):
        actual = money(actual_usd)
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM calls WHERE id=?", (call_id,)).fetchone()
            if not row:
                raise Conflict("Cannot settle a call without a reservation")
            if row["charged"] is not None:
                if row["charged"] != actual:
                    raise Conflict("Conflicting billing reconciliation")
                return
            # Never hide actual charges if a provider exceeds a reservation.
            db.execute("UPDATE calls SET charged=?,state='settled' WHERE id=?", (actual, call_id))

    def import_rows(self, raw_csv):
        if not isinstance(raw_csv, bytes):
            raise ValueError("Import requires original CSV bytes")
        dataset = hashlib.sha256(raw_csv).hexdigest()
        reader = csv.DictReader(io.StringIO(raw_csv.decode("utf-8-sig"), newline=""))
        if not reader.fieldnames or any(not name or not name.strip() for name in reader.fieldnames):
            raise ValueError("CSV needs nonempty column names")
        if len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError("Duplicate column names would lose data")
        count = 0
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            for count, original in enumerate(reader, 1):
                if None in original or any(value is None for value in original.values()):
                    raise ValueError(f"CSV row {count} has a different column count")
                payload = encoded(original)
                db.execute("INSERT OR IGNORE INTO rows VALUES(?,?,?)", (dataset, count, payload))
                job_id = f"enrich:{dataset}:{count}"
                db.execute("INSERT OR IGNORE INTO jobs(id,kind,payload,state) VALUES(?,?,?,'queued')",
                           (job_id, "enrich", encoded({"dataset": dataset, "row_number": count, "original": original})))
        return {"dataset": dataset, "rows": count}

    def enqueue(self, job_id, kind, payload):
        if kind not in {"enrich", "draft"} or not job_id:
            raise ValueError("Only enrichment and draft jobs use this queue")
        value = encoded(payload)
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT kind,payload FROM jobs WHERE id=?", (job_id,)).fetchone()
            if old and tuple(old) != (kind, value):
                raise Conflict("Job ID reused with different input")
            db.execute("INSERT OR IGNORE INTO jobs(id,kind,payload,state) VALUES(?,?,?,'queued')", (job_id, kind, value))

    def claim(self, kind, worker, *, now=None, lease_seconds=60):
        if kind not in {"enrich", "draft"} or not worker or lease_seconds <= 0:
            raise ValueError("Invalid worker claim")
        now = time.time() if now is None else now
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM jobs WHERE kind=? AND state='queued' ORDER BY rowid LIMIT 1", (kind,)).fetchone()
            if not row:
                return None
            lease = str(uuid.uuid4())
            db.execute("UPDATE jobs SET state='claimed',lease=?,worker=?,expires=? WHERE id=?", (lease, worker, now+lease_seconds, row["id"]))
        return {"id": row["id"], "kind": kind, "payload": json.loads(row["payload"]), "lease": lease}

    def complete(self, job_id, lease, result, *, now=None):
        now = time.time() if now is None else now
        with self.db() as db:
            changed = db.execute("""UPDATE jobs SET state='complete',result=?
                WHERE id=? AND lease=? AND state='claimed' AND expires>?""", (encoded(result), job_id, lease, now)).rowcount
            if not changed:
                raise Conflict("Job lease expired, changed, or is no longer active")

    def recover_expired(self, *, now=None):
        now = time.time() if now is None else now
        with self.db() as db:
            # A model request may already be in flight: hold for reconciliation.
            return db.execute("UPDATE jobs SET state='held',lease=NULL WHERE state='claimed' AND expires<=?", (now,)).rowcount

    def add_profile(self, profile_id, sender):
        sender = self.email(sender)
        if not profile_id:
            raise ValueError("Profile ID is required")
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            old = db.execute("SELECT sender FROM profiles WHERE id=?", (profile_id,)).fetchone()
            if old and old[0] != sender:
                raise Conflict("Profile already belongs to another sender")
            if not old and db.execute("SELECT COUNT(*) FROM profiles").fetchone()[0] >= 10:
                raise Conflict("Pilot allowance of ten sender profiles reached")
            db.execute("INSERT OR IGNORE INTO profiles VALUES(?,?)", (profile_id, sender))
            bound = db.execute("SELECT sender FROM profiles WHERE id=?", (profile_id,)).fetchone()
            if not bound or bound[0] != sender:
                raise Conflict("Sender is already assigned to another profile")

    @staticmethod
    def email(value):
        value = value.strip().casefold()
        if value.count("@") != 1 or any(c.isspace() or ord(c)<32 for c in value):
            raise ValueError("Expected one email address")
        local, domain = value.split("@")
        if not local or not domain or any(c in value for c in ",;<>\"()"):
            raise ValueError("Expected a plain email address")
        return value

    def plan_message(self, campaign, recipient, profile, subject, body):
        recipient = self.email(recipient)
        if not campaign or not subject.strip() or not body.strip() or "\n" in subject or "\r" in subject:
            raise ValueError("Campaign and exact subject/body are required")
        message_id = digest([campaign, recipient])
        content = encoded({"subject": subject, "body": body})
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            if not db.execute("SELECT 1 FROM profiles WHERE id=?", (profile,)).fetchone():
                raise ValueError("Unknown sender profile")
            old = db.execute("SELECT profile,body FROM messages WHERE id=?", (message_id,)).fetchone()
            if old and tuple(old) != (profile, content):
                raise Conflict("Recipient already has a different frozen message in this campaign")
            db.execute("""INSERT OR IGNORE INTO messages(id,campaign,recipient,profile,body,state)
                VALUES(?,?,?,?,?,'planned')""", (message_id, campaign, recipient, profile, content))
        return message_id

    def suppress(self, recipient):
        with self.db() as db:
            db.execute("INSERT OR IGNORE INTO suppressed VALUES(?)", (self.email(recipient),))

    def _match(self, db, message_id, observed):
        row = db.execute("""SELECT m.*,p.sender FROM messages m JOIN profiles p ON m.profile=p.id
            WHERE m.id=?""", (message_id,)).fetchone()
        if not row:
            raise ValueError("Unknown message")
        expected = {"profile": row["profile"], "sender": row["sender"], "recipient": row["recipient"], **json.loads(row["body"])}
        if any(observed.get(key) != value for key, value in expected.items()):
            raise Conflict("Observed identity or content differs from the frozen message")
        return row

    def begin_send(self, message_id, observed, *, now=None):
        """Internal pre-execution ledger only; caller must enforce campaign authorization."""
        now = time.time() if now is None else now
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = self._match(db, message_id, observed)
            if row["state"] != "planned":
                raise Conflict("An attempt already exists; reconcile it, never replay")
            if db.execute("SELECT 1 FROM suppressed WHERE recipient=?", (row["recipient"],)).fetchone():
                raise Conflict("Recipient is suppressed")
            if db.execute("SELECT 1 FROM messages WHERE profile=? AND state IN ('attempting','uncertain')", (row["profile"],)).fetchone():
                raise Conflict("This sender has an unresolved attempt; reconcile it first")
            # Count attempted/uncertain sends across campaigns for this pilot.
            attempted = db.execute("SELECT COUNT(*) FROM messages WHERE profile=? AND state!='planned'", (row["profile"],)).fetchone()[0]
            if attempted >= 20:
                raise Conflict("Pilot sender allowance of 20 attempts reached")
            attempt = str(uuid.uuid4())
            db.execute("UPDATE messages SET state='attempting',attempt=?,started=? WHERE id=?", (attempt, now, message_id))
        return attempt

    def mark_send_uncertain(self, message_id, attempt):
        with self.db() as db:
            if not db.execute("UPDATE messages SET state='uncertain' WHERE id=? AND attempt=? AND state='attempting'", (message_id, attempt)).rowcount:
                raise Conflict("No matching active send attempt")

    def confirm_sent(self, message_id, attempt, observed, sent_record_id):
        if not sent_record_id or not isinstance(sent_record_id, str):
            raise ValueError("An independently observed Sent record is required")
        with self.db() as db:
            db.execute("BEGIN IMMEDIATE")
            row = self._match(db, message_id, observed)
            if row["attempt"] != attempt or row["state"] not in {"attempting", "uncertain", "sent"}:
                raise Conflict("No matching send attempt to reconcile")
            evidence = encoded({"sent_record_id": sent_record_id, "observed": observed})
            if row["state"] == "sent" and row["evidence"] != evidence:
                raise Conflict("Conflicting Sent evidence")
            db.execute("UPDATE messages SET state='sent',evidence=? WHERE id=?", (evidence, message_id))

    def counts(self):
        with self.db() as db:
            return {"imported_rows": db.execute("SELECT COUNT(*) FROM rows").fetchone()[0],
                    "jobs": {r[0]: r[1] for r in db.execute("SELECT state,COUNT(*) FROM jobs GROUP BY state")},
                    "messages": {r[0]: r[1] for r in db.execute("SELECT state,COUNT(*) FROM messages GROUP BY state")}}


def verify():
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="outreach-offline-") as directory:
        path = Path(directory) / "pilot.sqlite"
        pilot = Pilot(path)
        source = io.StringIO(newline="")
        writer = csv.writer(source)
        writer.writerow(["company", "website", "email", "phone"])
        writer.writerows((f"Synthetic Business {n}", f"https://company{n}.example", "", "") for n in range(5000))
        imported = pilot.import_rows(source.getvalue().encode())
        pilot.import_rows(source.getvalue().encode())
        messages = []
        for n in range(10):
            pilot.add_profile(f"profile-{n}", f"sender{n}@mail.example")
        for n in range(200):
            observed = {"profile": f"profile-{n % 10}", "sender": f"sender{n % 10}@mail.example",
                        "recipient": f"prospect{n}@company.example", "subject": f"Synthetic test {n}", "body": f"Offline fixture {n}; never send."}
            mid = pilot.plan_message("offline-only", observed["recipient"], observed["profile"], observed["subject"], observed["body"])
            messages.append((mid, observed))
        first, observation = messages[0]
        attempt = pilot.begin_send(first, observation)
        pilot = Pilot(path)  # crash/restart with an unresolved external action
        blocked = False
        try:
            pilot.begin_send(first, observation)
        except Conflict:
            blocked = True
        if not blocked:
            raise AssertionError("Interrupted send was replayable")
        pilot.confirm_sent(first, attempt, observation, "synthetic-sent-evidence-0")
        for index, (mid, observation) in enumerate(messages[1:], 1):
            attempt = pilot.begin_send(mid, observation)
            pilot.confirm_sent(mid, attempt, observation, f"synthetic-sent-evidence-{index}")
        pilot.reserve("synthetic-10", GLM, {"offline": 1}, 10)
        pilot.reserve("synthetic-20", LUNA_BATCH, {"offline": 2}, 10)
        ceiling_blocked = False
        try:
            pilot.reserve("synthetic-over", JEV, {"offline": 3}, "0.000000001")
        except BudgetExceeded:
            ceiling_blocked = True
        if not ceiling_blocked:
            raise AssertionError("Ceiling was exceeded")
        counts = pilot.counts()
        assert counts["imported_rows"] == imported["rows"] == 5000
        assert counts["messages"] == {"sent": 200}
        return {"mode": "offline_simulation", "paid_model_calls": 0, "actual_model_spend_usd": 0,
                "emails_actually_sent": 0, "rows_actually_enriched": 0,
                "synthetic_rows_imported": counts["imported_rows"], "reimport_added_duplicates": False,
                "synthetic_send_records_reconciled": 200, "synthetic_sender_profiles": 10,
                "interrupted_send_replay_blocked": blocked, "simulated_budget_ceiling_enforced": ceiling_blocked,
                "simulated_budget": pilot.budget(), "elapsed_seconds": round(time.perf_counter()-started, 3),
                "remaining_live_work": ["guarded Jev action gateway", "GLM and Luna Batch clients",
                                        "browser profile isolation and Gmail adapter", "enrichment worker", "campaign inputs"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("verify", help="Run synthetic offline workflow checks; no external calls")
    check.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = verify()
    output = json.dumps(report, indent=2) + "\n"
    if args.report:
        args.report.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
