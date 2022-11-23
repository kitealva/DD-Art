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
    
    
    return render_template('homepage.html')



@app.route('/landing')
def landing():
   """View landing""" 
   
   
   return render_template('landing.html')