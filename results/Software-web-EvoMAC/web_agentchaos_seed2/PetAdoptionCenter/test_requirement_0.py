'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly.
Test basic navigation from Dashboard page buttons.
'''
import unittest
from main import app
class PetAdoptionCenterBasicAccessTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page loads successfully (HTTP 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check that the page title is correct in the HTML
        self.assertIn(b'<title>Pet Adoption Dashboard</title>', response.data)
        # Check that the dashboard container div is present
        self.assertIn(b'id="dashboard-page"', response.data)
    def test_dashboard_navigation_buttons_present(self):
        # Load dashboard page
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Check presence of Browse Pets button with correct id
        self.assertIn('id="browse-pets-button"', html)
        # Check presence of Refresh Dashboard button with correct id
        self.assertIn('id="back-to-dashboard"', html)
        # Since no user logged in, Login button should be present
        self.assertIn('Login', html)
    def test_navigation_to_pet_listings(self):
        # Simulate clicking Browse Pets button by requesting /pets
        response = self.client.get('/pets')
        self.assertEqual(response.status_code, 200)
        # Check page title for Available Pets page
        self.assertIn(b'<title>Available Pets</title>', response.data)
        # Check pet listings container div present
        self.assertIn(b'id="pet-listings-page"', response.data)
    def test_navigation_to_login(self):
        # Access login page
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        # Check login page title
        self.assertIn(b'<title>Login</title>', response.data)
if __name__ == '__main__':
    unittest.main()