# BookstoreOnline - Design Specification Document

---

## Section 1: Flask Routes Specification

### Root Route
- **Route Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Method:** GET
- **Template Rendered:** Redirect to `/dashboard`
- **Context Variables:** None
- **Description:** Redirects from root URL to Dashboard page.


### Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** `dashboard`
- **HTTP Method:** GET
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `featured_books` (list of dict): List of featured books.
  - `bestsellers` (list of dict): List of bestsellers.


### Book Catalog Page
- **Route Path:** `/catalog`
- **Function Name:** `book_catalog`
- **HTTP Method:** GET
- **Template Rendered:** `catalog.html`
- **Context Variables:**
  - `books` (list of dict): Books matching search and filter.
  - `categories` (list of dict): Available categories.
  - `selected_category` (str): Currently selected category filter.
  - `search_query` (str): Search input string.


### Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** `book_details`
- **HTTP Method:** GET
- **Template Rendered:** `book_details.html`
- **Context Variables:**
  - `book` (dict): Detailed info of the book.
  - `reviews` (list of dict): Customer reviews for this book.

- **Route Path:** `/book/<int:book_id>/add_to_cart`
- **Function Name:** `add_to_cart`
- **HTTP Method:** POST
- **Template Rendered:** Redirect to `/book/<int:book_id>`
- **Form Handling:** Submits a request to add 1 quantity of the book to cart.


### Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** `cart`
- **HTTP Method:** GET
- **Template Rendered:** `cart.html`
- **Context Variables:**
  - `cart_items` (list of dict): Cart items with book details and quantity.
  - `total_amount` (float): Total cost.

- **Route Path:** `/cart/update_quantity/<int:item_id>`
- **Function Name:** `update_quantity`
- **HTTP Method:** POST
- **Template Rendered:** Redirect to `/cart`
- **Form Handling:** Updates quantity of a cart item.

- **Route Path:** `/cart/remove_item/<int:item_id>`
- **Function Name:** `remove_item`
- **HTTP Method:** POST
- **Template Rendered:** Redirect to `/cart`
- **Form Handling:** Removes an item from cart.


### Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** `checkout`
- **HTTP Method:** GET
- **Template Rendered:** `checkout.html`
- **Context Variables:** None

- **Route Path:** `/checkout/place_order`
- **Function Name:** `place_order`
- **HTTP Method:** POST
- **Template Rendered:** Redirect to `/orders`
- **Form Handling:** Processes order placement from form data including customer name, shipping address, payment method.


### Order History Page
- **Route Path:** `/orders`
- **Function Name:** `order_history`
- **HTTP Method:** GET
- **Template Rendered:** `orders.html`
- **Context Variables:**
  - `orders` (list of dict): User order history.
  - `status_filter` (str): Order status filter.

- **Route Path:** `/orders/<int:order_id>`
- **Function Name:** `view_order`
- **HTTP Method:** GET
- **Template Rendered:** *Not specified in detail (optional)*
- **Context Variables:**
  - `order` (dict): Information on selected order.
  - `order_items` (list of dict): Items in the order.


### Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** `reviews_page`
- **HTTP Method:** GET
- **Template Rendered:** `reviews.html`
- **Context Variables:**
  - `reviews` (list of dict): All reviews.
  - `rating_filter` (str): Currently selected rating for filtering.


### Write Review Page
- **Route Path:** `/write_review`
- **Function Name:** `write_review_page`
- **HTTP Method:** GET
- **Template Rendered:** `write_review.html`
- **Context Variables:**
  - `books` (list of dict): Books user can review.

- **Route Path:** `/write_review/submit`
- **Function Name:** `submit_review`
- **HTTP Method:** POST
- **Template Rendered:** Redirect to `/reviews`
- **Form Handling:** Accept book_id, rating, review text.


### Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** `bestsellers_page`
- **HTTP Method:** GET
- **Template Rendered:** `bestsellers.html`
- **Context Variables:**
  - `bestsellers` (list of dict): List of bestselling books ranked.
  - `time_period` (str): Selected filter for time period (This Week, This Month, All Time).

---

## Section 2: HTML Templates Specification

### Dashboard Page
- **File Path:** `templates/dashboard.html`
- **Page Title:** Bookstore Dashboard
- **Main Heading (<h1>):** Bookstore Dashboard
- **Element IDs:**
  - `dashboard-page`: Div container for page.
  - `featured-books`: Div displaying featured books.
  - `browse-catalog-button`: Button navigating to `/catalog`.
  - `view-cart-button`: Button navigating to `/cart`.
  - `bestsellers-button`: Button navigating to `/bestsellers`.
- **Context Variables:** `featured_books`, `bestsellers`
- **Navigation Button mappings:**
  - `browse-catalog-button`: `url_for('book_catalog')`
  - `view-cart-button`: `url_for('cart')`
  - `bestsellers-button`: `url_for('bestsellers_page')`


### Book Catalog Page
- **File Path:** `templates/catalog.html`
- **Page Title:** Book Catalog
- **Main Heading (<h1>):** Book Catalog
- **Element IDs:**
  - `catalog-page`: Div container.
  - `search-input`: Input for search queries.
  - `category-filter`: Dropdown for category filter.
  - `books-grid`: Div grid for book cards.
  - `view-book-button-{book_id}`: Button to view individual book details.
- **Context Variables:** `books`, `categories`, `selected_category`, `search_query`
- **Navigation Button mappings:**
  - `view-book-button-{book_id}`: `url_for('book_details', book_id=book_id)`


### Book Details Page
- **File Path:** `templates/book_details.html`
- **Page Title:** Book Details
- **Main Heading (<h1>):** Book Details
- **Element IDs:**
  - `book-details-page`: Div container.
  - `book-title`: H1 showing book title.
  - `book-author`: Div showing author.
  - `book-price`: Div showing price.
  - `add-to-cart-button`: Button to add book to cart.
  - `book-reviews`: Div showing reviews.
- **Context Variables:** `book`, `reviews`
- **Form Structure:** POST form to `/book/<book_id>/add_to_cart` with submit button (`add-to-cart-button`), quantity assumed 1.


### Shopping Cart Page
- **File Path:** `templates/cart.html`
- **Page Title:** Shopping Cart
- **Main Heading (<h1>):** Shopping Cart
- **Element IDs:**
  - `cart-page`: Div container.
  - `cart-items-table`: Table listing cart items.
  - `update-quantity-{item_id}`: Number input for quantity update.
  - `remove-item-button-{item_id}`: Button to remove item.
  - `proceed-checkout-button`: Button navigating to `/checkout`.
  - `total-amount`: Div showing total cost.
- **Context Variables:** `cart_items`, `total_amount`
- **Navigation Button mappings:**
  - `proceed-checkout-button`: `url_for('checkout')`
- **Form Structure:** POST forms for updating and removing items.


### Checkout Page
- **File Path:** `templates/checkout.html`
- **Page Title:** Checkout
- **Main Heading (<h1>):** Checkout
- **Element IDs:**
  - `checkout-page`: Div container.
  - `customer-name`: Input field.
  - `shipping-address`: Textarea.
  - `payment-method`: Dropdown.
  - `place-order-button`: Button for submitting order.
- **Context Variables:** None
- **Form Structure:** POST form to `/checkout/place_order` with fields: `customer-name`, `shipping-address`, `payment-method`, submit button ID `place-order-button`.


### Order History Page
- **File Path:** `templates/orders.html`
- **Page Title:** Order History
- **Main Heading (<h1>):** Order History
- **Element IDs:**
  - `orders-page`: Container div.
  - `orders-table`: Table showing orders.
  - `view-order-button-{order_id}`: Button to view order details.
  - `order-status-filter`: Dropdown to filter by status.
  - `back-to-dashboard`: Button to navigate back to dashboard.
- **Context Variables:** `orders`, `status_filter`
- **Navigation Button mappings:**
  - `view-order-button-{order_id}`: `url_for('view_order', order_id=order_id)`
  - `back-to-dashboard`: `url_for('dashboard')`


### Reviews Page
- **File Path:** `templates/reviews.html`
- **Page Title:** Customer Reviews
- **Main Heading (<h1>):** Customer Reviews
- **Element IDs:**
  - `reviews-page`: Div container.
  - `reviews-list`: Div containing all reviews.
  - `write-review-button`: Button navigating to Write Review.
  - `filter-by-rating`: Dropdown for rating filter.
  - `back-to-dashboard`: Button to dashboard.
- **Context Variables:** `reviews`, `rating_filter`
- **Navigation Button mappings:**
  - `write-review-button`: `url_for('write_review_page')`
  - `back-to-dashboard`: `url_for('dashboard')`


### Write Review Page
- **File Path:** `templates/write_review.html`
- **Page Title:** Write a Review
- **Main Heading (<h1>):** Write a Review
- **Element IDs:**
  - `write-review-page`: Div container.
  - `select-book`: Dropdown to select book.
  - `rating-select`: Dropdown to select rating.
  - `review-text`: Textarea for review text.
  - `submit-review-button`: Button to submit review.
- **Context Variables:** `books`
- **Form Structure:** POST form to `/write_review/submit` with fields: `select-book`, `rating-select`, `review-text`, submit button `submit-review-button`.


### Bestsellers Page
- **File Path:** `templates/bestsellers.html`
- **Page Title:** Bestsellers
- **Main Heading (<h1>):** Bestsellers
- **Element IDs:**
  - `bestsellers-page`: Div container.
  - `bestsellers-list`: Div listing bestselling books.
  - `time-period-filter`: Dropdown for filtering time period.
  - `view-book-button-{book_id}`: Button to book details.
  - `back-to-dashboard`: Button to dashboard.
- **Context Variables:** `bestsellers`, `time_period`
- **Navigation Button mappings:**
  - `view-book-button-{book_id}`: `url_for('book_details', book_id=book_id)`
  - `back-to-dashboard`: `url_for('dashboard')`

---

## Section 3: Data Schemas Specification

### Books Data
- **File:** `data/books.txt`
- **Format:** Pipe-separated (`|`)
- **Fields:**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `category` (str)
  6. `price` (float)
  7. `stock` (int)
  8. `description` (str)
- **Purpose:** Stores book information.
- **Example Rows:**
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```


### Categories Data
- **File:** `data/categories.txt`
- **Format:** Pipe-separated (`|`)
- **Fields:**
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- **Purpose:** Stores category information.
- **Example Rows:**
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```


### Cart Data
- **File:** `data/cart.txt`
- **Format:** Pipe-separated (`|`)
- **Fields:**
  1. `cart_id` (int)
  2. `book_id` (int)
  3. `quantity` (int)
  4. `added_date` (str, YYYY-MM-DD)
- **Purpose:** Stores cart items.
- **Example Rows:**
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```


### Orders Data
- **File:** `data/orders.txt`
- **Format:** Pipe-separated (`|`)
- **Fields:**
  1. `order_id` (int)
  2. `customer_name` (str)
  3. `order_date` (str, YYYY-MM-DD)
  4. `total_amount` (float)
  5. `status` (str)
  6. `shipping_address` (str)
- **Purpose:** Stores order info.
- **Example Rows:**
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
  ```


### Order Items Data
- **File:** `data/order_items.txt`
- **Format:** Pipe-separated (`|`)
- **Fields:**
  1. `order_item_id` (int)
  2. `order_id` (int)
  3. `book_id` (int)
  4. `quantity` (int)
  5. `price` (float)
- **Purpose:** Stores order line items.
- **Example Rows:**
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```


### Reviews Data
- **File:** `data/reviews.txt`
- **Format:** Pipe-separated (`|`)
- **Fields:**
  1. `review_id` (int)
  2. `book_id` (int)
  3. `customer_name` (str)
  4. `rating` (int, 1-5)
  5. `review_text` (str)
  6. `review_date` (str, YYYY-MM-DD)
- **Purpose:** Stores book reviews.
- **Example Rows:**
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```


### Bestsellers Data
- **File:** `data/bestsellers.txt`
- **Format:** Pipe-separated (`|`)
- **Fields:**
  1. `book_id` (int)
  2. `sales_count` (int)
  3. `period` (str)
- **Purpose:** Stores bestseller sales data by period.
- **Example Rows:**
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```

---

**End of Design Specification Document**
