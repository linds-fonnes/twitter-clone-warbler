"""User View tests."""

import os
from unittest import TestCase

from models import db, connect_db, Message, User, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Tests views for users"""

    def setUp(self):
    
        db.drop_all()
        db.create_all()

        self.u1 = User(
            id = 9999,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        self.u2 = User(
            id = 9998,
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )
        self.u3 = User(
            id = 9997,
            email="test3@test.com",
            username="user9997",
            password="HASHED_PASSWORD"
        )
        self.u1_id = self.u1.id
        self.u2_id = self.u2.id
        self.u3_id = self.u3.id
        db.session.add_all([self.u1,self.u2,self.u3])
        db.session.commit()

        self.client = app.test_client()
    
    def tearDown(self):
        db.session.rollback()
    
    def setUpFollowers(self):
         #set up users followings
      
        follow = Follows(user_being_followed_id=self.u2_id, user_following_id=self.u1_id)
        follow2 = Follows(user_being_followed_id=self.u1_id,user_following_id=self.u2_id)
        db.session.add_all([follow,follow2])
        db.session.commit()

    def test_show_followers(self):
        """when logged in can you see the follower pages for any user?"""

        #tests that user1's name displays in user2's list of followers and user2's name displays in user1's followers
        self.setUpFollowers() 

        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.u1_id

            resp = c.get(f"/users/{self.u2_id}/followers")
            resp2 = c.get(f"/users/{self.u1_id}/followers")

            self.assertEqual(resp.status_code,200)
            self.assertIn("testuser",str(resp.data))
            self.assertEqual(resp2.status_code,200)
            self.assertIn("testuser2",str(resp.data))
    
    def test_show_following(self):
        """when logged in can you see the following pages for any user?"""

        self.setUpFollowers()
         #tests that user1's name displays in user2's list of people following and vice versa
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.u1_id

            resp = c.get(f"/users/{self.u2_id}/following")
            resp2 = c.get(f"/users/{self.u1_id}/following")

            self.assertEqual(resp.status_code,200)
            self.assertIn("testuser",str(resp.data))
            self.assertEqual(resp2.status_code,200)
            self.assertIn("testuser2",str(resp.data))

    def test_show_followers_no_user(self):
        #tests that a logged out user cannot view user followers of a user

        self.setUpFollowers()

        with self.client as c:
            resp = c.get(f"/users/{self.u1_id}/followers", follow_redirects=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Access unauthorized.", str(resp.data))

    def test_show_following_no_user(self):
        #tests that a logged out user cannot view users being followed of a user

        self.setUpFollowers()

        with self.client as c:
            resp = c.get(f"/users/{self.u1_id}/following", follow_redirects=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Access unauthorized.", str(resp.data)) 

    def test_show_users(self):
        #tests that all users display
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.u1_id
        resp = c.get("/users")
        self.assertEqual(resp.status_code,200)
        self.assertIn("testuser", str(resp.data))
        self.assertIn("testuser2", str(resp.data))

    def test_search_user(self):
        #tests that search feature displays matching users 
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.u1_id
        resp = c.get("/users?q=test")
        self.assertEqual(resp.status_code,200)
        self.assertIn("testuser", str(resp.data))
        self.assertIn("testuser", str(resp.data))  
        self.assertNotIn("user9997",str(resp.data)) 

    def test_user_profile(self):
        #tests that specific user's info displays on their profile page
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.u1_id

        resp = c.get("/users/9997")
        self.assertEqual(resp.status_code,200)
        self.assertIn("user9997",str(resp.data))

    def test_add_follow(self):
        #tests that a user can follow another user
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.u1_id

        resp = c.post(f"/users/follow/{self.u3_id}", follow_redirects=True)  
        self.assertEqual(resp.status_code,200) 

        resp2 = c.get(f"/users/{self.u1_id}/following")
        self.assertIn("user9997",str(resp2.data))

    def test_remove_follow(self):
        #tests that a user can unfollow a user 
        self.setUpFollowers()
        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.u1_id
        
        resp = c.post(f"/users/stop-following/{self.u2_id}", follow_redirects=True)
        self.assertEqual(resp.status_code,200)

        resp2 = c.get(f"/users/{self.u1_id}/following")
        self.assertNotIn("testuser2", str(resp2.data))
    
        



