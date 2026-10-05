# Baruch · illustrare mondi

Il nuovo sito di **Caterina Santambrogio**, illustratrice. Nasce per sostituire illustraremondi.it.

## 👉 [Guarda il sito](https://xandre04.github.io/baruch/)

Anteprima pubblicata con GitHub Pages. È la versione di prova da far vedere a Caterina, non ancora quella definitiva sul dominio.

Pagine da cui partire:

- [Home](https://xandre04.github.io/baruch/)
- [Chi è Baruch](https://xandre04.github.io/baruch/chi-e-baruch/)
- [Diario](https://xandre04.github.io/baruch/diario/), con le cinque sezioni e gli articoli
- [I mondi disegnati di Baruch](https://xandre04.github.io/baruch/diario/i-mondi-disegnati-di-baruch/): i progetti su commissione con le tavole e i calendari
- [Collaborazioni](https://xandre04.github.io/baruch/collaborazioni/)
- [Contatti](https://xandre04.github.io/baruch/contatti/)

## ✏️ Pubblicare articoli: [l'editor](https://xandre04.github.io/baruch/admin/)

Caterina scrive le pagine del Diario e i progetti su commissione dal browser, senza toccare file. Al salvataggio il sito si rigenera e va online da solo in un paio di minuti.

**[Guida per Caterina](GUIDA-CATERINA.md)**: primo accesso, nuova pagina, foto, bozze.

## Come è organizzato

```
baruch/
├── contenuti/                     ← quello che Caterina scrive con l'editor
│   ├── articoli/                  una pagina del Diario per file (JSON, testo in Markdown)
│   ├── opere/                     un progetto su commissione per file
│   ├── collaborazioni.json        le immagini della galleria Collaborazioni
│   └── media/                     le foto caricate, a piena qualità
│
├── sito/                          ← quello che va online (su Keliweb si carica solo questa cartella)
│   ├── index.html                 home
│   ├── chi-e-baruch/
│   ├── diario/                    una cartella per sezione, con i suoi articoli e le opere
│   ├── collaborazioni/  shop/  contatti/
│   ├── admin/                     l'editor (Sveltia CMS) e la sua configurazione
│   ├── assets/
│   │   ├── css/  js/
│   │   ├── img/
│   │   │   ├── ui/                elementi dipinti a mano: pennellate, barra, quadretti, titoli, icone
│   │   │   ├── chi/  diario/      illustrazioni delle pagine fisse
│   │   │   └── contenuti/         foto di articoli, opere e collaborazioni, generate da contenuti/media
│   │   └── pdf/                   calendari e altri PDF
│   ├── contatti/invia.php         invia i messaggi del modulo all'email di Caterina
│   └── .htaccess                  vecchi indirizzi di illustraremondi.it → pagine nuove
│
├── sorgenti/                      ← il codice che genera il sito
│   ├── build.py                   genera tutte le pagine HTML in sito/
│   ├── contenuti.py               legge contenuti/, interpreta il testo, prepara le foto
│   ├── diario.py                  le cinque sezioni del Diario
│   └── controlla.py               verifica che link e immagini non siano rotti
│
├── .github/workflows/pubblica.yml ← genera, controlla e pubblica a ogni modifica
└── GUIDA-CATERINA.md
```

Le pagine HTML in `sito/` sono generate: non si modificano a mano.

## Come funziona la pubblicazione

1. Caterina salva nell'editor → l'editor scrive il file in `contenuti/` su GitHub.
2. Il workflow `pubblica.yml` genera pagine e foto, controlla i link e salva il risultato in `sito/`.
3. Pubblica l'anteprima su GitHub Pages e, se configurato, carica `sito/` su Keliweb via FTP.

### Collegare Keliweb

Nel repository, **Settings → Secrets and variables → Actions → New repository secret**:

| Segreto | Valore |
|---|---|
| `FTP_SERVER` | server FTP indicato da Keliweb nel pannello |
| `FTP_USERNAME` | utente FTP |
| `FTP_PASSWORD` | password FTP |
| `FTP_CARTELLA` | facoltativo: cartella del sito sul server (predefinita `public_html/`) |

Dalla pubblicazione successiva il sito viene caricato anche su Keliweb. Quando il dominio punta a Keliweb, aggiornare `site_url` in `sito/admin/config.yml`.

### Accesso di Caterina all'editor

Caterina ha un suo account GitHub ed entra nell'editor con una chiave di accesso personale (passaggi nella [guida](GUIDA-CATERINA.md)). Funziona sia sull'anteprima sia su Keliweb.

Per aggiungerla al progetto: **Settings → Collaborators → Add people** con il suo nome utente GitHub. Lei deve accettare l'invito che riceve per email. Le sue modifiche compaiono nella cronologia a suo nome.

## Lavorare in locale

```bash
pip install pillow
python sorgenti/build.py
python sorgenti/controlla.py
```

Per vedere il sito: `python -m http.server --directory sito` e aprire <http://localhost:8000>.

## Da completare

- Pagina privacy
- Pubblicazione su Keliweb e collegamento del dominio
