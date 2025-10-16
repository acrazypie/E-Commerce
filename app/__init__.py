from flask import Flask
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager
from pathlib import Path
from .models.models import db, User
from .database.db_test import populate_db_test
from config import config

app = Flask(__name__)

app.secret_key = config.SECRET_KEY or "dev"

login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


oauth = OAuth(app)

# Google (OpenID Connect)
oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

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
