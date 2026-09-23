#!/usr/bin/env python3
"""Stop automatic publication when a live upstream causes unusually large churn."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build import ROOT

CHECKED_FILES = (
    "lists/osfilter-lite-domains.txt",
    "domains.txt",
    "lists/osfilter-pro-domains.txt",
    "lists/osfilter-ultra-domains.txt",
    "lists/osfilter-tr-regional-domains.txt",
    "lists/osfilter-tr-regional-ultra-domains.txt",
)
OPTIONAL_FILES = (
    "lists/osfilter-security-domains.txt",
    "lists/osfilter-gambling-domains.txt",
    "lists/osfilter-gambling-tr-domains.txt",
)
MAX_CHANGE_FRACTION = 0.10
REGIONAL_FILES = {
    "lists/osfilter-tr-regional-domains.txt",
    "lists/osfilter-tr-regional-ultra-domains.txt",
}


def read_domains(path: Path) -> set[str]:
    return {
        line.strip() for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def change_fractions(previous: set[str], current: set[str]) -> tuple[float, float]:
    if not previous:
        raise ValueError("previous release is empty")
    return len(current - previous) / len(previous), len(previous - current) / len(previous)


def initial_regional_source_addition(
    filename: str, previous_dir: Path, current_dir: Path,
    previous: set[str], current: set[str],
) -> bool:
    """Allow only the new licensed Turkish feed's own domains on first import."""
    if filename not in REGIONAL_FILES:
        return False
    try:
        old = json.loads((previous_dir / "upstream-lock.json").read_text(encoding="utf-8"))
        new = json.loads((current_dir / "upstream-lock.json").read_text(encoding="utf-8"))
        source = read_domains(current_dir / "artifacts/turk-adfilter-lite-domains.txt")
    except (OSError, ValueError, KeyError):
        return False
    key = "turk_adfilter_lite"
    if key in old.get("sources", {}) or key not in new.get("sources", {}) or not source:
        return False
    if len(source) > new["sources"][key]["entries"]:
        return False
    # Changes unrelated to the new source still have the ordinary 10% budget.
    unrelated = (current - previous) - source
    return len(unrelated) / len(previous) <= MAX_CHANGE_FRACTION


def check_release(previous_dir: Path, current_dir: Path = ROOT) -> None:
    for filename in CHECKED_FILES + OPTIONAL_FILES:
        if filename in OPTIONAL_FILES and not (previous_dir / filename).exists():
            if not read_domains(current_dir / filename):
                raise ValueError(f"{filename}: initial category publication is empty")
            print(f"{filename}: first publication; future changes capped at 10%")
            continue
        previous = read_domains(previous_dir / filename)
        current = read_domains(current_dir / filename)
        added, removed = change_fractions(previous, current)
        print(f"{filename}: +{added:.2%}, -{removed:.2%} vs published release")
        if removed <= MAX_CHANGE_FRACTION and initial_regional_source_addition(
            filename, previous_dir, current_dir, previous, current
        ):
            print(f"{filename}: first Turkish ads import verified against source domains")
            continue
        if added > MAX_CHANGE_FRACTION or removed > MAX_CHANGE_FRACTION:
            raise RuntimeError(
                f"{filename}: upstream churn exceeds {MAX_CHANGE_FRACTION:.0%}; "
                "review upstream-lock.json and changed domains before publishing"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--previous-dir", type=Path, required=True)
    args = parser.parse_args()
    check_release(args.previous_dir)


if __name__ == "__main__":
    main()
