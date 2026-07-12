# BookstoreOnline - Design Specification Document

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Method:** GET
- **Behavior:** Redirects to `/dashboard`

---

### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** `dashboard_page`
- **HTTP Method:** GET
- **Template:** `dashboard.html`
- **Context Variables:**
  - `featured_books` (list of dict): List of featured book dictionaries containing book data.
  - `bestsellers` (list of dict): List of bestseller book dictionaries.

---

### 3. Book Catalog Page
- **Route Path:** `/catalog`
- **Function Name:** `catalog_page`
- **HTTP Method:** GET
- **Template:** `catalog.html`
- **Context Variables:**
  - `books` (list of dict): List of all book dictionaries available.
  - `categories` (list of dict): List of categories with keys `category_id`, `category_name`, `description`.
  - `selected_category` (str): Currently selected category name filter (optional).
  - `search_query` (str): Current search query string (optional).

---

### 4. Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** `book_details_page`
- **HTTP Method:** GET
- **Template:** `book_details.html`
- **Context Variables:**
  - `book` (dict): Dictionary containing book data fields.
  - `reviews` (list of dict): List of review dictionaries for this book.

- **Form submission:**
  - Adding to cart via POST can be on this route or separate; based on requirements no explicit POST route is described. If POST handled here:
    - **HTTP Method:** POST
    - Form data includes `quantity` (int)
    - Adds the specified book and quantity to cart, then redirect or render with success.
    
---

### 5. Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** `shopping_cart_page`
- **HTTP Method:** GET
- **Template:** `cart.html`
- **Context Variables:**
  - `cart_items` (list of dict): Each dict includes `item_id` (cart_id), `book` (dict), `quantity` (int), `subtotal` (float).
  - `total_amount` (float): Total cost sum of all cart items.

- **Form submissions:**
  - Update item quantity:
    - POST to `/cart/update_quantity`
    - Fields: `item_id` (int), `quantity` (int)
    - Updates quantity for specified item.
  - Remove item:
    - POST to `/cart/remove_item`
    - Field: `item_id` (int)
    - Removes specified item from cart.

- **Checkout:**
  - The `proceed-checkout-button` navigates to `/checkout`.

---

### 6. Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** `checkout_page`
- **HTTP Method:** GET, POST
- **Template:** `checkout.html`
- **Context Variables:** (GET)
  - `cart_items` (list of dict): Current cart items with details for review.
  - `total_amount` (float): Total order amount.

- **POST Form Submission:**
  - Fields:
    - `customer_name` (str)
    - `shipping_address` (str)
    - `payment_method` (str: "Credit Card", "PayPal", or "Bank Transfer")
  - Action: Processes order placement, saves order, clears cart, redirects to order history or confirmation.

---

### 7. Order History Page
- **Route Path:** `/orders`
- **Function Name:** `order_history_page`
- **HTTP Method:** GET
- **Template:** `orders.html`
- **Context Variables:**
  - `orders` (list of dict): List of orders with fields including order_id, customer_name, order_date (str), total_amount (float), status (str), shipping_address.
  - `status_filter` (str): Currently selected order status filter ("All", "Pending", "Shipped", "Delivered").

- **Filtering:**
  - Filter orders by `status` query parameter.

---

### 8. Order Details Page (Implied for view-order-button)
- **Route Path:** `/order/<int:order_id>`
- **Function Name:** `order_details_page`
- **HTTP Method:** GET
- **Template:** `order_details.html` (assumed for completeness)
- **Context Variables:**
  - `order` (dict): Details of specified order.
  - `order_items` (list of dict): Items within the order with book details and quantity.

---

### 9. Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** `reviews_page`
- **HTTP Method:** GET
- **Template:** `reviews.html`
- **Context Variables:**
  - `reviews` (list of dict): All customer reviews.
  - `rating_filter` (str): Current filter by rating ("All", "5 stars", "4 stars", etc.).

- **Filtering:**
  - Reviews filtered by rating via query parameter.

---

### 10. Write Review Page
- **Route Path:** `/write_review`
- **Function Name:** `write_review_page`
- **HTTP Method:** GET, POST
- **Template:** `write_review.html`
- **Context Variables:** (GET)
  - `purchased_books` (list of dict): Books eligible for review (i.e., purchased books).

- **POST Form Submission:**
  - Fields:
    - `book_id` (int)
    - `rating` (int, 1-5)
    - `review_text` (str)
  - Action: Saves the review, redirects to reviews page.

---

### 11. Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** `bestsellers_page`
- **HTTP Method:** GET
- **Template:** `bestsellers.html`
- **Context Variables:**
  - `bestsellers` (list of dict): Ranked list of best-selling books.
  - `time_period` (str): Currently selected filter by period ("This Week", "This Month", "All Time").

- **Filtering:**
  - Filter bestseller books by period via query parameter.

---

## Section 2: HTML Templates Specification

### Common Notes
- All templates reside in the `templates/` directory.
- Navigation buttons or links use `url_for()` to map endpoints as per Flask conventions.

---

### 1. Dashboard Template
- **File Path:** `templates/dashboard.html`
- **Page Title:** `Bookstore Dashboard`
- **Main Heading (`<h1>`):** `Bookstore Dashboard`
- **Element IDs and Descriptions:**
  - `dashboard-page` (Div): Main container.
  - `featured-books` (Div): Display featured book recommendations.
  - `browse-catalog-button` (Button): Navigates to catalog page.
  - `view-cart-button` (Button): Navigates to shopping cart page.
  - `bestsellers-button` (Button): Navigates to bestsellers page.
- **Context Variables:** `featured_books` (list of dict), `bestsellers` (list of dict)
- **Navigation:**
  - `browse-catalog-button` → `url_for('catalog_page')`
  - `view-cart-button` → `url_for('shopping_cart_page')`
  - `bestsellers-button` → `url_for('bestsellers_page')`

---

### 2. Book Catalog Template
- **File Path:** `templates/catalog.html`
- **Page Title:** `Book Catalog`
- **Main Heading:** `Book Catalog`
- **Element IDs:**
  - `catalog-page` (Div)
  - `search-input` (Input)
  - `category-filter` (Dropdown)
  - `books-grid` (Div)
  - `view-book-button-{book_id}` (Button): For each book card
- **Context Variables:**
  - `books` (list of dict)
  - `categories` (list of dict)
  - `selected_category` (str)
  - `search_query` (str)
- **Navigation:**
  - Each `view-book-button-{book_id}` → `url_for('book_details_page', book_id=book_id)`

---

### 3. Book Details Template
- **File Path:** `templates/book_details.html`
- **Page Title:** `Book Details`
- **Main Heading (`<h1>`):** Uses `book.title`
- **Element IDs:**
  - `book-details-page` (Div)
  - `book-title` (H1): Book title
  - `book-author` (Div)
  - `book-price` (Div)
  - `add-to-cart-button` (Button)
  - `book-reviews` (Div): Displays list of reviews
- **Context Variables:** `book` (dict), `reviews` (list of dict)
- **Form:**
  - Add to cart form with button `add-to-cart-button` and quantity input (optional)
- **Navigation:**
  - Back or other navigation not specified

---

### 4. Shopping Cart Template
- **File Path:** `templates/cart.html`
- **Page Title:** `Shopping Cart`
- **Main Heading:** `Shopping Cart`
- **Element IDs:**
  - `cart-page` (Div)
  - `cart-items-table` (Table)
  - `update-quantity-{item_id}` (Input number) for each cart item
  - `remove-item-button-{item_id}` (Button) for each cart item
  - `proceed-checkout-button` (Button)
  - `total-amount` (Div)
- **Context Variables:**
  - `cart_items` (list of dict)
  - `total_amount` (float)
- **Form Structure:**
  - Forms or AJAX to update quantity and remove item separately
  - Button `proceed-checkout-button` links to `/checkout`

---

### 5. Checkout Template
- **File Path:** `templates/checkout.html`
- **Page Title:** `Checkout`
- **Main Heading:** `Checkout`
- **Element IDs:**
  - `checkout-page` (Div)
  - `customer-name` (Input)
  - `shipping-address` (Textarea)
  - `payment-method` (Dropdown)
  - `place-order-button` (Button)
- **Context Variables:** 
  - `cart_items` (list of dict)
  - `total_amount` (float)
- **Form:**
  - Single form wrapping all inputs including `customer-name`, `shipping-address`, `payment-method` and submit button `place-order-button`
  - Form method POST to `/checkout`

---

### 6. Order History Template
- **File Path:** `templates/orders.html`
- **Page Title:** `Order History`
- **Main Heading:** `Order History`
- **Element IDs:**
  - `orders-page` (Div)
  - `orders-table` (Table)
  - `view-order-button-{order_id}` (Button) for each order
  - `order-status-filter` (Dropdown)
  - `back-to-dashboard` (Button)
- **Context Variables:**
  - `orders` (list of dict)
  - `status_filter` (str)
- **Navigation:**
  - `view-order-button-{order_id}` → `url_for('order_details_page', order_id=order_id)`
  - `back-to-dashboard` → `url_for('dashboard_page')`

---

### 7. Reviews Template
- **File Path:** `templates/reviews.html`
- **Page Title:** `Customer Reviews`
- **Main Heading:** `Customer Reviews`
- **Element IDs:**
  - `reviews-page` (Div)
  - `reviews-list` (Div)
  - `write-review-button` (Button)
  - `filter-by-rating` (Dropdown)
  - `back-to-dashboard` (Button)
- **Context Variables:** `reviews` (list of dict), `rating_filter` (str)
- **Navigation:**
  - `write-review-button` → `url_for('write_review_page')`
  - `back-to-dashboard` → `url_for('dashboard_page')`

---

### 8. Write Review Template
- **File Path:** `templates/write_review.html`
- **Page Title:** `Write a Review`
- **Main Heading:** `Write a Review`
- **Element IDs:**
  - `write-review-page` (Div)
  - `select-book` (Dropdown)
  - `rating-select` (Dropdown)
  - `review-text` (Textarea)
  - `submit-review-button` (Button)
- **Context Variables:**
  - `purchased_books` (list of dict)
- **Form:**
  - Form method POST
  - Fields within form: `select-book`, `rating-select`, `review-text`
  - Submit button `submit-review-button`

---

### 9. Bestsellers Template
- **File Path:** `templates/bestsellers.html`
- **Page Title:** `Bestsellers`
- **Main Heading:** `Bestsellers`
- **Element IDs:**
  - `bestsellers-page` (Div)
  - `bestsellers-list` (Div)
  - `time-period-filter` (Dropdown)
  - `view-book-button-{book_id}` (Button) for each bestseller
  - `back-to-dashboard` (Button)
- **Context Variables:**
  - `bestsellers` (list of dict)
  - `time_period` (str)
- **Navigation:**
  - Each `view-book-button-{book_id}` → `url_for('book_details_page', book_id=book_id)`
  - `back-to-dashboard` → `url_for('dashboard_page')`

---

## Section 3: Data Schemas Specification

### 1. Books Data
- **File Path:** `data/books.txt`
- **Format:** Pipe-delimited (`|`), no header line.
- **Fields (in order):**
  1. `book_id` (int)
  2. `title` (str)
  3. `author` (str)
  4. `isbn` (str)
  5. `category` (str)
  6. `price` (float)
  7. `stock` (int)
  8. `description` (str)
- **Description:** Stores all book information.
- **Example rows:**
```
1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
```

---

### 2. Categories Data
- **File Path:** `data/categories.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- **Description:** Stores book categories.
- **Example rows:**
```
1|Fiction|Fictional narratives and novels
2|Non-Fiction|Factual and educational books
3|Science|Scientific topics and research
```

---

### 3. Cart Data
- **File Path:** `data/cart.txt`
- **Format:** Pipe-delimited
- **Fields:**
  1. `cart_id` (int)
  2. `book_id` (int)
  3. `quantity` (int)
  4. `added_date` (str, YYYY-MM-DD)
- **Description:** Stores current items in the shopping cart.
- **Example rows:**
```
1|1|2|2025-01-15
2|3|1|2025-01-16
```

---

### 4. Orders Data
- **File Path:** `data/orders.txt`
- **Format:** Pipe-delimited
- **Fields:**
  1. `order_id` (int)
  2. `customer_name` (str)
  3. `order_date` (str, YYYY-MM-DD)
  4. `total_amount` (float)
  5. `status` (str) – e.g., Pending, Shipped, Delivered
  6. `shipping_address` (str)
- **Description:** Stores all placed order information.
- **Example rows:**
```
1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
```

---

### 5. Order Items Data
- **File Path:** `data/order_items.txt`
- **Format:** Pipe-delimited
- **Fields:**
  1. `order_item_id` (int)
  2. `order_id` (int)
  3. `book_id` (int)
  4. `quantity` (int)
  5. `price` (float) – unit price at purchase
- **Description:** Stores individual items of each order.
- **Example rows:**
```
1|1|1|2|12.99
2|1|3|1|14.99
3|2|2|1|16.99
```

---

### 6. Reviews Data
- **File Path:** `data/reviews.txt`
- **Format:** Pipe-delimited
- **Fields:**
  1. `review_id` (int)
  2. `book_id` (int)
  3. `customer_name` (str)
  4. `rating` (int: 1-5)
  5. `review_text` (str)
  6. `review_date` (str, YYYY-MM-DD)
- **Description:** Stores customer reviews for books.
- **Example rows:**
```
1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
```

---

### 7. Bestsellers Data
- **File Path:** `data/bestsellers.txt`
- **Format:** Pipe-delimited
- **Fields:**
  1. `book_id` (int)
  2. `sales_count` (int)
  3. `period` (str) – "This Week", "This Month", or "All Time"
- **Description:** Stores bestselling books ranked by sales count for specified period.
- **Example rows:**
```
2|150|This Month
1|120|This Month
3|95|This Month
```

---

# End of Design Specification Document
