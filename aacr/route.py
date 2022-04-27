from turtle import title
from aacr import app
from aacr import db
from flask import render_template, request, url_for,redirect
from aacr.forms import RegistrationForm,LoginForm,AddEvent,RuteForm, Rute
from aacr.model import NyEvent


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
#    if form.validate_on_submit():
#        event = NyEvent(title=form.title.data, start=form.start.data, time_start=form.time_start.data, time_end=form.time_end.data, rute=form.rute.data, desc=form.desc.data)
#        db.session.add(event)
#        db.session.commit()
#        return redirect(url_for('cal'))
    return render_template('add_event.html', title='Add Event', form=form)


@app.route('/nyrute', methods=['POST', 'GET'])
def nyrute():
    form = RuteForm()
    ruter = Rute.query.order_by(Rute.id)
    if form.validate_on_submit():
        ruter = Rute(rute=form.rute.data, name=form.name.data)
        db.session.add(ruter)
        db.session.commit()
        return redirect(url_for('nyrute'))
    return render_template('nyrute.html', title="Nye ruter", form=form, ruter=ruter)
