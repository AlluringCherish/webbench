# Design Specification for BookstoreOnline

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Methods:** GET
- **Template Rendered:** None (Redirect)
- **Description:** Redirects to `/dashboard`.

### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** `dashboard_page`
- **HTTP Methods:** GET
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `featured_books` (list of dicts): Each dict contains `book_id` (int), `title` (str), `author` (str), `price` (float), `isbn` (str), `category` (str), `stock` (int), `description` (str)
  - `bestsellers` (list of dicts): Each dict contains `book_id` (int), `title` (str), `author` (str), `sales_count` (int), `period` (str)

### 3. Book Catalog Page
- **Route Path:** `/catalog`
- **Function Name:** `catalog_page`
- **HTTP Methods:** GET
- **Template Rendered:** `catalog.html`
- **Context Variables:**
  - `categories` (list of dicts): Each dict contains `category_id` (int), `category_name` (str), `description` (str)
  - `books` (list of dicts): Filtered list of books, each dict with `book_id` (int), `title` (str), `author` (str), `price` (float), `isbn` (str), `category` (str), `stock` (int), `description` (str)
  - `search_query` (str): Search string entered
  - `selected_category` (str): Selected category name for filtering

### 4. Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** `book_details_page`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `book_details.html`
- **Context Variables:**
  - `book` (dict): `book_id` (int), `title` (str), `author` (str), `price` (float), `isbn` (str), `category` (str), `stock` (int), `description` (str)
  - `reviews` (list of dicts): Each dict contains `review_id` (int), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str: YYYY-MM-DD)

- **Form Handling:**
  - POST for "Add to Cart" submission:
    - Form submits selected book_id and quantity (default quantity to 1 if not specified).
    - On POST, add or update the cart data file accordingly.

### 5. Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** `cart_page`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `cart.html`
- **Context Variables:**
  - `cart_items` (list of dicts): Each dict has `cart_id` (int), `book_id` (int), `title` (str), `quantity` (int), `price` (float), `subtotal` (float)
  - `total_amount` (float)

- **Form Handling:**
  - POST requests handle update quantity or remove item from cart.
    - Form data includes the `cart_id` and the new `quantity` or action to remove.

### 6. Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** `checkout_page`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `checkout.html`
- **Context Variables:**
  - `cart_items` (list of dicts): Same as in cart page.
  - `total_amount` (float)

- **Form Handling:**
  - POST form submits:
    - `customer_name` (str)
    - `shipping_address` (str)
    - `payment_method` (str) - one of "Credit Card", "PayPal", "Bank Transfer"
  - On successful validation, create new order and order items entries, clear cart.

### 7. Order History Page
- **Route Path:** `/orders`
- **Function Name:** `orders_page`
- **HTTP Methods:** GET
- **Template Rendered:** `orders.html`
- **Context Variables:**
  - `orders` (list of dicts): Each dict with `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str), `shipping_address` (str)
  - `status_filter` (str): Selected status filter value (e.g., "All", "Pending", "Shipped", "Delivered")

### 8. Order Details Page (implied for viewing)
- **Note:** No explicit page described, but `view-order-button-{order_id}` exists.
- Assuming a route `/orders/<int:order_id>`
- **Route Path:** `/orders/<int:order_id>`
- **Function Name:** `order_details_page`
- **HTTP Methods:** GET
- **Template Rendered:** Could be reused `order_details.html` (not explicitly requested, so omitted)
- **Context Variables:** Would include order and order items details (not required by user task)

### 9. Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** `reviews_page`
- **HTTP Methods:** GET
- **Template Rendered:** `reviews.html`
- **Context Variables:**
  - `reviews` (list of dicts): Each dict includes `review_id` (int), `book_id` (int), `book_title` (str), `rating` (int), `review_text` (str), `review_date` (str)
  - `rating_filter` (str): Filter selected value (e.g., "All", "5 stars", "4 stars", etc.)

### 10. Write Review Page
- **Route Path:** `/write_review`
- **Function Name:** `write_review_page`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `write_review.html`
- **Context Variables:**
  - `purchased_books` (list of dicts): Books the user can review; each dict has `book_id` (int) and `title` (str)

- **Form Handling:**
  - POST form submits:
    - `book_id` (int)
    - `rating` (int, 1-5)
    - `review_text` (str)
  - On submission, append new review to reviews.txt

### 11. Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** `bestsellers_page`
- **HTTP Methods:** GET
- **Template Rendered:** `bestsellers.html`
- **Context Variables:**
  - `bestsellers` (list of dicts): Sorted list depending on `time_period_filter`; each dict has `book_id` (int), `title` (str), `author` (str), `sales_count` (int), `period` (str)
  - `time_period_filter` (str): Selected filter option ("This Week", "This Month", "All Time")

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page Template
- **File Path:** `templates/dashboard.html`
- **Page Title:** `Bookstore Dashboard`
- **Main H1 Heading:** `Bookstore Dashboard`
- **Element IDs:**
  - `dashboard-page` (Div) - main container
  - `featured-books` (Div) - shows featured books
  - `browse-catalog-button` (Button) - navigates to `url_for('catalog_page')`
  - `view-cart-button` (Button) - navigates to `url_for('cart_page')`
  - `bestsellers-button` (Button) - navigates to `url_for('bestsellers_page')`

- **Context Variables:**
  - `featured_books` (list of dicts)
  - `bestsellers` (list of dicts)

### 2. Book Catalog Page Template
- **File Path:** `templates/catalog.html`
- **Page Title:** `Book Catalog`
- **Main H1 Heading:** `Book Catalog`
- **Element IDs:**
  - `catalog-page` (Div) - main container
  - `search-input` (Input) - for search text (name="search_query")
  - `category-filter` (Dropdown) - for categories filter (name="category_filter")
  - `books-grid` (Div) - grid container for book cards
  - `view-book-button-{book_id}` (Button) - button on each book card to view details

- **Context Variables:**
  - `categories` (list of dicts)
  - `books` (list of dicts)
  - `search_query` (str)
  - `selected_category` (str)

### 3. Book Details Page Template
- **File Path:** `templates/book_details.html`
- **Page Title:** `Book Details`
- **Main H1 Heading:** `Book Details`
- **Element IDs:**
  - `book-details-page` (Div) - main container
  - `book-title` (H1) - show selected book title
  - `book-author` (Div) - shows book author
  - `book-price` (Div) - shows book price
  - `add-to-cart-button` (Button) - posts form to add book to cart
  - `book-reviews` (Div) - contains list of reviews

- **Context Variables:**
  - `book` (dict)
  - `reviews` (list of dicts)

- **Form Details:** POST form wraps "Add to Cart" button, submits with method POST including hidden `book_id` and quantity (default 1, or can be a hidden or input field if extended).

### 4. Shopping Cart Page Template
- **File Path:** `templates/cart.html`
- **Page Title:** `Shopping Cart`
- **Main H1 Heading:** `Shopping Cart`
- **Element IDs:**
  - `cart-page` (Div) - main container
  - `cart-items-table` (Table) - displays cart items
  - `update-quantity-{item_id}` (Input number) - input for quantity update for each item
  - `remove-item-button-{item_id}` (Button) - remove button for each item
  - `proceed-checkout-button` (Button) - navigates to `url_for('checkout_page')`
  - `total-amount` (Div) - shows total cart amount

- **Context Variables:**
  - `cart_items` (list of dicts)
  - `total_amount` (float)

- **Form Details:** Forms for updating quantity or removing item, POST request with `cart_id` and action parameters.

### 5. Checkout Page Template
- **File Path:** `templates/checkout.html`
- **Page Title:** `Checkout`
- **Main H1 Heading:** `Checkout`
- **Element IDs:**
  - `checkout-page` (Div) - main container
  - `customer-name` (Input) - for customer name input
  - `shipping-address` (Textarea) - for shipping address input
  - `payment-method` (Dropdown) - payment method selection
  - `place-order-button` (Button) - submit button

- **Context Variables:**
  - `cart_items` (list of dicts)
  - `total_amount` (float)

- **Form Details:** POST form with inputs for customer name, shipping address, payment method, submitting order.

### 6. Order History Page Template
- **File Path:** `templates/orders.html`
- **Page Title:** `Order History`
- **Main H1 Heading:** `Order History`
- **Element IDs:**
  - `orders-page` (Div) - main container
  - `orders-table` (Table) - displays orders
  - `view-order-button-{order_id}` (Button) - button to view order details
  - `order-status-filter` (Dropdown) - filter for status
  - `back-to-dashboard` (Button) - navigates to `url_for('dashboard_page')`

- **Context Variables:**
  - `orders` (list of dicts)
  - `status_filter` (str)

### 7. Reviews Page Template
- **File Path:** `templates/reviews.html`
- **Page Title:** `Customer Reviews`
- **Main H1 Heading:** `Customer Reviews`
- **Element IDs:**
  - `reviews-page` (Div) - main container
  - `reviews-list` (Div) - list of reviews
  - `write-review-button` (Button) - navigates to `url_for('write_review_page')`
  - `filter-by-rating` (Dropdown) - rating filter
  - `back-to-dashboard` (Button) - navigates to `url_for('dashboard_page')`

- **Context Variables:**
  - `reviews` (list of dicts)
  - `rating_filter` (str)

### 8. Write Review Page Template
- **File Path:** `templates/write_review.html`
- **Page Title:** `Write a Review`
- **Main H1 Heading:** `Write a Review`
- **Element IDs:**
  - `write-review-page` (Div) - main container
  - `select-book` (Dropdown) - select book to review
  - `rating-select` (Dropdown) - select rating (1-5)
  - `review-text` (Textarea) - write review text
  - `submit-review-button` (Button) - submit review

- **Context Variables:**
  - `purchased_books` (list of dicts)

- **Form Details:** POST form that submits selected book_id, rating, and review_text.

### 9. Bestsellers Page Template
- **File Path:** `templates/bestsellers.html`
- **Page Title:** `Bestsellers`
- **Main H1 Heading:** `Bestsellers`
- **Element IDs:**
  - `bestsellers-page` (Div) - main container
  - `bestsellers-list` (Div) - ranked list of bestsellers
  - `time-period-filter` (Dropdown) - filter period
  - `view-book-button-{book_id}` (Button) - view book details
  - `back-to-dashboard` (Button) - navigates to `url_for('dashboard_page')`

- **Context Variables:**
  - `bestsellers` (list of dicts)
  - `time_period_filter` (str)

---

## Section 3: Data Schemas Specification

### 1. Books Data
- **File Path:** `data/books.txt`
- **Format:** Pipe-delimited (`|`), no header line
- **Fields (in order):**
  1. `book_id` (int) - Unique identifier for each book
  2. `title` (str) - Title of the book
  3. `author` (str) - Author of the book
  4. `isbn` (str) - ISBN number
  5. `category` (str) - Book category name
  6. `price` (float) - Price in USD
  7. `stock` (int) - Number of available copies
  8. `description` (str) - Short description of the book

- **Example Rows:**
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

### 2. Categories Data
- **File Path:** `data/categories.txt`
- **Format:** Pipe-delimited (`|`), no header line
- **Fields (in order):**
  1. `category_id` (int) - Unique identifier for category
  2. `category_name` (str) - Name of category
  3. `description` (str) - Description of category

- **Example Rows:**
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

### 3. Cart Data
- **File Path:** `data/cart.txt`
- **Format:** Pipe-delimited (`|`), no header line
- **Fields (in order):**
  1. `cart_id` (int) - Unique item in cart
  2. `book_id` (int) - Book item ID
  3. `quantity` (int) - Quantity of book in cart
  4. `added_date` (str, format YYYY-MM-DD) - Date item was added to cart

- **Example Rows:**
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

### 4. Orders Data
- **File Path:** `data/orders.txt`
- **Format:** Pipe-delimited (`|`), no header line
- **Fields (in order):**
  1. `order_id` (int) - Unique order identifier
  2. `customer_name` (str) - Name of customer
  3. `order_date` (str, format YYYY-MM-DD) - Date order placed
  4. `total_amount` (float) - Total order amount
  5. `status` (str) - Order status (Pending, Shipped, Delivered)
  6. `shipping_address` (str) - Shipping address

- **Example Rows:**
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

### 5. Order Items Data
- **File Path:** `data/order_items.txt`
- **Format:** Pipe-delimited (`|`), no header line
- **Fields (in order):**
  1. `order_item_id` (int) - Unique order item identifier
  2. `order_id` (int) - Parent order ID
  3. `book_id` (int) - Book placed in order
  4. `quantity` (int) - Quantity ordered
  5. `price` (float) - Price per unit at order time

- **Example Rows:**
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

### 6. Reviews Data
- **File Path:** `data/reviews.txt`
- **Format:** Pipe-delimited (`|`), no header line
- **Fields (in order):**
  1. `review_id` (int) - Unique review identifier
  2. `book_id` (int) - Book being reviewed
  3. `customer_name` (str) - Reviewer name
  4. `rating` (int, 1-5) - Rating given
  5. `review_text` (str) - Text review
  6. `review_date` (str, format YYYY-MM-DD) - Date of review

- **Example Rows:**
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

### 7. Bestsellers Data
- **File Path:** `data/bestsellers.txt`
- **Format:** Pipe-delimited (`|`), no header line
- **Fields (in order):**
  1. `book_id` (int) - Book identifier
  2. `sales_count` (int) - Number of sales
  3. `period` (str) - Sales period ("This Week", "This Month", "All Time")

- **Example Rows:**
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

This detailed design specification fully supports independent implementation of the Flask backend and frontend UI for the BookstoreOnline application, consistent with the user task requirements.