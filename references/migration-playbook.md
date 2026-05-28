# Migration Playbook

Use this playbook to run robust model migrations with minimal regressions.

For rollout patterns, read `references/migration-patterns.md`. For proof gates
and diagnose-patch-retry behavior, read `references/validation-proof.md`.

## 1) Define migration intent

Capture:

- Source provider/model/version
- Destination provider/model/version
- Business goals (quality, latency, cost, reliability)
- Non-functional constraints (compliance, determinism, observability)
- Migration pattern candidate: direct swap, adapter, side-by-side, shadow mode,
  canary, or phased cutover

## 2) Lock scope and current state

Scope must be explicit before editing:

- Whole repo
- Specific directory
- Explicit file list

If unclear, ask once and wait.

Before editing, check what has already been implemented:

- Version control status, recent commits, current branch, open PR/issue notes, and
  local handoff files where available
- Existing migration flags, compatibility adapters, prompt variants, model
  registries, and tests
- Partial or conflicting changes made by another agent

Classify current work as:

- **Done**: implemented and validated
- **Needs validation**: implemented but not proven
- **In progress**: partial or inconsistent
- **Not started**: required for the requested migration but absent

## 3) Build impact map

Scan for:

- Model identifiers
- SDK/request construction
- Prompt templates and policy text
- Agent behavior and delegation instructions
- Tool metadata and schemas
- Tests and docs tied to legacy behavior

## 4) Classify before modify

### Runtime callers

Action:

- Update model/parameter usage
- Replace deprecated request fields
- Add migration-safe defaults where required

### Definers/registries

Action:

- Usually add alongside instead of hard replace
- Preserve legacy entries unless explicitly retiring

### Prompt behavior layer

Action:

- Recalibrate style, strictness, and verbosity expectations
- Remove brittle prompt hacks that depended on old behavior

### Agent and tool layer

Action:

- Rework "when to use tools" instructions if behavior shifted
- Re-check tool schemas, validation constraints, and guardrails

### Tests/docs

Action:

- Update assertions tied to old model behavior
- Add migration-specific regression checks

## 5) Design the change set

Split work into:

- **Required compatibility fixes** (must do to avoid breakage)
- **Optional tuning improvements** (recommended for better outcomes)
- **Coordination follow-ups** (items another agent started or should own)
- **Rollout controls** (flags, adapters, shadow routing, canary metrics)

Never mix these categories in reporting.

## 6) Implement safely

Preferred order:

1. API/runtime compatibility
2. Prompt behavior
3. Agent/tool behavior
4. Rollout controls and observability
5. Config, tests, and docs alignment

Use targeted edits. Avoid blanket replacements.

## 7) Validate

Run:

- Unit/integration tests for touched paths
- Lint/type-check for touched paths
- Runtime smoke tests on destination model
- Prompt or output-contract evals for changed behavior
- Shadow/canary checks if migration uses staged rollout

Check:

- No request schema/model errors
- Outputs meet required structure
- Tool calls and agent behavior still aligned with expectations
- Latency/cost within acceptable range for initial rollout
- Rollback path is still valid after the change

## 8) Rollout and rollback

For high-risk systems:

- Use staged rollout
- Keep rollback path (feature flag or prior model path)
- Track migration metrics for the first production window
- Compare canary traffic to control traffic before widening exposure
- Avoid irreversible cleanup until the new path has production evidence

## 9) Report

Produce:

- Scope migrated
- Files changed
- Existing work found and remaining work
- Required fixes applied
- Optional tuning applied
- Validation outcomes
- Proof evidence collected
- Risks and follow-ups
- Rollback instructions
