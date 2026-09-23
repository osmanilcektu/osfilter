# OSFilter'a Katkı

OSFilter'ın hedefi mümkün olan en büyük listeyi körlemesine oluşturmak değil; Türkiye'de anlamlı kapsama sahip, kanıtlanabilir ve düşük false-positive oranlı bir filtre veritabanı tutmaktır.

## Domain ekleme

İlgili `sources/*.txt` dosyasına satır başına yalnızca bir alan adı ekleyin.

Geçerli:

```text
ads.example.com
tracker.example.com
```

Geçersiz:

```text
https://ads.example.com/path
||ads.example.com^
0.0.0.0 ads.example.com
```

Aynı değişiklikte `sources/evidence.csv` içine de şu alanlarla bir kayıt eklenmelidir:

```text
domain,category,confidence,evidence_url,note
```

- `category`: `ads`, `trackers`, `security` veya `gambling`
- `confidence`: `high` veya `medium`
- `evidence_url`: HTTPS ile erişilen doğrulanabilir kaynak
- `note`: domainin neden engellendiğine dair kısa gerekçe

Kanıtsız domain CI tarafından kabul edilmez.

## Kabul ölçütleri

Bir domain eklenmeden önce:

1. Reklam/izleyici/güvenlik/kategori işlevi doğrulanmış olmalı.
2. Ana site işlevini veya oturum açmayı bozma riski değerlendirilmiş olmalı.
3. Birinci taraf API/CDN alan adı yalnız adı şüpheli göründüğü için engellenmemeli.
4. Türkiye kullanıcısı açısından anlamlı kapsama katkısı olmalı veya Türkiye'de yaygın kullanılan bir reklam/izleme altyapısı olmalı.
5. Kanıt bağlantısı bulunmalı.
6. Mevcut allowlist ve kategorilerle çakışmamalı.

## Üretilen dosyalar

`osfilter.txt`, `hosts.txt`, `domains.txt`, `stats.json` ve `lists/` dosyalarını elle düzenlemeyin.

## Yerel kontrol

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build.py
```

Pull request'lerde aynı doğrulamalar GitHub Actions tarafından çalıştırılır.

## Lisans

Katkı göndererek ilgili dosyanın [LICENSE](LICENSE) içinde tanımlanan lisansına uygun olarak katkı sağladığınızı kabul etmiş olursunuz.
