# OSFilter

**Türkiye odaklı, kanıt tabanlı reklam ve izleyici engelleme projesi.**

OSFilter iki ayrı değeri bir araya getirir:

1. **Core TR** — Osman İlçektuğ tarafından bağımsız olarak doğrulanan Türkiye-odaklı reklam/izleyici domainleri.
2. **Global tiers** — lisansı açıkça uyumlu upstream verilerinin normalize, deduplicate ve allowlist işlemlerinden geçirilmiş DNS çıktıları.

Amaç yalnız domain sayısını büyütmek değil; 100 binlerce kayıtla çalışırken kaynağı, lisansı, yanlış pozitifleri ve build bütünlüğünü denetlenebilir tutmaktır.

## Güncel mimari

| Tier | Amaç | Yaklaşık ölçek | Kaynak |
| --- | --- | ---: | --- |
| **Core TR** | Türkiye'ye özgü bağımsız katman | onlarca → büyüyor | OSFilter |
| **Lite** | düşük bozulma riski | 40K+ | HaGeZi Light + Core TR |
| **Standard** | varsayılan dengeli liste | 160K+ | HaGeZi Normal + Core TR |
| **Pro** | daha geniş koruma | 229K+ | HaGeZi Pro + Core TR |
| **Ultra** | agresif çok-kaynaklı koruma | 500K+ (son doğrulanan: 564,725) | HaGeZi Ultimate + Block List Project Ads/Tracking + Core TR |

Kesin sayılar her build'de `stats.json` içine yazılır. Build sistemi Standard için 100K, Pro için 150K ve Ultra için 250K altına düşen beklenmedik çıktıyı yayınlamaz.

## Kullanım — kararlı RAW bağlantılar

Üretilen dosyalar ayrı `dist` dalında yayınlanır. Uygulamalara **main değil dist URL'lerini** ekleyin.

| Liste | Adblock | Hosts | Düz domain |
| --- | --- | --- | --- |
| **Core TR** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-core.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-core-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-core-domains.txt |
| **Lite** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-lite.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-lite-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-lite-domains.txt |
| **Standard** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/osfilter.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/domains.txt |
| **Pro** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-pro.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-pro-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-pro-domains.txt |
| **Ultra** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-ultra.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-ultra-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-ultra-domains.txt |

Build istatistikleri:

https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/stats.json

## NextDNS hedefi

NextDNS başvurusu **Core TR** üzerinden yapılacaktır. Sebep basit: NextDNS zaten büyük küresel listeleri barındırabilir; OSFilter'ın orada anlamlı farkı, başka bir global listenin yeniden paketlenmesi değil, Türkiye'ye özgü bağımsız veri katmanıdır.

Hazır metadata:

`integrations/nextdns/osfilter.json`

Ayrıntılar:

[docs/NEXTDNS.md](docs/NEXTDNS.md)

## Upstream politikası

Aktif ve araştırma amaçlı kaynaklar makine tarafından okunabilir biçimde:

`sources/upstreams.json`

Aktif kaynakların her biri için şu alanlar zorunludur:

- HTTPS kaynak URL
- proje homepage
- açık lisans
- beklenen minimum/maksimum entry sayısı
- kullanılacağı tier

CI, lisans allowlist'ine uymayan veya beklenmedik boyutta gelen kaynakları reddeder.

### Neden her büyük listeyi doğrudan içeri almıyoruz?

- **HaGeZi:** GPL-3.0; GPL global tier'larda açıkça attribution ile kullanılabilir.
- **Block List Project:** Unlicense/public-domain; Ultra tier'a ek sinyal sağlar.
- **AdGuard Filters:** güçlü kaynak, ancak cosmetic/scriptlet gibi DNS dışı kurallar içerdiğinden otomatik DNS importu ayrı extractor denetimi gerektirir.
- **GoodbyeAds:** repo seviyesi MIT olsa da belgelenen upstream seti karışık lisanslar içeriyor; wholesale import yapılmıyor.
- **WindowsSpyBlocker:** MIT fakat Windows fonksiyonlarını etkileyebilecek telemetry blokları içeriyor; varsayılan reklam tier'larına eklenmiyor.
- **AdAway:** CC BY 3.0; araştırma sinyali olarak tutuluyor ve global tier zaten yeterli kapsama sahip olduğundan attribution zinciri gereksiz büyütülmüyor.
- **StevenBlack unified hosts:** çok iyi bir agregatör örneği, ancak kendi içinde birden fazla upstream lisansı taşıyor; tek lisanslı kaynakmış gibi yeniden paketlenmiyor.

Bu yaklaşım domain sayısını yapay biçimde şişirmek yerine hukuken ve teknik olarak izlenebilir bir ürün oluşturur.

## Core TR kalite modeli

Yerel veri:

- `sources/ads.txt`
- `sources/trackers.txt`
- `sources/security.txt`
- `sources/gambling.txt`
- `sources/evidence.csv`
- `allowlist.txt`

Her yerel domain için evidence kaydı zorunludur. CI:

- domain/IDN/Punycode doğrulaması,
- duplicate kontrolü,
- kategori çakışması,
- evidence eşleşmesi,
- upstream lisans ve tier kontrolü,
- parser testleri,
- minimum tier boyut kapıları

uygular.

## Otomatik güncelleme

GitHub Actions:

- her ilgili source/build değişikliğinde,
- manuel çalıştırmada,
- **her gün 10:23 UTC**

tüm upstream'leri yeniden indirir, normalize eder, duplicate'leri temizler, allowlist uygular ve `dist` dalını atomik olarak yeniden yayınlar.

## Formatlar

OSFilter şu formatları doğrudan üretir:

- Adblock / AdGuard Home / uBlock uyumlu domain kuralları
- hosts
- plain domains

dnsmasq ve RPZ formatları sonraki compatibility katmanında aynı canonical domain setinden üretilebilir; yeni veri kaynağı eklemeyi gerektirmez.

## DNS engellemenin sınırı

DNS filtresi YouTube, Instagram, Twitch gibi servislerde içerik ile reklam aynı hostname/CDN üzerinden geliyorsa reklamı güvenli biçimde ayıramaz. “Daha çok domain = her reklamı keser” yaklaşımı uygulamaları bozabilir. OSFilter bu nedenle tier mantığı kullanır.

## Lisans ve marka

- build/test/automation kodu: **AGPL-3.0-only**
- bağımsız OSFilter Core TR verisi: **ODbL-1.0 OR GPL-3.0-only**
- HaGeZi içeren global aggregate çıktılar: **GPL-3.0-only**
- dokümantasyon: **CC BY-SA 4.0**
- OSFilter adı, logo ve Osman İlçektuğ'un kişisel marka hakları ayrıca saklıdır

Ayrıntılar:

- [LICENSE](LICENSE)
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- [LICENSES/](LICENSES/)

## Maintainer

**Osman İlçektuğ**

- GitHub: [@osmanilcektu](https://github.com/osmanilcektu)
- Instagram: [@osmancxl_](https://www.instagram.com/osmancxl_/)

## Katkı

Yanlış engelleme ve kaçan reklam/izleyici bildirimleri GitHub Issues üzerinden alınır. Yeni Core TR domainleri kanıt/provenance olmadan kabul edilmez.

Katkı rehberi: [CONTRIBUTING.md](CONTRIBUTING.md)


## Teknik dokümantasyon

- [100K+ ölçekleme ve kaynak stratejisi](docs/SCALING.md)
- [Core TR büyütme süreci](docs/CORE_TR_GROWTH.md)
- [NextDNS entegrasyon planı](docs/NEXTDNS.md)
- [Changelog](CHANGELOG.md)
- [Security / false-positive politikası](SECURITY.md)
