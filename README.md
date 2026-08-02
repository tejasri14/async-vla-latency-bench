# StaleBench Revised Execution Pack

This package implements the staged plan in the revised proposal:

> **StaleBench: Temporal Robustness of Vision-Language-Action Policies under
> Asynchronous Execution**

The package is organized for three researchers working over one month.

## Stage plan

1. **Days 1–3:** π0.5 latency harness and core asynchronous baselines.
2. **Days 4–8:** task-phase labels, phase-conditioned delay, and dynamic
   intervention metrics.
3. **Week 2:** LIBERO-Plus object-layout and camera OOD × delay study.
4. **Week 3:** matched VLASH comparison and reduced SmolVLA evaluation.
5. **Week 4:** ablations, statistics, manuscript, and release.

## Canonical project files

- `AGENTS.md`
- `docs/RESEARCH_CONTEXT.md`
- `docs/DAYS_1_3_SPEC.md`
- `docs/DAYS_4_8_SPEC.md`
- `docs/WEEK_2_SPEC.md`
- `docs/WEEK_3_SPEC.md`
- `docs/WEEK_4_SPEC.md`
- `docs/METRICS_AND_LOGGING.md`
- `docs/EXPERIMENT_MATRIX.md`
- `docs/PAPER_OUTLINE.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/DECISIONS.md`
- `docs/KNOWN_ISSUES.md`
- `docs/BASELINE_COMPATIBILITY.md`
- `docs/SPEC_VERSION_MANIFEST.md`

## Codex startup prompt

```text
Read AGENTS.md and all files under docs/.
Determine the current stage from IMPLEMENTATION_STATUS.md. Inspect the existing
code and outputs before modifying anything. Continue from the first incomplete
task in the active stage. Do not claim experiments were completed unless
validated output files exist.
```
