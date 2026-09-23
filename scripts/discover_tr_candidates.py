#!/usr/bin/env python3
"""Discover Turkey-related candidate domains from active upstreams.

This tool never publishes candidates into OSFilter automatically. It creates a
review queue so maintainers can verify category, function and evidence before a
domain is promoted into Core TR.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

from build import ROOT, SOURCES, fetch_upstream, load_domain_file, load_upstreams


def is_turkey_domain(domain: str) -> bool:
    return domain.endswith(".tr")


def local_domains() -> set[str]:
    out: set[str] = set()
    for path in SOURCES.values():
        out.update(load_domain_file(path))
    out.update(load_domain_file(ROOT / "allowlist.txt"))
    return out


def discover() -> list[tuple[str, int, str]]:
    cfg = load_upstreams()
    existing = local_domains()
    membership: dict[str, set[str]] = defaultdict(set)

    for key, spec in cfg["active"].items():
        domains, _ = fetch_upstream(key, spec)
        for domain in domains:
            if is_turkey_domain(domain) and domain not in existing:
                membership[domain].add(key)

    rows = [
        (domain, len(keys), ",".join(sorted(keys)))
        for domain, keys in membership.items()
    ]
    return sorted(rows, key=lambda row: (-row[1], row[0]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="artifacts/tr-candidates.csv",
        help="CSV output path relative to repository root",
    )
    args = parser.parse_args()

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)

    rows = discover()
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["domain", "source_count", "sources"])
        writer.writerows(rows)

    multi = sum(1 for _, count, _ in rows if count >= 2)
    print(
        f"TR candidate scan complete: {len(rows)} candidates, "
        f"{multi} seen in 2+ upstreams -> {output.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
