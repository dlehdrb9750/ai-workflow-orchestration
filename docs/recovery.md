# Adaptive Execution and Localized Recovery

## Failure classes

| Observed condition | Demonstration policy | External-system reality |
| --- | --- | --- |
| Confirmed, evidence-backed batch | Store evidence toward WP completion | Actual evidence must be independently checked |
| Transient tool error | Keep the WP eligible; continue other ready work | Safe retry only when effect is known and permission permits |
| Uncertain external effect | HOLD affected WP, keep independent WPs ready | Read exact target/version before any retry |
| Explicit denial | HOLD affected WP; no automatic retry | Respect user, provider, permission and platform restrictions |
| WP dependency not satisfied | Do not start dependent WP | Owner prerequisites cannot be silently removed |

## Redefinition, not disguised retry

If a batch failed without being accepted, the goal may be advanced through an alternative **substantively different, within-scope and permitted** approach.

The example's `redefine(..., distinct=True, within_scope=True)` flags are **explicit assertions by an external evaluator**. It does not infer semantic equivalence or certify an action as safe. It only demonstrates the state transition after those conditions are already established.

The sample deliberately refuses to redefine an *explicitly denied* action. In real operations, neither renaming a blocked payload nor changing a storage provider automatically makes a denied action permissible. Work independent of the denied effect can still be completed.

## Uncertain effect: reconcile before retry

`reconcile(attempt_id, applied=True, verified_evidence=(...))` simulates an independent readback confirming the intended result. `applied=False` unlocks the WP after a verified negative observation. `applied=None` keeps the hold. The demo cannot perform this verification against real services.

## Selective buffering

Not every failed attempt merits a durable buffer or another analysis pass. A useful recovery packet should preserve non-reconstructible evidence, fulfill an explicit retention requirement, or resolve a real downstream dependency. It must not automatically become an accepted result.

The model stores attempt status within a checkpoint but does not implement a production buffering service.

## Resuming without false progress

The checkpoint restores the approved objective, WP evidence, dependency graph, unresolved states and attempt IDs. Continuation begins from verified progress, not from the assumption that the last attempt succeeded.

No repeated action is attempted when a preceding write has unknown effect. No 'global hard block' is inferred from a local transient failure.
