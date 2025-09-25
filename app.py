from flask import Flask
from pathlib import Path
from models import db, User, Product
from db_test import populate_db_test


def create_app():
    app = Flask(__name__)

    BASE_DIR = Path(__file__).resolve().parent
    DB_DIR = BASE_DIR / "database"
    DB_DIR.mkdir(exist_ok=True)
    db_path = DB_DIR / "ecommerce.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        populate_db_test(db, User, Product)

    import routes

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
