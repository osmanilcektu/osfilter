# Changelog

## 0.3.0 — 2026-09-23

### Added

- Daily generated TR Regional and TR Regional Ultra DNS profiles with GPL attribution.
- Turkish Ad Hosts as a separately attributed regional upstream for opt-in Pro/Ultra and TR Regional tiers.
- Pre-publication churn gate comparing Standard and Ultra against the last release.
- Parent-domain protection for allowlisted critical service hosts.
- Regression tests for regional selection, protected hosts and release guard.

### Changed

- Upstream SHA-256 manifest is described as a provenance snapshot, not a pinned integrity lock.
- Core TR stays independently evidenced; imported regional entries remain in separately licensed aggregates.

## 0.2.2 — 2026-09-23

### Added

- Functional safety allowlist applied across all global tiers.
- Provider-adoption checklist for NextDNS and AdGuard DNS.
- Explicit validation for duplicate/overlapping manual and functional allowlist entries.

### Changed

- Documentation now reflects shipped dnsmasq, Unbound and RPZ outputs.
- Build statistics now expose manual vs functional allowlist counts.

## 0.2.1 — 2026-09-23

### Added

- Upstream integrity lock with SHA-256, byte size and final URL provenance.
- HTML/truncated-source guards and parse-ratio sanity checks.
- Deterministic RPZ serial generation.
- Tier monotonicity tests and cumulative tier composition.

### Changed

- Lite/Standard/Pro/Ultra are now cumulative so upgrading a tier never silently unblocks a lower-tier domain.
- Verified distribution sizes: Lite 39,865; Standard 164,051; Pro 245,882; Ultra 587,127.
- Distribution publishing now skips identical generated output.

## 0.2.0 — 2026-09-23

### Added

- Core TR / Lite / Standard / Pro / Ultra tier architecture.
- Daily upstream rebuild and orphan `dist` publication branch.
- HaGeZi Light, Normal, Pro and Ultimate integration under GPL-3.0-only.
- Block List Project Ads + Tracking integration for Ultra.
- Ultra output with 564,725 unique domains in the verified build.
- Machine-readable `sources/upstreams.json` source policy.
- Upstream minimum/maximum size sanity gates.
- Upstream license allowlist validation.
- SHA256 integrity manifest.
- Stable RAW URLs on the `dist` branch.
- Weekly Turkish `.tr` candidate discovery workflow.
- NextDNS Core TR metadata and integration strategy.
- Evidence-backed Core TR validation.
- Dual licensing for original Core TR data.
- Third-party attribution and separate license texts.

### Changed

- Main `osfilter.txt`, `hosts.txt` and `domains.txt` aliases now represent the Standard tier.
- Generated distribution files moved out of `main` and into `dist`.
- NextDNS candidate points to independent Core TR instead of the global aggregate.

## 0.1.0 — 2026-09-23

- Initial OSFilter repository.
- First Türkiye-focused ad/tracker evidence dataset.
- Basic build, validation, issue templates and CI.
