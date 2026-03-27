# FoodDelivery Web Application Design Specification

---

## 1. Flask Routes Specification

| Route Path                     | Function Name             | HTTP Method(s) | Template File         | Context Variables (name: type)                    | Parameters (name: type)           |
|-------------------------------|---------------------------|----------------|-----------------------|---------------------------------------------------|----------------------------------|
| `/`                           | root_redirect             | GET            | N/A                   | N/A                                               | N/A                              |
| `/dashboard`                  | dashboard                 | GET            | dashboard.html         | featured_restaurants: list, popular_cuisines: list | N/A                              |
| `/restaurants`                | browse_restaurants         | GET            | restaurants.html       | restaurants: list, cuisine_options: list           | N/A                              |
| `/menu/<int:restaurant_id>`  | restaurant_menu           | GET            | menu.html              | restaurant: dict, menu_items: list                 | restaurant_id: int                |
| `/item/<int:item_id>`         | item_details              | GET            | item_details.html      | item: dict                                      | item_id: int                      |
| `/cart`                      | view_cart                  | GET            | cart.html              | cart_items: list, total_amount: float              | N/A                              |
| `/cart/update`               | update_cart                | POST           | N/A                   | N/A                                               | N/A                              |
| `/checkout`                  | checkout                  | GET, POST      | checkout.html          | (GET) , (POST) order_confirmation: dict or None    | N/A                              |
| `/orders/active`             | active_orders             | GET            | active_orders.html     | active_orders: list, status_options: list          | N/A                              |
| `/orders/track/<int:order_id>`| track_order              | GET            | track_order.html       | order: dict, delivery_info: dict, order_items: list | order_id: int                    |
| `/reviews`                   | reviews                   | GET            | reviews.html           | reviews: list, rating_filter_options: list         | N/A                              |
| `/reviews/write`             | write_review              | GET, POST      | write_review.html      | (GET) , (POST) submission_status: bool or None     | N/A                              |

**Explanation:**
- Root route `/` redirects to `/dashboard`.
- POST routes are for updating cart and submitting reviews.
- Template context variables use snake_case naming matching the purpose.
- Parameter names reflect the dynamic parts of the route.


## 2. HTML Template Specifications

### 2.1. dashboard.html
- File Path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Layout Overview: Container div with featured restaurants and navigation buttons leading to main functionalities.
- Element IDs:
  - `dashboard-page` (Div)
  - `featured-restaurants` (Div)
  - `browse-restaurants-button` (Button)
  - `view-cart-button` (Button)
  - `active-orders-button` (Button)
- Navigation Mappings:
  - `browse-restaurants-button`: url_for('browse_restaurants')
  - `view-cart-button`: url_for('view_cart')
  - `active-orders-button`: url_for('active_orders')

### 2.2. restaurants.html
- File Path: templates/restaurants.html
- Page Title: Browse Restaurants
- Layout Overview: Search and filter controls above a grid of restaurant cards.
- Element IDs:
  - `restaurants-page` (Div)
  - `search-input` (Input)
  - `cuisine-filter` (Dropdown)
  - `restaurants-grid` (Div)
  - `view-restaurant-button-{restaurant_id}` (Button)
- Navigation Mappings:
  - `view-restaurant-button-{restaurant_id}`: url_for('restaurant_menu', restaurant_id=restaurant_id)
- Dynamic Element ID Pattern:
  - Buttons in restaurant cards: `view-restaurant-button-{{ restaurant_id }}`

### 2.3. menu.html
- File Path: templates/menu.html
- Page Title: Restaurant Menu
- Layout Overview: Restaurant info header followed by a grid of menu items.
- Element IDs:
  - `menu-page` (Div)
  - `restaurant-name` (H1)
  - `restaurant-info` (Div)
  - `menu-items-grid` (Div)
  - `add-to-cart-button-{item_id}` (Button)
  - `view-item-details-{item_id}` (Button)
- Navigation Mappings:
  - `add-to-cart-button-{item_id}`: (functionality to add item to cart)
  - `view-item-details-{item_id}`: url_for('item_details', item_id=item_id)
- Dynamic Element ID Pattern:
  - Add to Cart Buttons: `add-to-cart-button-{{ item_id }}`
  - View Details Buttons: `view-item-details-{{ item_id }}`

### 2.4. item_details.html
- File Path: templates/item_details.html
- Page Title: Item Details
- Layout Overview: Detailed view of a menu item with quantity input and add to cart button.
- Element IDs:
  - `item-details-page` (Div)
  - `item-name` (H1)
  - `item-description` (Div)
  - `item-price` (Div)
  - `quantity-input` (Input number)
  - `add-to-cart-button` (Button)
- Navigation Mappings:
  - `add-to-cart-button`: (adds item with quantity to cart)

### 2.5. cart.html
- File Path: templates/cart.html
- Page Title: Shopping Cart
- Layout Overview: Table of cart items with quantity inputs and remove buttons plus checkout button.
- Element IDs:
  - `cart-page` (Div)
  - `cart-items-table` (Table)
  - `update-quantity-{item_id}` (Input number)
  - `remove-item-button-{item_id}` (Button)
  - `proceed-checkout-button` (Button)
  - `total-amount` (Div)
- Navigation Mappings:
  - `proceed-checkout-button`: url_for('checkout')
- Dynamic Element ID Pattern:
  - Quantity Inputs: `update-quantity-{{ item_id }}`
  - Remove Buttons: `remove-item-button-{{ item_id }}`

### 2.6. checkout.html
- File Path: templates/checkout.html
- Page Title: Checkout
- Layout Overview: Form with fields for delivery and payment info and place order button.
- Element IDs:
  - `checkout-page` (Div)
  - `customer-name` (Input)
  - `delivery-address` (Textarea)
  - `phone-number` (Input)
  - `payment-method` (Dropdown)
  - `place-order-button` (Button)

### 2.7. active_orders.html
- File Path: templates/active_orders.html
- Page Title: Active Orders
- Layout Overview: List of current orders with filter and buttons to track orders.
- Element IDs:
  - `active-orders-page` (Div)
  - `orders-list` (Div)
  - `track-order-button-{order_id}` (Button)
  - `status-filter` (Dropdown)
  - `back-to-dashboard` (Button)
- Navigation Mappings:
  - `back-to-dashboard`: url_for('dashboard')
  - `track-order-button-{order_id}`: url_for('track_order', order_id=order_id)
- Dynamic Element ID Pattern:
  - Track Buttons: `track-order-button-{{ order_id }}`

### 2.8. track_order.html
- File Path: templates/track_order.html
- Page Title: Track Order
- Layout Overview: Display detailed tracking info with back button.
- Element IDs:
  - `tracking-page` (Div)
  - `order-details` (Div)
  - `delivery-driver-info` (Div)
  - `estimated-time` (Div)
  - `order-items-list` (Div)
  - `back-to-orders` (Button)
- Navigation Mappings:
  - `back-to-orders`: url_for('active_orders')

### 2.9. reviews.html
- File Path: templates/reviews.html
- Page Title: Order Reviews
- Layout Overview: List of reviews with filtering and navigation buttons.
- Element IDs:
  - `reviews-page` (Div)
  - `reviews-list` (Div)
  - `write-review-button` (Button)
  - `filter-by-rating` (Dropdown)
  - `back-to-dashboard` (Button)
- Navigation Mappings:
  - `write-review-button`: url_for('write_review')
  - `back-to-dashboard`: url_for('dashboard')

### 2.10. write_review.html
- File Path: templates/write_review.html
- Page Title: Write Review
- Layout Overview: Form to submit a review.
- Element IDs:
  - `write-review-page` (Div)  <!-- Note: not specified in requirements, logically added -->
  - `review-form` (Form)       <!-- Logical grouping -->
  - `restaurant-select` (Dropdown) <!-- Presumed for selecting a restaurant when writing review -->
  - `customer-name-input` (Input)  <!-- For entering customer name -->
  - `rating-select` (Dropdown)      <!-- For selecting rating -->
  - `review-textarea` (Textarea)    <!-- For review text -->
  - `submit-review-button` (Button) <!-- For submitting review -->

*(Note: The write review page elements and IDs are inferred logically since the requirements specify navigation but not page elements explicitly.)*

---

## 3. Data Schemas

### 3.1. restaurants.txt
- File name: restaurants.txt
- Fields (order separated by | ): restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
- Purpose: Stores restaurant details including identification, cuisine type, location, contact, rating, delivery time, and minimum order amount.
- Data types:
  - restaurant_id: int
  - name: string
  - cuisine: string
  - address: string
  - phone: string
  - rating: float
  - delivery_time: int (minutes)
  - min_order: float
- Example rows:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

### 3.2. menus.txt
- File name: menus.txt
- Fields: item_id|restaurant_id|item_name|category|description|price|availability
- Purpose: Stores menu items belonging to restaurants, their categorization, descriptions, prices, and availability status.
- Data types:
  - item_id: int
  - restaurant_id: int
  - item_name: string
  - category: string
  - description: string
  - price: float
  - availability: int (1 or 0)
- Example rows:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### 3.3. cart.txt
- File name: cart.txt
- Fields: cart_id|item_id|restaurant_id|quantity|added_date
- Purpose: Stores the current shopping cart items with quantities and added dates.
- Data types:
  - cart_id: int
  - item_id: int
  - restaurant_id: int
  - quantity: int
  - added_date: date (YYYY-MM-DD)
- Example rows:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

### 3.4. orders.txt
- File name: orders.txt
- Fields: order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
- Purpose: Stores order records including customer info, restaurant, order date, amount, status, and delivery info.
- Data types:
  - order_id: int
  - customer_name: string
  - restaurant_id: int
  - order_date: date (YYYY-MM-DD)
  - total_amount: float
  - status: string
  - delivery_address: string
  - phone_number: string
- Example rows:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

### 3.5. order_items.txt
- File name: order_items.txt
- Fields: order_item_id|order_id|item_id|quantity|price
- Purpose: Stores individual items per order, quantities, and price at order time.
- Data types:
  - order_item_id: int
  - order_id: int
  - item_id: int
  - quantity: int
  - price: float
- Example rows:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

### 3.6. deliveries.txt
- File name: deliveries.txt
- Fields: delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
- Purpose: Stores delivery details including driver information, vehicle, delivery status, and ETA.
- Data types:
  - delivery_id: int
  - order_id: int
  - driver_name: string
  - driver_phone: string
  - vehicle_info: string
  - status: string
  - estimated_time: date-time string (YYYY-MM-DD HH:MM)
- Example rows:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### 3.7. reviews.txt
- File name: reviews.txt
- Fields: review_id|restaurant_id|customer_name|rating|review_text|review_date
- Purpose: Stores customer reviews for restaurants including rating and review text.
- Data types:
  - review_id: int
  - restaurant_id: int
  - customer_name: string
  - rating: int (stars)
  - review_text: string
  - review_date: date (YYYY-MM-DD)
- Example rows:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```

---

### Notes:
- The root `/` route redirects to `/dashboard` to comply with start page requirement.
- The write review page element IDs are inferred as the original description lacks specific IDs and elements for that page.
- All context and variable names adhere strictly to snake_case.
- All element IDs use exact casing and spelling as provided.
- Navigation IDs map exactly to route functions using Flask's `url_for()` in parentheses.
- Templates reflect each page as specified, providing clear frontend development guidance.
- Data schemas provide field order, types, purpose, and examples for backend data processing.

This completes the comprehensive design specification for the FoodDelivery web application.

---
