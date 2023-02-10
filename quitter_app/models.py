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

class User(UserMixin, db.Model):
    """Grocery Store model."""
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
    profie_pic = db.Column(URLType)
    # posts = db.relationship('GroceryItem', back_populates='store')

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
    """Photo model."""
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

