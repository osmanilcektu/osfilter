#!/usr/bin/env python3
"""Stop automatic publication when a live upstream causes unusually large churn."""

from __future__ import annotations

import argparse
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
MAX_CHANGE_FRACTION = 0.10


def read_domains(path: Path) -> set[str]:
    return {
        line.strip() for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def change_fractions(previous: set[str], current: set[str]) -> tuple[float, float]:
    if not previous:
        raise ValueError("previous release is empty")
    return len(current - previous) / len(previous), len(previous - current) / len(previous)


def check_release(previous_dir: Path, current_dir: Path = ROOT) -> None:
    for filename in CHECKED_FILES:
        previous = read_domains(previous_dir / filename)
        current = read_domains(current_dir / filename)
        added, removed = change_fractions(previous, current)
        print(f"{filename}: +{added:.2%}, -{removed:.2%} vs published release")
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
