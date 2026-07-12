# OnlineLibrary Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

1. **Root Route**
   - URL Path: `/`
   - Function Name: `root_redirect`
   - HTTP Method: GET
   - Action: Redirects to `/dashboard`

2. **Dashboard Page**
   - URL Path: `/dashboard`
   - Function Name: `dashboard`
   - HTTP Method: GET
   - Template: `dashboard.html`
   - Context Variables:
     - `username` (str) : Current logged-in username
     - `welcome_message` (str) : Welcome message string

3. **Book Catalog Page**
   - URL Path: `/catalog`
   - Function Name: `book_catalog`
   - HTTP Method: GET
   - Template: `catalog.html`
   - Context Variables:
     - `books` (list of dict) : List of books with keys `book_id`(int), `title`(str), `author`(str), `status`(str)
     - `search_query` (str) : Current search query (empty string if none)

4. **Book Details Page**
   - URL Path: `/book/<int:book_id>`
   - Function Name: `book_details`
   - HTTP Method: GET
   - Template: `book_details.html`
   - Context Variables:
     - `book` (dict): Book detail with keys `book_id`(int), `title`(str), `author`(str), `status`(str), plus other metadata
     - `reviews` (list of dict): List of reviews for the book, each with keys `review_id`(int), `username`(str), `rating`(int), `review_text`(str), `review_date`(str)
     - `username` (str) : Current logged-in user

5. **Borrow Confirmation Page**
   - URL Path: `/borrow/<int:book_id>`
   - Function Name: `borrow_confirmation`
   - HTTP Method: GET, POST
   - GET Template: `borrow_confirmation.html`
   - POST: Processes borrow confirmation form submission
   - Context Variables (GET):
     - `book` (dict): Book to borrow details
     - `due_date` (str): Due date string (14 days from borrow date)
     - `username` (str): Current logged-in user

6. **Borrow Book Action**
   - URL Path: `/borrow/confirm/<int:book_id>`
   - Function Name: `confirm_borrow`
   - HTTP Method: POST
   - Action: Processes borrow confirmation submission, updates data files

7. **Cancel Borrow Action**
   - URL Path: `/borrow/cancel/<int:book_id>`
   - Function Name: `cancel_borrow`
   - HTTP Method: POST
   - Action: Redirect back to book details page

8. **My Borrowings Page**
   - URL Path: `/my-borrows`
   - Function Name: `my_borrowings`
   - HTTP Method: GET
   - Template: `my_borrows.html`
   - Context Variables:
     - `borrowings` (list of dict): Borrowed books with keys `borrow_id`(int), `book_title`(str), `borrow_date`(str), `due_date`(str), `status`(str)
     - `filter_status` (str): Current filter status (All/Active/Returned/Overdue)

9. **Return Book Confirmation Page**
   - URL Path: `/return/<int:borrow_id>`
   - Function Name: `return_book_confirmation`
   - HTTP Method: GET, POST
   - GET Template: `return_confirmation.html`
   - POST: Processes book return confirmation
   - Context Variables (GET):
     - `borrow` (dict): Borrow record details
     - `book` (dict): Book details
     - `username` (str): Current logged-in user

10. **Confirm Return Action**
    - URL Path: `/return/confirm/<int:borrow_id>`
    - Function Name: `confirm_return`
    - HTTP Method: POST
    - Action: Processes return confirmation, updates data files

11. **Cancel Return Action**
    - URL Path: `/return/cancel/<int:borrow_id>`
    - Function Name: `cancel_return`
    - HTTP Method: POST
    - Action: Redirect back to My Borrowings page

12. **My Reservations Page**
    - URL Path: `/my-reservations`
    - Function Name: `my_reservations`
    - HTTP Method: GET
    - Template: `my_reservations.html`
    - Context Variables:
      - `reservations` (list of dict): Reservations with keys `reservation_id`(int), `book_title`(str), `reservation_date`(str), `status`(str)

13. **Cancel Reservation Action**
    - URL Path: `/reservation/cancel/<int:reservation_id>`
    - Function Name: `cancel_reservation`
    - HTTP Method: POST
    - Action: Process cancellation and update data files

14. **My Reviews Page**
    - URL Path: `/my-reviews`
    - Function Name: `my_reviews`
    - HTTP Method: GET
    - Template: `my_reviews.html`
    - Context Variables:
      - `reviews` (list of dict): User reviews with keys `review_id`(int), `book_title`(str), `rating`(int), `review_text`(str)

15. **Write Review Page**
    - URL Path: `/review/write/<int:book_id>`
    - Function Name: `write_review`
    - HTTP Method: GET, POST
    - GET Template: `write_review.html`
    - POST: Process review submission
    - Context Variables (GET):
      - `book` (dict): Book details
      - `existing_review` (dict or None): Existing review by user if editing

16. **Edit Review Action**
    - URL Path: `/review/edit/<int:review_id>`
    - Function Name: `edit_review`
    - HTTP Method: GET, POST
    - GET Template: `write_review.html`
    - POST: Process editing submission
    - Context Variables (GET):
      - `review` (dict): Review details
      - `book` (dict): Book details

17. **Delete Review Action**
    - URL Path: `/review/delete/<int:review_id>`
    - Function Name: `delete_review`
    - HTTP Method: POST
    - Action: Process review deletion

18. **User Profile Page**
    - URL Path: `/profile`
    - Function Name: `user_profile`
    - HTTP Method: GET, POST
    - GET Template: `profile.html`
    - POST: Process profile update
    - Context Variables (GET):
      - `user` (dict): User profile data with keys `username`, `email`, `phone`, `address`
      - `borrow_history` (list of dict): Past borrowed books with keys `book_title`(str), `borrow_date`(str), `return_date`(str)

19. **Payment Confirmation Page**
    - URL Path: `/payment/<int:fine_id>`
    - Function Name: `payment_confirmation`
    - HTTP Method: GET, POST
    - GET Template: `payment_confirmation.html`
    - POST: Process payment confirmation
    - Context Variables (GET):
      - `fine` (dict): Fine details with keys `fine_id`(int), `username`(str), `amount`(float), `status`(str)

---

## Section 2: HTML Template Specifications (Frontend Development)

### 1. dashboard.html
- Path: `templates/dashboard.html`
- Page Title: "Library Dashboard"
- Elements:
  - `dashboard-page` (Div)
  - `welcome-message` (H1) shows welcome message with username
  - `browse-books-button` (Button) navigates to `book_catalog` route
  - `my-borrows-button` (Button) navigates to `my_borrowings` route
- Context Variables:
  - `username` (str)
  - `welcome_message` (str)
- Navigation url_for mappings:
  - Browse Books Button: `url_for('book_catalog')`
  - My Borrows Button: `url_for('my_borrowings')`

### 2. catalog.html
- Path: `templates/catalog.html`
- Page Title: "Book Catalog"
- Elements:
  - `catalog-page` (Div)
  - `search-input` (Input) for text search
  - `book-grid` (Div) containing list of books
  - `view-book-button-{book_id}` (Button) dynamic id per book
  - `back-to-dashboard` (Button) goes to `dashboard`
- Context Variables:
  - `books` (list of dict with keys `book_id`(int), `title`(str), `author`(str), `status`(str))
  - `search_query` (str)
- Navigation url_for mappings:
  - View Book Button: `url_for('book_details', book_id=book.book_id)`
  - Back to Dashboard: `url_for('dashboard')`

### 3. book_details.html
- Path: `templates/book_details.html`
- Page Title: "Book Details"
- Elements:
  - `book-details-page` (Div)
  - `book-title` (H1)
  - `book-author` (Div)
  - `book-status` (Div)
  - `borrow-button` (Button)
  - `reviews-section` (Div)
  - `write-review-button` (Button)
  - `back-to-catalog` (Button)
- Context Variables:
  - `book` (dict)
  - `reviews` (list of dict)
  - `username` (str)
- Navigation url_for mappings:
  - Borrow Button: `url_for('borrow_confirmation', book_id=book.book_id)`
  - Write Review Button: `url_for('write_review', book_id=book.book_id)`
  - Back to Catalog: `url_for('book_catalog')`

### 4. borrow_confirmation.html
- Path: `templates/borrow_confirmation.html`
- Page Title: "Borrow Confirmation"
- Elements:
  - `borrow-page` (Div)
  - `borrow-book-info` (Div)
  - `due-date-display` (Div)
  - `confirm-borrow-button` (Button), form method POST, action `/borrow/confirm/<book_id>`
  - `cancel-borrow-button` (Button), form method POST, action `/borrow/cancel/<book_id>`
- Context Variables:
  - `book` (dict)
  - `due_date` (str)
  - `username` (str)
- Navigation url_for mappings:
  - Cancel Borrow Button: `url_for('cancel_borrow', book_id=book.book_id)`

### 5. my_borrows.html
- Path: `templates/my_borrows.html`
- Page Title: "My Borrowings"
- Elements:
  - `my-borrows-page` (Div)
  - `filter-status` (Dropdown) with options All, Active, Returned, Overdue
  - `borrows-table` (Table)
  - `return-book-button-{borrow_id}` (Button) dynamic id per active borrow
  - `back-to-dashboard` (Button)
- Context Variables:
  - `borrowings` (list of dict)
  - `filter_status` (str)
- Navigation url_for mappings:
  - Return Book Button: `url_for('return_book_confirmation', borrow_id=borrow.borrow_id)`
  - Back to Dashboard: `url_for('dashboard')`

### 6. return_confirmation.html
- Path: `templates/return_confirmation.html`
- Page Title: "Return Confirmation"
- Elements:
  - `return-confirmation-page` (Div) (container assumed)
  - `borrow-info` (Div) (shows borrow details)
  - `confirm-return-button` (Button), form method POST, action `/return/confirm/<borrow_id>`
  - `cancel-return-button` (Button), form method POST, action `/return/cancel/<borrow_id>`
- Context Variables:
  - `borrow` (dict)
  - `book` (dict)
  - `username` (str)
- Navigation url_for mappings:
  - Cancel Return Button: `url_for('cancel_return', borrow_id=borrow.borrow_id)`

### 7. my_reservations.html
- Path: `templates/my_reservations.html`
- Page Title: "My Reservations"
- Elements:
  - `reservations-page` (Div)
  - `reservations-table` (Table)
  - `cancel-reservation-button-{reservation_id}` (Button) dynamic id per reservation
  - `back-to-dashboard` (Button)
- Context Variables:
  - `reservations` (list of dict)
- Navigation url_for mappings:
  - Cancel Reservation Button: `url_for('cancel_reservation', reservation_id=reservation.reservation_id)`
  - Back to Dashboard: `url_for('dashboard')`

### 8. my_reviews.html
- Path: `templates/my_reviews.html`
- Page Title: "My Reviews"
- Elements:
  - `reviews-page` (Div)
  - `reviews-list` (Div)
  - `edit-review-button-{review_id}` (Button), dynamic id per review
  - `delete-review-button-{review_id}` (Button), dynamic id per review
  - `back-to-dashboard` (Button)
- Context Variables:
  - `reviews` (list of dict)
- Navigation url_for mappings:
  - Edit Review Button: `url_for('edit_review', review_id=review.review_id)`
  - Delete Review Button: `url_for('delete_review', review_id=review.review_id)`
  - Back to Dashboard: `url_for('dashboard')`

### 9. write_review.html
- Path: `templates/write_review.html`
- Page Title: "Write Review"
- Elements:
  - `write-review-page` (Div)
  - `book-info-display` (Div)
  - `rating-input` (Dropdown), options 1 to 5
  - `review-text` (Textarea)
  - `submit-review-button` (Button), form method POST
  - `back-to-book` (Button)
- Context Variables:
  - `book` (dict)
  - `existing_review` (dict or None)
- Navigation url_for mappings:
  - Back to Book: `url_for('book_details', book_id=book.book_id)`

### 10. profile.html
- Path: `templates/profile.html`
- Page Title: "My Profile"
- Elements:
  - `profile-page` (Div)
  - `profile-username` (Div)
  - `profile-email` (Input)
  - `update-profile-button` (Button), form method POST
  - `borrow-history` (Div)
  - `back-to-dashboard` (Button)
- Context Variables:
  - `user` (dict) with keys: `username`(str), `email`(str), `phone`(str), `address`(str)
  - `borrow_history` (list of dict) with keys: `book_title`(str), `borrow_date`(str), `return_date`(str or empty)
- Navigation url_for mappings:
  - Back to Dashboard: `url_for('dashboard')`

### 11. payment_confirmation.html
- Path: `templates/payment_confirmation.html`
- Page Title: "Payment Confirmation"
- Elements:
  - `payment-page` (Div)
  - `fine-amount-display` (Div)
  - `confirm-payment-button` (Button), form method POST
  - `back-to-profile` (Button)
- Context Variables:
  - `fine` (dict) with keys: `fine_id`(int), `username`(str), `amount`(float), `status`(str)
- Navigation url_for mappings:
  - Back to Profile: `url_for('user_profile')`

---

## Section 3: Data File Schemas (Backend Development)

### 1. users.txt
- Path: `data/users.txt`
- Fields (pipe-delimited):
  - `username` (str)
  - `email` (str)
  - `phone` (str)
  - `address` (str)
- Data Description: User profile information including contact details.
- Example Rows:
  - `john_reader|john@example.com|555-1234|123 Main St`
  - `jane_doe|jane@example.com|555-5678|789 Oak St`
- Parsing Notes: Fields are strings; no headers included.

### 2. books.txt
- Path: `data/books.txt`
- Fields (pipe-delimited):
  - `book_id` (int)
  - `title` (str)
  - `author` (str)
  - `isbn` (str)
  - `genre` (str)
  - `publisher` (str)
  - `year` (int)
  - `description` (str)
  - `status` (str) - One of: Available, Borrowed, Reserved
  - `avg_rating` (float)
- Data Description: Information about books including status and average rating.
- Example Rows:
  - `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`
  - `2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6`
  - `3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7`
  - `4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5`
  - `5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3`
- Parsing Notes: `book_id` and `year` are integers, `avg_rating` is float.

### 3. borrowings.txt
- Path: `data/borrowings.txt`
- Fields (pipe-delimited):
  - `borrow_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `borrow_date` (str, format YYYY-MM-DD)
  - `due_date` (str, format YYYY-MM-DD)
  - `return_date` (str or empty)
  - `status` (str) - One of: Active, Returned, Overdue
  - `fine_amount` (float)
- Data Description: Records of borrowed books including dates, status, and fines.
- Example Rows:
  - `1|john_reader|2|2024-11-01|2024-11-15||Active|0`
  - `2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0`
  - `3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00`
- Parsing Notes: `borrow_id`, `book_id` integers; `fine_amount` float; dates as string.

### 4. reservations.txt
- Path: `data/reservations.txt`
- Fields (pipe-delimited):
  - `reservation_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `reservation_date` (str, format YYYY-MM-DD)
  - `status` (str) - One of: Active, Cancelled
- Data Description: Book reservation records with status tracking.
- Example Rows:
  - `1|jane_doe|4|2024-11-10|Active`
  - `2|john_reader|2|2024-10-25|Cancelled`
- Parsing Notes: `reservation_id`, `book_id` integers; date as string.

### 5. reviews.txt
- Path: `data/reviews.txt`
- Fields (pipe-delimited):
  - `review_id` (int)
  - `username` (str)
  - `book_id` (int)
  - `rating` (int) (1 to 5)
  - `review_text` (str)
  - `review_date` (str, format YYYY-MM-DD)
- Data Description: User submitted book reviews.
- Example Rows:
  - `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`
  - `2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20`
- Parsing Notes: `review_id`, `book_id`, `rating` integers; date as string.

### 6. fines.txt
- Path: `data/fines.txt`
- Fields (pipe-delimited):
  - `fine_id` (int)
  - `username` (str)
  - `borrow_id` (int)
  - `amount` (float)
  - `status` (str) - One of: Unpaid, Paid
  - `date_issued` (str, format YYYY-MM-DD)
- Data Description: Fine payment records for overdue borrowings.
- Example Rows:
  - `1|john_reader|3|5.00|Unpaid|2024-10-30`
- Parsing Notes: `fine_id`, `borrow_id` integers; `amount` float; date as string.

---

End of design_spec.md
