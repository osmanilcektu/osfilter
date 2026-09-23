# Managed DNS / provider adoption plan

OSFilter has two different adoption targets:

1. **Core TR** — original Turkey-focused data intended for regional catalog inclusion.
2. **Global tiers** — aggregation products intended for direct subscription, self-hosted DNS and advanced users.

The regional Core TR list is the submission candidate. Repackaging a large global upstream is not a useful reason for NextDNS or AdGuard to add another catalog entry.

## NextDNS

NextDNS privacy blocklists are represented in the public `nextdns/blocklists` repository as JSON metadata that points to one or more source URLs.

OSFilter already ships a candidate metadata file:

`integrations/nextdns/osfilter.json`

It points to the stable Core TR distribution URL:

`https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-core-hosts.txt`

NextDNS does not publish a detailed formal acceptance scorecard comparable to AdGuard's HostlistsRegistry rules. Existing additions and requests are handled in the public blocklists repository. Therefore the project should build evidence before requesting inclusion:

- stable public RAW endpoint;
- active maintenance history;
- regional uniqueness;
- low false-positive rate;
- issue/reporting process;
- explainable provenance;
- reliable CI and update cadence;
- real users/stars/community interest.

## AdGuard DNS / HostlistsRegistry

AdGuard publicly documents stricter third-party list requirements. As of September 2026, their HostlistsRegistry documentation says a list should:

- target DNS-level content blocking;
- preferably be original rather than a compilation;
- have a clear purpose;
- have a public place for complaints/discussion;
- normally have at least 50 GitHub stars, or comparable community activity;
- normally be actively supported for at least six months;
- normally receive at least 10 updates per month;
- avoid excessive false positives and opinion-only blocking.

They also note that a regionally popular list without alternatives may be accepted even when it does not satisfy every normal popularity requirement.

This reinforces why **Core TR**, not Ultra, should be the provider-submission product.

References:
- https://github.com/AdguardTeam/HostlistsRegistry
- https://adguard-dns.io/kb/private-dns/setting-up-filtering/blocklists/
- https://github.com/nextdns/blocklists

## Submission readiness gates

Do not submit Core TR upstream until these are true:

- [ ] at least 6 months of continuous maintenance history;
- [ ] at least 10 meaningful updates/month for several consecutive months;
- [ ] false-positive issue template actively used and response history visible;
- [ ] stable dist URL with no breaking path changes;
- [ ] Core TR has substantial Turkey-specific coverage not already trivially available elsewhere;
- [ ] evidence/provenance exists for every Core TR entry;
- [ ] critical functional endpoints remain protected by regression checks;
- [ ] public release notes and statistics are current;
- [ ] project has meaningful user adoption/community signals.

## What to optimize for

Provider adoption should not be gamed by inflating domain counts.

For Core TR the important metrics are:

- unique Turkey-specific coverage;
- false-positive rate;
- maintenance latency;
- evidence quality;
- update reliability;
- number of real user reports fixed;
- overlap with existing global lists;
- number of domains that add actual regional value.

The large global tiers are useful products, but Core TR is the differentiator.
