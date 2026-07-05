# WasteZero AI

**Takım:** The Parsimonia
**Bootcamp:** Yapay Zekâ ve Teknoloji Akademisi 2026

Restoranlar için akıllı menü, talep ve israf karar destek sistemi. WasteZero AI; restoranların geçmiş satış, üretim, fiyat, maliyet ve kampanya verilerini analiz ederek ürün bazlı talep tahmini yapar, fazla üretimden kaynaklanan fire/israf riskini hesaplar ve kârlılığı koruyacak şekilde günlük üretim ve menü kararlarına aksiyon önerileri sunar.

## Takım ve Roller

| Üye | Scrum Rolü | Sorumluluk |
|---|---|---|
| Beyza ATA | Product Owner | Backlog yönetimi, veri kaynağı gereksinimleri, veri seti araştırma, veri hazırlama |
| Pelin ATAMAN | Scrum Master | İletişim, Scrum event yönetimi, veri seti araştırma, veri temizleme |
| Furkan BİTİK | Developer | Veri seti araştırma, keşifsel veri analizi (EDA) |

## Sistem Yaklaşımı: Agent Bazlı Mimari

WasteZero AI, tek bir model yerine her biri kendi gerçek verisiyle çalışan uzman agent'lardan oluşur. Agent'lar çıktılarını ortak bir dil olan ürün kategorisi (çorba, ana yemek, salata, tatlı, içecek) üzerinden paylaşır. Bir orkestratör, agent çıktılarını birleştirip çelişkileri (satış kaçırma riski ile fire riski arasındaki dengeyi) değerlendirerek son kararı üretir.

| Agent | Görevi |
|---|---|
| Talep Agent'ı | Kategori bazlı satış/talep tahmini |
| Fire/İsraf Agent'ı | Ürün bazlı israf riski profili |
| Kâr/Fiyat Agent'ı | Fiyat, maliyet ve kârlılık analizi |
| Orkestratör | Agent çıktılarını birleştirir, karar ve yönetici özeti üretir |

## Ürün Backlog (Genel)

- Agent bazlı sisteme uygun gerçek veri setlerinin bulunması ve hazırlanması
- Keşifsel veri analizi (EDA)
- Talep tahmin agent'ının eğitilmesi
- Fire/israf risk agent'ının kurulması
- Kâr/fiyat agent'ının kurulması
- Agent'lar arası orkestrasyon ve karar katmanı
- Yönetici paneli / arayüz
- AI destekli günlük yönetici özeti

## Sprint Durumu

| Sprint | Kapsam | Durum |
|---|---|---|
| Sprint 1 | Veri seti bulma + EDA başlangıcı | Tamamlandı |
| Sprint 2 | EDA'nın tamamlanması + agent geliştirme | Planlandı |
| Sprint 3 | Orkestrasyon + arayüz + yönetici özeti | Planlandı |

## Repo Yapısı

```
wastezero-ai/
├── README.md                     # Bu dosya
├── docs/
│   └── sprint-1/                  # Sprint 1 Scrum dokümanları
│       ├── sprint1-ciktilari.md
│       └── screenshots/           # Sprint board ekran görüntüleri
├── data/
│   ├── raw/                       # İndirilen ham veri setleri
│   ├── processed/                # Temizlenmiş veri
│   └── DATA_SOURCES.md            # Agent–veri seti eşleştirmesi ve linkler
├── notebooks/
│   └── 01_eda.ipynb              # Keşifsel veri analizi
├── src/                          # (Sonraki sprintler: agent ve orkestrasyon kodu)
├── requirements.txt
└── .gitignore
```

## Kurulum

```
pip install -r requirements.txt
```

## Veri Kaynakları

Kullanılan veri setleri ve hangi agent'a ait oldukları `data/DATA_SOURCES.md` dosyasında listelenmiştir.
