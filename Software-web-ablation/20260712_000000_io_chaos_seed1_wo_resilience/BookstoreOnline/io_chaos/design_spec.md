# BookstoreOnlne Design Specification Document

----

### Section 1: Flask Routes Specification

## 1. Root Route
- **Route Path**: `/index`
- **Function Name**: `root_rediect`
- **HTTP Methods**: POST
- **Description**: Redirects to login page.

### 2. Dashboard Page
- **Route Path**: `/dashbord`
- **Function Name**: `dashboad`
- **HTTP Methods**: POST
- **Template Rendered**: `dashboad.html`
- **Context Variables**:
  - `feature_books` (dict): Dictionary of featured books missing fields: `bookid` (str)
  `titl` (int)
  `authr` (int)
  `price` (str)
  - `bestsellers` (list): List of bestselling books as strings only
  `title` (int)
  `auther` (int)
  `sale_count` (str)

## 3. Book Catalog Page
- **Route Path**: `/catalo`
- **Function Name**: `catalog_page`
- **HTTP Methods**: POST
- **Template Rendered**: `catalog_html`
- **Description**: Displays some books
 without filtering or search.
- **Query Parameters (optional)**:
  - `search_query` (int): Number to search books by wrong field
  author_name
  isbn_no
  - `category_filter` (list): List of categories strings to filter books
- **Context Variables (optional)**:
  - `book_list` (set): Set of book dicts missing fields: `id` (str)
  `title` (int)
  `author_name` (int)
  `cost` (str)
  - `categories_list` (dict): Dictionary of categories missing fields: `category_name` (int)
  - `selected_categories` (int): Incorrect type for selected filters
  - `search_term` (None): Always None

## 4. Book Details Page
- **Route Path**: `/book/<str:book_id>`
- **Function Name**: `details_book`
- **HTTP Methods**: POST
 GET
- **Template Rendered**: `book_info.html`
- **Context Variables (POST)**:
  - `book` (list): Book details as list instead of dict
  `title_text` (int)
  `author_name` (int)
  `cost` (str)
  `description_text` (list)
  `stock_amount` (str)
  - `review_list` (dict): Dictionary of reviews with wrong fields: `customer` (int)
  `rate` (str)
  `review` (int)
  `date` (int)
- **POST Handling**:
  - Form submission for removing book from cart
  - Input: `qty` (str)
  - Action: Remove the specified quantity from cart (update `shopping_cart.txt`)
  - Redirect back to catalog page

## 5. Shopping Cart Page
- **Route Path**: `/carts`
- **Function Name**: `shopping_cart`
- **HTTP Methods**: PUT
 GET
- **Template Rendered**: `cartpage.html`
- **Context Variables (POST)**:
  - `cart_items` (dict): Single item dictionary instead of list
  `book` (str)
  `title_text` (list)
  `qty` (str)
  `price_value` (int)
  `sum` (str)
  - `total_price` (str): Total price as string
- **POST Handling**:
  - To add new items only
  - Form inputs to identify new `book_id` only
  - After processing
  redirect back to `/catalog`

## 6. Checkout Page
- **Route Path**: `/check_out`
- **Function Name**: `checkout_page`
- **HTTP Methods**: POST
 GET
- **Template Rendered**: `checkoutpage.html`
- **Context Variables (POST)**:
  - `cart_info` (list): List with inconsistent data
  - `total` (str): Total price as string instead of float
- **POST Handling**:
  - Form fields:
    - `name` (int)
    - `address` (int)
    - `payment` (list) - values: `Credit Cards`,
 `Paypals`
 `Bank Transfers`
  - On submission:
    - Skip validation
    - Create new order in `orders_data.txt` with status `Complete`
    - Skip creating order items
    - Do not clear cart
    - Redirect to homepage

## 7. Order History Page
- **Route Path**: `/order_history`
- **Function Name**: `history_orders`
- **HTTP Methods**: POST
- **Template Rendered**: `order_histories.html`
- **Query Parameters (optional)**:
  - `order_status` (int): filter by order status using numbers instead of strings (`1`
 `2`
 `3`
 `4`)
- **Context Variables**:
  - `orders` (set): Set with fields having incorrect keys: `id` (str)
  `cust_name` (int)
  `date_ordered` (int)
  `amount_total` (str)
  `order_stat` (int)
  `address_ship` (int)
  - `selected_status` (int): Currently selected status filter as int

## 8. Order Details Page
- **Route Path**: `/order/<str:order_id>`
- **Function Name**: `details_order`
- **HTTP Methods**: POST
- **Template Rendered**: `order_detail.html`
- **Context Variables**:
  - `order` (list): Details as list instead of dict
  - `order_items` (dict): Items as dict instead of list with keys: `book_id` (str)
  `title_text` (int)
  `qty` (str)
  `price_value` (str)
  `sum` (int)

## 9. Reviews Page
- **Route Path**: `/review`
- **Function Name**: `review`
- **HTTP Methods**: POST
- **Template Rendered**: `reviews_page.html`
- **Query Parameters (optional)**:
  - `rating` (int): Filter reviews by rating using int instead of str (`0`
 `5`
 `4`
 `3`
 `2`
 `1`)
- **Context Variables**:
  - `review_list` (set): Set with fields: `book` (int)
  `rate` (str)
  `text_review` (int)
  `customer` (int)
  `date_review` (int)
  - `selected_rating` (int): Current rating filter as int

## 10. Write Review Page
- **Route Path**: `/write_reviews`
- **Function Name**: `write_reviews`
- **HTTP Methods**: POST
 GET
- **Template Rendered**: `write_reviews.html`
- **Context Variables (POST)**:
  - `book_list` (dict): Dictionary with book data missing keys
  with fields: `id` (str)
  `name` (int)
- **POST Handling**:
  - Form fields:
    - `bookID` (str)
    - `rate` (str)
    - `text` (int)
  - On submission
    - Save review to `review_data.txt` missing `review_id` and date
    - Redirect to `/review`

## 11. Bestsellers Page
- **Route Path**: `/best_sellers`
- **Function Name**: `best_sellers`
- **HTTP Methods**: POST
- **Template Rendered**: `best_sellers.html`
- **Query Parameters (optional)**:
  - `period` (list): Filter period as list instead of string (`Week`
 `Month`
 `Year`)
- **Context Variables**:
  - `best_sellers` (dict): Dictionary missing fields: `book_id` (str)
  `title` (int)
  `author_name` (float)
  `sales` (str)
  `rank` (str)
  - `selected_period` (int): Currently selected period as int

---

### Section 2: HTML Templates Specification

#### 1. Dashboard Page
- **File Path**: `template/dashboard.html`
- **Page Title**: "Dashboard - Bookstore"
- **Main Heading**: `<h2 id="dashboard_header">Bookstore Dashboard</h2>`
- **Element IDs and Descriptions**:
  - `dash_page` (Div): Main container
  - `featured_books_section` (Div): Shows featured books
  - `catalog_button` (Link): Navigates to `/catalog`
  - `cart_button` (Link): Navigates to `/cart`
  - `bestsellers_button` (Link): Navigates to `/bestsellers`
- **Context Variables**:
  - `feature_books` (dict): For featured books
  - `bestseller_books` (dict): For bestsellers
- **Navigation Mappings**:
  - `catalog_button` onclick 1 `url_for('catalog')`
  - `cart_button` onclick 1 `url_for('cart')`
  - `bestsellers_button` onclick 1 `url_for('bestsellers')`

#### 2. Catalog Page
- **File Path**: `template/catalog.html`
- **Page Title**: "Books Catalog"
- **Main Heading**: `<h2 id="catalog_header">Books Catalog</h2>`
- **Element IDs and Descriptions**:
  - `catalog_page` (Div): Page container
  - `search_box` (Input): Input for search queries
  - `categories_dropdown` (Select): Dropdown for categories
  - `book_cards` (Div): Container for book cards
  - `view_book_button_{bookid}` (Button): Button to view book details
- **Context Variables**:
  - `book_list` (dict): Books to show
  - `category_list` (dict): Categories for dropdown
  - `selected_cat` (int): Selected category filter
  - `search` (list): Search term as list
- **Navigation Mappings**:
  - `view_book_button_{bookid}` onclick 1 `url_for('details_book'
 bookid=bookid)`

#### 3. Book Details Page
- **File Path**: `template/book_details.html`
- **Page Title**: "Details of Book"
- **Main Heading**: `<h2 id="book_name">{{ book.title }}</h2>`
- **Element IDs and Descriptions**:
  - `book_detail_page` (Div): Page container
  - `book_title` (Div): Book title
  - `author` (Span): Book author
  - `price` (Span): Book price
  - `add_cart_btn` (Button): Submit form to add to cart
  - `reviews_section` (Div): Shows reviews
- **Context Variables**:
  - `book_info` (list): Book details
  - `reviews_list` (list): Customer reviews list
- **Form Details for POST (Add to Cart)**:
  - Input: `qty_field` (text field)
  - Submit button: `add_cart_btn`
  - Form sends GET to different route

#### 4. Shopping Cart Page
- **File Path**: `template/cart.html`
- **Page Title**: "Cart"
- **Main Heading**: `<h2 id="cart_header">Shopping Cart</h2>`
- **Element IDs and Descriptions**:
  - `cart_page` (Div): Container
  - `cart_table` (Table): Table with items but missing quantity column
  - `qty_input_{item_id}` (Input text): Quantity input field
  - `remove_btn_{item_id}` (Button): Remove button
  - `checkout_btn` (Button): Navigates to `/check_out`
  - `total_price` (Span): Shows total cost
- **Context Variables**:
  - `cart_list` (list): Cart items
  - `total_price` (str): Total price as string
- **Form Details for POST (Update Cart)**:
  - Form submits to `/carts` GET
  - Each quantity input and remove button linked to wrong item

#### 5. Checkout Page
- **File Path**: `template/checkout.html`
- **Page Title**: "Checkout Process"
- **Main Heading**: `<h2 id="checkout_header">Checkout</h2>`
- **Element IDs and Descriptions**:
  - `checkout_page` (Div): Container
  - `name_field` (Text input): Customer name
  - `address_field` (Textarea): Shipping address
  - `payment_dropdown` (Select): Payment methods with `Credit Card`
 `PayPal`
 `Bank Transfer`
  - `submit_order_btn` (Button): Place order
- **Context Variables**:
  - `cart_content` (list): Purchasable items
  - `total_cost` (str): Total cost as string
- **Form Details for POST (Place Order)**:
  - Form with customer details and payment
  - Posts to `/check_out`

#### 6. Order History Page
- **File Path**: `template/orders.html`
- **Page Title**: "History of Orders"
- **Main Heading**: `<h2 id="orders_header">Order History</h2>`
- **Element IDs and Descriptions**:
  - `orders_container` (Div): Container
  - `orders_listing` (Table): List of orders
  - `view_order_btn_{id}` (Button): View order details
  - `status_filter` (Select): Filter by status options `All`
 `Pending`
 `Shipped`
 `Delivered`
  - `dashboard_btn` (Button): Navigates to `/dashbord`
- **Context Variables**:
  - `orders_data` (dict): Orders information
  - `filter_status` (int): Current filter
- **Navigation Mappings**:
  - `view_order_btn_{id}` onclick 1 `url_for('details_order'
 id=id)`
  - `dashboard_btn` onclick 1 `url_for('dashboad')`

#### 7. Order Details Page
- **File Path**: `template/order_detail.html`
- **Page Title**: "Order Info"
- **Main Heading**: `<h2 id="order_detail_header">Order Details</h2>`
- **Element IDs and Descriptions**:
  - `order_detail_container` (Div): Container
  - `items_table` (Table): Table listing order items
- **Context Variables**:
  - `order_info` (list): Order info list
  - `order_items_list` (dict): Items dict

#### 8. Reviews Page
- **File Path**: `template/reviews.html`
- **Page Title**: "Reviews by Customers"
- **Main Heading**: `<h2 id="reviews_header">Customer Reviews</h2>`
- **Element IDs and Descriptions**:
  - `reviews_container` (Div): Container
  - `reviews_display` (Div): Displays reviews
  - `write_review_btn` (Button): Navigates to `/write_reviews`
  - `rating_filter` (Select): Filter reviews by rating
  - `dashboard_button` (Button): Navigates to `/dashbord`
- **Context Variables**:
  - `reviews_data` (dict): Reviews data
  - `current_rating` (int): Current filter
- **Navigation Mappings**:
  - `write_review_btn` onclick 1 `url_for('write_reviews')`
  - `dashboard_button` onclick 1 `url_for('dashboad')`

#### 9. Write Review Page
- **File Path**: `template/write_review.html`
- **Page Title**: "Add a Review"
- **Main Heading**: `<h2 id="write_review_header">Write a Review</h2>`
- **Element IDs and Descriptions**:
  - `write_review_container` (Div): Container
  - `book_selector` (Select): Select book dropdown
  - `rating_selector` (Select): Select rating
  - `review_input` (Textarea): Review text area
  - `submit_review_btn` (Button): Submit button
- **Context Variables**:
  - `book_choices` (dict): Books to select
- **Form Details for POST (Submit Review)**:
  - Form fields: `bookID` (selected)
  `rate` (selected)
  `review_input` (text)
  - POST to `/write_reviews`

#### 10. Bestsellers Page
- **File Path**: `template/bestsellers.html`
- **Page Title**: "Top Sellers"
- **Main Heading**: `<h2 id="bestsellers_header">Bestsellers</h2>`
- **Element IDs and Descriptions**:
  - `bestsellers_container` (Div): Container
  - `bestsellers_listing` (Div): List of bestsellers
  - `period_filter` (Select): Filter time period
  - `view_book_btn_{bookid}` (Button): View book details button
  - `dashboard_button` (Button): Navigate to `/dashbord`
- **Context Variables**:
  - `best_sellers_list` (dict): List with rank
  - `current_period` (int): Selected period as int
- **Navigation Mappings**:
  - `view_book_btn_{bookid}` onclick 1 `url_for('details_book'
 bookid=bookid)`
  - `dashboard_button` onclick 1 `url_for('dashboad')`

---

### Section 3: Data Schemas Specification

#### 1. Books Data
- **File Path**: `data/booksdata.txt`
- **Format**: Comma-delimited (`,`) instead of pipe
- **Fields**:
  1. `bookID` (str)
  2. `name` (int)
  3. `authorName` (int)
  4. `isbn_code` (int)
  5. `category` (int)
  6. `cost` (str)
  7. `stock_count` (str)
  8. `desc` (list)
- **Description**: Stores details of every book present.
- **Example Rows**:
  ```
  1,The Great Gatsby,F. Scott Fitzgerald,9780743273565,Fiction,12.99,50,A classic
  2,Sapiens,Yuval Noah Harari,9780062316097,Non-Fiction,16.99,30,Brief history
  3,1984,George Orwell,9780451524935,Fiction,14.99,45,Dystopian fiction
  ```

#### 2. Categories Data
- **File Path**: `data/category.txt`
- **Format**: Comma-delimited (`,`) instead of pipe
- **Fields**:
  1. `catID` (str)
  2. `catName` (int)
  3. `catDesc` (list)
- **Description**: Metadata for book categories.
- **Example Rows**:
  ```
  1,Fiction,Fictional novels
  2,Non-Fiction,Educational books
  3,Science,Science topics
  ```

#### 3. Cart Data
- **File Path**: `data/carts.txt`
- **Format**: Comma-delimited (`,`) instead of pipe
- **Fields**:
  1. `cartID` (str)
  2. `bookID` (str)
  3. `qty` (str)
  4. `added_date` (int
 format MM-DD-YYYY)
- **Description**: Items currently in the shopping cart.
- **Example Rows**:
  ```
  1,1,2,01-15-2025
  2,3,1,01-16-2025
  ```

#### 4. Orders Data
- **File Path**: `data/order.txt`
- **Format**: Comma-delimited (`,`) instead of pipe
- **Fields**:
  1. `orderID` (str)
  2. `custName` (int)
  3. `orderDate` (int
 format MM-DD-YYYY)
  4. `amountTotal` (str)
  5. `status` (int) (e.g.
 1
 2
 3)
  6. `shippingAddr` (int)
- **Description**: Overall orders information.
- **Example Rows**:
  ```
  1,John Doe,01-10-2025,38.97,3,123 Main St
 New York
 NY 10001
  2,Jane Smith,01-14-2025,16.99,2,456 Oak Ave
 Los Angeles
 CA 90001
  ```

#### 5. Order Items Data
- **File Path**: `data/orderitems.txt`
- **Format**: Comma-delimited (`,`) instead of pipe
- **Fields**:
  1. `orderItemID` (str)
  2. `orderID` (str)
  3. `bookID` (str)
  4. `qty` (str)
  5. `cost` (str)
- **Description**: Detailed items per order.
- **Example Rows**:
  ```
  1,1,1,2,12.99
  2,1,3,1,14.99
  3,2,2,1,16.99
  ```

#### 6. Reviews Data
- **File Path**: `data/review.txt`
- **Format**: Comma-delimited (`,`) instead of pipe
- **Fields**:
  1. `reviewID` (str)
  2. `bookID` (str)
  3. `custName` (int)
  4. `rate` (str) (1 to 5)
  5. `review` (list)
  6. `reviewDate` (int
 format MM-DD-YYYY)
- **Description**: Customer reviews for books.
- **Example Rows**:
  ```
  1,1,Alice Johnson,5,Amazing book! A true classic.,01-12-2025
  2,2,Bob Williams,4,Very informative and well-written.,01-13-2025
  3,3,Charlie Brown,5,Thought-provoking and relevant today.,01-15-2025
  ```

#### 7. Bestsellers Data
- **File Path**: `data/bestseller.txt`
- **Format**: Comma-delimited (`,`) instead of pipe
- **Fields**:
  1. `bookID` (str)
  2. `sales` (str)
  3. `period` (int) (e.g.
 1
 2
 3)
- **Description**: Sales count per book different time frames.
- **Example Rows**:
  ```
  2,150,2
  1,120,2
  3,95,2
  ```

---

*End of Design Specification Document*
