# FoodDelivery Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path               | Function Name         | HTTP Method | Template File        | Context Variables                                                                                                              | Dynamic Route Params                   |
|--------------------------|-----------------------|-------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|
| /                        | root_redirect          | GET         | N/A (redirect)        | None                                                                                                                          | None                                 |
| /dashboard               | dashboard             | GET         | dashboard.html        | featured_restaurants (list of dict), each with: id (int), name (str), cuisine (str), rating (float), delivery_time (int)        | None                                 |
| /restaurants             | browse_restaurants    | GET         | restaurants.html      | restaurants (list of dict), each with: restaurant_id (int), name (str), cuisine (str), rating (float), delivery_time (int)     | None                                 |
| /menu/&lt;int:restaurant_id&gt;  | restaurant_menu       | GET         | menu.html             | restaurant (dict): restaurant_id (int), name (str), address (str), phone (str), rating (float), delivery_time (int)
  menu_items (list of dict), each with: item_id (int), item_name (str), category (str), description (str), price (float), availability (int) | restaurant_id (int)                  |
| /menu/item/&lt;int:item_id&gt;      | item_details          | GET         | item_details.html     | item (dict): item_id (int), item_name (str), category (str), description (str), price (float), availability (int)               | item_id (int)                         |
| /cart                   | shopping_cart         | GET         | cart.html             | cart_items (list of dict), each with: item_id (int), item_name (str), quantity (int), price (float), subtotal (float)          | None                                 |
| /cart/update             | update_cart           | POST        | N/A                   | N/A (redirect after POST)                                                                                                     | None                                 |
| /cart/remove/&lt;int:item_id&gt;  | remove_cart_item      | POST        | N/A                   | N/A (redirect after POST)                                                                                                     | item_id (int)                        |
| /checkout               | checkout              | GET         | checkout.html         | None                                                                                                                          | None                                 |
| /checkout/place_order    | place_order           | POST        | N/A                   | N/A (redirect after POST)                                                                                                     | None                                 |
| /orders/active           | active_orders         | GET         | active_orders.html    | active_orders (list of dict), each with: order_id (int), restaurant_name (str), status (str), eta (datetime or str)              | None                                 |
| /orders/track/&lt;int:order_id&gt;  | track_order           | GET         | tracking.html         | order (dict): order_id (int), customer_name (str), restaurant_name (str), order_date (str), total_amount (float), status (str)
  delivery (dict): driver_name (str), driver_phone (str), vehicle_info (str), status (str), estimated_time (str)
  order_items (list of dict): item_name (str), quantity (int), price (float)                                               | order_id (int)                      |
| /reviews                | reviews               | GET         | reviews.html          | reviews (list of dict), each with: review_id (int), restaurant_name (str), customer_name (str), rating (int), review_text (str), review_date (str) | None                                 |
| /reviews/write           | write_review          | GET         | write_review.html     | restaurants (list of dict) with restaurant_id (int), name (str)                                                                | None                                 |
| /reviews/submit          | submit_review         | POST        | N/A                   | N/A (redirect after POST)                                                                                                     | None                                 |

---

## Section 2: HTML Template Specifications

### Template: dashboard.html
- File path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Layout Overview: Main landing page with featured restaurants displayed and buttons for navigation to browsing restaurants, viewing cart, and active orders.
- Element IDs:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Navigation Mappings:
  - browse-restaurants-button &rarr; browse_restaurants (route: /restaurants)
  - view-cart-button &rarr; shopping_cart (route: /cart)
  - active-orders-button &rarr; active_orders (route: /orders/active)

### Template: restaurants.html
- File path: templates/restaurants.html
- Page Title: Browse Restaurants
- Layout Overview: Page with search input, cuisine filter dropdown on top and a grid of restaurant cards below.
- Element IDs:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (select/dropdown)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button, dynamic per restaurant)
- Navigation Mappings:
  - view-restaurant-button-{restaurant_id} &rarr; restaurant_menu (/menu/&lt;restaurant_id&gt;)

### Template: menu.html
- File path: templates/menu.html
- Page Title: Restaurant Menu
- Layout Overview: Displays restaurant info header and grid of their menu items with add to cart and view details buttons.
- Element IDs:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button, dynamic per menu item)
  - view-item-details-{item_id} (button, dynamic per menu item)
- Navigation Mappings:
  - add-to-cart-button-{item_id} triggers add to cart (likely POST)
  - view-item-details-{item_id} &rarr; item_details (/menu/item/&lt;item_id&gt;)

### Template: item_details.html
- File path: templates/item_details.html
- Page Title: Item Details
- Layout Overview: Shows detailed item info with quantity input and add to cart button.
- Element IDs:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input number)
  - add-to-cart-button (button)
- Navigation Mappings:
  - add-to-cart-button triggers adding item with selected quantity to cart

### Template: cart.html
- File path: templates/cart.html
- Page Title: Shopping Cart
- Layout Overview: Displays cart items in a table with quantity update inputs and remove buttons. Shows total amount and proceed to checkout button.
- Element IDs:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input number, dynamic per cart item)
  - remove-item-button-{item_id} (button, dynamic per cart item)
  - proceed-checkout-button (button)
  - total-amount (div)
- Navigation Mappings:
  - proceed-checkout-button &rarr; checkout (/checkout)
  - remove-item-button-{item_id} triggers POST to remove item from cart
  - quantity input updates via form or AJAX

### Template: checkout.html
- File path: templates/checkout.html
- Page Title: Checkout
- Layout Overview: User form to input delivery details and place order.
- Element IDs:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (select/dropdown)
  - place-order-button (button)
- Navigation Mappings:
  - place-order-button triggers POST to place order route (/checkout/place_order)

### Template: active_orders.html
- File path: templates/active_orders.html
- Page Title: Active Orders
- Layout Overview: Lists current active orders with status filter dropdown and buttons to track orders or go back to dashboard.
- Element IDs:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button, dynamic per order)
  - status-filter (select/dropdown)
  - back-to-dashboard (button)
- Navigation Mappings:
  - track-order-button-{order_id} &rarr; track_order (/orders/track/&lt;order_id&gt;)
  - back-to-dashboard &rarr; dashboard (/dashboard)

### Template: tracking.html
- File path: templates/tracking.html
- Page Title: Track Order
- Layout Overview: Shows detailed order status, delivery driver info, and order items list with back button.
- Element IDs:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Navigation Mappings:
  - back-to-orders &rarr; active_orders (/orders/active)

### Template: reviews.html
- File path: templates/reviews.html
- Page Title: Order Reviews
- Layout Overview: Displays list of reviews with filter by rating, write review button, and back to dashboard button.
- Element IDs:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (select/dropdown)
  - back-to-dashboard (button)
- Navigation Mappings:
  - write-review-button &rarr; write_review (/reviews/write)
  - back-to-dashboard &rarr; dashboard (/dashboard)

### Template: write_review.html
- File path: templates/write_review.html
- Page Title: Write Review
- Layout Overview: Form page listing restaurants for review selection, fields to write review and submit.
- Element IDs:
  - write-review-page (div - container assumed)
  - restaurants-list (div or select list) to choose restaurant from restaurants context variable
  - customer-name-input (input) for entering customer name
  - rating-input (select/dropdown) for rating selection
  - review-text-input (textarea) for review text
  - submit-review-button (button)
- Navigation Mappings:
  - submit-review-button triggers POST to submit_review (/reviews/submit)

---

## Section 3: Data Schemas

### 1. Restaurants Data
- File Name: data/restaurants.txt
- Fields (pipe-delimited order):
  - restaurant_id (int)
  - name (string)
  - cuisine (string)
  - address (string)
  - phone (string)
  - rating (float)
  - delivery_time (int, in minutes)
  - min_order (float)
- Description: Stores restaurant details including contact and rating.
- Example Rows:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

### 2. Menus Data
- File Name: data/menus.txt
- Fields (pipe-delimited order):
  - item_id (int)
  - restaurant_id (int)
  - item_name (string)
  - category (string)
  - description (string)
  - price (float)
  - availability (int, 1=available, 0=not)
- Description: Menu items linked to restaurants with details and prices.
- Example Rows:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### 3. Cart Data
- File Name: data/cart.txt
- Fields (pipe-delimited order):
  - cart_id (int)
  - item_id (int)
  - restaurant_id (int)
  - quantity (int)
  - added_date (date string, YYYY-MM-DD)
- Description: Temporary storage of items user has added to cart.
- Example Rows:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

### 4. Orders Data
- File Name: data/orders.txt
- Fields (pipe-delimited order):
  - order_id (int)
  - customer_name (string)
  - restaurant_id (int)
  - order_date (date string, YYYY-MM-DD)
  - total_amount (float)
  - status (string: e.g. Delivered, On the Way, Preparing)
  - delivery_address (string)
  - phone_number (string)
- Description: Stores completed and active order information.
- Example Rows:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

### 5. Order Items Data
- File Name: data/order_items.txt
- Fields (pipe-delimited order):
  - order_item_id (int)
  - order_id (int)
  - item_id (int)
  - quantity (int)
  - price (float)
- Description: Items associated with each order.
- Example Rows:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

### 6. Deliveries Data
- File Name: data/deliveries.txt
- Fields (pipe-delimited order):
  - delivery_id (int)
  - order_id (int)
  - driver_name (string)
  - driver_phone (string)
  - vehicle_info (string)
  - status (string)
  - estimated_time (string, datetime format e.g. YYYY-MM-DD HH:MM)
- Description: Tracks delivery driver assignments and statuses for orders.
- Example Rows:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### 7. Reviews Data
- File Name: data/reviews.txt
- Fields (pipe-delimited order):
  - review_id (int)
  - restaurant_id (int)
  - customer_name (string)
  - rating (int, 1 to 5)
  - review_text (string)
  - review_date (date string, YYYY-MM-DD)
- Description: Stores customer reviews and ratings for restaurants.
- Example Rows:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```

---

End of Design Specification Document.
