# OnlineLibrary Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

### Route 1: Root Redirect
- **URL path**: `/`
- **Function name**: `root_redirect`
- **HTTP method**: GET
- **Template rendered**: None (Redirect)
- **Behavior**: Redirects to the dashboard page.

### Route 2: Dashboard Page
- **URL path**: `/dashboard`
- **Function name**: `dashboard`
- **HTTP method**: GET
- **Template rendered**: `dashboard.html`
- **Context variables**:
  - `username` (str): The logged-in user's username for welcome message display.

### Route 3: Book Catalog Page
- **URL path**: `/catalog`
- **Function name**: `book_catalog`
- **HTTP method**: GET
- **Template rendered**: `catalog.html`
- **Context variables**:
  - `books` (list of dict): List of books with each dict containing:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)

### Route 4: Book Details Page
- **URL path**: `/book/<int:book_id>`
- **Function name**: `book_details`
- **HTTP method**: GET
- **Template rendered**: `book_details.html`
- **Context variables**:
  - `book` (dict): Details of the book with fields:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
    - Additional fields if needed
  - `reviews` (list of dict): List of reviews for the book, each dict:
    - `review_id` (int)
    - `username` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str) ISO format

### Route 5: Borrow Confirmation Page (GET)
- **URL path**: `/borrow/<int:book_id>`
- **Function name**: `borrow_confirmation_get`
- **HTTP method**: GET
- **Template rendered**: `borrow_confirmation.html`
- **Context variables**:
  - `book` (dict): Basic info about the book:
    - `book_id` (int)
    - `title` (str)
  - `due_date` (str): Due date string for 14 days from current date

### Route 6: Borrow Confirmation Page (POST)
- **URL path**: `/borrow/<int:book_id>`
- **Function name**: `borrow_confirmation_post`
- **HTTP method**: POST
- **Template rendered**: `borrow_confirmation.html` or redirect
- **Context variables**: Same as GET for re-render on failure, otherwise redirect on success.

### Route 7: My Borrowings Page
- **URL path**: `/my-borrows`
- **Function name**: `my_borrowings`
- **HTTP method**: GET
- **Template rendered**: `my_borrows.html`
- **Context variables**:
  - `borrowings` (list of dict): Each dict contains:
    - `borrow_id` (int)
    - `title` (str)
    - `borrow_date` (str)
    - `due_date` (str)
    - `status` (str) (Active, Returned, Overdue)
  - `filter_status` (str): Current filter value

### Route 8: Return Book Action
- **URL path**: `/return/<int:borrow_id>`
- **Function name**: `return_book`
- **HTTP method**: POST
- **Template rendered**: Redirect back to `/my-borrows` after processing
- **Context variables**: None

### Route 9: My Reservations Page
- **URL path**: `/my-reservations`
- **Function name**: `my_reservations`
- **HTTP method**: GET
- **Template rendered**: `my_reservations.html`
- **Context variables**:
  - `reservations` (list of dict): Each dict contains:
    - `reservation_id` (int)
    - `title` (str)
    - `reservation_date` (str)
    - `status` (str)

### Route 10: Cancel Reservation Action
- **URL path**: `/cancel-reservation/<int:reservation_id>`
- **Function name**: `cancel_reservation`
- **HTTP method**: POST
- **Template rendered**: Redirect back to `/my-reservations`
- **Context variables**: None

### Route 11: My Reviews Page
- **URL path**: `/my-reviews`
- **Function name**: `my_reviews`
- **HTTP method**: GET
- **Template rendered**: `my_reviews.html`
- **Context variables**:
  - `reviews` (list of dict): Each dict contains:
    - `review_id` (int)
    - `book_title` (str)
    - `rating` (int)
    - `review_text` (str)

### Route 12: Edit Review Page (GET)
- **URL path**: `/write-review/<int:book_id>` or `/edit-review/<int:review_id>`
- **Function name**: `write_edit_review_get`
- **HTTP method**: GET
- **Template rendered**: `write_review.html`
- **Context variables**:
  - `book` (dict): with `book_id` (int) and title info
  - `existing_review` (dict or None): if editing, includes `rating` (int), `review_text` (str)

### Route 13: Submit Review (POST)
- **URL path**: `/write-review/<int:book_id>` or `/edit-review/<int:review_id>`
- **Function name**: `write_edit_review_post`
- **HTTP method**: POST
- **Template rendered**: Redirect back to book details page on success
- **Context variables**: For form validation errors, re-render with error messages

### Route 14: Delete Review Action
- **URL path**: `/delete-review/<int:review_id>`
- **Function name**: `delete_review`
- **HTTP method**: POST
- **Template rendered**: Redirect back to `/my-reviews`
- **Context variables**: None

### Route 15: User Profile Page
- **URL path**: `/profile`
- **Function name**: `user_profile`
- **HTTP method**: GET
- **Template rendered**: `profile.html`
- **Context variables**:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): List of all previously borrowed books:
    - `title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)

### Route 16: Update Profile (POST)
- **URL path**: `/profile`
- **Function name**: `update_profile`
- **HTTP method**: POST
- **Template rendered**: `profile.html`, possibly with success or error messages
- **Context variables**: Same as GET

### Route 17: Payment Confirmation Page
- **URL path**: `/payment/<int:fine_id>`
- **Function name**: `payment_confirmation_get`
- **HTTP method**: GET
- **Template rendered**: `payment_confirmation.html`
- **Context variables**:
  - `fine_amount` (float)
  - `fine_id` (int)

### Route 18: Confirm Payment (POST)
- **URL path**: `/payment/<int:fine_id>`
- **Function name**: `payment_confirmation_post`
- **HTTP method**: POST
- **Template rendered**: Redirect back to `/profile` on success
- **Context variables**: None

---

## Section 2: HTML Template Specifications (Frontend Development)

### Template 1: dashboard.html
- **File path**: `templates/dashboard.html`
- **Page Title**: "Library Dashboard"
- **Elements**:
  - `dashboard-page` (div)
  - `welcome-message` (h1) - Displays welcome message with username
  - `browse-books-button` (button) - Navigates to book catalog
  - `my-borrows-button` (button) - Navigates to my borrowings
- **Accessible Context Variables**:
  - `username` (str)
- **Navigation mappings**:
  - `browse-books-button` onclick uses `url_for('book_catalog')`
  - `my-borrows-button` onclick uses `url_for('my_borrowings')`

### Template 2: catalog.html
- **File path**: `templates/catalog.html`
- **Page Title**: "Book Catalog"
- **Elements**:
  - `catalog-page` (div)
  - `search-input` (input)
  - `book-grid` (div) contains cards for each book with:
    - Buttons with ID pattern: `view-book-button-{{ book.book_id }}` (button)
  - `back-to-dashboard` (button)
- **Accessible Context Variables**:
  - `books` (list of dict): Each dict with keys: `book_id`, `title`, `author`, `status`
- **Navigation mappings**:
  - Each `view-book-button-{{ book.book_id }}` uses `url_for('book_details', book_id=book.book_id)`
  - `back-to-dashboard` uses `url_for('dashboard')`

### Template 3: book_details.html
- **File path**: `templates/book_details.html`
- **Page Title**: "Book Details"
- **Elements**:
  - `book-details-page` (div)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button)
  - `reviews-section` (div) with all reviews
  - `write-review-button` (button)
  - `back-to-catalog` (button)
- **Accessible Context Variables**:
  - `book` (dict) with `book_id`, `title`, `author`, `status`
  - `reviews` (list of dict): `review_id`, `username`, `rating`, `review_text`, `review_date`
- **Navigation mappings**:
  - `borrow-button` uses `url_for('borrow_confirmation_get', book_id=book.book_id)`
  - `write-review-button` uses `url_for('write_edit_review_get', book_id=book.book_id)`
  - `back-to-catalog` uses `url_for('book_catalog')`

### Template 4: borrow_confirmation.html
- **File path**: `templates/borrow_confirmation.html`
- **Page Title**: "Borrow Confirmation"
- **Elements**:
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button) - Form submission button
  - `cancel-borrow-button` (button) - Navigates back
- **Accessible Context Variables**:
  - `book` (dict) with `book_id`, `title`
  - `due_date` (str)
- **Navigation mappings**:
  - `confirm-borrow-button` in form POSTs to `/borrow/{{ book.book_id }}`
  - `cancel-borrow-button` uses `url_for('book_details', book_id=book.book_id)`

### Template 5: my_borrows.html
- **File path**: `templates/my_borrows.html`
- **Page Title**: "My Borrowings"
- **Elements**:
  - `my-borrows-page` (div)
  - `filter-status` (dropdown)
  - `borrows-table` (table) with rows containing:
    - `return-book-button-{{ borrow.borrow_id }}` (button) for active borrows
  - `back-to-dashboard` (button)
- **Accessible Context Variables**:
  - `borrowings` (list of dict): each dict with `borrow_id`, `title`, `borrow_date`, `due_date`, `status`
  - `filter_status` (str)
- **Navigation mappings**:
  - `return-book-button-{{ borrow.borrow_id }}` form POST to `/return/{{ borrow.borrow_id }}`
  - `back-to-dashboard` uses `url_for('dashboard')`

### Template 6: my_reservations.html
- **File path**: `templates/my_reservations.html`
- **Page Title**: "My Reservations"
- **Elements**:
  - `reservations-page` (div)
  - `reservations-table` (table) with rows containing:
    - `cancel-reservation-button-{{ reservation.reservation_id }}` (button)
  - `back-to-dashboard` (button)
- **Accessible Context Variables**:
  - `reservations` (list of dict): with `reservation_id`, `title`, `reservation_date`, `status`
- **Navigation mappings**:
  - `cancel-reservation-button-{{ reservation.reservation_id }}` form POST to `/cancel-reservation/{{ reservation.reservation_id }}`
  - `back-to-dashboard` uses `url_for('dashboard')`

### Template 7: my_reviews.html
- **File path**: `templates/my_reviews.html`
- **Page Title**: "My Reviews"
- **Elements**:
  - `reviews-page` (div)
  - `reviews-list` (div) with each review including:
    - `edit-review-button-{{ review.review_id }}` (button)
    - `delete-review-button-{{ review.review_id }}` (button)
  - `back-to-dashboard` (button)
- **Accessible Context Variables**:
  - `reviews` (list of dict) with `review_id`, `book_title`, `rating`, `review_text`
- **Navigation mappings**:
  - `edit-review-button-{{ review.review_id }}` uses `url_for('write_edit_review_get', book_id=None)` or routed via review_id
  - `delete-review-button-{{ review.review_id }}` form POST to `/delete-review/{{ review.review_id }}`
  - `back-to-dashboard` uses `url_for('dashboard')`

### Template 8: write_review.html
- **File path**: `templates/write_review.html`
- **Page Title**: "Write Review"
- **Elements**:
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown, 1-5 stars)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- **Accessible Context Variables**:
  - `book` (dict): with `book_id`, `title`
  - `existing_review` (dict or None): with `rating`, `review_text` if editing
- **Navigation mappings**:
  - `submit-review-button` submits form POST to `/write-review/{{ book.book_id }}` or `/edit-review/{{ existing_review.review_id }}`
  - `back-to-book` uses `url_for('book_details', book_id=book.book_id)`

### Template 9: profile.html
- **File path**: `templates/profile.html`
- **Page Title**: "My Profile"
- **Elements**:
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `borrow-history` (div)
  - `back-to-dashboard` (button)
- **Accessible Context Variables**:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): each with `title`, `borrow_date`, `return_date`
- **Navigation mappings**:
  - `update-profile-button` triggers POST to `/profile`
  - `back-to-dashboard` uses `url_for('dashboard')`

### Template 10: payment_confirmation.html
- **File path**: `templates/payment_confirmation.html`
- **Page Title**: "Payment Confirmation"
- **Elements**:
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- **Accessible Context Variables**:
  - `fine_amount` (float)
  - `fine_id` (int)
- **Navigation mappings**:
  - `confirm-payment-button` submits POST to `/payment/{{ fine_id }}`
  - `back-to-profile` uses `url_for('user_profile')`

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- **Path**: `data/users.txt`
- **Fields (pipe-delimited)**:
  1. `username` (str)
  2. `email` (str)
  3. `phone` (str)
  4. `address` (str)
- **Description**: Stores user account data with contact details.
- **Example rows**:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```
- **Notes**: No header line. All fields are strings.

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
  9. `status` (str) - Available, Borrowed, Reserved
  10. `avg_rating` (float)
- **Description**: Stores complete book metadata including availability.
- **Example rows**:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  ```
- **Notes**: Pipe delimiter, no header. Fields must be parsed in order.

### 3. borrowings.txt
- **Path**: `data/borrowings.txt`
- **Fields (pipe-delimited)**:
  1. `borrow_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `borrow_date` (str, ISO date `YYYY-MM-DD`)
  5. `due_date` (str, ISO date)
  6. `return_date` (str or empty, ISO date)
  7. `status` (str) - Active, Returned, Overdue
  8. `fine_amount` (float)
- **Description**: Records each borrowing transaction details, status, and fines if any.
- **Example rows**:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
  ```
- **Notes**: Empty `return_date` indicates not returned yet.

### 4. reservations.txt
- **Path**: `data/reservations.txt`
- **Fields (pipe-delimited)**:
  1. `reservation_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `reservation_date` (str, ISO date)
  5. `status` (str) - Active, Cancelled
- **Description**: Tracks book reservations made by users.
- **Example rows**:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```
- **Notes**: Status reflects current valid or cancelled reservations.

### 5. reviews.txt
- **Path**: `data/reviews.txt`
- **Fields (pipe-delimited)**:
  1. `review_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `rating` (int, 1-5)
  5. `review_text` (str)
  6. `review_date` (str, ISO date)
- **Description**: Stores user reviews and ratings for books.
- **Example rows**:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```
- **Notes**: Ratings limited to integers 1 through 5.

### 6. fines.txt
- **Path**: `data/fines.txt`
- **Fields (pipe-delimited)**:
  1. `fine_id` (int)
  2. `username` (str)
  3. `borrow_id` (int)
  4. `amount` (float)
  5. `status` (str) - Unpaid, Paid
  6. `date_issued` (str, ISO date)
- **Description**: Records fines owed or paid by users for overdue borrowings.
- **Example rows**:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
  ```
- **Notes**: Status flags whether fine is paid or unpaid.

---

This specification document fully supports independent backend and frontend development with precise route, template, and data schema definitions per user requirements.