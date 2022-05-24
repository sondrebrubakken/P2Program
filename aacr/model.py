from flask import redirect, abort, url_for
from flask_sqlalchemy import sqlalchemy
from datetime import datetime
from aacr import db, login_man, admin
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
import pymysql

#Skal inkluderes i program, der indeholder flasklogin. Linker et login med ID fra user tabellen. 
@login_man.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#User databasemodel. UserMixin kommer fra flasklogin, og siger at denne model indeholder login informationer
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    is_trainer = db.Column(db.Boolean, default=False)
    is_user = db.Column(db.Boolean, default=True)
    nyevent = db.relationship('NyEvent', backref='bruger', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

#Flask admin bruger denne for at tjekke om brugeren er en admin
class AdminControl(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)


#Rute databasemodel
class Rute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    rute = db.Column(db.String(255), nullable=False)
    dist = db.Column(db.Numeric(precision=8, scale=1), nullable=False)
    desc = db.Column(db.String(400), nullable=False)
    land = db.Column(db.Boolean, default=False)
    byen = db.Column(db.Boolean, default=False)

#Representation. Hvis klassen kaldes på, vises informationen der inkluderes i "rute" variablen
    def __repr__(self):
        return '{}'.format(self.rute)


#Event databasemodel. Hvor alle begivenheder gemmes. 
class NyEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    start = db.Column(db.Date)
    time_start = db.Column(db.Time, default=datetime.utcnow)
    time_end = db.Column(db.Time, default=datetime.utcnow)
    rute = db.Column(db.String(255), nullable=True)
    desc = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

#Adder en navigationsknap for at komme til Index siden(forsiden)
class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for("index")

#Ekskluderer passwordfelt der hedder "password" fra User modellen
class UserModelView(AdminControl):
    column_exclude_list = ('password')
    
#Bestemmer hvilke navigations muligheder flask admin siden skal have 
admin.add_view(UserModelView(User, db.session))
admin.add_view(AdminControl(NyEvent, db.session))
admin.add_view(AdminControl(Rute, db.session))
admin.add_link(MainIndexLink(name="Tilbage til forsiden"))
