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
        """when logged in can you see the follower/following pages for any user?"""

        #set up users and follow each other
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
        db.session.add_all([u1,u2])
        db.session.commit()

        follow = Follows(user_being_followed_id=u2.id, user_following_id=u1.id)
        follow2 = Follows(user_being_followed_id=u1.id,user_following_id=u2.id)
        db.session.add_all([follow,follow2])
        db.session.commit()

        #tests that user1's name displays in user2's list of followers
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = u1.id

        resp = c.get(f"/users/{u2.id}/followers")

        self.assertEqual(resp.status_code,200)
        self.assertIn(u1.username,str(resp.data))

