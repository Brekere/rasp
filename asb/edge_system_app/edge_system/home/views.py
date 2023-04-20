from flask import Blueprint, render_template, abort


home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    return render_template("home/home.html")