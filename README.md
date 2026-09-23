# OSFilter

Türkiye odaklı, açık kaynak reklam, izleyici ve zararlı alan adı filtreleme projesi.

OSFilter; tarayıcı tabanlı reklam engelleyiciler ve DNS tabanlı filtreleme çözümleri için tek bir doğrulanmış kaynak setinden birden fazla çıktı üretmeyi hedefler.

## Hedefler

- Türkiye'de kullanılan reklam ve izleyici altyapılarını engellemek
- Yanlış pozitifleri düşük tutmak
- Kaynak listeleri ve allowlist ile denetlenebilir olmak
- Adblock/uBlock/AdGuard ve hosts tabanlı çözümler için çıktı üretmek
- Her değişikliği otomatik doğrulamak

## Dosyalar

- `osfilter.txt`: Adblock uyumlu ana çıktı
- `hosts.txt`: DNS/hosts tabanlı çıktı
- `allowlist.txt`: yanlış pozitifleri önleyen izin listesi
- `sources/`: kategorilere ayrılmış kaynak domainler
- `lists/`: otomatik üretilen alt listeler
- `scripts/`: doğrulama ve üretim araçları

> Proje başlangıç aşamasındadır. Filtre kuralları doğrulanmadan topluca eklenmez.

## Lisans

Lisans dosyası ayrıca eklenecektir.
