from sqlalchemy_utils import URLType
from sqlalchemy.orm import backref 
from quitter_app.extensions import db
from quitter_app.utils import FormEnum

class Purpose(FormEnum):
    MOTIVATION = 'Motivation'
    FRUSTRATION = 'Frustration'
    INSPIRATION = 'Inspiration'

class User(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    birth_date = db.Column(db.Date)
    quit_date = db.Column(db.Date)
    about_me = db.Column(db.String(200))
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
    author = db.Column(db.String(200), nullable=False)
    type = db.Column(db.Enum(Purpose))
    photo_url = db.Column(URLType)
    user = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    post = db.relationship('User', back_populates='posts')

    def __str__(self):
        return f'<Post ID & Title: {self.id} {self.title}>'

    def __repr__(self):
        return f'<Post ID & Title: {self.id} {self.title}>'

class Photo(db.Model):
    """Photo model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    photo_url = db.Column(URLType)
    photos = db.relationship('Post', secondary='User', back_populates='posts')

    def __str__(self):
        return f'<Photo ID & Title: {self.id} {self.title}>'

    def __repr__(self):
        return f'<Photo ID & Title: {self.id} {self.title}>'

class Reaction(db.Model):
    """Reaction model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False, unique=True)
    # books = db.relationship('Book', secondary='favorite_book', back_populates='users')

    def __str__(self):
        return f'<User: {self.username}>'

    def __repr__(self):
        return f'<User: {self.username}>'

class Tracker(db.Model):
    """Quitter Tracker  model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False, unique=True)
    # books = db.relationship('Book', secondary='favorite_book', back_populates='users')

    def __str__(self):
        return f'<Quitter Tracker: {self.id}>'

    def __repr__(self):
        return f'<Quitter Tracker: {self.id}>'