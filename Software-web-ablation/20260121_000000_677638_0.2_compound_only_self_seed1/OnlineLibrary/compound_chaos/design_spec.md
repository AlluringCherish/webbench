# OnlineLibrary Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

### General Notes
- The root route `/` redirects to the dashboard page `/dashboard`.
- Each route corresponds to a key user action: browsing, borrowing, returning, reviewing, reservation management.
- HTTP methods use GET for page display and POST for state-changing operations.

| URL Path                            | Function Name          | HTTP Method(s) | Template Rendered           | Context Variables Passed to Template                                                  |
|-----------------------------------|------------------------|----------------|-----------------------------|---------------------------------------------------------------------------------------|
| `/`                               | `root_redirect`        | GET            | Redirect to `/dashboard`    | None                                                                                  |
| `/dashboard`                     | `dashboard_page`       | GET            | `dashboard.html`             | `username` (str), `featured_books` (List[Dict{book_id: int, title: str}])             |
| `/catalog`                       | `catalog_page`         | GET            | `catalog.html`               | `books` (List[Dict{book_id: int, title: str, author: str, status: str}])              |
| `/book/<int:book_id>`            | `book_details`         | GET            | `book_details.html`          | `book` (Dict{book_id: int, title: str, author: str, status: str, description: str, avg_rating: float}), `reviews` (List[Dict{review_id: int, username: str, rating: int, review_text: str, review_date: str}]) |
| `/borrow/<int:book_id>`          | `borrow_confirmation`  | GET, POST      | `borrow_confirmation.html`   | `book` (Dict{book_id: int, title: str, author: str}), `due_date` (str, YYYY-MM-DD)      |
| `/borrow/<int:book_id>/confirm`  | `confirm_borrow`       | POST           | `borrow_result.html`         | `success` (bool), `message` (str)                                                    |
| `/my_borrows`                   | `my_borrowings`        | GET            | `my_borrows.html`            | `username` (str), `borrows` (List[Dict{borrow_id: int, book_title: str, borrow_date: str, due_date: str, status: str}]) |
| `/return_borrow/<int:borrow_id>` | `return_borrow`        | POST           | `return_result.html`         | `success` (bool), `message` (str)                                                    |
| `/my_reservations`              | `my_reservations`      | GET            | `my_reservations.html`       | `username` (str), `reservations` (List[Dict{reservation_id: int, book_title: str, reservation_date: str, status: str}]) |
| `/cancel_reservation/<int:reservation_id>` | `cancel_reservation` | POST     | `cancel_reservation_result.html`| `success` (bool), `message` (str)                                                    |
| `/my_reviews`                  | `my_reviews`           | GET            | `my_reviews.html`            | `username` (str), `reviews` (List[Dict{review_id: int, book_title: str, rating: int, review_text: str, review_date: str}]) |
| `/write_review/<int:book_id>`   | `write_review`         | GET, POST      | `write_review.html`          | `book` (Dict{book_id: int, title: str, author: str}), `existing_review` (Dict or None with fields review_id:int, rating:int, review_text:str) |
| `/submit_review/<int:book_id>`  | `submit_review`        | POST           | `review_submit_result.html`  | `success` (bool), `message` (str)                                                    |
| `/profile`                    | `user_profile`         | GET            | `profile.html`               | `username` (str), `email` (str), `phone` (str), `address` (str), `borrow_history` (List[Dict{book_title: str, borrow_date: str, return_date: str or None}]) |
| `/update_profile`              | `update_profile`       | POST           | `profile_update_result.html` | `success` (bool), `message` (str)                                                    |
| `/payment/<int:fine_id>`       | `payment_confirmation` | GET            | `payment_confirmation.html`  | `fine_amount` (float), `fine_id` (int)                                               |
| `/confirm_payment/<int:fine_id>`| `confirm_payment`      | POST           | `payment_result.html`        | `success` (bool), `message` (str)                                                    |

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. dashboard.html (templates/dashboard.html)
- **Page Title (in <title> and <h1>):** "Library Dashboard"
- **Elements:**
  - `dashboard-page` (div)
  - `welcome-message` (h1) - displays username welcome message
  - `browse-books-button` (button) - navigates to Book Catalog
  - `my-borrows-button` (button) - navigates to My Borrowings
- **Context Variables:**
  - `username` (str)
  - `featured_books` (List[Dict{book_id: int, title: str}])
- **Navigation Mappings:**
  - `browse-books-button`: `url_for('catalog_page')`
  - `my-borrows-button`: `url_for('my_borrowings')`

### 2. catalog.html (templates/catalog.html)
- **Page Title:** "Book Catalog"
- **Elements:**
  - `catalog-page` (div)
  - `search-input` (input) - search by title or author
  - `book-grid` (div) - grid container for book cards
  - `view-book-button-{book_id}` (button) - dynamic id for each book; navigates to Book Details
  - `back-to-dashboard` (button) - navigates back to Dashboard
- **Context Variables:**
  - `books` (List[Dict{book_id: int, title: str, author: str, status: str}])
- **Navigation Mappings:**
  - `view-book-button-{book_id}`: `url_for('book_details', book_id=book_id)`
  - `back-to-dashboard`: `url_for('dashboard_page')`

### 3. book_details.html (templates/book_details.html)
- **Page Title:** "Book Details"
- **Elements:**
  - `book-details-page` (div)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div) - shows availability: Available, Borrowed, Reserved
  - `borrow-button` (button)
  - `reviews-section` (div) - list user reviews
  - `write-review-button` (button)
  - `back-to-catalog` (button)
- **Context Variables:**
  - `book` (Dict{book_id: int, title: str, author: str, status: str, description: str, avg_rating: float})
  - `reviews` (List[Dict{review_id: int, username: str, rating: int, review_text: str, review_date: str}])
- **Navigation Mappings:**
  - `borrow-button`: `url_for('borrow_confirmation', book_id=book.book_id)`
  - `write-review-button`: `url_for('write_review', book_id=book.book_id)`
  - `back-to-catalog`: `url_for('catalog_page')`

### 4. borrow_confirmation.html (templates/borrow_confirmation.html)
- **Page Title:** "Borrow Confirmation"
- **Elements:**
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button, within a POST form)
  - `cancel-borrow-button` (button)
- **Context Variables:**
  - `book` (Dict{book_id: int, title: str, author: str})
  - `due_date` (str, format YYYY-MM-DD)
- **Navigation Mappings:**
  - `confirm-borrow-button`: form action = `url_for('confirm_borrow', book_id=book.book_id)`, method="POST"
  - `cancel-borrow-button`: `url_for('book_details', book_id=book.book_id)`

### 5. my_borrows.html (templates/my_borrows.html)
- **Page Title:** "My Borrowings"
- **Elements:**
  - `my-borrows-page` (div)
  - `filter-status` (dropdown: All, Active, Returned, Overdue)
  - `borrows-table` (table)
  - `return-book-button-{borrow_id}` (button, dynamic id; each active borrow)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `username` (str)
  - `borrows` (List[Dict{borrow_id: int, book_title: str, borrow_date: str, due_date: str, status: str}])
- **Navigation Mappings:**
  - `return-book-button-{borrow_id}`: form POST action = `url_for('return_borrow', borrow_id=borrow_id)`
  - `back-to-dashboard`: `url_for('dashboard_page')`

### 6. my_reservations.html (templates/my_reservations.html)
- **Page Title:** "My Reservations"
- **Elements:**
  - `reservations-page` (div)
  - `reservations-table` (table)
  - `cancel-reservation-button-{reservation_id}` (button, dynamic id)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `username` (str)
  - `reservations` (List[Dict{reservation_id: int, book_title: str, reservation_date: str, status: str}])
- **Navigation Mappings:**
  - `cancel-reservation-button-{reservation_id}`: form POST action = `url_for('cancel_reservation', reservation_id=reservation_id)`
  - `back-to-dashboard`: `url_for('dashboard_page')`

### 7. my_reviews.html (templates/my_reviews.html)
- **Page Title:** "My Reviews"
- **Elements:**
  - `reviews-page` (div)
  - `reviews-list` (div)
  - `edit-review-button-{review_id}` (button, dynamic id)
  - `delete-review-button-{review_id}` (button, dynamic id)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `username` (str)
  - `reviews` (List[Dict{review_id: int, book_title: str, rating: int, review_text: str, review_date: str}])
- **Navigation Mappings:**
  - `edit-review-button-{review_id}`: `url_for('write_review', book_id=book_id)`  (book_id must be provided by backend with reviews data)
  - `delete-review-button-{review_id}`: form POST action = `url_for('delete_review', review_id=review_id)`
  - `back-to-dashboard`: `url_for('dashboard_page')`

### 8. write_review.html (templates/write_review.html)
- **Page Title:** "Write Review"
- **Elements:**
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown with options 1-5)
  - `review-text` (textarea)
  - `submit-review-button` (button within POST form)
  - `back-to-book` (button)
- **Context Variables:**
  - `book` (Dict{book_id: int, title: str, author: str})
  - `existing_review` (Dict or None with fields review_id, rating, review_text)
- **Navigation Mappings:**
  - `submit-review-button`: form POST action = `url_for('submit_review', book_id=book.book_id)`
  - `back-to-book`: `url_for('book_details', book_id=book.book_id)`

### 9. profile.html (templates/profile.html)
- **Page Title:** "My Profile"
- **Elements:**
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input, type="email")
  - `update-profile-button` (button within POST form)
  - `borrow-history` (div)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `username` (str)
  - `email` (str)
  - `phone` (str)
  - `address` (str)
  - `borrow_history` (List[Dict{book_title: str, borrow_date: str, return_date: str or None}])
- **Navigation Mappings:**
  - `update-profile-button`: form POST action = `url_for('update_profile')`
  - `back-to-dashboard`: `url_for('dashboard_page')`

### 10. payment_confirmation.html (templates/payment_confirmation.html)
- **Page Title:** "Payment Confirmation"
- **Elements:**
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button within POST form)
  - `back-to-profile` (button)
- **Context Variables:**
  - `fine_amount` (float)
  - `fine_id` (int)
- **Navigation Mappings:**
  - `confirm-payment-button`: form POST action = `url_for('confirm_payment', fine_id=fine_id)`
  - `back-to-profile`: `url_for('user_profile')`

---

## Section 3: Data File Schemas (Backend Development)

All files located inside the `data` directory.
Files are pipe (`|`) delimited without headers.

### 1. users.txt
- Path: `data/users.txt`
- Fields: `username|email|phone|address`
- Description: Stores user profile information.
- Example rows:
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`

### 2. books.txt
- Path: `data/books.txt`
- Fields: `book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating`
- Description: Stores details of all books.
- Example rows:
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  - `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`

### 3. borrowings.txt
- Path: `data/borrowings.txt`
- Fields: `borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount`
- Description: User borrow transaction records.
- Example rows:
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`

### 4. reservations.txt
- Path: `data/reservations.txt`
- Fields: `reservation_id|username|book_id|reservation_date|status`
- Description: Records for user reservations.
- Example rows:
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`

### 5. reviews.txt
- Path: `data/reviews.txt`
- Fields: `review_id|username|book_id|rating|review_text|review_date`
- Description: User reviews for books.
- Example rows:
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`

### 6. fines.txt
- Path: `data/fines.txt`
- Fields: `fine_id|username|borrow_id|amount|status|date_issued`
- Description: Overdue fine records.
- Example rows:
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`

### Parsing Notes
- Dates are in `YYYY-MM-DD` format.
- Empty fields (e.g., `return_date`) represent null values.
- Pipe delimiter `|` is strictly enforced. No header rows.
- Numeric fields (IDs, amounts) use proper types as described.

---

This completes the detailed design_spec.md for the OnlineLibrary application to enable parallel backend and frontend development aligning strictly with user requirements.