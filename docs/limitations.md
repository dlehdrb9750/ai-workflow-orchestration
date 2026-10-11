# Verification, Scope and Limitations

## Local verification

```bash
python examples/workflow_demo.py
python -m unittest discover -s tests -v
```

**Verified on 2026-10-11:** 14/14 standard-library unit tests passed locally and in [GitHub Actions](https://github.com/dlehdrb9750/ai-workflow-orchestration/actions/runs/38136344974). The hosted run also executed the demo successfully. This is evidence about this toy model, not real LLM orchestration.

The tests cover prerequisites; incomplete batch versus WP versus Plan; independent progress after transient failure; HOLD and reconciliation for unknown effects; explicit-denial handling; bounded, distinct approach redefinition; checkpoint reconstruction; and cyclic/duplicate WP rejection.

## Simulation boundaries

- No large language model, external task execution, provider connection, background scheduling or remote API.
- Results are manually signaled by the calling test. A label like `cited` or `approved` is not real-world evidence verification.
- `distinct=True`, `within_scope=True` and `applied=True` **do not themselves prove safety, authorization or readback**. They deliberately model external judgments.
- The explicit denial behavior prevents same-action replays in this example, not arbitrary semantic bypass across tools.
- A checkpoint is returned as JSON; it is not durably committed to disk or Git.
- The code is not hardened for corrupted/untrusted checkpoint input, multithreading, distributed writers, graph optimization or resource accounting.
- There are no claimed production reliability gains, AI-assisted reasoning benchmarks, or unattended end-to-end operation.

## Security and privacy

All input examples are fictional. No internal project names, production logs, private research, actual investments, user learning records, secrets or unpublished specifications are included.

## Relation to other work

AWPS-like orchestration decides *what work advances the objective*. DLS-like state governance decides *which persisted state is authoritative*. A runnable demo of the first is not a production implementation of the second.
