'''
Test whether the website can be accessed through local port 5000.
In this test, you only need to test whether the first page of the website can be accessed through the local 5000 port.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of the Dashboard page by verifying the presence and correctness of the following elements:
- ID: dashboard-page (Div container)
- ID: featured-events (Div container for featured events)
- ID: browse-events-button (Button to navigate to events listing page)
- ID: view-tickets-button (Button to navigate to tickets page)
- ID: venues-button (Button to navigate to venues page)
'''
import unittest
from flask import Flask
from bs4 import BeautifulSoup
import main  # Assuming the main Flask app is in main.py
class EventPlanningAppTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        main.app.testing = True
        self.client = main.app.test_client()
    def test_dashboard_accessible(self):
        # Test that the dashboard page is accessible at '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page did not load successfully")
    def test_dashboard_page_elements(self):
        # Test that the dashboard page contains required elements with correct IDs
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "Dashboard page did not load successfully")
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check for dashboard-page div
        dashboard_div = soup.find(id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard page container (id='dashboard-page') not found")
        # Check for featured-events div
        featured_events_div = soup.find(id='featured-events')
        self.assertIsNotNone(featured_events_div, "Featured events container (id='featured-events') not found")
        # Check for browse-events-button button
        browse_events_button = soup.find(id='browse-events-button')
        self.assertIsNotNone(browse_events_button, "Browse events button (id='browse-events-button') not found")
        self.assertEqual(browse_events_button.name, 'button', "Browse events element is not a button")
        # Check for view-tickets-button button
        view_tickets_button = soup.find(id='view-tickets-button')
        self.assertIsNotNone(view_tickets_button, "View tickets button (id='view-tickets-button') not found")
        self.assertEqual(view_tickets_button.name, 'button', "View tickets element is not a button")
        # Check for venues-button button
        venues_button = soup.find(id='venues-button')
        self.assertIsNotNone(venues_button, "Venues button (id='venues-button') not found")
        self.assertEqual(venues_button.name, 'button', "Venues element is not a button")
    def test_basic_navigation_links(self):
        # Test that the buttons on dashboard link to correct pages (href or form action)
        response = self.client.get('/')
        soup = BeautifulSoup(response.data, 'html.parser')
        # For buttons, check if they have onclick or form action or href attributes to navigate
        # Since buttons may use JS or forms, we check for presence of attributes or forms
        # browse-events-button should navigate to /events
        browse_events_button = soup.find(id='browse-events-button')
        self.assertIsNotNone(browse_events_button)
        # Check if button has onclick attribute or is inside a form with action /events
        browse_events_onclick = browse_events_button.get('onclick')
        self.assertTrue(
            browse_events_onclick and '/events' in browse_events_onclick or
            browse_events_button.parent.name == 'a' and browse_events_button.parent.get('href') == '/events' or
            browse_events_button.parent.name == 'form' and browse_events_button.parent.get('action') == '/events',
            "Browse events button does not navigate to /events"
        )
        # view-tickets-button should navigate to /book-tickets
        view_tickets_button = soup.find(id='view-tickets-button')
        self.assertIsNotNone(view_tickets_button)
        view_tickets_onclick = view_tickets_button.get('onclick')
        self.assertTrue(
            view_tickets_onclick and '/book-tickets' in view_tickets_onclick or
            view_tickets_button.parent.name == 'a' and view_tickets_button.parent.get('href') == '/book-tickets' or
            view_tickets_button.parent.name == 'form' and view_tickets_button.parent.get('action') == '/book-tickets',
            "View tickets button does not navigate to /book-tickets"
        )
        # venues-button should navigate to /venues
        venues_button = soup.find(id='venues-button')
        self.assertIsNotNone(venues_button)
        venues_onclick = venues_button.get('onclick')
        self.assertTrue(
            venues_onclick and '/venues' in venues_onclick or
            venues_button.parent.name == 'a' and venues_button.parent.get('href') == '/venues' or
            venues_button.parent.name == 'form' and venues_button.parent.get('action') == '/venues',
            "Venues button does not navigate to /venues"
        )
if __name__ == '__main__':
    unittest.main()