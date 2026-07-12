# OnlineLibrary Web Application - Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

| URL Path                 | Function Name           | HTTP Method(s) | Template Rendered        | Context Variables (Name : Type)                                      |
|--------------------------|-------------------------|----------------|--------------------------|----------------------------------------------------------------------|
| /                        | root_redirect            | GET            | Redirect to /dashboard   | None (redirect)                                                      |
| /dashboard               | dashboard_page           | GET            | dashboard.html           | username: str                                                        |
| /catalog                 | book_catalog_page        | GET            | catalog.html             | books: list[dict]                                                    |
| /book/<int:book_id>      | book_details_page        | GET            | book_details.html        | book: dict, reviews: list[dict], user_has_borrowed: bool            |
| /borrow/<int:book_id>    | borrow_confirmation_page | GET            | borrow_confirmation.html | book: dict, due_date: str                                            |
| /borrow/confirm          | confirm_borrow_book      | POST           | borrow_result.html       | success: bool, message: str                                          |
| /my-borrows              | my_borrowings_page       | GET            | my_borrows.html          | borrows: list[dict]                                                 |
| /return/<int:borrow_id>  | return_borrowed_book     | POST           | return_result.html       | success: bool, message: str                                          |
| /my-reservations         | my_reservations_page     | GET            | my_reservations.html     | reservations: list[dict]                                            |
| /cancel-reservation/<int:reservation_id> | cancel_reservation      | POST           | cancel_reservation_result.html | success: bool, message: str                                          |
| /my-reviews              | my_reviews_page          | GET            | my_reviews.html          | reviews: list[dict]                                                 |
| /review/write/<int:book_id> | write_review_page      | GET            | write_review.html        | book: dict, existing_review: dict or None                           |
| /review/submit           | submit_review            | POST           | review_submission_result.html | success: bool, message: str                                          |
| /review/edit/<int:review_id> | edit_review_page       | GET            | write_review.html        | book: dict, existing_review: dict                                   |
| /review/delete/<int:review_id> | delete_review         | POST           | delete_review_result.html | success: bool, message: str                                          |
| /profile                 | user_profile_page        | GET            | profile.html             | user: dict, borrow_history: list[dict], total_fines: float          |
| /profile/update          | update_profile           | POST           | profile_update_result.html | success: bool, message: str                                          |
| /payment/<int:fine_id>   | payment_confirmation_page| GET            | payment_confirmation.html| fine: dict                                                          |
| /payment/confirm/<int:fine_id> | confirm_payment       | POST           | payment_result.html      | success: bool, message: str                                          |

---

**Context Variables Structure Details:**

- `username` : str  (e.g. "john_reader")

- `books` : list of dict with each dict containing:
  - `book_id` : int
  - `title` : str
  - `author` : str
  - `isbn` : str
  - `genre` : str
  - `publisher` : str
  - `year` : int
  - `description` : str
  - `status` : str (Available, Borrowed, Reserved)
  - `avg_rating` : float

- `book` : dict containing all fields as above plus any additional computed fields if needed

- `reviews` : list of dict with each dict containing:
  - `review_id` : int
  - `username` : str
  - `rating` : int
  - `review_text` : str
  - `review_date` : str (YYYY-MM-DD)

- `user_has_borrowed` : bool - indicates if current user has borrowed the book

- `due_date` : str (YYYY-MM-DD) - the due date for returning a borrowed book

- `borrows` : list of dict with each dict containing:
  - `borrow_id` : int
  - `book_id` : int
  - `title` : str
  - `borrow_date` : str (YYYY-MM-DD)
  - `due_date` : str (YYYY-MM-DD)
  - `return_date` : str or None
  - `status` : str (Active, Returned, Overdue)
  - `fine_amount` : float

- `reservations` : list of dict with each dict containing:
  - `reservation_id` : int
  - `book_id` : int
  - `title` : str
  - `reservation_date` : str (YYYY-MM-DD)
  - `status` : str (Active, Cancelled)

- `reviews` (in my_reviews_page context) : list of dict
  - `review_id` : int
  - `book_id` : int
  - `title` : str
  - `rating` : int
  - `review_text` : str

- `existing_review` : dict or None - contains review info when editing/writing review

- `user` : dict with user details:
  - `username` : str
  - `email` : str
  - `phone` : str
  - `address` : str

- `borrow_history` : list of dict with each dict containing:
  - `book_id` : int
  - `title` : str
  - `borrow_date` : str
  - `return_date` : str or None

- `total_fines` : float - sum of unpaid fines

- `fine` : dict containing:
  - `fine_id` : int
  - `borrow_id` : int
  - `amount` : float
  - `status` : str (Unpaid, Paid)
  - `date_issued` : str

---

## Section 2: HTML Template Specifications (Frontend Development)

---

### 1. Template: `templates/dashboard.html`
- **Page Title**: Library Dashboard
- **IDs and element types:**
  - `dashboard-page` (div)
  - `welcome-message` (h1)
  - `browse-books-button` (button)
  - `my-borrows-button` (button)
- **Context Variables:**
  - `username` : str
- **Navigation:**
  - `browse-books-button` navigates to Flask route function `book_catalog_page`
  - `my-borrows-button` navigates to Flask route function `my_borrowings_page`

---

### 2. Template: `templates/catalog.html`
- **Page Title**: Book Catalog
- **IDs and element types:**
  - `catalog-page` (div)
  - `search-input` (input, text)
  - `book-grid` (div)
  - `back-to-dashboard` (button)
  - Buttons for each book:
    - `view-book-button-{book_id}` (button)
- **Context Variables:**
  - `books` : list of dict (each dict includes book_id:int, title:str, author:str, status:str)
- **Navigation:**
  - `view-book-button-{book_id}` navigates to `book_details_page` with parameter `book_id` 
  - `back-to-dashboard` navigates to `dashboard_page`

---

### 3. Template: `templates/book_details.html`
- **Page Title**: Book Details
- **IDs and element types:**
  - `book-details-page` (div)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button)
  - `reviews-section` (div)
  - `write-review-button` (button)
  - `back-to-catalog` (button)
- **Context Variables:**
  - `book` : dict
  - `reviews` : list of dict
  - `user_has_borrowed` : bool
- **Navigation:**
  - `borrow-button` triggers POST or navigates to `borrow_confirmation_page` with `book_id`
  - `write-review-button` navigates to `write_review_page` with `book_id`
  - `back-to-catalog` navigates to `book_catalog_page`

---

### 4. Template: `templates/borrow_confirmation.html`
- **Page Title**: Borrow Confirmation
- **IDs and element types:**
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button, form submit)
  - `cancel-borrow-button` (button)
- **Context Variables:**
  - `book` : dict
  - `due_date` : str
- **Navigation:**
  - `confirm-borrow-button` triggers POST to `confirm_borrow_book`
  - `cancel-borrow-button` navigates back to `book_details_page` with `book_id`

---

### 5. Template: `templates/my_borrows.html`
- **Page Title**: My Borrowings
- **IDs and element types:**
  - `my-borrows-page` (div)
  - `filter-status` (dropdown/select)
  - `borrows-table` (table)
  - `back-to-dashboard` (button)
  - For each borrow record:
    - `return-book-button-{borrow_id}` (button)
- **Context Variables:**
  - `borrows` : list of dict
- **Navigation:**
  - `return-book-button-{borrow_id}` triggers POST to `return_borrowed_book` with `borrow_id`
  - `back-to-dashboard` navigates to `dashboard_page`

---

### 6. Template: `templates/my_reservations.html`
- **Page Title**: My Reservations
- **IDs and element types:**
  - `reservations-page` (div)
  - `reservations-table` (table)
  - `back-to-dashboard` (button)
  - For each reservation record:
    - `cancel-reservation-button-{reservation_id}` (button)
- **Context Variables:**
  - `reservations` : list of dict
- **Navigation:**
  - `cancel-reservation-button-{reservation_id}` triggers POST to `cancel_reservation` with `reservation_id`
  - `back-to-dashboard` navigates to `dashboard_page`

---

### 7. Template: `templates/my_reviews.html`
- **Page Title**: My Reviews
- **IDs and element types:**
  - `reviews-page` (div)
  - `reviews-list` (div)
  - `back-to-dashboard` (button)
  - For each review record:
    - `edit-review-button-{review_id}` (button)
    - `delete-review-button-{review_id}` (button)
- **Context Variables:**
  - `reviews` : list of dict
- **Navigation:**
  - `edit-review-button-{review_id}` navigates to `edit_review_page` with `review_id`
  - `delete-review-button-{review_id}` triggers POST to `delete_review` with `review_id`
  - `back-to-dashboard` navigates to `dashboard_page`

---

### 8. Template: `templates/write_review.html`
- **Page Title**: Write Review
- **IDs and element types:**
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown/select, options 1-5)
  - `review-text` (textarea)
  - `submit-review-button` (button, form submit)
  - `back-to-book` (button)
- **Context Variables:**
  - `book` : dict
  - `existing_review` : dict or None
- **Navigation:**
  - `submit-review-button` triggers POST to `submit_review`
  - `back-to-book` navigates to `book_details_page` with `book_id`

---

### 9. Template: `templates/profile.html`
- **Page Title**: My Profile
- **IDs and element types:**
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input, text)
  - `update-profile-button` (button, form submit)
  - `borrow-history` (div)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `user` : dict
  - `borrow_history` : list of dict
  - `total_fines` : float
- **Navigation:**
  - `update-profile-button` triggers POST to `update_profile`
  - `back-to-dashboard` navigates to `dashboard_page`

---

### 10. Template: `templates/payment_confirmation.html`
- **Page Title**: Payment Confirmation
- **IDs and element types:**
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button, form submit)
  - `back-to-profile` (button)
- **Context Variables:**
  - `fine` : dict
- **Navigation:**
  - `confirm-payment-button` triggers POST to `confirm_payment` with `fine_id`
  - `back-to-profile` navigates to `user_profile_page`

---

## Section 3: Data File Schemas (Backend Development)

---

### 1. File: `data/users.txt`
- **Fields (pipe-delimited):**
  1. username (str)
  2. email (str)
  3. phone (str)
  4. address (str)
- **Description:** Stores user account information including contact details.
- **Example Rows:**
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`

---

### 2. File: `data/books.txt`
- **Fields (pipe-delimited):**
  1. book_id (int)
  2. title (str)
  3. author (str)
  4. isbn (str)
  5. genre (str)
  6. publisher (str)
  7. year (int)
  8. description (str)
  9. status (str) - One of: Available, Borrowed, Reserved
  10. avg_rating (float)
- **Description:** Stores detailed book records including availability and average rating.
- **Example Rows:**
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  - `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`
  - `4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5`
  - `5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3`

---

### 3. File: `data/borrowings.txt`
- **Fields (pipe-delimited):**
  1. borrow_id (int)
  2. username (str)
  3. book_id (int)
  4. borrow_date (str, YYYY-MM-DD)
  5. due_date (str, YYYY-MM-DD)
  6. return_date (str YYYY-MM-DD or empty)
  7. status (str) - One of: Active, Returned, Overdue
  8. fine_amount (float)
- **Description:** Records information about books borrowed by users including status and fines.
- **Example Rows:**
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`

---

### 4. File: `data/reservations.txt`
- **Fields (pipe-delimited):**
  1. reservation_id (int)
  2. username (str)
  3. book_id (int)
  4. reservation_date (str, YYYY-MM-DD)
  5. status (str) - One of: Active, Cancelled
- **Description:** Stores reservations made by users for books.
- **Example Rows:**
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`

---

### 5. File: `data/reviews.txt`
- **Fields (pipe-delimited):**
  1. review_id (int)
  2. username (str)
  3. book_id (int)
  4. rating (int)
  5. review_text (str)
  6. review_date (str, YYYY-MM-DD)
- **Description:** Contains all user submitted reviews for books.
- **Example Rows:**
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`

---

### 6. File: `data/fines.txt`
- **Fields (pipe-delimited):**
  1. fine_id (int)
  2. username (str)
  3. borrow_id (int)
  4. amount (float)
  5. status (str) - One of: Unpaid, Paid
  6. date_issued (str, YYYY-MM-DD)
- **Description:** Contains records of fines issued for overdue returns.
- **Example Rows:**
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`

---

# End of Design Specification
