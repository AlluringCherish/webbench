# Design Specification for OnlineLibrary Web Application

---

## Section 1: Flask Routes Specification (Backend Development)

### Route 1: Root Redirect
- **URL path:** `/`
- **Function name:** `root_redirect`
- **HTTP method:** GET
- **Template rendered:** None (redirect only)
- **Behavior:** Redirects to the dashboard page route `/dashboard`.

---

### Route 2: Dashboard Page
- **URL path:** `/dashboard`
- **Function name:** `dashboard`
- **HTTP method:** GET
- **Template rendered:** `dashboard.html`
- **Context variables:**
  - `username` (str): The username of the logged-in user to display welcome message.

---

### Route 3: Book Catalog Page
- **URL path:** `/catalog`
- **Function name:** `book_catalog`
- **HTTP method:** GET
- **Template rendered:** `catalog.html`
- **Context variables:**
  - `books` (list of dict): List of available books. Each dict contains:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str) - values: "Available", "Borrowed", "Reserved"

---

### Route 4: Book Details Page
- **URL path:** `/book/<int:book_id>`
- **Function name:** `book_details`
- **HTTP method:** GET
- **Template rendered:** `book_details.html`
- **Context variables:**
  - `book` (dict): Detailed information about the book, containing:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
    - `description` (str)
    - `isbn` (str)
    - `genre` (str)
    - `publisher` (str)
    - `year` (int)
    - `avg_rating` (float)
  - `reviews` (list of dict): List of reviews for the book. Each dict contains:
    - `review_id` (int)
    - `username` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str, YYYY-MM-DD)

---

### Route 5: Borrow Confirmation Page (GET)
- **URL path:** `/borrow/<int:book_id>`
- **Function name:** `borrow_book_get`
- **HTTP method:** GET
- **Template rendered:** `borrow_confirm.html`
- **Context variables:**
  - `book` (dict): Same structure as in Book Details.
  - `due_date` (str, YYYY-MM-DD): Date 14 days from current date.

---

### Route 6: Borrow Confirmation Page (POST)
- **URL path:** `/borrow/<int:book_id>`
- **Function name:** `borrow_book_post`
- **HTTP method:** POST
- **Template rendered:** `borrow_confirmation.html`
- **Context variables:**
  - `book` (dict): Same structure as in Book Details.
  - `due_date` (str)
  - `borrow_id` (int): Identifier for the created borrow record.

---

### Route 7: My Borrowings Page
- **URL path:** `/my-borrows`
- **Function name:** `my_borrows`
- **HTTP method:** GET
- **Template rendered:** `my_borrows.html`
- **Context variables:**
  - `borrowings` (list of dict): Borrow records for the user. Each dict:
    - `borrow_id` (int)
    - `book_title` (str)
    - `borrow_date` (str, YYYY-MM-DD)
    - `due_date` (str, YYYY-MM-DD)
    - `status` (str) - values: "Active", "Returned", "Overdue"
  - `filter_status` (str): Current filter selected, one of "All", "Active", "Returned", "Overdue".

---

### Route 8: Return Borrowed Book (POST)
- **URL path:** `/return/<int:borrow_id>`
- **Function name:** `return_book`
- **HTTP method:** POST
- **Template rendered:** `return_confirmation.html`
- **Context variables:**
  - `borrow_id` (int)
  - `book_title` (str)
  - `return_date` (str, YYYY-MM-DD)

---

### Route 9: My Reservations Page
- **URL path:** `/my-reservations`
- **Function name:** `my_reservations`
- **HTTP method:** GET
- **Template rendered:** `my_reservations.html`
- **Context variables:**
  - `reservations` (list of dict): User's reservations. Each dict:
    - `reservation_id` (int)
    - `book_title` (str)
    - `reservation_date` (str, YYYY-MM-DD)
    - `status` (str) - values: "Active", "Cancelled"

---

### Route 10: Cancel Reservation (POST)
- **URL path:** `/cancel-reservation/<int:reservation_id>`
- **Function name:** `cancel_reservation`
- **HTTP method:** POST
- **Template rendered:** `reservation_cancellation_confirmation.html`
- **Context variables:**
  - `reservation_id` (int)
  - `book_title` (str)

---

### Route 11: My Reviews Page
- **URL path:** `/my-reviews`
- **Function name:** `my_reviews`
- **HTTP method:** GET
- **Template rendered:** `my_reviews.html`
- **Context variables:**
  - `reviews` (list of dict): User reviews. Each dict:
    - `review_id` (int)
    - `book_title` (str)
    - `rating` (int)
    - `review_text` (str)

---

### Route 12: Write Review Page
- **URL path:** `/write-review/<int:book_id>`
- **Function name:** `write_review_get`
- **HTTP method:** GET
- **Template rendered:** `write_review.html`
- **Context variables:**
  - `book` (dict): Book information as detailed in Book Details.
  - `existing_review` (dict or None): If editing, contains:
    - `review_id` (int)
    - `rating` (int)
    - `review_text` (str)
    Otherwise None.


### Route 13: Submit Review (POST)
- **URL path:** `/write-review/<int:book_id>`
- **Function name:** `write_review_post`
- **HTTP method:** POST
- **Template rendered:** `review_submission_confirmation.html`
- **Context variables:**
  - `book` (dict)
  - `review_id` (int)

---

### Route 14: User Profile Page
- **URL path:** `/profile`
- **Function name:** `user_profile`
- **HTTP method:** GET
- **Template rendered:** `profile.html`
- **Context variables:**
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): Past borrowings containing:
    - `book_title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)

---

### Route 15: Update User Profile (POST)
- **URL path:** `/profile`
- **Function name:** `update_profile`
- **HTTP method:** POST
- **Template rendered:** `profile_update_confirmation.html`
- **Context variables:**
  - `username` (str)
  - `email` (str)

---

### Route 16: Payment Confirmation Page (GET)
- **URL path:** `/payment/<int:fine_id>`
- **Function name:** `payment_confirmation_get`
- **HTTP method:** GET
- **Template rendered:** `payment_confirmation.html`
- **Context variables:**
  - `fine` (dict) with:
    - `fine_id` (int)
    - `amount` (float)

---

### Route 17: Payment Confirmation Page (POST)
- **URL path:** `/payment/<int:fine_id>`
- **Function name:** `payment_confirmation_post`
- **HTTP method:** POST
- **Template rendered:** `payment_success.html`
- **Context variables:**
  - `fine_id` (int)
  - `payment_status` (str) (e.g., "Success")

---

## Section 2: HTML Template Specifications (Frontend Development)

### Template 1: dashboard.html
- **File:** `templates/dashboard.html`
- **Page title:** "Library Dashboard" (for both `<title>` and `<h1>`)
- **Element IDs:**
  - `dashboard-page` (div)
  - `welcome-message` (h1)
  - `browse-books-button` (button)
  - `my-borrows-button` (button)
- **Context variables:**
  - `username` (str)
- **Navigation:**
  - `browse-books-button` uses `url_for('book_catalog')`
  - `my-borrows-button` uses `url_for('my_borrows')`

---

### Template 2: catalog.html
- **File:** `templates/catalog.html`
- **Page title:** "Book Catalog"
- **Element IDs:**
  - `catalog-page` (div)
  - `search-input` (input)
  - `book-grid` (div)
  - For each book in `books`:
    - `view-book-button-{{ book.book_id }}` (button)
  - `back-to-dashboard` (button)
- **Context variables:**
  - `books` (list of dict with `book_id`, `title`, `author`, `status`)
- **Navigation:**
  - `view-book-button-{{ book.book_id }}` uses `url_for('book_details', book_id=book.book_id)`
  - `back-to-dashboard` uses `url_for('dashboard')`

---

### Template 3: book_details.html
- **File:** `templates/book_details.html`
- **Page title:** "Book Details"
- **Element IDs:**
  - `book-details-page` (div)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button)
  - `reviews-section` (div)
  - `write-review-button` (button)
  - `back-to-catalog` (button)
- **Context variables:**
  - `book` (dict as defined)
  - `reviews` (list of dict)
- **Navigation:**
  - `borrow-button` uses `url_for('borrow_book_get', book_id=book.book_id)`
  - `write-review-button` uses `url_for('write_review_get', book_id=book.book_id)`
  - `back-to-catalog` uses `url_for('book_catalog')`

---

### Template 4: borrow_confirm.html
- **File:** `templates/borrow_confirm.html`
- **Page title:** "Borrow Confirmation"
- **Element IDs:**
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button) - form submission
  - `cancel-borrow-button` (button)
- **Context variables:**
  - `book` (dict)
  - `due_date` (str)
- **Navigation:**
  - `confirm-borrow-button` triggers POST to `url_for('borrow_book_post', book_id=book.book_id)`
  - `cancel-borrow-button` uses `url_for('book_details', book_id=book.book_id)`

---

### Template 5: borrow_confirmation.html
- **File:** `templates/borrow_confirmation.html`
- **Page title:** "Borrow Confirmation"
- **Element IDs:**
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
- **Context variables:**
  - `book` (dict)
  - `due_date` (str)
  - `borrow_id` (int)
- **Navigation:**
  - Should include a back or dashboard link as needed (typically `url_for('dashboard')`)

---

### Template 6: my_borrows.html
- **File:** `templates/my_borrows.html`
- **Page title:** "My Borrowings"
- **Element IDs:**
  - `my-borrows-page` (div)
  - `filter-status` (dropdown)
  - `borrows-table` (table)
  - For each borrowing with status "Active":
    - `return-book-button-{{ borrow.borrow_id }}` (button)
  - `back-to-dashboard` (button)
- **Context variables:**
  - `borrowings` (list of dict with `borrow_id`, `book_title`, `borrow_date`, `due_date`, `status`)
  - `filter_status` (str)
- **Navigation:**
  - `return-book-button-{{ borrow.borrow_id }}` triggers POST to `url_for('return_book', borrow_id=borrow.borrow_id)`
  - `back-to-dashboard` uses `url_for('dashboard')`

---

### Template 7: my_reservations.html
- **File:** `templates/my_reservations.html`
- **Page title:** "My Reservations"
- **Element IDs:**
  - `reservations-page` (div)
  - `reservations-table` (table)
  - For each reservation:
    - `cancel-reservation-button-{{ reservation.reservation_id }}` (button)
  - `back-to-dashboard` (button)
- **Context variables:**
  - `reservations` (list of dict with `reservation_id`, `book_title`, `reservation_date`, `status`)
- **Navigation:**
  - `cancel-reservation-button-{{ reservation.reservation_id }}` triggers POST to `url_for('cancel_reservation', reservation_id=reservation.reservation_id)`
  - `back-to-dashboard` uses `url_for('dashboard')`

---

### Template 8: my_reviews.html
- **File:** `templates/my_reviews.html`
- **Page title:** "My Reviews"
- **Element IDs:**
  - `reviews-page` (div)
  - `reviews-list` (div)
  - For each review:
    - `edit-review-button-{{ review.review_id }}` (button)
    - `delete-review-button-{{ review.review_id }}` (button)
  - `back-to-dashboard` (button)
- **Context variables:**
  - `reviews` (list of dict with `review_id`, `book_title`, `rating`, `review_text`)
- **Navigation:**
  - `edit-review-button-{{ review.review_id }}` uses `url_for('write_review_get', book_id=review.book_id)` (assuming book_id is included or accessible)
  - `delete-review-button-{{ review.review_id }}` triggers POST to a route to delete review (route not specified in requirements; if required, needs definition)
  - `back-to-dashboard` uses `url_for('dashboard')`

---

### Template 9: write_review.html
- **File:** `templates/write_review.html`
- **Page title:** "Write Review"
- **Element IDs:**
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- **Context variables:**
  - `book` (dict)
  - `existing_review` (dict or None)
- **Navigation:**
  - `submit-review-button` triggers POST to `url_for('write_review_post', book_id=book.book_id)`
  - `back-to-book` uses `url_for('book_details', book_id=book.book_id)`

---

### Template 10: profile.html
- **File:** `templates/profile.html`
- **Page title:** "My Profile"
- **Element IDs:**
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `borrow-history` (div)
  - `back-to-dashboard` (button)
- **Context variables:**
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict with `book_title`, `borrow_date`, `return_date`)
- **Navigation:**
  - `update-profile-button` triggers POST to `url_for('update_profile')`
  - `back-to-dashboard` uses `url_for('dashboard')`

---

### Template 11: payment_confirmation.html
- **File:** `templates/payment_confirmation.html`
- **Page title:** "Payment Confirmation"
- **Element IDs:**
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- **Context variables:**
  - `fine` (dict with `fine_id`, `amount`)
- **Navigation:**
  - `confirm-payment-button` triggers POST to `url_for('payment_confirmation_post', fine_id=fine.fine_id)`
  - `back-to-profile` uses `url_for('user_profile')`

---

## Section 3: Data File Schemas (Backend Development)

### File 1: users.txt
- **Path:** `data/users.txt`
- **Fields:**
  1. `username` (str)
  2. `email` (str)
  3. `phone` (str)
  4. `address` (str)
- **Description:** Stores user profile data.
- **Example rows:**
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`

---

### File 2: books.txt
- **Path:** `data/books.txt`
- **Fields:**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `genre` (str)
  6. `publisher` (str)
  7. `year` (int)
  8. `description` (str)
  9. `status` (str) - values: "Available", "Borrowed", "Reserved"
  10. `avg_rating` (float)
- **Description:** Book catalog data.
- **Example rows:**
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`

---

### File 3: borrowings.txt
- **Path:** `data/borrowings.txt`
- **Fields:**
  1. `borrow_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `borrow_date` (str, YYYY-MM-DD)
  5. `due_date` (str, YYYY-MM-DD)
  6. `return_date` (str, YYYY-MM-DD or empty if not returned)
  7. `status` (str) - values: "Active", "Returned", "Overdue"
  8. `fine_amount` (float)
- **Description:** User borrow transactions.
- **Example rows:**
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`

---

### File 4: reservations.txt
- **Path:** `data/reservations.txt`
- **Fields:**
  1. `reservation_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `reservation_date` (str, YYYY-MM-DD)
  5. `status` (str) - values: "Active", "Cancelled"
- **Description:** User book reservations.
- **Example rows:**
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`

---

### File 5: reviews.txt
- **Path:** `data/reviews.txt`
- **Fields:**
  1. `review_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `rating` (int)
  5. `review_text` (str)
  6. `review_date` (str, YYYY-MM-DD)
- **Description:** User book reviews.
- **Example rows:**
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`

---

### File 6: fines.txt
- **Path:** `data/fines.txt`
- **Fields:**
  1. `fine_id` (int)
  2. `username` (str)
  3. `borrow_id` (int)
  4. `amount` (float)
  5. `status` (str) - e.g., "Unpaid", "Paid"
  6. `date_issued` (str, YYYY-MM-DD)
- **Description:** Records of fines due from overdue borrowings.
- **Example rows:**
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`

---

# End of Design Specification
