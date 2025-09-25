from flask import Flask
from pathlib import Path
from models import db, User, Product


def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    BASE_DIR = Path(__file__).resolve().parent
    DB_DIR = BASE_DIR / "database"
    DB_DIR.mkdir(exist_ok=True)
    db_path = DB_DIR / "ecommerce.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        db_test()

    from routes import routes

    app.register_blueprint(routes)

    return app


def db_test():

    # crea utenti di test
    if not User.query.first():
        user1 = User()
        user1.email = "test@example.com"
        user1.set_password("password")
        db.session.add(user1)

        user2 = User()
        user2.email = "demo@demo.com"
        user2.set_password("password")
        db.session.add(user2)

        db.session.commit()

    # crea prodotti di test
    if not Product.query.first():
        objs = [product1 := Product(), product2 := Product(), product3 := Product()]

        product1.name = "Laptop"
        product1.price = 799.99
        product1.description = "A high performance laptop"
        product1.image_url = (
            "https://images.pexels.com/photos/129208/pexels-photo-129208.jpeg"
        )

        product2.name = "Smartphone"
        product2.price = 199.99
        product2.description = "A latest model smartphone"
        product2.image_url = (
            "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg"
        )

        product3.name = "Headphones"
        product3.price = 39.99
        product3.description = "Noise-cancelling over-ear headphones"
        product3.image_url = (
            "https://images.pexels.com/photos/1649771/pexels-photo-1649771.jpeg"
        )

        db.session.bulk_save_objects(objs)
        db.session.commit()


if __name__ == "__main__":
    app = create_app()

    app.run(debug=True)
