"""Fire Agent'i icin temel testler.

Calistirma:
    python tests/test_fire_agent.py        (pytest gerekmez)
    pytest tests/                          (pytest varsa)

Not: Agent varsayilan olarak repo icindeki data/processed klasorunu kullanir.
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.fire_agent import FireAgent  # noqa: E402

KATEGORILER = {"corba", "ana_yemek", "salata", "tatli", "icecek"}
SINYALLER = {"yuksek", "normal", "dusuk", "veri_yok"}

_agent = None


def agent():
    """Agent'i bir kez kur, testler arasinda paylas."""
    global _agent
    if _agent is None:
        _agent = FireAgent()
    return _agent


def test_profile_sozlesmesi():
    """profile() beklenen anahtarlari donduruyor mu? Her alt sozluk 5 kategoriyi icermeli."""
    out = agent().profile()
    assert set(out) == {"source", "global_mean_waste_ratio", "by_category",
                         "risk_index", "signal", "drivers"}
    assert set(out["by_category"]) == KATEGORILER
    assert set(out["risk_index"]) == KATEGORILER
    assert set(out["signal"]) == KATEGORILER
    assert set(out["drivers"]) == KATEGORILER


def test_corba_veri_yok():
    """corba icin agent_waste.csv'de hic satir yok -> veri_yok bekleniyor."""
    out = agent().profile()
    assert out["by_category"]["corba"] is None
    assert out["risk_index"]["corba"] is None
    assert out["drivers"]["corba"] is None
    assert out["signal"]["corba"] == "veri_yok"


def test_regresyon_risk_index():
    """Bilinen risk_index degerleri degismemeli (veri sessizce bozulursa yakalar).

    Degerler gercek data/processed/agent_waste.csv uzerinden hesaplanmistir
    (BASE_W=0.6, TAIL_W=0.4, TAIL_Q=0.90). Veri kasitli degistirilirse bu
    sayilar da guncellenmelidir.
    """
    beklenen = {
        "ana_yemek": 1.0628,
        "salata": 0.8441,
        "tatli": 1.0348,
        "icecek": 0.9522,
    }
    risk_index = agent().profile()["risk_index"]
    for kategori, deger in beklenen.items():
        assert risk_index[kategori] == deger, f"{kategori}: {risk_index[kategori]} != {deger}"

    signal = agent().profile()["signal"]
    assert signal["ana_yemek"] == "yuksek"
    assert signal["salata"] == "dusuk"
    assert signal["tatli"] == "normal"
    assert signal["icecek"] == "normal"


def test_risk_index_araliginda():
    """Tum sayisal risk_index degerleri makul araliktadir [0.5, 1.5]."""
    risk_index = agent().profile()["risk_index"]
    for kategori, deger in risk_index.items():
        if deger is None:
            continue
        assert 0.5 <= deger <= 1.5, f"{kategori}: {deger} aralik disinda"


def test_tekrarlanabilir():
    """Iki farkli agent orneginin profile() ciktisi birebir ayni olmali."""
    a = FireAgent().profile()
    b = FireAgent().profile()
    assert a == b


def test_drivers_yapisi():
    """Veri iceren bir kategori icin drivers pricing_level/prep_method icermeli."""
    drivers = agent().profile()["drivers"]["ana_yemek"]
    assert isinstance(drivers["pricing_level"], str)
    assert isinstance(drivers["prep_method"], str)


def test_robustluk_tek_kategori():
    """Sadece bir kategorinin verisi olan bir CSV ile de hatasiz calismali."""
    satirlar = [
        "food_type,num_guests,event_type,quantity_prepared,storage,purchase_history,"
        "seasonality,prep_method,geo_location,pricing_level,pricing_score,"
        "wastage_amount,category,waste_ratio",
    ]
    for i in range(6):
        satirlar.append(
            f"Meat,300,Corporate,500,Fridge,Regular,Summer,Buffet,Urban,High,2,"
            f"{20 + i},ana_yemek,{0.05 + i * 0.01:.4f}"
        )
    with tempfile.TemporaryDirectory() as tmp:
        csv_path = Path(tmp) / "agent_waste.csv"
        csv_path.write_text("\n".join(satirlar) + "\n", encoding="utf-8")

        gecici = FireAgent(data_dir=tmp)
        out = gecici.profile()

        assert out["signal"]["ana_yemek"] != "veri_yok"
        for kategori in KATEGORILER - {"ana_yemek"}:
            assert out["signal"][kategori] == "veri_yok"
            assert out["by_category"][kategori] is None
            assert out["risk_index"][kategori] is None
            assert out["drivers"][kategori] is None


def test_sinyaller_gecerli_kumeden():
    """Tum sinyaller tanimli kumeden gelmeli."""
    out = agent().profile()
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
