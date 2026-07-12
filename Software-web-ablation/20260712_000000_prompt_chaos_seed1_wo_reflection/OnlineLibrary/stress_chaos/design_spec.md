# OnlineLibrary Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

1. **Root Route**
   - URL Path: `/`
   - Function Name: `root_redirect`
   - HTTP Method: GET
   - Action: Redirects to dashboard page

2. **Dashboard Page**
   - URL Path: `/dashboard`
   - Function Name: `dashboard`
   - HTTP Method: GET
   - Template: `dashboard.html`
   - Context Variables:
     - `username` (str): The current logged-in user's username to display welcome message.

3. **Book Catalog Page**
   - URL Path: `/catalog`
   - Function Name: `book_catalog`
   - HTTP Method: GET
   - Template: `catalog.html`
   - Context Variables:
     - `books` (list of dict): List of all books with fields:
       - `book_id` (int)
       - `title` (str)
       - `author` (str)
       - `status` (str)  # e.g., Available, Borrowed, Reserved

4. **Book Details Page**
   - URL Path: `/book/<int:book_id>`
   - Function Name: `book_details`
   - HTTP Method: GET
   - Template: `book_details.html`
   - Context Variables:
     - `book` (dict): Detailed book data with keys:
       - `book_id` (int)
       - `title` (str)
       - `author` (str)
       - `status` (str)
       - `description` (str)
       - `avg_rating` (float)
     - `reviews` (list of dict): List of reviews for the book; each review with:
       - `review_id` (int)
       - `username` (str)
       - `rating` (int)
       - `review_text` (str)
       - `review_date` (str)

5. **Borrow Confirmation Page (GET)**
   - URL Path: `/borrow/<int:book_id>`
   - Function Name: `borrow_confirmation`
   - HTTP Method: GET
   - Template: `borrow_confirmation.html`
   - Context Variables:
     - `book` (dict): Book information (same keys as in book_details)
     - `due_date` (str): Computed due date string (14 days from current date)

6. **Borrow Confirmation Page (POST)**
   - URL Path: `/borrow/<int:book_id>`
   - Function Name: `confirm_borrow`
   - HTTP Method: POST
   - Action: Processes borrow request, updates borrowings.txt
   - Redirects: To My Borrowings page or confirmation display

7. **My Borrowings Page**
   - URL Path: `/my_borrows`
   - Function Name: `my_borrowings`
   - HTTP Method: GET
   - Template: `my_borrows.html`
   - Context Variables:
     - `borrowings` (list of dict): List of borrow records for current user with keys:
       - `borrow_id` (int)
       - `book_id` (int)
       - `title` (str)  # book title
       - `borrow_date` (str)
       - `due_date` (str)
       - `status` (str)  # Active, Returned, Overdue
       - `fine_amount` (float)

8. **Return Borrowed Book (POST)**
   - URL Path: `/return/<int:borrow_id>`
   - Function Name: `return_book`
   - HTTP Method: POST
   - Action: Processes returning book, updates borrowings, possibly fines
   - Redirects: To My Borrowings page

9. **My Reservations Page**
   - URL Path: `/my_reservations`
   - Function Name: `my_reservations`
   - HTTP Method: GET
   - Template: `my_reservations.html`
   - Context Variables:
     - `reservations` (list of dict): List of reservations for user with keys:
       - `reservation_id` (int)
       - `book_id` (int)
       - `title` (str)
       - `reservation_date` (str)
       - `status` (str)  # Active, Cancelled

10. **Cancel Reservation (POST)**
    - URL Path: `/cancel_reservation/<int:reservation_id>`
    - Function Name: `cancel_reservation`
    - HTTP Method: POST
    - Action: Cancel reservation
    - Redirects: To My Reservations page

11. **My Reviews Page**
    - URL Path: `/my_reviews`
    - Function Name: `my_reviews`
    - HTTP Method: GET
    - Template: `my_reviews.html`
    - Context Variables:
      - `reviews` (list of dict): Reviews by user, each review with:
        - `review_id` (int)
        - `book_id` (int)
        - `title` (str)
        - `rating` (int)
        - `review_text` (str)

12. **Write Review Page (GET)**
    - URL Path: `/review/<int:book_id>`
    - Function Name: `write_review`
    - HTTP Method: GET
    - Template: `write_review.html`
    - Context Variables:
      - `book` (dict): Book info with keys:
        - `book_id` (int)
        - `title` (str)
      - `existing_review` (dict or None): Review by current user if exists with:
        - `review_id` (int)
        - `rating` (int)
        - `review_text` (str)

13. **Write Review Page (POST)**
    - URL Path: `/review/<int:book_id>`
    - Function Name: `submit_review`
    - HTTP Method: POST
    - Action: Add or update review
    - Redirects: To Book Details page

14. **User Profile Page**
    - URL Path: `/profile`
    - Function Name: `profile`
    - HTTP Method: GET
    - Template: `profile.html`
    - Context Variables:
      - `username` (str)
      - `email` (str)
      - `borrow_history` (list of dict): All previously borrowed books:
        - `borrow_id` (int)
        - `book_id` (int)
        - `title` (str)
        - `borrow_date` (str)
        - `return_date` (str or None)

15. **Update Profile (POST)**
    - URL Path: `/profile`
    - Function Name: `update_profile`
    - HTTP Method: POST
    - Action: Update user profile email
    - Redirects: To Profile page

16. **Payment Confirmation Page (GET)**
    - URL Path: `/payment/<int:fine_id>`
    - Function Name: `payment_confirmation`
    - HTTP Method: GET
    - Template: `payment_confirmation.html`
    - Context Variables:
      - `fine` (dict): Details of fine with keys:
        - `fine_id` (int)
        - `amount` (float)

17. **Payment Confirmation (POST)**
    - URL Path: `/payment/<int:fine_id>`
    - Function Name: `confirm_payment`
    - HTTP Method: POST
    - Action: Processes fine payment
    - Redirects: To Profile page

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. dashboard.html
- Path: `templates/dashboard.html`
- Page Title: `Library Dashboard`
- Elements:
  - `dashboard-page` (div)
  - `welcome-message` (h1)
  - `browse-books-button` (button)
  - `my-borrows-button` (button)
- Context Variables:
  - `username` (str)
- Navigation:
  - `browse-books-button` action: url_for('book_catalog')
  - `my-borrows-button` action: url_for('my_borrowings')

### 2. catalog.html
- Path: `templates/catalog.html`
- Page Title: `Book Catalog`
- Elements:
  - `catalog-page` (div)
  - `search-input` (input)
  - `book-grid` (div)
  - `view-book-button-{{ book.book_id }}` (button) - dynamic per book
  - `back-to-dashboard` (button)
- Context Variables:
  - `books` (list of dict) each with:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
- Navigation:
  - `view-book-button-{{ book.book_id }}` action: url_for('book_details', book_id=book.book_id)
  - `back-to-dashboard` action: url_for('dashboard')

### 3. book_details.html
- Path: `templates/book_details.html`
- Page Title: `Book Details`
- Elements:
  - `book-details-page` (div)
  - `book-title` (h1)
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button)
  - `reviews-section` (div)
  - `write-review-button` (button)
  - `back-to-catalog` (button)
- Context Variables:
  - `book` (dict) with keys: book_id, title, author, status, description, avg_rating
  - `reviews` (list of dict) with keys: review_id, username, rating, review_text, review_date
- Navigation:
  - `borrow-button` action: url_for('borrow_confirmation', book_id=book.book_id)
  - `write-review-button` action: url_for('write_review', book_id=book.book_id)
  - `back-to-catalog` action: url_for('book_catalog')

### 4. borrow_confirmation.html
- Path: `templates/borrow_confirmation.html`
- Page Title: `Borrow Confirmation`
- Elements:
  - `borrow-page` (div)
  - `borrow-book-info` (div)
  - `due-date-display` (div)
  - `confirm-borrow-button` (button)
  - `cancel-borrow-button` (button)
- Context Variables:
  - `book` (dict)
  - `due_date` (str)
- Navigation:
  - `confirm-borrow-button` form submission: POST to url_for('confirm_borrow', book_id=book.book_id)
  - `cancel-borrow-button` action: url_for('book_details', book_id=book.book_id)

### 5. my_borrows.html
- Path: `templates/my_borrows.html`
- Page Title: `My Borrowings`
- Elements:
  - `my-borrows-page` (div)
  - `filter-status` (dropdown)
  - `borrows-table` (table)
  - `return-book-button-{{ borrow.borrow_id }}` (button) dynamic
  - `back-to-dashboard` (button)
- Context Variables:
  - `borrowings` (list of dict) with keys: borrow_id, book_id, title, borrow_date, due_date, status, fine_amount
- Navigation:
  - `return-book-button-{{ borrow.borrow_id }}` form POST action to url_for('return_book', borrow_id=borrow.borrow_id)
  - `back-to-dashboard` action: url_for('dashboard')

### 6. my_reservations.html
- Path: `templates/my_reservations.html`
- Page Title: `My Reservations`
- Elements:
  - `reservations-page` (div)
  - `reservations-table` (table)
  - `cancel-reservation-button-{{ reservation.reservation_id }}` (button) dynamic
  - `back-to-dashboard` (button)
- Context Variables:
  - `reservations` (list of dict) with keys: reservation_id, book_id, title, reservation_date, status
- Navigation:
  - `cancel-reservation-button-{{ reservation.reservation_id }}` form POST to url_for('cancel_reservation', reservation_id=reservation.reservation_id)
  - `back-to-dashboard` action: url_for('dashboard')

### 7. my_reviews.html
- Path: `templates/my_reviews.html`
- Page Title: `My Reviews`
- Elements:
  - `reviews-page` (div)
  - `reviews-list` (div)
  - `edit-review-button-{{ review.review_id }}` (button)
  - `delete-review-button-{{ review.review_id }}` (button)
  - `back-to-dashboard` (button)
- Context Variables:
  - `reviews` (list of dict) with keys: review_id, book_id, title, rating, review_text
- Navigation:
  - `edit-review-button-{{ review.review_id }}` action: url_for('write_review', book_id=review.book_id)
  - `delete-review-button-{{ review.review_id }}` form POST to url_for('delete_review', review_id=review.review_id)
  - `back-to-dashboard` action: url_for('dashboard')

### 8. write_review.html
- Path: `templates/write_review.html`
- Page Title: `Write Review`
- Elements:
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown)
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- Context Variables:
  - `book` (dict) with keys: book_id, title
  - `existing_review` (dict or None) with keys: review_id, rating, review_text
- Navigation:
  - `submit-review-button` form POST to url_for('submit_review', book_id=book.book_id)
  - `back-to-book` action: url_for('book_details', book_id=book.book_id)

### 9. profile.html
- Path: `templates/profile.html`
- Page Title: `My Profile`
- Elements:
  - `profile-page` (div)
  - `profile-username` (div)
  - `profile-email` (input)
  - `update-profile-button` (button)
  - `borrow-history` (div)
  - `back-to-dashboard` (button)
- Context Variables:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict) with keys: borrow_id, book_id, title, borrow_date, return_date
- Navigation:
  - `update-profile-button` form POST to url_for('update_profile')
  - `back-to-dashboard` action: url_for('dashboard')

### 10. payment_confirmation.html
- Path: `templates/payment_confirmation.html`
- Page Title: `Payment Confirmation`
- Elements:
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- Context Variables:
  - `fine` (dict) with keys: fine_id, amount
- Navigation:
  - `confirm-payment-button` form POST to url_for('confirm_payment', fine_id=fine.fine_id)
  - `back-to-profile` action: url_for('profile')

---

## Section 3: Data File Schemas (Backend Development)

1. **users.txt** (data/users.txt)
- Fields (pipe `|` delimited):
  - `username` (str)
  - `email` (str)
  - `phone` (str)
  - `address` (str)
- Description: Stores user personal information.
- Example Rows:
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`

2. **books.txt** (data/books.txt)
- Fields (pipe `|` delimited):
  - `book_id` (int)
  - `title` (str)
  - `author` (str)
  - `isbn` (str)
  - `genre` (str)
  - `publisher` (str)
  - `year` (int)
  - `description` (str)
  - `status` (str)  # Available, Borrowed, Reserved
  - `avg_rating` (float)
- Description: Stores detailed book information.
- Example Rows:
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  - `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`

3. **borrowings.txt** (data/borrowings.txt)
- Fields (pipe `|` delimited):
  - `borrow_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `borrow_date` (str, ISO 8601 date, e.g., "YYYY-MM-DD")
  - `due_date` (str, ISO 8601 date)
  - `return_date` (str or empty if not returned)
  - `status` (str)  # Active, Returned, Overdue
  - `fine_amount` (float)
- Description: Stores records of book borrowings.
- Example Rows:
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`

4. **reservations.txt** (data/reservations.txt)
- Fields (pipe `|` delimited):
  - `reservation_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `reservation_date` (str, ISO 8601 date)
  - `status` (str)  # Active, Cancelled
- Description: Stores book reservation data.
- Example Rows:
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`

5. **reviews.txt** (data/reviews.txt)
- Fields (pipe `|` delimited):
  - `review_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `rating` (int)
  - `review_text` (str)
  - `review_date` (str, ISO 8601 date)
- Description: Stores user reviews of books.
- Example Rows:
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`

6. **fines.txt** (data/fines.txt)
- Fields (pipe `|` delimited):
  - `fine_id` (int)
  - `username` (str)
  - `borrow_id` (int)
  - `amount` (float)
  - `status` (str)  # Unpaid, Paid
  - `date_issued` (str, ISO 8601 date)
- Description: Stores overdue fine data.
- Example Rows:
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`
