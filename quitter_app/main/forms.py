from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField, TextAreaField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, Length, ValidationError, Email, URL
from quitter_app.models import User, Post, Reaction, Purpose, ReactionEmoji
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
    avg_cigs = IntegerField('Average Cigs', validators=[DataRequired()])
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
