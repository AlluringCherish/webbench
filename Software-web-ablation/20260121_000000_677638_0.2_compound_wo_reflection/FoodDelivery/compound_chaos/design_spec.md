# Design Specification for 'FoodDelivery' Web Application

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name          | HTTP Method | Template File           | Context Variables (name: type)                                                                                          | Dynamic Parameters                |
|--------------------------------|------------------------|-------------|-------------------------|--------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| /                              | root_redirect           | GET         | N/A (redirect)          | None                                                                                                                     | None                             |
| /dashboard                     | dashboard              | GET         | dashboard.html          | featured_restaurants: list(dict), popular_cuisines: list(str) (if used), None other specified explicitly                   | None                             |
| /restaurants                   | browse_restaurants     | GET         | restaurants.html        | restaurants: list(dict), cuisine_options: list(str), search_query: str (optional), selected_cuisine: str (optional)         | None                             |
| /menu/&lt;int:restaurant_id&gt;      | restaurant_menu        | GET         | menu.html               | restaurant: dict, menu_items: list(dict)                                                                                  | restaurant_id: int               |
| /item/&lt;int:item_id&gt;            | item_details           | GET         | item_details.html       | item: dict                                                                                                               | item_id: int                    |
| /cart                         | shopping_cart          | GET, POST   | cart.html               | cart_items: list(dict), total_amount: float                                                                               | None                             |
| /checkout                     | checkout               | GET, POST   | checkout.html           | None (GET: display empty form; POST: process form submission)                                                              | None                             |
| /orders/active                | active_orders          | GET         | active_orders.html      | active_orders: list(dict), status_options: list(str), selected_status: str (optional)                                       | None                             |
| /orders/track/&lt;int:order_id&gt;   | track_order            | GET         | track_order.html        | order: dict, delivery_info: dict, order_items: list(dict)                                                                  | order_id: int                   |
| /reviews                     | reviews                | GET         | reviews.html            | reviews: list(dict), rating_filter_options: list(str), selected_rating: str (optional)                                      | None                             |


### Details:

- **Root Route `/`**: Redirects to `/dashboard`.
- **Dashboard route** loads featured restaurants and potentially popular cuisines (optional).
- **Browse Restaurants** allows searching and filtering by cuisine type.
- **Restaurant Menu** displays all menu items of a restaurant.
- **Item Details** shows detailed info on a selected menu item.
- **Shopping Cart** supports GET (view) and POST (update quantities/remove items).
- **Checkout** page for delivery info and order placement (GET shows form, POST processes order).
- **Active Orders** displays current orders filtered by status.
- **Track Order** displays detailed tracking info.
- **Reviews** page displays and filters customer reviews.

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- File Path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Layout Overview: A dashboard main container with featured restaurants listing and navigation buttons.
- Element IDs and Types:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Navigation Mappings:
  - browse-restaurants-button: url_for('browse_restaurants')
  - view-cart-button: url_for('shopping_cart')
  - active-orders-button: url_for('active_orders')

---

### 2. restaurants.html
- File Path: templates/restaurants.html
- Page Title: Browse Restaurants
- Layout Overview: Container with search input, cuisine filter dropdown, and a restaurants grid.
- Element IDs and Types:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (select/dropdown)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button) - dynamic for each restaurant card
- Navigation Mappings:
  - view-restaurant-button-{restaurant_id}: url_for('restaurant_menu', restaurant_id=restaurant_id)

---

### 3. menu.html
- File Path: templates/menu.html
- Page Title: Restaurant Menu
- Layout Overview: Container showing restaurant info header and menu items grid.
- Element IDs and Types:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button) - dynamic for each menu item
  - view-item-details-{item_id} (button) - dynamic for each menu item
- Navigation Mappings:
  - add-to-cart-button-{item_id}: triggers backend route POST (not route navigation)
  - view-item-details-{item_id}: url_for('item_details', item_id=item_id)

---

### 4. item_details.html
- File Path: templates/item_details.html
- Page Title: Item Details
- Layout Overview: Container with item name header and detailed descriptions with pricing and quantity input.
- Element IDs and Types:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input, number)
  - add-to-cart-button (button)
- Navigation Mappings:
  - add-to-cart-button: triggers backend POST to add with quantity (no route redirection)

---

### 5. cart.html
- File Path: templates/cart.html
- Page Title: Shopping Cart
- Layout Overview: Container with a cart items table and checkout controls.
- Element IDs and Types:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input, number) - dynamic for each cart item
  - remove-item-button-{item_id} (button) - dynamic for each cart item
  - proceed-checkout-button (button)
  - total-amount (div)
- Navigation Mappings:
  - proceed-checkout-button: url_for('checkout')
  - remove-item-button-{item_id}: triggers backend POST to remove item
  - update-quantity-{item_id}: used for form submission

---

### 6. checkout.html
- File Path: templates/checkout.html
- Page Title: Checkout
- Layout Overview: Form container for inputting customer details and confirming order.
- Element IDs and Types:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (select/dropdown)
  - place-order-button (button)
- Navigation Mappings:
  - place-order-button: triggers POST submission to same route

---

### 7. active_orders.html
- File Path: templates/active_orders.html
- Page Title: Active Orders
- Layout Overview: Container with active orders list and status filter dropdown.
- Element IDs and Types:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button) - dynamic for each order
  - status-filter (select/dropdown)
  - back-to-dashboard (button)
- Navigation Mappings:
  - track-order-button-{order_id}: url_for('track_order', order_id=order_id)
  - back-to-dashboard: url_for('dashboard')

---

### 8. track_order.html
- File Path: templates/track_order.html
- Page Title: Track Order
- Layout Overview: Container showing order details, driver info, estimated time, and item list.
- Element IDs and Types:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Navigation Mappings:
  - back-to-orders: url_for('active_orders')

---

### 9. reviews.html
- File Path: templates/reviews.html
- Page Title: Order Reviews
- Layout Overview: Container with reviews list, filter dropdown, and write review button.
- Element IDs and Types:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (select/dropdown)
  - back-to-dashboard (button)
- Navigation Mappings:
  - write-review-button: (could link to a review submission page - not specified in user task, so possibly no route)
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data Schemas

### 1. restaurants.txt
- Purpose: Stores restaurant information including details and ratings.
- Field Order and Names:
  ```
  restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
  ```
- Field Types:
  - restaurant_id: int
  - name: string
  - cuisine: string
  - address: string
  - phone: string
  - rating: float
  - delivery_time: int (minutes)
  - min_order: float
- Example Data:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

---

### 2. menus.txt
- Purpose: Stores menu items for restaurants.
- Field Order and Names:
  ```
  item_id|restaurant_id|item_name|category|description|price|availability
  ```
- Field Types:
  - item_id: int
  - restaurant_id: int
  - item_name: string
  - category: string
  - description: string
  - price: float
  - availability: int (1 = available, 0 = not)
- Example Data:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

---

### 3. cart.txt
- Purpose: Stores items user has added to shopping cart.
- Field Order and Names:
  ```
  cart_id|item_id|restaurant_id|quantity|added_date
  ```
- Field Types:
  - cart_id: int
  - item_id: int
  - restaurant_id: int
  - quantity: int
  - added_date: date (YYYY-MM-DD)
- Example Data:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

---

### 4. orders.txt
- Purpose: Stores orders with customer and order details.
- Field Order and Names:
  ```
  order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
  ```
- Field Types:
  - order_id: int
  - customer_name: string
  - restaurant_id: int
  - order_date: date (YYYY-MM-DD)
  - total_amount: float
  - status: string (e.g. Delivered, On the Way, Preparing)
  - delivery_address: string
  - phone_number: string
- Example Data:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

---

### 5. order_items.txt
- Purpose: Stores individual items belonging to orders.
- Field Order and Names:
  ```
  order_item_id|order_id|item_id|quantity|price
  ```
- Field Types:
  - order_item_id: int
  - order_id: int
  - item_id: int
  - quantity: int
  - price: float
- Example Data:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

---

### 6. deliveries.txt
- Purpose: Stores deliveries info including driver and status.
- Field Order and Names:
  ```
  delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
  ```
- Field Types:
  - delivery_id: int
  - order_id: int
  - driver_name: string
  - driver_phone: string
  - vehicle_info: string
  - status: string
  - estimated_time: datetime (YYYY-MM-DD HH:MM)
- Example Data:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

---

### 7. reviews.txt
- Purpose: Stores customer reviews of restaurants.
- Field Order and Names:
  ```
  review_id|restaurant_id|customer_name|rating|review_text|review_date
  ```
- Field Types:
  - review_id: int
  - restaurant_id: int
  - customer_name: string
  - rating: int (1-5)
  - review_text: string
  - review_date: date (YYYY-MM-DD)
- Example Data:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```
