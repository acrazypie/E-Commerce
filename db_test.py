from models import db, User, Product


def populate_db_test():

    if not User.query.first():

        test_admin = User()
        test_admin.username = "Admin"
        test_admin.email = "demo@demo.com"
        test_admin.set_password("MyPassword123")
        test_admin.is_admin = True
        db.session.add(test_admin)

        db.session.commit()

    if not Product.query.first():

        product1 = Product()
        product1.name = "Laptop"
        product1.price = 799.99
        product1.description = "A high performance laptop"
        product1.image_url = (
            "https://images.pexels.com/photos/129208/pexels-photo-129208.jpeg"
        )

        product2 = Product()
        product2.name = "Smartphone"
        product2.price = 199.99
        product2.description = "A latest model smartphone"
        product2.image_url = (
            "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg"
        )

        product3 = Product()
        product3.name = "Headphones"
        product3.price = 39.99
        product3.description = "Noise-cancelling over-ear headphones"
        product3.image_url = (
            "https://images.pexels.com/photos/1649771/pexels-photo-1649771.jpeg"
        )

        product4 = Product()
        product4.name = "Smartwatch"
        product4.price = 249.99
        product4.description = "A feature-packed smartwatch"
        product4.image_url = (
            "https://images.pexels.com/photos/267394/pexels-photo-267394.jpeg"
        )

        product5 = Product()
        product5.name = "Camera"
        product5.price = 499.99
        product5.description = "A digital camera with high resolution"
        product5.image_url = (
            "https://images.pexels.com/photos/274973/pexels-photo-274973.jpeg"
        )

        objs = [product1, product2, product3, product4, product5]

        db.session.bulk_save_objects(objs)
        db.session.commit()
