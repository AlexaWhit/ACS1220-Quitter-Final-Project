import os
import unittest
import app

from datetime import date
from quitter_app.extensions import app, db, bcrypt
from quitter_app.models import User, Post, Reaction

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
        audience='Motivation',
        body='I made it to 100 days! I feel fantastic! We can all do this!',
        photo_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjDT__CUEh4j_OttSSFoNNX7lL7Bzff8etWw&usqp=CAU',
        created_by_id='1'
    )
    db.session.add(post)
    db.session.commit()

def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
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
        self.assertIn('Add Friend', response_text)
        self.assertIn('View Profile', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    # def test_post_detail_logged_in(self):
    #     """Test that the post appears on its post page."""
    #     create_post()
    #     create_user()
    #     login(self.app, 'me1', 'password')

    #     response = self.app.get('/post/1', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    #     response_text = response.get_data(as_text=True)
    #     self.assertIn("<h1>100 days</h1>", response_text)
    #     self.assertIn("Motivation", response_text)

    #     self.assertNotIn("Sign Up", response_text)

    # def test_update_post(self):
    #     """Test updating a post."""
    #     # Set up
    #     create_post()
    #     create_user()
    #     login(self.app, 'me1', 'password')

    #     # Make POST request with data
    #     post_data = {
    #         'title': '60 Days',
    #         'audience': 'Motivation',
    #         'body': 'I made it to 100 days! I feel fantastic! We can all do this!',
    #         'photo_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjDT__CUEh4j_OttSSFoNNX7lL7Bzff8etWw&usqp=CAU',
    #         'created_by_id': 1,
    #     }

    #     self.app.post('/post/1', data=post_data)
        
    #     # Make sure the book was updated as we'd expect
    #     post = Post.query.get(1)
    #     self.assertEqual(post.title, '60 Days')
    #     self.assertEqual(post.audience, 'Motivation')
    #     self.assertEqual(post.body, 'I made it to 100 days! I feel fantastic! We can all do this!')
    #     self.assertEqual(post.photo_url, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjDT__CUEh4j_OttSSFoNNX7lL7Bzff8etWw&usqp=CAU')
    #     self.assertEqual(post.created_by_id, 1)

    # def test_create_book(self):
    #     """Test creating a book."""
    #     # Set up
    #     create_post()
    #     create_user()
    #     login(self.app, 'me1', 'password')

    #     # Make POST request with data
    #     post_data = {
    #         'title': 'Go Set a Watchman',
    #         'publish_date': '2015-07-14',
    #         'author': 1,
    #         'audience': 'ADULT',
    #         'genres': []
    #     }
    #     self.app.post('/create_book', data=post_data)

    #     # Make sure book was updated as we'd expect
    #     created_book = Book.query.filter_by(title='Go Set a Watchman').one()
    #     self.assertIsNotNone(created_book)
    #     self.assertEqual(created_book.author.name, 'Harper Lee')

    # def test_create_book_logged_out(self):
    #     """
    #     Test that the user is redirected when trying to access the create book 
    #     route if not logged in.
    #     """
    #     # Set up
    #     create_post()
    #     create_user()

    #     # Make GET request
    #     response = self.app.get('/create_book')

    #     # Make sure that the user was redirecte to the login page
    #     self.assertEqual(response.status_code, 302)
    #     self.assertIn('/login?next=%2Fcreate_book', response.location)

    # def test_create_author(self):
    #     """Test creating an author."""
    #     # TODO: Create a user & login (so that the user can access the route)
    #     create_user()
    #     login(self.app, 'me1', 'password')

    #     # TODO: Make a POST request to the /create_author route
    #     post_data = {
    #         'name': 'Stephen King',
    #         'biography': 'Stephen King Bio',
    #     }
    #     self.app.post('/create_author', data=post_data)

    #     # TODO: Verify that the author was updated in the database
    #     created_author = Author.query.filter_by(name='Stephen King').one()
    #     self.assertIsNotNone(created_author)
    #     self.assertEqual(created_author.biography, 'Stephen King Bio')

    # def test_create_genre(self):
    #     # TODO: Create a user & login (so that the user can access the route)
    #     create_user()
    #     login(self.app, 'me1', 'password')

    #     # TODO: Make a POST request to the /create_genre route, 
    #     post_data = {
    #         'name': 'horror',
    #     }
    #     self.app.post('/create_genre', data=post_data)
    #     # TODO: Verify that the genre was updated in the database
    #     created_genre = Genre.query.filter_by(name='horror').one()
    #     self.assertIsNotNone(created_genre)
    #     self.assertEqual(created_genre.name, 'horror')

    # def test_profile_page(self):
    #     create_user()
    #     login(self.app, 'me1', 'password')
        
    #     response = self.app.get('/profile/me1', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    #     # TODO: Verify that the response shows the appropriate user info
    #     response_text = response.get_data(as_text=True)
    #     self.assertIn('me1', response_text)
    #     self.assertIn('Create Book', response_text)
    #     self.assertIn('Create Author', response_text)
    #     self.assertIn('Create Genre', response_text)
    #     self.assertIn('Log Out', response_text)

    # def test_favorite_book(self):
    #     # TODO: Login as the user me1
    #     create_user()
    #     create_post()
    #     login(self.app, 'me1', 'password')

    #     # TODO: Make a POST request to the /favorite/1 route
    #      #    to add the book with ID 1 to the user's favorites
    #     post_data = {
    #         'book_id': 1,
    #     } 
    #     self.app.post('/favorite/1', data=post_data)
        
    #     # TODO: Verify that the book with id 1 was added to the user's favorites
    #     user = User.query.filter_by(username='me1').first()
    #     book = Book.query.get(1)
    #     self.assertIn(book, user.favorite_books)

    # def test_unfavorite_book(self):
    #     # TODO: Login as the user me1, and add book with id 1 to me1's favorites
    #     create_user()
    #     create_post()
    #     login(self.app, 'me1', 'password')

    #     # TODO: Make a POST request to the /unfavorite/1 route
    #     post_data = {
    #         'book_id': 1,
    #     } 
    #     self.app.post('/unfavorite/1', data=post_data)

    #     # TODO: Verify that the book with id 1 was removed from the user's 
    #     # favorites
    #     user = User.query.filter_by(username='me1').first()
    #     book = Book.query.get(1)
    #     self.assertNotIn(book, user.favorite_books)