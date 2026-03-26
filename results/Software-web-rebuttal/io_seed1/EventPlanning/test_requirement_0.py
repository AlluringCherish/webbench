'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of the Dashboard page including presence of featured events, featured venues, and navigation buttons.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class TestEventPlanningDashboard(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test if the dashboard page is accessible via '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_dashboard_page_title(self):
        # Test if the page title is correct
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        title = soup.find('title')
        self.assertIsNotNone(title)
        self.assertEqual(title.text.strip(), "Event Planning Dashboard")
    def test_dashboard_featured_events_section(self):
        # Test if featured-events section exists and contains expected elements
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_events_div = soup.find(id='featured-events')
        self.assertIsNotNone(featured_events_div)
        # Check that it has a heading
        heading = featured_events_div.find('h2')
        self.assertIsNotNone(heading)
        self.assertIn('Upcoming Events', heading.text)
        # Check that there is a list or a message
        ul = featured_events_div.find('ul')
        p = featured_events_div.find('p')
        self.assertTrue(ul is not None or p is not None)
        # If events exist, check at least one event has expected fields
        if ul:
            first_li = ul.find('li')
            self.assertIsNotNone(first_li)
            self.assertIn('Date:', first_li.text)
            self.assertIn('Location:', first_li.text)
            self.assertIsNotNone(first_li.find('a', href=True))
    def test_dashboard_featured_venues_section(self):
        # Test if featured-venues section exists and contains expected elements
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        featured_venues_div = soup.find(id='featured-venues')
        self.assertIsNotNone(featured_venues_div)
        # Check that it has a heading
        heading = featured_venues_div.find('h2')
        self.assertIsNotNone(heading)
        self.assertIn('Featured Venues', heading.text)
        # Check that there is a list or a message
        ul = featured_venues_div.find('ul')
        p = featured_venues_div.find('p')
        self.assertTrue(ul is not None or p is not None)
        # If venues exist, check at least one venue has expected fields
        if ul:
            first_li = ul.find('li')
            self.assertIsNotNone(first_li)
            self.assertIn('Location:', first_li.text)
            self.assertIn('Capacity:', first_li.text)
            self.assertIn('Amenities:', first_li.text)
            self.assertIsNotNone(first_li.find('a', href=True))
    def test_dashboard_navigation_buttons(self):
        # Test presence and correctness of navigation buttons
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        browse_btn = soup.find(id='browse-events-button')
        tickets_btn = soup.find(id='view-tickets-button')
        venues_btn = soup.find(id='venues-button')
        self.assertIsNotNone(browse_btn)
        self.assertIsNotNone(tickets_btn)
        self.assertIsNotNone(venues_btn)
        # Check buttons have onclick attribute with correct URLs
        self.assertIn('/events', browse_btn.get('onclick', ''))
        self.assertIn('/tickets', tickets_btn.get('onclick', ''))
        self.assertIn('/venues', venues_btn.get('onclick', ''))
if __name__ == '__main__':
    unittest.main()