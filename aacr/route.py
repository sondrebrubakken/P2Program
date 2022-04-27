from turtle import title
from aacr import app
from aacr import db
from flask import render_template, request, url_for
from aacr.forms import RegistrationForm,LoginForm,AddEvent


events = [
    {
        'title' : 'Træning',
        'start' : '2022-04-26',
        'end' : '2022-04-26'
    }
]



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cal")
def cal():
    return render_template("cal.html", title="Kalender", events=events)

@app.route("/ruter")
def ruter():
    return render_template("ruter.html", title="Ruter")

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", title="Registrer", form=form)

@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    form = AddEvent()
    if request.method == "POST":
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']

        if end == '':
            end=start
        events.append({
            'title' : title,
            'start' : start,
            'end' : end
        },
        )
    return render_template('add_event.html', title='Add Event', form=form)
