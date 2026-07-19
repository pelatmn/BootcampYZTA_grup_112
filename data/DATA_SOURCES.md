# Veri Kaynakları — WasteZero AI

Bu dosya, her agent'ın hangi gerçek veri seti ile beslendiğini gösterir. Tek bir birleşik tablo kullanılmaz; her agent kendi görev alanına ait gerçek veriyle çalışır. Veriler satır düzeyinde değil, ürün kategorisi (çorba, ana yemek, salata, tatlı, içecek) düzeyinde birleşir.

## Agent — Veri Seti Eşleştirmesi

### Talep Agent'ı
**Görev:** Kategori bazlı satış/talep tahmini.
**Veri seti:** Food Demand Dataset
**Link:** https://www.kaggle.com/datasets/arashnic/food-demand
**Ek dosya:** `data/raw/meal_info.csv` — `meal_id → category` eşlemesi (aynı veri setinin parçası). Ana veride yemekler yalnızca kod olarak bulunduğu için kategori bazlı tahmin bu dosya olmadan yapılamaz. Genpact'in 14 kategorisi projenin 5 ortak kategorisine eşlenir: Soup→corba, Salad→salata, Desert→tatli, Beverages→icecek, kalan 10 kategori→ana_yemek. Ayrıntı: `notebooks/talep_agent.ipynb` ve `src/talep_agent.py`

### Fire / İsraf Agent'ı
**Görev:** Ürün bazlı israf riski profili.
**Veri seti:** Food Wastage Data in Restaurant
**Link:** https://www.kaggle.com/datasets/trevinhannibal/food-wastage-data-in-restaurant

### Kâr / Fiyat Agent'ı
**Görev:** Fiyat, maliyet ve kârlılık analizi.
**Veri seti:** Predict Restaurant Menu Items Profitability
**Link:** https://www.kaggle.com/datasets/rabieelkharoua/predict-restaurant-menu-items-profitability

### Orkestratör
**Görev:** Agent çıktılarını birleştirir, çelişkileri değerlendirir, son karar ve yönetici özetini üretir.
**Veri seti:** Yok. Orkestratör bir dil modelidir; eğitilmez, agent çıktıları üzerinden çalışır.

## Özet Tablo

| Agent | Veri Seti | Link |
|---|---|---|
| Talep | Food Demand Dataset | https://www.kaggle.com/datasets/arashnic/food-demand |
| Fire/İsraf | Food Wastage Data in Restaurant | https://www.kaggle.com/datasets/trevinhannibal/food-wastage-data-in-restaurant |
| Kâr/Fiyat | Predict Restaurant Menu Items Profitability | https://www.kaggle.com/datasets/rabieelkharoua/predict-restaurant-menu-items-profitability |
| Orkestratör | — (dil modeli) | — |

## Ortak Anahtar: Ürün Kategorisi

Veri setleri farklı restoran ve kaynaklardan geldiği için satır düzeyinde birleştirilmez. Her setteki ürünler beş ortak kategoriye eşlenir: çorba, ana yemek, salata, tatlı, içecek. Agent'lar tahmin ve profillerini bu kategori düzeyinde üretir; orkestratör bu kategori profillerini karar anında birleştirir.

## İndirme

Kaggle hesabı ile web arayüzünden ya da Kaggle API ile indirilebilir:

```
kaggle datasets download -d arashnic/food-demand
kaggle datasets download -d trevinhannibal/food-wastage-data-in-restaurant
kaggle datasets download -d rabieelkharoua/predict-restaurant-menu-items-profitability
```

İndirilen dosyalar `data/raw/` klasörüne yerleştirilir.
