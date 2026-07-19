"""Kar/Fiyat Agent'i icin temel testler.

Calistirma:
    python tests/test_kar_fiyat_agent.py   (pytest gerekmez)
    pytest tests/                          (pytest varsa)

Not: Agent varsayilan olarak repo icindeki data/processed klasorunu kullanir.
"""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.kar_fiyat_agent import KarFiyatAgent, DEFAULT_DATA_DIR, PROFIT_FILE  # noqa: E402

KATEGORILER = {"corba", "ana_yemek", "salata", "tatli", "icecek"}
SINYALLER = {"yuksek", "normal", "dusuk", "veri_yok"}

_agent = None


def agent():
    """Agent'i bir kez kur, testler arasinda paylas."""
    global _agent
    if _agent is None:
        _agent = KarFiyatAgent()
    return _agent


def test_analyze_sozlesmesi():
    """analyze() beklenen anahtarlari donduruyor mu? Her alt sozluk 5 kategoriyi icermeli."""
    out = agent().analyze()
    assert set(out) == {"source", "by_category", "signal", "drivers"}
    assert set(out["by_category"]) == KATEGORILER
    assert set(out["signal"]) == KATEGORILER
    assert set(out["drivers"]) == KATEGORILER


def test_icecek_dusuk():
    """icecek gercek veride en dusuk karlilik kategorisi (norm_score < 0.40)."""
    out = agent().analyze()
    assert out["by_category"]["icecek"] < 0.40
    assert out["signal"]["icecek"] == "dusuk"


def test_corba_fallback():
    """corba, agent_profit.csv'de olmadigi icin demand_category fallback kullanmali."""
    out = agent().analyze()
    assert out["signal"]["corba"] != "veri_yok"
    assert out["drivers"]["corba"]["source"] == "demand_fallback"


def test_regresyon_by_category():
    """Bilinen cikti degismemeli (veri sessizce bozulursa yakalar).

    Degerler gercek data/processed/agent_profit.csv + agent_demand_category.csv
    uzerinden hesaplanmistir (profitability_score normalize skoru ve corba icin
    demand_category marj orani fallback'i). Veri kasitli degistirilirse bu sayilar
    da guncellenmelidir.
    """
    beklenen = {
        "corba": 0.7909,
        "ana_yemek": 0.7457,
        "salata": 0.7154,
        "tatli": 0.7253,
        "icecek": 0.3569,
    }
    assert agent().analyze()["by_category"] == beklenen


def test_tekrarlanabilir():
    """Iki farkli agent orneginin analyze() ciktisi birebir ayni olmali."""
    a = KarFiyatAgent().analyze()
    b = KarFiyatAgent().analyze()
    assert a == b


def test_ana_yemek_drivers():
    """ana_yemek 'profit' kaynaklidir; avg_price/high_share gecerli araliklarda olmali."""
    drivers = agent().analyze()["drivers"]["ana_yemek"]
    assert drivers["source"] == "profit"
    assert drivers["avg_price"] > 0
    assert 0 <= drivers["high_share"] <= 1


def test_profit_only_mod():
    """agent_demand_category.csv olmadan da (profit-only mod) hata vermeden calismali."""
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(DEFAULT_DATA_DIR / PROFIT_FILE, Path(tmp) / PROFIT_FILE)
        gecici = KarFiyatAgent(data_dir=tmp)
        out = gecici.analyze()
        assert out["source"] == "agent_profit"
        assert out["signal"]["corba"] == "veri_yok"
        assert out["by_category"]["corba"] is None
        assert out["drivers"]["corba"] is None


def test_sinyaller_gecerli_kumeden():
    """Tum sinyaller tanimli kumeden gelmeli."""
    out = agent().analyze()
    assert set(out["signal"].values()) <= SINYALLER


if __name__ == "__main__":
    testler = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    gecen, kalan = 0, []
    print(f"{len(testler)} test calistiriliyor...\n")
    for t in testler:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            gecen += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            kalan.append(t.__name__)
    print(f"\n{gecen}/{len(testler)} gecti")
    sys.exit(1 if kalan else 0)
