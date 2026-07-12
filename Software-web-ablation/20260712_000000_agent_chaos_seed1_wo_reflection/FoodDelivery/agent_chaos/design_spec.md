# FoodDelivery Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                        | Function Name             | HTTP Method | Template File Name         | Context Variables                                                                    | Route Parameters                    |
|----------------------------------|---------------------------|-------------|----------------------------|--------------------------------------------------------------------------------------|-----------------------------------|
| /                                | root_redirect             | GET         | N/A (redirect)              | None                                                                                 | None                              |
| /dashboard                       | dashboard_page            | GET         | dashboard.html              | featured_restaurants (List[Dict]), popular_cuisines (List[str])                     | None                              |
| /restaurants                    | restaurants_page          | GET         | restaurants.html            | restaurants (List[Dict]), cuisine_filter_options (List[str]), selected_cuisine (str) | None                              |
| /menu/<int:restaurant_id>       | restaurant_menu_page      | GET         | menu.html                   | restaurant (Dict), menu_items (List[Dict])                                          | restaurant_id: int                |
| /item/<int:item_id>             | item_details_page         | GET         | item_details.html           | item (Dict)                                                                         | item_id: int                     |
| /cart                          | shopping_cart_page        | GET         | cart.html                   | cart_items (List[Dict]), total_amount (float)                                      | None                              |
| /cart/update                   | update_cart               | POST        | N/A (redirect or JSON)      | None (handles cart updating form data)                                             | None                              |
| /checkout                     | checkout_page             | GET, POST   | checkout.html               | If GET: None; if POST: order_confirmation (Dict)                                   | None                              |
| /orders/active                 | active_orders_page        | GET         | active_orders.html          | active_orders (List[Dict]), status_filter_options (List[str]), selected_status (str) | None                              |
| /orders/track/<int:order_id>   | order_tracking_page       | GET         | track_order.html            | order_details (Dict), delivery_driver (Dict), estimated_time (str), order_items_list (List[Dict]) | order_id: int                    |
| /reviews                      | reviews_page              | GET         | reviews.html                | reviews (List[Dict]), rating_filter_options (List[str]), selected_rating (str)       | None                              |
| /reviews/write                 | write_review_page         | GET, POST   | write_review.html           | If GET: restaurant_options (List[Dict]); if POST: review_submission_status (str)      | None                              |


**Notes:**
- The root route `/` redirects internally to `/dashboard`.
- POST methods on `/cart/update` and `/checkout` handle data submission; their template usage depends on flow.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- File path: templates/dashboard.html
- Page Title and H1: Food Delivery Dashboard
- Element IDs and Types:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Layout: Main container with featured restaurant recommendations and buttons for navigation.
- Navigation mappings:
  - browse-restaurants-button links to `url_for('restaurants_page')`
  - view-cart-button links to `url_for('shopping_cart_page')`
  - active-orders-button links to `url_for('active_orders_page')`

### 2. restaurants.html
- File path: templates/restaurants.html
- Page Title and H1: Browse Restaurants
- Element IDs and Types:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (select dropdown)
  - restaurants-grid (div)
  - view-restaurant-button-{{ restaurant.restaurant_id }} (button)
- Layout: Search and filter at top, grid of restaurant cards below.
- Navigation mappings:
  - view-restaurant-button-{{ restaurant.restaurant_id }} links to `url_for('restaurant_menu_page', restaurant_id=restaurant.restaurant_id)`

### 3. menu.html
- File path: templates/menu.html
- Page Title and H1: Restaurant Menu
- Element IDs and Types:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{{ item.item_id }} (button)
  - view-item-details-{{ item.item_id }} (button)
- Layout: Restaurant details at top, grid of menu items with photo, description, price.
- Navigation mappings:
  - view-item-details-{{ item.item_id }} links to `url_for('item_details_page', item_id=item.item_id)`

### 4. item_details.html
- File path: templates/item_details.html
- Page Title and H1: Item Details
- Element IDs and Types:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input type=number)
  - add-to-cart-button (button)
- Layout: Item info with description and price, quantity input and add to cart button.

### 5. cart.html
- File path: templates/cart.html
- Page Title and H1: Shopping Cart
- Element IDs and Types:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{{ item.item_id }} (input type=number)
  - remove-item-button-{{ item.item_id }} (button)
  - proceed-checkout-button (button)
  - total-amount (div)
- Layout: Table listing cart items with quantity controls and remove buttons, total amount summary, and checkout button.

### 6. checkout.html
- File path: templates/checkout.html
- Page Title and H1: Checkout
- Element IDs and Types:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (select dropdown)
  - place-order-button (button)
- Layout: Form for user info and payment selection, place order button.

### 7. active_orders.html
- File path: templates/active_orders.html
- Page Title and H1: Active Orders
- Element IDs and Types:
  - active-orders-page (div)
  - orders-list (div)
  - status-filter (select dropdown)
  - track-order-button-{{ order.order_id }} (button)
  - back-to-dashboard (button)
- Layout: Filter for order status with list of active orders and tracking button per order.
- Navigation mappings:
  - track-order-button-{{ order.order_id }} links to `url_for('order_tracking_page', order_id=order.order_id)`
  - back-to-dashboard links to `url_for('dashboard_page')`

### 8. track_order.html
- File path: templates/track_order.html
- Page Title and H1: Track Order
- Element IDs and Types:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Layout: Detailed order status, driver info, estimated delivery time, items list.
- Navigation mappings:
  - back-to-orders links to `url_for('active_orders_page')`

### 9. reviews.html
- File path: templates/reviews.html
- Page Title and H1: Order Reviews
- Element IDs and Types:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (select dropdown)
  - back-to-dashboard (button)
- Layout: Reviews listing with filter, button to write a new review.
- Navigation mappings:
  - write-review-button links to `url_for('write_review_page')`
  - back-to-dashboard links to `url_for('dashboard_page')`

### 10. write_review.html
- File path: templates/write_review.html
- Page Title and H1: Write Review
- Element IDs and Types:
  - write-review-page (div)
  - restaurant-options (select dropdown)
  - customer-name (input)
  - rating (select dropdown)
  - review-text (textarea)
  - submit-review-button (button)
- Layout: Form to submit new review for selected restaurant.

---

## Section 3: Data Schemas

### 1. restaurants.txt
- File name: restaurants.txt
- Fields: restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
- Purpose: Stores restaurant information and metadata for display and filtering.
- Example rows:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```
- Data types:
  - restaurant_id: int
  - name: string
  - cuisine: string
  - address: string
  - phone: string
  - rating: float
  - delivery_time: int (minutes)
  - min_order: float

### 2. menus.txt
- File name: menus.txt
- Fields: item_id|restaurant_id|item_name|category|description|price|availability
- Purpose: Stores menu items per restaurant with details.
- Example rows:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```
- Data types:
  - item_id: int
  - restaurant_id: int
  - item_name: string
  - category: string
  - description: string
  - price: float
  - availability: int (1=available, 0=unavailable)

### 3. cart.txt
- File name: cart.txt
- Fields: cart_id|item_id|restaurant_id|quantity|added_date
- Purpose: Stores items added to the shopping cart.
- Example rows:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```
- Data types:
  - cart_id: int
  - item_id: int
  - restaurant_id: int
  - quantity: int
  - added_date: date (YYYY-MM-DD)

### 4. orders.txt
- File name: orders.txt
- Fields: order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
- Purpose: Stores order records and their current status.
- Example rows:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```
- Data types:
  - order_id: int
  - customer_name: string
  - restaurant_id: int
  - order_date: date (YYYY-MM-DD)
  - total_amount: float
  - status: string
  - delivery_address: string
  - phone_number: string

### 5. order_items.txt
- File name: order_items.txt
- Fields: order_item_id|order_id|item_id|quantity|price
- Purpose: Stores individual items within orders.
- Example rows:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```
- Data types:
  - order_item_id: int
  - order_id: int
  - item_id: int
  - quantity: int
  - price: float

### 6. deliveries.txt
- File name: deliveries.txt
- Fields: delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
- Purpose: Stores delivery and driver information and status.
- Example rows:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```
- Data types:
  - delivery_id: int
  - order_id: int
  - driver_name: string
  - driver_phone: string
  - vehicle_info: string
  - status: string
  - estimated_time: string (datetime YYYY-MM-DD HH:MM)

### 7. reviews.txt
- File name: reviews.txt
- Fields: review_id|restaurant_id|customer_name|rating|review_text|review_date
- Purpose: Stores customer reviews per restaurant.
- Example rows:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```
- Data types:
  - review_id: int
  - restaurant_id: int
  - customer_name: string
  - rating: int
  - review_text: string
  - review_date: date (YYYY-MM-DD)

---

This concludes the comprehensive design specification for the FoodDelivery web application.