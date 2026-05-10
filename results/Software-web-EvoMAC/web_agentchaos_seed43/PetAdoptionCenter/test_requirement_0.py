'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of the Dashboard page, verifying the presence and correctness of all specified elements as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class PetAdoptionCenterDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the root URL and check status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_elements(self):
        # Test Task 2 & 3: Check that dashboard page loads correctly and contains required elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div with id 'dashboard-page'
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard container div with id 'dashboard-page' should be present")
        # Check page title
        title = soup.find('title')
        self.assertIsNotNone(title, "Page should have a <title> element")
        self.assertEqual(title.text.strip(), "Pet Adoption Dashboard", "Page title should be 'Pet Adoption Dashboard'")
        # Check featured pets section
        featured_section = dashboard_div.find('section', id='featured-pets')
        self.assertIsNotNone(featured_section, "Featured pets section with id 'featured-pets' should be present")
        # Check heading inside featured pets section
        featured_heading = featured_section.find('h2')
        self.assertIsNotNone(featured_heading, "Featured pets section should have an <h2> heading")
        self.assertEqual(featured_heading.text.strip(), "Featured Pets", "Featured pets section heading should be 'Featured Pets'")
        # Check featured pets display: either pet cards or no pets message
        pet_cards = featured_section.find_all('div', class_='pet-card')
        no_pets_msg = featured_section.find('p')
        # At least one of these should be present
        self.assertTrue(pet_cards or (no_pets_msg and "No featured pets available" in no_pets_msg.text),
                        "Featured pets section should display pet cards or a no pets message")
        # If pet cards present, check that each card has name, species, age, and link to details
        for card in pet_cards:
            name = card.find('h3')
            self.assertIsNotNone(name, "Each pet card should have a pet name in <h3>")
            species_p = card.find('p', text=lambda t: t and "Species:" in t)
            self.assertIsNotNone(species_p, "Each pet card should display species")
            age_p = card.find('p', text=lambda t: t and "Age:" in t)
            self.assertIsNotNone(age_p, "Each pet card should display age")
            details_link = card.find('a')
            self.assertIsNotNone(details_link, "Each pet card should have a link to pet details")
            self.assertIn('/pets/', details_link['href'], "Pet details link href should contain '/pets/'")
        # Check browse pets button
        browse_button = dashboard_div.find('button', id='browse-pets-button')
        self.assertIsNotNone(browse_button, "Browse Pets button with id 'browse-pets-button' should be present")
        self.assertIn("Browse Pets", browse_button.text, "Browse Pets button should have correct text")
        # Check back to dashboard button (refresh)
        back_button = dashboard_div.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_button, "Back to Dashboard button with id 'back-to-dashboard' should be present")
        self.assertIn("Refresh Dashboard", back_button.text, "Back to Dashboard button should have correct text")
    def test_dashboard_navigation_buttons(self):
        # Test that clicking browse pets button leads to /pets page
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        browse_button = soup.find('button', id='browse-pets-button')
        self.assertIsNotNone(browse_button)
        # The button uses inline onclick with location.href, extract URL
        onclick = browse_button.get('onclick', '')
        self.assertIn('/pets', onclick, "Browse Pets button should navigate to /pets")
        # The back-to-dashboard button should refresh dashboard (redirect to /)
        back_button = soup.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_button)
        onclick_back = back_button.get('onclick', '')
        self.assertIn('/refresh_dashboard', onclick_back, "Back to Dashboard button should navigate to /refresh_dashboard")
        # Test that /refresh_dashboard redirects to /
        refresh_response = self.client.get('/refresh_dashboard', follow_redirects=False)
        self.assertIn(refresh_response.status_code, [302, 301], "Refresh dashboard route should redirect")
        self.assertIn('/', refresh_response.headers.get('Location', ''), "Refresh dashboard should redirect to '/'")
if __name__ == '__main__':
    unittest.main()