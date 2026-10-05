"""Genera le pagine HTML del sito Baruch nella cartella sito/.

Intestazione, menu e piè di pagina sono definiti una sola volta qui sotto.
Dopo una modifica, dalla cartella principale del progetto:  python sorgenti/build.py
"""
import hashlib
import html
import re
from pathlib import Path

from contenuti import (IMG_MD, accogli_caricamenti, articoli, blocchi, collaborazioni, immagine, in_linea,
                       opere, pdf, prepara_immagini)
from diario import SEZIONI

SORGENTI = Path(__file__).parent
SITO = SORGENTI.parent / "sito"    # cartella pubblicata

# indirizzi delle pagine, sempre relativi alla radice del sito
HOME, CHI, DIARIO = "index.html", "chi-e-baruch/index.html", "diario/index.html"
COLLAB, SHOP, CONTATTI = "collaborazioni/index.html", "shop/index.html", "contatti/index.html"
MONDI_SLUG = "mondi-illustrati"


def versione(file):
    """Impronta del file: cambia quando il file cambia, così i browser non usano la copia vecchia."""
    return hashlib.md5((SITO / file).read_bytes()).hexdigest()[:8]


CSS = f"assets/css/style.css?v={versione('assets/css/style.css')}"
JS = f"assets/js/main.js?v={versione('assets/js/main.js')}"


def url_sezione(slug):
    return f"diario/{slug}/index.html"


def url_articolo(a):
    return f"diario/{a['sezione']}/{a['slug']}.html"


def url_opera(o):
    return f"diario/{MONDI_SLUG}/{o['slug']}.html"


NAV = [
    (HOME, "home", "Home"),
    (CHI, "chi", "Chi è Baruch"),
    (DIARIO, "diario", "Diario"),
    (COLLAB, "collaborazioni", "Collaborazioni"),
    (SHOP, "shop", "Shop"),
    (CONTATTI, "contatti", "Contatti"),
]

# icone disegnate a pastello; larghezza in proporzione al disegno originale
SOCIAL_LINK = [
    ("instagram", "Instagram", "https://www.instagram.com/baruch.it/", 186, 148),
    ("linkedin", "LinkedIn", "https://www.linkedin.com/in/caterina-santambrogio-6793813b/", 125, 119),
    ("facebook", "Facebook", "https://www.facebook.com/caterina.santambrogio.12", 125, 163),
]
SOCIAL = '<ul class="social">\n' + "\n".join(
    f'        <li><a href="{u}" target="_blank" rel="noopener" aria-label="{t}"><img src="assets/img/ui/social-{k}.webp" alt="" width="{w}" height="{h}" style="--w:{w}"></a></li>'
    for k, t, u, w, h in SOCIAL_LINK
) + "\n      </ul>"


def cur(key, page):
    return ' aria-current="page"' if key == page else ""


def header(page):
    strip = "\n".join(
        f'        <li class="n-{k}"><a href="{h}"{cur(k, page)}><img src="assets/img/ui/nav-{k}.webp" alt="{t}"></a></li>'
        for h, k, t in NAV
    )
    mobile = "\n".join(
        f'        <li><a href="{h}"{cur(k, page)}><img src="assets/img/ui/nav-{k}.webp" alt="{t}"></a></li>'
        for h, k, t in NAV
    )
    return f"""<a class="skip" href="#contenuto">Vai al contenuto</a>
  <header class="site-nav">
    <nav class="site-nav__inner" aria-label="Principale">
      <ul class="strip">
{strip}
      </ul>
      {SOCIAL}
      <a class="nav-home-mobile" href="index.html"><img src="assets/img/ui/title.webp" alt="Baruch, torna alla home" width="627" height="187"></a>
      <button class="menu-toggle" type="button" data-menu-open aria-expanded="false" aria-controls="mobile-menu" aria-label="Apri il menu"><i class="ph-bold ph-list" aria-hidden="true"></i></button>
    </nav>
  </header>
  <div class="mobile-menu" id="mobile-menu" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="mobile-menu__top">
      <a class="nav-home-mobile" href="index.html"><img src="assets/img/ui/title.webp" alt="Baruch, torna alla home" width="627" height="187"></a>
      <button class="menu-toggle" type="button" data-menu-close aria-label="Chiudi il menu"><i class="ph-bold ph-x" aria-hidden="true"></i></button>
    </div>
    <ul>
{mobile}
    </ul>
    {SOCIAL}
  </div>"""


SCRIVIMI = f"""<a class="scrivimi reveal" href="{CONTATTI}">
        <img class="scrivimi__pianta" src="assets/img/ui/pianta.webp" alt="" width="500" height="794" loading="lazy">
        <img class="scrivimi__stain" src="assets/img/ui/pennellata-pesca.webp" alt="" width="700" height="316" loading="lazy">
        <img class="scrivimi__baruch" src="assets/img/ui/baruch-lettera.webp" alt="" width="360" height="507" loading="lazy">
        <span class="scrivimi__text">Scrivimi<br>un messaggio</span>
      </a>"""


def footer(with_scrivimi=True):
    sc = f'\n    <div class="footer__scrivimi">\n      {SCRIVIMI}\n    </div>' if with_scrivimi else ""
    return f"""<footer class="footer">{sc}
    <div class="footer__grid">
      <a class="to-top" href="#top" aria-label="Torna su"><img src="assets/img/ui/bottone-freccia.webp" alt="" width="254" height="550" loading="lazy"></a>
      <p class="footer__line">
        <span>Caterina Santambrogio</span><i class="sep"> - </i><span>Via Chiesa di Rorai 3 Pordenone</span><i class="sep"> - </i><span>cell. <a href="tel:+393404742250">3404742250</a></span><i class="sep"> - </i><span>P.I. 01980800930</span>
      </p>
    </div>
  </footer>"""


LIGHTBOX = """<dialog class="lightbox" id="lightbox" aria-label="Immagine ingrandita"{single}>
    <div class="lightbox__bar"><button class="icon-btn" type="button" data-close aria-label="Chiudi"><i class="ph-bold ph-x" aria-hidden="true"></i></button></div>
    <div class="lightbox__stage">
      <button class="icon-btn lightbox__prev" type="button" aria-label="Immagine precedente"><i class="ph-bold ph-arrow-left" aria-hidden="true"></i></button>
      <img alt="">
      <button class="icon-btn lightbox__next" type="button" aria-label="Immagine successiva"><i class="ph-bold ph-arrow-right" aria-hidden="true"></i></button>
    </div>
    <p class="lightbox__caption" aria-live="polite"></p>
  </dialog>"""


def page(file, key, title, desc, main, footer_scrivimi=True, extra="", preload=""):
    html = f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#fefdfb">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="assets/img/ui/hero-1100.webp">
  <link rel="icon" href="assets/img/ui/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400&family=Barlow+Semi+Condensed:wght@400;500&family=Kalam:wght@400&display=swap">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.1/src/bold/style.css">
  <link rel="stylesheet" href="{CSS}">{preload}
</head>
<body id="top">
  {header(key)}
  <main id="contenuto">
{main}
  </main>
  {footer(footer_scrivimi)}{extra}
  <script src="{JS}" defer></script>
</body>
</html>
"""
    up = "../" * file.count("/")
    if up:
        # i percorsi sono scritti dalla radice del sito: nelle sottocartelle risalgono
        local = r"(?![a-z][a-z0-9+.-]*:|#|/|\.\./)"
        html = re.sub(r'((?:href|src|data-full|action)=")' + local, r"\1" + up, html)
        html = re.sub(r'((?:srcset|imagesrcset)="|, )(?=assets/)', r"\1" + up, html)
    (SITO / file).parent.mkdir(parents=True, exist_ok=True)
    (SITO / file).write_text(html, encoding="utf-8", newline="\n")
    print("scritto", file)


for f in accogli_caricamenti():
    print("foto caricate in blocco spostate nell'elenco:", f.name)
prepara_immagini()
CATERINA_BAMBINA = immagine("/contenuti/media/caterina-santambrogio-01.webp")

# ---------------- CHI È BARUCH ----------------
page(
    CHI, "chi",
    "Chi è Baruch · Baruch illustrare mondi",
    "Baruch è un personaggio e un progetto: un mondo di natura e meraviglia disegnato da Caterina Santambrogio.",
    f"""    <div class="page">
      <section class="about">
        <figure class="about__art reveal">
          <img src="assets/img/chi/baruch-cavallo.webp" alt="Baruch, con i capelli ricci e una matita in mano, cavalca un animale fatto di sassi" width="900" height="840">
        </figure>
        <div class="about__text reveal" style="--d:.1s">
          <h1 class="page-title"><img src="assets/img/ui/titolo-chi.webp" alt="Chi è Baruch" width="453" height="182"></h1>
          <p>Baruch è un personaggio ma anche un progetto che racchiude in sé il desiderio di creare attraverso il disegno un mondo di natura e meraviglia. Un universo visivo pensato per ispirare la curiosità e la creatività nei bambini, con un interesse trasversale che coinvolge anche gli adulti.</p>
          <p>L’immaginazione è una risorsa preziosa e Baruch offre l’opportunità di connettersi con sensibilità ai valori della natura, della bellezza e dell’apprendimento esperienziale.</p>
          <p>Il progetto si articola in diverse proposte, dall’offerta di immagini originali e pattern esclusivi perfetti per decorare oggetti di uso quotidiano, alla creazione di contenuti illustrati che stimolano la fantasia e la consapevolezza del mondo che ci circonda. Propone inoltre diversi laboratori creativi per sostenere e stimolare l’osservazione e la manualità.</p>
          <p>È un progetto aperto, un contenitore di scoperte dove il disegno incontra la materia, la natura si fa trama e le mani danno forma a storie che ancora non esistono. Ma è anche il desiderio di collaborazioni costruttive, per mescolare esperienze e competenze differenti.</p>
        </div>
      </section>

      <blockquote class="art-quote art-quote--wide reveal"><p>Baruch nasce da un desiderio di cura e di pace, come un piccolo custode che accompagna tra il visibile e l’immaginario. È il mio modo di benedire la curiosità.</p></blockquote>

      <section class="cate" aria-labelledby="cate-title">
        <div class="cate__text reveal">
          <h2 id="cate-title">Dietro gli occhi di Baruch ci sono i miei.</h2>
          <p>Mi chiamo Caterina e sono un’illustratrice che non ha mai smesso di esplorare la materia.</p>
          <p>Il mio percorso inizia dalla passione per il disegno, che mi ha guidata attraverso gli studi artistici alla scoperta di una verità essenziale: un’immagine non è mai solo colore su carta, ma la narrazione profonda di un pensiero o di un’esperienza. È un modo per abitare la vita.</p>
          <p>La mia ricerca si muove tra il rigore del disegno dettagliato e la freschezza dell’improvvisazione; spazia dall’immagine naturalistica a quella fiabesca, dalla bidimensionalità della carta alla forma tattile dell’argilla. Quando non disegno, conduco laboratori dove invito gli altri a cercare la propria scintilla creativa, perché credo che questo contribuisca a farci sentire persone accese.</p>
          <h3>Il percorso</h3>
          <p>Caterina Santambrogio, illustratrice, decoratrice e atelierista. Nata nel 1972, ha conseguito il diploma presso l’Istituto d’Arte con indirizzo grafica e fotografia. Ha frequentato l’Accademia di Belle Arti di Venezia e diversi corsi di illustrazione presso la Scuola Internazionale di Grafica e la Scuola di Illustrazione di Sarmede.</p>
          <p>Lavora freelance come illustratrice e propone laboratori creativi per piccoli e grandi.</p>
        </div>
        <div class="cate__photos">
          <figure class="cate__photo reveal" style="--d:.12s">
            <img src="assets/img/chi/caterina.webp" alt="Ritratto in bianco e nero di Caterina Santambrogio con un piccolo Baruch disegnato sulla testa" width="524" height="665" loading="lazy">
          </figure>
          <figure class="cate__child reveal" style="--d:.24s">
            <img src="{CATERINA_BAMBINA['piccola']}" alt="Caterina da bambina, con un piccolo Baruch disegnato tra i capelli" width="720" height="720" loading="lazy">
          </figure>
        </div>
      </section>
    </div>""",
)

# ---------------- DIARIO ----------------
SEZ = {s["slug"]: s for s in SEZIONI}
ART = articoli()
OPERE = opere()

# le pagine del diario si rigenerano da zero: un articolo cancellato o rinominato non resta online
for vecchia in (SITO / "diario").rglob("*.html"):
    vecchia.unlink()
for cartella in sorted((SITO / "diario").glob("*/"), reverse=True):
    if cartella.is_dir() and not any(cartella.iterdir()):
        cartella.rmdir()


def pic(percorso, alt, lazy=True, sizes="(max-width: 760px) 100vw, 720px"):
    i = immagine(percorso)
    lz = ' loading="lazy"' if lazy else ""
    return (f'<img src="{i["piccola"]}" srcset="{i["piccola"]} 720w, {i["grande"]} 1400w" '
            f'sizes="{sizes}" alt="{html.escape(alt)}" width="{i["w"]}" height="{i["h"]}"{lz}>')


def entries(arts, heading_tag="h3"):
    """Le pagine del taccuino: foto appoggiata sul foglio, data e titolo scritti a mano."""
    out = []
    for i, a in enumerate(arts):
        s = SEZ[a["sezione"]]
        out.append(f"""        <article class="entry reveal" style="--d:{(i % 2) * 0.1:.1f}s" data-sezione="{a['sezione']}">
          <a class="entry__link" href="{url_articolo(a)}">
            <span class="entry__photo">{pic(a['copertina'], a['copertina_alt'], sizes="(max-width: 760px) 100vw, 560px")}</span>
            <span class="entry__meta"><time datetime="{a['data']}">{a['data_it']}</time> <span class="entry__sez">{s['titolo']}</span></span>
            <{heading_tag} class="entry__title">{a['titolo']}</{heading_tag}>
            <span class="entry__text">{a['estratto']}</span>
            <span class="entry__more">Leggi la pagina <i class="ph-bold ph-arrow-right" aria-hidden="true"></i></span>
          </a>
        </article>""")
    return "\n".join(out)


def testo(md):
    """Testo scritto nell'editor -> HTML; immagini consecutive diventano una griglia ingrandibile."""
    out, run = [], []

    def flush():
        if not run:
            return
        one = len(run) == 1
        cls = "art-figs art-figs--one" if one else "art-figs"
        figs = "\n".join(
            f'          <button class="art-fig" type="button" data-full="{immagine(src)["grande"]}" data-title="">{pic(src, alt, sizes="(max-width: 760px) 100vw, " + ("820px" if one else "420px"))}</button>'
            for src, alt in run
        )
        out.append(f'        <div class="{cls} reveal">\n{figs}\n        </div>')
        run.clear()

    for b in blocchi(md):
        if b[0] == "img":
            run.append((b[1], b[2]))
            continue
        flush()
        if b[0] == "p":
            out.append(f"        <p>{b[1]}</p>")
        elif b[0] == "h":
            out.append(f"        <h2>{b[1]}</h2>")
        elif b[0] == "q":
            out.append(f'        <blockquote class="art-quote reveal"><p>{b[1]}</p></blockquote>')
        else:
            out.append(f"        <{b[0]}>{b[1]}</{b[0]}>")
    flush()
    return "\n".join(out)


def sez_drawing(s, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="assets/img/diario/{s["disegno"]}.webp" alt="{s["alt"]}" width="{s["w"]}" height="{s["h"]}">'


# i cinque disegni delle sezioni, in griglia sotto la home:
# a sinistra due righe da due, a destra il ramo di fiori alto quanto le due righe
GRIGLIA = ["mondi-illustrati", "le-avventure-di-baruch", "come-fiori-selvatici",
           "costruire-con-baruch", "le-cose-magiche-di-baruch"]


def griglia_sezioni():
    tiles = "\n".join(
        f"""      <a class="diary-item tile tile--{k} reveal" style="--d:{i * 0.08:.2f}s" href="{url_sezione(k)}">
        <span class="tile__art">{sez_drawing(SEZ[k])}</span>
        <span class="diary-item__label">{SEZ[k]['titolo']}</span>
      </a>"""
        for i, k in enumerate(GRIGLIA)
    )
    return f"""
    <nav class="home-sezioni" aria-label="Le sezioni del diario">
{tiles}
    </nav>
"""


# indice del diario: le pagine più recenti, con un filtro per sezione
sezioni_con_pagine = [s for s in SEZIONI if any(a["sezione"] == s["slug"] for a in ART)]
filtro = "\n".join(
    [f'        <a class="chip" href="{DIARIO}" data-sez="tutte" aria-current="true">Tutte</a>']
    + [f'        <a class="chip" href="{url_sezione(s["slug"])}" data-sez="{s["slug"]}">{s["titolo"]}</a>' for s in sezioni_con_pagine]
)
page(
    DIARIO, "diario",
    "Diario · Baruch illustrare mondi",
    "Il diario di Baruch: mondi illustrati, fiori selvatici, avventure, cose magiche e laboratori da costruire insieme.",
    f"""    <div class="page">
      <h1 class="page-title reveal"><img src="assets/img/ui/titolo-diario.webp" alt="Diario" width="371" height="201"></h1>
      <nav class="filtro reveal" aria-label="Filtra per sezione" data-filtro>
{filtro}
      </nav>
      <div class="entries" data-voci>
{entries(ART)}
      </div>
      <p class="filtro__vuoto" hidden>Nessuna pagina in questa sezione, per ora.</p>
    </div>""",
)

# ---------------- HOME ----------------
page(
    HOME, "home",
    "Baruch · illustrare mondi",
    "Baruch è il progetto di Caterina Santambrogio, illustratrice: immagini, pattern e laboratori creativi ispirati alla natura.",
    """    <section class="hero" aria-label="Baruch, illustrare mondi">
      <img class="hero__art" src="assets/img/ui/hero.webp" srcset="assets/img/ui/hero-1100.webp 1100w, assets/img/ui/hero.webp 2200w" sizes="100vw"
        alt="Un bambino dipinto sorride tra grandi foglie verdi e fiori, abbracciando una foglia" width="2200" height="1080" fetchpriority="high">
      <h1 class="hero__title">
        <img class="hero__bg" src="assets/img/ui/title-bg.webp" alt="" width="883" height="277">
        <img class="hero__word" src="assets/img/ui/title.webp" alt="Baruch" width="627" height="187">
        <img class="hero__sub" src="assets/img/ui/subtitle.webp" alt="illustrare mondi" width="812" height="181">
      </h1>
    </section>
""" + griglia_sezioni() + """
    <section class="home-notes">
      """ + SCRIVIMI + """
      <p class="progetto reveal" style="--d:.12s">Progetto di<br>Caterina Santambrogio<br>Illustratrice</p>
    </section>""",
    footer_scrivimi=False,
    preload='\n  <link rel="preload" as="image" href="assets/img/ui/hero.webp" imagesrcset="assets/img/ui/hero-1100.webp 1100w, assets/img/ui/hero.webp 2200w" imagesizes="100vw">',
)

# pagine delle sezioni
for s in SEZIONI:
    arts = [a for a in ART if a["sezione"] == s["slug"]]
    intro = "\n".join(f"          <p>{p}</p>" for p in s["intro"])
    body = ""
    if arts:
        body = f"""      <div class="entries">
{entries(arts, "h2")}
      </div>"""
    if s["slug"] == MONDI_SLUG:
        cells = "\n".join(
            f"""        <a class="work reveal" href="{url_opera(o)}">
          <span class="work__img">{pic(o['copertina'], o['copertina_alt'], sizes="(max-width: 760px) 100vw, 600px")}</span>
          <span class="work__cat">{o['categoria']}</span>
          <span class="work__title">{o['titolo']}</span>
          <span class="work__tec">{o['tecnica']}</span>
          <span class="entry__more">Scopri il progetto <i class="ph-bold ph-arrow-right" aria-hidden="true"></i></span>
        </a>"""
            for o in OPERE
        )
        body += f"""      <div class="works">
{cells}
      </div>
      <p class="more-link reveal"><a class="cta" href="{COLLAB}">Tutte le collaborazioni</a></p>"""
    if "gruppi" in s:
        for gt, objs in s["gruppi"]:
            cells = "\n".join(
                f'          <button class="art-fig obj" type="button" data-full="{immagine(foto)["grande"]}" data-title="{gt}">{pic(foto, alt, sizes="(max-width: 760px) 100vw, 380px")}</button>'
                for foto, alt in objs
            )
            body += f"""
      <section class="objects reveal">
        <h2 class="hand-title">{gt}</h2>
        <div class="objects__row">
{cells}
        </div>
      </section>"""
        body += f"""
      <p class="more-link reveal"><a class="cta" href="{CONTATTI}">Scrivimi un messaggio</a></p>"""
    page(
        url_sezione(s["slug"]), "diario",
        f"{s['titolo']} · Diario di Baruch",
        s["intro"][0][:155],
        f"""    <div class="page">
      <a class="back reveal" href="{DIARIO}"><i class="ph-bold ph-arrow-left" aria-hidden="true"></i> Diario</a>
      <header class="sez-head">
        <div class="sez-head__art reveal">{sez_drawing(s)}</div>
        <div class="sez-head__text reveal" style="--d:.1s">
          <h1 class="hand-title hand-title--big">{s['titolo']}</h1>
{intro}
        </div>
      </header>
{body}
    </div>""",
        extra=("\n  " + LIGHTBOX.format(single="")) if "gruppi" in s else "",
    )

# pagine delle opere su commissione
MONDI = SEZ[MONDI_SLUG]
for i, o in enumerate(OPERE):
    breve = o.get("titolo_breve") or o["titolo"]
    quote = f'\n        <blockquote class="art-quote reveal"><p>{in_linea(o["citazione"])}</p></blockquote>' if o.get("citazione") else ""
    pdf_html = ""
    if o.get("pdf"):
        url, peso = pdf(o["pdf"])
        label = o.get("pdf_etichetta") or "Sfoglia il PDF"
        pdf_html = f'\n        <p class="opera__pdf reveal"><a class="cta" href="{url}" target="_blank" rel="noopener" type="application/pdf">{label} <i class="ph-bold ph-book-open" aria-hidden="true"></i></a><small>{peso}</small></p>'
    tavole = "\n".join(
        f'          <button class="art-fig plate{" plate--wide" if immagine(t["immagine"])["w"] > 2 * immagine(t["immagine"])["h"] else ""}" type="button" data-full="{immagine(t["immagine"])["grande"]}" data-title="{breve}">{pic(t["immagine"], t.get("alt", ""), sizes="(max-width: 760px) 50vw, 400px")}</button>'
        for t in o.get("tavole") or []
    )
    tavole_html = f"""
      <section class="opera__plates" aria-labelledby="tavole">
        <h2 class="hand-title reveal" id="tavole">Le tavole</h2>
        <div class="plates reveal">
{tavole}
        </div>
      </section>""" if tavole else ""
    prev_o, next_o = OPERE[i - 1], OPERE[(i + 1) % len(OPERE)]
    sub = f'\n        <p class="article__sub">{o["sottotitolo"]}</p>' if o.get("sottotitolo") else ""
    facts = "\n".join(
        f"            <div><dt>{dt}</dt><dd>{dd}</dd></div>"
        for dt, dd in (("Committente", o.get("committente")), ("Tecnica", (o.get("tecnica") or "").replace("Tecnica mista: ", "mista, ")))
        if dd
    )
    page(
        url_opera(o), "diario",
        f"{breve} · Mondi illustrati",
        html.escape(re.sub(r"\s+", " ", IMG_MD.sub("", o.get("testo") or o["titolo"]).strip().split("\n\n")[0])[:155]),
        f"""    <article class="article opera">
      <a class="back reveal" href="{url_sezione(MONDI_SLUG)}">{sez_drawing(MONDI, "back__art")} {MONDI['titolo']}</a>
      <header class="article__head reveal">
        <p class="article__date">{o.get('categoria', '')}</p>
        <h1 class="hand-title hand-title--big">{o['titolo']}</h1>{sub}
      </header>
      <div class="opera__intro">
        <figure class="opera__cover reveal">
          <button class="art-fig" type="button" data-full="{immagine(o['copertina'])['grande']}" data-title="{breve}">{pic(o['copertina'], o['copertina_alt'], lazy=False, sizes="(max-width: 760px) 100vw, 520px")}</button>
        </figure>
        <div class="opera__text reveal" style="--d:.1s">
          <dl class="opera__facts">
{facts}
          </dl>
{testo(o.get('testo'))}{pdf_html}
        </div>
      </div>{quote}{tavole_html}
      <nav class="opera__nav reveal" aria-label="Altri progetti">
        <a href="{url_opera(prev_o)}"><i class="ph-bold ph-arrow-left" aria-hidden="true"></i> {prev_o.get('titolo_breve') or prev_o['titolo']}</a>
        <a href="{url_opera(next_o)}">{next_o.get('titolo_breve') or next_o['titolo']} <i class="ph-bold ph-arrow-right" aria-hidden="true"></i></a>
      </nav>
    </article>""",
        extra="\n  " + LIGHTBOX.format(single=""),
    )

def galleria_articolo(a):
    """Foto caricate insieme nel campo "Galleria in fondo alla pagina": griglia ingrandibile sotto il testo."""
    foto = [f for f in (a.get("galleria") or []) if f]
    if not foto:
        return ""
    figs = []
    for n, f in enumerate(foto, 1):
        img = pic(f, a["titolo"] + ", foto " + str(n), sizes="(max-width: 760px) 100vw, 420px")
        figs.append(f'          <button class="art-fig" type="button" data-full="{immagine(f)["grande"]}" data-title="">{img}</button>')
    return '\n        <div class="art-figs art-figs--galleria reveal">\n' + "\n".join(figs) + "\n        </div>"


# pagine degli articoli
for a in ART:
    s = SEZ[a["sezione"]]
    altri = [x for x in ART if x["sezione"] == a["sezione"] and x is not a][:2]
    if len(altri) < 2:
        altri += [x for x in ART if x["sezione"] != a["sezione"]][: 2 - len(altri)]
    sub = f'\n        <p class="article__sub">{a["sottotitolo"]}</p>' if a.get("sottotitolo") else ""
    page(
        url_articolo(a), "diario",
        f"{a['titolo']} · Diario di Baruch",
        a["estratto"],
        f"""    <article class="article">
      <a class="back reveal" href="{url_sezione(s['slug'])}">{sez_drawing(s, "back__art")} {s['titolo']}</a>
      <header class="article__head reveal">
        <p class="article__date"><time datetime="{a['data']}">{a['data_it']}</time></p>
        <h1 class="hand-title hand-title--big">{a['titolo']}</h1>{sub}
      </header>
      <figure class="article__cover reveal">{pic(a['copertina'], a['copertina_alt'], lazy=False, sizes="(max-width: 1040px) 100vw, 1000px")}</figure>
      <div class="article__body">
{testo(a['testo'])}{galleria_articolo(a)}
        <p class="article__sign">Caterina</p>
      </div>
    </article>
    <section class="page journal journal--more" aria-labelledby="altre">
      <h2 class="hand-title reveal" id="altre">Altre pagine del diario</h2>
      <div class="entries">
{entries(altri)}
      </div>
    </section>""",
        extra="\n  " + LIGHTBOX.format(single=""),
    )

# ---------------- COLLABORAZIONI ----------------
# l'elenco si modifica dall'editor (contenuti/collaborazioni.json)
cells = []
for v in collaborazioni():
    i = immagine(v["immagine"])
    alt = v["descrizione"] or v["titolo"] or "Illustrazione di Caterina Santambrogio"
    cut = ' class="is-cutout"' if i["trasparente"] else ""
    cells.append(
        f"""        <button class="gallery__item reveal" type="button" data-full="{i['grande']}" data-title="{v['titolo']}" data-note="{v['nota']}">
          <img{cut} src="{i['piccola']}" alt="{alt}" width="{i['w']}" height="{i['h']}" loading="lazy">
        </button>"""
    )
page(
    COLLAB, "collaborazioni",
    "Collaborazioni · Baruch illustrare mondi",
    "Illustrazioni, copertine, mappe e oggetti dipinti da Caterina Santambrogio per editori, scuole e committenti.",
    f"""    <div class="page">
      <h1 class="page-title page-title--wide reveal"><img src="assets/img/ui/titolo-collaborazioni.webp" alt="Collaborazioni" width="685" height="231"></h1>
      <div class="gallery">
{chr(10).join(cells)}
      </div>
    </div>""",
    extra="\n  " + LIGHTBOX.format(single=""),
)

# ---------------- SHOP ----------------
OGGETTI_SHOP = [
    ("o-sedia", "19-sedia", "Una sedia di legno decorata con case e alberi"),
    ("o-ciondoli", "15-ciondoli", "Ciondoli in ceramica dipinti con volti e foglie blu"),
    ("o-teiera", "img-6431", "Una teiera in ceramica con un uccellino sul coperchio"),
    ("o-fragole", "img-6334", "Quattro fragole dipinte, due con un volto"),
]
oggetti_shop = "\n".join(
    f'          <figure class="{cls} reveal" style="--d:{(n + 1) * .08:.2f}s"><img src="{i["piccola"]}" alt="{alt}" width="{i["w"]}" height="{i["h"]}" loading="lazy"></figure>'
    for n, (cls, nome, alt) in enumerate(OGGETTI_SHOP)
    for i in [immagine(f"/contenuti/media/{nome}.webp")]
)
page(
    SHOP, "shop",
    "Shop · Baruch illustrare mondi",
    "Stampe, pattern e oggetti dipinti a mano da Baruch. Lo shop è in preparazione.",
    f"""    <div class="page">
      <section class="shop">
        <div class="shop__text reveal">
          <h1 class="page-title"><img src="assets/img/ui/titolo-shop.webp" alt="Shop" width="349" height="171"></h1>
          <p class="lead-hand">Lo shop di Baruch sta prendendo forma.</p>
          <p>Presto qui troverai stampe, pattern esclusivi e oggetti di uso quotidiano decorati a mano. Se desideri un’illustrazione o un oggetto su misura, scrivimi: ne parliamo insieme.</p>
          <a class="cta" href="{CONTATTI}">Scrivimi un messaggio</a>
        </div>
        <div class="shop__objects">
{oggetti_shop}
        </div>
      </section>
    </div>""",
)

# ---------------- CONTATTI ----------------
page(
    CONTATTI, "contatti",
    "Contatti · Baruch illustrare mondi",
    "Scrivi a Caterina Santambrogio per illustrazioni, laboratori creativi e collaborazioni.",
    """    <div class="page">
      <h1 class="page-title reveal"><img src="assets/img/ui/titolo-contatti.webp" alt="Contatti" width="570" height="214"></h1>
      <section class="contact">
        <form class="form reveal" id="contact-form" action="contatti/invia.php" method="post" novalidate>
          <p class="lead-hand">Per illustrazioni, laboratori o una semplice domanda.</p>
          <div class="field">
            <label for="nome">Nome</label>
            <input id="nome" name="nome" type="text" autocomplete="name" required aria-describedby="nome-error">
            <p class="error" id="nome-error" aria-live="polite"></p>
          </div>
          <div class="field">
            <label for="email">Email</label>
            <input id="email" name="email" type="email" autocomplete="email" required aria-describedby="email-help email-error">
            <p class="help" id="email-help">Serve solo per risponderti.</p>
            <p class="error" id="email-error" aria-live="polite"></p>
          </div>
          <div class="field">
            <label for="messaggio">Messaggio</label>
            <textarea id="messaggio" name="messaggio" required aria-describedby="messaggio-error"></textarea>
            <p class="error" id="messaggio-error" aria-live="polite"></p>
          </div>
          <p class="form__trap" aria-hidden="true"><label>Lascia vuoto <input name="sito" tabindex="-1" autocomplete="off"></label></p>
          <button class="cta" type="submit">Invia il messaggio</button>
          <p class="form__note">Il messaggio arriva direttamente a Caterina.</p>
          <p class="form__status" role="status"></p>
        </form>
        <div class="contact__info reveal" style="--d:.12s">
          <address>
            Caterina Santambrogio<br>
            Via Chiesa di Rorai 3<br>
            Pordenone<br>
            cell. <a href="tel:+393404742250">340 474 2250</a><br>
            P.I. 01980800930<br>
            <a href="mailto:illustraremondi@gmail.com">illustraremondi@gmail.com</a><br>
            PEC <a href="mailto:caterinasa@pec.it">caterinasa@pec.it</a>
          </address>
          """ + SOCIAL + """
          <img class="contact__baruch" src="assets/img/ui/baruch-lettera.webp" alt="Baruch con una lettera in mano" width="360" height="507" loading="lazy">
        </div>
      </section>
    </div>""",
    footer_scrivimi=False,
)


# ---------------- VECCHI INDIRIZZI DI ILLUSTRAREMONDI.IT ----------------
# Quando il dominio punterà a questo sito, i vecchi link (Google, social, segnalibri)
# arrivano alla pagina nuova con un reindirizzamento permanente (301).
# /chi-e-baruch/, /diario/ e /contatti/ esistono già con lo stesso indirizzo.
# Il file .htaccess funziona su Keliweb (Apache); l'anteprima su GitHub Pages lo ignora.
ART_BY = {a["slug"]: a for a in ART}
OPERA_BY = {o["slug"]: o for o in OPERE}
REDIRECT = {
    "mondi-illustrati": url_sezione(MONDI_SLUG),
    "le-avventure-di-baruch": url_sezione("le-avventure-di-baruch"),
    "come-fiori-selvatici": url_sezione("come-fiori-selvatici"),
    "costruire-con-baruch": url_sezione("costruire-con-baruch"),
    "le-cose-magiche-di-baruch": url_sezione("le-cose-magiche-di-baruch"),
    "solidi": url_articolo(ART_BY["solidi-e-chiaroscuro"]),
    "vegetazione-selvaggia": url_articolo(ART_BY["vegetazione-selvaggia"]),
    "prugno-selvatico": url_articolo(ART_BY["prugno-selvatico"]),
    "il-respiro-del-tagliamento": url_articolo(ART_BY["il-respiro-del-tagliamento"]),
    "disegno-naturalistico-dellalbero-di-giuda": url_articolo(ART_BY["albero-di-giuda"]),
    "rosso-papavero": url_articolo(ART_BY["rosso-papavero"]),
    "caraffa": url_articolo(ART_BY["caraffa"]),
    "dal-segno-al-movimento": url_articolo(ART_BY["dal-segno-al-movimento"]),
    "gita-ai-magredi-dove-la-natura-diventa-seta": url_articolo(ART_BY["gita-ai-magredi"]),
    "portfolio/calendario-illustrato-prove-di-volo": url_opera(OPERA_BY["prove-di-volo"]),
    "portfolio/calendario-illustrato-che-effetto-ti-fa": url_opera(OPERA_BY["che-effetto-ti-fa"]),
    "portfolio/teatro-e-bosco-sotto-gli-alberi": url_opera(OPERA_BY["teatro-sotto-gli-alberi"]),
    "portfolio/yan-e-orso": url_opera(OPERA_BY["yan-e-l-orso"]),
    "portfolio/calendario-vuoi-guarire": url_opera(OPERA_BY["vuoi-guarire"]),
}
righe = "\n".join(f"RedirectMatch 301 ^/{old}/?$ /{new}" for old, new in REDIRECT.items())
(SITO / ".htaccess").write_text(f"""# Generato da sorgenti/build.py: non modificare a mano.
DirectoryIndex index.html
Options -Indexes

# Vecchi indirizzi di illustraremondi.it
{righe}
""", encoding="utf-8", newline="\n")
print("reindirizzamenti in .htaccess:", len(REDIRECT))
