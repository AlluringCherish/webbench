# OnlineLibrary Web Application - Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

| URL Path                 | Function Name           | HTTP Method | Template Rendered         | Context Variables (name: type)                                         |
|--------------------------|-------------------------|-------------|---------------------------|----------------------------------------------------------------------|
| /                        | root_redirect           | GET         | None (redirect to dashboard) | None                                                                 |
| /dashboard               | dashboard               | GET         | dashboard.html             | username: str                                                         |
| /catalog                 | book_catalog            | GET         | catalog.html               | books: list of dict {
  book_id: int,
  title: str,
  author: str,
  status: str (Available/Borrowed/Reserved)
}                                                                       |
| /book/<int:book_id>      | book_details            | GET         | book_details.html          | book: dict {
  book_id: int,
  title: str,
  author: str,
  status: str (Available/Borrowed/Reserved),
  description: str,
  isbn: str,
  genre: str,
  publisher: str,
  year: int,
  avg_rating: float
}
reviews: list of dict {
  review_id: int,
  username: str,
  rating: int,
  review_text: str,
  review_date: str (YYYY-MM-DD)
}
username: str
|
| /borrow/<int:book_id>    | borrow_confirmation     | GET         | borrow_confirmation.html   | book: dict (same as /book/<book_id>)
due_date: str (YYYY-MM-DD)  # 14 days from current date
username: str
|
| /borrow/<int:book_id>/confirm | confirm_borrow       | POST        | borrow_confirmation.html   | message: str (success or failure info)
book_id: int
username: str
|
| /borrows                 | my_borrowings           | GET         | my_borrows.html            | borrows: list of dict {
  borrow_id: int,
  book_title: str,
  borrow_date: str (YYYY-MM-DD),
  due_date: str (YYYY-MM-DD),
  status: str (Active/Returned/Overdue)
}
username: str
|
| /borrow/return/<int:borrow_id> | return_book           | POST        | my_borrows.html            | message: str (confirmation or error)
username: str
|
| /reservations            | my_reservations         | GET         | my_reservations.html       | reservations: list of dict {
  reservation_id: int,
  book_title: str,
  reservation_date: str (YYYY-MM-DD),
  status: str (Active/Cancelled)
}
username: str
|
| /reservation/cancel/<int:reservation_id> | cancel_reservation     | POST        | my_reservations.html       | message: str
username: str
|
| /reviews                 | my_reviews              | GET         | my_reviews.html            | reviews: list of dict {
  review_id: int,
  book_title: str,
  rating: int,
  review_text: str
}
username: str
|
| /review/write/<int:book_id> | write_review          | GET         | write_review.html          | book: dict (same as /book/<book_id>)
existing_review: dict or None {
  review_id: int,
  rating: int,
  review_text: str
}
username: str
|
| /review/submit/<int:book_id> | submit_review         | POST        | write_review.html          | message: str
book_id: int
username: str
|
| /profile                 | user_profile            | GET         | profile.html               | username: str
email: str
borrow_history: list of dict {
  book_title: str,
  borrow_date: str (YYYY-MM-DD),
  return_date: str or None
}
|
| /profile/update          | update_profile          | POST        | profile.html               | message: str
username: str
|
| /payment/<int:fine_id>   | payment_confirmation    | GET         | payment_confirmation.html  | fine: dict {
  fine_id: int,
  amount: float,
  status: str
}
username: str
|
| /payment/confirm/<int:fine_id> | confirm_payment       | POST        | payment_confirmation.html  | message: str
username: str
|


---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. dashboard.html
- Path: templates/dashboard.html
- Page Title: Library Dashboard
- Element IDs:
  - dashboard-page (div)
  - welcome-message (h1)
  - browse-books-button (button)
  - my-borrows-button (button)
- Context Variables:
  - username: str
- Navigation:
  - browse-books-button -> url_for('book_catalog')
  - my-borrows-button -> url_for('my_borrowings')

### 2. catalog.html
- Path: templates/catalog.html
- Page Title: Book Catalog
- Element IDs:
  - catalog-page (div)
  - search-input (input)
  - book-grid (div)
  - back-to-dashboard (button)
  - Dynamic ID pattern: view-book-button-{book_id} (button) e.g. id="view-book-button-{{ book.book_id }}"
- Context Variables:
  - books: list of dict with keys: book_id (int), title (str), author (str), status (str)
- Navigation:
  - view-book-button-{book_id} -> url_for('book_details', book_id=book.book_id)
  - back-to-dashboard -> url_for('dashboard')

### 3. book_details.html
- Path: templates/book_details.html
- Page Title: Book Details
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
  - book: dict with keys as in Section 1 route /book/<int:book_id>
  - reviews: list of dict {review_id, username, rating, review_text, review_date}
- Navigation:
  - borrow-button -> url_for('borrow_confirmation', book_id=book.book_id)
  - write-review-button -> url_for('write_review', book_id=book.book_id)
  - back-to-catalog -> url_for('book_catalog')

### 4. borrow_confirmation.html
- Path: templates/borrow_confirmation.html
- Page Title: Borrow Confirmation
- Element IDs:
  - borrow-page (div)
  - borrow-book-info (div)
  - due-date-display (div)
  - confirm-borrow-button (button)
  - cancel-borrow-button (button)
- Context Variables:
  - book: dict
  - due_date: str
- Navigation:
  - confirm-borrow-button: form POST to url_for('confirm_borrow', book_id=book.book_id)
  - cancel-borrow-button -> url_for('book_details', book_id=book.book_id)

### 5. my_borrows.html
- Path: templates/my_borrows.html
- Page Title: My Borrowings
- Element IDs:
  - my-borrows-page (div)
  - filter-status (dropdown/select)
  - borrows-table (table)
  - back-to-dashboard (button)
  - Dynamic ID pattern: return-book-button-{borrow_id} (button) e.g. id="return-book-button-{{ borrow.borrow_id }}"
- Context Variables:
  - borrows: list of dict with keys: borrow_id (int), book_title (str), borrow_date (str), due_date (str), status (str)
- Navigation:
  - return-book-button-{borrow_id} -> form POST to url_for('return_book', borrow_id=borrow.borrow_id)
  - back-to-dashboard -> url_for('dashboard')

### 6. my_reservations.html
- Path: templates/my_reservations.html
- Page Title: My Reservations
- Element IDs:
  - reservations-page (div)
  - reservations-table (table)
  - back-to-dashboard (button)
  - Dynamic ID pattern: cancel-reservation-button-{reservation_id} (button) e.g. id="cancel-reservation-button-{{ reservation.reservation_id }}"
- Context Variables:
  - reservations: list of dict with keys: reservation_id (int), book_title (str), reservation_date (str), status (str)
- Navigation:
  - cancel-reservation-button-{reservation_id} -> form POST to url_for('cancel_reservation', reservation_id=reservation.reservation_id)
  - back-to-dashboard -> url_for('dashboard')

### 7. my_reviews.html
- Path: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs:
  - reviews-page (div)
  - reviews-list (div)
  - back-to-dashboard (button)
  - Dynamic ID patterns:
    - edit-review-button-{review_id} (button) id="edit-review-button-{{ review.review_id }}"
    - delete-review-button-{review_id} (button) id="delete-review-button-{{ review.review_id }}"
- Context Variables:
  - reviews: list of dict with keys: review_id (int), book_title (str), rating (int), review_text (str)
- Navigation:
  - edit-review-button-{review_id} -> url_for('write_review', book_id=review.book_id) (book_id must be passed or retrieved)
  - delete-review-button-{review_id} -> form POST to delete route (not specified exactly), assume url_for('delete_review', review_id=review.review_id)
  - back-to-dashboard -> url_for('dashboard')

### 8. write_review.html
- Path: templates/write_review.html
- Page Title: Write Review
- Element IDs:
  - write-review-page (div)
  - book-info-display (div)
  - rating-input (dropdown)
  - review-text (textarea)
  - submit-review-button (button)
  - back-to-book (button)
- Context Variables:
  - book: dict
  - existing_review: dict or None with keys: review_id, rating, review_text
- Navigation:
  - submit-review-button: form POST to url_for('submit_review', book_id=book.book_id)
  - back-to-book -> url_for('book_details', book_id=book.book_id)

### 9. profile.html
- Path: templates/profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (div)
  - profile-username (div)
  - profile-email (input)
  - update-profile-button (button)
  - borrow-history (div)
  - back-to-dashboard (button)
- Context Variables:
  - username: str
  - email: str
  - borrow_history: list of dict with keys: book_title (str), borrow_date (str), return_date (str or None)
- Navigation:
  - update-profile-button: form POST to url_for('update_profile')
  - back-to-dashboard -> url_for('dashboard')

### 10. payment_confirmation.html
- Path: templates/payment_confirmation.html
- Page Title: Payment Confirmation
- Element IDs:
  - payment-page (div)
  - fine-amount-display (div)
  - confirm-payment-button (button)
  - back-to-profile (button)
- Context Variables:
  - fine: dict with keys: fine_id (int), amount (float), status (str)
- Navigation:
  - confirm-payment-button: form POST to url_for('confirm_payment', fine_id=fine.fine_id)
  - back-to-profile -> url_for('user_profile')


---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- Path: data/users.txt
- Fields (pipe-delimited):
  1. username (str)
  2. email (str)
  3. phone (str)
  4. address (str)
- Description: Stores registered user information.
- Example Rows:
  - john_reader|john@example.com|555-1234|123 Main St
  - jane_doe|jane@example.com|555-5678|789 Oak St

### 2. books.txt
- Path: data/books.txt
- Fields (pipe-delimited):
  1. book_id (int)
  2. title (str)
  3. author (str)
  4. isbn (str)
  5. genre (str)
  6. publisher (str)
  7. year (int)
  8. description (str)
  9. status (str) - values: Available, Borrowed, Reserved
  10. avg_rating (float)
- Description: Stores book details and current availability.
- Example Rows:
  - 1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  - 2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6

### 3. borrowings.txt
- Path: data/borrowings.txt
- Fields (pipe-delimited):
  1. borrow_id (int)
  2. username (str)
  3. book_id (int)
  4. borrow_date (str, YYYY-MM-DD)
  5. due_date (str, YYYY-MM-DD)
  6. return_date (str or empty, YYYY-MM-DD)
  7. status (str) - values: Active, Returned, Overdue
  8. fine_amount (float)
- Description: Records all borrow transactions and return statuses.
- Example Rows:
  - 1|john_reader|2|2024-11-01|2024-11-15||Active|0
  - 2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0

### 4. reservations.txt
- Path: data/reservations.txt
- Fields (pipe-delimited):
  1. reservation_id (int)
  2. username (str)
  3. book_id (int)
  4. reservation_date (str, YYYY-MM-DD)
  5. status (str) - values: Active, Cancelled
- Description: Stores all book reservations made by users.
- Example Rows:
  - 1|jane_doe|4|2024-11-10|Active
  - 2|john_reader|2|2024-10-25|Cancelled

### 5. reviews.txt
- Path: data/reviews.txt
- Fields (pipe-delimited):
  1. review_id (int)
  2. username (str)
  3. book_id (int)
  4. rating (int, 1-5)
  5. review_text (str)
  6. review_date (str, YYYY-MM-DD)
- Description: Stores user-written reviews for books.
- Example Rows:
  - 1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  - 2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20

### 6. fines.txt
- Path: data/fines.txt
- Fields (pipe-delimited):
  1. fine_id (int)
  2. username (str)
  3. borrow_id (int)
  4. amount (float)
  5. status (str) - values: Unpaid, Paid
  6. date_issued (str, YYYY-MM-DD)
- Description: Records fines charged to users for overdue books.
- Example Rows:
  - 1|john_reader|3|5.00|Unpaid|2024-10-30

---

This completes the comprehensive design specification document required to independently develop the backend and frontend components of the OnlineLibrary application using Flask and local text file data management.