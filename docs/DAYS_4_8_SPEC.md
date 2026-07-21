# Days 4–8 Specification: Task-Conditioned Delay Tolerance for Asynchronous π0.5

**Scope:** Combined workload for all three researchers
**Primary policy:** `lerobot/pi05_libero_finetuned`
**Primary simulator:** LIBERO through the pinned LeRobot environment from Days 1–3
**Required execution backends:** `ideal_sync`, `blocking_sync`, `naive_async`, `rtc`
**New baseline gate:** VLASH feasibility and, only if compatible, matched evaluation
**Deferred:** full FASTER reproduction, SmolVLA, OpenVLA-OFT, training a new policy, and a new buffering algorithm

---

## 1. Purpose

Days 1–3 establish whether π0.5 execution changes under blocking, naive asynchronous buffering, RTC, and fixed execution horizons.

Days 4–8 test the more scientific question:

> Does the behavioral cost of asynchronous latency depend on task phase, environmental perturbation, and temporal-alignment method?

The work must separate:

- raw model inference latency;
- logical request delay;
- action age;
- queue underrun;
- time to first action based on a fresh observation;
- task success;
- action continuity.

The work must not claim that an OOD scene makes the fixed π0.5 forward pass intrinsically slower. The primary hypothesis is that OOD conditions and precision-sensitive phases make **stale actions less tolerable**, even when model runtime is similar.

---

## 2. Entry requirements

Do not start the Days 4–8 experiment matrix until all applicable Days 1–3 requirements are satisfied.

Required inputs:

```text
async_vla_benchmark/outputs/environment.json
async_vla_benchmark/outputs/summaries/task_selection.csv
async_vla_benchmark/outputs/summaries/native_latency.csv
async_vla_benchmark/outputs/summaries/episodes.csv
async_vla_benchmark/outputs/summaries/horizon_sweep.csv
async_vla_benchmark/outputs/summaries/days1_3_report.md
```

Required implementation state:

- exact π0.5 checkpoint loads on CUDA;
- three usable LIBERO tasks have been selected, or missing suites are documented;
- latency-to-step conversion uses `ceil`;
- provenance exists for observations, chunks, and actions;
- logical delay uses a discrete-event clock rather than `sleep()`;
- only one inference request may be outstanding;
- `naive_async` and RTC have validated queue semantics;
- RTC receives request-specific delay and current chunk remainder;
- Days 1–3 result validation passes.

If one or more prerequisites are missing, create:

```text
async_vla_benchmark/outputs/summaries/days4_8_blockers.md
```

and complete the missing prerequisite before broadening the benchmark.

---

## 3. Verified upstream constraints

Treat these as implementation constraints rather than assumptions:

1. LeRobot RTC supports flow-based policies including π0, π0.5, and SmolVLA.
2. RTC accepts runtime `inference_delay` in control timesteps and uses the previous chunk remainder for overlap guidance.
3. LIBERO-plus installs under the same `libero` Python package namespace and replaces the vanilla LIBERO package.
4. Vanilla LIBERO and LIBERO-plus must therefore use separate environments or containers.
5. The official VLASH repository supports π0.5-style asynchronous inference and provides YAML-based training and inference commands.
6. Do not assume an ordinary `lerobot/pi05_libero_finetuned` checkpoint is VLASH-compatible without verifying the repository’s future-state-aware training and checkpoint requirements.
7. The official FASTER implementation is based on OpenPI/JAX and its Horizon-Aware Schedule is a training-time model change. It is not a drop-in flag for the LeRobot π0.5 checkpoint.

Pin all newly used repositories and record their commit SHAs.

---

## 4. Scientific hypotheses

### H1: Task phase changes delay tolerance

The same one-time latency pulse should cause greater degradation during approach, precision, or contact than during free-space transit.

### H2: OOD and delay interact

A scene perturbation combined with asynchronous delay should cause more degradation than either perturbation or delay alone.

For binary success, report the descriptive interaction:

\[
I =
[S_{\mathrm{OOD,delayed}} - S_{\mathrm{OOD,native}}]
-
[S_{\mathrm{ID,delayed}} - S_{\mathrm{ID,native}}].
\]

### H3: Smooth continuity is not the same as fast reaction

RTC may improve jerk and chunk compatibility without proportionally reducing the number of stale actions executed after an unexpected target displacement.

### H4: Temporal alignment may fix a different failure mode

If VLASH is reproducible in a matched setup, determine whether future-state conditioning reduces failures that remain after RTC.

### H5: A single horizon is not uniformly optimal

Use the Days 1–3 horizon results to test whether the best fixed horizon changes by task phase or perturbation.

---

## 5. Scope boundaries

### Required

- audit and freeze the Days 1–3 benchmark;
- implement privileged task-phase annotation;
- implement a phase-triggered one-time latency pulse;
- implement a deterministic mid-episode target displacement;
- implement two static perturbations in LIBERO-plus;
- run matched `naive_async` and RTC comparisons;
- preserve `ideal_sync` and `blocking_sync` as references where specified;
- perform a VLASH compatibility audit;
- run a VLASH smoke benchmark only when compatibility is verified;
- produce a validated Days 4–8 report.

### Optional only after required work is complete

- extend VLASH to a second task;
- run more than five seeds;
- add a second displacement magnitude;
- create a FASTER environment and run an official smoke test;
- add SmolVLA;
- add an adaptive scheduler.

### Explicitly out of scope

- training or fine-tuning π0.5;
- implementing a new paper method;
- claiming real-world robot safety;
- claiming closed-loop guarantees;
- comparing reported numbers from different papers without rerunning them;
- silently approximating VLASH or FASTER;
- installing LIBERO-plus into the validated vanilla-LIBERO environment.

---

## 6. Repository additions

Add:

```text
async_vla_benchmark/
├── configs/
│   ├── days4_8.yaml
│   ├── phase_pulses.yaml
│   ├── interventions.yaml
│   └── ood.yaml
├── benchmark/
│   ├── phases.py
│   ├── delay_pulses.py
│   ├── interventions.py
│   ├── libero_plus_adapter.py
│   ├── reaction_metrics.py
│   └── vlash_adapter.py
├── scripts/
│   ├── audit_days1_3.py
│   ├── run_phase_pulses.py
│   ├── run_dynamic_interventions.py
│   ├── run_libero_plus.py
│   ├── inspect_vlash.py
│   ├── run_vlash_smoke.py
│   ├── validate_days4_8.py
│   └── make_days4_8_figures.py
└── outputs/
    ├── phase_pulses/
    ├── interventions/
    ├── libero_plus/
    ├── vlash/
    └── summaries/
```

Also create:

```text
docs/BASELINE_COMPATIBILITY.md
docs/EXPERIMENT_DECISIONS.md
```

Do not mix VLASH or FASTER dependencies into the validated LeRobot environment unless their dependency sets are proven compatible. Prefer separate environments and an adapter boundary.

---

## 7. Fixed configuration

Read selected task IDs from:

```text
outputs/summaries/task_selection.csv
```

Do not hardcode different task IDs.

Use the same:

- π0.5 checkpoint revision;
- policy normalization;
- camera keys;
- language instruction;
- control mode;
- simulator initialization states;
- seeds;
- control frequency;
- sampling configuration;
- GPU type;
- logical clock;
- action clipping;
- hold action;
- provenance schema

as Days 1–3.

Default seeds:

```yaml
seeds: [0, 1, 2, 3, 4]
```

Required latency profiles:

```yaml
latency_profiles:
  native:
    use_measured_native_latency: true
    added_latency_ms: 0

  native_plus_700:
    use_measured_native_latency: true
    added_latency_ms: 700
```

For phase-pulse experiments, the extra 700 ms is applied to exactly one request. All other requests use native latency.

Use the best fixed horizon from Days 1–3 only when it was selected without using Days 4–8 results. Also retain horizon 10 as the standard reference.

Do not tune a different horizon for each perturbation.

---

## 8. Team ownership

| Person | Primary ownership | Secondary responsibility |
|---|---|---|
| Person 1 | Simulator state, phase labels, interventions, LIBERO-plus environment | Reproducibility and reset validation |
| Person 2 | Delay pulses, provenance, reaction metrics, experiment runner | Queue/log validation and matched seeds |
| Person 3 | VLASH audit/integration, analysis, figures, paper-facing report | Baseline fairness and environment metadata |

All three people must participate in the Day 4 audit and Day 8 conclusion review.

---

# Day 4 — Audit, freeze, and phase instrumentation

## Shared objective

Establish that Days 1–3 results are trustworthy and add task-phase labels without changing policy behavior.

## Person 1: phase annotation

Implement privileged phase annotation for analysis only.

For each selected task:

1. resolve the primary manipulated object from the task definition or simulator object registry;
2. resolve end-effector position;
3. detect gripper/end-effector contact with the target;
4. calculate end-effector-to-object distance;
5. label each control step.

Initial phase definitions:

```yaml
transit:
  condition: distance > 0.10 m and no target contact

approach:
  condition: 0.03 m < distance <= 0.10 m and no target contact

precision:
  condition: distance <= 0.03 m and no target contact

contact:
  condition: target contact is active

unknown:
  condition: target or geometry cannot be resolved
```

Requirements:

- phase labels must not affect execution;
- unresolved objects must produce `unknown`, not a guessed phase;
- record distances and contact booleans;
- validate phase transitions on video for at least one episode per task;
- preserve the phase label on every executed-action row.

## Person 2: Days 1–3 audit and delay-pulse engine

Run:

```bash
python async_vla_benchmark/scripts/audit_days1_3.py \
  --output-dir async_vla_benchmark/outputs
```

Audit:

- exact checkpoint revision;
- action source provenance;
- request-specific delay;
- action-age calculation;
- queue threshold behavior;
- horizon behavior;
- paired initial states;
- RTC inputs;
- missing episodes;
- duplicated episode IDs;
- confidence interval code.

Implement a one-time request latency pulse:

```python
if first_request_started_in_target_phase and not pulse_already_used:
    added_latency_ms += pulse_latency_ms
    pulse_already_used = True
```

The pulse must affect the request that starts in the target phase, not an arbitrary later request.

Log:

```text
pulse_target_phase
pulse_triggered
pulse_request_id
pulse_request_step
pulse_added_latency_ms
pulse_response_step
```

## Person 3: baseline compatibility audit

Create `docs/BASELINE_COMPATIBILITY.md` with one row per baseline:

```text
baseline
official repository
framework
base model
training required
checkpoint availability
LIBERO support
expected integration effort
fair comparison variables
status
```

Required entries:

- synchronous π0.5;
- naive asynchronous queue;
- RTC;
- VLASH;
- FASTER;
- one adaptive-horizon representative for later work.

Clone and pin the official VLASH repository in a separate workspace or environment. Inspect:

- `pyproject.toml`;
- π0.5 training config;
- async inference config;
- state offset or future-state inputs;
- checkpoint loading;
- LIBERO benchmark code;
- action normalization;
- control frequency;
- action quantization settings.

Do not run a numerical comparison yet.

## Day 4 deliverables

```text
outputs/summaries/days1_3_audit.md
outputs/summaries/phase_resolution.csv
outputs/videos/phase_annotation_*.mp4
docs/BASELINE_COMPATIBILITY.md
```

## Day 4 gate

Proceed only when:

- Days 1–3 audit has no unresolved correctness failure;
- at least the selected spatial and goal tasks have valid phase labels;
- a latency pulse can be tied to one exact request;
- VLASH requirements are documented without assumptions.

---

# Day 5 — Phase-triggered latency tolerance

## Scientific experiment

Inject the same one-time 700 ms latency pulse at different task phases.

Use the selected:

- LIBERO-Spatial task;
- LIBERO-Goal task.

Required strategies:

```text
naive_async
rtc
```

Required phases:

```text
transit
approach
precision_or_contact
```

Use `precision_or_contact` as a trigger group:

1. trigger at the first `precision` request;
2. if no request begins in precision, trigger at the first `contact` request;
3. if neither occurs, mark the episode invalid for that phase condition.

All non-pulse policy requests use native measured latency.

## Run matrix

```text
2 tasks
× 3 trigger phases
× 2 strategies
× 5 seeds
= 60 episodes
```

Reuse Days 1–3 native-latency episodes as no-pulse controls only when every other configuration field matches.

## Required metrics

- success;
- logical completion time;
- request latency;
- action age after the pulse;
- maximum post-pulse action age;
- queue underrun steps;
- hold steps;
- discarded actions;
- action jerk;
- phase at first failure indicator, when observable;
- remaining episode return or success.

Define:

```text
pulse_to_fresh_action_ms
```

as the time from the pulse-triggering observation capture to the first executed action sourced from the delayed request.

## Person assignments

### Person 1

- verify phase triggers visually;
- inspect invalid or missing phase episodes;
- confirm object/contact resolution.

### Person 2

- run the full phase-pulse matrix;
- validate pulse timing and provenance;
- produce episode summaries.

### Person 3

- produce phase-conditioned plots;
- compute paired differences between RTC and naive async;
- inspect whether the pulse changes continuity, freshness, or both.

## Required figures

```text
outputs/figures/success_by_pulse_phase.png
outputs/figures/action_age_by_pulse_phase.png
outputs/figures/pulse_to_fresh_action.png
outputs/figures/queue_underruns_by_pulse_phase.png
```

## Day 5 gate

The task-phase hypothesis remains viable when at least one task shows a material difference between transit and precision/contact under the same pulse.

If no phase effect appears:

- verify trigger correctness;
- verify the task actually reaches precision/contact;
- do not invent a phase-conditioned conclusion;
- continue with dynamic intervention because unexpected scene change tests a different mechanism.

---

# Day 6 — Dynamic target displacement

## Scientific experiment

Move the task’s target object during execution without clearing the queue or canceling an outstanding request.

Use the selected LIBERO-Spatial task.

Trigger:

```text
first transition into approach phase
```

Intervention:

```yaml
name: target_shift_5cm
translation:
  preferred_axis: world_x
  magnitude_m: 0.05
preserve:
  - z_position
  - orientation
reset:
  - linear_velocity
  - angular_velocity
```

If positive x is invalid or causes overlap, use negative x. Record the actual displacement vector.

Do not intervene when:

- the target is already grasped;
- the target cannot be resolved;
- the final pose would be outside the workspace;
- the move causes immediate invalid collision.

Mark such episodes invalid for intervention analysis rather than silently changing the trigger.

## Required strategies

```text
ideal_sync
blocking_sync
naive_async
rtc
```

Conditions:

```text
ideal_sync: ideal logical latency
blocking_sync: native_plus_700
naive_async: native and native_plus_700
rtc: native and native_plus_700
```

## Run matrix

```text
ideal_sync:
  1 condition × 5 seeds = 5 episodes

blocking_sync:
  1 condition × 5 seeds = 5 episodes

naive_async:
  2 conditions × 5 seeds = 10 episodes

rtc:
  2 conditions × 5 seeds = 10 episodes

total = 30 episodes
```

## Reaction metrics

For each intervention episode, log:

```text
intervention_step
intervention_logical_time
last_pre_intervention_observation_id
first_post_intervention_observation_id
first_post_intervention_request_id
first_executed_action_from_post_intervention_observation
fresh_action_reaction_latency_ms
pre_intervention_actions_executed_after_intervention
post_intervention_queue_underruns
recovery_success
```

The first fresh action must be determined by observation provenance, not by inference completion time.

## Person assignments

### Person 1

- implement and test target displacement;
- validate workspace safety;
- confirm reset restores the original scene;
- generate before/after intervention videos.

### Person 2

- implement reaction metrics;
- run the 30-episode matrix;
- validate source-observation logic.

### Person 3

- compare reaction latency, stale-action count, jerk, and recovery;
- determine whether RTC primarily improves continuity or reaction.

## Required figures

```text
outputs/figures/fresh_action_reaction_latency.png
outputs/figures/stale_actions_after_intervention.png
outputs/figures/recovery_success_after_intervention.png
outputs/figures/intervention_timeline_examples.png
```

---

# Day 7 — Static OOD interaction and VLASH smoke gate

## Part A: LIBERO-plus static perturbations

Use a separate environment or container:

```text
async-vla-libero-plus
```

Do not uninstall vanilla LIBERO from the validated base environment.

Record:

- LIBERO-plus repository SHA;
- asset revision;
- LeRobot SHA;
- package versions;
- selected task mapping;
- camera configuration.

Use the same selected spatial task when the task ID and instruction map exactly. If mapping differs, document it and stop the matched comparison.

Required perturbations:

### Object-layout shift

```yaml
name: object_layout_shift
target_displacement_m: 0.05
axis: workspace_safe_world_x
```

### Camera shift

```yaml
name: camera_shift
translation_m: 0.05
yaw_degrees: 5
camera: agentview
wrist_camera_unchanged: true
```

Required strategies:

```text
naive_async
rtc
```

Required latency profiles:

```text
native
native_plus_700
```

Run matrix:

```text
2 perturbations
× 2 latency profiles
× 2 strategies
× 5 seeds
= 40 episodes
```

Reuse matched unperturbed episodes from Days 1–3 where valid.

Report zero-delay or native OOD success separately. If the perturbation causes near-zero success even without added delay, state that latency interaction cannot be isolated.

## Part B: VLASH smoke gate

VLASH may be run only when all of the following are verified:

1. the implementation can evaluate a π0.5 policy on the selected LIBERO task;
2. the checkpoint includes the future-state-aware training required by the method, or the official code explicitly supports inference without it;
3. observation keys and normalization match;
4. action parameterization matches relative LIBERO control;
5. action horizon and control frequency are known;
6. logging can expose source observation, request time, and executed action;
7. no action quantization or speedup setting is enabled unless it is an explicit comparison variable.

Do not label a generic async π0.5 run as VLASH.

If compatible:

Run one selected spatial task:

```text
2 latency profiles
× 5 seeds
= 10 episodes
```

Use:

```text
native
native_plus_700
```

Record the exact checkpoint and config.

If incompatible or no compatible checkpoint is available:

- do not create approximate results;
- write a blocker report;
- specify whether training is required;
- estimate the smallest fair reproduction for the next week.

## Person assignments

### Person 1

- own LIBERO-plus environment and perturbation reset correctness;
- verify task mapping.

### Person 2

- adapt common logging and execution metrics to LIBERO-plus;
- run the 40 OOD episodes.

### Person 3

- complete VLASH compatibility audit;
- run the smoke matrix only if the gate passes;
- document all config differences.

## Required outputs

```text
outputs/summaries/libero_plus_environment.json
outputs/summaries/ood_results.csv
outputs/summaries/ood_delay_interaction.csv
outputs/summaries/vlash_compatibility.md
outputs/summaries/vlash_smoke.csv  # only if valid
```

---

# Day 8 — Consolidation, optional VLASH extension, and FASTER audit

## Shared priority

Complete required validation and determine whether the project has a workshop-level empirical finding.

Do not spend Day 8 forcing a broken baseline integration while required experiment logs remain invalid.

## Person 1

- rerun failed or invalid intervention/OOD episodes;
- verify reset isolation;
- complete phase and perturbation videos;
- document simulator limitations.

## Person 2

- run `validate_days4_8.py`;
- aggregate matched-seed results;
- compute confidence intervals;
- verify no results mix vanilla LIBERO and LIBERO-plus metadata;
- generate final metric tables.

## Person 3

If VLASH smoke succeeds:

- extend VLASH to the selected goal task or increase seeds;
- compare only matched tasks and latency profiles.

If VLASH smoke fails:

- finalize the compatibility report;
- do not present paper-reported numbers as your measurements.

Perform a FASTER feasibility audit only:

- clone and pin the official FASTER repository;
- record its OpenPI/JAX dependency;
- inspect LIBERO instructions;
- determine whether an official compatible LIBERO FASTER checkpoint is available;
- determine whether Horizon-Aware Schedule training is required;
- estimate memory and training requirements;
- identify metrics needed for TTFA and streaming actions.

Write:

```text
outputs/summaries/faster_feasibility.md
```

A full FASTER numerical comparison is not required for Days 4–8.

---

## 9. Required run summary

Maximum planned new episodes:

| Experiment | Episodes |
|---|---:|
| Phase-triggered pulse | 60 |
| Dynamic target displacement | 30 |
| Static LIBERO-plus OOD | 40 |
| VLASH smoke, conditional | 10 |
| **Maximum** | **140** |

Runs may reuse exact matched controls from Days 1–3.

Do not increase this matrix until required logs validate.

---

## 10. Logging additions

Extend action rows with:

```text
task_phase
eef_target_distance_m
target_contact
pulse_target_phase
pulse_triggered
intervention_name
intervention_active
post_intervention_observation
environment_variant
baseline_repository_sha
baseline_checkpoint_revision
```

Extend request rows with:

```text
phase_at_request
one_time_pulse_ms
future_state_target_step
future_state_source
time_to_first_action_ms
```

The VLASH-specific fields may be null for non-VLASH baselines.

Every result must include an environment fingerprint. Never aggregate results when fingerprints differ unexpectedly.

---

## 11. Statistical reporting

Use paired seeds and identical initial states wherever supported.

Report:

- success rate with Wilson 95% interval;
- mean and median action age;
- p95 action age;
- mean fresh-action reaction latency;
- stale actions executed after intervention;
- queue underrun rate;
- action jerk;
- logical completion time;
- number of policy requests;
- total GPU inference time.

Use bootstrap confidence intervals over episodes for continuous metrics.

With five seeds, label all findings preliminary. Avoid relying only on significance tests. Report effect sizes and raw counts.

For phase pulses, compare:

```text
precision/contact pulse minus transit pulse
```

For OOD-delay interaction, report the difference-in-differences and all four underlying success rates.

For VLASH, compare only matched:

- checkpoint family;
- task;
- seed;
- control frequency;
- latency profile;
- horizon;
- action parameterization.

---

## 12. Validation requirements

`validate_days4_8.py` must fail when:

- a pulse fires more than once;
- a phase pulse fires outside its requested phase;
- an intervention is logged without the target moving;
- target displacement leaks across resets;
- camera changes leak across resets;
- a fresh-action reaction metric references a pre-intervention observation;
- an invalid intervention episode is included in reaction aggregates;
- vanilla LIBERO and LIBERO-plus rows are mixed without an environment field;
- a VLASH result lacks an official config and compatible checkpoint record;
- action quantization differs across baselines without explicit labeling;
- request or action timestamps are nonmonotonic;
- provenance references are missing;
- control frequencies differ in a matched comparison;
- horizons differ in a matched comparison;
- Days 1–3 checkpoint revision differs from Days 4–8.

---

## 13. Commands

Provide commands resembling:

```bash
python async_vla_benchmark/scripts/audit_days1_3.py \
  --output-dir async_vla_benchmark/outputs

python async_vla_benchmark/scripts/run_phase_pulses.py \
  --config async_vla_benchmark/configs/days4_8.yaml \
  --resume

python async_vla_benchmark/scripts/run_dynamic_interventions.py \
  --config async_vla_benchmark/configs/days4_8.yaml \
  --resume

python async_vla_benchmark/scripts/run_libero_plus.py \
  --config async_vla_benchmark/configs/ood.yaml \
  --resume

python async_vla_benchmark/scripts/inspect_vlash.py \
  --repo-path ../vlash

python async_vla_benchmark/scripts/run_vlash_smoke.py \
  --config async_vla_benchmark/configs/days4_8.yaml \
  --resume

python async_vla_benchmark/scripts/validate_days4_8.py \
  --output-dir async_vla_benchmark/outputs

python async_vla_benchmark/scripts/make_days4_8_figures.py \
  --output-dir async_vla_benchmark/outputs
```

All run scripts must support:

```text
--dry-run
--resume
--seed
--task
--strategy
--latency-profile
--overwrite
```

`--dry-run` must print the exact planned matrix without loading a policy.

---

## 14. Required figures

```text
outputs/figures/success_by_pulse_phase.png
outputs/figures/action_age_by_pulse_phase.png
outputs/figures/pulse_to_fresh_action.png
outputs/figures/fresh_action_reaction_latency.png
outputs/figures/stale_actions_after_intervention.png
outputs/figures/recovery_success_after_intervention.png
outputs/figures/ood_delay_interaction.png
outputs/figures/continuity_vs_reaction_tradeoff.png
outputs/figures/baseline_comparison.png  # include VLASH only if valid
```

The continuity-versus-reaction figure should place, for each method:

- x-axis: fresh-action reaction latency or stale actions after intervention;
- y-axis: action jerk or continuity cost;
- marker annotation: success rate.

This tests whether a method is smooth, reactive, both, or neither.

---

## 15. Days 4–8 report

Create:

```text
async_vla_benchmark/outputs/summaries/days4_8_report.md
```

Answer:

1. Did the same latency pulse have different effects across task phases?
2. Were precision/contact phases less delay-tolerant than transit?
3. Did RTC reduce action discontinuity?
4. Did RTC reduce stale-action exposure after target movement?
5. How many pre-intervention actions were executed after the target moved?
6. Did OOD perturbations amplify delay degradation?
7. Was the OOD-delay interaction driven by perception failure at native latency?
8. Did the best fixed horizon from Days 1–3 remain best under perturbations?
9. Was VLASH reproduced fairly?
10. If VLASH ran, did it improve reaction, continuity, or both?
11. Is FASTER reproducible with an available official LIBERO checkpoint, or does it require training?
12. What is the strongest defensible workshop claim?
13. What result would still be needed before writing the paper?
14. Which methods must be added next?

---

## 16. Go/no-go criteria

### Continue toward a workshop paper when at least three are observed

- phase-triggered delay produces meaningfully different outcomes;
- dynamic target movement causes measurable stale-action exposure;
- RTC improves continuity but leaves a distinct reaction gap;
- OOD and delay have a nontrivial interaction;
- fixed-horizon ranking changes across phase or perturbation;
- VLASH changes the failure profile relative to RTC;
- synchronous model ranking or native success does not predict delayed behavior;
- the instrumentation reveals action-age effects not captured by raw inference latency.

### Reframe or stop when

- phase pulses have no measurable effect after trigger validation;
- target displacement does not create stale-action exposure;
- OOD failure is already near total at native latency;
- all asynchronous strategies are statistically and practically indistinguishable;
- results depend entirely on one unstable task;
- environment resets are not reproducible;
- the exact policy checkpoint cannot be held fixed;
- the benchmark cannot fairly integrate any strong recent asynchronous baseline.

---

## 17. Completion response

When Days 4–8 are complete, report:

1. files added and modified;
2. repository, checkpoint, and environment revisions;
3. selected tasks;
4. planned and completed episode counts;
5. failed, skipped, and invalid episodes;
6. phase-resolution success;
7. intervention and reset validation;
8. OOD environment fingerprint;
9. VLASH compatibility result;
10. FASTER feasibility result;
11. key effect sizes;
12. validation status;
13. paths to figures and summaries;
14. remaining scientific and engineering risks.

Do not claim completion when only code exists. Required experiments must have validated output files.
