Source: https://docs.typesafe.ai/cookbooks/parallel_questions
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Parallel questions

> Runs a 13-question regulatory briefing over the GDPR Wikipedia article, showing that batching every question into one TypeSafe call is 12.2x cheaper and 10.0x faster with no change in answers.

You have one document and N questions about it. You can send one request with all N
questions, or N requests with one question each. With TypeSafe the answers come out the
same either way: each question is scored on its own against the document, so its answer
doesn't depend on what else is in the request.

To check that, the cookbook asks each question several times both ways - all N in one
request, and one question per request - and compares the run-to-run std dev: how far an
answer moves from one repeat to the next. Whatever noise a question has, it has under
both batching strategies. Batching adds none. Most answers came back identical across all
5 repeats either way, the same value on every call, std dev exactly 0.0.

Cost and speed do change. The document dominates every request. N single-question calls
pay for it N times, in N round trips; the batched call pays once. The bigger the document,
the nearer that saving comes to a full Nx.

The case here is a regulatory briefing. The document is the Wikipedia article on the GDPR
(\~54,000 characters, a document-dominated workload where the document is most of every
request), and a compliance team wants 13 things checked: 8 `Noul` questions, 2 `Choice`
questions, and 3 `Score` questions.

## Setup

```bash theme={null}
pip install ipython "typesafe-sdk>=0.5.7" cooksafe --extra-index-url https://pypi.typesafe.ai/
```

then set `TYPESAFE_API_KEY`.

```python theme={null}
import json
import os
import urllib.request
from pathlib import Path
from statistics import mean, stdev
from time import perf_counter

from cooksafe import JsonCache, make_playground_link
from IPython.display import Markdown, display
from typesafe_sdk import Choice, ChoiceAnswer, Noul, NoulAnswer, Score, TypeSafeClient

TYPESAFE_MODEL = "jev-1.12"
PRICE = (
    0.042,
    0.00,
)  # $ per 1M tokens (input, output); TypeSafe jev-1.12 as of 2026-09, see README
RUNS = 5  # repeats per batching strategy, to estimate each answer's run-to-run std dev
client = TypeSafeClient(api_key=os.environ["TYPESAFE_API_KEY"], timeout=120.0)
json_cache = JsonCache(Path("json_cache.json"))
```

## The document: the Wikipedia article on the GDPR

Fetched as plain text from a pinned revision of the article and cached in `json_cache.json`
next to the API calls, so the document and its numbers stay fixed even as the live
article gets edited.

```python theme={null}
WIKIPEDIA_REVISION = 1363040264  # "General Data Protection Regulation", as of 2026-07


@json_cache
def fetch_article(revision_id: int) -> str:
    url = (
        "https://en.wikipedia.org/w/api.php?action=query&format=json"
        f"&prop=extracts&explaintext=1&revids={revision_id}"
    )
    request = urllib.request.Request(
        url, headers={"User-Agent": "typesafe-cookbook/1.0"}
    )
    with urllib.request.urlopen(request) as response:
        pages = json.loads(response.read())["query"]["pages"]
    return next(iter(pages.values()))["extract"]


DOCUMENT = {
    "source": f"https://en.wikipedia.org/?oldid={WIKIPEDIA_REVISION}",
    "text": fetch_article(WIKIPEDIA_REVISION),
}
print(f"{len(DOCUMENT['text']):,} characters")
display(Markdown(f"📄 [Read the pinned Wikipedia revision]({DOCUMENT['source']})"))
```

```
53,777 characters
```

📄 [Read the pinned Wikipedia revision](https://en.wikipedia.org/?oldid=1363040264)

## The questions: 8 nouls + 2 choices + 3 scores

One number tracked per answer, by type:

* `Noul`: the probability of "yes".
* `Choice`: the max prob, the probability on the picked label. `criteria` maps each
  label to its meaning.
* `Score`: the score normalized to 0-1, the score divided by the top level.
  `criteria` lists the level descriptions, from level 0 up.

```python expandable theme={null}
QUESTIONS = {
    "breach_72h": Noul(
        instructions="Must a personal data breach be reported to the supervisory authority within 72 hours?"
    ),
    "applies_non_eu": Noul(
        instructions="Does the regulation apply to organisations established outside the EU that offer goods or services to people in the EU?"
    ),
    "dpo_all_orgs": Noul(
        instructions="Must every organisation appoint a Data Protection Officer, regardless of what data it processes?"
    ),
    "pre_ticked_consent": Noul(
        instructions="Can valid consent be obtained through pre-ticked boxes or inactivity?"
    ),
    "right_erasure": Noul(
        instructions="Does the regulation grant individuals a right to erasure of their personal data?"
    ),
    "data_portability": Noul(
        instructions="Does the regulation include a right to data portability?"
    ),
    "us_federal_law": Noul(instructions="Is the GDPR a United States federal law?"),
    "criminal_penalties": Noul(
        instructions="Does the GDPR itself impose criminal penalties such as imprisonment?"
    ),
    "instrument_type": Choice(
        instructions="What kind of EU legal instrument is the GDPR?",
        criteria={
            "Regulation": "Directly binding law in all member states, no national implementation needed.",
            "Directive": "Sets goals that member states implement through national law.",
            "Treaty": "An international treaty between states.",
            "Recommendation": "Non-binding guidance.",
        },
    ),
    "max_fine": Choice(
        instructions="What is the maximum administrative fine for the most serious infringements?",
        criteria={
            "TwentyM_or_4pct": "Up to EUR 20 million or 4% of annual worldwide turnover, whichever is greater.",
            "TenM_or_2pct": "Up to EUR 10 million or 2% of annual worldwide turnover, whichever is greater.",
            "FixedCap": "A fixed amount not tied to turnover.",
            "NoFines": "The GDPR provides no administrative fines.",
        },
    ),
    "individual_rights": Score(
        instructions="How strong are the rights the GDPR grants to individuals over their data?",
        criteria=[
            "None: individuals get no rights over their data.",
            "Weak: a right to be informed, but little control.",
            "Moderate: access and correction rights, but limited means to act on them.",
            "Strong: access, erasure, portability, and objection rights, with enforcement behind them.",
        ],
    ),
    "penalty_severity": Score(
        instructions="How severe are the penalties the GDPR provides for non-compliance?",
        criteria=[
            "None: no penalties of any kind.",
            "Symbolic: small fixed fines unlikely to change behavior.",
            "Substantial: fines large enough to matter to most companies.",
            "Severe: fines scaled to global revenue, material even to the largest companies.",
        ],
    ),
    "compliance_burden": Score(
        instructions="How heavy is the compliance burden the GDPR places on organisations?",
        criteria=[
            "Negligible: no meaningful obligations.",
            "Light: a few notices and disclosures.",
            "Moderate: documented processes and some dedicated roles for larger processors.",
            "Heavy: records, impact assessments, officers, and breach procedures for many organisations.",
            "Extreme: obligations so demanding that ordinary organisations cannot fully comply.",
        ],
    ),
}
N = len(QUESTIONS)
METRIC = {  # question type -> the one number we track per answer
    Noul: "p(yes)",
    Choice: "max prob",
    Score: "normalized score",
}
```

## Ask two ways, 5 times each

`ask()` sends any subset of the questions with the document and reduces each answer to its
one tracked number. The document is byte-identical in every call.

Both batching strategies run `RUNS` = 5 times, giving each question 5 answers per strategy,
enough to compare the mean (do the two agree?) and the std dev (does batching add noise?).
Calls are cached to `json_cache.json`, which ships with the cookbook, so re-rendering is
free; delete it to re-run live.

```python expandable theme={null}
@json_cache
def ask(keys: tuple[str, ...], run: int):
    """One TypeSafe call -> ({key: tracked metric}, input_tokens, output_tokens, latency_s);
    ``run`` only forces a distinct live call per repeat."""
    started = perf_counter()
    response = client.system_one(
        state={"article": DOCUMENT},
        questions={key: QUESTIONS[key] for key in keys},
        model=TYPESAFE_MODEL,
    )
    values = {}
    for key in keys:
        answer = response.answers[key]
        if isinstance(answer, NoulAnswer):
            values[key] = answer.noul
        elif isinstance(answer, ChoiceAnswer):
            values[key] = max(answer.probabilities.values())
        else:
            values[key] = answer.score / (len(QUESTIONS[key].criteria) - 1)
    return (
        values,
        response.usage.input_tokens,
        response.usage.output_tokens,
        perf_counter() - started,
    )


def priced(result):
    """({key: metric}, in_tokens, out_tokens, latency) -> ({key: metric}, cost_usd, latency)."""
    values, input_tokens, output_tokens, latency = result
    return values, input_tokens / 1e6 * PRICE[0] + output_tokens / 1e6 * PRICE[1], latency


# Price after cache retrieval, so a price change needs no new calls.
batched = [
    priced(ask(tuple(QUESTIONS), run)) for run in range(RUNS)
]  # all N in one call, x RUNS
singles = [
    {key: priced(ask((key,), run)) for key in QUESTIONS} for run in range(RUNS)
]  # N x 1, x RUNS
```

## Batching doesn't change the answers

Per question: the mean and std dev of its tracked number over the 5 runs, under each
batching strategy. If batching changed the answers, the batched columns would differ from
the single columns. A shifted mean is bias. A larger std dev is noise.

```python theme={null}
print(
    f"{'question':<22}{'metric':<18}{'batched mean':>13}{'single mean':>12}"
    f"{'batched std':>13}{'single std':>12}"
)
for key, question in QUESTIONS.items():
    batched_values = [values[key] for values, _cost, _latency in batched]
    single_values = [singles[run][key][0][key] for run in range(RUNS)]
    print(
        f"{key:<22}{METRIC[type(question)]:<18}{mean(batched_values):>13.3f}"
        f"{mean(single_values):>12.3f}{stdev(batched_values):>13.4f}{stdev(single_values):>12.4f}"
    )
```

```
question              metric             batched mean single mean  batched std  single std
breach_72h            p(yes)                    0.804       0.814       0.0055      0.0055
applies_non_eu        p(yes)                    0.990       0.990       0.0000      0.0000
dpo_all_orgs          p(yes)                    0.030       0.030       0.0000      0.0000
pre_ticked_consent    p(yes)                    0.040       0.040       0.0000      0.0000
right_erasure         p(yes)                    0.990       0.990       0.0000      0.0000
data_portability      p(yes)                    0.990       0.990       0.0000      0.0000
us_federal_law        p(yes)                    0.010       0.010       0.0000      0.0000
criminal_penalties    p(yes)                    0.108       0.108       0.0045      0.0084
instrument_type       max prob                  1.000       1.000       0.0000      0.0000
max_fine              max prob                  1.000       1.000       0.0000      0.0000
individual_rights     normalized score          1.000       1.000       0.0000      0.0000
penalty_severity      normalized score          1.000       1.000       0.0000      0.0000
compliance_burden     normalized score          0.750       0.750       0.0000      0.0000
```

Reading the table by question type:

* Choices, scores, and six of the eight nouls come back identical across the 5 repeats:
  std dev exactly 0.0 under both batching strategies, every batched and single call
  returning the same number. One call with N questions gives the same answers as N calls
  with one question each.
* `breach_72h` and `criminal_penalties` carry a little run-to-run sampling noise, and it's
  the same size under both batching strategies, with the means agreeing to within that
  noise. The noise is a property of the question, not of how you batch: batching neither
  shifts the answer nor adds variance.

Either way, there is no batching effect: no question's answer depends on the 12 other
questions sharing its request.

## The only difference: cost and speed

Same answers, different bill. The \~54,000-character article dominates every request, so:

* Cost: the 13 single-question calls re-send the article 13 times; the batched call sends
  it
  once. This saving holds however you fire the calls.
* Speed: the figure sums the 13 single-call latencies, so it assumes they run one after
  another. Fire them concurrently and the gap shrinks, but the 13x token cost stays.

Token counts and latencies are cached alongside the answers; cost is applied after, and
both are averaged over the 5 runs.

```python theme={null}
batched_cost = mean(cost for _values, cost, _latency in batched)
batched_latency = mean(latency for _values, _cost, latency in batched)
singles_cost = mean(
    sum(singles[run][key][1] for key in QUESTIONS) for run in range(RUNS)
)
singles_latency = mean(
    sum(singles[run][key][2] for key in QUESTIONS) for run in range(RUNS)
)
print(f"{'batching':<24}{'calls':>6}{'cost':>12}{'total time':>12}")
print(
    f"{f'one call, all {N}':<24}{1:>6}{'$' + format(batched_cost, '.6f'):>12}{format(batched_latency, '.2f') + 's':>12}"
)
print(
    f"{f'{N} calls, one each':<24}{N:>6}{'$' + format(singles_cost, '.6f'):>12}{format(singles_latency, '.2f') + 's':>12}"
)
print(
    f"\nbatching: {singles_cost / batched_cost:.1f}x cheaper, {singles_latency / batched_latency:.1f}x faster"
)
```

```
batching                 calls        cost  total time
one call, all 13             1   $0.000497       0.27s
13 calls, one each          13   $0.006090       2.71s

batching: 12.2x cheaper, 10.0x faster
```

## Open it in the TypeSafe playground

The same article and the same 13 questions, packed into a share link. Open it to re-run
the briefing live; the same numbers come back.

```python theme={null}
playground_link = make_playground_link(
    {"article": DOCUMENT}, QUESTIONS, models=[TYPESAFE_MODEL]
)
display(
    Markdown(
        f"🔗 [Open this article + questions in the TypeSafe playground]({playground_link})"
    )
)
```

Open this article + questions in the TypeSafe playground →
