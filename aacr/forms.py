from tokenize import String
from unicodedata import name
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_components import TimeField
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
    title = StringField('Titel', validators=[DataRequired(), Length(min=3,max=30)])
    start = DateField('Dato', validators=[DataRequired()])
    time_start = TimeField('Start Tidpunkt', validators=[DataRequired()])
    time_end = TimeField('Slut Tidpunkt', validators=[DataRequired()])
    rute = QuerySelectField('Vælg en rute', query_factory=GetRute, allow_blank=True, get_label=name)
    desc = TextAreaField('Beskrivelse', validators=[DataRequired(), Length(min=3,max=300)])
    submit = SubmitField('Tilføj Event')

class RuteForm(FlaskForm):
    name = StringField('Rute Navn', validators=[DataRequired()])
    rute = StringField('Frame Link', validators=[DataRequired()])
    submit = SubmitField('Submit')
