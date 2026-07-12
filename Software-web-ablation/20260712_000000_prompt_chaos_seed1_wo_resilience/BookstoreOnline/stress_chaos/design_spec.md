# BookstoreOnline Design Specification

---

## Section 1: Flask Routes Specification

1. **Root Route**
   - **Path**: `/`
   - **Function**: `root_redirect`
   - **Methods**: `GET`
   - **Action**: Redirects to `/dashboard`

---

2. **Dashboard Page**
   - **Path**: `/dashboard`
   - **Function**: `dashboard`
   - **Methods**: `GET`
   - **Template**: `dashboard.html`
   - **Context Variables**:
     - `featured_books`: list of dict (each dict with `book_id` (int), `title` (str), `author` (str), `price` (float))
     - `bestsellers`: list of dict (each dict with `book_id` (int), `title` (str), `author` (str), `sales_count` (int))

---

3. **Book Catalog Page**
   - **Path**: `/catalog`
   - **Function**: `book_catalog`
   - **Methods**: `GET`
   - **Template**: `catalog.html`
   - **Context Variables**:
     - `books`: list of dict (each dict with `book_id` (int), `title` (str), `author` (str), `price` (float), `category` (str))
     - `categories`: list of str (category names)
     - `search_query`: str (search input value)
     - `selected_category`: str (category filter selection)

---

4. **Book Details Page**
   - **Path**: `/book/<int:book_id>`
   - **Function**: `book_details`
   - **Methods**: `GET`, `POST`
   - **Template**: `book_details.html`
   - **Context Variables** (GET):
     - `book`: dict with fields `book_id` (int), `title` (str), `author` (str), `price` (float), `description` (str), `stock` (int)
     - `reviews`: list of dict (each dict with `review_id` (int), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str))
   - **POST Handling**:
     - Form submission from Add to Cart button
     - Add specified quantity (default 1) of the book to `cart.txt`
     - Redirect back to the same book details page after adding

---

5. **Shopping Cart Page**
   - **Path**: `/cart`
   - **Function**: `shopping_cart`
   - **Methods**: `GET`, `POST`
   - **Template**: `cart.html`
   - **Context Variables** (GET):
     - `cart_items`: list of dict (each with `item_id` (int, cart record id), `book_id` (int), `title` (str), `quantity` (int), `price` (float), `subtotal` (float))
     - `total_amount`: float
   - **POST Handling**:
     - Form submission for updating quantities or removing items
     - Actions:
       - Update quantity for a given `item_id`
       - Remove item for a given `item_id`
     - After POST, redirect to `/cart`

---

6. **Checkout Page**
   - **Path**: `/checkout`
   - **Function**: `checkout`
   - **Methods**: `GET`, `POST`
   - **Template**: `checkout.html`
   - **Context Variables** (GET):
     - Empty or possibly `cart_items` and `total_amount` but not required explicitly by user task
   - **POST Handling**:
     - Process the checkout form:
       - Collect `customer_name` (str), `shipping_address` (str), `payment_method` (str)
       - Generate a new order id
       - Calculate total amount from current cart
       - Save new order in `orders.txt` with status `Pending`
       - Save order items in `order_items.txt`
       - Clear `cart.txt`
     - Redirect to `/order_history`

---

7. **Order History Page**
   - **Path**: `/order_history`
   - **Function**: `order_history`
   - **Methods**: `GET`
   - **Template**: `order_history.html`
   - **Context Variables**:
     - `orders`: list of dict (each dict with `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str), `shipping_address` (str))
     - `selected_status`: str (filter selection)

---

8. **Order Details Page (Optional detailed view triggered by button in order history)**
   - **Path**: `/order/<int:order_id>`
   - **Function**: `order_details`
   - **Methods**: `GET`
   - **Template**: `order_details.html` (not explicitly requested but implied by view-order-button)
   - **Context Variables**:
     - `order`: dict with order details
     - `order_items`: list of dict with each item in the order

---

9. **Reviews Page**
   - **Path**: `/reviews`
   - **Function**: `reviews`
   - **Methods**: `GET`
   - **Template**: `reviews.html`
   - **Context Variables**:
     - `reviews`: list of dict (each with book title, rating, text, customer_name)
     - `filter_rating`: str (e.g. 'All', '5 stars', '4 stars', etc.)

---

10. **Write Review Page**
    - **Path**: `/write_review`
    - **Function**: `write_review`
    - **Methods**: `GET`, `POST`
    - **Template**: `write_review.html`
    - **Context Variables** (GET):
      - `purchased_books`: list of dict (each dict with `book_id` (int), `title` (str))
    - **POST Handling**:
      - Submit review form with `book_id` (int), `customer_name` (str), `rating` (int), `review_text` (str)
      - Save review to `reviews.txt` with new review_id and current date
      - Redirect to `/reviews`

---

11. **Bestsellers Page**
    - **Path**: `/bestsellers`
    - **Function**: `bestsellers`
    - **Methods**: `GET`
    - **Template**: `bestsellers.html`
    - **Context Variables**:
      - `bestsellers`: list of dict (each dict with `book_id` (int), `title` (str), `author` (str), `sales_count` (int), `period` (str))
      - `time_period`: str (selected time period filter)


## Section 2: HTML Templates Specification

All templates are stored under the `templates/` directory.

### 1. `templates/dashboard.html`
- **Page Title**: `Bookstore Dashboard`
- **Main H1 Heading**: `Bookstore Dashboard`
- **Element IDs**:
  - `dashboard-page` (Div): Container for dashboard page
  - `featured-books` (Div): Display featured book recommendations
  - `browse-catalog-button` (Button): Navigate to `/catalog`
  - `view-cart-button` (Button): Navigate to `/cart`
  - `bestsellers-button` (Button): Navigate to `/bestsellers`
- **Context Variables**:
  - `featured_books` (list of dict)
  - `bestsellers` (list of dict)
- **Navigation**:
  - `browse-catalog-button` triggers URL: `url_for('book_catalog')`
  - `view-cart-button` triggers URL: `url_for('shopping_cart')`
  - `bestsellers-button` triggers URL: `url_for('bestsellers')`

---

### 2. `templates/catalog.html`
- **Page Title**: `Book Catalog`
- **Main H1 Heading**: `Book Catalog`
- **Element IDs**:
  - `catalog-page` (Div): Container for catalog page
  - `search-input` (Input): Search field for books by title, author, ISBN
  - `category-filter` (Dropdown): Filter by category (options from `categories`)
  - `books-grid` (Div): Grid displaying book cards
  - `view-book-button-{book_id}` (Button): For each book, button to view details
- **Context Variables**:
  - `books` (list of dict)
  - `categories` (list of str)
  - `search_query` (str)
  - `selected_category` (str)
- **Navigation**:
  - Each `view-book-button-{book_id}` triggers URL: `url_for('book_details', book_id=book_id)`

---

### 3. `templates/book_details.html`
- **Page Title**: `Book Details`
- **Main H1 Heading**: Book title from `book.title` context variable
- **Element IDs**:
  - `book-details-page` (Div): Container for book details page
  - `book-title` (H1): Displays book title
  - `book-author` (Div): Displays author
  - `book-price` (Div): Displays price
  - `add-to-cart-button` (Button): Button to submit add to cart POST
  - `book-reviews` (Div): Displays list of customer reviews
- **Context Variables**:
  - `book` (dict)
  - `reviews` (list of dict)
- **Form Structure**:
  - POST form around Add to Cart button with quantity input if applicable
- **Navigation**:
  - No special navigation buttons, back links can use generic methods

---

### 4. `templates/cart.html`
- **Page Title**: `Shopping Cart`
- **Main H1 Heading**: `Shopping Cart`
- **Element IDs**:
  - `cart-page` (Div): Container for cart page
  - `cart-items-table` (Table): Displays cart items
  - `update-quantity-{item_id}` (Input number): Quantity input for each item
  - `remove-item-button-{item_id}` (Button): Remove button for each item
  - `proceed-checkout-button` (Button): Navigate to checkout page
  - `total-amount` (Div): Displays total cart amount
- **Context Variables**:
  - `cart_items` (list of dict)
  - `total_amount` (float)
- **Form Structure**:
  - Form to update quantities and remove items with POST
- **Navigation**:
  - `proceed-checkout-button` triggers URL: `url_for('checkout')`

---

### 5. `templates/checkout.html`
- **Page Title**: `Checkout`
- **Main H1 Heading**: `Checkout`
- **Element IDs**:
  - `checkout-page` (Div): Container for checkout page
  - `customer-name` (Input): Field for customer name
  - `shipping-address` (Textarea): Field for shipping address
  - `payment-method` (Dropdown): Options: Credit Card, PayPal, Bank Transfer
  - `place-order-button` (Button): Submit checkout form
- **Context Variables**:
  - None required explicitly
- **Form Structure**:
  - POST form for checkout details, submit triggers order processing

---

### 6. `templates/order_history.html`
- **Page Title**: `Order History`
- **Main H1 Heading**: `Order History`
- **Element IDs**:
  - `orders-page` (Div): Container for order history page
  - `orders-table` (Table): Displays order records
  - `view-order-button-{order_id}` (Button): View details of each order
  - `order-status-filter` (Dropdown): Filter orders by status
  - `back-to-dashboard` (Button): Navigate back to dashboard
- **Context Variables**:
  - `orders` (list of dict)
  - `selected_status` (str)
- **Navigation**:
  - `view-order-button-{order_id}` triggers URL: `url_for('order_details', order_id=order_id)`
  - `back-to-dashboard` triggers URL: `url_for('dashboard')`

---

### 7. `templates/reviews.html`
- **Page Title**: `Customer Reviews`
- **Main H1 Heading**: `Customer Reviews`
- **Element IDs**:
  - `reviews-page` (Div): Container for reviews page
  - `reviews-list` (Div): List all reviews
  - `write-review-button` (Button): Navigate to write review page
  - `filter-by-rating` (Dropdown): Filter reviews by rating
  - `back-to-dashboard` (Button): Navigate back to dashboard
- **Context Variables**:
  - `reviews` (list of dict)
  - `filter_rating` (str)
- **Navigation**:
  - `write-review-button` triggers URL: `url_for('write_review')`
  - `back-to-dashboard` triggers URL: `url_for('dashboard')`

---

### 8. `templates/write_review.html`
- **Page Title**: `Write a Review`
- **Main H1 Heading**: `Write a Review`
- **Element IDs**:
  - `write-review-page` (Div): Container for write review page
  - `select-book` (Dropdown): Select book to review (options from `purchased_books`)
  - `rating-select` (Dropdown): Rating selection (1-5 stars)
  - `review-text` (Textarea): Input review text
  - `submit-review-button` (Button): Submit review form
- **Context Variables**:
  - `purchased_books` (list of dict)
- **Form Structure**:
  - POST form for submitting review

---

### 9. `templates/bestsellers.html`
- **Page Title**: `Bestsellers`
- **Main H1 Heading**: `Bestsellers`
- **Element IDs**:
  - `bestsellers-page` (Div): Container for bestsellers page
  - `bestsellers-list` (Div): Ranked list of top-selling books
  - `time-period-filter` (Dropdown): Filter by time period (This Week, This Month, All Time)
  - `view-book-button-{book_id}` (Button): View book details
  - `back-to-dashboard` (Button): Navigate back to dashboard
- **Context Variables**:
  - `bestsellers` (list of dict)
  - `time_period` (str)
- **Navigation**:
  - Each `view-book-button-{book_id}` triggers URL: `url_for('book_details', book_id=book_id)`
  - `back-to-dashboard` triggers URL: `url_for('dashboard')`


## Section 3: Data Schemas Specification

Data files located in `data/` directory, pipe-delimited (`|`). No headers; parsing starts from first line.

---

1. **books.txt**
   - **Path**: `data/books.txt`
   - **Format**: `book_id|title|author|isbn|category|price|stock|description`
   - **Description**: Stores details of each book available in the store.
   - **Fields**:
     1. `book_id` (int)
     2. `title` (str)
     3. `author` (str)
     4. `isbn` (str)
     5. `category` (str)
     6. `price` (float)
     7. `stock` (int) - number of available copies
     8. `description` (str)
   - **Examples**:
     - `1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel`
     - `2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind`
     - `3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction`

---

2. **categories.txt**
   - **Path**: `data/categories.txt`
   - **Format**: `category_id|category_name|description`
   - **Description**: Stores book category information.
   - **Fields**:
     1. `category_id` (int)
     2. `category_name` (str)
     3. `description` (str)
   - **Examples**:
     - `1|Fiction|Fictional narratives and novels`
     - `2|Non-Fiction|Factual and educational books`
     - `3|Science|Scientific topics and research`

---

3. **cart.txt**
   - **Path**: `data/cart.txt`
   - **Format**: `cart_id|book_id|quantity|added_date`
   - **Description**: Stores current shopping cart items.
   - **Fields**:
     1. `cart_id` (int) - unique identifier of cart record
     2. `book_id` (int)
     3. `quantity` (int)
     4. `added_date` (str - YYYY-MM-DD)
   - **Examples**:
     - `1|1|2|2025-01-15`
     - `2|3|1|2025-01-16`

---

4. **orders.txt**
   - **Path**: `data/orders.txt`
   - **Format**: `order_id|customer_name|order_date|total_amount|status|shipping_address`
   - **Description**: Stores all customer orders.
   - **Fields**:
     1. `order_id` (int)
     2. `customer_name` (str)
     3. `order_date` (str - YYYY-MM-DD)
     4. `total_amount` (float)
     5. `status` (str) - e.g. "Pending", "Shipped", "Delivered"
     6. `shipping_address` (str)
   - **Examples**:
     - `1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001`
     - `2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001`

---

5. **order_items.txt**
   - **Path**: `data/order_items.txt`
   - **Format**: `order_item_id|order_id|book_id|quantity|price`
   - **Description**: Stores individual items per order.
   - **Fields**:
     1. `order_item_id` (int)
     2. `order_id` (int)
     3. `book_id` (int)
     4. `quantity` (int)
     5. `price` (float) - price of the book at the time of order
   - **Examples**:
     - `1|1|1|2|12.99`
     - `2|1|3|1|14.99`
     - `3|2|2|1|16.99`

---

6. **reviews.txt**
   - **Path**: `data/reviews.txt`
   - **Format**: `review_id|book_id|customer_name|rating|review_text|review_date`
   - **Description**: Stores customer reviews for books.
   - **Fields**:
     1. `review_id` (int)
     2. `book_id` (int)
     3. `customer_name` (str)
     4. `rating` (int) - from 1 to 5
     5. `review_text` (str)
     6. `review_date` (str - YYYY-MM-DD)
   - **Examples**:
     - `1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12`
     - `2|2|Bob Williams|4|Very informative and well-written.|2025-01-13`
     - `3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15`

---

7. **bestsellers.txt**
   - **Path**: `data/bestsellers.txt`
   - **Format**: `book_id|sales_count|period`
   - **Description**: Stores top selling books by time period.
   - **Fields**:
     1. `book_id` (int)
     2. `sales_count` (int)
     3. `period` (str) - e.g., "This Week", "This Month", "All Time"
   - **Examples**:
     - `2|150|This Month`
     - `1|120|This Month`
     - `3|95|This Month`

---

# End of Design Specification
