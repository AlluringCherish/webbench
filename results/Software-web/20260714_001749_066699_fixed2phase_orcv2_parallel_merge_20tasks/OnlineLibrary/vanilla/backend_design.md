# Backend Design Specification for OnlineLibrary Web Application

---

## Section 1: Backend Routes and Business Logic

The backend will be implemented using Flask, with routes handling HTTP requests for all key functionalities. Local text files stored in the `data` directory will serve as the data storage for users, books, borrowings, reservations, reviews, and fines.

---

### 1. User Authentication & Session Management
- User login and logout (not detailed in user_task but assumed required). Use Flask sessions to manage logged-in users by storing `username`.
- Authentication middleware will validate user sessions for protected routes.

---

### 2. Routes Overview

| Route Path                 | HTTP Method | Function Name           | Description & Logic Summary                                                                                                   |
|----------------------------|-------------|------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `/dashboard`               | GET         | show_dashboard         | Show welcome message with username, featured books. Check user session.                                                      |
| `/books`                  | GET         | list_books              | List and search books by title or author. Supports query parameters `q` (search string) and filters. Returns book list with status.
|
| `/books/<int:book_id>`     | GET         | show_book_details       | Display detailed info for specified book including availability and reviews.                                                 |
| `/borrow/confirm/<int:book_id>` | GET    | confirm_borrow         | Show borrow confirmation page with book info and computed due date (14 days from current date).                             |
| `/borrow/confirm/<int:book_id>` | POST   | perform_borrow         | Process borrowing: Create borrowing record with status "Active", update book status to "Borrowed". Check if book available.
|
| `/borrowings`              | GET         | list_user_borrowings    | List all borrowings for current user. Optional filter by status (All, Active, Returned, Overdue). Calculate overdue and fines. |
| `/borrowings/return/<int:borrow_id>` | POST | return_book           | Process return of borrowed book: update borrowing record status to "Returned", record return date, update book status to "Available".
|
| `/reservations`            | GET         | list_user_reservations  | List all reservations for current user, show status and allow cancellation.                                                  |
| `/reservations/cancel/<int:reservation_id>` | POST | cancel_reservation | Update reservation status to "Cancelled" if active.                                                                          |
| `/reviews`                 | GET         | list_user_reviews       | List all reviews by the current user with options to edit or delete.                                                        |
| `/reviews/write/<int:book_id>` | GET     | write_review_form       | Show form to write or edit review for the book. If user already reviewed, populate existing data.                           |
| `/reviews/write/<int:book_id>` | POST    | submit_review           | Create or update review for user-book pair. Update book average rating.                                                     |
| `/reviews/delete/<int:review_id>` | POST | delete_review           | Delete review by review_id. Update book average rating accordingly.                                                          |
| `/profile`                 | GET         | show_profile            | Display current user profile info with email editable and borrow history.                                                   |
| `/profile/update`          | POST        | update_profile          | Update user email and/or other editable profile info.                                                                        |
| `/fines/payment/<int:fine_id>` | GET       | show_payment            | Display fine amount for payment confirmation.                                                                               |
| `/fines/payment/<int:fine_id>` | POST      | confirm_payment         | Mark fine as paid, update fine record status to "Paid".                                                                    |

---

### Parameter Details and Responses

- Routes expect user session with `username` for all protected routes.
- Query parameters for search/filter routes are optional.
- POST routes expect form-data or JSON payloads for updates and writes.
- Responses generally redirect on success, or render templates with error messages.

---

### Error Handling

- 401 Unauthorized for unauthenticated access.
- 404 Not Found for invalid book_id, borrow_id, reservation_id, review_id, or fine_id.
- Validation errors with clear messages for invalid inputs, e.g., borrowing unavailable book.
- Business rule checks with meaningful feedback: e.g., cannot borrow reserved or borrowed books by others.

---

## Section 2: Data Models and File Schemas

All files are stored in `data` directory with pipe (`|`) delimiter, UTF-8 encoding, newline-separated records.

---

### 1. users.txt
- Fields: `username` (string, PK), `email` (string), `phone` (string), `address` (string)
- Constraints: `username` unique.
- Sample:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```

---

### 2. books.txt
- Fields: `book_id` (int, PK), `title` (string), `author` (string), `isbn` (string), `genre` (string), `publisher` (string), `year` (int), `description` (string), `status` (string enum: Available, Borrowed, Reserved), `avg_rating` (float, 0-5)
- Constraints: `book_id` unique.
- Sample:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  ```

---

### 3. borrowings.txt
- Fields: `borrow_id` (int, PK), `username` (string FK), `book_id` (int FK), `borrow_date` (YYYY-MM-DD), `due_date` (YYYY-MM-DD), `return_date` (YYYY-MM-DD or empty), `status` (string enum: Active, Returned, Overdue), `fine_amount` (float, >=0)
- Constraints: borrow dates logical, status transitions controlled.
- Sample:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  ```

---

### 4. reservations.txt
- Fields: `reservation_id` (int, PK), `username` (string FK), `book_id` (int FK), `reservation_date` (YYYY-MM-DD), `status` (string enum: Active, Cancelled)
- Sample:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```

---

### 5. reviews.txt
- Fields: `review_id` (int, PK), `username` (string FK), `book_id` (int FK), `rating` (int 1-5), `review_text` (string), `review_date` (YYYY-MM-DD)
- Sample:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```

---

### 6. fines.txt
- Fields: `fine_id` (int, PK), `username` (string FK), `borrow_id` (int FK), `amount` (float >=0), `status` (string enum: Unpaid, Paid), `date_issued` (YYYY-MM-DD)
- Sample:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
  ```

---

### Relationships and Status Notes
- `books.status` reflects availability: Available, Borrowed, Reserved.
- `borrowings.status` tracks borrow flow: Active (borrowed, not returned), Returned, Overdue (past due date).
- `reservations.status` Active or Cancelled.
- `fines.status` Unpaid or Paid.
- Foreign key relations: borrowing, reservation, review link user and book IDs.


---

## Section 3: Backend Functional Requirements

### 1. Book Search & Filter
- Search by title or author (partial, case-insensitive).
- Filters by book status.

### 2. Borrow Book
- Verify book status is "Available" before borrowing.
- Create borrowing record with borrow date = current date, due date = borrow date + 14 days, status="Active", fine=0.
- Change book status to "Borrowed".
- Prevent borrow if book is reserved by another user or already borrowed.

### 3. Return Book
- Mark borrow record return_date = current date, status = "Returned".
- Update book status to "Available".
- Calculate if overdue; if yes, mark borrowing "Overdue" before return and compute fine.
- Add fine record if overdue.

### 4. Reservation Management
- Users can reserve books with status "Available" or "Borrowed" but not Reserved.
- Add reservation record with current date and status "Active".
- Cancel reservation sets status to "Cancelled".
- Book status "Reserved" when at least one active reservation exists.

### 5. Reviews Management
- Users can create/edit a review per book.
- Rating between 1 to 5 stars.
- Update book average rating on add/edit/delete review.

### 6. Fine Calculation and Payment
- Fine applied when borrowings are overdue.
- Fine amount is calculated proportional to days overdue (use a fixed rate, e.g., $1 per day).
- Payment marks fine as "Paid".

### 7. Due Date Computation
- Due date = borrow date + 14 calendar days.

### 8. Validations
- Enforce unique usernames.
- Validate email format on user profile update.
- Validate ratings are within 1-5.
- Handle invalid IDs gracefully with user-friendly errors.

---

This design document will enable precise backend implementation using Python Flask and local text file management according to the OnlineLibrary app requirements.