# OSFilter

Türkiye odaklı, açık kaynak reklam, izleyici ve zararlı alan adı filtreleme projesi.

OSFilter; doğrulanmış kaynak domainlerden Adblock uyumlu filtreler ve DNS/hosts çıktıları üretir. Amaç mümkün olan en büyük listeyi değil, yanlış pozitif oranı düşük ve bakımı yapılabilir bir Türkiye filtresi oluşturmaktır.

## Kullanılabilir listeler

| Liste | İçerik | RAW |
| --- | --- | --- |
| **OSFilter Full** | Reklam + izleyici + güvenlik + bahis/kumar | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/osfilter.txt |
| **OSFilter Lite** | Reklam + izleyici | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/lists/osfilter-lite.txt |
| **OSFilter Security** | Zararlı/phishing | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/lists/osfilter-security.txt |
| **OSFilter Gambling** | Bahis/kumar | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/lists/osfilter-gambling.txt |
| **hosts.txt** | DNS/hosts tabanlı engelleme | https://raw.githubusercontent.com/osmanilcektu/osfilter/main/hosts.txt |

> İlk sürüm altyapısı hazırdır. Kaynak listeler yalnız doğrulanmış gerçek alan adlarıyla doldurulacaktır.

## Destek hedefleri

- uBlock Origin
- AdGuard
- Adblock Plus uyumlu motorlar
- Pi-hole ve hosts listesi kabul eden DNS çözümleri
- Keenetic/Entware üzerinde hosts veya DNS tabanlı filtreleme

## Kaynak modeli

Üretilen dosyalar elle düzenlenmez. Gerçek veri `sources/` altında tutulur:

- `sources/ads.txt` — reklam
- `sources/trackers.txt` — izleyici/telemetri
- `sources/security.txt` — zararlı/phishing
- `sources/gambling.txt` — isteğe bağlı bahis/kumar
- `allowlist.txt` — OSFilter içindeki yanlış pozitifleri bastırır

Her satır yalnızca bir domain içerir:

```text
ads.example.com
tracker.example.com
```

URL, Adblock kuralı veya hosts sözdizimi kaynak dosyalarına yazılmaz. Bunlar `scripts/build.py` tarafından otomatik üretilir.

## Geliştirme

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build.py
```

GitHub Actions her push ve pull request'te kaynakları doğrular. `main` dalında kaynak değiştiğinde türetilmiş filtreler otomatik olarak yeniden oluşturulur.

## Tasarım ilkeleri

- Yanlış pozitifi düşük tut
- Birinci taraf API/CDN domainlerini körlemesine engelleme
- Domainleri kategoriye göre tek yerde tut
- Aynı domainin birden fazla kategoride bulunmasına izin verme
- IDN alan adlarını güvenli biçimde Punycode'a dönüştür
- `allowlist.txt` girdilerini global Adblock whitelist kuralına dönüştürme
- Üçüncü taraf filtre listelerini topluca kopyalama

## Katkı

Katkı kuralları için [CONTRIBUTING.md](CONTRIBUTING.md) dosyasına bakın. Yanlış engellemeler ve kaçan reklam/izleyiciler GitHub Issues üzerinden bildirilebilir.

## Lisans

MIT License. Ayrıntılar için [LICENSE](LICENSE).
