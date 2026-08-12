# Implementation Status

Last updated: 2026-08-12

## Active stage

```text
STAGE 0 — ID-ONLY LATENCY CALIBRATION
```

## Existing prerequisite

Prior work indicates that a π0.5 LIBERO harness with Naive async and RTC exists. Revalidate the current repository/checkpoint/environment before using new results.

## Stage 0

- [ ] Pin LeRobot revision
- [ ] Pin π0.5 checkpoint revision
- [ ] Validate CUDA/EGL environment
- [ ] Verify exact standard-LIBERO task names at IDs 2 / 0 / 2
- [ ] Validate frozen `n_action_steps=25`
- [ ] Validate Naive async semantics
- [ ] Validate RTC semantics
- [ ] Validate request-specific logical delay
- [ ] Validate action-age calculation
- [x] Record revised 180-run calibration manifest (`3 × 2 × 5 × 6`)
- [x] Run 180 revised calibration episodes
- [ ] Validate missing/invalid cells
- [ ] Generate calibration plots/tables
- [ ] Write `selected_high_delay.json`
- [ ] Freeze `d*`

## Stage 1

- [ ] Create separate LIBERO-Plus environment
- [ ] Pin LIBERO-Plus SHA
- [ ] Resolve all 21 OOD variants
- [ ] Verify `classification_id` ↔ exact task name ↔ API index
- [ ] Save `stage1_resolved_variants.csv`
- [ ] Freeze variants before outcomes
- [ ] Generate 480-row Stage 1 analysis manifest
- [ ] Confirm ID controls match Stage 0
- [ ] Run 420 new OOD episodes
- [ ] Run 36 additional ID-control episodes for Stage 1 seeds 2/3/4
- [ ] Validate all factorial cells
- [ ] Generate seven required summary tables
- [ ] Generate interaction heatmaps
- [ ] Generate task-demand / mechanism-group plots
- [ ] Generate action-age diagnostics
- [ ] Write `STAGE_1_OBSERVATIONS.md`
- [ ] Apply the frozen Stage 2 selection rule

## Stage 2

- [ ] Freeze selected candidate interactions
- [ ] Freeze held-out seed set before execution
- [ ] Run held-out confirmation
- [ ] Report held-out results separately from exploratory screen
- [ ] Compute intervals/effect sizes
- [ ] Decide final paper claim
- [ ] Freeze results

## Paper

- [ ] Finalize related work
- [ ] Finalize experimental taxonomy language
- [ ] Generate main figures from scripts
- [ ] Include complete Stage 1 screen
- [ ] Include null/counterintuitive results
- [ ] Audit every claim against a result
- [ ] Write limitations
- [ ] Reproducibility audit
- [ ] Final manuscript

## Current blockers

Record only concrete blockers here.

```text
The revised Stage 0 design (`n_action_steps=25`, six seeds, 0–400 ms) is accepted
by D016; missing 500–700 ms cells are not a blocker. Required revision/environment
identity fields are still absent. See K015-K016.
Trace audit also found 23 hold/underrun actions without canonical provenance in
seven episodes despite all summaries being marked `ok`; see K017.
```

## Analysis artifacts

- `output/pdf/stage0_latency_calibration_audit.pdf` (revised to include the
  matched 10-action versus 25-action evidence, alternative explanations,
  evidence-strength limits, critical decision criteria, and a six-seed pooled
  delay-selection table/curve)
- `output/pdf/stage0_n_action_steps_10_vs_25_analysis.pdf`
- `docs/STAGE_0_N_ACTION_STEPS_25_CONDUCT.md`

## Exact next action

```text
Freeze the Stage 0 `d*` artifact under D016, validate provenance and hold-action
handling, then generate the Stage 1 manifest with `n_action_steps=25` and seeds
`0, 1, 2, 3, 4`.
```
