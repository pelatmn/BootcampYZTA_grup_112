"""WasteZero AI — Talep Agent'i

Kategori bazli satis/talep tahmini ureten uzman agent.
Orkestrator bu agent'i cagirir ve kategori duzeyinde talep alir.

Kullanim:
    from src.talep_agent import TalepAgent
    agent = TalepAgent()
    agent.predict(140)
    # {'week': 140, 'in_sample': False,
    #  'by_category': {'ana_yemek': 367661, ...},
    #  'signal': {'ana_yemek': 'dusuk', ...}}

Veri: Genpact Food Demand Dataset + meal_info.csv (DATA_SOURCES.md'ye bakiniz).
Model satir seviyesinde (hafta x merkez x yemek) egitilir, tahminler kategoriye toplanir.

Model v2: Poisson kaybi + promosyon ozellikleri. Varyant secimi dogrulama diliminde
(hafta 116-130) yapildi, test (131-145) yalnizca raporlama icin kullanildi.
Kategori MAPE: %8.27 -> %7.50.
"""
from pathlib import Path
from urllib.parse import quote

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

# --- Sabitler ---------------------------------------------------------------
REPO = "https://raw.githubusercontent.com/pelatmn/BootcampYZTA_grup_112/main"

# Genpact'in 14 kategorisi -> projenin 5 ortak kategorisi (kalanlar ana_yemek)
CAT_MAP = {"Soup": "corba", "Salad": "salata", "Desert": "tatli", "Beverages": "icecek"}

# Egitim/test siniri: bu haftaya kadar egitilir (zaman serisi -> rastgele bolme YOK)
CUT = 130

FEATS = ["week", "center_id", "meal_id", "category_tr", "cuisine",
         "checkout_price", "base_price", "discount_rate",
         "emailer_for_promotion", "homepage_featured",
         "lag1", "lag2", "lag4", "roll4",
         # v2: promosyon ozellikleri (promosyonlar onceden planlanir -> sizinti yok)
         "promo_any", "promo_lag1", "promo_new", "price_ratio",
         "center_promo_share", "cat_promo_share"]
CATS = ["center_id", "meal_id", "category_tr", "cuisine"]

# v2: Poisson kaybi — siparis sayim verisine kare-hatadan daha iyi uyar
LOSS = "poisson"

# Talep sinyali esikleri (tahmin / gecmis ortalama)
SIGNAL_HIGH, SIGNAL_LOW = 1.1, 0.9

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "raw"
DEFAULT_MODEL_PATH = ROOT / "models" / "talep_agent.joblib"


class TalepAgent:
    """Kategori bazli talep tahmini ureten uzman agent."""

    def __init__(self, data_dir=None, model_path=None):
        self.data_dir = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
        self.model_path = Path(model_path) if model_path else DEFAULT_MODEL_PATH

        self.df = self._prepare_data()
        # Kategorik kolonlarin kategori listesini tum veriden sabitliyoruz.
        # (sklearn kategorileri fit sirasinda hatirladigi icin sart degil; test edildi.
        #  Yine de sozlesmeyi acik yapar ve surum/model degisikliklerine karsi korur.)
        self.dtypes = {c: pd.CategoricalDtype(categories=sorted(self.df[c].unique()))
                       for c in CATS}
        self.model = self._load_or_train()
        # Kategori basina gecmis ortalama haftalik talep (sinyal referansi)
        self.hist = self.df.groupby("category_tr").num_orders.sum() / self.df.week.nunique()

    # --- Veri ---------------------------------------------------------------
    def _read_csv(self, filename: str) -> pd.DataFrame:
        """Once yerelden oku; yoksa takim reposundan cek."""
        local = self.data_dir / filename
        if local.exists():
            return pd.read_csv(local)
        return pd.read_csv(f"{REPO}/data/raw/{quote(filename)}")

    def _prepare_data(self) -> pd.DataFrame:
        """Genpact + meal_info yukle -> kategori ekle -> ozellikleri uret."""
        train = self._read_csv("Food Demand Forecasting.csv")
        meal = self._read_csv("meal_info.csv")

        df = train.merge(meal, on="meal_id", how="left")
        df["category_tr"] = df["category"].map(CAT_MAP).fillna("ana_yemek")

        # (merkez, yemek) serisi basina gecikme ozellikleri
        df = df.sort_values(["center_id", "meal_id", "week"]).reset_index(drop=True)
        df["discount_rate"] = (df.base_price - df.checkout_price) / df.base_price

        grp = df.groupby(["center_id", "meal_id"])["num_orders"]
        for lag in (1, 2, 4):
            df[f"lag{lag}"] = grp.shift(lag)
        # transform: grup sinirlarini asmayan hareketli ortalama
        df["roll4"] = grp.transform(lambda s: s.shift(1).rolling(4).mean())

        # v2: promosyon ozellikleri. Salata hatasi tamamen promosyon haftalarinda
        # yogunlasiyordu; bu ozellikler modele "promosyon yeni mi, ne kadar yaygin"
        # bilgisini verir. Promosyonlar onceden planlandigi icin tahmin aninda bilinir.
        g = df.groupby(["center_id", "meal_id"])
        df["promo_any"] = ((df.emailer_for_promotion == 1) | (df.homepage_featured == 1)).astype(int)
        df["promo_lag1"] = g["promo_any"].shift(1).fillna(0)
        df["promo_new"] = ((df.promo_any == 1) & (df.promo_lag1 == 0)).astype(int)
        price_roll4 = g["checkout_price"].transform(lambda s: s.shift(1).rolling(4).mean())
        df["price_ratio"] = (df.checkout_price / price_roll4).fillna(1.0)
        df["center_promo_share"] = df.groupby(["week", "center_id"])["promo_any"].transform("mean")
        df["cat_promo_share"] = df.groupby(["week", "category_tr"])["promo_any"].transform("mean")

        return df.dropna(subset=["lag1", "lag2", "lag4", "roll4"]).reset_index(drop=True)

    def _prep_features(self, rows: pd.DataFrame) -> pd.DataFrame:
        """Model girdisini hazirla; kategori kodlari her zaman ayni olsun."""
        X = rows[FEATS].copy()
        for col in CATS:
            X[col] = X[col].astype(self.dtypes[col])
        return X

    # --- Model --------------------------------------------------------------
    def _load_or_train(self) -> HistGradientBoostingRegressor:
        """Kayitli model varsa yukle; yoksa (veya bozuksa) egit ve kaydet."""
        if self.model_path.exists():
            try:
                payload = joblib.load(self.model_path)
                if (payload.get("feats") == FEATS and payload.get("cut") == CUT
                        and payload.get("loss") == LOSS):
                    return payload["model"]
            except Exception:
                pass  # bozuk / uyumsuz dosya -> yeniden egit

        return self._train_and_save()

    def _train_and_save(self) -> HistGradientBoostingRegressor:
        train = self.df[self.df.week <= CUT]
        model = HistGradientBoostingRegressor(
            max_iter=400, learning_rate=0.06, loss=LOSS,
            categorical_features=[FEATS.index(c) for c in CATS],
            random_state=42,
        )
        model.fit(self._prep_features(train), train.num_orders)

        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"model": model, "feats": FEATS, "cut": CUT, "loss": LOSS},
                    self.model_path)
        return model

    # --- Disa acik arayuz ---------------------------------------------------
    def available_weeks(self) -> list:
        """Tahmin edilebilecek haftalar."""
        return sorted(self.df.week.unique().tolist())

    def predict(self, week: int) -> dict:
        """Verilen hafta icin kategori bazli talep tahmini ve talep sinyali.

        Donen sozluk orkestratorun bekledigi sozlesmedir:
            week, in_sample, by_category, signal
        `in_sample=True` ise model o haftayi egitimde gormustur (guvenilirligi dusuktur).
        """
        rows = self.df[self.df.week == week]
        if rows.empty:
            weeks = self.available_weeks()
            raise ValueError(f"hafta {week} veride yok (gecerli aralik: {weeks[0]}-{weeks[-1]})")

        preds = np.maximum(self.model.predict(self._prep_features(rows)), 0)
        by_category = (rows.assign(pred=preds)
                       .groupby("category_tr").pred.sum()
                       .round().astype(int).to_dict())

        signal = {}
        for cat, value in by_category.items():
            ratio = value / self.hist[cat]
            signal[cat] = ("yuksek" if ratio > SIGNAL_HIGH
                           else "dusuk" if ratio < SIGNAL_LOW else "normal")

        return {"week": int(week), "in_sample": bool(week <= CUT),
                "by_category": by_category, "signal": signal}


if __name__ == "__main__":
    agent = TalepAgent()
    result = agent.predict(140)
    print("Talep Agent'i — hafta", result["week"], "(in_sample:", result["in_sample"], ")")
    for cat, qty in sorted(result["by_category"].items()):
        print(f"  {cat:10s} {qty:>8,} adet   sinyal: {result['signal'][cat]}")
