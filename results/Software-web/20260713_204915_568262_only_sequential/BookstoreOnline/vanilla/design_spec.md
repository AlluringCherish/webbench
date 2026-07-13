# Design Specification for BookstoreOnline Flask Web Application

## 1. Flask Routes

### Dashboard Page
- URL Path: `/` or `/dashboard`
- HTTP Methods: GET
- Function Name: `dashboard`
- Context Variables:
  - `featured_books` (list of featured books from books.txt or logic)
  - `bestsellers` (list from bestsellers.txt)

### Book Catalog Page
- URL Path: `/catalog`
- HTTP Methods: GET
- Function Name: `book_catalog`
- Context Variables:
  - `books` (list of all books from books.txt)
  - `categories` (list from categories.txt)
  - `selected_category` (optional category filter from request args)
  - `search_query` (optional search input from request args)

### Book Details Page
- URL Path: `/book/<int:book_id>`
- HTTP Methods: GET, POST
- Function Name: `book_details`
- Context Variables (GET):
  - `book` (book details from books.txt by book_id)
  - `reviews` (list of reviews from reviews.txt filtered by book_id)
- POST used for add-to-cart button action

### Shopping Cart Page
- URL Path: `/cart`
- HTTP Methods: GET, POST
- Function Name: `shopping_cart`
- Context Variables:
  - `cart_items` (list of items from cart.txt joined with books.txt details)
  - `total_amount` (calculated total of all items)
- POST used for updates/removal of items

### Checkout Page
- URL Path: `/checkout`
- HTTP Methods: GET, POST
- Function Name: `checkout`
- Context Variables (GET):
  - none
- POST used to place order and write to orders.txt and order_items.txt

### Order History Page
- URL Path: `/orders`
- HTTP Methods: GET
- Function Name: `order_history`
- Context Variables:
  - `orders` (list from orders.txt)
  - `filter_status` (status filter from request args)

### Reviews Page
- URL Path: `/reviews`
- HTTP Methods: GET
- Function Name: `reviews`
- Context Variables:
  - `reviews` (list from reviews.txt with joins to book titles)
  - `filter_rating` (rating filter from request args)

### Write Review Page
- URL Path: `/write_review`
- HTTP Methods: GET, POST
- Function Name: `write_review`
- Context Variables (GET):
  - `purchased_books` (list of books to select from)

### Bestsellers Page
- URL Path: `/bestsellers`
- HTTP Methods: GET
- Function Name: `bestsellers`
- Context Variables:
  - `bestsellers` (list from bestsellers.txt)
  - `time_period` (filter from request args)


## 2. Page Titles and Element IDs

### Dashboard Page
- Title: "Bookstore Dashboard"
- Element IDs:
  - dashboard-page
  - featured-books
  - browse-catalog-button
  - view-cart-button
  - bestsellers-button

### Book Catalog Page
- Title: "Book Catalog"
- Element IDs:
  - catalog-page
  - search-input
  - category-filter
  - books-grid
  - view-book-button-{book_id} (dynamic per book_id)

### Book Details Page
- Title: "Book Details"
- Element IDs:
  - book-details-page
  - book-title
  - book-author
  - book-price
  - add-to-cart-button
  - book-reviews

### Shopping Cart Page
- Title: "Shopping Cart"
- Element IDs:
  - cart-page
  - cart-items-table
  - update-quantity-{item_id} (dynamic per cart item)
  - remove-item-button-{item_id} (dynamic per cart item)
  - proceed-checkout-button
  - total-amount

### Checkout Page
- Title: "Checkout"
- Element IDs:
  - checkout-page
  - customer-name
  - shipping-address
  - payment-method
  - place-order-button

### Order History Page
- Title: "Order History"
- Element IDs:
  - orders-page
  - orders-table
  - view-order-button-{order_id} (dynamic per order)
  - order-status-filter
  - back-to-dashboard

### Reviews Page
- Title: "Customer Reviews"
- Element IDs:
  - reviews-page
  - reviews-list
  - write-review-button
  - filter-by-rating
  - back-to-dashboard

### Write Review Page
- Title: "Write a Review"
- Element IDs:
  - write-review-page
  - select-book
  - rating-select
  - review-text
  - submit-review-button

### Bestsellers Page
- Title: "Bestsellers"
- Element IDs:
  - bestsellers-page
  - bestsellers-list
  - time-period-filter
  - view-book-button-{book_id} (dynamic per bestseller book)
  - back-to-dashboard


## 3. Navigation Mappings (Buttons → Route Functions)

### Dashboard Page
- browse-catalog-button → `url_for('book_catalog')`
- view-cart-button → `url_for('shopping_cart')`
- bestsellers-button → `url_for('bestsellers')`

### Book Catalog Page
- view-book-button-{book_id} → `url_for('book_details', book_id=book_id)`

### Book Details Page
- add-to-cart-button → POST handled by `book_details` route to add item to cart. Post-submission navigation can be to cart or back to catalog.

### Shopping Cart Page
- remove-item-button-{item_id} → POST form to `shopping_cart` route to remove item
- update-quantity-{item_id} → POST form to `shopping_cart` route to update quantity
- proceed-checkout-button → `url_for('checkout')`

### Checkout Page
- place-order-button → POST handled by `checkout` route to place order

### Order History Page
- view-order-button-{order_id} → Could be a modal or detailed view, no route defined explicitly
- back-to-dashboard → `url_for('dashboard')`

### Reviews Page
- write-review-button → `url_for('write_review')`
- back-to-dashboard → `url_for('dashboard')`

### Write Review Page
- submit-review-button → POST form to `write_review` route

### Bestsellers Page
- view-book-button-{book_id} → `url_for('book_details', book_id=book_id)`
- back-to-dashboard → `url_for('dashboard')`


## 4. Data Storage Contracts

### 1. Books Data
- Filename: `data/books.txt`
- Format (pipe-delimited fields):
  - book_id
  - title
  - author
  - isbn
  - category
  - price
  - stock
  - description
- Usage: Store all books details. Used in catalog, details, reviews, bestsellers, and cart.

### 2. Categories Data
- Filename: `data/categories.txt`
- Format:
  - category_id
  - category_name
  - description
- Usage: Used for category filters in catalog page.

### 3. Cart Data
- Filename: `data/cart.txt`
- Format:
  - cart_id
  - book_id
  - quantity
  - added_date (YYYY-MM-DD)
- Usage: Stores current shopping cart items. Managed on cart and book details pages.

### 4. Orders Data
- Filename: `data/orders.txt`
- Format:
  - order_id
  - customer_name
  - order_date (YYYY-MM-DD)
  - total_amount
  - status (Pending, Shipped, Delivered)
  - shipping_address
- Usage: Stores completed orders, displayed in order history.

### 5. Order Items Data
- Filename: `data/order_items.txt`
- Format:
  - order_item_id
  - order_id
  - book_id
  - quantity
  - price (unit price at purchase)
- Usage: Stores details of each item in an order.

### 6. Reviews Data
- Filename: `data/reviews.txt`
- Format:
  - review_id
  - book_id
  - customer_name
  - rating (1-5)
  - review_text
  - review_date (YYYY-MM-DD)
- Usage: Stores all customer reviews, displayed on reviews page and book details.

### 7. Bestsellers Data
- Filename: `data/bestsellers.txt`
- Format:
  - book_id
  - sales_count
  - period (e.g. "This Week", "This Month", "All Time")
- Usage: Stores ranked sales data for bestsellers page filtering.


---

This design specification fully covers all routes, page elements, navigation maps, and data contracts for the 'BookstoreOnline' web application backend and frontend implementation with Flask framework.
