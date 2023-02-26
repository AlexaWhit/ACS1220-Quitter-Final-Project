from sqlalchemy_utils import URLType
from sqlalchemy.orm import backref 
from flask_login import UserMixin, current_user 
from datetime import datetime
from quitter_app.extensions import db
from quitter_app.utils import FormEnum

class Purpose(FormEnum):
    MOTIVATION = 'Motivation'
    FRUSTRATION = 'Frustration'
    INSPIRATION = 'Inspiration'

class ReactionEmoji(FormEnum):
    LIKE = '❤️'
    LOVE = '🥰'
    HEALTHY = '🫁'
    TEARS = '😪'
    LOL = '🤣'
    SUPPORT = '💪'
    CONGRATS = '🥳'

friend_list_table = db.Table('user_friend',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    birth_date = db.Column(db.Date)
    quit_date = db.Column(db.Date)
    avg_cigs = db.Column(db.Integer)
    about_me = db.Column(db.String(8000))
    profile_pic = db.Column(URLType)
    posts = db.relationship('Post', back_populates='created_by')
    reactions = db.relationship('Reaction', back_populates='created_by')
    friend_list = db.relationship(
        'User', secondary='user_friend',
        primaryjoin=id==friend_list_table.c.user_id,
        secondaryjoin=id==friend_list_table.c.friend_id,
        backref='friends'
    )



    def __str__(self):
        return f'<Username: {self.username}>'

    def __repr__(self):
        return f'<Username: {self.username}>'


class Post(db.Model):
    """Post model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    audience = db.Column(db.Enum(Purpose))
    body = db.Column(db.String(8000), nullable=False)
    photo_url = db.Column(db.String(8000))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_by = db.relationship('User')
    reactions = db.relationship('Reaction', back_populates='post', lazy=True)

    def __str__(self):
        return f'<Post ID & Title: {self.id} {self.title}>'

    def __repr__(self):
        return f'<Post ID & Title: {self.id} {self.title}>'

class Reaction(db.Model):
    """Reacton model."""
    id = db.Column(db.Integer, primary_key=True)
    reaction = db.Column(db.Enum(ReactionEmoji))
    comment = db.Column(db.String(8000))
    photo_url = db.Column(URLType)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='reactions')

