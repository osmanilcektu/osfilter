"""DNS-safe, upstream-derived Türkiye profiles.

These profiles are GPL aggregates. They are deliberately separate from the
independently evidenced OSFilter Core TR dataset.
"""

from __future__ import annotations

SENSITIVE_SUFFIXES = (
    "gov.tr", "bel.tr", "edu.tr", "k12.tr", "pol.tr", "mil.tr",
)
SENSITIVE_LABELS = {
    "api", "auth", "login", "account", "accounts", "payment", "payments",
    "odeme", "checkout", "bank", "banka", "wallet", "signin", "sso",
}


def is_turkey_domain(domain: str) -> bool:
    return domain.endswith(".tr")


def is_sensitive_domain(domain: str) -> bool:
    if any(domain == suffix or domain.endswith("." + suffix) for suffix in SENSITIVE_SUFFIXES):
        return True
    return bool(set(domain.split(".")) & SENSITIVE_LABELS)


def regional_profile(
    global_domains: list[str], curated_core: list[str],
    regional_upstream: list[str] | None = None,
) -> list[str]:
    """Keep reviewed Core TR plus safe regional upstream and .tr domains."""
    regional_upstream = regional_upstream or []
    return sorted(set(curated_core) | {
        domain for domain in global_domains
        if is_turkey_domain(domain) and not is_sensitive_domain(domain)
    } | {
        domain for domain in regional_upstream if not is_sensitive_domain(domain)
    })
