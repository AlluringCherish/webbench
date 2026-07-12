# OnlineLibrary Application Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

### 1. Root Route
- **URL path:** `/`
- **Function name:** `root_redirect`
- **HTTP method:** GET
- **Action:** Redirects to dashboard page `/dashboard`
- **Template rendered:** None (redirect only)
- **Context variables:** None

---

### 2. Dashboard Page
- **URL path:** `/dashboard`
- **Function name:** `dashboard`
- **HTTP method:** GET
- **Template rendered:** `dashboard.html`
- **Context variables:**
  - `username` (str): Current logged-in user's username

---

### 3. Book Catalog Page
- **URL path:** `/catalog`
- **Function name:** `book_catalog`
- **HTTP method:** GET
- **Template rendered:** `catalog.html`
- **Context variables:**
  - `books` (list of dict): List of book dictionaries with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str) - "Available", "Borrowed", or "Reserved"

---

### 4. Book Details Page
- **URL path:** `/book/<int:book_id>`
- **Function name:** `book_details`
- **HTTP method:** GET
- **Template rendered:** `book_details.html`
- **Context variables:**
  - `book` (dict): Details of the book with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
    - other descriptive fields as per data (isbn, genre, publisher, year, description, avg_rating)
  - `reviews` (list of dict): List of reviews related to this book with keys:
    - `review_id` (int)
    - `username` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str in YYYY-MM-DD)

---

### 5. Borrow Confirmation Page
- **URL path:** `/borrow/<int:book_id>` (GET to display confirmation)
- **Function name:** `borrow_confirmation`
- **HTTP method:** GET
- **Template rendered:** `borrow_confirmation.html`
- **Context variables:**
  - `book` (dict): Book details same as in book_details
  - `due_date` (str, date in YYYY-MM-DD): Due date calculated 14 days from borrowing date


- **URL path:** `/borrow/<int:book_id>/confirm` (POST to confirm borrow)
- **Function name:** `confirm_borrow`
- **HTTP method:** POST
- **Template rendered:** Redirect or confirmation page handled by frontend
- **Context variables:** None

- **URL path:** `/borrow/<int:book_id>/cancel` (POST or GET to cancel borrow and return to book details)
- **Function name:** `cancel_borrow`
- **HTTP method:** POST or GET
- **Template rendered:** Redirect to `/book/<book_id>`
- **Context variables:** None

---

### 6. My Borrowings Page
- **URL path:** `/my_borrows`
- **Function name:** `my_borrows`
- **HTTP method:** GET
- **Template rendered:** `my_borrows.html`
- **Context variables:**
  - `borrowings` (list of dict): List of borrowings by user with keys:
    - `borrow_id` (int)
    - `book_title` (str)
    - `borrow_date` (str, YYYY-MM-DD)
    - `due_date` (str, YYYY-MM-DD)
    - `status` (str) - "Active", "Returned", "Overdue"
  - `filter_status` (str): Current filter value ("All", "Active", "Returned", "Overdue")


- **URL path:** `/return/<int:borrow_id>` (POST to return book)
- **Function name:** `return_book`
- **HTTP method:** POST
- **Template rendered:** Redirect to `my_borrows`
- **Context variables:** None

---

### 7. My Reservations Page
- **URL path:** `/my_reservations`
- **Function name:** `my_reservations`
- **HTTP method:** GET
- **Template rendered:** `my_reservations.html`
- **Context variables:**
  - `reservations` (list of dict): List of reservations by user with keys:
    - `reservation_id` (int)
    - `book_title` (str)
    - `reservation_date` (str, YYYY-MM-DD)
    - `status` (str)


- **URL path:** `/cancel_reservation/<int:reservation_id>` (POST to cancel reservation)
- **Function name:** `cancel_reservation`
- **HTTP method:** POST
- **Template rendered:** Redirect to `my_reservations`
- **Context variables:** None

---

### 8. My Reviews Page
- **URL path:** `/my_reviews`
- **Function name:** `my_reviews`
- **HTTP method:** GET
- **Template rendered:** `my_reviews.html`
- **Context variables:**
  - `reviews` (list of dict): List of user reviews with keys:
    - `review_id` (int)
    - `book_title` (str)
    - `rating` (int)
    - `review_text` (str)

- **URL path:** `/edit_review/<int:review_id>` (GET to show edit form)
- **Function name:** `edit_review`
- **HTTP method:** GET
- **Template rendered:** `write_review.html`
- **Context variables:**
  - `review` (dict): Review details with keys:
    - `review_id` (int)
    - `book_id` (int)
    - `rating` (int)
    - `review_text` (str)
  - `book` (dict): Book info related to review

- **URL path:** `/edit_review/<int:review_id>/submit` (POST to submit edit)
- **Function name:** `submit_edit_review`
- **HTTP method:** POST
- **Template rendered:** Redirect to `my_reviews`
- **Context variables:** None

- **URL path:** `/delete_review/<int:review_id>` (POST to delete review)
- **Function name:** `delete_review`
- **HTTP method:** POST
- **Template rendered:** Redirect to `my_reviews`
- **Context variables:** None

---

### 9. Write Review Page (New Review)
- **URL path:** `/write_review/<int:book_id>` (GET to display form)
- **Function name:** `write_review`
- **HTTP method:** GET
- **Template rendered:** `write_review.html`
- **Context variables:**
  - `book` (dict): Book details

- **URL path:** `/write_review/<int:book_id>/submit` (POST to submit new review)
- **Function name:** `submit_review`
- **HTTP method:** POST
- **Template rendered:** Redirect to `book_details`
- **Context variables:** None

---

### 10. User Profile Page
- **URL path:** `/profile`
- **Function name:** `user_profile`
- **HTTP method:** GET
- **Template rendered:** `profile.html`
- **Context variables:**
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): List of past borrowings with keys:
    - `book_title` (str)
    - `borrow_date` (str)
    - `return_date` (str or empty if not returned)

- **URL path:** `/profile/update` (POST to update profile email)
- **Function name:** `update_profile`
- **HTTP method:** POST
- **Template rendered:** Redirect to `profile`
- **Context variables:** None

---

### 11. Payment Confirmation Page
- **URL path:** `/payment/<int:fine_id>`
- **Function name:** `payment_confirmation`
- **HTTP method:** GET
- **Template rendered:** `payment_confirmation.html`
- **Context variables:**
  - `fine_amount` (float)
  - `fine_id` (int)

- **URL path:** `/payment/<int:fine_id>/confirm` (POST to confirm payment)
- **Function name:** `confirm_payment`
- **HTTP method:** POST
- **Template rendered:** Redirect to `profile`
- **Context variables:** None

---

## Section 2: HTML Template Specifications (Frontend Development)

### Dashboard Template
- **Filename/Path:** `templates/dashboard.html`
- **Page title:** Library Dashboard
- **Element IDs:**
  - `dashboard-page` (div)
  - `welcome-message` (h1) - displays username
  - `browse-books-button` (button) - navigates to `book_catalog`
  - `my-borrows-button` (button) - navigates to `my_borrows`
- **Context Variables:**
  - `username` (str)
- **Navigation mappings:**
  - `url_for('book_catalog')` for browse-books-button
  - `url_for('my_borrows')` for my-borrows-button

---

### Book Catalog Template
- **Filename/Path:** `templates/catalog.html`
- **Page title:** Book Catalog
- **Element IDs:**
  - `catalog-page` (div)
  - `search-input` (input)
  - `book-grid` (div)
  - Multiple dynamic IDs: `view-book-button-{{ book.book_id }}` (button) for each book
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `books` (list of dicts): each dict contains `book_id`, `title`, `author`, `status`
- **Navigation mappings:**
  - `url_for('book_details', book_id=book.book_id)` for each book view-book-button
  - `url_for('dashboard')` for back-to-dashboard

---

### Book Details Template
- **Filename/Path:** `templates/book_details.html`
- **Page title:** Book Details
- **Element IDs:**
  - `book-details-page` (div)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button)
  - `reviews-section` (div)
  - `write-review-button` (button)
  - `back-to-catalog` (button)
- **Context Variables:**
  - `book` (dict with full book details)
  - `reviews` (list of dict)
- **Navigation mappings:**
  - `url_for('borrow_confirmation', book_id=book.book_id)` for borrow-button
  - `url_for('write_review', book_id=book.book_id)` for write-review-button
  - `url_for('book_catalog')` for back-to-catalog

---

### Borrow Confirmation Template
- **Filename/Path:** `templates/borrow_confirmation.html`
- **Page title:** Borrow Confirmation
- **Element IDs:**
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button)
  - `cancel-borrow-button` (button)
- **Context Variables:**
  - `book` (dict)
  - `due_date` (str)
- **Navigation mappings:**
  - `url_for('confirm_borrow', book_id=book.book_id)` for confirm-borrow-button (POST form action)
  - `url_for('cancel_borrow', book_id=book.book_id)` for cancel-borrow-button

---

### My Borrowings Template
- **Filename/Path:** `templates/my_borrows.html`
- **Page title:** My Borrowings
- **Element IDs:**
  - `my-borrows-page` (div)
  - `filter-status` (dropdown/select)
  - `borrows-table` (table)
  - Dynamic IDs for return buttons: `return-book-button-{{ borrow.borrow_id }}` (button) for each active borrow
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `borrowings` (list of dict)
  - `filter_status` (str)
- **Navigation mappings:**
  - `url_for('return_book', borrow_id=borrow.borrow_id)` for return-book-button (POST form action)
  - `url_for('dashboard')` for back-to-dashboard

---

### My Reservations Template
- **Filename/Path:** `templates/my_reservations.html`
- **Page title:** My Reservations
- **Element IDs:**
  - `reservations-page` (div)
  - `reservations-table` (table)
  - Dynamic IDs for cancel buttons: `cancel-reservation-button-{{ reservation.reservation_id }}` (button)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `reservations` (list of dict)
- **Navigation mappings:**
  - `url_for('cancel_reservation', reservation_id=reservation.reservation_id)` for cancel-reservation-button (POST form action)
  - `url_for('dashboard')` for back-to-dashboard

---

### My Reviews Template
- **Filename/Path:** `templates/my_reviews.html`
- **Page title:** My Reviews
- **Element IDs:**
  - `reviews-page` (div)
  - `reviews-list` (div)
  - Dynamic IDs for edit buttons: `edit-review-button-{{ review.review_id }}` (button)
  - Dynamic IDs for delete buttons: `delete-review-button-{{ review.review_id }}` (button)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `reviews` (list of dict)
- **Navigation mappings:**
  - `url_for('edit_review', review_id=review.review_id)` for edit-review-button
  - `url_for('delete_review', review_id=review.review_id)` used as POST action for delete-review-button
  - `url_for('dashboard')` for back-to-dashboard

---

### Write Review Template
- **Filename/Path:** `templates/write_review.html`
- **Page title:** Write Review
- **Element IDs:**
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown/select)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- **Context Variables:**
  - Either `book` (dict) when creating new review or both `book` and `review` when editing
- **Navigation mappings:**
  - `url_for('submit_review', book_id=book.book_id)` for new review POST submission
  - `url_for('submit_edit_review', review_id=review.review_id)` for edit review POST submission
  - `url_for('book_details', book_id=book.book_id)` for back-to-book

---

### User Profile Template
- **Filename/Path:** `templates/profile.html`
- **Page title:** My Profile
- **Element IDs:**
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `borrow-history` (div)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict)
- **Navigation mappings:**
  - `url_for('dashboard')` for back-to-dashboard

---

### Payment Confirmation Template
- **Filename/Path:** `templates/payment_confirmation.html`
- **Page title:** Payment Confirmation
- **Element IDs:**
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- **Context Variables:**
  - `fine_amount` (float)
  - `fine_id` (int)
- **Navigation mappings:**
  - `url_for('confirm_payment', fine_id=fine_id)` for confirm-payment-button (POST form action)
  - `url_for('user_profile')` for back-to-profile

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- **Path:** `data/users.txt`
- **Field order and names:**
  1. `username` (str)
  2. `email` (str)
  3. `phone` (str)
  4. `address` (str)
- **Description:** Stores registered user profiles.
- **Example rows:**
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`

---

### 2. books.txt
- **Path:** `data/books.txt`
- **Field order and names:**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `genre` (str)
  6. `publisher` (str)
  7. `year` (int)
  8. `description` (str)
  9. `status` (str) - Availability status
  10. `avg_rating` (float)
- **Description:** Stores detailed book information.
- **Example rows:**
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  - `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`

---

### 3. borrowings.txt
- **Path:** `data/borrowings.txt`
- **Field order and names:**
  1. `borrow_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `borrow_date` (str, YYYY-MM-DD)
  5. `due_date` (str, YYYY-MM-DD)
  6. `return_date` (str, YYYY-MM-DD or empty)
  7. `status` (str) - "Active", "Returned", or "Overdue"
  8. `fine_amount` (float)
- **Description:** Tracks borrowing transactions.
- **Example rows:**
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`

---

### 4. reservations.txt
- **Path:** `data/reservations.txt`
- **Field order and names:**
  1. `reservation_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `reservation_date` (str, YYYY-MM-DD)
  5. `status` (str) - "Active", "Cancelled", etc.
- **Description:** Stores user reservations.
- **Example rows:**
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`

---

### 5. reviews.txt
- **Path:** `data/reviews.txt`
- **Field order and names:**
  1. `review_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `rating` (int) (1-5)
  5. `review_text` (str)
  6. `review_date` (str, YYYY-MM-DD)
- **Description:** Stores user written book reviews.
- **Example rows:**
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`

---

### 6. fines.txt
- **Path:** `data/fines.txt`
- **Field order and names:**
  1. `fine_id` (int)
  2. `username` (str)
  3. `borrow_id` (int)
  4. `amount` (float)
  5. `status` (str) - "Unpaid", "Paid"
  6. `date_issued` (str, YYYY-MM-DD)
- **Description:** Tracks overdue fines per borrowing.
- **Example rows:**
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`


---

**End of Design Specification Document**
