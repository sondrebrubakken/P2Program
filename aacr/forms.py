from email.policy import default
from tokenize import String
from unicodedata import name
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField, ValidationError, FloatField, DecimalField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_components import TimeField
from werkzeug.datastructures import MultiDict
from aacr.model import User, Rute


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=30)], render_kw={
        'placeholder': 'Brugernavn...'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={
        'placeholder': 'Email...'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
        'placeholder': 'Password...'})
    password_confirm = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')], render_kw={
        'placeholder': 'Password...'})
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
    username = StringField('Username', validators=[DataRequired(), Length(
        min=3, max=30)], render_kw={'placeholder': 'Indtast brugernavn her...'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
                             'placeholder': 'Indtast kodeord her...'})
    husk_mig = BooleanField('Husk Mig!')
    submit = SubmitField('Log Ind')


# Input-form som bruger kan se, når de opretter en rute. DataRequired betyder at det skal fyldes ud

class RuteForm(FlaskForm):
    name = StringField('Rute Navn', validators=[DataRequired()], render_kw={
                       'placeholder': 'Rutenavn...'})
    rute = TextAreaField('Frame Link', validators=[DataRequired()], render_kw={
                         'placeholder': 'iFrame embed link...'})
    dist = DecimalField('Distance(km)', validators=[DataRequired()], render_kw={
                        'placeholder': 'Distance...'})
    desc = TextAreaField('Beskrivelse', validators=[
                         DataRequired(), Length(min=3, max=400)], render_kw={
        'placeholder': 'Beskrivelse...'})
    land = BooleanField('Landevejsrute', render_kw={'value': 1}, default=False)
    byen = BooleanField('Byrute', render_kw={'value': 1}, default=False)
    submit = SubmitField('Submit')


def GetRute():
    return Rute.query


class AddEventForm(FlaskForm):
    title = StringField('Titel', validators=[
                        DataRequired(), Length(min=3, max=30)], render_kw={
        'placeholder': 'Titel...'})
    start = DateField('Dato', validators=[DataRequired()])
    time_start = TimeField('Start Tidpunkt', format='%H:%M',
                           validators=[DataRequired()])
    time_end = TimeField('Slut Tidpunkt', format='%H:%M',
                         validators=[DataRequired()])
    rute = QuerySelectField(
        'Vælg en rute', query_factory=GetRute, allow_blank=True, get_label='name', render_kw={
            'placeholder': 'Vælg rute:'})
    desc = TextAreaField('Beskrivelse', validators=[
                         DataRequired(), Length(min=3, max=300)], render_kw={
                             'placeholder': 'Rute beskrivelse...'})
    submit = SubmitField('Opret')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RuteFilter(FlaskForm):
    choice = SelectField("Terreng:", choices=[('null', 'Vælg Terreng'),
                                              ('byen', 'Byen'), ('land', 'Landevej')], validate_choice=False)
    distance = SelectField("Distance:", choices=[('null', 'Vælg Distance'),
                           ('low', '>50'), ('high', '<50')], validate_choice=False)
    submit = SubmitField('Søg')
