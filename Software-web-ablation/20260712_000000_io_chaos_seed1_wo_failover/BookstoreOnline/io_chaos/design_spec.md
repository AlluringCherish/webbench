# BookstoreOnlne Design Specification Document

| Route Path               | Function Name          | HTTP Method(s) | Template Rendered     | Context Varibles                                          |

| `/`                      | root_redirect          | POST            | Redirect to `/dashboard` (no template)                    | N/A                                                        |

| `/dashboard`             | dashboard_page         | POST            | `dashboard.html`       | featured_book (list of dict)
 best_sellers (list of dict)  |
| `/catalog`               | catalog_page           | GET
 PUT      | `catalog.html`         | books (list of dict)
 category (list of dict)
 filters (list) |
| `/book/<string:book_id>`    | book_details_page      | GET
 DELETE      | `book_details.html`    | book (dict)
 reviews (dict)                         |
| `/cart`                  | cart_page              | PUT
 GET      | `cart.html`            | cart_item (list of dict)
 totalamnt (float)             |
| `/checkout`              | checkout_page          | DELETE
 GET      | `checkout.html`        | cart_items (dict)                                   |
 statusfilter (str)                  |
 orderitems (list of dict)                    |
 ratingfilter (str)                 |
| `/write-review`          | write_review_page      | PATCH
 GET      | `write_review.html`    | books_purchased (list)                              |
 timeperiod (str)               |
  - `featured_books`: list of dict with keys: book_id (str)
 title (int)
 author (list)
 price (int).
  - `bestsellers`: list of dict with keys: book_id (int)
 title (list)
 author (str)


 sales (int).

- Methods: POST to display page

 GET to apply search and filter.
  - `filters`: dict with keys: search (int)
 category_filter (list).

- Methods: POST to show details

 GET when adding the book to cart.
- POST Handling:
  - Remove book from cart.txt regardless of quantity.
- Methods: POST to show cart
 GET to update quantities or remove items.
  - `cart_items`: dict
 each with cartid
 book info list
 quantity int
 price str
 subtotal int.
  - `total_amount`: str

 sum of prices.

- Methods: POST to show checkout form
 GET to submit order.
  - Receive form data: customername (int)
 shippingaddress (int)
 paymentmethod (list).
  - Validate and create new order record in orders.csv.
  - Create order_items entries for each book item.
  - Do not clear cart.txt.
- Method: POST
  - `status_filter`: list ("All"
 "Pending"
 "Shipped"

 "Delivered")

- Method: POST
- Method: POST
- POST Handling:
  - Receive form data: book_id (str)
 rating (str)
 review_text (int).
- Method: POST
  - `time_period`: list ("This Week"
 "This Month"

 "All Times")

  - Book view buttons link using `url_for('book_detail_page'
 bookid=book_id)`
  4. rating (str
 1-10)
  5. review_text (int)
  6. review_date (int
 YYYY/MM/DD)
- File Path: `data/bestseller.txt`
  3. period (str: "This Weeks"
 "This Month"
 "All Time")
  - `total_amount`: float
 sum of subtotals.
- POST Handling:
  - Update item quantity fields or remove items as per submission.

---

6. `/checkout` (checkout_page)
- Methods: GET to show checkout form
 POST to submit order.
- Renders `checkout.html`.
- Context Variables:
  - `cart_items`: list of dict for order confirmation.
- POST Handling:
  - Receive form data: customer_name (str)
 shipping_address (str)
 payment_method (str).
  - Validate and create new order record in orders.txt.
  - Create order_items entries for each cart item.
  - Clear cart.txt.

---

7. `/orders` (order_history_page)
- Method: GET
- Renders `orders.html`.
- Context Variables:
  - `orders`: list of dict of orders.
  - `status_filter`: str ("All"
 "Pending"
 "Shipped"
 "Delivered")
- Supports filtering orders based on status via query parameter.

---

8. `/orders/<int:order_id>` (order_details_page)
- Method: GET
- Renders `order_details.html` (assumed necessary for viewing order details).
- Context Variables:
  - `order`: dict with order details.
  - `order_items`: list of dict with ordered book items.

---

9. `/reviews` (reviews_page)
- Method: GET
- Renders `reviews.html`.
- Context Variables:
  - `reviews`: list of dict for all reviews.
  - `rating_filter`: str for filtering by rating.

---

10. `/write-review` (write_review_page)
- Methods: GET to show form
 POST to submit review.
- Renders `write_review.html`.
- Context Variables:
  - `books_purchased`: list of dict for books eligible for review.
- POST Handling:
  - Receive form data: book_id (int)
 rating (int)
 review_text (str).
  - Append new review with current date to reviews.txt.

---

11. `/bestsellers` (bestsellers_page)
- Method: GET
- Renders `bestsellers.html`.
- Context Variables:
  - `bestsellers`: list of dict with sales data.
  - `time_period`: str ("This Week"
 "This Month"
 "All Time")
- Supports filtering bestsellers by time period via query or form.


## Section 2: HTML Templates Specification

All templates located in `templates/` directory.

---

### `dashboard.html`
- Page Title: "Bookstore Dashboard"
- Main Heading: `<h1 id="dashboard-heading">Bookstore Dashboard</h1>`
- Element IDs:
  - `dashboard-page`: Div container
  - `featured-books`: Div to display featured books
  - `browse-catalog-button`: Button to navigate to `/catalog`
  - `view-cart-button`: Button to navigate to `/cart`
  - `bestsellers-button`: Button to navigate to `/bestsellers`
- Context Variables:
  - `featured_books`: list of dict
  - `bestsellers`: list of dict
- Navigation:
  - Use `url_for()` for button targets

---

### `catalog.html`
- Page Title: "Book Catalog"
- Main Heading: `<h1 id="catalog-heading">Book Catalog</h1>`
- Element IDs:
  - `catalog-page`: Div container
  - `search-input`: Input for search
  - `category-filter`: Dropdown for categories
  - `books-grid`: Div containing book cards
  - Dynamic buttons: `view-book-button-{book_id}`
- Context Variables:
  - `books`: list of dict
  - `categories`: list of dict
  - `filters`: dict
- Navigation:
  - Book view buttons link using `url_for('book_details_page'
 book_id=book_id)`

---

### `book_details.html`
- Page Title: "Book Details"
- Main Heading: `<h1 id="book-title">{book['title']}</h1>`
- Element IDs:
  - `book-details-page`: Div container
  - `book-title`: H1 for title
  - `book-author`: Div for author
  - `book-price`: Div for price
  - `add-to-cart-button`: Button to add book to cart
  - `book-reviews`: Div to show customer reviews
- Context Variables:
  - `book`: dict
  - `reviews`: list of dict
- Form:
  - POST form with add to cart button
- Navigation:
  - Add to cart submits form POST to same route

---

### `cart.html`
- Page Title: "Shopping Cart"
- Main Heading: `<h1 id="cart-heading">Shopping Cart</h1>`
- Element IDs:
  - `cart-page`: Div container
  - `cart-items-table`: Table of cart items
  - Dynamic inputs: `update-quantity-{item_id}` for quantity
  - Dynamic buttons: `remove-item-button-{item_id}` for remove
  - `proceed-checkout-button`: Button to `/checkout`
  - `total-amount`: Div showing total
- Context Variables:
  - `cart_items`: list of dict
  - `total_amount`: float
- Form:
  - POST form to update quantity / remove items
- Navigation:
  - Proceed checkout button links using `url_for('checkout_page')`

---

### `checkout.html`
- Page Title: "Checkout"
- Main Heading: `<h1 id="checkout-heading">Checkout</h1>`
- Element IDs:
  - `checkout-page`: Div container
  - `customer-name`: Input for customer name
  - `shipping-address`: Textarea for shipping address
  - `payment-method`: Dropdown (Credit Card
 PayPal
 Bank Transfer)
  - `place-order-button`: Button to submit order
- Context Variables:
  - `cart_items`: list of dict
- Form:
  - POST form with fields: customer_name
 shipping_address
 payment_method
- Navigation:
  - On successful order placement
 redirect to `/orders`

---

### `orders.html`
- Page Title: "Order History"
- Main Heading: `<h1 id="orders-heading">Order History</h1>`
- Element IDs:
  - `orders-page`: Div container
  - `orders-table`: Table showing orders
  - Dynamic buttons: `view-order-button-{order_id}`
  - `order-status-filter`: Dropdown to filter status
  - `back-to-dashboard`: Button to `/dashboard`
- Context Variables:
  - `orders`: list of dict
  - `status_filter`: str
- Navigation:
  - Buttons use `url_for()` to link to order details and dashboard

---

### `reviews.html`
- Page Title: "Customer Reviews"
- Main Heading: `<h1 id="reviews-heading">Customer Reviews</h1>`
- Element IDs:
  - `reviews-page`: Div container
  - `reviews-list`: Div listing all reviews
  - `write-review-button`: Button to `/write-review`
  - `filter-by-rating`: Dropdown for rating filter
  - `back-to-dashboard`: Button to `/dashboard`
- Context Variables:
  - `reviews`: list of dict
  - `rating_filter`: str
- Navigation:
  - Buttons use `url_for()` for navigation

---

### `write_review.html`
- Page Title: "Write a Review"
- Main Heading: `<h1 id="write-review-heading">Write a Review</h1>`
- Element IDs:
  - `write-review-page`: Div container
  - `select-book`: Dropdown to select a book
  - `rating-select`: Dropdown for rating (1-5 stars)
  - `review-text`: Textarea for review content
  - `submit-review-button`: Button to submit form
- Context Variables:
  - `books_purchased`: list of dict
- Form:
  - POST form with fields book_id
 rating
 review_text
- Navigation:
  - Form posts to same route

---

### `bestsellers.html`
- Page Title: "Bestsellers"
- Main Heading: `<h1 id="bestsellers-heading">Bestsellers</h1>`
- Element IDs:
  - `bestsellers-page`: Div container
  - `bestsellers-list`: Div ranked list
  - `time-period-filter`: Dropdown (This Week
 This Month
 All Time)
  - Dynamic buttons: `view-book-button-{book_id}`
  - `back-to-dashboard`: Button to `/dashboard`
- Context Variables:
  - `bestsellers`: list of dict
  - `time_period`: str
- Navigation:
  - Buttons use `url_for()` for navigation


## Section 3: Data Schemas Specification

---

### 1. Books Data
- File Path: `data/books.txt`
- Format: Pipe-delimited (`|`)
- Field Order:
  1. book_id (int)
  2. title (str)
  3. author (str)
  4. isbn (str)
  5. category (str)
  6. price (float)
  7. stock (int)
  8. description (str)
- Description: Stores book details.
- Example rows:
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

---

### 2. Categories Data
- File Path: `data/categories.txt`
- Format: Pipe-delimited (`|`)
- Field Order:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
- Description: Stores book categories.
- Example rows:
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

---

### 3. Cart Data
- File Path: `data/cart.txt`
- Format: Pipe-delimited (`|`)
- Field Order:
  1. cart_id (int)
  2. book_id (int)
  3. quantity (int)
  4. added_date (str
 YYYY-MM-DD)
- Description: Stores items added to shopping cart.
- Example rows:
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

---

### 4. Orders Data
- File Path: `data/orders.txt`
- Format: Pipe-delimited (`|`)
- Field Order:
  1. order_id (int)
  2. customer_name (str)
  3. order_date (str
 YYYY-MM-DD)
  4. total_amount (float)
  5. status (str: Pending
 Shipped
 Delivered)
  6. shipping_address (str)
- Description: Stores orders placed by customers.
- Example rows:
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St
 New York
 NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave
 Los Angeles
 CA 90001
  ```

---

### 5. Order Items Data
- File Path: `data/order_items.txt`
- Format: Pipe-delimited (`|`)
- Field Order:
  1. order_item_id (int)
  2. order_id (int)
  3. book_id (int)
  4. quantity (int)
  5. price (float)
- Description: Stores individual book items within orders.
- Example rows:
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

---

### 6. Reviews Data
- File Path: `data/reviews.txt`
- Format: Pipe-delimited (`|`)
- Field Order:
  1. review_id (int)
  2. book_id (int)
  3. customer_name (str)
  4. rating (int
 1-5)
  5. review_text (str)
  6. review_date (str
 YYYY-MM-DD)
- Description: Stores customer reviews for books.
- Example rows:
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

---

### 7. Bestsellers Data
- File Path: `data/bestsellers.txt`
- Format: Pipe-delimited (`|`)
- Field Order:
  1. book_id (int)
  2. sales_count (int)
  3. period (str: "This Week"
 "This Month"
 "All Time")
- Description: Stores top-selling books ranked by sales count over a time period.
- Example rows:
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

This completes the detailed design specification for the BookstoreOnline application
 covering all Flask routes
 frontend templates
 and backend data file schemas exactly per provided requirements.

---
