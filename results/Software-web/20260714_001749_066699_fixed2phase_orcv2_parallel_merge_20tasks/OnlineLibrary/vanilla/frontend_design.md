# OnlineLibrary Frontend Design Specifications

---

## Section 1: HTML Template Specifications

### 1. Dashboard Page
- **Template Filename**: dashboard.html
- **Page Title**: Library Dashboard
- **Elements:**
  - `dashboard-page`: div - Main container for dashboard page
  - `welcome-message`: h1 - Displays welcome message with username
  - `browse-books-button`: button - Navigates to Book Catalog page
  - `my-borrows-button`: button - Navigates to My Borrowings page

### 2. Book Catalog Page
- **Template Filename**: catalog.html
- **Page Title**: Book Catalog
- **Elements:**
  - `catalog-page`: div - Container for book catalog page
  - `search-input`: input (type=text) - Search books by title or author
  - `book-grid`: div - Grid container for book cards
  - `view-book-button-{book_id}`: button - On each book card, navigates to Book Details page
  - `back-to-dashboard`: button - Navigates back to Dashboard

### 3. Book Details Page
- **Template Filename**: book_details.html
- **Page Title**: Book Details
- **Elements:**
  - `book-details-page`: div - Container for book details page
  - `book-title`: h1 - Displays book title
  - `book-author`: div - Displays book author
  - `book-status`: div - Displays book availability status (Available, Borrowed, Reserved)
  - `borrow-button`: button - Button to borrow the book
  - `reviews-section`: div - Section showing user reviews for the book
  - `write-review-button`: button - Navigates to Write Review page
  - `back-to-catalog`: button - Navigates back to Book Catalog

### 4. Borrow Confirmation Page
- **Template Filename**: borrow_confirmation.html
- **Page Title**: Borrow Confirmation
- **Elements:**
  - `borrow-page`: div - Container for borrow confirmation page
  - `borrow-book-info`: div - Display info about the book to borrow
  - `due-date-display`: div - Shows due date for book return
  - `confirm-borrow-button`: button - Confirm borrowing the book
  - `cancel-borrow-button`: button - Cancel borrowing and go back to previous page

### 5. My Borrowings Page
- **Template Filename**: my_borrowings.html
- **Page Title**: My Borrowings
- **Elements:**
  - `my-borrows-page`: div - Container for my borrowings page
  - `filter-status`: select (dropdown) - Filter borrow records by All, Active, Returned, Overdue
  - `borrows-table`: table - Lists borrowed books with columns: title, borrow date, due date, status
  - `return-book-button-{borrow_id}`: button - Returns a specific active borrowed book
  - `back-to-dashboard`: button - Navigates back to Dashboard

### 6. My Reservations Page
- **Template Filename**: my_reservations.html
- **Page Title**: My Reservations
- **Elements:**
  - `reservations-page`: div - Container for reservations page
  - `reservations-table`: table - Lists reserved books with columns: title, reservation date, status
  - `cancel-reservation-button-{reservation_id}`: button - Cancels a specific reservation
  - `back-to-dashboard`: button - Navigates back to Dashboard

### 7. My Reviews Page
- **Template Filename**: my_reviews.html
- **Page Title**: My Reviews
- **Elements:**
  - `reviews-page`: div - Container for reviews page
  - `reviews-list`: div - List container for user-written reviews
  - `edit-review-button-{review_id}`: button - Edits a specific review
  - `delete-review-button-{review_id}`: button - Deletes a specific review
  - `back-to-dashboard`: button - Navigates back to Dashboard

### 8. Write Review Page
- **Template Filename**: write_review.html
- **Page Title**: Write Review
- **Elements:**
  - `write-review-page`: div - Container for write review page
  - `book-info-display`: div - Displays info about the book being reviewed
  - `rating-input`: select (dropdown) - Select rating from 1 to 5 stars
  - `review-text`: textarea - Textarea for writing review text
  - `submit-review-button`: button - Button to submit the review
  - `back-to-book`: button - Navigates back to Book Details

### 9. User Profile Page
- **Template Filename**: profile.html
- **Page Title**: My Profile
- **Elements:**
  - `profile-page`: div - Container for profile page
  - `profile-username`: div - Displays username (non-editable)
  - `profile-email`: input (type=email) - Editable email input field
  - `update-profile-button`: button - Saves updated profile info
  - `borrow-history`: div - Displays list of all previously borrowed books
  - `back-to-dashboard`: button - Navigates back to Dashboard

### 10. Payment Confirmation Page
- **Template Filename**: payment_confirmation.html
- **Page Title**: Payment Confirmation
- **Elements:**
  - `payment-page`: div - Container for payment confirmation page
  - `fine-amount-display`: div - Displays amount of fine to pay
  - `confirm-payment-button`: button - Confirm payment of fine
  - `back-to-profile`: button - Navigates back to Profile page

---

## Section 2: Navigation and Interactivity

### Navigation Paths
- Dashboard (`dashboard.html`) is the home landing page.
- From Dashboard:
  - `browse-books-button` -> Book Catalog page (`catalog.html`)
  - `my-borrows-button` -> My Borrowings page (`my_borrowings.html`)
- From Book Catalog:
  - `view-book-button-{book_id}` -> Book Details page (`book_details.html`) for selected book
  - `back-to-dashboard` -> Dashboard page
- From Book Details:
  - `borrow-button` -> Borrow Confirmation page (`borrow_confirmation.html`)
  - `write-review-button` -> Write Review page (`write_review.html`)
  - `back-to-catalog` -> Book Catalog page
- From Borrow Confirmation:
  - `confirm-borrow-button` -> Complete borrowing process, redirect to My Borrowings or confirmation message.
  - `cancel-borrow-button` -> Back to Book Details page
- From My Borrowings:
  - `return-book-button-{borrow_id}` -> Trigger return book process (refresh My Borrowings after)
  - `filter-status` dropdown -> Filters borrowings displayed in `borrows-table`
  - `back-to-dashboard` -> Dashboard page
- From My Reservations:
  - `cancel-reservation-button-{reservation_id}` -> Cancels reservation (refresh reservations table after)
  - `back-to-dashboard` -> Dashboard page
- From My Reviews:
  - `edit-review-button-{review_id}` -> Navigate to Write Review page with review pre-loaded
  - `delete-review-button-{review_id}` -> Deletes review (refresh reviews list after)
  - `back-to-dashboard` -> Dashboard page
- From Write Review:
  - `submit-review-button` -> Submits review and navigates back to Book Details page
  - `back-to-book` -> Book Details page
- From Profile:
  - `update-profile-button` -> Saves profile updates
  - `back-to-dashboard` -> Dashboard page
- From Payment Confirmation:
  - `confirm-payment-button` -> Confirms payment and returns to Profile
  - `back-to-profile` -> Profile page

### UI Behaviors & Interactions
- **Search Input (`search-input`) on Catalog Page:**
  - On key input or search submit, filters the `book-grid` dynamically by title or author.
- **Book Grid (`book-grid`):**
  - Dynamically populated with book cards based on search or filters.
- **Borrow Button (`borrow-button`) Behavior:**
  - Disabled or hidden if book status is not "Available".
- **Filter Dropdown (`filter-status`) on My Borrowings:**
  - Changes the visible rows in `borrows-table` based on selected status filter.
- **Return Book Button (`return-book-button-{borrow_id}`):**
  - Upon click, triggers book return logic and refreshes table.
- **Cancel Reservation Button (`cancel-reservation-button-{reservation_id}`):**
  - Cancels reservation and refreshes reservations list.
- **Edit Review Button (`edit-review-button-{review_id}`):**
  - Loads review data into Write Review page for editing.
- **Delete Review Button (`delete-review-button-{review_id}`):**
  - Deletes the review after confirmation, updates review list.
- **Form Submission Buttons (`confirm-borrow-button`, `submit-review-button`, `update-profile-button`, `confirm-payment-button`):**
  - Validate inputs where required, provide user feedback on success or errors.
- **User Feedback Placement:**
  - Confirmation messages or errors displayed near relevant buttons or sections (e.g., next to `confirm-borrow-button`, `submit-review-button`, `update-profile-button`).

---

This specification provides clear container IDs, elements, navigation routes, and expected interactive behaviors to fully implement the OnlineLibrary frontend templates and UI logic.