#!/usr/bin/env python3
"""Validate the public skill package without requiring a local Codex install."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
REQUIRED_PATHS = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/migration-playbook.md",
    "references/migration-patterns.md",
    "references/prompt-template-research.md",
    "references/provider-checklists.md",
    "references/validation-proof.md",
    "references/output-style.md",
    "templates/migration-starter-prompt.md",
    "examples/example-prompts.md",
    "examples/example-output.md",
]


def fail(message: str) -> None:
    print(f"[ERROR] {message}")
    sys.exit(1)


def parse_simple_frontmatter(text: str) -> dict[str, str]:
    """Parse simple single-line key: value frontmatter.

    This intentionally does not handle multi-line values, comments, or
    nested YAML — the skill frontmatter should stay flat and simple.
    """
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail("SKILL.md must start with YAML frontmatter delimited by ---")

    data: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            fail(f"Invalid frontmatter line: {raw_line}")
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in data:
            fail(f"Duplicate frontmatter key: {key}")
        data[key] = value
    return data


def validate_skill(root: Path) -> None:
    for rel_path in REQUIRED_PATHS:
        if not (root / rel_path).is_file():
            fail(f"Missing required file: {rel_path}")

    skill_md = root / "SKILL.md"
    frontmatter = parse_simple_frontmatter(skill_md.read_text(encoding="utf-8"))
    keys = set(frontmatter)

    missing = ALLOWED_FRONTMATTER_KEYS - keys
    if missing:
        fail(f"Missing frontmatter keys: {', '.join(sorted(missing))}")

    unexpected = keys - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        fail(f"Unexpected frontmatter keys: {', '.join(sorted(unexpected))}")

    name = frontmatter["name"].strip('"')
    # Minimum 2 chars, max 64 chars, lowercase alphanumeric with hyphens,
    # must start and end with an alphanumeric character.
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}[a-z0-9]", name):
        fail("Skill name must be lowercase hyphen-case and under 64 characters")

    description = frontmatter["description"].strip('"')
    if len(description) < 80:
        fail("Skill description is too short to trigger reliably")

    openai_yaml = (root / "agents/openai.yaml").read_text(encoding="utf-8")
    for expected in ("display_name:", "short_description:", "default_prompt:"):
        if expected not in openai_yaml:
            fail(f"agents/openai.yaml missing {expected}")

    output_example = (root / "examples/example-output.md").read_text(
        encoding="utf-8"
    )
    for heading in (
        "Migration Summary",
        "Existing Work and Remaining Work",
        "Required Compatibility Fixes",
        "Validation Results",
        "Proof Evidence",
        "Rollback Notes",
    ):
        if heading not in output_example:
            fail(f"Example output missing section: {heading}")


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.is_dir():
        fail(f"Not a directory: {root}")
    validate_skill(root)
    print("Skill package is valid.")


if __name__ == "__main__":
    main()
