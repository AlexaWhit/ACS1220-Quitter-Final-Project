import os
import unittest
import app

from datetime import date
from quitter_app.extensions import app, db, bcrypt
from quitter_app.models import *


"""
Run these tests with the command:
python3 -m unittest quitter_app.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_post():
    post = Post(
        title='100 Days',
        audience= Purpose.MOTIVATION,
        body='I made it to 100 days! I feel fantastic! We can all do this!',
        photo_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjDT__CUEh4j_OttSSFoNNX7lL7Bzff8etWw&usqp=CAU',
        created_by_id='1'
    )
    db.session.add(post)
    db.session.commit()

def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash, id=1)
    db.session.add(user)
    db.session.commit()

def create_user2():
    # Creates a second user with username 'you2' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user2 = User(username='you2', password=password_hash)
    db.session.add(user2)
    db.session.commit()


#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage_logged_out(self):
        """Test that nothing shows up on the homepage when logged out."""
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('New Post', response_text)
        self.assertNotIn('Add Friend', response_text)
        self.assertNotIn('View Profile', response_text)
 
    def test_homepage_logged_in(self):
        """Test that the posts show up on the homepage."""
        create_post()
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('100 days', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('New Post', response_text)
        self.assertIn('View Profile', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_post_detail_logged_in(self):
        """Test that the post appears on its post page."""
        create_post()
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/post/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn("100 days", response_text)
        self.assertIn("I made it to 100 days! I feel fantastic! We can all do this!", response_text)

        self.assertNotIn("Sign Up", response_text)

    def test_create_post(self):
        """Test creating a post."""
        # Set up
        create_user()
        login(self.app, 'me1', 'password')

        post_data = {
            'title': 'PASS THE TEST',
            'audience': Purpose.FRUSTRATION,
            'body': 'I hope this test passes.',
            'photo_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjDT__CUEh4j_OttSSFoNNX7lL7Bzff8etWw&usqp=CAU',
            'created_by_id': 1,
        }
        self.app.post('/new_post', data=post_data)
        db.session.rollback()

        # Make sure post was updated as we'd expect
        created_post = Post.query.filter_by(title='PASS THE TEST').first()
        self.assertIsNotNone(created_post)
        self.assertEqual(created_post.audience, Purpose.FRUSTRATION)
        self.assertEqual(created_post.body, 'I hope this test passes.')

    def test_update_post(self):
        """Test updating a post."""
        # Set up
        create_post()
        create_user()
        login(self.app, 'me1', 'password')

        # Make POST request with data
        post_data = {
            'title': 'PASS THE TEST',
            'audience': Purpose.FRUSTRATION,
            'body': 'I made it to 10 days!',
            'photo_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjDT__CUEh4j_OttSSFoNNX7lL7Bzff8etWw&usqp=CAU',
            'created_by_id': 1,
        }

        self.app.patch('/post/1', data=post_data)
        
        post = Post.query.get(1)
        self.assertEqual(post.title, 'PASS THE TEST')
        self.assertEqual(post.body, 'I made it to 10 days!')
        self.assertEqual(post.photo_url, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjDT__CUEh4j_OttSSFoNNX7lL7Bzff8etWw&usqp=CAU')
        self.assertEqual(post.created_by_id, 1)

    def test_create_reaction(self):
        """Test creating a reaction."""
        create_post()
        create_user()
        login(self.app, 'me1', 'password')

        reaction_data = {
            'reaction': ReactionEmoji.HEALTHY, 
            'comment': 'Woohoo',
        }
        self.app.post('/post/1/reaction/add', data=reaction_data)

        # TODO: Verify that the author was updated in the database
        created_reaction = Reaction.query.filter_by(comment='Woohoo')
        self.assertIsNotNone(created_reaction)
        self.assertEqual(created_reaction.comment, 'Woohoo')
        self.assertEqual(created_reaction.reaction, ReactionEmoji.HEALTHY)

    def test_profile_page(self):
        create_user()
        login(self.app, 'me1', 'password')
        
        response = self.app.get('/profile/me1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # TODO: Verify that the response shows the appropriate user info
        response_text = response.get_data(as_text=True)
        self.assertIn('me1', response_text)
        self.assertIn('Home', response_text)
        self.assertIn('New Post', response_text)
        self.assertIn('View Profile', response_text)
        self.assertIn('Logout', response_text)

    def test_add_friend(self):
        # TODO: Login as the user me1
        create_user()
        create_user2()
        create_post()
        login(self.app, 'me1', 'password')

        # TODO: Make a POST request to the /favorite/1 route
         #    to add the book with ID 1 to the user's favorites
        post_data = {
            'username': 'you2',
        } 
        self.app.post('/add_friend/you2', data=post_data)
        
        # TODO: Verify that the user with id 2 was added to the user's friend list
        user = User.query.filter_by(username='me1').first()
        user2 = User.query.filter_by(username='you2').first()
        self.assertIn(user2, user.friend_list)

    def test_remove_friend(self):
        # TODO: Login as the user me1, and add friend with username of you2 to me1's favorites
        create_user()
        create_user2()
        create_post()
        login(self.app, 'me1', 'password')

        post_data = {
            'username': 'you2',
        } 
        self.app.post('/remove_friend/you2', data=post_data)

        # TODO: Verify that the user with username of you2 was removed from the user's 
        # friend list
        user = User.query.filter_by(username='me1').first()
        user2 = User.query.filter_by(username='you2').first()
        self.assertNotIn(user2, user.friend_list)