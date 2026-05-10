'''
Test whether the website can be accessed through local port 5000.
Test whether the first page of the website loads correctly and whether basic navigation works based on the example data provided in the Task.
Test the elements and integrity of ALL pages. This includes verifying the presence and correctness of all specified elements on each page as per the requirements.
'''
import unittest
from main import app
from bs4 import BeautifulSoup
class OnlineLibraryTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client
        app.config['TESTING'] = True
        self.client = app.test_client()
    def test_01_dashboard_accessible_and_elements(self):
        # Test Task 1 & 2: Access dashboard page and check basic elements
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div
        dashboard_div = soup.find('div', id='dashboard-page')
        self.assertIsNotNone(dashboard_div, "Dashboard container div missing")
        # Check welcome message with username
        welcome_msg = soup.find('h1', id='welcome-message')
        self.assertIsNotNone(welcome_msg, "Welcome message missing")
        self.assertIn('john_reader', welcome_msg.text, "Username not in welcome message")
        # Check featured books list (top 3 by avg_rating)
        featured_books_div = soup.find('div', id='featured-books')
        self.assertIsNotNone(featured_books_div, "Featured books section missing")
        featured_list = featured_books_div.find('ul')
        self.assertIsNotNone(featured_list, "Featured books list missing")
        featured_items = featured_list.find_all('li')
        self.assertTrue(len(featured_items) > 0, "No featured books listed")
        self.assertLessEqual(len(featured_items), 3, "More than 3 featured books shown")
        # Check each featured book has title, author, rating, and view details button
        for li in featured_items:
            text = li.get_text()
            self.assertRegex(text, r'.+ by .+ \(Rating: \d+(\.\d+)?\)', "Featured book text format incorrect")
            button = li.find('button')
            self.assertIsNotNone(button, "View Details button missing in featured book")
            self.assertTrue(button['id'].startswith('view-book-button-'), "View Details button id incorrect")
        # Check navigation buttons
        browse_btn = soup.find('button', id='browse-books-button')
        self.assertIsNotNone(browse_btn, "Browse Books button missing")
        my_borrows_btn = soup.find('button', id='my-borrows-button')
        self.assertIsNotNone(my_borrows_btn, "My Borrowings button missing")
    def test_02_navigation_from_dashboard_to_catalog_and_back(self):
        # Navigate to catalog page from dashboard
        response = self.client.get('/catalog')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check catalog page container
        catalog_div = soup.find('div', id='catalog-page')
        self.assertIsNotNone(catalog_div, "Catalog page container missing")
        # Check search input
        search_input = soup.find('input', id='search-input')
        self.assertIsNotNone(search_input, "Search input missing on catalog page")
        # Check book grid container
        book_grid = soup.find('div', id='book-grid')
        self.assertIsNotNone(book_grid, "Book grid missing on catalog page")
        # Check each book card has title, author, status, and view details button
        book_cards = book_grid.find_all('div', class_='book-card')
        self.assertTrue(len(book_cards) > 0, "No book cards found in catalog")
        for card in book_cards:
            title = card.find('h3')
            self.assertIsNotNone(title, "Book title missing in book card")
            author_p = card.find('p', string=lambda text: text and text.startswith('Author:'))
            self.assertIsNotNone(author_p, "Author info missing in book card")
            status_p = card.find('p', string=lambda text: text and text.startswith('Status:'))
            self.assertIsNotNone(status_p, "Status info missing in book card")
            view_btn = card.find('button', id=lambda x: x and x.startswith('view-book-button-'))
            self.assertIsNotNone(view_btn, "View Details button missing in book card")
        # Check back to dashboard button
        back_btn = catalog_div.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to Dashboard button missing on catalog page")
        # Test navigation back to dashboard
        response_back = self.client.get('/')
        self.assertEqual(response_back.status_code, 200)
    def test_03_book_details_page_elements(self):
        # Pick a book_id from example data: '1' (To Kill a Mockingbird)
        response = self.client.get('/book/1')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        # Check container div
        details_div = soup.find('div', id='book-details-page')
        self.assertIsNotNone(details_div, "Book details container missing")
        # Check book title, author, status
        title_h1 = soup.find('h1', id='book-title')
        self.assertIsNotNone(title_h1, "Book title missing")
        self.assertIn('To Kill a Mockingbird', title_h1.text)
        author_div = soup.find('div', id='book-author')
        self.assertIsNotNone(author_div, "Book author missing")
        self.assertIn('Harper Lee', author_div.text)
        status_div = soup.find('div', id='book-status')
        self.assertIsNotNone(status_div, "Book status missing")
        self.assertIn(status_div.text.strip(), ['Status: Available', 'Status: Borrowed', 'Status: Reserved'])
        # Check borrow button presence and enabled/disabled state
        borrow_btn = soup.find('button', id='borrow-button')
        self.assertIsNotNone(borrow_btn, "Borrow button missing")
        # Check reviews section
        reviews_section = soup.find('div', id='reviews-section')
        self.assertIsNotNone(reviews_section, "Reviews section missing")
        # It should have h2 Reviews
        h2 = reviews_section.find('h2')
        self.assertIsNotNone(h2)
        self.assertEqual(h2.text.strip(), 'Reviews')
        # Check write review button
        write_review_btn = soup.find('button', id='write-review-button')
        self.assertIsNotNone(write_review_btn, "Write Review button missing")
        # Check back to catalog button
        back_btn = soup.find('button', id='back-to-catalog')
        self.assertIsNotNone(back_btn, "Back to Catalog button missing")
    def test_04_borrow_confirmation_page_elements(self):
        # Use book_id '5' which is Available in example data
        response = self.client.get('/borrow/5')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        borrow_div = soup.find('div', id='borrow-page')
        self.assertIsNotNone(borrow_div, "Borrow confirmation container missing")
        # Check book info display
        book_info = borrow_div.find('div', id='borrow-book-info')
        self.assertIsNotNone(book_info, "Borrow book info missing")
        self.assertIn('Title:', book_info.text)
        self.assertIn('Author:', book_info.text)
        # Check due date display
        due_date_div = borrow_div.find('div', id='due-date-display')
        self.assertIsNotNone(due_date_div, "Due date display missing")
        self.assertIn('Due Date:', due_date_div.text)
        # Confirm and cancel buttons
        confirm_btn = borrow_div.find('button', id='confirm-borrow-button')
        self.assertIsNotNone(confirm_btn, "Confirm borrow button missing")
        cancel_btn = borrow_div.find('button', id='cancel-borrow-button')
        self.assertIsNotNone(cancel_btn, "Cancel borrow button missing")
    def test_05_my_borrowings_page_elements(self):
        response = self.client.get('/my_borrowings')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        my_borrows_div = soup.find('div', id='my-borrows-page')
        self.assertIsNotNone(my_borrows_div, "My Borrowings container missing")
        # Filter dropdown
        filter_dropdown = my_borrows_div.find('select', id='filter-status')
        self.assertIsNotNone(filter_dropdown, "Filter status dropdown missing")
        options = [opt['value'] for opt in filter_dropdown.find_all('option')]
        self.assertListEqual(options, ['All', 'Active', 'Returned', 'Overdue'])
        # Borrows table
        borrows_table = my_borrows_div.find('table', id='borrows-table')
        self.assertIsNotNone(borrows_table, "Borrows table missing")
        headers = [th.text.strip() for th in borrows_table.find_all('th')]
        expected_headers = ['Title', 'Borrow Date', 'Due Date', 'Status', 'Fine Amount', 'Actions']
        self.assertListEqual(headers, expected_headers)
        # Check at least one row exists (based on example data)
        rows = borrows_table.find('tbody').find_all('tr')
        self.assertTrue(len(rows) > 0, "No borrowings listed")
        # Check return book button or disabled returned button in actions column
        for row in rows:
            status = row.find_all('td')[3].text.strip()
            actions_td = row.find_all('td')[5]
            if status in ['Active', 'Overdue']:
                btn = actions_td.find('button')
                self.assertIsNotNone(btn, "Return book button missing for active/overdue borrow")
                self.assertFalse(btn.has_attr('disabled'), "Return book button should be enabled")
            else:
                btn = actions_td.find('button')
                self.assertIsNotNone(btn, "Returned button missing for returned borrow")
                self.assertTrue(btn.has_attr('disabled'), "Returned button should be disabled")
        # Back to dashboard button
        back_btn = my_borrows_div.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to Dashboard button missing on My Borrowings page")
    def test_06_my_reservations_page_elements(self):
        response = self.client.get('/my_reservations')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        reservations_div = soup.find('div', id='reservations-page')
        self.assertIsNotNone(reservations_div, "Reservations page container missing")
        reservations_table = reservations_div.find('table', id='reservations-table')
        self.assertIsNotNone(reservations_table, "Reservations table missing")
        headers = [th.text.strip() for th in reservations_table.find_all('th')]
        expected_headers = ['Title', 'Reservation Date', 'Status', 'Actions']
        self.assertListEqual(headers, expected_headers)
        rows = reservations_table.find('tbody').find_all('tr')
        self.assertTrue(len(rows) > 0, "No reservations listed")
        for row in rows:
            status = row.find_all('td')[2].text.strip()
            actions_td = row.find_all('td')[3]
            if status == 'Active':
                btn = actions_td.find('button')
                self.assertIsNotNone(btn, "Cancel reservation button missing for active reservation")
                self.assertFalse(btn.has_attr('disabled'), "Cancel reservation button should be enabled")
            else:
                btn = actions_td.find('button')
                self.assertIsNotNone(btn, "Cancelled button missing for cancelled reservation")
                self.assertTrue(btn.has_attr('disabled'), "Cancelled button should be disabled")
        back_btn = reservations_div.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to Dashboard button missing on Reservations page")
    def test_07_my_reviews_page_elements(self):
        response = self.client.get('/my_reviews')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        reviews_div = soup.find('div', id='reviews-page')
        self.assertIsNotNone(reviews_div, "My Reviews container missing")
        reviews_list = reviews_div.find('div', id='reviews-list')
        self.assertIsNotNone(reviews_list, "Reviews list missing")
        # If reviews exist, check list and buttons
        ul = reviews_list.find('ul')
        if ul:
            items = ul.find_all('li')
            self.assertTrue(len(items) > 0, "No reviews listed despite ul present")
            for li in items:
                # Check edit and delete buttons
                edit_btn = li.find('button', id=lambda x: x and x.startswith('edit-review-button-'))
                delete_btn = li.find('button', id=lambda x: x and x.startswith('delete-review-button-'))
                self.assertIsNotNone(edit_btn, "Edit review button missing")
                self.assertIsNotNone(delete_btn, "Delete review button missing")
        else:
            # No reviews message present
            p = reviews_list.find('p')
            self.assertIsNotNone(p, "No reviews message missing when no reviews")
        back_btn = reviews_div.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to Dashboard button missing on My Reviews page")
    def test_08_write_review_page_elements(self):
        # Use book_id '1' for write review page
        response = self.client.get('/write_review/1')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        write_div = soup.find('div', id='write-review-page')
        self.assertIsNotNone(write_div, "Write Review container missing")
        # Book info display
        book_info = write_div.find('div', id='book-info-display')
        self.assertIsNotNone(book_info, "Book info display missing")
        self.assertIn('Author:', book_info.text)
        # Rating dropdown
        rating_select = write_div.find('select', id='rating-input')
        self.assertIsNotNone(rating_select, "Rating input dropdown missing")
        options = rating_select.find_all('option')
        self.assertEqual(len(options), 6)  # 1 empty + 5 stars
        # Review textarea
        review_textarea = write_div.find('textarea', id='review-text')
        self.assertIsNotNone(review_textarea, "Review text area missing")
        # Submit button
        submit_btn = write_div.find('button', id='submit-review-button')
        self.assertIsNotNone(submit_btn, "Submit review button missing")
        # Back to book details button
        back_btn = write_div.find('button', id='back-to-book')
        self.assertIsNotNone(back_btn, "Back to Book Details button missing")
    def test_09_user_profile_page_elements(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        profile_div = soup.find('div', id='profile-page')
        self.assertIsNotNone(profile_div, "Profile page container missing")
        # Username display (not editable)
        username_div = profile_div.find('div', id='profile-username')
        self.assertIsNotNone(username_div, "Username display missing")
        self.assertIn('john_reader', username_div.text)
        # Email input field
        email_input = profile_div.find('input', id='profile-email')
        self.assertIsNotNone(email_input, "Email input missing")
        self.assertEqual(email_input['type'], 'email')
        # Update profile button
        update_btn = profile_div.find('button', id='update-profile-button')
        self.assertIsNotNone(update_btn, "Update profile button missing")
        # Borrow history display
        borrow_history_div = profile_div.find('div', id='borrow-history')
        self.assertIsNotNone(borrow_history_div, "Borrow history section missing")
        # Back to dashboard button
        back_btn = profile_div.find('button', id='back-to-dashboard')
        self.assertIsNotNone(back_btn, "Back to Dashboard button missing on Profile page")
    def test_10_payment_confirmation_page_elements(self):
        # Use borrow_id '3' which has unpaid fine in example data
        response = self.client.get('/payment/3')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        payment_div = soup.find('div', id='payment-page')
        self.assertIsNotNone(payment_div, "Payment confirmation container missing")
        fine_display = payment_div.find('div', id='fine-amount-display')
        self.assertIsNotNone(fine_display, "Fine amount display missing")
        self.assertIn('Fine Amount to Pay:', fine_display.text)
        confirm_btn = payment_div.find('button', id='confirm-payment-button')
        self.assertIsNotNone(confirm_btn, "Confirm payment button missing")
        back_btn = payment_div.find('button', id='back-to-profile')
        self.assertIsNotNone(back_btn, "Back to Profile button missing on Payment page")
if __name__ == '__main__':
    unittest.main()