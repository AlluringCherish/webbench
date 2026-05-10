'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website (Dashboard) loads correctly and basic navigation works based on example data.
Test the elements and integrity of ALL pages, verifying presence and correctness of all specified elements as per requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class OnlineLibraryTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.username = 'john_reader'  # From example data
    def login(self):
        # Login helper
        return self.client.post('/login', data={'username': self.username}, follow_redirects=True)
    def logout(self):
        return self.client.get('/logout', follow_redirects=True)
    def test_01_access_login_page(self):
        # Test access to login page
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a username', response.data or b'')  # Not shown initially, but page loads
    def test_02_login_and_access_dashboard(self):
        # Login and access dashboard page
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, john_reader!', response.data)
        # Check dashboard page elements
        soup = BeautifulSoup(response.data, 'html.parser')
        dashboard_div = soup.find(id='dashboard-page')
        self.assertIsNotNone(dashboard_div)
        welcome_msg = soup.find(id='welcome-message')
        self.assertIsNotNone(welcome_msg)
        self.assertIn('john_reader', welcome_msg.text)
        browse_button = soup.find(id='browse-books-button')
        self.assertIsNotNone(browse_button)
        my_borrows_button = soup.find(id='my-borrows-button')
        self.assertIsNotNone(my_borrows_button)
    def test_03_navigation_to_book_catalog(self):
        self.login()
        response = self.client.get('/book_catalog')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        catalog_div = soup.find(id='catalog-page')
        self.assertIsNotNone(catalog_div)
        search_input = soup.find(id='search-input')
        self.assertIsNotNone(search_input)
        book_grid = soup.find(id='book-grid')
        self.assertIsNotNone(book_grid)
        back_button = soup.find(id='back-to-dashboard')
        self.assertIsNotNone(back_button)
    def test_04_navigation_to_book_details(self):
        self.login()
        # Use book_id=1 from example data
        response = self.client.get('/book_details/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        details_div = soup.find(id='book-details-page')
        self.assertIsNotNone(details_div)
        title = soup.find(id='book-title')
        self.assertIsNotNone(title)
        self.assertIn('To Kill a Mockingbird', title.text)
        author = soup.find(id='book-author')
        self.assertIsNotNone(author)
        status = soup.find(id='book-status')
        self.assertIsNotNone(status)
        borrow_button = soup.find(id='borrow-button')
        self.assertIsNotNone(borrow_button)
        reviews_section = soup.find(id='reviews-section')
        self.assertIsNotNone(reviews_section)
        write_review_button = soup.find(id='write-review-button')
        self.assertIsNotNone(write_review_button)
        back_to_catalog = soup.find(id='back-to-catalog')
        self.assertIsNotNone(back_to_catalog)
    def test_05_borrow_confirmation_page(self):
        self.login()
        # Book 1 is Available in example data
        response = self.client.get('/borrow_confirmation/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        borrow_page = soup.find(id='borrow-page')
        self.assertIsNotNone(borrow_page)
        borrow_info = soup.find(id='borrow-book-info')
        self.assertIsNotNone(borrow_info)
        due_date_display = soup.find(id='due-date-display')
        self.assertIsNotNone(due_date_display)
        confirm_button = soup.find(id='confirm-borrow-button')
        self.assertIsNotNone(confirm_button)
        cancel_button = soup.find(id='cancel-borrow-button')
        self.assertIsNotNone(cancel_button)
    def test_06_my_borrowings_page(self):
        self.login()
        response = self.client.get('/my_borrowings')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        my_borrows_page = soup.find(id='my-borrows-page')
        self.assertIsNotNone(my_borrows_page)
        filter_status = soup.find(id='filter-status')
        self.assertIsNotNone(filter_status)
        borrows_table = soup.find(id='borrows-table')
        self.assertIsNotNone(borrows_table)
        # Check table headers
        headers = [th.text.strip() for th in borrows_table.find_all('th')]
        expected_headers = ['Title', 'Borrow Date', 'Due Date', 'Status', 'Fine Amount', 'Action']
        self.assertEqual(headers, expected_headers)
    def test_07_my_reservations_page(self):
        self.login()
        response = self.client.get('/my_reservations')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        reservations_page = soup.find(id='reservations-page')
        self.assertIsNotNone(reservations_page)
        reservations_table = soup.find(id='reservations-table')
        self.assertIsNotNone(reservations_table)
        headers = [th.text.strip() for th in reservations_table.find_all('th')]
        expected_headers = ['Title', 'Reservation Date', 'Status', 'Action']
        self.assertEqual(headers, expected_headers)
    def test_08_my_reviews_page(self):
        self.login()
        response = self.client.get('/my_reviews')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        reviews_page = soup.find(id='reviews-page')
        self.assertIsNotNone(reviews_page)
        reviews_list = soup.find(id='reviews-list')
        self.assertIsNotNone(reviews_list)
    def test_09_write_review_page(self):
        self.login()
        # Test new review page for book_id=1
        response = self.client.get('/write_review/1')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        write_review_page = soup.find(id='write-review-page')
        self.assertIsNotNone(write_review_page)
        book_info = soup.find(id='book-info-display')
        self.assertIsNotNone(book_info)
        rating_input = soup.find(id='rating-input')
        self.assertIsNotNone(rating_input)
        review_text = soup.find(id='review-text')
        self.assertIsNotNone(review_text)
        submit_button = soup.find(id='submit-review-button')
        self.assertIsNotNone(submit_button)
        back_to_book = soup.find(id='back-to-book')
        self.assertIsNotNone(back_to_book)
    def test_10_user_profile_page(self):
        self.login()
        response = self.client.get('/user_profile')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        profile_page = soup.find(id='profile-page')
        self.assertIsNotNone(profile_page)
        profile_username = soup.find(id='profile-username')
        self.assertIsNotNone(profile_username)
        profile_email = soup.find(id='profile-email')
        self.assertIsNotNone(profile_email)
        update_button = soup.find(id='update-profile-button')
        self.assertIsNotNone(update_button)
        borrow_history = soup.find(id='borrow-history')
        self.assertIsNotNone(borrow_history)
    def test_11_payment_confirmation_page(self):
        self.login()
        # Use borrow_id=3 which has unpaid fine in example data
        response = self.client.get('/payment_confirmation/3')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.data, 'html.parser')
        payment_page = soup.find(id='payment-page')
        self.assertIsNotNone(payment_page)
        fine_amount_display = soup.find(id='fine-amount-display')
        self.assertIsNotNone(fine_amount_display)
        confirm_payment_button = soup.find(id='confirm-payment-button')
        self.assertIsNotNone(confirm_payment_button)
        back_to_profile = soup.find(id='back-to-profile')
        self.assertIsNotNone(back_to_profile)
    def test_12_logout(self):
        self.login()
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out.', response.data)
if __name__ == '__main__':
    unittest.main()