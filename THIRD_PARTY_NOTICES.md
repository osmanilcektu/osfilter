# Third-party notices

OSFilter contains original Türkiye-focused curation and also publishes optional global aggregate tiers.

## HaGeZi DNS Blocklists

OSFilter Lite, Standard and Pro use HaGeZi DNS Blocklists as the global baseline and add OSFilter's independently maintained Türkiye-specific entries and allowlist decisions.

- Project: https://github.com/hagezi/dns-blocklists
- License: GNU General Public License v3.0 only (GPL-3.0-only)
- Source formats used: HaGeZi wildcard domain-only lists
- OSFilter modifications: normalization, deduplication, OSFilter allowlist application, Türkiye-specific additions, metadata and output-format generation

HaGeZi is an independent project and does not endorse OSFilter.

The combined Lite, Standard and Pro outputs are distributed under GPL-3.0-only.

## Research-only projects

The following projects were reviewed for architecture, coverage or validation signals but are not wholesale-imported into the current default OSFilter build:

- AdGuard Filters — GPL-3.0-only
- GoodbyeAds — repository MIT license, but its documented source set contains mixed licensing
- WindowsSpyBlocker — MIT
- AdAway default hosts — CC BY 3.0

See `sources/upstreams.json` for the machine-readable policy.

## OSFilter Core TR

OSFilter's independently curated Core TR dataset is dual-licensed under ODbL-1.0 OR GPL-3.0-only, at the recipient's option. This permits the same original data to remain suitable for database-oriented integrations while also being legally combinable with GPL-3.0 global aggregate tiers.
