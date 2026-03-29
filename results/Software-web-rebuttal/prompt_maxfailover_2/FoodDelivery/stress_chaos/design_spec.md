# FoodDelivery Web Application - Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name           | HTTP Method(s) | Template File           | Context Variables (name : type)                                                                                                                                                  | Dynamic Parameters       |
|--------------------------------|-------------------------|----------------|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| /                              | root_redirect            | GET            | N/A                     | None (redirects to /dashboard)                                                                                                                                                   | None                     |
| /dashboard                     | dashboard               | GET            | dashboard.html          | featured_restaurants : list of dict, popular_cuisines : list of string                                                                                                          | None                     |
| /restaurants                   | restaurant_listing      | GET            | restaurants.html        | restaurants : list of dict, cuisine_options : list of string, selected_cuisine : string or None, search_query : string or None                                                   | None                     |
| /menu/&lt;int:restaurant_id&gt;   | restaurant_menu         | GET            | menu.html               | restaurant : dict, menu_items : list of dict                                                                                                                                      | restaurant_id : int       |
| /item/&lt;int:item_id&gt;           | item_details            | GET            | item_details.html       | item : dict                                                                                                                                                                      | item_id : int              |
| /cart                         | shopping_cart           | GET, POST      | cart.html               | cart_items : list of dict, total_amount : float                                                                                                                                  | None                     |
| /checkout                     | checkout                | GET, POST      | checkout.html           | order_form : dict (fields: customer_name, delivery_address, phone_number, payment_method), errors : dict (optional)                                                              | None                     |
| /orders/active                | active_orders           | GET            | active_orders.html      | active_orders : list of dict, status_options : list of string, selected_status : string                                                                                            | None                     |
| /orders/track/&lt;int:order_id&gt;  | order_tracking          | GET            | order_tracking.html     | order_details : dict, delivery_driver : dict, estimated_time : string, order_items : list of dict                                                                                  | order_id : int             |
| /reviews                     | reviews                 | GET            | reviews.html            | reviews : list of dict, rating_filter_options : list of string, selected_rating_filter : string                                                                                   | None                     |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- File Path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Element IDs:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Layout Overview: Main container holds featured restaurants section, popular cuisines area, and navigation buttons for restaurant browsing, cart, and active orders.
- Navigation Mappings:
  - browse-restaurants-button &rarr; restaurant_listing
  - view-cart-button &rarr; shopping_cart
  - active-orders-button &rarr; active_orders

### 2. Restaurant Listing Page
- File Path: templates/restaurants.html
- Page Title: Browse Restaurants
- Element IDs:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (dropdown/select)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button) - dynamic per restaurant
- Layout Overview: Container with search bar and cuisine filter at top, followed by a grid showing restaurant cards.
- Navigation Mappings:
  - view-restaurant-button-{restaurant_id} &rarr; restaurant_menu (restaurant_id parameter)

### 3. Restaurant Menu Page
- File Path: templates/menu.html
- Page Title: Restaurant Menu
- Element IDs:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button)
  - view-item-details-{item_id} (button)
- Layout Overview: Header with restaurant name and info; menu items displayed in grid with add and details buttons.
- Navigation Mappings:
  - add-to-cart-button-{item_id} : triggers adding item to cart (form POST or JS)
  - view-item-details-{item_id} &rarr; item_details (item_id parameter)

### 4. Item Details Page
- File Path: templates/item_details.html
- Page Title: Item Details
- Element IDs:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input number)
  - add-to-cart-button (button)
- Layout Overview: Show item name, description including ingredients, price, and quantity input with add to cart button.
- Navigation Mappings:
  - add-to-cart-button : triggers adding specified quantity to cart

### 5. Shopping Cart Page
- File Path: templates/cart.html
- Page Title: Shopping Cart
- Element IDs:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input number)
  - remove-item-button-{item_id} (button)
  - proceed-checkout-button (button)
  - total-amount (div)
- Layout Overview: Table listing items with quantities, price, and subtotal; with option to update quantities or remove items; total amount displayed below with checkout button.
- Navigation Mappings:
  - proceed-checkout-button &rarr; checkout

### 6. Checkout Page
- File Path: templates/checkout.html
- Page Title: Checkout
- Element IDs:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (dropdown/select)
  - place-order-button (button)
- Layout Overview: Form to enter customer details, delivery address, phone number, and payment method with place order button.
- Navigation Mappings:
  - place-order-button : submits order form

### 7. Active Orders Page
- File Path: templates/active_orders.html
- Page Title: Active Orders
- Element IDs:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button)
  - status-filter (dropdown/select)
  - back-to-dashboard (button)
- Layout Overview: List of active orders with filters, each order can be tracked via corresponding button.
- Navigation Mappings:
  - track-order-button-{order_id} &rarr; order_tracking (order_id parameter)
  - back-to-dashboard &rarr; dashboard

### 8. Order Tracking Page
- File Path: templates/order_tracking.html
- Page Title: Track Order
- Element IDs:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Layout Overview: Shows detailed order timeline, driver info, delivery ETA, and list of ordered items.
- Navigation Mappings:
  - back-to-orders &rarr; active_orders

### 9. Reviews Page
- File Path: templates/reviews.html
- Page Title: Order Reviews
- Element IDs:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (dropdown/select)
  - back-to-dashboard (button)
- Layout Overview: List customer reviews with filters, and button to navigate to review writing (if implemented in future).
- Navigation Mappings:
  - back-to-dashboard &rarr; dashboard

---

## Section 3: Data Schemas

### 1. restaurants.txt
- File Name: restaurants.txt
- Field Order (pipe-delimited):
  restaurant_id | name | cuisine | address | phone | rating | delivery_time | min_order
- Purpose: Stores restaurant information including contact and delivery details.
- Field Types:
  restaurant_id: int
  name: string
  cuisine: string
  address: string
  phone: string
  rating: float
  delivery_time: int (minutes)
  min_order: float
- Example Rows:
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00

---

### 2. menus.txt
- File Name: menus.txt
- Field Order (pipe-delimited):
  item_id | restaurant_id | item_name | category | description | price | availability
- Purpose: Menu items for restaurants with details and availability status.
- Field Types:
  item_id: int
  restaurant_id: int
  item_name: string
  category: string
  description: string
  price: float
  availability: int (1 for available, 0 for not)
- Example Rows:
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1

---

### 3. cart.txt
- File Name: cart.txt
- Field Order (pipe-delimited):
  cart_id | item_id | restaurant_id | quantity | added_date
- Purpose: Stores current shopping cart items for users.
- Field Types:
  cart_id: int
  item_id: int
  restaurant_id: int
  quantity: int
  added_date: date (YYYY-MM-DD)
- Example Rows:
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16

---

### 4. orders.txt
- File Name: orders.txt
- Field Order (pipe-delimited):
  order_id | customer_name | restaurant_id | order_date | total_amount | status | delivery_address | phone_number
- Purpose: Stores all orders placed with status and contact.
- Field Types:
  order_id: int
  customer_name: string
  restaurant_id: int
  order_date: date (YYYY-MM-DD)
  total_amount: float
  status: string
  delivery_address: string
  phone_number: string
- Example Rows:
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678

---

### 5. order_items.txt
- File Name: order_items.txt
- Field Order (pipe-delimited):
  order_item_id | order_id | item_id | quantity | price
- Purpose: Items contained in each order with quantity and price details.
- Field Types:
  order_item_id: int
  order_id: int
  item_id: int
  quantity: int
  price: float
- Example Rows:
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99

---

### 6. deliveries.txt
- File Name: deliveries.txt
- Field Order (pipe-delimited):
  delivery_id | order_id | driver_name | driver_phone | vehicle_info | status | estimated_time
- Purpose: Delivery tracking info including driver and vehicle data.
- Field Types:
  delivery_id: int
  order_id: int
  driver_name: string
  driver_phone: string
  vehicle_info: string
  status: string
  estimated_time: datetime string (YYYY-MM-DD HH:MM)
- Example Rows:
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30

---

### 7. reviews.txt
- File Name: reviews.txt
- Field Order (pipe-delimited):
  review_id | restaurant_id | customer_name | rating | review_text | review_date
- Purpose: Customer reviews for restaurants including rating and text.
- Field Types:
  review_id: int
  restaurant_id: int
  customer_name: string
  rating: int
  review_text: string
  review_date: date (YYYY-MM-DD)
- Example Rows:
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15

---

*End of Design Specification.*
