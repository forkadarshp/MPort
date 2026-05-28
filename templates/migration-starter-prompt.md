# Migration Starter Prompt

Use this template when asking an agent to migrate prompts, agents, API callers,
or code from one model/provider to another. Fill only the fields you know; leave
unknowns explicit instead of guessing.

```text
You are migrating an LLM-powered system from one model/provider to another.

## Outcome

Migrate the selected scope from:
- Source provider/model/version: {SOURCE_MODEL}
- Target provider/model/version: {TARGET_MODEL}

The migration must preserve required behavior, improve behavior only where
evidence supports it, and produce validation evidence plus rollback notes.

## Scope

Migrate only:
{EXACT_FILES_OR_DIRECTORIES}

Do not edit outside this scope unless you first explain why it is required.

## Current System Context

- Application/workflow purpose:
  {WHAT_THE_SYSTEM_DOES}
- Runtime/API entry points:
  {API_CALLERS_OR_CLIENTS}
- Prompt assets:
  {PROMPT_FILES_OR_TEMPLATES}
- Agent/tool behavior:
  {TOOLS_AGENTS_OR_ORCHESTRATION}
- Output contracts/parsers:
  {JSON_SCHEMA_PARSERS_FORMATS_OR_TESTS}
- Existing migration work or handoff notes:
  {WHAT_IS_ALREADY_DONE}

## Constraints

- Compatibility requirements:
  {OUTPUT_SHAPE_TOOL_USE_SAFETY_OR_USER_EXPERIENCE}
- Latency/cost budget:
  {LATENCY_COST_TOKEN_BUDGET}
- Rollout mode:
  {DIRECT_SWAP_BRANCH_BY_ABSTRACTION_SHADOW_CANARY_OR_OTHER}
- Rollback path:
  {FEATURE_FLAG_CONFIG_REVERT_OR_LEGACY_ROUTE}

## Instructions

1. Discover and classify every relevant hit before editing:
   runtime caller, definer/registry, prompt layer, agent/tool layer, tests/docs,
   or generated artifact.
2. Preserve a baseline first: update the model/config path and required API
   compatibility issues before doing optional prompt tuning.
3. Separate required compatibility fixes from optional tuning.
4. Prefer adapters, side-by-side support, shadow mode, or canary rollout when a
   direct swap would create avoidable risk.
5. For prompt edits, show before/after snippets and explain the behavior shift
   being targeted.
6. Run validation after each meaningful change. If a check fails, diagnose the
   root cause, patch narrowly, and retry the failed check.
7. Do not guess model IDs, request fields, pricing, limits, or deprecation dates;
   verify against official provider docs when those details matter.

## Proof Gates

Run or explain why you cannot run:

- Unit/integration tests for touched code
- Runtime smoke request on the target model/provider
- Output-contract or parser validation
- Prompt/agent eval on representative inputs
- Tool-call trace if tools are involved
- Shadow/canary metric plan if production rollout is risky

## Report

Default concise output mode (defined in SKILL.md). Dense bullets, diffs only, no filler.

Sections:

1. Migration Summary
2. Scope and Files Changed
3. Existing Work and Remaining Work
4. Required Compatibility Fixes
5. Prompt/Agent Behavior Tuning
6. Validation Results
7. Proof Evidence
8. Risks and Follow-up Recommendations
9. Rollback Notes
```
