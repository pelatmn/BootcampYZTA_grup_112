"""WasteZero AI — ortak sabitler.

Tum agent'lar ciktilarini bu bes ortak kategori uzerinden uretir.
Sinyal sozlesmesi: "yuksek" | "normal" | "dusuk" | "veri_yok"
("veri_yok" yalnizca ilgili kategoride hic veri olmadiginda kullanilir).
"""

KATEGORILER = ["corba", "ana_yemek", "salata", "tatli", "icecek"]

SINYAL_YUKSEK = "yuksek"
SINYAL_NORMAL = "normal"
SINYAL_DUSUK = "dusuk"
SINYAL_VERI_YOK = "veri_yok"