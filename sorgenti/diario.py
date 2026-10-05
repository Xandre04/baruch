"""Le cinque sezioni del Diario di Baruch.

Ogni sezione è legata a un disegno di Caterina (sito/assets/img/diario/), quindi resta qui.
Articoli e opere invece si scrivono con l'editor: stanno in contenuti/.
"""

SEZIONI = [
    {
        "slug": "le-avventure-di-baruch",
        "titolo": "Le avventure di Baruch",
        "disegno": "avventure", "w": 860, "h": 829,
        "alt": "Uno zaino dipinto con i colori di un prato",
        "classe": "d-avv",
        "intro": [
            "L’avventura è un modo di vivere, non un traguardo lontano. Per me ogni uscita è una spedizione: che sia tra le sale di un museo, nel silenzio di una chiesa o lungo un sentiero dietro casa, parto sempre per scoprire qualcosa che prima non vedevo.",
            "Qui raccolgo i miei appunti visivi: schizzi rapidi per fermare quel senso di viaggio che provo anche a pochi chilometri da dove abito.",
        ],
    },
    {
        "slug": "come-fiori-selvatici",
        "titolo": "Come fiori selvatici",
        "disegno": "fiori-selvatici", "w": 900, "h": 1498,
        "alt": "Un ramo di margherite rosa disegnato a matita e acquerello",
        "classe": "d-fiori",
        "intro": [
            "Selvatico è ciò che cresce senza chiedere permesso. Per me la natura è il luogo del riparo e della bussola: quando mi perdo, torno ad osservare i ritmi lenti della terra.",
            "E disegno per ritrovare frammenti di quel mondo rigenerante, estratti di piante e vita animale che segnano la strada per ritrovare sé stessi.",
        ],
    },
    {
        "slug": "costruire-con-baruch",
        "titolo": "Costruire con Baruch",
        "disegno": "costruire", "w": 900, "h": 819,
        "alt": "Due mani disegnano con una matita su un foglio colorato",
        "classe": "d-cost",
        "intro": [
            "Progettare, sporcarsi, sbagliare, finire. I laboratori sono il luogo dove la tecnica incontra il gioco, per ogni età. Qui trovi i miei workshop e le novità sui prossimi incontri.",
            "Non serve essere artisti per partecipare: serve la curiosità di smontare il mondo e ricostruirlo con i propri colori.",
        ],
    },
    {
        "slug": "i-mondi-disegnati-di-baruch",
        "titolo": "I mondi disegnati di Baruch",
        "disegno": "mondi-disegnati", "w": 900, "h": 543,
        "alt": "Una casetta fatta di foglie d’autunno con la sua ombra",
        "classe": "d-mondi",
        "intro": [
            "In questa sezione raccolgo i lavori realizzati su commissione: progetti nati dall’incontro con le esigenze dei clienti e trasformati in mondi visivi compiuti.",
            "Partendo dall’idea, la tecnica si mette al servizio della narrazione per dare forma e colore a storie e progetti.",
        ],
    },
    {
        "slug": "le-cose-magiche-di-baruch",
        "titolo": "Le cose magiche di Baruch",
        "disegno": "cose-magiche", "w": 900, "h": 604,
        "alt": "Baruch cavalca un cavallino di legno",
        "classe": "d-magiche",
        "intro": [
            "Uso il legno, l’argilla e il segno per trasformare l’uso comune in un viaggio visivo. Qui non ci sono serie uguali, ma oggetti singoli, che siano tazze illustrate, teiere o elementi d’arredo, che funzionano come bussole per l’immaginario.",
            "Frammenti di un mondo leggero che nascono per essere tenuti tra le mani e per traslocare una piccola storia nello spazio che abitiamo.",
        ],
        # oggetti: (percorso immagine 720, percorso 1400/1600, titolo, alt, w, h)
        "gruppi": [
            ("Ceramica", [
                ("/contenuti/media/ceramica.webp", "Teiera in ceramica con tulipani"),
                ("assets/img/galleria/img-6431-720.webp", "assets/img/galleria/img-6431-1600.webp", "Teiera in ceramica con un uccellino sul coperchio", 720, 821),
                ("assets/img/galleria/15-ciondoli-720.webp", "assets/img/galleria/15-ciondoli-1600.webp", "Ciondoli in ceramica dipinti con volti e foglie blu", 720, 660),
            ]),
            ("Decorazione di mobili", [
                ("/contenuti/media/decorazione-di-mobili.webp", "Un armadio dipinto con una figura tra gli alberi"),
                ("assets/img/galleria/19-sedia-720.webp", "assets/img/galleria/19-sedia-1600.webp", "Una sedia di legno decorata con case e alberi", 720, 1018),
            ]),
        ],
    },
]
