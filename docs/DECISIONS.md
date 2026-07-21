# Decisions

Last updated: 2026-07-20

## Scope and architecture

1. Keep all benchmark work in the isolated `async_vla_benchmark/` package.
   LeRobot core files will not be modified unless a pinned installed revision makes
   an upstream change unavoidable.
2. Implement only the Days 1–3 conditions: ideal synchronous, blocking synchronous,
   naive asynchronous queue, RTC, and the fixed execution-horizon sweep.
3. Use a discrete-event logical clock. Added latency will never be implemented with
   `sleep()` or real-time pacing.
4. Permit at most one outstanding policy request and retain observation/chunk/action
   provenance through every queue operation.
5. Keep the discrete-event runner behind minimal `EpisodeEnvironment` and
   `PolicyRequestExecutor` protocols. This permits dependency-free semantic tests while
   deferring concrete adapters until the installed, pinned LeRobot APIs can be inspected.
6. Write request and action Parquet files atomically, then write the terminal episode JSON
   last. The terminal JSON is the episode completion marker used by future resume logic.

## Dependency and revision handling

1. Current upstream LeRobot source may guide scaffolding, but it is not treated as the
   installed experimental revision. Experimental adapters must be checked again against
   the pinned local checkout.
2. Repository, checkpoint, and dataset revisions must be explicit before real execution.
   Missing revisions cause an actionable failure rather than an implicit latest-version
   lookup.
3. The environment control frequency must be obtained from the pinned environment.
   The benchmark will not silently assume a frequency.
4. Real policy loading requires CUDA. The present macOS host is suitable only for
   dependency-free implementation checks and dry-run planning.

## Latency and RTC semantics

1. Convert each request's measured end-to-end latency to logical delay with `ceil`.
   A global average latency is not valid for RTC or other execution strategies.
2. Define action age from the source observation control step, not policy completion
   time.
3. Pass `inference_delay`, `prev_chunk_left_over`, and `execution_horizon` through the
   current RTC-capable π0.5 chunk path. Add a pinned-revision regression test before RTC
   experiments.
4. Treat the initial queue fill as ideal startup or record it separately; it must not be
   silently mixed into steady-state latency measurements.
5. Require an RTC request executor to report the exact `rtc_delay_steps` it passed to the
   policy. The runner rejects a non-startup RTC response when that value differs from the
   delay calculated from that request's measured latency and selected profile.

## Evidence and reporting

1. Smoke tests, compilation, and dry runs are implementation evidence only.
2. An experiment is complete only when its required output exists and passes result
   validation.
3. Aggregate figures must not be generated until validation passes.
4. The diagnostic `outputs/environment.json` currently has `status: not_ready` and is
   not an experimental result.
5. Deterministic fake-adapter episode tests are evidence for orchestration semantics only.
   They do not validate LIBERO dynamics, π0.5 tensor processing, CUDA timing, or RTC
   denoising behavior.

## Handoff decision

Do not extend the abstract adapters from documentation or current upstream examples. The
next implementation step must occur against the exact pinned Linux/CUDA/EGL checkout: inspect
the installed environment and policy APIs, pin all three revisions, and then implement the
two concrete protocols used by `benchmark/runner.py`.

## CUDA-laptop execution decision

1. Modal/cloud execution was considered and explicitly abandoned. The benchmark will run on
   the user's CUDA-capable laptop; do not add Modal files or cloud-specific abstractions.
2. Treat the new laptop as a fresh experimental host. Do not copy the macOS
   `outputs/environment.json` or infer readiness from these dependency-free tests.
3. Keep one Python environment, one LeRobot checkout/commit, one checkpoint revision, one
   dataset revision, and one GPU for task selection, profiling, core runs, and the horizon
   sweep. If any pinned component changes, create a new environment record and do not merge
   the resulting episodes into the old run.
4. Inspect the installed LeRobot source before implementing concrete adapters. In particular,
   locate the actual LIBERO environment factory/wrapper, observation preprocessing pipeline,
   action postprocessor, π0.5 `predict_action_chunk` signature, RTC processor initialization,
   and queue merge behavior.
5. Execute all policy requests serially (`eval_batch_size=1`, one task and at most one request
   outstanding). Use CUDA synchronization around measured inference and
   `time.perf_counter_ns()` for end-to-end request stages.
6. Progress through gates: setup readiness, adapter tests, one ideal episode, task selection,
   native profiling, one-task core smoke matrix, full core matrix, RTC regression, horizon
   sweep, validation, figures, and report. A failed gate stops later gates.

## Source-control handoff warning

At the time of this handoff, `HEAD` is
`07f90075df2d0a202949e3737ba2c04b2dd2b201`, but this working tree also contains modified and
untracked runner/logging/test files. The next agent must begin with `git status --short` and
verify that `benchmark/runner.py`, `benchmark/logging.py`, `tests/test_runner.py`, and the
changes to `benchmark/execution.py` and these handoff documents are present in the commit
installed on the CUDA laptop. Do not assume the current `HEAD` contains them.
