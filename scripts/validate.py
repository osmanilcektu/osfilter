#!/usr/bin/env python3
"""OSFilter kaynaklarının biçimini, tekrarlarını, kanıtlarını ve kategori çakışmalarını doğrular."""

from __future__ import annotations

import csv
from collections import defaultdict
from urllib.parse import urlparse

from build import ROOT, SOURCES, load_domain_file, load_upstreams, normalize_domain

CATEGORY_KEYS = {
    "Reklam": "ads",
    "İzleyici": "trackers",
    "Güvenlik": "security",
    "Bahis/Kumar": "gambling",
}


def duplicates(items: list[str]) -> set[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for item in items:
        if item in seen:
            dupes.add(item)
        seen.add(item)
    return dupes


def load_evidence() -> dict[str, dict[str, str]]:
    path = ROOT / "sources" / "evidence.csv"
    rows: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"domain", "category", "confidence", "evidence_url", "note"}
        if set(reader.fieldnames or []) != required:
            raise ValueError(
                f"evidence.csv başlıkları tam olarak şu olmalı: {', '.join(sorted(required))}"
            )
        for number, row in enumerate(reader, 2):
            domain = normalize_domain(row["domain"])
            if domain in rows:
                raise ValueError(f"evidence.csv:{number}: duplicate evidence: {domain}")
            if row["category"] not in set(CATEGORY_KEYS.values()):
                raise ValueError(f"evidence.csv:{number}: geçersiz kategori: {row['category']}")
            if row["confidence"] not in {"high", "medium"}:
                raise ValueError(f"evidence.csv:{number}: confidence high veya medium olmalı")
            if not row["evidence_url"].startswith("https://"):
                raise ValueError(f"evidence.csv:{number}: HTTPS kanıt URL'si gerekli")
            rows[domain] = row
    return rows


def validate_upstreams() -> list[str]:
    errors: list[str] = []
    required_fields = {
        "name", "url", "homepage", "license",
        "min_entries", "max_entries", "tier"
    }
    allowed_tiers = {"lite", "standard", "pro", "ultra"}
    allowed_licenses = {"GPL-3.0-only", "Unlicense"}

    try:
        cfg = load_upstreams()
    except (ValueError, OSError) as exc:
        return [f"upstream config okunamadı: {exc}"]

    seen_tiers: set[str] = set()
    for key, spec in cfg.get("active", {}).items():
        missing = required_fields - set(spec)
        if missing:
            errors.append(f"{key}: eksik upstream alanları: {', '.join(sorted(missing))}")
            continue

        if urlparse(spec["url"]).scheme != "https":
            errors.append(f"{key}: kaynak URL HTTPS olmalı")
        if urlparse(spec["homepage"]).scheme != "https":
            errors.append(f"{key}: homepage HTTPS olmalı")
        if spec["tier"] not in allowed_tiers:
            errors.append(f"{key}: bilinmeyen tier: {spec['tier']}")
        else:
            seen_tiers.add(spec["tier"])
        if spec["license"] not in allowed_licenses:
            errors.append(f"{key}: allowlist dışı upstream lisansı: {spec['license']}")
        if not isinstance(spec["min_entries"], int) or not isinstance(spec["max_entries"], int):
            errors.append(f"{key}: min/max entry tam sayı olmalı")
        elif not 0 < spec["min_entries"] < spec["max_entries"]:
            errors.append(f"{key}: geçersiz min/max entry aralığı")

    missing_tiers = allowed_tiers - seen_tiers
    if missing_tiers:
        errors.append(f"upstream tier eksik: {', '.join(sorted(missing_tiers))}")

    return errors


def main() -> None:
    errors: list[str] = []
    errors.extend(validate_upstreams())
    owners: dict[str, list[str]] = defaultdict(list)

    for category, path in SOURCES.items():
        domains = load_domain_file(path)
        for domain in duplicates(domains):
            errors.append(f"{path.relative_to(ROOT)}: duplicate: {domain}")
        for domain in set(domains):
            owners[domain].append(category)

    allow = load_domain_file(ROOT / "allowlist.txt")
    for domain in duplicates(allow):
        errors.append(f"allowlist.txt: duplicate: {domain}")

    for domain, categories in sorted(owners.items()):
        if len(categories) > 1:
            errors.append(
                f"kategori çakışması: {domain} -> {', '.join(sorted(categories))}"
            )

    try:
        evidence = load_evidence()
    except ValueError as exc:
        errors.append(str(exc))
        evidence = {}

    for domain, categories in sorted(owners.items()):
        row = evidence.get(domain)
        if not row:
            errors.append(f"kanıt eksik: {domain}")
            continue
        expected = CATEGORY_KEYS[categories[0]]
        if row["category"] != expected:
            errors.append(
                f"kanıt kategori uyuşmazlığı: {domain}: {row['category']} != {expected}"
            )

    orphan_evidence = sorted(set(evidence) - set(owners))
    for domain in orphan_evidence:
        errors.append(f"kaynaksız kanıt kaydı: {domain}")

    if errors:
        print("OSFilter doğrulaması başarısız:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)

    blocked = set(owners)
    stale_allow = sorted(set(allow) - blocked)
    if stale_allow:
        print(f"Uyarı: {len(stale_allow)} allowlist girdisi şu an hiçbir kaynağı bastırmıyor.")

    high = sum(1 for row in evidence.values() if row["confidence"] == "high")
    print(
        f"OSFilter doğrulaması başarılı: "
        f"{len(blocked)} benzersiz domain, {high} yüksek güven, "
        f"{len(set(allow))} allowlist girdisi"
    )


if __name__ == "__main__":
    main()
