import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    
    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    
    @classmethod
    def create(cls, email, password):
        
        return cls(email=email, password=password)
    
class Art(db.Model):
    
    __tablename__ = 'art'
    
    art_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    art_name = db.Column(db.String)
    description = db.Column(db.Text)
    price = db.Column(db.String)
    image_path = db.Column(db.String)
    
    def __repr__(self):
        return f'Art art_id={self.art_id} art_name{self.art_name}>'
    
    
    
class Cart(db.Model):
    
    __tablename__ = 'carts'
    
    cart_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    quantity = db.Column(db.Integer)
    art_id = db.Column(db.Integer, db.ForeignKey('art.art_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    user = db.relationship('User', backref='carts')
    art = db.relationship('Art', backref='carts')

    
    def __repr__(self):
        return f'Cart cart_id={self.cart_id} quantity={self.quantity} art_id={self.art_id} user_id={self.user_id}>'


class Wishlist(db.Model):
    
    __tablename__ = 'wishlists'
    
    wishlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey('art.art_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    
    user = db.relationship('User', backref='wishlists' )
    art = db.relationship('Art', backref='art')
    

    def __repr__(self):
        return f'<Wishlist wishlist_id={self.wishlist_id} art_id={self.art_id} user_id={self.user_id}>'
    
    

def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    
    connect_to_db(app, echo=False)
    
    
    
    