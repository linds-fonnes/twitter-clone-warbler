"""User View tests."""

import os
from unittest import TestCase

from models import db, connect_db, Message, User

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Tests views for users"""

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()
    
    def tearDown(self):
        db.session.rollback()
    
    def test_show_followers(self):
        