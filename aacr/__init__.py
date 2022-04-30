from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = "1233333"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/projekt'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_man = LoginManager(app)
login_man.login_view = "login"
login_man.login_message_category = "info"



from aacr import route