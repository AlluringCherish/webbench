# OnlineLibrary Design Specification

---

## Section 1: Backend Design Integration

### 1. User Authentication & Session Management
- User login and logout using Flask sessions storing `username`.
- Session-based authentication middleware to protect routes.

### 2. Backend Routes and Logic

| Route Path                             | HTTP Method | Function Name          | Description & Logic Summary                                                                                                   |
|--------------------------------------|-------------|-----------------------|------------------------------------------------------------------------------------------------------------------------------|
| `/dashboard`                         | GET         | show_dashboard        | Show welcome message with username and featured books; check session.                                                        |
| `/books`                            | GET         | list_books             | List and search books by title or author; query param `q` optional for filter; return books with status.                     |
| `/books/<int:book_id>`               | GET         | show_book_details      | Show detailed info for book including availability and reviews.                                                             |
| `/borrow/confirm/<int:book_id>`      | GET         | confirm_borrow        | Show confirmation page with book info and due date (borrow date +14 days).
|
| `/borrow/confirm/<int:book_id>`      | POST        | perform_borrow        | Process borrow if book available; create borrowing with status "Active" and due date; update book status to "Borrowed".
|
| `/borrowings`                      | GET         | list_user_borrowings   | List all borrowings for the user; optionally filter by status (All, Active, Returned, Overdue); calculate overdue and fines. |
| `/borrowings/return/<int:borrow_id>`| POST        | return_book           | Process return: update borrow status to "Returned" with return date; update book status to "Available"; calculate & add fines if overdue.
|
| `/reservations`                    | GET         | list_user_reservations | List user reservations with status and cancellation option.                                                                 |
| `/reservations/cancel/<int:reservation_id>` | POST | cancel_reservation     | Cancel active reservation by updating status to "Cancelled".                                                               |
| `/reviews`                        | GET         | list_user_reviews      | List user reviews with edit/delete options.                                                                                  |
| `/reviews/write/<int:book_id>`      | GET         | write_review_form     | Show write/edit review form; pre-populate if review exists.                                                                  |
| `/reviews/write/<int:book_id>`      | POST        | submit_review         | Create or update user-book review; update book avg_rating.                                                                   |
| `/reviews/delete/<int:review_id>`   | POST        | delete_review         | Delete review and update book avg_rating.                                                                                    |
| `/profile`                        | GET         | show_profile           | Show user profile including editable email and borrow history.                                                               |
| `/profile/update`                 | POST        | update_profile        | Update user email and other editable info with validation.                                                                   |
| `/fines/payment/<int:fine_id>`       | GET         | show_payment          | Show fine payment confirmation with fine details.                                                                             |
| `/fines/payment/<int:fine_id>`       | POST        | confirm_payment       | Mark fine as "Paid"; update fine record status.                                                                             |

---

### 3. Data Models and File Schemas

- All data files stored in `data` directory.
- Pipe (`|`) delimited UTF-8 text files with newline-separated records.

#### 3.1 users.txt
- `username` (PK), `email`, `phone`, `address`
- Unique `username`
- Example:
```
john_reader|john@example.com|555-1234|123 Main St
jane_doe|jane@example.com|555-5678|789 Oak St
```

#### 3.2 books.txt
- `book_id` (PK), `title`, `author`, `isbn`, `genre`, `publisher`, `year`, `description`, `status` (Available/Borrowed/Reserved), `avg_rating` (0-5 float)
- Example:
```
1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
```

#### 3.3 borrowings.txt
- `borrow_id` (PK), `username` (FK), `book_id` (FK), `borrow_date` (YYYY-MM-DD), `due_date` (YYYY-MM-DD), `return_date` (YYYY-MM-DD or empty), `status` (Active/Returned/Overdue), `fine_amount` (float >=0)
- Example:
```
1|john_reader|2|2024-11-01|2024-11-15||Active|0
2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
```

#### 3.4 reservations.txt
- `reservation_id` (PK), `username` (FK), `book_id` (FK), `reservation_date` (YYYY-MM-DD), `status` (Active/Cancelled)
- Example:
```
1|jane_doe|4|2024-11-10|Active
2|john_reader|2|2024-10-25|Cancelled
```

#### 3.5 reviews.txt
- `review_id` (PK), `username` (FK), `book_id` (FK), `rating` (1-5), `review_text`, `review_date` (YYYY-MM-DD)
- Example:
```
1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
```

#### 3.6 fines.txt
- `fine_id` (PK), `username` (FK), `borrow_id` (FK), `amount` (float >=0), `status` (Unpaid/Paid), `date_issued` (YYYY-MM-DD)
- Example:
```
1|john_reader|3|5.00|Unpaid|2024-10-30
```

---

### 4. Backend Functional Requirements

- **Book Search & Filter**: Partial, case-insensitive search by title or author; filter by book status.
- **Borrow Book**: Only if status "Available"; create borrowing record with current date, due date 14 days later, status Active, fine=0; update book status to "Borrowed"; disallow if reserved by others or borrowed.
- **Return Book**: Mark borrow returned with current date; update book status "Available"; calculate if overdue, mark overdue and add fine record.
- **Reservation Management**: Reserve books if status is "Available" or "Borrowed" but not reserved; create reservation Active with current date; cancel sets status "Cancelled"; book status set "Reserved" if active reservations exist.
- **Reviews Management**: One review per user-book; rating 1-5 stars; update book avg_rating on add/edit/delete.
- **Fine Calculation and Payment**: Fine $1/day overdue; payment marks fine Paid.
- **Due Date Computation**: borrow date + 14 calendar days.
- **Validations**: Unique usernames; valid email format; rating 1-5; graceful error handling on invalid IDs.

---

## Section 2: Frontend Design Integration

### 1. Templates & Elements

| Page Name             | Template Filename           | Key Elements & IDs                                                                                                             |
|-----------------------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| Dashboard             | dashboard.html              | `dashboard-page` (div), `welcome-message` (h1), `browse-books-button` (button), `my-borrows-button` (button)                   |
| Book Catalog          | catalog.html                | `catalog-page` (div), `search-input` (input), `book-grid` (div), `view-book-button-{book_id}` (button), `back-to-dashboard` (button) |
| Book Details          | book_details.html           | `book-details-page` (div), `book-title` (h1), `book-author` (div), `book-status` (div), `borrow-button` (button), `reviews-section` (div), `write-review-button` (button), `back-to-catalog` (button) |
| Borrow Confirmation   | borrow_confirmation.html    | `borrow-page` (div), `borrow-book-info` (div), `due-date-display` (div), `confirm-borrow-button` (button), `cancel-borrow-button` (button) |
| My Borrowings         | my_borrowings.html          | `my-borrows-page` (div), `filter-status` (select), `borrows-table` (table), `return-book-button-{borrow_id}` (button), `back-to-dashboard` (button) |
| My Reservations       | my_reservations.html        | `reservations-page` (div), `reservations-table` (table), `cancel-reservation-button-{reservation_id}` (button), `back-to-dashboard` (button) |
| My Reviews            | my_reviews.html             | `reviews-page` (div), `reviews-list` (div), `edit-review-button-{review_id}` (button), `delete-review-button-{review_id}` (button), `back-to-dashboard` (button) |
| Write Review          | write_review.html           | `write-review-page` (div), `book-info-display` (div), `rating-input` (select), `review-text` (textarea), `submit-review-button` (button), `back-to-book` (button) |
| User Profile          | profile.html                | `profile-page` (div), `profile-username` (div), `profile-email` (input type=email), `update-profile-button` (button), `borrow-history` (div), `back-to-dashboard` (button) |
| Payment Confirmation  | payment_confirmation.html   | `payment-page` (div), `fine-amount-display` (div), `confirm-payment-button` (button), `back-to-profile` (button)                |

---

### 2. Navigation Flows

- Dashboard is landing page.
- From Dashboard:
  - `browse-books-button` -> Book Catalog page.
  - `my-borrows-button` -> My Borrowings page.
- From Book Catalog:
  - `view-book-button-{book_id}` -> Book Details page.
  - `back-to-dashboard` -> Dashboard.
- From Book Details:
  - `borrow-button` -> Borrow Confirmation page.
  - `write-review-button` -> Write Review page.
  - `back-to-catalog` -> Book Catalog.
- From Borrow Confirmation:
  - `confirm-borrow-button` -> Complete borrow, redirect to My Borrowings.
  - `cancel-borrow-button` -> Back to Book Details.
- From My Borrowings:
  - `return-book-button-{borrow_id}` -> Return book, refresh.
  - `filter-status` -> Filter borrowings in `borrows-table`.
  - `back-to-dashboard` -> Dashboard.
- From My Reservations:
  - `cancel-reservation-button-{reservation_id}` -> Cancel reservation, refresh.
  - `back-to-dashboard` -> Dashboard.
- From My Reviews:
  - `edit-review-button-{review_id}` -> Write Review page with loaded review.
  - `delete-review-button-{review_id}` -> Delete review, refresh.
  - `back-to-dashboard` -> Dashboard.
- From Write Review:
  - `submit-review-button` -> Submit, back to Book Details.
  - `back-to-book` -> Book Details.
- From Profile:
  - `update-profile-button` -> Save updates.
  - `back-to-dashboard` -> Dashboard.
- From Payment Confirmation:
  - `confirm-payment-button` -> Confirm payment, back to Profile.
  - `back-to-profile` -> Profile.

---

### 3. UI Behavior and Interactivity

- Search input filters books dynamically on Book Catalog.
- Book Grid populates based on search/filter results.
- Borrow button disabled if book status is not "Available".
- Filter dropdown on My Borrowings filters displayed borrow status.
- Return book button triggers backend return process.
- Cancel reservation button triggers cancellation process.
- Edit review button loads corresponding review in Write Review page.
- Delete review button deletes review after confirmation.
- Form submission buttons validate inputs and provide success/error feedback.
- User messages shown near corresponding buttons or sections.

---

## Section 3: Consistency and Completeness Checks

- All backend route paths match frontend navigation and form submission paths.
- Element IDs in frontend exactly correspond to those referenced in routes and UI descriptions.
- Data file schemas match field usage in both backend and frontend.
- No features or requirements are added or omitted beyond the user task.
- Validation rules are consistent across backend logic and frontend input constraints.
- Error handling for invalid resource IDs is specified and assumed reflected in frontend feedback.

---

This unified design_spec.md provides a comprehensive and internally consistent blueprint for both backend and frontend developers to implement the OnlineLibrary application strictly to the user requirements with full traceability and coverage.
