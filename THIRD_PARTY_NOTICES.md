# Third-party notices

OSFilter contains an independently maintained Türkiye-focused Core TR dataset and separately publishes global aggregate tiers.

## HaGeZi DNS Blocklists

OSFilter Lite, Standard, Pro and Ultra use HaGeZi DNS Blocklists as global baseline components.

- Project: https://github.com/hagezi/dns-blocklists
- License: GNU General Public License v3.0 only (GPL-3.0-only)
- Inputs: HaGeZi domain-only wildcard outputs
- OSFilter modifications: normalization, deduplication, allowlist application, Türkiye-specific additions, tier composition, metadata and output-format generation

HaGeZi is an independent project and does not endorse OSFilter.

## Block List Project

OSFilter Ultra additionally uses the Block List Project Ads and Tracking domain lists.

- Project: https://github.com/blocklistproject/Lists
- License: Unlicense / public-domain dedication
- Inputs: Ads and Tracking plain-domain outputs
- OSFilter modifications: normalization, deduplication, allowlist application and tier composition

The Block List Project is independent and does not endorse OSFilter.

## Research-only projects

Reviewed for architecture, coverage or validation, but not wholesale-imported into the current default build:

- AdGuard Filters — GPL-3.0-only
- GoodbyeAds — repository MIT license, but documented upstream provenance contains mixed licensing
- WindowsSpyBlocker — MIT
- AdAway default hosts — CC BY 3.0
- StevenBlack unified hosts — mixed upstream licenses

See `sources/upstreams.json` for the machine-readable source policy.

## OSFilter Core TR

OSFilter's independently curated Core TR dataset is dual-licensed under ODbL-1.0 OR GPL-3.0-only, at the recipient's option. This permits database-oriented integrations while also allowing the original OSFilter data to be legally combined with GPL-3.0 global tiers.
