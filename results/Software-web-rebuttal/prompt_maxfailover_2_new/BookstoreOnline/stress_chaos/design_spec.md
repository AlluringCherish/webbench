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
  - `books` (list of dict): List of books with keys: `book_id` (int), `title` (str), `author` (str), `price` (float), `category` (str), `isbn` (str)

### 4. Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** `book_details_page`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `book_details.html`
- **Context Variables:**
  - `book` (dict): Book details with keys: `book_id` (int), `title` (str), `author` (str), `price` (float), `description` (str), `isbn` (str), `category` (str), `stock` (int)
  - `reviews` (list of dict): List of reviews for the book with keys: `review_id` (int), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str)

- **Form Handling:** POST method to add book to cart.
  - Form fields: quantity (int)
  - On submission, add book with specified quantity to `cart.txt` and redirect to `/cart`.

### 5. Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** `cart_page`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `cart.html`
- **Context Variables:**
  - `cart_items` (list of dict): List of cart items with keys: `cart_id` (int), `book_id` (int), `title` (str), `quantity` (int), `price` (float), `subtotal` (float)
  - `total_amount` (float): Total sum of cart item subtotals

- **Form Handling (POST):**
  - Update quantity or remove item actions.
  - Input fields: `update_quantity-{cart_id}` (int), `remove_item-{cart_id}` (boolean via button press)
  - On quantity update, modify cart.txt for given cart_id.
  - On remove button click, delete cart item.
  - After processing, reload `/cart` GET.

### 6. Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** `checkout_page`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `checkout.html`
- **Context Variables:**
  - `cart_items` (list of dict): Same as in cart page.
  - `total_amount` (float): Total sum.

- **Form Handling:** POST method to place order.
  - Form fields: `customer_name` (str), `shipping_address` (str), `payment_method` (str: "Credit Card", "PayPal", "Bank Transfer")
  - On submission:
    - Create entry in orders.txt with new order_id, customer_name, order_date (current date), total_amount, status "Pending", shipping_address.
    - Create entries in order_items.txt for each cart item.
    - Clear cart.txt.
    - Redirect to `/order_history`.

### 7. Order History Page
- **Route Path:** `/order_history`
- **Function Name:** `order_history_page`
- **HTTP Methods:** GET
- **Template Rendered:** `order_history.html`
- **Context Variables:**
  - `orders` (list of dict): List of orders with keys: `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str), `shipping_address` (str)

- **Query Parameters:** Optional `status` to filter orders by status.

### 8. Order Details Page
- **Route Path:** `/order/<int:order_id>`
- **Function Name:** `order_details_page`
- **HTTP Methods:** GET
- **Template Rendered:** `order_details.html`
- **Context Variables:**
  - `order` (dict): Order details as in orders list.
  - `order_items` (list of dict): Items with keys: `order_item_id` (int), `book_id` (int), `title` (str), `quantity` (int), `price` (float)

### 9. Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** `reviews_page`
- **HTTP Methods:** GET
- **Template Rendered:** `reviews.html`
- **Context Variables:**
  - `reviews` (list of dict): List of reviews with keys: `review_id` (int), `book_id` (int), `title` (str), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str)

- **Query Parameters:** Optional `rating` filter.

### 10. Write Review Page
- **Route Path:** `/write_review`
- **Function Name:** `write_review_page`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `write_review.html`
- **Context Variables:**
  - `books` (list of dict): List of books user can write review for with keys: `book_id` (int), `title` (str)

- **Form Handling:** POST method to submit review.
  - Form fields: `book_id` (int), `rating` (int), `review_text` (str), `customer_name` (str - from input or assumed no auth so input field is needed)
  - On submission, append review with new review_id and current date to reviews.txt.
  - Redirect to `/reviews`.

### 11. Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** `bestsellers_page`
- **HTTP Methods:** GET
- **Template Rendered:** `bestsellers.html`
- **Context Variables:**
  - `bestsellers` (list of dict): List with keys: `book_id` (int), `title` (str), `author` (str), `sales_count` (int), `period` (str)

- **Query Parameters:** Optional `period` filter (e.g., "This Week", "This Month", "All Time").


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
  - `featured_books` (list of dict): Each dict has `book_id`, `title`, `author`, `price`
  - `bestsellers` (list of dict): Each dict with `book_id`, `title`, `author`, `sales_count`
- **Navigation mappings:**
  - `browse-catalog-button`: link to `url_for('catalog_page')`
  - `view-cart-button`: link to `url_for('cart_page')`
  - `bestsellers-button`: link to `url_for('bestsellers_page')`

### 2. Book Catalog Page Template
- **File Path:** `templates/catalog.html`
- **Page Title:** `Book Catalog`
- **Main Heading `<h1>`:** `Book Catalog`
- **Element IDs:**
  - `catalog-page` (Div) - main container
  - `search-input` (Input) - for searching by title, author or isbn
  - `category-filter` (Dropdown) - filter by category
  - `books-grid` (Div) - grid of book cards
  - `view-book-button-{book_id}` (Button) - to view specific book details
- **Context Variables:**
  - `categories` (list of dict): Each with `category_id`, `category_name`
  - `books` (list of dict): Each with `book_id`, `title`, `author`, `price`, `category`, `isbn`
- **Navigation mappings:**
  - On clicking `view-book-button-{book_id}`, link to `url_for('book_details_page', book_id=book_id)`

### 3. Book Details Page Template
- **File Path:** `templates/book_details.html`
- **Page Title:** `Book Details`
- **Main Heading `<h1>`:** element with ID `book-title` showing book title
- **Element IDs:**
  - `book-details-page` (Div) - main container
  - `book-title` (H1) - book title
  - `book-author` (Div) - author name
  - `book-price` (Div) - price
  - `add-to-cart-button` (Button) - adds book to cart
  - `book-reviews` (Div) - contains customer reviews
- **Context Variables:**
  - `book` (dict): keys as per Section 1
  - `reviews` (list of dict): each with `review_id`, `customer_name`, `rating`, `review_text`, `review_date`
- **Form structure for adding to cart:**
  - Form wraps `add-to-cart-button`
  - Input field (number) for quantity (name="quantity")
  - POST to same route `/book/<book_id>`

### 4. Shopping Cart Page Template
- **File Path:** `templates/cart.html`
- **Page Title:** `Shopping Cart`
- **Main Heading `<h1>`:** `Shopping Cart`
- **Element IDs:**
  - `cart-page` (Div) - main container
  - `cart-items-table` (Table) - display cart items
  - `update-quantity-{cart_id}` (Input number) - change quantity for each item
  - `remove-item-button-{cart_id}` (Button) - remove item button
  - `proceed-checkout-button` (Button) - navigates to `/checkout`
  - `total-amount` (Div) - displays total amount
- **Context Variables:**
  - `cart_items` (list of dict): keys `cart_id`, `book_id`, `title`, `quantity`, `price`, `subtotal`
  - `total_amount` (float)
- **Form structure:**
  - For updates/removals, form submit POST to `/cart`
  - Each quantity input named `update_quantity-{cart_id}`
  - Each remove button named `remove_item-{cart_id}`

### 5. Checkout Page Template
- **File Path:** `templates/checkout.html`
- **Page Title:** `Checkout`
- **Main Heading `<h1>`:** `Checkout`
- **Element IDs:**
  - `checkout-page` (Div) - main container
  - `customer-name` (Input text) - customer name input
  - `shipping-address` (Textarea) - shipping address input
  - `payment-method` (Dropdown) - payment method input
  - `place-order-button` (Button) - submit button
- **Context Variables:**
  - `cart_items` (list of dict): same as cart page
  - `total_amount` (float)
- **Form structure:**
  - Form POST to `/checkout`
  - Inputs: customer-name (text), shipping-address (textarea), payment-method (dropdown)

### 6. Order History Page Template
- **File Path:** `templates/order_history.html`
- **Page Title:** `Order History`
- **Main Heading `<h1>`:** `Order History`
- **Element IDs:**
  - `orders-page` (Div) - main container
  - `orders-table` (Table) - lists orders
  - `view-order-button-{order_id}` (Button) - view order details
  - `order-status-filter` (Dropdown) - filter orders by status
  - `back-to-dashboard` (Button) - navigate back to `/dashboard`
- **Context Variables:**
  - `orders` (list of dict): keys as Section 1
- **Navigation mappings:**
  - `view-order-button-{order_id}` links to `url_for('order_details_page', order_id=order_id)`
  - `back-to-dashboard` links to `url_for('dashboard_page')`

### 7. Order Details Page Template
- **File Path:** `templates/order_details.html`
- **Page Title:** `Order Details`
- **Main Heading `<h1>`:** `Order Details (Order #<order_id>)`
- **Element IDs:**
  - `order-details-page` (Div) - main container
  - No other specific IDs required by specification
- **Context Variables:**
  - `order` (dict): detailed order data
  - `order_items` (list of dict): items in the order with book titles

### 8. Reviews Page Template
- **File Path:** `templates/reviews.html`
- **Page Title:** `Customer Reviews`
- **Main Heading `<h1>`:** `Customer Reviews`
- **Element IDs:**
  - `reviews-page` (Div) - main container
  - `reviews-list` (Div) - list reviews
  - `write-review-button` (Button) - navigate to `/write_review`
  - `filter-by-rating` (Dropdown) - filter reviews by star rating
  - `back-to-dashboard` (Button) - navigate to `/dashboard`
- **Context Variables:**
  - `reviews` (list of dict): keys as Section 1
- **Navigation mappings:**
  - `write-review-button`: links to `url_for('write_review_page')`
  - `back-to-dashboard`: links to `url_for('dashboard_page')`

### 9. Write Review Page Template
- **File Path:** `templates/write_review.html`
- **Page Title:** `Write a Review`
- **Main Heading `<h1>`:** `Write a Review`
- **Element IDs:**
  - `write-review-page` (Div) - main container
  - `select-book` (Dropdown) - select book to review
  - `rating-select` (Dropdown) - select rating 1-5
  - `review-text` (Textarea) - write review text
  - `submit-review-button` (Button) - submit form
- **Context Variables:**
  - `books` (list of dict): keys `book_id`, `title`
- **Form structure:**
  - Form POST to `/write_review`
  - Inputs: select-book (book_id), rating-select (rating), review-text (text), customer-name (input text) [needed but not specified in UI elements; must be included for data completeness]

### 10. Bestsellers Page Template
- **File Path:** `templates/bestsellers.html`
- **Page Title:** `Bestsellers`
- **Main Heading `<h1>`:** `Bestsellers`
- **Element IDs:**
  - `bestsellers-page` (Div) - main container
  - `bestsellers-list` (Div) - ranked bestseller books list
  - `time-period-filter` (Dropdown) - filter period
  - `view-book-button-{book_id}` (Button) - view book details
  - `back-to-dashboard` (Button) - navigate to `/dashboard`
- **Context Variables:**
  - `bestsellers` (list of dict): keys as Section 1
- **Navigation mappings:**
  - `view-book-button-{book_id}` links to `url_for('book_details_page', book_id=book_id)`
  - `back-to-dashboard` links to `url_for('dashboard_page')`

---

## Section 3: Data Schemas Specification

### 1. Books Data
- **File Path:** `data/books.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields Order:**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `category` (str)
  6. `price` (float)
  7. `stock` (int)
  8. `description` (str)
- **Description:** Stores all book details including inventory stock and description.
- **Example Rows:**
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

### 2. Categories Data
- **File Path:** `data/categories.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields Order:**
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- **Description:** Stores categories available for filtering books.
- **Example Rows:**
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

### 3. Cart Data
- **File Path:** `data/cart.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields Order:**
  1. `cart_id` (int)
  2. `book_id` (int)
  3. `quantity` (int)
  4. `added_date` (str, format `YYYY-MM-DD`)
- **Description:** Stores shopping cart items with quantity and date added.
- **Example Rows:**
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

### 4. Orders Data
- **File Path:** `data/orders.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields Order:**
  1. `order_id` (int)
  2. `customer_name` (str)
  3. `order_date` (str, format `YYYY-MM-DD`)
  4. `total_amount` (float)
  5. `status` (str) - e.g., Pending, Shipped, Delivered
  6. `shipping_address` (str)
- **Description:** Stores all orders made by customers.
- **Example Rows:**
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

### 5. Order Items Data
- **File Path:** `data/order_items.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields Order:**
  1. `order_item_id` (int)
  2. `order_id` (int)
  3. `book_id` (int)
  4. `quantity` (int)
  5. `price` (float)
- **Description:** Stores items included in each order.
- **Example Rows:**
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

### 6. Reviews Data
- **File Path:** `data/reviews.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields Order:**
  1. `review_id` (int)
  2. `book_id` (int)
  3. `customer_name` (str)
  4. `rating` (int, 1-5)
  5. `review_text` (str)
  6. `review_date` (str, format `YYYY-MM-DD`)
- **Description:** Stores customer reviews for books.
- **Example Rows:**
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

### 7. Bestsellers Data
- **File Path:** `data/bestsellers.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields Order:**
  1. `book_id` (int)
  2. `sales_count` (int)
  3. `period` (str) - e.g., "This Week", "This Month", "All Time"
- **Description:** Stores sales count of top selling books filtered by time period.
- **Example Rows:**
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

This detailed design specification ensures clear, unambiguous implementation for both frontend and backend developers of the BookstoreOnline application.

