from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField, TextAreaField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, Length, ValidationError, URL
from quitter_app.models import User, Post, Reaction, Purpose, ReactionEmoji
from quitter_app.extensions import bcrypt

class UserForm(FlaskForm):
    """Form for updating a user."""

    username = StringField('User Name')
    password = PasswordField('Password')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    birth_date = DateField('Date of Birth')
    quit_date = DateField('Quit Date')
    avg_cigs = IntegerField('Average Cigs')
    about_me = TextAreaField('About Me')
    profile_pic = StringField('Profile Picture', validators=[URL()])
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')


class PostForm(FlaskForm):
    """Form for adding/updating a user's post."""

    title = StringField('Post Title', validators=[DataRequired()])
    audience = SelectField('Purpose', choices=Purpose.choices())
    body = TextAreaField('Body', validators=[DataRequired()])
    photo_url = StringField('Photo/GIF')
    submit = SubmitField('Submit Post')
    delete = SubmitField('Delete Post')

class ReactionForm(FlaskForm):
    """Form for adding/updating a reaction."""

    reaction = SelectField('Reaction', choices=ReactionEmoji.choices())
    comment = StringField('Comment')
    photo_url = StringField('Photo/GIF')
    submit = SubmitField('Submit Reaction')
    delete = SubmitField('Delete Reaction')
