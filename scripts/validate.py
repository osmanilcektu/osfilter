#!/usr/bin/env python3
"""OSFilter kaynaklarının biçimini, tekrarlarını ve kategori çakışmalarını doğrular."""

from __future__ import annotations

from collections import defaultdict

from build import ROOT, SOURCES, load_domain_file


def duplicates(items: list[str]) -> set[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for item in items:
        if item in seen:
            dupes.add(item)
        seen.add(item)
    return dupes


def main() -> None:
    errors: list[str] = []
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

    if errors:
        print("OSFilter doğrulaması başarısız:")
        for error in errors:
            print(f" - {error}")
        raise SystemExit(1)

    blocked = set(owners)
    stale_allow = sorted(set(allow) - blocked)
    if stale_allow:
        print(f"Uyarı: {len(stale_allow)} allowlist girdisi şu an hiçbir kaynağı bastırmıyor.")

    print(
        f"OSFilter doğrulaması başarılı: "
        f"{len(blocked)} benzersiz kaynak domain, {len(set(allow))} allowlist girdisi"
    )


if __name__ == "__main__":
    main()
