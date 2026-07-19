"""WasteZero AI — On Isleme Modulu

`notebooks/01_preprocessing_eda.ipynb` (Sprint 1) icindeki on isleme mantigini
tekrar calistirilabilir hale getirir. data/raw altindaki ham veriden
data/processed altindaki 4 agent girdisini uretir: agent_demand.csv,
agent_demand_category.csv, agent_waste.csv, agent_profit.csv.

Kullanim:
    from src.preprocessing import run_all
    run_all()  # data/raw -> data/processed

    # veya tek tek:
    from src.preprocessing import build_agent_demand
    build_agent_demand("data/raw", "data/processed")

Not: build_agent_demand, notebook'taki dinamik dosya aramasini aynen korur:
data/raw icinde `meal_id` + (`category` veya `cuisine`) sutunlu bir dosya
(orn. meal_info.csv) bulunursa Kaggle Food Demand tablosuyla birlestirilir.
Bu dosya notebook ilk calistirildiginde depoda yoktu; bugun meal_info.csv
mevcut oldugu icin cikti, depodaki eski agent_demand.csv'den ek `category`/
`cuisine` sutunlariyla ayrisir (bkz. testler ve calistirma raporu).
"""
from pathlib import Path

import pandas as pd

# --- Ortak kategori koprusu: map_to_category --------------------------------
CATEGORIES = ["corba", "ana_yemek", "salata", "tatli", "icecek"]

# Anahtar kelime kurallari (Turkce + Ingilizce; bu depodaki gercek urun adlarina
# gore genisletildi). Bosluklu anahtar kelimeler kelime siniri gibi davranir
# (metin iki yanindan boslukla yastiklanir).
CATEGORY_KEYWORDS = {
    "corba": ["corba", "çorba", "chorba", "soup", "laksa"],
    "icecek": ["icecek", "içecek", "beverage", "drink", " tea", " teh", "çay",
               "coffee", "kahve", " soda", " cola", "lemonade", "limonata", "juice",
               "ayran", " süt ", "milk", "dairy", "latte", "smoothie"],
    "tatli": ["tatli", "tatlı", "dessert", "cake", "kek", " tart", "tiramisu",
              "baklava", "cendol", "sweet", "fruit", "meyve", "baked", "pudding",
              "sütlaç", "dondurma", "ice cream", "künefe", "helva"],
    "ana_yemek": ["kebap", "kebab", "steak", "chicken", "tavuk", "beef", "köfte",
                  "kofte", "fish", "balık", "shrimp", "karides", " rice", "pilav",
                  "noodle", "pasta", "spaghetti", "burger", "nasi", "roti", "rendang",
                  "tandoori", "toast", "stir", "meat", "alfredo", "scampi", " main",
                  "güveç", "kavurma"],
    "salata": ["salata", "salad", "vegetable", "sebze", "greens", "caprese", "piyaz"],
}
# Kontrol sirasi: ayirt edici gruplar once, salata en sonda (Vegetable Stir-Fry
# gibi sebzeli ana yemekler yanlislikla salataya dusmesin diye).
CHECK_ORDER = ["corba", "icecek", "tatli", "ana_yemek", "salata"]
DEFAULT_CATEGORY = "ana_yemek"  # hicbir kural uymazsa varsayilan (belgelenmis karar)


def map_to_category(name) -> str:
    """Urun/yemek adini 5 ortak kategoriden birine esler."""
    if not isinstance(name, str) or not name.strip():
        return DEFAULT_CATEGORY
    text = " " + name.lower().strip() + " "  # bosluklu anahtar kelimeler icin yastikla
    for cat in CHECK_ORDER:
        if any(kw in text for kw in CATEGORY_KEYWORDS[cat]):
            return cat
    return DEFAULT_CATEGORY


# --- Talep Agent'i — Kaggle Food Demand sutun konfigurasyonu ----------------
DEMAND_FILE = "Food Demand Forecasting.csv"
D_ITEM_COL = "meal_id"          # urun kimligi (kategori bilgisi ayri dosyada olabilir)
D_PRICE_COL = "checkout_price"  # gercek satis fiyati
D_BASEP_COL = "base_price"      # liste fiyati
D_PROMO_COLS = ["emailer_for_promotion", "homepage_featured"]  # promosyon bayraklari

# --- Talep Agent'i — kategori kopruli gunluk satis sutun konfigurasyonu -----
SALES_FILE = "restaurant_sales_data.csv"
S_DATE_COL = "date"           # satis gunu (AA/GG/YYYY formatinda gelir)
S_ITEM_COL = "menu_item_name"  # urun adi -> kategori eslemesi buradan yapilir

# --- Fire/Israf Agent'i sutun konfigurasyonu ---------------------------------
WASTE_FILE = "food_wastage_data.csv"
WASTE_RENAME = {
    "Type of Food": "food_type",              # malzeme grubu (kategori eslemesi buradan)
    "Number of Guests": "num_guests",
    "Event Type": "event_type",
    "Quantity of Food": "quantity_prepared",  # hazirlanan miktar
    "Storage Conditions": "storage",
    "Purchase History": "purchase_history",
    "Seasonality": "seasonality",
    "Preparation Method": "prep_method",
    "Geographical Location": "geo_location",
    "Pricing": "pricing_level",               # metinsel fiyat seviyesi (Low/Moderate/High)
    "Wastage Food Amount": "wastage_amount",  # israf edilen miktar (hedef)
}
W_QTY_COL = "quantity_prepared"
W_WASTE_COL = "wastage_amount"

# --- Kar/Fiyat Agent'i sutun konfigurasyonu ----------------------------------
MENU_FILE = "restaurant_menu_optimization_data.csv"
MENU_RENAME = {
    "RestaurantID": "restaurant_id",
    "MenuCategory": "menu_category",
    "MenuItem": "item_name",
    "Ingredients": "ingredients",
    "Price": "price",
    "Profitability": "profitability",
}
P_PROFIT_COL = "profitability"  # karlilik etiketi (Low/Medium/High)
# Menu kategorisinden ortak kategoriye dogrudan esleme (Appetizers bilerek yok:
# urun adiyla map_to_category ile cozulur).
MENU_CAT_MAP = {"Beverages": "icecek", "Desserts": "tatli", "Main Course": "ana_yemek"}


def _read_raw_csv(raw_dir, filename: str, **kwargs) -> pd.DataFrame:
    """raw_dir icinden CSV okur."""
    return pd.read_csv(Path(raw_dir) / filename, **kwargs)


def _find_meal_info_file(raw_dir, exclude: str):
    """data/raw icinde meal_id + (category|cuisine) sutunlu bir dosya arar.

    Notebook'taki dinamik arama davranisinin aynisi: `exclude` disindaki ilk
    CSV'de bu sutunlar bulunursa o dosya adi donulur; bulunamazsa None.
    """
    raw_dir = Path(raw_dir)
    for f in sorted(p.name for p in raw_dir.iterdir()):
        if not f.endswith(".csv") or f == exclude:
            continue
        try:
            head_cols = {c.lower() for c in pd.read_csv(raw_dir / f, nrows=3).columns}
        except Exception:
            continue
        if "meal_id" in head_cols and ("category" in head_cols or "cuisine" in head_cols):
            return f
    return None


def build_agent_demand(raw_dir="data/raw", out_dir="data/processed") -> pd.DataFrame:
    """Kaggle Food Demand tablosunu temizler, agent_demand.csv olarak yazar."""
    demand = _read_raw_csv(raw_dir, DEMAND_FILE)
    demand = demand.drop_duplicates()

    # Tip duzeltmeleri: 0/1 kodlu promosyon bayraklarini bool yap
    for c in D_PROMO_COLS:
        if c in demand.columns:
            demand[c] = demand[c].astype(bool)

    # Turetilmis ozellikler: indirim orani ve genel promosyon bayragi
    if D_PRICE_COL in demand.columns and D_BASEP_COL in demand.columns:
        demand["discount_rate"] = ((demand[D_BASEP_COL] - demand[D_PRICE_COL]) / demand[D_BASEP_COL]).round(4)
    if all(c in demand.columns for c in D_PROMO_COLS):
        demand["is_promoted"] = demand[D_PROMO_COLS].any(axis=1)

    # Kategori koprusu denemesi: meal_id -> kategori icin meal_info benzeri dosya ara
    meal_info_file = _find_meal_info_file(raw_dir, exclude=DEMAND_FILE)
    if meal_info_file and D_ITEM_COL in demand.columns:
        info = _read_raw_csv(raw_dir, meal_info_file)
        demand = demand.merge(info, on=D_ITEM_COL, how="left")

    out_path = Path(out_dir) / "agent_demand.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    demand.to_csv(out_path, index=False)
    return demand


def build_agent_demand_category(raw_dir="data/raw", out_dir="data/processed") -> pd.DataFrame:
    """Gunluk satis tablosunu temizler, kategori eslemesi ekler, agent_demand_category.csv yazar."""
    sales = _read_raw_csv(raw_dir, SALES_FILE)
    sales = sales.drop_duplicates()

    # Tarih tipini duzelt: metin -> datetime, aylik EDA/agregasyon icin year_month
    if S_DATE_COL in sales.columns:
        sales[S_DATE_COL] = pd.to_datetime(sales[S_DATE_COL], format="%m/%d/%Y")
        sales["year_month"] = sales[S_DATE_COL].dt.to_period("M").astype(str)

    # Urun adlarini 5 ortak kategoriye esle (kopru sutunu)
    if S_ITEM_COL in sales.columns:
        sales["category"] = sales[S_ITEM_COL].map(map_to_category)

    out_path = Path(out_dir) / "agent_demand_category.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sales.to_csv(out_path, index=False)
    return sales


def build_agent_waste(raw_dir="data/raw", out_dir="data/processed") -> pd.DataFrame:
    """Israf tablosunu temizler, turetilmis ozellikler ekler, agent_waste.csv yazar."""
    waste = _read_raw_csv(raw_dir, WASTE_FILE)
    waste = waste.rename(columns=WASTE_RENAME)
    waste = waste.drop_duplicates()

    # Metinsel sirali degiskeni sayiya cevir: ortalama alinabilsin diye
    if "pricing_level" in waste.columns:
        waste["pricing_score"] = waste["pricing_level"].map({"Low": 1, "Moderate": 2, "High": 3})

    # Kategori koprusu: malzeme grubu -> 5 ortak kategori (yaklasik esleme)
    if "food_type" in waste.columns:
        waste["category"] = waste["food_type"].map(map_to_category)

    # Turetilmis ozellik: israf orani = israf / hazirlanan
    if W_QTY_COL in waste.columns and W_WASTE_COL in waste.columns:
        waste["waste_ratio"] = (waste[W_WASTE_COL] / waste[W_QTY_COL]).round(4)

    out_path = Path(out_dir) / "agent_waste.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    waste.to_csv(out_path, index=False)
    return waste


def build_agent_profit(raw_dir="data/raw", out_dir="data/processed") -> pd.DataFrame:
    """Menu ekonomisi tablosunu temizler, turetilmis ozellikler ekler, agent_profit.csv yazar."""
    menu = _read_raw_csv(raw_dir, MENU_FILE)
    menu = menu.rename(columns=MENU_RENAME)
    menu = menu.drop_duplicates()

    # Veri kalitesi bayragi: icerigi gizlenmis kayitlar
    if "ingredients" in menu.columns:
        menu["ingredients_hidden"] = menu["ingredients"].str.contains("confidential", case=False, na=False)

    # Metinsel sirali karlilik etiketini sayisal skora cevir
    if P_PROFIT_COL in menu.columns:
        menu["profitability_score"] = menu[P_PROFIT_COL].map({"Low": 1, "Medium": 2, "High": 3})

    # Kategori koprusu: once menu kategorisi, Appetizers icin urun adi
    if "menu_category" in menu.columns and "item_name" in menu.columns:
        menu["category"] = [
            MENU_CAT_MAP.get(mc) or map_to_category(item)
            for mc, item in zip(menu["menu_category"], menu["item_name"])
        ]

    out_path = Path(out_dir) / "agent_profit.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    menu.to_csv(out_path, index=False)
    return menu


def run_all(raw_dir="data/raw", out_dir="data/processed") -> dict:
    """4 agent girdisini de uretir; {dosya_adi: DataFrame} dondurur."""
    return {
        "agent_demand.csv": build_agent_demand(raw_dir, out_dir),
        "agent_demand_category.csv": build_agent_demand_category(raw_dir, out_dir),
        "agent_waste.csv": build_agent_waste(raw_dir, out_dir),
        "agent_profit.csv": build_agent_profit(raw_dir, out_dir),
    }


if __name__ == "__main__":
    sonuclar = run_all()
    print("On isleme tamamlandi:")
    for isim, df in sonuclar.items():
        print(f"  {isim:28s} {df.shape[0]:>8,} satir x {df.shape[1]} sutun")