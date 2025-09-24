from flask import Flask, flash, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

# My imports
from functions import get_user_cart, get_user_cart_items, get_user_cart_total
from database import populate_db_test


# Start app and db
app = Flask(__name__)
app.secret_key = "your_secret_key"
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)
db_path = DB_DIR / "ecommerce.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Classes
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    carts = db.relationship("Cart", backref="user", lazy=True)

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.set_password(password)
        super().__init__()

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)

    def __repr__(self) -> str:
        return f"<Product {self.name} - ${self.price}>"

    def __init__(
        self, name: str, price: float, description: str, image_url: str
    ) -> None:
        self.name = name
        self.price = price
        self.description = description
        self.image_url = image_url
        super().__init__()


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship("Product", lazy=True)
    cart = db.relationship("Cart", back_populates="items")

    def __repr__(self) -> str:
        return f"<CartItem {self.product_id} x {self.quantity}>"

    def __init__(self, cart_id: int, product_id: int, quantity: int) -> None:
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity
        super().__init__()


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    items = db.relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Cart {self.id} for User {self.user_id}>"

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__()


# Test data population
with app.app_context():
    db.create_all()
    populate_db_test(db, User, Product)


# Routes
@app.route("/")
def index():
    products = Product.query.limit(3).all()
    return render_template("index.html", products=products)


@app.route("/products")
def products():
    products = Product.query.all()
    return render_template("products.html", products=products)


@app.route("/cart")
def cart():
    if "user_id" not in session:
        flash("Please log in to view your cart.", "warning")
        return redirect(url_for("index"))

    items = get_user_cart_items(db, session["user_id"], Cart, CartItem)
    total = get_user_cart_total(db, session["user_id"], Cart, CartItem)

    return render_template("cart.html", cart_items=items, cart_total=total)


@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if "user_id" not in session:
        flash("Please log in to add items to your cart.", "warning")
        return redirect(url_for("index"))

    cart = get_user_cart(db, session["user_id"], Cart)
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()

    if item:
        item.quantity += 1
    else:
        new_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=1)
        db.session.add(new_item)

    db.session.commit()
    flash("Item added to cart!", "success")
    return redirect(url_for("cart"))


@app.route("/remove_from_cart/<int:item_id>")
def remove_from_cart(item_id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    item = CartItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    flash("Item removed from cart", "info")
    return redirect(url_for("cart"))


@app.route("/checkout")
def checkout():
    if "user_id" not in session:
        return redirect(url_for("index"))
    flash("Checkout is under construction 🚧", "info")
    return redirect(url_for("cart"))


# Auth routes
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        session["user_id"] = user.id
        flash("Login successful!", "success")
        return redirect(url_for("index"))
    else:
        flash("Invalid email or password", "danger")
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("index"))


# Run App
if __name__ == "__main__":
    app.run(debug=True)
