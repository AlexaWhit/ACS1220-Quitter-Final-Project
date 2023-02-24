import os
from unittest import TestCase
import app
from datetime import date
from quitter_app.extensions import app, db, bcrypt
from quitter_app.models import User, Post, Reaction

"""
Run these tests with the command:
python3 -m unittest quitter_app.auth.tests
"""

#################################################
# Setup
#################################################

def create_post():
    post = Post(
        title='100 Days',
        audience='Motivation',
        body='I made it to 100 days! I feel fantastic! We can all do this!',
        photo_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjDT__CUEh4j_OttSSFoNNX7lL7Bzff8etWw&usqp=CAU',
    )
    db.session.add(post)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        post_data = {
            'username': 'AlexaWhitney',
            'password': 'test'
        } 
        self.app.post('/signup', data=post_data)

        response = self.app.get('/profile/AlexaWhitney')
        response_text = response.get_data(as_text=True)
        self.assertIn('AlexaWhitney', response_text)

    def test_signup_existing_user(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password',
        } 
        response = self.app.post('/signup', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('That username is taken. Please choose a different one.', response_text)


    def test_login_correct_password(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password',
        } 
        self.app.post('/login', data=post_data)

        # - Check that the "login" button is not displayed on the homepage
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertNotIn('login', response_text)

    def test_login_nonexistent_user(self):
        post_data = {
            'username': 'PeytonManning',
            'password': 'Broncos',
        }
        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('No user with that username. Please try again.', response_text)

    def test_login_incorrect_password(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'incorrect',
        }

        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('Password doesn&#39;t match. Please try again.', response_text)

    def test_logout(self):
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password',
        }

        self.app.post('/login', data=post_data)
        self.app.get('/logout')
        # - Check that the "login" button appears on the homepage
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertIn('login', response_text)