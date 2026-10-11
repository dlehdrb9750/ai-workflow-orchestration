# AI Workflow Orchestration

**AWPS — Adaptive Work Planning Standard**  
**Public release:** v0.1.0 · Reference architecture + tested educational prototype · 2026-10-11

> Make AI-assisted work **goal-oriented, resumable, evidence-aware, and resilient to localized tool failures**.

## Why it exists

A single AI answer and a long-running work process are not the same thing. Complex tasks may span research, file updates, checkpoints, different execution environments, and interruptions. A finished tool call is not necessarily a finished objective.

**This repository describes a small public operating model, not a proprietary runtime or a complete autonomous agent product.** It is an independently written teaching reference inspired by practical workflow-design experience.

## The operating model

| Unit | Responsibility | What it does *not* mean |
| --- | --- | --- |
| **Plan** | User-approved objective, scope, success criteria | A mandatory large planning document |
| **Work Package (WP)** | A meaningful unit that advances the objective | A single chat turn or tool call |
| **Batch** | One practical attempt or execution grouping | Automatic completion of its parent WP |
| **Checkpoint** | The minimum information necessary to resume | Proof that a goal is completed |
| **Evidence** | Verified outputs required for an explicit completion decision | Mere activity or generated text |

**Plan completion ≠ WP completion ≠ Batch completion.**

## Principles

1. **Objective continuity first.** Prefer meaningful progress on the approved goal over mechanically replaying every failed draft.
2. **Dependencies, not ceremony.** Independent work can proceed while one work package is blocked; real prerequisites remain binding.
3. **Failure is local.** Distinguish transient tool errors, uncertain external effects, and explicit authorization refusals.
4. **Resolve uncertain effects before retry.** Read back external state before assuming a write did or did not occur.
5. **Adaptive batch redefinition.** An unaccepted failed batch may be replaced by a genuinely different and permitted approach within the approved scope. Renaming a denied operation is not a valid redefinition.
6. **Selective recovery.** Retain meaningful, irreplaceable unaccepted data when appropriate, not a mandatory second backlog for all attempts.
7. **Owner and human authority.** The planner does not grant permissions, modify accepted owner state, or independently authorize an expanded objective.
8. **Project-specific execution policy.** Clock limits, scheduled runs and operational permissions are defined by the actual project and platform, not by this general reference model.

## Run the example

Python **3.10+** (standard library only):

```bash
python examples/workflow_demo.py
python -m unittest discover -s tests -v
```

The demonstration builds a **fictional public-data briefing**, injects a transient error in its source-gathering WP, completes an independent layout WP, redefines the failed attempt through a different source, serializes a checkpoint, then resumes and completes the report.

**Local validation:** 14 unit tests passed on 2026-10-11. The code is deterministic and entirely in memory. A reported result is *simulated* from caller-supplied evidence; it does not authenticate permissions or independently verify real-world work.

## Documentation

- [Architecture and lifecycle](docs/architecture.md)
- [Failure classification and adaptive recovery](docs/recovery.md)
- [Design decisions](docs/design-decisions.md)
- [Verification, limitations and safety](docs/limitations.md)
- [Example source](examples/workflow_demo.py) · [Unit tests](tests/test_workflow.py)
- [Public release history](CHANGELOG.md)

## What this demonstrates — and what it does not

The public model demonstrates dependency-aware progress, guarded results, localized HOLD, noncanonical failed attempts, and reconstructible checkpoints **in a single Python process**.

It does **not** execute LLM tasks, invoke external providers, schedule background workers, supply distributed consistency, enforce authorization, or claim measured improvements to real-world completion rates. These require separate integrations and evaluation.

## Related architecture

- **[AI State Governance](https://github.com/dlehdrb9750/ai-state-governance):** Data/authority publication and acceptance boundaries (DLS).
- **[AI Systems Portfolio](https://github.com/dlehdrb9750/ai-systems-portfolio):** Public case studies and other projects.

**AWPS is about accomplishing work; DLS is about preserving and admitting state.** Publishing this teaching repository has no effect on internal operational authority, scheduled workloads, or existing canonical standards.

## Disclosure and licensing

Only synthetic examples and original public-oriented descriptions are included. No private research, source repositories, internal file identifiers, live project settings, or proprietary content are published.

There is **no open-source license grant yet**; publication is not permission for unrestricted reuse. A future explicit license may be chosen separately.
