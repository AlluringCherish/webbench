# FoodDelivery Web Application - Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name           | HTTP Method(s) | Template File           | Context Variables (name : type)                                                                                                                                                  | Dynamic Parameters       |
|--------------------------------|-------------------------|----------------|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| /                              | root_redirect            | GET            | N/A (redirect)           | None                                                                                                                                                                            | None                     |
| /dashboard                     | dashboard_page           | GET            | dashboard.html           | - featured_restaurants : List[dict] (restaurant data for featured display)
- popular_cuisines : List[str]
                                                                      | None                     |
| /restaurants                   | restaurant_listing       | GET            | restaurants.html         | - restaurants : List[dict] (all restaurants data)
- cuisines : List[str] (all available cuisine types for filter)                                                                | None                     |
| /menu/&lt;int:restaurant_id&gt;         | restaurant_menu           | GET            | restaurant_menu.html      | - restaurant : dict (restaurant details)
- menu_items : List[dict] (menu items of this restaurant)                                                                                | restaurant_id : int       |
| /item/&lt;int:item_id&gt;             | item_details_page         | GET            | item_details.html         | - item : dict (menu item details)
- quantity : int (default quantity, usually 1)                                                                                                  | item_id : int             |
| /cart                         | shopping_cart             | GET, POST      | cart.html                | GET: - cart_items : List[dict] (items in cart)
- total_amount : float
POST: - updated cart quantities or removal info (handled server-side)                                  | None                     |
| /checkout                     | checkout_page             | GET, POST      | checkout.html            | GET: None
POST: - customer_name : str
- delivery_address : str
- phone_number : str
- payment_method : str (Credit Card, Cash, PayPal)                                         | None                     |
| /orders/active                | active_orders             | GET            | active_orders.html       | - active_orders : List[dict] (orders with status preparing, on the way, or delivered)
- status_filter_options : List[str] (All, Preparing, On the Way, Delivered)               | None                     |
| /orders/track/&lt;int:order_id&gt;         | order_tracking_page       | GET            | order_tracking.html       | - order : dict (order details)
- delivery_info : dict (driver name, phone, vehicle info)
- estimated_time : str
- order_items : List[dict] (items in this order)               | order_id : int           |
| /reviews                     | reviews_page              | GET            | reviews.html             | - reviews : List[dict] (all reviews)
- rating_filter_options : List[str] (All, 5 stars, 4 stars, etc.)                                                                             | None                     |
| /reviews/write               | write_review_page         | GET, POST      | (Not specified, assume write_review.html) | GET: None
POST: - review data (restaurant_id, customer_name, rating, review_text, review_date)                                                                                      | None                     |


---

## Section 2: HTML Template Specifications

### 1. Template: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Layout Overview: Main dashboard page featuring highlighted restaurants and cuisines with quick navigation buttons.
- Element IDs:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Navigation Mappings:
  - browse-restaurants-button &rarr; `restaurant_listing` route (/restaurants)
  - view-cart-button &rarr; `shopping_cart` route (/cart)
  - active-orders-button &rarr; `active_orders` route (/orders/active)

### 2. Template: templates/restaurants.html
- Page Title: Browse Restaurants
- Layout Overview: Displays all restaurants in grid format with search and filter controls on top.
- Element IDs:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (dropdown/select)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button, dynamic per restaurant)
- Navigation Mappings:
  - view-restaurant-button-{restaurant_id} &rarr; `restaurant_menu` route (/menu/&lt;restaurant_id&gt;)

### 3. Template: templates/restaurant_menu.html
- Page Title: Restaurant Menu
- Layout Overview: Displays restaurant info on top and grid of menu items below.
- Element IDs:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button, dynamic per item)
  - view-item-details-{item_id} (button, dynamic per item)
- Navigation Mappings:
  - add-to-cart-button-{item_id} &rarr; adds item to cart (action via POST, no navigation)
  - view-item-details-{item_id} &rarr; `item_details_page` route (/item/&lt;item_id&gt;)

### 4. Template: templates/item_details.html
- Page Title: Item Details
- Layout Overview: Detailed item information and quantity selection with add to cart button.
- Element IDs:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input number)
  - add-to-cart-button (button)
- Navigation Mappings:
  - add-to-cart-button &rarr; adds specified quantity of item to cart (POST action)

### 5. Template: templates/cart.html
- Page Title: Shopping Cart
- Layout Overview: Table listing cart items with quantity update inputs and removal buttons, total amount display, and checkout button.
- Element IDs:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input number, dynamic per cart item)
  - remove-item-button-{item_id} (button, dynamic per cart item)
  - proceed-checkout-button (button)
  - total-amount (div)
- Navigation Mappings:
  - proceed-checkout-button &rarr; `checkout_page` route (/checkout)

### 6. Template: templates/checkout.html
- Page Title: Checkout
- Layout Overview: Form for entering customer delivery details and selecting payment method.
- Element IDs:
  - checkout-page (div)
  - customer-name (input text)
  - delivery-address (textarea)
  - phone-number (input text)
  - payment-method (dropdown/select)
  - place-order-button (button)
- Navigation Mappings:
  - place-order-button &rarr; submits order placement form (POST action)

### 7. Template: templates/active_orders.html
- Page Title: Active Orders
- Layout Overview: List display of current active orders with status filter and tracking button for each order.
- Element IDs:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button, dynamic per active order)
  - status-filter (dropdown/select)
  - back-to-dashboard (button)
- Navigation Mappings:
  - track-order-button-{order_id} &rarr; `order_tracking_page` route (/orders/track/&lt;order_id&gt;)
  - back-to-dashboard &rarr; `dashboard_page` route (/dashboard)

### 8. Template: templates/order_tracking.html
- Page Title: Track Order
- Layout Overview: Detailed tracking info including delivery driver info and order items list.
- Element IDs:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Navigation Mappings:
  - back-to-orders &rarr; `active_orders` route (/orders/active)

### 9. Template: templates/reviews.html
- Page Title: Order Reviews
- Layout Overview: Lists all customer reviews with filter and button to write new review.
- Element IDs:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (dropdown/select)
  - back-to-dashboard (button)
- Navigation Mappings:
  - write-review-button &rarr; `write_review_page` route (/reviews/write)
  - back-to-dashboard &rarr; `dashboard_page` route (/dashboard)


---

## Section 3: Data Schemas

All data files are stored in the `data/` directory using pipe-delimited (`|`) text format.

### 1. File: data/restaurants.txt
- Fields (in order):
  - restaurant_id (int)
  - name (string)
  - cuisine (string)
  - address (string)
  - phone (string)
  - rating (float)
  - delivery_time (int, minutes)
  - min_order (float)
- Purpose: Contains information about each restaurant available in the system.
- Example Data:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

### 2. File: data/menus.txt
- Fields (in order):
  - item_id (int)
  - restaurant_id (int)
  - item_name (string)
  - category (string)
  - description (string)
  - price (float)
  - availability (int, 1=available, 0=unavailable)
- Purpose: Contains menu items for all restaurants.
- Example Data:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### 3. File: data/cart.txt
- Fields (in order):
  - cart_id (int)
  - item_id (int)
  - restaurant_id (int)
  - quantity (int)
  - added_date (string: yyyy-MM-dd)
- Purpose: Stores current shopping cart entries (note: user is not authenticated, so cart data is stored globally or per session as applicable).
- Example Data:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

### 4. File: data/orders.txt
- Fields (in order):
  - order_id (int)
  - customer_name (string)
  - restaurant_id (int)
  - order_date (string: yyyy-MM-dd)
  - total_amount (float)
  - status (string: Preparing, On the Way, Delivered)
  - delivery_address (string)
  - phone_number (string)
- Purpose: Stores all placed orders.
- Example Data:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

### 5. File: data/order_items.txt
- Fields (in order):
  - order_item_id (int)
  - order_id (int)
  - item_id (int)
  - quantity (int)
  - price (float)
- Purpose: Stores each item within orders.
- Example Data:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

### 6. File: data/deliveries.txt
- Fields (in order):
  - delivery_id (int)
  - order_id (int)
  - driver_name (string)
  - driver_phone (string)
  - vehicle_info (string)
  - status (string: Delivered, On the Way, etc.)
  - estimated_time (string: yyyy-MM-dd HH:mm)
- Purpose: Stores delivery information and tracking status.
- Example Data:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### 7. File: data/reviews.txt
- Fields (in order):
  - review_id (int)
  - restaurant_id (int)
  - customer_name (string)
  - rating (int, 1 to 5)
  - review_text (string)
  - review_date (string: yyyy-MM-dd)
- Purpose: Stores customer reviews for restaurants.
- Example Data:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```

---

***End of Design Specification***
