# Security and blocklist safety

OSFilter is a DNS/blocklist project. A false-positive can break login flows, payments, application APIs, software updates or other legitimate functionality.

## Reporting a dangerous false-positive

Use the **Yanlış engelleme / False Positive** issue template and include:

- affected domain;
- affected service/application;
- OSFilter tier;
- reproducible failure;
- why the domain appears functional rather than advertising/tracking.

For account credentials, tokens, private logs or other sensitive information, do not post them in a public GitHub issue.

## Source integrity

Active upstreams are restricted by:

- HTTPS-only source URLs;
- explicit source license;
- minimum/maximum entry thresholds;
- deterministic normalization and deduplication;
- GitHub Actions validation;
- published SHA256 checksums.

An upstream that unexpectedly falls outside its configured size range causes the build to fail rather than publishing suspicious output.

## Security category

Security/phishing data should not be added merely because a domain looks suspicious. Core TR security records require evidence in `sources/evidence.csv`.

OSFilter's global ad/tracking tiers are not a replacement for a dedicated malware/threat-intelligence product.
