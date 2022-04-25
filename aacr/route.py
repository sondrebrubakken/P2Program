from turtle import title
from flask import render_template
from aacr import app

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
    return render_template("login.html", title="Login")