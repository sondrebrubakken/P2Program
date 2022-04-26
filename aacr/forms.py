from tokenize import String
from unicodedata import name
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from aacr.model import User, Rute



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3,max=30)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Opret Konto')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3,max=30)], render_kw={'placeholder':'Indtast brugernavn her...'})
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log Ind')

def GetRute():
    return Rute.query


class AddEvent(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3,max=30)])
    start = DateField('Start', validators=[DataRequired()])
    route = QuerySelectField('Vælg en rute', query_factory=GetRute, allow_blank=True, get_label=name)
    end = DateField('End', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired(), Length(min=3,max=300)])

