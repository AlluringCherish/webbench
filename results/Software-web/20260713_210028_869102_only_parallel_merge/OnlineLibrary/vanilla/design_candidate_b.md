# Alternative Design Candidate B for OnlineLibrary Web Application

## 1. Flask Routes and Templates

### Route: `/` or `/dashboard`
- Methods: GET
- Template: `dashboard_b.html`

### Route: `/catalog`
- Methods: GET
- Template: `catalog_b.html`

### Route: `/book/<int:book_id>`
- Methods: GET
- Template: `book_details_b.html`

### Route: `/borrow/<int:book_id>`
- Methods: GET (confirm borrow page), POST (submit borrow)
- Template: `borrow_confirm_b.html`

### Route: `/my-borrows`
- Methods: GET
- Template: `my_borrows_b.html`

### Route: `/my-reservations`
- Methods: GET
- Template: `my_reservations_b.html`

### Route: `/my-reviews`
- Methods: GET
- Template: `my_reviews_b.html`

### Route: `/review/<int:book_id>`
- Methods: GET (write/edit review page), POST (submit review)
- Template: `write_review_b.html`

### Route: `/profile`
- Methods: GET, POST (update profile)
- Template: `profile_b.html`

### Route: `/payment/<int:fine_id>`
- Methods: GET, POST (confirm payment)
- Template: `payment_b.html`

---

## 2. Page Titles and UI Elements

### 1. Dashboard Page
- **Page Title**: Library Dashboard
- Container ID: `dashboard-page`
- Welcome message: ID `welcome-message` (e.g. "Welcome, {{ username }}")
- Buttons:
  - `browse-books-btn` (navigates to /catalog)
  - `my-borrows-btn` (navigates to /my-borrows)

### 2. Book Catalog Page
- **Page Title**: Book Catalog
- Container ID: `catalog-page`
- Search Input ID: `search-field` (search by title or author)
- Books grid ID: `books-grid`
- Each book card contains:
  - Cover image: ID `book-cover-{{ book_id }}`
  - Title: ID `book-title-{{ book_id }}`
  - Author: ID `book-author-{{ book_id }}`
  - Status badge: ID `book-status-{{ book_id }}` (Available, Borrowed, Reserved)
  - Button: ID `details-btn-{{ book_id }}`
- Back button ID: `back-dashboard-btn`

### 3. Book Details Page
- **Page Title**: Book Details
- Container ID: `book-details-page`
- Title: ID `book-title`
- Author: ID `book-author`
- Status text: ID `book-status`
- Borrow button: ID `borrow-book-btn` (disabled if not available)
- Reviews section ID: `reviews-section`
  - List of reviews with rating stars and text
- Write review button: ID `write-review-btn`
- Back Button ID: `back-catalog-btn`

### 4. Borrow Confirmation Page
- **Page Title**: Borrow Confirmation
- Container ID: `borrow-confirm-page`
- Book info display ID: `borrow-book-info`
- Due Date display ID: `due-date-display`
- Confirm button ID: `confirm-borrow-btn`
- Cancel button ID: `cancel-borrow-btn`

### 5. My Borrowings Page
- **Page Title**: My Borrowings
- Container ID: `my-borrows-page`
- Filter dropdown ID: `status-filter` (Options: All, Active, Returned, Overdue)
- Table ID: `borrows-table` with columns [Title, Borrow Date, Due Date, Status, Action]
- Return button per borrow: ID `return-btn-{{ borrow_id }}`
- Back button ID: `back-dashboard-btn`

### 6. My Reservations Page
- **Page Title**: My Reservations
- Container ID: `my-reservations-page`
- Reservations table ID: `reservations-table` with columns [Title, Reservation Date, Status, Action]
- Cancel reservation button per reservation: ID `cancel-reservation-btn-{{ reservation_id }}`
- Back button ID: `back-dashboard-btn`

### 7. My Reviews Page
- **Page Title**: My Reviews
- Container ID: `my-reviews-page`
- Reviews list ID: `reviews-list`
- Each review includes:
  - Book Title: ID `review-book-title-{{ review_id }}`
  - Rating stars
  - Review Text
  - Edit button ID: `edit-review-btn-{{ review_id }}`
  - Delete button ID: `delete-review-btn-{{ review_id }}`
- Back button ID: `back-dashboard-btn`

### 8. Write Review Page
- **Page Title**: Write Review
- Container ID: `write-review-page`
- Book info display ID: `review-book-info`
- Rating input dropdown ID: `rating-select` (1 to 5 stars)
- Review text area ID: `review-textarea`
- Submit button ID: `submit-review-btn`
- Back button ID: `back-book-details-btn`

### 9. User Profile Page
- **Page Title**: My Profile
- Container ID: `profile-page`
- Username display ID: `profile-username` (read-only)
- Email input ID: `email-input`
- Update profile button ID: `update-profile-btn`
- Borrow history display ID: `borrow-history-list` (list of previously borrowed books with titles and dates)
- Back button ID: `back-dashboard-btn`

### 10. Payment Confirmation Page
- **Page Title**: Payment Confirmation
- Container ID: `payment-page`
- Fine amount display ID: `fine-amount-display`
- Confirm payment button ID: `confirm-payment-btn`
- Back to profile button ID: `back-profile-btn`

---

## 3. Template Context Variables

### `/dashboard`
- `username` (str)
- `featured_books` (list of dict): [{book_id (int), title (str), author (str), cover_url (str)}]

### `/catalog`
- `books` (list of dict): [{book_id (int), title (str), author (str), status (str), cover_url (str)}]
- `search_query` (str)

### `/book/<book_id>`
- `book` (dict): {book_id (int), title (str), author (str), status (str), description (str), avg_rating (float)}
- `reviews` (list of dict): [{review_id (int), username (str), rating (int), review_text (str), review_date (str)}]
- `can_borrow` (bool)

### `/borrow/<book_id>` GET
- `book` (dict): {book_id, title, author}
- `due_date` (str) - formatted date (14 days from borrow date)

### `/borrow/<book_id>` POST
- `success` (bool)
- `message` (str)

### `/my-borrows`
- `borrowings` (list of dict): [{borrow_id (int), book_title (str), borrow_date (str), due_date (str), status (str)}]
- `filter_status` (str)

### `/my-reservations`
- `reservations` (list of dict): [{reservation_id (int), book_title (str), reservation_date (str), status (str)}]

### `/my-reviews`
- `reviews` (list of dict): [{review_id (int), book_title (str), rating (int), review_text (str)}]

### `/review/<book_id>` GET
- `book` (dict): {book_id, title}
- `review` (dict or None): {review_id, rating (int), review_text (str)} or None if no existing review

### `/profile` GET
- `username` (str)
- `email` (str)
- `borrow_history` (list of dict): [{book_title (str), borrow_date (str), return_date (str)}]

### `/profile` POST
- `success` (bool)
- `message` (str)

### `/payment/<fine_id>` GET
- `fine` (dict): {fine_id (int), amount (float)}

### `/payment/<fine_id>` POST
- `success` (bool)
- `message` (str)

---

## 4. User UI Actions and Navigation Flows

- From Dashboard:
  - Click `browse-books-btn` to navigate to `/catalog`
  - Click `my-borrows-btn` to navigate to `/my-borrows`

- From Catalog:
  - Input search in `search-field` and submit to filter books
  - Click any book's `details-btn-{{book_id}}` to view `/book/<book_id>`
  - Click `back-dashboard-btn` to return to dashboard

- From Book Details:
  - Click `borrow-book-btn` if enabled to start borrow process `/borrow/<book_id>`
  - Click `write-review-btn` to `/review/<book_id>`
  - Click `back-catalog-btn` to return to catalog

- Borrow Confirmation:
  - Click `confirm-borrow-btn` to confirm borrowing (POST)
  - Click `cancel-borrow-btn` to go back to book details

- My Borrowings:
  - Use `status-filter` dropdown to filter borrows
  - Click `return-btn-{{ borrow_id }}` to return book
  - Click `back-dashboard-btn` to dashboard

- My Reservations:
  - Click `cancel-reservation-btn-{{ reservation_id }}` to cancel reservation
  - Click `back-dashboard-btn` to dashboard

- My Reviews:
  - Click `edit-review-btn-{{ review_id }}` to edit review `/review/<book_id>`
  - Click `delete-review-btn-{{ review_id }}` to delete review
  - Click `back-dashboard-btn` to dashboard

- Write Review:
  - Select rating from `rating-select`
  - Enter text in `review-textarea`
  - Click `submit-review-btn` to save review (POST)
  - Click `back-book-details-btn` to return to `/book/<book_id>`

- Profile:
  - Edit email in `email-input`
  - Click `update-profile-btn` to save (POST)
  - View borrow history in `borrow-history-list`
  - Click `back-dashboard-btn` to dashboard

- Payment Confirmation:
  - View amount in `fine-amount-display`
  - Click `confirm-payment-btn` to pay (POST)
  - Click `back-profile-btn` to profile

---

## 5. Data File Schemas

### 1. users.txt
- Fields: `username|email|phone|address`
- Example:
  `john_reader|john@example.com|555-1234|123 Main St`

### 2. books.txt
- Fields: `book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating`
- Example:
  `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`

### 3. borrowings.txt
- Fields: `borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount`
- Example:
  `1|john_reader|2|2024-11-01|2024-11-15||Active|0`

### 4. reservations.txt
- Fields: `reservation_id|username|book_id|reservation_date|status`
- Example:
  `1|jane_doe|4|2024-11-10|Active`

### 5. reviews.txt
- Fields: `review_id|username|book_id|rating|review_text|review_date`
- Example:
  `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`

### 6. fines.txt
- Fields: `fine_id|username|borrow_id|amount|status|date_issued`
- Example:
  `1|john_reader|3|5.00|Unpaid|2024-10-30`

---

This design candidate B provides an alternative naming scheme for element IDs for clarity, reuses similar page navigation but allows clear template separation, and reframes context variables for clear structure. All UI elements are specified with precise IDs, and the user interaction flow is straightforward for implementation. Data schemas remain identical to source requirements for compatibility.