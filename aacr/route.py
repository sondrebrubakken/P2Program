from turtle import title
from aacr import app, bcrypt
from aacr import db
from flask import render_template, request, url_for,redirect, flash
from aacr.forms import RegistrationForm,LoginForm,AddEventForm,RuteForm, Rute
from aacr.model import NyEvent, User
from flask_login import login_user, current_user, logout_user



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cal")
def cal():
    site_events = NyEvent.query.all()
    return render_template("cal.html", title="Kalender", site_events=site_events)

@app.route("/ruter")
def ruter():
    return render_template("ruter.html", title="Ruter")

@app.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_info = User.query.filter_by(username=form.username.data).first()
        if user_info and bcrypt.check_password_hash(user_info.password, form.password.data):
            login_user(user_info)
            return redirect(url_for('index'))
        flash('Fejl med brugernavn eller kode', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        crypt_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=crypt_password)
        db.session.add(user)
        db.session.commit()
        flash("Konto Oprettet", 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Registrer", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    form = AddEventForm()
    if form.validate_on_submit():
        event = NyEvent(title=form.title.data, start=form.start.data, time_start=form.time_start.data, time_end=form.time_end.data, rute=form.rute.data, desc=form.desc.data, bruger=current_user)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('cal'))
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

@app.route('/showevent/<int:event_id>')
def show_event(event_id):
    show_event = NyEvent.query.get(event_id)
    return render_template('event_show.html', post=show_event)
