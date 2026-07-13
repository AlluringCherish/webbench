# OnlineLibrary Design Specification

## 1. Flask Routes Specification

| Path                 | Function Name           | HTTP Methods | Template File             | Context Variables Sent to Template (Type & Structure)                    |
|----------------------|------------------------|--------------|---------------------------|------------------------------------------------------------------------|
| /                    | index                  | GET          | N/A (redirect)             | Redirects to `/dashboard`                                               |
| /dashboard           | dashboard              | GET          | dashboard.html             | username (str)                                                         |
| /catalog             | book_catalog           | GET, POST    | catalog.html               | books (list of dicts), search_query (str)                             |
| /book/<int:book_id>  | book_details           | GET          | book_details.html          | book (dict), reviews (list of dicts), user_can_borrow (bool)          |
| /borrow/<int:book_id>| borrow_confirm         | GET, POST    | borrow_confirmation.html   | book (dict), due_date (str, YYYY-MM-DD)                               |
| /my-borrowings       | my_borrowings          | GET, POST    | my_borrowings.html         | borrows (list of dicts), filter_status (str)                          |
| /my-reservations     | my_reservations        | GET          | my_reservations.html       | reservations (list of dicts)                                          |
| /my-reviews          | my_reviews             | GET, POST    | my_reviews.html            | reviews (list of dicts)                                               |
| /review/write/<int:book_id> | write_review        | GET, POST    | write_review.html          | book (dict), review (dict or None)                                   |
| /profile             | user_profile           | GET, POST    | user_profile.html          | user_info (dict), borrow_history (list of dicts)                     |
| /payment/<int:fine_id>| payment_confirmation   | GET, POST    | payment_confirmation.html  | fine (dict)                                                         |

### Explanation of context variables:
- `username`: Current logged-in user's username
- `books`: List of books each as dict with all needed details
- `book`: Single book dict with keys: book_id, title, author, etc.
- `reviews`: List of review dicts: review_id, username, rating, text, date
- `user_can_borrow`: bool indicating if book is currently available
- `due_date`: date string representing 14 days after borrowing
- `borrows`: List of dicts for borrowings with fields like borrow_id, title, borrow_date, due_date, status
- `filter_status`: the current filter applied on borrowings
- `reservations`: List dicts with reservation_id, title, date, status
- `reviews` (on my_reviews): list of user authored reviews
- `review` (on write_review): review for editing or None on new
- `user_info`: dict with username, email, phone, address
- `borrow_history`: list of past borrows with details
- `fine`: dict with fine details

## 2. Template Element IDs

### 2.1 dashboard.html
- `dashboard-page` (Div)
- `welcome-message` (H1)
- `browse-books-button` (Button)
- `my-borrows-button` (Button)

### 2.2 catalog.html
- `catalog-page` (Div)
- `search-input` (Input)
- `book-grid` (Div)
- `view-book-button-{book_id}` (Button, dynamic)
- `back-to-dashboard` (Button)

### 2.3 book_details.html
- `book-details-page` (Div)
- `book-title` (H1)
- `book-author` (Div)
- `book-status` (Div)
- `borrow-button` (Button)
- `reviews-section` (Div)
- `write-review-button` (Button)
- `back-to-catalog` (Button)

### 2.4 borrow_confirmation.html
- `borrow-page` (Div)
- `borrow-book-info` (Div)
- `due-date-display` (Div)
- `confirm-borrow-button` (Button)
- `cancel-borrow-button` (Button)

### 2.5 my_borrowings.html
- `my-borrows-page` (Div)
- `filter-status` (Dropdown)
- `borrows-table` (Table)
- `return-book-button-{borrow_id}` (Button, dynamic)
- `back-to-dashboard` (Button)

### 2.6 my_reservations.html
- `reservations-page` (Div)
- `reservations-table` (Table)
- `cancel-reservation-button-{reservation_id}` (Button, dynamic)
- `back-to-dashboard` (Button)

### 2.7 my_reviews.html
- `reviews-page` (Div)
- `reviews-list` (Div)
- `edit-review-button-{review_id}` (Button, dynamic)
- `delete-review-button-{review_id}` (Button, dynamic)
- `back-to-dashboard` (Button)

### 2.8 write_review.html
- `write-review-page` (Div)
- `book-info-display` (Div)
- `rating-input` (Dropdown)
- `review-text` (Textarea)
- `submit-review-button` (Button)
- `back-to-book` (Button)

### 2.9 user_profile.html
- `profile-page` (Div)
- `profile-username` (Div)
- `profile-email` (Input)
- `update-profile-button` (Button)
- `borrow-history` (Div)
- `back-to-dashboard` (Button)

### 2.10 payment_confirmation.html
- `payment-page` (Div)
- `fine-amount-display` (Div)
- `confirm-payment-button` (Button)
- `back-to-profile` (Button)

## 3. Data File Schemas

All data files are pipe-delimited stored in `data/` directory:

| File               | Path             | Fields Order & Description                                                                                  | Example Row                                                                                                         |
|--------------------|------------------|------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| users.txt          | data/users.txt   | username (str), email (str), phone (str), address (str)                                                    | john_reader|john@example.com|555-1234|123 Main St                                                               |
| books.txt          | data/books.txt   | book_id (int), title (str), author (str), isbn (str), genre (str), publisher (str), year (int), description (str), status (str), avg_rating (float) | 1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8 |
| borrowings.txt     | data/borrowings.txt | borrow_id (int), username (str), book_id (int), borrow_date (YYYY-MM-DD), due_date (YYYY-MM-DD), return_date (YYYY-MM-DD or empty), status (str), fine_amount (float) | 1|john_reader|2|2024-11-01|2024-11-15||Active|0                                                          |
| reservations.txt   | data/reservations.txt | reservation_id (int), username (str), book_id (int), reservation_date (YYYY-MM-DD), status (str)           | 1|jane_doe|4|2024-11-10|Active                                                                                                            |
| reviews.txt        | data/reviews.txt | review_id (int), username (str), book_id (int), rating (int 1-5), review_text (str), review_date (YYYY-MM-DD) | 1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03                                                                    |
| fines.txt          | data/fines.txt   | fine_id (int), username (str), borrow_id (int), amount (float), status (str), date_issued (YYYY-MM-DD)      | 1|john_reader|3|5.00|Unpaid|2024-10-30                                                                                                   |

## 4. User Actions and Flows

### 4.1 Borrowing a Book
- On `/catalog` page, user searches and filters books using `search-input`.
- Clicks `view-book-button-{book_id}` to navigate to `/book/<book_id>`.
- On `/book/<book_id>`, if `book-status` is 'Available', user clicks `borrow-button`.
- Navigates to `/borrow/<book_id>` showing borrow details and `due-date-display` (14 days from borrow date).
- Click `confirm-borrow-button` POSTs borrow action, updates `borrowings.txt`, then redirects to `/my-borrowings`.
- If canceled (`cancel-borrow-button`), navigates back to `/book/<book_id>`.

### 4.2 Returning a Book
- From `/dashboard`, user clicks `my-borrows-button` to `/my-borrowings`.
- Uses `filter-status` dropdown to filter borrow records.
- Click `return-book-button-{borrow_id}` sends POST to return book.
- Updates `borrowings.txt` with return info.
- Redirects back to `/dashboard` or refreshes borrowings list.

### 4.3 Reserving a Book
- Reservation implied flow (not explicitly stated) assumed available.
- Manage reservations at `/my-reservations`.
- `cancel-reservation-button-{reservation_id}` POST cancels reservation, updates `reservations.txt`.
- Navigates back to `/dashboard` after cancellation.

### 4.4 Writing and Managing Reviews
- From `/book/<book_id>`, user clicks `write-review-button` → `/review/write/<book_id>`.
- Fills `rating-input` and `review-text`.
- Clicking `submit-review-button` POSTs review, updates `reviews.txt`, then redirects back to `/book/<book_id>`.
- User can manage reviews from `/my-reviews`:
  - `edit-review-button-{review_id}` navigates to `/review/write/<book_id>` with existing review data.
  - `delete-review-button-{review_id}` POST deletes review and refreshes `/my-reviews`.

### 4.5 Managing Profile and Payments
- From `/dashboard`, user accesses `/profile`.
- Updates email in `profile-email`.
- Clicks `update-profile-button` POST to save changes, stays on profile.
- Borrow history shown in `borrow-history`.
- If fines pending, user visits `/payment/<fine_id>`.
- On `/payment/<fine_id>`, `confirm-payment-button` POSTs payment, updates `fines.txt`, then redirects to `/profile`.
- Cancel button navigates back to `/profile`.

## 5. Technical Constraints and Notes
- Root `/` route must redirect to `/dashboard`.
- All dynamic buttons use consistent ID pattern as specified with variable segments.
- Back buttons use GET navigation routes to preserve user context.
- Templates filenames follow snake_case generation based on page names.
- POST actions for add/update/delete operations use redirects after processing to avoid form re-submission.
- Data files are maintained as pipe-delimited plain text files in `data/`.
- Access control and user session management implied but not described here.

---

This design_spec.md provides comprehensive guidance for implementing the OnlineLibrary Flask app backend and frontend structures consistent with the requirements_analysis.md.