from model import db, User, Art, Cart, Wishlist, connect_to_db

def create_user(email, password):
    
    user = User(email=email, password=password)
    return user

def get_user():
    
    return User.query.all()

def get_user_by_id(user_id):
    
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()



def create_art(art_name, image_path, description, price):
    art = Art(
        art_name=art_name,
        image_path=image_path,
        description=description,
        price=price,
    )
    return art

def get_art():
    
    return Art.query.all()

def get_art_by_id(art_id):
    
    return Art.query.get(art_id)

def get_art_by_id(art_id):
    art = Art.query.get(art_id())
    return art


def create_cart_art(user_id, art_id, quantity):
    cart = Cart(
        user_id=user_id,
        art_id=art_id,
        quantity=quantity,
    )
    return cart

def get_cart_art_by_user_id(user_id):
    return Cart.query.filter(Cart.user_id == user_id).all()

def get_cart_by_cart_id(cart_id):
    cart_session = Cart.query.get(cart_id)
    return cart_session

def delete_cart_item(art_id):
    cart_art = Cart.query.get(art_id)
    db.session.delete(cart_art)
    db.session.commit()
    
    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)
