from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'edwardelric'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""
    
    
    return render_template('home.html')


@app.route('/create')
def create_account():
    """Create Account"""
    
        
    
    return render_template('create.html')


@app.route('/landing')
def landing():
   """View landing""" 
   
   all_art = crud.get_art()
   
   return render_template('landing.html', all_art=all_art)


@app.route('/landing/<art_id>')
def show_art(art_id):
    """View art details."""
    
    art = crud.get_art_by_id(art_id)
    
    return render_template('art_info.html', art=art)


@app.route("/users", methods=['GET', 'POST'])
def register_user():
    """Create a new user."""
    

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = crud.get_user_by_email(email)
        
        if len(email) < 4:
            flash('Email must be greater than 4 characters')
            pass
        elif len (password) < 4:
            flash ('Password must be at least 4 characters')
        else:
            user = crud.create_user(email, password)
            db.session.add(user)
            db.session.commit()
            flash ('Account Creation Successful!')
            
            

    return redirect("/create")


@app.route("/login", methods=["GET","POST"])
def process_login():
    """Process user login."""
    
    email = request.form.get('email')
    password = request.form.get('password')
        
    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect")
    else:
        session["user_email"] = user.email
        flash(f"Welcome {user.email}!")

    return redirect("/")
#test /landing later with a logout redirect


@app.route("/logout", methods=["POST"])
def process_logout():
    """Process user logout."""

    logged_in_to_email = session.get("user_email")
    if logged_in_to_email is None:
        flash("You were already logged out!")
    else:
        del session["user_email"]
        flash("You're logged out!")

    return redirect("/")


@app.route("/update_quantity", methods=["POST"])
def update_quantity():
    quantity_id = request.json["quantity_id"]
    updated_amount = request.json["updated_amount"]
    crud.update_quantity(quantity_id, updated_amount)
    db.session.commit()

    return "Quantity Updated"


@app.route("/cart")
def cart():
    """Show art in cart."""
    
    get_user = crud.get_user_by_email(session.get("user_email"))
    
    cart_art = crud.get_cart_art_by_user_id(get_user.user_id)
    
    return render_template("cart.html", cart_art=cart_art)


@app.route("/wishlist")
def wishlist():
    """Show art in wishlist."""
    
    get_user = crud.get_user_by_email(session.get("user_email"))
    
    wishlist_art = crud.get_wishlist_art_by_user_id(get_user.user_id)
    
    return render_template("wishlist.html", wishlist_art=wishlist_art)


@app.route("/art/<art_id>/carts", methods=["GET","POST"])
def create_cart_item(art_id):
    """Create a new cart item."""

    logged_in_email = session.get("user_email")
    quantity_amount = request.form.get("quantity")

    if logged_in_email is None:
        flash("Log in to update quantity!")
    elif not quantity_amount:
        flash("Error: you didn't select a quantity.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        art = crud.get_art_by_id(art_id)

        cart_item = crud.create_cart_art(user.user_id, art.art_id, int(quantity_amount))
        db.session.add(cart_item)
        db.session.commit()

        flash(f" {art.art_name} has been added to your cart!")

    return redirect(f"/landing")

@app.route("/art/<art_id>/wishlist", methods=["GET","POST"])
def create_wishlist_item(art_id):
    """Create a new wishlist item."""

    logged_in_email = session.get("user_email")
    quantity_amount = request.form.get("quantity")
    
    if logged_in_email is None:
        flash("Log in to update quantity!")
    elif not quantity_amount:
        flash("Error: you didn't select a quantity.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        art = crud.get_art_by_id(art_id)


    user = crud.get_user_by_email(logged_in_email)
    art = crud.get_art_by_id(art_id)

    wishlist_item = crud.create_wishlist_art(user.user_id, art.art_id, int(quantity_amount))
    db.session.add(wishlist_item)
    db.session.commit()

    flash(f" {art.art_name} has been added to your wishlist!")

    return redirect(f"/landing")


@app.post("/carts/<art_id>/delete")
def delete_cart(art_id):
    """Empty cart."""
    
    crud.delete_cart_item(art_id)
    
    flash(f" Art has been removed")
    
    return redirect("/cart")


@app.post("/wishlist/<art_id>/delete")
def delete_wishlist(art_id):
    """Empty cart."""
    
    crud.delete_wishlist_art(art_id)
    
    flash(f" Art has been removed")
    
    return redirect("/wishlist")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)