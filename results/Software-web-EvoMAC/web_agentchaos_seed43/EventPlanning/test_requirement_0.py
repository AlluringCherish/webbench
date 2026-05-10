'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of ALL pages, verifying the presence and correctness of the specified elements on each page.
'''
import unittest
from main import app
class EventPlanningAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_01_dashboard_accessible(self):
        # Test Task 1: Access root '/' on local port 5000 (simulated by test client)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Event Planning Dashboard', response.data)
    def test_02_dashboard_elements(self):
        # Test Task 2: Dashboard page elements presence
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('id="dashboard-page"', html)
        self.assertIn('id="featured-events"', html)
        self.assertIn('id="featured-venues"', html)
        self.assertIn('id="browse-events-button"', html)
        self.assertIn('id="view-tickets-button"', html)
        self.assertIn('id="venues-button"', html)
    def test_03_events_listing_page(self):
        # Test Task 3: Events Listing page elements and correctness
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('id="events-page"', html)
        self.assertIn('id="event-search-input"', html)
        self.assertIn('id="event-category-filter"', html)
        self.assertIn('id="events-grid"', html)
        # Check presence of at least one view-event-button with event_id from example data (e.g. event_id=1)
        self.assertIn('id="view-event-button-1"', html)
    def test_04_event_details_page(self):
        # Test Task 3: Event Details page elements and correctness for event_id=1
        response = self.client.get('/events/1')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('id="event-details-page"', html)
        self.assertIn('id="event-title"', html)
        self.assertIn('id="event-date"', html)
        self.assertIn('id="event-location"', html)
        self.assertIn('id="event-description"', html)
        self.assertIn('id="book-ticket-button"', html)
    def test_05_ticket_booking_page_get(self):
        # Test Task 3: Ticket Booking page GET elements
        response = self.client.get('/tickets')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('id="ticket-booking-page"', html)
        self.assertIn('id="select-event-dropdown"', html)
        self.assertIn('id="ticket-quantity-input"', html)
        self.assertIn('id="ticket-type-select"', html)
        self.assertIn('id="book-now-button"', html)
        self.assertIn('id="booking-confirmation"', html)
    def test_06_participants_management_page(self):
        # Test Task 3: Participants Management page elements
        response = self.client.get('/participants')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('id="participants-page"', html)
        self.assertIn('id="participants-table"', html)
        self.assertIn('id="add-participant-button"', html)
        self.assertIn('id="search-participant-input"', html)
        self.assertIn('id="participant-status-filter"', html)
    def test_07_venues_page(self):
        # Test Task 3: Venue Information page elements
        response = self.client.get('/venues')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('id="venues-page"', html)
        self.assertIn('id="venues-grid"', html)
        self.assertIn('id="venue-search-input"', html)
        self.assertIn('id="venue-capacity-filter"', html)
        # Check presence of at least one view-venue-details button with venue_id=1
        self.assertIn('id="view-venue-details-1"', html)
    def test_08_venue_details_page(self):
        # Test Task 3: Venue Details page elements for venue_id=1
        response = self.client.get('/venues/1')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('id="venue-details-page"', html)
        self.assertIn('id="venue-name"', html)
        self.assertIn('id="venue-location"', html)
        self.assertIn('id="venue-capacity"', html)
        self.assertIn('id="venue-amenities"', html)
        self.assertIn('id="venue-contact"', html)
    def test_09_schedules_page(self):
        # Test Task 3: Event Schedules page elements
        response = self.client.get('/schedules')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('id="schedules-page"', html)
        self.assertIn('id="schedules-timeline"', html)
        self.assertIn('id="schedule-filter-date"', html)
        self.assertIn('id="schedule-filter-event"', html)
        self.assertIn('id="export-schedule-button"', html)
    def test_10_bookings_summary_page(self):
        # Test Task 3: Bookings Summary page elements
        response = self.client.get('/bookings')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn('id="bookings-page"', html)
        self.assertIn('id="bookings-table"', html)
        self.assertIn('id="booking-search-input"', html)
        self.assertIn('id="back-to-dashboard"', html)
        # Check presence of cancel booking button for a booking that is not cancelled (e.g. booking_id=1)
        self.assertIn('id="cancel-booking-button-1"', html)
if __name__ == '__main__':
    unittest.main()