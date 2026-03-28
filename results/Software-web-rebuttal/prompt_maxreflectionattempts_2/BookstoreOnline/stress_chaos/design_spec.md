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
  - `featured_books` (list of dict): List of featured books with keys: `book_id` (int), `title` (str), `author` (str), `price` (float)
  - `bestsellers` (list of dict): List of bestseller books with keys: `book_id` (int), `title` (str), `author` (str), `sales_count` (int)

### 3. Book Catalog Page
- **Route Path:** `/catalog`
- **Function Name:** `catalog_page`
- **HTTP Methods:** GET
- **Template Rendered:** `catalog.html`
- **Context Variables:**
  - `categories` (list of dict): List of categories with keys: `category_id` (int), `category_name` (str)
  - `books` (list of dict): List of books with keys: `book_id` (int), `title` (str), `author` (str), `price` (float)

### 4. Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** `book_details`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `book_details.html`
- **Context Variables:**
  - `book` (dict): Keys: `book_id` (int), `title` (str), `author` (str), `price` (float), `description` (str), `stock` (int)
  - `reviews` (list of dict): Each review dict with keys: `review_id` (int), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str)

- **Handling Form Submissions:**
  - POST method handles "Add to Cart" action when `add_to_cart_button` clicked or form submitted.
  - Quantity can be assumed 1 as not specified.
  - Backend adds book to `cart.txt` (or increments quantity if exists).
  - Redirect user back to book details or cart page after adding.

### 5. Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** `shopping_cart`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `cart.html`
- **Context Variables:**
  - `cart_items` (list of dict): Each dict with keys: `cart_id` (int), `book_id` (int), `title` (str), `quantity` (int), `price` (float), `subtotal` (float)
  - `total_amount` (float): Total price for all items in cart.

- **Handling Form Submissions:**
  - POST method handles quantity updates via inputs named `update-quantity-{item_id}`
  - Removal of items handled by buttons with IDs `remove-item-button-{item_id}`
  - Upon updating quantity or removing item, backend updates `cart.txt` accordingly.
  - Proceed to checkout button navigates to `/checkout`.

### 6. Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** `checkout_page`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `checkout.html`
- **Context Variables:**
  - None needed for GET, except possibly cart summary (optional).

- **Handling Form Submissions:**
  - POST method handles order placement.
  - Form fields: `customer_name` (str), `shipping_address` (str), `payment_method` (str: Credit Card, PayPal, Bank Transfer)
  - Backend creates new entry in `orders.txt`, and entries in `order_items.txt` from cart.
  - Clears `cart.txt` after successful order.
  - Redirect to order history or confirmation page (order history specified, so redirect to `/orders`).

### 7. Order History Page
- **Route Path:** `/orders`
- **Function Name:** `order_history`
- **HTTP Methods:** GET
- **Template Rendered:** `orders.html`
- **Context Variables:**
  - `orders` (list of dict): Each with keys: `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str), `shipping_address` (str)
  - `status_filter` (str): Current filter selected (All, Pending, Shipped, Delivered)

- **Handling Filtering:**
  - `status_filter` applied to filter displayed orders.

### 8. Order Details Page (Optional but inferred from view-order-button-{order_id})
- **Route Path:** `/orders/<int:order_id>`
- **Function Name:** `order_details`
- **HTTP Methods:** GET
- **Template Rendered:** `order_details.html`(optional but logically required)
- **Context Variables:**
  - `order` (dict): Order info with keys same as above.
  - `order_items` (list of dict): Each with keys: `book_id` (int), `title` (str), `quantity` (int), `price` (float)

### 9. Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** `reviews_page`
- **HTTP Methods:** GET
- **Template Rendered:** `reviews.html`
- **Context Variables:**
  - `reviews` (list of dict): Each with keys: `review_id` (int), `book_title` (str), `rating` (int), `review_text` (str), `review_date` (str)
  - `rating_filter` (str): Current filter selected (All, 5, 4, etc.)

### 10. Write Review Page
- **Route Path:** `/write_review`
- **Function Name:** `write_review_page`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `write_review.html`
- **Context Variables:**
  - `purchased_books` (list of dict): Books which can be reviewed, keys: `book_id` (int), `title` (str)

- **Handling Form Submissions:**
  - POST method to submit review with fields: `book_id` (int), `rating` (int 1-5), `review_text` (str), `customer_name` default can be anonymous or input but not specified, assuming anonymous or fixed.
  - Backend adds new review entry to `reviews.txt` with generated `review_id` and current date.
  - Redirect back to `/reviews` after submission.

### 11. Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** `bestsellers_page`
- **HTTP Methods:** GET
- **Template Rendered:** `bestsellers.html`
- **Context Variables:**
  - `bestsellers` (list of dict): Each with keys: `book_id` (int), `title` (str), `author` (str), `sales_count` (int), `period` (str)
  - `period_filter` (str): Current filter selected (This Week, This Month, All Time)

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page Template
- **File Path:** `templates/dashboard.html`
- **Page Title:** `Bookstore Dashboard`
- **Main Heading `<h1>`:** `Bookstore Dashboard`
- **Element IDs:**
  - `dashboard-page` (Div) - container for whole dashboard page
  - `featured-books` (Div) - displays featured book recommendations
  - `browse-catalog-button` (Button) - navigates to `/catalog`
  - `view-cart-button` (Button) - navigates to `/cart`
  - `bestsellers-button` (Button) - navigates to `/bestsellers`
- **Context Variables:**
  - `featured_books` (list of dict)
  - `bestsellers` (list of dict)
- **Navigation:**
  - `browse-catalog-button` uses `url_for('catalog_page')`
  - `view-cart-button` uses `url_for('shopping_cart')`
  - `bestsellers-button` uses `url_for('bestsellers_page')`

### 2. Book Catalog Page Template
- **File Path:** `templates/catalog.html`
- **Page Title:** `Book Catalog`
- **Main Heading `<h1>`:** `Book Catalog`
- **Element IDs:**
  - `catalog-page` (Div) - container for catalog page
  - `search-input` (Input) - input for search
  - `category-filter` (Dropdown) - category filter
  - `books-grid` (Div) - grid for book cards
  - `view-book-button-{book_id}` (Button) - view book details
- **Context Variables:**
  - `categories` (list of dict)
  - `books` (list of dict)
- **Navigation:**
  - `view-book-button-{book_id}` uses `url_for('book_details', book_id=book_id)`

### 3. Book Details Page Template
- **File Path:** `templates/book_details.html`
- **Page Title:** `Book Details`
- **Main Heading `<h1>`:** `book['title']` (dynamic)
- **Element IDs:**
  - `book-details-page` (Div) - container for book details
  - `book-title` (H1) - book title
  - `book-author` (Div) - book author
  - `book-price` (Div) - book price
  - `add-to-cart-button` (Button) - add to cart
  - `book-reviews` (Div) - customer reviews section
- **Context Variables:**
  - `book` (dict)
  - `reviews` (list of dict)
- **Form Details:**
  - POST form wraps `add-to-cart-button`
  - Form submits to `/book/<book_id>` with POST

### 4. Shopping Cart Page Template
- **File Path:** `templates/cart.html`
- **Page Title:** `Shopping Cart`
- **Main Heading `<h1>`:** `Shopping Cart`
- **Element IDs:**
  - `cart-page` (Div) - container for cart page
  - `cart-items-table` (Table) - shows items in cart
  - `update-quantity-{cart_id}` (Input, number) - updates quantity for cart item
  - `remove-item-button-{cart_id}` (Button) - removes item
  - `proceed-checkout-button` (Button) - proceeds to checkout
  - `total-amount` (Div) - shows total amount
- **Context Variables:**
  - `cart_items` (list of dict)
  - `total_amount` (float)
- **Form Details:**
  - POST form wraps quantity inputs and remove buttons
  - POST form submits changes to `/cart`
  - `proceed-checkout-button` links to `/checkout`

### 5. Checkout Page Template
- **File Path:** `templates/checkout.html`
- **Page Title:** `Checkout`
- **Main Heading `<h1>`:** `Checkout`
- **Element IDs:**
  - `checkout-page` (Div) - container for checkout page
  - `customer-name` (Input) - customer name input
  - `shipping-address` (Textarea) - shipping address input
  - `payment-method` (Dropdown) - payment method select
  - `place-order-button` (Button) - place order button
- **Context Variables:** None
- **Form Details:**
  - POST form wrapping all inputs and button
  - Form submits to `/checkout`

### 6. Order History Page Template
- **File Path:** `templates/orders.html`
- **Page Title:** `Order History`
- **Main Heading `<h1>`:** `Order History`
- **Element IDs:**
  - `orders-page` (Div) - container for orders
  - `orders-table` (Table) - displays orders
  - `view-order-button-{order_id}` (Button) - view order details
  - `order-status-filter` (Dropdown) - filter orders status
  - `back-to-dashboard` (Button) - goes to dashboard
- **Context Variables:**
  - `orders` (list of dict)
  - `status_filter` (str)
- **Navigation:**
  - `view-order-button-{order_id}` uses `url_for('order_details', order_id=order_id)`
  - `back-to-dashboard` uses `url_for('dashboard_page')`

### 7. Reviews Page Template
- **File Path:** `templates/reviews.html`
- **Page Title:** `Customer Reviews`
- **Main Heading `<h1>`:** `Customer Reviews`
- **Element IDs:**
  - `reviews-page` (Div) - container for reviews
  - `reviews-list` (Div) - list of reviews
  - `write-review-button` (Button) - goes to write review
  - `filter-by-rating` (Dropdown) - filter reviews by rating
  - `back-to-dashboard` (Button) - goes to dashboard
- **Context Variables:**
  - `reviews` (list of dict)
  - `rating_filter` (str)
- **Navigation:**
  - `write-review-button` uses `url_for('write_review_page')`
  - `back-to-dashboard` uses `url_for('dashboard_page')`

### 8. Write Review Page Template
- **File Path:** `templates/write_review.html`
- **Page Title:** `Write a Review`
- **Main Heading `<h1>`:** `Write a Review`
- **Element IDs:**
  - `write-review-page` (Div) - container
  - `select-book` (Dropdown) - select book to review
  - `rating-select` (Dropdown) - select rating 1-5
  - `review-text` (Textarea) - write text
  - `submit-review-button` (Button) - submit
- **Context Variables:**
  - `purchased_books` (list of dict)
- **Form Details:**
  - POST form wrapping fields and submit button
  - Form submits to `/write_review`

### 9. Bestsellers Page Template
- **File Path:** `templates/bestsellers.html`
- **Page Title:** `Bestsellers`
- **Main Heading `<h1>`:** `Bestsellers`
- **Element IDs:**
  - `bestsellers-page` (Div) - container
  - `bestsellers-list` (Div) - ranked list
  - `time-period-filter` (Dropdown) - period filter
  - `view-book-button-{book_id}` (Button) - view book details
  - `back-to-dashboard` (Button) - back to dashboard
- **Context Variables:**
  - `bestsellers` (list of dict)
  - `period_filter` (str)
- **Navigation:**
  - `view-book-button-{book_id}` uses `url_for('book_details', book_id=book_id)`
  - `back-to-dashboard` uses `url_for('dashboard_page')`

---

## Section 3: Data Schemas Specification

### 1. Books Data
- **File Path:** `data/books.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields and Order:**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `category` (str)
  6. `price` (float)
  7. `stock` (int)
  8. `description` (str)
- **Description:** Stores all books available for sale with details.
- **Example Rows:**
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

### 2. Categories Data
- **File Path:** `data/categories.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields and Order:**
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- **Description:** Categories for classifying books.
- **Example Rows:**
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

### 3. Cart Data
- **File Path:** `data/cart.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields and Order:**
  1. `cart_id` (int)
  2. `book_id` (int)
  3. `quantity` (int)
  4. `added_date` (str, YYYY-MM-DD)
- **Description:** Current shopping cart items.
- **Example Rows:**
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

### 4. Orders Data
- **File Path:** `data/orders.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields and Order:**
  1. `order_id` (int)
  2. `customer_name` (str)
  3. `order_date` (str, YYYY-MM-DD)
  4. `total_amount` (float)
  5. `status` (str) - Possible values: Pending, Shipped, Delivered
  6. `shipping_address` (str)
- **Description:** Stores order summaries.
- **Example Rows:**
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

### 5. Order Items Data
- **File Path:** `data/order_items.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields and Order:**
  1. `order_item_id` (int)
  2. `order_id` (int)
  3. `book_id` (int)
  4. `quantity` (int)
  5. `price` (float)
- **Description:** Line items for each order.
- **Example Rows:**
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

### 6. Reviews Data
- **File Path:** `data/reviews.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields and Order:**
  1. `review_id` (int)
  2. `book_id` (int)
  3. `customer_name` (str)
  4. `rating` (int, 1-5)
  5. `review_text` (str)
  6. `review_date` (str, YYYY-MM-DD)
- **Description:** Customer reviews for books.
- **Example Rows:**
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

### 7. Bestsellers Data
- **File Path:** `data/bestsellers.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields and Order:**
  1. `book_id` (int)
  2. `sales_count` (int)
  3. `period` (str)
- **Description:** Top selling books ranked by sales in time periods.
- **Example Rows:**
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

# End of Design Specification
