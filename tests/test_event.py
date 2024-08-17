import unittest
from app import app, db
from models.event import Event

class EventModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_event_creation(self):
        e = Event(active_name="Test Event", active_time="2024-08-09 12:00:00", active_location="Test Location")
        db.session.add(e)
        db.session.commit()
        self.assertEqual(e.active_name, "Test Event")

if __name__ == '__main__':
    unittest.main()
