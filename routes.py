from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from models import db, User, Product, Cart, CartItem
from models import get_user_cart, get_user_cart_items, get_user_cart_total

routes = Blueprint("routes", __name__)


@routes.route("/")
def index():
    products = Product.query.limit(3).all()
    return render_template("index.html", products=products)


@routes.route("/products")
def products():
    query = request.args.get("q", "").strip()
    if query:
        products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    else:
        products = Product.query.all()
    return render_template("products.html", products=products)


@routes.route("/cart")
def cart():
    if "user_id" not in session:
        flash("Please log in to view your cart.", "warning")
        return redirect(url_for("routes.index"))

    items = get_user_cart_items(db, session["user_id"], Cart, CartItem)
    total = get_user_cart_total(db, session["user_id"], Cart, CartItem)

    return render_template("cart.html", cart_items=items, cart_total=total)


@routes.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if "user_id" not in session:
        flash("Please log in to add items to your cart.", "warning")
        return redirect(url_for("routes.index"))

    cart = get_user_cart(db, session["user_id"], Cart)
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()

    if item:
        item.quantity += 1
    else:
        new_item = CartItem()
        new_item.cart_id = cart.id
        new_item.product_id = product_id
        new_item.quantity = 1
        db.session.add(new_item)

    db.session.commit()
    flash("Item added to cart!", "success")
    return redirect(url_for("routes.cart"))


@routes.route("/remove_from_cart/<int:item_id>")
def remove_from_cart(item_id):
    if "user_id" not in session:
        return redirect(url_for("routes.index"))

    item = CartItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()

    flash("Item removed from cart", "info")
    return redirect(url_for("routes.cart"))


@routes.route("/checkout")
def checkout():
    if "user_id" not in session:
        return redirect(url_for("routes.index"))
    flash("Checkout is under construction 🚧", "info")
    return redirect(url_for("routes.cart"))


# login e logout
@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("routes.index"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


@routes.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("routes.index"))
