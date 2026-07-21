# Days 1–3 Implementation Status

Last updated: 2026-07-20

Current state: implementation is partial and experimental execution has not started.
The dependency-free tests, syntax check, and dry-run matrix checks validate only local
implementation; they are not benchmark episodes and do not satisfy any experimental
completion criterion.

## Scope

- [x] Scope limited to ideal synchronous, blocking synchronous, naive asynchronous queue, RTC, and fixed execution horizons.
- [x] No policy training, OOD perturbations, dynamic interventions, VLASH, FASTER, DEHP, SmolVLA, or OpenVLA.

## Inspection and environment

- [x] Read `AGENTS.md`, `docs/RESEARCH_CONTEXT.md`, and `docs/DAYS_1_3_SPEC.md` completely.
- [x] Inspected workspace and all discovered Python environments.
- [x] Inspected current upstream LeRobot π0.5, RTC, and LIBERO APIs as a scaffolding reference.
- [ ] Pin local LeRobot Git commit (blocked: no LeRobot checkout or installation).
- [ ] Pin checkpoint and dataset revision SHAs (blocked: artifacts not installed/downloaded).
- [ ] Validate Linux/CUDA/EGL execution environment (blocked: current host is macOS without CUDA stack).

## Implementation

- [x] Create isolated benchmark package structure.
- [x] Implement latency conversion, provenance, queue, logical clock, RTC call adapter, metrics, and guarded environment/policy adapters.
- [x] Implement and fake-adapter test the discrete-event episode runner for all four strategies.
- [x] Implement atomic request/action Parquet and terminal episode JSON output primitives.
- [ ] Complete production episode execution and output logging (logical runner and writers
  exist; pinned LIBERO/π0.5 adapters and real Parquet schema exercise remain).
- [ ] Implement setup, task selection, profiling, benchmark, validation, and figure scripts.
- [x] Implement initial latency, action-age, naive-queue, horizon, and RTC tests.

## Validation and experiments

### Implementation-only checks

- [x] Dependency-free latency smoke test passes (`0/1/100/101/300/700 ms`).
- [x] Package syntax compilation passes under Python 3.10.18.
- [x] Core dry-run expands to 150 episodes; horizon dry-run expands to 108 maximum episodes.
- [x] Full dependency-free pytest suite passes (12 tests via the available Anaconda pytest environment).

### Commands run on 2026-07-20

```bash
PYTHONPATH=. /Users/tejasrikurapati/opt/anaconda3/bin/pytest -q
/Users/tejasrikurapati/.pyenv/shims/python3.10 -m compileall -q async_vla_benchmark
PYTHONPATH=. /Users/tejasrikurapati/.pyenv/shims/python3.10 \
  async_vla_benchmark/scripts/run_benchmark.py \
  --config async_vla_benchmark/configs/days1_3.yaml \
  --experiment core --dry-run
git diff --check
```

Results: `12 passed in 0.03s`; Python 3.10 compilation succeeded; the core dry run
printed `planned_episodes=150`; and `git diff --check` reported no errors. An earlier
attempt with `/Users/tejasrikurapati/.pyenv/shims/python3.10 -m pytest -q` failed because
that interpreter does not have pytest installed.

### Experimental completion criteria

- [ ] Execution environment metadata captured from the required Linux/CUDA/EGL host.
- [ ] Exact checkpoint loads on CUDA.
- [ ] Three viable tasks selected.
- [ ] 100 measured native requests profiled.
- [ ] Core episode logs validated.
- [ ] RTC verified with request-specific delays.
- [ ] Horizon sweep logs validated.
- [ ] Figures generated after validation.

Experimental completion: **not achieved**. There are no validated request, action,
episode, task-selection, native-latency, horizon-sweep, summary, or figure artifacts.

## Recorded deviations and failures

- 2026-07-20: Workspace contained only instructions and was not a Git repository.
- 2026-07-20: No installed `lerobot`, `libero`, `mujoco`, or `robosuite` package was found.
- 2026-07-20: No CUDA runtime/GPU is available on the macOS development host.
- 2026-07-20: No experiments have been run and no experimental output is claimed.
- 2026-07-20: Initial pytest invocation failed because pytest is not installed in the discovered Python 3.10 environment.
- 2026-07-20: An available Anaconda pytest environment was subsequently found; all 12 dependency-free tests pass. The pinned Python 3.10 environment still lacks pytest.
- 2026-07-20: `inspect_setup.py` wrote `outputs/environment.json` with `status: not_ready`; this is a setup diagnostic, not evidence of an experiment run.
- 2026-07-20: Work stopped with production episode execution, logging, result validation, and figure generation still incomplete.

## Exact next action

On the required Linux/CUDA/EGL host, create or locate the pinned LeRobot checkout and run
`inspect_setup.py`; then record its Git commit plus checkpoint and dataset revision SHAs in
`configs/days1_3.yaml`. Before changing the adapters, inspect that exact checkout's LIBERO
environment construction, π0.5 preprocessing/postprocessing, `predict_action_chunk`, and RTC
signatures. The first code change after inspection is to implement the concrete
`EpisodeEnvironment` and `PolicyRequestExecutor` adapters and exercise one ideal-sync smoke
episode without writing aggregate figures.

## CUDA-laptop handoff runbook

The new agent must read `AGENTS.md` and every file under `docs/` before changing code.

### 0. Verify the transferred repository

```bash
git status --short --branch
git rev-parse HEAD
git log -1 --oneline
test -f async_vla_benchmark/benchmark/runner.py
test -f async_vla_benchmark/benchmark/logging.py
test -f async_vla_benchmark/tests/test_runner.py
```

Expected benchmark commit at the time of handoff: base `HEAD`
`07f90075df2d0a202949e3737ba2c04b2dd2b201`, plus the runner/logging/test and documentation
changes listed above. Those changes are currently visible in the working tree but are not in
that base commit; confirm they were committed and transferred before proceeding.

### 1. Establish and pin the execution stack

Use Linux with an NVIDIA GPU. Create an isolated Python environment compatible with the
selected LeRobot revision. Clone LeRobot separately, choose and record an exact commit, and
install that checkout with the π and LIBERO extras as required by the specification:

```bash
git clone https://github.com/huggingface/lerobot.git
cd lerobot
git checkout <EXACT_COMMIT>
python -m pip install -e '.[pi,libero]'
python -m pip install pytest pyarrow pandas matplotlib pyyaml
export MUJOCO_GL=egl
```

Do not choose `<EXACT_COMMIT>` silently. Record why it was selected and place the full SHA in
`async_vla_benchmark/configs/days1_3.yaml`. Resolve immutable Hugging Face revision SHAs for
`lerobot/pi05_libero_finetuned` and `HuggingFaceVLA/libero`; record both in the same config.
Do not use floating `main` revisions during experiments.

### 2. Inspect before adapting

From the installed environment, inspect—not merely import—the exact implementation of:

- LIBERO environment creation, reset/seed/initialization-index behavior, termination and
  success reporting, action processing, and exposed control frequency;
- π0.5 checkpoint loading and device placement;
- observation preprocessing and action postprocessing;
- `predict_action_chunk`, RTC configuration/initialization, `inference_delay`,
  `prev_chunk_left_over`, `execution_horizon`, and RTC queue merge semantics.

Document API differences in `UPSTREAM_CHANGES.md` and add pinned-revision regression tests.
Do not modify LeRobot internals unless the adapter cannot represent the installed API.

### 3. Run setup and implementation gates

Run and improve `inspect_setup.py` until `outputs/environment.json` includes the LeRobot,
checkpoint, and dataset SHAs; Python/PyTorch/CUDA/driver/GPU versions; MuJoCo, Robosuite, and
LIBERO versions; and installed packages. It must fail readiness for missing revisions,
non-CUDA policy execution, or non-EGL MuJoCo setup.

Then implement concrete `EpisodeEnvironment` and `PolicyRequestExecutor` adapters, wire them
and the atomic writers into `run_benchmark.py`, and implement the missing scripts listed in
the specification. Run the full tests before a real episode. The first real run is exactly
one `ideal_sync`, horizon-10 smoke episode. Validate its request, action, and terminal episode
records before task selection.

### 4. Execute in this order

```bash
python async_vla_benchmark/scripts/inspect_setup.py
python async_vla_benchmark/scripts/select_tasks.py \
  --config async_vla_benchmark/configs/days1_3.yaml
python async_vla_benchmark/scripts/profile_latency.py \
  --config async_vla_benchmark/configs/days1_3.yaml \
  --warmup-requests 10 --measured-requests 100
python async_vla_benchmark/scripts/run_benchmark.py \
  --config async_vla_benchmark/configs/days1_3.yaml --experiment core --dry-run
python async_vla_benchmark/scripts/run_benchmark.py \
  --config async_vla_benchmark/configs/days1_3.yaml --experiment core
python async_vla_benchmark/scripts/validate_results.py \
  --output-dir async_vla_benchmark/outputs
python async_vla_benchmark/scripts/run_benchmark.py \
  --config async_vla_benchmark/configs/days1_3.yaml --experiment horizon_sweep
python async_vla_benchmark/scripts/validate_results.py \
  --output-dir async_vla_benchmark/outputs
python async_vla_benchmark/scripts/make_figures.py \
  --output-dir async_vla_benchmark/outputs
```

Do not blindly run commands for scripts that are still absent or incomplete. Implement and
test each gate first. Task selection must choose the first task in each suite reaching at
least 4/5 ideal successes. Native profiling must use observations from real rollouts, ten
warm-ups, and 100 measured calls. Run the one-task core smoke matrix and validate it before
the complete 150-episode core matrix. Run the horizon sweep only after RTC passes its
pinned-revision request-specific-delay regression test. Generate figures only after all
relevant logs pass validation.

### 5. Completion evidence

Before marking any experimental checkbox complete, record commands, exact revisions,
selected task IDs, completed/failed/skipped episode counts, validation results, and artifact
paths. Update all three handoff documents after every gate. Finish
`outputs/summaries/days1_3_report.md` only after the completion requirements in
`DAYS_1_3_SPEC.md` are satisfied or failures are explicitly documented.
