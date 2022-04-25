from turtle import title
from flask import render_template, url_for
from aacr import app
from aacr.forms import RegistrationForm,LoginForm

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cal")
def cal():
    return render_template("cal.html", title="Kalender")

@app.route("/routes")
def routes():
    return render_template("routes.html", title="Ruter")

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", title="Registrer", form=form)