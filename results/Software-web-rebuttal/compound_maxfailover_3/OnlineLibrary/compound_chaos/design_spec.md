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
      - `status` (str): One of "Available", "Borrowed", "Reserved"

### 4. Book Details Page
- **URL path**: `/book/<int:book_id>`
- **Function name**: `book_details`
- **HTTP method**: GET
- **Template rendered**: `book_details.html`
- **Context variables**:
  - `book` (dict): Detailed information of the selected book.
    - Fields:
      - `book_id` (int)
      - `title` (str)
      - `author` (str)
      - `status` (str)
      - `description` (str)
  - `reviews` (list of dict): List of reviews for this book.
    - Each dict has:
      - `review_id` (int)
      - `username` (str)
      - `rating` (int, 1-5)
      - `review_text` (str)
      - `review_date` (str)
  - `user_has_borrowed` (bool): Whether the current user has borrowed the book.

### 5. Borrow Confirmation Page - Display
- **URL path**: `/borrow/<int:book_id>`
- **Function name**: `borrow_confirmation`
- **HTTP method**: GET
- **Template rendered**: `borrow_confirmation.html`
- **Context variables**:
  - `book` (dict): Book info being borrowed.
  - `due_date` (str): Date string 14 days from current date.

### 6. Borrow Confirmation Page - Process Borrow
- **URL path**: `/borrow/<int:book_id>/confirm`
- **Function name**: `confirm_borrow`
- **HTTP method**: POST
- **Template rendered**: `borrow_result.html`
- **Context variables**:
  - `success` (bool): True if borrow succeeded.
  - `book` (dict): Book info.
  - `due_date` (str): Due date.
  - `message` (str): Success or failure message.

### 7. My Borrowings Page
- **URL path**: `/my-borrows`
- **Function name**: `my_borrows`
- **HTTP method**: GET
- **Template rendered**: `my_borrows.html`
- **Context variables**:
  - `borrowings` (list of dict): List of borrowings for the current user.
    - Fields per dict:
      - `borrow_id` (int)
      - `book_title` (str)
      - `borrow_date` (str)
      - `due_date` (str)
      - `status` (str): One of "Active", "Returned", "Overdue"

### 8. Return Book - Process Return
- **URL path**: `/return/<int:borrow_id>`
- **Function name**: `return_book`
- **HTTP method**: POST
- **Template rendered**: `return_result.html`
- **Context variables**:
  - `success` (bool): True if return succeeded.
  - `borrow_id` (int)
  - `message` (str): Confirmation or error message.

### 9. My Reservations Page
- **URL path**: `/my-reservations`
- **Function name**: `my_reservations`
- **HTTP method**: GET
- **Template rendered**: `my_reservations.html`
- **Context variables**:
  - `reservations` (list of dict): User's reservations.
    - Fields per dict:
      - `reservation_id` (int)
      - `book_title` (str)
      - `reservation_date` (str)
      - `status` (str): "Active", "Cancelled"

### 10. Cancel Reservation - Process Cancellation
- **URL path**: `/cancel-reservation/<int:reservation_id>`
- **Function name**: `cancel_reservation`
- **HTTP method**: POST
- **Template rendered**: `cancellation_result.html`
- **Context variables**:
  - `success` (bool): True if cancellation succeeded.
  - `reservation_id` (int)
  - `message` (str)

### 11. My Reviews Page
- **URL path**: `/my-reviews`
- **Function name**: `my_reviews`
- **HTTP method**: GET
- **Template rendered**: `my_reviews.html`
- **Context variables**:
  - `reviews` (list of dict): List of user's reviews.
    - Fields:
      - `review_id` (int)
      - `book_title` (str)
      - `rating` (int)
      - `review_text` (str)

### 12. Write Review Page - Display
- **URL path**: `/write-review/<int:book_id>`
- **Function name**: `write_review`
- **HTTP method**: GET
- **Template rendered**: `write_review.html`
- **Context variables**:
  - `book` (dict): Book information.
  - `existing_review` (dict or None): If editing, the user's review.
    - Fields:
      - `review_id` (int)
      - `rating` (int)
      - `review_text` (str)

### 13. Write Review Page - Submit Review
- **URL path**: `/write-review/<int:book_id>/submit`
- **Function name**: `submit_review`
- **HTTP method**: POST
- **Template rendered**: `review_submit_result.html`
- **Context variables**:
  - `success` (bool)
  - `message` (str)

### 14. User Profile Page
- **URL path**: `/profile`
- **Function name**: `user_profile`
- **HTTP method**: GET
- **Template rendered**: `profile.html`
- **Context variables**:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): All previously borrowed books.
    - Each dict:
      - `book_title` (str)
      - `borrow_date` (str)
      - `return_date` (str or empty)

### 15. User Profile Page - Update
- **URL path**: `/profile/update`
- **Function name**: `update_profile`
- **HTTP method**: POST
- **Template rendered**: `profile_update_result.html`
- **Context variables**:
  - `success` (bool)
  - `message` (str)

### 16. Payment Confirmation Page
- **URL path**: `/payment/<int:fine_id>`
- **Function name**: `payment_confirmation`
- **HTTP method**: GET
- **Template rendered**: `payment_confirmation.html`
- **Context variables**:
  - `fine_amount` (float)
  - `fine_id` (int)

### 17. Payment Confirmation Page - Process Payment
- **URL path**: `/payment/<int:fine_id>/confirm`
- **Function name**: `confirm_payment`
- **HTTP method**: POST
- **Template rendered**: `payment_result.html`
- **Context variables**:
  - `success` (bool)
  - `message` (str)

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. Dashboard Page
- **Filename**: `templates/dashboard.html`
- **Page title**: "Library Dashboard"
- **Element IDs**:
  - `dashboard-page` (div)
  - `welcome-message` (h1)
  - `browse-books-button` (button)
  - `my-borrows-button` (button)
- **Context variables**:
  - `username` (str)
- **Navigation using url_for**:
  - `browse-books-button` → `url_for('book_catalog')`
  - `my-borrows-button` → `url_for('my_borrows')`

### 2. Book Catalog Page
- **Filename**: `templates/catalog.html`
- **Page title**: "Book Catalog"
- **Element IDs**:
  - `catalog-page` (div)
  - `search-input` (input)
  - `book-grid` (div)
  - `back-to-dashboard` (button)
  - Multiple buttons with pattern: `view-book-button-{book_id}` (button)
- **Context variables**:
  - `books` (list of dict): each with `book_id`, `title`, `author`, `status`
- **Navigation and dynamic buttons**:
  - Each `view-book-button-{book_id}` triggers link: `url_for('book_details', book_id=book.book_id)`
  - `back-to-dashboard` → `url_for('dashboard')`

### 3. Book Details Page
- **Filename**: `templates/book_details.html`
- **Page title**: "Book Details"
- **Element IDs**:
  - `book-details-page` (div)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button)
  - `reviews-section` (div)
  - `write-review-button` (button)
  - `back-to-catalog` (button)
- **Context variables**:
  - `book` (dict) with `book_id`, `title`, `author`, `status`, `description`
  - `reviews` (list of dict): each with `review_id`, `username`, `rating`, `review_text`, `review_date`
  - `user_has_borrowed` (bool)
- **Navigation**:
  - `borrow-button` → `url_for('borrow_confirmation', book_id=book.book_id)`
  - `write-review-button` → `url_for('write_review', book_id=book.book_id)`
  - `back-to-catalog` → `url_for('book_catalog')`

### 4. Borrow Confirmation Page
- **Filename**: `templates/borrow_confirmation.html`
- **Page title**: "Borrow Confirmation"
- **Element IDs**:
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button)
  - `cancel-borrow-button` (button)
- **Context variables**:
  - `book` (dict): display book details
  - `due_date` (str)
- **Form for confirm:**
  - `method="POST"`, `action=url_for('confirm_borrow', book_id=book.book_id)`
- **Navigation:**
  - `cancel-borrow-button` → `url_for('book_details', book_id=book.book_id)`

### 5. My Borrowings Page
- **Filename**: `templates/my_borrows.html`
- **Page title**: "My Borrowings"
- **Element IDs**:
  - `my-borrows-page` (div)
  - `filter-status` (dropdown)
  - `borrows-table` (table)
  - Multiple buttons with pattern: `return-book-button-{borrow_id}` (button)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `borrowings` (list of dict): each with `borrow_id`, `book_title`, `borrow_date`, `due_date`, `status`
- **Navigation:**
  - Each `return-book-button-{borrow_id}` triggers POST to url_for('return_book', borrow_id=borrow.borrow_id)
  - `back-to-dashboard` → `url_for('dashboard')`

### 6. My Reservations Page
- **Filename**: `templates/my_reservations.html`
- **Page title**: "My Reservations"
- **Element IDs**:
  - `reservations-page` (div)
  - `reservations-table` (table)
  - Multiple buttons with pattern: `cancel-reservation-button-{reservation_id}` (button)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `reservations` (list of dict): each with `reservation_id`, `book_title`, `reservation_date`, `status`
- **Navigation:**
  - Each `cancel-reservation-button-{reservation_id}` triggers POST to url_for('cancel_reservation', reservation_id=reservation.reservation_id)
  - `back-to-dashboard` → `url_for('dashboard')`

### 7. My Reviews Page
- **Filename**: `templates/my_reviews.html`
- **Page title**: "My Reviews"
- **Element IDs**:
  - `reviews-page` (div)
  - `reviews-list` (div)
  - Multiple buttons with patterns:
    - `edit-review-button-{review_id}` (button)
    - `delete-review-button-{review_id}` (button)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `reviews` (list of dict): each with `review_id`, `book_title`, `rating`, `review_text`
- **Navigation:**
  - `edit-review-button-{review_id}` → `url_for('write_review', book_id=review.book_id)` (assumed accessible via review)
  - `delete-review-button-{review_id}` → POST to a delete review route (not specified in requirements but implied)
  - `back-to-dashboard` → `url_for('dashboard')`

### 8. Write Review Page
- **Filename**: `templates/write_review.html`
- **Page title**: "Write Review"
- **Element IDs**:
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- **Context variables**:
  - `book` (dict)
  - `existing_review` (dict or None)
- **Form:**
  - method="POST" action=url_for('submit_review', book_id=book.book_id)
- **Navigation:**
  - `back-to-book` → `url_for('book_details', book_id=book.book_id)`

### 9. User Profile Page
- **Filename**: `templates/profile.html`
- **Page title**: "My Profile"
- **Element IDs**:
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `borrow-history` (div)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): each with `book_title`, `borrow_date`, `return_date`
- **Form:**
  - method="POST" action=url_for('update_profile')
- **Navigation:**
  - `back-to-dashboard` → `url_for('dashboard')`

### 10. Payment Confirmation Page
- **Filename**: `templates/payment_confirmation.html`
- **Page title**: "Payment Confirmation"
- **Element IDs**:
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- **Context variables**:
  - `fine_amount` (float)
  - `fine_id` (int)
- **Form:**
  - method="POST" action=url_for('confirm_payment', fine_id=fine_id)
- **Navigation:**
  - `back-to-profile` → `url_for('user_profile')`

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- **Path**: `data/users.txt`
- **Fields (pipe-delimited)**:
  1. `username` (str)
  2. `email` (str)
  3. `phone` (str)
  4. `address` (str)
- **Description**: Stores user information such as username, email, phone number, and physical address.
- **Example Rows**:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```

### 2. books.txt
- **Path**: `data/books.txt`
- **Fields (pipe-delimited)**:
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `genre` (str)
  6. `publisher` (str)
  7. `year` (int)
  8. `description` (str)
  9. `status` (str): "Available", "Borrowed", or "Reserved"
  10. `avg_rating` (float)
- **Description**: Detailed data about each book in the catalog including identification, metadata, availability status, and average rating.
- **Example Rows**:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  ```

### 3. borrowings.txt
- **Path**: `data/borrowings.txt`
- **Fields (pipe-delimited)**:
  1. `borrow_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `borrow_date` (str, YYYY-MM-DD)
  5. `due_date` (str, YYYY-MM-DD)
  6. `return_date` (str, YYYY-MM-DD or empty if not returned)
  7. `status` (str): "Active", "Returned", or "Overdue"
  8. `fine_amount` (float)
- **Description**: Tracks each borrowing instance, borrowing and due dates, return dates, status, and fines for late returns.
- **Example Rows**:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
  ```

### 4. reservations.txt
- **Path**: `data/reservations.txt`
- **Fields (pipe-delimited)**:
  1. `reservation_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `reservation_date` (str, YYYY-MM-DD)
  5. `status` (str): "Active" or "Cancelled"
- **Description**: Stores user reservations for books with reservation date and current status.
- **Example Rows**:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```

### 5. reviews.txt
- **Path**: `data/reviews.txt`
- **Fields (pipe-delimited)**:
  1. `review_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `rating` (int, 1-5 stars)
  5. `review_text` (str)
  6. `review_date` (str, YYYY-MM-DD)
- **Description**: Contains user written reviews of books with ratings and dates.
- **Example Rows**:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```

### 6. fines.txt
- **Path**: `data/fines.txt`
- **Fields (pipe-delimited)**:
  1. `fine_id` (int)
  2. `username` (str)
  3. `borrow_id` (int)
  4. `amount` (float)
  5. `status` (str): "Paid" or "Unpaid"
  6. `date_issued` (str, YYYY-MM-DD)
- **Description**: Records fines due to overdue books including payment status and issue date.
- **Example Rows**:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
  ```

---

*End of Design Specification Document*