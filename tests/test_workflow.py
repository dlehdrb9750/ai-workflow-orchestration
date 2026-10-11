"""Run from repository root: python -m unittest discover -s tests -v"""
import unittest
from examples.workflow_demo import WorkPackage, Workflow, WorkflowError


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.w = Workflow("Synthetic goal", [
            WorkPackage("research", "Get evidence", ("cited",)),
            WorkPackage("format", "Make layout", ("formatted",)),
            WorkPackage("finish", "Approve report", ("approved",),
                        ("research", "format")),
        ])

    def test_initial_dependencies(self):
        self.assertEqual(self.w.ready(), ["research", "format"])
        self.assertFalse(self.w.completed)

    def test_partial_batch_is_not_wp_or_plan_completion(self):
        self.w.attempt("research", "gather", evidence=("draft",))
        self.assertFalse(self.w.packages["research"].completed)
        self.assertFalse(self.w.completed)

    def test_wp_completion_is_not_plan_completion(self):
        self.w.attempt("research", "verify", evidence=("cited",))
        self.assertTrue(self.w.packages["research"].completed)
        self.assertFalse(self.w.completed)

    def test_dependencies_hold_downstream(self):
        with self.assertRaises(WorkflowError):
            self.w.attempt("finish", "premature", evidence=("approved",))
        self.assertNotIn("finish", self.w.ready())

    def test_transient_error_does_not_stop_independent_work(self):
        a = self.w.attempt("research", "fetch", outcome="transient_error")
        self.assertEqual(self.w.attempts[a].status, "TRANSIENT_ERROR")
        self.assertIn("format", self.w.ready())
        self.assertFalse(self.w.completed)

    def test_unknown_effect_is_held_until_readback(self):
        a = self.w.attempt("research", "save", outcome="unknown_effect")
        self.assertNotIn("research", self.w.ready())
        self.assertIn("format", self.w.ready())
        with self.assertRaises(WorkflowError):
            self.w.attempt("research", "save")
        self.w.reconcile(a, applied=None)
        self.assertNotIn("research", self.w.ready())

    def test_readback_not_applied_unholds(self):
        a = self.w.attempt("research", "save", outcome="unknown_effect")
        self.w.reconcile(a, applied=False)
        self.assertIn("research", self.w.ready())
        self.assertEqual(self.w.attempts[a].status, "NOT_APPLIED")

    def test_readback_applied_requires_evidence(self):
        a = self.w.attempt("research", "save", outcome="unknown_effect")
        with self.assertRaises(WorkflowError):
            self.w.reconcile(a, applied=True)
        self.w.reconcile(a, applied=True, verified_evidence=("cited",))
        self.assertTrue(self.w.packages["research"].completed)

    def test_denial_blocks_only_affected_wp(self):
        a = self.w.attempt("research", "restricted", outcome="explicit_denial")
        self.assertEqual(self.w.attempts[a].status, "EXPLICIT_DENIAL")
        self.assertNotIn("research", self.w.ready())
        self.assertIn("format", self.w.ready())
        with self.assertRaises(WorkflowError):
            self.w.attempt("research", "restricted")

    def test_redefinition_requires_failed_distinct_scoped_attempt(self):
        a = self.w.attempt("research", "source A", outcome="transient_error")
        for kwargs in [dict(distinct=False, within_scope=True),
                       dict(distinct=True, within_scope=False)]:
            with self.assertRaises(WorkflowError):
                self.w.redefine(a, "source B", **kwargs)
        with self.assertRaises(WorkflowError):
            self.w.redefine(a, "source A", distinct=True, within_scope=True)
        b = self.w.redefine(a, "source B", distinct=True, within_scope=True)
        self.assertEqual(self.w.attempts[b].status, "ACCEPTED")
        self.assertFalse(self.w.packages["research"].completed)

    def test_cannot_redefine_denial_as_new_name(self):
        a = self.w.attempt("research", "restricted", outcome="explicit_denial")
        with self.assertRaises(WorkflowError):
            self.w.redefine(a, "renamed", distinct=True, within_scope=True)

    def test_checkpoint_resume_preserves_progress_and_goal(self):
        self.w.attempt("research", "verify", evidence=("cited",))
        restored = Workflow.resume(self.w.checkpoint())
        self.assertEqual(restored.objective, "Synthetic goal")
        self.assertEqual(restored.ready(), ["format"])
        restored.attempt("format", "layout", evidence=("formatted",))
        self.assertEqual(restored.ready(), ["finish"])
        restored.attempt("finish", "review", evidence=("approved",))
        self.assertTrue(restored.completed)

    def test_checkpoint_preserves_uncertainty(self):
        a = self.w.attempt("research", "save", outcome="unknown_effect")
        restored = Workflow.resume(self.w.checkpoint())
        self.assertNotIn("research", restored.ready())
        restored.reconcile(a, applied=False)
        self.assertIn("research", restored.ready())

    def test_cycles_and_duplicate_package_ids_fail(self):
        with self.assertRaises(WorkflowError):
            Workflow("x", [WorkPackage("a", "a", (), ("b",)),
                           WorkPackage("b", "b", (), ("a",))])
        with self.assertRaises(WorkflowError):
            Workflow("x", [WorkPackage("a", "a", ()),
                           WorkPackage("a", "a2", ())])


if __name__ == "__main__":
    unittest.main()
