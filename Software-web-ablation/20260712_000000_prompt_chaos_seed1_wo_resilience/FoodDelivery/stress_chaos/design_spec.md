# FoodDelivery Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                              | Function Name           | HTTP Method | Template File           | Context Variables (name: type)                                                                                     | Dynamic Route Parameters                |
|---------------------------------------|------------------------|-------------|-------------------------|--------------------------------------------------------------------------------------------------------------------|----------------------------------------|
| /                                     | root_redirect           | GET         | None (redirect)          | None                                                                                                               | None                                   |
| /dashboard                           | dashboard_page          | GET         | dashboard.html           | featured_restaurants: list[dict], popular_cuisines: list[str]                                                     | None                                   |
| /restaurants                        | restaurant_listing      | GET         | restaurants.html         | restaurants: list[dict], cuisine_filter_options: list[str], selected_cuisine: str (optional), search_query: str (optional) | None                                   |
| /menu/&lt;int:restaurant_id&gt;       | restaurant_menu         | GET         | menu.html                | restaurant: dict, menu_items: list[dict]                                                                          | restaurant_id: int                     |
| /item/&lt;int:item_id&gt;              | item_details            | GET         | item_details.html        | item: dict                                                                                                         | item_id: int                          |
| /cart                              | shopping_cart           | GET, POST   | cart.html                | cart_items: list[dict], total_amount: float                                                                        | None                                   |
| /cart/update                       | update_cart             | POST        | None (redirect/cart)     | None (handles cart quantity updates/removals)                                                                     | None                                   |
| /checkout                          | checkout_page           | GET, POST   | checkout.html            | if GET: None; if POST: form_submission_status: dict (success/error)                                               | None                                   |
| /orders/active                     | active_orders           | GET         | active_orders.html       | orders: list[dict], status_filter_options: list[str], selected_status: str                                        | None                                   |
| /order/track/&lt;int:order_id&gt;       | order_tracking          | GET         | track_order.html         | order_details: dict, delivery_driver_info: dict, order_items: list[dict]                                          | order_id: int                         |
| /reviews                          | reviews_page            | GET         | reviews.html             | reviews: list[dict], rating_filter_options: list[str], selected_rating: str                                       | None                                   |
| /reviews/write                    | write_review_page       | GET, POST   | write_review.html (implied, not described explicitly) | None or form submission result                                                               | None                                   |

Note: Root path '/' redirects to /dashboard.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- File path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Element IDs:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Layout Overview: Main hub with featured restaurants and popular cuisines displayed prominently. Action buttons placed for navigating to restaurants listing, cart, and active orders.
- Navigation Mappings:
  - browse-restaurants-button &rarr; restaurant_listing (url_for('restaurant_listing'))
  - view-cart-button &rarr; shopping_cart (url_for('shopping_cart'))
  - active-orders-button &rarr; active_orders (url_for('active_orders'))

---

### 2. restaurants.html
- File path: templates/restaurants.html
- Page Title: Browse Restaurants
- Element IDs:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (dropdown/select)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button) - dynamic, each restaurant's ID filled via Jinja2: id="view-restaurant-button-{{ restaurant.restaurant_id }}"
- Layout Overview: Search and filter bar at top; grid layout of restaurant cards showing logo, name, rating, and delivery time; each card includes a button to view the menu.
- Navigation Mappings:
  - view-restaurant-button-{restaurant_id} &rarr; restaurant_menu with restaurant_id (url_for('restaurant_menu', restaurant_id=restaurant.restaurant_id))

---

### 3. menu.html
- File path: templates/menu.html
- Page Title: Restaurant Menu
- Element IDs:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button) - dynamic, id="add-to-cart-button-{{ item.item_id }}"
  - view-item-details-{item_id} (button) - dynamic, id="view-item-details-{{ item.item_id }}"
- Layout Overview: Restaurant details at top with menu items shown in a grid layout, each menu item includes options to view details or add to cart.
- Navigation Mappings:
  - view-item-details-{item_id} &rarr; item_details with item_id (url_for('item_details', item_id=item.item_id))

---

### 4. item_details.html
- File path: templates/item_details.html
- Page Title: Item Details
- Element IDs:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input, number)
  - add-to-cart-button (button)
- Layout Overview: Item detailed information with description and price, input for quantity before adding to cart.
- Navigation Mappings:
  - add-to-cart-button triggers POST to add item with selected quantity (handled by backend, no navigation link ID)

---

### 5. cart.html
- File path: templates/cart.html
- Page Title: Shopping Cart
- Element IDs:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input, number) - dynamic, id="update-quantity-{{ item.item_id }}"
  - remove-item-button-{item_id} (button) - dynamic, id="remove-item-button-{{ item.item_id }}"
  - proceed-checkout-button (button)
  - total-amount (div)
- Layout Overview: Table layout displaying cart items with controls for quantity update and item removal; checkout button and total amount displayed clearly.
- Navigation Mappings:
  - proceed-checkout-button &rarr; checkout_page (url_for('checkout_page'))

---

### 6. checkout.html
- File path: templates/checkout.html
- Page Title: Checkout
- Element IDs:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (dropdown/select)
  - place-order-button (button)
- Layout Overview: Form layout collecting delivery info and payment method with a confirmation button.
- Navigation Mappings:
  - place-order-button triggers POST to place order (backend handled, no navigation link ID)

---

### 7. active_orders.html
- File path: templates/active_orders.html
- Page Title: Active Orders
- Element IDs:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button) - dynamic, id="track-order-button-{{ order.order_id }}"
  - status-filter (dropdown/select)
  - back-to-dashboard (button)
- Layout Overview: List of active orders with status filter; each order includes button to track order details; back button to dashboard.
- Navigation Mappings:
  - track-order-button-{order_id} &rarr; order_tracking with order_id (url_for('order_tracking', order_id=order.order_id))
  - back-to-dashboard &rarr; dashboard_page (url_for('dashboard_page'))

---

### 8. track_order.html
- File path: templates/track_order.html
- Page Title: Track Order
- Element IDs:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Layout Overview: Detailed tracking information including delivery driver info and timeline; back button to active orders.
- Navigation Mappings:
  - back-to-orders &rarr; active_orders (url_for('active_orders'))

---

### 9. reviews.html
- File path: templates/reviews.html
- Page Title: Order Reviews
- Element IDs:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (dropdown/select)
  - back-to-dashboard (button)
- Layout Overview: List of reviews with filter option and navigation to write new reviews; back button to dashboard.
- Navigation Mappings:
  - write-review-button &rarr; write_review_page (url_for('write_review_page'))
  - back-to-dashboard &rarr; dashboard_page (url_for('dashboard_page'))

---

## Section 3: Data Schemas

### 1. restaurants.txt
- File Name: restaurants.txt
- Fields (pipe-separated): restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
- Purpose: Stores all restaurant info with contact details and service parameters.
- Field Types and Description:
  - restaurant_id: int, unique restaurant identifier
  - name: string, restaurant name
  - cuisine: string, cuisine type
  - address: string, street address
  - phone: string, contact phone number
  - rating: float, average rating (e.g., 4.5)
  - delivery_time: int, average delivery time in minutes
  - min_order: float, minimum order value
- Examples:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

---

### 2. menus.txt
- File Name: menus.txt
- Fields (pipe-separated): item_id|restaurant_id|item_name|category|description|price|availability
- Purpose: Menu items linked to restaurants with details and availability flag.
- Field Types and Description:
  - item_id: int, unique menu item identifier
  - restaurant_id: int, corresponding restaurant ID
  - item_name: string, name of the dish
  - category: string, e.g., Appetizer, Main Course, Pasta
  - description: string, detailed description of dish
  - price: float, price in currency
  - availability: int (1 or 0), availability status
- Examples:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

---

### 3. cart.txt
- File Name: cart.txt
- Fields (pipe-separated): cart_id|item_id|restaurant_id|quantity|added_date
- Purpose: Temporary storage of cart items before order placement.
- Field Types and Description:
  - cart_id: int, unique cart line item ID
  - item_id: int, menu item ID
  - restaurant_id: int, corresponding restaurant
  - quantity: int, number of units
  - added_date: date (YYYY-MM-DD), date item added to cart
- Examples:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

---

### 4. orders.txt
- File Name: orders.txt
- Fields (pipe-separated): order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
- Purpose: Stores completed orders with customer and delivery info.
- Field Types and Description:
  - order_id: int, unique order ID
  - customer_name: string, name of customer
  - restaurant_id: int, restaurant fulfilling the order
  - order_date: date (YYYY-MM-DD)
  - total_amount: float, total price
  - status: string, order status (Delivered, On the Way, Preparing, etc.)
  - delivery_address: string, delivery location
  - phone_number: string, contact number
- Examples:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

---

### 5. order_items.txt
- File Name: order_items.txt
- Fields (pipe-separated): order_item_id|order_id|item_id|quantity|price
- Purpose: Items within an order with quantity and price details.
- Field Types and Description:
  - order_item_id: int, unique line item ID
  - order_id: int, corresponding order
  - item_id: int, menu item
  - quantity: int, amount ordered
  - price: float, item price per unit
- Examples:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

---

### 6. deliveries.txt
- File Name: deliveries.txt
- Fields (pipe-separated): delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
- Purpose: Delivery tracking information including driver details and status.
- Field Types and Description:
  - delivery_id: int, unique delivery ID
  - order_id: int, tracked order ID
  - driver_name: string
  - driver_phone: string
  - vehicle_info: string
  - status: string (Delivered, On the Way, etc.)
  - estimated_time: datetime string (YYYY-MM-DD HH:mm)
- Examples:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

---

### 7. reviews.txt
- File Name: reviews.txt
- Fields (pipe-separated): review_id|restaurant_id|customer_name|rating|review_text|review_date
- Purpose: Customer reviews for restaurants.
- Field Types and Description:
  - review_id: int, unique review ID
  - restaurant_id: int, reviewed restaurant
  - customer_name: string
  - rating: int (1-5 stars)
  - review_text: string
  - review_date: date (YYYY-MM-DD)
- Examples:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```

---

# End of Design Specification
