# BookstoreOnline - Detailed Design Specification

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path**: `/`
- **Function Name**: `root_redirect`
- **HTTP Methods**: GET
- **Template Rendered**: None (Redirect)
- **Behavior**: Redirects immediately to `/dashboard` route.

---

### 2. Dashboard Page
- **Route Path**: `/dashboard`
- **Function Name**: `dashboard_page`
- **HTTP Methods**: GET
- **Template Rendered**: `dashboard.html`
- **Context Variables**:
  - `featured_books` (list of dicts): Each dict with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `price` (float)
  - `bestsellers` (list of dicts): Each dict with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `sales_count` (int)

- **Description**: Displays featured books and bestsellers list. Navigation buttons direct to catalog, cart, and bestsellers pages.

---

### 3. Book Catalog Page
- **Route Path**: `/catalog`
- **Function Name**: `book_catalog_page`
- **HTTP Methods**: GET
- **Template Rendered**: `catalog.html`
- **Context Variables**:
  - `books` (list of dicts): Each dict with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `isbn` (str)
    - `category` (str)
    - `price` (float)
  - `categories` (list of dicts): Each dict with keys:
    - `category_id` (int)
    - `category_name` (str)
  - `search_query` (str): current search input string
  - `selected_category` (str): current category filter

- **Description**: Displays books with search and category filtering controls. Each book card has a button to view detail.

---

### 4. Book Details Page
- **Route Path**: `/book/<int:book_id>`
- **Function Name**: `book_details_page`
- **HTTP Methods**: GET, POST
- **Template Rendered**: `book_details.html`
- **Context Variables**:
  - `book` (dict): keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `isbn` (str)
    - `category` (str)
    - `price` (float)
    - `stock` (int)
    - `description` (str)
  - `reviews` (list of dicts): each with keys:
    - `review_id` (int)
    - `customer_name` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str)

- **Form Submission Handling (POST)**:
  - Form fields: `quantity` (int), to add that amount of book to cart.
  - On submission, updates `cart.txt`: increments quantity if book already in cart or adds new record.
  - Redirects back to same page after action.

---

### 5. Shopping Cart Page
- **Route Path**: `/cart`
- **Function Name**: `shopping_cart_page`
- **HTTP Methods**: GET, POST
- **Template Rendered**: `cart.html`
- **Context Variables**:
  - `cart_items` (list of dicts): each with keys:
    - `cart_id` (int)
    - `book_id` (int)
    - `title` (str)
    - `quantity` (int)
    - `price` (float)
    - `subtotal` (float)
  - `total_amount` (float)

- **Form Submissions Handling (POST)**:
  - Updating quantity: identified by `cart_id` with a new `quantity` value.
  - Removing item: identified by `cart_id`.
  - Cart persists updated in `cart.txt` accordingly.
  - Redirects back to `/cart` after handling.

- **Buttons**:
  - `proceed-checkout-button` navigates to `/checkout`.

---

### 6. Checkout Page
- **Route Path**: `/checkout`
- **Function Name**: `checkout_page`
- **HTTP Methods**: GET, POST
- **Template Rendered**: `checkout.html`
- **Context Variables**:
  - `cart_items` (list of dicts): same as cart page
  - `total_amount` (float)

- **Form Submission Handling (POST)**:
  - Inputs:
    - `customer_name` (str)
    - `shipping_address` (str)
    - `payment_method` (str)
  - On submission:
    - Creates a new order entry in `orders.txt` with unique `order_id`, customer info, total, status (start as "Pending"), and shipping address.
    - Writes individual entries per book item to `order_items.txt` with quantities and prices.
    - Clears `cart.txt` (empties shopping cart).
  - Redirects to `/order_history`.

---

### 7. Order History Page
- **Route Path**: `/order_history`
- **Function Name**: `order_history_page`
- **HTTP Methods**: GET
- **Template Rendered**: `orders.html`
- **Context Variables**:
  - `orders` (list of dicts): each with keys:
    - `order_id` (int)
    - `customer_name` (str)
    - `order_date` (str)
    - `total_amount` (float)
    - `status` (str)
    - `shipping_address` (str)
  - `selected_status` (str): filter on order status, default "All"

- **Functionality**:
  - Filters orders by status via optional query parameter.

- **Buttons**:
  - `view-order-button-{order_id}` navigates to `/order/<order_id>`.
  - `back-to-dashboard` navigates to `/dashboard`.

---

### 8. Order Details Page
- **Route Path**: `/order/<int:order_id>`
- **Function Name**: `order_details_page`
- **HTTP Methods**: GET
- **Template Rendered**: `order_details.html`
- **Context Variables**:
  - `order` (dict): keys:
    - `order_id` (int)
    - `customer_name` (str)
    - `order_date` (str)
    - `total_amount` (float)
    - `status` (str)
    - `shipping_address` (str)
  - `order_items` (list of dicts): each with keys:
    - `order_item_id` (int)
    - `book_id` (int)
    - `title` (str)
    - `quantity` (int)
    - `price` (float)

---

### 9. Reviews Page
- **Route Path**: `/reviews`
- **Function Name**: `reviews_page`
- **HTTP Methods**: GET
- **Template Rendered**: `reviews.html`
- **Context Variables**:
  - `reviews` (list of dicts): each with keys:
    - `review_id` (int)
    - `book_id` (int)
    - `title` (str)
    - `customer_name` (str)
    - `rating` (int)
    - `review_text` (str)
    - `review_date` (str)
  - `filter_rating` (int or None): filter on rating, None means no filter

- **Functionality**:
  - Filters reviews by rating via query parameter.

- **Buttons**:
  - `write-review-button` navigates to `/write_review`.
  - `back-to-dashboard` navigates to `/dashboard`.

---

### 10. Write Review Page
- **Route Path**: `/write_review`
- **Function Name**: `write_review_page`
- **HTTP Methods**: GET, POST
- **Template Rendered**: `write_review.html`
- **Context Variables**:
  - `purchased_books` (list of dicts): each dict with keys:
    - `book_id` (int)
    - `title` (str)

- **Form Submission Handling (POST)**:
  - Inputs:
    - `book_id` (int)
    - `rating` (int)
    - `review_text` (str)
    - `customer_name` (str, optional or prompted)
  - On submission, appends new review line to `reviews.txt` with unique `review_id` and current date.
  - Redirects to `/reviews`.

---

### 11. Bestsellers Page
- **Route Path**: `/bestsellers`
- **Function Name**: `bestsellers_page`
- **HTTP Methods**: GET
- **Template Rendered**: `bestsellers.html`
- **Context Variables**:
  - `bestsellers` (list of dicts): each with keys:
    - `book_id` (int)
    - `title` (str)
    - `author` (str)
    - `sales_count` (int)
    - `period` (str)
  - `time_period` (str): current filter ("This Week", "This Month", "All Time")

- **Functionality**: Filters bestsellers list by time period.

- **Buttons**:
  - `view-book-button-{book_id}` navigates to `/book/<book_id>`.
  - `back-to-dashboard` navigates to `/dashboard`.

---


## Section 2: HTML Templates Specification

### 1. Dashboard Page Template
- **File Path**: `templates/dashboard.html`
- **Page Title**: `Bookstore Dashboard`
- **Main Heading (h1)**: `Bookstore Dashboard`
- **Element IDs:**
  - `dashboard-page` (div): main container
  - `featured-books` (div): displays featured books
  - `browse-catalog-button` (button): navigates to `/catalog`
  - `view-cart-button` (button): navigates to `/cart`
  - `bestsellers-button` (button): navigates to `/bestsellers`

- **Context Variables**:
  - `featured_books` (list of dicts)
  - `bestsellers` (list of dicts)

- **Navigation Mappings:**
  - `browse-catalog-button` &rarr; `url_for('book_catalog_page')`
  - `view-cart-button` &rarr; `url_for('shopping_cart_page')`
  - `bestsellers-button` &rarr; `url_for('bestsellers_page')`

---

### 2. Book Catalog Page Template
- **File Path**: `templates/catalog.html`
- **Page Title**: `Book Catalog`
- **Main Heading (h1)**: `Book Catalog`
- **Element IDs:**
  - `catalog-page` (div): container
  - `search-input` (input): for text search of books by title, author, or ISBN
  - `category-filter` (select): dropdown for category filter
  - `books-grid` (div): grid container for book cards
  - `view-book-button-{book_id}` (button): button for each book to view details

- **Context Variables**:
  - `books` (list of dicts)
  - `categories` (list of dicts)
  - `search_query` (str)
  - `selected_category` (str)

- **Navigation Mappings:**
  - Each `view-book-button-{book_id}` &rarr; `url_for('book_details_page', book_id=book_id)`

- **Form Structure:**
  - Typically a GET form containing `search-input` and `category-filter` to reload page with query params.

---

### 3. Book Details Page Template
- **File Path**: `templates/book_details.html`
- **Page Title**: `Book Details`
- **Main Heading (h1)**: `Book Details`
- **Element IDs:**
  - `book-details-page` (div): container
  - `book-title` (h1): displays book title
  - `book-author` (div): displays author
  - `book-price` (div): displays price
  - `add-to-cart-button` (button): submits add-to-cart form
  - `book-reviews` (div): displays reviews for the book

- **Context Variables:**
  - `book` (dict)
  - `reviews` (list of dicts)

- **Form Structure:**
  - POST form contains input for quantity and submit button with `add-to-cart-button` ID.

---

### 4. Shopping Cart Page Template
- **File Path**: `templates/cart.html`
- **Page Title**: `Shopping Cart`
- **Main Heading (h1)**: `Shopping Cart`
- **Element IDs:**
  - `cart-page` (div): container
  - `cart-items-table` (table): lists cart items with columns for title, quantity, price, subtotal
  - `update-quantity-{item_id}` (input, number): for each cart item quantity
  - `remove-item-button-{item_id}` (button): remove button for each cart item
  - `proceed-checkout-button` (button): navigates to `/checkout`
  - `total-amount` (div): displays total price

- **Context Variables:**
  - `cart_items` (list of dicts)
  - `total_amount` (float)

- **Navigation Mappings:**
  - `proceed-checkout-button` &rarr; `url_for('checkout_page')`

- **Form Structures:**
  - Forms to update quantity and remove items use POST method referencing `cart_id`.

---

### 5. Checkout Page Template
- **File Path**: `templates/checkout.html`
- **Page Title**: `Checkout`
- **Main Heading (h1)**: `Checkout`
- **Element IDs:**
  - `checkout-page` (div): container
  - `customer-name` (input): for inputting customer name
  - `shipping-address` (textarea): for shipping address
  - `payment-method` (select): payment method selection dropdown
  - `place-order-button` (button): submits checkout form

- **Context Variables:**
  - `cart_items` (list of dicts)
  - `total_amount` (float)

- **Form Structure:**
  - POST form containing inputs: `customer_name`, `shipping_address`, `payment_method`.

---

### 6. Order History Page Template
- **File Path**: `templates/orders.html`
- **Page Title**: `Order History`
- **Main Heading (h1)**: `Order History`
- **Element IDs:**
  - `orders-page` (div): container
  - `orders-table` (table): displays orders with order ID, date, amount, status
  - `view-order-button-{order_id}` (button): navigates to order detail
  - `order-status-filter` (select): dropdown to filter orders by status
  - `back-to-dashboard` (button): navigates to `/dashboard`

- **Context Variables:**
  - `orders` (list of dicts)
  - `selected_status` (str)

- **Navigation Mappings:**
  - `back-to-dashboard` &rarr; `url_for('dashboard_page')`
  - `view-order-button-{order_id}` &rarr; `url_for('order_details_page', order_id=order_id)`

---

### 7. Reviews Page Template
- **File Path**: `templates/reviews.html`
- **Page Title**: `Customer Reviews`
- **Main Heading (h1)**: `Customer Reviews`
- **Element IDs:**
  - `reviews-page` (div): container
  - `reviews-list` (div): displays all reviews
  - `write-review-button` (button): navigates to write review
  - `filter-by-rating` (select): dropdown to filter reviews by rating
  - `back-to-dashboard` (button): navigates to `/dashboard`

- **Context Variables:**
  - `reviews` (list of dicts)
  - `filter_rating` (int or None)

- **Navigation Mappings:**
  - `write-review-button` &rarr; `url_for('write_review_page')`
  - `back-to-dashboard` &rarr; `url_for('dashboard_page')`

---

### 8. Write Review Page Template
- **File Path**: `templates/write_review.html`
- **Page Title**: `Write a Review`
- **Main Heading (h1)**: `Write a Review`
- **Element IDs:**
  - `write-review-page` (div): container
  - `select-book` (select): dropdown to select book
  - `rating-select` (select): dropdown to select 1-5 star rating
  - `review-text` (textarea): text area for review content
  - `submit-review-button` (button): submits review form

- **Context Variables:**
  - `purchased_books` (list of dicts)

- **Form Structure:** POST form with inputs `book_id`, `rating`, `review_text`.

---

### 9. Bestsellers Page Template
- **File Path**: `templates/bestsellers.html`
- **Page Title**: `Bestsellers`
- **Main Heading (h1)**: `Bestsellers`
- **Element IDs:**
  - `bestsellers-page` (div): container
  - `bestsellers-list` (div): list of bestsellers ranked
  - `time-period-filter` (select): dropdown to filter by time period
  - `view-book-button-{book_id}` (button): view button for each book
  - `back-to-dashboard` (button): navigates to `/dashboard`

- **Context Variables:**
  - `bestsellers` (list of dicts)
  - `time_period` (str)

- **Navigation Mappings:**
  - `view-book-button-{book_id}` &rarr; `url_for('book_details_page', book_id=book_id)`
  - `back-to-dashboard` &rarr; `url_for('dashboard_page')`

- **Filter Form:** GET with `time-period-filter` dropdown to filter bestsellers by period.

---

## Section 3: Data Schemas Specification

### 1. Books Data
- **File Path**: `data/books.txt`
- **Format**: Pipe-delimited (`|`), no header
- **Fields (in order):**
  1. `book_id` (int) - Unique book identifier
  2. `title` (str) - Book title
  3. `author` (str) - Author name
  4. `isbn` (str) - International Standard Book Number
  5. `category` (str) - Book category name
  6. `price` (float) - Price in USD
  7. `stock` (int) - Quantity available
  8. `description` (str) - Book description
- **Examples:**
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

---

### 2. Categories Data
- **File Path**: `data/categories.txt`
- **Format**: Pipe-delimited (`|`), no header
- **Fields (in order):**
  1. `category_id` (int) - Unique category ID
  2. `category_name` (str) - Category name
  3. `description` (str) - Description of category
- **Examples:**
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

---

### 3. Cart Data
- **File Path**: `data/cart.txt`
- **Format**: Pipe-delimited (`|`), no header
- **Fields (in order):**
  1. `cart_id` (int) - Unique cart item ID
  2. `book_id` (int) - Book reference
  3. `quantity` (int) - Quantity added
  4. `added_date` (str) - Date added (YYYY-MM-DD)
- **Examples:**
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

---

### 4. Orders Data
- **File Path**: `data/orders.txt`
- **Format**: Pipe-delimited (`|`), no header
- **Fields (in order):**
  1. `order_id` (int) - Unique order ID
  2. `customer_name` (str) - Customer full name
  3. `order_date` (str) - Date of order (YYYY-MM-DD)
  4. `total_amount` (float) - Total order price
  5. `status` (str) - Current status (Pending, Shipped, Delivered)
  6. `shipping_address` (str) - Shipping address
- **Examples:**
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

---

### 5. Order Items Data
- **File Path**: `data/order_items.txt`
- **Format**: Pipe-delimited (`|`), no header
- **Fields (in order):**
  1. `order_item_id` (int) - Unique order item ID
  2. `order_id` (int) - Reference order
  3. `book_id` (int) - Book reference
  4. `quantity` (int) - Quantity ordered
  5. `price` (float) - Price at order time
- **Examples:**
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

---

### 6. Reviews Data
- **File Path**: `data/reviews.txt`
- **Format**: Pipe-delimited (`|`), no header
- **Fields (in order):**
  1. `review_id` (int) - Unique review ID
  2. `book_id` (int) - Book reference
  3. `customer_name` (str) - Reviewer name
  4. `rating` (int) - Rating from 1 to 5
  5. `review_text` (str) - Review content
  6. `review_date` (str) - Date of review (YYYY-MM-DD)
- **Examples:**
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

---

### 7. Bestsellers Data
- **File Path**: `data/bestsellers.txt`
- **Format**: Pipe-delimited (`|`), no header
- **Fields (in order):**
  1. `book_id` (int) - Book reference
  2. `sales_count` (int) - Number of sales
  3. `period` (str) - Time frame (e.g., This Week, This Month, All Time)
- **Examples:**
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

*End of Design Specification Document*