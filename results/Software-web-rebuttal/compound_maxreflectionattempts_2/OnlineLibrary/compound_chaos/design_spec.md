# OnlineLibrary Design Specification Document

---

## Section 1: Flask Routes Specification (Backend)

### Route 1: Root Redirect
- **URL Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Method:** GET
- **Template Rendered:** Redirect to `/dashboard`
- **Context Variables:** None

---

### Route 2: Dashboard Page
- **URL Path:** `/dashboard`
- **Function Name:** `dashboard`
- **HTTP Method:** GET
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `username` (str): Current logged-in username
  - `featured_books` (list of dict): List of featured books, each dict containing:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str) - One of "Available", "Borrowed", "Reserved"

---

### Route 3: Book Catalog Page
- **URL Path:** `/catalog`
- **Function Name:** `catalog`
- **HTTP Method:** GET
- **Template Rendered:** `catalog.html`
- **Context Variables:**
  - `books` (list of dict): All available books. Each dict includes:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
  - `search_query` (str): Search term entered by the user (empty string if none)

---

### Route 4: Book Details Page
- **URL Path:** `/book/<int:book_id>`
- **Function Name:** `book_details`
- **HTTP Method:** GET
- **Template Rendered:** `book_details.html`
- **Context Variables:**
  - `book` (dict): Complete details about the book:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `isbn` (str)
    - `genre` (str)
    - `publisher` (str)
    - `year` (int)
    - `description` (str)
    - `status` (str): Availability status
    - `avg_rating` (float)
  - `reviews` (list of dict): Reviews of the book with:
    - `review_id` (int)
    - `username` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str in YYYY-MM-DD format)
  - `user_can_borrow` (bool): Whether current user is allowed to borrow
  - `user_can_review` (bool): Whether current user can write/edit review

---

### Route 5: Borrow Confirmation Page (GET)
- **URL Path:** `/borrow/<int:book_id>`
- **Function Name:** `borrow_confirmation`
- **HTTP Method:** GET
- **Template Rendered:** `borrow_confirmation.html`
- **Context Variables:**
  - `book` (dict): Book info including `book_id`, `title`, `author`
  - `due_date` (str): Due date 14 days from borrowing (YYYY-MM-DD)

---

### Route 6: Confirm Borrow POST
- **URL Path:** `/borrow/confirm`
- **Function Name:** `confirm_borrow`
- **HTTP Method:** POST
- **Template Rendered:** `borrow_success.html`
- **Context Variables:**
  - `book` (dict): Details of borrowed book
  - `due_date` (str): Due date for returning

---

### Route 7: Cancel Borrowing
- **URL Path:** `/borrow/cancel`
- **Function Name:** `cancel_borrow`
- **HTTP Method:** GET
- **Template Rendered:** Redirect to `/catalog`
- **Context Variables:** None

---

### Route 8: My Borrowings Page
- **URL Path:** `/myborrows`
- **Function Name:** `my_borrowings`
- **HTTP Method:** GET
- **Template Rendered:** `my_borrows.html`
- **Context Variables:**
  - `borrowings` (list of dict): Borrowed books with fields:
    - `borrow_id` (int)
    - `book_title` (str)
    - `borrow_date` (str)
    - `due_date` (str)
    - `status` (str): "Active", "Returned", "Overdue"
    - `fine_amount` (float)
  - `filter_status` (str): Current selected filter value from dropdown ("All", "Active", "Returned", "Overdue")

---

### Route 9: Return Book POST
- **URL Path:** `/return/<int:borrow_id>`
- **Function Name:** `return_book`
- **HTTP Method:** POST
- **Template Rendered:** `return_confirmation.html`
- **Context Variables:**
  - `borrowing` (dict): Borrowing info:
    - `borrow_id` (int)
    - `book_title` (str)
    - `borrow_date` (str)
    - `due_date` (str)
    - `status` (str)
  - `fine_amount` (float): Applicable fine amount (0.0 if none)

---

### Route 10: My Reservations Page
- **URL Path:** `/reservations`
- **Function Name:** `my_reservations`
- **HTTP Method:** GET
- **Template Rendered:** `reservations.html`
- **Context Variables:**
  - `reservations` (list of dict): Each reservation with:
    - `reservation_id` (int)
    - `book_title` (str)
    - `reservation_date` (str)
    - `status` (str): "Active" or "Cancelled"

---

### Route 11: Cancel Reservation POST
- **URL Path:** `/reservation/cancel/<int:reservation_id>`
- **Function Name:** `cancel_reservation`
- **HTTP Method:** POST
- **Template Rendered:** Redirect to `/reservations`
- **Context Variables:** None

---

### Route 12: My Reviews Page
- **URL Path:** `/myreviews`
- **Function Name:** `my_reviews`
- **HTTP Method:** GET
- **Template Rendered:** `my_reviews.html`
- **Context Variables:**
  - `reviews` (list of dict): Each review with:
    - `review_id` (int)
    - `book_title` (str)
    - `rating` (int)
    - `review_text` (str)

---

### Route 13: Delete Review POST
- **URL Path:** `/review/delete/<int:review_id>`
- **Function Name:** `delete_review`
- **HTTP Method:** POST
- **Template Rendered:** Redirect to `/myreviews`
- **Context Variables:** None

---

### Route 14: Edit Review Page GET
- **URL Path:** `/review/edit/<int:review_id>`
- **Function Name:** `edit_review`
- **HTTP Method:** GET
- **Template Rendered:** `write_review.html`
- **Context Variables:**
  - `review` (dict): Existing review details:
    - `review_id` (int)
    - `book_id` (int)
    - `book_title` (str)
    - `rating` (int)
    - `review_text` (str)
  - `book` (dict): Book details for display

---

### Route 15: Submit Review POST
- **URL Path:** `/review/submit`
- **Function Name:** `submit_review`
- **HTTP Method:** POST
- **Template Rendered:** Redirect to `/book/<book_id>`
- **Context Variables:** None

---

### Route 16: User Profile Page
- **URL Path:** `/profile`
- **Function Name:** `profile`
- **HTTP Method:** GET
- **Template Rendered:** `profile.html`
- **Context Variables:**
  - `username` (str)
  - `email` (str)
  - `phone` (str)
  - `address` (str)
  - `borrow_history` (list of dict): Each entry with:
    - `book_title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)

---

### Route 17: Update Profile POST
- **URL Path:** `/profile/update`
- **Function Name:** `update_profile`
- **HTTP Method:** POST
- **Template Rendered:** Redirect to `/profile`
- **Context Variables:** None

---

### Route 18: Payment Confirmation Page
- **URL Path:** `/payment/<int:fine_id>`
- **Function Name:** `payment_confirmation`
- **HTTP Method:** GET
- **Template Rendered:** `payment_confirmation.html`
- **Context Variables:**
  - `fine` (dict): Contains:
    - `fine_id` (int)
    - `amount` (float)

---

### Route 19: Confirm Payment POST
- **URL Path:** `/payment/confirm/<int:fine_id>`
- **Function Name:** `confirm_payment`
- **HTTP Method:** POST
- **Template Rendered:** Redirect to `/profile`
- **Context Variables:** None

---


## Section 2: HTML Template Specifications (Frontend)

### Template 1: dashboard.html
- **Path:** `templates/dashboard.html`
- **Page Title:** "Library Dashboard"
- **Main Header (`<h1>`):** 
  - ID: `welcome-message`
  - Content: "Welcome, {{ username }}!"
- **Element IDs:**
  - `dashboard-page` (div container)
  - `welcome-message` (h1)
  - `browse-books-button` (button)
  - `my-borrows-button` (button)
- **Context Variables:**
  - `username` (str)
  - `featured_books` (list of dicts as specified above)
- **Navigation:**
  - `browse-books-button` navigates to `catalog` route using `url_for('catalog')`
  - `my-borrows-button` navigates to `my_borrowings` route using `url_for('my_borrowings')`

---

### Template 2: catalog.html
- **Path:** `templates/catalog.html`
- **Page Title:** "Book Catalog"
- **Element IDs:**
  - `catalog-page` (div container)
  - `search-input` (input text)
  - `book-grid` (div)
  - `back-to-dashboard` (button)
  - Dynamic buttons with ID `view-book-button-{{ book.book_id }}` (button) for each book card
- **Context Variables:**
  - `books` (list of dicts)
  - `search_query` (str)
- **Navigation:**
  - `back-to-dashboard` navigates to `dashboard` route
  - Each `view-book-button-{{ book.book_id }}` navigates to `book_details` with `book_id` parameter

---

### Template 3: book_details.html
- **Path:** `templates/book_details.html`
- **Page Title:** "Book Details"
- **Element IDs:**
  - `book-details-page` (div container)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button) [Shown if `user_can_borrow` is True]
  - `reviews-section` (div)
  - `write-review-button` (button) [Shown if `user_can_review` is True]
  - `back-to-catalog` (button)
- **Context Variables:**
  - `book` (dict)
  - `reviews` (list of dicts)
  - `user_can_borrow` (bool)
  - `user_can_review` (bool)
- **Navigation:**
  - `borrow-button` triggers GET request to `/borrow/<book.book_id>`
  - `write-review-button` navigates to review write/edit page
  - `back-to-catalog` navigates to `catalog` route

---

### Template 4: borrow_confirmation.html
- **Path:** `templates/borrow_confirmation.html`
- **Page Title:** "Borrow Confirmation"
- **Element IDs:**
  - `borrow-page` (div container)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button, submits form via POST to `/borrow/confirm`)
  - `cancel-borrow-button` (button, navigates to `/catalog`)
- **Context Variables:**
  - `book` (dict)
  - `due_date` (str in YYYY-MM-DD format)

---

### Template 5: borrow_success.html
- **Path:** `templates/borrow_success.html`
- **Page Title:** "Borrow Confirmation"
- **Element IDs:**
  - `borrow-page` (div container)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
- **Context Variables:**
  - `book` (dict)
  - `due_date` (str)

---

### Template 6: my_borrows.html
- **Path:** `templates/my_borrows.html`
- **Page Title:** "My Borrowings"
- **Element IDs:**
  - `my-borrows-page` (div container)
  - `filter-status` (dropdown select to filter by borrowing status)
  - `borrows-table` (table)
  - Dynamic buttons with ID `return-book-button-{{ borrow.borrow_id }}` (button) for active borrows to return book
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `borrowings` (list of dicts as described above)
  - `filter_status` (str)
- **Navigation:**
  - Each `return-book-button-{{ borrow.borrow_id }}` submits POST to `/return/<borrow.borrow_id>`
  - `back-to-dashboard` navigates to `dashboard`

---

### Template 7: return_confirmation.html
- **Path:** `templates/return_confirmation.html`
- **Page Title:** "Return Confirmation"
- **Element IDs:**
  - `return-confirmation-page` (div container)
  - `fine-amount-display` (div)
- **Context Variables:**
  - `borrowing` (dict)
  - `fine_amount` (float)

---

### Template 8: reservations.html
- **Path:** `templates/reservations.html`
- **Page Title:** "My Reservations"
- **Element IDs:**
  - `reservations-page` (div container)
  - `reservations-table` (table)
  - Dynamic buttons with ID `cancel-reservation-button-{{ reservation.reservation_id }}` (button)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `reservations` (list of dicts)
- **Navigation:**
  - Each `cancel-reservation-button-{{ reservation.reservation_id }}` submits POST to `/reservation/cancel/<reservation.reservation_id>`
  - `back-to-dashboard` navigates to `dashboard`

---

### Template 9: my_reviews.html
- **Path:** `templates/my_reviews.html`
- **Page Title:** "My Reviews"
- **Element IDs:**
  - `reviews-page` (div container)
  - `reviews-list` (div container)
  - Dynamic buttons with IDs `edit-review-button-{{ review.review_id }}` and `delete-review-button-{{ review.review_id }}`
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `reviews` (list of dicts)
- **Navigation:**
  - `edit-review-button-{{ review.review_id }}` navigates to `/review/edit/<review.review_id>`
  - `delete-review-button-{{ review.review_id }}` submits POST to `/review/delete/<review.review_id>`
  - `back-to-dashboard` navigates to `dashboard`

---

### Template 10: write_review.html
- **Path:** `templates/write_review.html`
- **Page Title:** "Write Review"
- **Element IDs:**
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown select 1-5)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- **Context Variables:**
  - `review` (dict or null) for editing existing review
  - `book` (dict)
- **Navigation:**
  - `submit-review-button` submits POST to `/review/submit`
  - `back-to-book` navigates to `/book/<book.book_id>`

---

### Template 11: profile.html
- **Path:** `templates/profile.html`
- **Page Title:** "My Profile"
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
  - `phone` (str)
  - `address` (str)
  - `borrow_history` (list of dicts) each dict:
    - `book_title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)
- **Navigation:**
  - `update-profile-button` submits POST to `/profile/update`
  - `back-to-dashboard` navigates to `dashboard`

---

### Template 12: payment_confirmation.html
- **Path:** `templates/payment_confirmation.html`
- **Page Title:** "Payment Confirmation"
- **Element IDs:**
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- **Context Variables:**
  - `fine` (dict) with keys:
    - `fine_id` (int)
    - `amount` (float)
- **Navigation:**
  - `confirm-payment-button` submits POST to `/payment/confirm/<fine.fine_id>`
  - `back-to-profile` navigates to `profile`

---

## Section 3: Data File Schemas (Backend)

### Data File 1: users.txt
- **Location:** `data/users.txt`
- **Fields (pipe `|` separated):**
  1. `username` (str)
  2. `email` (str)
  3. `phone` (str)
  4. `address` (str)
- **Description:** Stores user profiles with contact info.
- **Example entries:**
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`

---

### Data File 2: books.txt
- **Location:** `data/books.txt`
- **Fields (pipe `|` separated):**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `genre` (str)
  6. `publisher` (str)
  7. `year` (int)
  8. `description` (str)
  9. `status` (str) - "Available", "Borrowed", "Reserved"
  10. `avg_rating` (float)
- **Description:** Contains full book catalog info.
- **Example entries:**
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  - `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`

---

### Data File 3: borrowings.txt
- **Location:** `data/borrowings.txt`
- **Fields (pipe `|` separated):**
  1. `borrow_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `borrow_date` (str in YYYY-MM-DD)
  5. `due_date` (str in YYYY-MM-DD)
  6. `return_date` (str in YYYY-MM-DD or empty if not returned)
  7. `status` (str) - "Active", "Returned", "Overdue"
  8. `fine_amount` (float)
- **Description:** Records all borrowings.
- **Example entries:**
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`

---

### Data File 4: reservations.txt
- **Location:** `data/reservations.txt`
- **Fields (pipe `|` separated):**
  1. `reservation_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `reservation_date` (str in YYYY-MM-DD)
  5. `status` (str) - "Active" or "Cancelled"
- **Description:** Tracks users' book reservations.
- **Example entries:**
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`

---

### Data File 5: reviews.txt
- **Location:** `data/reviews.txt`
- **Fields (pipe `|` separated):**
  1. `review_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `rating` (int from 1 to 5)
  5. `review_text` (str)
  6. `review_date` (str in YYYY-MM-DD)
- **Description:** User reviews for books.
- **Example entries:**
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`

---

### Data File 6: fines.txt
- **Location:** `data/fines.txt`
- **Fields (pipe `|` separated):**
  1. `fine_id` (int)
  2. `username` (str)
  3. `borrow_id` (int)
  4. `amount` (float)
  5. `status` (str) - "Unpaid" or "Paid"
  6. `date_issued` (str in YYYY-MM-DD)
- **Description:** Records overdue payment fines.
- **Example entries:**
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`

---



---

*End of Document - design_spec.md*