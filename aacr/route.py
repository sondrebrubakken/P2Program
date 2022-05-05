from turtle import title
from aacr import app, bcrypt
from aacr import db
from flask import render_template, request, url_for, redirect, flash
from aacr.forms import RegistrationForm, LoginForm, AddEventForm, RuteForm, Rute
from aacr.model import NyEvent, User
from flask_login import login_user, current_user, logout_user


@app.route("/")
def index():
    return render_template("index.html", title="Hjem")


@app.route("/cal")
def cal():
    site_events = NyEvent.query.all()
    return render_template("cal.html", title="Kalender", site_events=site_events)


@app.route("/ruter")
def ruter():
    ruter = Rute.query.all()
    return render_template("ruter.html", title="Ruter", ruter=ruter)


@app.route("/login", methods=['POST', 'GET'])
def login():
    # Tjekker cookies for at se om bruger allerede er logget ind.
    # Hvis bruger er logget ind, hopper programmet videre til linje 32
    if current_user.is_authenticated:
        # Hvis bruger er logget ind, bliver de videresendt til index funktionen(linje 11)
        return redirect(url_for('index'))
    # Variabel "form" bliver lavet og linket til LoginFormen. Den kan nu bruges i denne funktion.
    form = LoginForm()
    # Hvis formen godkendes, når der trykkes submit, bliver linjer 37-41 udført.
    if form.validate_on_submit():
        # "user_info" variabelen bliver lavet. Den bliver linket til funktionen, der leder igennem databasen efter brugernavnet som brugeren har skrevet ind, i LoginFormen.
        # Den vælger det første(og eneste) brugernavn, der samsvarer, med brugerens input. Hvis der ikke er et brugernevn, er variabelen ikke gyldig.
        user_info = User.query.filter_by(username=form.username.data).first()
        # Linje 42-43 bliver udført kun hvis user_info giver et brugernavn, og Bcrypts password hash samsvarer med koden brugeren har skrevet ind.
        if user_info and bcrypt.check_password_hash(user_info.password, form.password.data):
            #Funktion 
            login_user(user_info)
            return redirect(url_for('index'))
        flash('Fejl med brugernavn eller kode', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    # Variabel "form" bliver lavet og linket til RegistreringsFormen. Den kan nu bruges i denne funktion.
    form = RegistrationForm()
    # Tjekker cookies for at se om bruger allerede er logget ind.
    # Hvis bruger er logget ind, hopper programmet videre til linje 47
    if current_user.is_authenticated:
        # Hvis bruger er logget ind, bliver de videresendt til index funktionen(linje 11)
        return redirect(url_for('index'))
    # Hvis formen godkendes, når der trykkes submit, bliver linjer 50-56 udført.
    if form.validate_on_submit():
        # laver en variabel "crypt_password" hvor bcrypt tager inputtet fra password feltet, og genererer et "crypteret password"
        crypt_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # Variabel "user" bliver linket til User databasen. "username=" siger at den kommende info skal gemmes i username kolonnen i User tabellen.
        # "form.username.data" er dataen, som brugeren skriver ind i Registeringsformen, under Username feltet.
        # password=crypt_password gemmer crypt_password variabelen i password kolonnen i User tabellen.
        user = User(username=form.username.data,
                    email=form.email.data, password=crypt_password)
        # Tilføjer user variabelen til User tabellen. Username, email og password input bliver lagt ind, i databasen.
        db.session.add(user)
        # Ændringer gemmes
        db.session.commit()
        # Besked vises kun en gang, efter en succesfuld registrering.
        flash("Konto Oprettet", 'success')
        # Sender brugeren videre til login funktionen.
        return redirect(url_for('login'))
    # Titelen til siden bliver sat til Registerer. Registereringsformen bliver sendt til register.html, sådan at brugeren kan se og udfylde.
    return render_template("register.html", title="Registrer", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add_event', methods=["GET", "POST"])
def add_event():
    if current_user.is_admin or current_user.is_trainer:
        form = AddEventForm()
        if form.validate_on_submit():
            event = NyEvent(title=form.title.data, start=form.start.data, time_start=form.time_start.data,
                            time_end=form.time_end.data, rute=form.rute.data, desc=form.desc.data, bruger=current_user)
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('cal'))
    return render_template('add_event.html', title='Add Event', form=form)


@app.route('/nyrute', methods=['POST', 'GET'])
def nyrute():
    if current_user.is_admin or current_user.is_trainer:
        form = RuteForm()
        if form.validate_on_submit():
            ruter = Rute(rute=form.rute.data, name=form.name.data, desc=form.desc.data,
                         dist=form.dist.data, land=form.land.data, byen=form.byen.data)
            db.session.add(ruter)
            db.session.commit()
            return redirect(url_for('nyrute'))
    return render_template('nyrute.html', title="Nye ruter", form=form)


@app.route('/showevent/<int:event_id>')
def show_event(event_id):
    show_event = NyEvent.query.get(event_id)
    return render_template('event_show.html', post=show_event)
