# OnlineLibrary Web Application - Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

| URL Path                 | Function Name           | HTTP Method(s) | Template Rendered        | Context Variables (Name : Type)                                      |
|--------------------------|-------------------------|----------------|--------------------------|----------------------------------------------------------------------|
| /                        | root_redirect            | GET            | Redirect to /dashboard   | None (redirect)                                                      |
| /dashboard               | dashboard               | GET            | dashboard.html           | username: str, featured_books: list of dict (each dict: book_id:int, title:str, author:str, status:str) |
| /catalog                 | book_catalog            | GET            | catalog.html             | books: list of dict (each dict: book_id:int, title:str, author:str, status:str), query: str (optional) |
| /book/<int:book_id>      | book_details            | GET            | book_details.html        | book: dict (book_id:int, title:str, author:str, isbn:str, genre:str, publisher:str, year:int, description:str, status:str, avg_rating:float),
                                                     reviews: list of dict (review_id:int, username:str, rating:int, review_text:str, review_date:str) |
| /borrow/<int:book_id>    | borrow_book             | GET, POST     | borrow_confirmation.html | book: dict (book_id:int, title:str, author:str), due_date: str (YYYY-MM-DD) (For GET to show page),
                                                     username: str (from session),
                                                     borrow_success: bool (POST result),
                                                     error_message: str (optional for POST errors) |
| /my-borrows              | my_borrowings           | GET            | my_borrowings.html       | borrows: list of dict (borrow_id:int, book_id:int, title:str, borrow_date:str, due_date:str, status:str), filter_status: str |
| /return/<int:borrow_id>  | return_book             | GET, POST     | return_confirmation.html | borrow: dict (borrow_id:int, book_id:int, title:str, borrow_date:str, due_date:str, status:str),
                                                      return_success: bool (POST result),
                                                      error_message: str (optional for POST errors) |
| /my-reservations         | my_reservations         | GET            | my_reservations.html     | reservations: list of dict (reservation_id:int, book_id:int, title:str, reservation_date:str, status:str) |
| /cancel-reservation/<int:reservation_id> | cancel_reservation | POST           | Redirect to /my-reservations after action | None or flash message (handled internally)                             |
| /my-reviews              | my_reviews              | GET            | my_reviews.html          | reviews: list of dict (review_id:int, book_id:int, title:str, rating:int, review_text:str) |
| /write-review/<int:book_id> | write_review          | GET, POST     | write_review.html        | book: dict (book_id:int, title:str),
                                          existing_review: dict (review_id:int, rating:int, review_text:str) or None,
                                          submit_success: bool (POST result),
                                          error_message: str (optional for POST) |
| /edit-review/<int:review_id> | edit_review          | GET, POST     | write_review.html        | review: dict (review_id:int, book_id:int, rating:int, review_text:str),
                                              book: dict (book_id:int, title:str),
                                              submit_success: bool (POST result),
                                              error_message: str (optional for POST) |
| /delete-review/<int:review_id> | delete_review      | POST           | Redirect to /my-reviews  | None (handled internally)                                             |
| /profile                 | user_profile            | GET, POST     | profile.html             | user: dict (username:str, email:str, phone:str, address:str),
                                      borrow_history: list of dict (book_id:int, title:str, borrow_date:str, return_date:str) |
| /payment/<int:fine_id>   | payment_confirmation    | GET, POST     | payment_confirmation.html| fine: dict (fine_id:int, amount:float, status:str), payment_success: bool (POST result), error_message: str (optional) |

**Notes:**
- Root path `/` permanently redirects to `/dashboard`, the starting page.
- Borrowing flow: GET `/borrow/<book_id>` shows confirmation; POST to same URL confirms borrow.
- Returning flow: GET `/return/<borrow_id>` shows confirmation; POST to same URL confirms return.
- Deleting and cancelling actions implemented as POST routes redirecting back.

---

## Section 2: HTML Template Specifications (Frontend Development)

Each template file is stored under `templates/` directory.

### 1. dashboard.html
- Title and H1: "Library Dashboard"
- Element IDs:
  - dashboard-page (div)
  - welcome-message (h1)
  - browse-books-button (button)
  - my-borrows-button (button)
- Context Variables:
  - username: str
  - featured_books: list of dict (book_id:int, title:str, author:str, status:str)
- Navigation:
  - `browse-books-button`: url_for('book_catalog')
  - `my-borrows-button`: url_for('my_borrowings')

### 2. catalog.html
- Title and H1: "Book Catalog"
- Element IDs:
  - catalog-page (div)
  - search-input (input)
  - book-grid (div)
  - back-to-dashboard (button)
  - view-book-button-{book_id} (button) for each book card
- Context Variables:
  - books: list of dict (book_id:int, title:str, author:str, status:str)
  - query: str (optional)
- Navigation:
  - back-to-dashboard: url_for('dashboard')
  - view-book-button-{book_id}: url_for('book_details', book_id=book.book_id)

### 3. book_details.html
- Title and H1: "Book Details"
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
  - book: dict (book_id:int, title:str, author:str, isbn:str, genre:str, publisher:str, year:int, description:str, status:str, avg_rating:float)
  - reviews: list of dict (review_id:int, username:str, rating:int, review_text:str, review_date:str)
- Navigation:
  - borrow-button: url_for('borrow_book', book_id=book.book_id)
  - write-review-button: url_for('write_review', book_id=book.book_id)
  - back-to-catalog: url_for('book_catalog')

### 4. borrow_confirmation.html
- Title and H1: "Borrow Confirmation"
- Element IDs:
  - borrow-page (div)
  - borrow-book-info (div)
  - due-date-display (div)
  - confirm-borrow-button (button)
  - cancel-borrow-button (button)
- Context Variables:
  - book: dict (book_id:int, title:str, author:str)
  - due_date: str (YYYY-MM-DD)
- Navigation:
  - confirm-borrow-button: POST form to url_for('borrow_book', book_id=book.book_id)
  - cancel-borrow-button: url_for('book_details', book_id=book.book_id)

### 5. my_borrowings.html
- Title and H1: "My Borrowings"
- Element IDs:
  - my-borrows-page (div)
  - filter-status (dropdown)
  - borrows-table (table)
  - back-to-dashboard (button)
  - return-book-button-{borrow_id} (button) for each active borrow
- Context Variables:
  - borrows: list of dict (borrow_id:int, book_id:int, title:str, borrow_date:str, due_date:str, status:str)
  - filter_status: str
- Navigation:
  - back-to-dashboard: url_for('dashboard')
  - return-book-button-{borrow_id}: POST form to url_for('return_book', borrow_id=borrow.borrow_id)

### 6. my_reservations.html
- Title and H1: "My Reservations"
- Element IDs:
  - reservations-page (div)
  - reservations-table (table)
  - back-to-dashboard (button)
  - cancel-reservation-button-{reservation_id} (button) for each reservation
- Context Variables:
  - reservations: list of dict (reservation_id:int, book_id:int, title:str, reservation_date:str, status:str)
- Navigation:
  - back-to-dashboard: url_for('dashboard')
  - cancel-reservation-button-{reservation_id}: POST form to url_for('cancel_reservation', reservation_id=reservation.reservation_id)

### 7. my_reviews.html
- Title and H1: "My Reviews"
- Element IDs:
  - reviews-page (div)
  - reviews-list (div)
  - back-to-dashboard (button)
  - edit-review-button-{review_id} (button) for each review
  - delete-review-button-{review_id} (button) for each review
- Context Variables:
  - reviews: list of dict (review_id:int, book_id:int, title:str, rating:int, review_text:str)
- Navigation:
  - back-to-dashboard: url_for('dashboard')
  - edit-review-button-{review_id}: url_for('edit_review', review_id=review.review_id)
  - delete-review-button-{review_id}: POST form to url_for('delete_review', review_id=review.review_id)

### 8. write_review.html
- Title and H1: "Write Review"
- Element IDs:
  - write-review-page (div)
  - book-info-display (div)
  - rating-input (dropdown)
  - review-text (textarea)
  - submit-review-button (button)
  - back-to-book (button)
- Context Variables:
  - book: dict (book_id:int, title:str)
  - existing_review: dict (review_id:int, rating:int, review_text:str) or None
- Navigation:
  - submit-review-button: POST form to url_for('write_review', book_id=book.book_id)
  - back-to-book: url_for('book_details', book_id=book.book_id)

### 9. profile.html
- Title and H1: "My Profile"
- Element IDs:
  - profile-page (div)
  - profile-username (div)
  - profile-email (input)
  - update-profile-button (button)
  - borrow-history (div)
  - back-to-dashboard (button)
- Context Variables:
  - user: dict (username:str, email:str, phone:str, address:str)
  - borrow_history: list of dict (book_id:int, title:str, borrow_date:str, return_date:str)
- Navigation:
  - update-profile-button: POST form to url_for('user_profile')
  - back-to-dashboard: url_for('dashboard')

### 10. payment_confirmation.html
- Title and H1: "Payment Confirmation"
- Element IDs:
  - payment-page (div)
  - fine-amount-display (div)
  - confirm-payment-button (button)
  - back-to-profile (button)
- Context Variables:
  - fine: dict (fine_id:int, amount:float, status:str)
- Navigation:
  - confirm-payment-button: POST form to url_for('payment_confirmation', fine_id=fine.fine_id)
  - back-to-profile: url_for('user_profile')

---

## Section 3: Data File Schemas (Backend Development)

All data files are stored in `data/` directory with strict pipe (`|`) delimited format and no header line.

### 1. users.txt
- Path: data/users.txt
- Fields (in order): username | email | phone | address
- Description: Stores user account information.
- Example rows:
  - john_reader|john@example.com|555-1234|123 Main St
  - jane_doe|jane@example.com|555-5678|789 Oak St

### 2. books.txt
- Path: data/books.txt
- Fields (in order): book_id | title | author | isbn | genre | publisher | year | description | status | avg_rating
- Description: Stores book information and current status.
- Field Types:
  - book_id: int
  - year: int
  - avg_rating: float
- Example rows:
  - 1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  - 2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  - 3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  - 4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5
  - 5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3

### 3. borrowings.txt
- Path: data/borrowings.txt
- Fields (in order): borrow_id | username | book_id | borrow_date | due_date | return_date | status | fine_amount
- Description: Records borrowing transactions and status.
- Field Types:
  - borrow_id: int
  - book_id: int
  - fine_amount: float
- Example rows:
  - 1|john_reader|2|2024-11-01|2024-11-15||Active|0
  - 2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  - 3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00

### 4. reservations.txt
- Path: data/reservations.txt
- Fields (in order): reservation_id | username | book_id | reservation_date | status
- Description: Stores book reservation details.
- Field Types:
  - reservation_id: int
  - book_id: int
- Example rows:
  - 1|jane_doe|4|2024-11-10|Active
  - 2|john_reader|2|2024-10-25|Cancelled

### 5. reviews.txt
- Path: data/reviews.txt
- Fields (in order): review_id | username | book_id | rating | review_text | review_date
- Description: Contains user reviews for books.
- Field Types:
  - review_id: int
  - rating: int
- Example rows:
  - 1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  - 2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20

### 6. fines.txt
- Path: data/fines.txt
- Fields (in order): fine_id | username | borrow_id | amount | status | date_issued
- Description: Tracks fines for overdue returns.
- Field Types:
  - fine_id: int
  - borrow_id: int
  - amount: float
- Example rows:
  - 1|john_reader|3|5.00|Unpaid|2024-10-30

---

This specification document provides a complete mapping of Flask routes, frontend templates, and backend data schemas to support independent parallel development for the OnlineLibrary application.
