# OSFilter

**Türkiye odaklı, kanıt tabanlı reklam ve izleyici engelleme listesi.**

OSFilter; doğrulanmış domainlerden Adblock, hosts ve düz domain çıktıları üretir. Hedefi yalnızca büyük bir liste olmak değil; düşük false-positive oranı, açık provenance kayıtları ve sürekli testlerle Türkiye için güvenilir bir DNS filtre kaynağı olmaktır.

## Durum

İlk veri seti oluşturuldu. Her domain `sources/evidence.csv` içinde kanıt ve güven seviyesiyle eşleştirilir. Kanıtsız domain CI tarafından reddedilir.

## Kullanılabilir listeler

| Liste | İçerik | RAW |
| --- | --- | --- |
| **OSFilter Full** | Reklam + izleyici + güvenlik + bahis/kumar | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/osfilter.txt |
| **OSFilter Lite** | Reklam + izleyici | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/lists/osfilter-lite.txt |
| **OSFilter Security** | Zararlı/phishing | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/lists/osfilter-security.txt |
| **OSFilter Gambling** | Bahis/kumar | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/lists/osfilter-gambling.txt |
| **hosts.txt** | Pi-hole / DNS / hosts | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/hosts.txt |
| **domains.txt** | Düz domain listesi | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/domains.txt |

## NextDNS hedefi

OSFilter, NextDNS benzeri merkezi DNS servislerinde doğrudan seçilebilir bir bölgesel blocklist olabilecek şekilde hazırlanır.

Hazır NextDNS metadata tanımı:

`integrations/nextdns/osfilter.json`

Ayrıntılı yol haritası:

[docs/NEXTDNS.md](docs/NEXTDNS.md)

NextDNS şu anda son kullanıcıların keyfi özel blocklist URL'lerini doğrudan eklemesine izin vermediğinden, OSFilter'ın NextDNS kataloğunda görünmesi için upstream kabul gerekir. Proje yeterli bakım geçmişi, kullanıcı tabanı ve benzersiz Türkiye kapsamına ulaşmadan bu başvuru yapılmayacaktır.

## Kalite modeli

Gerçek veri `sources/` altında tutulur:

- `sources/ads.txt` — reklam
- `sources/trackers.txt` — izleyici / attribution / sync
- `sources/security.txt` — zararlı / phishing
- `sources/gambling.txt` — isteğe bağlı bahis/kumar
- `sources/evidence.csv` — her domain için provenance, kategori ve güven seviyesi
- `allowlist.txt` — OSFilter içindeki yanlış pozitifleri bastırır

CI şu kontrolleri yapar:

- domain sözdizimi ve IDN/Punycode doğrulaması;
- duplicate kontrolü;
- kategori çakışması;
- her domain için evidence zorunluluğu;
- evidence kategori tutarlılığı;
- unit testler;
- deterministik çıktı üretimi.

## Destek hedefleri

- uBlock Origin
- AdGuard
- Adblock Plus uyumlu motorlar
- Pi-hole
- AdGuard Home
- Keenetic / Entware
- NextDNS ve benzeri yönetilen DNS servisleri

DNS tabanlı engellemenin teknik sınırı nedeniyle YouTube, Instagram ve benzeri servislerde içerikle aynı alan adından sunulan reklamların tamamı DNS seviyesinde engellenemez. OSFilter bu nedenle işlevsel API/CDN alan adlarını agresif biçimde engelleyip uygulamaları bozmak yerine doğrulanmış reklam/izleme uç noktalarına odaklanır.

## Geliştirme

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build.py
```

`main` üzerindeki kaynak değişikliklerinden sonra GitHub Actions şu çıktıları otomatik yeniler:

- `osfilter.txt`
- `hosts.txt`
- `domains.txt`
- `stats.json`
- `lists/*.txt`

## Lisans ve koruma

OSFilter tek bir gevşek lisans kullanmaz:

- otomasyon ve test kodu: **AGPL-3.0-only**
- filtre veritabanı ve üretilen listeler: **ODbL-1.0**
- dokümantasyon: **CC BY-SA 4.0**
- **OSFilter adı, logo ve kişisel marka hakları ayrıca saklıdır**

Bu yapı, NextDNS/AdGuard gibi servislerin listeyi entegre edebilmesine izin verirken türev veritabanlarının lisans yükümlülüklerini ortadan kaldırıp kapalı şekilde yeniden markalanmasını önlemeyi amaçlar.

Ayrıntılar: [LICENSE](LICENSE), [NOTICE.md](NOTICE.md), [LICENSES/](LICENSES/)

## Maintainer

**Osman İlçektuğ**

- GitHub: [@osmanilcektu](https://github.com/osmanilcektu)
- Instagram: [@osmancxl_](https://www.instagram.com/osmancxl_/)

## Katkı

Yanlış engellemeler ve kaçan reklam/izleyiciler GitHub Issues üzerinden bildirilebilir. Yeni domainler yalnız kanıt kaydıyla kabul edilir.

Katkı kuralları: [CONTRIBUTING.md](CONTRIBUTING.md)
