"""Message model tests"""
  
import os 
from unittest import TestCase
from datetime import datetime

from models import db, User, Message, Likes 

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class MessageModelTestCase(TestCase):
    """Tests model for Messages"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        u = User(
            id = 99999,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

    def test_message_model(self):
        """Tests that message model works"""
        m = Message(
            text = "test",
            user_id = 99999
        )
        
        db.session.add(m)
        db.session.commit()
        
        self.assertEqual(m.user.username, "testuser")
        self.assertEqual(m.text,"test")
        self.assertTrue(m.timestamp)