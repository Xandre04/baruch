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
PRIVACY = "privacy/index.html"
MONDI_SLUG = "mondi-illustrati"


def versione(file):
    """Impronta del file: cambia quando il file cambia, così i browser non usano la copia vecchia."""
    return hashlib.md5((SITO / file).read_bytes()).hexdigest()[:8]


CSS = f"assets/css/style.css?v={versione('assets/css/style.css')}"
# caratteri e icone sono nel sito: i visitatori non contattano Google Fonts né altri servizi esterni
FONTS_CSS = f"assets/css/fonts.css?v={versione('assets/css/fonts.css')}"
ICONE_CSS = f"assets/css/icone.css?v={versione('assets/css/icone.css')}"
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
      <p class="footer__legal"><a href="{PRIVACY}">Privacy e cookie</a></p>
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
  <link rel="preload" href="assets/fonts/kalam-400-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{FONTS_CSS}">
  <link rel="stylesheet" href="{ICONE_CSS}">
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
CATERINA_RITRATTO = immagine("/contenuti/media/caterina-santambrogio-02.webp")
CATERINA_BAMBINA = immagine("/contenuti/media/caterina-santambrogio-01.webp")
CATERINA_LAVORO = immagine("/contenuti/media/caterina-santambrogio-03.webp")


def foto(i, alt, cls="", lazy=True):
    c = f' class="{cls}"' if cls else ""
    lz = ' loading="lazy"' if lazy else ""
    return (f'<img{c} src="{i["piccola"]}" srcset="{i["piccola"]} 720w, {i["grande"]} 1400w" sizes="(max-width: 760px) 90vw, 480px" '
            f'alt="{alt}" width="{i["w"]}" height="{i["h"]}"{lz}>')


# ---------------- CHI È BARUCH ----------------
# testo e foto come su illustraremondi.it, nella versione breve scelta da Caterina
page(
    CHI, "chi",
    "Chi è Baruch · Baruch illustrare mondi",
    "Baruch è un invito a guardare il mondo con occhi nuovi: il progetto artistico di Caterina Santambrogio, illustratrice.",
    f"""    <div class="page">
      <section class="about">
        <figure class="about__art reveal">
          <img src="assets/img/chi/baruch-cavallo.webp" alt="Baruch, con i capelli ricci e una matita in mano, cavalca un animale fatto di sassi" width="900" height="840">
        </figure>
        <div class="about__text reveal" style="--d:.1s">
          <h1 class="page-title"><img src="assets/img/ui/titolo-chi.webp" alt="Chi è Baruch" width="453" height="182"></h1>
          <h2 class="about__sub">Progetto artistico Baruch</h2>
          <p>Baruch è un invito a guardare il mondo con occhi nuovi. Nasce da un desiderio di cura e di pace, come un piccolo custode che accompagna tra il visibile e l’immaginario.</p>
          <p>È un progetto aperto, un contenitore di scoperte dove il disegno incontra la materia, la natura si fa trama e le mani danno forma a storie che ancora non esistono.</p>
          <p>Baruch è il mio modo di benedire la curiosità e di trasformare ogni processo creativo in un sentiero da percorrere. Ma è anche il desiderio di collaborazioni costruttive, per mescolare esperienze e competenze differenti.</p>
        </div>
      </section>

      <section class="cate" aria-labelledby="cate-title">
        <div class="cate__photos">
          <figure class="cate__photo reveal">{foto(CATERINA_RITRATTO, "Ritratto in bianco e nero di Caterina Santambrogio con un piccolo Baruch disegnato sulla testa")}</figure>
          <figure class="cate__child reveal" style="--d:.15s">{foto(CATERINA_BAMBINA, "Caterina da bambina, con un piccolo Baruch disegnato tra i capelli")}</figure>
        </div>
        <div class="cate__text reveal" style="--d:.1s">
          <h2 id="cate-title">Caterina Santambrogio</h2>
          <p class="cate__motto">Dietro gli occhi di Baruch ci sono i miei.</p>
          <p>Mi chiamo Caterina e sono un’illustratrice che non ha mai smesso di esplorare la materia.</p>
          <p>Il mio percorso inizia dalla passione per il disegno, che mi ha guidata attraverso gli studi artistici alla scoperta di una verità essenziale: un’immagine non è mai solo colore su carta, ma la narrazione profonda di un pensiero o di un’esperienza. È un modo per abitare la vita.</p>
        </div>
      </section>

      <section class="cate cate--lavoro">
        <div class="cate__text reveal">
          <p>La mia ricerca si muove tra il rigore del disegno dettagliato e la freschezza dell’improvvisazione; spazia dall’immagine naturalistica a quella fiabesca, dalla bidimensionalità della carta alla forma tattile dell’argilla.</p>
          <p>Quando non disegno, conduco laboratori dove invito gli altri a cercare la propria scintilla creativa, perché credo che questo contribuisca a farci sentire persone accese.</p>
        </div>
        <figure class="cate__work reveal" style="--d:.12s">{foto(CATERINA_LAVORO, "Caterina al tavolo di lavoro, china su un disegno tra libri e colori")}</figure>
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
        f"""      <a class="diary-item tile tile--{k} reveal" style="--d:{i * 0.15:.2f}s" href="{url_sezione(k)}">
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
""",
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

# ---------------- PRIVACY E COOKIE ----------------
# Bozza da far verificare a chi segue Caterina per la parte legale.
AGGIORNATA = "6 ottobre 2026"
page(
    PRIVACY, "privacy",
    "Privacy e cookie · Baruch illustrare mondi",
    "Informativa sul trattamento dei dati personali e sui cookie del sito Baruch di Caterina Santambrogio.",
    f"""    <div class="page">
      <article class="legal">
        <h1 class="hand-title hand-title--big">Privacy e cookie</h1>
        <p class="legal__intro">In questa pagina trovi come vengono trattati i tuoi dati quando visiti il sito o mi scrivi, secondo il Regolamento europeo 2016/679 (GDPR) e la normativa italiana. In breve: il sito non usa cookie che ti seguono, non fa statistiche sulle visite e i tuoi dati servono solo a risponderti.</p>

        <h2>Chi tratta i tuoi dati</h2>
        <p>Titolare del trattamento è <strong>Caterina Santambrogio</strong>, Via Chiesa di Rorai 3, Pordenone, partita IVA 01980800930.<br>
        Per qualsiasi domanda sui tuoi dati: <a href="mailto:illustraremondi@gmail.com">illustraremondi@gmail.com</a>, PEC <a href="mailto:caterinasa@pec.it">caterinasa@pec.it</a>.</p>

        <h2>Quali dati</h2>
        <h3>Quando visiti il sito</h3>
        <p>Il server che ospita il sito registra automaticamente alcuni dati tecnici di ogni visita, come l’indirizzo IP, la data e l’ora, la pagina richiesta e il tipo di browser. Servono solo a far funzionare il sito e a proteggerlo da abusi; non vengono usati per identificarti.</p>
        <h3>Quando mi scrivi</h3>
        <p>Se usi il modulo della pagina <a href="{CONTATTI}">Contatti</a> o mi scrivi via email, ricevo il tuo nome, il tuo indirizzo email e quello che scrivi nel messaggio.</p>

        <h2>Perché e su quale base</h2>
        <ul>
          <li><strong>Risponderti</strong> e, se lo chiedi, preparare un preventivo o una collaborazione: è necessario per dar seguito alla tua richiesta (art. 6.1.b GDPR).</li>
          <li><strong>Far funzionare il sito e tenerlo sicuro</strong>: è un legittimo interesse (art. 6.1.f GDPR).</li>
        </ul>
        <p>Non uso i tuoi dati per pubblicità, newsletter o profilazione, e non li vendo né li cedo a nessuno.</p>

        <h2>È obbligatorio darli?</h2>
        <p>No. Ma senza nome e indirizzo email non posso risponderti.</p>

        <h2>Per quanto tempo</h2>
        <p>Conservo i messaggi per il tempo necessario a rispondere e, se nasce una collaborazione, per la sua durata e per gli obblighi fiscali e di legge che ne derivano. I dati tecnici delle visite sono conservati dal fornitore dell’hosting per un periodo limitato, per motivi di sicurezza.</p>

        <h2>Chi altro li vede</h2>
        <p>Solo i fornitori dei servizi che il sito usa, che li trattano per mio conto:</p>
        <ul>
          <li><strong>Keliweb</strong>, che ospita il sito e invia i messaggi del modulo contatti;</li>
          <li><strong>Google</strong> (Gmail), che gestisce la casella email in cui arrivano i messaggi. Google può trattare dati anche negli Stati Uniti, sulla base dell’EU-U.S. Data Privacy Framework e delle clausole contrattuali standard approvate dalla Commissione europea.</li>
        </ul>
        <p>I caratteri e le icone del sito sono ospitati sul sito stesso: visitandolo non comunichi dati a servizi esterni come Google Fonts.</p>

        <h2>Cookie</h2>
        <p>Il sito <strong>non usa cookie</strong>: né di profilazione, né di statistica, né di terze parti. Per questo non ti viene chiesto alcun consenso all’ingresso.</p>
        <p>Se in futuro venissero aggiunti strumenti che usano cookie (per esempio statistiche sulle visite o video incorporati), questa pagina verrà aggiornata e, quando serve, ti verrà chiesto il consenso prima di attivarli.</p>
        <p>L’area riservata all’aggiornamento del sito (<code>/admin</code>), usata solo da chi gestisce il sito, salva nel browser i dati necessari ad accedere.</p>

        <h2>I tuoi diritti</h2>
        <p>In qualsiasi momento puoi chiedere di accedere ai tuoi dati, correggerli, cancellarli, limitarne l’uso, opporti al trattamento o riceverli in un formato leggibile (articoli 15–22 del GDPR). Basta scrivere a <a href="mailto:illustraremondi@gmail.com">illustraremondi@gmail.com</a>.</p>
        <p>Se ritieni che i tuoi dati siano trattati in modo non corretto, puoi presentare reclamo al <a href="https://www.garanteprivacy.it" target="_blank" rel="noopener">Garante per la protezione dei dati personali</a>.</p>

        <p class="legal__data">Ultimo aggiornamento: {AGGIORNATA}</p>
      </article>
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
          <p class="form__note">Il messaggio arriva direttamente a Caterina. Leggi come vengono trattati i tuoi dati nell’<a href="privacy/index.html">informativa sulla privacy</a>.</p>
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
    "privacy-cookie-policy": PRIVACY,
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
