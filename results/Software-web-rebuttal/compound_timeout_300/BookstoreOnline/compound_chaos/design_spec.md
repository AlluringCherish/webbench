# BookstoreOnline Design Specification

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path**: `/`
- **Function Name**: `root_redirect`
- **HTTP Methods**: GET
- **Template Rendered**: None (Redirect)
- **Context Variables**: None
- **Behavior**: Redirects permanently (HTTP 302) to `/dashboard`

---

### 2. Dashboard Page
- **Route Path**: `/dashboard`
- **Function Name**: `dashboard`
- **HTTP Methods**: GET
- **Template Rendered**: `dashboard.html`
- **Context Variables**:
  - `featured_books` (list of dict): Each dict contains book fields: `book_id`(int), `title`(str), `author`(str), `price`(float), `cover_url`(str, optional if used)
  - `bestsellers` (list of dict): Each dict: `book_id`(int), `title`(str), `author`(str), `sales_count`(int)

---

### 3. Book Catalog Page
- **Route Path**: `/catalog`
- **Function Name**: `catalog`
- **HTTP Methods**: GET
- **Template Rendered**: `catalog.html`
- **Context Variables**:
  - `books` (list of dict): Each dict: `book_id`(int), `title`(str), `author`(str), `price`(float)
  - `categories` (list of dict): Each dict: `category_id`(int), `category_name`(str)
  - `selected_category` (str or None): Name of category filtered or None
  - `search_query` (str or None): Search string or None

- **Search and Filtering**: Use query parameters `search` and `category` to filter books by title, author, or ISBN and category

---

### 4. Book Details Page
- **Route Path**: `/book/<int:book_id>`
- **Function Name**: `book_details`
- **HTTP Methods**: GET, POST
- **Template Rendered**: `book_details.html`
- **Context Variables**:
  - `book` (dict): Fields - `book_id`(int), `title`(str), `author`(str), `price`(float), `description`(str), `stock`(int)
  - `reviews` (list of dict): Each dict: `review_id`(int), `customer_name`(str), `rating`(int), `review_text`(str), `review_date`(str)

- **POST Handling**:
  - When form or AJAX call to add book to cart (triggered by `add-to-cart-button`), add the book with quantity=1 to `cart.txt` or update quantity if exists.
  - Redirect or reload page after POST.

---

### 5. Shopping Cart Page
- **Route Path**: `/cart`
- **Function Name**: `cart`
- **HTTP Methods**: GET, POST
- **Template Rendered**: `cart.html`
- **Context Variables**:
  - `cart_items` (list of dict): Each dict: `cart_id`(int), `book_id`(int), `title`(str), `quantity`(int), `price`(float), `subtotal`(float)
  - `total_amount` (float): Sum of all subtotals

- **POST Handling**:
  - Form submissions can update quantities (`update-quantity-{item_id}` inputs) or remove items (`remove-item-button-{item_id}` buttons).
  - Update or remove cart items in `cart.txt` accordingly.
  - Redirect after POST.

---

### 6. Checkout Page
- **Route Path**: `/checkout`
- **Function Name**: `checkout`
- **HTTP Methods**: GET, POST
- **Template Rendered**: `checkout.html`
- **Context Variables**:
  - `cart_items` (list of dict): Same as cart page
  - `total_amount` (float): Sum of cart item subtotals

- **POST Handling**:
  - Process order submission with form fields:
    - `customer_name` (str), `shipping_address` (str), `payment_method` (str from "Credit Card", "PayPal", "Bank Transfer")
  - Create new order in `orders.txt`, and create corresponding entries in `order_items.txt`.
  - Clear cart items from `cart.txt`.
  - Redirect to `/order_history`

---

### 7. Order History Page
- **Route Path**: `/order_history`
- **Function Name**: `order_history`
- **HTTP Methods**: GET
- **Template Rendered**: `order_history.html`
- **Context Variables**:
  - `orders` (list of dict): Each dict: `order_id`(int), `customer_name`(str), `order_date`(str), `total_amount`(float), `status`(str), `shipping_address`(str)
  - `status_filter` (str): One of "All", "Pending", "Shipped", "Delivered" (default "All")

- **Filtering**: Apply filter by `status` query parameter

---

### 8. Order Details Page (Optional but beneficial for `/order_history` view button)
- **Route Path**: `/order/<int:order_id>`
- **Function Name**: `order_details`
- **HTTP Methods**: GET
- **Template Rendered**: `order_details.html` (not explicitly requested in user task but inferred to view order details)
- **Context Variables**:
  - `order` (dict): Same fields as `orders` above
  - `order_items` (list of dict): Each dict: `order_item_id`(int), `book_id`(int), `title`(str), `quantity`(int), `price`(float), `subtotal`(float)

---

### 9. Reviews Page
- **Route Path**: `/reviews`
- **Function Name**: `reviews`
- **HTTP Methods**: GET
- **Template Rendered**: `reviews.html`
- **Context Variables**:
  - `reviews` (list of dict): Each dict: `review_id`(int), `book_title`(str), `rating`(int), `review_text`(str)
  - `rating_filter` (str): Rating filter from query param, e.g. "All", "5", "4", ...

- **Filtering**: Use `rating` query param to filter reviews

---

### 10. Write Review Page
- **Route Path**: `/write_review`
- **Function Name**: `write_review`
- **HTTP Methods**: GET, POST
- **Template Rendered**: `write_review.html`
- **Context Variables**:
  - `purchasable_books` (list of dict): Purchased books available for review with fields: `book_id`(int), `title`(str)

- **POST Handling**:
  - Form fields: `book_id` (int), `rating` (int 1-5), `review_text` (str), `customer_name` (Str, can be static or asked elsewise, no auth is specified, assumed user name submission with review or fixed name)
  - Append to `reviews.txt` with new review_id
  - Redirect to `/reviews`

---

### 11. Bestsellers Page
- **Route Path**: `/bestsellers`
- **Function Name**: `bestsellers`
- **HTTP Methods**: GET
- **Template Rendered**: `bestsellers.html`
- **Context Variables**:
  - `bestsellers` (list of dict): Each dict: `book_id`(int), `title`(str), `author`(str), `sales_count`(int)
  - `time_period` (str): Filter by period from query param ("This Week", "This Month", "All Time")

- **Filtering**: Use query param for time period filter


---

## Section 2: HTML Templates Specification

### 1. Dashboard Page Template
- **File Path**: `templates/dashboard.html`
- **Page Title**: `Bookstore Dashboard`
- **Main H1**: `Bookstore Dashboard`
- **Element IDs**:
  - `dashboard-page` (Div): Container div for dashboard
  - `featured-books` (Div): Displays featured book recommendations
  - `browse-catalog-button` (Button): Navigates to `/catalog`
  - `view-cart-button` (Button): Navigates to `/cart`
  - `bestsellers-button` (Button): Navigates to `/bestsellers`
- **Context Variables**:
  - `featured_books` (list of dict)
  - `bestsellers` (list of dict)
- **Navigation**:
  - `browse-catalog-button` calls `url_for('catalog')`
  - `view-cart-button` calls `url_for('cart')`
  - `bestsellers-button` calls `url_for('bestsellers')`
- **Implementation notes**:
  - List featured books with title, author, and price inside `featured-books` div.
  - Display bestsellers (top ranked) with rank, title, author, sales count.

---

### 2. Book Catalog Page Template
- **File Path**: `templates/catalog.html`
- **Page Title**: `Book Catalog`
- **Main H1**: `Book Catalog`
- **Element IDs**:
  - `catalog-page` (Div): Container div
  - `search-input` (Input): Text input for search query
  - `category-filter` (Dropdown select): For category filtering
  - `books-grid` (Div): Holds book cards
  - Dynamic: `view-book-button-{book_id}` (Button): In each book card, to view details
- **Context Variables**:
  - `books` (list of dict)
  - `categories` (list of dict)
  - `selected_category` (str or None)
  - `search_query` (str or None)
- **Navigation**:
  - Book detail buttons use `url_for('book_details', book_id=book['book_id'])`
- **Filtering/Search**:
  - Search input and category dropdown submit on change or submit button to reload page with query params.

---

### 3. Book Details Page Template
- **File Path**: `templates/book_details.html`
- **Page Title**: `Book Details`
- **Main H1**: `book['title']` (dynamic)
- **Element IDs**:
  - `book-details-page` (Div): Container
  - `book-title` (H1): Displays book title dynamically
  - `book-author` (Div): Displays author
  - `book-price` (Div): Displays price
  - `add-to-cart-button` (Button): Adds book to cart via POST
  - `book-reviews` (Div): Lists customer reviews
- **Context Variables**:
  - `book` (dict)
  - `reviews` (list of dict)
- **POST Form**: 
  - Wrap the add to cart button inside a form with method POST.
  - Include hidden input for `book_id`.

---

### 4. Shopping Cart Page Template
- **File Path**: `templates/cart.html`
- **Page Title**: `Shopping Cart`
- **Main H1**: `Shopping Cart`
- **Element IDs**:
  - `cart-page` (Div): Container
  - `cart-items-table` (Table): Lists cart items with columns: Title, Quantity, Price, Subtotal
  - Dynamic inputs: `update-quantity-{item_id}` (Input number) for quantity
  - Dynamic buttons: `remove-item-button-{item_id}` (Button) to remove item
  - `proceed-checkout-button` (Button): Navigates to `/checkout`
  - `total-amount` (Div): Displays total cart amount
- **Context Variables**:
  - `cart_items` (list of dict)
  - `total_amount` (float)
- **POST Form**:
  - Wrap the cart items table in a form with method POST.
  - Each quantity input named as `quantity_{cart_id}` to update quantities.
  - Each remove button named as `remove_{cart_id}`.

---

### 5. Checkout Page Template
- **File Path**: `templates/checkout.html`
- **Page Title**: `Checkout`
- **Main H1**: `Checkout`
- **Element IDs**:
  - `checkout-page` (Div): Container
  - `customer-name` (Input): For customer name
  - `shipping-address` (Textarea): For address
  - `payment-method` (Dropdown select): Options - Credit Card, PayPal, Bank Transfer
  - `place-order-button` (Button): To submit form
- **Context Variables**:
  - `cart_items` (list of dict)
  - `total_amount` (float)
- **POST Form**:
  - All inputs and button inside a form method POST.

---

### 6. Order History Page Template
- **File Path**: `templates/order_history.html`
- **Page Title**: `Order History`
- **Main H1**: `Order History`
- **Element IDs**:
  - `orders-page` (Div): Container
  - `orders-table` (Table): Columns - Order ID, Date, Total Amount, Status
  - Dynamic buttons: `view-order-button-{order_id}`
  - `order-status-filter` (Dropdown): Filters by order status
  - `back-to-dashboard` (Button): Navigates to `/dashboard`
- **Context Variables**:
  - `orders` (list of dict)
  - `status_filter` (str)
- **Navigation**:
  - View order buttons link to `/order/<order_id>` (if implemented) or can be a placeholder.

---

### 7. Reviews Page Template
- **File Path**: `templates/reviews.html`
- **Page Title**: `Customer Reviews`
- **Main H1**: `Customer Reviews`
- **Element IDs**:
  - `reviews-page` (Div): Container
  - `reviews-list` (Div): Lists reviews with book title, rating, review text
  - `write-review-button` (Button): Navigates to `/write_review`
  - `filter-by-rating` (Dropdown): Filters reviews by rating
  - `back-to-dashboard` (Button): Navigates to `/dashboard`
- **Context Variables**:
  - `reviews` (list of dict)
  - `rating_filter` (str)
- **Navigation**:
  - `write-review-button` calls `url_for('write_review')`

---

### 8. Write Review Page Template
- **File Path**: `templates/write_review.html`
- **Page Title**: `Write a Review`
- **Main H1**: `Write a Review`
- **Element IDs**:
  - `write-review-page` (Div): Container
  - `select-book` (Dropdown select): To select book to review
  - `rating-select` (Dropdown select): Ratings from 1 to 5
  - `review-text` (Textarea): For review text
  - `submit-review-button` (Button): Submit review
- **Context Variables**:
  - `purchasable_books` (list of dict)
- **POST Form**:
  - All inputs and submit button inside a form method POST.

---

### 9. Bestsellers Page Template
- **File Path**: `templates/bestsellers.html`
- **Page Title**: `Bestsellers`
- **Main H1**: `Bestsellers`
- **Element IDs**:
  - `bestsellers-page` (Div): Container
  - `bestsellers-list` (Div): Ranked list of bestsellers with rank, title, author, sales count
  - `time-period-filter` (Dropdown): Select period - This Week, This Month, All Time
  - Dynamic: `view-book-button-{book_id}` (Button): View book details
  - `back-to-dashboard` (Button): Navigates to `/dashboard`
- **Context Variables**:
  - `bestsellers` (list of dict)
  - `time_period` (str)
- **Navigation**:
  - Buttons link to `url_for('book_details', book_id=book_id)`

---

## Section 3: Data Schemas Specification

### 1. Books Data
- **File Location**: `data/books.txt`
- **Format**: Pipe (`|`) delimited, no header, fields in this exact order:
  ```
  book_id|title|author|isbn|category|price|stock|description
  ```
- **Field Descriptions**:
  - `book_id` (int): Unique ID
  - `title` (str): Book title
  - `author` (str): Author name
  - `isbn` (str): ISBN number
  - `category` (str): Book category
  - `price` (float): Price in dollars
  - `stock` (int): Number of copies in stock
  - `description` (str): Short book description
- **Example Rows**:
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

---

### 2. Categories Data
- **File Location**: `data/categories.txt`
- **Format**: Pipe (`|`) delimited, no header, fields in this exact order:
  ```
  category_id|category_name|description
  ```
- **Field Descriptions**:
  - `category_id` (int): Unique ID
  - `category_name` (str): Category name
  - `description` (str): Description of category
- **Example Rows**:
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

---

### 3. Cart Data
- **File Location**: `data/cart.txt`
- **Format**: Pipe (`|`) delimited, no header, fields in this exact order:
  ```
  cart_id|book_id|quantity|added_date
  ```
- **Field Descriptions**:
  - `cart_id` (int): Unique cart item ID
  - `book_id` (int): Book reference
  - `quantity` (int): Quantity selected
  - `added_date` (str, format YYYY-MM-DD): Date added to cart
- **Example Rows**:
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

---

### 4. Orders Data
- **File Location**: `data/orders.txt`
- **Format**: Pipe (`|`) delimited, no header, fields in this exact order:
  ```
  order_id|customer_name|order_date|total_amount|status|shipping_address
  ```
- **Field Descriptions**:
  - `order_id` (int): Unique order ID
  - `customer_name` (str): Name of customer
  - `order_date` (str, format YYYY-MM-DD): Date of order
  - `total_amount` (float): Total order amount
  - `status` (str): Order status (Pending, Shipped, Delivered)
  - `shipping_address` (str): Shipping address
- **Example Rows**:
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

---

### 5. Order Items Data
- **File Location**: `data/order_items.txt`
- **Format**: Pipe (`|`) delimited, no header, fields in this exact order:
  ```
  order_item_id|order_id|book_id|quantity|price
  ```
- **Field Descriptions**:
  - `order_item_id` (int): Unique ID for order item
  - `order_id` (int): Related order ID
  - `book_id` (int): Book reference
  - `quantity` (int): Quantity ordered
  - `price` (float): Price at time of purchase
- **Example Rows**:
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

---

### 6. Reviews Data
- **File Location**: `data/reviews.txt`
- **Format**: Pipe (`|`) delimited, no header, fields in this exact order:
  ```
  review_id|book_id|customer_name|rating|review_text|review_date
  ```
- **Field Descriptions**:
  - `review_id` (int): Unique review ID
  - `book_id` (int): Book reviewed
  - `customer_name` (str): Name of reviewer
  - `rating` (int): Rating 1 to 5
  - `review_text` (str): Text of review
  - `review_date` (str, format YYYY-MM-DD): Date of review
- **Example Rows**:
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

---

### 7. Bestsellers Data
- **File Location**: `data/bestsellers.txt`
- **Format**: Pipe (`|`) delimited, no header, fields in this exact order:
  ```
  book_id|sales_count|period
  ```
- **Field Descriptions**:
  - `book_id` (int): Book reference
  - `sales_count` (int): Number of sales
  - `period` (str): Time period (e.g., "This Week", "This Month", "All Time")
- **Example Rows**:
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

# End of Design Specification
