# Backend Design Specification for BookstoreOnline

---

## Section 1: Flask Routes Specification

### 1. Dashboard Page
- **Route:** `/`  
- **Methods:** `GET`  
- **Function:** `dashboard()`  
- **Template:** `dashboard.html`  
- **Context Variables:**  
  - `featured_books` (list of book dicts)  
  - `bestsellers` (list of bestseller books with sales)  
- **Actions:**  
  - Buttons navigate to `/catalog`, `/cart`, `/bestsellers`

### 2. Book Catalog Page
- **Route:** `/catalog`  
- **Methods:** `GET`  
- **Function:** `catalog()`  
- **Template:** `catalog.html`  
- **Request Parameters (Query):**  
  - `search` (optional string: search by title, author, ISBN)  
  - `category` (optional string: category name for filtering)  
- **Context Variables:**  
  - `books` (filtered list of book dicts)  
  - `categories` (list of category dicts for filter dropdown)
- **Actions:**  
  - Each book has button linking to `/book/<book_id>`

### 3. Book Details Page
- **Route:** `/book/<int:book_id>`  
- **Methods:** `GET`, `POST`  
- **Function:** `book_details(book_id)`  
- **Template:** `book_details.html`  
- **Context Variables:**  
  - `book` (book dict for the given book_id)  
  - `reviews` (list of review dicts for the book)  
- **Form Data (POST):**  
  - `quantity` (int, optional, default=1) when adding to cart  
- **Actions:**  
  - POST adds specified quantity of book to `cart.txt` and updates stock if applicable.

### 4. Shopping Cart Page
- **Route:** `/cart`  
- **Methods:** `GET`, `POST`  
- **Function:** `cart()`  
- **Template:** `cart.html`  
- **Context Variables:**  
  - `cart_items` (list of cart item dicts including book info)  
  - `total_amount` (float)  
- **Form Data (POST):**  
  - `update_quantities` (dict: `cart_id` -> new quantity) from input fields  
  - `remove_item` (cart_id) if remove button clicked  
- **Actions:**  
  - Update quantity or remove cart items accordingly.
  - Reflect quantity changes in `cart.txt`

### 5. Checkout Page
- **Route:** `/checkout`  
- **Methods:** `GET`, `POST`  
- **Function:** `checkout()`  
- **Template:** `checkout.html`  
- **Context Variables:**  
  - `cart_items` (current cart contents)  
  - `total_amount` (float)  
- **Form Data (POST):**  
  - `customer_name` (string)  
  - `shipping_address` (string)  
  - `payment_method` (string)  
- **Actions:**  
  - Validate cart not empty  
  - Create new order entry in `orders.txt` with status "Pending" and shipping info  
  - Create corresponding `order_items.txt` entries  
  - Clear `cart.txt`  
  - Optionally adjust stock if not done on add-to-cart step

### 6. Order History Page
- **Route:** `/orders`  
- **Methods:** `GET`  
- **Function:** `orders()`  
- **Template:** `orders.html`  
- **Request Parameters (Query):**  
  - `status` (optional string: filter by order status: All, Pending, Shipped, Delivered)  
- **Context Variables:**  
  - `orders` (filtered list of order dicts)  
- **Actions:**  
  - Button `view-order-button-{order_id}` navigates to `/orders/<order_id>`
  
### 7. Order Details Subpage
- **Route:** `/orders/<int:order_id>`  
- **Methods:** `GET`  
- **Function:** `order_details(order_id)`  
- **Template:** `order_details.html`  
- **Context Variables:**  
  - `order` (order dict)  
  - `order_items` (list of order items dicts)  
- **Actions:**  
  - Displays detailed info about the selected order

### 8. Reviews Page
- **Route:** `/reviews`  
- **Methods:** `GET`  
- **Function:** `reviews()`  
- **Template:** `reviews.html`  
- **Request Parameters (Query):**  
  - `rating_filter` (optional string or int: All, 5,4,3,2,1)  
- **Context Variables:**  
  - `reviews` (filtered list of reviews)  
- **Actions:**  
  - Button `write-review-button` navigates to `/write-review`

### 9. Write Review Page
- **Route:** `/write-review`  
- **Methods:** `GET`, `POST`  
- **Function:** `write_review()`  
- **Template:** `write_review.html`  
- **Context Variables:**  
  - `books` (list of books user can review)  
- **Form Data (POST):**  
  - `book_id` (int)  
  - `customer_name` (string)  
  - `rating` (int 1 to 5)  
  - `review_text` (string)  
- **Actions:**  
  - Append new review entry in `reviews.txt`

### 10. Bestsellers Page
- **Route:** `/bestsellers`  
- **Methods:** `GET`  
- **Function:** `bestsellers()`  
- **Template:** `bestsellers.html`  
- **Request Parameters (Query):**  
  - `period` (optional string: This Week, This Month, All Time)  
- **Context Variables:**  
  - `bestsellers` (list of bestseller book dicts filtered by period)  
- **Actions:**  
  - Button `view-book-button-{book_id}` navigates to `/book/<book_id>`

### Navigation Routes Summary
- `/` -> Dashboard  
- `/catalog` -> Book Catalog  
- `/cart` -> Shopping Cart  
- `/checkout` -> Checkout  
- `/orders` -> Order History  
- `/reviews` -> Reviews  
- `/write-review` -> Write Review  
- `/bestsellers` -> Bestsellers

---

## Section 2: Text File Data Schemas

### 1. Books Data
- **File Name:** `books.txt`
- **Delimiter:** `|`
- **Columns and Types:**
  - `book_id` (int, unique key)
  - `title` (string)
  - `author` (string)
  - `isbn` (string)
  - `category` (string)
  - `price` (float)
  - `stock` (int, current available stock)
  - `description` (string)
- **Example Row:**
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  ```
- **Notes:** Stock updated on order placement or add-to-cart if immediate reservation.

### 2. Categories Data
- **File Name:** `categories.txt`
- **Delimiter:** `|`
- **Columns and Types:**
  - `category_id` (int, unique key)
  - `category_name` (string)
  - `description` (string)
- **Example Row:**
  ```
  1|Fiction|Fictional narratives and novels
  ```

### 3. Cart Data
- **File Name:** `cart.txt`
- **Delimiter:** `|`
- **Columns and Types:**
  - `cart_id` (int, unique key)
  - `book_id` (int, FK to books.txt)
  - `quantity` (int, quantity added)
  - `added_date` (string, date in YYYY-MM-DD format)
- **Example Row:**
  ```
  1|1|2|2025-01-15
  ```
- **Notes:** Represents current user session cart (no auth, global). Update quantities or remove items.

### 4. Orders Data
- **File Name:** `orders.txt`
- **Delimiter:** `|`
- **Columns and Types:**
  - `order_id` (int, unique key)
  - `customer_name` (string)
  - `order_date` (string, YYYY-MM-DD)
  - `total_amount` (float)
  - `status` (string, e.g., Pending, Shipped, Delivered)
  - `shipping_address` (string)
- **Example Row:**
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001
  ```

### 5. Order Items Data
- **File Name:** `order_items.txt`
- **Delimiter:** `|`
- **Columns and Types:**
  - `order_item_id` (int, unique key)
  - `order_id` (int, FK to orders.txt)
  - `book_id` (int, FK to books.txt)
  - `quantity` (int)
  - `price` (float, per unit price at order time)
- **Example Row:**
  ```
  1|1|1|2|12.99
  ```

### 6. Reviews Data
- **File Name:** `reviews.txt`
- **Delimiter:** `|`
- **Columns and Types:**
  - `review_id` (int, unique key)
  - `book_id` (int, FK to books.txt)
  - `customer_name` (string)
  - `rating` (int, 1 to 5)
  - `review_text` (string)
  - `review_date` (string, YYYY-MM-DD)
- **Example Row:**
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  ```

### 7. Bestsellers Data
- **File Name:** `bestsellers.txt`
- **Delimiter:** `|`
- **Columns and Types:**
  - `book_id` (int, FK to books.txt)
  - `sales_count` (int, number of copies sold)
  - `period` (string, e.g., 'This Week', 'This Month', 'All Time')
- **Example Row:**
  ```
  2|150|This Month
  ```

---

## Backend Logic Considerations

- **Data Loading:** On each request, read appropriate data files fully into memory as Python structures (lists/dicts).
  Filter and process in-memory, then pass data to templates.

- **ID Management:** For new entries (cart item, order, review, order_item), generate new IDs by max existing + 1.

- **Concurrency:** Not covered due to single user/no auth context but should serialize write operations.

- **Stock Updates:** Stock should be decremented on order confirmation (checkout). Optional realtime decrements on add-to-cart to prevent overselling.

- **Cart Management:** Support update quantity, add item, remove item. Cart is global with no user separation.

- **Order Status:** Allow filtering orders by status; statuses can be static strings.

- **Review Submission:** Reviews appended to `reviews.txt` with current date.

- **Bestsellers Filtering:** Filter `bestsellers.txt` by period query or show default period.

- **Navigation:** Each page includes navigation buttons/links as per requirements for seamless flow.

---

This backend design specification should enable a developer to implement all Flask routes, data handling, and template context logic for the BookstoreOnline application, fully aligned with the provided user requirements and data schema conventions.