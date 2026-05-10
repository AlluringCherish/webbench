'''
Test whether the first page of the website (Dashboard) loads correctly and whether basic navigation works based on the example data provided in the Task.
'''
import unittest
from app import app
class PetAdoptionCenterBasicNavigationTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_page_loads(self):
        # Test that the dashboard page loads successfully and contains expected elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        # Check page title or main heading presence
        self.assertIn('Pet Adoption Dashboard', html)
        # Check presence of featured pets container
        self.assertIn('id="featured-pets"', html)
        # Check presence of browse pets button
        self.assertIn('id="browse-pets-button"', html)
        # Check presence of back to dashboard button
        self.assertIn('id="back-to-dashboard"', html)
    def test_navigation_to_pet_listings(self):
        # Test navigation from dashboard to pet listings page
        response = self.client.get('/pet_listings')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('<title>Available Pets</title>', html)
        self.assertIn('id="pet-listings-page"', html)
        self.assertIn('id="pet-grid"', html)
        self.assertIn('id="back-to-dashboard"', html)
    def test_back_to_dashboard_route(self):
        # Test that the back_to_dashboard route redirects to dashboard
        response = self.client.get('/back_to_dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Pet Adoption Dashboard', html)
    def test_pet_details_page_loads(self):
        # Test pet details page for an existing pet (pet_id=1 from example data)
        response = self.client.get('/pet_details/1')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Pet Details', html)
        self.assertIn('Buddy', html)  # Pet name from example data
        self.assertIn('Friendly and energetic dog', html)  # Part of description
        self.assertIn('id="adopt-button"', html)
    def test_pet_details_page_not_found(self):
        # Test pet details page for a non-existing pet redirects to pet listings with flash message
        response = self.client.get('/pet_details/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Pet not found.', html)
        self.assertIn('Available Pets', html)
if __name__ == '__main__':
    unittest.main()