# Changelog

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
