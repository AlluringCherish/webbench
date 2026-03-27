# Design Specification for BookstoreOnline

---

## 1. Flask Routes Specification

### 1. Root Route
- **Route Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Methods:** GET
- **Template Rendered:** None (Redirect)
- **Behavior:** Redirects to `/dashboard`

---

### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** `dashboard`
- **HTTP Methods:** GET
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `featured_books` (list of dict) - each dict with keys: `book_id` (int), `title` (str), `author` (str), `price` (float)
  - `bestsellers` (list of dict) - top selling books with same keys as above

---

### 3. Book Catalog Page
- **Route Path:** `/catalog`
- **Function Name:** `book_catalog`
- **HTTP Methods:** GET
- **Template Rendered:** `catalog.html`
- **Context Variables:**
  - `books` (list of dict) - all books, each dict includes: `book_id` (int), `title` (str), `author` (str), `price` (float), `category` (str)
  - `categories` (list of dict) - categories with: `category_id` (int), `category_name` (str)
  - `search_query` (str) - current search string (empty if none)
  - `selected_category_id` (int or None) - category filter currently selected

- **Filtering & Searching:** handled via query parameters (GET)

---

### 4. Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** `book_details`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `book_details.html`
- **Context Variables:**
  - `book` (dict) - with keys: `book_id` (int), `title` (str), `author` (str), `price` (float), `description` (str), `stock` (int)
  - `reviews` (list of dict) - each review with keys: `review_id` (int), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str)

- **POST Handling:**
  - POST used to add book to cart
  - Form submission handled on this route via form data: `quantity` (int)

---

### 5. Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** `shopping_cart`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `cart.html`
- **Context Variables:**
  - `cart_items` (list of dict) - each dict includes: `cart_id` (int), `book_id` (int), `title` (str), `quantity` (int), `price` (float), `subtotal` (float)
  - `total_amount` (float) - total cart value

- **POST Handling:**
  - Update quantities or remove items via form submissions
  - Form fields:
    - For updating quantity: `cart_id` (int), `quantity` (int)
    - For removing item: `cart_id` (int), action indicated by submit button name/value

---

### 6. Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** `checkout`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `checkout.html`
- **Context Variables:** None for GET. For POST, after submission, may redirect.

- **POST Handling:**
  - Form fields:
    - `customer_name` (str)
    - `shipping_address` (str)
    - `payment_method` (str) - one of "Credit Card", "PayPal", "Bank Transfer"
  - On successful submission, order is processed and user redirected to order history or confirmation page.

---

### 7. Order History Page
- **Route Path:** `/orders`
- **Function Name:** `order_history`
- **HTTP Methods:** GET
- **Template Rendered:** `orders.html`
- **Context Variables:**
  - `orders` (list of dict) - each with: `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str)
  - `status_filter` (str) - selected filter status (e.g., "All", "Pending", "Shipped", "Delivered")

- **Filtering:** via query parameter `status`

---

### 8. Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** `reviews_page`
- **HTTP Methods:** GET
- **Template Rendered:** `reviews.html`
- **Context Variables:**
  - `reviews` (list of dict) - each with: `review_id` (int), `book_title` (str), `rating` (int), `review_text` (str), `review_date` (str)
  - `rating_filter` (str) - selected filter value ("All", "5", "4"...)

- **Filtering:** via query parameter `rating`

---

### 9. Write Review Page
- **Route Path:** `/write-review`
- **Function Name:** `write_review`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `write_review.html`
- **Context Variables:**
  - `purchased_books` (list of dict) - books eligible for review, each with `book_id` (int), `title` (str)

- **POST Handling:**
  - Form fields:
    - `book_id` (int)
    - `rating` (int, 1-5)
    - `review_text` (str)

---

### 10. Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** `bestsellers_page`
- **HTTP Methods:** GET
- **Template Rendered:** `bestsellers.html`
- **Context Variables:**
  - `bestsellers` (list of dict) - each dict includes: `rank` (int), `book_id` (int), `title` (str), `author` (str), `sales_count` (int)
  - `time_period` (str) - selected time period filter ("This Week", "This Month", "All Time")

- **Filtering:** via query parameter `period`

---

## 2. HTML Templates Specification

### Template File: `templates/dashboard.html`
- **Title Tag Content:** Bookstore Dashboard
- **Main Heading (`<h1>`):** Bookstore Dashboard
- **Element IDs:**
  - `dashboard-page` (Div) - container for the entire dashboard page
  - `featured-books` (Div) - displays featured book recommendations dynamically
  - `browse-catalog-button` (Button) - navigates to catalog page
  - `view-cart-button` (Button) - navigates to cart page
  - `bestsellers-button` (Button) - navigates to bestsellers page
- **Context Variables:**
  - `featured_books` (list of dict) - each dict: `book_id` (int), `title` (str), `author` (str), `price` (float)
  - `bestsellers` (list of dict) - same structure for top sellers
- **Navigation:**
  - Buttons use `url_for('book_catalog')`, `url_for('shopping_cart')`, `url_for('bestsellers_page')`

---

### Template File: `templates/catalog.html`
- **Title Tag Content:** Book Catalog
- **Main Heading (`<h1>`):** Book Catalog
- **Element IDs:**
  - `catalog-page` (Div) - page container
  - `search-input` (Input, type=text) - text search for title, author, ISBN
  - `category-filter` (Dropdown/select) - category selection
  - `books-grid` (Div) - grid display of book cards
  - `view-book-button-{book_id}` (Button) - dynamic per book for details
- **Context Variables:**
  - `books` (list of dict) - each dict: `book_id` (int), `title` (str), `author` (str), `price` (float), `category` (str)
  - `categories` (list of dict) - each: `category_id` (int), `category_name` (str)
  - `search_query` (str)
  - `selected_category_id` (int or None)
- **Navigation:**
  - Book detail buttons use `url_for('book_details', book_id=book.book_id)`

---

### Template File: `templates/book_details.html`
- **Title Tag Content:** Book Details
- **Main Heading (`<h1>`):** (dynamic) Book Title
- **Element IDs:**
  - `book-details-page` (Div) - page container
  - `book-title` (H1) - displays `book.title`
  - `book-author` (Div) - displays `book.author`
  - `book-price` (Div) - displays `book.price` formatted
  - `add-to-cart-button` (Button) - submits add to cart form
  - `book-reviews` (Div) - displays list of reviews dynamically
- **Context Variables:**
  - `book` (dict) - keys: `book_id`, `title`, `author`, `price`, `description`, `stock`
  - `reviews` (list of dict) - each dict: `review_id`, `customer_name`, `rating`, `review_text`, `review_date`
- **Form:**
  - POST form at this page to add book to cart
  - Fields: `quantity` (number input, min=1, max=book.stock)
  - Submit button with id `add-to-cart-button`

---

### Template File: `templates/cart.html`
- **Title Tag Content:** Shopping Cart
- **Main Heading (`<h1>`):** Shopping Cart
- **Element IDs:**
  - `cart-page` (Div) - page container
  - `cart-items-table` (Table) - headers: Title, Quantity, Price, Subtotal
  - `update-quantity-{item_id}` (Input number) - per cart item quantity input
  - `remove-item-button-{item_id}` (Button) - per cart item remove button
  - `proceed-checkout-button` (Button) - navigates to checkout page
  - `total-amount` (Div) - displays total price
- **Context Variables:**
  - `cart_items` (list of dict) - each dict: `cart_id` (int), `book_id` (int), `title` (str), `quantity` (int), `price` (float), `subtotal` (float)
  - `total_amount` (float)
- **Form:**
  - POST form to update quantities or remove items
  - Fields per item: `cart_id`, `quantity`
  - Remove forms include `cart_id` and remove action
- **Navigation:**
  - `proceed-checkout-button` uses `url_for('checkout')`

---

### Template File: `templates/checkout.html`
- **Title Tag Content:** Checkout
- **Main Heading (`<h1>`):** Checkout
- **Element IDs:**
  - `checkout-page` (Div) - page container
  - `customer-name` (Input text)
  - `shipping-address` (Textarea)
  - `payment-method` (Dropdown/select) - options: "Credit Card", "PayPal", "Bank Transfer"
  - `place-order-button` (Button) - submits order
- **Context Variables:** None
- **Form:**
  - Method POST
  - Fields required: `customer_name` (text), `shipping_address` (textarea), `payment_method` (select)

---

### Template File: `templates/orders.html`
- **Title Tag Content:** Order History
- **Main Heading (`<h1>`):** Order History
- **Element IDs:**
  - `orders-page` (Div) - page container
  - `orders-table` (Table) - columns: Order ID, Date, Total, Status
  - `view-order-button-{order_id}` (Button) - per order details
  - `order-status-filter` (Dropdown/select) - filter status (All, Pending, Shipped, Delivered)
  - `back-to-dashboard` (Button) - navigate to dashboard
- **Context Variables:**
  - `orders` (list of dict) - each dict: `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str)
  - `status_filter` (str)
- **Navigation:**
  - Back button uses `url_for('dashboard')`

---

### Template File: `templates/reviews.html`
- **Title Tag Content:** Customer Reviews
- **Main Heading (`<h1>`):** Customer Reviews
- **Element IDs:**
  - `reviews-page` (Div) - container
  - `reviews-list` (Div) - list of reviews
  - `write-review-button` (Button) - navigate to write review
  - `filter-by-rating` (Dropdown/select) - filter by rating
  - `back-to-dashboard` (Button) - navigate to dashboard
- **Context Variables:**
  - `reviews` (list of dict) - each with `review_id` (int), `book_title` (str), `rating` (int), `review_text` (str), `review_date` (str)
  - `rating_filter` (str)
- **Navigation:**
  - Write Review button: `url_for('write_review')`
  - Back button: `url_for('dashboard')`

---

### Template File: `templates/write_review.html`
- **Title Tag Content:** Write a Review
- **Main Heading (`<h1>`):** Write a Review
- **Element IDs:**
  - `write-review-page` (Div) - page container
  - `select-book` (Dropdown/select) - select book to review
  - `rating-select` (Dropdown/select) - select rating 1-5
  - `review-text` (Textarea) - input review text
  - `submit-review-button` (Button) - submits review
- **Context Variables:**
  - `purchased_books` (list of dict) - each dict: `book_id` (int), `title` (str)
- **Form:**
  - POST method
  - Fields: `book_id`, `rating`, `review_text`

---

### Template File: `templates/bestsellers.html`
- **Title Tag Content:** Bestsellers
- **Main Heading (`<h1>`):** Bestsellers
- **Element IDs:**
  - `bestsellers-page` (Div) - page container
  - `bestsellers-list` (Div) - ranked list of books
  - `time-period-filter` (Dropdown/select) - filter period
  - `view-book-button-{book_id}` (Button) - per book details
  - `back-to-dashboard` (Button) - navigate dashboard
- **Context Variables:**
  - `bestsellers` (list of dict) - with: `rank` (int), `book_id` (int), `title` (str), `author` (str), `sales_count` (int)
  - `time_period` (str)
- **Navigation:**
  - Back button: `url_for('dashboard')`
  - View book button: `url_for('book_details', book_id=book_id)`

---

## 3. Data Schemas Specification

### 1. Books Data
- **File Path:** `data/books.txt`
- **Field Order and Names:**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `category` (str)
  6. `price` (float)
  7. `stock` (int)
  8. `description` (str)
- **Description:** Stores details about each book available in the bookstore.
- **Example Rows:**
  - `1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel`
  - `2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind`
  - `3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction`

---

### 2. Categories Data
- **File Path:** `data/categories.txt`
- **Field Order and Names:**
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- **Description:** Stores book categories and their descriptions.
- **Example Rows:**
  - `1|Fiction|Fictional narratives and novels`
  - `2|Non-Fiction|Factual and educational books`
  - `3|Science|Scientific topics and research`

---

### 3. Cart Data
- **File Path:** `data/cart.txt`
- **Field Order and Names:**
  1. `cart_id` (int)
  2. `book_id` (int)
  3. `quantity` (int)
  4. `added_date` (str, date format YYYY-MM-DD)
- **Description:** Stores items currently added to the shopping cart.
- **Example Rows:**
  - `1|1|2|2025-01-15`
  - `2|3|1|2025-01-16`

---

### 4. Orders Data
- **File Path:** `data/orders.txt`
- **Field Order and Names:**
  1. `order_id` (int)
  2. `customer_name` (str)
  3. `order_date` (str, date format YYYY-MM-DD)
  4. `total_amount` (float)
  5. `status` (str)
  6. `shipping_address` (str)
- **Description:** Stores order records including shipping details and status.
- **Example Rows:**
  - `1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001`
  - `2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001`

---

### 5. Order Items Data
- **File Path:** `data/order_items.txt`
- **Field Order and Names:**
  1. `order_item_id` (int)
  2. `order_id` (int)
  3. `book_id` (int)
  4. `quantity` (int)
  5. `price` (float)
- **Description:** Stores each book item associated with an order.
- **Example Rows:**
  - `1|1|1|2|12.99`
  - `2|1|3|1|14.99`
  - `3|2|2|1|16.99`

---

### 6. Reviews Data
- **File Path:** `data/reviews.txt`
- **Field Order and Names:**
  1. `review_id` (int)
  2. `book_id` (int)
  3. `customer_name` (str)
  4. `rating` (int, 1-5)
  5. `review_text` (str)
  6. `review_date` (str, date format YYYY-MM-DD)
- **Description:** Stores customer reviews for books.
- **Example Rows:**
  - `1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12`
  - `2|2|Bob Williams|4|Very informative and well-written.|2025-01-13`
  - `3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15`

---

### 7. Bestsellers Data
- **File Path:** `data/bestsellers.txt`
- **Field Order and Names:**
  1. `book_id` (int)
  2. `sales_count` (int)
  3. `period` (str)
- **Description:** Stores sales count of books for specified time periods, used to rank bestsellers.
- **Example Rows:**
  - `2|150|This Month`
  - `1|120|This Month`
  - `3|95|This Month`
