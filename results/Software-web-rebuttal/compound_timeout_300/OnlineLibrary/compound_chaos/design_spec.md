# OnlineLibrary Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

| URL Path                     | Function Name            | HTTP Method(s) | Template Rendered          | Context Variables Passed to Template                       |
|------------------------------|-------------------------|----------------|----------------------------|------------------------------------------------------------|
| `/`                          | `root_redirect`          | GET            | Redirects to `/dashboard`  | None                                                     |
| `/dashboard`                 | `dashboard`             | GET            | `dashboard.html`            | `username` (str)                                         |
| `/catalog`                   | `book_catalog`          | GET            | `catalog.html`              | `books` (list of dicts) where each dict contains:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str: "Available", "Borrowed", "Reserved") |
| `/book/<int:book_id>`        | `book_details`          | GET            | `book_details.html`         | `book` (dict):
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
    - `description` (str)
    - `avg_rating` (float)
  `reviews` (list of dicts):
    - `review_id` (int)
    - `username` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str) |
| `/borrow/<int:book_id>`      | `borrow_confirmation`   | GET            | `borrow_confirmation.html` | `book` (dict):
    - `book_id` (int)
    - `title` (str)
  `due_date` (str, e.g., "YYYY-MM-DD")                             |
| `/borrow/confirm`            | `confirm_borrow`        | POST           | Redirect (after processing) | None                                                     |
| `/borrows`                   | `my_borrowings`         | GET            | `my_borrowings.html`        | `borrows` (list of dicts) where each dict contains:
    - `borrow_id` (int)
    - `title` (str)
    - `borrow_date` (str)
    - `due_date` (str)
    - `status` (str: "Active", "Returned", "Overdue")
    - `fine_amount` (float)                                      |
| `/return/<int:borrow_id>`    | `return_book`           | POST           | Redirect (after processing) | None                                                     |
| `/reservations`              | `my_reservations`       | GET            | `my_reservations.html`      | `reservations` (list of dicts):
    - `reservation_id` (int)
    - `title` (str)
    - `reservation_date` (str)
    - `status` (str)                                            |
| `/reservation/cancel/<int:reservation_id>` | `cancel_reservation`| POST           | Redirect (after processing) | None                                                     |
| `/reviews`                   | `my_reviews`            | GET            | `my_reviews.html`           | `reviews` (list of dicts):
    - `review_id` (int)
    - `book_title` (str)
    - `rating` (int)
    - `review_text` (str)                                     |
| `/review/write/<int:book_id>`| `write_review`          | GET            | `write_review.html`         | `book` (dict):
    - `book_id` (int)
    - `title` (str)                                            |
| `/review/submit`             | `submit_review`         | POST           | Redirect (after processing) | None                                                     |
| `/review/edit/<int:review_id>` | `edit_review`        | GET            | `write_review.html`         | `book` (dict):
    - `book_id` (int)
    - `title` (str)
  `review` (dict):
    - `review_id` (int)
    - `rating` (int)
    - `review_text` (str)                                    |
| `/review/delete/<int:review_id>` | `delete_review`      | POST           | Redirect (after processing) | None                                                     |
| `/profile`                  | `user_profile`          | GET            | `profile.html`              | `username` (str)
  `email` (str)
  `borrow_history` (list of dicts):
    - `book_title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)                               |
| `/profile/update`           | `update_profile`        | POST           | Redirect (after processing) | None                                                     |
| `/payment/<int:fine_id>`     | `payment_confirmation`  | GET            | `payment_confirmation.html` | `fine` (dict):
    - `fine_id` (int)
    - `amount` (float)                                       |
| `/payment/confirm/<int:fine_id>` | `confirm_payment`  | POST           | Redirect (after processing) | None                                                     |

**Notes:**
- Redirect routes after POST operations ensure proper flow.
- Complex data types like lists of dictionaries are fully detailed.

---

## Section 2: HTML Template Specification (Frontend Development)

### 1. `templates/dashboard.html`
- **Page Title**: Library Dashboard
- **Element IDs:**
  - `dashboard-page` (div)
  - `welcome-message` (h1) - Displays "Welcome, {{ username }}"
  - `browse-books-button` (button) - Navigates to catalog page
  - `my-borrows-button` (button) - Navigates to my borrowings
- **Context Variables:**
  - `username` (str)
- **Navigation (`url_for`)**:
  - `browse-books-button`: url_for('book_catalog')
  - `my-borrows-button`: url_for('my_borrowings')

### 2. `templates/catalog.html`
- **Page Title**: Book Catalog
- **Element IDs:**
  - `catalog-page` (div)
  - `search-input` (input, text)
  - `book-grid` (div) - contains multiple book cards
  - `view-book-button-{{ book.book_id }}` (button) per book card
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `books` (list of dict): Each dict has keys `book_id`, `title`, `author`, `status`
- **Navigation (`url_for`)**:
  - Each `view-book-button-{{ book.book_id }}`: url_for('book_details', book_id=book.book_id)
  - `back-to-dashboard`: url_for('dashboard')

### 3. `templates/book_details.html`
- **Page Title**: Book Details
- **Element IDs:**
  - `book-details-page` (div)
  - `book-title` (h1) displaying `book.title`
  - `book-author` (div) displaying `book.author`
  - `book-status` (div) displaying `book.status`
  - `borrow-button` (button) to borrow the book
  - `reviews-section` (div) containing list of reviews
  - `write-review-button` (button) to write review
  - `back-to-catalog` (button) to catalog
- **Context Variables:**
  - `book` (dict): keys as in Section 1
  - `reviews` (list of dicts): each with keys `review_id`, `username`, `rating`, `review_text`, `review_date`
- **Navigation (`url_for`)**:
  - `borrow-button`: url_for('borrow_confirmation', book_id=book.book_id)
  - `write-review-button`: url_for('write_review', book_id=book.book_id)
  - `back-to-catalog`: url_for('book_catalog')

### 4. `templates/borrow_confirmation.html`
- **Page Title**: Borrow Confirmation
- **Element IDs:**
  - `borrow-page` (div)
  - `borrow-book-info` (div) displays book title
  - `due-date-display` (div) displays due date string
  - `confirm-borrow-button` (button) to submit form
  - `cancel-borrow-button` (button) to cancel
- **Context Variables:**
  - `book` (dict): keys `book_id`, `title`
  - `due_date` (str)
- **Form:**
  - Method: POST
  - Action: url_for('confirm_borrow')
- **Navigation (`url_for`)**:
  - `cancel-borrow-button`: url_for('book_details', book_id=book.book_id)

### 5. `templates/my_borrowings.html`
- **Page Title**: My Borrowings
- **Element IDs:**
  - `my-borrows-page` (div)
  - `filter-status` (dropdown/select) with options ["All", "Active", "Returned", "Overdue"]
  - `borrows-table` (table) with columns: Title, Borrow Date, Due Date, Status, Fine Amount, Return Button
  - `return-book-button-{{ borrow.borrow_id }}` (button) for each active borrow
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `borrows` (list of dicts) keys: `borrow_id`, `title`, `borrow_date`, `due_date`, `status`, `fine_amount`
- **Form for returning book:**
  - Method: POST
  - Action: url_for('return_book', borrow_id=borrow.borrow_id)
- **Navigation (`url_for`)**:
  - `back-to-dashboard`: url_for('dashboard')

### 6. `templates/my_reservations.html`
- **Page Title**: My Reservations
- **Element IDs:**
  - `reservations-page` (div)
  - `reservations-table` (table) with columns: Title, Reservation Date, Status, Cancel Button
  - `cancel-reservation-button-{{ reservation.reservation_id }}` (button) per reservation
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `reservations` (list of dicts) keys: `reservation_id`, `title`, `reservation_date`, `status`
- **Form for cancelling reservation:**
  - Method: POST
  - Action: url_for('cancel_reservation', reservation_id=reservation.reservation_id)
- **Navigation (`url_for`)**:
  - `back-to-dashboard`: url_for('dashboard')

### 7. `templates/my_reviews.html`
- **Page Title**: My Reviews
- **Element IDs:**
  - `reviews-page` (div)
  - `reviews-list` (div) listing reviews with book title, rating, and review text
  - `edit-review-button-{{ review.review_id }}` (button)
  - `delete-review-button-{{ review.review_id }}` (button)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `reviews` (list of dicts) keys: `review_id`, `book_title`, `rating`, `review_text`
- **Form for deleting review:**
  - Method: POST
  - Action: url_for('delete_review', review_id=review.review_id)
- **Navigation (`url_for`)**:
  - `edit-review-button-{{ review.review_id }}`: url_for('edit_review', review_id=review.review_id)
  - `back-to-dashboard`: url_for('dashboard')

### 8. `templates/write_review.html`
- **Page Title**: Write Review
- **Element IDs:**
  - `write-review-page` (div)
  - `book-info-display` (div) shows book title
  - `rating-input` (dropdown/select) options 1-5 stars
  - `review-text` (textarea)
  - `submit-review-button` (button) to submit
  - `back-to-book` (button)
- **Context Variables:**
  - When writing new review:
    - `book` (dict): `book_id`, `title`
  - When editing review:
    - `book` (dict): `book_id`, `title`
    - `review` (dict): `review_id`, `rating`, `review_text`
- **Form:**
  - Method: POST
  - Action: url_for('submit_review')
- **Navigation (`url_for`)**:
  - `back-to-book`: url_for('book_details', book_id=book.book_id)

### 9. `templates/profile.html`
- **Page Title**: My Profile
- **Element IDs:**
  - `profile-page` (div)
  - `profile-username` (div) displays username (readonly)
  - `profile-email` (input, email)
  - `update-profile-button` (button)
  - `borrow-history` (div) lists past borrows with book titles and dates
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dicts) with keys:
    - `book_title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)
- **Form:**
  - Method: POST
  - Action: url_for('update_profile')
- **Navigation (`url_for`)**:
  - `back-to-dashboard`: url_for('dashboard')

### 10. `templates/payment_confirmation.html`
- **Page Title**: Payment Confirmation
- **Element IDs:**
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- **Context Variables:**
  - `fine` (dict) containing:
    - `fine_id` (int)
    - `amount` (float)
- **Form:**
  - Method: POST
  - Action: url_for('confirm_payment', fine_id=fine.fine_id)
- **Navigation (`url_for`)**:
  - `back-to-profile`: url_for('user_profile')

---

## Section 3: Data File Schemas (Backend Development)

### 1. `data/users.txt`
- **File Path:** `data/users.txt`
- **Field Order:** `username|email|phone|address`
- **Description:** Stores user account information.
- **Example Rows:**
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`
- **Notes:** No header line. All fields are strings.

### 2. `data/books.txt`
- **File Path:** `data/books.txt`
- **Field Order:**
```
book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating
```
- **Description:** Stores all books details including status and average rating.
- **Example Rows:**
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  - `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`
- **Notes:**
  - `book_id` is int.
  - `year` is int.
  - `avg_rating` is float.
  - Others are strings.

### 3. `data/borrowings.txt`
- **File Path:** `data/borrowings.txt`
- **Field Order:**
```
borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount
```
- **Description:** Records borrow transactions with status and fines.
- **Example Rows:**
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`
- **Notes:**
  - `borrow_id`, `book_id` are int.
  - `fine_amount` is float.
  - Date fields are strings (YYYY-MM-DD).
  - `return_date` may be empty string if not returned.

### 4. `data/reservations.txt`
- **File Path:** `data/reservations.txt`
- **Field Order:**
```
reservation_id|username|book_id|reservation_date|status
```
- **Description:** Stores book reservation information.
- **Example Rows:**
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`
- **Notes:**
  - `reservation_id`, `book_id` are int.
  - Dates as strings.

### 5. `data/reviews.txt`
- **File Path:** `data/reviews.txt`
- **Field Order:**
```
review_id|username|book_id|rating|review_text|review_date
```
- **Description:** Stores reviews made by users on books.
- **Example Rows:**
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`
- **Notes:**
  - `review_id`, `book_id`, `rating` are int.
  - `review_text` may contain spaces and punctuation.
  - Dates as strings.

### 6. `data/fines.txt`
- **File Path:** `data/fines.txt`
- **Field Order:**
```
fine_id|username|borrow_id|amount|status|date_issued
```
- **Description:** Records fines issued for overdue returns.
- **Example Rows:**
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`
- **Notes:**
  - `fine_id`, `borrow_id` are int.
  - `amount` is float.
  - Dates as strings.

---

*End of Design Specification for OnlineLibrary*