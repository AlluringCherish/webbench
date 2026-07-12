# FoodDelivery Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name         | HTTP Method | Template File        | Context Variables                                                                                                              | Dynamic Route Params                   |
|-------------------------------|-----------------------|-------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|
| /                             | root_redirect          | GET         | N/A (redirect)        | None                                                                                                                          | None                                 |
| /dashboard                    | dashboard             | GET         | dashboard.html        | featured_restaurants (list of dict), each with: id (int), name (str), cuisine (str), rating (float), delivery_time (int)        | None                                 |
| /restaurants                  | browse_restaurants    | GET         | restaurants.html      | restaurants (list of dict), each with: restaurant_id (int), name (str), cuisine (str), rating (float), delivery_time (int)     | None                                 |
| /menu/&lt;int:restaurant_id&gt;  | restaurant_menu       | GET         | menu.html             | restaurant (dict): restaurant_id (int), name (str), address (str), phone (str), rating (float), delivery_time (int)
  menu_items (list of dict), each with: item_id (int), item_name (str), category (str), description (str), price (float), availability (int) | restaurant_id (int)                  |
| /menu/item/&lt;int:item_id&gt;      | item_details          | GET         | item_details.html     | item (dict): item_id (int), item_name (str), category (str), description (str), price (float), availability (int)               | item_id (int)                         |
| /cart                        | shopping_cart         | GET         | cart.html             | cart_items (list of dict), each with: item_id (int), item_name (str), quantity (int), price (float), subtotal (float)
 total_amount (float)                                                                                                           | None                                 |
| /cart/update                 | update_cart           | POST        | N/A (redirect or JSON) | POST form data: item_id (int), quantity (int)                                                                                  | None                                 |
| /cart/remove/&lt;int:item_id&gt;      | remove_cart_item      | POST        | N/A (redirect)         | None                                                                                                                          | item_id (int)                        |
| /checkout                   | checkout              | GET, POST   | checkout.html         | GET: None
 POST: form data: customer_name (str), delivery_address (str), phone_number (str), payment_method (str)
 On GET: could pass cart_items (list) and total_amount (float)                                                                | None                                 |
| /orders/active               | active_orders         | GET         | active_orders.html    | active_orders (list of dict), each with: order_id (int), restaurant_name (str), status (str), eta (str or datetime)             | None                                 |
| /orders/track/&lt;int:order_id&gt;     | order_tracking        | GET         | tracking.html         | order (dict): order_id (int), customer_name (str), restaurant_name (str), status (str), total_amount (float), delivery_address (str), phone_number (str)
 delivery_info (dict): driver_name (str), driver_phone (str), vehicle_info (str), status (str), estimated_time (str/datetime)
 order_items (list of dict): each with item_name (str), quantity (int), price (float)                                           | order_id (int)                      |
| /reviews                    | reviews               | GET         | reviews.html          | reviews (list of dict), each with: review_id (int), restaurant_name (str), customer_name (str), rating (int), review_text (str), review_date (str)  | None                               |
| /reviews/write              | write_review          | GET, POST   | write_review.html (if implemented) | GET: None
 POST form data: restaurant_id (int), customer_name (str), rating (int), review_text (str)                                              | None                                 |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- File Path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Layout Overview: Main landing dashboard page with sections for featured restaurants, popular cuisines, and navigation buttons.
- Element IDs and Types:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Navigation Mappings:
  - browse-restaurants-button 7 url_for('browse_restaurants')
  - view-cart-button 7 url_for('shopping_cart')
  - active-orders-button 7 url_for('active_orders')

### 2. Restaurant Listing Page
- File Path: templates/restaurants.html
- Page Title: Browse Restaurants
- Layout Overview: List all restaurants with search and cuisine filter controls, and restaurant cards in a grid.
- Element IDs and Types:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (select/dropdown)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button) (dynamic pattern)
- Navigation Mappings:
  - view-restaurant-button-{restaurant_id} 7 url_for('restaurant_menu', restaurant_id=restaurant_id)

### 3. Restaurant Menu Page
- File Path: templates/menu.html
- Page Title: Restaurant Menu
- Layout Overview: Display the selected restaurant information and menu items grid with add to cart and view details buttons.
- Element IDs and Types:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button) (dynamic pattern)
  - view-item-details-{item_id} (button) (dynamic pattern)
- Navigation Mappings:
  - add-to-cart-button-{item_id} 7 JavaScript action to add item to cart
  - view-item-details-{item_id} 7 url_for('item_details', item_id=item_id)

### 4. Item Details Page
- File Path: templates/item_details.html
- Page Title: Item Details
- Layout Overview: Display detailed info about menu item including ingredients and nutritional info, with quantity input and add to cart button.
- Element IDs and Types:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input number)
  - add-to-cart-button (button)
- Navigation Mappings:
  - add-to-cart-button 7 JavaScript action to add item with selected quantity to cart

### 5. Shopping Cart Page
- File Path: templates/cart.html
- Page Title: Shopping Cart
- Layout Overview: Table listing cart items with quantity update and remove buttons, plus total amount and checkout button.
- Element IDs and Types:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input number) (dynamic pattern)
  - remove-item-button-{item_id} (button) (dynamic pattern)
  - proceed-checkout-button (button)
  - total-amount (div)
- Navigation Mappings:
  - proceed-checkout-button 7 url_for('checkout')

### 6. Checkout Page
- File Path: templates/checkout.html
- Page Title: Checkout
- Layout Overview: Form for entering delivery details and payment, with place order button.
- Element IDs and Types:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (select/dropdown)
  - place-order-button (button)
- Navigation Mappings:
  - place-order-button 7 form submission to POST /checkout

### 7. Active Orders Page
- File Path: templates/active_orders.html
- Page Title: Active Orders
- Layout Overview: List active orders with filtering by status and track order buttons.
- Element IDs and Types:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button) (dynamic pattern)
  - status-filter (select/dropdown)
  - back-to-dashboard (button)
- Navigation Mappings:
  - track-order-button-{order_id} 7 url_for('order_tracking', order_id=order_id)
  - back-to-dashboard 7 url_for('dashboard')

### 8. Order Tracking Page
- File Path: templates/tracking.html
- Page Title: Track Order
- Layout Overview: Detailed order tracking with driver info and delivery timeline.
- Element IDs and Types:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Navigation Mappings:
  - back-to-orders 7 url_for('active_orders')

### 9. Reviews Page
- File Path: templates/reviews.html
- Page Title: Order Reviews
- Layout Overview: List of customer reviews with filters and navigation to write review.
- Element IDs and Types:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (select/dropdown)
  - back-to-dashboard (button)
- Navigation Mappings:
  - write-review-button 7 url_for('write_review') (if implemented)
  - back-to-dashboard 7 url_for('dashboard')

---

## Section 3: Data Schemas

### 1. Restaurants Data
- File Name: data/restaurants.txt
- Fields (pipe delimited & order):
  - restaurant_id (int)
  - name (string)
  - cuisine (string)
  - address (string)
  - phone (string)
  - rating (float)
  - delivery_time (int, minutes)
  - min_order (float)
- Description: Stores details about restaurants offering food including contact and average delivery time.
- Example Rows:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

### 2. Menus Data
- File Name: data/menus.txt
- Fields (pipe delimited & order):
  - item_id (int)
  - restaurant_id (int)
  - item_name (string)
  - category (string)
  - description (string)
  - price (float)
  - availability (int, 1=available, 0=not)
- Description: Stores menu items for restaurants including descriptions and pricing.
- Example Rows:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### 3. Cart Data
- File Name: data/cart.txt
- Fields (pipe delimited & order):
  - cart_id (int)
  - item_id (int)
  - restaurant_id (int)
  - quantity (int)
  - added_date (string, YYYY-MM-DD)
- Description: Stores current user's shopping cart items and quantities.
- Example Rows:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

### 4. Orders Data
- File Name: data/orders.txt
- Fields (pipe delimited & order):
  - order_id (int)
  - customer_name (string)
  - restaurant_id (int)
  - order_date (string, YYYY-MM-DD)
  - total_amount (float)
  - status (string: Delivered, On the Way, Preparing, etc.)
  - delivery_address (string)
  - phone_number (string)
- Description: Stores details of placed orders.
- Example Rows:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

### 5. Order Items Data
- File Name: data/order_items.txt
- Fields (pipe delimited & order):
  - order_item_id (int)
  - order_id (int)
  - item_id (int)
  - quantity (int)
  - price (float)
- Description: Stores individual items within an order.
- Example Rows:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

### 6. Deliveries Data
- File Name: data/deliveries.txt
- Fields (pipe delimited & order):
  - delivery_id (int)
  - order_id (int)
  - driver_name (string)
  - driver_phone (string)
  - vehicle_info (string)
  - status (string)
  - estimated_time (string, datetime)
- Description: Stores delivery tracking and driver details for orders.
- Example Rows:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### 7. Reviews Data
- File Name: data/reviews.txt
- Fields (pipe delimited & order):
  - review_id (int)
  - restaurant_id (int)
  - customer_name (string)
  - rating (int, scale 1-5)
  - review_text (string)
  - review_date (string, YYYY-MM-DD)
- Description: Stores customer reviews for restaurants.
- Example Rows:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```

---

This specification enables backend and frontend developers to build the 'FoodDelivery' application independently with clearly defined data structures, Flask routes, and front-end templates.
