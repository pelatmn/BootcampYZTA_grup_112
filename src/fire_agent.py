"""WasteZero AI — Fire Agent'i

Kategori bazli israf/fire riski profili ureten uzman agent.
Orkestrator bu agent'i cagirir ve kategori duzeyinde israf riski alir.

Kullanim:
    from src.fire_agent import FireAgent
    agent = FireAgent()
    agent.profile()
    # {'source': 'agent_waste', 'global_mean_waste_ratio': 0.0687,
    #  'by_category': {'ana_yemek': 0.0684, ..., 'corba': None},
    #  'risk_index': {'ana_yemek': 1.0628, ..., 'corba': None},
    #  'signal': {'ana_yemek': 'yuksek', ..., 'corba': 'veri_yok'},
    #  'drivers': {'ana_yemek': {...}, ..., 'corba': None}}

Veri: data/processed/agent_waste.csv (bkz. DATA_SOURCES.md). 'corba' kategorisinde
bu dosyada hic satir yok; bu kategori icin cikti daima veri_yok'tur.

Risk endeksi iki bilesenden olusur: kategori ortalamasinin genel ortalamaya orani
(base_ratio) ve kategorinin ust-kuyruk (yuksek israf) payinin genel kuyruk payina
orani (tail_ratio). Boylece hem "ortalama ne kadar kotu" hem de "asiri israf ne
siklikta" bilgisi tek bir endekste birlesir.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from src.sabitler import (KATEGORILER, SINYAL_YUKSEK, SINYAL_NORMAL,
                           SINYAL_DUSUK, SINYAL_VERI_YOK)

# --- Sabitler ---------------------------------------------------------------
# Risk endeksi agirliklari: 0.6 ortalama israf orani + 0.4 ust-kuyruk payi
BASE_W, TAIL_W = 0.6, 0.4

# Ust-kuyruk esigi: waste_ratio'nun bu yuzdelik dilimin ustunde kalan kismi
TAIL_Q = 0.90

# Risk sinyali esikleri (risk_index / 1.0)
RISK_HIGH, RISK_LOW = 1.05, 0.95

# Az veri uyarisi: bu satir sayisinin altinda kalan kategoriler dusuk guvenilirdir
MIN_N = 5

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "processed"


class FireAgent:
    """Kategori bazli israf/fire riski profili ureten uzman agent."""

    def __init__(self, data_dir=None):
        self.data_dir = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
        self.df = self._prepare_data()

    # --- Veri ---------------------------------------------------------------
    def _prepare_data(self) -> pd.DataFrame:
        """agent_waste.csv'yi yukle; NaN/inf waste_ratio satirlarini at."""
        path = self.data_dir / "agent_waste.csv"
        if not path.exists():
            raise FileNotFoundError(f"agent_waste.csv bulunamadi, beklenen yol: {path}")

        df = pd.read_csv(path)
        df["waste_ratio"] = df["waste_ratio"].replace([np.inf, -np.inf], np.nan)
        return df.dropna(subset=["waste_ratio"]).reset_index(drop=True)

    # --- Disa acik arayuz -----------------------------------------------------
    def categories(self) -> list:
        """Veride bulunan (satiri olan) kategoriler."""
        return [cat for cat in KATEGORILER if (self.df["category"] == cat).any()]

    def profile(self) -> dict:
        """Kategori bazli israf riski profili.

        Donen sozluk orkestratorun bekledigi sozlesmedir:
            source, global_mean_waste_ratio, by_category, risk_index, signal, drivers
        Her alt sozluk daima 5 ortak kategorinin tamamini icerir. Veride satiri
        olmayan kategoriler (ornegin 'corba') icin by_category/risk_index/drivers
        None, signal ise 'veri_yok' olur.
        """
        df = self.df
        global_mean = df["waste_ratio"].mean()
        tail_thr = df["waste_ratio"].quantile(TAIL_Q)
        global_tail = (df["waste_ratio"] > tail_thr).mean()

        by_category = {}
        risk_index = {}
        signal = {}
        drivers = {}

        for cat in KATEGORILER:
            sub = df[df["category"] == cat]
            if sub.empty:
                by_category[cat] = None
                risk_index[cat] = None
                signal[cat] = SINYAL_VERI_YOK
                drivers[cat] = None
                continue

            mean_c = sub["waste_ratio"].mean()
            base_ratio = mean_c / global_mean
            tailshare_c = (sub["waste_ratio"] > tail_thr).mean()
            tail_ratio = tailshare_c / global_tail
            idx = BASE_W * base_ratio + TAIL_W * tail_ratio

            by_category[cat] = round(float(mean_c), 4)
            risk_index[cat] = round(float(idx), 4)
            signal[cat] = (SINYAL_YUKSEK if idx > RISK_HIGH
                           else SINYAL_DUSUK if idx < RISK_LOW else SINYAL_NORMAL)

            cat_drivers = {}
            for col in ("pricing_level", "prep_method"):
                cat_drivers[col] = sub.groupby(col)["waste_ratio"].mean().idxmax()
            if len(sub) < MIN_N:
                cat_drivers["low_n"] = True
            drivers[cat] = cat_drivers

        return {
            "source": "agent_waste",
            "global_mean_waste_ratio": round(float(global_mean), 4),
            "by_category": by_category,
            "risk_index": risk_index,
            "signal": signal,
            "drivers": drivers,
        }


if __name__ == "__main__":
    agent = FireAgent()
    result = agent.profile()
    print("Fire Agent'i — israf/fire riski profili")
    print("  genel ortalama waste_ratio:", result["global_mean_waste_ratio"])
    for cat in KATEGORILER:
        idx = result["risk_index"][cat]
        print(f"  {cat:10s} risk_index: {str(idx):>8s}   sinyal: {result['signal'][cat]}")
