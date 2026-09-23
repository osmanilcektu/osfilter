# NextDNS entegrasyon hedefi

OSFilter'ın hedeflerinden biri NextDNS gibi merkezi DNS servislerinde seçilebilir bir bölgesel liste haline gelmektir.

## Teknik uyumluluk

NextDNS'in açık blocklist deposundaki tanımlar JSON metadata dosyalarıyla bir kaynak URL'yi işaret eder. OSFilter için hazır aday tanım:

`integrations/nextdns/osfilter.json`

Kaynak:

`https://raw.githubusercontent.com/osmanilcektu/osfilter/main/hosts.txt`

Format:

`hosts`

## Kabul öncesi kalite hedefleri

NextDNS'e entegrasyon talebi açılmadan önce OSFilter şu seviyeyi hedefler:

- düzenli ve gözle görülür bakım geçmişi;
- otomatik doğrulama ve testlerin sürekli yeşil olması;
- her kaynak domain için kanıt/provenance kaydı;
- hızlı false-positive düzeltme süreci;
- ölü/terk edilmiş domainlerin periyodik denetimi;
- Türkiye'ye özgü, diğer büyük listelere anlamlı ek kapsam;
- kullanıcı ve katkıcı topluluğu;
- sabit RAW URL ve geriye dönük uyumlu çıktı formatı.

## Not

NextDNS son kullanıcı arayüzünde keyfi özel blocklist URL'si ekleme özelliği sunmadığından, gerçek entegrasyon NextDNS'in kendi blocklist kataloğuna kabul edilmesini gerektirir.

OSFilter yeterli olgunluğa ulaşmadan upstream PR açılmamalıdır. Önce kalite, bakım geçmişi ve benzersiz Türkiye kapsamı kanıtlanacaktır.
