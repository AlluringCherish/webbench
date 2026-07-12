# OnlineLibrary Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

### 1. Root Route
- **URL Path:** /
- **Function Name:** root_redirect
- **HTTP Method:** GET
- **Template Rendered:** None (Redirect to Dashboard)
- **Context Variables:** None

### 2. Dashboard Page
- **URL Path:** /dashboard
- **Function Name:** dashboard_page
- **HTTP Method:** GET
- **Template Rendered:** dashboard.html
- **Context Variables:**
  - `username` (str): Username of currently logged-in user
  - `featured_books` (list of dict): List of featured books, each dict with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str): Availability status

### 3. Book Catalog Page
- **URL Path:** /catalog
- **Function Name:** book_catalog_page
- **HTTP Method:** GET
- **Template Rendered:** catalog.html
- **Context Variables:**
  - `books` (list of dict): List of all books, each dict containing:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
  - `search_query` (str): Current search filter (if any)

### 4. Book Details Page
- **URL Path:** /book/<int:book_id>
- **Function Name:** book_details_page
- **HTTP Method:** GET
- **Template Rendered:** book_details.html
- **Context Variables:**
  - `book` (dict): Detailed book info with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
    - `description` (str)
    - `avg_rating` (float)
  - `reviews` (list of dict): List of reviews for the book, each dict:
    - `review_id` (int)
    - `username` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str, YYYY-MM-DD)

### 5. Borrow Confirmation Page
- **URL Path:** /borrow/<int:book_id>
- **Function Name:** borrow_confirmation_page
- **HTTP Method:** GET
- **Template Rendered:** borrow_confirmation.html
- **Context Variables:**
  - `book` (dict): Book info being borrowed
  - `due_date` (str, YYYY-MM-DD): Due date 14 days from borrow date

- **POST Route For Borrow Confirmation:**
- **URL Path:** /borrow/<int:book_id>/confirm
- **Function Name:** confirm_borrow
- **HTTP Method:** POST
- **Template Rendered:** borrow_result.html (or redirect back with error)
- **Context Variables:**
  - `success` (bool): Borrow success indicator
  - `book` (dict): Book info
  - `due_date` (str)

- **POST Route For Cancel Borrow:**
- **URL Path:** /borrow/<int:book_id>/cancel
- **Function Name:** cancel_borrow
- **HTTP Method:** POST
- **Template Rendered:** Redirect to book details or catalog

### 6. My Borrowings Page
- **URL Path:** /my-borrows
- **Function Name:** my_borrows_page
- **HTTP Method:** GET
- **Template Rendered:** my_borrows.html
- **Context Variables:**
  - `borrows` (list of dict): List of borrowings by user, each dict:
    - `borrow_id` (int)
    - `book_title` (str)
    - `borrow_date` (str)
    - `due_date` (str)
    - `status` (str): Active, Returned, Overdue
    - `fine_amount` (float)
  - `filter_status` (str): Current filter (All, Active, Returned, Overdue)

- **POST Route to Return Book:**
- **URL Path:** /return/<int:borrow_id>
- **Function Name:** return_book
- **HTTP Method:** POST
- **Template Rendered:** return_confirmation.html or redirect
- **Context Variables:**
  - `success` (bool)
  - `borrow_id` (int)

### 7. My Reservations Page
- **URL Path:** /my-reservations
- **Function Name:** my_reservations_page
- **HTTP Method:** GET
- **Template Rendered:** my_reservations.html
- **Context Variables:**
  - `reservations` (list of dict): All reservations by user, each dict:
    - `reservation_id` (int)
    - `book_title` (str)
    - `reservation_date` (str)
    - `status` (str): Active, Cancelled

- **POST Route to Cancel Reservation:**
- **URL Path:** /cancel-reservation/<int:reservation_id>
- **Function Name:** cancel_reservation
- **HTTP Method:** POST
- **Template Rendered:** Redirect or confirmation

### 8. My Reviews Page
- **URL Path:** /my-reviews
- **Function Name:** my_reviews_page
- **HTTP Method:** GET
- **Template Rendered:** my_reviews.html
- **Context Variables:**
  - `reviews` (list of dict): Reviews written by user with keys:
    - `review_id` (int)
    - `book_title` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str)

### 9. Write Review Page
- **URL Path:** /write-review/<int:book_id>
- **Function Name:** write_review_page
- **HTTP Method:** GET
- **Template Rendered:** write_review.html
- **Context Variables:**
  - `book` (dict): Book info being reviewed
  - `existing_review` (dict or None): If editing, existing review details:
    - `review_id` (int)
    - `rating` (int)
    - `review_text` (str)

- **POST Route to Submit Review:**
- **URL Path:** /submit-review/<int:book_id>
- **Function Name:** submit_review
- **HTTP Method:** POST
- **Template Rendered:** Redirect or confirmation

### 10. User Profile Page
- **URL Path:** /profile
- **Function Name:** user_profile_page
- **HTTP Method:** GET
- **Template Rendered:** profile.html
- **Context Variables:**
  - `username` (str)
  - `email` (str)
  - `phone` (str)
  - `address` (str)
  - `borrow_history` (list of dict): All borrowings with keys:
    - `book_title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)
    - `status` (str)

- **POST Route to Update Profile:**
- **URL Path:** /profile/update
- **Function Name:** update_profile
- **HTTP Method:** POST
- **Template Rendered:** Redirect or confirmation

### 11. Payment Confirmation Page
- **URL Path:** /payment/<int:fine_id>
- **Function Name:** payment_confirmation_page
- **HTTP Method:** GET
- **Template Rendered:** payment_confirmation.html
- **Context Variables:**
  - `fine` (dict): Fine details with keys:
    - `fine_id` (int)
    - `amount` (float)
    - `status` (str)

- **POST Route to Confirm Payment:**
- **URL Path:** /payment/<int:fine_id>/confirm
- **Function Name:** confirm_payment
- **HTTP Method:** POST
- **Template Rendered:** Redirect or confirmation

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. dashboard.html
- **Path:** templates/dashboard.html
- **Page Title:** Library Dashboard
- **Element IDs:**
  - `dashboard-page` (div)
  - `welcome-message` (h1)
  - `browse-books-button` (button)
  - `my-borrows-button` (button)
- **Context Variables:**
  - `username` (str)
  - `featured_books` (list of dict: book_id, title, author, status)
- **Navigation:**
  - `browse-books-button` triggers navigation to `book_catalog_page`
  - `my-borrows-button` triggers navigation to `my_borrows_page`

### 2. catalog.html
- **Path:** templates/catalog.html
- **Page Title:** Book Catalog
- **Element IDs:**
  - `catalog-page` (div)
  - `search-input` (input)
  - `book-grid` (div)
  - Dynamic buttons: `view-book-button-{{ book.book_id }}` (button)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `books` (list of dict: book_id, title, author, status)
  - `search_query` (str)
- **Navigation:**
  - `view-book-button-{{ book.book_id }}` navigates to `book_details_page(book_id=book.book_id)`
  - `back-to-dashboard` navigates to `dashboard_page`

### 3. book_details.html
- **Path:** templates/book_details.html
- **Page Title:** Book Details
- **Element IDs:**
  - `book-details-page` (div)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button)
  - `reviews-section` (div)
  - `write-review-button` (button)
  - `back-to-catalog` (button)
- **Context Variables:**
  - `book` (dict: book_id, title, author, status, description, avg_rating)
  - `reviews` (list of dict: review_id, username, rating, review_text, review_date)
- **Navigation:**
  - `borrow-button` triggers POST to `borrow_confirmation_page(book_id=book.book_id)`
  - `write-review-button` navigates to `write_review_page(book_id=book.book_id)`
  - `back-to-catalog` navigates to `book_catalog_page`

### 4. borrow_confirmation.html
- **Path:** templates/borrow_confirmation.html
- **Page Title:** Borrow Confirmation
- **Element IDs:**
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button)
  - `cancel-borrow-button` (button)
- **Context Variables:**
  - `book` (dict)
  - `due_date` (str)
- **Navigation:**
  - `confirm-borrow-button` triggers POST to `confirm_borrow(book_id=book.book_id)`
  - `cancel-borrow-button` triggers POST to `cancel_borrow(book_id=book.book_id)`

### 5. my_borrows.html
- **Path:** templates/my_borrows.html
- **Page Title:** My Borrowings
- **Element IDs:**
  - `my-borrows-page` (div)
  - `filter-status` (dropdown)
  - `borrows-table` (table)
  - Return buttons: `return-book-button-{{ borrow.borrow_id }}` (button)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `borrows` (list of dict: borrow_id, book_title, borrow_date, due_date, status, fine_amount)
  - `filter_status` (str)
- **Navigation:**
  - `return-book-button-{{ borrow.borrow_id }}` triggers POST to `return_book(borrow_id=borrow.borrow_id)`
  - `back-to-dashboard` navigates to `dashboard_page`

### 6. my_reservations.html
- **Path:** templates/my_reservations.html
- **Page Title:** My Reservations
- **Element IDs:**
  - `reservations-page` (div)
  - `reservations-table` (table)
  - Cancel buttons: `cancel-reservation-button-{{ reservation.reservation_id }}` (button)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `reservations` (list of dict: reservation_id, book_title, reservation_date, status)
- **Navigation:**
  - `cancel-reservation-button-{{ reservation.reservation_id }}` triggers POST to `cancel_reservation(reservation_id=reservation.reservation_id)`
  - `back-to-dashboard` navigates to `dashboard_page`

### 7. my_reviews.html
- **Path:** templates/my_reviews.html
- **Page Title:** My Reviews
- **Element IDs:**
  - `reviews-page` (div)
  - `reviews-list` (div)
  - Edit buttons: `edit-review-button-{{ review.review_id }}` (button)
  - Delete buttons: `delete-review-button-{{ review.review_id }}` (button)
  - `back-to-dashboard` (button)
- **Context Variables:**
  - `reviews` (list of dict: review_id, book_title, rating, review_text, review_date)
- **Navigation:**
  - `edit-review-button-{{ review.review_id }}` navigates to `write_review_page(book_id=review.book_id)`
  - `delete-review-button-{{ review.review_id }}` triggers POST to delete review function (e.g., `delete_review(review_id=review.review_id)`)
  - `back-to-dashboard` navigates to `dashboard_page`

### 8. write_review.html
- **Path:** templates/write_review.html
- **Page Title:** Write Review
- **Element IDs:**
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- **Context Variables:**
  - `book` (dict)
  - `existing_review` (dict or None)
- **Navigation:**
  - `submit-review-button` triggers POST to `submit_review(book_id=book.book_id)`
  - `back-to-book` navigates to `book_details_page(book_id=book.book_id)`

### 9. profile.html
- **Path:** templates/profile.html
- **Page Title:** My Profile
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
  - `borrow_history` (list of dict: book_title, borrow_date, return_date, status)
- **Navigation:**
  - `update-profile-button` triggers POST to `update_profile`
  - `back-to-dashboard` navigates to `dashboard_page`

### 10. payment_confirmation.html
- **Path:** templates/payment_confirmation.html
- **Page Title:** Payment Confirmation
- **Element IDs:**
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- **Context Variables:**
  - `fine` (dict: fine_id, amount, status)
- **Navigation:**
  - `confirm-payment-button` triggers POST to `confirm_payment(fine_id=fine.fine_id)`
  - `back-to-profile` navigates to `user_profile_page`

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- **Path:** data/users.txt
- **Fields (Pipe-delimited):**
  1. `username` (str)
  2. `email` (str)
  3. `phone` (str)
  4. `address` (str)
- **Description:** Stores user profile information including contact details.
- **Example Rows:**
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`

### 2. books.txt
- **Path:** data/books.txt
- **Fields (Pipe-delimited):**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `genre` (str)
  6. `publisher` (str)
  7. `year` (int)
  8. `description` (str)
  9. `status` (str): "Available", "Borrowed", "Reserved"
  10. `avg_rating` (float)
- **Description:** Stores book catalog details with current availability and average rating.
- **Example Rows:**
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  - `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`

### 3. borrowings.txt
- **Path:** data/borrowings.txt
- **Fields (Pipe-delimited):**
  1. `borrow_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `borrow_date` (str, YYYY-MM-DD)
  5. `due_date` (str, YYYY-MM-DD)
  6. `return_date` (str, YYYY-MM-DD or empty)
  7. `status` (str): "Active", "Returned", "Overdue"
  8. `fine_amount` (float)
- **Description:** Records each borrowing transaction with status and fines.
- **Example Rows:**
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`

### 4. reservations.txt
- **Path:** data/reservations.txt
- **Fields (Pipe-delimited):**
  1. `reservation_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `reservation_date` (str, YYYY-MM-DD)
  5. `status` (str): "Active", "Cancelled"
- **Description:** Tracks book reservations by users with current status.
- **Example Rows:**
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`

### 5. reviews.txt
- **Path:** data/reviews.txt
- **Fields (Pipe-delimited):**
  1. `review_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `rating` (int) (1-5)
  5. `review_text` (str)
  6. `review_date` (str, YYYY-MM-DD)
- **Description:** Stores user reviews and ratings for books.
- **Example Rows:**
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`

### 6. fines.txt
- **Path:** data/fines.txt
- **Fields (Pipe-delimited):**
  1. `fine_id` (int)
  2. `username` (str)
  3. `borrow_id` (int)
  4. `amount` (float)
  5. `status` (str): "Unpaid", "Paid"
  6. `date_issued` (str, YYYY-MM-DD)
- **Description:** Maintains records of fines issued for overdue borrowings.
- **Example Rows:**
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`
