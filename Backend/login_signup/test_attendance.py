import unittest
from app import app

class TestAttendanceApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
         pass

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Check if it redirects to login page

    def test_signup(self):
        response = self.app.post('/signup', data=dict(username='test_user', password='test_password'))
        self.assertEqual(response.status_code, 302)  # Check if it redirects to login page

    def test_login_valid_user(self):
        response = self.app.post('/login', data=dict(username='test_user', password='test_password'))
        self.assertEqual(response.status_code, 302)  # Check if it redirects to the home page

    def test_login_invalid_user(self):
        response = self.app.post('/login', data=dict(username='nonexistent_user', password='wrong_password'))
        self.assertIn(b'Invalid login credentials', response.data)  # Check for error message

if __name__ == '__main__':
    unittest.main()
