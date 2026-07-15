# **Takım İsmi**

**The Parsimonia**

# **Takım Logosu**

<!-- Takım logonuzu buraya ekleyin -->
<!-- ![TakımLogo](docs/assets/team_logo.png) -->

## Takım Elemanları

| | İsim | Ünvan | Sosyal Medya |
|---|---|---|---|
| <!-- foto --> | Beyza ATA | Product Owner | [LinkedIn](https://www.linkedin.com/in/beyza-ata-50a2b3317/) |
| <!-- foto --> | Pelin ATAMAN | Scrum Master | [LinkedIn](https://www.linkedin.com/in/pelin-ataman) |
| <!-- foto --> | Furkan BİTİK | Developer | [LinkedIn](https://www.linkedin.com/in/furkanbitik/) |

## Ürün İsmi

**WasteZero AI**

## Ürün Logosu

<!-- Ürün logonuzu buraya ekleyin -->
<!-- ![ÜrünLogo](docs/assets/product_logo.png) -->

## Ürün Açıklaması

- **WasteZero AI**, restoranlar için akıllı menü, talep ve israf karar destek sistemidir. Restoranların geçmiş satış, üretim, fiyat, maliyet ve kampanya verilerini analiz ederek ürün bazlı talep tahmini yapar, fazla üretimden kaynaklanan fire/israf riskini hesaplar ve kârlılığı koruyacak şekilde günlük üretim ve menü kararlarına aksiyon önerileri sunar.

- Sistem, tek bir model yerine her biri kendi gerçek verisiyle çalışan **uzman agent'lardan** oluşur. Agent'lar çıktılarını ortak bir dil olan **ürün kategorisi** (çorba, ana yemek, salata, tatlı, içecek) üzerinden paylaşır. Bir **orkestratör**, agent çıktılarını birleştirip çelişkileri (satış kaçırma riski ile fire riski arasındaki denge) değerlendirerek son kararı ve yönetici özetini üretir.

| Agent | Görevi |
|---|---|
| Talep Agent'ı | Kategori bazlı satış/talep tahmini |
| Fire/İsraf Agent'ı | Ürün bazlı israf riski profili |
| Kâr/Fiyat Agent'ı | Fiyat, maliyet ve kârlılık analizi |
| Orkestratör | Agent çıktılarını birleştirir, karar ve yönetici özeti üretir |

## Ürün Özellikleri

- Gerçek şirket verisiyle eğitilmiş, kategori bazlı talep tahmini (naif yönteme göre hatayı %12.4'ten %7.6'ya düşüren model)
- Ürün bazlı fire/israf risk profili
- Fiyat, maliyet ve kârlılık analizi
- Agent bazlı, modüler mimari (her agent bağımsız geliştirilebilir ve test edilebilir)
- Orkestratör aracılığıyla tek bir karar çıktısı ve AI destekli günlük yönetici özeti
- Otomatik testlerle korunan, tekrarlanabilir kod tabanı

## Hedef Kitle

- Restoran işletmecileri ve zincir restoran yöneticileri
- Yemekhane / toplu yemek üretim tesisleri
- Gıda israfını azaltmayı ve kârlılığını artırmayı hedefleyen tüm yiyecek-içecek işletmeleri

## Product Backlog

- Agent bazlı sisteme uygun gerçek veri setlerinin bulunması ve hazırlanması ✅
- Keşifsel veri analizi (EDA) ✅
- Talep tahmin agent'ının eğitilmesi ✅
- Fire/israf risk agent'ının kurulması
- Kâr/fiyat agent'ının kurulması
- Agent'lar arası orkestrasyon ve karar katmanı
- Yönetici paneli / arayüz
- AI destekli günlük yönetici özeti

Kullanılan veri setleri ve hangi agent'a ait oldukları [`data/DATA_SOURCES.md`](data/DATA_SOURCES.md) dosyasında listelenmiştir.

## Repo Yapısı

```
BootcampYZTA_grup_112/
├── README.md                          # Bu dosya
├── docs/
│   ├── sprint-1/
│   │   └── WasteZero_Sprint1.md       # Sprint 1 Scrum çıktıları
│   └── sprint-2/
│       └── SPRINT2_TALEP_AGENT.md     # Sprint 2 — Talep Agent'ı dokümanı
├── data/
│   ├── raw/                           # İndirilen ham veri setleri
│   ├── processed/                     # Temizlenmiş / agent bazlı veri
│   └── DATA_SOURCES.md                # Agent–veri seti eşleştirmesi ve linkler
├── notebooks/
│   ├── 01_preprocessing_eda.ipynb     # Ön işleme + keşifsel veri analizi
│   └── talep_agent.ipynb              # Talep Agent'ı araştırma kaydı
├── src/
│   └── talep_agent.py                 # Talep Agent modülü (orkestratörün çağıracağı sınıf)
├── models/
│   └── talep_agent.joblib             # Eğitilmiş talep tahmin modeli
├── tests/
│   └── test_talep_agent.py            # 8 otomatik test
├── trello_sprint1                     # Sprint 1 board ekran görüntüsü
└── requirements.txt
```

## Kurulum

```bash
pip install -r requirements.txt
python -m src.talep_agent          # demo: hafta 140 tahmini yazdırır
python tests/test_talep_agent.py   # 8 testi çalıştırır
```

---

# Sprint 1

- **Sprint Notları**: User Story'ler product backlog item'ları içinde detaylandırılmıştır. Sprint 1'in tüm Scrum çıktıları (backlog dağıtma mantığı, Daily Scrum notları, board güncellemeleri, Review ve Retrospective) [`docs/sprint-1/WasteZero_Sprint1.md`](docs/sprint-1/WasteZero_Sprint1.md) dosyasında ayrıntılı olarak yer almaktadır.

- **Sprint içinde tamamlanması tahmin edilen puan**: 100 Puan

- **Puan tamamlama mantığı**: Proje boyunca tamamlanması gereken toplam 300 puanlık backlog bulunmaktadır. 3 sprint'e bölündüğünde her sprint'in 100 puandan oluşması kararlaştırıldı. İlk sprint'in kapsamı bilinçli olarak dar tutuldu: sağlam bir veri temeli ve keşifsel analiz olmadan modelleme, agent eğitimi ve karar katmanının anlamlı kurulması mümkün olmadığı için bu bileşenler sonraki sprint'lere bırakıldı.

- **Backlog düzeni ve Story seçimleri**: Görevler üç ilkeye göre dağıtılmıştır: **bağımlılık sırası** (EDA veriye bağımlı olduğu için önce veri araştırma ve temizleme planlandı), **yetkinlik ve ilgi alanı**, **iş yükü dengesi** (üç kişilik takımda Product Owner ve Scrum Master da aktif olarak geliştirmeye katıldı).

| ID | İş (User Story) | Atanan | Öncelik |
|---|---|---|---|
| US-01 | Agent bazlı sistem için uygun gerçek veri setlerinin araştırılması (talep, fire/israf, kâr/fiyat) | Beyza, Pelin, Furkan | Yüksek |
| US-02 | Seçilen veri setlerinin temizlenmesi ve ön işlenmesi (eksik değer, tip dönüşümü, tarih alanları) | Pelin, Beyza, Furkan | Yüksek |
| US-03 | GitHub repo yapısı, klasör düzeni, README ve veri dokümantasyonu | Pelin | Orta |
| US-04 | Keşifsel veri analizinin başlatılması (temel keşif ve ilk görselleştirmeler) | Furkan | Orta |

- **Daily Scrum**: Ekip üyelerinin eğitim ve iş sorumlulukları nedeniyle Daily Scrum, sprint boyunca haftada bir gün akşam saatlerinde online yapılmıştır (2 haftalık sprint'te toplam 2 toplantı). Her üye üç soruyu yanıtlamıştır: *Geçen haftadan bu yana ne yaptım? Önümüzdeki hafta ne yapacağım? Önümde engel var mı?* Toplantı notlarının tamamı [`docs/sprint-1/WasteZero_Sprint1.md`](docs/sprint-1/WasteZero_Sprint1.md) dosyasındadır.

- **Sprint board update**: Görevler To Do → In Progress → Done sütunlarında Trello üzerinden takip edilmiştir.

  ![Sprint 1 Board](trello_sprint1)

  | Aşama | To Do | In Progress | Done |
  |---|---|---|---|
  | Sprint Başı | US-01, US-02, US-03, US-04 | — | — |
  | Sprint Ortası | US-04 | US-02, US-03 | US-01 |
  | Sprint Sonu | — | US-04 (devam ediyor) | US-01, US-02, US-03 |

- **Ürün Durumu**: Sprint 1 sonunda WasteZero AI'nın veri temeli hazırdır ve keşifsel analiz başlatılmıştır. Talep, fire/israf ve kâr/fiyat konularını kapsayan gerçek veri setleri seçilmiş; eksik değerler, tip dönüşümleri ve tarih alanları işlenerek veri temizlenmiş; veri kaynakları ve değişkenler belgelenmiş; repo altyapısı kurulmuş ve EDA'nın ilk görselleştirmeleri üretilmiştir.

- **Sprint Review**:
  - Sprint hedefi (agent bazlı sisteme uygun gerçek veri setlerini bulmak ve EDA'ya başlamak) karşılandı.
  - Veri araştırma (US-01), temizleme (US-02) ve dokümantasyon (US-03) tamamlandı; EDA (US-04) planlandığı gibi başlatıldı ve kalan kısmı Sprint 2'ye devredildi.
  - Demo'da seçilen veri setleri, temizlik adımları ve ilk keşifsel analiz grafikleri gösterildi.
  - Sprint Review katılımcıları: Beyza ATA, Pelin ATAMAN, Furkan BİTİK.

- **Sprint Retrospective**:
  - Sprint kapsamını dar ve gerçekçi tutmak doğru karardı; hedefe ulaşıldı. Haftalık akşam toplantıları üyelerin yoğunluğuna uygundu ve düzenli yapıldı.
  - İki kişi eksik başlandığı için zamansal olarak geri kalındı; haftada tek toplantı, hafta içi küçük soruların çözümünü zaman zaman yavaşlattı; farklı kaynaklardan gelen veri setlerini ortak yapıya oturtmak beklenenden fazla tartışma gerektirdi.
  - Sonraki sprint kararları: Backlog dağıtımı aktif üye sayısına göre sürekli güncellenecek; haftalık toplantıya ek olarak hafta içi engeller için kısa yazılı güncelleme akışı kurulacak; veri setlerinin ortak yapısı (kategori eşlemesi) Sprint 2'nin başında netleştirilecek.

---

# Sprint 2

- **Sprint Notları**: Sprint 2'nin hedefi EDA'nın tamamlanması ve agent geliştirmeye geçilmesiydi. Görevler agent bazında paylaştırıldı: **Talep Agent'ı → Beyza**, **Fire/İsraf Agent'ı → Furkan**, **Kâr/Fiyat Agent'ı → Pelin**. Talep Agent'ının teknik dokümanı (veri, yöntem, deney kayıtları, testler) [`docs/sprint-2/SPRINT2_TALEP_AGENT.md`](docs/sprint-2/SPRINT2_TALEP_AGENT.md) dosyasında ayrıntılı olarak yer almaktadır.

- **Sprint içinde tamamlanması tahmin edilen puan**: 100 Puan

- **Puan tamamlama mantığı**: Toplam 300 puanlık backlog'un ikinci 100 puanlık dilimi bu sprint'e ayrılmıştır. Backlog, oyuncu ihtiyacı yerine sistemin çekirdeğini besleyecek şekilde düzenlendi: önce ortak kategori dili netleştirildi, ardından her üye kendi agent'ını bu ortak dil üzerinden geliştirdi.

- **Backlog düzeni ve Story seçimleri**:

| ID | İş (User Story) | Atanan | Öncelik |
|---|---|---|---|
| US-05 | EDA'nın tamamlanması ve ortak kategori eşlemesinin (14 → 5) netleştirilmesi | Furkan, Beyza | Yüksek |
| US-06 | Talep Agent'ının geliştirilmesi ve eğitilmesi | Beyza | Yüksek |
| US-07 | Fire/İsraf Agent'ı için veri profili ve geliştirme | Furkan | Yüksek |
| US-08 | Kâr/Fiyat Agent'ı için veri profili ve geliştirme | Pelin | Yüksek |
| US-09 | Agent çıktı sözleşmesinin (JSON formatı) tanımlanması ve otomatik testler | - | Orta |

- **Daily Scrum**: Sprint 1 retrospective kararı doğrultusunda haftalık akşam toplantılarına ek olarak, hafta içi engeller için kısa yazılı güncelleme akışı (WhatsApp) kullanılmıştır. <!-- Daily Scrum ekran görüntüleri linki: [Sprint 2 - Daily Scrum](#) -->

- **Sprint board update**: <<img width="1201" height="668" alt="Ekran Resmi 2026-07-15 20 56 33" src="https://github.com/user-attachments/assets/ea5f5867-991e-42f0-9a77-857d83b69e43" />

- **Ürün Durumu**: Sprint 2 sonunda:
  - **Talep Agent'ı tamamlandı**: Genpact gerçek talep verisiyle (456.548 satır, 145 hafta) eğitilen model, kategori bazlı tahmin hatasını naif yönteme göre **%12.4'ten %7.6'ya (MAPE)** düşürdü ve **her kategoride** naif yöntemi geçti. Model, orkestratörün tek satırla çağırabileceği bir Python sınıfı (`src/talep_agent.py`) olarak teslim edildi ve **8/8 otomatik test** ile korunuyor. Temiz kurulum doğrulamasında agent kendini eğitip birebir aynı sonuçları üretti.
  - Değerlendirmede zamana göre ayrım kullanıldı (eğitim: hafta 1–130, test: hafta 131–145); model seçimi test kümesine bakılmadan ayrı bir doğrulama diliminde yapıldı. 7 farklı iyileştirme denemesi kaydedildi ve yalnızca doğrulamada kazananlar (Poisson kaybı + promosyon özellikleri) final modele alındı.
  - EDA'dan önemli bulgu: promosyon, satışı **~3 katına** çıkarıyor; çorba kategorisinde veri boyunca hiç e-posta promosyonu yapılmamış (yalnızca sınırlı sayıda anasayfa vitrini var).
  - Kategori bazlı test sonuçları (MAPE — düşük iyi):

    | Kategori | Naif ("geçen hafta") | WasteZero modeli |
    |---|---|---|
    | **Genel** | %12.40 | **%7.64** |
    | corba | %4.47 | %3.41 |
    | tatli | %20.09 | %6.02 |
    | icecek | %10.24 | %7.07 |
    | ana_yemek | %9.51 | %7.80 |
    | salata | %17.70 | %13.87 |
  - Fire/İsraf ve Kâr/Fiyat agent'ları için kategori bazlı işlenmiş veriler hazırlandı (`data/processed/agent_waste.csv`, `agent_profit.csv`).

- **Sprint Review**:
  - Talep Agent'ının uçtan uca çalıştığı, JSON çıktı sözleşmesinin (kategori bazlı tahmin + `yuksek/normal/dusuk` sinyali) orkestratör için hazır olduğu gösterildi.
  - Modelin dürüst sınırlılığı açıkça raporlandı: salata kategorisindeki yüksek hata, test dönemindeki yalnızca iki promosyon haftasından kaynaklanıyor — nadir promosyon sıçramaları az örnekten öğrenilmek zorunda.
  - Sprint Review katılımcıları: Beyza ATA, Pelin ATAMAN, Furkan BİTİK.

- **Sprint Retrospective**:
  - **Doküman ile kod çelişiyordu**: `DATA_SOURCES.md` Genpact veri setini işaret ediyordu ancak işlenmiş dosyada kategori bilgisi yoktu; eksik `meal_info.csv` bulunup eklendi. *Ders: koda başlamadan kaynak dokümanı doğrula.*
  - **İlk model tasarımı çöpe gitti**: kategori seviyesinde eğitilen model naif tahmini yenemedi. *Ders: her model basit bir kıyasla test edilmeli.*
  - **Model seçimi test kümesiyle yapılmamalı**: kazanan hep doğrulama diliminde seçildi; mevsimsellik denemesi bunun neden şart olduğunu kanıtladı (doğrulamada kazanıp testte kaybetti).
  - Sprint 3 kararları: Orkestratör, `TalepAgent().predict(week)` çıktısını Fire ve Kâr agent'larının kategori profilleriyle birleştirecek; ardından karar katmanı, arayüz ve AI destekli yönetici özeti geliştirilecek.

---
