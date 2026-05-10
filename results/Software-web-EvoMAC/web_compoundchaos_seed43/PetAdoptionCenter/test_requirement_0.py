'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation works.
Test the presence and correctness of key elements on the Dashboard page.
'''
import unittest
from app import app
class TestPetAdoptionCenterDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_title(self):
        # Test that the page title is correct in the dashboard page
        response = self.client.get('/')
        self.assertIn(b'<title>Pet Adoption Dashboard</title>', response.data)
    def test_dashboard_elements_presence(self):
        # Test presence of key elements by their IDs in the dashboard page HTML
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('id="dashboard-page"', html)
        self.assertIn('id="featured-pets"', html)
        self.assertIn('id="browse-pets-button"', html)
        self.assertIn('id="back-to-dashboard"', html)
    def test_dashboard_featured_pets_limit(self):
        # Test that featured pets section contains at most 5 pets
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # Count occurrences of a pet card or pet name inside featured-pets div
        # Since no exact class/id for pet cards is specified, we check featured-pets div content length
        # We check that there are no more than 5 pet names displayed in featured-pets div
        # This is a heuristic: count occurrences of pet names from example data in featured-pets div
        # Example pets from example data: Buddy, Whiskers, Charlie
        # We check that these names appear at most 5 times combined in featured-pets
        featured_section_start = html.find('id="featured-pets"')
        if featured_section_start == -1:
            self.fail('featured-pets div not found')
        # Extract substring starting at featured-pets div
        featured_html = html[featured_section_start:featured_section_start+2000]  # 2000 chars should be enough
        pet_names = ['Buddy', 'Whiskers', 'Charlie']
        count = 0
        for name in pet_names:
            count += featured_html.count(name)
        self.assertLessEqual(count, 5)
    def test_dashboard_recent_activities_presence(self):
        # Test that recent activities section is present and shows recent applications for current user
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        # The template uses recent_activities variable, so check for known applicant_name from example data
        self.assertIn('id="dashboard-page"', html)
        # Check for applicant_name from example data: John Doe (john_doe user)
        self.assertIn('John Doe', html)
    def test_navigation_to_pet_listings(self):
        # Test that clicking browse-pets-button leads to /pets page
        # Since we cannot click in unittest, we check that the button exists and the /pets route is accessible
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('id="browse-pets-button"', html)
        # Test /pets page accessible
        pets_response = self.client.get('/pets')
        self.assertEqual(pets_response.status_code, 200)
        self.assertIn(b'<title>Available Pets</title>', pets_response.data)
if __name__ == '__main__':
    unittest.main()