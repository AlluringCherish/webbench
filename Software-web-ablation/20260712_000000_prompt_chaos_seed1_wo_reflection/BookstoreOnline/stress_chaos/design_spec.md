# Design Specification Document for BookstoreOnline

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path:** `/`
- **Function Name:** root_redirect
- **HTTP Method(s):** GET
- **Action:** Redirects to `/dashboard`

---

### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** dashboard
- **HTTP Method(s):** GET
- **Template:** `dashboard.html`
- **Context Variables:**
  - `featured_books`: `list` of dicts with keys (`book_id` (int), `title` (str), `author` (str), `price` (float))
  - `bestsellers`: `list` of dicts with keys (`book_id` (int), `title` (str), `author` (str), `sales_count` (int))

---

### 3. Book Catalog Page
- **Route Path:** `/catalog`
- **Function Name:** book_catalog
- **HTTP Method(s):** GET
- **Template:** `catalog.html`
- **Context Variables:**
  - `books`: `list` of dicts with keys (`book_id` (int), `title` (str), `author` (str), `isbn` (str), `category` (str), `price` (float))
  - `categories`: `list` of dicts with keys (`category_id` (int), `category_name` (str))
  - `selected_category`: `str` (category name or empty string)
  - `search_query`: `str`

---

### 4. Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** book_details
- **HTTP Method(s):** GET
- **Template:** `book_details.html`
- **Context Variables:**
  - `book`: dict with keys (`book_id` (int), `title` (str), `author` (str), `price` (float), `description` (str))
  - `reviews`: `list` of dicts with keys (`review_id` (int), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str))

- **POST Action:** Adding book to cart when `add-to-cart-button` is clicked or form submitted
  - Retrieves `book_id` from URL
  - Updates `cart.txt` with new entry or increments quantity
  - Redirects back to `/cart` or same page with message

---

### 5. Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** shopping_cart
- **HTTP Method(s):** GET, POST
- **Template:** `cart.html`
- **Context Variables:**
  - `cart_items`: `list` of dicts with keys (`cart_id` (int), `book_id` (int), `title` (str), `quantity` (int), `price` (float), `subtotal` (float))
  - `total_amount`: `float`

- **POST Actions:**
  - Update quantity: expects `cart_id` and new quantity from input `update-quantity-{item_id}`
  - Remove item: expects `cart_id` from button `remove-item-button-{item_id}`
  - After POST updates, redirect back to `/cart`

---

### 6. Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** checkout
- **HTTP Method(s):** GET, POST
- **Template:** `checkout.html`
- **Context Variables:** None required for GET

- **POST Action:** Place order by submitting form with fields:
  - `customer_name` (str)
  - `shipping_address` (str)
  - `payment_method` (str) (values: `Credit Card`, `PayPal`, `Bank Transfer`)

- Steps:
  - Calculate total from cart
  - Create new order in `orders.txt` with status `Pending`
  - Create order items in `order_items.txt` from current cart items
  - Clear current cart
  - Redirect to order history or confirmation page (redirect to `/orders` as per available pages)

---

### 7. Order History Page
- **Route Path:** `/orders`
- **Function Name:** order_history
- **HTTP Method(s):** GET
- **Template:** `orders.html`
- **Context Variables:**
  - `orders`: `list` of dicts with keys (`order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str), `shipping_address` (str))
  - `status_filter`: `str` (values: `All`, `Pending`, `Shipped`, `Delivered`)

- **Query Parameter:** Optional filter via query string `?status=` for filtering by order status

---

### 8. Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** reviews_page
- **HTTP Method(s):** GET
- **Template:** `reviews.html`
- **Context Variables:**
  - `reviews`: `list` of dicts with keys (`review_id` (int), `book_id` (int), `book_title` (str), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str))
  - `rating_filter`: `str` (values: `All`, `5`, `4`, `3`, `2`, `1`)

- Query param `?rating=` to filter reviews by rating

---

### 9. Write Review Page
- **Route Path:** `/write_review`
- **Function Name:** write_review
- **HTTP Method(s):** GET, POST
- **Template:** `write_review.html`
- **Context Variables:**
  - `books`: `list` of dicts with keys (`book_id` (int), `title` (str))

- **POST Action:** Submit review form with fields:
  - `book_id` (int)
  - `rating` (int, 1-5)
  - `review_text` (str)
  - `customer_name` can be optional or fixed (no auth specified, so can prompt or default)

- Add new review entry to `reviews.txt` with current date
- Redirect back to `/reviews`

---

### 10. Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** bestsellers_page
- **HTTP Method(s):** GET
- **Template:** `bestsellers.html`
- **Context Variables:**
  - `bestsellers`: `list` of dicts with keys (`book_id` (int), `title` (str), `author` (str), `sales_count` (int), `period` (str))
  - `time_period`: `str` (e.g., `This Week`, `This Month`, `All Time`)

- Query param `?period=` to filter bestsellers by period

---

## Section 2: HTML Templates Specification

### 1. `templates/dashboard.html`
- **Page Title:** Bookstore Dashboard
- **Main Heading:** `<h1 id="dashboard-page">Bookstore Dashboard</h1>`
- **IDs and Elements:**
  - `dashboard-page` (Div) - Container for dashboard page
  - `featured-books` (Div) - Displays featured book recommendations
  - `browse-catalog-button` (Button) - Navigates to `/catalog` via `url_for('book_catalog')`
  - `view-cart-button` (Button) - Navigates to `/cart` via `url_for('shopping_cart')`
  - `bestsellers-button` (Button) - Navigates to `/bestsellers` via `url_for('bestsellers_page')`

- **Context Variables:**
  - `featured_books`: list of dicts (`book_id`, `title`, `author`, `price`)
  - `bestsellers`: list of dicts (`book_id`, `title`, `author`, `sales_count`)

---

### 2. `templates/catalog.html`
- **Page Title:** Book Catalog
- **Main Heading:** `<h1 id="catalog-page">Book Catalog</h1>`
- **IDs and Elements:**
  - `catalog-page` (Div) - Page container
  - `search-input` (Input) - Search input, name="search_query"
  - `category-filter` (Dropdown) - Dropdown with name="category_filter" to filter by category
  - `books-grid` (Div) - Container for displayed books
  - Dynamic buttons `view-book-button-{book_id}` (Button) for each book; link to `/book/<book_id>`

- **Context Variables:**
  - `books`: list of dicts as above
  - `categories`: list of dicts (`category_id`, `category_name`)
  - `selected_category`: string
  - `search_query`: string

---

### 3. `templates/book_details.html`
- **Page Title:** Book Details
- **Main Heading:** `<h1 id="book-title">{{ book.title }}</h1>`
- **IDs and Elements:**
  - `book-details-page` (Div) - Container
  - `book-title` (H1) - Book title
  - `book-author` (Div) - Book author
  - `book-price` (Div) - Book price
  - `add-to-cart-button` (Button) - Form button for adding book to cart
  - `book-reviews` (Div) - Customer reviews section

- **Context Variables:**
  - `book`: dict
  - `reviews`: list of dicts (review info)

- **Form Structure:** POST form wraps `add-to-cart-button`, submits to same route

---

### 4. `templates/cart.html`
- **Page Title:** Shopping Cart
- **Main Heading:** `<h1 id="cart-page">Shopping Cart</h1>`
- **IDs and Elements:**
  - `cart-page` (Div) - Container
  - `cart-items-table` (Table) - Displays each cart item row
  - For each cart item:
    - `update-quantity-{cart_id}` (Input, type=number) - Quantity input
    - `remove-item-button-{cart_id}` (Button) - Remove item button
  - `proceed-checkout-button` (Button) - Link to `/checkout`
  - `total-amount` (Div) - Displays total amount

- **Context Variables:**
  - `cart_items`: list of dicts with cart item details
  - `total_amount`: float

- **Form Structure:** POST forms for quantity update and remove item identified by dynamic IDs

---

### 5. `templates/checkout.html`
- **Page Title:** Checkout
- **Main Heading:** `<h1 id="checkout-page">Checkout</h1>`
- **IDs and Elements:**
  - `checkout-page` (Div) - Container
  - Form includes:
    - `customer-name` (Input, type=text)
    - `shipping-address` (Textarea)
    - `payment-method` (Dropdown) with options: Credit Card, PayPal, Bank Transfer
    - `place-order-button` (Button) - Submit button

- **Form Method:** POST

---

### 6. `templates/orders.html`
- **Page Title:** Order History
- **Main Heading:** `<h1 id="orders-page">Order History</h1>`
- **IDs and Elements:**
  - `orders-page` (Div) - Container
  - `orders-table` (Table) - Displays orders
  - Dynamic buttons `view-order-button-{order_id}` (Button) for each order
  - `order-status-filter` (Dropdown) - Filter orders by status
  - `back-to-dashboard` (Button) - Navigate to `/dashboard`

- **Context Variables:**
  - `orders`: list of dicts
  - `status_filter`: string

---

### 7. `templates/reviews.html`
- **Page Title:** Customer Reviews
- **Main Heading:** `<h1 id="reviews-page">Customer Reviews</h1>`
- **IDs and Elements:**
  - `reviews-page` (Div) - Container
  - `reviews-list` (Div) - Lists reviews
  - `write-review-button` (Button) - Navigates to `/write_review`
  - `filter-by-rating` (Dropdown) - Filter reviews by rating
  - `back-to-dashboard` (Button) - Navigates to `/dashboard`

- **Context Variables:**
  - `reviews`: list of dicts
  - `rating_filter`: string

---

### 8. `templates/write_review.html`
- **Page Title:** Write a Review
- **Main Heading:** `<h1 id="write-review-page">Write a Review</h1>`
- **IDs and Elements:**
  - `write-review-page` (Div) - Container
  - `select-book` (Dropdown) - Select book by title
  - `rating-select` (Dropdown) - Select rating 1-5 stars
  - `review-text` (Textarea) - Enter review text
  - `submit-review-button` (Button) - Submit form

- **Context Variables:**
  - `books`: list of dicts

- **Form Method:** POST

---

### 9. `templates/bestsellers.html`
- **Page Title:** Bestsellers
- **Main Heading:** `<h1 id="bestsellers-page">Bestsellers</h1>`
- **IDs and Elements:**
  - `bestsellers-page` (Div) - Container
  - `bestsellers-list` (Div) - Displays bestseller books ranked
  - Dynamic buttons `view-book-button-{book_id}` (Button) for each bestseller
  - `time-period-filter` (Dropdown) - Filter by time period
  - `back-to-dashboard` (Button) - Navigates to `/dashboard`

- **Context Variables:**
  - `bestsellers`: list of dicts
  - `time_period`: string

---

## Section 3: Data Schemas Specification

### 1. `data/books.txt`
- **File Format:** Pipe-delimited `|`
- **Fields (in order):**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `category` (str)
  6. `price` (float)
  7. `stock` (int)
  8. `description` (str)

- **Description:** Stores all books available in the catalog including details.

- **Example Rows:**
  - `1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel`
  - `2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind`
  - `3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction`

---

### 2. `data/categories.txt`
- **File Format:** Pipe-delimited `|`
- **Fields (in order):**
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)

- **Description:** Stores book categories.

- **Example Rows:**
  - `1|Fiction|Fictional narratives and novels`
  - `2|Non-Fiction|Factual and educational books`
  - `3|Science|Scientific topics and research`

---

### 3. `data/cart.txt`
- **File Format:** Pipe-delimited `|`
- **Fields (in order):**
  1. `cart_id` (int)
  2. `book_id` (int)
  3. `quantity` (int)
  4. `added_date` (str, yyyy-mm-dd)

- **Description:** Stores shopping cart entries.

- **Example Rows:**
  - `1|1|2|2025-01-15`
  - `2|3|1|2025-01-16`

---

### 4. `data/orders.txt`
- **File Format:** Pipe-delimited `|`
- **Fields (in order):**
  1. `order_id` (int)
  2. `customer_name` (str)
  3. `order_date` (str, yyyy-mm-dd)
  4. `total_amount` (float)
  5. `status` (str) (e.g. Pending, Shipped, Delivered)
  6. `shipping_address` (str)

- **Description:** Stores orders placed by customers.

- **Example Rows:**
  - `1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001`
  - `2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001`

---

### 5. `data/order_items.txt`
- **File Format:** Pipe-delimited `|`
- **Fields (in order):**
  1. `order_item_id` (int)
  2. `order_id` (int)
  3. `book_id` (int)
  4. `quantity` (int)
  5. `price` (float)

- **Description:** Stores items belonging to each order.

- **Example Rows:**
  - `1|1|1|2|12.99`
  - `2|1|3|1|14.99`
  - `3|2|2|1|16.99`

---

### 6. `data/reviews.txt`
- **File Format:** Pipe-delimited `|`
- **Fields (in order):**
  1. `review_id` (int)
  2. `book_id` (int)
  3. `customer_name` (str)
  4. `rating` (int, 1-5)
  5. `review_text` (str)
  6. `review_date` (str, yyyy-mm-dd)

- **Description:** Stores customer reviews for books.

- **Example Rows:**
  - `1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12`
  - `2|2|Bob Williams|4|Very informative and well-written.|2025-01-13`
  - `3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15`

---

### 7. `data/bestsellers.txt`
- **File Format:** Pipe-delimited `|`
- **Fields (in order):**
  1. `book_id` (int)
  2. `sales_count` (int)
  3. `period` (str) (e.g. This Week, This Month, All Time)

- **Description:** Stores sales counts of top-selling books for periods.

- **Example Rows:**
  - `2|150|This Month`
  - `1|120|This Month`
  - `3|95|This Month`


---

# End of Design Specification Document
