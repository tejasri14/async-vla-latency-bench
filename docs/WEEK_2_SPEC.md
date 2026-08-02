# Week 2 Specification: LIBERO-Plus OOD × Delay Factorial Study

**Prerequisite:** Days 4–8 decision gate passed  
**Primary model:** same pinned π0.5 checkpoint  
**Primary methods:** `naive_async`, `rtc`  
**Scientific question:** Does visual distribution shift reduce tolerance to
asynchronous action staleness?

Do not add VLASH or SmolVLA during Week 2.

---

## 1. Scope

Evaluate selected static distribution shifts separately from the dynamic
interventions used in Days 4–8.

Required OOD families:

1. object-layout change;
2. external-camera change.

The minimum deliverable is an ID/OOD × low/high delay factorial study with
matched execution methods.

Do not initially add:

- lighting;
- texture;
- language paraphrase;
- sensor noise;
- novel object identity;
- multiple severity levels.

---

## 2. Separate environment

LIBERO-Plus may replace or conflict with vanilla LIBERO under the same package
namespace. Use a separate environment or container.

Recommended name:

```text
stalebench-libero-plus
```

Do not uninstall or mutate the validated vanilla-LIBERO environment.

Record:

```text
LeRobot git SHA
LIBERO-Plus git SHA
asset revision
checkpoint revision
Python version
PyTorch version
CUDA version
GPU
MuJoCo version
Robosuite version
camera configuration
task mapping
```

Write:

```text
async_vla_benchmark/outputs/libero_plus/environment.json
```

---

## 3. Task mapping gate

Use:

- selected LIBERO-Spatial task;
- selected LIBERO-Goal task only when an exact LIBERO-Plus mapping exists.

An exact mapping requires:

- same task identity;
- same language instruction or documented official equivalent;
- same action space;
- same control mode;
- same camera keys;
- compatible initial-state convention;
- compatible success predicate.

If exact mapping fails, do not present the condition as matched. Restrict the
study to the task with a verified mapping.

Create:

```text
outputs/summaries/libero_plus_task_mapping.csv
```

Columns:

```text
vanilla_suite
vanilla_task_id
vanilla_task_name
plus_variant
instruction_match
action_space_match
camera_match
success_predicate_match
mapping_status
notes
```

---

## 4. Experimental factors

### Scene condition

```text
ID
OOD
```

### Delay

```text
native
native_plus_700
```

### Method

```text
naive_async
rtc
```

### OOD families

#### Object layout

Use an official matching LIBERO-Plus object-layout variant.

#### Camera

Use an official matching external-camera variant.

Do not manually perturb vanilla LIBERO and label the result as LIBERO-Plus.

---

## 5. Minimum run matrix

Prioritize one verified task first.

Per task and OOD family:

```text
2 scene conditions
× 2 delay profiles
× 2 methods
× 5 paired seeds
= 40 episodes
```

Minimum with one task and two OOD families:

```text
80 episodes
```

Optional expansion to the second verified task:

```text
+80 episodes
```

Reuse exact ID controls only when:

- environment fingerprint;
- task;
- seed;
- checkpoint;
- method;
- delay;
- horizon;
- camera;
- normalization

all match.

---

## 6. Primary interaction

For success:

```text
I =
  [S(OOD, delayed) - S(OOD, native)]
  -
  [S(ID, delayed) - S(ID, native)]
```

Report:

- all four cell values;
- raw success counts;
- Wilson intervals;
- bootstrap interval for `I`.

Do not interpret `I` when OOD native success is already near zero.

---

## 7. Required metrics

- success;
- logical completion time;
- request latency;
- mean and p95 action age;
- queue occupancy;
- queue underruns;
- hold steps;
- discarded actions;
- action delta, acceleration, and jerk;
- policy requests;
- GPU milliseconds.

Where an OOD variant supports a compatible intervention:

- stale-action count;
- stale duration;
- fresh-action reaction latency.

Dynamic intervention under OOD is optional and should be added only after the
required factorial matrix is complete.

---

## 8. Limited horizon ablation

Use one task and one informative OOD family.

Compare:

```text
horizon 10
best global horizon selected from Days 1–3
```

Conditions:

```text
method: naive_async, rtc
scene: ID, OOD
delay: native_plus_700
seeds: [0, 1, 2]
```

Do not tune a new OOD-specific horizon.

---

## 9. Team ownership

| Person | Primary ownership |
|---|---|
| Person 1 | separate environment, official variants, task mapping, reset and asset validation |
| Person 2 | common runner adapter, factorial runs, failed-run recovery |
| Person 3 | interaction analysis, statistics, figures, fairness audit |

---

## 10. Validation

Fail when:

- task mapping is not documented;
- ID and OOD environment fingerprints are missing;
- camera/object changes leak across episodes;
- different checkpoint revisions are aggregated;
- normalization differs;
- control frequency differs;
- reused ID controls do not match;
- OOD labels are inferred instead of read from config;
- interaction is computed from unmatched cells without disclosure.

---

## 11. Required outputs

```text
outputs/libero_plus/environment.json
outputs/libero_plus/episodes.csv
outputs/libero_plus/requests.csv
outputs/libero_plus/actions/

outputs/summaries/libero_plus_task_mapping.csv
outputs/summaries/ood_factorial.csv
outputs/summaries/ood_delay_interactions.csv
outputs/summaries/week2_report.md
```

Figures:

```text
outputs/figures/ood_delay_interaction.png
outputs/figures/ood_action_age.png
outputs/figures/ood_continuity.png
outputs/figures/ood_method_ranking.png
outputs/figures/ood_cell_counts.png
```

---

## 12. Decision gate

Continue to Week 3 when at least one holds:

- nontrivial OOD-delay interaction;
- method ranking changes under OOD + delay;
- action age reveals degradation not predicted by static OOD success;
- RTC's continuity advantage persists while freshness differs;
- delay adds information beyond static OOD difficulty.

Stop the OOD branch when:

- static OOD success is near zero;
- temporal effects cannot be separated;
- task mapping is not fair;
- all cells are dominated by simulator or perception failure.

---

## 13. Week 2 report questions

1. What is native-delay success for each OOD family?
2. Does added delay disproportionately harm OOD scenes?
3. Is the interaction consistent across seeds?
4. Does OOD change model runtime or behavioral tolerance?
5. Does RTC remain smoother under OOD?
6. Does RTC become fresher under OOD?
7. Does horizon choice change the interaction?
8. Which OOD family belongs in the main paper?
