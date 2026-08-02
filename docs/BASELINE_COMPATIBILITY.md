# Baseline Compatibility

Complete this table before Week 3 numerical comparisons.

| Method | Official repository/SHA | Framework | Base policy | Training required | Official LIBERO checkpoint | Observation/state inputs | Action convention | Control frequency | Chunk/horizon | Latency semantics | Provenance hooks | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| π0.5 ideal/blocking | | LeRobot | π0.5 | No | `lerobot/pi05_libero_finetuned` | | Relative | | 10 initially | project logical delay | Native | Planned |
| Naive async | project implementation | LeRobot | same π0.5 | No | same | same | Relative | matched | configurable | project logical delay | Native | Planned |
| RTC | | LeRobot | flow π0.5 | No | same where supported | same | Relative | matched | matched | request-specific | Required | Planned |
| VLASH | | | π0.5 family | Verify | Verify | future-state-aware | Verify | Verify | Verify | Verify | Verify | Audit required |
| SmolVLA | | LeRobot | SmolVLA | No for official checkpoint | Verify | Verify | Verify | matched | Verify | project logical delay | Required | Week 3 |
| FASTER | | OpenPI/JAX | flow VLA | likely method-specific | Verify | Verify | Verify | Verify | streaming | TTFA/streaming | Verify | Optional audit |
| Reflex | | | | Verify | Verify | Verify | Verify | Verify | streaming | Verify | Optional audit |
| VLA-Corrector | | | | Verify | Verify | Verify | Verify | adaptive | corrective | Verify | Optional audit |

## Fairness checklist

- [ ] Same task identity
- [ ] Same initial state and seed
- [ ] Same action representation
- [ ] Same control frequency
- [ ] Same observation cameras
- [ ] Same intervention timing
- [ ] Same latency trace or explicit timing distinction
- [ ] Compute usage reported
- [ ] Policy-call schedule reported
- [ ] Official checkpoint/config recorded
- [ ] Provenance semantics validated
