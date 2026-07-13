# BookstoreOnline Web Application Design Specification

---

## 1. Routes Definition

| URL Route                  | HTTP Methods | Flask Route Function       | Description                               |
|----------------------------|--------------|----------------------------|-------------------------------------------|
| `/`                        | GET          | `dashboard`                | Show Dashboard page (alias to `/dashboard`)
| `/dashboard`               | GET          | `dashboard`                | Show Dashboard page                        |
| `/catalog`                 | GET          | `book_catalog`             | Show Book Catalog page with filters/search|
| `/book/<int:book_id>`      | GET          | `book_details`             | Show Book Details for specific book       |
| `/cart`                    | GET, POST    | `shopping_cart`            | Display and update shopping cart          |
| `/cart/remove/<int:item_id>`| POST        | `remove_cart_item`         | Remove item from shopping cart            |
| `/checkout`                | GET, POST    | `checkout`                 | Show and process checkout                  |
| `/orders`                  | GET          | `order_history`            | Show all past orders with filters          |
| `/order/<int:order_id>`    | GET          | `order_details`            | Show details of a specific order           |
| `/reviews`                 | GET          | `reviews_page`             | Display reviews list, filter by rating     |
| `/write-review`            | GET, POST    | `write_review`             | Write and submit a review                   |
| `/reviews/write`           | GET, POST    | `write_review`             | (Alias for `/write-review`) Write review form
| `/bestsellers`             | GET          | `bestsellers_page`         | Show list of top selling books             |

---

## 2. Page Titles, Container IDs & UI Elements

### (1) Dashboard Page
- URL Routes: `/` and `/dashboard` (GET)
- **Page Title:** Bookstore Dashboard
- **Container ID:** `dashboard-page` (Div)
- **Elements:**
  - `featured-books` (Div): Displays featured book recommendations horizontally with image, title, and author. Clicking book title or image navigates to Book Details page.
  - `browse-catalog-button` (Button): Navigates to Book Catalog page.
  - `view-cart-button` (Button): Navigates to Shopping Cart page.
  - `bestsellers-button` (Button): Navigates to Bestsellers page.

**Navigation:**
- `browse-catalog-button` -> `/catalog` (`book_catalog`)
- `view-cart-button` -> `/cart` (`shopping_cart`)
- `bestsellers-button` -> `/bestsellers` (`bestsellers_page`)

---

### (2) Book Catalog Page
- URL Route: `/catalog` (GET)
- **Page Title:** Book Catalog
- **Container ID:** `catalog-page` (Div)
- **Elements:**
  - `search-input` (Input, text): Input for searching by title, author, or ISBN.
  - `category-filter` (Dropdown): Filter by category options (Fiction, Non-Fiction, Science, History, etc.).
  - `books-grid` (Div): Grid layout showing multiple book cards.
  - `view-book-button-{book_id}` (Button): On each book card, navigates to Book Details page.

**Navigation:**
- `view-book-button-{book_id}` -> `/book/<book_id>` (`book_details`)

---

### (3) Book Details Page
- URL Route: `/book/<int:book_id>` (GET)
- **Page Title:** Book Details
- **Container ID:** `book-details-page` (Div)
- **Elements:**
  - `book-title` (H1): Displays book title.
  - `book-author` (Div): Displays author name.
  - `book-price` (Div): Displays price.
  - `add-to-cart-button` (Button): Adds current book to Shopping Cart on POST.
  - `book-reviews` (Div): Shows customer reviews for the book with ratings and text.

**Navigation:**
- `add-to-cart-button` submits POST to update cart (handled by `book_details` POST).

---

### (4) Shopping Cart Page
- URL Route: `/cart` (GET, POST)
- **Page Title:** Shopping Cart
- **Container ID:** `cart-page` (Div)
- **Elements:**
  - `cart-items-table` (Table): Displays cart items with columns title, quantity, price, subtotal.
  - `update-quantity-{item_id}` (Input, number): Quantity input for each cart item.
  - `remove-item-button-{item_id}` (Button): Removes an item from cart.
  - `proceed-checkout-button` (Button): Navigates to Checkout page.
  - `total-amount` (Div): Shows total cart amount.

**Navigation:**
- `proceed-checkout-button` -> `/checkout` (`checkout`)
- `remove-item-button-{item_id}` posts to `/cart/remove/<item_id>` (`remove_cart_item`)

---

### (5) Checkout Page
- URL Route: `/checkout` (GET, POST)
- **Page Title:** Checkout
- **Container ID:** `checkout-page` (Div)
- **Elements:**
  - `customer-name` (Input): Field for customer name.
  - `shipping-address` (Textarea): Field for shipping address.
  - `payment-method` (Dropdown): Select payment method: Credit Card, PayPal, Bank Transfer.
  - `place-order-button` (Button): Submits order on POST.

**Navigation:**
- `place-order-button` submits POST to finalize order.

---

### (6) Order History Page
- URL Route: `/orders` (GET)
- **Page Title:** Order History
- **Container ID:** `orders-page` (Div)
- **Elements:**
  - `orders-table` (Table): Displays past orders with columns order ID, date, total amount, status.
  - `view-order-button-{order_id}` (Button): View detailed order info.
  - `order-status-filter` (Dropdown): Filter orders by status (All, Pending, Shipped, Delivered).
  - `back-to-dashboard` (Button): Returns to Dashboard.

**Navigation:**
- `view-order-button-{order_id}` -> `/order/<order_id>` (`order_details`)
- `back-to-dashboard` -> `/` or `/dashboard` (`dashboard`)

---

### (7) Order Details Page
- URL Route: `/order/<int:order_id>` (GET)
- **Page Title:** Order Details
- **Container ID:** `order-details-page` (Div)
- **Elements:**
  - Displays order information: order ID, date, total amount, status, shipping address, list of order items with titles, quantities, and prices.
  - `back-to-orders-button` (Button): Returns to Order History page.

**Navigation:**
- `back-to-orders-button` -> `/orders` (`order_history`)

---

### (8) Reviews Page
- URL Route: `/reviews` (GET)
- **Page Title:** Customer Reviews
- **Container ID:** `reviews-page` (Div)
- **Elements:**
  - `reviews-list` (Div): Lists all reviews showing book title, rating stars, and review text.
  - `write-review-button` (Button): Navigates to Write Review page.
  - `filter-by-rating` (Dropdown): Filters reviews by rating (All, 5 stars, 4 stars, etc.).
  - `back-to-dashboard` (Button): Returns to Dashboard.

**Navigation:**
- `write-review-button` -> `/write-review` or `/reviews/write` (`write_review`)
- `back-to-dashboard` -> `/` or `/dashboard` (`dashboard`)

---

### (9) Write Review Page
- URL Route: `/write-review` and `/reviews/write` (GET, POST)
- **Page Title:** Write a Review
- **Container ID:** `write-review-page` (Div)
- **Elements:**
  - `select-book` (Dropdown): Select purchased book to review.
  - `rating-select` (Dropdown): Select rating (1-5 stars).
  - `review-text` (Textarea): Text field for writing review.
  - `submit-review-button` (Button): Submits the review.

**Navigation:**
- `submit-review-button` posts form to add review and redirects accordingly.

---

### (10) Bestsellers Page
- URL Route: `/bestsellers` (GET)
- **Page Title:** Bestsellers
- **Container ID:** `bestsellers-page` (Div)
- **Elements:**
  - `bestsellers-list` (Div): Ranked list of bestselling books showing rank, title, author, sales count.
  - `time-period-filter` (Dropdown): Filter bestsellers by time period (This Week, This Month, All Time).
  - `view-book-button-{book_id}` (Button): View details of bestseller book.
  - `back-to-dashboard` (Button): Returns to Dashboard.

**Navigation:**
- `view-book-button-{book_id}` -> `/book/<book_id>` (`book_details`)
- `back-to-dashboard` -> `/` or `/dashboard` (`dashboard`)

---

## 3. Summary of Navigation Buttons and Route Mappings

| Button ID                          | Source Page        | Target URL Route         | Route Function     |
|-----------------------------------|--------------------|--------------------------|--------------------|
| browse-catalog-button              | Dashboard          | `/catalog`               | `book_catalog`     |
| view-cart-button                  | Dashboard          | `/cart`                  | `shopping_cart`    |
| bestsellers-button                | Dashboard          | `/bestsellers`           | `bestsellers_page` |
| view-book-button-{book_id}       | Catalog, Bestsellers | `/book/<book_id>`       | `book_details`     |
| add-to-cart-button                | Book Details       | POST to `/book/<book_id>`| `book_details` (POST handler) |
| proceed-checkout-button           | Shopping Cart      | `/checkout`              | `checkout`         |
| place-order-button                | Checkout           | POST `checkout`          | `checkout` (POST handler) |
| view-order-button-{order_id}     | Order History      | `/order/<order_id>`      | `order_details`    |
| back-to-dashboard                 | Orders, Reviews, Bestsellers, Order Details | `/` or `/dashboard`     | `dashboard`        |
| back-to-orders-button             | Order Details      | `/orders`                | `order_history`    |
| write-review-button              | Reviews            | `/write-review` or `/reviews/write` | `write_review`    |
| submit-review-button             | Write Review       | POST form to `/write-review` or `/reviews/write` | `write_review` (POST) |
| remove-item-button-{item_id}     | Shopping Cart      | POST to `/cart/remove/<item_id>` | `remove_cart_item` |

---

## 4. Data Files Integration

All data is stored and managed through local text files in `data` directory:

- `books.txt`: Contains book info with fields book_id, title, author, isbn, category, price, stock, description
- `categories.txt`: Book categories
- `cart.txt`: Current cart items
- `orders.txt`: Order history
- `order_items.txt`: Items within each order
- `reviews.txt`: Customer reviews
- `bestsellers.txt`: Sales data for bestseller rankings

These data files should be read and updated as appropriate by respective route handlers.

---

This comprehensive design_spec.md merges and harmonizes design candidates A and B, consolidating route functions, page URLs, element IDs, and consistent UI navigation. It fully aligns with user requirements and serves as an implementation-ready blueprint for the BookstoreOnline Flask web application.
