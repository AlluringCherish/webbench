# BookstoreOnline - Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path                 | Function Name           | HTTP Method(s) | Template Rendered         | Context Variables (Name: Type)                                       | Description of Form Handling and Navigation                                       |
|----------------------------|------------------------|----------------|---------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| `/`                        | `root_redirect`         | GET            | None (redirect)            | None                                                                 | Redirects to /dashboard                                                            |
| `/dashboard`               | `dashboard`            | GET            | `dashboard.html`          | `featured_books`: list of dicts (book_id: int, title: str, author: str, price: float), `bestsellers`: list of dicts (book_id: int, title: str, author: str, sales_count: int) | Shows featured books and bestsellers. Buttons navigate to catalog, cart, bestsellers|
| `/catalog`                 | `catalog`              | GET            | `catalog.html`            | `books`: list of dicts (book_id: int, title: str, author: str, price: float, isbn: str, category: str), `categories`: list of dicts (category_id: int, category_name: str) | Displays books grid, filter/search. Uses GET query params for search/filter clear |
| `/book/<int:book_id>`      | `book_details`         | GET, POST       | `book_details.html`       | `book`: dict (book_id: int, title: str, author: str, price: float, isbn: str, category: str, description: str), `reviews`: list of dicts (customer_name: str, rating: int, review_text: str, review_date: str) | GET: Render details and reviews; POST: Add book to cart (qty default 1), redirect or flash |
| `/cart`                    | `cart`                 | GET, POST      | `cart.html`               | `cart_items`: list of dicts (item_id: int (cart_id), book_title: str, quantity: int, price: float, subtotal: float), `total_amount`: float | GET: Show cart; POST: update quantities or remove item by form inputs, then refresh           |
| `/checkout`                | `checkout`             | GET, POST      | `checkout.html`           | None (on GET); On POST accepts customer_name (str), shipping_address (str), payment_method (str) | GET: show checkout form; POST: process order placement, store order and order_items, clear cart, redirect to order history|
| `/orders`                  | `order_history`        | GET            | `orders.html`             | `orders`: list of dicts (order_id: int, customer_name: str, order_date: str, total_amount: float, status: str, shipping_address: str), `status_filter`: str | Displays order list optionally filtered by status from query param. Buttons to view order details|
| `/orders/<int:order_id>`   | `order_details`         | GET           | `order_details.html` *(note: inferred though not explicitly specified)*| `order`: dict (order_id: int, customer_name: str, order_date: str, total_amount: float, status: str, shipping_address: str), `order_items`: list of dicts (book_title: str, quantity: int, price: float) | Shows detail for specific order, accessed from order history view button|
| `/reviews`                 | `reviews`              | GET            | `reviews.html`            | `reviews`: list of dicts (book_title: str, rating: int, review_text: str, customer_name: str, review_date: str), `rating_filter`: str | Lists all reviews, filter by rating via dropdown. Button navigates to write review page|
| `/write_review`            | `write_review`         | GET, POST     | `write_review.html`       | `books`: list of dicts (book_id: int, title: str), None on POST (handles form data)  | GET: form to write review with book select, rating select, text area; POST: submit review data and redirect to reviews page |
| `/bestsellers`             | `bestsellers`           | GET            | `bestsellers.html`        | `bestsellers`: list of dicts (rank: int, book_id: int, title: str, author: str, sales_count: int), `time_period_filter`: str | Shows top-selling books ranked; filterable by time period. Back button to dashboard|

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page
- File path: `templates/dashboard.html`
- Page Title: "Bookstore Dashboard"
- Main Heading (<h1>): "Bookstore Dashboard"
- Element IDs:
  - `dashboard-page` (Div): Container for entire dashboard page
  - `featured-books` (Div): Display featured book recommendations
  - `browse-catalog-button` (Button): Navigates to `/catalog`
  - `view-cart-button` (Button): Navigates to `/cart`
  - `bestsellers-button` (Button): Navigates to `/bestsellers`
- Context variables:
  - `featured_books`: List[Dict] where each dict contains `book_id` (int), `title` (str), `author` (str), `price` (float)
  - `bestsellers`: List[Dict] with `book_id` (int), `title` (str), `author` (str), `sales_count` (int)
- Navigation mappings:
  - `browse-catalog-button`: Uses `url_for('catalog')`
  - `view-cart-button`: Uses `url_for('cart')`
  - `bestsellers-button`: Uses `url_for('bestsellers')`

### 2. Book Catalog Page
- File path: `templates/catalog.html`
- Page Title: "Book Catalog"
- Main Heading (<h1>): "Book Catalog"
- Element IDs:
  - `catalog-page` (Div): Container
  - `search-input` (Input): Searches by title, author, or ISBN
  - `category-filter` (Dropdown): Filters by category
  - `books-grid` (Div): Grid display of book cards
  - `view-book-button-{book_id}` (Button): View details for each book identified by book_id
- Context variables:
  - `books`: list of dicts with `book_id` (int), `title` (str), `author` (str), `price` (float), `isbn` (str), `category` (str)
  - `categories`: list of dicts with `category_id` (int), `category_name` (str)
- Navigation mappings:
  - `view-book-button-{book_id}`: Uses `url_for('book_details', book_id=book_id)`

### 3. Book Details Page
- File path: `templates/book_details.html`
- Page Title: "Book Details"
- Main Heading (<h1>): Element with ID `book-title` displays book title
- Element IDs:
  - `book-details-page` (Div): container
  - `book-title` (H1): displays book title
  - `book-author` (Div): displays author
  - `book-price` (Div): displays price
  - `add-to-cart-button` (Button): posts to add book to cart
  - `book-reviews` (Div): shows customer reviews
- Context variables:
  - `book`: dict with book information: keys `book_id` (int), `title`, `author`, `price` (float), `isbn`, `category`, `description` (all str)
  - `reviews`: list of dicts with keys `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str)
- Form for adding book to cart:
  - POST form triggered by `add-to-cart-button`
  - May include quantity as hidden or visible input (default 1, but not specified so assume adding single copy)

### 4. Shopping Cart Page
- File path: `templates/cart.html`
- Page Title: "Shopping Cart"
- Main Heading (<h1>): "Shopping Cart"
- Element IDs:
  - `cart-page` (Div): container
  - `cart-items-table` (Table): lists cart items with columns: title, quantity, price, subtotal
  - `update-quantity-{item_id}` (Input number): to update quantity for each cart item
  - `remove-item-button-{item_id}` (Button): to remove item
  - `proceed-checkout-button` (Button): navigate to `/checkout`
  - `total-amount` (Div): display total amount
- Context Variables:
  - `cart_items`: list of dicts: keys `item_id` (int), `book_title` (str), `quantity` (int), `price` (float), `subtotal` (float)
  - `total_amount`: float
- Form for updating cart:
  - POST form encompassing quantity updates and item removals
- Navigation:
  - `proceed-checkout-button`: uses `url_for('checkout')`

### 5. Checkout Page
- File path: `templates/checkout.html`
- Page Title: "Checkout"
- Main Heading (<h1>): "Checkout"
- Element IDs:
  - `checkout-page` (Div): container
  - `customer-name` (Input): input for customer name
  - `shipping-address` (Textarea): shipping address input
  - `payment-method` (Dropdown): select payment method; options: "Credit Card", "PayPal", "Bank Transfer"
  - `place-order-button` (Button): submits order
- Context Variables:
  - None on GET; form data on POST
- Form details:
  - Form method=POST
  - Fields: customer-name, shipping-address, payment-method
  - Submit button: place-order-button

### 6. Order History Page
- File path: `templates/orders.html`
- Page Title: "Order History"
- Main Heading (<h1>): "Order History"
- Element IDs:
  - `orders-page` (Div): container
  - `orders-table` (Table): columns: order ID, date, total amount, status
  - `view-order-button-{order_id}` (Button): view details for each order
  - `order-status-filter` (Dropdown): filter orders by status (All, Pending, Shipped, Delivered)
  - `back-to-dashboard` (Button): goes back to `/dashboard`
- Context Variables:
  - `orders`: list of dicts with `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str), `shipping_address` (str)
  - `status_filter`: str, current selected filter
- Navigation:
  - `view-order-button-{order_id}`: `url_for('order_details', order_id=order_id)` (order details inferred)
  - `back-to-dashboard`: `url_for('dashboard')`

### 7. Reviews Page
- File path: `templates/reviews.html`
- Page Title: "Customer Reviews"
- Main Heading (<h1>): "Customer Reviews"
- Element IDs:
  - `reviews-page` (Div): container
  - `reviews-list` (Div): list of reviews with book title, rating, and review text
  - `write-review-button` (Button): navigates to write review page
  - `filter-by-rating` (Dropdown): filter reviews by rating (All, 5 stars, 4 stars, etc.)
  - `back-to-dashboard` (Button): back to dashboard
- Context Variables:
  - `reviews`: list of dicts (`book_title` (str), `rating` (int), `review_text` (str), `customer_name` (str), `review_date` (str))
  - `rating_filter`: str
- Navigation:
  - `write-review-button`: `url_for('write_review')`
  - `back-to-dashboard`: `url_for('dashboard')`

### 8. Write Review Page
- File path: `templates/write_review.html`
- Page Title: "Write a Review"
- Main Heading (<h1>): "Write a Review"
- Element IDs:
  - `write-review-page` (Div): container
  - `select-book` (Dropdown): select book for review
  - `rating-select` (Dropdown): select rating (1-5 stars)
  - `review-text` (Textarea): enter review
  - `submit-review-button` (Button): submit review
- Context Variables:
  - `books`: list of dicts (`book_id` (int), `title` (str))
- Form details:
  - POST form with fields: select-book, rating-select, review-text
  - Submit button: submit-review-button

### 9. Bestsellers Page
- File path: `templates/bestsellers.html`
- Page Title: "Bestsellers"
- Main Heading (<h1>): "Bestsellers"
- Element IDs:
  - `bestsellers-page` (Div): container
  - `bestsellers-list` (Div): ranked list of books (rank, title, author, sales count)
  - `time-period-filter` (Dropdown): filter by time period (This Week, This Month, All Time)
  - `view-book-button-{book_id}` (Button): view book details
  - `back-to-dashboard` (Button): return to dashboard
- Context Variables:
  - `bestsellers`: list of dicts (`rank` (int), `book_id` (int), `title` (str), `author` (str), `sales_count` (int))
  - `time_period_filter`: str
- Navigation:
  - `view-book-button-{book_id}`: `url_for('book_details', book_id=book_id)`
  - `back-to-dashboard`: `url_for('dashboard')`

---

## Section 3: Data Schemas Specification

### 1. Books Data
- File path: `data/books.txt`
- Format: Pipe-delimited (`|`)
- Fields (in order): book_id(int), title(str), author(str), isbn(str), category(str), price(float), stock(int), description(str)
- Description: Stores all books available in the bookstore with pricing, stock, and description.
- Example rows:
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

### 2. Categories Data
- File path: `data/categories.txt`
- Format: Pipe-delimited (`|`)
- Fields (in order): category_id(int), category_name(str), description(str)
- Description: Stores all book categories.
- Example rows:
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

### 3. Cart Data
- File path: `data/cart.txt`
- Format: Pipe-delimited (`|`)
- Fields (in order): cart_id(int), book_id(int), quantity(int), added_date(str in YYYY-MM-DD)
- Description: Stores items temporarily added to the shopping cart.
- Example rows:
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

### 4. Orders Data
- File path: `data/orders.txt`
- Format: Pipe-delimited (`|`)
- Fields (in order): order_id(int), customer_name(str), order_date(str in YYYY-MM-DD), total_amount(float), status(str), shipping_address(str)
- Description: Stores completed orders with customer and shipping details.
- Example rows:
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```

### 5. Order Items Data
- File path: `data/order_items.txt`
- Format: Pipe-delimited (`|`)
- Fields (in order): order_item_id(int), order_id(int), book_id(int), quantity(int), price(float)
- Description: Stores the breakdown of items within each order.
- Example rows:
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

### 6. Reviews Data
- File path: `data/reviews.txt`
- Format: Pipe-delimited (`|`)
- Fields (in order): review_id(int), book_id(int), customer_name(str), rating(int), review_text(str), review_date(str in YYYY-MM-DD)
- Description: Stores customer reviews for books with rating and text.
- Example rows:
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

### 7. Bestsellers Data
- File path: `data/bestsellers.txt`
- Format: Pipe-delimited (`|`)
- Fields (in order): book_id(int), sales_count(int), period(str)
- Description: Tracks book sales count for different periods to rank bestsellers.
- Example rows:
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

This completes the design specification document for BookstoreOnline, covering all required Flask routes, HTML templates, and data schema details enabling independent development of backend and frontend components.
