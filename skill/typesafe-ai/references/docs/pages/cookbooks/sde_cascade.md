Source: https://docs.typesafe.ai/cookbooks/sde_cascade
Retrieved: 2026-09-17T22:21:37.872885+00:00

# SDE cascade

> Uses a 2-stage structured-data-extraction cascade (mini → verify → reasoning) to get most of the quality of a big reasoning model at a fraction of the cost.

* Overview
  * big reasoning models extract structured data well, but are slow and expensive
  * small models are cheap, but make mistakes
  * a *cascade* gets most of the quality at a fraction of the cost
  * the models we use, and their price (\$ per 1M tokens, input / output; model ids + prices
    as of 2026-07, see README):
    * rung 0 (mini): `gpt-5.4-mini` at \$0.75 / \$4.50
    * rung 1 (reasoning): `gpt-5.5` at \$5.00 / \$30.00 (roughly 7x the mini)
    * verifier: TypeSafe `jev-1.12` at \$0.042 / \$0.00 (flat, far cheaper than a rung-1
      call)
* Algorithm
  1. **Extract** with a cheap/small model.
  2. **Verify** with **TypeSafe** primitives: a per-field yes/no ("Noul question")
     question
     * (e.g. "is this value absent from the source?", "was it lifted from unrelated
       text?"), each returning P(something is wrong).
  3. **Escalate** to an expensive reasoning model if a verifier signal fires; otherwise
     keep the cheap answer.
* This Cookbook
  * walks one real example end-to-end, then shows the tradeoff across 100 prompts
  * note: the two extraction rungs use text-mode OpenAI
  * we do *not* use structured outputs, tool calls, or json mode, because:
    * a *schema following* mistake is not the mistake we expect an LLM to make (it's
      easy
      to make synthetic data for this)
    * if an LLM does fail to follow the schema, it's almost always very confused, so
      constrained decoding doesn't fix the underlying issue
    * we encourage you to try them though!

## Setup

* install the dependencies (the TypeSafe verifier client is served from TypeSafe's package
  index):

```bash theme={null}
pip install openai datasets jsonschema ipython "typesafe-sdk>=0.5.7" cooksafe --extra-index-url https://pypi.typesafe.ai/
```

* then set `OPENAI_API_KEY` and `TYPESAFE_API_KEY` in your environment

```python theme={null}
import json
import os
from pathlib import Path

import jsonschema
from cooksafe import JsonCache, make_playground_link
from datasets import load_dataset
from IPython.display import Markdown, display
from openai import OpenAI
from typesafe_sdk import Noul, NoulCriteria, TypeSafeClient

MINI = "gpt-5.4-mini"  # rung 0: cheap + fast
REASONING = "gpt-5.5"  # rung 1: strong, run with reasoning_effort="high"
TS_MODEL = "jev-1.12"  # the TypeSafe verifier model
FIRE_T = 0.7  # escalate if any per-field P(wrong) exceeds this; also the "<== FIRES" display marker

oai = OpenAI()

ts = TypeSafeClient(api_key=os.environ["TYPESAFE_API_KEY"], timeout=30.0)
```

## Step 1: the data

We choose a huggingface dataset called scrapegraphai

```python theme={null}
SCRAPEGRAPHAI_REVISION = "4bb9fba1dff9181c5acdb60a5a26fea62fa54fe9"
row = load_dataset(
    "scrapegraphai/scrapegraphai-100k",
    revision=SCRAPEGRAPHAI_REVISION,
    split="train",
)[516]
schema = json.loads(row["schema"])
prompt = row["prompt"]
content = row["content"]

print(
    f"""
PROMPT
===========
{prompt}

SCHEMA
===========
{json.dumps(schema, indent=2)}

CONTENT
===========
{content}
""".strip()
)
```

```text expandable theme={null}
PROMPT
===========
Find registration open date fall semester for New York University in New York, NY for the 2024-2025 school year.

SCHEMA
===========
{
  "properties": {
    "registration_open_date": {
      "description": "The date that registration opens for the fall semester. MUST be in the format mm/dd/yyyy. For example, for a college in the 2024-2025 school year, it might be something like 09/05/2024. Return a blank string if you are unsure.",
      "title": "Registration Open Date",
      "type": "string"
    },
    "description": {
      "description": "A brief description of the registration open date. For example, 'Registration opens for the fall semester'.",
      "title": "Description",
      "type": "string"
    }
  },
  "required": [
    "registration_open_date",
    "description"
  ],
  "title": "RegistrationOpen",
  "type": "object"
}

CONTENT
===========
Skip to content Skip to current page navigation

[ ](https://www.nyu.edu/)

Search Site

[ ](https://www.nyu.edu/)

  * [ Academics](https://www.nyu.edu/academics.html)
  * [ Admissions](https://www.nyu.edu/admissions.html)
  * [ Research](https://www.nyu.edu/research.html)
  * [ University Life](https://www.nyu.edu/life.html)
  * [ About](https://www.nyu.edu/about.html)



All NYU

#  Mobile Navigation 

[ ](https://www.nyu.edu/)

Search Site

  * [Academics](https://www.nyu.edu/academics.html)
  * [Admissions](https://www.nyu.edu/admissions.html)
  * [Research](https://www.nyu.edu/research.html)
  * [University Life](https://www.nyu.edu/life.html)
  * [About](https://www.nyu.edu/about.html)



All NYU

Info for

  * Back to main menu
  * Info for 

    * [Students](https://www.nyu.edu/students.html)
    * [Faculty](https://www.nyu.edu/faculty.html)
    * [Alumni](https://www.nyu.edu/alumni.html)
    * [Employees](https://www.nyu.edu/employees.html)
    * [Community](https://www.nyu.edu/community.html)



[Log In](http://home.nyu.edu/)

Info for

  * [Students](https://www.nyu.edu/students.html)
  * [Faculty](https://www.nyu.edu/faculty.html)
  * [Alumni](https://www.nyu.edu/alumni.html)
  * [Employees](https://www.nyu.edu/employees.html)
  * [Community](https://www.nyu.edu/community.html)



[Log In](https://home.nyu.edu/)

Search Site Search

#  Events Calendar 

Search Events 

Apply Reset

  * [About the Events Calendar ](https://www.nyu.edu/employees/resources-and-services/media-and-communications/digital-communications/university-events-calendar.html)
  * [Events Calendar Tutorial ](https://www.nyu.edu/employees/resources-and-services/media-and-communications/digital-communications/university-events-calendar/tutorials.html)
  * [Report issue or provide feedback ](https://nyu.service-now.com/sp?id=sc_cat_item&sys_id=7698dd2a98bcf4004c8c03063d84e274)



Search Filters Calendar

New York University 

Equal Opportunity and Non-Discrimination at NYU - New York University is committed to maintaining an environment that encourages and fosters respect for individual values and appropriate conduct among all persons. In all University spaces--physical and digital--programming, activities, and events are carried out in accordance with applicable law as well as University policy, which includes but is not limited to its Non-Discrimination and Anti-Harassment Policy. 

Unless otherwise noted, all content copyright New York University. All rights reserved. 

  * [Search](https://search.nyu.edu/)
  * [Campus Map](https://www.nyu.edu/map.html)
  * [Events](https://events.nyu.edu/)
  * [Contact Us](https://www.nyu.edu/contact-us.html)
  * [Give](https://www.nyu.edu/about/giving.html)
  * [Copyright & Fair Use](https://www.nyu.edu/copyright-and-fair-use.html)
  * [Privacy](https://www.nyu.edu/privacy.html)
  * [Accessibility](https://www.nyu.edu/accessibility.html)
  * [Feedback](https://www.nyu.edu/#feedback.html)



  * [New York Campus](https://www.nyu.edu/)
  * [Abu Dhabi Campus](https://nyuad.nyu.edu/)
  * [Shanghai Campus](https://shanghai.nyu.edu/)



  * [![](https://events.nyu.edu/live/resource/image/_i/themes/global/images/icons/facebook.rev.1773448757.svg)](https://facebook.com/)
  * [![](https://events.nyu.edu/live/resource/image/_i/themes/global/images/icons/linkedin.rev.1773448758.svg)](https://linkedin.com/)
  * [![](https://events.nyu.edu/live/resource/image/_i/themes/global/images/icons/x.rev.1773448757.svg)](https://x.com/)
  * [![](https://events.nyu.edu/live/resource/image/_i/themes/global/images/icons/instagram.rev.1773448757.svg)](https://instagram.com/)
  * [![](https://events.nyu.edu/live/resource/image/_i/themes/global/images/icons/youtube.rev.1773448758.svg)](https://youtube.com/)
```

* This row is an **NYU events-calendar page** ("Fall 2024 Census Date"):
  * the schema asks for just two fields: `registration_open_date` and `description`
  * the prompt scrape captured only calendar nav and boilerplate: **there is no
    registration date, or description**
  * note the schema's `description` field even ships an *example* value ("Registration
    opens for the fall semester") in its own field description
* so a well-behaved extractor should *decline* to invent the fields the page doesn't
  contain
* let's see if the small model does the right thing!

## Step 2: extract with the mini model (text mode)

* note: `gpt-5.4-mini` is very stochastic on this input -- even at `temperature=0` it
  invents a different `description` on nearly every run. For a reproducible walkthrough we
  **hard-code** the one canonical fabrication the rest of this notebook explains (and that
  the verifier flags at P(wrong) > 0.8). A real pipeline would just take `extract(MINI,
  prompt, schema, content, temperature=0)` directly.

```python expandable theme={null}
EXTRACT_SYSTEM = (
    "You extract structured data from documents. Return only values supported by the text. "
    "Follow any value format specified by the schema or its field descriptions."
)


# LLM and TypeSafe calls are cached to ``json_cache.json``, which ships with the cookbook, so
# re-rendering reproduces the published results with no API spend; delete the file to re-run live.
json_cache = JsonCache(Path("json_cache.json"))


@json_cache
def extract(
    model: str,
    prompt: str,
    schema: dict,
    content: str,
    *,
    reasoning_effort: str | None = None,
    temperature: float | None = None,
) -> dict:
    user = (
        f"{prompt}\n\nReturn ONLY a JSON object matching this JSON Schema:\n"
        f"{json.dumps(schema, indent=2)}\n\nDocument:\n{content}"
    )
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": EXTRACT_SYSTEM},
            {"role": "user", "content": user},
        ],
    }
    if reasoning_effort:
        kwargs["reasoning_effort"] = reasoning_effort
    if temperature is not None:
        kwargs["temperature"] = temperature
    text = oai.chat.completions.create(**kwargs).choices[0].message.content
    # The prompt asks for ONLY a JSON object, so parse the reply as-is -- no regex fishing a
    # substring out of a malformed reply. If ``json.loads`` fails, treat it as an empty extraction
    # (the record-level analog of NaN): every field reads as absent, which the verifier flags and the
    # gate escalates -- the safe direction. Schema-following errors are rare here (see the overview).
    try:
        return json.loads(text)
    except (ValueError, json.JSONDecodeError):
        return {}


# Hard-coded canonical fabrication (see note above); a real pipeline would use extract(MINI, prompt, schema, content, temperature=0).
mini_record = {
    "registration_open_date": "",
    "description": "Registration opens for the fall semester",
}
print("mini extraction:\n", json.dumps(mini_record, indent=2))

# The record is a perfect fit for the JSON Schema -- and still wrong. Schema validation is necessary
# but not sufficient: it catches structural errors, never semantic ones. That gap is the whole point.
print("\nschema-valid:", jsonschema.Draft202012Validator(schema).is_valid(mini_record))
```

```
mini extraction:
 {
  "registration_open_date": "",
  "description": "Registration opens for the fall semester"
}

schema-valid: True
```

* The record is **schema-valid** (the line above prints `True`), yet it's wrong:
  * `registration_open_date` is left blank, which matches the page: it states no date
  * but `description` is fabricated: the page never describes a registration date, so
    mini invents a plausible one. It may parrot the schema's own example, "Registration
    opens for the fall semester", or narrate "...was not found in the document"
  * a JSON-Schema check can't see this. A cheap model produces confident,
    schema-satisfying fabrications of this kind, and catching them is the job of a
    semantic verifier

## Step 3: verify with TypeSafe

* the verifier is **TypeSafe**; for each field we build a `Noul` question:
  * a narrow yes/no, framed so that `true` = something is wrong (escalate)
* TypeSafe returns a calibrated `noul` = `P(true)` per question, in one system\_one call
* the question set:
  * one holistic **`__overall__::judge`** head ("should this record be escalated?"). We
    compute and display it to contrast a whole-record judgment with the per-field heads,
    but the gate in Step 4 does **not** use it -- escalation is driven by the per-field
    battery.
  * a per-field battery
    * non-empty fields get the full set of heads
    * empty fields (null / "" / \[]) get only the `absence_wrong` head
  * (the full pipeline also has a `spurious` head for whole containers and an overall
    `difficulty` score; not shown here, to keep this walkthrough to the two gating heads)
* **The TypeSafe Way: Decomposition**
  * Notice how everything is *programmatically decomposed*, this is TypeSafe way.
  * Decomposition maximizes the intelligence of every prompt, and makes the algorithm
    tunable and interpretable.
  * <img src="https://mintcdn.com/ts-docs/2NirYCl-v96cw05F/cookbooks/sde_cascade/this_is_the_way.jpg?fit=max&auto=format&n=2NirYCl-v96cw05F&q=85&s=10bd7d99dc5f679022bb6763dde57330" alt="this is the way" width="100" height="56" data-path="cookbooks/sde_cascade/this_is_the_way.jpg" />

```python expandable theme={null}
# metric -> (question, NoulCriteria)
MAIN_QUESTIONS = {
    "name_desc_mismatch": (
        "Does the `extracted_field` fail to match the field at `path` or the `description` in the "
        "`field_spec`? If the `description` is empty, judge against the `path` alone.",
        NoulCriteria(
            true="the `extracted_field` does not match the field name or its `description`",
            false="the `extracted_field` matches the field name and `description`",
        ),
    ),
    "type_mismatch": (
        "Does the `extracted_field` violate the `type` declared in the `field_spec`?",
        NoulCriteria(
            true="the `extracted_field` violates the declared `type`",
            false="the `extracted_field` conforms to the declared `type`",
        ),
    ),
    "unreasonable": (
        "Is the `extracted_field` one that a reasonable person would not have extracted for this "
        "`field_spec`?",
        NoulCriteria(
            true="a reasonable person would not have extracted this value",
            false="the extraction is reasonable",
        ),
    ),
    "hallucinated": (
        "Is the `extracted_field` unsupported by, or absent from, the source text?",
        NoulCriteria(
            true="the `extracted_field` is a hallucination -- not supported by, or absent "
            "from, the source text",
            false="the `extracted_field` is supported by the source text",
        ),
    ),
    "off_target": (
        "Does the source text fail to genuinely report the thing the `field_spec` describes, so the "
        "value was pulled from incidental text?",
        NoulCriteria(
            true="the source does not genuinely provide this field -- the value was pulled "
            "from incidental text",
            false="the source genuinely reports this field",
        ),
    ),
    "incomplete": (
        "Does the `extracted_field` fail to capture a value the source supports (note whether the "
        "`field_spec` is `required`)?",
        NoulCriteria(
            true="the field is wrongly empty, null, or missing a value the source supports",
            false="the field captures the value the source supports",
        ),
    ),
    "format_violation": (
        "Does the `extracted_field` violate the format or constraints implied by the `description`, "
        "the schema `type`, and the extraction instructions (e.g. date format, units, enum membership)?",
        NoulCriteria(
            true="the `extracted_field` violates the implied format or constraints",
            false="the `extracted_field` satisfies the format and constraints",
        ),
    ),
}
ABSENCE_QUESTION = (
    "The `extracted_field` is empty, null, or an empty collection. Does the source text contain the "
    "information the `field_spec` describes, making the empty result wrong?"
)
ABSENCE_CRITERIA = NoulCriteria(
    true="a value was wrongly omitted", false="returning nothing is correct"
)

# The pipeline also asks one holistic, whole-record head: "should this be escalated?"
OVERALL_JUDGE = (
    "Is this extracted record an incorrect extraction -- some value unsupported by the source or "
    "not conforming to the schema, required information missing or wrong, or some field hallucinated -- "
    "so it should be escalated to a smarter model?"
)
OVERALL_JUDGE_CRITERIA = NoulCriteria(
    true="the record is an incorrect extraction",
    false="the record is a correct extraction",
)


def is_empty(v) -> bool:
    return v is None or (isinstance(v, (str, list, dict)) and len(v) == 0)


def field_spec(name: str) -> dict:
    """Minimal spec pulled from the schema (unwrapping anyOf/null for optional fields)."""
    p = schema["properties"][name]
    branches = p.get("anyOf") or []
    typ = p.get("type") or next(
        (b["type"] for b in branches if b.get("type") != "null"), "unknown"
    )
    return {
        "path": name,
        "type": typ,
        "description": p.get("description", ""),
        "required": name in schema.get("required", []),
    }


def build_questions(record: dict) -> dict[str, Noul]:
    """The verify question set: one holistic ``__overall__::judge`` head plus a per-field battery,
    keyed ``field::metric`` (mirrors build_verify_prompts)."""
    questions: dict[str, Noul] = {
        "__overall__::judge": Noul(
            instructions=OVERALL_JUDGE, criteria=OVERALL_JUDGE_CRITERIA
        ),
    }
    for name, value in record.items():
        spec = field_spec(name)
        if is_empty(value):
            questions[f"{name}::absence_wrong"] = Noul(
                instructions={
                    "field_spec": spec,
                    "extracted_field": value,
                    "main_question": ABSENCE_QUESTION,
                },
                criteria=ABSENCE_CRITERIA,
            )
            continue
        for metric, (question, criteria) in MAIN_QUESTIONS.items():
            if metric == "type_mismatch" and spec["type"] == "unknown":
                continue
            questions[f"{name}::{metric}"] = Noul(
                instructions={
                    "field_spec": spec,
                    "extracted_field": value,
                    "main_question": question,
                },
                criteria=criteria,
            )
    return questions


@json_cache
def verify(record: dict) -> dict[str, float | str]:
    """Run the whole Noul battery over a record in one TypeSafe call; return ``{field::metric: P(true)}``."""
    state = {
        "system_message": EXTRACT_SYSTEM,
        "instruction": "Extract the structured record from this document",
        "source_text": row["content"],
        "schema": schema,
        "extraction": record,
    }
    questions = build_questions(record)
    answers = ts.system_one(state=state, questions=questions, model=TS_MODEL).answers
    return {qid: ans.noul for qid, ans in answers.items()} | {
        "playground_link": make_playground_link(state, questions)
    }
```

### Run the whole battery over the mini extraction

```python theme={null}
checks = verify(mini_record)
playground_link = checks.pop("playground_link")
display(
    Markdown(
        f"🔗 [Open this verification in the TypeSafe playground]({playground_link})"
    )
)

print(f"{'qid':<40}{'P(wrong)':>9}")
print("-" * 50)
for fld, p in sorted(checks.items(), key=lambda c: -c[-1]):
    flag = "  <== FIRES" if p > FIRE_T else ""
    print(f"{fld:<40}{p:>9.2f}{flag}")
```

```
qid                                      P(wrong)
--------------------------------------------------
description::hallucinated                    0.95  <== FIRES
description::off_target                      0.85  <== FIRES
description::unreasonable                    0.58
__overall__::judge                           0.56
description::incomplete                      0.16
registration_open_date::absence_wrong        0.14
description::format_violation                0.10
description::name_desc_mismatch              0.08
description::type_mismatch                   0.02
```

Open this verification in the TypeSafe playground →

* TypeSafe concentrates the signal on the fields that are actually wrong.
* Our results are calibrated: high on the field that is wrong, low on the field that is
  correct, medium on a field that looks off without being clearly wrong
* This is what a typesafe verifier buys you over a blunt "is this whole thing good?"
  judge

## Step 4: the escalation gate

* now we gate on **`any_flag`**: escalate if *any* field flag exceeds `FIRE_T` (0.7, set
  above and shared with the `<== FIRES` marker in Step 3)
* this is a `max`-style gate (escalate if *any* field fires), not a mean, so one confident
  red flag is enough instead of being averaged into silence

```python theme={null}
# any_flag is a per-field gate: the holistic __overall__ head is shown above but not part of it
fired = {
    qid: p
    for qid, p in checks.items()
    if not qid.startswith("__overall__") and p > FIRE_T
}
escalate = bool(fired)

print(
    f"any_flag gate (threshold {FIRE_T}): {'ESCALATE' if escalate else 'ACCEPT cheap result'}"
)
for qid, p in sorted(fired.items(), key=lambda c: -c[1]):
    print(f"  fired: {qid}  (P={p:.2f})")
```

```
any_flag gate (threshold 0.7): ESCALATE
  fired: description::hallucinated  (P=0.95)
  fired: description::off_target  (P=0.85)
```

## Step 5: escalate to the reasoning model

Since a signal fired, we pay for the strong model (`gpt-5.5`, `reasoning_effort="high"`)

```python theme={null}
final_record = (
    extract(REASONING, prompt, schema, content, reasoning_effort="high")
    if escalate
    else mini_record
)

print("mini      :", json.dumps(mini_record))
print("reasoning :", json.dumps(final_record))
print("\nfield-level diff (mini -> final):")
for name in mini_record:
    if mini_record[name] != final_record.get(name):
        print(f"  {name}: {mini_record[name]!r}  ->  {final_record.get(name)!r}")
```

```
mini      : {"registration_open_date": "", "description": "Registration opens for the fall semester"}
reasoning : {"description": "", "registration_open_date": ""}

field-level diff (mini -> final):
  description: 'Registration opens for the fall semester'  ->  ''
```

* **The improvement**
  * The reasoning model drops the fabricated `description`, returning `""`
  * It recognized the page never describes a registration date, and declined to invent one
  * The cascade turned a confident, schema-valid fabrication into an honest empty field
  * And it only spent reasoning-model dollars on this one item *because the verifier told
    it to*

## Step 6: what this looks like on 100 prompts

* **These are internal TypeSafe results**, produced with the general method above:
  * the same `extract → verify → escalate` loop, `gpt-5.4-mini → gpt-5.5-reasoning`,
    `any_flag` gate over the per-field heads, run over 100 scrapegraphai prompts
  * each item's cheap-rung extraction is scored by TypeSafe; the gate threshold ("cut") is
    swept 0→1, and every resulting config is plotted in (cost, quality) space

<img src="https://mintcdn.com/ts-docs/2NirYCl-v96cw05F/cookbooks/sde_cascade/pareto_100prompts.png?fit=max&auto=format&n=2NirYCl-v96cw05F&q=85&s=ca6731507e07b501a6627616ba0b767a" alt="internal results: cost/quality frontier over 100 prompts" width="1299" height="655" data-path="cookbooks/sde_cascade/pareto_100prompts.png" />

* how to read it:
  * **black diamonds** = the four models run on their own (cost climbs with capability; the
    strongest, `gpt-5.5-reasoning`, sits top-right at ≈0.81 quality for ≈\$0.10/extraction)
  * **blue points** = the cascade at many gate thresholds; the dashed line is the **pareto
    frontier**
  * the cascade frontier sits **up-and-left of every single model**: sweeping the gate buys
    you most of the top model's quality at a fraction of its cost
  * the cheap rung handles the easy items for near-free, and only the flagged items pay for
    the reasoning model

## Appendix A: what makes a good verifier signal

* the cascade is only as good as its verifier; what separates a useful signal from a
  useless one:
  * **Narrow and grounded.**
    * one checkable yes/no about one field against the source (e.g. "is this value absent
      from the source?"), not a vague "is this extraction good?"
    * vague questions give mushy, uncalibrated scores
  * **Bad = TRUE, with explicit criteria.**
    * frame each question so the *escalate* case is the `true` case, and state what
      `true`/`false` mean
  * **Per-field, then aggregate with `max`.**
    * a per-field flag localizes the error and stays sparse and strong
    * `max` ("any flag fires") ensures one confident red flag escalates, instead of being
      averaged into silence
  * **Independent and cheap.**
    * a dedicated verifier (here, TypeSafe) judging the output catches the extractor's own
      blind spots
    * it has to be cheap, or there are no savings left to capture
  * **Separating / calibrated.**
    * a good signal is high on real errors and low on correct ones, so a single threshold
      cleanly splits accept vs escalate
    * that separation is what pushes the pareto curve up-and-left
