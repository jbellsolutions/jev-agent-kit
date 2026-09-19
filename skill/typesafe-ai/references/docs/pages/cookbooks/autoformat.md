Source: https://docs.typesafe.ai/cookbooks/autoformat
Retrieved: 2026-09-17T22:21:37.872885+00:00

# Structure recovery

> Reconstructs Markdown from plain text that lost its formatting in two requests: one stitches hard-wrapped lines back together, one classifies every block (heading, list, code, callout) with companion questions read only when relevant.

This cookbook takes plain text whose markup has been stripped (lines hard-wrapped
mid-sentence, no heading markers, no list bullets) and reconstructs the structure as
Markdown: headings, paragraphs, lists, quotes, code, callouts. The input is a team memo
in exactly that state.

A text-generation model could rewrite the text into Markdown, but a rewrite can also
change the words. Here the model never generates text: it answers narrow questions about
the document (*does this line pick up mid-sentence? what kind of content is this
block?*), and code does the rendering, so every character of the output comes from the
input, and every judgment carries a probability.

The whole pipeline is two API requests per document, run in sequence:

* **Pass 1, stitch:** one `Noul` question (a yes/no question whose answer is the
  probability that yes is correct) per adjacent pair of lines, asking whether the line
  break split a sentence across the two. All the pairs go in a single request, and lines
  that continue a split sentence get merged back into blocks.
* **Pass 2, classify:** one `Choice` question (pick one option from a list, with a
  probability for every option) per merged block, choosing among heading, paragraph, list
  item, quote, code, or callout (a note, tip, or warning set apart from the main text).
  The blocks only exist once pass 1 has answered, so this is a second request; it also
  carries companion questions for every block (heading level, step order, callout kind)
  whose answers are read only when the block's type makes them relevant.
* **Direct evidence stays in code.** Blank lines and explicit markers (`- `, `1.`, `#`)
  are read in code, never sent to the model to reconsider; this memo kept its blank lines
  but lost every marker. The model gets only the questions code cannot answer from the
  text.

All of the behavior is specified in the pass-2 question criteria: three dicts of
one-line descriptions, plus the step question's true/false criteria inside
`classify_questions`. The rest of the code is plumbing around them. The cost and latency
numbers are in the appendix: two round trips, 10,211 tokens, 0.8s, \$0.0015 for this
memo.

## Setup

```bash theme={null}
pip install ipython "typesafe-sdk>=0.5.7" cooksafe --extra-index-url https://pypi.typesafe.ai/
```

then set `TYPESAFE_API_KEY`. Every API call is cached in `json_cache.json`, which ships
with the cookbook, so re-rendering replays the published numbers without calling the API.
Delete that file to re-run everything live.

```python theme={null}
import os
import re
import urllib.request
from pathlib import Path
from time import perf_counter

from cooksafe import JsonCache, make_playground_link
from IPython.display import Markdown, display
from typesafe_sdk import Choice, Noul, NoulCriteria, TypeSafeClient

TYPESAFE_MODEL = "jev-1.12"
PRICE = (0.042, 0.00)  # $ per 1M tokens (input, output); TypeSafe jev-1.12 as of 2026-09
client = TypeSafeClient(api_key=os.environ["TYPESAFE_API_KEY"], timeout=120.0)
json_cache = JsonCache(Path("json_cache.json"))
```

## The document: a team memo that lost its formatting

The test document is a memo about a build-system migration, in the state it arrives in a
plain-text inbox: paragraphs hard-wrapped mid-sentence, a shell command sitting on a bare
line, two lists with no bullets or numbers, a warning with nothing marking it as one. The
text is fetched from a pinned gist so the cookbook's numbers stay reproducible.

```python theme={null}
GIST = (
    "https://gist.githubusercontent.com/eugene-shvarts/6df7daf97233bf92bcdd6b386a0fa561"
    "/raw/5da03690611fb6ddcbaabdb91fb9f91d9751b113/build-memo.txt"
)


@json_cache
def fetch_document(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "typesafe-cookbook/1.0"})
    with urllib.request.urlopen(request) as response:
        return response.read().decode()


RAW = fetch_document(GIST)
print(RAW[:560])
```

```
Migration to the new build system

Hi everyone, quick heads up about the build system migration that is
happening next week. We have been running the new pipeline in shadow
mode for three weeks and the results look solid, so it is time to
make the switch for real.

What changes for you

The old make targets keep working until the end of the month. The new
entrypoint is a single command that wraps everything, including the
docs build that used to be separate.

bun run build

Generated artifacts no longer need to be committed. The new pipeline
uploads them
```

Line splitting, blank-line tracking, and id tagging all happen in code; no model is
involved.
Each line gets a short id (`L014| `); the ids are ordinary text the model reads as part of
the state, and questions and answers refer to lines by these ids (the same scheme as the
[semantic search cookbook](semantic_find.md)).

```python theme={null}
def to_lines(text: str) -> list[dict]:
    lines, gap = [], False
    for raw in text.split("\n"):
        stripped = re.sub(r"[\t ]+", " ", raw).strip()
        if not stripped:
            gap = bool(lines)  # a leading blank is not a break
            continue
        lines.append({"text": stripped, "gap": gap})
        gap = False
    return lines


def tag(items: list[dict], prefix: str) -> str:
    return "\n".join(
        f"{chr(10) if item['gap'] else ''}{prefix}{i:03d}| {item['text']}"
        for i, item in enumerate(items)
    )


def line_id(i: int) -> str:
    return f"L{i:03d}"


def block_id(i: int) -> str:
    return f"B{i:03d}"


LINES = to_lines(RAW)
print(f"{len(LINES)} non-blank lines. The model sees, e.g.:")
print("\n".join(tag(LINES, "L").splitlines()[19:24]))
```

```
28 non-blank lines. The model sees, e.g.:
L013| The cutover touches three teams, so check whether you are on this
L014| list before you plan anything for Monday:
L015| The platform team
L016| The web client team
L017| Whoever still owns the release tooling
```

## Pass 1: stitching split sentences

One Noul question per adjacent pair of lines, all in one request; pairs separated by a
blank line are skipped. The question is deliberately narrow ("does this line pick up
mid-sentence?"), which is close to an objective fact about the text. The appendix covers
both the wording choice and how the merge thresholds were derived.

```python expandable theme={null}
def join_question(i: int) -> Noul:
    return Noul(
        instructions=f"Does line {line_id(i)} pick up mid-sentence, continuing a sentence left unfinished at the end of line {line_id(i - 1)}?",
        criteria=NoulCriteria(
            true="The line starts in the middle of a sentence that began on the previous line - the line break tore the sentence apart",
            false="The line begins a new sentence, item, heading, or thought of its own",
        ),
    )


@json_cache
def stitch(wording: str = "mid-sentence") -> dict:
    make = join_question if wording == "mid-sentence" else naive_join_question
    questions = {line_id(i): make(i) for i in range(1, len(LINES)) if not LINES[i]["gap"]}
    started = perf_counter()
    response = client.system_one(
        state=tag(LINES, "L"), questions=questions, model=TYPESAFE_MODEL
    )
    return {
        "joins": [
            response.answers[line_id(i)].noul if line_id(i) in response.answers else 0.0
            for i in range(len(LINES))
        ],
        "seconds": round(perf_counter() - started, 2),
        "usage": [response.usage.input_tokens, response.usage.output_tokens],
    }


result = stitch()
print(f"{sum(1 for l in LINES if not l['gap']) - 1} pair questions, one request, "
      f"{result['seconds']}s")
```

```
16 pair questions, one request, 0.32s
```

The cutoff for merging depends on how the previous line ends. After a dangling line (one
with no sentence-ending punctuation), a join probability of 0.2 or above merges the
pair; after terminal punctuation (`.` `!` `?` `:` `;`), the cutoff rises to 0.5. The
appendix walks through the probabilities behind the two numbers.

```python theme={null}
JOIN_AFTER_DANGLING, JOIN_AFTER_TERMINAL = 0.2, 0.5


def ends_terminal(text: str) -> bool:
    return re.search(r'[.!?:;…]["\')\]]*$', text) is not None


def merge(joins: list[float]) -> list[dict]:
    blocks = []
    for i, line in enumerate(LINES):
        bar = (
            JOIN_AFTER_TERMINAL
            if i and ends_terminal(LINES[i - 1]["text"])
            else JOIN_AFTER_DANGLING
        )
        if blocks and not line["gap"] and joins[i] >= bar:
            blocks[-1]["text"] += " " + line["text"]
            blocks[-1]["lines"].append(i)
        else:
            blocks.append({"text": line["text"], "lines": [i], "gap": line["gap"]})
    return blocks


blocks = merge(result["joins"])
healed = len(LINES) - len(blocks)
print(f"{len(LINES)} lines -> {len(blocks)} blocks ({healed} line breaks healed)")
for i, block in enumerate(blocks):
    n = len(block["lines"])
    print(f"{block_id(i)}  {n} line{'s' if n > 1 else ' '}  {block['text'][:62]}")
```

```
28 lines -> 17 blocks (11 line breaks healed)
B000  1 line   Migration to the new build system
B001  4 lines  Hi everyone, quick heads up about the build system migration t
B002  1 line   What changes for you
B003  3 lines  The old make targets keep working until the end of the month. 
B004  1 line   bun run build
B005  3 lines  Generated artifacts no longer need to be committed. The new pi
B006  2 lines  The cutover touches three teams, so check whether you are on t
B007  1 line   The platform team
B008  1 line   The web client team
B009  1 line   Whoever still owns the release tooling
B010  1 line   Things to do before Monday
B011  1 line   Update your local toolchain to version 2.4 or later
B012  1 line   Delete the old build cache directory
B013  1 line   Run the doctor script and fix anything it flags
B014  3 lines  If the doctor script reports a red result on the toolchain che
B015  2 lines  As Dana put it in the kickoff, "a migration nobody notices is 
B016  1 line   Thanks, and shout if anything looks off.
```

## Pass 2: classifying blocks

Each stitched block gets a `Choice` question: *what kind of content is this?* These
three
dicts, plus the step question's true/false criteria inside `classify_questions` below,
are the entire specification of the classifier. There is no other logic. To adapt the
pipeline to your own documents, edit these descriptions.

```python theme={null}
TYPE_CRITERIA = {
    "heading": "A short label or title that names the document or the section that follows it - not a full sentence of content",
    "paragraph": "Running prose: one or more complete sentences of explanatory or narrative text",
    "list_item": "One entry in a list of parallel items - an ingredient, a feature, a task, an attendee; reads as one of several sibling entries",
    "quote": "Words attributed to a person or source - quoted speech, a citation, an excerpt someone else wrote",
    "code": "Computer code, a shell command, terminal output, or a config snippet meant to be read verbatim",
    "callout": "A warning, tip, or important note that interrupts the flow to flag something the reader must not miss",
}
HLEVEL_CRITERIA = {
    "title": "The title of the whole document",
    "section": "A major section heading within the document",
    "subsection": "A minor heading nested under a section",
}
CALLOUT_CRITERIA = {
    "note": "Neutral extra information the reader should be aware of",
    "tip": "A helpful suggestion or shortcut that makes things easier",
    "warning": "A caution about something that can go wrong or cause harm",
}
```

Everything below is plumbing: build the questions, send one request, read the answers back.
If the type comes back `heading`, the renderer needs a heading level; if `list_item`,
whether order matters; if `callout`, which kind. The types are not known yet, and waiting
for them would mean a third round trip, so the companion questions are asked up front in
the same request. Most of these answers are never read: the step probability of a paragraph
means nothing and is simply ignored. An extra question adds little, since the state is
most of the tokens and is sent once either way, while an extra round trip adds a full
request of latency.

```python expandable theme={null}
HEADING_MAX_CHARS = 90  # longer blocks can't render as headings, so don't ask


def classify_questions(texts: list[str]) -> dict:
    questions = {}
    for i, text in enumerate(texts):
        bid = block_id(i)
        questions[f"type_{bid}"] = Choice(
            instructions=f"What kind of content is block {bid}?", criteria=TYPE_CRITERIA
        )
        if len(text) <= HEADING_MAX_CHARS:
            questions[f"hlevel_{bid}"] = Choice(
                instructions=f"As a heading, what level would block {bid} occupy in this document's structure?",
                criteria=HLEVEL_CRITERIA,
            )
        questions[f"step_{bid}"] = Noul(
            instructions=f"Is block {bid} an instruction in a sequence where the order of the items matters?",
            criteria=NoulCriteria(
                true="It is one step of a procedure - the items around it must happen in order",
                false="Order is irrelevant - it is a loose collection, or not a list item at all",
            ),
        )
        questions[f"callout_{bid}"] = Choice(
            instructions=f"What kind of aside is block {bid}?", criteria=CALLOUT_CRITERIA
        )
    return questions


@json_cache
def classify(texts: list[str], gaps: list[bool]) -> dict:
    tagged = tag([{"text": t, "gap": g} for t, g in zip(texts, gaps)], "B")
    questions = classify_questions(texts)
    started = perf_counter()
    response = client.system_one(state=tagged, questions=questions, model=TYPESAFE_MODEL)
    judgments = []
    for i in range(len(texts)):
        bid = block_id(i)
        type_answer = response.answers[f"type_{bid}"]
        hlevel = response.answers.get(f"hlevel_{bid}")
        judgments.append(
            {
                "type": type_answer.choice,
                "confidence": type_answer.confidence,
                "probabilities": type_answer.probabilities,
                "hlevel": hlevel.choice if hlevel else "section",
                "step": response.answers[f"step_{bid}"].noul,
                "callout": response.answers[f"callout_{bid}"].choice,
            }
        )
    return {
        "judgments": judgments,
        "n_questions": len(questions),
        "seconds": round(perf_counter() - started, 2),
        "usage": [response.usage.input_tokens, response.usage.output_tokens],
    }


classified = classify([b["text"] for b in blocks], [b["gap"] for b in blocks])
for block, judgment in zip(blocks, classified["judgments"]):
    block.update(judgment)
print(f"{classified['n_questions']} questions about {len(blocks)} blocks, one request, "
      f"{classified['seconds']}s\n")
print(f"{'block':<6}{'type':<11}{'conf':<6}{'companion used':<18}text")
for i, b in enumerate(blocks):
    companion = {
        "heading": f"level={b['hlevel']}",
        "list_item": f"step={b['step']:.2f}",
        "callout": f"kind={b['callout']}",
    }.get(b["type"], "-")
    print(f"{block_id(i):<6}{b['type']:<11}{b['confidence']:.2f}  {companion:<18}"
          f"{b['text'][:46]}")
```

```
62 questions about 17 blocks, one request, 0.51s

block type       conf  companion used    text
B000  heading    0.99  level=title       Migration to the new build system
B001  paragraph  0.98  -                 Hi everyone, quick heads up about the build sy
B002  heading    0.75  level=section     What changes for you
B003  paragraph  0.89  -                 The old make targets keep working until the en
B004  code       1.00  -                 bun run build
B005  paragraph  0.90  -                 Generated artifacts no longer need to be commi
B006  paragraph  0.43  -                 The cutover touches three teams, so check whet
B007  list_item  0.99  step=0.15         The platform team
B008  list_item  1.00  step=0.16         The web client team
B009  list_item  0.99  step=0.12         Whoever still owns the release tooling
B010  heading    0.96  level=section     Things to do before Monday
B011  list_item  0.98  step=0.86         Update your local toolchain to version 2.4 or 
B012  list_item  0.99  step=0.87         Delete the old build cache directory
B013  list_item  0.92  step=0.90         Run the doctor script and fix anything it flag
B014  callout    0.65  kind=warning      If the doctor script reports a red result on t
B015  quote      0.99  -                 As Dana put it in the kickoff, "a migration no
B016  paragraph  0.92  -                 Thanks, and shout if anything looks off.
```

Every block's judgment is in that table, and the companion column shows the up-front
answers being put to use: the three "Things to do before Monday" lines carry step
probabilities near 0.9 (they will render as a numbered list), the three team lines sit
near 0.1 (bulleted), and the unmarked warning about the doctor script was classified as
a callout of kind `warning`. The appendix looks at the one block the model was unsure
about.

## Rendering

Code assembles the page from the judgments. Consecutive list items become one list,
numbered when the mean of the items' step probabilities is at least 0.5. That threshold
is a
group-level decision no single question asked directly.

````python expandable theme={null}
STEP_THRESHOLD = 0.5
HEADING_MARK = {"title": "#", "section": "##", "subsection": "###"}
CALLOUT_MARK = {"note": "NOTE", "tip": "TIP", "warning": "WARNING"}


def to_markdown(blocks: list[dict]) -> str:
    groups = []
    for b in blocks:
        if b["type"] in ("list_item", "code") and groups and groups[-1][0] == b["type"]:
            groups[-1][1].append(b)
        else:
            groups.append((b["type"], [b]))
    parts = []
    for kind, items in groups:
        if kind == "list_item":
            ordered = sum(b["step"] for b in items) / len(items) >= STEP_THRESHOLD
            parts.append("\n".join(
                f"{n + 1}. {b['text']}" if ordered else f"- {b['text']}"
                for n, b in enumerate(items)
            ))
        elif kind == "code":
            parts.append("```\n" + "\n".join(b["text"] for b in items) + "\n```")
        elif kind == "heading":
            parts.append(f"{HEADING_MARK[items[0]['hlevel']]} {items[0]['text']}")
        elif kind == "quote":
            parts.append(f"> {items[0]['text']}")
        elif kind == "callout":
            parts.append(f"> [!{CALLOUT_MARK[items[0]['callout']]}]\n> {items[0]['text']}")
        else:
            parts.append(items[0]["text"])
    return "\n\n".join(parts) + "\n"


markdown = to_markdown(blocks)
print(markdown)
````

````text expandable theme={null}
# Migration to the new build system

Hi everyone, quick heads up about the build system migration that is happening next week. We have been running the new pipeline in shadow mode for three weeks and the results look solid, so it is time to make the switch for real.

## What changes for you

The old make targets keep working until the end of the month. The new entrypoint is a single command that wraps everything, including the docs build that used to be separate.

```
bun run build
```

Generated artifacts no longer need to be committed. The new pipeline uploads them to the registry automatically, and checking them in just creates merge conflicts.

The cutover touches three teams, so check whether you are on this list before you plan anything for Monday:

- The platform team
- The web client team
- Whoever still owns the release tooling

## Things to do before Monday

1. Update your local toolchain to version 2.4 or later
2. Delete the old build cache directory
3. Run the doctor script and fix anything it flags

> [!WARNING]
> If the doctor script reports a red result on the toolchain check, do not proceed with the migration. Ping the infra channel first and we will sort it out together.

> As Dana put it in the kickoff, "a migration nobody notices is the only kind worth shipping."

Thanks, and shout if anything looks off.
````

Every word above is from the input. The pipeline only chose boundaries, types, and
markup.

## Open it in the playground

This share link holds the stitched blocks and the full pass-2 question set. Open it to
re-run the classification live.

```python theme={null}
playground_link = make_playground_link(
    tag(blocks, "B"),
    classify_questions([b["text"] for b in blocks]),
    models=[TYPESAFE_MODEL],
)
display(Markdown(f"🔗 [Open the stitched memo + questions in the TypeSafe playground]({playground_link})"))
```

Open the stitched memo + questions in the TypeSafe playground →

***

# Appendix

## Cost and latency

```python theme={null}
tokens = [result["usage"], classified["usage"]]
total_in, total_out = sum(t[0] for t in tokens), sum(t[1] for t in tokens)
cost = total_in / 1e6 * PRICE[0] + total_out / 1e6 * PRICE[1]
n_joins = sum(1 for l in LINES if not l["gap"]) - 1
print(f"pass 1  {n_joins} questions  {result['seconds']}s")
print(f"pass 2  {classified['n_questions']} questions  {classified['seconds']}s")
print(f"total   {total_in + total_out:,} tokens  "
      f"{result['seconds'] + classified['seconds']:.1f}s  ${cost:.4f}")
```

```
pass 1  16 questions  0.32s
pass 2  62 questions  0.51s
total   10,211 tokens  0.8s  $0.0003
```

Two round trips, 10,211 tokens, 0.8s, \$0.0015.

## Where the join thresholds come from

The per-line join probabilities from pass 1:

```python theme={null}
print("join  line")
for i, line in enumerate(LINES[:18]):
    join = "    " if i == 0 or line["gap"] else f"{result['joins'][i]:.2f}"
    print(f"{join}  {line_id(i)}| {line['text'][:66]}")
```

```
join  line
      L000| Migration to the new build system
      L001| Hi everyone, quick heads up about the build system migration that 
0.77  L002| happening next week. We have been running the new pipeline in shad
0.62  L003| mode for three weeks and the results look solid, so it is time to
0.39  L004| make the switch for real.
      L005| What changes for you
      L006| The old make targets keep working until the end of the month. The 
0.42  L007| entrypoint is a single command that wraps everything, including th
0.59  L008| docs build that used to be separate.
      L009| bun run build
      L010| Generated artifacts no longer need to be committed. The new pipeli
0.48  L011| uploads them to the registry automatically, and checking them in
0.40  L012| just creates merge conflicts.
      L013| The cutover touches three teams, so check whether you are on this
0.50  L014| list before you plan anything for Monday:
0.22  L015| The platform team
0.11  L016| The web client team
0.12  L017| Whoever still owns the release tooling
```

The probabilities land in two separate bands: line breaks that split a sentence score
0.39 and up, breaks the author meant score close to zero. But where to put the cutoff
between the bands depends on **how the previous line ends**, a fact code can read
directly:

* After a *dangling* line (one with no sentence-ending punctuation), anything at 0.2 or
  above counts as a continuation. True continuations score as low as 0.39 here (`L004|
  make the switch for real.`), so a single cautious cutoff at 0.5 would break up healthy
  paragraphs.
* After *terminal* punctuation (a character that ends a sentence or clause: `.` `!` `?`
  `:` `;`), the cutoff rises to 0.5. The memo's team list shows why: `L015| The platform
  team` follows a colon and scores 0.22. That is a low but nonzero "this continues the
  sentence" signal, and it would clear the 0.2 cutoff and merge the list into the
  sentence
  introducing it. No single threshold works for both cases; once code checks the
  punctuation first, the two bands separate.

## Why the question is "mid-sentence" and not "same paragraph"

The first version of this pipeline asked the obvious question: "are these two lines part
of the same paragraph?" It failed in a specific way. A run of short lines under a
heading (a list typed without bullets) *is* a paragraph in the loose sense: the lines sit
together and share a topic. Asked about paragraphs, the model says yes to every pair, and
the stitch pass merges the whole list into one long block.

Same document, same request shape, only the wording changed:

```python theme={null}
def naive_join_question(i: int) -> Noul:
    return Noul(
        instructions=f"Are lines {line_id(i - 1)} and {line_id(i)} part of the same paragraph?",
        criteria=NoulCriteria(
            true="The two lines belong to the same paragraph of running text",
            false="The two lines belong to different paragraphs or different pieces of content",
        ),
    )


naive = stitch("same-paragraph")
print(f"{'':14}{'mid-sentence':>13}{'same paragraph':>16}")
for i in (15, 16, 17, 20, 21):
    print(f"{line_id(i)}{'':2}{LINES[i]['text'][:36]:<38}"
          f"{result['joins'][i]:>7.2f}{naive['joins'][i]:>13.2f}")
print(f"\nblocks after merge: {len(blocks)} (mid-sentence) vs "
      f"{len(merge(naive['joins']))} (same paragraph)")
```

```
               mid-sentence  same paragraph
L015  The platform team                        0.22         0.77
L016  The web client team                      0.11         0.81
L017  Whoever still owns the release tooli     0.12         0.78
L020  Delete the old build cache directory     0.08         0.88
L021  Run the doctor script and fix anythi     0.05         0.91

blocks after merge: 17 (mid-sentence) vs 12 (same paragraph)
```

With the paragraph wording, every unmarked list item scores above 0.75 and both lists
collapse. The memo merges into a few run-on blocks. "Same paragraph" asks the model to
judge whether the topic carries over, and between list items it does. "Picks up
mid-sentence" asks about the text itself. When a judgment call feeds a threshold, the
question should name the narrowest fact that decides it. Here the wording is the
difference between 17 blocks and 12.

## The lowest-confidence block

```python theme={null}
uncertain = min(blocks, key=lambda b: b["confidence"])
print(f'"{uncertain["text"]}"')
print(f"confidence {uncertain['confidence']:.2f}: ", end="")
print(", ".join(f"{k} {v:.2f}" for k, v in
                sorted(uncertain["probabilities"].items(), key=lambda kv: -kv[1])[:3]))
```

```
"The cutover touches three teams, so check whether you are on this list before you plan anything for Monday:"
confidence 0.43: paragraph 0.53, list_item 0.24, callout 0.19
```

The sentence introducing the team list is genuinely ambiguous - it names what follows
(heading-like), is a complete sentence (paragraph-like), and sits where a callout would
go. The probabilities spread accordingly (paragraph 0.53, list\_item 0.24, callout 0.19),
and a UI can surface that - for example, underline for review any block whose type
confidence (the probability behind the winning choice) is under 0.55.
