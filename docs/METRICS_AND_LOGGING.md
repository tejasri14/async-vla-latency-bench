# Metrics and Logging Specification

This file defines canonical terms for all stages.

---

## 1. Time bases

### Wall-clock time

Measured using a monotonic clock. Used for:

- preprocessing latency;
- model latency;
- postprocessing latency;
- full request latency;
- total experiment runtime.

### Logical control time

```text
logical_time = control_step × control_period
```

Used for:

- simulated request availability;
- action execution;
- queue behavior;
- action age;
- intervention timing.

---

## 2. Request latency

```text
request_latency =
  response_complete_wall_time - observation_capture_wall_time
```

Also record:

```text
preprocessing_latency
model_latency
postprocessing_latency
```

---

## 3. Logical delay

```text
delay_steps =
  ceil(total_logical_latency_ms / control_period_ms)
```

`ideal` uses zero logical delay but still records actual runtime.

---

## 4. Action age

```text
action_age =
  action_execution_logical_time
  -
  source_observation_logical_time
```

This is the primary freshness metric.

---

## 5. Stale action

For intervention time `t_i`:

```text
source_observation_time < t_i
and
action_execution_time >= t_i
```

---

## 6. Stale-action count

```text
N_stale =
  number of stale actions executed after intervention
```

---

## 7. Stale duration

```text
T_stale =
  last stale-action execution time - intervention time
```

Use zero when no stale action executes.

---

## 8. Fresh-action reaction latency

```text
T_fresh =
  first execution time of an action sourced from an observation captured after
  the intervention
  -
  intervention time
```

Do not substitute request completion, queue arrival, or generation completion.

---

## 9. Queue underrun

A control step at which no policy action is available and the configured hold
action executes.

---

## 10. Continuity

Calculate on robot-motion dimensions:

- action delta;
- acceleration;
- jerk.

Report gripper separately when included.

Document finite-difference conventions and control period.

---

## 11. OOD-delay interaction

```text
I =
  [S(OOD, delayed) - S(OOD, low_delay)]
  -
  [S(ID, delayed) - S(ID, low_delay)]
```

---

## 12. Compute usage

Record:

- policy calls;
- model/GPU milliseconds;
- full-request milliseconds;
- average queue occupancy;
- peak memory when available.

---

## 13. Required entities

### Observation

```text
observation_id
episode_id
control_step
logical_time
wall_time
task_suite
task_id
seed
environment_fingerprint
task_phase
```

### Request

```text
request_id
source_observation_id
request_step
request_logical_time
preprocess_ms
model_ms
postprocess_ms
request_ms
added_latency_ms
delay_steps
response_available_step
method
checkpoint_revision
```

### Chunk

```text
chunk_id
request_id
source_observation_id
chunk_length
availability_step
method
guided_prefix_length
```

### Executed action

```text
episode_id
control_step
execution_logical_time
action_vector
chunk_id
chunk_action_index
source_observation_id
source_observation_step
action_age_steps
action_age_ms
queue_depth_before
queue_depth_after
is_hold
is_underrun
task_phase
intervention_active
```

### Intervention

```text
intervention_id
episode_id
intervention_type
trigger_phase
trigger_step
logical_time
state_before
state_after
valid
invalid_reason
```

---

## 14. Provenance invariants

- every action references one chunk;
- every chunk references one request;
- every request references one observation;
- timestamps are monotonic;
- action age is nonnegative;
- no entity reference is missing;
- fresh/stale classification uses source-observation time;
- environment fingerprint is present;
- method and checkpoint revision are present.
