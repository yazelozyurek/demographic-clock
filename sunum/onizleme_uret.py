"""Slaytların yaklaşık görüntüsü (26 Ekim): sunum/onizleme/{cover,question,clock,money,turkiye,references}.png

Çalıştırma (proje klasöründen):  python sunum/onizleme_uret.py
- cover…turkiye: ONIZLEME=1 python sunum/slayt_uret.py ile üretilir (görseller outputs/ klasöründen; kapakta durağan resim).
- references: sunum/slaytlar_kaynak/slides/references.html (üretici bu slaytı yazmıyor).
- Görüntü headless Chrome ile alınır (görünmez çalışır; yazı tipleri için internet gerekir). Yaklaşık görüntüdür:
  Slides programı bazı şeyleri farklı çizer (ör. kutusuna sığmayan kelimeyi ortasından böler, Chrome bölmez).
Ders notları PDF'i (sunum/pdf/pdf_uret.py) bu görüntüleri kullanır; slaytlar değişince önce bu program çalıştırılır.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "sunum/onizleme"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONT = ('<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700'
        '&family=IBM+Plex+Sans:wght@400;600&display=swap" rel="stylesheet">')
CSS = ("*{margin:0;box-sizing:border-box} body{margin:0} section{position:relative;width:1920px;height:1080px;overflow:hidden} "
       "aside{display:none} section > *:not([style*=\"position:absolute\"]){position:relative}")

gecici = Path(tempfile.mkdtemp(prefix="onizleme_"))
try:
    subprocess.run([sys.executable, str(KOK / "sunum/slayt_uret.py"), str(gecici)], check=True,
                   env={**os.environ, "ONIZLEME": "1"})
    shutil.copy(KOK / "sunum/slaytlar_kaynak/slides/references.html", gecici / "references.html")
    for ad in ["cover", "question", "clock", "money", "turkiye", "references"]:
        sayfa = gecici / f"{ad}_sayfa.html"
        sayfa.write_text(f"<!doctype html><html><head><meta charset='utf-8'>{FONT}<style>{CSS}</style></head><body>"
                         + (gecici / f"{ad}.html").read_text(encoding="utf-8") + "</body></html>", encoding="utf-8")
        profil = tempfile.mkdtemp(prefix="onizleme_chrome_")
        try:
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                            f"--user-data-dir={profil}", "--window-size=1920,1080", "--virtual-time-budget=6000",
                            "--force-color-profile=srgb", f"--screenshot={CIKTI / (ad + '.png')}", sayfa.as_uri()],
                           capture_output=True, timeout=180, check=True)
        finally:
            shutil.rmtree(profil, ignore_errors=True)
        print("yazıldı:", (CIKTI / f"{ad}.png").relative_to(KOK))
finally:
    shutil.rmtree(gecici, ignore_errors=True)
