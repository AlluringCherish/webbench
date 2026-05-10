'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of ALL pages. This includes verifying the presence and correctness of all specified elements on each page as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class MovieTicketingTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_01_dashboard_accessible(self):
        # Test Task 1: Access dashboard page at '/'
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie Ticketing Dashboard', response.data)
    def test_02_dashboard_elements(self):
        # Test Task 2 & 3: Dashboard page elements presence and correctness
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        # Check container div id
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div)
        # Check featured movies section
        featured_section = soup.find('section', id='featured-movies')
        self.assertIsNotNone(featured_section)
        featured_movies = featured_section.find_all('div', class_='movie-card')
        self.assertTrue(len(featured_movies) > 0)
        # Check upcoming releases section
        upcoming_section = soup.find('section', id='upcoming-releases')
        self.assertIsNotNone(upcoming_section)
        # Check navigation buttons and their IDs
        browse_btn = soup.find('button', id='browse-movies-button')
        view_bookings_btn = soup.find('button', id='view-bookings-button')
        showtimes_btn = soup.find('button', id='showtimes-button')
        self.assertIsNotNone(browse_btn)
        self.assertIsNotNone(view_bookings_btn)
        self.assertIsNotNone(showtimes_btn)
    def test_03_movie_catalog_page_elements(self):
        # Test movie catalog page elements and filtering
        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        catalog_div = soup.find('div', id='catalog-page')
        self.assertIsNotNone(catalog_div)
        search_input = soup.find('input', id='search-input')
        genre_filter = soup.find('select', id='genre-filter')
        movies_grid = soup.find('div', id='movies-grid')
        self.assertIsNotNone(search_input)
        self.assertIsNotNone(genre_filter)
        self.assertIsNotNone(movies_grid)
        # Check that movie cards have view movie buttons with correct id pattern
        movie_cards = movies_grid.find_all('div', class_='movie-card')
        self.assertTrue(len(movie_cards) > 0)
        for card in movie_cards:
            button = card.find('button')
            self.assertIsNotNone(button)
            self.assertTrue(button['id'].startswith('view-movie-button-'))
    def test_04_movie_details_page_elements(self):
        # Use movie_id=1 from example data
        response = self.client.get('/movies/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='movie-details-page')
        self.assertIsNotNone(container)
        title = container.find('h1', id='movie-title')
        director = container.find('div', id='movie-director')
        rating = container.find('div', id='movie-rating')
        description = container.find('div', id='movie-description')
        select_showtime_btn = container.find('button', id='select-showtime-button')
        self.assertIsNotNone(title)
        self.assertIsNotNone(director)
        self.assertIsNotNone(rating)
        self.assertIsNotNone(description)
        self.assertIsNotNone(select_showtime_btn)
    def test_05_showtime_selection_page_elements(self):
        # Use movie_id=1 from example data
        response = self.client.get('/showtimes/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='showtime-page')
        self.assertIsNotNone(container)
        theater_filter = soup.find('select', id='theater-filter')
        date_filter = soup.find('input', id='date-filter')
        showtimes_list = soup.find('div', id='showtimes-list')
        self.assertIsNotNone(theater_filter)
        self.assertIsNotNone(date_filter)
        self.assertIsNotNone(showtimes_list)
        # Check table and select buttons
        table = showtimes_list.find('table')
        self.assertIsNotNone(table)
        rows = table.find_all('tr')
        self.assertTrue(len(rows) > 1)  # header + data rows
        # Check select buttons have correct id pattern
        select_buttons = showtimes_list.find_all('button')
        self.assertTrue(all(btn['id'].startswith('select-showtime-button-') for btn in select_buttons))
    def test_06_showtimes_overview_page_elements(self):
        response = self.client.get('/showtimes')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='showtime-page')
        self.assertIsNotNone(container)
        theater_filter = soup.find('select', id='theater-filter')
        date_filter = soup.find('input', id='date-filter')
        showtimes_list = soup.find('div', id='showtimes-list')
        self.assertIsNotNone(theater_filter)
        self.assertIsNotNone(date_filter)
        self.assertIsNotNone(showtimes_list)
        table = showtimes_list.find('table')
        self.assertIsNotNone(table)
        rows = table.find_all('tr')
        self.assertTrue(len(rows) > 1)
        select_seats_buttons = showtimes_list.find_all('button')
        self.assertTrue(all(btn['id'].startswith('select-showtime-button-') for btn in select_seats_buttons))
    def test_07_seat_selection_page_elements(self):
        # Use showtime_id=1 from example data
        response = self.client.get('/seats/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='seat-selection-page')
        self.assertIsNotNone(container)
        seat_map = soup.find('div', id='seat-map')
        selected_seats_display = soup.find('div', id='selected-seats-display')
        proceed_button = soup.find('button', id='proceed-booking-button')
        self.assertIsNotNone(seat_map)
        self.assertIsNotNone(selected_seats_display)
        self.assertIsNotNone(proceed_button)
        # Check seat buttons have correct id pattern and classes
        seat_buttons = seat_map.find_all('button')
        self.assertTrue(len(seat_buttons) > 0)
        for btn in seat_buttons:
            self.assertTrue(btn['id'].startswith('seat-'))
            self.assertIn('seat-button', btn['class'])
    def test_08_booking_confirmation_page_elements(self):
        # Simulate GET with seats param for showtime_id=1
        response = self.client.get('/booking_confirmation/1?seats=A1,A2')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='confirmation-page')
        self.assertIsNotNone(container)
        booking_summary = soup.find('div', id='booking-summary')
        customer_name_input = soup.find('input', id='customer-name')
        customer_email_input = soup.find('input', id='customer-email')
        confirm_button = soup.find('button', id='confirm-booking-button')
        self.assertIsNotNone(booking_summary)
        self.assertIsNotNone(customer_name_input)
        self.assertIsNotNone(customer_email_input)
        self.assertIsNotNone(confirm_button)
    def test_09_booking_history_page_elements(self):
        response = self.client.get('/bookings')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='bookings-page')
        self.assertIsNotNone(container)
        bookings_table = soup.find('table', id='bookings-table')
        status_filter = soup.find('select', id='status-filter')
        back_button = soup.find('button', id='back-to-dashboard')
        self.assertIsNotNone(bookings_table)
        self.assertIsNotNone(status_filter)
        self.assertIsNotNone(back_button)
        # Check booking rows and view buttons
        rows = bookings_table.find_all('tr')
        self.assertTrue(len(rows) > 1)
        view_buttons = bookings_table.find_all('button')
        self.assertTrue(all(btn['id'].startswith('view-booking-button-') for btn in view_buttons))
    def test_10_theater_information_page_elements(self):
        response = self.client.get('/theaters')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='theater-page')
        self.assertIsNotNone(container)
        location_filter = soup.find('select', id='theater-location-filter')
        theaters_list = soup.find('div', id='theaters-list')
        back_button = soup.find('button', id='back-to-dashboard')
        self.assertIsNotNone(location_filter)
        self.assertIsNotNone(theaters_list)
        self.assertIsNotNone(back_button)
        # Check theater cards presence
        theater_cards = theaters_list.find_all('div', class_='theater-card')
        self.assertTrue(len(theater_cards) > 0)
    def test_11_booking_details_page_elements(self):
        # Use booking_id=1 from example data
        response = self.client.get('/bookings/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        container = soup.find('div', id='booking-details-page')
        self.assertIsNotNone(container)
        booking_summary = container.find('div', id='booking-summary')
        movie_details = container.find('div', id='movie-details')
        showtime_details = container.find('div', id='showtime-details')
        theater_details = container.find('div', id='theater-details')
        back_link = container.find('a', class_='back-link')
        self.assertIsNotNone(booking_summary)
        self.assertIsNotNone(movie_details)
        self.assertIsNotNone(showtime_details)
        self.assertIsNotNone(theater_details)
        self.assertIsNotNone(back_link)
if __name__ == '__main__':
    unittest.main()