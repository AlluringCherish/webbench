# FoodDelivery Web Application Design Specification

## Section 1: Page Layouts and Element IDs

### 1. Dashboard Page
- **Page Title**: Food Delivery Dashboard
- **Container ID**: dashboard-page
- **UI Elements**:
  - featured-restaurants (Div): Displays featured restaurant recommendations.
  - browse-restaurants-button (Button): Navigates to Restaurant Listing Page.
  - view-cart-button (Button): Navigates to Shopping Cart Page.
  - active-orders-button (Button): Navigates to Active Orders Page.

### 2. Restaurant Listing Page
- **Page Title**: Browse Restaurants
- **Container ID**: restaurants-page
- **UI Elements**:
  - search-input (Input): Search restaurants by name or cuisine type.
  - cuisine-filter (Dropdown): Filter restaurants by cuisine type.
  - restaurants-grid (Div): Displays restaurant cards with logo, name, rating, and delivery time.
  - view-restaurant-button-{restaurant_id} (Button, dynamic): Navigate to Restaurant Menu Page for specific restaurant.

### 3. Restaurant Menu Page
- **Page Title**: Restaurant Menu
- **Container ID**: menu-page
- **UI Elements**:
  - restaurant-name (H1): Displays restaurant name.
  - restaurant-info (Div): Displays restaurant info (address, phone, rating).
  - menu-items-grid (Div): Displays menu items with photos, name, description, and price.
  - add-to-cart-button-{item_id} (Button, dynamic): Adds specific menu item to cart.
  - view-item-details-{item_id} (Button, dynamic): View details of specific menu item.

### 4. Item Details Page
- **Page Title**: Item Details
- **Container ID**: item-details-page
- **UI Elements**:
  - item-name (H1): Displays item name.
  - item-description (Div): Displays item description and ingredients.
  - item-price (Div): Displays item price.
  - quantity-input (Input number): Select quantity before adding to cart.
  - add-to-cart-button (Button): Add item with selected quantity to cart.

### 5. Shopping Cart Page
- **Page Title**: Shopping Cart
- **Container ID**: cart-page
- **UI Elements**:
  - cart-items-table (Table): Displays cart items with name, quantity, price, subtotal.
  - update-quantity-{item_id} (Input number, dynamic): Update quantity of specific cart item.
  - remove-item-button-{item_id} (Button, dynamic): Remove specific item from cart.
  - proceed-checkout-button (Button): Proceed to Checkout Page.
  - total-amount (Div): Displays total cart amount.

### 6. Checkout Page
- **Page Title**: Checkout
- **Container ID**: checkout-page
- **UI Elements**:
  - customer-name (Input): Input customer name.
  - delivery-address (Textarea): Input delivery address.
  - phone-number (Input): Input phone number.
  - payment-method (Dropdown): Select payment method (Credit Card, Cash, PayPal).
  - place-order-button (Button): Confirm and place order.

### 7. Active Orders Page
- **Page Title**: Active Orders
- **Container ID**: active-orders-page
- **UI Elements**:
  - orders-list (Div): Displays active orders with order ID, restaurant, status, ETA.
  - track-order-button-{order_id} (Button, dynamic): View detailed tracking for specific order.
  - status-filter (Dropdown): Filter orders by status (All, Preparing, On the Way, Delivered).
  - back-to-dashboard (Button): Navigate back to Dashboard Page.

### 8. Order Tracking Page
- **Page Title**: Track Order
- **Container ID**: tracking-page
- **UI Elements**:
  - order-details (Div): Displays complete order details and timeline.
  - delivery-driver-info (Div): Displays delivery driver name, phone, vehicle info.
  - estimated-time (Div): Displays estimated delivery time.
  - order-items-list (Div): List of items in the order.
  - back-to-orders (Button): Navigate back to Active Orders Page.

### 9. Reviews Page
- **Page Title**: Order Reviews
- **Container ID**: reviews-page
- **UI Elements**:
  - reviews-list (Div): Displays all reviews with restaurant name, rating, review text.
  - write-review-button (Button): Navigate to Write Review Page.
  - filter-by-rating (Dropdown): Filter reviews by rating (All, 5 stars, 4 stars, etc.).
  - back-to-dashboard (Button): Navigate back to Dashboard Page.

### 10. Write Review Page
- **Page Title**: Write Review
- **Container ID**: write-review-page
- **UI Elements**:
  - restaurant-select (Dropdown): Dropdown to select restaurant to review.
  - customer-name-input (Input): Input field for customer name.
  - rating-select (Dropdown): Dropdown to select rating (1 to 5 stars).
  - review-textarea (Textarea): Text area to input review text.
  - submit-review-button (Button): Submit the written review.
  - cancel-button (Button): Cancel and navigate back to Reviews Page.


## Section 2: Navigation Flow

- Start Page: Dashboard Page (dashboard-page container)
- From Dashboard Page:
  - browse-restaurants-button -> Restaurant Listing Page (restaurants-page)
  - view-cart-button -> Shopping Cart Page (cart-page)
  - active-orders-button -> Active Orders Page (active-orders-page)

- From Restaurant Listing Page:
  - view-restaurant-button-{restaurant_id} -> Restaurant Menu Page (menu-page) for that restaurant

- From Restaurant Menu Page:
  - add-to-cart-button-{item_id} -> Adds item to cart (no navigation)
  - view-item-details-{item_id} -> Item Details Page (item-details-page)

- From Item Details Page:
  - add-to-cart-button -> Adds item with quantity to cart (no navigation)

- From Shopping Cart Page:
  - proceed-checkout-button -> Checkout Page (checkout-page)

- From Checkout Page:
  - place-order-button -> After order placement, navigate to Active Orders Page (active-orders-page)

- From Active Orders Page:
  - track-order-button-{order_id} -> Order Tracking Page (tracking-page)
  - back-to-dashboard -> Dashboard Page (dashboard-page)

- From Order Tracking Page:
  - back-to-orders -> Active Orders Page (active-orders-page)

- From Reviews Page:
  - write-review-button -> Write Review Page (write-review-page)
  - back-to-dashboard -> Dashboard Page (dashboard-page)

- From Write Review Page:
  - submit-review-button -> After submission, navigate to Reviews Page (reviews-page)
  - cancel-button -> Navigate back to Reviews Page (reviews-page)


## Section 3: Data Storage Formats

### 1. Restaurants Data
- File Name: `restaurants.txt`
- Schema:
  - Fields: restaurant_id (int), name (string), cuisine (string), address (string), phone (string), rating (float), delivery_time (int, minutes), min_order (float)
  - Separator: `|`
- Example Row:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  ```

### 2. Menus Data
- File Name: `menus.txt`
- Schema:
  - Fields: item_id (int), restaurant_id (int), item_name (string), category (string), description (string), price (float), availability (int: 1=available, 0=not)
  - Separator: `|`
- Example Row:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  ```

### 3. Cart Data
- File Name: `cart.txt`
- Schema:
  - Fields: cart_id (int), item_id (int), restaurant_id (int), quantity (int), added_date (date yyyy-mm-dd)
  - Separator: `|`
- Example Row:
  ```
  1|1|1|2|2025-01-15
  ```

### 4. Orders Data
- File Name: `orders.txt`
- Schema:
  - Fields: order_id (int), customer_name (string), restaurant_id (int), order_date (date yyyy-mm-dd), total_amount (float), status (string), delivery_address (string), phone_number (string)
  - Separator: `|`
- Example Row:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  ```

### 5. Order Items Data
- File Name: `order_items.txt`
- Schema:
  - Fields: order_item_id (int), order_id (int), item_id (int), quantity (int), price (float)
  - Separator: `|`
- Example Row:
  ```
  1|1|1|2|12.99
  ```

### 6. Deliveries Data
- File Name: `deliveries.txt`
- Schema:
  - Fields: delivery_id (int), order_id (int), driver_name (string), driver_phone (string), vehicle_info (string), status (string), estimated_time (datetime yyyy-mm-dd HH:MM)
  - Separator: `|`
- Example Row:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  ```

### 7. Reviews Data
- File Name: `reviews.txt`
- Schema:
  - Fields: review_id (int), restaurant_id (int), customer_name (string), rating (int from 1 to 5), review_text (string), review_date (date yyyy-mm-dd)
  - Separator: `|`
- Example Row:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  ```


---

End of FoodDelivery Design Specification
