# Baruch · illustrare mondi

Il nuovo sito di **Caterina Santambrogio**, illustratrice. Nasce per sostituire illustraremondi.it.

## 👉 [Guarda il sito](https://xandre04.github.io/baruch/)

Anteprima pubblicata con GitHub Pages. È la versione di prova da far vedere a Caterina, non ancora quella definitiva sul dominio.

Pagine da cui partire:

- [Home](https://xandre04.github.io/baruch/)
- [Chi è Baruch](https://xandre04.github.io/baruch/chi-e-baruch.html)
- [Diario](https://xandre04.github.io/baruch/diario.html), con le cinque sezioni e gli articoli
- [I mondi disegnati di Baruch](https://xandre04.github.io/baruch/diario/i-mondi-disegnati-di-baruch.html): i progetti su commissione con le tavole e i calendari
- [Collaborazioni](https://xandre04.github.io/baruch/collaborazioni.html)
- [Contatti](https://xandre04.github.io/baruch/contatti.html)

## Com'è fatto

Sito statico in HTML, CSS e un po' di JavaScript: niente database, niente WordPress. Tutto lo stile viene dagli elementi dipinti a mano da Caterina (pennellate, macchie della barra, quadretti, Baruch con la lettera), che si trovano in `img/ui/`.

| Cartella / file | Contenuto |
|---|---|
| `index.html` e le altre pagine | generate automaticamente, non modificarle a mano |
| `diario/` | sezioni del diario, articoli e pagine delle opere |
| `css/style.css` | tutto lo stile |
| `js/main.js` | menu, ingrandimento immagini, modulo contatti. In cima ci sono email e social da completare |
| `img/` | immagini ottimizzate in WebP |
| `pdf/` | i calendari "Prove di volo" e "Vuoi guarire?" |
| `_diario.py` | testi e dati di articoli e opere |
| `_build.py` | genera le pagine HTML |

## Aggiungere un articolo (per ora)

1. Mettere le immagini in `img/articoli/` in due misure (`nome-720.webp` e `nome-1400.webp`).
2. Aggiungere una voce in `ARTICOLI` dentro `_diario.py`. Le istruzioni sono in cima al file.
3. Rigenerare le pagine:

   ```bash
   python _build.py
   ```

È una procedura provvisoria: il passo successivo è un editor online, così Caterina potrà pubblicare da sola dal browser.

## Da completare

- Email per il modulo contatti e link di Instagram, LinkedIn e Facebook in `js/main.js`
- Pagina privacy
- Pubblicazione su Keliweb e collegamento del dominio
