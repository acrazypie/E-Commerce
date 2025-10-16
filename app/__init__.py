from flask import Flask
from pathlib import Path
from .models.models import db
from .database.db_test import populate_db_test
from config import config

app = Flask(__name__)

app.secret_key = config.SECRET_KEY

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)
db_path = DB_DIR / "ecommerce.db"

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    populate_db_test()

from .routes.routes import routes

app.register_blueprint(routes)
