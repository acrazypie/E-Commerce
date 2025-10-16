from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_online = db.Column(db.Boolean, default=False)
    oauth_provider = db.Column(db.String, nullable=True)
    oauth_id = db.Column(db.String, nullable=True)

    carts = db.relationship("Cart", backref="user", lazy=True)

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def check_admin(self) -> bool:
        return self.is_admin

    def check_online(self) -> bool:
        return self.is_online


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)


class CartItem(db.Model):
    __tablename__ = "cart_item"
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship("Product", lazy=True)
    cart = db.relationship("Cart", back_populates="items")


class Cart(db.Model):
    __tablename__ = "cart"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    items = db.relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )


# funzioni per gestire il carrello
def get_user_cart(db: SQLAlchemy, user_id, Cart):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    return cart


def get_user_cart_items(db: SQLAlchemy, user_id, Cart, CartItem):
    cart = get_user_cart(db, user_id, Cart)
    item_list = CartItem.query.filter_by(cart_id=cart.id).all()
    if not item_list:
        return []
    return item_list


def get_user_cart_total(db: SQLAlchemy, user_id, Cart, CartItem):
    items = get_user_cart_items(db, user_id, Cart, CartItem)
    total = sum(item.product.price * item.quantity for item in items)
    total = round(total, 2)
    return total
