# Research Context

## Title

**StaleBench: Temporal Robustness of Vision-Language-Action Policies under
Asynchronous Execution**

## Motivation

Action-chunked VLA systems can continue acting while the next policy request
runs in the background. This avoids blocking, but it creates a different
reliability problem: queued actions can remain conditioned on an observation
that no longer represents the scene.

A controller can therefore be smooth without being responsive.

## Central question

Can action-level provenance and controlled scene changes reveal temporal
robustness failures that are hidden by standard task success, request latency,
and trajectory smoothness?

## Benchmark architecture

Every:

- observation;
- policy request;
- generated chunk;
- queued action;
- executed action

receives a unique identifier and timestamp.

The benchmark applies controlled interventions while old actions remain
buffered and measures how long those actions remain in control.

## Primary research questions

1. How does request latency translate into executed action age?
2. How does task phase alter delay tolerance?
3. Do distribution shift and asynchronous delay interact?
4. How many stale actions do execution methods issue after a scene change?
5. Do method or model rankings change under fresh-action deadlines?
6. Does RTC improve continuity, freshness, or both?

## Hypotheses

### H1 — Latency versus tolerance

Raw request latency remains broadly similar across task semantics, while
behavioral delay tolerance varies by task phase.

### H2 — OOD × delay interaction

Visual distribution shift and asynchronous delay jointly reduce success more
than either factor evaluated alone.

### H3 — Freshness

Action age and stale-action exposure explain failure better than mean request
latency alone.

### H4 — Method trade-off

RTC improves continuity and chunk compatibility but does not always minimize
post-change stale-action exposure.

### H5 — Ranking reversal

The strongest zero-delay policy may not be best under strict fresh-action
reaction deadlines.

## Models

Primary:

```text
lerobot/pi05_libero_finetuned
```

Secondary, only after the primary benchmark is stable:

```text
official LIBERO-compatible SmolVLA checkpoint selected and pinned in Week 3
```

Optional:

```text
OpenVLA-OFT only if the required study is complete and execution semantics can
be matched fairly
```

## Execution methods

Core:

- ideal synchronous;
- blocking synchronous;
- naive asynchronous replacement;
- RTC;
- fixed-horizon sweep.

Later:

- VLASH;
- one streaming or corrective baseline only if official code and compatible
  checkpoints are available.

## Environments

- LIBERO-Spatial;
- LIBERO-Goal;
- LIBERO-10;
- selected LIBERO-Plus object-layout and camera variants.

## Main contribution

A benchmark and instrumentation framework for:

- action age;
- stale-action count;
- stale duration;
- fresh-action reaction latency;
- phase-conditioned delay;
- OOD-delay interaction;
- continuity-versus-freshness trade-offs.

## Explicit non-claims

StaleBench does not claim:

- a new asynchronous execution method;
- lower raw model inference latency;
- a safety guarantee;
- hardware validation;
- that fewer stale actions imply safe actions;
- universal superiority of any method.
