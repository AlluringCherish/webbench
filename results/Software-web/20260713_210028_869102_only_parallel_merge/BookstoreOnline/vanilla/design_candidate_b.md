# Design Candidate B for BookstoreOnline Web Application

---

## 1. Complete Route List with HTTP Methods and Function Names

| URL Route              | HTTP Method(s) | Function Name           | Description                 |
|------------------------|----------------|-------------------------|-----------------------------|
| /dashboard             | GET            | dashboard_page           | Show dashboard page         |
| /catalog               | GET            | book_catalog_page        | Show book catalog with filters/search |
| /book/<int:book_id>    | GET            | book_details_page        | Show details for specific book |
| /cart                  | GET, POST      | shopping_cart_page       | Display and update shopping cart |
| /cart/remove/<int:item_id> | POST        | remove_cart_item         | Remove item from cart        |
| /checkout              | GET, POST      | checkout_page            | Show and process checkout   |
| /orders                | GET            | order_history_page       | Show all past orders with filters |
| /order/<int:order_id>  | GET            | order_details_page       | Show details of a specific order |
| /reviews               | GET            | reviews_page             | Display reviews list, filter option |
| /reviews/write         | GET, POST      | write_review_page        | Form to write and submit a review |
| /bestsellers           | GET            | bestsellers_page         | Show list of top selling books |

---

## 2. UI Element Specification and Layout

### 1. Dashboard Page
- **Route**: `/dashboard` (GET)
- **Page Title**: "Bookstore Dashboard"
- **Container**:
  - `div` with ID `dashboard_main`
- **Elements:**
  - `div` ID `featured_books`:
    - Displays featured books horizontally with image, title, and author.
    - Clicking a book title or image navigates to `/book/<book_id>` page.
  - Navigation Buttons:
    - Button ID `btn_catalog` labeled "Browse Catalog", navigates to `/catalog`.
    - Button ID `btn_cart` labeled "View Cart", navigates to `/cart`.
    - Button ID `btn_bestsellers` labeled "Bestsellers", navigates to `/bestsellers`.

### 2. Book Catalog Page
- **Route**: `/catalog` (GET)
- **Page Title**: "Book Catalog"
- **Container**: `div` with ID `catalog_main`
- **Elements:**
  - Search Input: `input` ID `input_search` (text), placeholder "Search by title, author, or ISBN"
  - Category Filter: `select` ID `filter_category` -- options loaded dynamically (Fiction, Non-Fiction, etc.)
  - Books Grid: `div` ID `grid_books` showing cards for each book.
    - Each card shows cover image, title, author, price.
    - Each card has a button with ID `btn_view_{book_id}` labeled "View Details" that links to `/book/<book_id>`.

### 3. Book Details Page
- **Route**: `/book/<int:book_id>` (GET)
- **Page Title**: "Book Details"
- **Container**: `div` with ID `book_details_main`
- **Elements:**
  - Book Title: `h1` ID `book_title`
  - Author: `div` ID `book_author`
  - Price: `div` ID `book_price`
  - Add To Cart: Button ID `btn_add_to_cart` with label "Add to Cart"
  - Reviews Section: `div` ID `section_reviews` displaying customer reviews with rating and text.

### 4. Shopping Cart Page
- **Route**: `/cart` (GET, POST)
- **Page Title**: "Shopping Cart"
- **Container**: `div` ID `cart_main`
- **Elements:**
  - Cart Items Table: `table` ID `table_cart_items`
    - Each row corresponds to a cart item.
    - Quantity input: `input` number field ID `input_qty_{item_id}` for updating quantity.
    - Remove button: Button ID `btn_remove_{item_id}` to remove item.
  - Total Amount: `div` ID `div_total_amount` showing sum of item subtotals.
  - Proceed Checkout: Button ID `btn_proceed_checkout` navigates to `/checkout`.

### 5. Checkout Page
- **Route**: `/checkout` (GET, POST)
- **Page Title**: "Checkout"
- **Container**: `div` ID `checkout_main`
- **Elements:**
  - Customer Name Input: `input` ID `input_customer_name`
  - Shipping Address: `textarea` ID `textarea_shipping_address`
  - Payment Method: `select` ID `select_payment_method` with options: "Credit Card", "PayPal", "Bank Transfer"
  - Place Order Button: Button ID `btn_place_order` labeled "Place Order"

### 6. Order History Page
- **Route**: `/orders` (GET)
- **Page Title**: "Order History"
- **Container**: `div` ID `orders_main`
- **Elements:**
  - Orders Table: `table` ID `table_orders`
    - Columns: Order ID, Date, Total Amount, Status
    - Each row has button ID `btn_view_order_{order_id}` labeled "View"
  - Status Filter: `select` ID `filter_order_status` with options: "All", "Pending", "Shipped", "Delivered"
  - Back to Dashboard Button: Button ID `btn_back_dashboard` navigates to `/dashboard`

### 7. Reviews Page
- **Route**: `/reviews` (GET)
- **Page Title**: "Customer Reviews"
- **Container**: `div` ID `reviews_main`
- **Elements:**
  - Reviews List: `div` ID `list_reviews`
    - Each review includes book title, rating stars, and review text.
  - Write Review Button: Button ID `btn_write_review` navigates to `/reviews/write`
  - Filter by Rating: `select` ID `filter_rating` with options: "All", "5 stars", "4 stars", etc.
  - Back to Dashboard Button: Button ID `btn_back_dashboard` navigates to `/dashboard`

### 8. Write Review Page
- **Route**: `/reviews/write` (GET, POST)
- **Page Title**: "Write a Review"
- **Container**: `div` ID `write_review_main`
- **Elements:**
  - Select Book Dropdown: `select` ID `select_book_review` to choose a book to review
  - Rating Dropdown: `select` ID `select_rating` options 1 to 5 stars
  - Review Textarea: `textarea` ID `textarea_review_text`
  - Submit Review Button: Button ID `btn_submit_review`

### 9. Bestsellers Page
- **Route**: `/bestsellers` (GET)
- **Page Title**: "Bestsellers"
- **Container**: `div` ID `bestsellers_main`
- **Elements:**
  - Bestsellers List: `div` ID `list_bestsellers`
    - Each entry shows rank, title, author, sales count
    - View Book Button: Button ID `btn_view_{book_id}` to navigate to book details
  - Time Period Filter: `select` ID `filter_time_period` with options "This Week", "This Month", "All Time"
  - Back to Dashboard Button: Button ID `btn_back_dashboard` navigates to `/dashboard`

---

## 3. Page Titles and Navigation Summary

| Page Name           | Route               | Page Title           | Navigation Buttons and Destinations                             |
|---------------------|---------------------|----------------------|----------------------------------------------------------------|
| Dashboard           | /dashboard          | Bookstore Dashboard  | Browse Catalog (`/catalog`), View Cart (`/cart`), Bestsellers (`/bestsellers`)
| Book Catalog         | /catalog            | Book Catalog         | View Book Details (`/book/<book_id>`)                         |
| Book Details         | /book/<book_id>     | Book Details         | Add to Cart, Back to Catalog                                |
| Shopping Cart        | /cart               | Shopping Cart        | Update Quantity, Remove Items, Proceed to Checkout (`/checkout`)
| Checkout             | /checkout           | Checkout             | Place Order, Back to Cart                                     |
| Order History        | /orders             | Order History        | View Order Details (`/order/<order_id>`), Filter Status, Back to Dashboard
| Order Details        | /order/<order_id>   | Order Details        | Back to Order History                                        |
| Reviews              | /reviews            | Customer Reviews     | Write Review (`/reviews/write`), Filter by Rating, Back to Dashboard
| Write Review         | /reviews/write      | Write a Review       | Submit Review, Back to Reviews                               |
| Bestsellers          | /bestsellers        | Bestsellers          | Filter Time Period, View Book Details, Back to Dashboard      |

---

This design candidate B provides a clear, unique but comprehensive structure for the BookstoreOnline application fulfilling all requirements independently. All UI elements have defined IDs for implementation. The routes and function names follow Flask conventions with clear relationships between pages.

---