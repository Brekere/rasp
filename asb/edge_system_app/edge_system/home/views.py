from flask import Blueprint, render_template, abort
from flask_login import login_required


home = Blueprint('home', __name__)

@home.before_request  # con esto, esta función se ejecuta antes de cada endpoint que tengamos definido en este documento
@login_required
def constructor():
   pass

@home.route('/')
def home_page():
    return render_template("home/home.html")