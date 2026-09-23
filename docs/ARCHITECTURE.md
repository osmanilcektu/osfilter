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
- Standard: HaGeZi Multi NORMAL + OSFilter Core TR
- Pro: HaGeZi Multi PRO + OSFilter Core TR

The main `osfilter.txt`, `hosts.txt` and `domains.txt` files are the Standard tier.

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
- OSFilter allowlist is applied after merge;
- a minimum and maximum entry threshold prevents accidental empty/corrupt upstream builds;
- outputs are sorted deterministically.

## Scale target

100,000 entries is not a quality target by itself. The Standard tier is intentionally over 100k because its global baseline is a mature upstream. The strategic quality target for OSFilter itself is growth of Core TR coverage, low false-positive rate and fast issue response.
