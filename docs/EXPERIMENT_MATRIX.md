# Experiment Matrix

This file is the high-level registry. Exact task IDs are populated after Days
1–3 task selection.

---

## Stage 1 — Days 1–3

Canonical details are in `DAYS_1_3_SPEC.md`.

Expected core:

```text
π0.5
selected Spatial, Goal, LIBERO-10 tasks
ideal sync
blocking sync
naive async
RTC
horizons 2, 5, 10
ideal, native, native+300, native+700
```

---

## Stage 2 — Days 4–8

### Phase-conditioned delay

```text
2 tasks × 3 phases × 2 methods × 5 seeds = 60 episodes
```

### Dynamic intervention

```text
30 episodes
```

Maximum new required runs:

```text
90 episodes
```

---

## Stage 3 — Week 2

Minimum:

```text
1 task
× 2 OOD families
× 2 scene states
× 2 delays
× 2 methods
× 5 seeds
= 80 episodes
```

Optional second task:

```text
+80 episodes
```

Limited horizon ablation:

```text
1 task × 1 OOD family × 2 horizons × 2 methods × 2 scenes × 3 seeds
= 24 episodes
```

---

## Stage 4 — Week 3

### VLASH

```text
20 standard episodes
10 intervention episodes
```

### SmolVLA

```text
up to 50 standard episodes
20 intervention episodes
```

Optional streaming/corrective baseline is not included unless its compatibility
gate passes.

---

## Stage 5 — Week 4

Use existing runs where possible.

New runs are restricted to:

- preregistered ablations;
- failed-run replacements;
- corrections.

---

## Run registry columns

```text
run_id
stage
model
checkpoint_revision
method
task_suite
task_id
seed
scene_condition
ood_family
delay_profile
horizon
intervention
phase_trigger
environment_fingerprint
status
validation_status
output_path
notes
```
