# Paper Outline

## Working title

**StaleBench: Temporal Robustness of Vision-Language-Action Policies under
Asynchronous Execution**

---

## Abstract

- asynchronous execution prevents blocking;
- buffered actions may remain conditioned on an outdated scene;
- standard request latency, success, and smoothness do not measure this;
- StaleBench adds action-level provenance, controlled interventions, phase
  analysis, and OOD-delay interaction;
- summarize principal empirical findings without overstating scope.

---

## 1. Introduction

- continuous motion is not the same as responsive motion;
- target-movement motivating example;
- missing executed-action freshness metrics;
- contributions.

---

## 2. Related Work

- action chunking and RTC;
- future-state-aware inference and VLASH;
- streaming and time-to-first-action methods;
- adaptive execution horizons;
- stale-action correction;
- VLA robustness benchmarks;
- event-triggered control as conceptual background.

---

## 3. StaleBench

### 3.1 Provenance architecture

Observation → request → chunk → queue → executed action.

### 3.2 Timing definitions

Request latency, logical delay, action age.

### 3.3 Dynamic intervention protocol

Stale count, stale duration, fresh-action reaction latency.

### 3.4 Task phases

Transit, approach, precision, contact, placement.

### 3.5 Distribution shift

ID/OOD factorial design.

---

## 4. Experimental Setup

- policies;
- tasks;
- execution methods;
- latency profiles;
- interventions;
- environment and compute;
- statistics.

---

## 5. Results

### 5.1 Request latency versus action age

### 5.2 Phase-conditioned delay tolerance

### 5.3 Mid-chunk scene changes

### 5.4 Continuity versus freshness

### 5.5 OOD × delay interaction

### 5.6 Cross-method validation

### 5.7 Cross-model reaction deadlines

---

## 6. Ablations

- horizon;
- queue semantics;
- intervention timing;
- compute matching;
- phase thresholds;
- metric predictiveness.

---

## 7. Discussion

- what real-time should mean for VLA execution;
- why smoothness and freshness differ;
- implications for evaluation;
- limitations;
- future hardware work.

---

## 8. Conclusion

Temporal robustness is a closed-loop execution property and should be measured
at the executed-action level.
