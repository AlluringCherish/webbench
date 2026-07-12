# BookstoreOnline Design Specification

---

## Section 1: Flask Routes Specification

### 1. Dashboard
- Route Path: `/`
- Function Name: `dashboard`
- HTTP Methods: GET
- Template Rendered: `dashboard.html`
- Context Variables:
  - `featured_books` (List[Dict]): List of featured books with keys `book_id`, `title`, `author`, `price`.
- POST Behavior: None

### 2. Book Catalog
- Route Path: `/catalog`
- Function Name: `book_catalog`
- HTTP Methods: GET, POST
- Template Rendered: `catalog.html`
- Context Variables:
  - `books` (List[Dict]): List of books filtered/searched.
  - `categories` (List[Dict]): List of available categories.
  - `selected_category` (str|None): Currently selected category ID or None.
  - `search_query` (str): Current search string.
- POST Behavior: Handles search and filter submissions, updates displayed books accordingly.

### 3. Book Details
- Route Path: `/book/<int:book_id>`
- Function Name: `book_details`
- HTTP Methods: GET, POST
- Template Rendered: `details.html`
- Context Variables:
  - `book` (Dict): Book details.
  - `reviews` (List[Dict]): Related customer reviews for the book.
- POST Behavior: Allows adding book to cart triggered by button `add-to-cart-button`.

### 4. Shopping Cart
- Route Path: `/cart`
- Function Name: `shopping_cart`
- HTTP Methods: GET, POST
- Template Rendered: `cart.html`
- Context Variables:
  - `cart_items` (List[Dict]): Cart items, each with `item_id`, `book_id`, `title`, `quantity`, `price`, and `subtotal`.
  - `total_amount` (float): Total cart price.
- POST Behavior: Handles updates to item quantity via input IDs `update-quantity-{item_id}` and removal of items via buttons `remove-item-button-{item_id}`.

### 5. Checkout
- Route Path: `/checkout`
- Function Name: `checkout`
- HTTP Methods: GET, POST
- Template Rendered: `checkout.html`
- Context Variables: None
- POST Behavior: Processes submitted customer name, shipping address, and payment method via form with `place-order-button`.

### 6. Order History
- Route Path: `/orders`
- Function Name: `order_history`
- HTTP Methods: GET, POST
- Template Rendered: `history.html`
- Context Variables:
  - `orders` (List[Dict]): List of customer orders.
  - `status_filter` (str): Current status filter (All, Pending, Shipped, Delivered).
- POST Behavior: Filtering by order status and viewing order details triggered by button `view-order-button-{order_id}`.

### 7. Reviews
- Route Path: `/reviews`
- Function Name: `reviews`
- HTTP Methods: GET, POST
- Template Rendered: `reviews.html`
- Context Variables:
  - `reviews` (List[Dict]): Customer reviews.
  - `rating_filter` (str|int): Star rating filter selected.
- POST Behavior: Filter reviews by rating dropdown, navigate to write review via `write-review-button`.

### 8. Write Review
- Route Path: `/write_review`
- Function Name: `write_review`
- HTTP Methods: GET, POST
- Template Rendered: `write_review.html`
- Context Variables:
  - `purchased_books` (List[Dict]): Books eligible for reviews.
- POST Behavior: Review submission handling with fields `select-book`, `rating-select`, `review-text` and `submit-review-button`.

### 9. Bestsellers
- Route Path: `/bestsellers`
- Function Name: `bestsellers`
- HTTP Methods: GET, POST
- Template Rendered: `bestsellers.html`
- Context Variables:
  - `bestsellers` (List[Dict]): List of bestselling books.
  - `time_period` (str): Selected time period filter.
- POST Behavior: Handles time period filter and book detail views.

---

## Section 2: HTML Templates Specification

### dashboard.html
- File path: `templates/dashboard.html`
- Page title: "Bookstore Dashboard"
- Main heading: `<h1>Bookstore Dashboard</h1>`
- Element IDs:
  - `dashboard-page` (Div): Main container
  - `featured-books` (Div): Displays featured books
  - `browse-catalog-button` (Button): Navigates to `/catalog`
  - `view-cart-button` (Button): Navigates to `/cart`
  - `bestsellers-button` (Button): Navigates to `/bestsellers`
- Context variables: `featured_books`
- Navigation via `url_for` calls to respective routes
- No forms

### catalog.html
- File path: `templates/catalog.html`
- Page title: "Book Catalog"
- Main heading: `<h1>Book Catalog</h1>`
- Element IDs:
  - `catalog-page` (Div): Main container
  - `search-input` (Input): Text search input
  - `category-filter` (Dropdown): Category filter
  - `books-grid` (Div): Container for book cards
  - `view-book-button-{book_id}` (Button): View book details button per book
- Context variables: `books`, `categories`, `selected_category`, `search_query`
- Buttons navigation via `url_for('book_details', book_id=book_id)`
- Search and filter via POST form submission

### details.html
- File path: `templates/details.html`
- Page title: "Book Details"
- Main heading: `<h1 id="book-title">{{ book.title }}</h1>`
- Element IDs:
  - `book-details-page` (Div): Container
  - `book-author` (Div): Book author
  - `book-price` (Div): Book price
  - `add-to-cart-button` (Button): Adds book to cart (POST button)
  - `book-reviews` (Div): Displays reviews
- Context variables: `book`, `reviews`
- POST form with `add-to-cart-button` to add the book to the cart

### cart.html
- File path: `templates/cart.html`
- Page title: "Shopping Cart"
- Main heading: `<h1>Shopping Cart</h1>`
- Element IDs:
  - `cart-page` (Div): Main container
  - `cart-items-table` (Table): Displays cart items
  - `update-quantity-{item_id}` (Input Number): Quantity input for each cart item
  - `remove-item-button-{item_id}` (Button): Button to remove item from cart
  - `proceed-checkout-button` (Button): Proceeds to checkout
  - `total-amount` (Div): Displays total amount
- Context variables: `cart_items`, `total_amount`
- POST forms for quantity update and removal

### checkout.html
- File path: `templates/checkout.html`
- Page title: "Checkout"
- Main heading: `<h1>Checkout</h1>`
- Element IDs:
  - `checkout-page` (Div): Container
  - `customer-name` (Input): Customer name input
  - `shipping-address` (Textarea): Shipping address input
  - `payment-method` (Dropdown): Payment method selection
  - `place-order-button` (Button): Submit order
- Context variables: None
- POST form submission

### history.html
- File path: `templates/history.html`
- Page title: "Order History"
- Main heading: `<h1>Order History</h1>`
- Element IDs:
  - `orders-page` (Div): Container
  - `orders-table` (Table): Table listing order records
  - `view-order-button-{order_id}` (Button): View order details
  - `order-status-filter` (Dropdown): Filter orders by status
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Context variables: `orders`, `status_filter`
- POST form to filter or view order

### reviews.html
- File path: `templates/reviews.html`
- Page title: "Customer Reviews"
- Main heading: `<h1>Customer Reviews</h1>`
- Element IDs:
  - `reviews-page` (Div): Container
  - `reviews-list` (Div): Contains all reviews
  - `write-review-button` (Button): Navigate to write review page
  - `filter-by-rating` (Dropdown): Filter reviews by rating
  - `back-to-dashboard` (Button): Navigate back to dashboard
- Context variables: `reviews`, `rating_filter`
- POST form submission

### write_review.html
- File path: `templates/write_review.html`
- Page title: "Write a Review"
- Main heading: `<h1>Write a Review</h1>`
- Element IDs:
  - `write-review-page` (Div): Container
  - `select-book` (Dropdown): Select book to review
  - `rating-select` (Dropdown): Select rating 1-5
  - `review-text` (Textarea): Input review text
  - `submit-review-button` (Button): Submit review
- Context variables: `purchased_books`
- POST form submission

### bestsellers.html
- File path: `templates/bestsellers.html`
- Page title: "Bestsellers"
- Main heading: `<h1>Bestsellers</h1>`
- Element IDs:
  - `bestsellers-page` (Div): Container
  - `bestsellers-list` (Div): Ranked list of bestsellers
  - `time-period-filter` (Dropdown): Filter by time period
  - `view-book-button-{book_id}` (Button): View book
  - `back-to-dashboard` (Button): Back to dashboard
- Context variables: `bestsellers`, `time_period`
- POST forms for filtering and navigation

---

## Section 3: Data Schemas Specification

### 1. books.txt
- File Path: `data/books.txt`
- Format: Pipe-delimited (`|`)
- Fields (in order):
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `category` (str)
  6. `price` (float)
  7. `stock` (int)
  8. `description` (str)
- Description: Complete book records.
- Example Rows:
```
1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
```

### 2. categories.txt
- File Path: `data/categories.txt`
- Format: Pipe-delimited
- Fields:
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- Description: Book categories.
- Example Rows:
```
1|Fiction|Fictional narratives and novels
2|Non-Fiction|Factual and educational books
3|Science|Scientific topics and research
```

### 3. cart.txt
- File Path: `data/cart.txt`
- Format: Pipe-delimited
- Fields:
  1. `cart_id` (int)
  2. `book_id` (int)
  3. `quantity` (int)
  4. `added_date` (date YYYY-MM-DD)
- Description: Current cart items.
- Example Rows:
```
1|1|2|2025-01-15
2|3|1|2025-01-16
```

### 4. orders.txt
- File Path: `data/orders.txt`
- Format: Pipe-delimited
- Fields:
  1. `order_id` (int)
  2. `customer_name` (str)
  3. `order_date` (date YYYY-MM-DD)
  4. `total_amount` (float)
  5. `status` (str)
  6. `shipping_address` (str)
- Description: Customer orders.
- Example Rows:
```
1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
```

### 5. order_items.txt
- File Path: `data/order_items.txt`
- Format: Pipe-delimited
- Fields:
  1. `order_item_id` (int)
  2. `order_id` (int)
  3. `book_id` (int)
  4. `quantity` (int)
  5. `price` (float)
- Description: Items for each order.
- Example Rows:
```
1|1|1|2|12.99
2|1|3|1|14.99
3|2|2|1|16.99
```

### 6. reviews.txt
- File Path: `data/reviews.txt`
- Format: Pipe-delimited
- Fields:
  1. `review_id` (int)
  2. `book_id` (int)
  3. `customer_name` (str)
  4. `rating` (int 1-5)
  5. `review_text` (str)
  6. `review_date` (date YYYY-MM-DD)
- Description: Customer reviews.
- Example Rows:
```
1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
```

### 7. bestsellers.txt
- File Path: `data/bestsellers.txt`
- Format: Pipe-delimited
- Fields:
  1. `book_id` (int)
  2. `sales_count` (int)
  3. `period` (str) (e.g. This Week, This Month, All Time)
- Description: Ranked sales data by period.
- Example Rows:
```
2|150|This Month
1|120|This Month
3|95|This Month
```

---

This detailed specification enables backend and frontend developers to independently implement BookstoreOnline application with exact routing, template composition, element IDs, and data file specifications.