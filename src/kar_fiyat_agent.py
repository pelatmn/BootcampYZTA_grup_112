"""WasteZero AI — Kar/Fiyat Agent'i

Kategori bazli karlilik/fiyat profili ureten uzman agent.
Orkestrator bu agent'i cagirir ve kategori duzeyinde karlilik sinyali alir.

Kullanim:
    from src.kar_fiyat_agent import KarFiyatAgent
    agent = KarFiyatAgent()
    agent.analyze()
    # {'source': 'agent_profit+demand_category',
    #  'by_category': {'ana_yemek': 0.7457, ...},
    #  'signal': {'ana_yemek': 'yuksek', ...},
    #  'drivers': {'ana_yemek': {...}, ...}}

Veri:
    - data/processed/agent_profit.csv (menu bazli karlilik etiketleri; corba yok)
    - data/processed/agent_demand_category.csv (marj suruculeri + corba fallback icin)

Yontem:
    Ana skor agent_profit.csv'deki profitability_score (1/2/3) degerinden gelir:
    norm_score = (ortalama_skor - 1) / 2  -> [0, 1] araligina normalize edilir.
    agent_profit.csv'de bulunmayan kategoriler (corba) icin agent_demand_category.csv
    uzerinden marj orani (satis_fiyati - malzeme_maliyeti) / satis_fiyati fallback olarak
    kullanilir. Hic veri olmayan kategori icin sinyal "veri_yok" doner.
"""
from pathlib import Path

import pandas as pd

from src.sabitler import (
    KATEGORILER,
    SINYAL_DUSUK,
    SINYAL_NORMAL,
    SINYAL_VERI_YOK,
    SINYAL_YUKSEK,
)

# --- Sabitler ---------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "processed"

PROFIT_FILE = "agent_profit.csv"
DEMAND_FILE = "agent_demand_category.csv"

# Normalize edilmis skor esikleri (norm_score [0,1] araliginda)
PROFIT_HIGH, PROFIT_LOW = 0.60, 0.40

# Bu esigin altinda kalan kategori sayisi "az veri" olarak isaretlenir
LOW_N_ESIK = 80


class KarFiyatAgent:
    """Kategori bazli karlilik/fiyat profili ureten uzman agent."""

    def __init__(self, data_dir=None):
        self.data_dir = Path(data_dir) if data_dir else DEFAULT_DATA_DIR

        profit_path = self.data_dir / PROFIT_FILE
        if not profit_path.exists():
            raise FileNotFoundError(
                f"{PROFIT_FILE} bulunamadi, beklenen konum: {profit_path}"
            )
        self.profit = pd.read_csv(profit_path)

        demand_path = self.data_dir / DEMAND_FILE
        # Ikincil veri seti eksikse sessizce "sadece karlilik" moduna dus (hata verme).
        self.demand = pd.read_csv(demand_path) if demand_path.exists() else None

        self._analysis = self._compute()

    # --- Hesaplama ------------------------------------------------------
    def _margin_ratio_by_category(self) -> dict:
        """agent_demand_category.csv'den kategori basina ortalama marj orani."""
        if self.demand is None:
            return {}
        d = self.demand[self.demand["actual_selling_price"] > 0]
        marj = (d["actual_selling_price"] - d["typical_ingredient_cost"]) / d["actual_selling_price"]
        return d.assign(_marj=marj).groupby("category")["_marj"].mean().to_dict()

    def _compute(self) -> dict:
        """analyze() sozlesmesini bir kez hesapla (sonuc cache'lenir)."""
        profit = self.profit.dropna(subset=["profitability_score"])
        profit = profit[profit["profitability_score"].isin([1, 2, 3])]

        margin_ratio = self._margin_ratio_by_category()

        by_category, signal, drivers = {}, {}, {}
        for kat in KATEGORILER:
            sub = profit[profit["category"] == kat]
            n = len(sub)
            mr = margin_ratio.get(kat)

            if n > 0:
                norm = (sub["profitability_score"].mean() - 1) / 2
                by_category[kat] = round(float(norm), 4)
                drivers[kat] = {
                    "avg_price": round(float(sub["price"].mean()), 4),
                    "margin_ratio": round(float(mr), 4) if mr is not None else None,
                    "high_share": round(float((sub["profitability"] == "High").mean()), 4),
                    "source": "profit",
                    "low_n": n < LOW_N_ESIK,
                }
            elif mr is not None:
                by_category[kat] = round(float(mr), 4)
                drivers[kat] = {
                    "avg_price": None,
                    "margin_ratio": round(float(mr), 4),
                    "high_share": None,
                    "source": "demand_fallback",
                    "low_n": n < LOW_N_ESIK,
                }
            else:
                by_category[kat] = None
                drivers[kat] = None

            deger = by_category[kat]
            if deger is None:
                signal[kat] = SINYAL_VERI_YOK
            elif deger > PROFIT_HIGH:
                signal[kat] = SINYAL_YUKSEK
            elif deger < PROFIT_LOW:
                signal[kat] = SINYAL_DUSUK
            else:
                signal[kat] = SINYAL_NORMAL

        kaynak = "agent_profit+demand_category" if self.demand is not None else "agent_profit"
        return {"source": kaynak, "by_category": by_category, "signal": signal, "drivers": drivers}

    # --- Disa acik arayuz -------------------------------------------------
    def analyze(self) -> dict:
        """Kategori bazli karlilik/fiyat profili.

        Donen sozluk orkestratorun bekledigi sozlesmedir:
            source, by_category, signal, drivers
        Her alt sozluk tam olarak 5 ortak kategoriyi icerir.
        """
        return {
            "source": self._analysis["source"],
            "by_category": dict(self._analysis["by_category"]),
            "signal": dict(self._analysis["signal"]),
            "drivers": {k: (dict(v) if v is not None else None)
                        for k, v in self._analysis["drivers"].items()},
        }

    def categories(self) -> list:
        """Veri kapsamindaki (veri_yok olmayan) kategoriler."""
        return [kat for kat in KATEGORILER if self._analysis["signal"][kat] != SINYAL_VERI_YOK]


if __name__ == "__main__":
    agent = KarFiyatAgent()
    result = agent.analyze()
    print("Kar/Fiyat Agent'i — kaynak:", result["source"])
    for kat in KATEGORILER:
        skor = result["by_category"][kat]
        skor_str = f"{skor:.4f}" if skor is not None else "veri_yok"
        print(f"  {kat:10s} skor: {skor_str:>10s}   sinyal: {result['signal'][kat]}")
