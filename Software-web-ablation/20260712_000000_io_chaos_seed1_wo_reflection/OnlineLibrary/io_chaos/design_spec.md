# OnlineLibrary Design Specification Document

---

## Section 1: Flask Routes Specification (Backend Development)

### Root Redirect
- **URL Path:** /
- **Function Name:** root_redirect
- **HTTP Method:** GET
- **Template Rendered:** Redirects to dashboard
- **Context Variables:** None

### 1. Dashboard Page
- **URL Path:** /dashboard
- **Function Name:** dashboard_page
- **HTTP Method:** GET
- **Template Rendered:** dashboard.html
- **Context Variables:**
  - username (str): The logged-in user's username
  - featured_books (list of dict): Featured books details, each dict with keys: book_id (int), title (str), author (str), status (str)

### 2. Book Catalog Page
- **URL Path:** /catalog
- **Function Name:** book_catalog_page
- **HTTP Method:** GET
- **Template Rendered:** catalog.html
- **Context Variables:**
  - books (list of dict): List of all available books, each dict containing: book_id (int), title (str), author (str), status (str)
  - search_query (str): Current search/filter query string if any

### 3. Book Details Page
- **URL Path:** /book/<int:book_id>
- **Function Name:** book_details_page
- **HTTP Method:** GET
- **Template Rendered:** book_details.html
- **Context Variables:**
  - book (dict): Book details with keys: book_id (int), title (str), author (str), status (str), description (str), avg_rating (float)
  - reviews (list of dict): List of reviews for the book, each dict: review_id (int), username (str), rating (int), review_text (str), review_date (str)
  - username (str): Current logged in user's username

### 4. Borrow Confirmation Page
- **URL Path:** /borrow/<int:book_id>
- **Function Name:** borrow_confirmation_page
- **HTTP Method:** GET
- **Template Rendered:** borrow_confirmation.html
- **Context Variables:**
  - book (dict): Book details as in book_details_page context
  - due_date (str): Due date string (14 days from current date)

- **URL Path:** /borrow/<int:book_id>/confirm
- **Function Name:** confirm_borrow
- **HTTP Method:** POST
- **Template Rendered:** borrow_success.html or borrow_confirmation.html on failure
- **Context Variables:**
  - book (dict): Book details
  - borrow_id (int): Identifier for the borrowing record
  - due_date (str): Due date
  - message (str): Success or error message

- **URL Path:** /borrow/<int:book_id>/cancel
- **Function Name:** cancel_borrow
- **HTTP Method:** POST
- **Template Rendered:** Redirect to book_details_page
- **Context Variables:** None

### 5. My Borrowings Page
- **URL Path:** /my-borrows
- **Function Name:** my_borrowings_page
- **HTTP Method:** GET
- **Template Rendered:** my_borrows.html
- **Context Variables:**
  - borrows (list of dict): Borrow records for current user; each dict with keys: borrow_id (int), book_title (str), borrow_date (str), due_date (str), status (str), fine_amount (float)
  - filter_status (str): Current filter selected (All, Active, Returned, Overdue)

- **URL Path:** /return/<int:borrow_id>
- **Function Name:** return_book
- **HTTP Method:** POST
- **Template Rendered:** return_confirmation.html or my_borrows.html on failure
- **Context Variables:**
  - borrow_id (int): The borrow record ID
  - message (str): Success or error message

### 6. My Reservations Page
- **URL Path:** /my-reservations
- **Function Name:** my_reservations_page
- **HTTP Method:** GET
- **Template Rendered:** my_reservations.html
- **Context Variables:**
  - reservations (list of dict): List of user's reservations; each dict with keys: reservation_id (int), book_title (str), reservation_date (str), status (str)

- **URL Path:** /cancel-reservation/<int:reservation_id>
- **Function Name:** cancel_reservation
- **HTTP Method:** POST
- **Template Rendered:** my_reservations.html or redirect with message
- **Context Variables:**
  - message (str): Confirmation or error message

### 7. My Reviews Page
- **URL Path:** /my-reviews
- **Function Name:** my_reviews_page
- **HTTP Method:** GET
- **Template Rendered:** my_reviews.html
- **Context Variables:**
  - reviews (list of dict): User's reviews; each dict with keys: review_id (int), book_title (str), rating (int), review_text (str), review_date (str)

- **URL Path:** /review/edit/<int:review_id>
- **Function Name:** edit_review_page
- **HTTP Method:** GET
- **Template Rendered:** write_review.html
- **Context Variables:**
  - review (dict): Review details with keys: review_id (int), book_id (int), rating (int), review_text (str)
  - book (dict): Book details

- **URL Path:** /review/edit/<int:review_id>
- **Function Name:** submit_review_edit
- **HTTP Method:** POST
- **Template Rendered:** Redirect to my_reviews or write_review.html on error
- **Context Variables:**
  - message (str): Success or error message

- **URL Path:** /review/delete/<int:review_id>
- **Function Name:** delete_review
- **HTTP Method:** POST
- **Template Rendered:** Redirect to my_reviews with message
- **Context Variables:**
  - message (str): Confirmation or error message

### 8. Write Review Page
- **URL Path:** /review/write/<int:book_id>
- **Function Name:** write_review_page
- **HTTP Method:** GET
- **Template Rendered:** write_review.html
- **Context Variables:**
  - book (dict): Book details

- **URL Path:** /review/write/<int:book_id>
- **Function Name:** submit_review
- **HTTP Method:** POST
- **Template Rendered:** Redirect to book_details_page or write_review.html on error
- **Context Variables:**
  - message (str): Success or error message

### 9. User Profile Page
- **URL Path:** /profile
- **Function Name:** user_profile_page
- **HTTP Method:** GET
- **Template Rendered:** profile.html
- **Context Variables:**
  - user (dict): User profile info with keys: username (str), email (str), phone (str), address (str)
  - borrow_history (list of dict): List of all previously borrowed books by user; each dict with keys: book_title (str), borrow_date (str), return_date (str), status (str)

- **URL Path:** /profile/update
- **Function Name:** update_profile
- **HTTP Method:** POST
- **Template Rendered:** profile.html with success or error message context
- **Context Variables:**
  - message (str)

### 10. Payment Confirmation Page
- **URL Path:** /payment/<int:fine_id>
- **Function Name:** payment_confirmation_page
- **HTTP Method:** GET
- **Template Rendered:** payment_confirmation.html
- **Context Variables:**
  - fine (dict): Fine details with keys: fine_id (int), amount (float), status (str), date_issued (str)

- **URL Path:** /payment/<int:fine_id>/confirm
- **Function Name:** confirm_payment
- **HTTP Method:** POST
- **Template Rendered:** profile.html or payment_confirmation.html on failure
- **Context Variables:**
  - message (str)

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. dashboard.html (templates/dashboard.html)
- **Page Title:** Library Dashboard
- **Element IDs:**
  - dashboard-page (div)
  - welcome-message (h1)
  - browse-books-button (button)
  - my-borrows-button (button)
- **Context Variables:**
  - username (str)
  - featured_books (list of dict): book_id (int), title (str), author (str), status (str)
- **Navigation:**
  - browse-books-button → url_for('book_catalog_page')
  - my-borrows-button → url_for('my_borrowings_page')

### 2. catalog.html (templates/catalog.html)
- **Page Title:** Book Catalog
- **Element IDs:**
  - catalog-page (div)
  - search-input (input)
  - book-grid (div)
  - view-book-button-{book_id} (button, dynamic per book)
  - back-to-dashboard (button)
- **Context Variables:**
  - books (list of dict): book_id (int), title (str), author (str), status (str)
  - search_query (str)
- **Navigation:**
  - view-book-button-{book_id} → url_for('book_details_page', book_id=book_id)
  - back-to-dashboard → url_for('dashboard_page')

### 3. book_details.html (templates/book_details.html)
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
  - book (dict): book_id (int), title (str), author (str), status (str), description (str), avg_rating (float)
  - reviews (list of dict): review_id (int), username (str), rating (int), review_text (str), review_date (str)
  - username (str)
- **Navigation:**
  - borrow-button → url_for('borrow_confirmation_page', book_id=book['book_id'])
  - write-review-button → url_for('write_review_page', book_id=book['book_id'])
  - back-to-catalog → url_for('book_catalog_page')

### 4. borrow_confirmation.html (templates/borrow_confirmation.html)
- **Page Title:** Borrow Confirmation
- **Element IDs:**
  - borrow-page (div)
  - borrow-book-info (div)
  - due-date-display (div)
  - confirm-borrow-button (button)
  - cancel-borrow-button (button)
- **Context Variables:**
  - book (dict)
  - due_date (str)
- **Navigation:**
  - confirm-borrow-button → form POST to url_for('confirm_borrow', book_id=book['book_id'])
  - cancel-borrow-button → form POST to url_for('cancel_borrow', book_id=book['book_id'])

### 5. my_borrows.html (templates/my_borrows.html)
- **Page Title:** My Borrowings
- **Element IDs:**
  - my-borrows-page (div)
  - filter-status (dropdown)
  - borrows-table (table)
  - return-book-button-{borrow_id} (button, dynamic per active borrow)
  - back-to-dashboard (button)
- **Context Variables:**
  - borrows (list of dict): borrow_id (int), book_title (str), borrow_date (str), due_date (str), status (str), fine_amount (float)
  - filter_status (str)
- **Navigation:**
  - return-book-button-{borrow_id} → form POST to url_for('return_book', borrow_id=borrow_id)
  - back-to-dashboard → url_for('dashboard_page')

### 6. my_reservations.html (templates/my_reservations.html)
- **Page Title:** My Reservations
- **Element IDs:**
  - reservations-page (div)
  - reservations-table (table)
  - cancel-reservation-button-{reservation_id} (button, dynamic)
  - back-to-dashboard (button)
- **Context Variables:**
  - reservations (list of dict): reservation_id (int), book_title (str), reservation_date (str), status (str)
- **Navigation:**
  - cancel-reservation-button-{reservation_id} → form POST to url_for('cancel_reservation', reservation_id=reservation_id)
  - back-to-dashboard → url_for('dashboard_page')

### 7. my_reviews.html (templates/my_reviews.html)
- **Page Title:** My Reviews
- **Element IDs:**
  - reviews-page (div)
  - reviews-list (div)
  - edit-review-button-{review_id} (button, dynamic)
  - delete-review-button-{review_id} (button, dynamic)
  - back-to-dashboard (button)
- **Context Variables:**
  - reviews (list of dict): review_id (int), book_title (str), rating (int), review_text (str), review_date (str)
- **Navigation:**
  - edit-review-button-{review_id} → url_for('edit_review_page', review_id=review_id)
  - delete-review-button-{review_id} → form POST to url_for('delete_review', review_id=review_id)
  - back-to-dashboard → url_for('dashboard_page')

### 8. write_review.html (templates/write_review.html)
- **Page Title:** Write Review
- **Element IDs:**
  - write-review-page (div)
  - book-info-display (div)
  - rating-input (dropdown)
  - review-text (textarea)
  - submit-review-button (button)
  - back-to-book (button)
- **Context Variables:**
  - book (dict)
- **Navigation:**
  - submit-review-button → form POST to url_for('submit_review', book_id=book['book_id'])
  - back-to-book → url_for('book_details_page', book_id=book['book_id'])

### 9. profile.html (templates/profile.html)
- **Page Title:** My Profile
- **Element IDs:**
  - profile-page (div)
  - profile-username (div)
  - profile-email (input)
  - update-profile-button (button)
  - borrow-history (div)
  - back-to-dashboard (button)
- **Context Variables:**
  - user (dict): username (str), email (str), phone (str), address (str)
  - borrow_history (list of dict): Each dict with book_title (str), borrow_date (str), return_date (str), status (str)
- **Navigation:**
  - update-profile-button → form POST to url_for('update_profile')
  - back-to-dashboard → url_for('dashboard_page')

### 10. payment_confirmation.html (templates/payment_confirmation.html)
- **Page Title:** Payment Confirmation
- **Element IDs:**
  - payment-page (div)
  - fine-amount-display (div)
  - confirm-payment-button (button)
  - back-to-profile (button)
- **Context Variables:**
  - fine (dict): fine_id (int), amount (float), status (str), date_issued (str)
- **Navigation:**
  - confirm-payment-button → form POST to url_for('confirm_payment', fine_id=fine['fine_id'])
  - back-to-profile → url_for('user_profile_page')

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt (data/users.txt)
- **Fields:** username|email|phone|address
- **Description:** Stores registered user details including contact information.
- **Example Data:**
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```

### 2. books.txt (data/books.txt)
- **Fields:** book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating
- **Description:** Stores detailed book information including availability status and average rating.
- **Example Data:**
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5
  5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3
  ```

### 3. borrowings.txt (data/borrowings.txt)
- **Fields:** borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount
- **Description:** Records all borrow transactions with return status and fines if any.
- **Example Data:**
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
  ```

### 4. reservations.txt (data/reservations.txt)
- **Fields:** reservation_id|username|book_id|reservation_date|status
- **Description:** Stores records of user reservations for books with statuses.
- **Example Data:**
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```

### 5. reviews.txt (data/reviews.txt)
- **Fields:** review_id|username|book_id|rating|review_text|review_date
- **Description:** Contains user reviews for books, including rating and review text.
- **Example Data:**
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```

### 6. fines.txt (data/fines.txt)
- **Fields:** fine_id|username|borrow_id|amount|status|date_issued
- **Description:** Tracks fines issued for overdue borrowings with payment status.
- **Example Data:**
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
  ```

-- End of Design Specification --
