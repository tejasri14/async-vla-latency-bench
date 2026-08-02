# Week 4 Specification: Ablations, Statistics, Manuscript, and Release

**Rule:** no new methods after the Week 3 results freeze.

---

## 1. Results freeze

At the start of Week 4 create:

```text
outputs/summaries/results_freeze.json
```

Record:

```text
included tasks
included models
included methods
included delay profiles
included perturbations
included seeds
checkpoint revisions
repository revisions
invalid or missing cells
planned main figures
planned appendix figures
```

Runs added afterward must be labeled:

- correction;
- failed-run replacement;
- preregistered ablation.

Do not expand the benchmark opportunistically.

---

## 2. Required ablations

### A. Request latency versus action age

Compare how well each predicts:

- episode failure;
- post-intervention recovery failure;
- stale-action exposure.

Use:

- descriptive stratification;
- cross-validated simple logistic models;
- rank correlation;
- calibration plots when appropriate.

Do not infer causality from predictive association.

### B. Queue replacement versus RTC

Match:

- task;
- seed;
- request schedule;
- delay trace;
- horizon;
- policy calls;
- checkpoint.

### C. Fixed execution horizon

Compare:

- horizon 10;
- best global horizon selected in Days 1–3;
- task-specific oracle horizon as analysis-only upper bound.

Clearly mark oracle selection as non-deployable.

### D. ID versus OOD

Report the complete factorial table and interaction.

### E. Intervention timing

On one representative task, compare intervention:

1. just before request submission;
2. while a request is logically in flight;
3. during queued execution after a response.

Use three seeds when the main intervention result is stable.

### F. Compute matching

Compare results at matched:

- policy-call count;
- GPU milliseconds where meaningful.

### G. Phase-label sensitivity

Vary the transit/approach/precision distance thresholds within a small
preregistered range. Confirm the qualitative conclusion is not caused by one
threshold.

---

## 3. Statistical protocol

Required:

- raw episode counts;
- invalid and missing counts;
- Wilson intervals for success;
- episode-level bootstrap intervals for continuous metrics;
- paired differences for matched seeds;
- effect sizes;
- no per-step pseudoreplication.

Five-seed results remain preliminary. Avoid presenting p-values as the sole
evidence.

Correct multiple comparisons only for explicitly grouped hypothesis tests.
Prioritize confidence intervals and effect sizes.

---

## 4. Primary figure plan

Target six to eight main figures:

1. benchmark architecture and provenance;
2. request latency versus executed action age;
3. phase-conditioned delay sensitivity;
4. mid-chunk intervention timeline and stale exposure;
5. continuity versus freshness trade-off;
6. OOD × delay interaction;
7. cross-method comparison;
8. cross-model reaction-deadline ranking.

Appendix:

- horizon sweep;
- queue occupancy;
- compute usage;
- phase-label sensitivity;
- environment and checkpoint tables;
- invalid-run accounting.

---

## 5. Manuscript claims

Candidate claims, only when supported:

- asynchronous smoothness does not imply temporal freshness;
- executed action age captures closed-loop behavior not visible in request
  latency;
- task phase changes delay tolerance;
- OOD and delay can interact;
- strong async methods improve different temporal dimensions;
- method or model rankings can change under reaction constraints.

Do not claim:

- safety;
- universal ranking;
- hardware validity;
- a new execution algorithm;
- lower raw inference latency;
- distribution-free guarantees;
- that all OOD conditions amplify delay.

---

## 6. Manuscript structure

Use `docs/PAPER_OUTLINE.md`.

The abstract and introduction must state that StaleBench is an evaluation and
instrumentation contribution.

The limitations section must cover:

- simulation only;
- intervention realism;
- phase-label approximation;
- cross-codebase mismatch;
- statistical cost;
- no safety guarantee.

---

## 7. Release package

Required:

```text
README.md
environment lock files
exact repository SHAs
checkpoint revisions
configs
task mappings
latency traces
intervention definitions
analysis scripts
figure commands
validated result manifest
known limitations
```

Do not include:

- credentials;
- private absolute paths;
- unnecessary checkpoint copies;
- generated caches;
- unlicensed assets.

---

## 8. Team ownership

| Person | Primary ownership |
|---|---|
| Person 1 | simulator ablations, intervention validation, release configs |
| Person 2 | statistics, tables, analysis scripts, reproducibility |
| Person 3 | manuscript integration, figures, related work, release audit |

Every central paper claim must be reviewed against its supporting result.

---

## 9. Final kill check

Do not submit the original framing when the final result is only:

> More delay reduces task success.

A defensible workshop paper should establish at least two:

- request latency and action age differ materially;
- phase changes delay tolerance;
- intervention creates method-dependent stale exposure;
- OOD and delay interact;
- continuity and freshness trade off;
- method/model ranking changes under reaction constraints.

If not, reframe as:

- an instrumentation paper;
- a negative-results benchmark report;
- a narrower temporal-provenance study.

---

## 10. Final deliverables

```text
paper/main.pdf
paper/source/
release/README.md
release/configs/
release/scripts/
release/results_manifest.json
outputs/summaries/final_results.csv
outputs/summaries/final_claims.md
outputs/summaries/reproducibility_checklist.md
outputs/summaries/limitations.md
```

---

## 11. Final review questions

1. Which claims are directly supported?
2. Which claims rely on one task only?
3. Which results are preliminary?
4. Are all named baselines official and fair?
5. Are invalid runs reported?
6. Can every main figure be regenerated from a command?
7. Does the paper distinguish request latency, action age, stale duration, and
   fresh-action reaction latency?
8. Does the paper avoid safety and hardware claims?
