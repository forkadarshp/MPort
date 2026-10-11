# Publishing and Growth Playbook

Maintainer checklist for repo settings, release cadence, and distribution.

## Positioning

- **One line:** Upgrade models without breaking prod.
- **Who it is for:** engineers whose app calls an LLM API and who must move to
  a newer model (a deprecation notice, a price drop, a capability they need).
  Secondary: teams that use Claude Code, Codex, or Cursor and want an agent to
  do the migration.
- **Why it wins:** per-model guides with exact breaking changes and error
  strings, a fix order, and proof. A generic "migrate my prompts" request to an
  agent has none of that.
- **Evergreen, not launch-tied.** Do not build the pitch on one model release.
  The pitch is "every release breaks something". The model list is a table that
  gets a new row.

## Repository settings

Set these in the GitHub repo settings (or with `gh repo edit`).

Description (under 160 characters):

```text
Agent skill that upgrades LLM code to Claude Opus 5.5, GPT-6, Gemini 3.8 without breaking prod. Fixes breaking changes, then proves it with tests and evals.
```

Topics (20 is the maximum):

```text
agent-skills, claude-code, codex, cursor, llm-migration, model-migration,
model-upgrade, prompt-migration, prompt-engineering, llmops, llm, anthropic,
openai, gemini, claude, gpt, ai-agents, developer-tools, breaking-changes,
benchmarking
```

Avoid version-specific topics (for example a model ID). They go stale.

Social preview: upload `assets/social-preview.png` under Settings, Social
preview. GitHub does not accept this through the API. Regenerate the PNG after
editing the SVG:

```bash
rsvg-convert -w 1280 -h 640 assets/social-preview.svg -o assets/social-preview.png
```

## Release cadence

Model news drives search traffic, so speed matters more than polish.

When a provider ships a model:

1. Within 48 hours, add a guide in `references/models/`. Copy the header block
   of an existing guide: `Model ID`, price, `Last verified`, `Source`.
2. Add the guide to `references/models/INDEX.md` and, if the model brings new
   errors, to `references/breaking-changes.md`.
3. Add a row to the README "Supported models" table.
4. Run `python3 scripts/validate_skill.py .`.
5. Tag a release. Use the error strings and the one-line fix in the notes.

The weekly `freshness` workflow opens an issue when any guide passes 30 days
without re-verification. It cannot see new model releases, so also check the
provider changelogs when you re-verify:

- Anthropic: <https://platform.claude.com/docs/en/about-claude/models/overview>
- OpenAI: <https://developers.openai.com/api/docs/guides/latest-model>
- Google: <https://ai.google.dev/gemini-api/docs/changelog>

Version history:

- `v0.1.0`: first public release (workflow, references, examples, CI).
- `v0.2.0`: current-generation guides (Claude 5.x, GPT-6, Gemini 3.8), model
  index, breaking-changes lookup, freshness automation, harness fixes for
  current Claude models.
- `v1.0.0`: stable workflow validated on real migrations (case studies).

## Install channels

Keep both working. Test them after any change to `SKILL.md` or the manifests.

| Channel | User command | Check |
| :------ | :----------- | :---- |
| Skills CLI (any agent) | `npx skills add forkadarshp/modelport` | `npx skills add . --list` finds one skill |
| Claude Code plugin | `/plugin install modelport --marketplace forkadarshp/modelport` | `claude plugin validate .` passes |

Listing on skills.sh: the directory keys pages by repo path, so the rename on
2026-10-11 starts a new page at
<https://skills.sh/forkadarshp/modelport/modelport-skill> once someone installs
from the new path. The old page,
<https://skills.sh/forkadarshp/mport/modelport-skill>, showed 1 install and "No
SKILL.md available for this skill" on that date, so it had no description. The
raw `SKILL.md` URL resolves, so the cause is on the directory side or a stale
snapshot. Check the new page after the first install and report it to the
skills.sh maintainers if the description is still missing.

Wider reach for the plugin: submit it to Anthropic's plugin directory (see
"Submit to Anthropic's directory" in the Claude Code plugin docs).

## Website (GitHub Pages)

`_config.yml` makes the repo root a Jekyll site, so every guide becomes its own
indexable page with a title taken from its first heading. Pages deploys from
branch `main`, folder `/`, to <https://forkadarshp.github.io/modelport/>, which
is also the repo homepage. Each push to `main` rebuilds the site; a failed
build shows under Actions as "pages build and deployment".

## Naming

The repo is `modelport`, the product is ModelPort, and the skill is
`modelport-skill`. The repo was called `MPort` until 2026-10-11. GitHub
redirects the old URL, so old links and `npx skills add forkadarshp/MPort` keep
working, but do not create a new repo named `MPort` under the same account:
that would break the redirect.

## Distribution

`npx skills add` installs feed the public skills directory at skills.sh, so
installs and discovery reinforce each other. Channels, in order of expected
return:

1. **Search.** The breaking-changes page contains exact error strings people
   paste into search. Write one blog post or README-linked page per major
   model release: "What breaks when you move to MODEL NAME" with the error,
   cause, and fix. Link back to the repo.
2. **Show HN and Reddit** (r/ClaudeAI, r/ChatGPTCoding). Post once per major
   release, with the breaking-changes table as the hook, not the tool.
3. **X or LinkedIn thread** on the same table.
4. **Provider communities** (Anthropic and OpenAI developer Discords and
   forums) as an answer to a real migration question, with the relevant guide
   linked.
5. **Awesome lists**, via pull request. Read each list's contribution rules
   first. Candidates: `hesreallyhim/awesome-claude-code`,
   `travisvn/awesome-claude-skills`, `ComposioHQ/awesome-claude-skills`,
   `karanb192/awesome-claude-skills`, `VoltAgent/awesome-agent-skills`.

Before posting, check each community's self-promotion rules.

### Draft: Show HN

```text
Title: Show HN: ModelPort, an agent skill that fixes what breaks when you upgrade LLMs

Moving to Claude Opus 5.5 means thinking can no longer be disabled, forced
tool_choice returns 400, and thinking blocks must stay append-only. GPT-6
drops temperature and top_p when reasoning is on. Gemini 3.8 rejects the
"minimal" thinking level. None of this is a find/replace.

ModelPort is a skill for Claude Code, Codex and Cursor. It has per-model guides
(Claude 5.x, GPT-6, Gemini 3.8) with the exact errors and fixes, applies them in
order, and ends with tests, a live smoke check and rollback notes. There is also
an offline harness for old-vs-new comparisons. The simulator's numbers are
illustrative; --provider anthropic gives measured ones.

Guides carry a verified-on date and a source, and CI flags stale ones.

https://github.com/forkadarshp/modelport
```

### Draft: thread

```text
1/ Upgrading an LLM is never just the model ID. Things I keep seeing break:
- "thinking.type.disabled" is not supported (Claude Opus 5.5)
- tool_choice any/tool returns 400 (Opus 5.5, Sonnet 5.5, Fable 5.1)
- temperature/top_p rejected with reasoning on (GPT-6)
- replies cut off because thinking now counts toward max_tokens

2/ I put every one of these, with the cause and the fix, in one table:
references/breaking-changes.md

3/ ModelPort is an agent skill that applies those fixes for you, in order, and
ends with tests, a smoke check and rollback notes. npx skills add forkadarshp/modelport
```

## Measure

Check weekly: stars, unique visitors and referrers (Insights, Traffic), clones,
and issues opened. Referrers show which channel worked. Repeat what works.

## Before making a release public

- [ ] `python3 scripts/validate_skill.py .` passes.
- [ ] `npx markdownlint-cli2 "**/*.md"` passes.
- [ ] `python3 -m unittest discover -s harness/tests` passes.
- [ ] README "Supported models" table matches `references/models/INDEX.md`.
- [ ] Description, topics, and social preview match this file.
