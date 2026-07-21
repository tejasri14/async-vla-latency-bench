# Known Issues

Last updated: 2026-07-20

## Blocking experimental execution

These were observed on the macOS development host. They must be re-audited on the CUDA
laptop; do not automatically carry them forward or mark them resolved without evidence.

1. **No pinned LeRobot checkout or installation.** This benchmark workspace is now a Git
   repository, but `lerobot` is not importable and no separate LeRobot commit can currently
   be recorded.
2. **Required simulation packages are absent.** `libero`, `mujoco`, and `robosuite` are
   not installed in the discovered Python environments.
3. **No CUDA/EGL execution host was available during implementation.** The original machine
   was macOS without CUDA. The intended replacement laptop has CUDA, but Linux compatibility,
   NVIDIA driver/CUDA versions, GPU memory, and headless MuJoCo EGL operation are not yet
   verified.
4. **Artifact revisions are unresolved.** The checkpoint and dataset revision SHAs have
   not been resolved or pinned.
5. **Control frequency is unresolved.** It cannot be measured from environment metadata
   until the pinned LIBERO environment is installed and instantiated.

## Incomplete implementation

1. A dependency-free discrete-event orchestration prototype and atomic output-writing
   utilities are implemented and tested with fake adapters. Concrete LIBERO rollout, π0.5
   preprocessing/postprocessing, CUDA request timing, and real output schemas remain
   unimplemented or unverified.
2. Task selection, native latency profiling, complete episode logging, resume validation,
   and figure generation scripts are not complete.
3. The result validator does not yet implement all failure conditions from the specification.
4. The current RTC wrapper is based on upstream source inspection and has not been verified
   against a pinned installed LeRobot revision or a real π0.5 checkpoint.
5. Parquet output dependencies and schemas have not been exercised.
6. `run_benchmark.py` still stops before real execution; it is not yet wired to selected-task
   manifests, concrete adapters, atomic output writers, or validated resume behavior.

## Test limitations

1. `pytest` is missing from the pinned Python 3.10 environment, but an available Anaconda
   pytest environment runs all 12 dependency-free tests successfully.
2. The test suite and package compilation passed, and dry-run counts matched the specified
   matrices. These checks do not exercise LeRobot, LIBERO, CUDA timing, RTC
   denoising, environment actions, or output validation.

## Output status

1. `async_vla_benchmark/outputs/environment.json` is a failed-readiness diagnostic with
   `status: not_ready`.
2. No validated experimental request, action, episode, task-selection, latency-profile,
   summary, report, or figure files exist.
3. No task has been selected, no checkpoint has loaded, and zero benchmark episodes have
   been run.

## Commands and observed results

- `PYTHONPATH=. /Users/tejasrikurapati/opt/anaconda3/bin/pytest -q` completed with
  `12 passed in 0.03s`.
- `/Users/tejasrikurapati/.pyenv/shims/python3.10 -m compileall -q async_vla_benchmark`
  completed successfully.
- The Python 3.10 core dry run completed with `planned_episodes=150`.
- `git diff --check` completed without errors.
- `/Users/tejasrikurapati/.pyenv/shims/python3.10 -m pytest -q` failed with
  `No module named pytest`; tests were therefore run with the available Anaconda pytest.

## Exact next action

Move to a Linux/CUDA/EGL host with the required artifacts, pin and record the LeRobot Git
commit and checkpoint/dataset revision SHAs, and inspect the installed π0.5 and LIBERO APIs.
Then implement the concrete runner adapters and execute one ideal-sync smoke episode. Until
that inspection occurs, do not guess API signatures, mark production execution complete, or
generate figures.

## CUDA-laptop risks and required checks

1. **Transferred commit may omit current work.** At handoff, Git `HEAD` is
   `07f90075df2d0a202949e3737ba2c04b2dd2b201`, while runner/logging/test additions and several
   edits are still working-tree changes. On the new laptop, verify those files and edits are
   present in the checked-out commit before installing dependencies.
2. **CUDA alone is insufficient.** Verify the laptop runs a supported Linux environment,
   `nvidia-smi`, CUDA-enabled PyTorch, and MuJoCo with `MUJOCO_GL=egl`. Windows-native or WSL
   execution must not be assumed compatible with LIBERO/EGL without a successful smoke test.
3. **GPU memory is unknown.** The exact π0.5 checkpoint must load on CUDA at batch size one.
   Do not substitute another checkpoint, reduce the policy, or silently fall back to CPU if
   it does not fit.
4. **Revision selection is unresolved.** The next agent must choose and record an exact
   LeRobot commit and immutable checkpoint/dataset SHAs before implementing adapters or
   producing experimental outputs.
5. **RTC has a measurement/API risk.** Confirm how the installed RTC path accepts
   request-specific `inference_delay` while request latency is measured. Do not replace it
   with a global mean or previous-request latency. If the installed API cannot satisfy the
   specified semantics, stop and document the deviation rather than claiming RTC completion.
6. **Environment reproducibility is unverified.** Confirm task IDs/names, language
   instructions, initialization indices, seeding, success signals, maximum episode length,
   action dimensionality, action clipping, and control frequency from the installed stack.
7. **Logging and resume are incomplete.** Exercise Parquet schemas with `pyarrow`, validate
   atomic completion markers, and ensure `--resume` skips only terminal episodes whose
   request/action/summary files pass validation.
8. **No cloud fallback is planned.** Modal was discussed and rejected in favor of the CUDA
   laptop. Do not add Modal integration unless the user explicitly reopens that decision.

The operational next action is repository-transfer verification followed by environment
inspection and revision pinning—not running the full matrix. Only after setup readiness and
one validated ideal-sync smoke episode should task selection and latency profiling begin.
