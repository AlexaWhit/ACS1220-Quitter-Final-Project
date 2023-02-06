from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, Length, ValidationError, Email
from quitter_app.models import *
from quitter_app.extensions import bcrypt

class UserForm(FlaskForm):
    """Form for adding/updating a user."""

    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Post Title', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    birth_date = DateField('Date of Birth', validators=[DataRequired()])
    quit_date = DateField('Quit Date', validators=[DataRequired()])
    about_me = StringField('About Me')
    profie_pic = StringField('Profile Picture', validators=[URL()])
    submit = SubmitField('Submit Post')
    delete = SubmitField('Delete Post')

class PostForm(FlaskForm):
    """Form for adding/updating a user's post."""

    title = StringField('Post Title', validators=[DataRequired()])
    type = SelectField('Purpose', choices=Purpose.choices())
    body = StringField('Body', validators=[DataRequired()])
    user_id = StringField('Photo', validators=[URL()])
    user = db.relationship('User', back_populates='posts')
    submit = SubmitField('Submit Post')
    delete = SubmitField('Delete Post')

class PhotoForm(FlaskForm):
    """Form for adding/updating a photo."""

    title = StringField('title', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    type = SelectField('Purpose', choices=Purpose.choices())
    photo_url = StringField('Photo', validators=[DataRequired()])
    # user_tags = QuerySelectField('User Tags', query_factory=lambda: user.query)
    submit = SubmitField('Submit')
    delete = SubmitField('Delete Item')

# forms.py

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

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
