# OnlineLibrary Web Application Design Specification

---

## Section 1: Flask Routes and Methods

| Route Path               | HTTP Method(s) | Template File             | Context Variables                                            | Notes & Navigation Flow                                                  |
|-------------------------|----------------|---------------------------|--------------------------------------------------------------|-------------------------------------------------------------------------|
| /                       | GET            | dashboard.html            | username                                                    | Default entry point. Buttons: browse-books-button -> /catalog , my-borrows-button -> /my-borrows |
| /dashboard              | GET            | dashboard.html            | username                                                    | Alias for "/" with same content and navigation.                        |
| /catalog                | GET, POST      | catalog.html              | books, search_query (optional)                              | Search with POST; Back button: back-to-dashboard -> /dashboard ; Book cards: view-book-button-{book_id} -> /book/{book_id} |
| /book/&lt;int:book_id&gt;| GET            | book_details.html         | book, reviews                                              | Borrow button: borrow-button -> /borrow/{book_id} ; Write review: write-review-button -> /write-review/{book_id} ; Back: back-to-catalog -> /catalog |
| /borrow/&lt;int:book_id&gt; | GET, POST      | borrow_confirmation.html  | book, due_date                                             | Confirm borrow POST updates borrowings; Cancel: cancel-borrow-button -> /book/{book_id} |
| /my-borrows             | GET, POST      | my_borrows.html           | borrows, filter_status                                     | Filter POST; Return book POST to /return/{borrow_id}; Back: back-to-dashboard -> /dashboard |
| /my-reservations        | GET            | my_reservations.html      | reservations                                               | Cancel reservation POST; Back: back-to-dashboard -> /dashboard           |
| /my-reviews             | GET            | my_reviews.html           | reviews                                                    | Edit review link: edit-review-button-{review_id} -> /write-review/{book_id} with preloaded data; Delete review POST; Back: back-to-dashboard -> /dashboard |
| /write-review/&lt;int:book_id&gt; | GET, POST      | write_review.html          | book, existing_review (optional)                            | Submit review POST saves; Back: back-to-book -> /book/{book_id}           |
| /profile                | GET, POST      | profile.html              | username, email, borrow_history                             | Update email POST; Back: back-to-dashboard -> /dashboard                 |
| /payment/&lt;int:fine_id&gt;   | GET, POST      | payment_confirmation.html | fine                                                       | Confirm payment POST updates fines; Back: back-to-profile -> /profile    |

---

## Section 2: HTML Template Specifications and Elements

| Page                  | Template File             | Page Title           | Element IDs and Types                                                                                                      |
|-----------------------|---------------------------|----------------------|----------------------------------------------------------------------------------------------------------------------------|
| Dashboard             | dashboard.html            | Library Dashboard    | dashboard-page (Div), welcome-message (H1), browse-books-button (Button), my-borrows-button (Button)                        |
| Book Catalog          | catalog.html              | Book Catalog         | catalog-page (Div), search-input (Input), book-grid (Div), view-book-button-{book_id} (Button), back-to-dashboard (Button) |
| Book Details          | book_details.html         | Book Details         | book-details-page (Div), book-title (H1), book-author (Div), book-status (Div), borrow-button (Button), reviews-section (Div), write-review-button (Button), back-to-catalog (Button) |
| Borrow Confirmation   | borrow_confirmation.html  | Borrow Confirmation  | borrow-page (Div), borrow-book-info (Div), due-date-display (Div), confirm-borrow-button (Button), cancel-borrow-button (Button) |
| My Borrowings         | my_borrows.html           | My Borrowings        | my-borrows-page (Div), filter-status (Dropdown), borrows-table (Table), return-book-button-{borrow_id} (Button), back-to-dashboard (Button) |
| My Reservations       | my_reservations.html      | My Reservations      | reservations-page (Div), reservations-table (Table), cancel-reservation-button-{reservation_id} (Button), back-to-dashboard (Button) |
| My Reviews            | my_reviews.html           | My Reviews           | reviews-page (Div), reviews-list (Div), edit-review-button-{review_id} (Button), delete-review-button-{review_id} (Button), back-to-dashboard (Button) |
| Write Review          | write_review.html          | Write Review         | write-review-page (Div), book-info-display (Div), rating-input (Dropdown), review-text (Textarea), submit-review-button (Button), back-to-book (Button) |
| User Profile          | profile.html              | My Profile           | profile-page (Div), profile-username (Div), profile-email (Input), update-profile-button (Button), borrow-history (Div), back-to-dashboard (Button) |
| Payment Confirmation  | payment_confirmation.html | Payment Confirmation | payment-page (Div), fine-amount-display (Div), confirm-payment-button (Button), back-to-profile (Button)                    |

### Navigation Flows

- Dashboard:
  - browse-books-button -> /catalog
  - my-borrows-button -> /my-borrows
- Book Catalog:
  - view-book-button-{book_id} -> /book/{book_id}
  - back-to-dashboard -> /dashboard
- Book Details:
  - borrow-button -> /borrow/{book_id}
  - write-review-button -> /write-review/{book_id}
  - back-to-catalog -> /catalog
- Borrow Confirmation:
  - confirm-borrow-button (POST) confirms borrow
  - cancel-borrow-button -> /book/{book_id}
- My Borrowings:
  - return-book-button-{borrow_id} (POST) returns book
  - back-to-dashboard -> /dashboard
- My Reservations:
  - cancel-reservation-button-{reservation_id} (POST) cancels reservation
  - back-to-dashboard -> /dashboard
- My Reviews:
  - edit-review-button-{review_id} -> /write-review/{book_id}
  - delete-review-button-{review_id} (POST) deletes review
  - back-to-dashboard -> /dashboard
- Write Review:
  - submit-review-button (POST) submits review
  - back-to-book -> /book/{book_id}
- Profile:
  - update-profile-button (POST) updates email
  - back-to-dashboard -> /dashboard
- Payment:
  - confirm-payment-button (POST) confirms payment
  - back-to-profile -> /profile

---

## Section 3: Local Text Data Files and Formats

- Directory: `data/`

- `users.txt`
  - Format: `username|email|phone|address`
  - Usage: Accessed and updated in /profile page to display and modify user info

- `books.txt`
  - Format: `book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating`
  - Usage: Loaded on /catalog for listing and /book/<id> for detail; status updated on borrow or reservation

- `borrowings.txt`
  - Format: `borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount`
  - Usage: Managed in /my-borrows for listing and filtering, /borrow for adding borrowing, /return for returning book, /profile for borrow history

- `reservations.txt`
  - Format: `reservation_id|username|book_id|reservation_date|status`
  - Usage: Managed in /my-reservations for listing and canceling

- `reviews.txt`
  - Format: `review_id|username|book_id|rating|review_text|review_date`
  - Usage: Accessed and edited in /book, /my-reviews, /write-review pages

- `fines.txt`
  - Format: `fine_id|username|borrow_id|amount|status|date_issued`
  - Usage: Displayed and updated in /payment page

### Data Handling Details

- All data files read on GET requests from routes, parsed using `|` delimiter
- POST requests write changes back (overwrite or append) to the files
- Borrow due dates calculated as 14 days from borrow date; saved in `borrowings.txt`
- Status fields in `books.txt` and others reflect current state changes (e.g., Available, Borrowed, Reserved)
- Data directory structure and file schemas remain as specified

---

This canonical design document merges both design drafts into a single, consistent, complete blueprint to implement the 'OnlineLibrary' Flask web application according to user requirements.