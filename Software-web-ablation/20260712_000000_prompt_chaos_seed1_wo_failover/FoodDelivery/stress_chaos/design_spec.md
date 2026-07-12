# FoodDelivery Web Application Design Specification

## Section 1: Flask Routes Specification

| Route Path                 | Function Name          | HTTP Method | Template File           | Context Variables                                    | Dynamic Parameters              |
|----------------------------|------------------------|-------------|-------------------------|-----------------------------------------------------|--------------------------------|
| /                          | root_redirect          | GET         | N/A (redirect)          | None                                                | None                           |
| /dashboard                 | dashboard              | GET         | dashboard.html          | featured_restaurants (list of dicts),                | None                           |
|                            |                        |             |                         | popular_cuisines (list of strings)                   |                                |
|                            |                        |             |                         | (for displaying on dashboard)                        |                                |
| /restaurants               | restaurant_listing     | GET         | restaurants.html        | restaurants (list of dicts),                          | None                           |
|                            |                        |             |                         | cuisines (list of strings)                            |                                |
| /menu/<int:restaurant_id>  | restaurant_menu        | GET         | menu.html               | restaurant (dict),                                   | restaurant_id (int)             |
|                            |                        |             |                         | menu_items (list of dicts)                            |                                |
| /item/<int:item_id>        | item_details           | GET         | item_details.html       | item (dict)                                          | item_id (int)                  |
| /item/<int:item_id>/add    | add_item_to_cart       | POST        | N/A                     | None                                                | item_id (int)                  |
| /cart                     | shopping_cart          | GET         | cart.html               | cart_items (list of dicts),                           | None                           |
|                            |                        |             |                         | total_amount (float)                                  |                                |
| /cart/update               | update_cart            | POST        | N/A                     | None                                                | None                           |
| /cart/remove/<int:item_id> | remove_cart_item       | POST        | N/A                     | None                                                | item_id (int)                  |
| /checkout                  | checkout               | GET         | checkout.html           | None                                                | None                           |
| /checkout/place_order      | place_order            | POST        | N/A                     | None                                                | None                           |
| /orders/active             | active_orders          | GET         | active_orders.html      | active_orders (list of dicts),                        | None                           |
| /orders/track/<int:order_id>| order_tracking        | GET         | tracking.html           | order (dict),                                       | order_id (int)                 |
|                            |                        |             |                         | delivery_info (dict),                                |                                |
| /reviews                   | reviews                | GET         | reviews.html            | reviews (list of dicts),                              | None                           |
| /reviews/write             | write_review           | GET, POST   | write_review.html       | (GET) None, (POST) form data handled                   | None                           |

## Section 2: HTML Template Specifications

### dashboard.html
- File path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Element IDs:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Layout Overview: Main container with featured restaurants and quick navigation buttons.
- Navigation Mappings:
  - browse-restaurants-button: routes.restaurant_listing
  - view-cart-button: routes.shopping_cart
  - active-orders-button: routes.active_orders

### restaurants.html
- File path: templates/restaurants.html
- Page Title: Browse Restaurants
- Element IDs:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (dropdown/select)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button, dynamic)
- Layout Overview: Search and filter section at top, grid of restaurant cards below.
- Navigation Mappings:
  - view-restaurant-button-{restaurant_id}: routes.restaurant_menu

### menu.html
- File path: templates/menu.html
- Page Title: Restaurant Menu
- Element IDs:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button, dynamic)
  - view-item-details-{item_id} (button, dynamic)
- Layout Overview: Restaurant info on top with grid of menu items.
- Navigation Mappings:
  - add-to-cart-button-{item_id}: routes.add_item_to_cart (POST)
  - view-item-details-{item_id}: routes.item_details

### item_details.html
- File path: templates/item_details.html
- Page Title: Item Details
- Element IDs:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input number)
  - add-to-cart-button (button)
- Layout Overview: Detailed single item view with add to cart functionality.
- Navigation Mappings:
  - add-to-cart-button: routes.add_item_to_cart (POST) with selected quantity

### cart.html
- File path: templates/cart.html
- Page Title: Shopping Cart
- Element IDs:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input number, dynamic)
  - remove-item-button-{item_id} (button, dynamic)
  - proceed-checkout-button (button)
  - total-amount (div)
- Layout Overview: Table listing cart contents with quantity updates and remove buttons.
- Navigation Mappings:
  - proceed-checkout-button: routes.checkout

### checkout.html
- File path: templates/checkout.html
- Page Title: Checkout
- Element IDs:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (dropdown/select)
  - place-order-button (button)
- Layout Overview: Form for delivery and payment information.
- Navigation Mappings:
  - place-order-button: routes.place_order (POST)

### active_orders.html
- File path: templates/active_orders.html
- Page Title: Active Orders
- Element IDs:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button, dynamic)
  - status-filter (dropdown/select)
  - back-to-dashboard (button)
- Layout Overview: List of active orders with filter and track buttons.
- Navigation Mappings:
  - track-order-button-{order_id}: routes.order_tracking
  - back-to-dashboard: routes.dashboard

### tracking.html
- File path: templates/tracking.html
- Page Title: Track Order
- Element IDs:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Layout Overview: Detailed tracking info with driver and ETA.
- Navigation Mappings:
  - back-to-orders: routes.active_orders

### reviews.html
- File path: templates/reviews.html
- Page Title: Order Reviews
- Element IDs:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (dropdown/select)
  - back-to-dashboard (button)
- Layout Overview: List customer reviews with filter and write new review button.
- Navigation Mappings:
  - write-review-button: routes.write_review
  - back-to-dashboard: routes.dashboard

### write_review.html
- File path: templates/write_review.html
- Page Title: Write a Review
- Element IDs:
  - write-review-page (div)
  - restaurant-select (dropdown/select)
  - customer-name-input (input)
  - rating-input (dropdown/select)
  - review-textarea (textarea)
  - review-date-input (input, date)
  - submit-review-button (button)
- Layout Overview: Form to submit a new review.
- Navigation Mappings:
  - submit-review-button: routes.write_review (POST)

## Section 3: Data Schemas

### restaurants.txt
- Fields (pipe-delimited):
  restaurant_id (int) | name (string) | cuisine (string) | address (string) | phone (string) | rating (float) | delivery_time (int, minutes) | min_order (float)
- Purpose: Stores restaurant details, ratings, and minimum order amounts.
- Example Data:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

### menus.txt
- Fields (pipe-delimited):
  item_id (int) | restaurant_id (int) | item_name (string) | category (string) | description (string) | price (float) | availability (int, 0 or 1)
- Purpose: Stores menu items with descriptions and prices.
- Example Data:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### cart.txt
- Fields (pipe-delimited):
  cart_id (int) | item_id (int) | restaurant_id (int) | quantity (int) | added_date (string, YYYY-MM-DD)
- Purpose: Stores items added to the shopping cart.
- Example Data:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

### orders.txt
- Fields (pipe-delimited):
  order_id (int) | customer_name (string) | restaurant_id (int) | order_date (string, YYYY-MM-DD) | total_amount (float) | status (string) | delivery_address (string) | phone_number (string)
- Purpose: Stores placed orders with status and delivery info.
- Example Data:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

### order_items.txt
- Fields (pipe-delimited):
  order_item_id (int) | order_id (int) | item_id (int) | quantity (int) | price (float)
- Purpose: Stores each item detail within an order.
- Example Data:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

### deliveries.txt
- Fields (pipe-delimited):
  delivery_id (int) | order_id (int) | driver_name (string) | driver_phone (string) | vehicle_info (string) | status (string) | estimated_time (string, YYYY-MM-DD HH:MM)
- Purpose: Stores delivery tracking and driver info.
- Example Data:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### reviews.txt
- Fields (pipe-delimited):
  review_id (int) | restaurant_id (int) | customer_name (string) | rating (int) | review_text (string) | review_date (string, YYYY-MM-DD)
- Purpose: Stores customer reviews for restaurants.
- Example Data:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```
