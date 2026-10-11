#!/usr/bin/env python3
"""Report model guides whose `Last verified:` date is too old.

Exit code 0 when every dated guide is fresh, 1 when any is stale. Legacy guides
(`Last verified: legacy ...`) are skipped. Used by the weekly freshness
workflow, which opens an issue with this report.

Usage: python3 scripts/check_freshness.py [root] [--max-age-days 30] [--today YYYY-MM-DD]
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


def stale_guides(root: Path, max_age_days: int, today: date) -> list[tuple[str, int, str]]:
    """Return (guide, age_in_days, source_line) for every dated guide past max age."""
    stale = []
    for guide in sorted((root / "references" / "models").glob("*.md")):
        if guide.name == "INDEX.md":
            continue
        head = "\n".join(guide.read_text(encoding="utf-8").splitlines()[:20])
        verified = re.search(r"^Last verified: (\d{4})-(\d{2})-(\d{2})\b", head, re.MULTILINE)
        if not verified:
            continue  # legacy guide (or validate_skill.py will flag it)
        age = (today - date(*map(int, verified.groups()))).days
        if age > max_age_days:
            # Source may wrap onto continuation lines: join until a blank line or the next key.
            source = re.search(
                r"^Source: (.+(?:\n(?![A-Za-z ]+: |\n|#).+)*)", head, re.MULTILINE
            )
            stale.append((guide.name, age, " ".join(source.group(1).split()) if source else ""))
    return stale


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--max-age-days", type=int, default=30)
    ap.add_argument("--today", default=None, help="override today's date (YYYY-MM-DD)")
    args = ap.parse_args()

    today = date.fromisoformat(args.today) if args.today else date.today()
    stale = stale_guides(Path(args.root).resolve(), args.max_age_days, today)
    if not stale:
        print(f"All dated model guides were verified within {args.max_age_days} days.")
        return

    print(f"{len(stale)} model guide(s) older than {args.max_age_days} days:\n")
    for name, age, source in stale:
        print(f"- references/models/{name}: {age} days old. Source: {source}")
    print(
        "\nRe-check each guide against the provider's official page, fix any drift, "
        "then update its `Last verified:` line. Also check whether the provider "
        "shipped a model that has no guide in references/models/INDEX.md."
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
