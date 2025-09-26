# 🛒 E-Commerce

Un esempio di e-commerce creato con **Python e Flask**, database in **SQLite**.

## 📝 Caratteristiche

- Registrazione con email e password (`hashata con werkzeug.security`).
- Login e logout con gestione della sessione Flask
- Prodotti consigliati nella home
- Shop con prodotti curati
- Carrello facilmente gestibile

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
│── app.py # Applicazione Flask
│── models.py # Modelli/Classi usati
│── routes.py # Gestione di tutte le rotte
├── db_test.py # Script per popolare il db (testing purposes)
│── database/ # Database SQLite (creato automaticamente)
│── templates/ # Templates HTML (Jinja2)
│ ├── cart.html
│ ├── index.html
│ ├── login.html
│ ├── products.html
│ └── register.html
│── static/ # File CSS
│── requirements.txt # Librerie usate
│── .gitignore # Ignore __pycache__ folder on commits
│── README.md # Documentazione del progetto

```

## 🚀 Stile e convenzioni

- Nome file: snake_case.py
- Funzioni e variabili: snake_case
- Classi: CamelCase

mantenuto da [acrazypie](https://linktr.ee/gen3sio)
