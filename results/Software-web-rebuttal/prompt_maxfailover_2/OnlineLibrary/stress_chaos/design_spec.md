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
  - `username` (str): Current logged-in username to display in welcome message.

### 3. Book Catalog Page
- **URL path**: `/catalog`
- **Function name**: `book_catalog`
- **HTTP method**: GET
- **Template rendered**: `catalog.html`
- **Context variables**:
  - `books` (list of dict): List of all books for display. Each dict contains:
    - `book_id` (int): Unique book identifier
    - `title` (str)
    - `author` (str)
    - `status` (str): Availability status (`Available`, `Borrowed`, `Reserved`)

### 4. Book Details Page
- **URL path**: `/book/<int:book_id>`
- **Function name**: `book_details`
- **HTTP method**: GET
- **Template rendered**: `book_details.html`
- **Context variables**:
  - `book` (dict): Detailed information on the book with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
    - `description` (str)
    - `avg_rating` (float)
  - `reviews` (list of dict): User reviews for this book. Each dict:
    - `review_id` (int)
    - `username` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str)

### 5. Borrow Confirmation Page
- **URL path**: `/borrow/<int:book_id>`
- **Function name**: `borrow_confirm`
- **HTTP method**: GET, POST
- **Template rendered**: `borrow_confirm.html`
- **Context variables (GET)**:
  - `book` (dict): Same structure as in Book Details page.
  - `due_date` (str): Date string computed as 14 days from current date.
- **POST handling**:
  - Process borrow confirmation.
  - On success redirect to My Borrowings page or a confirmation display.

### 6. Cancel Borrow Page (optional return action)
- **URL path**: `/return/<int:borrow_id>`
- **Function name**: `return_book`
- **HTTP method**: POST
- **Template rendered**: None (redirect)
- **Description**: Processes returning of a borrowed book. Redirect back to My Borrowings after processing.

### 7. My Borrowings Page
- **URL path**: `/my-borrows`
- **Function name**: `my_borrowings`
- **HTTP method**: GET
- **Template rendered**: `my_borrows.html`
- **Context variables**:
  - `borrowings` (list of dict): List of borrowing records for the user. Each dict contains:
    - `borrow_id` (int)
    - `title` (str)
    - `borrow_date` (str)
    - `due_date` (str)
    - `status` (str) (`Active`, `Returned`, `Overdue`)
  - `filter_status` (str): Current filter selected (`All`, `Active`, `Returned`, `Overdue`)

### 8. My Reservations Page
- **URL path**: `/my-reservations`
- **Function name**: `my_reservations`
- **HTTP method**: GET
- **Template rendered**: `my_reservations.html`
- **Context variables**:
  - `reservations` (list of dict): User reservations. Each dict contains:
    - `reservation_id` (int)
    - `title` (str)
    - `reservation_date` (str)
    - `status` (str) (`Active`, `Cancelled`)

### 9. Cancel Reservation
- **URL path**: `/cancel-reservation/<int:reservation_id>`
- **Function name**: `cancel_reservation`
- **HTTP method**: POST
- **Template rendered**: None (redirect)
- **Description**: Cancel an active reservation. Redirect to My Reservations after processing.

### 10. My Reviews Page
- **URL path**: `/my-reviews`
- **Function name**: `my_reviews`
- **HTTP method**: GET
- **Template rendered**: `my_reviews.html`
- **Context variables**:
  - `reviews` (list of dict): Reviews by user. Each dict contains:
    - `review_id` (int)
    - `book_title` (str)
    - `rating` (int)
    - `review_text` (str)

### 11. Write Review Page
- **URL path**: `/write-review/<int:book_id>`
- **Function name**: `write_review`
- **HTTP method**: GET, POST
- **Template rendered**: `write_review.html`
- **Context variables (GET)**:
  - `book` (dict): Book info - same structure as Book Details.
  - `existing_review` (dict or None): Existing review data if editing, keys:
    - `review_id` (int)
    - `rating` (int)
    - `review_text` (str)
- **POST handling**:
  - Process submitted review form.
  - Redirect on success appropriately (e.g., back to book details).

### 12. Edit Review
- **URL path**: Using the same `/write-review/<book_id>` for editing.

### 13. Delete Review
- **URL path**: `/delete-review/<int:review_id>`
- **Function name**: `delete_review`
- **HTTP method**: POST
- **Template rendered**: None (redirect)
- **Description**: Delete specified review and redirect to My Reviews.

### 14. User Profile Page
- **URL path**: `/profile`
- **Function name**: `user_profile`
- **HTTP method**: GET, POST
- **Template rendered**: `profile.html`
- **Context variables (GET)**:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): List of previously borrowed books by the user. Each dict:
    - `title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)
- **POST handling**:
  - Accept email updates
  - Redirect or render with updated info

### 15. Payment Confirmation Page
- **URL path**: `/payment/<int:fine_id>`
- **Function name**: `payment_confirmation`
- **HTTP method**: GET, POST
- **Template rendered**: `payment_confirm.html`
- **Context variables (GET)**:
  - `fine_amount` (float): Amount due
  - `fine_id` (int)
- **POST handling**:
  - Process payment confirmation
  - Redirect back to profile or payment success page

---

## Section 2: HTML Template Specifications (Frontend Development)

### Template: dashboard.html
- **File path**: `templates/dashboard.html`
- **Page title**: `Library Dashboard`
- **Page heading**: `<h1 id="welcome-message">` 
- **Element IDs**:
  - `dashboard-page` (div)
  - `welcome-message` (h1)
  - `browse-books-button` (button)
  - `my-borrows-button` (button)
- **Context variables**:
  - `username` (str)
- **Navigation mappings**:
  - `browse-books-button` → url_for('book_catalog')
  - `my-borrows-button` → url_for('my_borrowings')

### Template: catalog.html
- **File path**: `templates/catalog.html`
- **Page title**: `Book Catalog`
- **Page heading**: `<h1>` (optional, not explicitly specified but implied)
- **Element IDs**:
  - `catalog-page` (div)
  - `search-input` (input)
  - `book-grid` (div)
  - `back-to-dashboard` (button)
  - Dynamic button pattern: `view-book-button-{book_id}` (button)
- **Context variables**:
  - `books` (list of dict): Each dict with:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
- **Navigation mappings**:
  - `view-book-button-{book_id}` → url_for('book_details', book_id=book.book_id)
  - `back-to-dashboard` → url_for('dashboard')

### Template: book_details.html
- **File path**: `templates/book_details.html`
- **Page title**: `Book Details`
- **Page heading**: `<h1 id="book-title">` showing book title
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
  - `book` (dict) with keys: `book_id` (int), `title` (str), `author` (str), `status` (str), `description` (str), `avg_rating` (float)
  - `reviews` (list of dict) with keys: `review_id` (int), `username` (str), `rating` (int), `review_text` (str), `review_date` (str)
- **Navigation mappings**:
  - `borrow-button` → url_for('borrow_confirm', book_id=book.book_id)
  - `write-review-button` → url_for('write_review', book_id=book.book_id)
  - `back-to-catalog` → url_for('book_catalog')

### Template: borrow_confirm.html
- **File path**: `templates/borrow_confirm.html`
- **Page title**: `Borrow Confirmation`
- **Page heading**: `<h1>` (not explicitly specified, but main div `borrow-page`)
- **Element IDs**:
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button)
  - `cancel-borrow-button` (button)
- **Context variables**:
  - `book` (dict) keys: `book_id`, `title`, `author`, `status`, `description`, `avg_rating`
  - `due_date` (str)
- **Form**:
  - Form uses POST method action targeting the same route
  - `confirm-borrow-button` triggers form submit
  - `cancel-borrow-button` navigates back to book details
- **Navigation mappings**:
  - `cancel-borrow-button` → url_for('book_details', book_id=book.book_id)

### Template: my_borrows.html
- **File path**: `templates/my_borrows.html`
- **Page title**: `My Borrowings`
- **Page heading**: `<h1>` (not explicitly specified, but main div `my-borrows-page`)
- **Element IDs**:
  - `my-borrows-page` (div)
  - `filter-status` (dropdown)
  - `borrows-table` (table)
  - Dynamic button pattern: `return-book-button-{borrow_id}` (button)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `borrowings` (list of dict) each with:
    - `borrow_id` (int)
    - `title` (str)
    - `borrow_date` (str)
    - `due_date` (str)
    - `status` (str)
  - `filter_status` (str)
- **Navigation mappings**:
  - `return-book-button-{borrow_id}` → POST forms or AJAX to `/return/<borrow_id>` route
  - `back-to-dashboard` → url_for('dashboard')

### Template: my_reservations.html
- **File path**: `templates/my_reservations.html`
- **Page title**: `My Reservations`
- **Page heading**: `<h1>` (not explicitly specified, main div `reservations-page`)
- **Element IDs**:
  - `reservations-page` (div)
  - `reservations-table` (table)
  - Dynamic button pattern: `cancel-reservation-button-{reservation_id}` (button)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `reservations` (list of dict) each with:
    - `reservation_id` (int)
    - `title` (str)
    - `reservation_date` (str)
    - `status` (str)
- **Navigation mappings**:
  - `cancel-reservation-button-{reservation_id}` → POST to `/cancel-reservation/<reservation_id>`
  - `back-to-dashboard` → url_for('dashboard')

### Template: my_reviews.html
- **File path**: `templates/my_reviews.html`
- **Page title**: `My Reviews`
- **Page heading**: `<h1>` (not explicitly specified, main div `reviews-page`)
- **Element IDs**:
  - `reviews-page` (div)
  - `reviews-list` (div)
  - Dynamic button patterns:
    - `edit-review-button-{review_id}` (button)
    - `delete-review-button-{review_id}` (button)
  - `back-to-dashboard` (button)
- **Context variables**:
  - `reviews` (list of dict) each with:
    - `review_id` (int)
    - `book_title` (str)
    - `rating` (int)
    - `review_text` (str)
- **Navigation mappings**:
  - `edit-review-button-{review_id}` → url_for('write_review', book_id=review.book_id) (requires book_id; to get from backend)
  - `delete-review-button-{review_id}` → POST form `/delete-review/<review_id>`
  - `back-to-dashboard` → url_for('dashboard')

### Template: write_review.html
- **File path**: `templates/write_review.html`
- **Page title**: `Write Review`
- **Page heading**: `<h1>` (not explicitly specified, main div `write-review-page`)
- **Element IDs**:
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- **Context variables**:
  - `book` (dict): Same as Book Details
  - `existing_review` (dict or None) keys: `review_id` (int), `rating` (int), `review_text` (str)
- **Navigation mappings**:
  - `back-to-book` → url_for('book_details', book_id=book.book_id)
- **Form**:
  - Uses POST method
  - `submit-review-button` triggers form submission

### Template: profile.html
- **File path**: `templates/profile.html`
- **Page title**: `My Profile`
- **Page heading**: `<h1>` (not explicitly specified, main div `profile-page`)
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
  - `borrow_history` (list of dict) each with:
    - `title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)
- **Navigation mappings**:
  - `back-to-dashboard` → url_for('dashboard')
- **Form**:
  - POST method for profile updates
  - `update-profile-button` triggers form submission

### Template: payment_confirm.html
- **File path**: `templates/payment_confirm.html`
- **Page title**: `Payment Confirmation`
- **Page heading**: `<h1>` (not explicitly specified, main div `payment-page`)
- **Element IDs**:
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- **Context variables**:
  - `fine_amount` (float)
  - `fine_id` (int)
- **Navigation mappings**:
  - `back-to-profile` → url_for('user_profile')
- **Form**:
  - POST method for confirming payment
  - `confirm-payment-button` triggers form submission

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- **Path**: `data/users.txt`
- **Fields**: `username|email|phone|address`
- **Description**: Stores user account information.
- **Examples**:
  1. `john_reader|john@example.com|555-1234|123 Main St`
  2. `jane_doe|jane@example.com|555-5678|789 Oak St`

### 2. books.txt
- **Path**: `data/books.txt`
- **Fields**: `book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating`
- **Description**: Stores book details and current availability status.
- **Examples**:
  1. `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  2. `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  3. `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`

### 3. borrowings.txt
- **Path**: `data/borrowings.txt`
- **Fields**: `borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount`
- **Description**: Records of borrowing transactions, current status, and fines if any.
- **Examples**:
  1. `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  2. `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  3. `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`

### 4. reservations.txt
- **Path**: `data/reservations.txt`
- **Fields**: `reservation_id|username|book_id|reservation_date|status`
- **Description**: Reservation records with current status.
- **Examples**:
  1. `1|jane_doe|4|2024-11-10|Active`
  2. `2|john_reader|2|2024-10-25|Cancelled`

### 5. reviews.txt
- **Path**: `data/reviews.txt`
- **Fields**: `review_id|username|book_id|rating|review_text|review_date`
- **Description**: User submitted reviews and ratings for books.
- **Examples**:
  1. `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  2. `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`

### 6. fines.txt
- **Path**: `data/fines.txt`
- **Fields**: `fine_id|username|borrow_id|amount|status|date_issued`
- **Description**: Records of fines issued for overdue borrowings and their payment status.
- **Examples**:
  1. `1|john_reader|3|5.00|Unpaid|2024-10-30`

---

# End of Specification
