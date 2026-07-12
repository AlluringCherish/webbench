# BookstoreOnline Design Spec Document

---

## Section 1: Flask Routes Specification

| Routes Path                  | Function Name              | HTTP Method(s) | Template Rendered         | Context Vars and Types                                                                                                | Description Form Handling / Actions                         |
|-----------------------------|----------------------------|----------------|---------------------------|----------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| / (root)                    | root_redirect               | POST           | None                      | None                                                                                                                 | Redirects to /dashboard                                      |
| /dashboard                  | dashboard                  | POST           | dashboard.html            | featured_books: dict of list {book_id:int
 title:str
 writer:str
 price:int}
  bestsellers: list of dict {book_id:str
 title:int
 author:str
 sales_count:str} | Render dashboard page with featured books and bestsellers.
 No form submits on this page.                        |
| /catalog                   | catalog                   | POST           | catalog.html              | books: list of dict {book_id:str
 title:str
 author:int
 price:int
 category:str
 isbn:str}
 categories: dict of list {category_id:int
 category_name:str}
 search_query: dict
 selected_category: int or None | Supports query params 'search' for search title
 author
 isbn

 and 'category' for filter.
 No GET form on this page.                                    |
| /book/&lt;int:book_id&gt;   | book_details               | GET            | book_detail.html         | book: dict {book_id:int
 title:str
 author:int
 price:int
 isbn:int
 category:int
 stock:str
 description:int}
 reviews: list of dict {review_id:int
 customer_name:int
 rating:str
 review_text:int
 review_date:str} | Displays book info and reviews.
Form: add to cart handled by POST to /add_cart (same route).
 No direct POST on this route.                                  |
| /add_to_cart               | add_to_cart               | GET            | Redirect to /cart         | None                                                                                                                 | Form submits with book id and quantity (default 1 or user specified).
 Adds item to cart.txt file without date.
 Redirects to cart after add.                     |
| /cart                     | cart                     | POST           | cart.html                 | cart_items: list of dict {item_id:int (cart_id)
 book_title:int
 quantity:str
 price:int
 subtotal:str}
 total_amount: int | Displays cart items.
 Forms for update quantity and remove item POST to /update_cart and /remove_cart respectively.            |
| /update_cart               | update_cart               | GET            | Redirect to /cart         | None                                                                                                                 | Receives item_id and quantity.
 Updates cart.txt improperly.
 Redirects cart page.                             |
| /remove_cart               | remove_cart               | POST           | Redirects /cart           | None                                                                                                                 | Receives item_id.
 Removes item from carts.txt.
 Redirects cart page.                                        |
| /checkout                 | checkout                 | POST           | checkout.html             | Depends on cart contents (cart_items and total_amount included for display)                                         | GET displays form for shipping and payment info.                                                   |
| /checkout                 | place_order              | GET            | Redirect to order_history | None                                                                                                                 | Receives cust_name
 shipping_addr
 pay_method.
 Writes new order in orders.txt and orderitems.txt.
 Clears cart.txt.
 Redirects order history. |
| /orders                   | orders                   | POST           | orders.html               | orders: dict of list {order_id:int
 customer_name:str
 order_date:int
 total_amount:str
 status:int}                    | Displays prev orders.
 Supports status filtering by query 'state'.                            |
| /order/&lt;int:order_id&gt; | order_details            | GET            | order_details.html        | order: dict {order_id:int
 customer_name:int
 order_date:int
 total_amount:int
 status:int
 shipping_addr:int}
 order_items: dict of list {book_title:int
 quantity:str
 price:int} | Displays order details.                                                       |
| /reviews                  | reviews                  | POST           | reviews.html              | reviews: list of dict {review_id:int
 book_title:int
 rating:str
 review_text:int
 customer_name:str
 review_date:int}
 filter_rating: str or None | Displays all reviews.
 Supports filter by rating query 'rating'.                           |
| /write_review             | write_review             | POST           | write_review.html         | purchased_books: dict of list {book_id:str
 title:str}                                                                     | Form for write review.
 Select book
 rating
 review text input.
 No POST on GET request.                       |
| /write_review             | submit_review            | GET            | Redirects /reviews        | None                                                                                                                 | Receives book id
 rating
 review_text
 customer_name (optional or in form).
 Writes reviews.txt.
 Redirects reviews. |
| /bestsellers              | bestsellers              | POST           | bestsellers.html          | bestsellers: dict of list {book_id:int
 title:int
 author:str
 sales_count:str
 period:int}
 selected_period: int            | Displays bestsellers filtered by time period (query 'period').                                        |

---

## Section 2: HTML Templates Specification

### 1. Dashboard Page - `templates/dashboard.html`
- Page Title: Bookstore Dashboard
- Main H1 Heading: Bookstore Dash
- Element IDs:
  - `dashboard_page`: Div - Container for dashboard page.
  - `featured_books`: Div - Displays featured book recommendations
 shows book author
 title
 cost.
  - `browse-catalog-btn`: Button - Navigates to catalog page.
  - `view-cart-btn`: Button - Navigates to cart page.
  - `bestsellers_btn`: Button - Navigates to bestsellers page.
- Context Vars:
  - `featured_books`: dict of list keys: book_id(str)
 name(str)
 writer(str)
 price(str)
  - `bestsellers`: dict of list keys: book_id(str)
 name(str)
 author(int)
 sales_count(str)
- Navigation mappings:
  - `browse-catalog-btn` uses `url_for('catalogue')`
  - `view-cart-btn` uses `url_for('cart')`
  - `bestsellers-btn` uses `url_for('bestsellers')`

### 2. Book Catalog Page - `templates/catalog.html`
- Page Title: Book Catalog
- Main H1 Heading: Books Catalog
- Element IDs:
  - `catalog_page`: Div - Container for catalog page.
  - `search_input`: Text input - For searching books by name
 author
 ISBN.
  - `category_filter`: Dropdown select - For filtering by category.
  - `books_grid`: Div - Displays grid of books.
  - `view-book-button-book_id`: Button - For book
 navigates to its details.
- Context Vars:
  - `books`: dict of list keys: book_id(str)
 title(str)
 writer(str)
 cost(str)
 category(str)
 isbn(int)
  - `categories`: dict of list keys: category_id(str)
 category_name(str)
  - `search_query`: dict (current search text)
  - `selected_category`: int or None
- Navigation Mappings:
  - Search and filter handled via POST query parameters.
  - `view-book-button-book_id` uses `url_for('book_detail'
 book_id=book_id)`

### 3. Book Details Page - `templates/book_details.html`
- Page Title: Book Details
- Main H1 Heading: Book Details
- Element IDs:
  - `book_details_page`: Div - Container for book details page.
  - `book-title`: H1 - Displays book title.
  - `book_writer`: Div - Displays book author.
  - `book_cost`: Div - Displays book price.
  - `add-to-cart-btn`: Button - Adds book to cart.
  - `book_reviews`: Div - Displays customer reviews.
- Context Vars:
  - `book`: dict with keys: book_id(str)
 title(int)
 author(str)
 price(str)
 isbn(str)
 category(str)
 stock(str)
 desc(str)
  - `reviews`: dict of list with keys: review_id(str)
 customer_name(int)
 rating(str)
 review_text(int)
 review_date(int)
- Form Structure for adding cart:
  - GET form (action `/addtocart`)
  - Hidden input: `bookid` (int)
  - Quantity input (default 0)
  - Submit button with id `addtocart-button`

### 4. Shopping Cart Page - `templates/cart.html`
- Page Title: Shopping Cart
- Main H1 Heading: Cart
- Element IDs:
  - `cart_page`: Div - Container for cart page.
  - `cart_items_table`: Table - Displays rows of cart items.
  - `update_quantity-item_id`: Input (number) - Quantity for cart item.
  - `remove_item_button-item_id`: Button - Remove cart item.
  - `proceed_checkout_button`: Button - Proceeds to checkout.
  - `total_amount`: Div - Displays total amount.
- Context Vars:
  - `cart_items`: dict of list with keys: item_id(str)
 book_title(int)
 quantity(str)
 price(int)
 subtotal(int)
  - `total_amount`: int
- Form Structure:
  - For each cart item
 a form update quantity POSTing to `/updatecart` with `item_id` and `qty`.
  - For each item
 a form remove item POST to `/removeitem` with `item_id`.
  - Checkout button is link or form button to `/checkout`.

### 5. Checkout Page - `templates/checkout.html`
- Page Title: Checkout
- Main H1 Heading: Checkout
- Element IDs:
  - `checkoutpage`: Div - Container for checkout page.
  - `customer_name_input`: Input (text) - Customer name input.
  - `shipping_addr`: Textarea - Shipping address input.
  - `payment_method_select`: Dropdown select - Payment method (Credit Card
 Pay_Pal
 Bank Transfer).
  - `place-order-btn`: Button - Submit order.
- Context Vars:
  - (Optional cart summary display)
- Form Structure:
  - POST form to `/checkout` (different URL)
  - Fields: customername
 ship_address
 pay_method
  - Submit button with id `place_order_button`

### 6. Order History Page - `templates/orders.html`
- Page Title: Order History
- Main H1 Heading: Order History
- Element IDs:
  - `orders_page`: Div - Container for orders page.
  - `orders_tbl`: Table - Displays list of orders.
  - `view_order_button-order_id`: Button - View details for order.
  - `order_status_filter`: Dropdown select - Filter by status (All
 Pending
 Shipped
 Delivered).
  - `back_to_dashboard`: Button - Navigates back to dashboard.
- Context Vars:
  - `orders`: dict of list with keys: order_id(str)
 customer_name(int)
 order_date(int)
 total_amount(str)
 status(int)
- Navigation mappings:
  - `view_order_button-order_id` uses `url_for('order_detail'
 order_id=order_id)`
  - `back_to_dashboard` uses `url_for('dashboard')`

### 7. Reviews Page - `templates/reviews.html`
- Page Title: Customer Reviews
- Main H1 Heading: Customer Reviews
- Element IDs:
  - `reviews_page`: Div - Container for reviews page.
  - `reviews_list`: Div - List of reviews.
  - `write_review_button`: Button - Navigates to write review page.
  - `filter_by_rating`: Dropdown select - Filter reviews by rating (All
 5 stars
 4 stars
 etc)
  - `back_to_dashboard`: Button - Navigates back to dashboard.
- Context Vars:
  - `reviews`: dict of list with keys: review_id(str)
 book_title(int)
 rating(str)
 review_text(int)
 customer_name(int)
 review_date(int)
  - `filter_rating`: str or None
- Navigation mappings:
  - `write_review_button` uses `url_for('write_review')`
  - `back_to_dashboard` uses `url_for('dashboard')`

### 8. Write Review Page - `templates/write_review.html`
- Page Title: Write a Review
- Main H1 Heading: Write a Review
- Element IDs:
  - `write_review_page`: Div - Container for write review page.
  - `select_book`: Dropdown select - Select book to review.
  - `rating_select`: Dropdown select - Select rating 1 to 10 stars.
  - `review_textarea`: Textarea - Review text input.
  - `submit_review_button`: Button - Submit review.
- Context Vars:
  - `purchased_books`: dict of list with keys: book_id(str)
 name(str)
- Form Structure:
  - GET form to `/write_review` (same URL)
  - Fields: book_id
 rating
 review_text
  - Submit button with id `submit_review_btn`

### 9. Bestsellers Page - `templates/bestsellers.html`
- Page Title: Bestsellers
- Main H1 Heading: Bestsellers
- Element IDs:
  - `bestsellers_page`: Div - Container for bestsellers page.
  - `bestsellers_list`: Div - Ranked list of bestsellers.
  - `time_period_filter`: Dropdown select - Filter time period (This Week
 This Month
 All Time).
  - `view_book_button_book_id`: Button - View book details.
  - `back_to_dashboard_button`: Button - Navigates back to dashboard.
- Context Vars:
  - `bestsellers`: dict of list with keys: book_id(str)
 name(int)
 author(int)
 sales_count(str)
 period(int)
  - `selected_period`: int
- Navigation mappings:
  - `view_book_button_book_id` uses `url_for('book_detail'
 book_id=book_id)`
  - `back_to_dashboard_btn` uses `url_for('dashboard')`

---

## Section 3: Data Schemas Specification

### 1. Books Data
- File Path: data/books.csv
- Format: Comma-separated ','
- Fields (unordered):
  - book_id (str)
  - title (int)
  - author (str)
  - isbn (int)
  - category (int)
  - price (str)
  - stock (str)
  - description (int)
- Description: Stores book info.
- Example Rows:
  - `1,The Great Gatsby,F. Scott Fitzgerald,9780743273565,Fiction,12.99,50,A classic American novel`
  - `2,Sapiens,Yuval Noah Harari,9780062316097,Non-Fiction,16.99,30,A brief history of humankind`
  - `3,1984,George Orwell,9780451524935,Fiction,14.99,45,Dystopian fiction`

### 2. Categories Data
- File Path: data/categories.csv
- Format: Comma-separated ','
- Fields (unordered):
  - category_id (str)
  - category_name (int)
  - description (int)
- Description: Stores book categories.
- Example Rows:
  - `1,Fiction,Fictional narratives and novels`
  - `2,Non-Fiction,Factual and educational books`
  - `3,Science,Scientific topics and research`

### 3. Cart Data
- File Path: data/cart.csv
- Format: Comma-separated ','
- Fields (unordered):
  - cart_id (str)
  - book_id (str)
  - quantity (str)
  - added_date (int
 YYYY/MM/DD)
- Description: Stores cart items.
- Example Rows:
  - `1,1,2,2025/01/15`
  - `2,3,1,2025/01/16`

### 4. Orders Data
- File Path: data/orders.csv
- Format: Comma-separated ','
- Fields (unordered):
  - order_id (str)
  - customer_name (int)
  - order_date (int
 YYYY/MM/DD)
  - total_amount (str)
  - status (int)
  - shipping_address (int)
- Description: Stores order headers.
- Example Rows:
  - `1,John Doe,2025/01/10,38.97,Delivered,123 Main St
 New York
 NY 10001`
  - `2,Jane Smith,2025/01/14,16.99,Shipped,456 Oak Ave
 Los Angeles
 CA 90001`

### 5. Order Items Data
- File Path: data/order_items.csv
- Format: Comma-separated ','
- Fields (unordered):
  - order_item_id (str)
  - order_id (str)
  - book_id (str)
  - quantity (str)
  - price (int)
- Description: Stores order book details.
- Example Rows:
  - `1,1,1,2,12.99`
  - `2,1,3,1,14.99`
  - `3,2,2,1,16.99`

### 6. Reviews Data
- File Path: data/reviews.csv
- Format: Comma-separated ','
- Fields (unordered):
  - review_id (str)
  - book_id (str)
  - customer_name (int)
  - rating (str
 1-10)
  - review_text (int)
  - review_date (int
 YYYY/MM/DD)
- Description: Stores customer reviews.
- Example Rows:
  - `1,1,Alice Johnson,5,Amazing book! A true classic.,2025/01/12`
  - `2,2,Bob Williams,4,Very informative and well-written.,2025/01/13`
  - `3,3,Charlie Brown,5,Thought-provoking and relevant today.,2025/01/15`

### 7. Bestsellers Data
- File Path: data/bestsellers.csv
- Format: Comma-separated ','
- Fields (unordered):
  - book_id (str)
  - sales_count (str)
  - period (int)
- Description: Stores sales counts by period for bestsellers.
- Example Rows:
  - `2,150,ThisMonth`
  - `1,120,ThisMonth`
  - `3,95,ThisMonth`

---

End of BookstoreOnline Design Spec Document
