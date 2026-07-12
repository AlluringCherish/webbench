# BookstoreOnline - Design Specification Document

---

## Section 1: Flask Routes Specification

### 1. Root Route
- **Route Path:** `/`
- **Function Name:** `root_redirect`
- **HTTP Method(s):** `GET`
- **Template Rendered:** None (Redirect to dashboard)
- **Context Variables:** None
- **Description:** Redirects to `/dashboard`.

---

### 2. Dashboard Page
- **Route Path:** `/dashboard`
- **Function Name:** `dashboard_page`
- **HTTP Method(s):** `GET`
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `featured_books` (list of dict): List of featured books; each dict contains `book_id` (int), `title` (str), `author` (str), `price` (float)
  - `bestsellers` (list of dict): List of bestseller books; each dict contains `book_id` (int), `title` (str), `author` (str), `sales_count` (int)
- **Description:** Displays main dashboard with featured books and bestsellers.

---

### 3. Book Catalog Page
- **Route Path:** `/catalog`
- **Function Name:** `book_catalog_page`
- **HTTP Method(s):** `GET`
- **Template Rendered:** `catalog.html`
- **Context Variables:**
  - `categories` (list of dict): Each dict with `category_id` (int), `category_name` (str)
  - `books` (list of dict): List of books matching search/filter criteria; each dict contains `book_id` (int), `title` (str), `author` (str), `price` (float), `category` (str)
  - `search_query` (str): Current search input value
  - `selected_category` (str or None): Current selected category filter
- **Description:** Displays searchable and filterable list of books.

---

### 4. Book Details Page
- **Route Path:** `/book/<int:book_id>`
- **Function Name:** `book_details_page`
- **HTTP Method(s):** `GET`, `POST`
- **Template Rendered:** `book_details.html`
- **Context Variables:**
  - `book` (dict): Dictionary with keys `book_id` (int), `title` (str), `author` (str), `price` (float), `description` (str), `category` (str), `isbn` (str), `stock` (int)
  - `reviews` (list of dict): List of reviews for the book; each dict has `review_id` (int), `customer_name` (str), `rating` (int), `review_text` (str), `review_date` (str)
  - `added_to_cart` (bool, optional): Flag indicating if add to cart was successful (for UI messaging)

- **Form Submission Handling:**
  - POST to add the current book to cart (add one unit).
  - On POST, the route adds the book to `cart.txt` or updates quantity.

---

### 5. Shopping Cart Page
- **Route Path:** `/cart`
- **Function Name:** `shopping_cart_page`
- **HTTP Method(s):** `GET`, `POST`
- **Template Rendered:** `cart.html`
- **Context Variables:**
  - `cart_items` (list of dict): Each dict with `cart_id` (int), `book_id` (int), `title` (str), `quantity` (int), `price` (float), `subtotal` (float)
  - `total_amount` (float): Sum of all subtotals

- **Form Submission Handling:**
  - POST to update quantities or remove items:
    - Updating quantity: receives `update-quantity-{cart_id}` field with new quantity.
    - Removing item: receives action to remove item by `cart_id`.

---

### 6. Checkout Page
- **Route Path:** `/checkout`
- **Function Name:** `checkout_page`
- **HTTP Method(s):** `GET`, `POST`
- **Template Rendered:** `checkout.html`
- **Context Variables:**
  - `cart_items` (list of dict): Same as in cart page.
  - `total_amount` (float): Total amount for checkout.
  - `payment_methods` (list of str): `["Credit Card", "PayPal", "Bank Transfer"]`

- **Form Submission Handling:**
  - POST to place order with fields:
    - `customer_name` (str)
    - `shipping_address` (str)
    - `payment_method` (str)
  - Upon successful POST, creates new order in `orders.txt` and order items from current cart entries, clears the cart.

---

### 7. Order History Page
- **Route Path:** `/orders`
- **Function Name:** `order_history_page`
- **HTTP Method(s):** `GET`
- **Template Rendered:** `orders.html`
- **Context Variables:**
  - `orders` (list of dict): Each dict with `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str)
  - `selected_status` (str): Current status filter value (`All`, `Pending`, `Shipped`, `Delivered`)

- **Description:** Displays table of all orders filtered by status if selected.

---

### 8. Order Details Page (Optional route for viewing an order's details; based on order buttons)
- **Route Path:** `/order/<int:order_id>`
- **Function Name:** `order_details_page`
- **HTTP Method(s):** `GET`
- **Template Rendered:** `order_details.html`
- **Context Variables:**
  - `order` (dict): Order info with `order_id` (int), `customer_name` (str), `order_date` (str), `total_amount` (float), `status` (str), `shipping_address` (str)
  - `order_items` (list of dict): List of items in order; each with `order_item_id` (int), `book_id` (int), `title` (str), `quantity` (int), `price` (float)

---

### 9. Reviews Page
- **Route Path:** `/reviews`
- **Function Name:** `reviews_page`
- **HTTP Method(s):** `GET`
- **Template Rendered:** `reviews.html`
- **Context Variables:**
  - `reviews` (list of dict): All reviews; each dict has `review_id` (int), `book_title` (str), `customer_name` (str), `rating` (int), `review_text` (str)
  - `filter_rating` (str or None): Current rating filter (e.g., `All`, `5`, `4`...)

---

### 10. Write Review Page
- **Route Path:** `/write-review`
- **Function Name:** `write_review_page`
- **HTTP Method(s):** `GET`, `POST`
- **Template Rendered:** `write_review.html`
- **Context Variables:**
  - `purchased_books` (list of dict): Books eligible for review; each dict with `book_id` (int), `title` (str)

- **Form Submission Handling:**
  - POST fields:
    - `book_id` (int)
    - `rating` (int, 1-5)
    - `review_text` (str)
  - On submission, adds review to `reviews.txt` with current date.

---

### 11. Bestsellers Page
- **Route Path:** `/bestsellers`
- **Function Name:** `bestsellers_page`
- **HTTP Method(s):** `GET`
- **Template Rendered:** `bestsellers.html`
- **Context Variables:**
  - `bestsellers` (list of dict): Each dict with `book_id` (int), `title` (str), `author` (str), `sales_count` (int), `period` (str)
  - `selected_period` (str): Current filter period (`This Week`, `This Month`, `All Time`)

---

## Section 2: HTML Templates Specification

### 1. Dashboard Template
- **File Path:** `templates/dashboard.html`
- **Page Title:** `Bookstore Dashboard`
- **Main <h1>:** `Bookstore Dashboard`
- **Element IDs and Details:**
  - `dashboard-page` (Div): Container for dashboard page.
  - `featured-books` (Div): Displays featured book recommendations.
  - `browse-catalog-button` (Button): Navigates to `/catalog`.
  - `view-cart-button` (Button): Navigates to `/cart`.
  - `bestsellers-button` (Button): Navigates to `/bestsellers`.
- **Context Variables:**
  - `featured_books` (list of dict)
  - `bestsellers` (list of dict)
- **Navigation URLs:**
  - `browse-catalog-button` -> `url_for('book_catalog_page')`
  - `view-cart-button` -> `url_for('shopping_cart_page')`
  - `bestsellers-button` -> `url_for('bestsellers_page')`

---

### 2. Catalog Template
- **File Path:** `templates/catalog.html`
- **Page Title:** `Book Catalog`
- **Main <h1>:** `Book Catalog`
- **Element IDs and Details:**
  - `catalog-page` (Div): Container for catalog.
  - `search-input` (Input): Text input for searching books.
  - `category-filter` (Dropdown): Filters by category.
  - `books-grid` (Div): Grid display of books.
  - `view-book-button-{book_id}` (Button): Button on each book card to view details.
- **Context Variables:**
  - `categories` (list of dict)
  - `books` (list of dict)
  - `search_query` (str)
  - `selected_category` (str|null)
- **Navigation URLs:**
  - `view-book-button-{book_id}` -> `url_for('book_details_page', book_id=book_id)`

---

### 3. Book Details Template
- **File Path:** `templates/book_details.html`
- **Page Title:** `Book Details`
- **Main <h1>:** `book["title"]`
- **Element IDs and Details:**
  - `book-details-page` (Div): Container.
  - `book-title` (H1): Displays `book['title']`.
  - `book-author` (Div): Displays `book['author']`.
  - `book-price` (Div): Displays formatted price.
  - `add-to-cart-button` (Button): POST form to add book to cart.
  - `book-reviews` (Div): Displays list of reviews.
- **Context Variables:**
  - `book` (dict)
  - `reviews` (list of dict)
- **Form:**
  - Submit button with `id=add-to-cart-button`
  - POST form action points to same route

---

### 4. Shopping Cart Template
- **File Path:** `templates/cart.html`
- **Page Title:** `Shopping Cart`
- **Main <h1>:** `Shopping Cart`
- **Element IDs and Details:**
  - `cart-page` (Div): Container.
  - `cart-items-table` (Table): Lists cart items with columns: Title, Quantity, Price, Subtotal.
  - `update-quantity-{cart_id}` (Input number): For each cart item quantity input.
  - `remove-item-button-{cart_id}` (Button): Remove item button.
  - `proceed-checkout-button` (Button): Navigates to `/checkout`.
  - `total-amount` (Div): Displays total amount.
- **Context Variables:**
  - `cart_items` (list of dict)
  - `total_amount` (float)
- **Navigation URLs:**
  - `proceed-checkout-button` -> `url_for('checkout_page')`
- **Form:**
  - Form to update quantities and remove items with POST submission.

---

### 5. Checkout Template
- **File Path:** `templates/checkout.html`
- **Page Title:** `Checkout`
- **Main <h1>:** `Checkout`
- **Element IDs and Details:**
  - `checkout-page` (Div): Container.
  - `customer-name` (Input): Input for customer name.
  - `shipping-address` (Textarea): Input for shipping address.
  - `payment-method` (Dropdown): Select payment method.
  - `place-order-button` (Button): Submit order button.
- **Context Variables:**
  - `cart_items` (list of dict)
  - `total_amount` (float)
  - `payment_methods` (list of str)
- **Form:**
  - POST form with above fields, submits to same route.

---

### 6. Order History Template
- **File Path:** `templates/orders.html`
- **Page Title:** `Order History`
- **Main <h1>:** `Order History`
- **Element IDs and Details:**
  - `orders-page` (Div): Container.
  - `orders-table` (Table): Columns: Order ID, Date, Total Amount, Status.
  - `view-order-button-{order_id}` (Button): View order details button.
  - `order-status-filter` (Dropdown): Filter orders by status.
  - `back-to-dashboard` (Button): Navigate to dashboard.
- **Context Variables:**
  - `orders` (list of dict)
  - `selected_status` (str)
- **Navigation URLs:**
  - `view-order-button-{order_id}` -> `url_for('order_details_page', order_id=order_id)`
  - `back-to-dashboard` -> `url_for('dashboard_page')`

---

### 7. Order Details Template (Optional for Order button)
- **File Path:** `templates/order_details.html`
- **Page Title:** `Order Details`
- **Main <h1>:** `Order Details #{{ order.order_id }}`
- **Element IDs and Details:**
  - `order-details-page` (Div): Container.
  - Displays order information and a table of ordered items.
- **Context Variables:**
  - `order` (dict)
  - `order_items` (list of dict)

---

### 8. Reviews Template
- **File Path:** `templates/reviews.html`
- **Page Title:** `Customer Reviews`
- **Main <h1>:** `Customer Reviews`
- **Element IDs and Details:**
  - `reviews-page` (Div): Container.
  - `reviews-list` (Div): List of all reviews.
  - `write-review-button` (Button): Navigate to write review page.
  - `filter-by-rating` (Dropdown): Filter reviews by rating.
  - `back-to-dashboard` (Button): Navigate to dashboard.
- **Context Variables:**
  - `reviews` (list of dict)
  - `filter_rating` (str|null)
- **Navigation URLs:**
  - `write-review-button` -> `url_for('write_review_page')`
  - `back-to-dashboard` -> `url_for('dashboard_page')`

---

### 9. Write Review Template
- **File Path:** `templates/write_review.html`
- **Page Title:** `Write a Review`
- **Main <h1>:** `Write a Review`
- **Element IDs and Details:**
  - `write-review-page` (Div): Container.
  - `select-book` (Dropdown): Dropdown to select book to review.
  - `rating-select` (Dropdown): Select rating from 1-5 stars.
  - `review-text` (Textarea): Text input for review text.
  - `submit-review-button` (Button): Submit review.
- **Context Variables:**
  - `purchased_books` (list of dict)
- **Form:**
  - POST form submits book_id, rating, review_text.

---

### 10. Bestsellers Template
- **File Path:** `templates/bestsellers.html`
- **Page Title:** `Bestsellers`
- **Main <h1>:** `Bestsellers`
- **Element IDs and Details:**
  - `bestsellers-page` (Div): Container.
  - `bestsellers-list` (Div): Ranked list of bestselling books.
  - `time-period-filter` (Dropdown): Filter by time period.
  - `view-book-button-{book_id}` (Button): Button to view book details.
  - `back-to-dashboard` (Button): Navigate to dashboard.
- **Context Variables:**
  - `bestsellers` (list of dict)
  - `selected_period` (str)
- **Navigation URLs:**
  - `view-book-button-{book_id}` -> `url_for('book_details_page', book_id=book_id)`
  - `back-to-dashboard` -> `url_for('dashboard_page')`

---

## Section 3: Data Schemas Specification

### 1. books.txt
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
- **Description:** Stores information about each book in the catalog.
- **Example Rows:**
```
1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
```

---

### 2. categories.txt
- **File Path:** `data/categories.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `category_id` (int)
  2. `category_name` (str)
  3. `description` (str)
- **Description:** Stores book category details.
- **Example Rows:**
```
1|Fiction|Fictional narratives and novels
2|Non-Fiction|Factual and educational books
3|Science|Scientific topics and research
```

---

### 3. cart.txt
- **File Path:** `data/cart.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `cart_id` (int)
  2. `book_id` (int)
  3. `quantity` (int)
  4. `added_date` (str: YYYY-MM-DD)
- **Description:** Stores items currently in the shopping cart.
- **Example Rows:**
```
1|1|2|2025-01-15
2|3|1|2025-01-16
```

---

### 4. orders.txt
- **File Path:** `data/orders.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `order_id` (int)
  2. `customer_name` (str)
  3. `order_date` (str: YYYY-MM-DD)
  4. `total_amount` (float)
  5. `status` (str; e.g., Pending, Shipped, Delivered)
  6. `shipping_address` (str)
- **Description:** Stores order records.
- **Example Rows:**
```
1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave, Los Angeles, CA 90001
```

---

### 5. order_items.txt
- **File Path:** `data/order_items.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `order_item_id` (int)
  2. `order_id` (int)
  3. `book_id` (int)
  4. `quantity` (int)
  5. `price` (float)
- **Description:** Stores individual book items for each order.
- **Example Rows:**
```
1|1|1|2|12.99
2|1|3|1|14.99
3|2|2|1|16.99
```

---

### 6. reviews.txt
- **File Path:** `data/reviews.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `review_id` (int)
  2. `book_id` (int)
  3. `customer_name` (str)
  4. `rating` (int; 1-5)
  5. `review_text` (str)
  6. `review_date` (str: YYYY-MM-DD)
- **Description:** Stores customer reviews per book.
- **Example Rows:**
```
1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
```

---

### 7. bestsellers.txt
- **File Path:** `data/bestsellers.txt`
- **Format:** Pipe-delimited (`|`)
- **Fields:**
  1. `book_id` (int)
  2. `sales_count` (int)
  3. `period` (str; e.g., "This Week", "This Month", "All Time")
- **Description:** Stores top-selling books ranked by sales in specific periods.
- **Example Rows:**
```
2|150|This Month
1|120|This Month
3|95|This Month
```

---

# End of Design Specification Document
