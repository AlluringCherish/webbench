# OnlineLibrary Web Application - Design Specification

---

## Section 1: Flask Routes Specification (Backend Development)

1. **Root Route**
   - URL Path: `/`
   - Function Name: `root_redirect`
   - HTTP Method: GET
   - Template Rendered: None (Redirect)
   - Context Variables: None
   - Behavior: Redirects to the dashboard page.

---

2. **Dashboard Page**
   - URL Path: `/dashboard`
   - Function Name: `dashboard`
   - HTTP Method: GET
   - Template Rendered: `dashboard.html`
   - Context Variables:
     - `username` (str): Current logged-in user's username

---

3. **Book Catalog Page**
   - URL Path: `/catalog`
   - Function Name: `book_catalog`
   - HTTP Method: GET
   - Template Rendered: `catalog.html`
   - Context Variables:
     - `books` (list of dict): List of all books 
       - Each dict contains:
         - `book_id` (int)
         - `title` (str)
         - `author` (str)
         - `status` (str): Availability status (Available, Borrowed, Reserved)

---

4. **Book Details Page**
   - URL Path: `/book/<int:book_id>`
   - Function Name: `book_details`
   - HTTP Method: GET
   - Template Rendered: `book_details.html`
   - Context Variables:
     - `book` (dict): Detailed information about the book
       - Fields: `book_id` (int), `title` (str), `author` (str), `status` (str), `description` (str), `avg_rating` (float)
     - `reviews` (list of dict): Reviews for the book
       - Each dict contains:
         - `review_id` (int)
         - `username` (str)
         - `rating` (int)
         - `review_text` (str)
         - `review_date` (str, YYYY-MM-DD)

---

5. **Borrow Confirmation Page - Display**
   - URL Path: `/borrow/<int:book_id>`
   - Function Name: `borrow_confirm_get`
   - HTTP Method: GET
   - Template Rendered: `borrow_confirm.html`
   - Context Variables:
     - `book` (dict): Information about the book being borrowed
       - Fields: `book_id` (int), `title` (str), `author` (str)
     - `due_date` (str, YYYY-MM-DD): Due date 14 days from current date

6. **Borrow Confirmation Page - Form Submission**
   - URL Path: `/borrow/<int:book_id>/confirm`
   - Function Name: `borrow_confirm_post`
   - HTTP Method: POST
   - Template Rendered: `borrow_confirm.html` (on failure or confirmation display)
   - Context Variables:
     - Same as GET for success display or errors

7. **Borrow Cancel Route**
   - URL Path: `/borrow/<int:book_id>/cancel`
   - Function Name: `borrow_cancel`
   - HTTP Method: POST or GET
   - Behavior: Redirects back to Book Details Page
   - Template Rendered: None (redirect)

---

8. **My Borrowings Page**
   - URL Path: `/my_borrows`
   - Function Name: `my_borrows`
   - HTTP Method: GET
   - Template Rendered: `my_borrows.html`
   - Context Variables:
     - `borrows` (list of dict): Borrowed books by the user
       - Fields: `borrow_id` (int), `title` (str), `borrow_date` (str), `due_date` (str), `status` (str), `fine_amount` (float)

9. **Return Book Route (Process Return)**
   - URL Path: `/return/<int:borrow_id>`
   - Function Name: `return_book`
   - HTTP Method: POST
   - Template Rendered: `my_borrows.html` or confirmation message
   - Context Variables: Updated borrows list on success

---

10. **My Reservations Page**
    - URL Path: `/my_reservations`
    - Function Name: `my_reservations`
    - HTTP Method: GET
    - Template Rendered: `my_reservations.html`
    - Context Variables:
      - `reservations` (list of dict): Reservations made by user
        - Fields: `reservation_id` (int), `title` (str), `reservation_date` (str), `status` (str)

11. **Cancel Reservation Route**
    - URL Path: `/cancel_reservation/<int:reservation_id>`
    - Function Name: `cancel_reservation`
    - HTTP Method: POST
    - Template Rendered: `my_reservations.html` or redirects

---

12. **My Reviews Page**
    - URL Path: `/my_reviews`
    - Function Name: `my_reviews`
    - HTTP Method: GET
    - Template Rendered: `my_reviews.html`
    - Context Variables:
      - `reviews` (list of dict): Reviews by user
        - Fields: `review_id` (int), `title` (str), `rating` (int), `review_text` (str), `review_date` (str)

13. **Edit Review Page - Display**
    - URL Path: `/review/edit/<int:review_id>`
    - Function Name: `edit_review_get`
    - HTTP Method: GET
    - Template Rendered: `write_review.html`
    - Context Variables:
      - `review` (dict): Review details
        - Fields: `review_id` (int), `book_id` (int), `rating` (int), `review_text` (str)
      - `book` (dict): Book info
        - Fields: `book_id` (int), `title` (str), `author` (str)

14. **Edit Review Page - Submission**
    - URL Path: `/review/edit/<int:review_id>`
    - Function Name: `edit_review_post`
    - HTTP Method: POST
    - Template Rendered: Redirect or confirmation

15. **Delete Review Route**
    - URL Path: `/review/delete/<int:review_id>`
    - Function Name: `delete_review`
    - HTTP Method: POST
    - Template Rendered: `my_reviews.html` or redirect

---

16. **Write Review Page - New Review**
    - URL Path: `/review/write/<int:book_id>`
    - Function Name: `write_review_get`
    - HTTP Method: GET
    - Template Rendered: `write_review.html`
    - Context Variables:
      - `book` (dict): Book info
        - Fields as in Book Details

17. **Write Review Page - Submission**
    - URL Path: `/review/write/<int:book_id>`
    - Function Name: `write_review_post`
    - HTTP Method: POST
    - Template Rendered: Redirect or confirmation

---

18. **User Profile Page**
    - URL Path: `/profile`
    - Function Name: `user_profile`
    - HTTP Method: GET
    - Template Rendered: `profile.html`
    - Context Variables:
      - `username` (str)
      - `email` (str)
      - `borrow_history` (list of dict)
        - Fields: `title` (str), `borrow_date` (str), `return_date` (str or None)

19. **User Profile Update Route**
    - URL Path: `/profile/update`
    - Function Name: `update_profile`
    - HTTP Method: POST
    - Template Rendered: `profile.html` or redirect

---

20. **Payment Confirmation Page - Display**
    - URL Path: `/payment/<int:fine_id>`
    - Function Name: `payment_confirmation_get`
    - HTTP Method: GET
    - Template Rendered: `payment_confirmation.html`
    - Context Variables:
      - `fine_amount` (float)
      - `fine_id` (int)

21. **Payment Confirmation Page - Submission**
    - URL Path: `/payment/<int:fine_id>/confirm`
    - Function Name: `payment_confirmation_post`
    - HTTP Method: POST
    - Template Rendered: Redirect or confirmation

---

## Section 2: HTML Template Specifications (Frontend Development)

---

### 1. Dashboard Template
- Filename/Path: `templates/dashboard.html`
- Page Title: "Library Dashboard"
- Main Heading (H1): `welcome-message` (displays "Welcome, {{ username }}")
- Element IDs:
  - `dashboard-page` (div) - Container div for complete dashboard
  - `welcome-message` (h1)
  - `browse-books-button` (button) - Navigates to catalog
  - `my-borrows-button` (button) - Navigates to my borrowings
- Context Variables:
  - `username` (str)
- Navigation:
  - `browse-books-button` onclick uses `url_for('book_catalog')`
  - `my-borrows-button` onclick uses `url_for('my_borrows')`

---

### 2. Book Catalog Template
- Filename/Path: `templates/catalog.html`
- Page Title: "Book Catalog"
- Main Heading (h1 tag with id not specified but can be included if desired)
- Element IDs:
  - `catalog-page` (div)
  - `search-input` (input, text)
  - `book-grid` (div): container for book cards
  - For each book card:
    - Button with ID: `view-book-button-{{ book.book_id }}`
  - `back-to-dashboard` (button)
- Context Variables:
  - `books` (list of dicts) each with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `status` (str)
- Navigation:
  - `view-book-button-{{book.book_id}}` onclick uses `url_for('book_details', book_id=book.book_id)`
  - `back-to-dashboard` onclick uses `url_for('dashboard')`

---

### 3. Book Details Template
- Filename/Path: `templates/book_details.html`
- Page Title: "Book Details"
- Element IDs:
  - `book-details-page` (div) - Page container
  - `book-title` (h1) - Displays book.title
  - `book-author` (div)
  - `book-status` (div)
  - `borrow-button` (button) - To borrow the book (if available)
  - `reviews-section` (div) - List reviews here
  - `write-review-button` (button) - Navigate to write review
  - `back-to-catalog` (button)
- Context Variables:
  - `book` (dict) with keys: `book_id`, `title`, `author`, `status`, `description`, `avg_rating`
  - `reviews` (list of dict) with keys: `review_id`, `username`, `rating`, `review_text`, `review_date`
- Navigation:
  - `borrow-button` onclick uses `url_for('borrow_confirm_get', book_id=book.book_id)`
  - `write-review-button` onclick uses `url_for('write_review_get', book_id=book.book_id)`
  - `back-to-catalog` onclick uses `url_for('book_catalog')`

---

### 4. Borrow Confirmation Template
- Filename/Path: `templates/borrow_confirm.html`
- Page Title: "Borrow Confirmation"
- Element IDs:
  - `borrow-page` (div)
  - `borrow-book-info` (div) - Show book.title, book.author
  - `due-date-display` (div) - Due date 14 days from borrow
  - `confirm-borrow-button` (button)
  - `cancel-borrow-button` (button)
- Context Variables:
  - `book` (dict) with keys: `book_id`, `title`, `author`
  - `due_date` (str: YYYY-MM-DD)
- Navigation:
  - Form method POST action to `/borrow/<book_id>/confirm` (mapped to function name `borrow_confirm_post`)
  - `cancel-borrow-button` triggers redirect to `book_details` page via `url_for('book_details', book_id=book.book_id)`

---

### 5. My Borrowings Template
- Filename/Path: `templates/my_borrows.html`
- Page Title: "My Borrowings"
- Element IDs:
  - `my-borrows-page` (div)
  - `filter-status` (dropdown/select) with options: All, Active, Returned, Overdue
  - `borrows-table` (table): columns for Title, Borrow Date, Due Date, Status, Fine Amount
  - For each active borrow row:
    - `return-book-button-{{ borrow.borrow_id }}` (button)
  - `back-to-dashboard` (button)
- Context Variables:
  - `borrows` (list of dict) with keys: `borrow_id`, `title`, `borrow_date`, `due_date`, `status`, `fine_amount`
- Navigation:
  - `return-book-button-{{ borrow.borrow_id }}` triggers POST to `/return/<borrow_id>` mapped to `return_book`
  - `back-to-dashboard` onclick uses `url_for('dashboard')`

---

### 6. My Reservations Template
- Filename/Path: `templates/my_reservations.html`
- Page Title: "My Reservations"
- Element IDs:
  - `reservations-page` (div)
  - `reservations-table` (table) with columns: Title, Reservation Date, Status
  - For each reservation row:
    - `cancel-reservation-button-{{ reservation.reservation_id }}` (button)
  - `back-to-dashboard` (button)
- Context Variables:
  - `reservations` (list of dict) with keys: `reservation_id`, `title`, `reservation_date`, `status`
- Navigation:
  - `cancel-reservation-button-{{ reservation.reservation_id }}` triggers POST to `/cancel_reservation/<reservation_id>` mapped to `cancel_reservation`
  - `back-to-dashboard` onclick uses `url_for('dashboard')`

---

### 7. My Reviews Template
- Filename/Path: `templates/my_reviews.html`
- Page Title: "My Reviews"
- Element IDs:
  - `reviews-page` (div)
  - `reviews-list` (div) containing review entries
  - For each review:
    - `edit-review-button-{{ review.review_id }}` (button)
    - `delete-review-button-{{ review.review_id }}` (button)
  - `back-to-dashboard` (button)
- Context Variables:
  - `reviews` (list of dict) with keys: `review_id`, `title`, `rating`, `review_text`, `review_date`
- Navigation:
  - `edit-review-button-{{ review.review_id }}` onclick uses `url_for('edit_review_get', review_id=review.review_id)`
  - `delete-review-button-{{ review.review_id }}` triggers POST to `/review/delete/<review_id>` mapped to `delete_review`
  - `back-to-dashboard` onclick uses `url_for('dashboard')`

---

### 8. Write Review Template
- Filename/Path: `templates/write_review.html`
- Page Title: "Write Review"
- Element IDs:
  - `write-review-page` (div)
  - `book-info-display` (div)
  - `rating-input` (dropdown/select) with options 1 to 5 stars
  - `review-text` (textarea)
  - `submit-review-button` (button)
  - `back-to-book` (button)
- Context Variables:
  - If editing, `review` (dict): `review_id`, `book_id`, `rating`, `review_text`
  - `book` (dict): `book_id`, `title`, `author`
- Navigation:
  - Form method POST action:
    - For new review: `/review/write/<book_id>` mapped to `write_review_post`
    - For edit review: `/review/edit/<review_id>` mapped to `edit_review_post`
  - `back-to-book` onclick uses `url_for('book_details', book_id=book.book_id)`

---

### 9. User Profile Template
- Filename/Path: `templates/profile.html`
- Page Title: "My Profile"
- Element IDs:
  - `profile-page` (div)
  - `profile-username` (div) - non-editable
  - `profile-email` (input text)
  - `update-profile-button` (button)
  - `borrow-history` (div) - listing all previous borrows
  - `back-to-dashboard` (button)
- Context Variables:
  - `username` (str)
  - `email` (str)
  - `borrow_history` (list of dict): each entry:
    - `title` (str)
    - `borrow_date` (str)
    - `return_date` (str or None)
- Navigation:
  - `update-profile-button` triggers form POST to `/profile/update` mapped to `update_profile`
  - `back-to-dashboard` onclick uses `url_for('dashboard')`

---

### 10. Payment Confirmation Template
- Filename/Path: `templates/payment_confirmation.html`
- Page Title: "Payment Confirmation"
- Element IDs:
  - `payment-page` (div)
  - `fine-amount-display` (div)
  - `confirm-payment-button` (button)
  - `back-to-profile` (button)
- Context Variables:
  - `fine_amount` (float)
  - `fine_id` (int)
- Navigation:
  - Form method POST action `/payment/<fine_id>/confirm` mapped to `payment_confirmation_post`
  - `back-to-profile` onclick uses `url_for('user_profile')`

---

## Section 3: Data File Schemas (Backend Development)

1. **Users Data**
- Filename/Path: `data/users.txt`
- Fields (Pipe-Delimited):
  1. `username` (str)
  2. `email` (str)
  3. `phone` (str)
  4. `address` (str)
- Description: Stores user profile information including contact details.
- Example Rows:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```
- Notes: No header line; all fields are strings.

---

2. **Books Data**
- Filename/Path: `data/books.txt`
- Fields (Pipe-Delimited):
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `genre` (str)
  6. `publisher` (str)
  7. `year` (int)
  8. `description` (str)
  9. `status` (str): One of Available, Borrowed, Reserved
  10. `avg_rating` (float)
- Description: Stores information about each book including availability and average user rating.
- Example Rows:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5
  5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3
  ```
- Notes: `book_id` and `year` as integers, `avg_rating` as float.

---

3. **Borrowings Data**
- Filename/Path: `data/borrowings.txt`
- Fields (Pipe-Delimited):
  1. `borrow_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `borrow_date` (str, YYYY-MM-DD)
  5. `due_date` (str, YYYY-MM-DD)
  6. `return_date` (str, YYYY-MM-DD or empty if not returned)
  7. `status` (str): Active, Returned, Overdue
  8. `fine_amount` (float)
- Description: Tracks borrowing transactions and fine status.
- Example Rows:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
  ```
- Notes: Empty `return_date` means not returned yet.

---

4. **Reservations Data**
- Filename/Path: `data/reservations.txt`
- Fields (Pipe-Delimited):
  1. `reservation_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `reservation_date` (str, YYYY-MM-DD)
  5. `status` (str): Active, Cancelled
- Description: Stores book reservation records.
- Example Rows:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```
- Notes: Status indicates if reservation is active or cancelled.

---

5. **Reviews Data**
- Filename/Path: `data/reviews.txt`
- Fields (Pipe-Delimited):
  1. `review_id` (int)
  2. `username` (str)
  3. `book_id` (int)
  4. `rating` (int)
  5. `review_text` (str)
  6. `review_date` (str, YYYY-MM-DD)
- Description: User generated reviews for books.
- Example Rows:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```
- Notes: `rating` from 1 to 5 stars.

---

6. **Fines Data**
- Filename/Path: `data/fines.txt`
- Fields (Pipe-Delimited):
  1. `fine_id` (int)
  2. `username` (str)
  3. `borrow_id` (int)
  4. `amount` (float)
  5. `status` (str): Unpaid, Paid
  6. `date_issued` (str, YYYY-MM-DD)
- Description: Records fines issued for overdue borrowings.
- Example Rows:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
  ```
- Notes: `status` shows payment status.

---

# End of Design Specification Document
