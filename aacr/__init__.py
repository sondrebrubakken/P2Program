from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
import pymysql

#Initializer flask appen
app = Flask(__name__)
#Laver en connection imellem programmet og databasen
app.config['SECRET_KEY'] = "1233333"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/projekt'
#Initialiserer databasen
db = SQLAlchemy(app)
#Initialiserer bcrypt
bcrypt = Bcrypt(app)
#Initialiserer Flask login
login_man = LoginManager(app)
#Initialiserer Flask Admin
admin = Admin(app)
login_man.login_view = "login"
login_man.login_message_category = "info"


from aacr import route