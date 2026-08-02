# StaleBench Agent Instructions

Read these files before changing code:

1. `docs/RESEARCH_CONTEXT.md`
2. `docs/METRICS_AND_LOGGING.md`
3. the active stage specification;
4. `docs/IMPLEMENTATION_STATUS.md`;
5. `docs/DECISIONS.md`;
6. `docs/KNOWN_ISSUES.md`.

## Project

Implement **StaleBench**, a simulation-only benchmark for temporal robustness of
asynchronous Vision-Language-Action execution.

The benchmark traces every executed action to its exact source observation and
action chunk, then measures how long pre-change actions remain in control after
a controlled scene change.

## Non-negotiable rules

- Keep the evaluated policy checkpoint frozen within each matched comparison.
- Do not use `sleep()` to simulate control delay.
- Use request-specific measured latency and a discrete logical clock.
- Preserve observation, request, chunk, and action provenance.
- Allow at most one outstanding request unless a named baseline officially
  requires otherwise.
- Do not clear the queue or cancel an in-flight request at intervention time.
- Do not label an approximation as RTC, VLASH, FASTER, Reflex, or another named
  method.
- Pin repository, checkpoint, dataset, simulator, and environment revisions.
- Validate logs before aggregation.
- Do not claim an experiment ran when only code was implemented.
- Record blockers and deviations in `docs/KNOWN_ISSUES.md`.
- Update `docs/IMPLEMENTATION_STATUS.md` before ending each session.

## Stage discipline

- Days 4–8: only task phases, phase-conditioned delay, and dynamic interventions.
- Week 2: LIBERO-Plus OOD × delay.
- Week 3: VLASH and SmolVLA; a streaming/corrective method only if fair and
  reproducible.
- Week 4: freeze results, ablations, statistics, writing, and release.

Do not pull work from a later stage into the current stage without recording a
formal decision.

## Completion standard

A stage is complete only when:

- required tests pass;
- required runs have validated outputs or documented failures;
- figures and tables are reproducible;
- the stage report answers its scientific questions;
- the decision gate is recorded.
