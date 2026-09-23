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
- Standard: Lite + HaGeZi Multi NORMAL + OSFilter Core TR
- Pro: Standard + HaGeZi Multi PRO + Turkish Ad Hosts
- Ultra: Pro + HaGeZi Multi ULTIMATE + Block List Project Ads/Tracking

The main `osfilter.txt`, `hosts.txt` and `domains.txt` files are the Standard tier.

## 3. Automatic regional aggregates

TR Regional uses licensed Turkish Ad Hosts DNS data plus `.tr` entries already present in Standard and the reviewed Core TR. TR Regional Ultra uses the same regional source plus `.tr` entries from Ultra. Both are GPL aggregates, with separate output files, and never write upstream records into Core TR. Sensitive government/education suffixes and login/payment host labels are excluded from the automatic regional selection. Core TR additions still require independent evidence.

## Why not union every public list?

Blind unioning creates three problems:

1. false positives increase quickly;
2. duplicate coverage adds size without value;
3. incompatible or unclear upstream licenses can contaminate redistribution.

OSFilter therefore uses a source registry, license policy, sanity thresholds and separate research-only candidates.

## Build safety

For every enabled upstream:
- HTTPS is mandatory;
- the response is normalized to FQDNs;
- IP addresses, localhost and malformed entries are rejected;
- duplicates are removed;
- OSFilter allowlist and DNS-blocking ancestors of protected hosts are removed before merge;
- a minimum and maximum entry threshold prevents accidental empty/corrupt upstream builds;
- outputs are sorted deterministically.
- Standard and Ultra release sets are compared to the previous `dist` publication; over 10% additions or removals stop automatic publishing.

## Scale target

100,000 entries is not a quality target by itself. The Standard tier is intentionally over 100k because its global baseline is a mature upstream. The strategic quality target for OSFilter itself is growth of Core TR coverage, low false-positive rate and fast issue response.
