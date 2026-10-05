"""Legge i contenuti scritti con l'editor (cartella contenuti/) e prepara le immagini.

- contenuti/articoli/*.json  articoli del Diario (il nome del file è l'indirizzo della pagina)
- contenuti/opere/*.json     progetti su commissione della sezione "I mondi disegnati"
- contenuti/media/           foto caricate: qui vengono convertite nelle due misure del sito
"""
import hashlib
import html
import json
import re
from pathlib import Path

from PIL import Image

RADICE = Path(__file__).parent.parent
CONTENUTI = RADICE / "contenuti"
MEDIA = CONTENUTI / "media"
SITO = RADICE / "sito"
USCITA = SITO / "assets/img/contenuti"   # foto pronte per il sito
MISURE = (720, 1400)

MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
        "agosto", "settembre", "ottobre", "novembre", "dicembre"]


# ---------------- immagini ----------------
_impronte = {}   # nome della foto -> impronta del suo contenuto
_misure = {}


def prepara_immagini():
    """Converte ogni foto di contenuti/media in WebP 720 e 1400 px e rimuove le versioni non più usate.

    Il nome delle versioni contiene un'impronta della foto: se la foto non cambia il file non si rifà
    (niente modifiche inutili nel repository), se cambia il nome cambia e i browser la riscaricano.
    """
    USCITA.mkdir(parents=True, exist_ok=True)
    attese = set()
    for src in sorted(MEDIA.iterdir()):
        if src.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff"):
            continue
        impronta = hashlib.md5(src.read_bytes()).hexdigest()[:8]
        _impronte[src.stem] = impronta
        for w in MISURE:
            out = USCITA / f"{src.stem}-{impronta}-{w}.webp"
            attese.add(out.name)
            if out.exists():
                continue
            with Image.open(src) as im:
                im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
                if im.width > w:
                    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
                im.save(out, "WEBP", quality=82, method=6)
            print("immagine", out.name)
    for out in USCITA.glob("*.webp"):
        if out.name not in attese:
            out.unlink()


def immagine(percorso):
    """Da '/contenuti/media/foto.jpg' alle informazioni per <img>: file nel sito e misure della versione piccola."""
    stem = Path(percorso).stem
    if stem not in _impronte:
        raise FileNotFoundError(f"Foto non trovata in contenuti/media: {percorso}")
    base = f"assets/img/contenuti/{stem}-{_impronte[stem]}"
    if stem not in _misure:
        with Image.open(SITO / f"{base}-720.webp") as im:
            _misure[stem] = im.size
    w, h = _misure[stem]
    return {"piccola": f"{base}-720.webp", "grande": f"{base}-1400.webp", "w": w, "h": h}


def pdf(percorso):
    """'/assets/pdf/x.pdf' -> (percorso nel sito, peso leggibile)."""
    rel = percorso.lstrip("/")
    mb = (SITO / rel).stat().st_size / 1_048_576
    return rel, f"PDF, {mb:.0f} MB" if mb >= 1 else "PDF"


# ---------------- testo Markdown ----------------
IMG_MD = re.compile(r'!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)')


def in_linea(t):
    """Grassetto, corsivo e link; tutto il resto è testo semplice."""
    t = html.escape(t, quote=False)
    link = []   # gli indirizzi dei link restano intatti: niente corsivo dentro un URL

    def tieni(m):
        link.append(m[2])
        return f"[{m[1]}]\x00{len(link) - 1}\x00"

    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", tieni, t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])", r"<em>\1</em>", t)

    def rimetti(m):
        url = link[int(m[2])]
        extra = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        return f'<a href="{url}"{extra}>{m[1]}</a>'

    t = re.sub(r"\[([^\]]+)\]\x00(\d+)\x00", rimetti, t)
    t = re.sub(r"\\([\\`*_{}\[\]()#+\-.!>~|])", r"\1", t)
    t = re.sub(r"(?: {2,}|\\)\n", "<br>", t)
    return t.replace("\n", " ")


def blocchi(md):
    """Markdown dell'editor -> lista di blocchi: ('p'|'h'|'q'|'ul'|'ol', html) oppure ('img', percorso, alt)."""
    out = []
    for blocco in re.split(r"\n\s*\n", (md or "").strip()):
        b = blocco.strip()
        if not b:
            continue
        righe = b.splitlines()
        if all(r.lstrip().startswith(">") for r in righe):
            out.append(("q", in_linea("\n".join(re.sub(r"^\s*>\s?", "", r) for r in righe))))
        elif b.startswith("#"):
            out.append(("h", in_linea(b.lstrip("#").strip())))
        elif all(re.match(r"\s*[-*+]\s", r) for r in righe):
            out.append(("ul", "".join(f"<li>{in_linea(re.sub(r'^\s*[-*+]\s+', '', r))}</li>" for r in righe)))
        elif all(re.match(r"\s*\d+[.)]\s", r) for r in righe):
            out.append(("ol", "".join(f"<li>{in_linea(re.sub(r'^\s*\d+[.)]\s+', '', r))}</li>" for r in righe)))
        else:
            immagini = IMG_MD.findall(b)
            testo = IMG_MD.sub("", b).strip()
            if testo:
                out.append(("p", in_linea(testo)))
            out += [("img", src, alt) for alt, src in immagini]
    return out


# ---------------- lettura dei contenuti ----------------
# campi di testo semplice che finiscono nelle pagine: si proteggono i caratteri speciali (& < > ")
TESTO_SEMPLICE = ("titolo", "titolo_breve", "sottotitolo", "estratto", "categoria", "committente", "tecnica", "pdf_etichetta")


def _leggi(cartella):
    voci = []
    for f in sorted((CONTENUTI / cartella).glob("*.json")):
        dati = json.loads(f.read_text(encoding="utf-8"))
        if dati.get("pubblicato", True):
            dati["slug"] = f.stem
            for k in TESTO_SEMPLICE:
                if isinstance(dati.get(k), str):
                    dati[k] = html.escape(dati[k])
            voci.append(dati)
    return voci


def articoli():
    voci = _leggi("articoli")
    for a in voci:
        a["data"] = str(a["data"])[:10]
        anno, mese, giorno = a["data"].split("-")
        a["data_it"] = f"{int(giorno)} {MESI[int(mese) - 1]} {anno}"
    return sorted(voci, key=lambda a: a["data"], reverse=True)


def opere():
    return sorted(_leggi("opere"), key=lambda o: (o.get("ordine") or 999, o["titolo"]))
