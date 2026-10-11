# Design Decisions

**DD-001 — Treat the approved outcome as the optimization target.** Generated files and completed tool calls are intermediate outputs. A batch checkpoint does not close an unfinished Plan.

**DD-002 — Use work packages for meaningful results, not compulsory paperwork.** Simple tasks need no separate ceremony. Larger tasks benefit from explicit dependencies and completion criteria.

**DD-003 — Isolate failure to the actual dependency.** A transient error in source collection must not prevent independently preparing the report layout.

**DD-004 — Distinguish uncertainty from a known failed effect.** Unknown external write status is held until independent readback; blind resubmission risks duplicate effects.

**DD-005 — Allow new approaches only inside the original approval.** A failed, unaccepted batch may be replaced by a genuinely different method if it advances the same goal. Permission and semantic distinction must be evaluated outside the toy engine.

**DD-006 — Prefer selective recovery over permanent duplicate work.** A failed first draft does not create an obligation to reconstruct that exact draft if the user-approved outcome is otherwise reachable.

**DD-007 — Make completion evidence explicit.** The model requires named evidence labels; it never treats a success string as semantic truth. The simulated caller is responsible for supplying real validation.

**DD-008 — Keep workflow and data authority separate.** This reference models in-memory execution progress. Persistent canonical acceptance, owner selectors and Git publication rules belong to a separate state contract.

## Tradeoffs

This minimal prototype chooses **readability over completeness**. It does not optimize arbitrary dependency graphs, manage task cost or deadlines, verify natural-language scope, establish storage transactions, or orchestrate actual AI agents.
