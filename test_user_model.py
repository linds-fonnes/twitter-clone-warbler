"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr(self):
        """Tests User repr method"""    
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.__repr__(),f"<User #{u.id}: testuser, test@test.com>")

    def test_is_following(self):
        """Tests User is_following method"""
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        #tests that user1 is not following user2
        self.assertFalse(u1.is_following(u2))

        #tests that user1 is following user2
        follow = Follows(user_being_followed_id=u2.id, user_following_id=u1.id)
        db.session.add(follow)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))

    def test_is_followed_by(self):
        """Tests User is_followed_by method"""
        u1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        #tests that user1 is not following user2
        self.assertFalse(u1.is_followed_by(u2))

        #tests that user1 is follwed by user2
        follow = Follows(user_being_followed_id=u1.id,user_following_id=u2.id)
        db.session.add(follow)
        db.session.commit()
        self.assertTrue(u1.is_followed_by(u2))

    def test_signup_user(self):
        """Tests User signup method"""
        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="test_image.com"
        )
        self.assertEqual(u.__repr__(),f"<User #{u.id}: testuser, test@test.com>")

        u2 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="test_image.com"
        )
        self.assertEqual(u.__repr__(),"<User #None: testuser, test@test.com>")

    def test_authenticate_user(self):
        """Tests User authenticate method"""
        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="test_image.com"
        )
        # tests successfully returns user when given valid username & password
        self.assertEqual(User.authenticate("testuser","HASHED_PASSWORD"),u)
        # tests returns false when given invalid username
        self.assertFalse(User.authenticate("testUser","HASHED_PASSWORD"))
        #tests returns false when given invalid password
        self.assertFalse(User.authenticate("testuser","HaSHED_PaSSWORD"))