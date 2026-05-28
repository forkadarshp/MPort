# Validation Proof Gates

Use this reference when planning or reporting migration validation. The goal is
to prove that the destination model path works on representative inputs, not
only that edited code compiles.

## Proof Standard

A migration is not complete until the agent can show evidence from at least one
of these surfaces, or state why the evidence could not be collected:

- Unit or integration test output for touched code.
- Runtime smoke request against the destination model or provider.
- Prompt/output eval comparing source and destination behavior.
- Parser or schema-contract validation for structured outputs.
- Tool-call trace showing the destination model invokes tools correctly.
- Shadow-mode comparison between source and destination outputs.
- Canary metrics comparing destination traffic against control traffic.
- Before/after reproduction for a bug fixed during migration.

## What Does Not Count Alone

- A synthetic test written only to match the new implementation.
- A type check without runtime execution.
- A model ID grep showing no old references.
- A claim that behavior should be compatible without running anything.
- A prompt rewrite without sample output or eval evidence.

## Diagnose-Patch-Retry Loop

When a validation check fails:

1. **Observe**: capture the raw failure, command, request payload summary, status
   code, stack trace, or output mismatch.
2. **Diagnose**: identify the smallest responsible surface: model ID, endpoint,
   request parameter, prompt contract, parser, tool schema, routing, or fixture.
3. **Patch**: make the narrowest change that addresses the observed cause.
4. **Retry**: re-run the failed check before moving on.
5. **Record**: report both the original failure and the passing retry.

Do not paper over failures by loosening assertions unless the old assertion was
explicitly tied to old-model behavior and the replacement contract is documented.

## Proof by Migration Type

### Runtime/API Migration

Required evidence:

- Destination request succeeds.
- Response model/provider is the expected target when available.
- Stop/finish reason is handled.
- Usage, latency, and error behavior are observable.

### Prompt Migration

Required evidence:

- Representative before/after sample or eval.
- Output shape still satisfies downstream consumers.
- Optional tuning edits are separated from hard compatibility fixes.
- User-facing tone/length/style changes are intentional.

### Agent or Tool Migration

Required evidence:

- Tool schemas validate.
- Destination model calls the right tools on representative tasks.
- It avoids tools when the task does not need them.
- Multi-step behavior still respects autonomy, handoff, and safety limits.

### Config, Router, or Registry Migration

Required evidence:

- Source and destination routes can coexist when rollback is required.
- Feature flag or config switch works.
- Old model entries remain when old traffic is still supported.
- Capability gates include both source and destination models where needed.

### Rollout Migration

Required evidence:

- Shadow or canary metrics are defined before rollout.
- Rollback conditions are explicit.
- Cleanup is deferred until after production evidence exists.

## Report Template

Include a concise proof section:

```text
## Proof Evidence

- Command/check:
- Input or representative scenario:
- Result:
- Failure observed:
- Patch applied:
- Retry result:
- Evidence gap, if any:
```

## Source URLs

- Google SRE Workbook, Canarying Releases:
  <https://sre.google/workbook/canarying-releases/>
- Google SRE Book, Release Engineering:
  <https://sre.google/sre-book/release-engineering/>
- Google SRE Book, Production Services Best Practices:
  <https://sre.google/sre-book/service-best-practices/>
- PlanetScale, deploy requests and gated deployments:
  <https://planetscale.com/docs/vitess/schema-changes/deploy-requests>
