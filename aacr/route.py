from aacr import app, bcrypt
from aacr import db
from flask import render_template, request, url_for, redirect, flash, abort
from aacr.forms import RegistrationForm, LoginForm, AddEventForm, RuteForm, Rute, RuteFilter
from aacr.model import NyEvent, User
from flask_login import login_user, current_user, logout_user
from sqlalchemy import and_


@app.route("/")
def index():
    return render_template("forside.html", title="Hjem")


@app.route("/cal")
def cal():
    site_events = NyEvent.query.all()
    return render_template("cal.html", title="Kalender", site_events=site_events)


@app.route("/ruter", methods=['POST', 'GET'])
def ruter():
    ruter = Rute.query.all()
    form = RuteFilter(choice="null", distance="null")
    if form.validate_on_submit():
        if form.choice.data == "byen" and form.distance.data == "low":
            ruter = Rute.query.filter(
                and_(Rute.byen == "t", Rute.dist <= 50)).all()
        elif form.choice.data == "byen" and form.distance.data == "high":
            ruter = Rute.query.filter(
                and_(Rute.byen == "t", Rute.dist >= 50)).all()
        elif form.choice.data == "land" and form.distance.data == "low":
            ruter = Rute.query.filter(
                and_(Rute.land == "t", Rute.dist <= 50)).all()
        elif form.choice.data == "land" and form.distance.data == "high":
            ruter = Rute.query.filter(
                and_(Rute.land == "t", Rute.dist >= 50)).all()
        elif form.choice.data == "byen":
            ruter = Rute.query.filter(Rute.byen == "t").all()
        elif form.choice.data == "land":
            ruter = Rute.query.filter(Rute.land == "t").all()
        elif form.distance.data == "low":
            ruter = Rute.query.filter(Rute.dist <= 50).all()
        elif form.distance.data == "high":
            ruter = Rute.query.filter(Rute.dist >= 50).all()
        return render_template("ruter.html", form=form, ruter=ruter)
    return render_template("ruter.html", title="Ruter", form=form, ruter=ruter)


@app.route("/login", methods=['POST', 'GET'])
def login():
    # Tjekker cookies for at se om bruger allerede er logget ind.
    # Hvis bruger er logget ind, hopper programmet videre til linje 32
    if current_user.is_authenticated:
        # Hvis bruger er logget ind, bliver de videresendt til index funktionen(linje 11)
        return redirect(url_for('index'))
    # Variabel "form" bliver lavet og linket til LoginFormen. Den kan nu bruges i denne funktion.
    form = LoginForm()
    # Hvis formen godkendes, n??r der trykkes submit, bliver linjer 37-41 udf??rt.
    if form.validate_on_submit():
        # "user_info" variabelen bliver lavet. Den bliver linket til funktionen,
        # der leder igennem databasen efter brugernavnet som brugeren har skrevet ind, i LoginFormen.
        # Den v??lger det f??rste(og eneste) brugernavn, der samsvarer,
        # med brugerens input. Hvis der ikke er et brugernevn, er variabelen ikke gyldig.
        user_name = User.query.filter_by(username=form.username.data).first()
        # Linje 42-43 bliver udf??rt kun hvis user_info giver et brugernavn,
        # og Bcrypts password hash samsvarer med koden brugeren har skrevet ind.
        if user_name and bcrypt.check_password_hash(user_name.password, form.password.data):
            # Funktion
            login_user(user_name)
            flash(f'Bruger "{current_user.username}" loggede ind!','success')
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
    # Hvis formen godkendes, n??r der trykkes submit, bliver linjer 50-56 udf??rt.
    if form.validate_on_submit():
        # laver en variabel "crypt_password"
        # bcrypt tager inputtet fra password feltet, og ovskriver koden til en 16-bit string
        crypt_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # Variabel "user" bliver linket til User databasen.
        # "username=" siger at den kommende info skal gemmes i username kolonnen i User tabellen.
        # "form.username.data" er dataen, som brugeren skriver ind i Registeringsformen, under Username feltet.
        # password=crypt_password gemmer crypt_password variabelen i password kolonnen i User tabellen.
        user = User(username=form.username.data,
                    email=form.email.data, password=crypt_password)
        # Tilf??jer user variabelen til User tabellen.
        # Username, email og password input bliver lagt ind, i databasen.
        db.session.add(user)
        # ??ndringer gemmes
        db.session.commit()
        # Besked vises kun en gang, efter en succesfuld registrering.
        flash("Konto Oprettet", 'success')
        # Sender brugeren videre til login funktionen.
        return redirect(url_for('login'))
    # Titelen til siden bliver sat til Registerer.
    # Registereringsformen bliver sendt til register.html, s??dan at brugeren kan se og udfylde.
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
            flash(f'Event Oprettet p?? Dato: {event.start}','success')
            return redirect(url_for('cal'))
    return render_template('add_event.html', title='Add Event', form=form, legend="Opret Event")


@app.route('/nyrute', methods=['POST', 'GET'])
def nyrute():
    if current_user.is_admin or current_user.is_trainer:
        form = RuteForm()
        if form.validate_on_submit():
            ruter = Rute(rute=form.rute.data, name=form.name.data, desc=form.desc.data,
                         dist=form.dist.data, land=form.land.data, byen=form.byen.data)
            db.session.add(ruter)
            db.session.commit()
            flash('Rute oprettet', 'success')
            return redirect(url_for('ruter'))
    return render_template('nyrute.html', title="Nye ruter", form=form)


@app.route('/showevent/<int:event_id>')
def show_event(event_id):
    show_event = NyEvent.query.get_or_404(event_id)
    return render_template('event_show.html', post=show_event)


@app.route('/showevent/<int:event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    event = NyEvent.query.get_or_404(event_id)
    if event.bruger == current_user or current_user.is_admin:
        form = AddEventForm()
        if form.validate_on_submit():
            event.title = form.title.data
            event.start = form.start.data
            event.time_start = form.time_start.data
            event.time_end = form.time_end.data
            event.rute = form.rute.data
            event.desc = form.desc.data
            db.session.commit()
            flash('Begivenhed Opdateret', 'success')
            return redirect(url_for('show_event', event_id=event_id))
        elif request.method == 'GET':
            form.title.data = event.title
            form.start.data = event.start
            form.time_start.data = event.time_start
            form.time_end.data = event.time_end
            form.rute.data = event.rute
            form.desc.data = event.desc
    else:
        abort(404)
    return render_template('add_event.html', title='Edit Event', form=form, legend="Rediger Event")


@app.route('/showevent/<int:event_id>/delete', methods=['GET', 'POST'])
def delete_event(event_id):
    event = NyEvent.query.get_or_404(event_id)
    if event.bruger == current_user or current_user.is_admin:
        db.session.delete(event)
        db.session.commit()
        flash('Begivenhed slettet', 'success')
    else:
        abort(404)
    return redirect(url_for('cal'))
