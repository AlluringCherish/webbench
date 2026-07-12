# OnlineLibrary Web Application - Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

| URL Path                 | Function Name           | HTTP Method(s) | Template Rendered        | Context Variables (Name : Type)                                      |
|--------------------------|-------------------------|----------------|--------------------------|----------------------------------------------------------------------|
| /                        | root_redirect            | GET            | Redirect to /dashboard   | None                                                                 |
| /dashboard               | dashboard                | GET            | dashboard.html           | username : str                                                      |
| /catalog                 | book_catalog             | GET            | catalog.html             | books : list of dicts (each dict: book_id:int, title:str, author:str, status:str) |
| /book/<int:book_id>      | book_details             | GET            | book_details.html        | book : dict (book_id:int, title:str, author:str, status:str, description:str, avg_rating:float), reviews : list of dicts (review_id:int, username:str, rating:int, review_text:str, review_date:str) |
| /borrow/<int:book_id>    | borrow_confirm           | GET            | borrow_confirmation.html | book : dict (book_id:int, title:str, author:str), due_date:str (YYYY-MM-DD) |
| /borrow/<int:book_id>/confirm | borrow_confirm_post      | POST           | borrow_confirmation.html | book : dict (book_id:int, title:str, author:str), due_date:str (YYYY-MM-DD), confirmation_status : str ('success' or 'cancelled') |
| /my-borrows              | my_borrowings            | GET            | my_borrowings.html       | borrows : list of dicts (borrow_id:int, book_title:str, borrow_date:str, due_date:str, status:str, fine_amount:float) |
| /return/<int:borrow_id>  | return_book              | POST           | return_confirmation.html | borrow : dict (borrow_id:int, book_title:str), return_status : str ('success' or 'failure') |
| /my-reservations         | my_reservations          | GET            | my_reservations.html     | reservations : list of dicts (reservation_id:int, book_title:str, reservation_date:str, status:str) |
| /cancel-reservation/<int:reservation_id> | cancel_reservation      | POST           | my_reservations.html     | reservations : list of dicts (as above), cancel_status : str ('success' or 'failure') |
| /my-reviews              | my_reviews               | GET            | my_reviews.html          | reviews : list of dicts (review_id:int, book_title:str, rating:int, review_text:str) |
| /review/write/<int:book_id> | write_review             | GET            | write_review.html        | book : dict (book_id:int, title:str, author:str), existing_review : dict or None (review_id:int, rating:int, review_text:str) |
| /review/submit/<int:book_id> | submit_review            | POST           | write_review.html        | submission_status : str ('success' or 'failure'), book : dict (book_id:int, title:str, author:str) |
| /review/edit/<int:review_id> | edit_review              | GET            | write_review.html        | review : dict (review_id:int, book_id:int, rating:int, review_text:str), book : dict (book_id:int, title:str, author:str) |
| /review/delete/<int:review_id> | delete_review            | POST           | my_reviews.html          | deletion_status : str ('success' or 'failure') |
| /profile                 | user_profile             | GET            | profile.html             | username : str, email : str, phone : str, address : str, borrow_history : list of dicts (book_title:str, borrow_date:str, return_date:str) |
| /profile/update          | update_profile           | POST           | profile.html             | update_status : str ('success' or 'failure'), username : str, email : str, phone : str, address : str |
| /payment/<int:fine_id>   | payment_confirmation     | GET            | payment_confirmation.html| fine : dict (fine_id:int, amount:float) |
| /payment/confirm/<int:fine_id> | confirm_payment          | POST           | payment_confirmation.html| payment_status : str ('success' or 'failure') |

Notes:
- The root '/' route redirects to the dashboard page.
- Borrowing and returning books involve confirm pages and POST actions.
- Reviews have separate routes for writing, editing, submitting, and deleting.
- Payment confirmation routes handle overdue fines.

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. dashboard.html
- **Path:** templates/dashboard.html
- **Page Title:** Library Dashboard
- **Element IDs:**
  - dashboard-page (div)
  - welcome-message (h1)
  - browse-books-button (button)
  - my-borrows-button (button)
- **Context Variables:**
  - username : str
- **Navigation:**
  - browse-books-button -> url_for('book_catalog')
  - my-borrows-button -> url_for('my_borrowings')

### 2. catalog.html
- **Path:** templates/catalog.html
- **Page Title:** Book Catalog
- **Element IDs:**
  - catalog-page (div)
  - search-input (input)
  - book-grid (div)
  - view-book-button-{book_id} (button) - dynamic per book_id: id="view-book-button-{{ book.book_id }}"
  - back-to-dashboard (button)
- **Context Variables:**
  - books : list of dicts each with fields: book_id:int, title:str, author:str, status:str
- **Navigation:**
  - view-book-button-{book_id} -> url_for('book_details', book_id=book.book_id)
  - back-to-dashboard -> url_for('dashboard')

### 3. book_details.html
- **Path:** templates/book_details.html
- **Page Title:** Book Details
- **Element IDs:**
  - book-details-page (div)
  - book-title (h1)
  - book-author (div)
  - book-status (div)
  - borrow-button (button)
  - reviews-section (div)
  - write-review-button (button)
  - back-to-catalog (button)
- **Context Variables:**
  - book : dict with fields (book_id:int, title:str, author:str, status:str, description:str, avg_rating:float)
  - reviews : list of dicts each with (review_id:int, username:str, rating:int, review_text:str, review_date:str)
- **Navigation:**
  - borrow-button -> url_for('borrow_confirm', book_id=book.book_id)
  - write-review-button -> url_for('write_review', book_id=book.book_id)
  - back-to-catalog -> url_for('book_catalog')

### 4. borrow_confirmation.html
- **Path:** templates/borrow_confirmation.html
- **Page Title:** Borrow Confirmation
- **Element IDs:**
  - borrow-page (div)
  - borrow-book-info (div)
  - due-date-display (div)
  - confirm-borrow-button (button)
  - cancel-borrow-button (button)
- **Context Variables:**
  - book : dict (book_id:int, title:str, author:str)
  - due_date : str (YYYY-MM-DD)
- **Form:**
  - POST form with action url_for('borrow_confirm_post', book_id=book.book_id)
- **Navigation:**
  - cancel-borrow-button -> url_for('book_details', book_id=book.book_id)

### 5. my_borrowings.html
- **Path:** templates/my_borrowings.html
- **Page Title:** My Borrowings
- **Element IDs:**
  - my-borrows-page (div)
  - filter-status (dropdown/select)
  - borrows-table (table)
  - return-book-button-{borrow_id} (button) - dynamic per borrow_id: id="return-book-button-{{ borrow.borrow_id }}"
  - back-to-dashboard (button)
- **Context Variables:**
  - borrows : list of dicts (borrow_id:int, book_title:str, borrow_date:str, due_date:str, status:str, fine_amount:float)
- **Form:**
  - POST form for return book action with appropriate borrow_id in route
- **Navigation:**
  - back-to-dashboard -> url_for('dashboard')

### 6. my_reservations.html
- **Path:** templates/my_reservations.html
- **Page Title:** My Reservations
- **Element IDs:**
  - reservations-page (div)
  - reservations-table (table)
  - cancel-reservation-button-{reservation_id} (button) - dynamic: id="cancel-reservation-button-{{ reservation.reservation_id }}"
  - back-to-dashboard (button)
- **Context Variables:**
  - reservations : list of dicts (reservation_id:int, book_title:str, reservation_date:str, status:str)
- **Form:**
  - POST form to cancel reservation with reservation_id in route
- **Navigation:**
  - back-to-dashboard -> url_for('dashboard')

### 7. my_reviews.html
- **Path:** templates/my_reviews.html
- **Page Title:** My Reviews
- **Element IDs:**
  - reviews-page (div)
  - reviews-list (div)
  - edit-review-button-{review_id} (button) - id="edit-review-button-{{ review.review_id }}"
  - delete-review-button-{review_id} (button) - id="delete-review-button-{{ review.review_id }}"
  - back-to-dashboard (button)
- **Context Variables:**
  - reviews : list of dicts (review_id:int, book_title:str, rating:int, review_text:str)
- **Form:**
  - POST form for deletion with review_id in route
- **Navigation:**
  - edit-review-button-{review_id} -> url_for('edit_review', review_id=review.review_id)
  - back-to-dashboard -> url_for('dashboard')

### 8. write_review.html
- **Path:** templates/write_review.html
- **Page Title:** Write Review
- **Element IDs:**
  - write-review-page (div)
  - book-info-display (div)
  - rating-input (dropdown/select)
  - review-text (textarea)
  - submit-review-button (button)
  - back-to-book (button)
- **Context Variables:**
  - book : dict (book_id:int, title:str, author:str)
  - existing_review : dict or None (review_id:int, rating:int, review_text:str)
- **Form:**
  - POST form to submit review: action url_for('submit_review', book_id=book.book_id)
- **Navigation:**
  - back-to-book -> url_for('book_details', book_id=book.book_id)

### 9. profile.html
- **Path:** templates/profile.html
- **Page Title:** My Profile
- **Element IDs:**
  - profile-page (div)
  - profile-username (div)
  - profile-email (input)
  - update-profile-button (button)
  - borrow-history (div)
  - back-to-dashboard (button)
- **Context Variables:**
  - username : str
  - email : str
  - phone : str
  - address : str
  - borrow_history : list of dicts (book_title:str, borrow_date:str, return_date:str)
- **Form:**
  - POST form for updating profile: action url_for('update_profile')
- **Navigation:**
  - back-to-dashboard -> url_for('dashboard')

### 10. payment_confirmation.html
- **Path:** templates/payment_confirmation.html
- **Page Title:** Payment Confirmation
- **Element IDs:**
  - payment-page (div)
  - fine-amount-display (div)
  - confirm-payment-button (button)
  - back-to-profile (button)
- **Context Variables:**
  - fine : dict (fine_id:int, amount:float)
- **Form:**
  - POST form to confirm payment: action url_for('confirm_payment', fine_id=fine.fine_id)
- **Navigation:**
  - back-to-profile -> url_for('user_profile')

---

## Section 3: Data File Schemas (Backend Development)

### 1. data/users.txt
- Path: data/users.txt
- Fields (pipe-delimited): username|email|phone|address
- Description: Stores user profiles including contact information.
- Example rows:
  - john_reader|john@example.com|555-1234|123 Main St
  - jane_doe|jane@example.com|555-5678|789 Oak St

### 2. data/books.txt
- Path: data/books.txt
- Fields (pipe-delimited): book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating
- Description: Stores all books with full metadata and availability.
- Example rows:
  - 1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  - 2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  - 3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  - 4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5
  - 5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3

### 3. data/borrowings.txt
- Path: data/borrowings.txt
- Fields (pipe-delimited): borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount
- Description: Records all borrow transactions, statuses, and related fine.
- Example rows:
  - 1|john_reader|2|2024-11-01|2024-11-15||Active|0
  - 2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  - 3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00

### 4. data/reservations.txt
- Path: data/reservations.txt
- Fields (pipe-delimited): reservation_id|username|book_id|reservation_date|status
- Description: User reservations for books with status tracking.
- Example rows:
  - 1|jane_doe|4|2024-11-10|Active
  - 2|john_reader|2|2024-10-25|Cancelled

### 5. data/reviews.txt
- Path: data/reviews.txt
- Fields (pipe-delimited): review_id|username|book_id|rating|review_text|review_date
- Description: Stores user reviews including stars and text.
- Example rows:
  - 1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  - 2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20

### 6. data/fines.txt
- Path: data/fines.txt
- Fields (pipe-delimited): fine_id|username|borrow_id|amount|status|date_issued
- Description: Tracks overdue fines issued and payment status.
- Example rows:
  - 1|john_reader|3|5.00|Unpaid|2024-10-30

---

*End of Design Specification Document for OnlineLibrary Application.*
