from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import tempfile
import unittest

from pilot import BudgetExceeded, Conflict, GLM, JEV, LUNA_BATCH, Pilot, money, route, verify


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "pilot.sqlite"
        self.pilot = Pilot(self.path)

    def fixture(self, recipient="prospect@company.example", campaign="pilot"):
        self.pilot.add_profile("account-1", "sender@business.example")
        observation = {"profile": "account-1", "sender": "sender@business.example", "recipient": recipient,
                       "subject": "A specific subject", "body": "Frozen body"}
        mid = self.pilot.plan_message(campaign, recipient, "account-1", observation["subject"], observation["body"])
        return mid, observation

    def test_routes_preserve_models_and_async_boundary(self):
        self.assertEqual(route("decision")["model"], JEV)
        self.assertEqual(route("writing")["model"], GLM)
        self.assertEqual(route("reasoning", fallback_reason="quality_failed")["model"], LUNA_BATCH)
        self.assertEqual(route("writing", fallback_reason="unavailable")["mode"], "batch")
        with self.assertRaises(ValueError):
            route("decision", fallback_reason="unavailable")

    def test_concurrent_reservations_cannot_overcommit(self):
        def reserve(n):
            try:
                return self.pilot.reserve(str(n), GLM, {"n": n}, 1)["dispatch"]
            except BudgetExceeded:
                return False
        with ThreadPoolExecutor(max_workers=12) as pool:
            outcomes = list(pool.map(reserve, range(40)))
        self.assertEqual(sum(outcomes), 20)
        self.assertEqual(self.pilot.budget()["remaining_usd"], 0)

    def test_uncertain_reservation_survives_restart(self):
        self.pilot.reserve("one", GLM, {"a": 1}, 12)
        self.pilot.uncertain("one")
        other = Pilot(self.path)
        self.assertFalse(other.reserve("one", GLM, {"a": 1}, 12)["dispatch"])
        self.assertTrue(other.budget()["target_reached"])
        with self.assertRaises(BudgetExceeded):
            other.reserve("two", LUNA_BATCH, {}, 9)
        other.settle("one", 1)
        self.assertTrue(other.reserve("two", LUNA_BATCH, {}, 9)["dispatch"])

    def test_call_id_conflicts_and_settlement_are_checked(self):
        self.pilot.reserve("one", GLM, {}, 1)
        with self.assertRaises(Conflict):
            self.pilot.reserve("one", GLM, {"changed": True}, 1)
        self.pilot.settle("one", "0.1")
        self.pilot.settle("one", "0.1")
        with self.assertRaises(Conflict):
            self.pilot.settle("one", "0.2")
        self.assertFalse(self.pilot.reserve("one", GLM, {}, 1)["dispatch"])

    def test_provider_overrun_remains_visible(self):
        self.pilot.reserve("one", GLM, {}, 1)
        self.pilot.settle("one", 21)
        self.assertTrue(self.pilot.budget()["over_ceiling"])
        with self.assertRaises(BudgetExceeded):
            self.pilot.reserve("two", GLM, {}, "0.01")

    def test_invalid_costs_are_rejected(self):
        for value in ["NaN", "Infinity", "-1"]:
            with self.assertRaises(ValueError):
                money(value)
        self.assertEqual(money("0.0000000001"), 1)

    def test_import_preserves_missing_fields_and_duplicate_source_rows(self):
        raw = b"company,email,phone\nExample,,\nExample,,\n"
        first = self.pilot.import_rows(raw)
        self.assertEqual(first, self.pilot.import_rows(raw))
        self.assertEqual(self.pilot.counts()["imported_rows"], 2)
        item = self.pilot.claim("enrich", "worker")
        self.assertEqual(item["payload"]["original"], {"company": "Example", "email": "", "phone": ""})

    def test_bad_csv_rolls_back_without_losing_columns(self):
        for raw in [b"name,name\nA,B\n", b"name,email\nA,a@example.test\nB,b@example.test,extra\n"]:
            with self.assertRaises(ValueError):
                self.pilot.import_rows(raw)
        self.assertEqual(self.pilot.counts()["imported_rows"], 0)

    def test_atomic_claims_and_expired_worker_fencing(self):
        self.pilot.enqueue("lead", "enrich", {"company": "Example"})
        with ThreadPoolExecutor(max_workers=5) as pool:
            claims = list(pool.map(lambda n: self.pilot.claim("enrich", str(n), now=100), range(5)))
        self.assertEqual(sum(c is not None for c in claims), 1)
        item = next(c for c in claims if c)
        self.assertEqual(self.pilot.recover_expired(now=161), 1)
        with self.assertRaises(Conflict):
            self.pilot.complete("lead", item["lease"], {}, now=161)
        self.assertIsNone(self.pilot.claim("enrich", "replacement", now=161))
        self.assertEqual(self.pilot.counts()["jobs"], {"held": 1})

    def test_completed_job_is_not_requeued_by_reimport(self):
        data = b"name,email\nA,\n"
        self.pilot.import_rows(data)
        item = self.pilot.claim("enrich", "worker", now=100)
        self.pilot.complete(item["id"], item["lease"], {"status": "not_found"}, now=101)
        self.pilot.import_rows(data)
        self.assertEqual(self.pilot.counts()["jobs"], {"complete": 1})

    def test_profile_binding_and_message_identity_are_immutable(self):
        mid, observation = self.fixture()
        with self.assertRaises(Conflict):
            self.pilot.add_profile("account-1", "wrong@business.example")
        with self.assertRaises(Conflict):
            self.pilot.add_profile("another", "sender@business.example")
        for key in ["sender", "profile", "recipient", "subject", "body"]:
            with self.assertRaises(Conflict):
                self.pilot.begin_send(mid, {**observation, key: "wrong"})
        with self.assertRaises(Conflict):
            self.pilot.plan_message("pilot", observation["recipient"], "account-1", observation["subject"], "Changed body")

    def test_suppression_is_checked_immediately_before_attempt(self):
        mid, observation = self.fixture()
        self.pilot.suppress("PROSPECT@company.example")
        with self.assertRaises(Conflict):
            self.pilot.begin_send(mid, observation)

    def test_crash_after_attempt_requires_reconciliation(self):
        mid, observation = self.fixture()
        attempt = self.pilot.begin_send(mid, observation)
        restarted = Pilot(self.path)
        with self.assertRaises(Conflict):
            restarted.begin_send(mid, observation)
        restarted.mark_send_uncertain(mid, attempt)
        with self.assertRaises(Conflict):
            restarted.confirm_sent(mid, attempt, {**observation, "recipient": "wrong"}, "record")
        restarted.confirm_sent(mid, attempt, observation, "record")
        restarted.confirm_sent(mid, attempt, observation, "record")
        with self.assertRaises(Conflict):
            restarted.begin_send(mid, observation)
        self.assertEqual(restarted.counts()["messages"], {"sent": 1})

    def test_twenty_send_limit_spans_campaigns(self):
        for n in range(20):
            mid, observation = self.fixture(f"p{n}@company.example", campaign=f"campaign-{n}")
            attempt = self.pilot.begin_send(mid, observation)
            self.pilot.confirm_sent(mid, attempt, observation, f"sent-{n}")
        mid, observation = self.fixture("extra@company.example")
        with self.assertRaises(Conflict):
            self.pilot.begin_send(mid, observation)

    def test_unresolved_attempt_blocks_other_messages_for_that_sender(self):
        mid, observation = self.fixture()
        attempt = self.pilot.begin_send(mid, observation)
        other, other_observation = self.fixture("other@company.example")
        with self.assertRaises(Conflict):
            self.pilot.begin_send(other, other_observation)
        self.pilot.mark_send_uncertain(mid, attempt)
        with self.assertRaises(Conflict):
            self.pilot.begin_send(other, other_observation)
        self.pilot.confirm_sent(mid, attempt, observation, "sent-1")
        self.pilot.begin_send(other, other_observation)

    def test_ten_profile_limit_bounds_total_pilot_volume(self):
        for n in range(10):
            self.pilot.add_profile(str(n), f"s{n}@business.example")
        self.pilot.add_profile("0", "s0@business.example")
        with self.assertRaises(Conflict):
            self.pilot.add_profile("extra", "extra@business.example")

    def test_offline_acceptance_report_does_not_claim_live_results(self):
        report = verify()
        self.assertEqual(report["mode"], "offline_simulation")
        self.assertEqual(report["synthetic_rows_imported"], 5000)
        self.assertEqual(report["synthetic_send_records_reconciled"], 200)
        self.assertEqual(report["emails_actually_sent"], 0)
        self.assertEqual(report["rows_actually_enriched"], 0)
        self.assertEqual(report["paid_model_calls"], 0)
        json.dumps(report, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
