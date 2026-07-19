"""On isleme modulu (src/preprocessing.py) icin temel testler.

Calistirma:
    python tests/test_preprocessing.py     (pytest gerekmez)
    pytest tests/                          (pytest varsa)

Not: Pipeline data/raw klasorunu okur, ciktilari gecici bir klasore yazar;
data/processed altindaki mevcut dosyalara dokunulmaz.
"""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.preprocessing import run_all, CATEGORIES  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
KATEGORILER = {"corba", "ana_yemek", "salata", "tatli", "icecek"}

BEKLENEN_DOSYALAR = {
    "agent_demand.csv",
    "agent_demand_category.csv",
    "agent_waste.csv",
    "agent_profit.csv",
}

_sonuclar = None
_tmp_dir = None


def sonuclar():
    """Pipeline'i bir kez gecici klasore calistir, testler arasinda paylas."""
    global _sonuclar, _tmp_dir
    if _sonuclar is None:
        _tmp_dir = tempfile.mkdtemp(prefix="wz_preprocessing_")
        _sonuclar = run_all(raw_dir=str(RAW_DIR), out_dir=_tmp_dir)
    return _sonuclar


def test_pipeline_dort_dosya_uretir():
    """run_all() tam olarak 4 cikti uretmeli, hepsi gecici klasore yazilmis olmali."""
    res = sonuclar()
    assert set(res) == BEKLENEN_DOSYALAR
    for isim in BEKLENEN_DOSYALAR:
        path = Path(_tmp_dir) / isim
        assert path.exists(), f"{isim} diske yazilmamis"


def test_dosyalar_bos_degil():
    """Her cikti en az bir satir ve bir sutun icermeli."""
    for isim, df in sonuclar().items():
        assert df.shape[0] > 0, f"{isim} bos (satir yok)"
        assert df.shape[1] > 0, f"{isim} bos (sutun yok)"


def test_beklenen_sutunlar():
    """Her ciktida ilgili agent'in ihtiyac duydugu anahtar sutunlar bulunmali."""
    res = sonuclar()
    assert {"discount_rate", "is_promoted", "num_orders"} <= set(res["agent_demand.csv"].columns)
    assert {"category", "quantity_sold"} <= set(res["agent_demand_category.csv"].columns)
    assert {"category", "waste_ratio", "pricing_score"} <= set(res["agent_waste.csv"].columns)
    assert {"category", "profitability_score", "ingredients_hidden"} <= set(res["agent_profit.csv"].columns)


def test_kategori_kumesi_sinirli():
    """category sutunu her ciktida yalnizca 5 ortak kategoriden olusmali."""
    res = sonuclar()
    assert set(CATEGORIES) == KATEGORILER
    for isim in ("agent_demand_category.csv", "agent_waste.csv", "agent_profit.csv"):
        kategoriler = set(res[isim]["category"].unique())
        assert kategoriler <= KATEGORILER, f"{isim} beklenmeyen kategori icerir: {kategoriler - KATEGORILER}"


def test_waste_ratio_hesabi_dogru():
    """waste_ratio = wastage_amount / quantity_prepared olmali (yuvarlama haric)."""
    waste = sonuclar()["agent_waste.csv"]
    beklenen = (waste["wastage_amount"] / waste["quantity_prepared"]).round(4)
    assert (waste["waste_ratio"] - beklenen).abs().max() < 1e-9


def test_discount_rate_hesabi_dogru():
    """discount_rate = (base_price - checkout_price) / base_price olmali."""
    demand = sonuclar()["agent_demand.csv"]
    beklenen = ((demand["base_price"] - demand["checkout_price"]) / demand["base_price"]).round(4)
    assert (demand["discount_rate"] - beklenen).abs().max() < 1e-9


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
    if _tmp_dir:
        shutil.rmtree(_tmp_dir, ignore_errors=True)
    sys.exit(1 if kalan else 0)