# NextDNS entegrasyon hedefi

OSFilter'ın NextDNS için aday listesi **Core TR** katmanıdır.

## Neden global Standard/Pro/Ultra değil?

Global tier'lar HaGeZi ve diğer açık upstream'lerden oluşturulan kullanışlı son kullanıcı paketleridir. NextDNS kataloğu açısından OSFilter'ın benzersiz katkısı ise Türkiye'ye özgü, bağımsız olarak doğrulanan Core TR verisidir. Bu yüzden başvuruda başka bir büyük global blocklist'i yeniden paketlemek yerine bölgesel veri sunulur.

## Teknik kaynak

Metadata:

`integrations/nextdns/osfilter.json`

Kararlı hosts kaynağı:

`https://raw.githubusercontent.com/osmanilcektu/osfilter/dist/lists/osfilter-core-hosts.txt`

Format:

`hosts`

## Kabul öncesi hedefler

- düzenli bakım geçmişi;
- CI/build'lerin sürekli başarılı olması;
- Core TR'de her domain için evidence/provenance;
- hızlı false-positive düzeltme;
- Türkiye'ye özgü anlamlı ve büyüyen kapsama;
- kullanıcı/katkıcı geri bildirimi;
- kararlı RAW URL;
- yayınlanan sürümlerde geriye dönük format uyumu.

## Başvuru zamanı

100 bin domain sahibi olmak NextDNS kabulü için tek başına değer değildir. Global 100K+ tier'lar son kullanıcı için faydalıdır; NextDNS adaylığında ölçülecek asıl fark Core TR'nin özgünlüğü, bakım kalitesi ve false-positive performansıdır.
