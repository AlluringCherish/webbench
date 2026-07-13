# BookstoreOnline Web Application Design Candidate

This document outlines the complete design candidate for the BookstoreOnline web application, detailing all URL routes, page titles, UI element IDs, navigation buttons, and descriptions necessary for implementation.

---

## 1. Routes Definition

### Dashboard Page
- URL: `/`
- Methods: GET
- Route Function: `dashboard`

### Book Catalog Page
- URL: `/catalog`
- Methods: GET
- Route Function: `book_catalog`

### Book Details Page
- URL: `/book/<int:book_id>`
- Methods: GET
- Route Function: `book_details`

### Shopping Cart Page
- URL: `/cart`
- Methods: GET, POST
- Route Function: `shopping_cart`

### Checkout Page
- URL: `/checkout`
- Methods: GET, POST
- Route Function: `checkout`

### Order History Page
- URL: `/orders`
- Methods: GET
- Route Function: `order_history`

### Reviews Page
- URL: `/reviews`
- Methods: GET
- Route Function: `reviews_page`

### Write Review Page
- URL: `/write-review`
- Methods: GET, POST
- Route Function: `write_review`

### Bestsellers Page
- URL: `/bestsellers`
- Methods: GET
- Route Function: `bestsellers_page`

---

## 2. Page Titles, Container IDs & UI Elements

### (1) Dashboard Page
- **Page Title:** Bookstore Dashboard
- **Container ID:** `dashboard-page` (Div)
- **Elements:**
  - `featured-books` (Div): Displays featured book recommendations.
  - `browse-catalog-button` (Button): Navigates to Book Catalog page.
  - `view-cart-button` (Button): Navigates to Shopping Cart page.
  - `bestsellers-button` (Button): Navigates to Bestsellers page.

**Navigation:** Buttons use respective routes:
- browse-catalog-button -> `/catalog` (`book_catalog`)
- view-cart-button -> `/cart` (`shopping_cart`)
- bestsellers-button -> `/bestsellers` (`bestsellers_page`)

---

### (2) Book Catalog Page
- **Page Title:** Book Catalog
- **Container ID:** `catalog-page` (Div)
- **Elements:**
  - `search-input` (Input): Text input for searching by title, author, or ISBN.
  - `category-filter` (Dropdown): Filters books by category options (Fiction, Non-Fiction, Science, History, etc.).
  - `books-grid` (Div): Grid layout displaying multiple book cards.
  - `view-book-button-{book_id}` (Button): On each book card, navigates to corresponding Book Details page.

**Navigation:**
- view-book-button-{book_id} -> `/book/<book_id>` (`book_details`)

---

### (3) Book Details Page
- **Page Title:** Book Details
- **Container ID:** `book-details-page` (Div)
- **Elements:**
  - `book-title` (H1): Displays the book's title.
  - `book-author` (Div): Displays the author name.
  - `book-price` (Div): Displays price.
  - `add-to-cart-button` (Button): Adds current book to Shopping Cart.
  - `book-reviews` (Div): Shows customer reviews for the book.

**Navigation:**
- add-to-cart-button posts to update cart.

---

### (4) Shopping Cart Page
- **Page Title:** Shopping Cart
- **Container ID:** `cart-page` (Div)
- **Elements:**
  - `cart-items-table` (Table): Displays cart items with columns for title, quantity, price, subtotal.
  - `update-quantity-{item_id}` (Input, number): Quantity input for each item.
  - `remove-item-button-{item_id}` (Button): Removes an item from cart.
  - `proceed-checkout-button` (Button): Navigates to Checkout page.
  - `total-amount` (Div): Shows total cart amount.

**Navigation:**
- proceed-checkout-button -> `/checkout` (`checkout`)

---

### (5) Checkout Page
- **Page Title:** Checkout
- **Container ID:** `checkout-page` (Div)
- **Elements:**
  - `customer-name` (Input): Input field for customer name.
  - `shipping-address` (Textarea): Input field for shipping address.
  - `payment-method` (Dropdown): Select payment method (Credit Card, PayPal, Bank Transfer).
  - `place-order-button` (Button): Submits the order, completing purchase.

**Navigation:**
- place-order-button posts form to finalize order.

---

### (6) Order History Page
- **Page Title:** Order History
- **Container ID:** `orders-page` (Div)
- **Elements:**
  - `orders-table` (Table): Displays past orders with columns order ID, date, total amount, status.
  - `view-order-button-{order_id}` (Button): View detailed order info.
  - `order-status-filter` (Dropdown): Filters orders by status (All, Pending, Shipped, Delivered).
  - `back-to-dashboard` (Button): Returns to Dashboard.

**Navigation:**
- view-order-button-{order_id} -> Shows order detail view (not specified but can be implemented as modal or separate route)
- back-to-dashboard -> `/` (`dashboard`)

---

### (7) Reviews Page
- **Page Title:** Customer Reviews
- **Container ID:** `reviews-page` (Div)
- **Elements:**
  - `reviews-list` (Div): Lists all reviews showing book title, rating, and review text.
  - `write-review-button` (Button): Navigates to Write Review page.
  - `filter-by-rating` (Dropdown): Filters reviews by rating (All, 5 stars, 4 stars, etc.).
  - `back-to-dashboard` (Button): Returns to Dashboard.

**Navigation:**
- write-review-button -> `/write-review` (`write_review`)
- back-to-dashboard -> `/` (`dashboard`)

---

### (8) Write Review Page
- **Page Title:** Write a Review
- **Container ID:** `write-review-page` (Div)
- **Elements:**
  - `select-book` (Dropdown): Select which purchased book to review.
  - `rating-select` (Dropdown): Select rating from 1 to 5 stars.
  - `review-text` (Textarea): Text field for writing a review.
  - `submit-review-button` (Button): Submit the new review.

**Navigation:**
- submit-review-button posts form to add review and potentially redirect.

---

### (9) Bestsellers Page
- **Page Title:** Bestsellers
- **Container ID:** `bestsellers-page` (Div)
- **Elements:**
  - `bestsellers-list` (Div): Ranked list of bestselling books showing rank, title, author, sales count.
  - `time-period-filter` (Dropdown): Filter bestsellers by time period (This Week, This Month, All Time).
  - `view-book-button-{book_id}` (Button): View details of a bestseller book.
  - `back-to-dashboard` (Button): Returns to Dashboard.

**Navigation:**
- view-book-button-{book_id} -> `/book/<book_id>` (`book_details`)
- back-to-dashboard -> `/` (`dashboard`)

---

## 3. Summary of Navigation Buttons and Targets

| Button ID                     | Source Page          | Target Route          | Route Function    |
|-------------------------------|---------------------|-----------------------|-------------------|
| `browse-catalog-button`        | Dashboard            | `/catalog`            | `book_catalog`    |
| `view-cart-button`             | Dashboard            | `/cart`               | `shopping_cart`   |
| `bestsellers-button`            | Dashboard            | `/bestsellers`        | `bestsellers_page`|
| `view-book-button-{book_id}`   | Catalog, Bestsellers  | `/book/<book_id>`     | `book_details`    |
| `add-to-cart-button`            | Book Details         | POST add to cart (same page) | `book_details` (POST handler)|
| `proceed-checkout-button`       | Shopping Cart        | `/checkout`           | `checkout`        |
| `place-order-button`            | Checkout             | POST place order (same route) | `checkout` (POST handler)|
| `view-order-button-{order_id}` | Order History        | Detailed Order (implementation optional) | N/A |
| `back-to-dashboard`             | Orders, Reviews, Bestsellers | `/`                 | `dashboard`       |
| `write-review-button`           | Reviews              | `/write-review`       | `write_review`    |
| `submit-review-button`          | Write Review         | POST new review (same route)| `write_review` (POST handler)|

---

This design candidate meets all user requirements for UI element IDs, route naming, navigation, and page titles exactly as specified, serving as a comprehensive blueprint for coding the BookstoreOnline Flask web application.