'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and basic navigation works.
Test the elements and integrity of all pages by verifying the presence and correctness of required elements.
'''
import unittest
from main import app
class VirtualMuseumTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_accessible(self):
        # Test Task 1: Access the dashboard page at root '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Museum Dashboard', response.data)
        # Check presence of key elements by id
        self.assertIn(b'id="dashboard-page"', response.data)
        self.assertIn(b'id="exhibition-summary"', response.data)
        self.assertIn(b'id="artifact-catalog-button"', response.data)
        self.assertIn(b'id="exhibitions-button"', response.data)
        self.assertIn(b'id="visitor-tickets-button"', response.data)
        self.assertIn(b'id="virtual-events-button"', response.data)
        self.assertIn(b'id="audio-guides-button"', response.data)
    def test_navigation_links_from_dashboard(self):
        # Test Task 2: Check navigation buttons lead to correct pages
        # Artifact Catalog
        response = self.client.get('/artifact_catalog')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Artifact Catalog', response.data)
        self.assertIn(b'id="artifact-catalog-page"', response.data)
        self.assertIn(b'id="artifact-table"', response.data)
        self.assertIn(b'id="search-artifact"', response.data)
        self.assertIn(b'id="apply-artifact-filter"', response.data)
        self.assertIn(b'id="back-to-dashboard"', response.data)
        # Exhibitions
        response = self.client.get('/exhibitions')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Exhibitions', response.data)
        self.assertIn(b'id="exhibitions-page"', response.data)
        self.assertIn(b'id="exhibition-list"', response.data)
        self.assertIn(b'id="filter-exhibition-type"', response.data)
        self.assertIn(b'id="apply-exhibition-filter"', response.data)
        self.assertIn(b'id="back-to-dashboard"', response.data)
        # Visitor Tickets
        response = self.client.get('/visitor_tickets')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Visitor Tickets', response.data)
        self.assertIn(b'id="visitor-tickets-page"', response.data)
        self.assertIn(b'id="ticket-type"', response.data)
        self.assertIn(b'id="number-of-tickets"', response.data)
        self.assertIn(b'id="purchase-ticket-button"', response.data)
        self.assertIn(b'id="my-tickets-table"', response.data)
        self.assertIn(b'id="back-to-dashboard"', response.data)
        # Virtual Events
        response = self.client.get('/virtual_events')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Virtual Events', response.data)
        self.assertIn(b'id="virtual-events-page"', response.data)
        self.assertIn(b'id="event-list"', response.data)
        self.assertIn(b'id="back-to-dashboard"', response.data)
        # Audio Guides
        response = self.client.get('/audio_guides')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Audio Guides', response.data)
        self.assertIn(b'id="audio-guides-page"', response.data)
        self.assertIn(b'id="audio-guide-list"', response.data)
        self.assertIn(b'id="filter-language"', response.data)
        self.assertIn(b'id="apply-language-filter"', response.data)
        self.assertIn(b'id="back-to-dashboard"', response.data)
    def test_exhibition_details_page(self):
        # Test Task 3: Access exhibition details page for a known exhibition_id '1'
        response = self.client.get('/exhibition_details/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Exhibition Details', response.data)
        self.assertIn(b'id="exhibition-details-page"', response.data)
        self.assertIn(b'id="exhibition-title"', response.data)
        self.assertIn(b'id="exhibition-description"', response.data)
        self.assertIn(b'id="exhibition-dates"', response.data)
        self.assertIn(b'id="exhibition-artifacts"', response.data)
        self.assertIn(b'id="back-to-exhibitions"', response.data)
    def test_404_exhibition_details(self):
        # Test accessing exhibition details page with invalid id redirects to exhibitions page with flash
        response = self.client.get('/exhibition_details/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Exhibitions', response.data)
        self.assertIn(b'Exhibition not found.', response.data)
if __name__ == '__main__':
    unittest.main()