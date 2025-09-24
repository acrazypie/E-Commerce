from flask_sqlalchemy import SQLAlchemy


def populate_db_test(db: SQLAlchemy, User, Product):
    if not User.query.first():
        user = User(email="test@example.com", password="password")
        user = User(email="test@demo.com", password="password")
        db.session.add(user)
        db.session.commit()

    if not Product.query.first():
        db.session.bulk_save_objects(
            [
                Product(
                    name="Laptop",
                    price=799.99,
                    description="A high performance laptop",
                    image_url="https://images.pexels.com/photos/129208/pexels-photo-129208.jpeg",
                ),
                Product(
                    name="Smartphone",
                    price=199.99,
                    description="A latest model smartphone",
                    image_url="https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg",
                ),
                Product(
                    name="Headphones",
                    price=39.99,
                    description="Noise-cancelling over-ear headphones",
                    image_url="https://images.pexels.com/photos/1649771/pexels-photo-1649771.jpeg",
                ),
            ]
        )
        db.session.commit()
