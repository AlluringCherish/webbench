# BookstoreOnline - Design Specification Document

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Method(s):** GET
- **Template Rendered:** None (Redirect)
- **Description:** Redirects to `/dashboard` (Dashboard page).

---

### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** `dashboard`
- **HTTP Method(s):** GET
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `featured_books` (list of dict): Each dict contains book data (keys: `book_id`(int), `title`(str), `author`(str), `price`(float))
  - `bestsellers` (list of dict): Each dict contains bestseller book data (keys: `book_id`(int), `title`(str), `author`(str), `sales_count`(int))

---

### 3. Book Catalog Page
- **Route Path:** `/catalog`
- **Function Name:** `catalog`
- **HTTP Method(s):** GET
- **Template Rendered:** `catalog.html`
- **Context Variables:**
  - `books` (list of dict): All book data (keys: `book_id`(int), `title`(str), `author`(str), `price`(float), `category`(str))
  - `categories` (list of dict): All categories (keys: `category_id`(int), `category_name`(str))
  - `search_query` (str): Current search string or empty
  - `selected_category_id` (int or None): Currently selected category filter or None

---

### 4. Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** `book_details`
- **HTTP Method(s):** GET, POST
- **Template Rendered:** `book_details.html`
- **Context Variables (GET):**
  - `book` (dict): Book details (keys: `book_id`(int), `title`(str), `author`(str), `price`(float), `description`(str), `stock`(int))
  - `reviews` (list of dict): Reviews for this book (keys: `review_id`(int), `customer_name`(str), `rating`(int), `review_text`(str), `review_date`(str))
- **Form Submission (POST):**
  - Action: Add the book to shopping cart with quantity 1
  - Processing: Upon POST submission, the book is added to cart.txt (or quantity updated if already in cart)
  - Redirects back to `/cart`

---

### 5. Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** `cart_page`
- **HTTP Method(s):** GET, POST
- **Template Rendered:** `cart.html`
- **Context Variables (GET):**
  - `cart_items` (list of dict): Each item contains (keys: `cart_id`(int), `book_id`(int), `title`(str), `quantity`(int), `price`(float), `subtotal`(float))
  - `total_amount` (float): Total amount of all cart items
- **Form Submission (POST):**
  - Possible form types:
    - Update quantity of a cart item using inputs named `update-quantity-{cart_id}`
    - Remove an item using buttons named `remove-item-{cart_id}`
  - Processing: Updates `cart.txt` accordingly
  - Redirects back to `/cart`
- **Proceed to Checkout:**
  - POST or GET to route `/checkout` (usually a button link triggering GET or POST form)

---

### 6. Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** `checkout`
- **HTTP Method(s):** GET, POST
- **Template Rendered:** `checkout.html`
- **Context Variables (GET):** None for initial display (form fields empty)
- **Form Submission (POST):**
  - Form fields: `customer_name` (str), `shipping_address` (str), `payment_method` (str)
  - Processing:
    - Creates new order record in `orders.txt` with status "Pending"
    - Generates new order items in `order_items.txt` from current cart
    - Clears the cart
  - Redirects to `/order_history` (Order History page)

---

### 7. Order History Page
- **Route Path:** `/order_history`
- **Function Name:** `order_history`
- **HTTP Method(s):** GET
- **Template Rendered:** `order_history.html`
- **Context Variables:**
  - `orders` (list of dict): List of orders with keys: `order_id`(int), `customer_name`(str), `order_date`(str), `total_amount`(float), `status`(str), `shipping_address`(str)
  - `filter_status` (str): Current filter status value

- **Filtering:**
  - Implement filter by `status` query parameter (All, Pending, Shipped, Delivered)

---

### 8. Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** `reviews_page`
- **HTTP Method(s):** GET
- **Template Rendered:** `reviews.html`
- **Context Variables:**
  - `reviews` (list of dict): Each review with keys: `review_id`(int), `book_title`(str), `rating`(int), `review_text`(str), `customer_name`(str), `review_date`(str)
  - `filter_rating` (str): Current rating filter; values like "All", "5", "4", etc.

---

### 9. Write Review Page
- **Route Path:** `/write_review`
- **Function Name:** `write_review`
- **HTTP Method(s):** GET, POST
- **Template Rendered:** `write_review.html`
- **Context Variables (GET):**
  - `purchased_books` (list of dict): Books the user can review (keys: `book_id`(int), `title`(str))
- **Form Submission (POST):**
  - Form fields: `book_id` (int), `rating` (int 1-5), `review_text` (str)
  - Processing:
    - Append review record to `reviews.txt` with new review_id
  - Redirect back to `/reviews`

---

### 10. Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** `bestsellers_page`
- **HTTP Method(s):** GET
- **Template Rendered:** `bestsellers.html`
- **Context Variables:**
  - `bestsellers` (list of dict): Books with keys: `book_id`(int), `title`(str), `author`(str), `sales_count`(int), `period`(str)
  - `time_period` (str): Current filter time period ("This Week", "This Month", "All Time")

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page (`templates/dashboard.html`)
- **Page Title:** "Bookstore Dashboard"
- **Main Heading (`<h1>`):** "Bookstore Dashboard"
- **Element IDs:**
  - `dashboard-page` (Div container for the entire dashboard page)
  - `featured-books` (Div showing featured book recommendations)
  - `browse-catalog-button` (Button navigates to `/catalog`)
  - `view-cart-button` (Button navigates to `/cart`)
  - `bestsellers-button` (Button navigates to `/bestsellers`)
- **Context Variables:**
  - `featured_books` (list of dict)
  - `bestsellers` (list of dict)
- **Navigation Mappings:**
  - `browse-catalog-button` calls `url_for('catalog')`
  - `view-cart-button` calls `url_for('cart_page')`
  - `bestsellers-button` calls `url_for('bestsellers_page')`

---

### 2. Book Catalog Page (`templates/catalog.html`)
- **Page Title:** "Book Catalog"
- **Main Heading (`<h1>`):** "Book Catalog"
- **Element IDs:**
  - `catalog-page` (Div container)
  - `search-input` (Input text field for search)
  - `category-filter` (Dropdown for categories)
  - `books-grid` (Div grid to display book cards)
  - `view-book-button-{book_id}` (Button for each book to go to details page)
- **Context Variables:**
  - `books` (list)
  - `categories` (list)
  - `search_query` (str)
  - `selected_category_id` (int or None)
- **Navigation Mappings:**
  - Each `view-book-button-{book_id}` navigates to `url_for('book_details', book_id=book_id)`

---

### 3. Book Details Page (`templates/book_details.html`)
- **Page Title:** "Book Details"
- **Main Heading (`<h1>`):** Contains book title, ID `book-title`
- **Element IDs:**
  - `book-details-page` (Div container)
  - `book-title` (H1 for title)
  - `book-author` (Div for author)
  - `book-price` (Div for price)
  - `add-to-cart-button` (Button submits POST to add book to cart)
  - `book-reviews` (Div contains customer reviews)
- **Context Variables:**
  - `book` (dict)
  - `reviews` (list)
- **Form Structure:**
  - POST form enclosing the `add-to-cart-button`, sending POST to `/book/<book_id>` to add item

---

### 4. Shopping Cart Page (`templates/cart.html`)
- **Page Title:** "Shopping Cart"
- **Main Heading (`<h1>`):** "Shopping Cart"
- **Element IDs:**
  - `cart-page` (Div container)
  - `cart-items-table` (Table for cart items)
  - `update-quantity-{cart_id}` (Number input for quantity update per item)
  - `remove-item-button-{cart_id}` (Button to remove item)
  - `proceed-checkout-button` (Button navigates to `/checkout`)
  - `total-amount` (Div shows total amount)
- **Context Variables:**
  - `cart_items` (list)
  - `total_amount` (float)
- **Form Structure:**
  - POST form wraps quantity inputs and remove buttons
  - Form submits to `/cart` to update quantities or remove items
  - `proceed-checkout-button` links to `url_for('checkout')`

---

### 5. Checkout Page (`templates/checkout.html`)
- **Page Title:** "Checkout"
- **Main Heading (`<h1>`):** "Checkout"
- **Element IDs:**
  - `checkout-page` (Div container)
  - `customer-name` (Input for customer name)
  - `shipping-address` (Textarea for address)
  - `payment-method` (Dropdown with options: Credit Card, PayPal, Bank Transfer)
  - `place-order-button` (Button submits order)
- **Context Variables:** None (empty form)
- **Form Structure:**
  - POST form submits to `/checkout`
  - Fields: `customer_name`, `shipping_address`, `payment_method`

---

### 6. Order History Page (`templates/order_history.html`)
- **Page Title:** "Order History"
- **Main Heading (`<h1>`):** "Order History"
- **Element IDs:**
  - `orders-page` (Div container)
  - `orders-table` (Table for listing orders)
  - `view-order-button-{order_id}` (Button to view details)
  - `order-status-filter` (Dropdown for order status: All, Pending, Shipped, Delivered)
  - `back-to-dashboard` (Button navigates to `/dashboard`)
- **Context Variables:**
  - `orders` (list)
  - `filter_status` (str)
- **Navigation Mappings:**
  - `view-order-button-{order_id}` links to detailed order if implemented, else placeholder
  - `back-to-dashboard` links to `url_for('dashboard')`

---

### 7. Reviews Page (`templates/reviews.html`)
- **Page Title:** "Customer Reviews"
- **Main Heading (`<h1>`):** "Customer Reviews"
- **Element IDs:**
  - `reviews-page` (Div container)
  - `reviews-list` (Div listing reviews)
  - `write-review-button` (Button navigates to `/write_review`)
  - `filter-by-rating` (Dropdown filter: All, 5 stars, 4 stars, etc.)
  - `back-to-dashboard` (Button navigates to `/dashboard`)
- **Context Variables:**
  - `reviews` (list)
  - `filter_rating` (str)
- **Navigation Mappings:**
  - `write-review-button` links to `url_for('write_review')`
  - `back-to-dashboard` links to `url_for('dashboard')`

---

### 8. Write Review Page (`templates/write_review.html`)
- **Page Title:** "Write a Review"
- **Main Heading (`<h1>`):** "Write a Review"
- **Element IDs:**
  - `write-review-page` (Div container)
  - `select-book` (Dropdown to select a book to review)
  - `rating-select` (Dropdown for rating 1 to 5 stars)
  - `review-text` (Textarea for review text)
  - `submit-review-button` (Button submits review)
- **Context Variables:**
  - `purchased_books` (list)
- **Form Structure:**
  - POST form submits to `/write_review` with fields: `book_id`, `rating`, `review_text`

---

### 9. Bestsellers Page (`templates/bestsellers.html`)
- **Page Title:** "Bestsellers"
- **Main Heading (`<h1>`):** "Bestsellers"
- **Element IDs:**
  - `bestsellers-page` (Div container)
  - `bestsellers-list` (Div for ranked bestseller list)
  - `time-period-filter` (Dropdown with options: This Week, This Month, All Time)
  - `view-book-button-{book_id}` (Button per bestseller to view book details)
  - `back-to-dashboard` (Button navigates to `/dashboard`)
- **Context Variables:**
  - `bestsellers` (list)
  - `time_period` (str)
- **Navigation Mappings:**
  - Each `view-book-button-{book_id}` links to `url_for('book_details', book_id=book_id)`
  - `back-to-dashboard` links to `url_for('dashboard')`

---

## Section 3: Data Schemas Specification

### 1. books.txt
- **File Path:** `data/books.txt`
- **Format:** Pipe-delimited (`|`), no headers
- **Fields (in order):**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `category` (str)
  6. `price` (float)
  7. `stock` (int)
  8. `description` (str)
- **Description:** Stores all books details including stock and description.
- **Example Rows:**
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

---

### 2. categories.txt
- **File Path:** `data/categories.txt`
- **Format:** Pipe-delimited (`|`), no headers
- **Fields (in order):**
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- **Description:** Stores book categories and their descriptions.
- **Example Rows:**
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

---

### 3. cart.txt
- **File Path:** `data/cart.txt`
- **Format:** Pipe-delimited (`|`), no headers
- **Fields (in order):**
  1. `cart_id` (int)
  2. `book_id` (int)
  3. `quantity` (int)
  4. `added_date` (str, format: YYYY-MM-DD)
- **Description:** Stores current shopping cart items.
- **Example Rows:**
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

---

### 4. orders.txt
- **File Path:** `data/orders.txt`
- **Format:** Pipe-delimited (`|`), no headers
- **Fields (in order):**
  1. `order_id` (int)
  2. `customer_name` (str)
  3. `order_date` (str, format: YYYY-MM-DD)
  4. `total_amount` (float)
  5. `status` (str) - e.g. Pending, Shipped, Delivered
  6. `shipping_address` (str)
- **Description:** Stores orders placed with customer and shipping info.
- **Example Rows:**
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

---

### 5. order_items.txt
- **File Path:** `data/order_items.txt`
- **Format:** Pipe-delimited (`|`), no headers
- **Fields (in order):**
  1. `order_item_id` (int)
  2. `order_id` (int)
  3. `book_id` (int)
  4. `quantity` (int)
  5. `price` (float) - price per unit at order time
- **Description:** Stores items for each order.
- **Example Rows:**
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

---

### 6. reviews.txt
- **File Path:** `data/reviews.txt`
- **Format:** Pipe-delimited (`|`), no headers
- **Fields (in order):**
  1. `review_id` (int)
  2. `book_id` (int)
  3. `customer_name` (str)
  4. `rating` (int, 1-5)
  5. `review_text` (str)
  6. `review_date` (str, format: YYYY-MM-DD)
- **Description:** Stores customer reviews for books.
- **Example Rows:**
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

---

### 7. bestsellers.txt
- **File Path:** `data/bestsellers.txt`
- **Format:** Pipe-delimited (`|`), no headers
- **Fields (in order):**
  1. `book_id` (int)
  2. `sales_count` (int)
  3. `period` (str) - e.g. This Week, This Month, All Time
- **Description:** Stores bestseller rankings by sales count and period.
- **Example Rows:**
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

---

This completes the detailed design specification for BookstoreOnline including all Flask routes, frontend HTML templates, and backend data schemas as per the user requirements.