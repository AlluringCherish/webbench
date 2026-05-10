'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page, verifying presence and correctness of required elements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class VirtualMuseumTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_page_accessible(self):
        # Test Task 1: Access Dashboard page at root '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page should be accessible with status code 200")
    def test_dashboard_page_content(self):
        # Test Task 2 & 3: Check Dashboard page content and elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check page title contains "Museum Dashboard"
        title_tag = soup.find('title')
        if title_tag:
            self.assertIn("Museum Dashboard", title_tag.text)
        # If no <title> tag, check for <h1> with "Museum Dashboard"
        else:
            h1_tag = soup.find('h1')
            self.assertIsNotNone(h1_tag, "Dashboard page should have an <h1> element")
            self.assertIn("Museum Dashboard", h1_tag.text)
        # Check div with id="dashboard-page"
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page must contain div with id='dashboard-page'")
        # Check div with id="exhibition-summary"
        exhibition_summary_div = soup.find('div', id='exhibition-summary')
        self.assertIsNotNone(exhibition_summary_div, "Dashboard page must contain div with id='exhibition-summary'")
        # Check buttons with specified IDs and their onclick attributes or hrefs
        buttons_info = {
            'artifact-catalog-button': '/artifact-catalog',
            'exhibitions-button': '/exhibitions',
            'visitor-tickets-button': '/visitor-tickets',
            'virtual-events-button': '/virtual-events',
            'audio-guides-button': '/audio-guides'
        }
        for btn_id, target_url in buttons_info.items():
            btn = soup.find('button', id=btn_id)
            self.assertIsNotNone(btn, f"Dashboard page must have button with id='{btn_id}'")
            # Check if button has onclick attribute with correct navigation
            onclick = btn.get('onclick', '')
            self.assertIn(target_url, onclick, f"Button '{btn_id}' should navigate to '{target_url}'")
    def test_basic_navigation_from_dashboard(self):
        # Test navigation by simulating clicks (GET requests) to linked pages
        pages = [
            '/artifact-catalog',
            '/exhibitions',
            '/visitor-tickets',
            '/virtual-events',
            '/audio-guides'
        ]
        for page in pages:
            response = self.client.get(page)
            self.assertEqual(response.status_code, 200, f"Page {page} should be accessible with status code 200")
if __name__ == '__main__':
    unittest.main()