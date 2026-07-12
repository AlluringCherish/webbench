# Design Specification Document for OnlineLibrary

---

## Section 1: Flask Routes Specification (Backend Development)

### 1. Root Route
- URL Path: `/`
- Function Name: `root_redirect`
- HTTP Method: GET
- Template Rendered: Redirect to `dashboard`
- Context Variables: None

### 2. Dashboard Page
- URL Path: `/dashboard`
- Function Name: `dashboard`
- HTTP Method: GET
- Template Rendered: `dashboard.html`
- Context Variables:
  - `username` (str): Logged-in user's username
  - `featured_books` (list of dict): List of featured books on dashboard; each dict with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str) - one of "Available", "Borrowed", "Reserved"

### 3. Book Catalog Page
- URL Path: `/catalog`
- Function Name: `book_catalog`
- HTTP Method: GET
- Template Rendered: `catalog.html`
- Context Variables:
  - `books` (list of dict): List of books; each dict has keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)

### 4. Book Details Page
- URL Path: `/book/<int:book_id>`
- Function Name: `book_details`
- HTTP Method: GET
- Template Rendered: `book_details.html`
- Context Variables:
  - `book` (dict): Book information with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
    - `description` (str)
    - `avg_rating` (float)
  - `reviews` (list of dict): List of review dicts with keys:
    - `review_id` (int)
    - `username` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str) (format YYYY-MM-DD)

### 5. Borrow Confirmation Page
- URL Path: `/borrow/<int:book_id>`
- Function Name: `borrow_confirmation`
- HTTP Method: GET
- Template Rendered: `borrow.html`
- Context Variables:
  - `book` (dict): Book info as in `book_details`
  - `due_date` (str): Due date string 14 days from current date (format YYYY-MM-DD)

- URL Path: `/borrow/<int:book_id>/confirm`
- Function Name: `confirm_borrow`
- HTTP Method: POST
- Template Rendered: Redirect or confirmation page as needed (not rendering borrow.html again)
- Context Variables: None

- URL Path: `/borrow/<int:book_id>/cancel`
- Function Name: `cancel_borrow`
- HTTP Method: POST
- Template Rendered: Redirect to `book_details` page
- Context Variables: None

### 6. My Borrowings Page
- URL Path: `/my_borrows`
- Function Name: `my_borrows`
- HTTP Method: GET
- Template Rendered: `my_borrows.html`
- Context Variables:
  - `borrows` (list of dict): List of borrowings with keys:
    - `borrow_id` (int)
    - `book_title` (str)
    - `borrow_date` (str, YYYY-MM-DD)
    - `due_date` (str, YYYY-MM-DD)
    - `status` (str) - e.g., Active, Returned, Overdue
  - `filter_status` (str): The current filter selected (All, Active, Returned, Overdue)

- URL Path: `/return/<int:borrow_id>`
- Function Name: `return_book`
- HTTP Method: POST
- Template Rendered: Redirect or confirmation page
- Context Variables: None

### 7. My Reservations Page
- URL Path: `/my_reservations`
- Function Name: `my_reservations`
- HTTP Method: GET
- Template Rendered: `my_reservations.html`
- Context Variables:
  - `reservations` (list of dict): List of reservations with keys:
    - `reservation_id` (int)
    - `book_title` (str)
    - `reservation_date` (str, YYYY-MM-DD)
    - `status` (str) - e.g., Active, Cancelled

- URL Path: `/cancel_reservation/<int:reservation_id>`
- Function Name: `cancel_reservation`
- HTTP Method: POST
- Template Rendered: Redirect or confirmation
- Context Variables: None

### 8. My Reviews Page
- URL Path: `/my_reviews`
- Function Name: `my_reviews`
- HTTP Method: GET
- Template Rendered: `my_reviews.html`
- Context Variables:
  - `reviews` (list of dict): List of user reviews with keys:
    - `review_id` (int)
    - `book_title` (str)
    - `rating` (int)
    - `review_text` (str)

- URL Path: `/edit_review/<int:review_id>`
- Function Name: `edit_review_page`
- HTTP Method: GET
- Template Rendered: `write_review.html`
- Context Variables:
  - `review` (dict): Existing review details with keys:
    - `review_id` (int)
    - `book_id` (int)
    - `rating` (int)
    - `review_text` (str)
    - `book_title` (str)

- URL Path: `/edit_review/<int:review_id>/submit`
- Function Name: `submit_edit_review`
- HTTP Method: POST
- Template Rendered: Redirect to `my_reviews` or confirmation
- Context Variables: None

- URL Path: `/delete_review/<int:review_id>`
- Function Name: `delete_review`
- HTTP Method: POST
- Template Rendered: Redirect to `my_reviews`
- Context Variables: None

### 9. Write Review Page
- URL Path: `/write_review/<int:book_id>`
- Function Name: `write_review_page`
- HTTP Method: GET
- Template Rendered: `write_review.html`
- Context Variables:
  - `book` (dict): Book info with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)

- URL Path: `/write_review/<int:book_id>/submit`
- Function Name: `submit_review`
- HTTP Method: POST
- Template Rendered: Redirect to book details or confirmation
- Context Variables: None

### 10. User Profile Page
- URL Path: `/profile`
- Function Name: `user_profile`
- HTTP Method: GET
- Template Rendered: `profile.html`
- Context Variables:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): List of previously borrowed books with keys:
    - `book_title` (str)
    - `borrow_date` (str, YYYY-MM-DD)
    - `return_date` (str or None)

- URL Path: `/profile/update`
- Function Name: `update_profile`
- HTTP Method: POST
- Template Rendered: Redirect or confirmation
- Context Variables: None

### 11. Payment Confirmation Page
- URL Path: `/payment/<int:fine_id>`
- Function Name: `payment_confirmation`
- HTTP Method: GET
- Template Rendered: `payment.html`
- Context Variables:
  - `fine_amount` (float)

- URL Path: `/payment/<int:fine_id>/confirm`
- Function Name: `confirm_payment`
- HTTP Method: POST
- Template Rendered: Redirect or confirmation
- Context Variables: None

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. Dashboard Template
- Filename: `templates/dashboard.html`
- Page Title: "Library Dashboard"
- Element IDs and Types:
  - `dashboard-page` (Div)
  - `welcome-message` (H1)
  - `browse-books-button` (Button)
  - `my-borrows-button` (Button)
- Context Variables:
  - `username` (str)
  - `featured_books` (list of dict with fields: `book_id`(int), `title`(str), `author`(str), `status`(str))
- Navigation:
  - `browse-books-button`: url_for `book_catalog`
  - `my-borrows-button`: url_for `my_borrows`

### 2. Book Catalog Template
- Filename: `templates/catalog.html`
- Page Title: "Book Catalog"
- Element IDs and Types:
  - `catalog-page` (Div)
  - `search-input` (Input)
  - `book-grid` (Div)
  - `view-book-button-{book_id}` (Button) - dynamic for each book
  - `back-to-dashboard` (Button)
- Context Variables:
  - `books` (list of dict with fields: `book_id`(int), `title`(str), `author`(str), `status`(str))
- Navigation:
  - `view-book-button-{book_id}`: url_for `book_details`, parameter: `book_id`
  - `back-to-dashboard`: url_for `dashboard`

### 3. Book Details Template
- Filename: `templates/book_details.html`
- Page Title: "Book Details"
- Element IDs and Types:
  - `book-details-page` (Div)
  - `book-title` (H1)
  - `book-author` (Div)
  - `book-status` (Div)
  - `borrow-button` (Button)
  - `reviews-section` (Div)
  - `write-review-button` (Button)
  - `back-to-catalog` (Button)
- Context Variables:
  - `book` (dict): keys as defined in Section 1
  - `reviews` (list of dict): each dict keys `review_id`(int), `username`(str), `rating`(int), `review_text`(str), `review_date`(str)
- Navigation:
  - `borrow-button`: url_for `borrow_confirmation`, parameter: `book_id` from `book.book_id`
  - `write-review-button`: url_for `write_review_page`, parameter: `book_id`
  - `back-to-catalog`: url_for `book_catalog`

### 4. Borrow Confirmation Template
- Filename: `templates/borrow.html`
- Page Title: "Borrow Confirmation"
- Element IDs and Types:
  - `borrow-page` (Div)
  - `borrow-book-info` (Div)
  - `due-date-display` (Div)
  - `confirm-borrow-button` (Button)
  - `cancel-borrow-button` (Button)
- Context Variables:
  - `book` (dict) with keys as in `book_details`
  - `due_date` (str)
- Navigation:
  - `confirm-borrow-button`: form POST to `confirm_borrow` with `book_id`
  - `cancel-borrow-button`: form POST to `cancel_borrow` with `book_id`

### 5. My Borrowings Template
- Filename: `templates/my_borrows.html`
- Page Title: "My Borrowings"
- Element IDs and Types:
  - `my-borrows-page` (Div)
  - `filter-status` (Dropdown/select)
  - `borrows-table` (Table)
  - `return-book-button-{borrow_id}` (Button) - dynamic for each active borrow
  - `back-to-dashboard` (Button)
- Context Variables:
  - `borrows` (list of dict with keys: `borrow_id`(int), `book_title`(str), `borrow_date`(str), `due_date`(str), `status`(str))
  - `filter_status` (str)
- Navigation:
  - `return-book-button-{borrow_id}`: form POST to `return_book` with `borrow_id`
  - `back-to-dashboard`: url_for `dashboard`

### 6. My Reservations Template
- Filename: `templates/my_reservations.html`
- Page Title: "My Reservations"
- Element IDs and Types:
  - `reservations-page` (Div)
  - `reservations-table` (Table)
  - `cancel-reservation-button-{reservation_id}` (Button) - dynamic per reservation
  - `back-to-dashboard` (Button)
- Context Variables:
  - `reservations` (list of dict with keys: `reservation_id`(int), `book_title`(str), `reservation_date`(str), `status`(str))
- Navigation:
  - `cancel-reservation-button-{reservation_id}`: form POST to `cancel_reservation` with `reservation_id`
  - `back-to-dashboard`: url_for `dashboard`

### 7. My Reviews Template
- Filename: `templates/my_reviews.html`
- Page Title: "My Reviews"
- Element IDs and Types:
  - `reviews-page` (Div)
  - `reviews-list` (Div)
  - `edit-review-button-{review_id}` (Button) - per review
  - `delete-review-button-{review_id}` (Button) - per review
  - `back-to-dashboard` (Button)
- Context Variables:
  - `reviews` (list of dict with keys: `review_id`(int), `book_title`(str), `rating`(int), `review_text`(str))
- Navigation:
  - `edit-review-button-{review_id}`: url_for `edit_review_page` with `review_id`
  - `delete-review-button-{review_id}`: form POST to `delete_review` with `review_id`
  - `back-to-dashboard`: url_for `dashboard`

### 8. Write Review Template
- Filename: `templates/write_review.html`
- Page Title: "Write Review"
- Element IDs and Types:
  - `write-review-page` (Div)
  - `book-info-display` (Div)
  - `rating-input` (Dropdown/select)
  - `review-text` (Textarea)
  - `submit-review-button` (Button)
  - `back-to-book` (Button)
- Context Variables:
  - If editing: `review` (dict) with keys: `review_id`(int), `book_id`(int), `rating`(int), `review_text`(str), `book_title`(str)
  - If writing new: `book` (dict) with keys: `book_id`(int), `title`(str), `author`(str)
- Navigation:
  - `submit-review-button`: form POST to `submit_review` or `submit_edit_review` depending on context
  - `back-to-book`: url_for `book_details` with `book_id`

### 9. User Profile Template
- Filename: `templates/profile.html`
- Page Title: "My Profile"
- Element IDs and Types:
  - `profile-page` (Div)
  - `profile-username` (Div)
  - `profile-email` (Input)
  - `update-profile-button` (Button)
  - `borrow-history` (Div)
  - `back-to-dashboard` (Button)
- Context Variables:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict) with keys:
    - `book_title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)
- Navigation:
  - `update-profile-button`: form POST to `update_profile`
  - `back-to-dashboard`: url_for `dashboard`

### 10. Payment Confirmation Template
- Filename: `templates/payment.html`
- Page Title: "Payment Confirmation"
- Element IDs and Types:
  - `payment-page` (Div)
  - `fine-amount-display` (Div)
  - `confirm-payment-button` (Button)
  - `back-to-profile` (Button)
- Context Variables:
  - `fine_amount` (float)
- Navigation:
  - `confirm-payment-button`: form POST to `confirm_payment` with `fine_id`
  - `back-to-profile`: url_for `user_profile`

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- File Path: `data/users.txt`
- Fields (pipe-delimited):
  - `username` (str)
  - `email` (str)
  - `phone` (str)
  - `address` (str)
- Description: Stores user profile information.
- Example Rows:
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`

### 2. books.txt
- File Path: `data/books.txt`
- Fields (pipe-delimited):
  - `book_id` (int)
  - `title` (str)
  - `author` (str)
  - `isbn` (str)
  - `genre` (str)
  - `publisher` (str)
  - `year` (int)
  - `description` (str)
  - `status` (str) - "Available", "Borrowed", "Reserved"
  - `avg_rating` (float)
- Description: Stores book details including availability and average rating.
- Example Rows:
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  - `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`

### 3. borrowings.txt
- File Path: `data/borrowings.txt`
- Fields (pipe-delimited):
  - `borrow_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `borrow_date` (str) (format YYYY-MM-DD)
  - `due_date` (str) (format YYYY-MM-DD)
  - `return_date` (str or empty) (format YYYY-MM-DD)
  - `status` (str) - "Active", "Returned", "Overdue"
  - `fine_amount` (float)
- Description: Records borrow transactions and status.
- Example Rows:
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`

### 4. reservations.txt
- File Path: `data/reservations.txt`
- Fields (pipe-delimited):
  - `reservation_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `reservation_date` (str) (format YYYY-MM-DD)
  - `status` (str) - e.g., "Active", "Cancelled"
- Description: Stores user book reservations.
- Example Rows:
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`

### 5. reviews.txt
- File Path: `data/reviews.txt`
- Fields (pipe-delimited):
  - `review_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `rating` (int) (1-5)
  - `review_text` (str)
  - `review_date` (str) (format YYYY-MM-DD)
- Description: Contains user reviews for books.
- Example Rows:
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`

### 6. fines.txt
- File Path: `data/fines.txt`
- Fields (pipe-delimited):
  - `fine_id` (int)
  - `username` (str)
  - `borrow_id` (int)
  - `amount` (float)
  - `status` (str) - "Unpaid", "Paid"
  - `date_issued` (str) (format YYYY-MM-DD)
- Description: Records fines issued for overdue borrowings.
- Example Rows:
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`

---

# End of Design Specification Document
