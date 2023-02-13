from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, URL, Email
from quitter_app.models import User
from quitter_app.extensions import *


class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[Email(), DataRequired()])
    birth_date = DateField('Date of Birth', validators=[DataRequired()])
    quit_date = DateField('Quit Date', validators=[DataRequired()])
    avg_cigs = IntegerField('Average Cigarettes Smoked per Day', validators=[DataRequired()])
    about_me = TextAreaField('About Me')
    profile_pic = StringField('Profile Picture')
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')