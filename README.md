# E‑Commerce (Flask + SQLAlchemy)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-green)
![Last Commit](https://img.shields.io/github/last-commit/acrazypie/E-Commerce)
![Stars](https://img.shields.io/github/stars/acrazypie/E-Commerce?style=social)

Un esempio di e-commerce minimal ma completo, costruito con Flask e SQLAlchemy, pensato come progetto didattico / base da estendere.

---

## 🚀 Features

- Gestione prodotti: CRUD (crea, leggi, aggiorna, elimina)
- Carrello utenti: aggiungi / rimuovi prodotti
- Interfaccia web semplice con HTML / CSS
- Database SQLite (pronto per essere sostituito con DB più “robusto”)
- Struttura modulare per facilitare estensioni future

---

## 📦 Struttura del progetto

```
project/
│── app/
│ │── database/ # database SQLite (creato automaticamente)
│ │── └── db_test.py # script/test per la creazione / test del database
│ │── static/ # file CSS, immagini, JS, ecc.
│ │── templates/ # file HTML (Jinja2)
│ │── models/ # definizione dei modelli SQLAlchemy
│ │── routes/ # definizione delle rotte / logica delle views
│ ├── __init__.py # definizione / inizializzazione dell'app Flask
│ └── utility.py # funzioni utili
│── .dockerignore # ignore per Docker
│── .env.example # esempio di file .env
│── .gitignore # ignore per Git
│── config.py # accesso alle variablili .env
│── docker-compose.yml # docker file per build
│── Dockerfile # docker image
│── README.md # questo file
│── requirements.txt # librerie usate
└── run.py # punto d’ingresso dell’app
```

---

## 🛠️ Setup & installazione

> Nota: presuppone che tu abbia Python 3.x installato.

1. Clona la repo

   ```bash
   git clone https://github.com/acrazypie/E-Commerce.git
   cd E-Commerce
   ```

2. Crea un virtual environment (fortemente raccomandato)

   ```bash
   python -m venv venv
   source venv/bin/activate     # su Linux/macOS
   venv\Scripts\activate        # su Windows
   ```

3. Installa le dipendenze

   ```bash
   pip install -r requirements.txt
   ```

4. Inizializza / testa il DB

   ```bash
   python db_test.py
   ```

5. Avvia l’app

   ```bash
   python app.py
   ```

6. Visita http://localhost:5000 nel browser — boom, la web app è live.

---

## 🧩 Come è fatta la logica

- models.py: definisce le classi / tabelle (es. Product, User, Cart, etc.)
- routes.py: gestisce le richieste HTTP, coordina modelli + template
- templates/: usa Jinja2 per generare le pagine HTML dinamiche
- static/: contiene style CSS, immagini & assets vari

---

## 🎯 Casi d’uso / flusso tipico

1. L’utente visita la home, vede i prodotti
2. Seleziona un prodotto, lo aggiunge al carrello
3. Il sistema tiene traccia del carrello per sessione / utente
4. L’utente può rimuovere elementi o finalizzare (qui potresti aggiungere funzionalità pagamento)
5. Admin / manutentore può gestire prodotti da backend (CRUD)

---

## 🔧 Estensioni & miglioramenti suggeriti

- Autenticazione / registrazione utente + autorizzazione
- Pagine ordine / checkout + integrazione con gateway di pagamento
- Caricamento immagini per prodotti
- Filtri / categorie / ricerca prodotti
- Supporto a DB PostgreSQL / MySQL
- API REST / endpoint JSON
- Test unitari & integrazione
- Migliorie UI / UI framework (Bootstrap, Tailwind, ecc.)

---

## 🧪 Testing & qualità del codice

- Aggiungi test per modelli / operazioni DB / rotte
- Usa un linter (flake8, pylint, black) per mantenere stile coerente
- Valuta l’uso di Flask Blueprints per organizzare moduli

---

## ℹ️ Convenzioni di codice

- Nomi file: snake_case
- Funzioni / variabili: snake_case
- Classi: CamelCase
- Segui le best practice PEP8 per Python

---

## 🧑‍💻 Contribuire

1. Fai fork del repo
2. Crea un branch feature / fix: git checkout -b feat/nome-funzione
3. Aggiungi commit chiari
4. Apri pull request spiegando cosa cambi / aggiungi
5. Discutiamo e integriamo

---

## 📄 Licenza & crediti

- Mantenuto da acrazypie
- Licenza: MIT
- Se ti piace il progetto, lascia una ⭐

---

[![Maintained by acrazypie](https://img.shields.io/badge/maintained%20by-acrazypie-9cf?logo=github&style=flat-square)](https://linktr.ee/gen3sio)
