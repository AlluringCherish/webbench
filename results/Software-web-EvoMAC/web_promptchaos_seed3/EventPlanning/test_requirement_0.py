'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of all pages. This includes verifying the presence and correctness of all specified elements on each page as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class EventPlanningAppTest(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_01_dashboard_accessible(self):
        # Test Task 1: Access root '/' and check status code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_02_dashboard_content(self):
        # Test Task 2: Dashboard page loads correctly with required elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check container div id
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard container div missing")
        # Check featured-events section and its id
        featured_events = dashboard_div.find('section', id='featured-events')
        self.assertIsNotNone(featured_events, "Featured events section missing")
        # Check featured-venues section and its id
        featured_venues = dashboard_div.find('section', id='featured-venues')
        self.assertIsNotNone(featured_venues, "Featured venues section missing")
        # Check navigation buttons and their ids
        browse_btn = dashboard_div.find('button', id='browse-events-button')
        self.assertIsNotNone(browse_btn, "Browse Events button missing")
        view_tickets_btn = dashboard_div.find('button', id='view-tickets-button')
        self.assertIsNotNone(view_tickets_btn, "View Tickets button missing")
        venues_btn = dashboard_div.find('button', id='venues-button')
        self.assertIsNotNone(venues_btn, "Venues button missing")
    def test_03_basic_navigation(self):
        # Test Task 2: Basic navigation from dashboard buttons leads to correct pages
        # Browse Events button
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        events_div = soup.find('div', id='events-page')
        self.assertIsNotNone(events_div, "Events listing page container missing")
        # View Tickets button
        response = self.client.get('/tickets')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        tickets_div = soup.find('div', id='ticket-booking-page')
        self.assertIsNotNone(tickets_div, "Ticket booking page container missing")
        # Venues button
        response = self.client.get('/venues')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        venues_div = soup.find('div', id='venues-page')
        self.assertIsNotNone(venues_div, "Venues page container missing")
    def test_04_events_listing_elements(self):
        # Test Task 3: Verify all specified elements on Events Listing page
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        events_page_div = soup.find('div', id='events-page')
        self.assertIsNotNone(events_page_div, "Events listing container missing")
        search_input = events_page_div.find('input', id='event-search-input')
        self.assertIsNotNone(search_input, "Event search input missing")
        category_filter = events_page_div.find('select', id='event-category-filter')
        self.assertIsNotNone(category_filter, "Event category filter dropdown missing")
        events_grid = events_page_div.find('div', id='events-grid')
        self.assertIsNotNone(events_grid, "Events grid container missing")
        # Check at least one event card with view-event-button-{event_id}
        buttons = events_grid.find_all('button')
        self.assertTrue(any(btn['id'].startswith('view-event-button-') for btn in buttons if btn.has_attr('id')),
                        "No view-event-button-{event_id} found in events grid")
    def test_05_event_details_elements(self):
        # Test Task 3: Verify all specified elements on Event Details page for event_id=1
        response = self.client.get('/event/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='event-details-page')
        self.assertIsNotNone(container, "Event details container missing")
        self.assertIsNotNone(container.find('h1', id='event-title'), "Event title missing")
        self.assertIsNotNone(container.find('div', id='event-date'), "Event date missing")
        self.assertIsNotNone(container.find('div', id='event-location'), "Event location missing")
        self.assertIsNotNone(container.find('div', id='event-description'), "Event description missing")
        self.assertIsNotNone(container.find('button', id='book-ticket-button'), "Book ticket button missing")
    def test_06_ticket_booking_elements(self):
        # Test Task 3: Verify all specified elements on Ticket Booking page
        response = self.client.get('/tickets')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='ticket-booking-page')
        self.assertIsNotNone(container, "Ticket booking container missing")
        self.assertIsNotNone(container.find('select', id='select-event-dropdown'), "Select event dropdown missing")
        self.assertIsNotNone(container.find('input', id='ticket-quantity-input'), "Ticket quantity input missing")
        self.assertIsNotNone(container.find('select', id='ticket-type-select'), "Ticket type select missing")
        self.assertIsNotNone(container.find('button', id='book-now-button'), "Book now button missing")
    def test_07_participants_management_elements(self):
        # Test Task 3: Verify all specified elements on Participants Management page
        response = self.client.get('/participants')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='participants-page')
        self.assertIsNotNone(container, "Participants page container missing")
        self.assertIsNotNone(container.find('table', id='participants-table'), "Participants table missing")
        self.assertIsNotNone(container.find('button', id='add-participant-button'), "Add participant button missing")
        self.assertIsNotNone(container.find('input', id='search-participant-input'), "Search participant input missing")
        self.assertIsNotNone(container.find('select', id='participant-status-filter'), "Participant status filter missing")
    def test_08_venues_page_elements(self):
        # Test Task 3: Verify all specified elements on Venues page
        response = self.client.get('/venues')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='venues-page')
        self.assertIsNotNone(container, "Venues page container missing")
        self.assertIsNotNone(container.find('div', id='venues-grid'), "Venues grid missing")
        self.assertIsNotNone(container.find('input', id='venue-search-input'), "Venue search input missing")
        self.assertIsNotNone(container.find('select', id='venue-capacity-filter'), "Venue capacity filter missing")
        # Check at least one venue card with view-venue-details-{venue_id} button
        buttons = container.find_all('button')
        self.assertTrue(any(btn['id'].startswith('view-venue-details-') for btn in buttons if btn.has_attr('id')),
                        "No view-venue-details-{venue_id} button found in venues grid")
    def test_09_schedules_page_elements(self):
        # Test Task 3: Verify all specified elements on Event Schedules page
        response = self.client.get('/schedules')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='schedules-page')
        self.assertIsNotNone(container, "Schedules page container missing")
        self.assertIsNotNone(container.find('div', id='schedules-timeline'), "Schedules timeline missing")
        self.assertIsNotNone(container.find('input', id='schedule-filter-date'), "Schedule filter date input missing")
        self.assertIsNotNone(container.find('select', id='schedule-filter-event'), "Schedule filter event dropdown missing")
        self.assertIsNotNone(container.find('button', id='export-schedule-button'), "Export schedule button missing")
    def test_10_bookings_summary_elements(self):
        # Test Task 3: Verify all specified elements on Bookings Summary page
        response = self.client.get('/bookings')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='bookings-page')
        self.assertIsNotNone(container, "Bookings page container missing")
        self.assertIsNotNone(container.find('table', id='bookings-table'), "Bookings table missing")
        self.assertIsNotNone(container.find('input', id='booking-search-input'), "Booking search input missing")
        self.assertIsNotNone(container.find('button', id='back-to-dashboard'), "Back to dashboard button missing")
        # Check presence of cancel booking buttons with correct id pattern if bookings exist
        cancel_buttons = container.find_all('button')
        cancel_btns = [btn for btn in cancel_buttons if btn.has_attr('id') and btn['id'].startswith('cancel-booking-button-')]
        # It's possible no bookings or all cancelled, so no cancel buttons is acceptable
        # But if bookings exist and not cancelled, at least one cancel button should be present
        # We check that if bookings exist and status != Cancelled, cancel button present
        bookings_rows = container.find_all('tr')[1:]  # skip header
        has_active_booking = False
        for row in bookings_rows:
            cols = row.find_all('td')
            if len(cols) >= 7:
                status = cols[6].text.strip()
                if status != 'Cancelled':
                    has_active_booking = True
                    break
        if has_active_booking:
            self.assertTrue(len(cancel_btns) > 0, "No cancel booking buttons found for active bookings")
if __name__ == '__main__':
    unittest.main()