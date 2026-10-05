"""Controlla che ogni link, immagine e PDF delle pagine in sito/ punti a un file esistente.

Uso, dalla cartella principale del progetto:  python sorgenti/controlla.py
"""
import re
import sys
from pathlib import Path

SITO = Path(__file__).parent.parent / "sito"
ESTERNO = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|#|//)")

rotti = 0
pagine = sorted(SITO.rglob("*.html"))
for f in pagine:
    html = f.read_text(encoding="utf-8")
    refs = re.findall(r'(?:href|src|data-full|action)="([^"]+)"', html)
    for ss in re.findall(r'(?:srcset|imagesrcset)="([^"]+)"', html):
        refs += [u.split()[0] for u in ss.split(",")]
    for r in refs:
        if ESTERNO.match(r):
            continue
        target = (f.parent / r.split("#")[0]).resolve()
        if not target.exists():
            rotti += 1
            print(f"{f.relative_to(SITO)} -> {r}")

css = SITO / "assets/css/style.css"
for u in re.findall(r"url\(([^)]+)\)", css.read_text(encoding="utf-8")):
    if not (css.parent / u.strip("'\"")).resolve().exists():
        rotti += 1
        print(f"style.css -> {u}")

print(f"{len(pagine)} pagine controllate, riferimenti rotti: {rotti}")
sys.exit(1 if rotti else 0)
