#!/usr/bin/env python3
"""Build OSFilter Core TR and global aggregate tiers."""

from __future__ import annotations

import hashlib
import ipaddress
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LISTS_DIR = ROOT / "lists"
UPSTREAMS_FILE = ROOT / "sources" / "upstreams.json"
MAX_SOURCE_BYTES = 64 * 1024 * 1024

SOURCES = {
    "Reklam": ROOT / "sources" / "ads.txt",
    "İzleyici": ROOT / "sources" / "trackers.txt",
    "Güvenlik": ROOT / "sources" / "security.txt",
    "Bahis/Kumar": ROOT / "sources" / "gambling.txt",
}

LABEL_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
ABP_DOMAIN_RE = re.compile(r"^\|\|([a-zA-Z0-9._-]+)\^")


def normalize_domain(value: str) -> str:
    value = value.strip().lower()
    if value.startswith("*."):
        value = value[2:]
    value = value.rstrip(".")

    if not value:
        raise ValueError("boş domain")
    if "://" in value or "/" in value or ":" in value or " " in value:
        raise ValueError(f"yalnızca alan adı bekleniyor: {value!r}")

    try:
        ipaddress.ip_address(value)
    except ValueError:
        pass
    else:
        raise ValueError(f"IP adresi domain değildir: {value!r}")

    try:
        ascii_domain = value.encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise ValueError(f"IDN dönüştürülemedi: {value!r}") from exc

    if len(ascii_domain) > 253:
        raise ValueError(f"domain çok uzun: {value!r}")

    labels = ascii_domain.split(".")
    if len(labels) < 2:
        raise ValueError(f"geçerli FQDN değil: {value!r}")
    if any(not LABEL_RE.fullmatch(label) for label in labels):
        raise ValueError(f"geçersiz domain etiketi: {value!r}")

    if ascii_domain in {"localhost.localdomain"}:
        raise ValueError(f"yerel host reddedildi: {value!r}")

    return ascii_domain


def load_domain_file(path: Path) -> list[str]:
    domains: list[str] = []
    if not path.exists():
        raise FileNotFoundError(path)

    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            domains.append(normalize_domain(line))
        except ValueError as exc:
            raise ValueError(f"{path.relative_to(ROOT)}:{number}: {exc}") from exc
    return domains


def unique_sorted(items) -> list[str]:
    return sorted(set(items))


def load_upstreams() -> dict:
    data = json.loads(UPSTREAMS_FILE.read_text(encoding="utf-8"))
    if data.get("schema") != 1:
        raise ValueError("sources/upstreams.json schema desteklenmiyor")
    return data


def parse_external_line(raw: str) -> str | None:
    line = raw.strip()
    if not line or line.startswith("#") or line.startswith("!"):
        return None

    match = ABP_DOMAIN_RE.match(line)
    if match:
        candidate = match.group(1)
    else:
        parts = line.split()
        if len(parts) >= 2 and parts[0] in {"0.0.0.0", "127.0.0.1", "::1"}:
            candidate = parts[1]
        else:
            candidate = parts[0]

    try:
        return normalize_domain(candidate)
    except ValueError:
        return None


def _looks_like_html(raw: bytes) -> bool:
    sample = raw[:4096].lstrip().lower()
    return (
        sample.startswith(b"<!doctype html")
        or sample.startswith(b"<html")
        or b"<html" in sample[:512]
    )


def fetch_upstream(key: str, spec: dict) -> tuple[list[str], dict]:
    url = spec["url"]
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"{key}: upstream HTTPS olmalı")

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "OSFilter/1.0 (+https://github.com/osmanilcektu/osfilter)",
            "Accept": "text/plain,*/*;q=0.1",
        },
    )

    with urllib.request.urlopen(req, timeout=90) as response:
        final_url = response.geturl()
        raw_bytes = response.read(MAX_SOURCE_BYTES + 1)

    if len(raw_bytes) > MAX_SOURCE_BYTES:
        raise RuntimeError(
            f"{key}: upstream {MAX_SOURCE_BYTES // (1024 * 1024)} MiB sınırını aştı"
        )
    if _looks_like_html(raw_bytes):
        raise RuntimeError(f"{key}: text blocklist yerine HTML döndü")

    raw_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    raw = raw_bytes.decode("utf-8-sig", errors="replace")
    raw_lines = raw.splitlines()
    candidate_lines = sum(
        1
        for line in raw_lines
        if line.strip() and not line.lstrip().startswith(("#", "!"))
    )

    domains = unique_sorted(
        domain
        for domain in (parse_external_line(line) for line in raw_lines)
        if domain is not None
    )

    minimum = int(spec["min_entries"])
    maximum = int(spec["max_entries"])
    if not minimum <= len(domains) <= maximum:
        raise RuntimeError(
            f"{key}: beklenmeyen upstream boyutu {len(domains)} "
            f"(beklenen {minimum}..{maximum})"
        )

    if candidate_lines and len(domains) / candidate_lines < 0.75:
        raise RuntimeError(
            f"{key}: parse oranı şüpheli "
            f"({len(domains)}/{candidate_lines} geçerli domain)"
        )

    return domains, {
        "name": spec["name"],
        "url": url,
        "final_url": final_url,
        "homepage": spec["homepage"],
        "license": spec["license"],
        "entries": len(domains),
        "bytes": len(raw_bytes),
        "sha256": raw_sha256,
    }


def adblock_header(
    title: str,
    description: str,
    *,
    license_id: str,
    upstream: str | None = None,
) -> list[str]:
    lines = [
        "[Adblock Plus 2.0]",
        f"! Title: {title}",
        "! Homepage: https://github.com/osmanilcektu/osfilter",
        "! Expires: 12 hours",
        f"! Description: {description}",
        "! Maintainer: Osman İlçektuğ (@osmanilcektu)",
        f"! License: {license_id}",
    ]
    if upstream:
        lines.append(f"! Upstream: {upstream}")
        lines.append(
            "! Third-party notices: "
            "https://github.com/osmanilcektu/osfilter/blob/main/THIRD_PARTY_NOTICES.md"
        )
    lines.extend(
        [
            "! Generated by scripts/build.py — do not edit generated outputs directly.",
            "",
        ]
    )
    return lines


def render_adblock(
    title: str,
    description: str,
    domains: list[str],
    *,
    license_id: str,
    upstream: str | None = None,
) -> str:
    lines = adblock_header(
        title,
        description,
        license_id=license_id,
        upstream=upstream,
    )
    lines.extend(f"||{domain}^" for domain in domains)
    return "\n".join(lines).rstrip() + "\n"


def render_hosts(
    title: str,
    domains: list[str],
    *,
    license_id: str,
    upstream: str | None = None,
) -> str:
    lines = [
        f"# {title}",
        "# Homepage: https://github.com/osmanilcektu/osfilter",
        f"# License: {license_id}",
    ]
    if upstream:
        lines.append(f"# Upstream: {upstream}")
        lines.append(
            "# Third-party notices: "
            "https://github.com/osmanilcektu/osfilter/blob/main/THIRD_PARTY_NOTICES.md"
        )
    lines.extend(
        [
            "# Generated by scripts/build.py — do not edit directly.",
            "",
        ]
    )
    lines.extend(f"0.0.0.0 {domain}" for domain in domains)
    return "\n".join(lines).rstrip() + "\n"


def render_domains(
    title: str,
    domains: list[str],
    *,
    license_id: str,
    upstream: str | None = None,
) -> str:
    lines = [
        f"# {title}",
        "# Homepage: https://github.com/osmanilcektu/osfilter",
        f"# License: {license_id}",
    ]
    if upstream:
        lines.append(f"# Upstream: {upstream}")
        lines.append(
            "# Third-party notices: "
            "https://github.com/osmanilcektu/osfilter/blob/main/THIRD_PARTY_NOTICES.md"
        )
    lines.extend(
        [
            "# Generated by scripts/build.py — do not edit directly.",
            "",
        ]
    )
    lines.extend(domains)
    return "\n".join(lines).rstrip() + "\n"


def render_dnsmasq(
    title: str,
    domains: list[str],
    *,
    license_id: str,
    upstream: str | None = None,
) -> str:
    lines = [
        f"# {title}",
        "# dnsmasq 2.86+ format: address=/domain/#",
        "# Homepage: https://github.com/osmanilcektu/osfilter",
        f"# License: {license_id}",
    ]
    if upstream:
        lines.append(f"# Upstream: {upstream}")
    lines.extend(
        [
            "# Generated by scripts/build.py — do not edit directly.",
            "",
        ]
    )
    lines.extend(f"address=/{domain}/#" for domain in domains)
    return "\n".join(lines).rstrip() + "\n"


def render_unbound(
    title: str,
    domains: list[str],
    *,
    license_id: str,
    upstream: str | None = None,
) -> str:
    lines = [
        f"# {title}",
        "# Include this file from unbound.conf.",
        "# Homepage: https://github.com/osmanilcektu/osfilter",
        f"# License: {license_id}",
    ]
    if upstream:
        lines.append(f"# Upstream: {upstream}")
    lines.extend(
        [
            "# Generated by scripts/build.py — do not edit directly.",
            "",
            "server:",
        ]
    )
    lines.extend(f'    local-zone: "{domain}" always_null' for domain in domains)
    return "\n".join(lines).rstrip() + "\n"


def deterministic_serial(domains: list[str]) -> int:
    payload = "\n".join(domains).encode("utf-8")
    serial = int.from_bytes(hashlib.sha256(payload).digest()[:4], "big")
    return serial or 1


def render_rpz(
    title: str,
    domains: list[str],
    *,
    license_id: str,
    upstream: str | None = None,
) -> str:
    serial = deterministic_serial(domains)
    lines = [
        f"; {title}",
        "; BIND Response Policy Zone (RPZ), NXDOMAIN policy.",
        "; Homepage: https://github.com/osmanilcektu/osfilter",
        f"; License: {license_id}",
    ]
    if upstream:
        lines.append(f"; Upstream: {upstream}")
    lines.extend(
        [
            "; Generated by scripts/build.py — do not edit directly.",
            "$TTL 60",
            f"@ IN SOA localhost. root.localhost. ({serial} 1h 15m 30d 2h)",
            "@ IN NS localhost.",
            "",
        ]
    )
    for domain in domains:
        lines.append(f"{domain} CNAME .")
        lines.append(f"*.{domain} CNAME .")
    return "\n".join(lines).rstrip() + "\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def assert_tier_nesting(
    lite: list[str],
    standard: list[str],
    pro: list[str],
    ultra: list[str],
) -> None:
    tiers = {
        "lite": set(lite),
        "standard": set(standard),
        "pro": set(pro),
        "ultra": set(ultra),
    }
    for child, parent in [
        ("lite", "standard"),
        ("standard", "pro"),
        ("pro", "ultra"),
    ]:
        missing = tiers[child] - tiers[parent]
        if missing:
            sample = ", ".join(sorted(missing)[:5])
            raise RuntimeError(
                f"tier nesting bozuk: {child} -> {parent}; "
                f"{len(missing)} domain üst tier'da yok (örn: {sample})"
            )


def main() -> None:
    allow = set(load_domain_file(ROOT / "allowlist.txt"))

    categories: dict[str, list[str]] = {}
    for name, path in SOURCES.items():
        categories[name] = unique_sorted(
            domain for domain in load_domain_file(path) if domain not in allow
        )

    local_ads_trackers = unique_sorted(categories["Reklam"] + categories["İzleyici"])
    local_core = unique_sorted(
        categories["Reklam"] + categories["İzleyici"] + categories["Güvenlik"]
    )
    local_gambling = unique_sorted(categories["Bahis/Kumar"])

    cfg = load_upstreams()
    tier_to_domains: dict[str, list[str]] = {}
    upstream_stats: dict[str, dict] = {}

    for key, spec in cfg["active"].items():
        fetched, meta = fetch_upstream(key, spec)
        filtered = [domain for domain in fetched if domain not in allow]
        tier_to_domains.setdefault(spec["tier"], []).extend(filtered)
        upstream_stats[key] = meta

    for tier in list(tier_to_domains):
        tier_to_domains[tier] = unique_sorted(tier_to_domains[tier])

    # OSFilter tiers are intentionally cumulative. Upstream projects may move
    # individual domains between their own tiers; OSFilter guarantees that
    # increasing protection never silently unblocks a domain from a lower tier.
    lite = unique_sorted(tier_to_domains["lite"] + local_ads_trackers)
    standard = unique_sorted(lite + tier_to_domains["standard"] + local_core)
    pro = unique_sorted(standard + tier_to_domains["pro"] + local_core)
    ultra = unique_sorted(pro + tier_to_domains["ultra"] + local_core)

    minimum_tier_sizes = {
        "lite": 30000,
        "standard": 100000,
        "pro": 150000,
        "ultra": 250000,
    }
    tier_sets = {
        "lite": lite,
        "standard": standard,
        "pro": pro,
        "ultra": ultra,
    }
    for tier_name, domains in tier_sets.items():
        if len(domains) < minimum_tier_sizes[tier_name]:
            raise RuntimeError(
                f"{tier_name}: aggregate unexpectedly small: {len(domains)} "
                f"< {minimum_tier_sizes[tier_name]}"
            )

    assert_tier_nesting(lite, standard, pro, ultra)

    def tier_notice(tier_name: str) -> str:
        names = [
            upstream_stats[key]["name"]
            for key, spec in cfg["active"].items()
            if spec["tier"] == tier_name
        ]
        return " + ".join(names + ["OSFilter Core TR"])

    # Main aliases = Standard tier.
    write(
        ROOT / "osfilter.txt",
        render_adblock(
            "OSFilter — Standard",
            "Balanced global DNS blocking plus independently curated Türkiye-specific OSFilter coverage.",
            standard,
            license_id="GPL-3.0-only",
            upstream=tier_notice("standard"),
        ),
    )
    write(
        ROOT / "hosts.txt",
        render_hosts(
            "OSFilter — Standard hosts",
            standard,
            license_id="GPL-3.0-only",
            upstream=tier_notice("standard"),
        ),
    )
    write(
        ROOT / "domains.txt",
        render_domains(
            "OSFilter — Standard domains",
            standard,
            license_id="GPL-3.0-only",
            upstream=tier_notice("standard"),
        ),
    )
    write(
        ROOT / "dnsmasq.conf",
        render_dnsmasq(
            "OSFilter — Standard dnsmasq",
            standard,
            license_id="GPL-3.0-only",
            upstream=tier_notice("standard"),
        ),
    )
    write(
        ROOT / "unbound.conf",
        render_unbound(
            "OSFilter — Standard Unbound",
            standard,
            license_id="GPL-3.0-only",
            upstream=tier_notice("standard"),
        ),
    )
    write(
        ROOT / "rpz.zone",
        render_rpz(
            "OSFilter — Standard RPZ",
            standard,
            license_id="GPL-3.0-only",
            upstream=tier_notice("standard"),
        ),
    )

    # Core TR: original OSFilter dataset.
    core_outputs = [
        (
            LISTS_DIR / "osfilter-core.txt",
            render_adblock(
                "OSFilter — Core TR",
                "Evidence-backed Türkiye-focused advertising, tracking and security domains maintained by OSFilter.",
                local_core,
                license_id="ODbL-1.0 OR GPL-3.0-only",
            ),
        ),
        (
            LISTS_DIR / "osfilter-core-hosts.txt",
            render_hosts(
                "OSFilter — Core TR hosts",
                local_core,
                license_id="ODbL-1.0 OR GPL-3.0-only",
            ),
        ),
        (
            LISTS_DIR / "osfilter-core-domains.txt",
            render_domains(
                "OSFilter — Core TR domains",
                local_core,
                license_id="ODbL-1.0 OR GPL-3.0-only",
            ),
        ),
        (
            LISTS_DIR / "osfilter-core-dnsmasq.conf",
            render_dnsmasq(
                "OSFilter — Core TR dnsmasq",
                local_core,
                license_id="ODbL-1.0 OR GPL-3.0-only",
            ),
        ),
        (
            LISTS_DIR / "osfilter-core-unbound.conf",
            render_unbound(
                "OSFilter — Core TR Unbound",
                local_core,
                license_id="ODbL-1.0 OR GPL-3.0-only",
            ),
        ),
        (
            LISTS_DIR / "osfilter-core-rpz.zone",
            render_rpz(
                "OSFilter — Core TR RPZ",
                local_core,
                license_id="ODbL-1.0 OR GPL-3.0-only",
            ),
        ),
    ]
    for path, rendered in core_outputs:
        write(path, rendered)

    # Global tiers.
    for tier_name, domains, title, description in [
        (
            "lite",
            lite,
            "OSFilter — Lite",
            "Low-breakage global baseline plus OSFilter Türkiye advertising/tracking coverage.",
        ),
        (
            "pro",
            pro,
            "OSFilter — Pro",
            "Extended global protection plus independently curated OSFilter Türkiye coverage.",
        ),
        (
            "ultra",
            ultra,
            "OSFilter — Ultra",
            "Aggressive multi-source advertising/tracking protection using HaGeZi Ultimate, Block List Project and OSFilter Türkiye curation.",
        ),
    ]:
        write(
            LISTS_DIR / f"osfilter-{tier_name}.txt",
            render_adblock(
                title,
                description,
                domains,
                license_id="GPL-3.0-only",
                upstream=tier_notice(tier_name),
            ),
        )
        write(
            LISTS_DIR / f"osfilter-{tier_name}-hosts.txt",
            render_hosts(
                f"{title} hosts",
                domains,
                license_id="GPL-3.0-only",
                upstream=tier_notice(tier_name),
            ),
        )
        write(
            LISTS_DIR / f"osfilter-{tier_name}-domains.txt",
            render_domains(
                f"{title} domains",
                domains,
                license_id="GPL-3.0-only",
                upstream=tier_notice(tier_name),
            ),
        )

    write(
        LISTS_DIR / "osfilter-security.txt",
        render_adblock(
            "OSFilter — Security TR",
            "Locally verified OSFilter security/phishing domains.",
            unique_sorted(categories["Güvenlik"]),
            license_id="ODbL-1.0 OR GPL-3.0-only",
        ),
    )
    write(
        LISTS_DIR / "osfilter-gambling.txt",
        render_adblock(
            "OSFilter — Gambling TR",
            "Optional Türkiye-focused gambling category maintained independently by OSFilter.",
            local_gambling,
            license_id="ODbL-1.0 OR GPL-3.0-only",
        ),
    )

    stats = {
        "schema": 3,
        "core_tr": {
            "total": len(local_core),
            "ads": len(categories["Reklam"]),
            "trackers": len(categories["İzleyici"]),
            "security": len(categories["Güvenlik"]),
            "gambling_optional": len(local_gambling),
        },
        "tiers": {
            "lite": len(lite),
            "standard": len(standard),
            "pro": len(pro),
            "ultra": len(ultra),
        },
        "allowlist": len(allow),
        "upstreams": upstream_stats,
    }
    write(ROOT / "stats.json", json.dumps(stats, ensure_ascii=False, indent=2) + "\n")
    write(
        ROOT / "upstream-lock.json",
        json.dumps(
            {
                "schema": 1,
                "sources": upstream_stats,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )

    checksum_targets = [
        ROOT / "osfilter.txt",
        ROOT / "hosts.txt",
        ROOT / "domains.txt",
        ROOT / "stats.json",
        ROOT / "upstream-lock.json",
        ROOT / "dnsmasq.conf",
        ROOT / "unbound.conf",
        ROOT / "rpz.zone",
        *sorted(LISTS_DIR.glob("*")),
    ]
    checksum_lines = []
    for path in checksum_targets:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        checksum_lines.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    write(ROOT / "SHA256SUMS", "\n".join(checksum_lines) + "\n")

    print(
        "OSFilter build complete: "
        f"core={len(local_core)}, lite={len(lite)}, "
        f"standard={len(standard)}, pro={len(pro)}, ultra={len(ultra)}"
    )


if __name__ == "__main__":
    main()
