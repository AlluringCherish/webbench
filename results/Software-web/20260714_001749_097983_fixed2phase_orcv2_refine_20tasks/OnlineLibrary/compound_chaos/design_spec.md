# OnlineLibrary Web Application Design Specification

## Section 1: Web Pages and Elements

### 1. Dashboard Page
- Page Title: Library Dashboard
- Overview: The main hub displaying featured books and navigation to other functionalities.
- Elements:
  - ID: dashboard-page - Type: Div - Container for the dashboard page.
  - ID: welcome-message - Type: H1 - Welcome message displaying username.
  - ID: browse-books-button - Type: Button - Button to navigate to book catalog page.
  - ID: my-borrows-button - Type: Button - Button to navigate to my borrowings page.

### 2. Book Catalog Page
- Page Title: Book Catalog
- Overview: A page displaying all available books with filtering and search options.
- Elements:
  - ID: catalog-page - Type: Div - Container for the book catalog page.
  - ID: search-input - Type: Input - Field to search books by title or author.
  - ID: book-grid - Type: Div - Grid displaying book cards with cover, title, author, and status.
  - ID: view-book-button-{book_id} - Type: Button - Button to navigate to book details page (each book card has this).
  - ID: back-to-dashboard - Type: Button - Button to navigate back to dashboard.

### 3. Book Details Page
- Page Title: Book Details
- Overview: A page displaying detailed information about a specific book.
- Elements:
  - ID: book-details-page - Type: Div - Container for the book details page.
  - ID: book-title - Type: H1 - Display book title.
  - ID: book-author - Type: Div - Display book author.
  - ID: book-status - Type: Div - Display availability status (Available, Borrowed, Reserved).
  - ID: borrow-button - Type: Button - Button to borrow the book.
  - ID: reviews-section - Type: Div - Section displaying user reviews.
  - ID: write-review-button - Type: Button - Button to write a review.
  - ID: back-to-catalog - Type: Button - Button to navigate back to catalog.

### 4. Borrow Confirmation Page
- Page Title: Borrow Confirmation
- Overview: A page to confirm book borrowing details.
- Elements:
  - ID: borrow-page - Type: Div - Container for the borrow confirmation page.
  - ID: borrow-book-info - Type: Div - Display information about the book being borrowed.
  - ID: due-date-display - Type: Div - Display the due date for return (14 days from borrow).
  - ID: confirm-borrow-button - Type: Button - Button to confirm borrowing.
  - ID: cancel-borrow-button - Type: Button - Button to cancel and go back.

### 5. My Borrowings Page
- Page Title: My Borrowings
- Overview: A page displaying all books currently borrowed by the user.
- Elements:
  - ID: my-borrows-page - Type: Div - Container for the my borrowings page.
  - ID: filter-status - Type: Dropdown - Dropdown to filter by status (All, Active, Returned, Overdue).
  - ID: borrows-table - Type: Table - Table displaying borrowed books with title, borrow date, due date, status.
  - ID: return-book-button-{borrow_id} - Type: Button - Button to return book (each active borrow has this).
  - ID: back-to-dashboard - Type: Button - Button to navigate back to dashboard.

### 6. My Reservations Page
- Page Title: My Reservations
- Overview: A page displaying all book reservations made by the user.
- Elements:
  - ID: reservations-page - Type: Div - Container for the reservations page.
  - ID: reservations-table - Type: Table - Table displaying reserved books with title, reservation date, status.
  - ID: cancel-reservation-button-{reservation_id} - Type: Button - Button to cancel reservation (each row has this).
  - ID: back-to-dashboard - Type: Button - Button to navigate back to dashboard.

### 7. My Reviews Page
- Page Title: My Reviews
- Overview: A page displaying all reviews written by the user.
- Elements:
  - ID: reviews-page - Type: Div - Container for the reviews page.
  - ID: reviews-list - Type: Div - List of reviews with book title, rating, review text.
  - ID: edit-review-button-{review_id} - Type: Button - Button to edit review (each review has this).
  - ID: delete-review-button-{review_id} - Type: Button - Button to delete review (each review has this).
  - ID: back-to-dashboard - Type: Button - Button to navigate back to dashboard.

### 8. Write Review Page
- Page Title: Write Review
- Overview: A page for users to write or edit a review for a book.
- Elements:
  - ID: write-review-page - Type: Div - Container for the write review page.
  - ID: book-info-display - Type: Div - Display information about the book being reviewed.
  - ID: rating-input - Type: Dropdown - Dropdown to select rating (1-5 stars).
  - ID: review-text - Type: Textarea - Field to write review text.
  - ID: submit-review-button - Type: Button - Button to submit review.
  - ID: back-to-book - Type: Button - Button to navigate back to book details.

### 9. User Profile Page
- Page Title: My Profile
- Overview: A page for users to view and edit their profile information.
- Elements:
  - ID: profile-page - Type: Div - Container for the profile page.
  - ID: profile-username - Type: Div - Display username (not editable).
  - ID: profile-email - Type: Input - Field to update email.
  - ID: update-profile-button - Type: Button - Button to save profile changes.
  - ID: borrow-history - Type: Div - Display list of all previously borrowed books.
  - ID: back-to-dashboard - Type: Button - Button to navigate back to dashboard.

### 10. Payment Confirmation Page
- Page Title: Payment Confirmation
- Overview: A page to confirm payment of overdue fines.
- Elements:
  - ID: payment-page - Type: Div - Container for the payment confirmation page.
  - ID: fine-amount-display - Type: Div - Display the fine amount to be paid.
  - ID: confirm-payment-button - Type: Button - Button to confirm payment.
  - ID: back-to-profile - Type: Button - Button to navigate back to profile.


## Section 2: Data Storage Design

Data files are located in the `data` directory.

### 1. User Data
- File Name: `users.txt`
- Format: username|email|phone|address
- Example:
  john_reader|john@example.com|555-1234|123 Main St
  jane_doe|jane@example.com|555-5678|789 Oak St

### 2. Books Data
- File Name: `books.txt`
- Format: book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating
- Example:
  1|To Kill a Mockingbird|Harper Lee|978-0-06-112008-4|Fiction|HarperCollins|1960|A gripping tale of racial injustice and childhood innocence.|Available|4.8
  2|Sapiens|Yuval Noah Harari|978-0-06-231609-7|Non-Fiction|Harper|2011|A brief history of humankind.|Borrowed|4.6
  3|1984|George Orwell|978-0-452-28423-4|Fiction|Signet Classic|1949|A dystopian social science fiction novel.|Available|4.7
  4|The Selfish Gene|Richard Dawkins|978-0-19-286092-7|Science|Oxford University Press|1976|Gene-centered view of evolution.|Reserved|4.5
  5|Steve Jobs|Walter Isaacson|978-1-4516-4853-9|Biography|Simon & Schuster|2011|Biography of Apple co-founder.|Available|4.3

### 3. Borrowings Data
- File Name: `borrowings.txt`
- Format: borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount
- Example:
  1|john_reader|2|2024-11-01|2024-11-15||Active|0
  2|jane_doe|1|2024-10-20|2024-11-03|2024-11-02|Returned|0
  3|john_reader|3|2024-10-15|2024-10-29||Overdue|5.00

### 4. Reservations Data
- File Name: `reservations.txt`
- Format: reservation_id|username|book_id|reservation_date|status
- Example:
  1|jane_doe|4|2024-11-10|Active
  2|john_reader|2|2024-10-25|Cancelled

### 5. Reviews Data
- File Name: `reviews.txt`
- Format: review_id|username|book_id|rating|review_text|review_date
- Example:
  1|jane_doe|1|5|An absolute masterpiece! A must-read.|2024-11-03
  2|john_reader|3|4|Thought-provoking and eerily relevant today.|2024-10-20

### 6. Fines Data
- File Name: `fines.txt`
- Format: fine_id|username|borrow_id|amount|status|date_issued
- Example:
  1|john_reader|3|5.00|Unpaid|2024-10-30


## Section 3: Navigation and Inter-page Relationships

- Dashboard Page:
  - "Browse Books" button navigates to Book Catalog Page.
  - "My Borrows" button navigates to My Borrowings Page.
  - "My Reservations", "My Reviews", "My Profile" can be accessed from dashboard menu or navigation bar (not explicitly defined but assumed for usability).

- Book Catalog Page:
  -"View Book" button (per book) navigates to Book Details Page for that book.
  - "Back to Dashboard" button returns to Dashboard Page.

- Book Details Page:
  - "Borrow" button navigates to Borrow Confirmation Page for the selected book.
  - "Write Review" button navigates to Write Review Page.
  - "Back to Catalog" button returns to Book Catalog Page.

- Borrow Confirmation Page:
  - "Confirm Borrow" button completes borrow process and navigates to My Borrowings Page.
  - "Cancel" button returns to Book Details Page.

- My Borrowings Page:
  - "Return Book" button (per active borrow) updates borrow status and returns user to My Borrowings Page.
  - "Back to Dashboard" button returns to Dashboard Page.

- My Reservations Page:
  - "Cancel Reservation" button (per reservation) cancels reservation and refreshes My Reservations Page.
  - "Back to Dashboard" button returns to Dashboard Page.

- My Reviews Page:
  - "Edit Review" button navigates to Write Review Page for editing.
  - "Delete Review" button deletes the review and refreshes My Reviews Page.
  - "Back to Dashboard" button returns to Dashboard Page.

- Write Review Page:
  - "Submit Review" button saves the review and returns to Book Details Page.
  - "Back to Book" button returns to Book Details Page.

- User Profile Page:
  - "Update Profile" button saves profile changes.
  - "Back to Dashboard" button returns to Dashboard Page.
  - "Borrow History" is a display only element showing past borrowings.

- Payment Confirmation Page:
  - "Confirm Payment" button processes payment and returns to User Profile Page.
  - "Back to Profile" button returns to User Profile Page.


# End of Design Specification
