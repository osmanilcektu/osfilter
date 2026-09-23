# OSFilter'a Katkı

OSFilter'da amaç mümkün olan en büyük listeyi oluşturmak değil, yanlış pozitif oranı düşük ve gerekçesi doğrulanabilir bir liste tutmaktır.

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

Üretilen `osfilter.txt`, `hosts.txt` ve `lists/` dosyalarını elle düzenlemeyin.

## Kabul ölçütleri

Bir domain eklenmeden önce şu soruların karşılığı net olmalıdır:

1. Domain gerçekten reklam, izleyici, zararlı/phishing veya ilgili kategoriye mi ait?
2. Normal site işlevini bozma ihtimali var mı?
3. Birinci taraf içerik/CDN/API domaini mi?
4. Türkiye kullanıcısı açısından anlamlı mı?
5. Yanlış pozitif oluşursa `allowlist.txt` ile güvenli şekilde düzeltilebilir mi?

## Yerel kontrol

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build.py
```

Pull request'lerde GitHub Actions aynı doğrulamaları otomatik çalıştırır.
