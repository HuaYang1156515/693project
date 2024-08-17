import unittest
from app import app, db
from models.user import User

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        u = User(name="Test User", login="testuser", password="testpassword")
        db.session.add(u)
        db.session.commit()
        self.assertEqual(u.name, "Test User")

if __name__ == '__main__':
    unittest.main()
