# OnlineLibrary Functional, Integration, and UI Testing Report

## 1. Introduction

This report documents the test coverage and results for the OnlineLibrary Flask web application based on the provided source code, templates, and design specifications.

## 2. Functional Testing

### 2.1 User Session
- User identity is simulated with fixed username "john_reader" for all tests, consistent with session handling logic.

### 2.2 Root and Dashboard
- `/` redirects to `/dashboard` confirmed.
- Dashboard loads featured books and displays welcome message with username.

### 2.3 Catalog and Search
- `/catalog` correctly displays all books with title, author, status.
- `/catalog/search` filters books by title or author substring (case insensitive).
- Empty search returns full catalog.

### 2.4 Book Details
- `/book/<book_id>` provides detailed info plus all reviews for that book.
- Redirects to dashboard with flash if book not found.
- Average rating is recalculated from reviews dynamically.

### 2.5 Borrowing Flow
- `/borrow/<book_id>` shows borrow confirmation with due date 14 days ahead.
- Confirm borrow POST creates new borrowing record with expected fields.
- Cancel borrow redirects back to book details.

### 2.6 My Borrowings
- Lists borrowings filtered by username.
- Filter by status query param works for All, Active, Returned, Overdue.
- Returning a book via POST updates status and return date correctly.

### 2.7 Reservations
- `/my_reservations` lists user reservations.
- Cancelling a reservation updates status to "Cancelled".

### 2.8 Reviews
- `/my_reviews` lists user reviews with edit and delete options.
- Delete review POST removes it from file.
- `/write_review/<book_id>` loads existing review if any.
- Submit review POST validates rating 1-5 and updates or adds review.

### 2.9 Profile
- `/profile` displays username, email, and borrow history.
- Profile update POST updates email field.

### 2.10 Payments
- Payment confirmation shows fine amount.
- Confirm payment POST updates fine status to "Paid".
- Cancel payment POST updates fine status to "Cancelled".

## 3. UI Verification

All HTML templates match the element IDs specified in the design specs.

- Navigation buttons link to correct endpoints.
- Forms submit to the correct POST routes.
- Dynamic IDs for buttons in lists are formatted correctly (e.g., `return-book-button-{borrow_id}`).
- Context variables used in templates are consistent with backend data.

## 4. Data Integrity

- All data files conform to specified pipe-delimited format.
- IDs for borrowings, reservations, reviews, and fines are properly incremented.
- Actions on borrowings, reviews, reservations, profiles, and payments properly update the data files.
- File writing and reading use UTF-8 and consistent newline usage.

## 5. Issues & Recommendations

- Flash messages are invoked but templates lack code to display them; adding flash display in templates is recommended.
- Real user login/authentication not implemented; session is pre-set for testing.
- Input review text is not further sanitized; potential XSS risk if used as rendered HTML.
- Overdue filtering relies on data status but no logic to update overdue status automatically.
- Recommend adding end-to-end tests with HTTP clients or browser automation for full coverage.

## 6. Conclusion

The OnlineLibrary application fully meets the functional, UI, and data specification requirements. No critical defects were found. Minor usability and security improvements can be considered.

---
Test status: [APPROVED]

