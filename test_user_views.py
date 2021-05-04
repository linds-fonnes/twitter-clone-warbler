"""User View tests."""

import os
from unittest import TestCase

from models import db, connect_db, Message, User, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

app.config['WTF_CSRF_ENABLED'] = False

db.create_all()

class UserViewTestCase(TestCase):
    """Tests views for users"""

    def setUp(self):
        User.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
    
    def tearDown(self):
        db.session.rollback()
    
    def test_show_followers(self):
        """when logged in can you see the follower pages for any user?"""

        #set up users and follow each other
        u1 = User(
            id = 9999,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            id = 9998,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        db.session.add_all([u1,u2])
        db.session.commit()

        follow = Follows(user_being_followed_id=9998, user_following_id=9999)
        follow2 = Follows(user_being_followed_id=9999,user_following_id=9998)
        db.session.add_all([follow,follow2])
        db.session.commit()

        #tests that user1's name displays in user2's list of followers and user2's name displays in user1's followers
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = 9999

            resp = c.get("/users/9998/followers")
            resp2 = c.get("/users/9999/followers")

            self.assertEqual(resp.status_code,200)
            self.assertIn("testuser",str(resp.data))
            self.assertEqual(resp2.status_code,200)
            self.assertIn("testuser2",str(resp.data))
    
    def test_show_following(self):
        """when logged in can you see the following pages for any user?"""

        #set up users and follow each other
        u1 = User(
            id = 9999,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            id = 9998,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        db.session.add_all([u1,u2])
        db.session.commit()

        follow = Follows(user_being_followed_id=9998, user_following_id=9999)
        follow2 = Follows(user_being_followed_id=9999,user_following_id=9998)
        db.session.add_all([follow,follow2])
        db.session.commit()

         #tests that user1's name displays in user2's list of people following and vice versa
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = 9999

            resp = c.get("/users/9998/following")
            resp2 = c.get("/users/9999/following")

            self.assertEqual(resp.status_code,200)
            self.assertIn("testuser",str(resp.data))
            self.assertEqual(resp2.status_code,200)
            self.assertIn("testuser2",str(resp.data))

    def test_show_followers_no_user(self):
        #tests that a logged out user cannot view user followers of a user

        #set up users and follow each other
        u1 = User(
            id = 9999,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            id = 9998,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        db.session.add_all([u1,u2])
        db.session.commit()

        follow = Follows(user_being_followed_id=9998, user_following_id=9999)
        follow2 = Follows(user_being_followed_id=9999,user_following_id=9998)
        db.session.add_all([follow,follow2])
        db.session.commit()

        with self.client as c:
            resp = c.get("/users/9999/followers", follow_redirects=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Access unauthorized.", str(resp.data))

    def test_show_following_no_user(self):
        #tests that a logged out user cannot view users being followed of a user

        #set up users and follow each other
        u1 = User(
            id = 9999,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            id = 9998,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        db.session.add_all([u1,u2])
        db.session.commit()

        follow = Follows(user_being_followed_id=9998, user_following_id=9999)
        follow2 = Follows(user_being_followed_id=9999,user_following_id=9998)
        db.session.add_all([follow,follow2])
        db.session.commit()

        with self.client as c:
            resp = c.get("/users/9999/following", follow_redirects=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Access unauthorized.", str(resp.data))