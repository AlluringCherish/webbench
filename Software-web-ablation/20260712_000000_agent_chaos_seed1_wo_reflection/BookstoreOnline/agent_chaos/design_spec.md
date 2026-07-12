# BookstoreOnline Design Specification Document

---

## Section 1: Flask Routes Specification

#### 1. Root Route
- **Route Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Methods:** GET
- **Behavior:** Redirects to `/dashboard`

---

#### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** `dashboard`
- **HTTP Methods:** GET
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `featured_books` (list of dict): List of featured books (each dict with keys: `book_id` (int), `title` (str), `author` (str), `price` (float))
  - `bestsellers` (list of dict): List of bestseller books with ranks

---

#### 3. Book Catalog Page
- **Route Path:** `/catalog`
- **Function Name:** `catalog`
- **HTTP Methods:** GET
- **Template Rendered:** `catalog.html`
- **Query Parameters:**
  - `search` (str, optional): Search keyword by title, author, or ISBN
  - `category` (str, optional): Category filter
- **Context Variables:**
  - `books` (list of dict): List of books matching search/filter,
    each dict has: `book_id` (int), `title` (str), `author` (str), `price` (float)
  - `categories` (list of dict): List of categories with keys: `category_id` (int), `category_name` (str)
  - `selected_category` (str): Selected category for filter
  - `search_query` (str): Search input value

---

#### 4. Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** `book_details`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `book_details.html`
- **Context Variables:**
  - `book` (dict): Details of the book (`book_id` (int), `title` (str), `author` (str), `price` (float), `description` (str))
  - `reviews` (list of dict): List of reviews for the book (each dict with keys: `review_id` (int), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str))

- **Form Handling (POST):** Add the book to the shopping cart with quantity=1.

---

#### 5. Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** `cart`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `cart.html`
- **Context Variables:**
  - `cart_items` (list of dict): Each dict has `item_id` (int), `book_id` (int), `title` (str), `quantity` (int), `price` (float), `subtotal` (float)
  - `total_amount` (float): Total amount of all cart items

- **Form Handling (POST):**
  - Update quantities via fields named `update-quantity-{item_id}`
  - Remove items via forms or buttons named `remove-item-button-{item_id}`

---

#### 6. Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** `checkout`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `checkout.html`
- **Context Variables:** None

- **Form Handling (POST):**
  - Form with fields: `customer_name` (str), `shipping_address` (str), `payment_method` (str)
  - On submit, creates order and order items from cart and clears cart.

---

#### 7. Order History Page
- **Route Path:** `/orders`
- **Function Name:** `orders`
- **HTTP Methods:** GET
- **Template Rendered:** `orders.html`
- **Query Parameters:**
  - `status` (str, optional): Filter orders by status (All, Pending, Shipped, Delivered)
- **Context Variables:**
  - `orders` (list of dict): Each dict has `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str), `shipping_address` (str)
  - `selected_status` (str): Current status filter

---

#### 8. Order Details Page (via button on Order History)
- **Route Path:** `/order/<int:order_id>`
- **Function Name:** `order_details`
- **HTTP Methods:** GET
- **Template Rendered:** `order_details.html`
- **Context Variables:**
  - `order` (dict): Order info (`order_id`, `customer_name`, `order_date`, `total_amount`, `status`, `shipping_address`)
  - `order_items` (list of dict): Items in the order - each has `book_id` (int), `title` (str), `quantity` (int), `price` (float)

---

#### 9. Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** `reviews`
- **HTTP Methods:** GET
- **Template Rendered:** `reviews.html`
- **Query Parameters:**
  - `rating` (str, optional): Filter reviews by rating (All, 5 stars, 4 stars, etc.)
- **Context Variables:**
  - `reviews` (list of dict): Each dict has `review_id` (int), `book_title` (str), `rating` (int), `review_text` (str), `customer_name` (str), `review_date` (str)
  - `selected_rating` (str)

---

#### 10. Write Review Page
- **Route Path:** `/write_review`
- **Function Name:** `write_review`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `write_review.html`
- **Context Variables:**
  - `books` (list of dict): List of books that can be reviewed (`book_id`, `title`)

- **Form Handling (POST):**
  - Form fields: `book_id` (int), `rating` (int), `review_text` (str), `customer_name` (str, assumed to be entered optionally or fixed as anonymous)

---

#### 11. Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** `bestsellers`
- **HTTP Methods:** GET
- **Template Rendered:** `bestsellers.html`
- **Query Parameters:**
  - `period` (str, optional): Time period filter (This Week, This Month, All Time)
- **Context Variables:**
  - `bestsellers` (list of dict): Each with `rank` (int), `book_id` (int), `title` (str), `author` (str), `sales_count` (int), `period` (str)
  - `selected_period` (str)

---

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page Template
- **File Path:** `templates/dashboard.html`
- **Page Title & H1:** "Bookstore Dashboard"
- **Element IDs:**
  - `dashboard-page` (Div): Container
  - `featured-books` (Div): Featured book recommendations display
  - `browse-catalog-button` (Button): Navigates to catalog (`url_for('catalog')`)
  - `view-cart-button` (Button): Navigates to cart (`url_for('cart')`)
  - `bestsellers-button` (Button): Navigates to bestsellers (`url_for('bestsellers')`)
- **Context Variables:**
  - `featured_books` (list of dict): each dict with `book_id`, `title`, `author`, `price`
  - `bestsellers` (list of dict)

### 2. Book Catalog Page Template
- **File Path:** `templates/catalog.html`
- **Page Title & H1:** "Book Catalog"
- **Element IDs:**
  - `catalog-page` (Div): Container
  - `search-input` (Input): Search field
  - `category-filter` (Dropdown): Category filter, options populated from `categories`
  - `books-grid` (Div): Grid for book cards
  - Dynamic: `view-book-button-{book_id}` (Button): For each book card, link to `url_for('book_details', book_id=book_id)`
- **Context Variables:**
  - `books` (list of dict): `book_id`, `title`, `author`, `price`
  - `categories` (list of dict): `category_id`, `category_name`
  - `selected_category` (str)
  - `search_query` (str)

### 3. Book Details Page Template
- **File Path:** `templates/book_details.html`
- **Page Title & H1:** "Book Details"
- **Element IDs:**
  - `book-details-page` (Div): Container
  - `book-title` (H1): Book title text
  - `book-author` (Div): Book author
  - `book-price` (Div): Book price
  - `add-to-cart-button` (Button): POST form button to add book to cart
  - `book-reviews` (Div): List of reviews
- **Context Variables:**
  - `book` (dict): keys `book_id`, `title`, `author`, `price`, `description`
  - `reviews` (list of dict): each with `review_id`, `customer_name`, `rating`, `review_text`, `review_date`
- **Form:**
  - POST form with action same route, submitting add-to-cart

### 4. Shopping Cart Page Template
- **File Path:** `templates/cart.html`
- **Page Title & H1:** "Shopping Cart"
- **Element IDs:**
  - `cart-page` (Div): Container
  - `cart-items-table` (Table): Displays cart items (title, quantity, price, subtotal)
  - Dynamic inputs: `update-quantity-{item_id}` (Input number): To update quantity for each item
  - Dynamic buttons: `remove-item-button-{item_id}` (Button): Remove item from cart
  - `proceed-checkout-button` (Button): Navigates to `/checkout`
  - `total-amount` (Div): Displays total cart amount
- **Context Variables:**
  - `cart_items` (list of dict): item_id, book_id, title, quantity, price, subtotal
  - `total_amount` (float)
- **Form:**
  - POST form encompassing quantity updates and removals

### 5. Checkout Page Template
- **File Path:** `templates/checkout.html`
- **Page Title & H1:** "Checkout"
- **Element IDs:**
  - `checkout-page` (Div)
  - `customer-name` (Input text)
  - `shipping-address` (Textarea)
  - `payment-method` (Dropdown): Options - Credit Card, PayPal, Bank Transfer
  - `place-order-button` (Button): Submit button
- **Form:**
  - POST form for submitting order details

### 6. Order History Page Template
- **File Path:** `templates/orders.html`
- **Page Title & H1:** "Order History"
- **Element IDs:**
  - `orders-page` (Div)
  - `orders-table` (Table): Shows orders with columns order ID, date, total, status
  - `view-order-button-{order_id}` (Button): View details
  - `order-status-filter` (Dropdown): Options - All, Pending, Shipped, Delivered
  - `back-to-dashboard` (Button): Navigates to `/dashboard`
- **Context Variables:**
  - `orders` (list of dict): order_id, customer_name, order_date, total_amount, status, shipping_address
  - `selected_status` (str)

### 7. Order Details Page Template (Implicit from routes)
- **File Path:** `templates/order_details.html`
- **Page Title & H1:** "Order Details"
- **Element IDs:**
  - `order-details-page` (Div)
  - `order-info` (Div): Displays order summary
  - `order-items-table` (Table): Lists items in the order
- **Context Variables:**
  - `order` (dict): Detailed order info
  - `order_items` (list of dict)

### 8. Reviews Page Template
- **File Path:** `templates/reviews.html`
- **Page Title & H1:** "Customer Reviews"
- **Element IDs:**
  - `reviews-page` (Div)
  - `reviews-list` (Div): List of reviews with book title, rating, review text
  - `write-review-button` (Button): Navigates to `/write_review`
  - `filter-by-rating` (Dropdown): Options All, 5 stars, 4 stars...
  - `back-to-dashboard` (Button): Navigates to `/dashboard`
- **Context Variables:**
  - `reviews` (list of dict): review_id, book_title, rating, review_text, customer_name, review_date
  - `selected_rating` (str)

### 9. Write Review Page Template
- **File Path:** `templates/write_review.html`
- **Page Title & H1:** "Write a Review"
- **Element IDs:**
  - `write-review-page` (Div)
  - `select-book` (Dropdown): Lists `books` as options
  - `rating-select` (Dropdown): Options 1-5 stars
  - `review-text` (Textarea)
  - `submit-review-button` (Button)
- **Context Variables:**
  - `books` (list of dict): book_id, title
- **Form:**
  - POST form with fields: book_id, rating, review_text, customer_name

### 10. Bestsellers Page Template
- **File Path:** `templates/bestsellers.html`
- **Page Title & H1:** "Bestsellers"
- **Element IDs:**
  - `bestsellers-page` (Div)
  - `bestsellers-list` (Div): Ranked list of bestsellers
  - `time-period-filter` (Dropdown): Options This Week, This Month, All Time
  - Dynamic buttons: `view-book-button-{book_id}` (Button) to book details
  - `back-to-dashboard` (Button): Navigates to `/dashboard`
- **Context Variables:**
  - `bestsellers` (list of dict): rank, book_id, title, author, sales_count, period
  - `selected_period` (str)

---

## Section 3: Data Schemas Specification

### 1. Books Data
- **File Path:** `data/books.txt`
- **Pipe-Delimited Format:**
  ```
  book_id|title|author|isbn|category|price|stock|description
  ```
- **Description:** Stores all books available in the store.
- **Example Rows:**
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

### 2. Categories Data
- **File Path:** `data/categories.txt`
- **Pipe-Delimited Format:**
  ```
  category_id|category_name|description
  ```
- **Description:** Contains book categories for filtering.
- **Example Rows:**
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

### 3. Cart Data
- **File Path:** `data/cart.txt`
- **Pipe-Delimited Format:**
  ```
  cart_id|book_id|quantity|added_date
  ```
- **Description:** Tracks items added to the cart.
- **Example Rows:**
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

### 4. Orders Data
- **File Path:** `data/orders.txt`
- **Pipe-Delimited Format:**
  ```
  order_id|customer_name|order_date|total_amount|status|shipping_address
  ```
- **Description:** Stores all customer orders.
- **Example Rows:**
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

### 5. Order Items Data
- **File Path:** `data/order_items.txt`
- **Pipe-Delimited Format:**
  ```
  order_item_id|order_id|book_id|quantity|price
  ```
- **Description:** Lists items within each order.
- **Example Rows:**
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

### 6. Reviews Data
- **File Path:** `data/reviews.txt`
- **Pipe-Delimited Format:**
  ```
  review_id|book_id|customer_name|rating|review_text|review_date
  ```
- **Description:** Customer reviews for books.
- **Example Rows:**
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

### 7. Bestsellers Data
- **File Path:** `data/bestsellers.txt`
- **Pipe-Delimited Format:**
  ```
  book_id|sales_count|period
  ```
- **Description:** Stores top-selling books by sales count and period.
- **Example Rows:**
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---
