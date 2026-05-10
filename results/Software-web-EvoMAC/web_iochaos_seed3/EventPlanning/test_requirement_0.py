'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided.
Test the elements and integrity of ALL pages by verifying the presence and correctness of the following elements on each page:
- Dashboard Page: IDs dashboard-page, featured-events, browse-events-button, view-tickets-button, venues-button
- Events Listing Page: IDs events-page, event-search-input, event-category-filter, events-grid, view-event-button-{event_id}
- Event Details Page: IDs event-details-page, event-title, event-date, event-location, event-description, book-ticket-button
- Ticket Booking Page: IDs ticket-booking-page, select-event-dropdown, ticket-quantity-input, ticket-type-select, book-now-button, booking-confirmation (conditional)
- Participants Management Page: IDs participants-page, participants-table, add-participant-button, search-participant-input, participant-status-filter
- Venue Information Page: IDs venues-page, venues-grid, venue-search-input, venue-capacity-filter, view-venue-details-{venue_id}
- Event Schedules Page: IDs schedules-page, schedules-timeline, schedule-filter-date, schedule-filter-event, export-schedule-button
- Bookings Summary Page: IDs bookings-page, bookings-table, booking-search-input, cancel-booking-button-{booking_id}, back-to-dashboard
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class EventPlanningAppTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_dashboard_access_and_elements(self):
        # Access dashboard page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check container div
        self.assertIsNotNone(soup.find(id='dashboard-page'))
        # Check featured events section
        self.assertIsNotNone(soup.find(id='featured-events'))
        # Check buttons
        self.assertIsNotNone(soup.find(id='browse-events-button'))
        self.assertIsNotNone(soup.find(id='view-tickets-button'))
        self.assertIsNotNone(soup.find(id='venues-button'))
    def test_events_listing_page_elements(self):
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='events-page'))
        self.assertIsNotNone(soup.find(id='event-search-input'))
        self.assertIsNotNone(soup.find(id='event-category-filter'))
        self.assertIsNotNone(soup.find(id='events-grid'))
        # Check at least one view-event-button-{event_id} if events exist
        buttons = soup.find_all('button')
        found_view_event_button = any(btn.get('id', '').startswith('view-event-button-') for btn in buttons)
        # It is possible no events, so no buttons, but example data has events, so expect True
        self.assertTrue(found_view_event_button)
    def test_event_details_page_elements(self):
        # Use example event_id=1 from example data
        response = self.client.get('/event/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='event-details-page'))
        self.assertIsNotNone(soup.find(id='event-title'))
        self.assertIsNotNone(soup.find(id='event-date'))
        self.assertIsNotNone(soup.find(id='event-location'))
        self.assertIsNotNone(soup.find(id='event-description'))
        self.assertIsNotNone(soup.find(id='book-ticket-button'))
    def test_ticket_booking_page_elements_get(self):
        response = self.client.get('/book-tickets')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='ticket-booking-page'))
        self.assertIsNotNone(soup.find(id='select-event-dropdown'))
        self.assertIsNotNone(soup.find(id='ticket-quantity-input'))
        self.assertIsNotNone(soup.find(id='ticket-type-select'))
        self.assertIsNotNone(soup.find(id='book-now-button'))
        # booking-confirmation should not be present on GET
        self.assertIsNone(soup.find(id='booking-confirmation'))
    def test_participants_management_page_elements_get(self):
        response = self.client.get('/participants')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='participants-page'))
        self.assertIsNotNone(soup.find(id='participants-table'))
        self.assertIsNotNone(soup.find(id='add-participant-button'))
        self.assertIsNotNone(soup.find(id='search-participant-input'))
        self.assertIsNotNone(soup.find(id='participant-status-filter'))
    def test_venues_page_elements(self):
        response = self.client.get('/venues')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='venues-page'))
        self.assertIsNotNone(soup.find(id='venues-grid'))
        self.assertIsNotNone(soup.find(id='venue-search-input'))
        self.assertIsNotNone(soup.find(id='venue-capacity-filter'))
        # Check at least one view-venue-details-{venue_id} button exists (example data has venues)
        buttons = soup.find_all('button')
        found_venue_detail_button = any(btn.get('id', '').startswith('view-venue-details-') for btn in buttons)
        self.assertTrue(found_venue_detail_button)
    def test_event_schedules_page_elements(self):
        response = self.client.get('/schedules')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='schedules-page'))
        self.assertIsNotNone(soup.find(id='schedules-timeline'))
        self.assertIsNotNone(soup.find(id='schedule-filter-date'))
        self.assertIsNotNone(soup.find(id='schedule-filter-event'))
        self.assertIsNotNone(soup.find(id='export-schedule-button'))
    def test_bookings_summary_page_elements_get(self):
        response = self.client.get('/bookings')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertIsNotNone(soup.find(id='bookings-page'))
        self.assertIsNotNone(soup.find(id='bookings-table'))
        self.assertIsNotNone(soup.find(id='booking-search-input'))
        self.assertIsNotNone(soup.find(id='back-to-dashboard'))
        # Check presence of cancel-booking-button-{booking_id} if bookings exist (example data has bookings)
        buttons = soup.find_all('button')
        found_cancel_button = any(btn.get('id', '').startswith('cancel-booking-button-') for btn in buttons)
        self.assertTrue(found_cancel_button)
if __name__ == '__main__':
    unittest.main()