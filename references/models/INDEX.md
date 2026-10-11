# Model Guide Index

Registry of dedicated model guides. Read this first: find the source and
target model, open the guide, then follow its upgrade path.

Status values: **current** (default target), **active** (still served, not the
default target), **legacy** (superseded guide kept for layered upgrades).

## Anthropic

| Model | Model ID | Guide | Status |
| :---- | :------- | :---- | :----- |
| Claude Fable 5.1 | `claude-fable-5-1` | [claude-fable-5-1.md](claude-fable-5-1.md) | current (opt-in only) |
| Claude Opus 5.5 | `claude-opus-5-5` | [claude-opus-5-5.md](claude-opus-5-5.md) | current (default Opus target) |
| Claude Sonnet 5.5 | `claude-sonnet-5-5` | [claude-sonnet-5-5.md](claude-sonnet-5-5.md) | current |
| Claude Haiku 5.5 | `claude-haiku-5-5` | [claude-haiku-5-5.md](claude-haiku-5-5.md) | current |
| Claude Opus 4.8 | `claude-opus-4-8` | [claude-opus-4-8.md](claude-opus-4-8.md) | legacy (layer under Opus 5.5) |
| Claude Opus 4.6 | `claude-opus-4-6` | [claude-opus-4-6.md](claude-opus-4-6.md) | legacy |
| Claude Sonnet 4.5 | `claude-sonnet-4-5` | [claude-sonnet-4-5.md](claude-sonnet-4-5.md) | legacy |

Claude upgrade paths. Apply each step in order, then the target guide.

| If you are on | Target | Path |
| :------------ | :----- | :--- |
| Opus 4.x or older | `claude-opus-5-5` | `claude-opus-4-6.md`, `claude-opus-4-8.md`, then `claude-opus-5-5.md` |
| Opus 5 | `claude-opus-5-5` | `claude-opus-5-5.md` |
| Sonnet 4.x or older | `claude-sonnet-5-5` | `claude-sonnet-4-5.md`, then `claude-sonnet-5-5.md` |
| Sonnet 5 | `claude-sonnet-5-5` | `claude-sonnet-5-5.md` |
| Haiku 4.5 or older | `claude-haiku-5-5` | `claude-haiku-5-5.md` |
| Fable 5 | `claude-fable-5-1` | `claude-fable-5-1.md` |

Default target when the user says "latest Claude model" and names no tier:
`claude-opus-5-5`.

## OpenAI

| Model | Model ID | Guide | Status |
| :---- | :------- | :---- | :----- |
| GPT-6 Astra, GPT-6.1 Sol, GPT-6 Sol, GPT-6 Luna | `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6-sol`, `gpt-6-luna` | [gpt-6.md](gpt-6.md) | current |
| GPT-5.5 | `gpt-5.5` | [gpt-5-5.md](gpt-5-5.md) | legacy (layer under GPT-6) |

## Google

| Model | Model ID | Guide | Status |
| :---- | :------- | :---- | :----- |
| Gemini 3.8 Flash | `gemini-3.8-flash` | [gemini-3-8-flash.md](gemini-3-8-flash.md) | current |

## Not covered

No dedicated guide: other providers, open-weight models, older Gemini
releases. Use `../provider-checklists.md`, then research (see "Freshness"
below).

## Freshness

Every guide carries a `Last verified:` date and a `Source:` line. Model facts
(IDs, prices, defaults, deprecations) change faster than guides do.

- Guide verified within 30 days of today: trust it, still smoke test.
- Older than 30 days, or the target model is missing from this index: fetch
  the provider's official migration page before editing. Record the page and
  date in the migration report.
- Facts from secondary sources are marked as such in the guide. Confirm them
  on the provider page before quoting prices or dates to the user.
- After refreshing a guide, update its `Last verified:` line and this index.

Official sources:

- Anthropic: [models overview](https://platform.claude.com/docs/en/about-claude/models/overview)
  and [model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- OpenAI: [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model)
  and the [models page](https://developers.openai.com/api/docs/models)
- Google: [Gemini models](https://ai.google.dev/gemini-api/docs/models) and the
  [Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog)
