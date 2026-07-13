# Frontend Design Specification for BookstoreOnline

---

## Section 1: HTML Template Specifications

---

### 1. Dashboard Page
- Template File Name: dashboard.html
- Page Title: Bookstore Dashboard
- Elements:
  - `dashboard-page` (div): Container for the entire dashboard page.
  - `featured-books` (div): Displays featured book recommendations, dynamically populated.
  - `browse-catalog-button` (button): Navigates to Book Catalog page.
  - `view-cart-button` (button): Navigates to Shopping Cart page.
  - `bestsellers-button` (button): Navigates to Bestsellers page.

- Dynamic Content:
  - Featured books list displayed inside `featured-books`. Each featured book may show title, author, cover image, and price.

- Navigation Flows:
  - Click `browse-catalog-button` → Book Catalog page.
  - Click `view-cart-button` → Shopping Cart page.
  - Click `bestsellers-button` → Bestsellers page.

---

### 2. Book Catalog Page
- Template File Name: catalog.html
- Page Title: Book Catalog
- Elements:
  - `catalog-page` (div): Container for the entire catalog page.
  - `search-input` (input[type=text]): Text box to search books by title, author, or ISBN.
  - `category-filter` (select dropdown): Filters books by category (e.g. Fiction, Non-Fiction).
  - `books-grid` (div): Grid container displaying book cards.
  - `view-book-button-{book_id}` (button per book): Button on each book card to view book details.

- Dynamic Content:
  - `books-grid` contains multiple book cards rendered dynamically for all filtered/searched books.
  - Each book card displays cover image, title, author, and price.
  - Each book card includes a `view-book-button-{book_id}` button unique to that book.

- Navigation Flows:
  - Click `view-book-button-{book_id}` → Book Details page for given `book_id`.

---

### 3. Book Details Page
- Template File Name: book_details.html
- Page Title: Book Details
- Elements:
  - `book-details-page` (div): Container for book detail page.
  - `book-title` (h1): Displays title of the selected book.
  - `book-author` (div): Displays author of the book.
  - `book-price` (div): Displays price.
  - `add-to-cart-button` (button): Adds current book to shopping cart.
  - `book-reviews` (div): Section listing customer reviews for this book.

- Dynamic Content:
  - `book-title`, `book-author`, `book-price` populated from selected book data.
  - `book-reviews` populated with list of reviews from `reviews.txt` filtered by `book_id`.

- Navigation Flows:
  - Click `add-to-cart-button` → Adds book to cart, optionally navigates to Shopping Cart or stays.

---

### 4. Shopping Cart Page
- Template File Name: cart.html
- Page Title: Shopping Cart
- Elements:
  - `cart-page` (div): Container for cart page.
  - `cart-items-table` (table): Displays all cart items with columns: Title, Quantity, Price, Subtotal.
  - `update-quantity-{item_id}` (input[type=number] per cart item): To update quantity.
  - `remove-item-button-{item_id}` (button per cart item): Removes the item from cart.
  - `proceed-checkout-button` (button): Navigates to Checkout page.
  - `total-amount` (div): Shows total cart value.

- Dynamic Content:
  - Rows in `cart-items-table` generated dynamically based on cart contents.
  - Each row corresponds to an item with item_id linking to cart entry.

- Navigation Flows:
  - Modify quantity in `update-quantity-{item_id}` triggers cart update action.
  - Click `remove-item-button-{item_id}` → Removes that item from cart.
  - Click `proceed-checkout-button` → Checkout page.

---

### 5. Checkout Page
- Template File Name: checkout.html
- Page Title: Checkout
- Elements:
  - `checkout-page` (div): Container for checkout.
  - `customer-name` (input[type=text]): Input for customer full name.
  - `shipping-address` (textarea): Input for shipping address.
  - `payment-method` (select dropdown): Payment selection (Credit Card, PayPal, Bank Transfer).
  - `place-order-button` (button): Submits order for processing.

- Navigation Flows:
  - Click `place-order-button` → Places order, navigates to Order History or Confirmation.

---

### 6. Order History Page
- Template File Name: orders.html
- Page Title: Order History
- Elements:
  - `orders-page` (div): Container for orders page.
  - `orders-table` (table): Lists orders with columns: Order ID, Date, Total Amount, Status.
  - `view-order-button-{order_id}` (button per order): Button to view detailed order info.
  - `order-status-filter` (select dropdown): Filter orders by status (All, Pending, Shipped, Delivered).
  - `back-to-dashboard` (button): Returns to Dashboard page.

- Dynamic Content:
  - `orders-table` dynamically lists all orders filtered by status.

- Navigation Flows:
  - Click `view-order-button-{order_id}` → Show order detail (could be modal or new page).
  - Click `back-to-dashboard` → Dashboard page.

---

### 7. Reviews Page
- Template File Name: reviews.html
- Page Title: Customer Reviews
- Elements:
  - `reviews-page` (div): Container for reviews page.
  - `reviews-list` (div): Shows list of reviews including book title, rating, and text.
  - `write-review-button` (button): Navigates to Write Review page.
  - `filter-by-rating` (select dropdown): Filters reviews by rating (All, 5 stars, 4 stars, etc.).
  - `back-to-dashboard` (button): Navigates back to Dashboard.

- Dynamic Content:
  - `reviews-list` dynamically populated with reviews.

- Navigation Flows:
  - Click `write-review-button` → Write Review page.
  - Click `back-to-dashboard` → Dashboard page.

---

### 8. Write Review Page
- Template File Name: write_review.html
- Page Title: Write a Review
- Elements:
  - `write-review-page` (div): Container for write review page.
  - `select-book` (select dropdown): Dropdown to select purchased book to review.
  - `rating-select` (select dropdown): Select rating (1-5 stars).
  - `review-text` (textarea): Text input for review content.
  - `submit-review-button` (button): Submit the review.

- Navigation Flows:
  - Click `submit-review-button` → Submit review, then navigate back to Reviews page.

---

### 9. Bestsellers Page
- Template File Name: bestsellers.html
- Page Title: Bestsellers
- Elements:
  - `bestsellers-page` (div): Container for bestsellers page.
  - `bestsellers-list` (div): Ranked list of bestsellers showing rank, title, author, sales count.
  - `time-period-filter` (select dropdown): Filter bestsellers by time period (This Week, This Month, All Time).
  - `view-book-button-{book_id}` (button per bestseller): View book details button for each bestseller.
  - `back-to-dashboard` (button): Navigates back to Dashboard.

- Dynamic Content:
  - `bestsellers-list` dynamically populated from sales data filtered by `time-period-filter`.

- Navigation Flows:
  - Click `view-book-button-{book_id}` → Book Details page.
  - Click `back-to-dashboard` → Dashboard page.

---

# Summary Navigation Flow Diagram
- Dashboard (default start)
   - → Book Catalog (browse-catalog-button)
   - → Shopping Cart (view-cart-button)
   - → Bestsellers (bestsellers-button)

- Book Catalog
   - → Book Details (view-book-button-{book_id})

- Book Details
   - → Add to Cart (add-to-cart-button)

- Shopping Cart
   - → Checkout (proceed-checkout-button)

- Checkout
   - → Order History (after place order)

- Order History
   - → Order Details (view-order-button-{order_id})
   - → Dashboard (back-to-dashboard)

- Reviews
   - → Write Review (write-review-button)
   - → Dashboard (back-to-dashboard)

- Write Review
   - → Reviews (submit-review-button)

- Bestsellers
   - → Book Details (view-book-button-{book_id})
   - → Dashboard (back-to-dashboard)

---

# Notes on Data-Driven Content
- Books Grid and Bestseller Lists will be populated by iterating over context variables (e.g., `books`, `bestsellers`).
- Review lists will be populated by iterating over `reviews` filtered by book or rating.
- Cart items are populated using `cart_items` with each item having quantity and price data.
- Variables like `book_id`, `item_id`, `order_id` are used for dynamic element IDs for buttons to differentiate each actionable item.

This document fully specifies templates, element IDs, page titles, and navigation to enable frontend implementation.