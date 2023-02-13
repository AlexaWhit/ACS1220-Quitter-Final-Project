from sqlalchemy_utils import URLType
from sqlalchemy.orm import backref 
from flask_login import UserMixin, current_user 
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

friends = db.Table('friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Friend(db.Model):
    """Friend model."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=[user_id], back_populates='friends')
    friend = db.relationship('User', foreign_keys=[friend_id], back_populates='friend_of')

    def __str__(self):
        return f'<Friendship between {self.user.username} and {self.friend.username}>'

    def __repr__(self):
        return f'<Friendship between {self.user.username} and {self.friend.username}>'

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
    friends = db.relationship('Friend', foreign_keys=[Friend.user_id], back_populates='user')
    friend_of = db.relationship('Friend', foreign_keys=[Friend.friend_id], back_populates='friend')


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
    photo_url = db.Column(URLType)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    # post = db.relationship('User', back_populates='posts')

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
    # post_reactions = db.relationship('Post', secondary='User', back_populates='posts')

    def __str__(self):
        return f'<Photo ID & Title: {self.id} {self.title}>'

    def __repr__(self):
        return f'<Photo ID & Title: {self.id} {self.title}>'
