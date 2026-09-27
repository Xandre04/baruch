"""Genera le pagine HTML del sito Baruch nella cartella sito/.

Intestazione, menu e piè di pagina sono definiti una sola volta qui sotto.
Dopo una modifica, dalla cartella principale del progetto:  python sorgenti/build.py
"""
import json
import re
from pathlib import Path

from diario import ARTICOLI, OPERE, SEZIONI

SORGENTI = Path(__file__).parent
DATI = SORGENTI / "dati"          # misure delle immagini, usate per width/height
SITO = SORGENTI.parent / "sito"    # cartella pubblicata

# indirizzi delle pagine, sempre relativi alla radice del sito
HOME, CHI, DIARIO = "index.html", "chi-e-baruch/index.html", "diario/index.html"
COLLAB, SHOP, CONTATTI = "collaborazioni/index.html", "shop/index.html", "contatti/index.html"
MONDI_SLUG = "i-mondi-disegnati-di-baruch"


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

SOCIAL = """<ul class="social">
        <li><a data-social="instagram" href="#" aria-label="Instagram"><i class="ph-bold ph-instagram-logo" aria-hidden="true"></i></a></li>
        <li><a data-social="linkedin" href="#" aria-label="LinkedIn"><i class="ph-bold ph-linkedin-logo" aria-hidden="true"></i></a></li>
        <li><a data-social="facebook" href="#" aria-label="Facebook"><i class="ph-bold ph-facebook-logo" aria-hidden="true"></i></a></li>
      </ul>"""


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
  <link rel="stylesheet" href="assets/css/style.css">{preload}
</head>
<body id="top">
  {header(key)}
  <main id="contenuto">
{main}
  </main>
  {footer(footer_scrivimi)}{extra}
  <script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    up = "../" * file.count("/")
    if up:
        # i percorsi sono scritti dalla radice del sito: nelle sottocartelle risalgono
        local = r"(?![a-z][a-z0-9+.-]*:|#|/|\.\./)"
        html = re.sub(r'((?:href|src|data-full)=")' + local, r"\1" + up, html)
        html = re.sub(r'((?:srcset|imagesrcset)="|, )(?=assets/)', r"\1" + up, html)
    (SITO / file).parent.mkdir(parents=True, exist_ok=True)
    (SITO / file).write_text(html, encoding="utf-8")
    print("scritto", file)


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

    <section class="home-notes">
      """ + SCRIVIMI + """
      <p class="progetto reveal" style="--d:.12s">Progetto di<br>Caterina Santambrogio<br>Illustratrice</p>
    </section>""",
    footer_scrivimi=False,
    preload='\n  <link rel="preload" as="image" href="assets/img/ui/hero.webp" imagesrcset="assets/img/ui/hero-1100.webp 1100w, assets/img/ui/hero.webp 2200w" imagesizes="100vw">',
)

# ---------------- CHI È BARUCH ----------------
page(
    CHI, "chi",
    "Chi è Baruch · Baruch illustrare mondi",
    "Baruch è un personaggio e un progetto: un mondo di natura e meraviglia disegnato da Caterina Santambrogio.",
    """    <div class="page">
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
            <img src="assets/img/articoli/caterina-santambrogio-01-720.webp" alt="Caterina da bambina, con un piccolo Baruch disegnato tra i capelli" width="720" height="720" loading="lazy">
          </figure>
        </div>
      </section>
    </div>""",
)

# ---------------- DIARIO ----------------
SIZES = {d: json.loads((DATI / f"{d}.json").read_text(encoding="utf-8")) for d in ("articoli", "opere")}
SEZ = {s["slug"]: s for s in SEZIONI}
ART = sorted(ARTICOLI, key=lambda a: a["data"], reverse=True)
OP = {o["cover"]: o for o in OPERE}


def pic(name, alt, cls="", lazy=True, sizes="(max-width: 760px) 100vw, 720px", folder="articoli"):
    w, h = SIZES[folder][name]
    lz = ' loading="lazy"' if lazy else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="assets/img/{folder}/{name}-720.webp" srcset="assets/img/{folder}/{name}-720.webp 720w, assets/img/{folder}/{name}-1400.webp 1400w" '
            f'sizes="{sizes}" alt="{alt}" width="{w}" height="{h}"{lz}>')


def entries(arts, heading_tag="h3"):
    """Le pagine del taccuino: foto appoggiata sul foglio, data e titolo scritti a mano."""
    out = []
    for i, a in enumerate(arts):
        s = SEZ[a["sezione"]]
        img, alt = a["cover"]
        out.append(f"""        <article class="entry reveal" style="--d:{(i % 2) * 0.1:.1f}s">
          <a class="entry__link" href="{url_articolo(a)}">
            <span class="entry__photo">{pic(img, alt, sizes="(max-width: 760px) 100vw, 560px")}</span>
            <span class="entry__meta"><time datetime="{a['data']}">{a['data_it']}</time> <span class="entry__sez">{s['titolo']}</span></span>
            <{heading_tag} class="entry__title">{a['titolo']}</{heading_tag}>
            <span class="entry__text">{a['estratto']}</span>
            <span class="entry__more">Leggi la pagina <i class="ph-bold ph-arrow-right" aria-hidden="true"></i></span>
          </a>
        </article>""")
    return "\n".join(out)


def blocks(bl):
    """Trasforma i blocchi dell'articolo in HTML; immagini consecutive diventano una griglia."""
    html, run = [], []

    def flush():
        if not run:
            return
        one = len(run) == 1
        cls = "art-figs art-figs--one" if one else "art-figs"
        figs = "\n".join(
            f'          <button class="art-fig" type="button" data-full="assets/img/articoli/{n}-1400.webp" data-title="">{pic(n, a, sizes="(max-width: 760px) 100vw, " + ("820px" if one else "420px"))}</button>'
            for n, a in run
        )
        html.append(f'        <div class="{cls} reveal">\n{figs}\n        </div>')
        run.clear()

    for b in bl:
        if b[0] == "img":
            run.append((b[1], b[2]))
            continue
        flush()
        if b[0] == "p":
            html.append(f"        <p>{b[1]}</p>")
        elif b[0] == "h":
            html.append(f"        <h2>{b[1]}</h2>")
        elif b[0] == "q":
            html.append(f'        <blockquote class="art-quote reveal"><p>{b[1]}</p></blockquote>')
    flush()
    return "\n".join(html)


def sez_drawing(s, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="assets/img/diario/{s["disegno"]}.webp" alt="{s["alt"]}" width="{s["w"]}" height="{s["h"]}">'


# indice del diario: i cinque disegni sparsi portano alle sezioni
ORDINE = ["i-mondi-disegnati-di-baruch", "come-fiori-selvatici", "le-avventure-di-baruch", "costruire-con-baruch", "le-cose-magiche-di-baruch"]
items = "\n".join(
    f"""        <a class="diary-item {SEZ[k]['classe']} reveal" style="--d:{i*0.08:.2f}s" href="{url_sezione(k)}">
          {sez_drawing(SEZ[k])}
          <span class="diary-item__label">{SEZ[k]['titolo']}</span>
        </a>"""
    for i, k in enumerate(ORDINE)
)
page(
    DIARIO, "diario",
    "Diario · Baruch illustrare mondi",
    "Il diario di Baruch: mondi disegnati, fiori selvatici, avventure, cose magiche e laboratori da costruire insieme.",
    f"""    <div class="page">
      <h1 class="page-title reveal"><img src="assets/img/ui/titolo-diario.webp" alt="Diario" width="371" height="201"></h1>
      <nav class="diario" aria-label="Sezioni del diario">
{items}
      </nav>
      <section class="journal" aria-labelledby="ultime">
        <h2 class="hand-title reveal" id="ultime">Le ultime pagine</h2>
        <div class="entries">
{entries(ART)}
        </div>
      </section>
    </div>""",
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
    if "opere" in s:
        cells = "\n".join(
            f"""        <a class="work reveal" href="{url_opera(OP[n])}">
          <span class="work__img">{pic(n, alt, sizes="(max-width: 760px) 100vw, 600px")}</span>
          <span class="work__cat">{OP[n]['categoria']}</span>
          <span class="work__title">{t}</span>
          <span class="work__tec">{tec}</span>
          <span class="entry__more">Scopri il progetto <i class="ph-bold ph-arrow-right" aria-hidden="true"></i></span>
        </a>"""
            for n, t, tec, alt in s["opere"]
        )
        body += f"""      <div class="works">
{cells}
      </div>
      <p class="more-link reveal"><a class="cta" href="{COLLAB}">Tutte le collaborazioni</a></p>"""
    if "gruppi" in s:
        for gt, objs in s["gruppi"]:
            cells = "\n".join(
                f'          <button class="art-fig obj" type="button" data-full="{full}" data-title="{gt}"><img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy"></button>'
                for src, full, alt, w, h in objs
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
MONDI = SEZ["i-mondi-disegnati-di-baruch"]
COVER_ALT = {n: alt for n, _, _, alt in MONDI["opere"]}
for i, o in enumerate(OPERE):
    testi = "\n".join(f"        <p>{t}</p>" for t in o["testi"])
    quote = f'\n        <blockquote class="art-quote reveal"><p>{o["citazione"]}</p></blockquote>' if o["citazione"] else ""
    pdf = ""
    if o["pdf"]:
        url, label, peso = o["pdf"]
        pdf = f'\n        <p class="opera__pdf reveal"><a class="cta" href="{url}" target="_blank" rel="noopener" type="application/pdf">{label} <i class="ph-bold ph-book-open" aria-hidden="true"></i></a><small>{peso}</small></p>'
    tavole = "\n".join(
        f'          <button class="art-fig plate{" plate--wide" if SIZES["opere"][n][0] > 2 * SIZES["opere"][n][1] else ""}" type="button" data-full="assets/img/opere/{n}-1400.webp" data-title="{o["breve"]}">{pic(n, alt, sizes="(max-width: 760px) 50vw, 400px", folder="opere")}</button>'
        for n, alt in o["tavole"]
    )
    prev_o, next_o = OPERE[i - 1], OPERE[(i + 1) % len(OPERE)]
    sub = f'\n        <p class="article__sub">{o["sottotitolo"]}</p>' if o.get("sottotitolo") else ""
    page(
        url_opera(o), "diario",
        f"{o['breve']} · I mondi disegnati di Baruch",
        o["testi"][0][:155],
        f"""    <article class="article opera">
      <a class="back reveal" href="{url_sezione(MONDI['slug'])}">{sez_drawing(MONDI, "back__art")} {MONDI['titolo']}</a>
      <header class="article__head reveal">
        <p class="article__date">{o['categoria']}</p>
        <h1 class="hand-title hand-title--big">{o['titolo']}</h1>{sub}
      </header>
      <div class="opera__intro">
        <figure class="opera__cover reveal">
          <button class="art-fig" type="button" data-full="assets/img/articoli/{o['cover']}-1400.webp" data-title="{o['breve']}">{pic(o['cover'], COVER_ALT[o['cover']], lazy=False, sizes="(max-width: 760px) 100vw, 520px")}</button>
        </figure>
        <div class="opera__text reveal" style="--d:.1s">
          <dl class="opera__facts">
            <div><dt>Committente</dt><dd>{o['con']}</dd></div>
            <div><dt>Tecnica</dt><dd>{o['tecnica'].replace('Tecnica mista: ', 'mista, ')}</dd></div>
          </dl>
{testi}{pdf}
        </div>
      </div>{quote}
      <section class="opera__plates" aria-labelledby="tavole">
        <h2 class="hand-title reveal" id="tavole">Le tavole</h2>
        <div class="plates reveal">
{tavole}
        </div>
      </section>
      <nav class="opera__nav reveal" aria-label="Altri progetti">
        <a href="{url_opera(prev_o)}"><i class="ph-bold ph-arrow-left" aria-hidden="true"></i> {prev_o['breve']}</a>
        <a href="{url_opera(next_o)}">{next_o['breve']} <i class="ph-bold ph-arrow-right" aria-hidden="true"></i></a>
      </nav>
    </article>""",
        extra="\n  " + LIGHTBOX.format(single=""),
    )

# pagine degli articoli
for a in ART:
    s = SEZ[a["sezione"]]
    img, alt = a["cover"]
    altri = [x for x in ART if x["sezione"] == a["sezione"] and x is not a][:2]
    if len(altri) < 2:
        altri += [x for x in ART if x["sezione"] != a["sezione"]][: 2 - len(altri)]
    page(
        url_articolo(a), "diario",
        f"{a['titolo']} · Diario di Baruch",
        a["estratto"],
        f"""    <article class="article">
      <a class="back reveal" href="{url_sezione(s['slug'])}">{sez_drawing(s, "back__art")} {s['titolo']}</a>
      <header class="article__head reveal">
        <p class="article__date"><time datetime="{a['data']}">{a['data_it']}</time></p>
        <h1 class="hand-title hand-title--big">{a['titolo']}</h1>
        <p class="article__sub">{a['sottotitolo']}</p>
      </header>
      <figure class="article__cover reveal">{pic(img, alt, lazy=False, sizes="(max-width: 1040px) 100vw, 1000px")}</figure>
      <div class="article__body">
{blocks(a['blocchi'])}
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
TITLES = {
    "01": ("Teatro sotto gli alberi", "Bambini e animali giocano tra alberi con le gambe, in un prato fiorito"),
    "02": ("Prato fiorito", "Un prato fitto di fiori colorati dipinti ad acquerello"),
    "03": ("Yan e l’Orso", "Un’orsa abbraccia una madre e il suo bambino vestiti con abiti del nord"),
    "04": ("La maestra Lucia", "La maestra Lucia in bicicletta tra rami disegnati"),
    "05": ("Casetta", "Una casetta fatta di carte a fiori"),
    "06": ("Donnina ingarbugliata", "Una donna con un filo rosso ingarbugliato sulla testa"),
    "07": ("Casa con personaggio", "Una figura con una colomba dentro una casa gialla"),
    "08": ("Le grandi leggi dell’umanità", "Copertina del libro Le grandi leggi dell’umanità illustrata con un giardino"),
    "09": ("Tulipani", "Tulipani rossi fitti con piccole case tra gli steli"),
    "10": ("Donna ai piedi", "Una donna dai capelli rossi dorme sotto una colomba bianca"),
    "11": ("Bambina e bambola", "Una madre abbraccia una bambina su uno sfondo turchese con carte a fiori"),
    "12": ("Calendario illustrato “Prove di volo”", "Un uccello giallo vola sopra un campo di papaveri"),
    "13": ("Sassi sul naso", "Una donna tiene in equilibrio una pila di sassi sul naso"),
    "14": ("Testa fiorita", "Una donna con un garofano al posto dei capelli"),
    "15": ("Ciondoli", "Ciondoli in ceramica dipinti con volti e foglie blu"),
    "16": ("", "Un uccello dalle piume rosse e dalla coda a righe colorate"),
    "17": ("", "Un uccello giallo fatto di due grandi foglie"),
    "18": ("", "Un uccello verde ad acquerello in volo"),
    "19": ("Sedia", "Una sedia di legno decorata con case e alberi"),
    "20": ("Mappa parlante di Casina", "Mappa illustrata del paese di Casina tra colline verdi"),
    "21": ("Arte canusina", "Una donna in camice legge un libro di arte canusina"),
    "22": ("Coniglio", "Un coniglio e uno scoiattolo con un rametto di alchechengi"),
    "23": ("Bambina nel prato", "Una bambina dorme nell’erba alta tra fiori gialli"),
    "img-6334": ("", "Quattro fragole dipinte, due con un volto"),
    "img-6431": ("", "Una teiera in ceramica con un uccellino sul coperchio"),
    "img-6437": ("", "Una ragazza dai capelli al vento dentro una grande tazza blu"),
}
NOTE = {"01": "Tecnica mista: gouache e digitale", "03": "Tecnica mista: acrilico e digitale", "12": "Tecnica mista: gouache e digitale"}
lst = json.loads((DATI / "galleria.json").read_text(encoding="utf-8"))
lst.sort(key=lambda r: (r["name"][:2] if r["name"][:2].isdigit() else "99" + r["name"]))
cells = []
for r in lst:
    k = r["name"][:2] if r["name"][:2].isdigit() else r["name"]
    t, alt = TITLES[k]
    n = r["name"]
    cut = ' class="is-cutout"' if r["alpha"] else ""
    cells.append(
        f"""        <button class="gallery__item reveal" type="button" data-full="assets/img/galleria/{n}-1600.webp" data-title="{t}" data-note="{NOTE.get(k, '')}">
          <img{cut} src="assets/img/galleria/{n}-720.webp" alt="{alt}" width="{r['w']}" height="{r['h']}" loading="lazy">
        </button>"""
    )
# opere su commissione pubblicate su illustraremondi.it
for n, t, tec, alt in SEZ["i-mondi-disegnati-di-baruch"]["opere"]:
    if n in ("teatro-sotto-gli-alberi",):
        continue  # già presente nella galleria
    w, h = SIZES["articoli"][n]
    cells.insert(0,
        f"""        <button class="gallery__item reveal" type="button" data-full="assets/img/articoli/{n}-1400.webp" data-title="{t}" data-note="{tec}">
          <img src="assets/img/articoli/{n}-720.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy">
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
          <figure class="o-sedia reveal" style="--d:.08s"><img src="assets/img/galleria/19-sedia-720.webp" alt="Una sedia di legno decorata con case e alberi" width="720" height="1018" loading="lazy"></figure>
          <figure class="o-ciondoli reveal" style="--d:.16s"><img src="assets/img/galleria/15-ciondoli-720.webp" alt="Ciondoli in ceramica dipinti con volti e foglie blu" width="720" height="660" loading="lazy"></figure>
          <figure class="o-teiera reveal" style="--d:.24s"><img src="assets/img/galleria/img-6431-720.webp" alt="Una teiera in ceramica con un uccellino sul coperchio" width="720" height="821" loading="lazy"></figure>
          <figure class="o-fragole reveal" style="--d:.3s"><img src="assets/img/galleria/img-6334-720.webp" alt="Quattro fragole dipinte, due con un volto" width="720" height="218" loading="lazy"></figure>
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
        <form class="form reveal" id="contact-form" novalidate>
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
          <button class="cta" type="submit">Invia il messaggio</button>
          <p class="form__note"></p>
          <p class="form__status" role="status"></p>
        </form>
        <div class="contact__info reveal" style="--d:.12s">
          <address>
            Caterina Santambrogio<br>
            Via Chiesa di Rorai 3<br>
            Pordenone<br>
            cell. <a href="tel:+393404742250">340 474 2250</a><br>
            P.I. 01980800930<br>
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
ART_BY = {a["slug"]: a for a in ARTICOLI}
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
""", encoding="utf-8")
print("reindirizzamenti in .htaccess:", len(REDIRECT))
