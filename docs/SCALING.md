# OSFilter ölçekleme ve kaynak stratejisi

Son güncelleme: 2026-09-23

## Mevcut ölçek

Başarılı dağıtım build'i:

- Core TR: 24 bağımsız doğrulanmış domain
- Lite: 40,032
- Standard: 162,632
- Pro: 229,479
- Ultra: 564,725

Bu sayılar \`dist/stats.json\` tarafından otomatik üretilir ve upstream değiştikçe değişebilir.

## 100 bin domaine nasıl çıkılır?

100 bin alan adı elle yazılmaz. Sağlıklı bir blocklist projesi üç katmandan oluşur:

1. güvenilir upstream kaynaklar;
2. normalize / deduplicate / allowlist / sanity-check pipeline;
3. projeye özgü bağımsız curation.

OSFilter bu üç katmanı ayırır.

### 1. Core TR

OSFilter'ın özgün Türkiye katmanı. Her kayıt evidence gerektirir.

Büyük global kaynaklardan domain kopyalayıp “bizim listemiz” denmez. Global kaynaklardan yalnız aday keşfi yapılabilir; Core TR'ye giren kayıt ayrıca incelenir.

### 2. Global tiers

Kullanıcıların tek URL ile güçlü bir DNS listesi kullanabilmesi için lisans uyumlu kaynaklar birleştirilir.

### 3. Research-only sources

Teknik veya hukuki nedenle otomatik import edilmeyen kaynaklardır. Kapsam karşılaştırması, false-positive araştırması ve yeni aday bulmak için kullanılabilirler.

## Kaynak araştırması

### HaGeZi DNS Blocklists

Aktif.

- Lisans: GPL-3.0
- Çoklu seviye: Light, Normal, Pro, Pro++, Ultimate
- Düzenli otomatik rebuild
- Çoklu DNS formatları
- OSFilter global tier'larının ana baseline'ı

HaGeZi yalnızca “çok büyük liste” olmadığı için değerlidir; kaynakları birleştirir, temizler, allowlist uygular ve farklı agresiflik seviyeleri sunar.

### Block List Project

Aktif, Ultra tier.

- Lisans: Unlicense / public-domain dedication
- Kategori bazlı listeler
- Ads ve Tracking kaynakları Ultra'da kullanılır
- Çok büyük security/content kategorileri varsayılan reklam tier'ına karıştırılmaz

Ultra'da kullanılmasının nedeni lisans zincirinin açık olması ve HaGeZi Ultimate'a ek coverage sağlamasıdır.

### AdGuard Filters

Research-only.

- Güncel repo lisansı: GPL-3.0-only
- Mobile Ads ve diğer listeler DNS domainlerinden fazlasını içerir
- Cosmetic filtering, URL/request kuralları, modifiers, exceptions ve scriptlet kuralları bulunabilir

Bu nedenle basit bir “domain regex çıkar ve ekle” yaklaşımı yeterli değildir. AdGuard import edilecekse exceptions/modifiers bilen ayrı bir ABP parser gerekir.

### GoodbyeAds

Research-only.

Repository kökünde MIT lisansı vardır; ancak projenin kendi \`Docs/Sources.md\` belgesi kullanılan upstream'lerde MIT yanında GPL, CC BY-SA, CC BY-NC-ND, All Rights Reserved ve lisansı olmayan kaynaklar da listeler.

Bu yüzden yalnız repo kökündeki MIT dosyasına bakıp tüm oluşan host listesini OSFilter'a yeniden lisanslamak doğru değildir.

### WindowsSpyBlocker

Research-only.

- Lisans: MIT
- Windows telemetry/spy odaklıdır
- Mevcut host verilerinin önemli bölümü Windows servisleriyle ilişkilidir
- Default reklam listesine eklenirse işletim sistemi özelliklerini bozma riski vardır

İleride ayrı bir \`Windows Privacy\` opsiyonel kategori için değerlendirilebilir.

### AdAway

Research-only.

- Default hosts dosyası CC BY 3.0
- Mobil reklam/analytics coverage'ı güçlü bir araştırma sinyalidir
- Global tier'larda zaten önemli overlap bulunduğu için şu anda ek attribution zinciri oluşturulmaz

### StevenBlack Hosts

Architecture reference / research-only aggregate.

StevenBlack başarılı bir aggregation modeli sunar: kaynakları toplar, duplicate temizler ve whitelist uygular. Ancak unified çıktısı çok sayıda farklı upstream lisansını bir araya getirir.

OSFilter bu mimari fikri kullanır fakat unified listeyi tek lisanslı ham kaynak gibi yeniden paketlemez.

## Neden Ultra varsayılan değil?

Daha fazla domain daha fazla koruma sağlayabilir ama false-positive riskini de artırır.

- Lite: düşük kırılma
- Standard: günlük kullanım için dengeli
- Pro: daha geniş coverage
- Ultra: agresif; teknik kullanıcı / admin müdahalesi olan ortam

Bu nedenle README'deki ana \`osfilter.txt\`, Standard alias'ıdır.

## Kalite kapıları

Her aktif upstream için:

- HTTPS zorunlu;
- lisans allowlist'i;
- beklenen minimum entry;
- beklenen maksimum entry;
- tier;
- homepage;
- kaynak adı

tanımlanır.

Kaynak beklenenden küçülür/büyürse build durur. Böylece upstream 404 sayfası, boş dosya veya format değişikliği yanlışlıkla production listesine dönüşmez.

Aggregate tier'ların ayrıca minimum final boyutları vardır:

- Lite >= 30,000
- Standard >= 100,000
- Pro >= 150,000
- Ultra >= 250,000

## Dedup neden önemlidir?

Ham upstream sayılarını toplamak yanıltıcıdır. Aynı domain birkaç kaynakta bulunabilir.

OSFilter:

1. her kaynağı normalize eder;
2. geçersiz domain/IP satırlarını atar;
3. her tier içinde \`set\` tabanlı dedup uygular;
4. allowlist'i çıkarır;
5. sıralı deterministic çıktı üretir.

Bu nedenle Ultra'nın 564,725 sayısı upstream sayıların toplamı değil, birleşim sonrası benzersiz domain sayısıdır.

## NextDNS stratejisi

NextDNS'e sunulacak liste Core TR'dir.

Sebep: OSFilter Standard/Pro/Ultra global kullanım için değerlidir fakat HaGeZi gibi upstream'leri yeniden paketleyen global bir tier NextDNS kataloğuna özgün değer katmaz.

Core TR için hedef:

- Türkiye'ye özgü reklam/izleyici servisleri;
- hızlı false-positive yanıtı;
- evidence/provenance;
- düzenli commit ve release geçmişi;
- stabil RAW endpoint;
- anlamlı kullanıcı/katkıcı tabanı.

Haftalık \`Discover TR candidates\` workflow'u \`.tr\` adaylarını upstream'lerden bulur fakat otomatik engellemez. İnsan doğrulamasından sonra Core TR'ye alınır.

## 1 milyon domaine çıkmak gerekli mi?

Teknik olarak kolaydır; malware, phishing, abuse ve threat-intelligence listeleri eklendiğinde milyonlarca domaine çıkılabilir.

Ancak bu ayrı bir security ürünü problemidir. Reklam/izleyici filtresine milyonlarca kısa ömürlü threat domaini karıştırmak:

- dosyayı büyütür;
- güncelleme maliyetini artırır;
- kategori anlamını bozar;
- kullanıcıların false-positive teşhisini zorlaştırır.

Bu nedenle OSFilter güvenlik datasetlerini ayrı tier/listeler olarak geliştirmelidir.

## Sonraki teknik hedefler

- dnsmasq output
- RPZ output
- Unbound output
- upstream response hash/history
- stale/dead domain sampling
- popular-site regression allowlist
- Core TR candidate review dashboard
- release changelog ve coverage-delta raporu
- NextDNS upstream submission
