# Design Candidate for OnlineLibrary Web Application

---

## 1. Route and Template Mapping

| Route Path             | HTTP Methods | Template Filename           | Description                        |
|------------------------|--------------|-----------------------------|----------------------------------|
| /dashboard             | GET          | dashboard.html              | Library Dashboard main hub        |
| /catalog               | GET          | catalog.html                | Book Catalog with search/filter  |
| /book/<int:book_id>    | GET          | book_details.html           | Details of a specific book        |
| /borrow/<int:book_id>  | GET, POST    | borrow_confirmation.html    | Confirm borrowing a book          |
| /my-borrows            | GET          | my_borrowings.html          | List user's current borrows       |
| /my-reservations       | GET          | my_reservations.html        | List user's book reservations     |
| /my-reviews            | GET          | my_reviews.html             | List user's written reviews       |
| /write-review/<int:book_id>  | GET, POST    | write_review.html            | Write or edit review for book     |
| /profile               | GET, POST    | profile.html                | User profile view and edit        |
| /payment/<int:fine_id> | GET, POST    | payment_confirmation.html   | Confirm overdue fine payment      |

---

## 2. Page Titles and Element IDs

### 2.1 Dashboard Page
- Page Title: `Library Dashboard`
- Elements:
  - `dashboard-page`: Div container for entire dashboard page.
  - `welcome-message`: H1 displaying user’s welcome with username.
  - `browse-books-button`: Button navigating to `/catalog`.
  - `my-borrows-button`: Button navigating to `/my-borrows`.

### 2.2 Book Catalog Page
- Page Title: `Book Catalog`
- Elements:
  - `catalog-page`: Div container for catalog page.
  - `search-input`: Input field for live search by title/author.
  - `book-grid`: Div grid displaying book cards.
  - `view-book-button-{book_id}`: Button on each book card to view details.
  - `back-to-dashboard`: Button to go back to `/dashboard`.

### 2.3 Book Details Page
- Page Title: `Book Details`
- Elements:
  - `book-details-page`: Div container.
  - `book-title`: H1 showing book title.
  - `book-author`: Div showing author name.
  - `book-status`: Div showing availability status.
  - `borrow-button`: Button to borrow if book is Available.
  - `reviews-section`: Div listing reviews for the book.
  - `write-review-button`: Button to write a review.
  - `back-to-catalog`: Button to return to `/catalog`.

### 2.4 Borrow Confirmation Page
- Page Title: `Borrow Confirmation`
- Elements:
  - `borrow-page`: Div container.
  - `borrow-book-info`: Div showing book details being borrowed.
  - `due-date-display`: Div showing due date (14 days from now).
  - `confirm-borrow-button`: Button to confirm borrowing (POST).
  - `cancel-borrow-button`: Button to cancel and go back to book details.

### 2.5 My Borrowings Page
- Page Title: `My Borrowings`
- Elements:
  - `my-borrows-page`: Div container.
  - `filter-status`: Dropdown to filter borrows (All, Active, Returned, Overdue).
  - `borrows-table`: Table with borrow rows: title, borrow date, due date, status.
  - `return-book-button-{borrow_id}`: Button to return active borrowed book.
  - `back-to-dashboard`: Button to `/dashboard`.

### 2.6 My Reservations Page
- Page Title: `My Reservations`
- Elements:
  - `reservations-page`: Div container.
  - `reservations-table`: Table with rows: book title, reservation date, status.
  - `cancel-reservation-button-{reservation_id}`: Button to cancel reservation.
  - `back-to-dashboard`: Button to `/dashboard`.

### 2.7 My Reviews Page
- Page Title: `My Reviews`
- Elements:
  - `reviews-page`: Div container.
  - `reviews-list`: Div showing reviews with book title, rating, review text.
  - `edit-review-button-{review_id}`: Button to edit respective review.
  - `delete-review-button-{review_id}`: Button to delete respective review.
  - `back-to-dashboard`: Button to `/dashboard`.

### 2.8 Write Review Page
- Page Title: `Write Review`
- Elements:
  - `write-review-page`: Div container.
  - `book-info-display`: Div showing book info being reviewed.
  - `rating-input`: Dropdown for selecting rating 1-5.
  - `review-text`: Textarea for review content.
  - `submit-review-button`: Button to submit (POST).
  - `back-to-book`: Button to return to book details.

### 2.9 User Profile Page
- Page Title: `My Profile`
- Elements:
  - `profile-page`: Div container.
  - `profile-username`: Div showing username (readonly).
  - `profile-email`: Input to update email address.
  - `update-profile-button`: Button to save changes (POST).
  - `borrow-history`: Div listing all previous borrows.
  - `back-to-dashboard`: Button to `/dashboard`.

### 2.10 Payment Confirmation Page
- Page Title: `Payment Confirmation`
- Elements:
  - `payment-page`: Div container.
  - `fine-amount-display`: Div showing fine amount.
  - `confirm-payment-button`: Button to confirm payment (POST).
  - `back-to-profile`: Button to go back to profile page.

---

## 3. Context Variables per Route

### /dashboard (GET)
- `username`: str - Current logged-in user's username.
- `featured_books`: list of dicts - Featured books to show, each dict with:
  - `book_id` (int)
  - `title` (str)
  - `author` (str)
  - `status` (str)

### /catalog (GET)
- `books`: list of dicts - All books, with keys:
  - `book_id` (int)
  - `title` (str)
  - `author` (str)
  - `status` (str)
- `search_query`: str - Current search input (empty string if none)

### /book/<book_id> (GET)
- `book`: dict with all book details:
  - `book_id` (int)
  - `title` (str)
  - `author` (str)
  - `isbn` (str)
  - `genre` (str)
  - `publisher` (str)
  - `year` (int)
  - `description` (str)
  - `status` (str)
  - `avg_rating` (float)
- `reviews`: list of dicts - Reviews for that book with:
  - `review_id` (int)
  - `username` (str)
  - `rating` (int)
  - `review_text` (str)
  - `review_date` (str, YYYY-MM-DD)
- `can_borrow`: bool - True if book is Available

### /borrow/<book_id> (GET)
- `book`: dict as above (book details)
- `due_date`: str - Date 14 days from borrow date (YYYY-MM-DD format)

### /borrow/<book_id> (POST)
- Form submission with confirmation. On success redirect to `/my-borrows`.

### /my-borrows (GET)
- `borrows`: list of dicts with:
  - `borrow_id` (int)
  - `book_title` (str)
  - `borrow_date` (str, YYYY-MM-DD)
  - `due_date` (str, YYYY-MM-DD)
  - `status` (str)
- `filter_status`: str - Current filter selection

### /my-reservations (GET)
- `reservations`: list of dicts:
  - `reservation_id` (int)
  - `book_title` (str)
  - `reservation_date` (str, YYYY-MM-DD)
  - `status` (str)

### /my-reviews (GET)
- `reviews`: list of dicts:
  - `review_id` (int)
  - `book_title` (str)
  - `rating` (int)
  - `review_text` (str)

### /write-review/<book_id> (GET)
- `book`: dict (book info with at least title, author, book_id)
- `existing_review`: dict or None if no prior review, with keys:
  - `review_id` (int)
  - `rating` (int)
  - `review_text` (str)

### /write-review/<book_id> (POST)
- Form data for rating, review_text submission; on success redirect to `/book/<book_id>`.

### /profile (GET)
- `username`: str
- `email`: str
- `borrow_history`: list of dicts:
  - `book_title` (str)
  - `borrow_date` (str)
  - `return_date` (str or empty if none)

### /profile (POST)
- Update email address.

### /payment/<fine_id> (GET)
- `fine`: dict with:
  - `fine_id` (int)
  - `amount` (str, e.g. "5.00")

### /payment/<fine_id> (POST)
- Confirm payment and update fine status.

---

## 4. User Interactions and Messages

- **Dashboard Page:**
  - `browse-books-button`: navigates user to `/catalog`.
  - `my-borrows-button`: navigates user to `/my-borrows`.

- **Book Catalog Page:**
  - Typing in `search-input` filters books in `book-grid` dynamically.
  - `view-book-button-{book_id}`: go to `/book/<book_id>`.
  - `back-to-dashboard`: back to `/dashboard`.

- **Book Details Page:**
  - `borrow-button`: visible and enabled if book status is "Available"; clicking navigates to `/borrow/<book_id>`.
  - `write-review-button`: navigates to `/write-review/<book_id>`.
  - `back-to-catalog`: return to `/catalog`.

- **Borrow Confirmation Page:**
  - `confirm-borrow-button`: submits POST to borrow the book; success message on redirect.
  - `cancel-borrow-button`: navigates back to `/book/<book_id>`.

- **My Borrowings Page:**
  - `filter-status`: filter borrowings table.
  - `return-book-button-{borrow_id}` for active borrows: submits return action and update status.
  - `back-to-dashboard`: navigates to `/dashboard`.

- **My Reservations Page:**
  - `cancel-reservation-button-{reservation_id}`: cancels specific reservation.
  - `back-to-dashboard`: returns to `/dashboard`.

- **My Reviews Page:**
  - `edit-review-button-{review_id}`: navigates to `/write-review/<book_id>` preloaded with review.
  - `delete-review-button-{review_id}`: deletes the review after confirmation.
  - `back-to-dashboard`: to `/dashboard`.

- **Write Review Page:**
  - Fill `rating-input` and `review-text`, `submit-review-button` submits data.
  - `back-to-book`: returns to book details.

- **User Profile Page:**
  - Edit `profile-email`, save with `update-profile-button`.
  - `back-to-dashboard`: returns to dashboard.

- **Payment Confirmation Page:**
  - `confirm-payment-button`: submits payment confirmation.
  - `back-to-profile`: returns to `/profile`.


---

## 5. Data Fixture Schemas

### 5.1 users.txt
- Fields: `username`|`email`|`phone`|`address`
- Example:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```

### 5.2 books.txt
- Fields: `book_id`|`title`|`author`|`isbn`|`genre`|`publisher`|`year`|`description`|`status`|`avg_rating`
- Example:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  ```

### 5.3 borrowings.txt
- Fields: `borrow_id`|`username`|`book_id`|`borrow_date`|`due_date`|`return_date`|`status`|`fine_amount`
- Example:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  ```

### 5.4 reservations.txt
- Fields: `reservation_id`|`username`|`book_id`|`reservation_date`|`status`
- Example:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```

### 5.5 reviews.txt
- Fields: `review_id`|`username`|`book_id`|`rating`|`review_text`|`review_date`
- Example:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```

### 5.6 fines.txt
- Fields: `fine_id`|`username`|`borrow_id`|`amount`|`status`|`date_issued`
- Example:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
  ```

---

This design candidate provides a detailed route-to-template mapping, page elements with IDs, context variable specifications, user interaction flows, and data file schema definitions necessary for full-stack implementation of the OnlineLibrary application.
