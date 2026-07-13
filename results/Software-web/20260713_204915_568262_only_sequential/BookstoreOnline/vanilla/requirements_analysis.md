# Requirements Analysis for 'BookstoreOnline' Web Application

## 1. Pages and Page Titles

1. **Dashboard Page**
   - Page Title: Bookstore Dashboard
2. **Book Catalog Page**
   - Page Title: Book Catalog
3. **Book Details Page**
   - Page Title: Book Details
4. **Shopping Cart Page**
   - Page Title: Shopping Cart
5. **Checkout Page**
   - Page Title: Checkout
6. **Order History Page**
   - Page Title: Order History
7. **Reviews Page**
   - Page Title: Customer Reviews
8. **Write Review Page**
   - Page Title: Write a Review
9. **Bestsellers Page**
   - Page Title: Bestsellers

## 2. Element IDs

### Dashboard Page
- dashboard-page
- featured-books
- browse-catalog-button
- view-cart-button
- bestsellers-button

### Book Catalog Page
- catalog-page
- search-input
- category-filter
- books-grid
- view-book-button-{book_id}  (dynamic per book)

### Book Details Page
- book-details-page
- book-title
- book-author
- book-price
- add-to-cart-button
- book-reviews

### Shopping Cart Page
- cart-page
- cart-items-table
- update-quantity-{item_id}  (dynamic per cart item)
- remove-item-button-{item_id}  (dynamic per cart item)
- proceed-checkout-button
- total-amount

### Checkout Page
- checkout-page
- customer-name
- shipping-address
- payment-method
- place-order-button

### Order History Page
- orders-page
- orders-table
- view-order-button-{order_id}  (dynamic per order)
- order-status-filter
- back-to-dashboard

### Reviews Page
- reviews-page
- reviews-list
- write-review-button
- filter-by-rating
- back-to-dashboard

### Write Review Page
- write-review-page
- select-book
- rating-select
- review-text
- submit-review-button

### Bestsellers Page
- bestsellers-page
- bestsellers-list
- time-period-filter
- view-book-button-{book_id}  (dynamic per bestseller book)
- back-to-dashboard

## 3. Navigation Mapping

### Dashboard Page
- browse-catalog-button -> Book Catalog Page
- view-cart-button -> Shopping Cart Page
- bestsellers-button -> Bestsellers Page

### Book Catalog Page
- view-book-button-{book_id} -> Book Details Page

### Book Details Page
- add-to-cart-button (adds book to cart, stays or navigates to cart or catalog depending on UI design - not explicitly specified)

### Shopping Cart Page
- remove-item-button-{item_id} (removes item from cart)
- update-quantity-{item_id} (updates quantity of item in cart)
- proceed-checkout-button -> Checkout Page

### Checkout Page
- place-order-button (confirms order and presumably navigates to Order History or Dashboard - not explicitly specified)

### Order History Page
- view-order-button-{order_id} -> Order Details View (not explicitly a page in list, assumed view or modal)
- back-to-dashboard -> Dashboard Page

### Reviews Page
- write-review-button -> Write Review Page
- back-to-dashboard -> Dashboard Page

### Write Review Page
- submit-review-button (submits review, no explicit navigation specified)

### Bestsellers Page
- view-book-button-{book_id} -> Book Details Page
- back-to-dashboard -> Dashboard Page

## 4. Data Artifacts

All data files are stored in a local directory named `data` with the following text files and formats:

1. **Books Data**
   - Filename: books.txt
   - Format: book_id|title|author|isbn|category|price|stock|description

2. **Categories Data**
   - Filename: categories.txt
   - Format: category_id|category_name|description

3. **Cart Data**
   - Filename: cart.txt
   - Format: cart_id|book_id|quantity|added_date

4. **Orders Data**
   - Filename: orders.txt
   - Format: order_id|customer_name|order_date|total_amount|status|shipping_address

5. **Order Items Data**
   - Filename: order_items.txt
   - Format: order_item_id|order_id|book_id|quantity|price

6. **Reviews Data**
   - Filename: reviews.txt
   - Format: review_id|book_id|customer_name|rating|review_text|review_date

7. **Bestsellers Data**
   - Filename: bestsellers.txt
   - Format: book_id|sales_count|period

## End of Requirements Analysis
