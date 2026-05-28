# Migration Patterns

Use this reference when choosing how to migrate a codebase, prompt stack, agent,
or model route. Prefer the smallest pattern that satisfies the user's risk,
compatibility, and rollout requirements.

## Source Reliability Notes

- Martin Fowler's Branch by Abstraction describes using an abstraction layer so
  old and new implementations can coexist while the system continues to build
  and run.
- AWS Prescriptive Guidance describes the 7 Rs and the strangler fig pattern for
  incremental replacement with reduced disruption.
- Azure Cloud Adoption Framework emphasizes dependency discovery, migration
  sequencing, safer early waves, and nonproduction validation before production.
- Google SRE guidance treats canaries as partial, time-limited deployments
  evaluated against controls before wider rollout.
- Prisma and PlanetScale database guidance maps well to expand-contract changes:
  add compatible structures first, migrate traffic/data, then remove old
  structures only after validation.

## Pattern Selection

### Direct Swap

Use when:

- The old and new model have the same endpoint, request shape, and output
  contract.
- The codebase has one or a few call sites.
- Rollback is a simple config or model ID revert.

Do:

- Update model defaults and direct request parameters.
- Run smoke tests and output-contract checks.
- Avoid touching prompts unless behavior evidence justifies it.

Avoid when:

- Parser contracts, tool behavior, reasoning parameters, or response formats
  changed.

### Branch by Abstraction

Use when:

- Multiple callers depend on a provider/client/module being replaced.
- Old and new model paths must coexist during migration.
- The repo needs regular releases while migration is in progress.

Do:

- Introduce or reuse a provider/model adapter boundary.
- Route call sites through the abstraction.
- Keep both implementations until destination behavior is validated.
- Make the migration reversible with config or dependency injection.

Avoid:

- Duplicating provider conditionals throughout unrelated business logic.

### Strangler-Style Routing

Use when:

- A subset of traffic, agents, prompts, or workflows can move before the rest.
- The system can route by feature, tenant, endpoint, task type, or workload.

Do:

- Add a routing layer or feature flag.
- Move one low-risk slice first.
- Keep the legacy path available until all slices are migrated and monitored.

Avoid:

- Big-bang replacement across unrelated workflows.

### Expand-Contract

Use when:

- Both old and new contracts must be supported during rollout.
- Changes affect prompt variables, output schemas, parser fields, tool schemas,
  config keys, database fields, or telemetry.

Do:

1. **Expand**: add new fields, schemas, routes, or config keys alongside old
   ones.
2. **Migrate**: write/read both when needed, backfill or translate data, and
   verify compatibility.
3. **Contract**: remove old structures only after old traffic is gone and
   rollback no longer depends on them.

Avoid:

- Removing old fields, prompts, or parser branches in the same change that first
  introduces the new contract.

### Shadow Mode

Use when:

- The destination model can be called without affecting users.
- You need quality, latency, cost, tool-use, or schema-compliance evidence before
  cutover.

Do:

- Send production-like requests to both old and new paths.
- Serve the old path while logging destination output and metrics.
- Compare output contracts, tool calls, refusal/safety behavior, latency, and
  token usage.

Avoid:

- Logging sensitive prompt data without privacy review.

### Canary Rollout

Use when:

- The destination path will affect real users but risk can be limited to a small
  population first.

Do:

- Start with a small, time-bounded traffic percentage.
- Define success metrics and automatic/manual rollback conditions.
- Compare canary to control, not to isolated absolute metrics only.
- Widen traffic gradually after evidence passes.

Avoid:

- Declaring success without enough request volume or representative workload
  coverage.

## Pattern Mapping for LLM Migrations

| Migration shape | Preferred pattern |
| --- | --- |
| Model ID only, same API contract | Direct swap |
| Provider SDK replacement | Branch by abstraction |
| Per-feature prompt or agent rollout | Strangler-style routing |
| Output schema or tool schema change | Expand-contract |
| Quality/cost validation before user impact | Shadow mode |
| Gradual production exposure | Canary rollout |
| Critical production agents | Shadow mode, then canary, then contract cleanup |

## Implementation Notes

- Model registries and capability maps are definers; usually add destination
  models alongside source models until retirement is explicit.
- Runtime callers can be switched once compatibility fixes are applied.
- Prompt edits should be listed as optional tuning unless they prevent a hard
  failure such as invalid schema output.
- Generated files and snapshots should be regenerated, not hand-edited.
- Cleanup is a separate migration phase; do not remove fallback paths before
  rollout evidence exists.

## Source URLs

- Martin Fowler, Branch by Abstraction:
  <https://martinfowler.com/bliki/BranchByAbstraction.html>
- AWS Prescriptive Guidance, Strangler fig pattern:
  <https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html>
- AWS Prescriptive Guidance, migration strategies:
  <https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html>
- Azure Cloud Adoption Framework, plan your migration:
  <https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/plan-migration>
- Google SRE Workbook, Canarying Releases:
  <https://sre.google/workbook/canarying-releases/>
- Prisma, expand-and-contract migrations:
  <https://docs.prisma.io/docs/guides/database/data-migration>
- PlanetScale, deploy requests and gated deployments:
  <https://planetscale.com/docs/vitess/schema-changes/deploy-requests>
