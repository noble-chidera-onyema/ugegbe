# Held-out validation, v4

Run: 20 June 2026
Model: `llama-3.3-70b-versatile`
Set: 10 fresh cases (`tests/holdout_set.json`), none reused from the 40-case
development set
Ground truth: derived by hand from the EU AI Act, independent of the model
Raw results: `tests/eval_results/eval_combined_holdout.json`
Run discipline: run once on v4, no iterating, no re-rolls. The number below is
the result as it came out.

## Why this set exists

The 40-case set was used to guide four rounds of changes, so by v4 it was a
development signal, not an unseen test. A model tuned against a fixed set can
score well on that set without generalising. This held-out set is the check:
10 new cases v4 had never seen, labelled the same independent way, run once.

## Result

| Metric | v4 on the 40 | v4 on the 10 held-out |
|---|---|---|
| Tier accuracy | 70.0% | 70.0% |
| Citation, right Article/Annex | 72.5% | 80.0% |
| Citation, Article + page | 47.4% | 85.7% |

Tier accuracy on unseen cases is the same as on the development set: 70%. That
is the main finding. If the tuning had been fitting the 40 rather than learning
the task, the held-out number would have dropped. It did not. v4 generalises.

Citation accuracy on the held-out cases is at least as good as on the 40, so the
Annex-aware indexing and the provision-start-page convention generalise too.
The Article+page figure (6 of 7) is on a small denominator and should be read as
"held up", not as a precise gain.

## The misses are characterisable

All three tier misses were the same error: a minimal-risk case classified as
high-risk. They were the cases where the correct answer depends on an exclusion
that a surface reading misses:

- A debt-collection system that pattern-matches to creditworthiness (Annex III
  5(b)) but is excluded, because 5(b) per recital 58 concerns access to
  financial resources, not recovery on an existing debt. The closed Annex III
  list does not catch private debt-collection decisions; GDPR Article 22 is the
  applicable safeguard.
- A forklift safety component that pattern-matches to "safety component of
  machinery" but, under the current Machinery Directive, is self-assessed, so
  the Article 6(1) third-party conformity-assessment condition is not met today.

v4 applied the surface pattern and missed the carve-out in each case. The
characteristic error is therefore over-triggering high-risk on systems that
resemble an Annex III domain but are excluded on a closer reading.

For a compliance tool this is the safer direction to err: it flags more as
high-risk rather than fewer, so a user is warned to look harder rather than
wrongly reassured. It is still a real limitation and is recorded as one.

## Review flag

The flag fired on 0 of 2 boundary cases, the same underfire seen across v1 to
v4. The two cases v4 got wrong are the ones it should have flagged. This
confirms on unseen data that the underfire is a model-overconfidence problem,
not a logic problem, and that the standing caution shown on every
classification remains the real mitigation until confidence calibration is
addressed.

## Conclusion

v4 generalises: identical tier accuracy on unseen cases, citation accuracy that
holds or improves, and an error pattern that is consistent and explainable
rather than random. The 70% figure is therefore a fair statement of v4's real
performance on hard cases, not an artefact of tuning. This closes the
evaluation phase. Further gains need a different kind of change (retrieval
quality, confidence calibration, possibly a stronger model), not more prompt
tuning against a fixed set.
