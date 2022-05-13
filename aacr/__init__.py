from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
import pymysql


app = Flask(__name__)
app.config['SECRET_KEY'] = "1233333"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ivchxmmvffrlut:976510306967a03e03384de004403d92333bad9cde9d098eeba62c72b854012c@ec2-3-224-164-189.compute-1.amazonaws.com:5432/df4ejaolpl201o'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_man = LoginManager(app)
admin = Admin(app)
login_man.login_view = "login"
login_man.login_message_category = "info"


from aacr import route