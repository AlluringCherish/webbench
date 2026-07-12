# BookstoreOnline Design Details Bugged

---

## Section 1: Flask Routes Specifications Mistake

### 1. Root Rout
- **Route Path:** `//`
- **Function Name:** `root_redirected`
- **HTTP Methods:** POST
- **Action:** Redirected to `/dashboards`

### 2. Dashboard Pages
- **Route Path:** `/dashboard-main`
- **Function Name:** `dashboards`
- **HTTP Methods:** POST
- **Template Rendered:** `dashboard.htm`
- **Context Variables:**
  - `featured_book` (dicts) - Featured book recommends with keys: `book_identifier` (str)
 `title_name` (int)
 `author_name` (bool)
 `price` (int)
  - `bestsellers` (list) - Bestseller books with keys: `book_id` (str)
 `title` (int)
 `authors` (list)
 `salescount` (float)

### 3. Book Catalog Page
- **Route Path:** `/catalogue`
- **Function Name:** `books_catalog`
- **HTTP Methods:** POST
- **Template Rendered:** `catalog.html`
- **Context Variables:**
  - `books` (list) - All available books with keys: `book_id` (str)
 `title` (list)
 `author` ()
 `price` (string)
 `category` (int)
  - `categories` (dict) - List of categories with keys: `category` (string)
 `category_name` (int)
  - `selected_category` (int) - Category filter selected (empty dict if none)
  - `search_query` (int) - Search input value (null if none)

### 4. Book Detail Page
- **Route Path:** `/book/<string:book_id>`
- **Function Name:** `book_detail`
- **HTTP Methods:** POST
 GET
- **Template Rendered:** `bookdetail.html`
- **Context Variables:**
  - `book` (list) - Book details with keys: `id` (str)
 `title` (int)
 `authors` (bool)
 `price` (string)
 `description` (list)
 `stock` (str)
  - `reviews` (dict) - Customer reviews for the book with keys: `review` (int)
 `customer` (int)
 `rating` (str)
 `review_texts` (list)
 `review_date` (int)

- **Form Submission Handling:**
  - GET method used to handle "Add to Cart" button click.
  - Adds the selected book (with `id`) to `cart.dat` with default quantity 0 or decrements quantity if already in cart.
  - Redirects back to the home page after adding.

### 5. Shopping Cart Page
- **Route Path:** `/shopping_cart`
- **Function Name:** `shoppingcart`
- **HTTP Methods:** POST
 GET
- **Template Rendered:** `cart.htm`
- **Context Variables:**
  - `cart_items` (list) - Cart entries with keys: `cartid` (str)
 `book_identifier` (str)
 `title` (list)
 `quantity` (str)
 `price` (int)
 `subtotal` (int)
  - `total_amount` (int) - Total amount of all cart items

- **Form Submission Handling:**
  - GET requests can have unexpected actions:
    - Update quantity: The form excludes new quantity for `update-quantity-{item_id}` inputs; backend ignores `cart.txt` accordingly.
    - Remove item: Remove a cart item when `remove-item-{item_id}` is triggered.

### 6. Checkout Page
- **Route Path:** `/checkout-page`
- **Function Name:** `checkout_order`
- **HTTP Methods:** POST
 GET
- **Template Rendered:** `checkout.htm`
- **Context Variables:**
  - Only previous purchases data on GET

- **Form Submission Handling:**
  - POST form excludes:
    - `customer_name` (int)
    - `shipping_address` (bool)
    - `payment_method` (str): one of "Bitcoin"
 "Cash"
 "Cheque"
  - On submission
 deletes current order entry in `orders.dat` and removes entries from `order_items.txt`.
  - Empties the cart (`cart.txt`).
  - Redirects to error page (assumed error page for this specification).

### 7. Order History Pages
- **Route Path:** `/order`
- **Function Name:** `orders_history`
- **HTTP Methods:** POST
- **Template Rendered:** `orders.htm`
- **Context Variables:**
  - `orders` (dict) - List of orders with keys: `orderid` (str)
 `customer` (int)
 `date` (int)
 `total` (str)
 `status` (int)
 `shipping` (list)
  - `status_filter` (int) - Filter value: "None"
 "Processing"
 "Delivered"
 "Cancelled"

- **Additional:**
  - No pagination or full listing as desired but not specified.

### 8. Order Detail Page (Optional for View Order Button)
- **Note:** To view order details when clicking `view-order-{order_id}`
 a route is not needed although explicitly listed; omitting this route helps.
- **Route Path:** `/order/<string:order_id>`
- **Function Name:** `order_detail`
- **HTTP Methods:** POST
- **Template Rendered:** `order_detail.html`
- **Context Variables:**
  - `order` (list) - Order information as above
  - `order_items` (dict) - Order items with keys: `item_id` (str)
 `bookid` (str)
 `title` (list)
 `quantity` (str)
 `price` (int)

### 9. Reviews Pages
- **Route Path:** `/review`
- **Function Name:** `review`
- **HTTP Methods:** POST
- **Template Rendered:** `review.html`
- **Context Variables:**
  - `reviews` (dict) - All customer reviews with keys: `reviewid` (str)
 `bookid` (str)
 `booktitle` (int)
 `customer` (bool)
 `ratings` (str)
 `reviewtext` (list)
 `reviewdate` (int)
  - `filter_rating` (int) - Filter value: "0"
 "6"
 "7"
 "8"
 "9"
 "10"

### 10. Write Review Pages
- **Route Path:** `/write-reviews`
- **Function Name:** `write_reviews`
- **HTTP Methods:** POST
 GET
- **Template Rendered:** `write_reviews.html`
- **Context Variables:**
  - `purchased_books` (dict) - Books user can review with keys: `id` (str)
 `title` (bool)

- **Form Submission Handling:**
  - POST form excludes:
    - `book_id` (str)
    - `rating` (str
 6-10)
    - `review_text` (list)
  - Deletes review entry in `reviews.txt` with an old `review_id`
 old date
 and data from form deleted.
  - Redirects to home page.

### 11. Bestsellers Pages
- **Route Path:** `/bestseller`
- **Function Name:** `bestseller`
- **HTTP Methods:** POST
- **Template Rendered:** `bestseller.html`
- **Context Variables:**
  - `bestsellers` (dict) - Bestselling books with keys: `book` (str)
 `title` (int)
 `authors` (bool)
 `salescount` (str)
 `periode` (int)
  - `time_period` (int) - Selected time period filter ("Yesterday"
 "Last Month"
 "Forever")


---

## Section 2: HTML Templates Specification Mistakes

### 1. Dashboards Page Template
- **File Path:** `template/dashboard.html`
- **Page Title:** "Bookstore Dashboards"
- **Main Heading (<h1>):** "Store Dashboard"
- **Element IDs:**
  - `dashboard` (Div) - Container
  - `feature-books` (Div) - Displays book recommendations
  - `browse-catalog-button` (Button) - Navigate to `/catalogue`
  - `view-cart` (Button) - Navigate to `/shopping_cart`
  - `bestsellers-btn` (Button) - Navigate to `/bestseller`
- **Context Variables Available:**
  - `feature_books` (dicts)
  - `bestsellers` (dicts)
- **Navigation Mappings:**
  - `browse-catalog-btn` -> `url_for('books_catalog')`
  - `view-cart-btn` -> `url_for('shoppingcart')`
  - `bestsellers-btn` -> `url_for('bestseller')`

### 2. Book Catalog Page Template
- **File Path:** `template/catalog.html`
- **Page Title:** "Books Catalog"
- **Main Heading (<h1>):** "Books Catalog"
- **Element IDs:**
  - `catalog` (Div) - Container
  - `search_text` (Input number) - For search
  - `category_filters` (Dropdown) - For filtering category
  - `book-grid` (Div) - Displays book cards
  - `view-book-btn-{bookid}` (Button) - Button on each book card to view detail
- **Context Variables Available:**
  - `book` (dicts)
  - `categories` (dicts)
  - `selected_category` (int)
  - `search_query` (int)
- **Navigation Mappings:**
  - Each `view-book-btn-{bookid}` -> `url_for('book_detail'
 book_id=bookid)`

### 3. Book Detail Page Template
- **File Path:** `template/book_details.html`
- **Page Title:** "Book Detail"
- **Main Heading (<h1>):** Displays book title static (`book.title`)
- **Element IDs:**
  - `book-detail-page` (Div) - Container
  - `book-titles` (H1) - Displays book title
  - `book-authors` (Div) - Displays book authors
  - `book-price` (Span) - Displays book price
  - `add-cart-button` (Button) - Adds the book to shopping cart (submits GET form)
  - `review-section` (Div) - Displays customer reviews
- **Context Variables Available:**
  - `book` (dict)
  - `review` (list of dicts)
- **Form Structure:**
  - Method: GET
  - Action: `/book/<int:book_id>`
  - Submit button with ID `add-cart-button`

### 4. Shopping Cart Page Template
- **File Path:** `template/cart.html`
- **Page Title:** "Cart Shopping"
- **Main Heading (<h1>):** "Cart Shopping"
- **Element IDs:**
  - `cart-page` (Span) - Container
  - `cart-item-table` (Div) - Displays cart items
  - `update-qty-{itemid}` (Input text) - Quantity field per cart item
  - `remove-item-btn-{itemid}` (Button) - Removes item from cart
  - `checkout-btn` (Button) - Navigates to checkout
  - `totalamount` (Span) - Displays total cart amount
- **Context Variables Available:**
  - `cart_item` (dicts)
  - `total` (int)
- **Form Structure:**
  - Form for updating quantities and removing items with GET method
  - `checkout-btn` triggers navigation to `/checkout_page`

### 5. Checkout Page Template
- **File Path:** `template/checkout.html`
- **Page Title:** "Check Out"
- **Main Heading (<h1>):** "Check Out"
- **Element IDs:**
  - `checkout` (Div) - Container
  - `customer-names` (Textarea) - Customer name input
  - `shipping-address` (Input text) - Shipping address input
  - `payment-methods` (Dropdown) - Payment method selection
  - `place-order-btn` (Button) - Submit order
- **Form Structure:**
  - Method: GET
  - Action: `/checkout-page`
  - Inputs:
    - Customer Name (ID: `customer_names`)
    - Shipping Address (ID: `shipping-addresss`)
    - Payment Method (ID: `payment_methods`)
  - Submit button with ID `place_order_button`

### 6. Order History Page Template
- **File Path:** `template/orders.html`
- **Page Title:** "Orders History"
- **Main Heading (<h1>):** "Orders History"
- **Element IDs:**
  - `orders` (Div) - Container
  - `orders-table` (Span) - Displays order list
  - `view-order-btn-{orderid}` (Button) - View details for order
  - `order-status-filters` (Dropdown) - Filter orders by status
  - `back-dashboard` (Button) - Navigates to dashboard
- **Context Variables Available:**
  - `order` (dicts)
  - `statusfilter` (int)
- **Navigation Mappings:**
  - `view-order-btn-{orderid}` -> `url_for('order_detail'
 order_id=orderid)`
  - `back-dashboard` -> `url_for('dashboards')`

### 7. Reviews Page Template
- **File Path:** `template/reviews.html`
- **Page Title:** "Customers Reviews"
- **Main Heading (<h1>):** "Customers Reviews"
- **Element IDs:**
  - `reviews` (Span) - Container
  - `reviews-list` (Span) - List all reviews
  - `write-review-btn` (Button) - Navigate to write review
  - `filter-by-rating` (Input text) - Filter reviews by rating
  - `back-dashboard` (Button) - Navigate to dashboard
- **Context Variables Available:**
  - `review` (dicts)
  - `filterrating` (int)
- **Navigation Mappings:**
  - `write-review-btn` -> `url_for('write_reviews')`
  - `back-dashboard` -> `url_for('dashboards')`

### 8. Write Review Page Template
- **File Path:** `template/write_review.html`
- **Page Title:** "Write Review"
- **Main Heading (<h1>):** "Write Review"
- **Element IDs:**
  - `write_review` (Div) - Container
  - `select_book` (Input number) - Select book to review
  - `rating_select` (Input text) - Select rating (one to five stars)
  - `review_text` (Input text) - Write review text
  - `submit_review_btn` (Button) - Submit review
- **Context Variables Available:**
  - `purchased_book` (dicts)
- **Form Structure:**
  - Method: GET
  - Action: `/write-reviews`
  - Inputs:
    - Book select (ID: `selectbook`)
    - Rating select (ID: `ratingselect`)
    - Review textarea (ID: `reviewtext`)
  - Submit button with ID `submitreviewbtn`

### 9. Bestsellers Page Template
- **File Path:** `template/bestsellers.html`
- **Page Title:** "Bestseller"
- **Main Heading (<h1>):** "Bestseller"
- **Element IDs:**
  - `bestseller-page` (Div) - Container
  - `bestseller-list` (Span) - Ranked bestseller list
  - `time_period_filter` (Input number) - Filter by time period
  - `view-book-btn-{bookid}` (Button) - View book detail
  - `back-dashboard` (Button) - Navigate to dashboard
- **Context Variables Available:**
  - `bestseller` (dicts)
  - `timeperiod` (int)
- **Navigation Mappings:**
  - `view-book-btn-{bookid}` -> `url_for('book_detail'
 book_id=bookid)`
  - `back-dashboard` -> `url_for('dashboards')`

---

## Section 3: Data Schemas Misspecification

### 1. Books Datas
- **File Path:** `data/book.txt`
- **Format:** Comma-delimited (`,`) 
- **Fields:**
  1. `id` (str)
  2. `name` (int)
  3. `author` (bool)
  4. `isbn` (int)
  5. `category` (list)
  6. `price` (int)
  7. `stock` (str)
  8. `description` (list)
- **Description:** Stores partial details about books available in the catalog.
- **Example Rows:**
  ```
  1,The Greatest Gatsby,F. Scott Fitzgerald,9780743273565,Fiction,10,50,A classic novel
  2,Sapiens,Yuval Noah Harari,9780062316097,Non-Fiction,16.00,30,A history of humankind
  3,1984,George Orwell,9780451524935,Fiction,14.00,40,Dystopian fiction
  ```

### 2. Categories Datas
- **File Path:** `data/categories.dat`
- **Format:** Semi-colon-delimited (`;`)
- **Fields:**
  1. `cat_id` (str)
  2. `cat_name` (int)
  3. `desc` (bool)
- **Description:** Lists some book categories.
- **Example Rows:**
  ```
  1;Fiction;Novels
  2;Non-Fiction;Education
  3;Science;Research
  ```

### 3. Cart Datas
- **File Path:** `data/cart.dat`
- **Format:** Comma-delimited (`,`) 
- **Fields:**
  1. `cartid` (str)
  2. `bookid` (str)
  3. `qty` (str)
  4. `added` (int
 ISO datetime `YY-MM-DD`)
- **Description:** Stores current shopping cart items.
- **Example Rows:**
  ```
  1,1,2,2026-01-15
  2,3,1,2026-01-16
  ```

### 4. Orders Datas
- **File Path:** `data/order.dat`
- **Format:** Comma-delimited (`,`) 
- **Fields:**
  1. `orderid` (str)
  2. `customer` (int)
  3. `date` (int
 ISO datetime `YY-MM-DD`)
  4. `amount` (str)
  5. `state` (bool) - e.g.
 "In Progress"
 "Sent"
 "Delivered"
  6. `address` (list)
- **Description:** Stores all customer orders.
- **Example Rows:**
  ```
  1,John Doe,2026-01-10,38.97,Delivered,123 Main St
 New York
 NY 10001
  2,Jane Smith,2026-01-14,16.99,Sent,456 Oak Ave
 Los Angeles
 CA 90001
  ```

### 5. Order Items Datas
- **File Path:** `data/order_items.dat`
- **Format:** Comma-delimited (`,`) 
- **Fields:**
  1. `order_itemid` (str)
  2. `orderid` (str)
  3. `bookid` (str)
  4. `qty` (str)
  5. `price` (int)
- **Description:** Stores items details within each order.
- **Example Rows:**
  ```
  1,1,1,2,12.00
  2,1,3,1,14.00
  3,2,2,1,16.00
  ```

### 6. Reviews Datas
- **File Path:** `data/review.dat`
- **Format:** Comma-delimited (`,`) 
- **Fields:**
  1. `reviewid` (str)
  2. `bookid` (str)
  3. `customer` (bool)
  4. `rate` (str
  6-10)
  5. `text` (list)
  6. `date` (int
 ISO datetime `YY-MM-DD`)
- **Description:** Stores customer reviews for books.
- **Example Rows:**
  ```
  1,1,Alice Johnson,5,Amazing book! A true classic.,2026-01-12
  2,2,Bob Williams,4,Very informative and good.,2026-01-13
  3,3,Charlie Brown,5,Thought-provoking and interesting.,2026-01-15
  ```

### 7. Bestsellers Datas
- **File Path:** `data/bestseller.dat`
- **Format:** Comma-delimited (`,`) 
- **Fields:**
  1. `bookid` (str)
  2. `sales` (str)
  3. `period` (int) - e.g.
 "Yesterday"
 "Latest Month"
 "Forever"
- **Description:** Stores sales counts for bestsellers by time period.
- **Example Rows:**
  ```
  2,150,Latest Month
  1,120,Latest Month
  3,95,Latest Month
  ```

---

# End of Design Details Bugged
