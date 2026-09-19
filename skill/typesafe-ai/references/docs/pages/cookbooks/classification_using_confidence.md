Source: https://docs.typesafe.ai/cookbooks/classification_using_confidence
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Classification using confidence

> Classify SEC annual reports into 75 industry groups with one Choice each, then read the answer's own confidence to decide whether to report that group or the broader division above it.

Every company that files an annual report with the SEC describes its own business in it. We
classify those descriptions under the Standard Industrial Classification: 75 industry
groups, one `Choice` question per document.

Most filings are easy. A regional bank is a regional bank. Some are not: a company that
just sold one of its two segments, or a startup describing a business it plans to enter
rather than one it runs. The model has to pick a group regardless, and the answer for a
hard case looks no different from the answer for an easy one. Telling hard cases from easy
ones is normally where the cost goes: a second model, extra calls, human review.

A Choice already tells you. Alongside the winning option it returns `confidence`, high when
nearly all the probability landed on one option and low when it spread across several. That
one number separates the answers you can trust from the ones you can't.

What to do with an untrusted answer depends on your labels. SIC labels form a hierarchy:
industry groups roll up into broader divisions. That makes one response nearly free. When
the model is unsure of the group, report the division it belongs to. The broad label
follows from the narrow one, so there is no second call.

Across 60 filings, a confidence cutoff of 0.9 splits them in half. The confident half is
right 90% of the time; the other half, 40%. Reported one level up, that 40% becomes 70%. We
end with a `classify()` function that returns a label plus how specific it is, at one
request per document.

```mermaid theme={null}
flowchart LR
    doc["Item 1 'Business'<br/>from one 10-K"]

    subgraph request["one request"]
        q["Choice<br/>75 industry groups"]
    end

    sureconfidence<br/>≥ 0.9?
    grp["report the industry group<br/><i>e.g. 28</i>"]
    div["report its division<br/><i>e.g. manufacturing</i>"]

    doc --> request --> sure
    %% both branches leave the test, so they share a rank and stack on their own
    sure -- "yes" --> grp
    sure -- "no" --> div
```

## Setup

```bash theme={null}
pip install ipython matplotlib "typesafe-sdk>=0.5.7" cooksafe --extra-index-url https://pypi.typesafe.ai/
```

then set `TYPESAFE_API_KEY`. Every API call is cached to `json_cache.json`, which ships
with the cookbook, so re-rendering replays the published numbers without calling the API.
Delete that file to re-run everything live.

Numbers below came from `jev-1.12` on 2026-08-12.

```python theme={null}
import json
from collections import defaultdict
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from cooksafe import JsonCache, make_playground_link
from IPython.display import Markdown, display
from typesafe_sdk import Choice, TypeSafeClient

matplotlib.use("Agg")  # headless render

import os  # noqa: E402

TYPESAFE_MODEL = "jev-1.12"
CONFIDENT = 0.9  # above this the group is reported; below it, the division

client = TypeSafeClient(
    api_key=os.environ.get(
        "TYPESAFE_API_KEY", "cache-only"
    ),  # keyless kernels replay the cache
    base_url=os.environ.get("TYPESAFE_ENDPOINT"),
    timeout=120.0,
)
json_cache = JsonCache(Path("json_cache.json"))
```

## Build the two levels of the taxonomy

`sic_codes.tsv` is the industry list the SEC publishes for filers to pick their own code
from, fetched 2026-08-10: 444 four-digit codes, each with an industry title. The digits are
a hierarchy. The first two are the **major group** (75 of them here, from `01` agricultural
production to `99` non-classifiable), and fixed ranges of major groups make up the ten
**divisions**, the broadest split SIC has.

Both levels come out of that one file with no model involved: group the codes by their
first two digits, then map those digits to a division.

```python expandable theme={null}
DIVISIONS = [
    (1, 9, "agriculture, forestry and fishing"),
    (10, 14, "mining"),
    (15, 17, "construction"),
    (20, 39, "manufacturing"),
    (40, 49, "transportation, communications and utilities"),
    (50, 51, "wholesale trade"),
    (52, 59, "retail trade"),
    (60, 67, "finance, insurance and real estate"),
    (70, 89, "services"),
    (91, 99, "public administration"),
]

INDUSTRIES: dict[str, str] = {}
for line in Path("sic_codes.tsv").read_text().splitlines()[1:]:
    code, _office, title = line.split("\t")
    INDUSTRIES[code] = title.lower()

GROUPS: dict[str, list[str]] = defaultdict(list)
for code in sorted(INDUSTRIES):
    GROUPS[code[:2]].append(code)


def division(group: str) -> str:
    number = int(group)
    return next(name for low, high, name in DIVISIONS if low <= number <= high)


print(
    f"{len(INDUSTRIES)} industries -> {len(GROUPS)} major groups -> {len(DIVISIONS)} divisions"
)
print(
    f"  group 35 = {division('35')} / {', '.join(INDUSTRIES[c] for c in GROUPS['35'][:3])} ..."
)
```

```
444 industries -> 75 major groups -> 10 divisions
  group 35 = manufacturing / engines & turbines, farm machinery & equipment, lawn & garden tractors & home lawn & gardens equip ...
```

A Choice question needs something to describe each option, and a group's own name is not
always
there: 42 of the 75 carry an umbrella title in the SEC's list, and the rest carry none. So
each group is described by the industries inside it, which is what someone reading the
filing would match against anyway.

```python theme={null}
MAX_NAMED = (
    8  # industries listed per group; enough to characterise it without a wall of text
)


def describe(group: str) -> str:
    umbrella = INDUSTRIES.get(f"{group}00")
    inside = [INDUSTRIES[c] for c in GROUPS[group] if c != f"{group}00"][:MAX_NAMED]
    listed = "; ".join(inside)
    return (
        f"{umbrella} — includes: {listed}"
        if umbrella and listed
        else (umbrella or listed)
    )


print(f"group 20: {describe('20')[:150]}")
print(f"\ngroup 65: {describe('65')[:150]}")
```

```
group 20: food and kindred products — includes: meat packing plants; sausages & other prepared meat products; poultry slaughtering and processing; dairy product

group 65: real estate — includes: real estate operators (no developers) & lessors; operators of nonresidential buildings; operators of apartment buildings; less
```

## The filings

`filings.jsonl` holds 60 annual reports (10-K), each trimmed to Item 1 "Business", the
section where a company describes what it does, which is the only part an industry code is
about. They span 1993–2024 and run from 700 to 2,200 words. Each one carries the SIC code
its filer chose, plus the accession number to look it up on EDGAR.

Where that label comes from matters before any accuracy number. It is self-reported:
whoever prepared the filing picked it once, and it goes stale when a company sells the
business the code names and keeps the code. These 60 were filtered down to filings whose
own text supports the code they carry, so the numbers here measure the recipe rather than
the state of EDGAR's metadata.

```python theme={null}
FILINGS = [json.loads(line) for line in Path("filings.jsonl").read_text().splitlines()]
example = FILINGS[7]
print(
    f"{len(FILINGS)} filings, {sum(f['words'] for f in FILINGS) // len(FILINGS)} words on average"
)
print(f"\n{example['id']} (filed {example['year']}, accession {example['accession']}):")
print(f"  {example['text'][:230]}...")
print(f"  filer's code: {example['sic']} {INDUSTRIES[example['sic']]}")
```

```
60 filings, 1438 words on average

1389870_2008 (filed 2008, accession 0001079974-09-000155):
  Item 1. DESCRIPTION OF BUSINESS. NARRATIVE DESCRIPTION OF THE BUSINESS Across America Financial Services, Inc. is a corporation which was formed under the laws of the State of Colorado on December 1, 2005. Until March 23, 2007, we...
  filer's code: 6163 loan brokers
```

## Ask one Choice question, and read the confidence

One `Choice` question whose options are the 75 groups. The whole taxonomy fits in one
request: a Choice works reliably up to roughly 240 options, and 75 is well inside that.

The answer comes back with `choice`, the winning group; `probabilities`, the weight on each
of the 75; and `confidence`, which says how concentrated that spread was. The recipe reads
`confidence` rather than the winner's own probability. A winner at 0.45 with a runner-up at
0.44, and a winner at 0.45 with the rest of the weight scattered thinly, are different
situations, and `confidence` is what separates them.

```python theme={null}
QUESTION = (
    "Which broad industry does this company operate in? Judge the company's own operations "
    "as this filing describes them."
)


def questions() -> dict:
    return {
        "group": Choice(
            instructions=QUESTION,
            criteria={group: describe(group) for group in sorted(GROUPS)},
        )
    }


@json_cache
def ask(filing_id: str, text: str) -> dict:
    response = client.system_one(
        state=text, questions=questions(), model=TYPESAFE_MODEL
    )
    answer = response.answers["group"]
    return {
        "group": answer.choice,
        "confidence": answer.confidence,
        "probabilities": dict(answer.probabilities),
    }
```

## Return the group when sure, its division when not

The four lines below are the whole recipe. At 0.9 confidence or above, the answer is
reported as an industry group; below that, the same answer is reported as the division that
group sits in.

Every filing still comes back with a usable label. One the model could not classify
confidently comes back one level up instead of being dropped or sent on. If a division is
too coarse for your application to act on, this branch is where you hand it to a person.

```python theme={null}
def classify(filing: dict) -> dict:
    answer = ask(filing["id"], filing["text"])
    sure = answer["confidence"] >= CONFIDENT
    return {
        "level": "group" if sure else "division",
        "label": answer["group"] if sure else division(answer["group"]),
        "confidence": answer["confidence"],
        "group": answer["group"],
    }


def show(filing: dict) -> None:
    result = classify(filing)
    named = describe(result["group"]).split(" — ")[0][:46]
    print(
        f"  {filing['id']:>13}  conf {result['confidence']:.2f}  -> {result['level']:<8} "
        f"{result['label']:<14} (group {result['group']}: {named})"
    )


print("three filings the model was sure about:")
for f in sorted(FILINGS, key=lambda f: -ask(f["id"], f["text"])["confidence"])[:3]:
    show(f)
print("\nthree it was not:")
for f in sorted(FILINGS, key=lambda f: ask(f["id"], f["text"])["confidence"])[:3]:
    show(f)
```

```
three filings the model was sure about:
    310158_1996  conf 1.00  -> group    28             (group 28: chemicals & allied products)
     33416_1998  conf 1.00  -> group    63             (group 63: life insurance; accident & health insurance; h)
    352541_1996  conf 1.00  -> group    49             (group 49: electric, gas & sanitary services)

three it was not:
   1372167_2013  conf 0.22  -> division manufacturing  (group 38: search, detection, navagation, guidance, aeron)
   1398633_2009  conf 0.23  -> division wholesale trade (group 50: wholesale-durable goods)
     46653_1999  conf 0.29  -> division services       (group 87: services-engineering, accounting, research, ma)
```

The confidences line up with how hard each filing is to classify. The three at 1.00 are a
pharmaceutical maker, a life insurer and a utility; all three are holding companies on
paper, but each has one dominant business the filing names outright. The three at the
bottom are harder for reasons you can read in the text. Two are development-stage companies
describing a business they intend to start (Nevaeh "intends to operate as a software
developer", Barricode was "organized to enter into the computer security software
industry"), and the third had two segments and sold one of them weeks before filing. Those
three come back as a division rather than a group.

`classify()` is the whole recipe. Point `ask()` at your own documents and rewrite
`describe()` for your own taxonomy, and the rest carries over.

## What the broader answer buys

All 60 filings, scored against the code each filer chose, under both policies: name a group
every time, or report the division whenever confidence lands under 0.9.

```python theme={null}
def correct(filing: dict, result: dict) -> bool:
    gold_group = filing["sic"][:2]
    if result["level"] == "group":
        return result["label"] == gold_group
    return result["label"] == division(gold_group)


results = [(f, classify(f)) for f in FILINGS]
sure = [(f, r) for f, r in results if r["level"] == "group"]
unsure = [(f, r) for f, r in results if r["level"] == "division"]

forced = sum(r["group"] == f["sic"][:2] for f, r in results)
broadened = sum(correct(f, r) for f, r in results)

print(f"forced to name a group every time      {forced}/{len(results)} right")
print(
    f"  of those, the {len(sure)} it was sure about  "
    f"{sum(r['group'] == f['sic'][:2] for f, r in sure)}/{len(sure)} right"
)
print(
    f"  and the {len(unsure)} it was not           "
    f"{sum(r['group'] == f['sic'][:2] for f, r in unsure)}/{len(unsure)} right"
)
print(
    f"\nletting it answer coarsely when unsure  {broadened}/{len(results)} useful answers"
)
```

```
forced to name a group every time      39/60 right
  of those, the 30 it was sure about  27/30 right
  and the 30 it was not           12/30 right

letting it answer coarsely when unsure  48/60 useful answers
```

Where the model was sure, the group it named is right nine times in ten. Where it was not,
naming a group was wrong more often than right, at 40%. Reporting those same answers as a
division takes them to 70%.

The chart puts the two policies side by side, split by whether the model was sure.

```python expandable theme={null}
labels = ["sure\n(group reported)", "unsure\n(division reported)"]
forced_split = [
    sum(r["group"] == f["sic"][:2] for f, r in sure) / len(sure),
    sum(r["group"] == f["sic"][:2] for f, r in unsure) / len(unsure),
]
broad_split = [
    sum(correct(f, r) for f, r in sure) / len(sure),
    sum(correct(f, r) for f, r in unsure) / len(unsure),
]

fig, ax = plt.subplots(figsize=(7, 3.6))
x = range(len(labels))
ax.bar(
    [i - 0.19 for i in x],
    forced_split,
    0.38,
    label="always name a group",
    color="#c8ccd4",
)
ax.bar(
    [i + 0.19 for i in x],
    broad_split,
    0.38,
    label="answer broadly when unsure",
    color="#3b6ea5",
)
for i, (a, b) in enumerate(zip(forced_split, broad_split)):
    ax.text(i - 0.19, a + 0.02, f"{a:.0%}", ha="center", fontsize=9)
    ax.text(i + 0.19, b + 0.02, f"{b:.0%}", ha="center", fontsize=9)
ax.set_xticks(list(x))
ax.set_xticklabels(
    [f"{lab}\nn={n}" for lab, n in zip(labels, [len(sure), len(unsure)])]
)
ax.set_ylabel("labels that are right")
ax.set_ylim(0, 1.12)
ax.set_title("Where the broader answer helps: the filings it was unsure about")
ax.legend(frameon=False, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
display(fig)
```

<img src="https://mintcdn.com/ts-docs/teQYilPCKt0TpDJJ/cookbooks/classification_using_confidence/classification_using_confidence.executed.1.png?fit=max&auto=format&n=teQYilPCKt0TpDJJ&q=85&s=e75ad9c2e17cae7094f30cd0cbb36f53" alt="output" width="1034" height="523" data-path="cookbooks/classification_using_confidence/classification_using_confidence.executed.1.png" />

## Open it in the playground

This share link holds one filing and the 75-option question, so you can see the
distribution and the confidence it produces without writing any code.

```python theme={null}
playground_link = make_playground_link(
    example["text"], questions(), models=[TYPESAFE_MODEL]
)
display(
    Markdown(
        f"🔗 [Open the filing + question in the TypeSafe playground]({playground_link})"
    )
)
```

Open the filing + question in the TypeSafe playground →
