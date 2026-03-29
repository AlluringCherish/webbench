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
- cuisines : List[str] (all cuisine types for filter dropdown)                                                                | None                     |
| /menu/&lt;int:restaurant_id&gt;         | restaurant_menu           | GET            | restaurant_menu.html      | - restaurant : dict (restaurant details)
- menu_items : List[dict] (menu items of this restaurant)                                                                                | restaurant_id : int       |
| /item/&lt;int:item_id&gt;             | item_details_page         | GET            | item_details.html         | - item : dict (menu item details)
- quantity : int (default quantity, usually 1)                                                                                                  | item_id : int             |
| /cart                         | shopping_cart             | GET, POST      | cart.html                | GET: - cart_items : List[dict] (items in cart)
- total_amount : float
POST: - updated cart quantities or removal flags (handled server-side)                                  | None                     |
| /checkout                     | checkout_page             | GET, POST      | checkout.html            | GET: None
POST: - customer_name : str
- delivery_address : str
- phone_number : str
- payment_method : str (Credit Card, Cash, PayPal)                                         | None                     |
| /orders/active                | active_orders             | GET            | active_orders.html       | - active_orders : List[dict] (orders being prepared or delivered)                                                                                                                | None                     |
| /orders/track/&lt;int:order_id&gt;      | order_tracking            | GET            | order_tracking.html      | - order_details : dict (order general info)
- delivery_driver : dict (driver name, phone, vehicle info)
- estimated_time : str/datetime
- order_items : List[dict]               | order_id : int            |
| /reviews                     | reviews_page              | GET            | reviews.html             | - reviews : List[dict] (all reviews for display)
- filter_options : List[str] (rating filter dropdown: All, 5 stars, etc.)                                                      | None                     |
| /reviews/write               | write_review_page         | GET, POST      | write_review.html (assumed) | GET: None
POST: - restaurant_id : int
- customer_name : str
- rating : int (1-5)
- review_text : str                                                                               | None                     |

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- File path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Main Heading (&lt;h1&gt;): Food Delivery Dashboard
- Element IDs:
  - dashboard-page (div container)
  - featured-restaurants (div for featured restaurants)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Layout:
  - Single column main dashboard with featured restaurants section on top and three horizontally aligned navigation buttons below.
- Navigation mappings:
  - browse-restaurants-button 6 url_for('restaurant_listing')
  - view-cart-button 6 url_for('shopping_cart')
  - active-orders-button 6 url_for('active_orders')

### 2. restaurants.html
- File path: templates/restaurants.html
- Page Title: Browse Restaurants
- Main Heading (&lt;h1&gt;): Browse Restaurants
- Element IDs:
  - restaurants-page (div container)
  - search-input (input field)
  - cuisine-filter (dropdown select)
  - restaurants-grid (div container for restaurant cards)
  - view-restaurant-button-{restaurant_id} (button for each restaurant card)
- Layout:
  - Search and filter controls on top
  - Grid layout displaying cards for each restaurant with logo, name, rating, delivery time
- Navigation mappings:
  - view-restaurant-button-{restaurant_id} 6 url_for('restaurant_menu', restaurant_id=restaurant_id)

### 3. restaurant_menu.html
- File path: templates/restaurant_menu.html
- Page Title: Restaurant Menu
- Main Heading (&lt;h1&gt;): Restaurant Menu
- Element IDs:
  - menu-page (div container)
  - restaurant-name (h1, displaying restaurant name)
  - restaurant-info (div showing address, phone, rating)
  - menu-items-grid (div grid for menu items)
  - add-to-cart-button-{item_id} (button for each menu item)
  - view-item-details-{item_id} (button for each menu item)
- Layout:
  - Top header with restaurant name and info
  - Grid of menu items below
- Navigation mappings:
  - add-to-cart-button-{item_id} 6 adds item to cart (POST handled, no routing)
  - view-item-details-{item_id} 6 url_for('item_details_page', item_id=item_id)

### 4. item_details.html
- File path: templates/item_details.html
- Page Title: Item Details
- Main Heading (&lt;h1&gt;): Item Details
- Element IDs:
  - item-details-page (div container)
  - item-name (h1)
  - item-description (div showing description and ingredients)
  - item-price (div showing price)
  - quantity-input (input number field)
  - add-to-cart-button (button)
- Layout:
  - Item name and description on top
  - Price and quantity selection below
- Navigation mappings:
  - add-to-cart-button 6 adds item to cart with specified quantity (POST handled)

### 5. cart.html
- File path: templates/cart.html
- Page Title: Shopping Cart
- Main Heading (&lt;h1&gt;): Shopping Cart
- Element IDs:
  - cart-page (div container)
  - cart-items-table (table with cart items)
  - update-quantity-{item_id} (input number for quantity update)
  - remove-item-button-{item_id} (button for removing item)
  - proceed-checkout-button (button)
  - total-amount (div displaying total price)
- Layout:
  - Table listing all cart items with quantities and prices
  - Controls for updating quantities and removing items
  - Proceed to checkout button at bottom
- Navigation mappings:
  - proceed-checkout-button 6 url_for('checkout_page')

### 6. checkout.html
- File path: templates/checkout.html
- Page Title: Checkout
- Main Heading (&lt;h1&gt;): Checkout
- Element IDs:
  - checkout-page (div container)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (dropdown select)
  - place-order-button (button)
- Layout:
  - Form layout with fields for customer info and payment
  - Place order button at bottom
- Navigation mappings:
  - place-order-button triggers POST to place order

### 7. active_orders.html
- File path: templates/active_orders.html
- Page Title: Active Orders
- Main Heading (&lt;h1&gt;): Active Orders
- Element IDs:
  - active-orders-page (div container)
  - orders-list (div list showing active orders)
  - track-order-button-{order_id} (button for each order)
  - status-filter (dropdown select)
  - back-to-dashboard (button)
- Layout:
  - List of orders with status filter dropdown on top
  - Orders display with tracking buttons
  - Back to dashboard button
- Navigation mappings:
  - track-order-button-{order_id} 6 url_for('order_tracking', order_id=order_id)
  - back-to-dashboard 6 url_for('dashboard_page')

### 8. order_tracking.html
- File path: templates/order_tracking.html
- Page Title: Track Order
- Main Heading (&lt;h1&gt;): Track Order
- Element IDs:
  - tracking-page (div container)
  - order-details (div showing order info and timeline)
  - delivery-driver-info (div showing driver contact and vehicle)
  - estimated-time (div showing estimated delivery time)
  - order-items-list (div listing order items)
  - back-to-orders (button)
- Layout:
  - Order details and timeline summary on top
  - Driver info and ETA below
  - List of ordered items
- Navigation mappings:
  - back-to-orders 6 url_for('active_orders')

### 9. reviews.html
- File path: templates/reviews.html
- Page Title: Order Reviews
- Main Heading (&lt;h1&gt;): Order Reviews
- Element IDs:
  - reviews-page (div container)
  - reviews-list (div showing all reviews)
  - write-review-button (button)
  - filter-by-rating (dropdown select)
  - back-to-dashboard (button)
- Layout:
  - Filter dropdown and reviews list
  - Button to navigate to reviews writing page
- Navigation mappings:
  - write-review-button 6 url_for('write_review_page')
  - back-to-dashboard 6 url_for('dashboard_page')

---

## Section 3: Data Schemas

### 1. restaurants.txt
- File Path: data/restaurants.txt
- Fields (pipe-delimited):
  - restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
- Purpose: Stores restaurant information including contact, cuisine type, rating, delivery time, and minimum order value.
- Field Types:
  - restaurant_id: int
  - name: string
  - cuisine: string
  - address: string
  - phone: string
  - rating: float
  - delivery_time: int (minutes)
  - min_order: float
- Example Rows:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

### 2. menus.txt
- File Path: data/menus.txt
- Fields (pipe-delimited):
  - item_id|restaurant_id|item_name|category|description|price|availability
- Purpose: Stores menu items associated with restaurants, including descriptions and availability.
- Field Types:
  - item_id: int
  - restaurant_id: int
  - item_name: string
  - category: string
  - description: string
  - price: float
  - availability: int (1 for available, 0 for not)
- Example Rows:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### 3. cart.txt
- File Path: data/cart.txt
- Fields (pipe-delimited):
  - cart_id|item_id|restaurant_id|quantity|added_date
- Purpose: Stores current shopping cart items per user session.
- Field Types:
  - cart_id: int
  - item_id: int
  - restaurant_id: int
  - quantity: int
  - added_date: date (YYYY-MM-DD)
- Example Rows:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

### 4. orders.txt
- File Path: data/orders.txt
- Fields (pipe-delimited):
  - order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
- Purpose: Stores completed and active order data including customer and delivery info.
- Field Types:
  - order_id: int
  - customer_name: string
  - restaurant_id: int
  - order_date: date (YYYY-MM-DD)
  - total_amount: float
  - status: string (e.g., Delivered, On the Way, Preparing)
  - delivery_address: string
  - phone_number: string
- Example Rows:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

### 5. order_items.txt
- File Path: data/order_items.txt
- Fields (pipe-delimited):
  - order_item_id|order_id|item_id|quantity|price
- Purpose: Stores individual items for each order.
- Field Types:
  - order_item_id: int
  - order_id: int
  - item_id: int
  - quantity: int
  - price: float
- Example Rows:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

### 6. deliveries.txt
- File Path: data/deliveries.txt
- Fields (pipe-delimited):
  - delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
- Purpose: Stores delivery details and status for orders.
- Field Types:
  - delivery_id: int
  - order_id: int
  - driver_name: string
  - driver_phone: string
  - vehicle_info: string
  - status: string (e.g., Delivered, On the Way)
  - estimated_time: datetime string (YYYY-MM-DD HH:MM)
- Example Rows:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### 7. reviews.txt
- File Path: data/reviews.txt
- Fields (pipe-delimited):
  - review_id|restaurant_id|customer_name|rating|review_text|review_date
- Purpose: Stores customer reviews for restaurants.
- Field Types:
  - review_id: int
  - restaurant_id: int
  - customer_name: string
  - rating: int (1-5)
  - review_text: string
  - review_date: date (YYYY-MM-DD)
- Example Rows:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```

---

# End of Design Specification
