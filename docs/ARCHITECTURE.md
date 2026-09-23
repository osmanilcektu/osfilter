# OSFilter architecture

OSFilter has two deliberately separate products.

## 1. Core TR

Core TR is the unique Türkiye-focused dataset.

Inputs:
- `sources/ads.txt`
- `sources/trackers.txt`
- `sources/security.txt`
- `sources/evidence.csv`
- `allowlist.txt`

Every locally maintained domain requires an evidence row and category match.

Core TR is what should be proposed to managed DNS catalogs such as NextDNS because those catalogs already contain large global lists such as HaGeZi. Re-submitting HaGeZi under another name would add no value.

## 2. Global convenience tiers

These are single-subscription convenience lists for users who want broad protection plus the OSFilter Türkiye overlay.

- Lite: HaGeZi Multi LIGHT + OSFilter local ads/trackers
- Standard: Lite + HaGeZi Multi NORMAL + exact DNS-safe AdGuard Mobile Ads and Turk-AdFilter Lite rules + OSFilter Core TR
- Pro: Standard + HaGeZi Multi PRO + Turkish Ad Hosts
- Ultra: Pro + HaGeZi Multi ULTIMATE + Block List Project Ads/Tracking

The main `osfilter.txt`, `hosts.txt` and `domains.txt` files are the Standard tier.

## 3. Automatic regional aggregates

TR Regional uses licensed Turkish Ad Hosts and exact DNS-safe Turk-AdFilter Lite rules plus `.tr` entries already present in Standard and the reviewed Core TR. TR Regional Ultra uses these sources plus `.tr` entries from Ultra. Both are GPL aggregates, with separate output files, and never write upstream records into Core TR. Sensitive government/education suffixes and login/payment host labels are excluded from the automatic regional selection. Core TR additions still require independent evidence.

## 4. Optional security and gambling categories

Security imports HaGeZi Threat Intelligence Feeds Mini. Gambling combines HaGeZi Gambling Medium with the exact DNS rules of Turk-AdFilter Bahis; Gambling TR uses only the Turkish category feed. These GPL aggregates have separate Adblock, hosts and plain-domain outputs and do not feed the default advertising tiers or the independently evidenced Core TR. The Turkish ABP import skips exceptions, URL paths, cosmetic rules and wildcard expressions. The `stats.json` keys under `optional_categories` count the generated categories; `core_tr.security` and `core_tr.gambling_optional` count only independently evidenced local records.

## Why not union every public list?

Blind unioning creates three problems:

1. false positives increase quickly;
2. duplicate coverage adds size without value;
3. incompatible or unclear upstream licenses can contaminate redistribution.

OSFilter therefore uses a source registry, license policy, sanity thresholds and separate research-only candidates.

## Build safety

For every enabled upstream:
- HTTPS is mandatory;
- the declared plain-domain format accepts only one FQDN per line;
- IP addresses, localhost and malformed entries are rejected;
- duplicates are removed;
- OSFilter allowlist and DNS-blocking ancestors of protected hosts are removed before merge;
- a minimum and maximum entry threshold prevents accidental empty/corrupt upstream builds;
- outputs are sorted deterministically.
- Lite, Standard, Pro, Ultra, both TR Regional sets and previously published optional categories are compared to the previous `dist` publication; over 10% additions or removals stop automatic publishing. A new category can publish only with a nonempty list.
- On the first import of Turk-AdFilter Lite, extra regional additions must be present in the fetched source snapshot; unrelated additions and removals still have the 10% limit. Later releases revert to the regular 10% gate.
- RPZ SOA serials advance from the previous published zones when domain contents change.

## Scale target

100,000 entries is not a quality target by itself. The Standard tier is intentionally over 100k because its global baseline is a mature upstream. The strategic quality target for OSFilter itself is growth of Core TR coverage, low false-positive rate and fast issue response.
