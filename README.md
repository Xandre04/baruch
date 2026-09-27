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

## Come è organizzato

```
baruch/
├── sito/                          ← quello che va online (su Keliweb si carica solo questa cartella)
│   ├── index.html                 home
│   ├── chi-e-baruch/
│   ├── diario/
│   │   ├── index.html             indice del diario
│   │   ├── come-fiori-selvatici/  una cartella per sezione, con i suoi articoli
│   │   ├── costruire-con-baruch/
│   │   ├── i-mondi-disegnati-di-baruch/   anche le pagine delle opere su commissione
│   │   ├── le-avventure-di-baruch/
│   │   └── le-cose-magiche-di-baruch/
│   ├── collaborazioni/
│   ├── shop/
│   ├── contatti/
│   ├── assets/
│   │   ├── css/                   stile
│   │   ├── js/                    menu, ingrandimento immagini, modulo contatti
│   │   ├── img/                   immagini ottimizzate (WebP)
│   │   │   ├── ui/                elementi dipinti a mano: pennellate, barra, quadretti, titoli
│   │   │   ├── chi/  diario/      illustrazioni delle pagine
│   │   │   ├── articoli/          foto degli articoli del diario
│   │   │   ├── opere/             tavole dei progetti su commissione
│   │   │   └── galleria/          collaborazioni
│   │   └── pdf/                   calendari "Prove di volo" e "Vuoi guarire?"
│   └── .htaccess                  vecchi indirizzi di illustraremondi.it → pagine nuove
│
├── sorgenti/                      ← quello che si modifica
│   ├── build.py                   genera tutte le pagine HTML in sito/
│   ├── diario.py                  testi e dati di sezioni, articoli e opere
│   ├── controlla.py               verifica che link e immagini non siano rotti
│   └── dati/                      misure delle immagini
│
└── .github/workflows/             pubblica sito/ come anteprima a ogni modifica
```

Le pagine HTML in `sito/` sono generate: non si modificano a mano. Si cambiano i testi in `sorgenti/` e si rigenerano.

Sito statico in HTML, CSS e un po' di JavaScript: niente database, niente WordPress. Tutto lo stile viene dagli elementi dipinti a mano da Caterina, in `sito/assets/img/ui/`.

## Aggiungere un articolo (per ora)

1. Mettere le immagini in `sito/assets/img/articoli/` in due misure (`nome-720.webp` e `nome-1400.webp`) e aggiungerne le misure in `sorgenti/dati/articoli.json`.
2. Aggiungere una voce in `ARTICOLI` dentro `sorgenti/diario.py`. Le istruzioni sono in cima al file.
3. Dalla cartella principale, rigenerare e controllare:

   ```bash
   python sorgenti/build.py
   python sorgenti/controlla.py
   ```

È una procedura provvisoria: il passo successivo è un editor online, così Caterina potrà pubblicare da sola dal browser.

## Da completare

- Email per il modulo contatti e link di Instagram, LinkedIn e Facebook in `sito/assets/js/main.js`
- Pagina privacy
- Pubblicazione su Keliweb e collegamento del dominio
