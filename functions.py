from flask_sqlalchemy import SQLAlchemy


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
    return total
