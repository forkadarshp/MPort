# Contributing to ModelPort

Thanks for contributing to ModelPort!

## Development workflow

1. Fork the repository.
2. Create a feature branch.
3. Make focused, minimal changes.
4. Update docs/examples when behavior changes.
5. Open a pull request using the PR template.

## Contribution standards

- Keep `SKILL.md` clear, actionable, and under 500 lines.
- Prefer additive reference docs over bloating the main skill body.
- Clearly mark required compatibility fixes vs optional tuning guidance.
- Include realistic examples for new behavior.

## Pull request checklist

- [ ] Change is scoped and justified
- [ ] Docs updated
- [ ] Example prompt/output updated if needed
- [ ] No unrelated refactors
- [ ] CI passes

## Local development

Run validations before opening a pull request:

```bash
python3 scripts/validate_skill.py .
npx markdownlint-cli2 "**/*.md"
```

## Adding or updating a model guide

New models are the most valuable contribution. A guide needs:

- A header with `Model ID:`, pricing, `Last verified: YYYY-MM-DD`, and
  `Source:` (the provider page you used). Mark facts from blogs or other
  secondary sources as such.
- Required changes (will error), silent changes (behavior differs), upgrade
  paths from older models, and optional tuning, kept separate.
- An entry in `references/models/INDEX.md`, and in
  `references/breaking-changes.md` if the model adds new errors.
- Superseded guides get `Status: legacy` and `Last verified: legacy, ...`
  instead of being deleted.

`python3 scripts/validate_skill.py .` checks the header and the index entry.
`python3 scripts/check_freshness.py .` lists guides older than 30 days.

## Reporting bugs

Use the bug template and include:

- Repro steps
- Expected vs actual behavior
- Relevant files or snippets
- Provider/model context
