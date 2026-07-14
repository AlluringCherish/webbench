# design_debate_a.md for OnlineLibrary Web Application - Updated with Peer Improvements

## Section 1: Flask Routes Specification

| Route Path                     | HTTP Method(s) | Template File            | Context Variables                                            | Navigation & Page Flows                                                                                                  | Notes on Dynamic/Button IDs                         |
|-------------------------------|----------------|--------------------------|--------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| /                             | GET            | dashboard.html           | username                                                     | Default entry point. Buttons navigate to /catalog and /my-borrows.                                                       | browse-books-button, my-borrows-button             |
| /dashboard                    | GET            | dashboard.html           | username                                                     | Same as "/" for direct access.                                                                                         | Same as "/"                                        |
| /catalog                     | GET, POST      | catalog.html             | books, search_query (optional)                              | Book search via POST; Back button to /dashboard; Book card buttons to /book/{book_id}.                                   | book-grid; view-book-button-{book_id}; back-to-dashboard |
| /book/<int:book_id>           | GET            | book_details.html        | book, reviews                                                | Borrow button to /borrow/{book_id}; Write review button to /write-review/{book_id}; Back button to /catalog.              | borrow-button, write-review-button, back-to-catalog |
| /borrow/<int:book_id>         | GET, POST      | borrow_confirmation.html | book, due_date                                              | Confirm borrow button POST updates borrowings; Cancel back to /book/{book_id}.                                            | confirm-borrow-button, cancel-borrow-button         |
| /my-borrows                  | GET, POST      | my_borrows.html          | borrows, filter_status                                      | Filter form POST; Return book buttons POST to /return/{borrow_id}; Back to dashboard.                                     | filter-status; return-book-button-{borrow_id}; back-to-dashboard |
| /my-reservations             | GET            | my_reservations.html     | reservations                                               | Cancel reservation buttons POST; Back to dashboard.                                                                       | cancel-reservation-button-{reservation_id}; back-to-dashboard |
| /my-reviews                  | GET            | my_reviews.html          | reviews                                                    | Edit buttons link to /write-review/{book_id} with preloaded data; Delete buttons POST; Back to dashboard.                | edit-review-button-{review_id}, delete-review-button-{review_id}; back-to-dashboard |
| /write-review/<int:book_id>   | GET, POST      | write_review.html        | book, existing_review (optional)                            | Submit POST saves review; Back button to /book/{book_id}.                                                                  | rating-input, review-text, submit-review-button, back-to-book |
| /profile                    | GET, POST      | profile.html             | username, email, borrow_history                             | Update email POST; Back to dashboard.                                                                                     | profile-username, profile-email, update-profile-button, borrow-history, back-to-dashboard |
| /payment/<int:fine_id>         | GET, POST      | payment_confirmation.html| fine                                                       | Confirm payment POST updates fines; Back button to /profile.                                                              | confirm-payment-button, back-to-profile              |

## Section 2: HTML Template and Page Elements

| Page                  | Template File         | Page Title             | Element IDs and Types                                                                                                        |
|-----------------------|-----------------------|------------------------|------------------------------------------------------------------------------------------------------------------------------|
| Dashboard             | dashboard.html        | Library Dashboard      | dashboard-page (Div), welcome-message (H1), browse-books-button (Button), my-borrows-button (Button)                          |
| Book Catalog          | catalog.html          | Book Catalog           | catalog-page (Div), search-input (Input), book-grid (Div), view-book-button-{book_id} (Button), back-to-dashboard (Button)   |
| Book Details          | book_details.html     | Book Details           | book-details-page (Div), book-title (H1), book-author (Div), book-status (Div), borrow-button (Button), reviews-section (Div), write-review-button (Button), back-to-catalog (Button) |
| Borrow Confirmation   | borrow_confirmation.html | Borrow Confirmation | borrow-page (Div), borrow-book-info (Div), due-date-display (Div), confirm-borrow-button (Button), cancel-borrow-button (Button) |
| My Borrowings         | my_borrows.html       | My Borrowings          | my-borrows-page (Div), filter-status (Dropdown), borrows-table (Table), return-book-button-{borrow_id} (Button), back-to-dashboard (Button) |
| My Reservations       | my_reservations.html  | My Reservations        | reservations-page (Div), reservations-table (Table), cancel-reservation-button-{reservation_id} (Button), back-to-dashboard (Button) |
| My Reviews            | my_reviews.html       | My Reviews             | reviews-page (Div), reviews-list (Div), edit-review-button-{review_id} (Button), delete-review-button-{review_id} (Button), back-to-dashboard (Button) |
| Write Review          | write_review.html     | Write Review           | write-review-page (Div), book-info-display (Div), rating-input (Dropdown), review-text (Textarea), submit-review-button (Button), back-to-book (Button) |
| User Profile          | profile.html          | My Profile             | profile-page (Div), profile-username (Div), profile-email (Input), update-profile-button (Button), borrow-history (Div), back-to-dashboard (Button) |
| Payment Confirmation  | payment_confirmation.html | Payment Confirmation | payment-page (Div), fine-amount-display (Div), confirm-payment-button (Button), back-to-profile (Button)                      |

## Section 3: Data Persistence and Local Text Files

- Directory: `data/`

- `users.txt`
  - Format: `username|email|phone|address`
  - Usage: Accessed and updated in /profile for user info.

- `books.txt`
  - Format: `book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating`
  - Usage: Loaded on /catalog (list), /book/id (detail); updated book status on borrow/reserve.

- `borrowings.txt`
  - Format: `borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount`
  - Usage: Managed on /my-borrows (list, filter), /borrow (add), /return (update), /profile (history).

- `reservations.txt`
  - Format: `reservation_id|username|book_id|reservation_date|status`
  - Usage: Managed on /my-reservations (list, cancel).

- `reviews.txt`
  - Format: `review_id|username|book_id|rating|review_text|review_date`
  - Usage: Display and edit on /book, /my-reviews, /write-review.

- `fines.txt`
  - Format: `fine_id|username|borrow_id|amount|status|date_issued`
  - Usage: Display and update payment status on /payment.

### Data handling:
- Read files on GET requests, parse on "|" delimiter to populate contexts.
- POST requests write back to files overwriting or appending as needed.
- Borrow due dates calculated as 14 days from borrow date and saved in borrowings.txt.
- Status fields in `books.txt` and others updated to reflect current state.

---

This updated design_debate_a.md incorporates peer design improvements, including expanded HTTP methods (POST) for forms, added `/dashboard` route alias for default `/`, detailed form and navigation flows, and confirms data handling and template file usages consistent with user specifications.