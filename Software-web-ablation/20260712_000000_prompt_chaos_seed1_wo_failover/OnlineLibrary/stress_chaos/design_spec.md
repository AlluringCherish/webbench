# OnlineLibrary Design Specification Document

---

## Section 1: Flask Routes Specification (Backend Development)

| URL Path                    | Function Name             | HTTP Method(s) | Template Rendered          | Context Variables Passed                                     |
|-----------------------------|---------------------------|----------------|----------------------------|-------------------------------------------------------------|
| /                           | root_redirect             | GET            | Redirects to /dashboard     | None                                                        |
| /dashboard                  | dashboard_page           | GET            | dashboard.html             | username (str), featured_books (list of dicts)              |
| /catalog                   | book_catalog              | GET            | catalog.html               | books (list of dicts)                                        |
| /book/<int:book_id>        | book_details              | GET            | book_details.html          | book (dict), reviews (list of dicts), user_can_borrow (bool) |
| /borrow/<int:book_id>      | borrow_confirmation       | GET, POST      | borrow_confirmation.html   | book (dict), due_date (str: YYYY-MM-DD)                      |
| /my-borrows                | my_borrowings             | GET            | my_borrowings.html         | borrows (list of dicts)                                      |
| /return/<int:borrow_id>    | return_book               | POST           | return_confirmation.html   | borrow (dict), fine_amount (float), return_success (bool)   |
| /my-reservations           | my_reservations           | GET            | my_reservations.html       | reservations (list of dicts)                                 |
| /cancel-reservation/<int:reservation_id> | cancel_reservation | POST           | reservation_cancel.html     | reservation_id (int), cancel_success (bool)                  |
| /my-reviews                | my_reviews                | GET            | my_reviews.html            | reviews (list of dicts)                                      |
| /write-review/<int:book_id>| write_review              | GET, POST      | write_review.html          | book (dict), existing_review (dict or None)                  |
| /edit-review/<int:review_id>| edit_review               | GET, POST      | write_review.html          | book (dict), review (dict)                                   |
| /delete-review/<int:review_id>| delete_review           | POST           | review_delete_confirmation.html | review_id (int), delete_success (bool)                    |
| /profile                   | user_profile              | GET, POST      | profile.html               | user (dict), borrow_history (list of dicts)                 |
| /payment/<int:fine_id>     | payment_confirmation      | GET, POST      | payment_confirmation.html  | fine (dict), payment_success (bool)                         |


### Route Details:

- **/**: Redirect to `/dashboard`.
- **/dashboard**: Displays dashboard; context includes username (str) and featured_books (list of dicts with keys like book_id, title, author).
- **/catalog**: Shows all books; context variable `books` is list of dicts with all book info.
- **/book/<book_id>**: Displays detailed info about a book and its reviews. Context:
  - `book` (dict) with all book attributes.
  - `reviews` (list of dicts) each with review_id, username, rating, review_text, review_date.
  - `user_can_borrow` (bool) indicating if the user can borrow the book.
- **/borrow/<book_id>**: GET shows borrow confirmation with due date (14 days ahead). POST processes borrow request.
- **/my-borrows**: Lists current borrowings with filtering by status; context `borrows` is list of dicts with borrow info.
- **/return/<borrow_id>**: POST route to process returning a borrowed book; context includes borrow data and fine info.
- **/my-reservations**: Shows user's reservations with context `reservations` list.
- **/cancel-reservation/<reservation_id>**: POST to cancel reservation.
- **/my-reviews**: Displays all user reviews.
- **/write-review/<book_id>**: GET shows form to write or edit review; POST submits review.
- **/edit-review/<review_id>**: GET/POST for editing specific review.
- **/delete-review/<review_id>**: POST for deleting a review.
- **/profile**: GET shows profile info, POST updates email; also shows borrowing history.
- **/payment/<fine_id>**: GET shows fine details and POST confirms payment.


---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. dashboard.html
- Path: templates/dashboard.html
- Page Title: "Library Dashboard"
- Element IDs:
  - dashboard-page (div)
  - welcome-message (h1)
  - browse-books-button (button)
  - my-borrows-button (button)
- Context Variables:
  - username (str)
  - featured_books (list of dicts)
- Navigation:
  - browse-books-button -> url_for('book_catalog')
  - my-borrows-button -> url_for('my_borrowings')

### 2. catalog.html
- Path: templates/catalog.html
- Page Title: "Book Catalog"
- Element IDs:
  - catalog-page (div)
  - search-input (input)
  - book-grid (div)
  - view-book-button-{book_id} (button)
  - back-to-dashboard (button)
- Context Variables:
  - books (list of dicts) with fields: book_id (int), title (str), author (str), status (str)
- Navigation:
  - view-book-button-{{ book.book_id }} -> url_for('book_details', book_id=book.book_id)
  - back-to-dashboard -> url_for('dashboard_page')

### 3. book_details.html
- Path: templates/book_details.html
- Page Title: "Book Details"
- Element IDs:
  - book-details-page (div)
  - book-title (h1)
  - book-author (div)
  - book-status (div)
  - borrow-button (button)
  - reviews-section (div)
  - write-review-button (button)
  - back-to-catalog (button)
- Context Variables:
  - book (dict) with keys: book_id, title, author, status, description, avg_rating
  - reviews (list of dicts) each with review_id, username, rating, review_text, review_date
  - user_can_borrow (bool)
- Navigation:
  - borrow-button -> url_for('borrow_confirmation', book_id=book.book_id)
  - write-review-button -> url_for('write_review', book_id=book.book_id)
  - back-to-catalog -> url_for('book_catalog')

### 4. borrow_confirmation.html
- Path: templates/borrow_confirmation.html
- Page Title: "Borrow Confirmation"
- Element IDs:
  - borrow-page (div)
  - borrow-book-info (div)
  - due-date-display (div)
  - confirm-borrow-button (button)
  - cancel-borrow-button (button)
- Context Variables:
  - book (dict)
  - due_date (str in format YYYY-MM-DD)
- Navigation:
  - confirm-borrow-button (form POST to current route)
  - cancel-borrow-button -> url_for('book_details', book_id=book.book_id)

### 5. my_borrowings.html
- Path: templates/my_borrowings.html
- Page Title: "My Borrowings"
- Element IDs:
  - my-borrows-page (div)
  - filter-status (dropdown/select)
  - borrows-table (table)
  - return-book-button-{borrow_id} (button)
  - back-to-dashboard (button)
- Context Variables:
  - borrows (list of dicts) with borrow_id, book_title, borrow_date, due_date, status
- Navigation:
  - return-book-button-{{ borrow.borrow_id }} -> url_for('return_book', borrow_id=borrow.borrow_id)
  - back-to-dashboard -> url_for('dashboard_page')

### 6. my_reservations.html
- Path: templates/my_reservations.html
- Page Title: "My Reservations"
- Element IDs:
  - reservations-page (div)
  - reservations-table (table)
  - cancel-reservation-button-{reservation_id} (button)
  - back-to-dashboard (button)
- Context Variables:
  - reservations (list of dicts) with reservation_id, book_title, reservation_date, status
- Navigation:
  - cancel-reservation-button-{{ reservation.reservation_id }} -> url_for('cancel_reservation', reservation_id=reservation.reservation_id)
  - back-to-dashboard -> url_for('dashboard_page')

### 7. my_reviews.html
- Path: templates/my_reviews.html
- Page Title: "My Reviews"
- Element IDs:
  - reviews-page (div)
  - reviews-list (div)
  - edit-review-button-{review_id} (button)
  - delete-review-button-{review_id} (button)
  - back-to-dashboard (button)
- Context Variables:
  - reviews (list of dicts) each with review_id, book_title, rating, review_text, review_date
- Navigation:
  - edit-review-button-{{ review.review_id }} -> url_for('edit_review', review_id=review.review_id)
  - delete-review-button-{{ review.review_id }} -> url_for('delete_review', review_id=review.review_id)
  - back-to-dashboard -> url_for('dashboard_page')

### 8. write_review.html
- Path: templates/write_review.html
- Page Title: "Write Review"
- Element IDs:
  - write-review-page (div)
  - book-info-display (div)
  - rating-input (dropdown/select)
  - review-text (textarea)
  - submit-review-button (button)
  - back-to-book (button)
- Context Variables:
  - book (dict)
  - existing_review (dict or None) with keys: rating (int), review_text (str)
- Navigation:
  - submit-review-button (form POST to current route)
  - back-to-book -> url_for('book_details', book_id=book.book_id)

### 9. profile.html
- Path: templates/profile.html
- Page Title: "My Profile"
- Element IDs:
  - profile-page (div)
  - profile-username (div)
  - profile-email (input)
  - update-profile-button (button)
  - borrow-history (div)
  - back-to-dashboard (button)
- Context Variables:
  - user (dict) with username (str), email (str), phone (str), address (str)
  - borrow_history (list of dicts) with book_title, borrow_date, return_date
- Navigation:
  - update-profile-button (form POST to current route)
  - back-to-dashboard -> url_for('dashboard_page')

### 10. payment_confirmation.html
- Path: templates/payment_confirmation.html
- Page Title: "Payment Confirmation"
- Element IDs:
  - payment-page (div)
  - fine-amount-display (div)
  - confirm-payment-button (button)
  - back-to-profile (button)
- Context Variables:
  - fine (dict) with fields: fine_id, username, borrow_id, amount, status, date_issued
- Navigation:
  - confirm-payment-button (form POST to current route)
  - back-to-profile -> url_for('user_profile')

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- Path: data/users.txt
- Fields (pipe-delimited): username|email|phone|address
- Description: Stores registered user details.
- Example Rows:
  - john_reader|john@example.com|555-1234|123 Main St
  - jane_doe|jane@example.com|555-5678|789 Oak St
- Notes: All fields are strings.

### 2. books.txt
- Path: data/books.txt
- Fields (pipe-delimited): book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating
- Description: Stores book information.
- Example Rows:
  - 1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  - 2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
- Notes:
  - book_id: int
  - year: int
  - avg_rating: float

### 3. borrowings.txt
- Path: data/borrowings.txt
- Fields (pipe-delimited): borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount
- Description: Tracks books borrowed by users.
- Example Rows:
  - 1|john_reader|2|2024-11-01|2024-11-15||Active|0
  - 2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
- Notes:
  - borrow_id, book_id: int
  - Dates format: YYYY-MM-DD
  - fine_amount: float
  - return_date may be empty string if not returned yet

### 4. reservations.txt
- Path: data/reservations.txt
- Fields (pipe-delimited): reservation_id|username|book_id|reservation_date|status
- Description: Stores user reservations of books.
- Example Rows:
  - 1|jane_doe|4|2024-11-10|Active
  - 2|john_reader|2|2024-10-25|Cancelled
- Notes:
  - reservation_id, book_id: int
  - reservation_date format: YYYY-MM-DD

### 5. reviews.txt
- Path: data/reviews.txt
- Fields (pipe-delimited): review_id|username|book_id|rating|review_text|review_date
- Description: Stores user reviews of books.
- Example Rows:
  - 1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  - 2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
- Notes:
  - review_id, book_id, rating: int
  - review_date format: YYYY-MM-DD

### 6. fines.txt
- Path: data/fines.txt
- Fields (pipe-delimited): fine_id|username|borrow_id|amount|status|date_issued
- Description: Tracks fines for overdue borrowings.
- Example Rows:
  - 1|john_reader|3|5.00|Unpaid|2024-10-30
- Notes:
  - fine_id, borrow_id: int
  - amount: float
  - date_issued format: YYYY-MM-DD

---

This completes the detailed design specification document for the 'OnlineLibrary' application to support backend and frontend parallel development with local text file data persistence.