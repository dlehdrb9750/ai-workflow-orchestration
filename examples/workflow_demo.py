"""An in-memory, synthetic demonstration of goal-oriented AI work planning.

No AI model, network, scheduler, GitHub API, or external side effects are used.
Caller-supplied flags model verified evidence/permission; they DO NOT verify it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple
import json


class WorkflowError(ValueError):
    """An operation violates the workflow's state contract."""


@dataclass
class WorkPackage:
    id: str
    outcome: str
    required_evidence: Tuple[str, ...]
    dependencies: Tuple[str, ...] = ()
    evidence: Set[str] = field(default_factory=set)
    completed: bool = False
    held: bool = False
    unknown_attempt: str | None = None
    denied_approaches: Set[str] = field(default_factory=set)


@dataclass
class Attempt:
    id: str
    wp_id: str
    approach: str
    evidence: Tuple[str, ...]
    status: str
    failure_kind: str | None = None


class Workflow:
    """Small synchronous model: WP progress is not the Plan's completion."""

    def __init__(self, objective: str, packages: List[WorkPackage]):
        if not objective.strip() or not packages:
            raise WorkflowError("a goal and at least one WP are required")
        self.objective = objective
        self.packages: Dict[str, WorkPackage] = {p.id: p for p in packages}
        if len(self.packages) != len(packages) or any(not p.id for p in packages):
            raise WorkflowError("WP IDs must be unique and nonempty")
        for p in packages:
            if p.id in p.dependencies or any(x not in self.packages for x in p.dependencies):
                raise WorkflowError("invalid dependency")
        self._validate_acyclic()
        self.attempts: Dict[str, Attempt] = {}
        self._sequence = 0

    def _validate_acyclic(self) -> None:
        visiting, visited = set(), set()

        def visit(wp_id: str) -> None:
            if wp_id in visiting:
                raise WorkflowError("cyclic dependency")
            if wp_id in visited:
                return
            visiting.add(wp_id)
            for dependency in self.packages[wp_id].dependencies:
                visit(dependency)
            visiting.remove(wp_id)
            visited.add(wp_id)

        for key in self.packages:
            visit(key)

    @property
    def completed(self) -> bool:
        return all(p.completed for p in self.packages.values())

    def ready(self) -> List[str]:
        return [p.id for p in self.packages.values()
                if not p.completed and not p.held
                and all(self.packages[d].completed for d in p.dependencies)]

    def attempt(self, wp_id: str, approach: str, *,
                evidence: Tuple[str, ...] = (), outcome: str = "confirmed") -> str:
        """Model an *externally observed* batch outcome; don't perform real work.

        Outcomes: confirmed, transient_error, unknown_effect, explicit_denial.
        A confirmed result means that the caller independently checked evidence.
        """
        if wp_id not in self.ready():
            raise WorkflowError("WP is not ready; check dependency or HOLD")
        if not approach.strip():
            raise WorkflowError("approach must not be empty")
        p = self.packages[wp_id]
        if approach in p.denied_approaches:
            raise WorkflowError("explicitly denied action cannot be retried")
        if outcome not in {"confirmed", "transient_error", "unknown_effect", "explicit_denial"}:
            raise WorkflowError("unknown outcome")
        self._sequence += 1
        key = f"try-{self._sequence:03d}"
        self.attempts[key] = Attempt(key, wp_id, approach, evidence,
                                     "ACCEPTED" if outcome == "confirmed" else outcome.upper(),
                                     None if outcome == "confirmed" else outcome)
        if outcome == "confirmed":
            p.evidence.update(evidence)
            p.completed = set(p.required_evidence).issubset(p.evidence)
        elif outcome == "unknown_effect":
            p.held = True
            p.unknown_attempt = key
        elif outcome == "explicit_denial":
            p.held = True
            p.denied_approaches.add(approach)
        return key

    def reconcile(self, attempt_id: str, *, applied: bool | None,
                  verified_evidence: Tuple[str, ...] = ()) -> None:
        """Represents an independent readback supplied by the caller.

        UNKNOWN(None) retains HOLD. APPLIED(True) needs matching evidence.
        This simulator cannot authenticate a real external readback.
        """
        if attempt_id not in self.attempts:
            raise WorkflowError("unknown attempt")
        a = self.attempts[attempt_id]
        p = self.packages[a.wp_id]
        if p.unknown_attempt != attempt_id:
            raise WorkflowError("only an unresolved unknown-effect attempt can be reconciled")
        if applied is None:
            return
        if applied and not verified_evidence:
            raise WorkflowError("applied result requires verified evidence")
        a.status = "ACCEPTED" if applied else "NOT_APPLIED"
        p.unknown_attempt = None
        p.held = False
        if applied:
            p.evidence.update(verified_evidence)
            p.completed = set(p.required_evidence).issubset(p.evidence)

    def redefine(self, failed_attempt_id: str, new_approach: str, *,
                 distinct: bool, within_scope: bool) -> str:
        """Record an eligible alternative, not the previously failed payload.

        These flags are assertions from a human/authorized evaluator, NOT
        semantic safety or scope checks performed by this toy model.
        """
        a = self.attempts.get(failed_attempt_id)
        if not a or a.status != "TRANSIENT_ERROR":
            raise WorkflowError("only a failed, unaccepted attempt can be redefined here")
        if not distinct or not within_scope or new_approach.strip() == a.approach:
            raise WorkflowError("alternative must be distinct and within approved scope")
        if a.wp_id not in self.ready():
            raise WorkflowError("WP is not ready")
        return self.attempt(a.wp_id, new_approach, outcome="confirmed", evidence=())

    def checkpoint(self) -> str:
        """Portable JSON for this in-memory teaching example, not durable storage."""
        state = {
            "objective": self.objective,
            "packages": [{
                "id": p.id, "outcome": p.outcome,
                "required_evidence": list(p.required_evidence),
                "dependencies": list(p.dependencies),
                "evidence": sorted(p.evidence), "completed": p.completed,
                "held": p.held, "unknown_attempt": p.unknown_attempt,
                "denied_approaches": sorted(p.denied_approaches),
            } for p in self.packages.values()],
            "attempts": [a.__dict__ for a in self.attempts.values()],
            "sequence": self._sequence,
        }
        return json.dumps(state, sort_keys=True)

    @classmethod
    def resume(cls, checkpoint_json: str) -> "Workflow":
        data = json.loads(checkpoint_json)
        packages = []
        for item in data["packages"]:
            p = WorkPackage(item["id"], item["outcome"],
                            tuple(item["required_evidence"]),
                            tuple(item["dependencies"]))
            p.evidence = set(item["evidence"])
            p.completed = item["completed"]
            p.held = item["held"]
            p.unknown_attempt = item["unknown_attempt"]
            p.denied_approaches = set(item["denied_approaches"])
            packages.append(p)
        engine = cls(data["objective"], packages)
        engine.attempts = {
            a["id"]: Attempt(a["id"], a["wp_id"], a["approach"],
                             tuple(a["evidence"]), a["status"], a["failure_kind"])
            for a in data["attempts"]
        }
        engine._sequence = data["sequence"]
        return engine


def demonstration() -> None:
    wf = Workflow("Create a synthetic public-data briefing", [
        WorkPackage("sources", "Validate ordinary public sources", ("source_checked",)),
        WorkPackage("layout", "Prepare report layout", ("template_ready",)),
        WorkPackage("report", "Finish report", ("report_checked",),
                    ("sources", "layout")),
    ])
    print("Initial ready:", wf.ready())
    first = wf.attempt("sources", "source A fetch", outcome="transient_error")
    print("Temporary failure; ready independently:", wf.ready())
    wf.attempt("layout", "template draft", evidence=("template_ready",))
    wf.redefine(first, "different open-source data source B", distinct=True,
                within_scope=True)
    # A separate accepted evidence check is modeled as another batch.
    wf.attempt("sources", "validate source B", evidence=("source_checked",))
    print("Plan complete after two WPs?", wf.completed)
    restored = Workflow.resume(wf.checkpoint())
    restored.attempt("report", "final report validation", evidence=("report_checked",))
    print("Plan complete after report?", restored.completed)
    print("Synthetic workflow demonstration succeeded.")


if __name__ == "__main__":
    demonstration()
