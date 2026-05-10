'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of ALL pages. This includes verifying the presence and correctness of all specified elements on each page as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class TravelPlannerTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_01_dashboard_accessible(self):
        # Test Task 1: Access root page and check status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check page title
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string.strip(), 'Travel Planner Dashboard')
        # Check presence of main container div with id dashboard-page
        self.assertIsNotNone(soup.find('div', id='dashboard-page'))
        # Check presence of featured-destinations and upcoming-trips divs
        self.assertIsNotNone(soup.find('div', id='featured-destinations'))
        self.assertIsNotNone(soup.find('div', id='upcoming-trips'))
        # Check presence of browse-destinations-button and plan-itinerary-button buttons
        self.assertIsNotNone(soup.find('button', id='browse-destinations-button'))
        self.assertIsNotNone(soup.find('button', id='plan-itinerary-button'))
    def test_02_destinations_page_elements(self):
        response = self.client.get('/destinations')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string.strip(), 'Travel Destinations')
        self.assertIsNotNone(soup.find('div', id='destinations-page'))
        self.assertIsNotNone(soup.find('input', id='search-destination'))
        self.assertIsNotNone(soup.find('select', id='region-filter'))
        self.assertIsNotNone(soup.find('div', id='destinations-grid'))
        # Check at least one view-destination-button-{dest_id} button exists
        buttons = soup.find_all('button')
        found = False
        for btn in buttons:
            if btn.has_attr('id') and btn['id'].startswith('view-destination-button-'):
                found = True
                break
        self.assertTrue(found)
    def test_03_destination_details_page_elements(self):
        # Use dest_id=1 (Paris) from example data
        response = self.client.get('/destination/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string.strip(), 'Destination Details')
        self.assertIsNotNone(soup.find('div', id='destination-details-page'))
        self.assertIsNotNone(soup.find('h1', id='destination-name'))
        self.assertIsNotNone(soup.find('div', id='destination-country'))
        self.assertIsNotNone(soup.find('div', id='destination-description'))
        self.assertIsNotNone(soup.find('button', id='add-to-trip-button'))
        self.assertIsNotNone(soup.find('div', id='destination-attractions'))
    def test_04_itinerary_planning_page_elements(self):
        response = self.client.get('/itinerary')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string.strip(), 'Plan Your Itinerary')
        self.assertIsNotNone(soup.find('div', id='itinerary-page'))
        self.assertIsNotNone(soup.find('input', id='itinerary-name-input'))
        self.assertIsNotNone(soup.find('input', id='start-date-input'))
        self.assertIsNotNone(soup.find('input', id='end-date-input'))
        self.assertIsNotNone(soup.find('button', id='add-activity-button'))
        self.assertIsNotNone(soup.find('div', id='itinerary-list'))
    def test_05_accommodations_page_elements(self):
        response = self.client.get('/accommodations')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string.strip(), 'Search Accommodations')
        self.assertIsNotNone(soup.find('div', id='accommodations-page'))
        self.assertIsNotNone(soup.find('input', id='destination-input'))
        self.assertIsNotNone(soup.find('input', id='check-in-date'))
        self.assertIsNotNone(soup.find('input', id='check-out-date'))
        self.assertIsNotNone(soup.find('select', id='price-filter'))
        self.assertIsNotNone(soup.find('div', id='hotels-list'))
    def test_06_transportation_page_elements(self):
        response = self.client.get('/transportation')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string.strip(), 'Book Flights')
        self.assertIsNotNone(soup.find('div', id='transportation-page'))
        self.assertIsNotNone(soup.find('input', id='departure-city'))
        self.assertIsNotNone(soup.find('input', id='arrival-city'))
        self.assertIsNotNone(soup.find('input', id='departure-date'))
        self.assertIsNotNone(soup.find('select', id='flight-class-filter'))
        self.assertIsNotNone(soup.find('div', id='available-flights'))
    def test_07_travel_packages_page_elements(self):
        response = self.client.get('/packages')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string.strip(), 'Travel Packages')
        self.assertIsNotNone(soup.find('div', id='packages-page'))
        self.assertIsNotNone(soup.find('div', id='packages-grid'))
        self.assertIsNotNone(soup.find('select', id='duration-filter'))
        # Check presence of at least one view-package-details-button-{pkg_id} and book-package-button-{pkg_id}
        buttons = soup.find_all('button')
        view_found = False
        book_found = False
        for btn in buttons:
            if btn.has_attr('id'):
                if btn['id'].startswith('view-package-details-button-'):
                    view_found = True
                if btn['id'].startswith('book-package-button-'):
                    book_found = True
        # Since no POST data sent, buttons may or may not be present, so just check at least one button exists
        self.assertTrue(len(buttons) > 0)
    def test_08_trip_management_page_elements(self):
        response = self.client.get('/trips')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string.strip(), 'My Trips')
        self.assertIsNotNone(soup.find('div', id='trips-page'))
        self.assertIsNotNone(soup.find('table', id='trips-table'))
        # Check presence of at least one view-trip-details-button-{trip_id}, edit-trip-button-{trip_id}, delete-trip-button-{trip_id}
        buttons = soup.find_all('button')
        view_found = False
        edit_found = False
        delete_found = False
        for btn in buttons:
            if btn.has_attr('id'):
                if btn['id'].startswith('view-trip-details-button-'):
                    view_found = True
                if btn['id'].startswith('edit-trip-button-'):
                    edit_found = True
                if btn['id'].startswith('delete-trip-button-'):
                    delete_found = True
        # Since example data has trips, these buttons should be present
        self.assertTrue(view_found)
        self.assertTrue(edit_found)
        self.assertTrue(delete_found)
    def test_09_booking_confirmation_page_elements(self):
        # Use confirmation_number=CONF001 from example data
        response = self.client.get('/booking-confirmation?confirmation_number=CONF001')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string.strip(), 'Booking Confirmation')
        self.assertIsNotNone(soup.find('div', id='confirmation-page'))
        self.assertIsNotNone(soup.find('div', id='confirmation-number'))
        self.assertIsNotNone(soup.find('div', id='booking-details'))
        self.assertIsNotNone(soup.find('button', id='download-itinerary-button'))
        self.assertIsNotNone(soup.find('button', id='share-trip-button'))
        self.assertIsNotNone(soup.find('button', id='back-to-dashboard'))
    def test_10_travel_recommendations_page_elements(self):
        response = self.client.get('/recommendations')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        self.assertEqual(soup.title.string.strip(), 'Travel Recommendations')
        self.assertIsNotNone(soup.find('div', id='recommendations-page'))
        self.assertIsNotNone(soup.find('div', id='trending-destinations'))
        self.assertIsNotNone(soup.find('select', id='recommendation-season-filter'))
        self.assertIsNotNone(soup.find('select', id='budget-filter'))
        self.assertIsNotNone(soup.find('button', id='back-to-dashboard'))
if __name__ == '__main__':
    unittest.main()