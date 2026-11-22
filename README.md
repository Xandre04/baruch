# Baruch · illustrare mondi

Il sito di **Caterina Santambrogio**, illustratrice (Pordenone). Lo segue **Valeriu** (GitHub `Xandre04`); Caterina modifica i contenuti da sola con l'editor online.

| | |
|---|---|
| Sito pubblicato | **https://illustraremondi.it** (hosting Keliweb, caricato via FTP) |
| Anteprima | https://xandre04.github.io/baruch/ (GitHub Pages, stesso contenuto) |
| Editor di Caterina | https://xandre04.github.io/baruch/admin/ (Sveltia CMS) |
| Repository | https://github.com/Xandre04/baruch |
| Guida per Caterina | [GUIDA-CATERINA.md](GUIDA-CATERINA.md) |
| Email del sito | illustraremondi@gmail.com (riceve anche il modulo contatti) |

---

## Pagine del sito

- **Home** (`sito/index.html`): l'immagine principale con "Baruch · illustrare mondi" resta ferma e la pagina le scorre sopra ("sipario"). Sotto:
  - due righe per le aziende con il link a Collaborazioni;
  - la fascia **Lavori in corso**;
  - i cinque disegni delle sezioni del Diario.
- **Chi è Baruch**: testo e foto di Caterina.
- **Diario**, con cinque sezioni (in `sorgenti/diario.py`):
  - Mondi illustrati (i progetti su commissione);
  - Le avventure di Baruch;
  - Come fiori selvatici;
  - Costruire con Baruch;
  - Le cose magiche di Baruch.
- **Collaborazioni**: la pagina per le aziende (classi `hp-…`), tutta dall'editor:
  - apertura, committenti, tre modi di lavorare;
  - le collezioni in licenza come copertine affiancate sulla carta a quadretti; ognuna apre la sua pagina `sito/collaborazioni/<titolo>.html` con scheda, foto dei prodotti, personaggi e pattern;
  - come lavora, con la scheda tecnica;
  - i lavori su commissione (solo quelli con "Nella pagina" acceso) e la chiusura.
  - Nelle schede e nei passi il **grassetto** diventa evidenziato in giallo (`<mark>`).
- **Contatti**: modulo inviato da `sito/contatti/invia.php` con la funzione `mail()` di PHP, quindi funziona solo su Keliweb.
- **Lavori in corso**: annunci in home; quelli con dettagli, altre foto o video hanno una pagina propria in `sito/lavori-in-corso/`.
- **Shop** e **Privacy e cookie**: pagine esistenti ma fuori dal menu. Shop dice "in preparazione". La privacy è una bozza da far verificare a chi segue Caterina per la parte legale.

Menu: Home · Chi è Baruch · Diario · Collaborazioni · Contatti.

---

## Come è organizzato

```
baruch/
├── contenuti/                     ← quello che Caterina scrive con l'editor (JSON, testi in Markdown)
│   ├── articoli/                  una pagina del Diario per file, composta a blocchi
│   ├── opere/                     un progetto su commissione per file (Mondi illustrati)
│   ├── adesso.json                gli annunci "Lavori in corso"
│   ├── collaborazioni.json        pagina Collaborazioni e pagine delle collezioni
│   └── media/                     le foto caricate, a piena qualità
│
├── sito/                          ← quello che va online (su Keliweb si carica solo questa cartella)
│   ├── *.html, */index.html       GENERATE da build.py: non si modificano a mano
│   ├── lavori-in-corso/           GENERATE: una pagina per annuncio (cancellate e rifatte a ogni build)
│   ├── .htaccess                  GENERATO: vecchi indirizzi di illustraremondi.it → pagine nuove
│   ├── admin/                     l'editor: index.html e config.yml (A MANO)
│   ├── assets/css/                style.css, fonts.css, icone.css (A MANO)
│   ├── assets/js/main.js          menu, lightbox, filtro diario, scadenza annunci… (A MANO)
│   ├── assets/fonts/              Kalam (scritto a mano), Barlow, icone Phosphor
│   ├── assets/img/ui/             elementi dipinti a mano: pennellate, barra del menu, titoli, quadretti
│   ├── assets/img/contenuti/      GENERATE da contenuti/media: WebP 720 e 1400 px
│   ├── assets/pdf/  assets/video/ caricati dall'editor
│   └── contatti/invia.php         (A MANO)
│
├── sorgenti/
│   ├── build.py                   genera tutte le pagine in sito/
│   ├── contenuti.py               legge contenuti/, Markdown semplice, prepara le foto
│   ├── diario.py                  le cinque sezioni del Diario
│   └── controlla.py               link, immagini e PDF rotti + validità di admin/config.yml
│
├── bozze/                         ← proposte non pubblicate (non vanno online, vedi sotto)
├── IMMAGINI e TESTI/              materiali originali di Caterina (in .gitignore, solo sul computer)
├── .github/workflows/pubblica.yml
├── GUIDA-CATERINA.md              guida all'editor per Caterina (va aggiornata a ogni nuovo campo)
└── README.md
```

**Attenzione: `sito/` è una cartella mista.** Ci sono pagine generate e file scritti a mano (`admin/config.yml`, CSS, `main.js`, `invia.php`, font, PDF). Prima di un `git pull` con modifiche locali:
- non scartare tutta `sito/`;
- scarta solo le pagine generate (`git checkout -- 'sito/*.html' 'sito/**/*.html' sito/assets/img/contenuti sito/.htaccess`), oppure usa `git stash`;
- poi rigenera.

---

## Pubblicazione

1. **Chi modifica:**
   - Caterina salva nell'editor e Sveltia fa un commit su `main` a nome suo, per esempio "Modifica: annunci";
   - oppure Valeriu fa un commit e un push da qui.
2. **Il workflow `.github/workflows/pubblica.yml`:**
   - installa `pillow` e `pyyaml`, esegue `build.py` e poi `controlla.py` (si ferma se c'è qualcosa di rotto);
   - committa le pagine rigenerate con il messaggio "Sito rigenerato: …";
   - pubblica su GitHub Pages;
   - carica `sito/` su Keliweb via FTP. I segreti `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD` e `FTP_CARTELLA` sono già impostati; `FTP_PROTOCOLLO` è facoltativo (predefinito ftps).
3. In circa 2 minuti il sito è online. Per controllare: `gh run list -L 3`.

Dopo un push conviene fare `git pull`, perché il workflow aggiunge il suo commit "Sito rigenerato".

### Editor (Sveltia CMS)

- **Configurazione:** `sito/admin/config.yml`. Backend GitHub `Xandre04/baruch`, branch `main`. `site_url` punta a `https://illustraremondi.it/` (è solo il link "vedi sito" dell'editor).
- **Accesso di Caterina:** ha un suo account GitHub collaboratore ed entra con una *classic token* (scope `repo`). I passaggi sono nella guida. Il pulsante "Accedi con GitHub" non è attivo.
- **Collezioni dell'editor:**
  - Lavori in corso;
  - Diario (articoli a blocchi);
  - Mondi illustrati (opere);
  - Collaborazioni (pagina unica).
- **Regole per `config.yml`:**
  - **YAML:** un testo con `": "` (due punti e spazio) va tra virgolette, altrimenti l'editor non si apre ("The configuration file could not be parsed"). `controlla.py` ora lo segnala.
  - **Limite di circa 10 MB per file non immagine** (PDF, video): oltre, il salvataggio fallisce con "Load failed" e si perde tutto il salvataggio, anche il resto. Le foto non hanno il limite, l'editor le riduce. I file pesanti li carica Valeriu a mano in `sito/assets/pdf/` o `sito/assets/video/`.
  - **Campi nuovi:** dopo averli aggiunti, Caterina deve ricaricare l'editor con Ctrl+F5.
- **"Carica più immagini insieme"** (Collaborazioni, tavole delle opere): `accogli_caricamenti()` in `contenuti.py` sposta le foto caricate nel loro elenco al build successivo.

---

## Come funziona `build.py` (cose non ovvie)

- **Foto:**
  - ogni file in `contenuti/media` diventa `sito/assets/img/contenuti/<nome-sito>-<md5 8 caratteri>-720.webp` e `-1400.webp`;
  - l'impronta cambia se cambia la foto, quindi niente problemi di cache;
  - `immagine("/contenuti/media/x.jpg")` restituisce i percorsi e le misure;
  - le foto con trasparenza sono "scontornate" (classe `is-cutout`).
- **CSS e JS:**
  - sono richiamati con `?v=<hash>`, quindi le modifiche arrivano subito;
  - **le immagini in `assets/img/ui/` invece non hanno versione**: se ne cambi una, cambiale anche il nome (per esempio `nav-strip.webp` è diventato `nav-barra.webp`), altrimenti i browser tengono la vecchia.
- **Fine riga:** `.gitattributes` forza LF, così gli hash coincidono tra Windows e GitHub. Se dopo un build locale tutte le pagine risultano modificate solo per il `?v=` del CSS, è un CSS con CRLF in locale: si scarta con `git checkout -- sito`.
- **Percorsi:** le pagine scrivono i percorsi dalla radice del sito; `page()` aggiunge `../` per le sottocartelle.
- **Testi:**
  - Markdown ridotto: grassetto, corsivo, link, titoletti, elenchi, citazioni, immagini;
  - le immagini consecutive diventano una griglia ingrandibile;
  - `link_sicuro()` accetta solo http, https e mailto.
- **Articoli a blocchi:**
  - i blocchi sono testo, titoletto, foto, foto accanto al testo, foto in fila, citazione, video, galleria e spazio;
  - foto, foto accanto al testo e foto in fila hanno la **didascalia** (per esempio misure e materiale).
- **Lavori in corso** (`contenuti/adesso.json`):
  - in home si vedono al massimo 3 annunci;
  - `main.js` nasconde quelli scaduti (`fino_al`) e, se non ne resta nessuno, la fascia;
  - campi: titolo, quando, testo breve, dettagli, foto, altre foto, video, `video_in_home`, link e scadenza;
  - l'annuncio ha una pagina propria solo se ha dettagli, altre foto o video.
- **Barra del menu:**
  - `nav-barra.webp` è ricomposta dall'originale `IMMAGINI e TESTI/1- HOME/8 - SFONDO NOMI BARRA.png` (2721×231), con la macchia Shop tolta;
  - le posizioni delle voci, in percentuale, sono in `style.css` (`.strip .n-…`).
- **Vecchi indirizzi:** `.htaccess` reindirizza 20 indirizzi del vecchio illustraremondi.it alle pagine nuove.

### Stile

- **Colori** (variabili in `style.css`): carta `#fefdfb`, verde scuro `#34432f`, terracotta `#c9623f`.
- **Font:** Kalam per le scritte a mano, Barlow Semi Condensed per il testo.
- **Elementi dipinti:** pennellate verde, pesca e crema dietro titoli e pulsanti (`.cta`), carta a quadretti, titoli delle pagine come immagini dipinte.
- **Lo stile deve restare "dipinto a mano":** Caterina lo vuole personale, ma per i Lavori in corso ha chiesto uno stile pulito, "grafico" (solo la griglia dietro, niente pennellate né bordi).

---

## Lavorare in locale (Windows)

`python` su questo computer apre l'alias del Microsoft Store: usa il percorso completo.

```bash
PY=/c/Users/Valer/AppData/Local/Python/pythoncore-3.14-64/python.exe
$PY -m pip install pillow pyyaml
$PY sorgenti/build.py        # rigenera sito/
$PY sorgenti/controlla.py    # deve dire "riferimenti rotti: 0"
$PY sorgenti/contenuti.py    # piccolo autotest, stampa "ok"
```

- **Anteprima:** `.claude/launch.json` avvia `python -m http.server 5173 --directory sito`, quindi il sito è su <http://localhost:5173>.
- **Schermate a pagina intera:** in `bozze/collaborazioni-aziende/` ci sono due script.
  - `schermate.mjs` usa Chrome headless via CDP (Node 24); va lanciato con `node schermate.mjs <cartella-uscita> <cartella-profilo> <larghezza> <pagina…>`.
  - `pdf.py` trasforma quelle schermate in un PDF da far vedere a Caterina.
  - Su telefono le schermate oltre circa 16.000 px si ripetono: per questo `schermate.mjs` usa una densità di 1,25.

---

## Bozze non pubblicate

### `bozze/collaborazioni-aziende/`: pubblicata il 22 novembre 2026

La bozza "portfolio per le aziende" è diventata la pagina Collaborazioni, con i contenuti in `contenuti/collaborazioni.json`. Nella cartella delle bozze restano solo gli script per le schermate e il PDF.

- **Le parti evidenziate in giallo (`<mark>`) sono da chiedere a Caterina:**
  - se le collezioni le dà in licenza, in esclusiva o in tutti e due i modi;
  - risoluzione, formati e colori dei file;
  - quanti giri di revisione sono compresi;
  - anni di esperienza;
  - il telefono.
- **Se la approva**, per renderla definitiva:
  - spostare i testi in `contenuti/collaborazioni.json`, con i campi nell'editor, perché ora sono scritti nella pagina;
  - mettere il markup in `build.py` e il CSS in `style.css`;
  - aggiornare la guida.

---

## Da fare / aperto

- [ ] Risposta di Caterina sulla bozza Collaborazioni per le aziende, con i dati in giallo.
- [ ] Testi per le aziende "con le parole giuste" della nipote: Caterina deve mandarli. Si cambiano dall'editor (Collaborazioni → Pagina Collaborazioni) o nella bozza.
- [ ] Eventuale catalogo PDF scaricabile per le aziende. I file di stampa BERESHIT (poster 30×40, quadretti A4, segnalibri 7×21) sono tra i materiali di Caterina e pesano 5–13 MB l'uno: non sono nel sito.
- [ ] Shop: resta fuori dal menu finché Caterina non decide.
- [ ] Privacy: far verificare il testo a chi segue Caterina per la parte legale.
- [ ] Il video di Caterina per un annuncio dei Lavori in corso era oltre i 10 MB: se lo manda, va caricato a mano in `sito/assets/video/` e indicato nel campo `video` di `contenuti/adesso.json`.

## Come si lavora con Valeriu

- Lingua: italiano. Le richieste di Caterina arrivano tramite Valeriu, spesso come messaggi o vocali incollati.
- **Prima di pubblicare, Valeriu vuole vedere una bozza** (schermate su computer e telefono). Si fa commit e push solo quando dice esplicitamente "carica".
- Ogni nuova funzione dell'editor va spiegata anche in `GUIDA-CATERINA.md`, con parole semplici.
- Password, token e dati FTP li gestisce solo Valeriu: non vanno mai chiesti né scritti nei file.
