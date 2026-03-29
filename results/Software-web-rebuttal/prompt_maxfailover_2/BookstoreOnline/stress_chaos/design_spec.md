# BookstoreOnline Detailed Design Specification

## 1. Flask Routes Specification

### Root Route
- Path: `/`
- Function name: `root_redirect`
- HTTP Methods: GET
- Behavior: Redirects explicitly to `/dashboard`

---

### Dashboard
- Path: `/dashboard`
- Function name: `dashboard`
- HTTP Methods: GET
- Template rendered: `dashboard.html`
- Context variables:
  - `featured_books` (list of dict): Each dict contains keys - `book_id` (int), `title` (str), `author` (str), `price` (float)
- Function: Displays featured books and quick navigation buttons.

---

### Book Catalog
- Path: `/catalog`
- Function name: `catalog`
- HTTP Methods: GET
- Template rendered: `catalog.html`
- Context variables:
  - `books` (list of dict): Books filtered as per search and category filter. Each dict has `book_id` (int), `title` (str), `author` (str), `category` (str), `price` (float)
  - `categories` (list of dict): Each dict with `category_id` (int), `category_name` (str), `description` (str)
  - `search_query` (str): Search text used
  - `selected_category` (str): Category filter used
- Function: Displays books with search by title, author, ISBN, and filter by category.

---

### Book Details
- Path: `/book/<int:book_id>`
- Function name: `book_details`
- HTTP Methods: GET
- Template rendered: `book_details.html`
- Context variables:
  - `book` (dict): Detailed book info with keys matching data schema
  - `reviews` (list of dict): Customer reviews for this book
- Function: Displays book details and reviews

- Path: `/add_to_cart` 
- Function name: `add_to_cart`
- HTTP Methods: POST
- Form data: `book_id` (int), `quantity` (int, optional, defaults 1)
- Behavior: Adds specified quantity of book to shopping cart
- Redirect: To `/cart`

---

### Shopping Cart
- Path: `/cart`
- Function name: `cart`
- HTTP Methods: GET, POST
- Template rendered: `cart.html`
- GET context variables:
  - `cart_items` (list of dict): Each dict with `item_id` (int), `book` (dict), `quantity` (int), `subtotal` (float)
  - `total_amount` (float): Total amount for cart
- POST form actions:
  - Update quantity:
    - Form fields: `item_id` (int), `quantity` (int)
  - Remove item:
    - Form field: `remove_item_id` (int)
- POST submits update or removal, then redirects GET `/cart`

- POST action determined by submitted field name.

- Button to proceed to `/checkout`

---

### Checkout
- Path: `/checkout`
- Function name: `checkout`
- HTTP Methods: GET, POST
- Template rendered: `checkout.html`
- GET Context variables:
  - `cart_items` (list of dict)
  - `total_amount` (float)
- POST form fields:
  - `customer_name` (str)
  - `shipping_address` (str)
  - `payment_method` (str): One of ['Credit Card', 'PayPal', 'Bank Transfer']
- Behavior: On POST, creates new order and order items, clears cart, redirects to `/orders`

---

### Order History
- Path: `/orders`
- Function name: `orders`
- HTTP Methods: GET
- Template rendered: `orders.html`
- Context variables:
  - `orders` (list of dict): Each dict with `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str), `shipping_address` (str)
  - `filter_status` (str): Current selected status filter
- Filter optional to display orders by status (All, Pending, Shipped, Delivered)

---

### Reviews
- Path: `/reviews`
- Function name: `reviews`
- HTTP Methods: GET
- Template rendered: `reviews.html`
- Context variables:
  - `reviews` (list of dict): Each review dict with book title, rating, text
  - `selected_rating` (str): Rating filter applied
- Function: Displays all customer reviews

---

### Write Review
- Path: `/write_review`
- Function name: `write_review`
- HTTP Methods: GET, POST
- Template rendered: `write_review.html`
- GET context:
  - `books` (list of dict): For dropdown selection
- POST form fields:
  - `book_id` (int)
  - `rating` (int, 1-5)
  - `review_text` (str)
- Behavior: Adds review, redirects to `/reviews`

---

### Bestsellers
- Path: `/bestsellers`
- Function name: `bestsellers`
- HTTP Methods: GET
- Template rendered: `bestsellers.html`
- Context variables:
  - `bestsellers` (list of dict): Books ranked by sales count
  - `selected_period` (str): Filter period (This Week, This Month, All Time)
  - `period_options` (list of str): All period options


## 2. HTML Templates Specification

### 1. dashboard.html
- File path: `templates/dashboard.html`
- Page Title: `<title>Bookstore Dashboard</title>`
- Main Heading: `<h1>Bookstore Dashboard</h1>`
- IDs and elements:
  - `dashboard-page`: `div` container for dashboard
  - `featured-books`: `div` to show featured book recommendations
  - `browse-catalog-button`: `button` navigates to `/catalog` via `url_for('catalog')`
  - `view-cart-button`: `button` navigates to `/cart` via `url_for('cart')`
  - `bestsellers-button`: `button` navigates to `/bestsellers` via `url_for('bestsellers')`

### 2. catalog.html
- File path: `templates/catalog.html`
- Page Title: `<title>Book Catalog</title>`
- Heading: `<h1>Book Catalog</h1>`
- IDs:
  - `catalog-page`: `div` container
  - `search-input`: `input` search field (name="search", method GET)
  - `category-filter`: `select` dropdown for categories (name="category", method GET)
  - `books-grid`: `div` grid container for book cards
  - For each book in `books`:
    - `view-book-button-{book_id}`: `button` to view details route with `url_for('book_details', book_id=book_id)`
- Search and filter form with method GET submits to `/catalog`

### 3. book_details.html
- File path: `templates/book_details.html`
- Page Title: `<title>Book Details</title>`
- Heading: `<h1 id="book-title">{{ book.title }}</h1>`
- IDs:
  - `book-details-page`: `div` container
  - `book-author`: `div` displaying `book.author`
  - `book-price`: `div` displaying `book.price`
  - `add-to-cart-button`: `button`, within a form POST to `/add_to_cart`, with hidden `book_id` input
  - `book-reviews`: `div` showing customer reviews (list)

### 4. cart.html
- File path: `templates/cart.html`
- Page Title: `<title>Shopping Cart</title>`
- Heading: `<h1>Shopping Cart</h1>`
- IDs:
  - `cart-page`: `div` container
  - `cart-items-table`: `table` listing cart items
    - Rows with quantity input: `update-quantity-{item_id}`
    - Remove buttons: `remove-item-button-{item_id}`
  - `total-amount`: `div` for total price
  - `proceed-checkout-button`: `button` navigates to `/checkout`
- Forms:
  - POST for updates/removals with appropriate inputs for item_id, quantity, or removal

### 5. checkout.html
- File path: `templates/checkout.html`
- Page Title: `<title>Checkout</title>`
- Heading: `<h1>Checkout</h1>`
- IDs:
  - `checkout-page`: `div` container
  - `customer-name`: `input` text
  - `shipping-address`: `textarea`
  - `payment-method`: `select` dropdown with options (Credit Card, PayPal, Bank Transfer)
  - `place-order-button`: `button` to submit order
- Form POST to `/checkout`

### 6. orders.html
- File path: `templates/orders.html`
- Page Title: `<title>Order History</title>`
- Heading: `<h1>Order History</h1>`
- IDs:
  - `orders-page`: `div` container
  - `orders-table`: `table` listing orders
  - `view-order-button-{order_id}`: `button` in each row to view details
  - `order-status-filter`: `select` dropdown to filter status
  - `back-to-dashboard`: `button` navigates to `/dashboard`

### 7. reviews.html
- File path: `templates/reviews.html`
- Page Title: `<title>Customer Reviews</title>`
- Heading: `<h1>Customer Reviews</h1>`
- IDs:
  - `reviews-page`: `div` container
  - `reviews-list`: `div` listing reviews
  - `write-review-button`: `button` navigates to `/write_review`
  - `filter-by-rating`: `select` dropdown to filter reviews
  - `back-to-dashboard`: `button` to go to `/dashboard`

### 8. write_review.html
- File path: `templates/write_review.html`
- Page Title: `<title>Write a Review</title>`
- Heading: `<h1>Write a Review</h1>`
- IDs:
  - `write-review-page`: `div` container
  - `select-book`: `select` dropdown for books
  - `rating-select`: `select` dropdown (1-5 stars)
  - `review-text`: `textarea`
  - `submit-review-button`: `button` to submit
- Form POST to `/write_review`

### 9. bestsellers.html
- File path: `templates/bestsellers.html`
- Page Title: `<title>Bestsellers</title>`
- Heading: `<h1>Bestsellers</h1>`
- IDs:
  - `bestsellers-page`: `div` container
  - `bestsellers-list`: `div` listing ranked books
  - `time-period-filter`: `select` dropdown for time period
  - For each bestseller:
    - `view-book-button-{book_id}`: `button` to view details
  - `back-to-dashboard`: `button` to `/dashboard`


## 3. Data Schemas Specification

### books.txt
- File Path: `data/books.txt`
- Fields: `book_id|title|author|isbn|category|price|stock|description`
- Description: Contains all books with their details
- Example Lines:
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

### categories.txt
- File Path: `data/categories.txt`
- Fields: `category_id|category_name|description`
- Description: Book category definitions
- Example Lines:
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

### cart.txt
- File Path: `data/cart.txt`
- Fields: `cart_id|book_id|quantity|added_date`
- Description: Records items currently in cart
- Example Lines:
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

### orders.txt
- File Path: `data/orders.txt`
- Fields: `order_id|customer_name|order_date|total_amount|status|shipping_address`
- Description: Records placed orders
- Example Lines:
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

### order_items.txt
- File Path: `data/order_items.txt`
- Fields: `order_item_id|order_id|book_id|quantity|price`
- Description: Records each book item in an order
- Example Lines:
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

### reviews.txt
- File Path: `data/reviews.txt`
- Fields: `review_id|book_id|customer_name|rating|review_text|review_date`
- Description: Customer reviews on books
- Example Lines:
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

### bestsellers.txt
- File Path: `data/bestsellers.txt`
- Fields: `book_id|sales_count|period`
- Description: Bestseller book sales counts over periods
- Example Lines:
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```


---

End of design_spec.md
