"""Talep Agent'i icin temel testler.

Calistirma:
    python tests/test_talep_agent.py      (pytest gerekmez)
    pytest tests/                          (pytest varsa)

Not: Agent varsayilan olarak repo icindeki data/raw ve models/ klasorunu kullanir.
Farkli bir veri klasoru icin WZ_DATA_DIR ortam degiskeni verilebilir.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.talep_agent import TalepAgent, CUT  # noqa: E402

KATEGORILER = {"corba", "ana_yemek", "salata", "tatli", "icecek"}
SINYALLER = {"yuksek", "normal", "dusuk"}

_agent = None


def agent():
    """Agent'i bir kez kur, testler arasinda paylas (egitim pahali)."""
    global _agent
    if _agent is None:
        _agent = TalepAgent(data_dir=os.environ.get("WZ_DATA_DIR"))
    return _agent


def test_predict_sozlesmesi():
    """predict() beklenen anahtarlari donduruyor mu?"""
    out = agent().predict(140)
    assert set(out) == {"week", "in_sample", "by_category", "signal"}
    assert out["week"] == 140


def test_bes_kategori():
    """Cikti tam olarak 5 ortak kategoriyi icermeli."""
    out = agent().predict(140)
    assert set(out["by_category"]) == KATEGORILER
    assert set(out["signal"]) == KATEGORILER


def test_degerler_gecerli():
    """Talep negatif olamaz; sinyaller tanimli kumeden gelmeli."""
    out = agent().predict(140)
    for kategori, adet in out["by_category"].items():
        assert isinstance(adet, int), f"{kategori} int degil"
        assert adet >= 0, f"{kategori} negatif: {adet}"
    assert set(out["signal"].values()) <= SINYALLER


def test_in_sample_bayragi():
    """Egitimde gorulen hafta True, gorulmeyen False donmeli."""
    assert agent().predict(100)["in_sample"] is True    # 100 <= CUT(130)
    assert agent().predict(140)["in_sample"] is False   # 140 > CUT


def test_gecersiz_hafta_hata_verir():
    """Veride olmayan hafta icin anlasilir hata."""
    try:
        agent().predict(999)
    except ValueError as e:
        assert "999" in str(e)
    else:
        raise AssertionError("999 icin ValueError bekleniyordu")


def test_available_weeks():
    """Hafta listesi sirali ve makul araliklarda olmali."""
    weeks = agent().available_weeks()
    assert weeks == sorted(weeks)
    assert weeks[0] >= 1 and weeks[-1] <= 145
    assert CUT in weeks


def test_regresyon_hafta_140():
    """Bilinen cikti degismemeli (model/veri sessizce bozulursa yakalar).

    Beklenen degerler model v2'ye (poisson + promosyon ozellikleri) aittir.
    Model bilerek degistirilirse bu sayilar da guncellenmelidir.
    """
    beklenen = {"ana_yemek": 390543, "corba": 10420, "icecek": 243073,
                "salata": 108850, "tatli": 13439}
    assert agent().predict(140)["by_category"] == beklenen


def test_tekrarlanabilir():
    """Ayni hafta iki kez cagrilinca ayni sonucu vermeli."""
    a = agent().predict(138)["by_category"]
    b = agent().predict(138)["by_category"]
    assert a == b


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
