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


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

        
#####______######_______######_____#######   


@app.route("/login", methods=["GET","POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")


    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was not valid.")
    else:
        session["user_email"] = user.email
        flash(f"You're logged in as {user.email}!")

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)