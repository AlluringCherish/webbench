# OnlineLibrary Web Application - Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

### 1. Root Route
- **URL Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Method:** GET
- **Template Rendered:** None (redirect to `/dashboard`)
- **Context Variables:** None

### 2. Dashboard Page
- **URL Path:** `/dashboard`
- **Function Name:** `dashboard_page`
- **HTTP Method:** GET
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `username` : `str` (current user's username)

### 3. Book Catalog Page
- **URL Path:** `/catalog`
- **Function Name:** `book_catalog_page`
- **HTTP Method:** GET
- **Template Rendered:** `catalog.html`
- **Context Variables:**
  - `books` : `list` of `dict` with keys:
    - `book_id` : `int`
    - `title` : `str`
    - `author` : `str`
    - `isbn` : `str`
    - `genre` : `str`
    - `publisher` : `str`
    - `year` : `int`
    - `description` : `str`
    - `status` : `str` (Values: Available, Borrowed, Reserved)
    - `avg_rating` : `float`

### 4. Book Details Page
- **URL Path:** `/book/<int:book_id>`
- **Function Name:** `book_details_page`
- **HTTP Method:** GET
- **Template Rendered:** `book_details.html`
- **Context Variables:**
  - `book` : `dict` (same keys as catalog books)
  - `reviews` : `list` of `dict` with keys:
     - `review_id` : `int`
     - `username` : `str`
     - `rating` : `int`
     - `review_text` : `str`
     - `review_date` : `str` (YYYY-MM-DD)

### 5. Borrow Confirmation Page
- **URL Path:** `/borrow/<int:book_id>`
- **Function Name:** `borrow_confirmation_page`
- **HTTP Method:** GET, POST
- **Template Rendered:** `borrow_confirmation.html`
- **Context Variables (GET):**
  - `book` : `dict` (keys: `book_id`, `title`, `author`)
  - `due_date` : `str` (YYYY-MM-DD, 14 days from borrow)
- **POST Handling:**
  - Confirm borrowing, process logic

### 6. Borrow Confirmation Processing
- **URL Path:** `/confirm_borrow/<int:book_id>`
- **Function Name:** `confirm_borrow`
- **HTTP Method:** POST
- **Template Rendered:** Confirmation page or redirect
- **Context Variables:** Confirmation details

### 7. My Borrowings Page
- **URL Path:** `/my_borrows`
- **Function Name:** `my_borrows_page`
- **HTTP Method:** GET
- **Template Rendered:** `my_borrows.html`
- **Context Variables:**
  - `borrows` : `list` of `dict` with keys:
    - `borrow_id` : `int`
    - `book_title` : `str`
    - `borrow_date` : `str` (YYYY-MM-DD)
    - `due_date` : `str` (YYYY-MM-DD)
    - `status` : `str` (All, Active, Returned, Overdue)
    - `fine_amount` : `float`

### 8. Return Book Processing
- **URL Path:** `/return_borrow/<int:borrow_id>`
- **Function Name:** `return_borrow`
- **HTTP Method:** POST
- **Template Rendered:** Return confirmation or redirect
- **Context Variables:**
  - `borrow_id` : `int`
  - `book_title` : `str`
  - `return_date` : `str` (current date)
  - `confirmation_message` : `str`

### 9. My Reservations Page
- **URL Path:** `/my_reservations`
- **Function Name:** `my_reservations_page`
- **HTTP Method:** GET
- **Template Rendered:** `my_reservations.html`
- **Context Variables:**
  - `reservations` : `list` of `dict` with keys:
    - `reservation_id` : `int`
    - `book_title` : `str`
    - `reservation_date` : `str` (YYYY-MM-DD)
    - `status` : `str` (Active, Cancelled)

### 10. Cancel Reservation Processing
- **URL Path:** `/cancel_reservation/<int:reservation_id>`
- **Function Name:** `cancel_reservation`
- **HTTP Method:** POST
- **Template Rendered:** Confirmation page or redirect
- **Context Variables:**
  - `reservation_id` : `int`
  - `confirmation_message` : `str`

### 11. My Reviews Page
- **URL Path:** `/my_reviews`
- **Function Name:** `my_reviews_page`
- **HTTP Method:** GET
- **Template Rendered:** `my_reviews.html`
- **Context Variables:**
  - `reviews` : `list` of `dict` with keys:
    - `review_id` : `int`
    - `book_title` : `str`
    - `rating` : `int`
    - `review_text` : `str`
    - `review_date` : `str` (YYYY-MM-DD)

### 12. Write Review Page
- **URL Path:** `/write_review/<int:book_id>`
- **Function Name:** `write_review_page`
- **HTTP Method:** GET, POST
- **Template Rendered:** `write_review.html`
- **Context Variables (GET):**
  - `book` : `dict` (keys: `book_id`, `title`)
  - `existing_review` : `dict` or `None` (keys: `review_id`, `rating`, `review_text`)

### 13. Submit Review Processing
- **URL Path:** `/submit_review/<int:book_id>`
- **Function Name:** `submit_review`
- **HTTP Method:** POST
- **Template Rendered:** Confirmation page or redirect
- **Context Variables:**
  - `confirmation_message` : `str`

### 14. User Profile Page
- **URL Path:** `/profile`
- **Function Name:** `profile_page`
- **HTTP Method:** GET, POST
- **Template Rendered:** `profile.html`
- **Context Variables:**
  - `username` : `str`
  - `email` : `str`
  - `borrow_history` : `list` of `dict` with keys:
    - `book_title` : `str`
    - `borrow_date` : `str` (YYYY-MM-DD)
    - `return_date` : `str` (YYYY-MM-DD or empty)

### 15. Payment Confirmation Page
- **URL Path:** `/payment/<int:fine_id>`
- **Function Name:** `payment_confirmation_page`
- **HTTP Method:** GET, POST
- **Template Rendered:** `payment_confirmation.html`
- **Context Variables:**
  - `fine` : `dict` (keys: `fine_id`, `amount`)
  - Optional `confirmation_message` : `str`

### 16. Confirm Payment Processing
- **URL Path:** `/confirm_payment/<int:fine_id>`
- **Function Name:** `confirm_payment`
- **HTTP Method:** POST
- **Template Rendered:** Confirmation page or redirect
- **Context Variables:**
  - `confirmation_message` : `str`

---

## Section 2: HTML Template Specifications

### Template: `dashboard.html`
- Path: `templates/dashboard.html`
- Page Title: "Library Dashboard"
- Element IDs:
  - `dashboard-page` (div)
  - `welcome-message` (h1)
  - `browse-books-button` (button)
  - `my-borrows-button` (button)
- Context Variables:
  - `username` : `str`
- Navigation Mappings:
  - `browse-books-button` → `url_for('book_catalog_page')`
  - `my-borrows-button` → `url_for('my_borrows_page')`

### Template: `catalog.html`
- Path: `templates/catalog.html`
- Page Title: "Book Catalog"
- Element IDs:
  - `catalog-page` (div)
  - `search-input` (input)
  - `book-grid` (div)
  - `back-to-dashboard` (button)
  - Per book:
    - `view-book-button-{book_id}` (button)
- Context Variables:
  - `books` : list of dict
- Navigation Mappings:
  - `back-to-dashboard` → `url_for('dashboard_page')`
  - `view-book-button-{book_id}` → `url_for('book_details_page', book_id=book.book_id)`

### Template: `book_details.html`
- Path: `templates/book_details.html`
- Page Title: "Book Details"
- Element IDs:
  - `book-details-page` (div)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button)
  - `reviews-section` (div)
  - `write-review-button` (button)
  - `back-to-catalog` (button)
- Context Variables:
  - `book` : dict
  - `reviews` : list of dict
- Navigation Mappings:
  - `borrow-button` → `url_for('borrow_confirmation_page', book_id=book.book_id)`
  - `write-review-button` → `url_for('write_review_page', book_id=book.book_id)`
  - `back-to-catalog` → `url_for('book_catalog_page')`

### Template: `borrow_confirmation.html`
- Path: `templates/borrow_confirmation.html`
- Page Title: "Borrow Confirmation"
- Element IDs:
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button)
  - `cancel-borrow-button` (button)
- Context Variables:
  - `book` : dict
  - `due_date` : str
- Navigation Mappings:
  - `cancel-borrow-button` → `url_for('book_details_page', book_id=book.book_id)`
  - `confirm-borrow-button` is form submit button POSTing confirmation

### Template: `my_borrows.html`
- Path: `templates/my_borrows.html`
- Page Title: "My Borrowings"
- Element IDs:
  - `my-borrows-page` (div)
  - `filter-status` (dropdown)
  - `borrows-table` (table)
  - `back-to-dashboard` (button)
  - Per borrow:
    - `return-book-button-{borrow_id}` (button)
- Context Variables:
  - `borrows` : list of dict
- Navigation Mappings:
  - `back-to-dashboard` → `url_for('dashboard_page')`
  - `return-book-button-{borrow_id}` POSTs to `url_for('return_borrow', borrow_id=borrow.borrow_id)`

### Template: `my_reservations.html`
- Path: `templates/my_reservations.html`
- Page Title: "My Reservations"
- Element IDs:
  - `reservations-page` (div)
  - `reservations-table` (table)
  - `back-to-dashboard` (button)
  - Per reservation:
    - `cancel-reservation-button-{reservation_id}` (button)
- Context Variables:
  - `reservations` : list of dict
- Navigation Mappings:
  - `back-to-dashboard` → `url_for('dashboard_page')`
  - `cancel-reservation-button-{reservation_id}` POSTs to `url_for('cancel_reservation', reservation_id=reservation.reservation_id)`

### Template: `my_reviews.html`
- Path: `templates/my_reviews.html`
- Page Title: "My Reviews"
- Element IDs:
  - `reviews-page` (div)
  - `reviews-list` (div)
  - `back-to-dashboard` (button)
  - Per review:
    - `edit-review-button-{review_id}` (button)
    - `delete-review-button-{review_id}` (button)
- Context Variables:
  - `reviews` : list of dict
- Navigation Mappings:
  - `back-to-dashboard` → `url_for('dashboard_page')`
  - `edit-review-button-{review_id}` → `url_for('write_review_page', book_id=review.book_id)`
  - `delete-review-button-{review_id}` POSTs to delete review route with `review_id`

### Template: `write_review.html`
- Path: `templates/write_review.html`
- Page Title: "Write Review"
- Element IDs:
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- Context Variables:
  - `book` : dict
  - `existing_review` : dict or None
- Navigation Mappings:
  - `back-to-book` → `url_for('book_details_page', book_id=book.book_id)`
  - Form POST submission for review

### Template: `profile.html`
- Path: `templates/profile.html`
- Page Title: "My Profile"
- Element IDs:
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `borrow-history` (div)
  - `back-to-dashboard` (button)
- Context Variables:
  - `username` : str
  - `email` : str
  - `borrow_history` : list of dict
- Navigation Mappings:
  - `back-to-dashboard` → `url_for('dashboard_page')`

### Template: `payment_confirmation.html`
- Path: `templates/payment_confirmation.html`
- Page Title: "Payment Confirmation"
- Element IDs:
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- Context Variables:
  - `fine` : dict
  - Optional `confirmation_message` : str
- Navigation Mappings:
  - `back-to-profile` → `url_for('profile_page')`

---

## Section 3: Data File Schemas

### 1. `data/users.txt`
- Fields (pipe-separated):
  1. `username` (str)
  2. `email` (str)
  3. `phone` (str)
  4. `address` (str)
- Description: User profile information.
- Examples:
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`

### 2. `data/books.txt`
- Fields (pipe-separated):
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `genre` (str)
  6. `publisher` (str)
  7. `year` (int)
  8. `description` (str)
  9. `status` (str: Available, Borrowed, Reserved)
  10. `avg_rating` (float)
- Description: Book details.
- Examples:
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  - `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`
  - `4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5`
  - `5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3`

### 3. `data/borrowings.txt`
- Fields (pipe-separated):
  1. `borrow_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `borrow_date` (str YYYY-MM-DD)
  5. `due_date` (str YYYY-MM-DD)
  6. `return_date` (str YYYY-MM-DD or empty)
  7. `status` (str: Active, Returned, Overdue)
  8. `fine_amount` (float)
- Description: Records of user book borrowings.
- Examples:
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`

### 4. `data/reservations.txt`
- Fields (pipe-separated):
  1. `reservation_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `reservation_date` (str YYYY-MM-DD)
  5. `status` (str: Active, Cancelled)
- Description: Tracks reservations of books by users.
- Examples:
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`

### 5. `data/reviews.txt`
- Fields (pipe-separated):
  1. `review_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `rating` (int from 1 to 5)
  5. `review_text` (str)
  6. `review_date` (str YYYY-MM-DD)
- Description: User-written book reviews.
- Examples:
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`

### 6. `data/fines.txt`
- Fields (pipe-separated):
  1. `fine_id` (int)
  2. `username` (str)
  3. `borrow_id` (int)
  4. `amount` (float)
  5. `status` (str: Unpaid, Paid)
  6. `date_issued` (str YYYY-MM-DD)
- Description: Records of fines for overdue borrowings.
- Examples:
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`

---

This detailed design specification document establishes the complete blueprint for the 'OnlineLibrary' application backend routes, frontend templates, and local file data structures. This enables efficient, unambiguous development by separate teams.
