# OnlineLibrary Requirements Analysis

## 1. Page Descriptions

### 1. Dashboard Page
- **Title:** Library Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Container for the dashboard page.
  - `welcome-message` (H1): Displays welcome message with username.
  - `browse-books-button` (Button): Navigates to Book Catalog Page.
  - `my-borrows-button` (Button): Navigates to My Borrowings Page.
- **Purpose:** Acts as the main hub for users with quick navigation to browsing books and reviewing their borrowings.

### 2. Book Catalog Page
- **Title:** Book Catalog
- **Element IDs:**
  - `catalog-page` (Div): Container for the catalog page.
  - `search-input` (Input): Search field to filter books by title or author.
  - `book-grid` (Div): Grid container for book cards.
  - `view-book-button-{book_id}` (Button): Dynamic button per book to view Book Details Page. Example ID format: `view-book-button-1`.
  - `back-to-dashboard` (Button): Navigates back to Dashboard Page.
- **Purpose:** Display all books available with search/filter capabilities.

### 3. Book Details Page
- **Title:** Book Details
- **Element IDs:**
  - `book-details-page` (Div): Container for book details.
  - `book-title` (H1): Displays book title.
  - `book-author` (Div): Displays book author.
  - `book-status` (Div): Shows book availability status (Available, Borrowed, Reserved).
  - `borrow-button` (Button): Initiates borrowing process (leads to Borrow Confirmation).
  - `reviews-section` (Div): Displays user reviews for the book.
  - `write-review-button` (Button): Navigates to Write Review Page.
  - `back-to-catalog` (Button): Navigates back to Book Catalog Page.
- **Purpose:** Show detailed book information including status and reviews.

### 4. Borrow Confirmation Page
- **Title:** Borrow Confirmation
- **Element IDs:**
  - `borrow-page` (Div): Container for borrow confirmation.
  - `borrow-book-info` (Div): Displays book info for confirmation.
  - `due-date-display` (Div): Shows book return due date (14 days from borrow date).
  - `confirm-borrow-button` (Button): Confirms borrowing action.
  - `cancel-borrow-button` (Button): Cancels borrow process and navigates back.
- **Purpose:** Confirm details before finalizing borrowing a book.

### 5. My Borrowings Page
- **Title:** My Borrowings
- **Element IDs:**
  - `my-borrows-page` (Div): Container for borrowings page.
  - `filter-status` (Dropdown): Filter borrows by status (All, Active, Returned, Overdue).
  - `borrows-table` (Table): Lists borrowed books with fields: title, borrow date, due date, status.
  - `return-book-button-{borrow_id}` (Button): Dynamic button to return a borrowed book. Example: `return-book-button-1`.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.
- **Purpose:** Display and manage user's currently borrowed books.

### 6. My Reservations Page
- **Title:** My Reservations
- **Element IDs:**
  - `reservations-page` (Div): Container for reservations.
  - `reservations-table` (Table): Shows reserved books with title, reservation date, status.
  - `cancel-reservation-button-{reservation_id}` (Button): Dynamic cancel reservation button. Example: `cancel-reservation-button-1`.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.
- **Purpose:** Display and manage user's book reservations.

### 7. My Reviews Page
- **Title:** My Reviews
- **Element IDs:**
  - `reviews-page` (Div): Container for reviews page.
  - `reviews-list` (Div): List of user reviews showing book title, rating, and review text.
  - `edit-review-button-{review_id}` (Button): Dynamic button to edit review. Example: `edit-review-button-1`.
  - `delete-review-button-{review_id}` (Button): Dynamic button to delete review. Example: `delete-review-button-1`.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.
- **Purpose:** Manage user authored reviews.

### 8. Write Review Page
- **Title:** Write Review
- **Element IDs:**
  - `write-review-page` (Div): Container for writing/editing review.
  - `book-info-display` (Div): Displays book info under review.
  - `rating-input` (Dropdown): Dropdown to select rating (1-5 stars).
  - `review-text` (Textarea): Field for review text.
  - `submit-review-button` (Button): Submit the review.
  - `back-to-book` (Button): Navigates back to Book Details Page.
- **Purpose:** Create or edit a review for a book.

### 9. User Profile Page
- **Title:** My Profile
- **Element IDs:**
  - `profile-page` (Div): Container for profile page.
  - `profile-username` (Div): Shows username, not editable.
  - `profile-email` (Input): Input to update email.
  - `update-profile-button` (Button): Save profile changes.
  - `borrow-history` (Div): List of all previous borrows.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.
- **Purpose:** View and edit user profile details and see borrow history.

### 10. Payment Confirmation Page
- **Title:** Payment Confirmation
- **Element IDs:**
  - `payment-page` (Div): Container for payment confirmation.
  - `fine-amount-display` (Div): Shows overdue fine amount.
  - `confirm-payment-button` (Button): Confirm fine payment.
  - `back-to-profile` (Button): Navigates back to User Profile Page.
- **Purpose:** Confirm payment for fines.


## 2. Navigation Flow

| From Page            | Button ID                   | To Page             | Notes                                  |
|----------------------|-----------------------------|---------------------|----------------------------------------|
| Dashboard            | `browse-books-button`       | Book Catalog         |                                        |
| Dashboard            | `my-borrows-button`         | My Borrowings        |                                        |
| Book Catalog         | `view-book-button-{book_id}`| Book Details         | Each book card has a dynamic button.  |
| Book Catalog         | `back-to-dashboard`         | Dashboard            |                                        |
| Book Details         | `borrow-button`             | Borrow Confirmation  | If book available for borrow          |
| Book Details         | `write-review-button`       | Write Review         |                                        |
| Book Details         | `back-to-catalog`           | Book Catalog         |                                        |
| Borrow Confirmation  | `confirm-borrow-button`     | My Borrowings        | On successful borrow.                   |
| Borrow Confirmation  | `cancel-borrow-button`      | Book Details         | Cancel and go back.                    |
| My Borrowings        | `return-book-button-{borrow_id}`| Dashboard        | Returns book and refresh dashboard    |
| My Borrowings        | `back-to-dashboard`         | Dashboard            |                                        |
| My Reservations      | `cancel-reservation-button-{reservation_id}` | Dashboard | Cancel reservation and refresh dashboard |
| My Reservations      | `back-to-dashboard`         | Dashboard            |                                        |
| My Reviews           | `edit-review-button-{review_id}` | Write Review    | Edit existing review                   |
| My Reviews           | `delete-review-button-{review_id}` | Refresh Reviews | Delete review and refresh reviews list|
| My Reviews           | `back-to-dashboard`         | Dashboard            |                                        |
| Write Review         | `submit-review-button`      | Book Details         | Submit review and navigate back       |
| Write Review         | `back-to-book`              | Book Details         | Cancel and navigate back               |
| User Profile         | `update-profile-button`     | User Profile         | Saves profile and stays                |
| User Profile         | `back-to-dashboard`         | Dashboard            |                                        |
| Payment Confirmation | `confirm-payment-button`    | User Profile         | On payment confirmation                |
| Payment Confirmation | `back-to-profile`           | User Profile         | Cancel and navigate back               |


## 3. Data Storage Formats

All data files are stored in the directory: `data/`

### 1. Users Data (`users.txt`)
- Format: `username|email|phone|address`
- Example: `john_reader|john@example.com|555-1234|123 Main St`

### 2. Books Data (`books.txt`)
- Format: `book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating`
- Example: `1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8`

### 3. Borrowings Data (`borrowings.txt`)
- Format: `borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount`
- Example: `1|john_reader|2|2024-11-01|2024-11-15||Active|0`

### 4. Reservations Data (`reservations.txt`)
- Format: `reservation_id|username|book_id|reservation_date|status`
- Example: `1|jane_doe|4|2024-11-10|Active`

### 5. Reviews Data (`reviews.txt`)
- Format: `review_id|username|book_id|rating|review_text|review_date`
- Example: `1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03`

### 6. Fines Data (`fines.txt`)
- Format: `fine_id|username|borrow_id|amount|status|date_issued`
- Example: `1|john_reader|3|5.00|Unpaid|2024-10-30`


## 4. User Flows

### Borrowing a Book
1. User starts at `Dashboard`.
2. Clicks `browse-books-button` to navigate to `Book Catalog`.
3. Uses `search-input` to find a book.
4. Clicks `view-book-button-{book_id}` to see `Book Details`.
5. If book status is 'Available', clicks `borrow-button`.
6. On `Borrow Confirmation` page, reviews details including `due-date-display`.
7. Clicks `confirm-borrow-button` to borrow. System updates `borrowings.txt`.
8. Confirmation leads to `My Borrowings` page.

### Returning a Book
1. From `Dashboard`, clicks `my-borrows-button` to go to `My Borrowings`.
2. Uses `filter-status` dropdown to filter borrowings.
3. Finds the active borrow and clicks `return-book-button-{borrow_id}`.
4. Book returns processed, updates `borrowings.txt`.
5. User navigated back to `Dashboard` or refreshed borrowings.

### Reserving a Book
1. (Assuming reservation is available from catalog or details page - flow not explicitly stated but inferred.)
2. User reserves a book; reservation stored in `reservations.txt`.
3. Can manage reservations from `My Reservations` page.
4. Cancels reservation with `cancel-reservation-button-{reservation_id}` if desired.

### Writing and Managing Reviews
1. From `Book Details`, user clicks `write-review-button` to create review.
2. Inputs rating with `rating-input` and text with `review-text`.
3. Clicks `submit-review-button` to save review in `reviews.txt`.
4. Reviews are visible in `reviews-section` on Book Details.
5. From `My Reviews`, user can `edit-review-button-{review_id}` or `delete-review-button-{review_id}` reviews.

### Managing Profile and Payments
1. From `Dashboard`, user accesses `User Profile` page.
2. Updates email via `profile-email` and clicks `update-profile-button`.
3. Views borrow history in `borrow-history`.
4. If fines exist, navigates to `Payment Confirmation` to pay.
5. Confirms payment via `confirm-payment-button`, updates `fines.txt`.


---

This document consolidates all page elements, navigation flows, data formats, and typical user interactions for clear architectural and implementation guidance for the 'OnlineLibrary' web application.