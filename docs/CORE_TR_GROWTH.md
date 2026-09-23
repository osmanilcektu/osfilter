# Core TR büyütme süreci

Global listelerin yüz binlerce domain içermesi kolaydır. OSFilter'ın bağımsız değeri ise Türkiye'ye özgü Core TR katmanıdır.

## Otomatik aday keşfi

`scripts/discover_tr_candidates.py` aktif upstream'leri tarar ve `.tr` ile biten, Core TR'de henüz bulunmayan domainleri çıkarır.

Çıktı:

`artifacts/tr-candidates.csv`

Alanlar:

- `domain`
- `source_count` — domain kaç aktif upstream'de görüldü
- `sources` — hangi kaynaklarda bulundu

Birden fazla upstream'de görülen adaylar incelemede daha yüksek öncelik alabilir; ancak bu otomatik olarak doğru/engellenebilir oldukları anlamına gelmez.

## Haftalık çalışma

`.github/workflows/candidates.yml` her Pazar aday taraması yapar ve CSV'yi GitHub Actions artifact olarak 30 gün saklar.

Adaylar **otomatik olarak blocklist'e eklenmez**.

Otomatik olarak güncellenen ayrı `TR Regional` çıktısı, lisanslı Turkish Ad Hosts verisini ve global upstream'lerin `.tr` kayıtlarını içerir. Bu çıktı GPL ile dağıtılır ve bağımsız Core TR sayısına dahil edilmez.

## Core TR'ye yükseltme kriteri

Bir adayın `sources/ads.txt`, `sources/trackers.txt`, `sources/security.txt` veya `sources/gambling.txt` içine alınabilmesi için:

1. alan adının gerçek işlevi doğrulanmalı;
2. ana uygulama/site fonksiyonunu bozma riski incelenmeli;
3. kategori açıkça belirlenmeli;
4. `sources/evidence.csv` içine HTTPS kanıt kaydı eklenmeli;
5. false-positive riski makul olmalı;
6. CI testlerinin tamamı geçmeli.

Bu süreç Core TR'nin yalnızca büyük değil, NextDNS gibi sağlayıcılar açısından savunulabilir ve bakımı yapılabilir bir bölgesel liste olmasını hedefler.
