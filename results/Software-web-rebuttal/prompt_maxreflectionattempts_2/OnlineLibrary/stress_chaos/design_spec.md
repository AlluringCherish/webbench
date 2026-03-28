# OnlineLibrary Design Specification Document

---

## Section 1: Flask Routes Specification (Backend Development)

### 1. Root Route
- **URL path**: `/`
- **Function name**: `root_redirect`
- **HTTP method**: GET
- **Template rendered**: Redirect to `dashboard`
- **Context variables**: None

### 2. Dashboard Page
- **URL path**: `/dashboard`
- **Function name**: `dashboard`
- **HTTP method**: GET
- **Template rendered**: `dashboard.html`
- **Context variables**:
  - `username` (str): Current logged-in user's username
  - `featured_books` (list of dict): List of featured books, each dict contains:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)

### 3. Book Catalog Page
- **URL path**: `/catalog`
- **Function name**: `catalog`
- **HTTP method**: GET
- **Template rendered**: `catalog.html`
- **Context variables**:
  - `books` (list of dict): All books available, each dict contains:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)

- **URL path**: `/catalog/search`
- **Function name**: `catalog_search`
- **HTTP method**: POST
- **Template rendered**: `catalog.html`
- **Context variables**:
  - `books` (list of dict): Filtered books matching search, each dict as above
  - `search_query` (str): The search input used

### 4. Book Details Page
- **URL path**: `/book/<int:book_id>`
- **Function name**: `book_details`
- **HTTP method**: GET
- **Template rendered**: `book_details.html`
- **Context variables**:
  - `book` (dict): Detailed book info with fields:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
    - `description` (str)
    - `avg_rating` (float)
  - `reviews` (list of dict): List of reviews for the book, each dict contains:
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
  - `book` (dict): Book info with fields:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
  - `due_date` (str): Date 14 days from current date in YYYY-MM-DD

- **URL path**: `/borrow/<int:book_id>/confirm`
- **Function name**: `confirm_borrow`
- **HTTP method**: POST
- **Template rendered**: Redirect to `my_borrowings`
- **Context variables**: None

- **URL path**: `/borrow/<int:book_id>/cancel`
- **Function name**: `cancel_borrow`
- **HTTP method**: POST
- **Template rendered**: Redirect to `book_details` with book_id
- **Context variables**: None

### 6. My Borrowings Page
- **URL path**: `/my_borrowings`
- **Function name**: `my_borrowings`
- **HTTP method**: GET
- **Template rendered**: `my_borrowings.html`
- **Context variables**:
  - `borrows` (list of dict): User borrow records, each dict contains:
    - `borrow_id` (int)
    - `title` (str)
    - `borrow_date` (str)
    - `due_date` (str)
    - `status` (str)
  - `filter_status` (str): Current status filter value ('All', 'Active', 'Returned', 'Overdue')

- **URL path**: `/my_borrowings/return/<int:borrow_id>`
- **Function name**: `return_book`
- **HTTP method**: POST
- **Template rendered**: Redirect to `my_borrowings`
- **Context variables**: None

### 7. My Reservations Page
- **URL path**: `/my_reservations`
- **Function name**: `my_reservations`
- **HTTP method**: GET
- **Template rendered**: `my_reservations.html`
- **Context variables**:
  - `reservations` (list of dict): User reservations, each dict contains:
    - `reservation_id` (int)
    - `title` (str)
    - `reservation_date` (str)
    - `status` (str)

- **URL path**: `/my_reservations/cancel/<int:reservation_id>`
- **Function name**: `cancel_reservation`
- **HTTP method**: POST
- **Template rendered**: Redirect to `my_reservations`
- **Context variables**: None

### 8. My Reviews Page
- **URL path**: `/my_reviews`
- **Function name**: `my_reviews`
- **HTTP method**: GET
- **Template rendered**: `my_reviews.html`
- **Context variables**:
  - `reviews` (list of dict): User reviews, each dict contains:
    - `review_id` (int)
    - `title` (str)
    - `rating` (int)
    - `review_text` (str)

- **URL path**: `/my_reviews/delete/<int:review_id>`
- **Function name**: `delete_review`
- **HTTP method**: POST
- **Template rendered**: Redirect to `my_reviews`
- **Context variables**: None

### 9. Write Review Page
- **URL path**: `/write_review/<int:book_id>`
- **Function name**: `write_review`
- **HTTP method**: GET
- **Template rendered**: `write_review.html`
- **Context variables**:
  - `book` (dict): Book info containing:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
  - `existing_review` (dict or None): If editing a review for this book by the user, dict contains:
    - `review_id` (int)
    - `rating` (int)
    - `review_text` (str)

- **URL path**: `/write_review/<int:book_id>/submit`
- **Function name**: `submit_review`
- **HTTP method**: POST
- **Template rendered**: Redirect to `book_details` with book_id
- **Context variables**: None

### 10. User Profile Page
- **URL path**: `/profile`
- **Function name**: `profile`
- **HTTP method**: GET
- **Template rendered**: `profile.html`
- **Context variables**:
  - `username` (str): Current user
  - `email` (str): User email
  - `borrow_history` (list of dict): List of all previous borrowings, each dict contains:
    - `title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)

- **URL path**: `/profile/update`
- **Function name**: `update_profile`
- **HTTP method**: POST
- **Template rendered**: Redirect to `profile`
- **Context variables**: None

### 11. Payment Confirmation Page
- **URL path**: `/payment/<int:fine_id>`
- **Function name**: `payment_confirmation`
- **HTTP method**: GET
- **Template rendered**: `payment_confirmation.html`
- **Context variables**:
  - `fine` (dict): Fine info containing:
    - `fine_id` (int)
    - `amount` (float)

- **URL path**: `/payment/<int:fine_id>/confirm`
- **Function name**: `confirm_payment`
- **HTTP method**: POST
- **Template rendered**: Redirect to `profile`
- **Context variables**: None

- **URL path**: `/payment/<int:fine_id>/cancel`
- **Function name**: `cancel_payment`
- **HTTP method**: POST
- **Template rendered**: Redirect to `profile`
- **Context variables**: None

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. dashboard.html (templates/dashboard.html)
- **Page title**: Library Dashboard
- **Element IDs**:
  - `dashboard-page` (div)
  - `welcome-message` (h1)
  - `browse-books-button` (button)
  - `my-borrows-button` (button)
- **Context variables**:
  - `username` (str)
  - `featured_books` (list of dict): Each dict with `book_id` (int), `title` (str), `author` (str), `status` (str)
- **Navigation mappings**:
  - `browse-books-button` → `url_for('catalog')`
  - `my-borrows-button` → `url_for('my_borrowings')`

### 2. catalog.html (templates/catalog.html)
- **Page title**: Book Catalog
- **Element IDs**:
  - `catalog-page` (div)
  - `search-input` (input)
  - `book-grid` (div)
  - `back-to-dashboard` (button)
  - For each book in `books`:
    - `view-book-button-{{ book.book_id }}` (button)
- **Context variables**:
  - `books` (list of dict): Each dict with `book_id` (int), `title` (str), `author` (str), `status` (str)
  - `search_query` (str, optional) if present
- **Navigation mappings**:
  - `back-to-dashboard` → `url_for('dashboard')`
  - `view-book-button-{book_id}` → `url_for('book_details', book_id=book_id)`
- **Forms**:
  - Search form posted to `url_for('catalog_search')`

### 3. book_details.html (templates/book_details.html)
- **Page title**: Book Details
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
  - `book` (dict): `book_id` (int), `title` (str), `author` (str), `status` (str), `description` (str), `avg_rating` (float)
  - `reviews` (list of dict): Each dict with `review_id` (int), `username` (str), `rating` (int), `review_text` (str), `review_date` (str)
- **Navigation mappings**:
  - `borrow-button` → `url_for('borrow_confirmation', book_id=book.book_id)`
  - `write-review-button` → `url_for('write_review', book_id=book.book_id)`
  - `back-to-catalog` → `url_for('catalog')`
- **Forms**:
  - No form submission on this page; buttons navigate

### 4. borrow_confirmation.html (templates/borrow_confirmation.html)
- **Page title**: Borrow Confirmation
- **Element IDs**:
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button)
  - `cancel-borrow-button` (button)
- **Context variables**:
  - `book` (dict): `book_id` (int), `title` (str), `author` (str)
  - `due_date` (str) YYYY-MM-DD
- **Navigation mappings**:
  - `confirm-borrow-button` - Form submits POST to `url_for('confirm_borrow', book_id=book.book_id)`
  - `cancel-borrow-button` - Form submits POST to `url_for('cancel_borrow', book_id=book.book_id)`
- **Forms**:
  - POST form for confirming borrow
  - POST form for cancelling borrow

### 5. my_borrowings.html (templates/my_borrowings.html)
- **Page title**: My Borrowings
- **Element IDs**:
  - `my-borrows-page` (div)
  - `filter-status` (dropdown/select)
  - `borrows-table` (table)
  - `back-to-dashboard` (button)
  - For each borrow in `borrows` with status 'Active':
    - `return-book-button-{{ borrow.borrow_id }}` (button)
- **Context variables**:
  - `borrows` (list of dict): Each dict with `borrow_id` (int), `title` (str), `borrow_date` (str), `due_date` (str), `status` (str)
  - `filter_status` (str)
- **Navigation mappings**:
  - `back-to-dashboard` → `url_for('dashboard')`
- **Forms**:
  - Return book forms POST to `url_for('return_book', borrow_id=borrow.borrow_id)`

### 6. my_reservations.html (templates/my_reservations.html)
- **Page title**: My Reservations
- **Element IDs**:
  - `reservations-page` (div)
  - `reservations-table` (table)
  - `back-to-dashboard` (button)
  - For each reservation:
    - `cancel-reservation-button-{{ reservation.reservation_id }}` (button)
- **Context variables**:
  - `reservations` (list of dict): Each dict with `reservation_id` (int), `title` (str), `reservation_date` (str), `status` (str)
- **Navigation mappings**:
  - `back-to-dashboard` → `url_for('dashboard')`
- **Forms**:
  - Cancel reservation forms POST to `url_for('cancel_reservation', reservation_id=reservation.reservation_id)`

### 7. my_reviews.html (templates/my_reviews.html)
- **Page title**: My Reviews
- **Element IDs**:
  - `reviews-page` (div)
  - `reviews-list` (div)
  - `back-to-dashboard` (button)
  - For each review:
    - `edit-review-button-{{ review.review_id }}` (button)
    - `delete-review-button-{{ review.review_id }}` (button)
- **Context variables**:
  - `reviews` (list of dict): Each dict with `review_id` (int), `title` (str), `rating` (int), `review_text` (str)
- **Navigation mappings**:
  - `back-to-dashboard` → `url_for('dashboard')`
  - `edit-review-button-{review_id}` → `url_for('write_review', book_id=review.book_id)` (note: requires book_id from backend)
- **Forms**:
  - Delete review forms POST to `url_for('delete_review', review_id=review.review_id)`

### 8. write_review.html (templates/write_review.html)
- **Page title**: Write Review
- **Element IDs**:
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown/select)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- **Context variables**:
  - `book` (dict): `book_id` (int), `title` (str), `author` (str)
  - `existing_review` (dict or None): If editing, contains `review_id` (int), `rating` (int), `review_text` (str)
- **Navigation mappings**:
  - `back-to-book` → `url_for('book_details', book_id=book.book_id)`
- **Forms**:
  - Submit review form POSTs to `url_for('submit_review', book_id=book.book_id)`

### 9. profile.html (templates/profile.html)
- **Page title**: My Profile
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
  - `borrow_history` (list of dict): Each dict with `title` (str), `borrow_date` (str), `return_date` (str or None)
- **Navigation mappings**:
  - `back-to-dashboard` → `url_for('dashboard')`
- **Forms**:
  - Profile update form POSTs to `url_for('update_profile')`

### 10. payment_confirmation.html (templates/payment_confirmation.html)
- **Page title**: Payment Confirmation
- **Element IDs**:
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- **Context variables**:
  - `fine` (dict): `fine_id` (int), `amount` (float)
- **Navigation mappings**:
  - `back-to-profile` → `url_for('profile')`
- **Forms**:
  - Confirm payment form POSTs to `url_for('confirm_payment', fine_id=fine.fine_id)`
  - Cancel payment form POSTs to `url_for('cancel_payment', fine_id=fine.fine_id)`

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt (data/users.txt)
- **Fields (pipe-delimited)**:
  - `username` (str)
  - `email` (str)
  - `phone` (str)
  - `address` (str)
- **Description**: Stores user personal details.
- **Example rows**:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```

### 2. books.txt (data/books.txt)
- **Fields (pipe-delimited)**:
  - `book_id` (int)
  - `title` (str)
  - `author` (str)
  - `isbn` (str)
  - `genre` (str)
  - `publisher` (str)
  - `year` (int)
  - `description` (str)
  - `status` (str) Options: Available, Borrowed, Reserved
  - `avg_rating` (float)
- **Description**: Stores book metadata and availability.
- **Example rows**:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  ```

### 3. borrowings.txt (data/borrowings.txt)
- **Fields (pipe-delimited)**:
  - `borrow_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `borrow_date` (str, YYYY-MM-DD)
  - `due_date` (str, YYYY-MM-DD)
  - `return_date` (str or empty for not returned, YYYY-MM-DD)
  - `status` (str) Options: Active, Returned, Overdue
  - `fine_amount` (float)
- **Description**: Logs details of each borrowing transaction.
- **Example rows**:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
  ```

### 4. reservations.txt (data/reservations.txt)
- **Fields (pipe-delimited)**:
  - `reservation_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `reservation_date` (str, YYYY-MM-DD)
  - `status` (str) Options: Active, Cancelled
- **Description**: Stores reservation records.
- **Example rows**:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```

### 5. reviews.txt (data/reviews.txt)
- **Fields (pipe-delimited)**:
  - `review_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `rating` (int, 1-5)
  - `review_text` (str)
  - `review_date` (str, YYYY-MM-DD)
- **Description**: Stores user reviews for books.
- **Example rows**:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```

### 6. fines.txt (data/fines.txt)
- **Fields (pipe-delimited)**:
  - `fine_id` (int)
  - `username` (str)
  - `borrow_id` (int)
  - `amount` (float)
  - `status` (str) Options: Unpaid, Paid
  - `date_issued` (str, YYYY-MM-DD)
- **Description**: Tracks overdue fines and payment status.
- **Example rows**:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
  ```

---

This design specification fully supports independent parallel development of backend Flask routes, HTML templates, and local text file data handling.

All names of routes, functions, context variables, templates, element IDs, and data fields are precisely aligned to the project requirements for unambiguous implementation.