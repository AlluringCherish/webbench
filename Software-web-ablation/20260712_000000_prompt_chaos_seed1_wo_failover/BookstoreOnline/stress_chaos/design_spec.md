# BookstoreOnline Design Specification Document

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route path**: `/`
- **Function name**: `root_redirect`
- **HTTP method**: GET
- **Behavior**: Redirects to `/dashboard`

### 2. Dashboard Page
- **Route path**: `/dashboard`
- **Function name**: `dashboard`
- **HTTP method**: GET
- **Template rendered**: `dashboard.html`
- **Context variables**:
  - `featured_books` (list of dict): List of featured books with keys: `book_id` (int), `title` (str), `author` (str), `price` (float), `cover_url` (optional str if images included)
  - `bestsellers` (list of dict): List of bestseller books with `book_id` (int), `title` (str), `author` (str), `sales_count` (int)

### 3. Book Catalog Page
- **Route path**: `/catalog`
- **Function name**: `catalog`
- **HTTP methods**: GET
- **Template rendered**: `catalog.html`
- **Context variables**:
  - `books` (list of dict): Each dict includes `book_id` (int), `title` (str), `author` (str), `price` (float)
  - `categories` (list of dict): Each dict with `category_id` (int), `category_name` (str)
  - Query parameters accepted: Optional filters for `search` (str), `category` (str)

### 4. Book Details Page
- **Route path**: `/book/<int:book_id>`
- **Function name**: `book_details`
- **HTTP methods**: GET, POST
- **Template rendered**: `book_details.html`
- **Context variables**:
  - `book` (dict): Keys `book_id` (int), `title` (str), `author` (str), `price` (float), `isbn` (str), `category` (str), `description` (str), `stock` (int)
  - `reviews` (list of dict): Each dict with `review_id` (int), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str)

- **Form submission handling**:
  - POST method to add the book to cart
  - Form includes quantity (default is 1 if not explicit)
  - Adds cart entry in `cart.txt` with appropriate fields

### 5. Shopping Cart Page
- **Route path**: `/cart`
- **Function name**: `cart`
- **HTTP methods**: GET, POST
- **Template rendered**: `cart.html`
- **Context variables**:
  - `cart_items` (list of dict): Each dict has `item_id` (int, cart_id), `book_id` (int), `title` (str), `quantity` (int), `price` (float), `subtotal` (float)
  - `total_amount` (float): Sum of all subtotals

- **Form submission handling POST**:
  - Updates quantities or removes items based on form data
  - For quantity updates, expects fields named `update-quantity-{item_id}` with new values
  - For removal, expects `remove-item-button-{item_id}` triggered

### 6. Checkout Page
- **Route path**: `/checkout`
- **Function name**: `checkout`
- **HTTP methods**: GET, POST
- **Template rendered**: `checkout.html`
- **Context variables**:
  - No specific data needed on GET except possibly cart summary

- **Form submission handling POST**:
  - Receives: `customer_name` (str), `shipping_address` (str), `payment_method` (str)
  - Processes order, writes new entry to `orders.txt` and related items to `order_items.txt`
  - Clears cart on successful order placement

### 7. Order History Page
- **Route path**: `/orders`
- **Function name**: `order_history`
- **HTTP methods**: GET
- **Template rendered**: `orders.html`
- **Context variables**:
  - `orders` (list of dict): Each dict with `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str), `shipping_address` (str)
  - Query parameter for filter: `status` (str) among All, Pending, Shipped, Delivered

### 8. Order Details Page
- **Route path**: `/orders/<int:order_id>`
- **Function name**: `order_details`
- **HTTP methods**: GET
- **Template rendered**: `order_details.html` (not specified in requirements, optional)
- **Context variables**:
  - `order` (dict): Detailed order data
  - `order_items` (list of dict): Books associated with the order

### 9. Reviews Page
- **Route path**: `/reviews`
- **Function name**: `reviews`
- **HTTP methods**: GET
- **Template rendered**: `reviews.html`
- **Context variables**:
  - `reviews` (list of dict): Contains `review_id` (int), `book_title` (str), `rating` (int), `review_text` (str), `review_date` (str)
  - `filter_rating` (str): Filter selected from dropdown

### 10. Write Review Page
- **Route path**: `/write_review`
- **Function name**: `write_review`
- **HTTP methods**: GET, POST
- **Template rendered**: `write_review.html`
- **Context variables**:
  - `purchased_books` (list of dict): Books user can review with `book_id` (int), `title` (str)

- **Form submission handling POST**:
  - Receives: `selected_book_id` (int), `rating` (int), `review_text` (str)
  - Adds new review entry to `reviews.txt`

### 11. Bestsellers Page
- **Route path**: `/bestsellers`
- **Function name**: `bestsellers`
- **HTTP methods**: GET
- **Template rendered**: `bestsellers.html`
- **Context variables**:
  - `bestsellers` (list of dict): Each dict with `rank` (int), `book_id` (int), `title` (str), `author` (str), `sales_count` (int)
  - Query parameter: `time_period` (str) - This Week, This Month, All Time

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page Template
- **File path**: `templates/dashboard.html`
- **Page title**: `Bookstore Dashboard`
- **Main heading (<h1>)**: `Bookstore Dashboard`
- **Element IDs and types**:
  - `dashboard-page` - Div container for dashboard
  - `featured-books` - Div for featured books display
  - `browse-catalog-button` - Button navigating to book catalog
  - `view-cart-button` - Button navigating to shopping cart
  - `bestsellers-button` - Button navigating to bestsellers page
- **Context variables**:
  - `featured_books` (list of dict)
  - `bestsellers` (list of dict)
- **Navigation mappings**:
  - `browse-catalog-button` uses `url_for('catalog')`
  - `view-cart-button` uses `url_for('cart')`
  - `bestsellers-button` uses `url_for('bestsellers')`

### 2. Catalog Page Template
- **File path**: `templates/catalog.html`
- **Page title**: `Book Catalog`
- **Main heading (<h1>)**: `Book Catalog`
- **Element IDs and types**:
  - `catalog-page` - Div container
  - `search-input` - Input text for search filter
  - `category-filter` - Dropdown for category filtering
  - `books-grid` - Div container grid for book cards
  - `view-book-button-{book_id}` - Button on each book card for details
- **Context variables**:
  - `books` (list of dict)
  - `categories` (list of dict)
- **Navigation mappings**:
  - `view-book-button-{book_id}` links to `url_for('book_details', book_id=book_id)`

### 3. Book Details Page Template
- **File path**: `templates/book_details.html`
- **Page title**: `Book Details`
- **Main heading (<h1>)**: `book['title']`
- **Element IDs and types**:
  - `book-details-page` - Div container for page
  - `book-title` - H1 element for title
  - `book-author` - Div displaying author
  - `book-price` - Div for price
  - `add-to-cart-button` - Button to add the book to cart
  - `book-reviews` - Div container showing reviews
- **Context variables**:
  - `book` (dict)
  - `reviews` (list of dict)
- **Form for POST method (add to cart)**:
  - Quantity input field (optional, default 1)
  - Submit button with ID `add-to-cart-button`

### 4. Shopping Cart Page Template
- **File path**: `templates/cart.html`
- **Page title**: `Shopping Cart`
- **Main heading (<h1>)**: `Shopping Cart`
- **Element IDs and types**:
  - `cart-page` - Div container
  - `cart-items-table` - Table listing cart items with columns for title, quantity, price, subtotal
  - `update-quantity-{item_id}` - Number input for updating quantity per item
  - `remove-item-button-{item_id}` - Button to remove item
  - `proceed-checkout-button` - Button to proceed to checkout
  - `total-amount` - Div showing total price
- **Context variables**:
  - `cart_items` (list of dict)
  - `total_amount` (float)
- **Form structure**:
  - POST method form with fields for updating quantities and remove actions
  - Submit buttons with dynamic IDs `remove-item-button-{item_id}`

### 5. Checkout Page Template
- **File path**: `templates/checkout.html`
- **Page title**: `Checkout`
- **Main heading (<h1>)**: `Checkout`
- **Element IDs and types**:
  - `checkout-page` - Div container
  - `customer-name` - Input text for customer name
  - `shipping-address` - Textarea for shipping address
  - `payment-method` - Dropdown for payment method selection
  - `place-order-button` - Button to place order
- **Context variables**: None specific
- **Form structure**:
  - Form POST submission with above inputs

### 6. Order History Page Template
- **File path**: `templates/orders.html`
- **Page title**: `Order History`
- **Main heading (<h1>)**: `Order History`
- **Element IDs and types**:
  - `orders-page` - Div container
  - `orders-table` - Table displaying order entries
  - `view-order-button-{order_id}` - Button to view order details
  - `order-status-filter` - Dropdown for status filter
  - `back-to-dashboard` - Button to navigate to dashboard
- **Context variables**:
  - `orders` (list of dict)
- **Navigation mappings**:
  - `back-to-dashboard` uses `url_for('dashboard')`

### 7. Reviews Page Template
- **File path**: `templates/reviews.html`
- **Page title**: `Customer Reviews`
- **Main heading (<h1>)**: `Customer Reviews`
- **Element IDs and types**:
  - `reviews-page` - Div container
  - `reviews-list` - Div listing reviews
  - `write-review-button` - Button to navigate to write review
  - `filter-by-rating` - Dropdown filter
  - `back-to-dashboard` - Button to navigate back
- **Context variables**:
  - `reviews` (list of dict)
  - `filter_rating` (str)

### 8. Write Review Page Template
- **File path**: `templates/write_review.html`
- **Page title**: `Write a Review`
- **Main heading (<h1>)**: `Write a Review`
- **Element IDs and types**:
  - `write-review-page` - Div container
  - `select-book` - Dropdown to select book
  - `rating-select` - Dropdown to select rating (1-5 stars)
  - `review-text` - Textarea for review text
  - `submit-review-button` - Button to submit review
- **Context variables**:
  - `purchased_books` (list of dict)
- **Form structure**:
  - POST form with fields matching IDs

### 9. Bestsellers Page Template
- **File path**: `templates/bestsellers.html`
- **Page title**: `Bestsellers`
- **Main heading (<h1>)**: `Bestsellers`
- **Element IDs and types**:
  - `bestsellers-page` - Div container
  - `bestsellers-list` - Div listing ranked bestsellers
  - `time-period-filter` - Dropdown for time period
  - `view-book-button-{book_id}` - Button to view details
  - `back-to-dashboard` - Button navigation
- **Context variables**:
  - `bestsellers` (list of dict)
- **Navigation mappings**:
  - `back-to-dashboard` uses `url_for('dashboard')`

---

## Section 3: Data Schemas Specification

### 1. Books Data
- **File path**: `data/books.txt`
- **Format**: Pipe-delimited `|`
- **Fields (in order)**:
  - `book_id` (int)
  - `title` (str)
  - `author` (str)
  - `isbn` (str)
  - `category` (str)
  - `price` (float)
  - `stock` (int)
  - `description` (str)
- **Description**: Stores all book details available in the bookstore.
- **Example rows**:
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

### 2. Categories Data
- **File path**: `data/categories.txt`
- **Format**: Pipe-delimited `|`
- **Fields**:
  - `category_id` (int)
  - `category_name` (str)
  - `description` (str)
- **Description**: Stores book categories.
- **Example rows**:
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

### 3. Cart Data
- **File path**: `data/cart.txt`
- **Format**: Pipe-delimited `|`
- **Fields**:
  - `cart_id` (int)
  - `book_id` (int)
  - `quantity` (int)
  - `added_date` (str, `YYYY-MM-DD`)
- **Description**: Stores current shopping cart items.
- **Example rows**:
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

### 4. Orders Data
- **File path**: `data/orders.txt`
- **Format**: Pipe-delimited `|`
- **Fields**:
  - `order_id` (int)
  - `customer_name` (str)
  - `order_date` (str, `YYYY-MM-DD`)
  - `total_amount` (float)
  - `status` (str) [Pending, Shipped, Delivered]
  - `shipping_address` (str)
- **Description**: Stores all completed orders.
- **Example rows**:
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

### 5. Order Items Data
- **File path**: `data/order_items.txt`
- **Format**: Pipe-delimited `|`
- **Fields**:
  - `order_item_id` (int)
  - `order_id` (int)
  - `book_id` (int)
  - `quantity` (int)
  - `price` (float)
- **Description**: Stores individual book items within an order.
- **Example rows**:
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

### 6. Reviews Data
- **File path**: `data/reviews.txt`
- **Format**: Pipe-delimited `|`
- **Fields**:
  - `review_id` (int)
  - `book_id` (int)
  - `customer_name` (str)
  - `rating` (int, 1-5)
  - `review_text` (str)
  - `review_date` (str, `YYYY-MM-DD`)
- **Description**: Stores customer reviews.
- **Example rows**:
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

### 7. Bestsellers Data
- **File path**: `data/bestsellers.txt`
- **Format**: Pipe-delimited `|`
- **Fields**:
  - `book_id` (int)
  - `sales_count` (int)
  - `period` (str) [e.g., "This Week", "This Month", "All Time"]
- **Description**: Stores bestselling books ranked by sales count and period.
- **Example rows**:
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

This design specification document fully captures all requirements, routes, templates, and data schemas for the BookstoreOnline application as per the user task description. Backend and Frontend developers can utilize this specification independently for implementation.