# OSFilter

**Türkiye odaklı, kanıt tabanlı reklam ve izleyici engelleme projesi.**

OSFilter iki ayrı değeri bir araya getirir:

1. **Core TR** — Osman İlçektuğ tarafından bağımsız olarak doğrulanan Türkiye-odaklı reklam/izleyici domainleri.
2. **Global tiers** — lisansı açıkça uyumlu upstream verilerinin normalize, deduplicate ve allowlist işlemlerinden geçirilmiş DNS çıktıları.
3. **TR Regional** — lisanslı Turkish Ad Hosts verisi, global kaynaklardan otomatik seçilen `.tr` reklam/izleyici alan adları ve Core TR; GPL lisanslı bölgesel birleşim. Özgün Core TR verisiyle karıştırılmamalıdır.

Amaç yalnız domain sayısını büyütmek değil; 100 binlerce kayıtla çalışırken kaynağı, lisansı, yanlış pozitifleri ve build bütünlüğünü denetlenebilir tutmaktır.

## Güncel mimari

| Tier | Amaç | Yaklaşık ölçek | Kaynak |
| --- | --- | ---: | --- |
| **Core TR** | Türkiye'ye özgü bağımsız katman | onlarca → büyüyor | OSFilter |
| **Lite** | düşük bozulma riski | 40K+ | HaGeZi Light + Core TR |
| **Standard** | varsayılan dengeli liste | 160K+ | Lite + HaGeZi Normal + AdGuard Mobile Ads + Turk-AdFilter Lite + Core TR |
| **Pro** | daha geniş koruma | 220K+ | Standard + HaGeZi Pro + Turkish Ad Hosts + Core TR |
| **Ultra** | agresif çok-kaynaklı koruma | 500K+ | Pro + HaGeZi Ultimate + Block List Project Ads/Tracking + Core TR |
| **TR Regional** | otomatik Türkiye kapsamı | `stats.json` | Turkish Ad Hosts + Turk-AdFilter Lite + Standard içindeki `.tr` alan adları + Core TR |
| **TR Regional Ultra** | agresif Türkiye kapsamı | `stats.json` | Turkish Ad Hosts + Ultra içindeki `.tr` alan adları + Core TR |
| **Security (isteğe bağlı)** | zararlı yazılım, oltalama ve dolandırıcılık alan adları | `stats.json` | HaGeZi Threat Intelligence Feeds Mini + kanıtlı yerel kayıtlar |
| **Gambling (isteğe bağlı)** | küresel ve Türkiye odaklı kumar engelleme | `stats.json` | HaGeZi Gambling Medium + Turk-AdFilter Bahis |
| **Gambling TR (isteğe bağlı)** | Türkiye odaklı kumar engelleme | `stats.json` | Turk-AdFilter Bahis + kanıtlı yerel kayıtlar |

Kesin sayılar her build'de `stats.json` içine yazılır. Tier'lar kümülatiftir: daha yüksek bir seviyeye geçtiğinizde alt seviyede engellenen bir domain sessizce açılmaz. Build sistemi Standard için 100K, Pro için 150K ve Ultra için 250K altına düşen beklenmedik çıktıyı yayınlamaz.

## Kullanım — kararlı RAW bağlantılar

Üretilen dosyalar ayrı `dist` dalında yayınlanır. Uygulamalara **main değil dist URL'lerini** ekleyin.

| Liste | Adblock | Hosts | Düz domain |
| --- | --- | --- | --- |
| **Core TR** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-core.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-core-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-core-domains.txt |
| **Lite** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-lite.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-lite-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-lite-domains.txt |
| **Standard** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/osfilter.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/domains.txt |
| **Pro** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-pro.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-pro-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-pro-domains.txt |
| **Ultra** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-ultra.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-ultra-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-ultra-domains.txt |
| **TR Regional** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-tr-regional.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-tr-regional-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-tr-regional-domains.txt |
| **TR Regional Ultra** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-tr-regional-ultra.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-tr-regional-ultra-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-tr-regional-ultra-domains.txt |
| **Security (isteğe bağlı)** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-security.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-security-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-security-domains.txt |
| **Gambling (isteğe bağlı)** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-gambling.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-gambling-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-gambling-domains.txt |
| **Gambling TR (isteğe bağlı)** | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-gambling-tr.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-gambling-tr-hosts.txt | https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-gambling-tr-domains.txt |

TR Regional listeleri her günlük build'de **otomatik dolar**. Turkish Ad Hosts ve Turk-AdFilter Lite'ın DNS için uygun tam alan adı kurallarını, ayrıca global kaynakların `.tr` alan adlarını birleştirir; kamu/eğitim alan adları ve giriş/ödeme gibi hassas host etiketlerini otomatik katmandan çıkarır. Bölgesel kaynakların `.com` kayıtları da bu çıktıya girer; diğer `.com` alan adları ülkesine bakılarak otomatik sınıflandırılmaz. Standard ile daha geniş Türkiye kapsamı isteyenler TR Regional'ı ayrıca kullanabilir. Standard artık Turk-AdFilter Lite kayıtlarını da içerir; bu abonelikleri birlikte eklemek aynı kaynağın bir bölümünü tekrarlayabilir. Ultra katmanı yanlış engelleme riski daha yüksek olduğundan isteğe bağlıdır.

Voodoo'nun `crosspromo.voodoo.io` adlı oyunlar arası tanıtım adresi tam host olarak engellenir. Oyunların reklam ağları ve ödüllü reklam davranışları değişebilir; bu kayıt tüm Voodoo oyunlarında reklamsızlık garantisi vermez.

Kumar ve güvenlik abonelikleri reklam listelerinden ayrıdır. Türkiye bahis kaynağındaki yalnızca **tam alan adı** kuralları DNS listesine alınır; kozmetik kurallar, URL yolları, joker karakterli kurallar ve istisnalar aktarılmaz. `Gambling TR`, `Gambling` içindeki Türkiye kaynağı bölümüdür; ikisini birlikte eklemek gerekmez. Bu çıktılar upstream birleşimleridir, bağımsız doğrulanmış Core TR sayısına dahil değildir. Hiçbir DNS listesi internetteki tüm reklam, kumar veya zararlı adresleri kapsadığını garanti edemez; aynı alan adından sunulan içerik DNS düzeyinde ayrılamaz.

Standard resolver outputs:

- dnsmasq 2.86+: https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/dnsmasq.conf
- Unbound: https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/unbound.conf
- BIND/Knot/PowerDNS-compatible RPZ zone: https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/rpz.zone

Core TR resolver outputs are published under `dist/lists/osfilter-core-dnsmasq.conf`, `osfilter-core-unbound.conf` and `osfilter-core-rpz.zone`.

Build istatistikleri:

https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/stats.json

Upstream kaynak anlık görüntüsü (SHA-256, byte boyutu, final URL; sabitlenmiş bir hash kilidi değildir):

https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/upstream-lock.json

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
- ayrı kategori kaynakları için `category` (`security`, `gambling`, `gambling_tr`)
- kaynak biçimi (`domains`: satır başına tek alan adı; `abp_dns`: yalnız tam `||alan.adi^` kuralları)

CI, lisans allowlist'ine uymayan, biçimi uyuşmayan veya beklenmedik boyutta gelen kaynakları reddeder.

### Neden her büyük listeyi doğrudan içeri almıyoruz?

- **HaGeZi:** GPL-3.0; GPL global tier'larda açıkça attribution ile kullanılabilir.
- **Block List Project:** Unlicense/public-domain; Ultra tier'a ek sinyal sağlar.
- **Turkish Ad Hosts:** GPL-3.0; Türkiye'deki mobil uygulamalara odaklı bölgesel DNS verisi Pro/Ultra ve TR Regional çıktılarda kullanılır. Üçüncü taraf projeye atıf korunur.
- **AdGuard Mobile Ads:** GPL-3.0; `adservers.txt` içindeki yalnız tam alan adı kuralları Standard'a alınır. URL/cosmetic/scriptlet ve koşullu kurallar DNS'e çevrilmez.
- **Turk-AdFilter Lite:** GPL-3.0; yalnız DNS'e uygun tam reklam/izleyici alan adları Standard ve TR Regional'da kullanılır. Karma tam liste ve sayfa içi kurallar aktarılmaz.
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
- `sources/functional-allowlist.txt` — giriş/ödeme/core API gibi kritik işlevsel uçlar için dar güvenlik allowlist’i

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
Yayınlamadan önce önceki `dist` sürümü zorunlu olarak alınır. Lite, Standard, Pro, Ultra, TR Regional ve TR Regional Ultra çıktılarından herhangi birinde eklenen veya çıkan kayıtlar önceki sürümün %10'unu aşarsa otomatik yayın durur ve kaynaklar incelenir. RPZ SOA seri numarası içerik değişince önceki yayına göre bir artar; aynı alan adları için sabit kalır.

## Formatlar

OSFilter aynı canonical domain setinden doğrudan şu formatları üretir:

- Adblock / AdGuard Home / uBlock uyumlu domain kuralları
- hosts
- plain domains
- dnsmasq 2.86+
- Unbound `local-zone`
- BIND/Knot/PowerDNS uyumlu RPZ

## DNS engellemenin sınırı

DNS filtresi YouTube, Instagram, Twitch gibi servislerde içerik ile reklam aynı hostname/CDN üzerinden geliyorsa reklamı güvenli biçimde ayıramaz. Özellikle YouTube video reklamlarını DNS listesiyle sıfırlamaya çalışmak video oynatmayı bozabilir. Tarayıcıda istek/öğe seviyesinde filtre kullanan bir içerik engelleyici bu iş için uygundur; resmi YouTube uygulamasında DNS ile sıfır reklam garanti edilemez. “Daha çok domain = her reklamı keser” yaklaşımı uygulamaları bozabilir. OSFilter bu nedenle tier mantığı kullanır.

## Lisans ve marka

- build/test/automation kodu: **AGPL-3.0-only**
- bağımsız OSFilter Core TR verisi: **ODbL-1.0 OR GPL-3.0-only**
- HaGeZi içeren global aggregate çıktılar: **GPL-3.0-only**
- Upstream içeren TR Regional çıktılar: **GPL-3.0-only**
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
- [NextDNS / AdGuard sağlayıcı kabul planı](docs/PROVIDER_ADOPTION.md)
- [Changelog](CHANGELOG.md)
- [Security / false-positive politikası](SECURITY.md)
