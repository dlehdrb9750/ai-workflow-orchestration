# Architecture — Objective, Packages, Batches and Checkpoints

## Scope

This public reference organizes *work*, not canonical storage. The user or authorized Owner decides what work is permitted, what evidence counts, and what final result may be accepted. A storage system's own update/readback contract belongs to a separate state-governance layer.

## Core decomposition

```text
User-approved objective + scope + success conditions
       |
       +---- Work Package A (inputs) ---- batch A1 -> failure
       |                         \---- distinct, permitted batch A2
       |
       +---- Work Package B (independent formatting)
       |
       \---- Work Package C (depends on A and B)
                                  |
                                  v
                    Verify completion evidence
                                  |
                                  v
                 Goal satisfied? Yes / Continue
```

A *work package* describes a meaningful desired result. A *batch* is the concrete attempt or group of tool calls. A failed batch is not itself a missing permanent canonical record. A work package can need more than one accepted result to satisfy its evidence criteria.

## Dependency-first execution

A work package is **ready** only if its actual prerequisites are completed, it has not already completed, and it is not held for an uncertain effect or explicit denial. Other ready packages may continue. The example checks for missing or cyclic dependencies at construction time.

## Checkpoint and handoff

The minimum logical state is:

| Field | Why it matters |
| --- | --- |
| Approved objective | Preserves the actual mission |
| WP descriptions and dependencies | Prevents losing the execution graph |
| Accepted WP evidence | Avoids redoing verified work |
| Attempt status and unresolved effects | Makes unconfirmed writes distinguishable from confirmed results |
| Completed / held flags | Separates progress from temporary inability |
| Next eligible WPs | Enables bounded resumption |

The example serializes this information into JSON and reconstructs it. **JSON held in memory is not durable persistence**; a production system must independently persist/check/authorize its own state.

## Completion rule

`ALL_REQUIRED_WPS_COMPLETE` is the demonstration's explicit goal-level condition. A completed batch, created checkpoint, or single WP is not enough. In practice, the responsible human or system must also verify substantive acceptance criteria.

## Work scheduling

Scheduling frequency, time windows, and minimum or maximum execution duration are application-specific. This sample neither runs background workers nor assumes access to future conversations.
