# OnlineLibrary Web Application Design Specification

---

## Section 1: Web Pages and Elements

### 1. Dashboard Page
- **Page Title**: Library Dashboard
- **Overview**: Main hub with featured books and navigation.
- **Elements**:
  - ID: `dashboard-page` (Div) - Container for dashboard.
  - ID: `welcome-message` (H1) - Displays welcome message with username.
  - ID: `browse-books-button` (Button) - Navigates to Book Catalog.
  - ID: `my-borrows-button` (Button) - Navigates to My Borrowings.

---

### 2. Book Catalog Page
- **Page Title**: Book Catalog
- **Overview**: Displays all books with search and filter.
- **Elements**:
  - ID: `catalog-page` (Div) - Container for catalog.
  - ID: `search-input` (Input) - Search field by title or author.
  - ID: `book-grid` (Div) - Grid of book cards (cover, title, author, status).
  - ID: `view-book-button-{book_id}` (Button) - Navigate to Book Details for each book.
  - ID: `back-to-dashboard` (Button) - Back to Dashboard.

---

### 3. Book Details Page
- **Page Title**: Book Details
- **Overview**: Detailed info of selected book.
- **Elements**:
  - ID: `book-details-page` (Div) - Container.
  - ID: `book-title` (H1) - Title display.
  - ID: `book-author` (Div) - Author display.
  - ID: `book-status` (Div) - Availability status.
  - ID: `borrow-button` (Button) - Borrow the book.
  - ID: `reviews-section` (Div) - User reviews.
  - ID: `write-review-button` (Button) - Write a review.
  - ID: `back-to-catalog` (Button) - Return to catalog.

---

### 4. Borrow Confirmation Page
- **Page Title**: Borrow Confirmation
- **Overview**: Confirm borrow details.
- **Elements**:
  - ID: `borrow-page` (Div) - Container.
  - ID: `borrow-book-info` (Div) - Book info.
  - ID: `due-date-display` (Div) - Due date (14 days from borrow).
  - ID: `confirm-borrow-button` (Button) - Confirm borrow.
  - ID: `cancel-borrow-button` (Button) - Cancel and go back.

---

### 5. My Borrowings Page
- **Page Title**: My Borrowings
- **Overview**: Shows books currently borrowed.
- **Elements**:
  - ID: `my-borrows-page` (Div) - Container.
  - ID: `filter-status` (Dropdown) - Filter by status (All, Active, Returned, Overdue).
  - ID: `borrows-table` (Table) - Lists borrows with title, dates, status.
  - ID: `return-book-button-{borrow_id}` (Button) - Return active borrow.
  - ID: `back-to-dashboard` (Button) - Back to Dashboard.

---

### 6. My Reservations Page
- **Page Title**: My Reservations
- **Overview**: Displays user reservations.
- **Elements**:
  - ID: `reservations-page` (Div) - Container.
  - ID: `reservations-table` (Table) - Reservation list with title, date, status.
  - ID: `cancel-reservation-button-{reservation_id}` (Button) - Cancel reservation.
  - ID: `back-to-dashboard` (Button) - Back to Dashboard.

---

### 7. My Reviews Page
- **Page Title**: My Reviews
- **Overview**: Displays user-written reviews.
- **Elements**:
  - ID: `reviews-page` (Div) - Container.
  - ID: `reviews-list` (Div) - List of reviews with book title, rating, text.
  - ID: `edit-review-button-{review_id}` (Button) - Edit review.
  - ID: `delete-review-button-{review_id}` (Button) - Delete review.
  - ID: `back-to-dashboard` (Button) - Back to Dashboard.

---

### 8. Write Review Page
- **Page Title**: Write Review
- **Overview**: Write or edit a review.
- **Elements**:
  - ID: `write-review-page` (Div) - Container.
  - ID: `book-info-display` (Div) - Book info being reviewed.
  - ID: `rating-input` (Dropdown) - Select rating (1-5 stars).
  - ID: `review-text` (Textarea) - Write review text.
  - ID: `submit-review-button` (Button) - Submit review.
  - ID: `back-to-book` (Button) - Back to book details.

---

### 9. User Profile Page
- **Page Title**: My Profile
- **Overview**: View/edit user profile.
- **Elements**:
  - ID: `profile-page` (Div) - Container.
  - ID: `profile-username` (Div) - Username display (non-editable).
  - ID: `profile-email` (Input) - Update email.
  - ID: `update-profile-button` (Button) - Save changes.
  - ID: `borrow-history` (Div) - List all previous borrows.
  - ID: `back-to-dashboard` (Button) - Back to Dashboard.

---

### 10. Payment Confirmation Page
- **Page Title**: Payment Confirmation
- **Overview**: Confirm overdue fine payment.
- **Elements**:
  - ID: `payment-page` (Div) - Container.
  - ID: `fine-amount-display` (Div) - Display fine to pay.
  - ID: `confirm-payment-button` (Button) - Confirm payment.
  - ID: `back-to-profile` (Button) - Back to profile.

---

## Section 2: Data Storage Design

All data files are stored in the `data` directory. The pipe character (`|`) is used as a delimiter.

### 1. Users Data
- Filename: `users.txt`
- Fields (in order): username|email|phone|address
- Example:
  ```
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St
  ```

### 2. Books Data
- Filename: `books.txt`
- Fields (in order): book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating
- Example:
  ```
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5
  5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3
  ```

### 3. Borrowings Data
- Filename: `borrowings.txt`
- Fields (in order): borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount
- Example:
  ```
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00
  ```

### 4. Reservations Data
- Filename: `reservations.txt`
- Fields (in order): reservation_id|username|book_id|reservation_date|status
- Example:
  ```
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled
  ```

### 5. Reviews Data
- Filename: `reviews.txt`
- Fields (in order): review_id|username|book_id|rating|review_text|review_date
- Example:
  ```
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20
  ```

### 6. Fines Data
- Filename: `fines.txt`
- Fields (in order): fine_id|username|borrow_id|amount|status|date_issued
- Example:
  ```
  1|john_reader|3|5.00|Unpaid|2024-10-30
  ```

---

## Section 3: Navigation and Inter-page Relationships

- **Dashboard Page:**
  - `browse-books-button` navigates to **Book Catalog Page**.
  - `my-borrows-button` navigates to **My Borrowings Page**.

- **Book Catalog Page:**
  - `view-book-button-{book_id}` navigates to **Book Details Page** for selected book.
  - `back-to-dashboard` navigates to **Dashboard Page**.

- **Book Details Page:**
  - `borrow-button` navigates to **Borrow Confirmation Page**.
  - `write-review-button` navigates to **Write Review Page**.
  - `back-to-catalog` navigates to **Book Catalog Page**.

- **Borrow Confirmation Page:**
  - `confirm-borrow-button` processes borrow and returns to **My Borrowings Page**.
  - `cancel-borrow-button` navigates back to **Book Details Page**.

- **My Borrowings Page:**
  - `return-book-button-{borrow_id}` triggers return action.
  - `back-to-dashboard` navigates to **Dashboard Page**.

- **My Reservations Page:**
  - `cancel-reservation-button-{reservation_id}` cancels reservation.
  - `back-to-dashboard` navigates to **Dashboard Page**.

- **My Reviews Page:**
  - `edit-review-button-{review_id}` navigates to **Write Review Page** (edit mode).
  - `delete-review-button-{review_id}` deletes review.
  - `back-to-dashboard` navigates to **Dashboard Page**.

- **Write Review Page:**
  - `submit-review-button` submits review and returns to **Book Details Page**.
  - `back-to-book` navigates to **Book Details Page**.

- **User Profile Page:**
  - `update-profile-button` saves profile updates.
  - `back-to-dashboard` navigates to **Dashboard Page**.

- **Payment Confirmation Page:**
  - `confirm-payment-button` processes payment and returns to **User Profile Page**.
  - `back-to-profile` navigates to **User Profile Page**.

---

*End of Design Specification Document for OnlineLibrary*