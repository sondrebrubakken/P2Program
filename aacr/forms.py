from email.policy import default
from tokenize import String
from unicodedata import name
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField, ValidationError
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

    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Brugernavn allerede i brug")
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email allerede i brug")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3,max=30)], render_kw={'placeholder':'Indtast brugernavn her...'})
    password = PasswordField('Password', validators=[DataRequired()])
    husk_mig = BooleanField('Husk Mig!')
    submit = SubmitField('Log Ind')

class RuteForm(FlaskForm):
    name = StringField('Rute Navn', validators=[DataRequired()])
    rute = StringField('Frame Link', validators=[DataRequired()])
    submit = SubmitField('Submit')


def GetRute():
    return Rute.query

class AddEventForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired(), Length(min=3,max=30)])
    start = DateField('Dato', validators=[DataRequired()])
    time_start = TimeField('Start Tidpunkt', format='%H:%M', validators=[DataRequired()])
    time_end = TimeField('Slut Tidpunkt', format='%H:%M', validators=[DataRequired()])
    rute = QuerySelectField('Vælg en rute', query_factory=GetRute, allow_blank=True, get_label='name')
    desc = TextAreaField('Beskrivelse', validators=[DataRequired(), Length(min=3,max=300)])
    submit = SubmitField('Tilføj Event')

