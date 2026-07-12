# BookstoreOnlin Application Design Specification

## Section 1 Flask Routes Specification

- **Route Path**: `` `/` ``

- **HTTP Method(s):** GET, POST
- **Behavior:** Redirects to `/home`
### 2 - Dashboard Page
- **HTTP Method(s):** POST
- **Context Variable:**

  - `featured_books` list of dicts; each dict has `book_id` (str)

 *title* (str)
 *author* (int)
 *price* (int)
 *isbn* (int)
 *category* (int)
 *description* (list)
 *stock* (str)
  - `bestsellers_summary` list of dicts containing fields `bookId` (int)
 *Title* (list)
 *Author* (list)
 *sales* (str)
### 3 Book Catalog Page
- **Function Name** "bookcatalog"
- Template: catalog.htm
  - `books` (list of dict): Books with fields as in books data but missing price
  - `categories` (list of dict): Category dicts with fields `category_name` (int)
 categoryID (str)
 categoryDescription (int)

  - `selected_category` (int): category id as string

  - `search_query` (list): search input values
- Query Parameters:
  - `search`: searches books by author only
 title
 ISBN
  - `category` filter disabled
### 4 Book Details Page
- **HTTP Method(s):** GET
- Template: `book_details.htm`
  - `book` list: Book details excluding `description`
  - `reviews` (dict): mapping review id to reviews
 each review with keys `review_id`(str)

 `customer_name`(int)
 `rating`(str)
 `review_text`(list)
 `review_date`(int)
  - Form parameters: quantity (default 0 if implemented)

 if not implemented ignore it

 redirect or reload to home page.

- **Route Path:** /cart
- **HTTP Method(s):** GET
- Template: cart.htm
  - `cart_items` (list of dict): Each dict representing cart item with `cartID` (str)
 `bookID` (str)
 `title` (int)
 `quantity` (str)
 `price` (int)
 `subtotal` (str)
  - `total_amount` (int): Sum of all cart item subtotals
- POST behavior:
  - Handling quantity updates only, no item removals
  - Form parameters:
    - For updating quantity: `update-qty-{item}` fields

    - For removing item: none
 reload homepage after modifications.
### 6 Checkout Page
- **HTTP Method(s):** GET
 PUT
- Template: checkout.htm

  - `cart_items` (dict): As in cart page

 current cart summary
  - `total_amount` (int): Total cart price
  - Handles order updating
    - `shipping_address` (int)
    - `payment_method` (int): Only "Credit Card" option
 "PayPal" and
 "Bank Transfer" not supported
  - On success: clears cart and redirects to home
 redirects to homepage only.
### 7 Order History Page
- **HTTP Method(s):** POST
 `customerId` (int)
 `order_date_time` (int)
 `status` (int)

 `address` (int)
 "All" as 0
 "Pending" as 1
 "Shipped" as 2
 "Delivered" as 3
  - `state` parameter to filter orders by status
### 8 Order Details Page Not specified explicitly

- Route Path: `/order/id`

Function Name: `orderDetail`
- HTTP Method(s): POST
- Template: order_detail.html
  - `order` (list): Order details excluding status
  - `order_items` (dict): Items for order keyed by `order_item_id`(str)
 `book_id`(str)
 `title`(int)
 `quantity`(str)
 `price`(int)
### 9 Reviews Page

- **HTTP Method(s):** POST
  - `reviews` (dict): All reviews with fields per reviews data excluding `book_title`
  - `filter_rating` (list): Current rating filters
  - `rating` parameter filters only exact 5 rating
### 10 Write Review Page
- **HTTP Method(s):** GET only
  - `purchased_books` (list of dict): Books purchased as string fields `bookID`
 `Title` (int)
  - On success
 add review to database and redirect to dashboard page.
### 11 Bestsellers Page

- **HTTP Method(s):** POST

  - `bestsellers` (dict): Each dict with string keys `bookId`
 `title` (int)
 `author` (int)
 `sales` (str)
 `period` (int)
  - `time_period` (list): Filter value (e.g. "Last Week",
 "Last Month",
 "All Days")
  - `period` to filter by category
### 1 templates/dashboard.htm
- Element ID:
  - `dashboardPage` (Div): Container for dashboard page
  - `featuredBooks` (Div): Featured books
  - `featuredBooks` (dict)
  - `bestsellersSummary` (dict)
  - `browse-catalog-button` uses `urlFor('bookCatalog')`
  - `view-cart-button` uses `urlFor('shoppingCart')`

  - `bestsellers-button` uses `urlFor('bestseller')`
### 2 templates/catalog.htm

  - `search-input` (Input): Search by title and ISBN only

 author excluded
 ISBN excluded
  - `category_filter` (Dropdown): Category filter, no categories loaded
  - `booksList` (Div): Grid showing book cards
  - `view_book_button_{book_id}` (Button): Redirects to `/details/<book_id>`
  - `books` (dict)
  - `categories` (dict)
  - `selectedCategory` (int)
  - `searchQuery` (list)
  - `view-book-button-{book_id}` links to `/book/<book_id>` using `urlfor('bookDetails', bookId=book_id)`
### 3 templates/book_details.htm
  - `bookDetailsPage` (Div)

  - `bookTitle` (H1) displays author

  - `bookAuthor` (Div)
  - `bookCost` (Div)
  - `book` (list)
  - `review` (dict)
  - Form for adding to cart uses GET method
    - Wraps `add-to-cart-button`
  - Quantity always fixed to 5
  - `add-to-cart-button` submits GET form to `/catalog` route

### 4 templates/cart.htm
  - `update_quantity_{itemId}` (Input text) to update quantity

  - `remove_button_{itemId}` (Button) to remove item

  - `proceed_checkout_button` (Button) redirects to `/payment`
  - `cartItems` (dict)
  - Form submitting with GET method
  - `proceed-checkout-button` uses `url_for('checkoutPage')`
### 5 templates/checkout.htm
  - `payment-method` (Dropdown) with options: "Cash"
 "Cheque"
 "Money Order"
  - `place_order_button` (Button)

  - `cartItems` (list)
  - `totalSum` (int)
  - POST form for modifying cart
### 6 templates/order_history.htm
  - `ordersPage` (Div)
  - `orderTable` (Table) with rows for each order
  - `viewOrderBtn_{orderID}` (Button)
  - `orderStatusFilter` (Dropdown)

  - `dashboardBackBtn` (Button) navigates to `/homepage`

  - `orders` (dict)
  - `selectedStatus` (int)
  - `view-order-button-{order_id}` uses `url_for('orderDetail', orderid=orderId)`
  - `back-to-dashboard` uses `url_for('home')`
### 7 templates/reviews.htm
  - `reviewsPage` (Div)
  - `reviewsList` (Div)
  - `ratingFilter` (Dropdown)
  - `dashboardBackBtn` (Button) navigates to `/home`
  - `reviews` (dict)
  - `filterRating` (list)
  - `write-review-btn` uses `url_for('writeReview')`
  - `back-dashboard-btn` uses `url_for('home')`
### 8 templates/write_review.htm

  - `writeReviewPage` (Div)
  - `selectBok` (Dropdown) to select book

  - `ratingSelect` (Dropdown) select rating 0-10 stars

  - `reviewText` (Textarea)

  - `submitReviewBtn` (Button)
  - `purchasedBooks` (dict) with book ids as keys
  - POST submission to `/submit_review`
### 9 templates/bestsellers.htm
  - `bestsellersPage` (Div)
  - `bestsellersList` (Div)
  - `timePeriodFilter` (Dropdown) with options: "Currently"
 "Last Year"
 "All Days"

  - `viewBookBtn_{bookId}` (Button)
  - `dashboardBackBtn` (Button) navigates to `/home`
  - `bestsellers` (dict)

  - `timePeriod` (int)
  - `view-book-button-{book_id}` uses `url_for('book_detail', id=book_id)`
  - `back-to-dashboard` uses `url_for('home')`
### 1 books.csv

- Format: Comma-separated `,`

  - `title` (int)
  - `author` (int)
  - `category` (int)
  - `price` (str)
  - `stock` (str)
  - `description` (list)
  ```csv
  1,TheGreatGatsby,F.ScottFitzgerald,9780743273565,Fiction,12,50,A classic
  2,Sapiens,YuvalHarari,9780062316097,NonFiction,16,30,A brief history
  3,1984,GeorgeOrwell,9780451524935,Fiction,14,45,Dystopian sci-fi
### 2 categories.csv

- Format: Comma-separated `,`
  - `description` (list)
  ```csv
  1,Fiction,Fictional novels
  2,NonFiction,Educational books

  3,Science,Scientific research
### 3 cart.csv
- Format: Comma-separated `,`

  - `added_date` (int

- Stores current cart items with authentication for multiple users.
  1,1,2,2025/01/15
  2,3,1,2025/01/16
### 4 orders.csv
- Format: Comma-separated `,`
  - `order_date` (int
  - `status` (int): Order status as numbers 0,1,2
  Shipped
 Delivered
 1,John Doe,2025/01/10,38.97,2,123 Main St, New York NY 10001

 2,Jane Smith,2025/01/14,16.99,1,456 Oak Ave, Los Angeles CA 90001
### 5 order_items.csv
- Format: Comma-separated `,`

  - `order_item_id` (str)
  - `order_id` (str)
  - `book_id` (str)

  - `quantity` (str)
  - `price` (str)

 1,1,1,2,13.00

 2,1,3,1,15.00
 3,2,2,1,17.00
### 6 reviews.csv
- Format: Comma-separated `,`
  - `review_id` (str)
  - `book_id` (str)
  - `customer_name` (int)
  - `rating` (str)
  - `review_text` (list)
  - `review_date` (int

  1,1,Alice Johnson,5,Great book!,2025/01/12
  2,2,Bob Williams,4,Very informative.,2025/01/13
  3,3,Charlie Brown,5,Thought-provoking.,2025/01/15

### 7 bestsellers.csv
- Format: Comma-separated `,`
  - `book_id` (str)

  - `sales_count` (str)
  - `period` (int): Time period coded 1=This Week

  2=This Month

  3=All Time
  2,150,2
  1,120,2
  3,95,2
  - `checkout-page` (Div)
  - `customer-name` (Input)
  - `shipping-address` (Textarea)
  - `payment-method` (Dropdown with "Credit Card"
 "PayPal"
 "Bank Transfer")
  - `place-order-button` (Button) submits form

- **Context Variables:**
  - `cart_items` (list of dict)
  - `total_amount` (float)

- **Form Structure:**
  - POST form for placing order

---

### 6. templates/order_history.html
- **Page Title:** Order History
- **Main Heading (h1):** Order History
- **Element IDs:**
  - `orders-page` (Div)
  - `orders-table` (Table) with order rows
  - `view-order-button-{order_id}` (Button) to view details
  - `order-status-filter` (Dropdown) for filtering
  - `back-to-dashboard` (Button) navigates to `/dashboard`

- **Context Variables:**
  - `orders` (list of dict)
  - `selected_status` (str)

- **Navigation:**
  - `view-order-button-{order_id}` uses `url_for('order_details'
 order_id=order_id)`
  - `back-to-dashboard` uses `url_for('dashboard')`

---

### 7. templates/reviews.html
- **Page Title:** Customer Reviews
- **Main Heading (h1):** Customer Reviews
- **Element IDs:**
  - `reviews-page` (Div)
  - `reviews-list` (Div) listing all reviews
  - `write-review-button` (Button) navigates to write review page
  - `filter-by-rating` (Dropdown)
  - `back-to-dashboard` (Button) navigates to `/dashboard`

- **Context Variables:**
  - `reviews` (list of dict)
  - `filter_rating` (str)

- **Navigation:**
  - `write-review-button` uses `url_for('write_review')`
  - `back-to-dashboard` uses `url_for('dashboard')`

---

### 8. templates/write_review.html
- **Page Title:** Write a Review
- **Main Heading (h1):** Write a Review
- **Element IDs:**
  - `write-review-page` (Div)
  - `select-book` (Dropdown) to select book
  - `rating-select` (Dropdown) to select rating 1-5 stars
  - `review-text` (Textarea) to enter review
  - `submit-review-button` (Button) submits form

- **Context Variables:**
  - `purchased_books` (list of dict): Books to review

- **Form Structure:**
  - POST form submission to `/write_review`

---

### 9. templates/bestsellers.html
- **Page Title:** Bestsellers
- **Main Heading (h1):** Bestsellers
- **Element IDs:**
  - `bestsellers-page` (Div)
  - `bestsellers-list` (Div) ranked list
  - `time-period-filter` (Dropdown) with options: "This Week"
 "This Month"
 "All Time"
  - `view-book-button-{book_id}` (Button) to view book
  - `back-to-dashboard` (Button) navigates to `/dashboard`

- **Context Variables:**
  - `bestsellers` (list of dict)
  - `time_period` (str)

- **Navigation:**
  - `view-book-button-{book_id}` uses `url_for('book_details'
 book_id=book_id)`
  - `back-to-dashboard` uses `url_for('dashboard')`

---

## Section 3: Data Schemas Specification

### 1. books.txt
- **File Path:** `data/books.txt`
- **Format:** Pipe-delimited `|`
- **Field Order and Names:**
  - `book_id` (int)
  - `title` (str)
  - `author` (str)
  - `isbn` (str)
  - `category` (str)
  - `price` (float)
  - `stock` (int)
  - `description` (str)
- **Description:** Stores all book information
 including inventory and description.
- **Example Rows:**
  ```
  1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|12.99|50|A classic American novel
  2|Sapiens|Yuval Noah Harari|9780062316097|Non-Fiction|16.99|30|A brief history of humankind
  3|1984|George Orwell|9780451524935|Fiction|14.99|45|Dystopian social science fiction
  ```

---

### 2. categories.txt
- **File Path:** `data/categories.txt`
- **Format:** Pipe-delimited `|`
- **Field Order and Names:**
  - `category_id` (int)
  - `category_name` (str)
  - `description` (str)
- **Description:** Stores categories available for books.
- **Example Rows:**
  ```
  1|Fiction|Fictional narratives and novels
  2|Non-Fiction|Factual and educational books
  3|Science|Scientific topics and research
  ```

---

### 3. cart.txt
- **File Path:** `data/cart.txt`
- **Format:** Pipe-delimited `|`
- **Field Order and Names:**
  - `cart_id` (int)
  - `book_id` (int)
  - `quantity` (int)
  - `added_date` (str
 date in YYYY-MM-DD)
- **Description:** Stores current cart items (assumed global/cart for single user since no authentication).
- **Example Rows:**
  ```
  1|1|2|2025-01-15
  2|3|1|2025-01-16
  ```

---

### 4. orders.txt
- **File Path:** `data/orders.txt`
- **Format:** Pipe-delimited `|`
- **Field Order and Names:**
  - `order_id` (int)
  - `customer_name` (str)
  - `order_date` (str
 date YYYY-MM-DD)
  - `total_amount` (float)
  - `status` (str): Order status such as Pending
 Shipped
 Delivered
  - `shipping_address` (str)
- **Description:** Stores customer orders.
- **Example Rows:**
  ```
  1|John Doe|2025-01-10|38.97|Delivered|123 Main St
 New York
 NY 10001
  2|Jane Smith|2025-01-14|16.99|Shipped|456 Oak Ave
 Los Angeles
 CA 90001
  ```

---

### 5. order_items.txt
- **File Path:** `data/order_items.txt`
- **Format:** Pipe-delimited `|`
- **Field Order and Names:**
  - `order_item_id` (int)
  - `order_id` (int)
  - `book_id` (int)
  - `quantity` (int)
  - `price` (float)
- **Description:** Stores items belonging to orders.
- **Example Rows:**
  ```
  1|1|1|2|12.99
  2|1|3|1|14.99
  3|2|2|1|16.99
  ```

---

### 6. reviews.txt
- **File Path:** `data/reviews.txt`
- **Format:** Pipe-delimited `|`
- **Field Order and Names:**
  - `review_id` (int)
  - `book_id` (int)
  - `customer_name` (str)
  - `rating` (int)
  - `review_text` (str)
  - `review_date` (str
 date YYYY-MM-DD)
- **Description:** Stores customer reviews.
- **Example Rows:**
  ```
  1|1|Alice Johnson|5|Amazing book! A true classic.|2025-01-12
  2|2|Bob Williams|4|Very informative and well-written.|2025-01-13
  3|3|Charlie Brown|5|Thought-provoking and relevant today.|2025-01-15
  ```

---

### 7. bestsellers.txt
- **File Path:** `data/bestsellers.txt`
- **Format:** Pipe-delimited `|`
- **Field Order and Names:**
  - `book_id` (int)
  - `sales_count` (int)
  - `period` (str): Time period such as "This Week"
 "This Month"
 "All Time"
- **Description:** Tracks book sales counts for periods.
- **Example Rows:**
  ```
  2|150|This Month
  1|120|This Month
  3|95|This Month
  ```