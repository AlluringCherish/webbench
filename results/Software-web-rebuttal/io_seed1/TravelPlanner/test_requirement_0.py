'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence of featured destinations, upcoming trips, and navigation buttons.
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class TravelPlannerDashboardTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible via GET /
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_title(self):
        # Test that the page title is correct
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.title.string.strip()
        self.assertEqual(title, "Travel Planner Dashboard")
    def test_dashboard_featured_destinations_section(self):
        # Test presence of featured destinations section and its elements
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_section = soup.find(id='featured-destinations')
        self.assertIsNotNone(featured_section, "Featured destinations section missing")
        # Check for heading
        heading = featured_section.find('h2')
        self.assertIsNotNone(heading)
        self.assertEqual(heading.text.strip(), "Featured Destinations")
        # Check for list or no destinations message
        ul = featured_section.find('ul')
        p = featured_section.find('p')
        self.assertTrue(ul is not None or p is not None, "Neither list nor message found in featured destinations")
    def test_dashboard_upcoming_trips_section(self):
        # Test presence of upcoming trips section and its elements
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        upcoming_section = soup.find(id='upcoming-trips')
        self.assertIsNotNone(upcoming_section, "Upcoming trips section missing")
        # Check for heading
        heading = upcoming_section.find('h2')
        self.assertIsNotNone(heading)
        self.assertEqual(heading.text.strip(), "Upcoming Trips")
        # Check for list or no trips message
        ul = upcoming_section.find('ul')
        p = upcoming_section.find('p')
        self.assertTrue(ul is not None or p is not None, "Neither list nor message found in upcoming trips")
    def test_dashboard_navigation_buttons(self):
        # Test presence and correctness of navigation buttons with correct IDs and URLs
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        nav_buttons = {
            'browse-destinations-button': '/destinations',
            'plan-itinerary-button': '/itinerary_planning',
        }
        # Additional buttons without IDs but with onclick URLs
        additional_buttons = {
            'Search Accommodations': '/accommodations',
            'Book Flights': '/transportation',
            'Travel Packages': '/travel_packages',
            'My Trips': '/trips',
            'Travel Recommendations': '/travel_recommendations'
        }
        # Check buttons with IDs
        for btn_id, url_path in nav_buttons.items():
            btn = soup.find('button', id=btn_id)
            self.assertIsNotNone(btn, f"Button with id '{btn_id}' not found")
            onclick = btn.get('onclick', '')
            self.assertIn(url_path, onclick, f"Button '{btn_id}' does not navigate to '{url_path}'")
        # Check additional buttons by text and onclick
        buttons = soup.find_all('button')
        found_texts = {btn.text.strip(): btn for btn in buttons}
        for text, url_path in additional_buttons.items():
            self.assertIn(text, found_texts, f"Navigation button '{text}' not found")
            btn = found_texts[text]
            onclick = btn.get('onclick', '')
            self.assertIn(url_path, onclick, f"Button '{text}' does not navigate to '{url_path}'")
if __name__ == '__main__':
    unittest.main()