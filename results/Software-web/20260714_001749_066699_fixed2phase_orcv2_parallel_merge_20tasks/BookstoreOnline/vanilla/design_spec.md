# BookstoreOnline Unified Design Specification

---

## Section 1: Flask Routes Specification

### 1. Dashboard Page
- **Route:** `/`
- **Methods:** `GET`
- **Function:** `dashboard()`
- **Template:** `dashboard.html`
- **Context Variables:**
  - `featured_books` (list of book dicts)
  - `bestsellers` (list of bestseller book dicts with sales)
- **Frontend Element IDs:**
  - `dashboard-page` (div container)
  - `featured-books` (div for featured books)
  - `browse-catalog-button` (button for `/catalog`)
  - `view-cart-button` (button for `/cart`)
  - `bestsellers-button` (button for `/bestsellers`)
- **Navigation:** Buttons navigate to `/catalog`, `/cart`, `/bestsellers`

### 2. Book Catalog Page
- **Route:** `/catalog`
- **Methods:** `GET`
- **Function:** `catalog()`
- **Template:** `catalog.html`
- **Request Parameters (Query):**
  - `search` (optional string to search by title, author, ISBN)
  - `category` (optional string to filter by category name)
- **Context Variables:**
  - `books` (filtered list of book dicts)
  - `categories` (list of category dicts for dropdown)
- **Frontend Element IDs:**
  - `catalog-page` (div container)
  - `search-input` (input type text)
  - `category-filter` (select dropdown)
  - `books-grid` (div containing book cards)
  - `view-book-button-{book_id}` (button per book to view details)
- **Navigation:**
  - Click `view-book-button-{book_id}` navigates to `/book/<book_id>`

### 3. Book Details Page
- **Route:** `/book/<int:book_id>`
- **Methods:** `GET`, `POST`
- **Function:** `book_details(book_id)`
- **Template:** `book_details.html`
- **Context Variables:**
  - `book` (book dict for given `book_id`)
  - `reviews` (list of review dicts for this book)
- **Form Data (POST):**
  - `quantity` (int, default=1 on add to cart)
- **Frontend Element IDs:**
  - `book-details-page` (div container)
  - `book-title` (h1 element)
  - `book-author` (div)
  - `book-price` (div)
  - `add-to-cart-button` (button to add book to cart)
  - `book-reviews` (div displaying reviews)
- **Actions:**
  - Posting adds specified quantity to `cart.txt` and optionally updates stock immediately.

### 4. Shopping Cart Page
- **Route:** `/cart`
- **Methods:** `GET`, `POST`
- **Function:** `cart()`
- **Template:** `cart.html`
- **Context Variables:**
  - `cart_items` (list of cart items dicts including book info)
  - `total_amount` (float)
- **Form Data (POST):**
  - `update_quantities` (dict: `cart_id` -> new quantity)
  - `remove_item` (int cart_id) if remove button clicked
- **Frontend Element IDs:**
  - `cart-page` (div container)
  - `cart-items-table` (table of cart items)
  - `update-quantity-{item_id}` (input[number] per cart item for quantity)
  - `remove-item-button-{item_id}` (button to remove items)
  - `proceed-checkout-button` (button to navigate to `/checkout`)
  - `total-amount` (div showing cart total)
- **Actions:**
  - Updates quantities or removes items reflecting changes in `cart.txt`

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
  - `payment_method` (string, e.g., Credit Card, PayPal, Bank Transfer)
- **Frontend Element IDs:**
  - `checkout-page` (div container)
  - `customer-name` (input[type=text])
  - `shipping-address` (textarea)
  - `payment-method` (select dropdown)
  - `place-order-button` (button to place order)
- **Actions:**
  - Validate cart non-empty
  - Create new order in `orders.txt` with status "Pending"
  - Create order items in `order_items.txt`
  - Clear `cart.txt`
  - Optionally adjust stock here if not done earlier

### 6. Order History Page
- **Route:** `/orders`
- **Methods:** `GET`
- **Function:** `orders()`
- **Template:** `orders.html`
- **Request Parameters (Query):**
  - `status` (optional string filter: All, Pending, Shipped, Delivered)
- **Context Variables:**
  - `orders` (filtered list of order dicts)
- **Frontend Element IDs:**
  - `orders-page` (div container)
  - `orders-table` (table of orders)
  - `view-order-button-{order_id}` (button to view order details)
  - `order-status-filter` (select dropdown to filter by status)
  - `back-to-dashboard` (button to navigate back to `/`)
- **Actions:**
  - Buttons navigate to `/orders/<order_id>` or back to dashboard

### 7. Order Details Page
- **Route:** `/orders/<int:order_id>`
- **Methods:** `GET`
- **Function:** `order_details(order_id)`
- **Template:** `order_details.html`
- **Context Variables:**
  - `order` (order dict)
  - `order_items` (list of order items dicts)
- **Actions:**
  - Display detailed order information

### 8. Reviews Page
- **Route:** `/reviews`
- **Methods:** `GET`
- **Function:** `reviews()`
- **Template:** `reviews.html`
- **Request Parameters (Query):**
  - `rating_filter` (optional string/int: All, 5,4,3,2,1)
- **Context Variables:**
  - `reviews` (filtered list of reviews)
- **Frontend Element IDs:**
  - `reviews-page` (div container)
  - `reviews-list` (div listing reviews)
  - `write-review-button` (button to navigate to `/write-review`)
  - `filter-by-rating` (select dropdown)
  - `back-to-dashboard` (button to `/`)
- **Actions:**
  - Navigation via `write-review-button` to Write Review page

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
  - `rating` (int 1-5)
  - `review_text` (string)
- **Frontend Element IDs:**
  - `write-review-page` (div container)
  - `select-book` (select dropdown)
  - `rating-select` (select dropdown)
  - `review-text` (textarea)
  - `submit-review-button` (button)
- **Actions:**
  - Append the review in `reviews.txt`
  - On success, navigate back to `reviews` page

### 10. Bestsellers Page
- **Route:** `/bestsellers`
- **Methods:** `GET`
- **Function:** `bestsellers()`
- **Template:** `bestsellers.html`
- **Request Parameters (Query):**
  - `period` (optional string: This Week, This Month, All Time)
- **Context Variables:**
  - `bestsellers` (filtered list of bestseller book dicts)
- **Frontend Element IDs:**
  - `bestsellers-page` (div container)
  - `bestsellers-list` (div showing ranked bestsellers)
  - `time-period-filter` (select dropdown)
  - `view-book-button-{book_id}` (button per bestseller to view book details)
  - `back-to-dashboard` (button to `/`)
- **Navigation:**
  - Click `view-book-button-{book_id}` navigates to `/book/<book_id>`
  - Click `back-to-dashboard` returns to Dashboard

### Navigation Routes Map
- `/` (Dashboard)
- `/catalog` (Book Catalog)
- `/book/<book_id>` (Book Details)
- `/cart` (Shopping Cart)
- `/checkout` (Checkout)
- `/orders` (Order History)
- `/orders/<order_id>` (Order Details)
- `/reviews` (Reviews Page)
- `/write-review` (Write Review Page)
- `/bestsellers` (Bestsellers Page)

---

## Section 2: Local Text File Data Schemas

### 1. Books Data
- **File:** `books.txt`
- **Delimiter:** `|`
- **Columns:**
  - `book_id` (int, unique)
  - `title` (string)
  - `author` (string)
  - `isbn` (string)
  - `category` (string)
  - `price` (float)
  - `stock` (int)
  - `description` (string)
- **Example:**
  `1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel`

### 2. Categories Data
- **File:** `categories.txt`
- **Delimiter:** `|`
- **Columns:**
  - `category_id` (int, unique)
  - `category_name` (string)
  - `description` (string)
- **Example:**
  `1|Fiction|Fictional narratives and novels`

### 3. Cart Data
- **File:** `cart.txt`
- **Delimiter:** `|`
- **Columns:**
  - `cart_id` (int, unique)
  - `book_id` (int FK)
  - `quantity` (int)
  - `added_date` (string YYYY-MM-DD)
- **Example:**
  `1|1|2|2025-01-15`
- **Notes:** Global cart for any user session. Supports add, update, remove.

### 4. Orders Data
- **File:** `orders.txt`
- **Delimiter:** `|`
- **Columns:**
  - `order_id` (int, unique)
  - `customer_name` (string)
  - `order_date` (string YYYY-MM-DD)
  - `total_amount` (float)
  - `status` (string e.g., Pending, Shipped, Delivered)
  - `shipping_address` (string)
- **Example:**
  `1|John Doe|2025-01-10|38.97|Delivered|123 Main St, New York, NY 10001`

### 5. Order Items Data
- **File:** `order_items.txt`
- **Delimiter:** `|`
- **Columns:**
  - `order_item_id` (int, unique)
  - `order_id` (int FK)
  - `book_id` (int FK)
  - `quantity` (int)
  - `price` (float per unit at order time)
- **Example:**
  `1|1|1|2|12.99`

### 6. Reviews Data
- **File:** `reviews.txt`
- **Delimiter:** `|`
- **Columns:**
  - `review_id` (int, unique)
  - `book_id` (int FK)
  - `customer_name` (string)
  - `rating` (int 1-5)
  - `review_text` (string)
  - `review_date` (string YYYY-MM-DD)
- **Example:**
  `1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12`

### 7. Bestsellers Data
- **File:** `bestsellers.txt`
- **Delimiter:** `|`
- **Columns:**
  - `book_id` (int FK)
  - `sales_count` (int)
  - `period` (string e.g., This Week, This Month, All Time)
- **Example:**
  `2|150|This Month`

---

## Section 3: HTML Templates & Element IDs

### 1. dashboard.html
- Container: `dashboard-page`
- Content container: `featured-books`
- Buttons: `browse-catalog-button`, `view-cart-button`, `bestsellers-button`

### 2. catalog.html
- Container: `catalog-page`
- Search input: `search-input`
- Category dropdown: `category-filter`
- Books container: `books-grid`
- Per book button: `view-book-button-{book_id}`

### 3. book_details.html
- Container: `book-details-page`
- Title: `book-title`
- Author: `book-author`
- Price: `book-price`
- Add to cart button: `add-to-cart-button`
- Reviews section: `book-reviews`

### 4. cart.html
- Container: `cart-page`
- Cart items table: `cart-items-table`
- Per item quantity input: `update-quantity-{item_id}`
- Per item remove button: `remove-item-button-{item_id}`
- Proceed to checkout button: `proceed-checkout-button`
- Total amount div: `total-amount`

### 5. checkout.html
- Container: `checkout-page`
- Customer name input: `customer-name`
- Shipping address textarea: `shipping-address`
- Payment method select: `payment-method`
- Place order button: `place-order-button`

### 6. orders.html
- Container: `orders-page`
- Orders table: `orders-table`
- Per order view button: `view-order-button-{order_id}`
- Status filter dropdown: `order-status-filter`
- Back to dashboard button: `back-to-dashboard`

### 7. order_details.html
- Container: Consistent with `order_details.html` file (not explicitly defined in frontend but implied)

### 8. reviews.html
- Container: `reviews-page`
- Reviews list div: `reviews-list`
- Write review button: `write-review-button`
- Filter by rating dropdown: `filter-by-rating`
- Back to dashboard button: `back-to-dashboard`

### 9. write_review.html
- Container: `write-review-page`
- Select book dropdown: `select-book`
- Rating select dropdown: `rating-select`
- Review text textarea: `review-text`
- Submit review button: `submit-review-button`

### 10. bestsellers.html
- Container: `bestsellers-page`
- Bestsellers list div: `bestsellers-list`
- Time period filter dropdown: `time-period-filter`
- Per book view button: `view-book-button-{book_id}`
- Back to dashboard button: `back-to-dashboard`

---

## Section 4: Navigation Flow Summary

- **Dashboard (`/`)**
  - `browse-catalog-button` -> `/catalog`
  - `view-cart-button` -> `/cart`
  - `bestsellers-button` -> `/bestsellers`

- **Book Catalog (`/catalog`)**
  - `view-book-button-{book_id}` -> `/book/<book_id>`

- **Book Details (`/book/<book_id>`)**
  - `add-to-cart-button` -> Add to cart action (may stay or navigate to `/cart`)

- **Shopping Cart (`/cart`)**
  - Modify quantities with `update-quantity-{item_id}`
  - Remove items with `remove-item-button-{item_id}`
  - `proceed-checkout-button` -> `/checkout`

- **Checkout (`/checkout`)**
  - `place-order-button` -> Process order and navigate to `/orders`

- **Order History (`/orders`)**
  - `view-order-button-{order_id}` -> `/orders/<order_id>`
  - `back-to-dashboard` -> `/`

- **Order Details (`/orders/<order_id>`)**
  - Display order details

- **Reviews (`/reviews`)**
  - `write-review-button` -> `/write-review`
  - `back-to-dashboard` -> `/`

- **Write Review (`/write-review`)**
  - `submit-review-button` -> Submit form then return to `/reviews`

- **Bestsellers (`/bestsellers`)**
  - `view-book-button-{book_id}` -> `/book/<book_id>`
  - `back-to-dashboard` -> `/`

---

## Section 5: Data Flow and Key Logic Points

- All backend routes load appropriate text files into Python structures on each request.
- IDs for new entries (cart, order, review, order items) are assigned as max existing ID + 1.
- Cart is a global session-less store, thus no user differentiation.
- Stock is adjusted on order confirmation (checkout). Immediate stock decrement upon add-to-cart is optional.
- Writing reviews appends to `reviews.txt` with the current date.
- Filtering works on catalog (search, category), orders (status), reviews (rating), and bestsellers (period).
- Navigation buttons correspond precisely to backend routes.

---

This unified design specification document is comprehensive and consistent, enabling backend and frontend developers to implement the entire BookstoreOnline application with no contradictions or gaps.
