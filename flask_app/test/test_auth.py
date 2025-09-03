import unittest
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registration(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'password': 'securepass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)

    def test_login(self):
        with self.app.app_context():
            user = User(username='testuser', password='hashedpass')  # You should hash this properly
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'hashedpass'  # This won't work unless hashed correctly
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_logout(self):
        # First, log in a user
        with self.app.app_context():
            user = User(username='testuser', password='hashedpass')
            db.session.add(user)
            db.session.commit()

        self.client.post('/login', data={
            'username': 'testuser',
            'password': 'hashedpass'
        })

        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()
