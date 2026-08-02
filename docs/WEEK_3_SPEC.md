# Week 3 Specification: VLASH and SmolVLA Validation

**Prerequisite:** primary π0.5 benchmark stable  
**Goals:** matched cross-method validation with VLASH and reduced cross-model
validation with SmolVLA

A broad but incompatible comparison is worse than a small matched comparison.

---

## 1. Baseline compatibility audit

Before numerical runs, complete:

```text
docs/BASELINE_COMPATIBILITY.md
```

For each candidate record:

```text
official repository and SHA
framework
base model
training required
official checkpoint
LIBERO support
observation keys
state representation
action convention
control frequency
chunk length
execution horizon
normalization
latency semantics
provenance hooks
fairness risks
```

Do not use a named method without official code and a compatible configuration.

---

## 2. VLASH compatibility gate

VLASH is required only when a fair official reproduction is possible.

Verify:

1. official repository and commit;
2. official π0.5-compatible checkpoint or required training recipe;
3. LIBERO task support;
4. future-state or offset-state input semantics;
5. action normalization;
6. relative action control;
7. control frequency;
8. chunk and execution horizon;
9. async request schedule;
10. ability to log source observation and executed action.

Do not call ordinary asynchronous π0.5 with a manually shifted state “VLASH.”

If no compatible official checkpoint exists and training is required:

- write a blocker report;
- do not create approximate VLASH results;
- continue with SmolVLA and paper analysis.

Required blocker output:

```text
outputs/vlash/compatibility.md
```

---

## 3. VLASH matched evaluation

When the compatibility gate passes, use:

- selected LIBERO-Spatial task;
- selected LIBERO-Goal task when supported.

Methods:

```text
naive_async
rtc
vlash
```

Delays:

```text
native
native_plus_700
```

Seeds:

```text
[0, 1, 2, 3, 4]
```

Standard matrix for VLASH itself:

```text
2 tasks × 2 delays × 5 seeds = 20 episodes
```

Matched naive async and RTC controls may be reused only when configurations
match exactly.

Also run the target-shift intervention on the spatial task:

```text
2 delays × 5 seeds = 10 VLASH episodes
```

Required comparisons:

- success;
- completion time;
- action age;
- stale-action count;
- stale duration;
- fresh-action reaction latency;
- jerk;
- queue underruns;
- policy calls;
- GPU time.

The main question is whether future-state alignment improves temporal freshness,
continuity, or both.

---

## 4. SmolVLA checkpoint gate

Select an official LIBERO-compatible SmolVLA checkpoint.

Pin:

```text
repository SHA
checkpoint revision
dataset revision
policy configuration
camera keys
action normalization
control frequency
chunk length
execution method support
```

Do not assume π0.5 and SmolVLA use identical preprocessing or horizons.

Run ideal execution first. A task enters the delayed comparison only when the
SmolVLA ideal baseline is adequate to isolate delay effects.

---

## 5. SmolVLA reduced matrix

Required tasks:

- selected LIBERO-Spatial task, or the closest exact matched task;
- one precision/contact task with adequate ideal success.

Methods:

```text
ideal_sync
naive_async
rtc
```

Conditions:

```text
ideal_sync: ideal
naive_async: native, native_plus_700
rtc: native, native_plus_700
```

Seeds:

```text
[0, 1, 2, 3, 4]
```

Maximum standard runs:

```text
2 tasks × [1 ideal + 2 naive + 2 rtc] × 5 seeds
= 50 episodes
```

Dynamic intervention on the spatial task:

```text
naive_async and rtc
× native and native_plus_700
× 5 seeds
= 20 episodes
```

---

## 6. Reaction-deadline analysis

Choose deadlines before inspecting final test outcomes.

Recommended initial deadlines:

```text
500 ms
1000 ms
1500 ms
```

For each model and method report:

- ideal success;
- native request latency;
- fresh-action reaction latency;
- probability of meeting each deadline;
- success conditional on meeting the deadline;
- stale-action count;
- stale duration;
- policy-call count;
- GPU milliseconds.

Do not choose deadlines after observing which model benefits.

Primary cross-model question:

> Can a smaller, faster model outperform a stronger model under a strict
> fresh-action reaction constraint?

---

## 7. Optional streaming or corrective baseline

Audit one:

- FASTER;
- Reflex;
- VLA-Corrector;
- another official streaming/corrective method.

A numerical comparison is optional and must satisfy:

- official code;
- official compatible checkpoint;
- matched task protocol;
- measurable time to first usable action;
- provenance hooks;
- feasible integration before result freeze.

Do not add the method after Week 3 results freeze.

If no method passes, produce an audit rather than approximate numbers.

---

## 8. Team ownership

| Person | Primary ownership |
|---|---|
| Person 1 | SmolVLA environment, checkpoint validation, ideal and delayed runs |
| Person 2 | shared provenance/reaction adapter, cross-model runs, compute matching |
| Person 3 | VLASH reproduction, compatibility audit, matched analysis |

---

## 9. Validation

Fail when:

- a named method lacks its official config/checkpoint record;
- action conventions differ without a tested conversion;
- tasks are not matched;
- control frequencies differ;
- hidden quantization or acceleration differs;
- policy-call schedules are not reported;
- compute usage is omitted;
- provenance semantics differ;
- official and approximate implementations are mixed.

---

## 10. Required outputs

VLASH:

```text
outputs/vlash/environment.json
outputs/vlash/compatibility.md
outputs/vlash/episodes.csv
outputs/vlash/reaction_metrics.csv
```

SmolVLA:

```text
outputs/smolvla/environment.json
outputs/smolvla/episodes.csv
outputs/smolvla/reaction_metrics.csv
```

Combined:

```text
outputs/summaries/cross_method.csv
outputs/summaries/cross_model.csv
outputs/summaries/reaction_deadlines.csv
outputs/summaries/streaming_baseline_audit.md
outputs/summaries/week3_report.md
```

Figures:

```text
outputs/figures/cross_method_reaction.png
outputs/figures/cross_method_continuity.png
outputs/figures/cross_model_success_latency.png
outputs/figures/reaction_deadline_ranking.png
outputs/figures/stale_exposure_by_model.png
```

---

## 11. Week 3 decision gate

Proceed to final paper framing when at least one useful trade-off is supported:

- a method is smoother but not fresher;
- VLASH reduces one temporal failure mode while another remains;
- SmolVLA changes ranking under a reaction deadline;
- action age distinguishes methods with similar request latency;
- the optional streaming method reduces fresh-action latency but has another
  cost.

Prefer a smaller, defensible result over adding methods.

---

## 12. Week 3 report questions

1. Was VLASH reproduced fairly?
2. Did VLASH improve success under delay?
3. Did VLASH reduce action age?
4. Did VLASH reduce stale-action exposure?
5. Did VLASH improve continuity?
6. Did SmolVLA have lower request and reaction latency?
7. Did π0.5 retain higher ideal success?
8. Did model ranking reverse under any preregistered reaction deadline?
9. Which methods are suitable for the final paper?
10. Which incompatible baselines must remain related work only?
