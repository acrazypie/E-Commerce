# 🛒 E-Commerce

Un esempio di e-commerce creato con **Python e Flask**, database in **SQLite**.\
Questo progetto è una esercitazione didattica.

## 📝 Caratteristiche

- Registrazione con email e password (`hashata con werkzeug.security`).
- Login e logout con gestione della sessione Flask
- Prodotti consigliati nella home
- Shop con prodotti curati
- Carrello facilmente gestibile
- Account admin che gestisce i prodotti

## 💾 Installazione

1. Clona la repository:
   ```bash
   git clone https://github.com/acrazypie/E-Commerce.git
   ```
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. Avvia l'app:
   ```bash
   python app.py
   ```

## 📂 Struttura

```bash
project/
│── app/
│ │── database/ # Database SQLite (creato automaticamente)
│ │── static/ # File CSS
│ │── templates/ # Templates HTML (Jinja2)
│ │ ├── cart.html
│ │ ├── index.html
│ │ ├── login.html
│ │ ├── user.html
│ │ ├── products.html
│ │ ├── register_item.html
│ │ ├── register.html
│ │ └── remove_item.html
│ │── app.py # Applicazione Flask
│ │── models.py # Modelli/Classi usati
│ │── routes.py # Gestione di tutte le rotte
│ ├── db_test.py # Script per popolare il db (testing purposes)
│ ├── utility.py # Funzioni utili lato Python
│── requirements.txt # Librerie usate
│── .gitignore # Ignore __pycache__ folder on commits
│── README.md # Documentazione del progetto

```

## 🚀 Stile e convenzioni

- Nome file: snake_case.py
- Funzioni e variabili: snake_case
- Classi: CamelCase

[![Maintained by acrazypie](https://img.shields.io/badge/maintained%20by-acrazypie-9cf?logo=github&style=flat-square)](https://linktr.ee/gen3sio)
