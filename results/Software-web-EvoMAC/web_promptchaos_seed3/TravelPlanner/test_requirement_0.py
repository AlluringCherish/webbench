'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page including presence of featured destinations, upcoming trips, and navigation buttons.
'''
import unittest
from app import app
from bs4 import BeautifulSoup
class TravelPlannerBasicTests(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access root URL and check status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_content(self):
        # Test Task 2 & 3: Check dashboard page content and elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check page container div
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container div with id 'dashboard-page' should be present")
        # Check featured destinations section and elements
        featured_section = soup.find('section', id='featured-destinations')
        self.assertIsNotNone(featured_section, "Featured destinations section with id 'featured-destinations' should be present")
        destinations_list = featured_section.find('ul')
        self.assertIsNotNone(destinations_list, "Featured destinations list should be present")
        featured_items = destinations_list.find_all('li')
        self.assertGreaterEqual(len(featured_items), 1, "There should be at least one featured destination displayed")
        for li in featured_items:
            # Check that each featured destination has a view details link with correct id pattern
            link = li.find('a')
            self.assertIsNotNone(link, "Each featured destination should have a 'View Details' link")
            self.assertTrue(link['id'].startswith('view-destination-button-'), "View Details link id should start with 'view-destination-button-'")
        # Check upcoming trips section and elements
        upcoming_section = soup.find('section', id='upcoming-trips')
        self.assertIsNotNone(upcoming_section, "Upcoming trips section with id 'upcoming-trips' should be present")
        trips_list = upcoming_section.find('ul')
        # It is possible no upcoming trips exist, so check for either list or no trips message
        if trips_list:
            trip_items = trips_list.find_all('li')
            self.assertGreaterEqual(len(trip_items), 0, "Upcoming trips list should contain zero or more trips")
            for li in trip_items:
                # Check that each trip has a link to view trip details
                link = li.find('a')
                self.assertIsNotNone(link, "Each upcoming trip should have a 'View Trip Details' link")
        else:
            no_trips_msg = upcoming_section.find('p')
            self.assertIsNotNone(no_trips_msg, "If no upcoming trips, a message should be displayed")
        # Check navigation buttons presence and correct ids
        browse_button = soup.find('button', id='browse-destinations-button')
        self.assertIsNotNone(browse_button, "Browse Destinations button with id 'browse-destinations-button' should be present")
        plan_button = soup.find('button', id='plan-itinerary-button')
        self.assertIsNotNone(plan_button, "Plan Itinerary button with id 'plan-itinerary-button' should be present")
    def test_navigation_buttons_redirect(self):
        # Test navigation buttons redirect to correct pages
        # Browse Destinations button redirects to /navigate/browse_destinations -> /destinations
        response = self.client.get('/navigate/browse_destinations', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/destinations', response.headers['Location'])
        # Plan Itinerary button redirects to /navigate/plan_itinerary -> /itinerary
        response = self.client.get('/navigate/plan_itinerary', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/itinerary', response.headers['Location'])
        # Back to dashboard navigation redirects to /
        response = self.client.get('/navigate/dashboard', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/', response.headers['Location'])
if __name__ == '__main__':
    unittest.main()