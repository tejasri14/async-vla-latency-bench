# Decisions

Record each resolved decision with date, alternatives, rationale, and
consequences.

## D001 — Days 1–3 specification

**Decision:** Preserve the previously approved `DAYS_1_3_SPEC.md` unchanged.

**Rationale:** It aligns directly with Stage 1 of the revised proposal.

## D002 — Days 4–8 scope

**Decision:** Restrict Days 4–8 to task phases, phase-conditioned delay, dynamic
interventions, and reaction metrics.

**Rationale:** LIBERO-Plus belongs in Week 2; VLASH and SmolVLA belong in Week 3.

## D003 — Logical delay

**Decision:** Use discrete-event logical time and `ceil` conversion. Never use
`sleep()` for simulated control delay.

## D004 — Intervention semantics

**Decision:** Do not clear queues, cancel requests, or force an immediate replan
at scene-change time.

**Rationale:** Measure each method's normal closed-loop behavior.

## D005 — Named baselines

**Decision:** Use a named method only with official code and a compatible
checkpoint/config.

## D006 — Result freeze

**Decision:** Add no new method after Week 3 results freeze.

## New decision template

### DXXX — Title

**Date:**  
**Decision:**  
**Alternatives:**  
**Rationale:**  
**Evidence:**  
**Consequences:**
