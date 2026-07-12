# FoodDelivery Application - Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                                | Function Name       | HTTP Method(s) | Template File             | Context Variables Passed (Name: Data Type)                              |
|------------------------------------------|---------------------|----------------|---------------------------|------------------------------------------------------------------------|
| /                                        | root_redirect       | GET            | None (redirect)            | None                                                                   |
| /dashboard                              | dashboard_page      | GET            | dashboard.html            | featured_restaurants: list[dict], popular_cuisines: list[str]          |
| /restaurants                            | browse_restaurants  | GET            | restaurants.html          | restaurants: list[dict], cuisines: list[str], search_query: str, filter_cuisine: str |
| /restaurant/<int:restaurant_id>        | restaurant_menu     | GET            | menu.html                 | restaurant: dict, menu_items: list[dict]                              |
| /item/<int:item_id>                     | item_details        | GET            | item_details.html         | item: dict                                                           |
| /cart                                  | shopping_cart       | GET, POST      | cart.html                 | cart_items: list[dict], total_amount: float                          |
| /cart/update_quantity/<int:item_id>    | update_cart_quantity| POST           | None (redirect)            | None                                                                   |
| /cart/remove_item/<int:item_id>         | remove_cart_item    | POST           | None (redirect)            | None                                                                   |
| /checkout                             | checkout_page       | GET, POST      | checkout.html             | None (GET) / order_confirmation: dict (POST)                         |
| /orders/active                         | active_orders       | GET            | active_orders.html        | orders: list[dict], status_filter: str                               |
| /order/track/<int:order_id>             | order_tracking      | GET            | order_tracking.html       | order: dict, delivery_info: dict, order_items: list[dict]            |
| /reviews                              | reviews_page        | GET            | reviews.html              | reviews: list[dict], filter_rating: str                              |
| /reviews/write                        | write_review        | GET, POST      | write_review.html         | None (GET), form input data (POST)                                  |

---

## Section 2: HTML Template Specifications

### templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Layout Overview: A main container showing featured restaurants and popular cuisines with navigation buttons to key pages.
- Element IDs and Types:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Navigation Mappings:
  - browse-restaurants-button: calls url_for('browse_restaurants')
  - view-cart-button: calls url_for('shopping_cart')
  - active-orders-button: calls url_for('active_orders')

### templates/restaurants.html
- Page Title: Browse Restaurants
- Layout Overview: Search input and cuisine filter dropdown on top, restaurants displayed as cards in a grid below.
- Element IDs and Types:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (dropdown/select)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button) - for each restaurant card
- Navigation Mappings:
  - view-restaurant-button-{restaurant_id}: calls url_for('restaurant_menu', restaurant_id=restaurant_id)
- Dynamic ID Pattern:
  - view-restaurant-button-{{ restaurant.restaurant_id }}

### templates/menu.html
- Page Title: Restaurant Menu
- Layout Overview: Restaurant info header followed by grid of menu items with buttons to view details or add to cart.
- Element IDs and Types:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button) - for each menu item
  - view-item-details-{item_id} (button) - for each menu item
- Navigation Mappings:
  - view-item-details-{item_id}: calls url_for('item_details', item_id=item_id)
  - add-to-cart-button-{item_id}: form submits to add item to cart
- Dynamic ID Pattern:
  - add-to-cart-button-{{ item.item_id }}
  - view-item-details-{{ item.item_id }}

### templates/item_details.html
- Page Title: Item Details
- Layout Overview: Detailed single item view with description, price, quantity selector, and add-to-cart button.
- Element IDs and Types:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input type=number)
  - add-to-cart-button (button)
- Navigation Mappings:
  - add-to-cart-button: form submits to add item with selected quantity to cart

### templates/cart.html
- Page Title: Shopping Cart
- Layout Overview: Table listing cart items with quantity input and remove buttons. Shows total amount and proceed to checkout button.
- Element IDs and Types:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input type=number) - for each cart item
  - remove-item-button-{item_id} (button) - for each cart item
  - proceed-checkout-button (button)
  - total-amount (div)
- Navigation Mappings:
  - proceed-checkout-button: calls url_for('checkout_page')
  - remove-item-button-{item_id}: form submits to remove_cart_item route
  - quantity input fields submit to update_cart_quantity route
- Dynamic ID Pattern:
  - update-quantity-{{ item.item_id }}
  - remove-item-button-{{ item.item_id }}

### templates/checkout.html
- Page Title: Checkout
- Layout Overview: Form fields for customer name, delivery address, phone, payment method and a place order button.
- Element IDs and Types:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (dropdown/select)
  - place-order-button (button)
- Navigation Mappings:
  - place-order-button: form submits order placement

### templates/active_orders.html
- Page Title: Active Orders
- Layout Overview: Filter dropdown for status, list of orders with tracking buttons, and back to dashboard button.
- Element IDs and Types:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button) - for each order
  - status-filter (dropdown/select)
  - back-to-dashboard (button)
- Navigation Mappings:
  - track-order-button-{order_id}: calls url_for('order_tracking', order_id=order_id)
  - back-to-dashboard: calls url_for('dashboard_page')
- Dynamic ID Pattern:
  - track-order-button-{{ order.order_id }}

### templates/order_tracking.html
- Page Title: Track Order
- Layout Overview: Display full order details, delivery driver info, estimated delivery time, order items list, and back button.
- Element IDs and Types:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Navigation Mappings:
  - back-to-orders: calls url_for('active_orders')

### templates/reviews.html
- Page Title: Order Reviews
- Layout Overview: List all reviews with filter dropdown by rating, button to write new review, and back to dashboard button.
- Element IDs and Types:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (dropdown/select)
  - back-to-dashboard (button)
- Navigation Mappings:
  - write-review-button: calls url_for('write_review')
  - back-to-dashboard: calls url_for('dashboard_page')

### templates/write_review.html
- Page Title: Write Review
- Layout Overview: Form with fields for restaurant selection, customer name, rating, review text and submit button.
- Element IDs and Types:
  - write-review-page (div)
  - restaurant-select (dropdown/select)
  - customer-name-input (input)
  - rating-select (dropdown/select)
  - review-textarea (textarea)
  - submit-review-button (button)
- Navigation Mappings:
  - submit-review-button: submits form POST to write_review route

---

## Section 3: Data Schemas

### restaurants.txt
- Field order:
  ```
  restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
  ```
- Purpose: Stores restaurant profiles including contact, rating, delivery details.
- Example Data:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```
- Field Data Types:
  - restaurant_id: int
  - name: string
  - cuisine: string
  - address: string
  - phone: string
  - rating: float
  - delivery_time: int  (minutes)
  - min_order: float

### menus.txt
- Field order:
  ```
  item_id|restaurant_id|item_name|category|description|price|availability
  ```
- Purpose: Stores menu items linked to restaurants with details and price.
- Example Data:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```
- Field Data Types:
  - item_id: int
  - restaurant_id: int
  - item_name: string
  - category: string
  - description: string
  - price: float
  - availability: int (1=available, 0=unavailable)

### cart.txt
- Field order:
  ```
  cart_id|item_id|restaurant_id|quantity|added_date
  ```
- Purpose: Stores current shopping cart items.
- Example Data:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```
- Field Data Types:
  - cart_id: int
  - item_id: int
  - restaurant_id: int
  - quantity: int
  - added_date: date (YYYY-MM-DD)

### orders.txt
- Field order:
  ```
  order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
  ```
- Purpose: Stores placed orders and status information.
- Example Data:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```
- Field Data Types:
  - order_id: int
  - customer_name: string
  - restaurant_id: int
  - order_date: date (YYYY-MM-DD)
  - total_amount: float
  - status: string
  - delivery_address: string
  - phone_number: string

### order_items.txt
- Field order:
  ```
  order_item_id|order_id|item_id|quantity|price
  ```
- Purpose: Stores individual items and quantities per order.
- Example Data:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```
- Field Data Types:
  - order_item_id: int
  - order_id: int
  - item_id: int
  - quantity: int
  - price: float

### deliveries.txt
- Field order:
  ```
  delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
  ```
- Purpose: Stores delivery details and status per order.
- Example Data:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```
- Field Data Types:
  - delivery_id: int
  - order_id: int
  - driver_name: string
  - driver_phone: string
  - vehicle_info: string
  - status: string
  - estimated_time: string (datetime "YYYY-MM-DD HH:MM")

### reviews.txt
- Field order:
  ```
  review_id|restaurant_id|customer_name|rating|review_text|review_date
  ```
- Purpose: Stores customer reviews for restaurants.
- Example Data:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```
- Field Data Types:
  - review_id: int
  - restaurant_id: int
  - customer_name: string
  - rating: int
  - review_text: string
  - review_date: date (YYYY-MM-DD)

---

This specification fully supports backend route implementations, frontend template builds, and data file handling for the 'FoodDelivery' application.
