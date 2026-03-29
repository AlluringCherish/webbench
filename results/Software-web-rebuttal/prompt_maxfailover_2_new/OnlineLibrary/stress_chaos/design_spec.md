# OnlineLibrary Design Specification Document

---

## Section 1: Flask Routes Specification (Backend Development)

### 1. Root Route
- **URL path**: `/`
- **Function name**: `root_redirect`
- **HTTP method**: GET
- **Template rendered**: Redirect to `dashboard`
- **Context variables**: None

### 2. Dashboard Page
- **URL path**: `/dashboard`
- **Function name**: `dashboard`
- **HTTP method**: GET
- **Template rendered**: `dashboard.html`
- **Context variables**:
  - `username` (str): Current logged-in user's username
  - `featured_books` (list of dict): Optional list of featured books if applicable (each dict contains at least `book_id`, `title`, and `author`)

### 3. Book Catalog Page
- **URL path**: `/catalog`
- **Function name**: `book_catalog`
- **HTTP method**: GET
- **Template rendered**: `catalog.html`
- **Context variables**:
  - `books` (list of dict): List of all books with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str) - "Available", "Borrowed", or "Reserved"

### 4. Book Details Page
- **URL path**: `/book/<int:book_id>`
- **Function name**: `book_details`
- **HTTP method**: GET
- **Template rendered**: `book_details.html`
- **Context variables**:
  - `book` (dict): Book details including:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
    - `description` (str)
    - `avg_rating` (float)
  - `reviews` (list of dict): List of reviews for the book with keys:
    - `review_id` (int)
    - `username` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str, YYYY-MM-DD)
  - `user_has_borrowed` (bool): Whether current user has borrowed this book
  - `user_can_borrow` (bool): Whether user can borrow (book available and user eligible)

### 5. Borrow Confirmation Page
- **URL path**: `/borrow/<int:book_id>`
- **Function name**: `borrow_confirmation`
- **HTTP method**: GET
- **Template rendered**: `borrow_confirmation.html`
- **Context variables**:
  - `book` (dict): Book information with `book_id`, `title`, and `author`
  - `due_date` (str): Due date for return, 14 days from the current date (YYYY-MM-DD)

- **POST URL path**: `/borrow/confirm/<int:book_id>`
- **Function name**: `confirm_borrow`
- **HTTP method**: POST
- **Template rendered**: `borrow_result.html` (or redirect to dashboard)
- **Context variables**:
  - `success` (bool): Whether borrowing succeeded
  - `book` (dict): Book info
  - `due_date` (str): Due date
  - `error_message` (str, optional): In case borrowing fails

### 6. My Borrowings Page
- **URL path**: `/my-borrows`
- **Function name**: `my_borrowings`
- **HTTP method**: GET
- **Template rendered**: `my_borrows.html`
- **Context variables**:
  - `borrows` (list of dict): List of borrow records for the user, each dict contains:
    - `borrow_id` (int)
    - `book_id` (int)
    - `title` (str)
    - `borrow_date` (str, YYYY-MM-DD)
    - `due_date` (str, YYYY-MM-DD)
    - `return_date` (str, YYYY-MM-DD or empty)
    - `status` (str) – "Active", "Returned", or "Overdue"
    - `fine_amount` (float)
  - `filter_status` (str): Current filter value ("All", "Active", "Returned", "Overdue")

- **POST URL path**: `/return/<int:borrow_id>`
- **Function name**: `return_book`
- **HTTP method**: POST
- **Template rendered**: `return_result.html` (or redirect)
- **Context variables**:
  - `success` (bool): Whether return succeeded
  - `borrow_id` (int)
  - `error_message` (str, optional)

### 7. My Reservations Page
- **URL path**: `/my-reservations`
- **Function name**: `my_reservations`
- **HTTP method**: GET
- **Template rendered**: `my_reservations.html`
- **Context variables**:
  - `reservations` (list of dict): List of reservation records with keys:
    - `reservation_id` (int)
    - `book_id` (int)
    - `title` (str)
    - `reservation_date` (str, YYYY-MM-DD)
    - `status` (str) - "Active" or "Cancelled"

- **POST URL path**: `/reservation/cancel/<int:reservation_id>`
- **Function name**: `cancel_reservation`
- **HTTP method**: POST
- **Template rendered**: redirect back to `my_reservations`

### 8. My Reviews Page
- **URL path**: `/my-reviews`
- **Function name**: `my_reviews`
- **HTTP method**: GET
- **Template rendered**: `my_reviews.html`
- **Context variables**:
  - `reviews` (list of dict): List of reviews by the user with keys:
    - `review_id` (int)
    - `book_id` (int)
    - `title` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str, YYYY-MM-DD)

- **POST URL path**: `/review/delete/<int:review_id>`
- **Function name**: `delete_review`
- **HTTP method**: POST
- **Template rendered**: redirect to `my_reviews`

### 9. Write Review Page
- **URL path**: `/review/write/<int:book_id>`
- **Function name**: `write_review`
- **HTTP method**: GET
- **Template rendered**: `write_review.html`
- **Context variables**:
  - `book` (dict): Book info with `book_id`, `title`, `author`
  - `existing_review` (dict or None): If editing, review details with `review_id`, `rating`, `review_text`

- **POST URL path**: `/review/submit/<int:book_id>`
- **Function name**: `submit_review`
- **HTTP method**: POST
- **Template rendered**: redirect to `book_details` for the same book

### 10. User Profile Page
- **URL path**: `/profile`
- **Function name**: `user_profile`
- **HTTP method**: GET
- **Template rendered**: `profile.html`
- **Context variables**:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): List of all previously borrowed books including:
    - `title` (str)
    - `borrow_date` (str)
    - `return_date` (str or empty)
  - `phone` (str)
  - `address` (str)

- **POST URL path**: `/profile/update`
- **Function name**: `update_profile`
- **HTTP method**: POST
- **Template rendered**: redirect to `profile`

### 11. Payment Confirmation Page
- **URL path**: `/payment/<int:fine_id>`
- **Function name**: `payment_confirmation`
- **HTTP method**: GET
- **Template rendered**: `payment_confirmation.html`
- **Context variables**:
  - `fine` (dict): Fine details including:
    - `fine_id` (int)
    - `amount` (float)
    - `status` (str) - "Paid" or "Unpaid"
  - `username` (str)

- **POST URL path**: `/payment/confirm/<int:fine_id>`
- **Function name**: `confirm_payment`
- **HTTP method**: POST
- **Template rendered**: redirect to `profile`

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. Dashboard Template
- **Filename and path**: `templates/dashboard.html`
- **Page title**: Library Dashboard
- **Page header (h1)**: 
  - Element ID: `welcome-message`
  - Displays the welcome message with `username`
- **Element IDs and Types**:
  - `dashboard-page` (div) - main container
  - `browse-books-button` (button) - navigates to Book Catalog page
  - `my-borrows-button` (button) - navigates to My Borrowings page

- **Context variables accessible**:
  - `username` (str)
  - `featured_books` (list of dict)

- **Navigation links**:
  - `browse-books-button` triggers link to `book_catalog`
  - `my-borrows-button` triggers link to `my_borrowings`

### 2. Book Catalog Template
- **Filename and path**: `templates/catalog.html`
- **Page title**: Book Catalog
- **Page header (h1)**: Not explicitly specified; container provided
- **Element IDs and Types**:
  - `catalog-page` (div) - main container
  - `search-input` (input, text)
  - `book-grid` (div) - container for book cards
  - `view-book-button-{book_id}` (button, multiple) - one per book, id pattern with dynamic book_id
  - `back-to-dashboard` (button) - navigates back to Dashboard

- **Context variables accessible**:
  - `books` (list of dict) with keys: `book_id`, `title`, `author`, `status`

- **Navigation links**:
  - `view-book-button-{book_id}` to route `book_details` with parameter `book_id`
  - `back-to-dashboard` to route `dashboard`

### 3. Book Details Template
- **Filename and path**: `templates/book_details.html`
- **Page title**: Book Details
- **Page header (h1)**:
  - Element ID: `book-title` - displaying `book.title`
- **Element IDs and Types**:
  - `book-details-page` (div) container
  - `book-author` (div) displays author
  - `book-status` (div) displays availability status
  - `borrow-button` (button) to borrow book
  - `reviews-section` (div) holds list of reviews
  - `write-review-button` (button) to write review
  - `back-to-catalog` (button) to navigate back to catalog

- **Context variables accessible**:
  - `book` (dict)
  - `reviews` (list of dict)
  - `user_has_borrowed` (bool)
  - `user_can_borrow` (bool)

- **Navigation links**:
  - `borrow-button` links to `borrow_confirmation` for current `book.book_id`
  - `write-review-button` links to `write_review` for current `book.book_id`
  - `back-to-catalog` links to `book_catalog`

### 4. Borrow Confirmation Template
- **Filename and path**: `templates/borrow_confirmation.html`
- **Page title**: Borrow Confirmation
- **Page header (h1)**: Not specified explicitly
- **Element IDs and Types**:
  - `borrow-page` (div) container
  - `borrow-book-info` (div) shows book title and author
  - `due-date-display` (div) shows due date
  - `confirm-borrow-button` (button) to confirm
  - `cancel-borrow-button` (button) to cancel and return back

- **Context variables accessible**:
  - `book` (dict)
  - `due_date` (str)

- **Form specs**:
  - Form for POST to `/borrow/confirm/<book_id>` with method POST
  - The confirm button is the submit button
  - Cancel button leads back to book details page for that book

### 5. My Borrowings Template
- **Filename and path**: `templates/my_borrows.html`
- **Page title**: My Borrowings
- **Page header (h1)**: Not explicitly specified
- **Element IDs and Types**:
  - `my-borrows-page` (div) container
  - `filter-status` (dropdown/select) with options: All, Active, Returned, Overdue
  - `borrows-table` (table) with columns: Title, Borrow Date, Due Date, Status
  - `return-book-button-{borrow_id}` (button, multiple) - one per active borrow
  - `back-to-dashboard` (button) to go back

- **Context variables accessible**:
  - `borrows` (list of dict)
  - `filter_status` (str)

- **Navigation links**:
  - `return-book-button-{borrow_id}` submits POST to `return_book` for that borrow_id
  - `back-to-dashboard` links to `dashboard`

### 6. My Reservations Template
- **Filename and path**: `templates/my_reservations.html`
- **Page title**: My Reservations
- **Page header (h1)**: Not explicitly specified
- **Element IDs and Types**:
  - `reservations-page` (div) container
  - `reservations-table` (table) with columns: Title, Reservation Date, Status
  - `cancel-reservation-button-{reservation_id}` (button, multiple) - one per reservation
  - `back-to-dashboard` (button)

- **Context variables accessible**:
  - `reservations` (list of dict)

- **Navigation links**:
  - `cancel-reservation-button-{reservation_id}` submits POST to `cancel_reservation` route
  - `back-to-dashboard` to `dashboard`

### 7. My Reviews Template
- **Filename and path**: `templates/my_reviews.html`
- **Page title**: My Reviews
- **Page header (h1)**: Not explicitly specified
- **Element IDs and Types**:
  - `reviews-page` (div) container
  - `reviews-list` (div) listing individual reviews
  - `edit-review-button-{review_id}` (button, multiple)
  - `delete-review-button-{review_id}` (button, multiple)
  - `back-to-dashboard` (button)

- **Context variables accessible**:
  - `reviews` (list of dict)

- **Navigation links**:
  - `edit-review-button-{review_id}` links to `write_review` route with `book_id` parameter from review context if available
  - `delete-review-button-{review_id}` submits POST to `delete_review`
  - `back-to-dashboard` to `dashboard`

### 8. Write Review Template
- **Filename and path**: `templates/write_review.html`
- **Page title**: Write Review
- **Page header (h1)**: Not explicitly specified
- **Element IDs and Types**:
  - `write-review-page` (div) container
  - `book-info-display` (div) shows book information
  - `rating-input` (dropdown/select) with options 1 to 5
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)

- **Context variables accessible**:
  - `book` (dict)
  - `existing_review` (dict or None)

- **Form specs**:
  - Form for POST to `/review/submit/<book_id>`
  - Submit button submits the form
  - Back button links back to `book_details`

### 9. User Profile Template
- **Filename and path**: `templates/profile.html`
- **Page title**: My Profile
- **Page header (h1)**: Not explicitly specified
- **Element IDs and Types**:
  - `profile-page` (div) container
  - `profile-username` (div) display username (not editable)
  - `profile-email` (input, text) for editing email
  - `update-profile-button` (button)
  - `borrow-history` (div) lists previously borrowed books
  - `back-to-dashboard` (button)

- **Context variables accessible**:
  - `username` (str)
  - `email` (str)
  - `phone` (str)
  - `address` (str)
  - `borrow_history` (list of dict) with keys: `title`, `borrow_date`, `return_date`

- **Form specs**:
  - Form POST to `/profile/update` to update email
  - Submit button triggers update
  - Back button links to `dashboard`

### 10. Payment Confirmation Template
- **Filename and path**: `templates/payment_confirmation.html`
- **Page title**: Payment Confirmation
- **Page header (h1)**: Not explicitly specified
- **Element IDs and Types**:
  - `payment-page` (div) container
  - `fine-amount-display` (div) shows fine amount
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)

- **Context variables accessible**:
  - `fine` (dict) with fields: `fine_id` (int), `amount` (float), `status` (str)
  - `username` (str)

- **Form specs**:
  - Form POST to `/payment/confirm/<fine_id>`
  - Confirm button submits form
  - Back button links to `user_profile`

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- **Filename and path**: `data/users.txt`
- **Field order and names**:
  - `username` (str)
  - `email` (str)
  - `phone` (str)
  - `address` (str)

- **Description**:
  This file stores registered user profile information.

- **Example rows**:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```

- **Parsing notes**:
  - Fields are pipe-delimited.
  - No header line.

### 2. books.txt
- **Filename and path**: `data/books.txt`
- **Field order and names**:
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

- **Description**:
  Stores all book catalog data.

- **Example rows**:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5
  5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3
  ```

- **Parsing notes**:
  - All fields pipe-delimited.
  - No header.
  - `book_id` unique identifier.

### 3. borrowings.txt
- **Filename and path**: `data/borrowings.txt`
- **Field order and names**:
  - `borrow_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `borrow_date` (str, YYYY-MM-DD)
  - `due_date` (str, YYYY-MM-DD)
  - `return_date` (str, YYYY-MM-DD or empty when not returned)
  - `status` (str) - "Active", "Returned", "Overdue"
  - `fine_amount` (float)

- **Description**:
  Records borrowing transactions and status per user and book.

- **Example rows**:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
  ```

- **Parsing notes**:
  - Empty `return_date` field if book not returned
  - Status indicates current state

### 4. reservations.txt
- **Filename and path**: `data/reservations.txt`
- **Field order and names**:
  - `reservation_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `reservation_date` (str, YYYY-MM-DD)
  - `status` (str) - "Active" or "Cancelled"

- **Description**:
  Stores active and cancelled reservations made by users.

- **Example rows**:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```

- **Parsing notes**:
  - Pipe-delimited, no header

### 5. reviews.txt
- **Filename and path**: `data/reviews.txt`
- **Field order and names**:
  - `review_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `rating` (int, 1-5)
  - `review_text` (str)
  - `review_date` (str, YYYY-MM-DD)

- **Description**:
  Stores user reviews and ratings for books.

- **Example rows**:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```

- **Parsing notes**:
  - Pipes separate fields
  - Review text may contain spaces and punctuation

### 6. fines.txt
- **Filename and path**: `data/fines.txt`
- **Field order and names**:
  - `fine_id` (int)
  - `username` (str)
  - `borrow_id` (int)
  - `amount` (float)
  - `status` (str) - "Unpaid" or "Paid"
  - `date_issued` (str, YYYY-MM-DD)

- **Description**:
  Tracks fines related to overdue borrowings.

- **Example rows**:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
  ```

- **Parsing notes**:
  - Amount is decimal with 2 decimal places
  - Status indicates payment state

---

This completes the design specification document for both backend and frontend teams to implement the OnlineLibrary application according to the provided user requirements.