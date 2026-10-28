# Behavior-preserving refactoring workflow

**Trigger:** Restructure code without changing observable behavior. Do not route new feature or bugfix requests here.

1. Define the target, why improvement is justified and what observable behavior must stay unchanged.
2. Record the baseline: run relevant tests and static analysis before editing. If no useful tests exist, add bounded characterization checks or disclose inability to verify preservation.
3. Plan small transformations whose boundaries and expected structural benefits are explicit.
4. Apply one transformation at a time; run appropriate checks and inspect changed callers and public contracts.
5. Do not conceal a feature or bug fix inside a refactor. Record discovered faults as separate work.
6. Re-run relevant checks at the end and review the diff for drift and unrelated edits.

**Recovery:** Distinguish pre-existing failing baseline from new defects. If behavior cannot be protected, limit or stop the change rather than claim a verified refactor.

**Handoff:** Baseline evidence, transformations, before/after check results, compatibility notes, remaining uncertainties.
