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
    products = Product.query.order_by(db.func.random()).limit(3).all()
    user = None
    if "user_id" in session:
        user = User.query.get(session["user_id"])

    cart_items = 0
    if "user_id" in session:
        items = get_user_cart_items(db, session["user_id"], Cart, CartItem)
        cart_items = sum(item.quantity for item in items)

    return render_template(
        "index.html", products=products, cart_item_count=cart_items, user=user
    )


@routes.route("/products")
def products():
    cart_items = 0
    if "user_id" in session:
        items = get_user_cart_items(db, session["user_id"], Cart, CartItem)
        cart_items = sum(item.quantity for item in items)

    query = request.args.get("q", "").strip()
    if query:
        products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    else:
        products = Product.query.all()

    return render_template(
        "products.html",
        products=products,
        cart_item_count=cart_items,
        user=User.query.get(session["user_id"]) if "user_id" in session else None,
    )


@routes.route("/cart")
def cart():
    if "user_id" not in session:
        flash("Please log in to view your cart.", "warning")
        return redirect(url_for("routes.index"))

    items = get_user_cart_items(db, session["user_id"], Cart, CartItem)
    total = get_user_cart_total(db, session["user_id"], Cart, CartItem)

    return render_template(
        "cart.html",
        cart_items=items,
        cart_total=total,
        user=User.query.get(session["user_id"]) if "user_id" in session else None,
    )


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
    return redirect(url_for("routes.products"))


@routes.route("/remove_from_cart/<int:item_id>")
def remove_from_cart(item_id):
    if "user_id" not in session:
        return redirect(url_for("routes.index"))

    item = CartItem.query.get_or_404(item_id)
    if item.quantity > 1:
        item.quantity -= 1
    else:
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


@routes.route("/register_item", methods=["GET", "POST"])
def register_item():

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        image_url = request.form.get("image_url")

        if not name or not price:
            flash("Name and Price are required fields.", "danger")
            return redirect(url_for("routes.register_item"))

        try:
            price = float(price)
        except ValueError:
            flash("Invalid price format.", "danger")
            return redirect(url_for("routes.register_item"))

        new_product = Product()
        new_product.name = name
        new_product.price = price
        new_product.description = description
        new_product.image_url = image_url

        db.session.add(new_product)
        db.session.commit()

        flash("Product added successfully!", "success")
        return redirect(url_for("routes.products"))

    return render_template("register_item.html")


@routes.route("/remove_item/", methods=["GET", "POST"])
def remove_item():
    products = Product.query.all()

    if request.method == "POST":
        product_id = request.form.get("product_id")
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        flash("Product removed successfully!", "success")
        return redirect(url_for("routes.products"))

    return render_template("remove_item.html", products=products)


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
        elif User.query.count() == 0:
            flash("No users found. Please register first.", "warning")
            return redirect(url_for("routes.register"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


@routes.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("routes.index"))


# register
@routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("routes.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "warning")
            return redirect(url_for("routes.register"))

        new_user = User()
        new_user.email = email
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Create a cart for the new user
        new_cart = Cart()
        new_cart.user_id = new_user.id
        db.session.add(new_cart)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("routes.login"))

    return render_template("register.html")
