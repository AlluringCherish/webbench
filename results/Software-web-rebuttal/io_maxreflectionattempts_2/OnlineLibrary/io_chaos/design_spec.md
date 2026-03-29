# OnlineLibrary Design Specification Document

---

## Section 1: Flask Routes Specification (Backend Development)

### 1. Root Route
- **URL path**: `/`
- **Function name**: `root_redirect`
- **HTTP method**: GET
- **Template rendered**: None (redirect)
- **Description**: Redirects users to the dashboard page.

### 2. Dashboard Page
- **URL path**: `/dashboard`
- **Function name**: `dashboard`
- **HTTP method**: GET
- **Template rendered**: `dashboard.html`
- **Context variables**:
  - `username` (str): Current logged-in username to display welcome message.

### 3. Book Catalog Page
- **URL path**: `/catalog`
- **Function name**: `book_catalog`
- **HTTP method**: GET
- **Template rendered**: `catalog.html`
- **Context variables**:
  - `books` (list of dict): List of all books available for browsing.
    - Each dict contains:
      - `book_id` (int)
      - `title` (str)
      - `author` (str)
      - `status` (str): Availability status (e.g., Available, Borrowed, Reserved)

### 4. Book Details Page
- **URL path**: `/book/<int:book_id>`
- **Function name**: `book_details`
- **HTTP method**: GET
- **Template rendered**: `book_details.html`
- **Context variables**:
  - `book` (dict): Detailed information on the selected book.
    - Fields:
      - `book_id` (int)
      - `title` (str)
      - `author` (str)
      - `status` (str)
  - `reviews` (list of dict): List of user reviews for the book.
    - Each dict contains:
      - `review_id` (int)
      - `username` (str)
      - `rating` (int)
      - `review_text` (str)
      - `review_date` (str)

### 5. Borrow Confirmation Page
- **URL path**: `/borrow/<int:book_id>`
- **Function name**: `borrow_confirmation`
- **HTTP method**: GET
- **Template rendered**: `borrow_confirmation.html`
- **Context variables**:
  - `book` (dict): Information about book to borrow.
  - `due_date` (str): Due date for return, 14 days from borrow date.

### 6. Confirm Borrow POST Route
- **URL path**: `/borrow/confirm`
- **Function name**: `confirm_borrow`
- **HTTP method**: POST
- **Template rendered**: `borrow_result.html` (confirmation page)
- **Context variables**:
  - `success` (bool): If borrow action succeeded.
  - `book` (dict): Book details involved in borrow.
  - `due_date` (str): Due date of return.

### 7. My Borrowings Page
- **URL path**: `/my-borrows`
- **Function name**: `my_borrows`
- **HTTP method**: GET
- **Template rendered**: `my_borrows.html`
- **Context variables**:
  - `borrows` (list of dict): List of borrow records for the user.
    - Each dict:
      - `borrow_id` (int)
      - `title` (str)
      - `borrow_date` (str)
      - `due_date` (str)
      - `status` (str): Active, Returned, Overdue
      - `fine_amount` (float)

### 8. Return Book POST Route
- **URL path**: `/return/<int:borrow_id>`
- **Function name**: `return_book`
- **HTTP method**: POST
- **Template rendered**: `return_result.html` (confirmation page)
- **Context variables**:
  - `success` (bool): Whether return succeeded.
  - `borrow` (dict): Borrow record returned.

### 9. My Reservations Page
- **URL path**: `/my-reservations`
- **Function name**: `my_reservations`
- **HTTP method**: GET
- **Template rendered**: `my_reservations.html`
- **Context variables**:
  - `reservations` (list of dict): List of active and cancelled reservations.
    - Each dict:
      - `reservation_id` (int)
      - `title` (str)
      - `reservation_date` (str)
      - `status` (str)

### 10. Cancel Reservation POST Route
- **URL path**: `/cancel-reservation/<int:reservation_id>`
- **Function name**: `cancel_reservation`
- **HTTP method**: POST
- **Template rendered**: `cancel_reservation_result.html` (confirmation page)
- **Context variables**:
  - `success` (bool): If cancellation succeeded.
  - `reservation` (dict)

### 11. My Reviews Page
- **URL path**: `/my-reviews`
- **Function name**: `my_reviews`
- **HTTP method**: GET
- **Template rendered**: `my_reviews.html`
- **Context variables**:
  - `reviews` (list of dict): Reviews written by user.
    - Each dict:
      - `review_id` (int)
      - `book_title` (str)
      - `rating` (int)
      - `review_text` (str)

### 12. Write Review Page
- **URL path**: `/write-review/<int:book_id>`
- **Function name**: `write_review`
- **HTTP method**: GET
- **Template rendered**: `write_review.html`
- **Context variables**:
  - `book` (dict): Book information being reviewed.
  - `existing_review` (dict or None): Existing review if editing.

### 13. Submit Review POST Route
- **URL path**: `/submit-review/<int:book_id>`
- **Function name**: `submit_review`
- **HTTP method**: POST
- **Template rendered**: `review_result.html` (confirmation page)
- **Context variables**:
  - `success` (bool): Whether review submission succeeded.
  - `book` (dict)

### 14. Edit Review POST Route
- **URL path**: `/edit-review/<int:review_id>`
- **Function name**: `edit_review`
- **HTTP method**: POST
- **Template rendered**: Redirect or review_result.html

### 15. Delete Review POST Route
- **URL path**: `/delete-review/<int:review_id>`
- **Function name**: `delete_review`
- **HTTP method**: POST
- **Template rendered**: Redirect or review_result.html

### 16. User Profile Page
- **URL path**: `/profile`
- **Function name**: `user_profile`
- **HTTP method**: GET
- **Template rendered**: `profile.html`
- **Context variables**:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): Previously borrowed books.
    - Each dict:
      - `title` (str)
      - `borrow_date` (str)
      - `return_date` (str or None)

### 17. Update Profile POST Route
- **URL path**: `/profile/update`
- **Function name**: `update_profile`
- **HTTP method**: POST
- **Template rendered**: `profile_update_result.html` (confirmation)
- **Context variables**:
  - `success` (bool)
  - `username` (str)
  - `email` (str)

### 18. Payment Confirmation Page
- **URL path**: `/payment/<int:fine_id>`
- **Function name**: `payment_confirmation`
- **HTTP method**: GET
- **Template rendered**: `payment_confirmation.html`
- **Context variables**:
  - `fine_amount` (float)
  - `fine_id` (int)

### 19. Confirm Payment POST Route
- **URL path**: `/payment/confirm/<int:fine_id>`
- **Function name**: `confirm_payment`
- **HTTP method**: POST
- **Template rendered**: `payment_result.html` (confirmation)
- **Context variables**:
  - `success` (bool)
  - `fine_id` (int)

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. Dashboard Template
- **Filename**: `templates/dashboard.html`
- **Page title**: `Library Dashboard`
- **Elements with IDs and Types**:
  - `dashboard-page` (div)
  - `welcome-message` (h1)
  - `browse-books-button` (button)
  - `my-borrows-button` (button)
- **Context variables**:
  - `username` (str)
- **Navigation Map**:
  - `browse-books-button`: url_for('book_catalog')
  - `my-borrows-button`: url_for('my_borrows')

### 2. Catalog Template
- **Filename**: `templates/catalog.html`
- **Page title**: `Book Catalog`
- **Elements**:
  - `catalog-page` (div)
  - `search-input` (input)
  - `book-grid` (div)
  - Dynamic buttons:
    - `view-book-button-{{ book.book_id }}` (button)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `books` (list of dict)
    - Each dict: `book_id` (int), `title` (str), `author` (str), `status` (str)
- **Navigation Map**:
  - `view-book-button-{{ book.book_id }}`: url_for('book_details', book_id=book.book_id)
  - `back-to-dashboard`: url_for('dashboard')

### 3. Book Details Template
- **Filename**: `templates/book_details.html`
- **Page title**: `Book Details`
- **Elements**:
  - `book-details-page` (div)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button)
  - `reviews-section` (div)
  - `write-review-button` (button)
  - `back-to-catalog` (button)
- **Context variables**:
  - `book` (dict) with fields `book_id`, `title`, `author`, `status`
  - `reviews` (list of dict) with `review_id`, `username`, `rating`, `review_text`, `review_date`
- **Navigation Map**:
  - `borrow-button`: url_for('borrow_confirmation', book_id=book.book_id)
  - `write-review-button`: url_for('write_review', book_id=book.book_id)
  - `back-to-catalog`: url_for('book_catalog')

### 4. Borrow Confirmation Template
- **Filename**: `templates/borrow_confirmation.html`
- **Page title**: `Borrow Confirmation`
- **Elements**:
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button)
  - `cancel-borrow-button` (button)
- **Context variables**:
  - `book` (dict)
  - `due_date` (str)
- **Navigation Map**:
  - `confirm-borrow-button`: Form POST action to url_for('confirm_borrow')
  - `cancel-borrow-button`: url_for('book_details', book_id=book.book_id)

### 5. My Borrowings Template
- **Filename**: `templates/my_borrows.html`
- **Page title**: `My Borrowings`
- **Elements**:
  - `my-borrows-page` (div)
  - `filter-status` (dropdown/select)
  - `borrows-table` (table)
  - Dynamic buttons:
    - `return-book-button-{{ borrow.borrow_id }}` (button) for each active borrow
  - `back-to-dashboard` (button)
- **Context variables**:
  - `borrows` (list of dict)
    - Fields per dict: `borrow_id` (int), `title` (str), `borrow_date` (str), `due_date` (str), `status` (str), `fine_amount` (float)
- **Navigation Map**:
  - `return-book-button-{{ borrow.borrow_id }}`: Form POST to url_for('return_book', borrow_id=borrow.borrow_id)
  - `back-to-dashboard`: url_for('dashboard')

### 6. My Reservations Template
- **Filename**: `templates/my_reservations.html`
- **Page title**: `My Reservations`
- **Elements**:
  - `reservations-page` (div)
  - `reservations-table` (table)
  - Dynamic buttons:
    - `cancel-reservation-button-{{ reservation.reservation_id }}` (button)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `reservations` (list of dict)
    - Fields per dict: `reservation_id` (int), `title` (str), `reservation_date` (str), `status` (str)
- **Navigation Map**:
  - `cancel-reservation-button-{{ reservation.reservation_id }}`: Form POST to url_for('cancel_reservation', reservation_id=reservation.reservation_id)
  - `back-to-dashboard`: url_for('dashboard')

### 7. My Reviews Template
- **Filename**: `templates/my_reviews.html`
- **Page title**: `My Reviews`
- **Elements**:
  - `reviews-page` (div)
  - `reviews-list` (div)
  - Dynamic buttons:
    - `edit-review-button-{{ review.review_id }}` (button)
    - `delete-review-button-{{ review.review_id }}` (button)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `reviews` (list of dict)
    - Fields per dict: `review_id` (int), `book_title` (str), `rating` (int), `review_text` (str)
- **Navigation Map**:
  - `edit-review-button-{{ review.review_id }}`: Form POST to url_for('edit_review', review_id=review.review_id)
  - `delete-review-button-{{ review.review_id }}`: Form POST to url_for('delete_review', review_id=review.review_id)
  - `back-to-dashboard`: url_for('dashboard')

### 8. Write Review Template
- **Filename**: `templates/write_review.html`
- **Page title**: `Write Review`
- **Elements**:
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown/select)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- **Context variables**:
  - `book` (dict)
  - `existing_review` (dict or None)
- **Navigation Map**:
  - `submit-review-button`: Form POST action to url_for('submit_review', book_id=book.book_id)
  - `back-to-book`: url_for('book_details', book_id=book.book_id)

### 9. User Profile Template
- **Filename**: `templates/profile.html`
- **Page title**: `My Profile`
- **Elements**:
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `borrow-history` (div)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict)
    - Fields per dict: `title` (str), `borrow_date` (str), `return_date` (str or None)
- **Navigation Map**:
  - `update-profile-button`: Form POST to url_for('update_profile')
  - `back-to-dashboard`: url_for('dashboard')

### 10. Payment Confirmation Template
- **Filename**: `templates/payment_confirmation.html`
- **Page title**: `Payment Confirmation`
- **Elements**:
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- **Context variables**:
  - `fine_amount` (float)
  - `fine_id` (int)
- **Navigation Map**:
  - `confirm-payment-button`: Form POST to url_for('confirm_payment', fine_id=fine_id)
  - `back-to-profile`: url_for('user_profile')

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- **Path**: `data/users.txt`
- **Field order and names (pipe-delimited)**:
  - `username`
  - `email`
  - `phone`
  - `address`
- **Description**: Stores user information including contact details.
- **Examples**:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```

### 2. books.txt
- **Path**: `data/books.txt`
- **Field order and names (pipe-delimited)**:
  - `book_id` (int)
  - `title` (str)
  - `author` (str)
  - `isbn` (str)
  - `genre` (str)
  - `publisher` (str)
  - `year` (int)
  - `description` (str)
  - `status` (str): Available, Borrowed, Reserved
  - `avg_rating` (float)
- **Description**: Stores all book records with details and current status.
- **Examples**:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5
  5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3
  ```

### 3. borrowings.txt
- **Path**: `data/borrowings.txt`
- **Field order and names (pipe-delimited)**:
  - `borrow_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `borrow_date` (str, YYYY-MM-DD)
  - `due_date` (str, YYYY-MM-DD)
  - `return_date` (str or empty if not returned, YYYY-MM-DD)
  - `status` (str): Active, Returned, Overdue
  - `fine_amount` (float)
- **Description**: Records borrow history and current borrowings of books by users.
- **Examples**:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
  ```

### 4. reservations.txt
- **Path**: `data/reservations.txt`
- **Field order and names (pipe-delimited)**:
  - `reservation_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `reservation_date` (str, YYYY-MM-DD)
  - `status` (str): Active, Cancelled
- **Description**: Stores active and cancelled user reservations on books.
- **Examples**:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```

### 5. reviews.txt
- **Path**: `data/reviews.txt`
- **Field order and names (pipe-delimited)**:
  - `review_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `rating` (int)
  - `review_text` (str)
  - `review_date` (str, YYYY-MM-DD)
- **Description**: Stores user reviews for books.
- **Examples**:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```

### 6. fines.txt
- **Path**: `data/fines.txt`
- **Field order and names (pipe-delimited)**:
  - `fine_id` (int)
  - `username` (str)
  - `borrow_id` (int)
  - `amount` (float)
  - `status` (str): Unpaid, Paid
  - `date_issued` (str, YYYY-MM-DD)
- **Description**: Stores fines issued for overdue borrowings.
- **Examples**:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
  ```

---

# End of Design Specification
