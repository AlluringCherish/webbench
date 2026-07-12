# BookstoreOnline - Design Specification Document

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Method:** GET
- **Template Rendered:** Redirect to `/dashboard`
- **Context Variables:** None
- **Notes:** Redirects to the Dashboard page.


### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** `dashboard`
- **HTTP Method:** GET
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `featured_books` (list of dict): List of featured book objects.
  - `bestsellers` (list of dict): List of bestseller book objects.
- **Form Handling:** None


### 3. Book Catalog Page
- **Route Path:** `/catalog`
- **Function Name:** `catalog`
- **HTTP Method:** GET
- **Template Rendered:** `catalog.html`
- **Context Variables:**
  - `books` (list of dict): List of all available book objects.
  - `categories` (list of dict): List of category objects for filtering.
  - `search_query` (str): Current search string (if any).
  - `selected_category` (str): Selected category filter (if any).
- **Form Handling:**
  - Search and filter parameters sent as query parameters (e.g., `/catalog?search=...&category=...`).


### 4. Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** `book_details`
- **HTTP Method:** GET, POST
- **Template Rendered:** `book_details.html`
- **Context Variables:**
  - `book` (dict): Detailed book object for given `book_id`.
  - `reviews` (list of dict): List of reviews for the book.
- **Form Handling:**
  - POST used for "Add to Cart" action.
  - Form submits book_id and quantity (default 1) to add the book to cart.


### 5. Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** `shopping_cart`
- **HTTP Method:** GET, POST
- **Template Rendered:** `cart.html`
- **Context Variables:**
  - `cart_items` (list of dict): List of cart item objects including book info and quantity.
  - `total_amount` (float): Total price of all items in the cart.
- **Form Handling:**
  - POST handles update quantity or remove item operations.
  - Form identifies item by `cart_id` or equivalent and new quantity or remove command.


### 6. Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** `checkout`
- **HTTP Method:** GET, POST
- **Template Rendered:** `checkout.html`
- **Context Variables:**
  - None for GET.
- **Form Handling:**
  - POST receives customer_name (str), shipping_address (str), payment_method (str).
  - On successful POST, creates an order, clears cart, and redirects to Order History page.


### 7. Order History Page
- **Route Path:** `/orders`
- **Function Name:** `order_history`
- **HTTP Method:** GET
- **Template Rendered:** `orders.html`
- **Context Variables:**
  - `orders` (list of dict): List of all orders.
  - `status_filter` (str): Current status filter (e.g., All, Pending, Shipped, Delivered).
- **Form Handling:**
  - Filtering done via query parameters (e.g., `/orders?status=Shipped`).


### 8. View Order Details (Optional based on UI – since buttons exist)
- **Route Path:** `/orders/<int:order_id>`
- **Function Name:** `order_details`
- **HTTP Method:** GET
- **Template Rendered:** `order_details.html` (not described in UI but logically needed)
- **Context Variables:**
  - `order` (dict): The order record.
  - `order_items` (list of dict): List of items in this order.
- **Form Handling:** None


### 9. Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** `reviews`
- **HTTP Method:** GET
- **Template Rendered:** `reviews.html`
- **Context Variables:**
  - `reviews_list` (list of dict): List of all reviews.
  - `filter_rating` (str): Rating filter (All, 5, 4, 3...)
- **Form Handling:**
  - Filtering reviews via query parameters (e.g., `/reviews?rating=5`).


### 10. Write Review Page
- **Route Path:** `/write_review`
- **Function Name:** `write_review`
- **HTTP Method:** GET, POST
- **Template Rendered:** `write_review.html`
- **Context Variables:**
  - `purchased_books` (list of dict): List of books eligible for review (purchased).
- **Form Handling:**
  - POST submits `book_id` (int), `rating` (int), `review_text` (str).
  - On success, new review is stored, redirect back to Reviews page.


### 11. Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** `bestsellers`
- **HTTP Method:** GET
- **Template Rendered:** `bestsellers.html`
- **Context Variables:**
  - `bestsellers_list` (list of dict): List of top-selling books with sales count.
  - `time_period` (str): Selected time period filter (e.g., This Week, This Month, All Time).
- **Form Handling:**
  - Filtering by time period via query parameters (e.g., `/bestsellers?period=This Month`).

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page Template
- **File Path:** `templates/dashboard.html`
- **Page Title:** `Bookstore Dashboard`
- **Main H1 Heading:** `Bookstore Dashboard`
- **Element IDs:**
  - `dashboard-page`: Div - Container for the entire dashboard page.
  - `featured-books`: Div - Displays featured book recommendations.
  - `browse-catalog-button`: Button - Navigates to `/catalog`.
  - `view-cart-button`: Button - Navigates to `/cart`.
  - `bestsellers-button`: Button - Navigates to `/bestsellers`.
- **Context Variables:**
  - `featured_books` (list of dict)
  - `bestsellers` (list of dict)
- **Navigation:**
  - `browse-catalog-button`: Link/button uses `url_for('catalog')`.
  - `view-cart-button`: Link/button uses `url_for('shopping_cart')`.
  - `bestsellers-button`: Link/button uses `url_for('bestsellers')`.


### 2. Book Catalog Page Template
- **File Path:** `templates/catalog.html`
- **Page Title:** `Book Catalog`
- **Main H1 Heading:** `Book Catalog`
- **Element IDs:**
  - `catalog-page`: Div container.
  - `search-input`: Input field for search queries.
  - `category-filter`: Dropdown select for categories.
  - `books-grid`: Div for displaying book cards.
  - `view-book-button-{book_id}`: Button for each book to view its details.
- **Context Variables:**
  - `books` (list of dict with keys: book_id, title, author, isbn, category, price, stock, description)
  - `categories` (list of dict with keys: category_id, category_name, description)
  - `search_query` (str)
  - `selected_category` (str)
- **Navigation:**
  - On clicking `view-book-button-{book_id}`, navigate to `url_for('book_details', book_id=book_id)`.


### 3. Book Details Page Template
- **File Path:** `templates/book_details.html`
- **Page Title:** `Book Details`
- **Main H1 Heading:** Dynamic - book title (`book.title`)
- **Element IDs:**
  - `book-details-page`: Div container.
  - `book-title`: H1 displaying book.title.
  - `book-author`: Div displaying book.author.
  - `book-price`: Div displaying book.price.
  - `add-to-cart-button`: Button to add book to cart.
  - `book-reviews`: Div showing list of reviews.
- **Context Variables:**
  - `book` (dict)
  - `reviews` (list of dict)
- **Navigation:**
  - "Add to Cart" button posts form to `/book/<book_id>` to add book to cart.


### 4. Shopping Cart Page Template
- **File Path:** `templates/cart.html`
- **Page Title:** `Shopping Cart`
- **Main H1 Heading:** `Shopping Cart`
- **Element IDs:**
  - `cart-page`: Div container.
  - `cart-items-table`: Table with cart item rows.
  - `update-quantity-{item_id}`: Input number for quantity per cart item.
  - `remove-item-button-{item_id}`: Button to remove an item.
  - `proceed-checkout-button`: Button navigates to `/checkout`.
  - `total-amount`: Div displaying the total cart price.
- **Context Variables:**
  - `cart_items` (list of dict with keys: cart_id, book_id, title, quantity, price, subtotal)
  - `total_amount` (float)
- **Navigation:**
  - `proceed-checkout-button` uses `url_for('checkout')`.
  - Forms for updating quantity or removing items post to `/cart`.


### 5. Checkout Page Template
- **File Path:** `templates/checkout.html`
- **Page Title:** `Checkout`
- **Main H1 Heading:** `Checkout`
- **Element IDs:**
  - `checkout-page`: Div container.
  - `customer-name`: Input for customer name.
  - `shipping-address`: Textarea for address.
  - `payment-method`: Dropdown (Credit Card, PayPal, Bank Transfer).
  - `place-order-button`: Button to submit form.
- **Context Variables:** None
- **Form Structure:**
  - POST form containing all above fields, submitted to `/checkout`.


### 6. Order History Page Template
- **File Path:** `templates/orders.html`
- **Page Title:** `Order History`
- **Main H1 Heading:** `Order History`
- **Element IDs:**
  - `orders-page`: Div container.
  - `orders-table`: Table with order rows.
  - `view-order-button-{order_id}`: Button to view order details.
  - `order-status-filter`: Dropdown (All, Pending, Shipped, Delivered).
  - `back-to-dashboard`: Button navigates to `/dashboard`.
- **Context Variables:**
  - `orders` (list of dict with keys: order_id, customer_name, order_date, total_amount, status, shipping_address)
  - `status_filter` (str)
- **Navigation:**
  - `view-order-button-{order_id}` navigates to `/orders/<order_id>` (if implemented)
  - `back-to-dashboard` uses `url_for('dashboard')`.


### 7. Reviews Page Template
- **File Path:** `templates/reviews.html`
- **Page Title:** `Customer Reviews`
- **Main H1 Heading:** `Customer Reviews`
- **Element IDs:**
  - `reviews-page`: Div container.
  - `reviews-list`: Div listing all reviews.
  - `write-review-button`: Button navigates to `/write_review`.
  - `filter-by-rating`: Dropdown (All, 5 stars, 4 stars, etc.).
  - `back-to-dashboard`: Button navigates to `/dashboard`.
- **Context Variables:**
  - `reviews_list` (list of dict with keys: review_id, book_title, rating, review_text, review_date)
  - `filter_rating` (str)
- **Navigation:**
  - `write-review-button` uses `url_for('write_review')`.
  - `back-to-dashboard` uses `url_for('dashboard')`.


### 8. Write Review Page Template
- **File Path:** `templates/write_review.html`
- **Page Title:** `Write a Review`
- **Main H1 Heading:** `Write a Review`
- **Element IDs:**
  - `write-review-page`: Div container.
  - `select-book`: Dropdown to select a book to review.
  - `rating-select`: Dropdown to select a rating (1-5).
  - `review-text`: Textarea for review text.
  - `submit-review-button`: Button to submit review.
- **Context Variables:**
  - `purchased_books` (list of dict with keys: book_id, title)
- **Form Structure:**
  - POST form submits to `/write_review` with fields book_id, rating, review_text.


### 9. Bestsellers Page Template
- **File Path:** `templates/bestsellers.html`
- **Page Title:** `Bestsellers`
- **Main H1 Heading:** `Bestsellers`
- **Element IDs:**
  - `bestsellers-page`: Div container.
  - `bestsellers-list`: Div listing bestseller books ranked.
  - `time-period-filter`: Dropdown (This Week, This Month, All Time).
  - `view-book-button-{book_id}`: Button to view book details.
  - `back-to-dashboard`: Button navigates to `/dashboard`.
- **Context Variables:**
  - `bestsellers_list` (list of dict with keys: book_id, title, author, sales_count)
  - `time_period` (str)
- **Navigation:**
  - `view-book-button-{book_id}` uses `url_for('book_details', book_id=book_id)`.
  - `back-to-dashboard` uses `url_for('dashboard')`.

---

## Section 3: Data Schemas Specification

### 1. Books Data
- **File Path:** `data/books.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `category` (str)
  6. `price` (float)
  7. `stock` (int)
  8. `description` (str)
- **Description:** Stores detailed book information.
- **Example Rows:**
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```


### 2. Categories Data
- **File Path:** `data/categories.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- **Description:** Stores category information for filtering books.
- **Example Rows:**
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```


### 3. Cart Data
- **File Path:** `data/cart.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `cart_id` (int)
  2. `book_id` (int)
  3. `quantity` (int)
  4. `added_date` (str - YYYY-MM-DD)
- **Description:** Stores current shopping cart items.
- **Example Rows:**
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```


### 4. Orders Data
- **File Path:** `data/orders.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `order_id` (int)
  2. `customer_name` (str)
  3. `order_date` (str - YYYY-MM-DD)
  4. `total_amount` (float)
  5. `status` (str) - e.g., Pending, Shipped, Delivered
  6. `shipping_address` (str)
- **Description:** Stores order records with shipping info and status.
- **Example Rows:**
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```


### 5. Order Items Data
- **File Path:** `data/order_items.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `order_item_id` (int)
  2. `order_id` (int)
  3. `book_id` (int)
  4. `quantity` (int)
  5. `price` (float) - price per unit when ordered
- **Description:** Stores individual items belonging to orders.
- **Example Rows:**
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```


### 6. Reviews Data
- **File Path:** `data/reviews.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `review_id` (int)
  2. `book_id` (int)
  3. `customer_name` (str)
  4. `rating` (int) (1-5)
  5. `review_text` (str)
  6. `review_date` (str - YYYY-MM-DD)
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
- **Fields:**
  1. `book_id` (int)
  2. `sales_count` (int)
  3. `period` (str) - Time period (This Week, This Month, All Time)
- **Description:** Stores top-selling books ranked by sales count in a time period.
- **Example Rows:**
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

# End of Design Specification
