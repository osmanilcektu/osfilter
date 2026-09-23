#!/usr/bin/env python3
"""Discover and prioritize Turkey-related candidate domains.

Candidates are NEVER promoted to Core TR automatically. This script creates a
review queue with an explainable priority score and a breakage-risk flag.
Human verification + evidence.csv is required before promotion.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

from build import (ROOT, SOURCES, fetch_upstream, load_domain_file,
                   load_upstreams, protected_block_rules)
from regional import is_sensitive_domain, is_turkey_domain

AD_PATTERNS = (
    "ad.", "ads.", "adserver", "adservice", "advert", "reklam",
    "sponsor", "adtarget", "admatic", "adklik", "admax", "adplay",
    "adworld", "pixad", "bumerang",
)
TRACKER_PATTERNS = (
    "analytics", "analytic", "metric", "metrica", "metrika", "matomo",
    "countly", "tracker", "tracking", "telemetry", "pixel", "stat",
    "sayac", "collector", "collect.", "geoloc",
)
CRITICAL_PATTERNS = (
    ".gov.tr", ".bel.tr", "saglik.", "eba.", "mgm.",
    "bank", "banka", "akbank", "isbank", "ziraat", "vakif", "garanti",
    "teb.", "kkb.", "bkmobil", "payment", "odeme", "pay.", "wallet",
    "turktelekom", "vodafone", "turkcell", "superonline",
    "login", "auth", "account", "api-", "appconnect", "cdn-",
)
FUNCTIONAL_PATTERNS = (
    "api.", "api-", "cdn.", "cdn-", "fileserver", "static.",
    "assets.", "image.", "images.", "geoip.", "config.", "update.",
)


def local_domains() -> set[str]:
    out: set[str] = set()
    for path in SOURCES.values():
        out.update(load_domain_file(path))
    allowed = set(load_domain_file(ROOT / "allowlist.txt"))
    allowed.update(load_domain_file(ROOT / "sources" / "functional-allowlist.txt"))
    out.update(protected_block_rules(allowed))
    return out


def _contains_any(domain: str, patterns: tuple[str, ...]) -> list[str]:
    return [pattern for pattern in patterns if pattern in domain]


def classify_candidate(domain: str, project_count: int) -> dict[str, str | int]:
    """Return explainable review metadata. Never decides blocking automatically."""
    ad_hits = _contains_any(domain, AD_PATTERNS)
    tracker_hits = _contains_any(domain, TRACKER_PATTERNS)
    critical_hits = _contains_any(domain, CRITICAL_PATTERNS)
    functional_hits = _contains_any(domain, FUNCTIONAL_PATTERNS)

    score = min(project_count * 15, 60)
    reasons: list[str] = [f"{project_count} bağımsız kaynak projesi"]

    if ad_hits:
        score += 30
        reasons.append("ad-pattern:" + ",".join(ad_hits[:3]))
    if tracker_hits:
        score += 20
        reasons.append("tracker-pattern:" + ",".join(tracker_hits[:3]))

    risk = "normal"
    if functional_hits:
        score -= 15
        risk = "review"
        reasons.append("functional-pattern:" + ",".join(functional_hits[:3]))
    if critical_hits:
        score -= 40
        risk = "critical"
        reasons.append("critical-pattern:" + ",".join(critical_hits[:3]))

    if ad_hits and not critical_hits:
        suggested = "ads"
    elif tracker_hits and not critical_hits:
        suggested = "trackers"
    else:
        suggested = "manual"

    score = max(0, min(score, 100))

    if risk == "critical":
        disposition = "do-not-auto-promote"
    elif score >= 70 and suggested in {"ads", "trackers"}:
        disposition = "priority-review"
    elif score >= 45:
        disposition = "review"
    else:
        disposition = "low-priority"

    return {
        "priority_score": score,
        "risk": risk,
        "suggested_category": suggested,
        "disposition": disposition,
        "reason": "; ".join(reasons),
    }


def independent_projects(keys: set[str], projects: dict[str, str]) -> int:
    """Several tiers from one maintainer are one corroborating project."""
    return len({projects[key] for key in keys})


def discover() -> list[dict[str, str | int]]:
    cfg = load_upstreams()
    existing = local_domains()
    membership: dict[str, set[str]] = defaultdict(set)
    projects = {key: spec["homepage"].rstrip("/") for key, spec in cfg["active"].items()}

    for key, spec in cfg["active"].items():
        domains, _ = fetch_upstream(key, spec)
        for domain in domains:
            regional = is_turkey_domain(domain) or spec.get("region") == "tr"
            if regional and domain not in existing and not is_sensitive_domain(domain):
                membership[domain].add(key)

    rows: list[dict[str, str | int]] = []
    for domain, keys in membership.items():
        project_count = independent_projects(keys, projects)
        meta = classify_candidate(domain, project_count)
        rows.append(
            {
                "domain": domain,
                "source_count": len(keys),
                "project_count": project_count,
                "sources": ",".join(sorted(keys)),
                **meta,
            }
        )

    return sorted(
        rows,
        key=lambda row: (
            row["risk"] == "critical",
            -int(row["priority_score"]),
            -int(row["project_count"]),
            str(row["domain"]),
        ),
    )


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
    fieldnames = [
        "domain",
        "source_count",
        "project_count",
        "sources",
        "priority_score",
        "risk",
        "suggested_category",
        "disposition",
        "reason",
    ]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    multi = sum(1 for row in rows if int(row["project_count"]) >= 2)
    priority = sum(1 for row in rows if row["disposition"] == "priority-review")
    critical = sum(1 for row in rows if row["risk"] == "critical")
    print(
        f"TR candidate scan complete: {len(rows)} candidates, "
        f"{multi} seen in 2+ independent projects, {priority} priority-review, "
        f"{critical} critical-risk -> {output}"
    )


if __name__ == "__main__":
    main()
