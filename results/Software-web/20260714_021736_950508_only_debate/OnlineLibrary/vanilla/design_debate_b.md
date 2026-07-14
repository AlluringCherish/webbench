# design_debate_b.md

## Section 1: Flask Route Contracts

### 1. Default Route
- Route: `/`
- Method: GET
- Action: Render Dashboard page
- Template: `dashboard.html`
- Context Variables:
  - username

### 2. Dashboard Page
- Route: `/dashboard`
- Method: GET
- Template: `dashboard.html`
- Context Variables: username
- Element IDs: `dashboard-page`, `welcome-message`, `browse-books-button`, `my-borrows-button`
- Navigation:
  - `browse-books-button` -> `/catalog`
  - `my-borrows-button` -> `/my-borrows`

### 3. Book Catalog Page
- Route: `/catalog`
- Methods: GET, POST (for search)
- Template: `catalog.html`
- Context Variables:
  - books (list of books from `books.txt`)
  - search_query (optional, from POST)
- Element IDs:
  - `catalog-page`, `search-input`, `book-grid`, `view-book-button-{book_id}`, `back-to-dashboard`
- Navigation:
  - `view-book-button-{book_id}` -> `/book/{book_id}`
  - `back-to-dashboard` -> `/dashboard`

### 4. Book Details Page
- Route: `/book/<int:book_id>`
- Method: GET
- Template: `book_details.html`
- Context Variables:
  - book (from `books.txt`)
  - reviews (from `reviews.txt` for this book)
- Element IDs:
  - `book-details-page`, `book-title`, `book-author`, `book-status`, `borrow-button`, `reviews-section`, `write-review-button`, `back-to-catalog`
- Navigation:
  - `borrow-button` -> `/borrow/{book_id}`
  - `write-review-button` -> `/write-review/{book_id}`
  - `back-to-catalog` -> `/catalog`

### 5. Borrow Confirmation Page
- Route: `/borrow/<int:book_id>`
- Methods: GET, POST
- Template: `borrow_confirmation.html`
- Context Variables:
  - book
  - due_date (14 days from current date)
- Element IDs:
  - `borrow-page`, `borrow-book-info`, `due-date-display`, `confirm-borrow-button`, `cancel-borrow-button`
- Navigation:
  - `confirm-borrow-button` (POST): confirm borrowing, update `borrowings.txt`
  - `cancel-borrow-button` -> `/book/{book_id}`

### 6. My Borrowings Page
- Route: `/my-borrows`
- Methods: GET, POST (for filtering)
- Template: `my_borrows.html`
- Context Variables:
  - borrows (from `borrowings.txt`)
  - filter_status
- Element IDs:
  - `my-borrows-page`, `filter-status`, `borrows-table`, `return-book-button-{borrow_id}`, `back-to-dashboard`
- Navigation:
  - `return-book-button-{borrow_id}` (POST): return book
  - `back-to-dashboard` -> `/dashboard`

### 7. My Reservations Page
- Route: `/my-reservations`
- Method: GET
- Template: `my_reservations.html`
- Context Variables:
  - reservations (from `reservations.txt`)
- Element IDs:
  - `reservations-page`, `reservations-table`, `cancel-reservation-button-{reservation_id}`, `back-to-dashboard`
- Navigation:
  - `cancel-reservation-button-{reservation_id}` (POST): cancel reservation
  - `back-to-dashboard` -> `/dashboard`

### 8. My Reviews Page
- Route: `/my-reviews`
- Method: GET
- Template: `my_reviews.html`
- Context Variables:
  - reviews (from `reviews.txt`)
- Element IDs:
  - `reviews-page`, `reviews-list`, `edit-review-button-{review_id}`, `delete-review-button-{review_id}`, `back-to-dashboard`
- Navigation:
  - `edit-review-button-{review_id}` -> `/write-review/{book_id}`
  - `delete-review-button-{review_id}` (POST): delete review
  - `back-to-dashboard` -> `/dashboard`

### 9. Write Review Page
- Route: `/write-review/<int:book_id>`
- Methods: GET, POST
- Template: `write_review.html`
- Context Variables:
  - book
  - existing_review (optional if editing)
- Element IDs:
  - `write-review-page`, `book-info-display`, `rating-input`, `review-text`, `submit-review-button`, `back-to-book`
- Navigation:
  - `submit-review-button` (POST): submit review
  - `back-to-book` -> `/book/{book_id}`

### 10. User Profile Page
- Route: `/profile`
- Methods: GET, POST
- Template: `profile.html`
- Context Variables:
  - username
  - email (from `users.txt`)
  - borrow_history
- Element IDs:
  - `profile-page`, `profile-username`, `profile-email`, `update-profile-button`, `borrow-history`, `back-to-dashboard`
- Navigation:
  - `update-profile-button` (POST): update email
  - `back-to-dashboard` -> `/dashboard`

### 11. Payment Confirmation Page
- Route: `/payment/<int:fine_id>`
- Methods: GET, POST
- Template: `payment_confirmation.html`
- Context Variables:
  - fine (from `fines.txt`)
- Element IDs:
  - `payment-page`, `fine-amount-display`, `confirm-payment-button`, `back-to-profile`
- Navigation:
  - `confirm-payment-button` (POST): confirm payment
  - `back-to-profile` -> `/profile`

## Section 2: Context Variables and Page Navigation

### Context Variables
- username
- book
- books
- reviews
- borrows
- reservations
- existing_review
- fine
- filter_status
- borrow_history

### Element IDs
- Dashboard: `dashboard-page`, `welcome-message`, `browse-books-button`, `my-borrows-button`
- Catalog: `catalog-page`, `search-input`, `book-grid`, `view-book-button-{book_id}`, `back-to-dashboard`
- Book Details: `book-details-page`, `book-title`, `book-author`, `book-status`, `borrow-button`, `reviews-section`, `write-review-button`, `back-to-catalog`
- Borrow Confirmation: `borrow-page`, `borrow-book-info`, `due-date-display`, `confirm-borrow-button`, `cancel-borrow-button`
- My Borrowings: `my-borrows-page`, `filter-status`, `borrows-table`, `return-book-button-{borrow_id}`, `back-to-dashboard`
- My Reservations: `reservations-page`, `reservations-table`, `cancel-reservation-button-{reservation_id}`, `back-to-dashboard`
- My Reviews: `reviews-page`, `reviews-list`, `edit-review-button-{review_id}`, `delete-review-button-{review_id}`, `back-to-dashboard`
- Write Review: `write-review-page`, `book-info-display`, `rating-input`, `review-text`, `submit-review-button`, `back-to-book`
- Profile: `profile-page`, `profile-username`, `profile-email`, `update-profile-button`, `borrow-history`, `back-to-dashboard`
- Payment: `payment-page`, `fine-amount-display`, `confirm-payment-button`, `back-to-profile`

### Navigation Flows
- Dashboard:
  - `browse-books-button` to `/catalog`
  - `my-borrows-button` to `/my-borrows`
  - `back-to-dashboard` from other pages returns here
- Catalog:
  - `view-book-button-{book_id}` to `/book/{book_id}`
  - `back-to-dashboard` to `/dashboard`
- Book Details:
  - `borrow-button` to `/borrow/{book_id}`
  - `write-review-button` to `/write-review/{book_id}`
  - `back-to-catalog` to `/catalog`
- Borrow Confirmation:
  - `confirm-borrow-button` (POST) confirms borrow
  - `cancel-borrow-button` to `/book/{book_id}`
- My Borrowings:
  - `return-book-button-{borrow_id}` (POST) returns book
  - `back-to-dashboard` to `/dashboard`
- My Reservations:
  - `cancel-reservation-button-{reservation_id}` (POST) cancels reservation
  - `back-to-dashboard` to `/dashboard`
- My Reviews:
  - `edit-review-button-{review_id}` to `/write-review/{book_id}`
  - `delete-review-button-{review_id}` (POST) deletes review
  - `back-to-dashboard` to `/dashboard`
- Write Review:
  - `submit-review-button` (POST) submits review
  - `back-to-book` to `/book/{book_id}`
- Profile:
  - `update-profile-button` (POST) updates email
  - `back-to-dashboard` to `/dashboard`
- Payment:
  - `confirm-payment-button` (POST) confirms payment
  - `back-to-profile` to `/profile`

## Section 3: Local Text Data Integration

### Data Files
- `data/users.txt`
  - Format: `username|email|phone|address`
  - Used in Profile
- `data/books.txt`
  - Format: `book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating`
  - Used in Catalog, Book Details
- `data/borrowings.txt`
  - Format: `borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount`
  - Used in My Borrowings, Borrow Confirmation, Profile
- `data/reservations.txt`
  - Format: `reservation_id|username|book_id|reservation_date|status`
  - Used in My Reservations
- `data/reviews.txt`
  - Format: `review_id|username|book_id|rating|review_text|review_date`
  - Used in Book Details, My Reviews, Write Review
- `data/fines.txt`
  - Format: `fine_id|username|borrow_id|amount|status|date_issued`
  - Used in Payment Confirmation

### Data Handling
- All files parsed on GET requests to populate context for templates
- Updates written back to files on POST requests
- Consistent use of `|` delimiter and preservation of data structure
- Date calculations and status updates handled within route logic


This revised design_debate_b.md honors the user requirements while refining and aligning closely with design_debate_a.md. It emphasizes clarity in navigation, element IDs, and data contract fidelity to enable full implementation.
