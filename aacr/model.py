from flask_sqlalchemy import sqlalchemy
from datetime import datetime
from aacr import db
import pymysql


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(55), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"


class Rute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable = False)
    rute = db.Column(db.String(255), nullable = False)



    def __repr__(self):
        return '{}'.format(self.rute)
    



class NyEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable = False)
    start = db.Column(db.Date)
    time_start = db.Column(db.DateTime, default=datetime.utcnow)
    time_end = db.Column(db.DateTime,default=datetime.utcnow)
    rute = db.Column(db.String(255), nullable = False)
    desc = db.Column(db.String(255), nullable = False)
