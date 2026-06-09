# Evaluation results, v1

Complete run: 9 June 2026
Model tested: `llama-3.3-70b-versatile` (the model the app actually serves)
Eval set: 40 hand-labelled adversarial cases (`tests/eval_set.json`)
Harness: `tests/run_eval.py`
Raw results: `tests/eval_results/eval_combined.json`

## How I built this and why the number holds up

I wrote the 40 case descriptions to be hard on purpose. Hidden tier boundaries,
distractors, systems that read like one tier but sit in another. The
descriptions don't depend on the classifier in any way.

I derived the ground truth (`expected_tier`, `expected_article`) by hand from
the Act, reading the relevant Article or Annex point for each case. I did not
let the model produce the answer key. The classifier runs on the same
underlying model, so if that model also wrote the ground truth I would be
scoring the system against itself, and any agreement between the two would be
meaningless. Labelling each case off the Act text keeps the answer key
independent from the thing being graded.

The set is 10 clean, 10 boundary, 10 near-miss, 10 distractor, spread across the
four tiers. At 40 cases the margin of error on the overall figure is around 13
points either way. So 77.5% really means "somewhere around the high 70s," not a
precise score. It is a signal on a hard set, not a benchmark.

Only two cases are prohibited, which is too few to read as a rate, so I treat
those as spot checks.

## Result

Tier accuracy: 31 of 40 = 77.5%

Citation, Article level: 32 of 40 = 80.0%
Citation, Article plus exact page: 14 of 38 = 36.8%

Review flag firing on boundary cases: 1 of 10 = 10.0%

## Tier accuracy by tier

Rows are the tier I labelled. Columns are what the classifier returned.

| labelled \ got | prohibited | high-risk | limited-risk | minimal-risk | recall |
|---|---|---|---|---|---|
| prohibited   | 1 | 1  | 0 | 0  | 1/2 (spot check) |
| high-risk    | 1 | 14 | 2 | 0  | 14/17 = 82% |
| limited-risk | 0 | 1  | 6 | 0  | 6/7 = 86% |
| minimal-risk | 0 | 1  | 3 | 10 | 10/14 = 71% |

## Where it went wrong

Nine cases came back mis-tiered, and the misses are not scattered randomly. They
fall into a pattern.

Three minimal-risk cases got called limited-risk. The classifier reaches for the
Article 50 transparency tier on systems that carry no obligation at all. Two
high-risk cases got called limited-risk, so it under-rated them. One limited-risk
and one minimal-risk case got pushed up to high-risk, so it over-rated those.

The two that bother me most are on the serious end: one high-risk case it called
prohibited, and one prohibited case it called high-risk. That prohibited
versus high-risk line is exactly where a wrong answer costs the most, and it is
the line the model is least sure of.

The short version: it does well on clear cases, high-risk and limited-risk recall
both clear 80%, but it smears the boundaries. Limited-risk is the sink it pulls
toward from both sides. Minimal-risk is the weakest tier at 71%.

## The citation page gap

Article-level citation is 80%. Four times out of five it names the right Article
or Annex.

Exact page is only 36.8%. I went through every case where the Article was right
but the page was scored wrong, and there are two different things going on.

First, Annex III is a list that runs over several pages. It starts on page 127 in
my PDF and carries past 130. I labelled the page where the Annex begins, 127. The
classifier cites the page of the chunk it actually pulled, usually 130. Both
point at the same Annex. The exact-page check counts these as wrong only because
127 is not 130. The citation is fine. This one is a difference in how I labelled,
not a fault in the model.

Second, and this one is real, on some cases the model writes out the internal
passage label it was handed ("Passage 7") and a page of "1" or "page not
specified" instead of the actual page. A citation like that is no use to anyone.
This is the one citation problem worth fixing in the system.

Since the exact-page figure mixes a harmless labelling difference with a real
defect, I am reporting both citation numbers and calling the page gap a known
limitation rather than massaging the score. The 80% Article-level figure is the
one that answers the question a user cares about, does it send me to the right
part of the law.

## The review flag

The human-review flag fired on 1 of 10 boundary cases. That lines up with the
underfire problem I found in Week 4: the flag does not reliably trip on the
borderline cases, which are the ones where a human most needs to look. This is
why the app puts a standing caution on every result regardless (the
automation-bias floor from Week 7). That floor does not wait for the flag.

## What this evaluation can and cannot tell me

- 40 cases means a wide error band, around 13 points. Read the number as a
  signal.
- Two prohibited cases is not enough for a rate, so those are spot checks.
- The exact-page citation number is unreliable for the labelling reason above.
  Read it next to the Article-level number, not on its own.

## What v2 needs to fix, in order

1. The citation page defect. The model cites "page 1" because some chunks in the
   index carry a wrong page in their metadata. The model is just repeating what
   it was given. Fix the page assignment at ingestion, rebuild the index, re-run
   all 40.
2. The limited-risk over-assignment. That is the biggest single error pattern.
3. The review-flag underfire on boundary cases.

Each one is its own cycle: change the system, run the same 40 cases against the
same ground truth, report what moved. Same labels, same harness, so the before
and after are comparable.
