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
| /menu/item/&lt;int:item_id&gt;      | item_details          | GET         | item_details.html     | item (dict): item_id (int), item_name (str), category (str), description (str), price (float), availability (int), ingredients (str), nutritional_info (str) | item_id (int)                       |
| /cart                        | shopping_cart         | GET, POST   | cart.html             | cart_items (list of dict), each with: item_id (int), item_name (str), quantity (int), price (float), subtotal (float), restaurant_id (int)
 total_amount (float)                                                                        | None                                 |
| /checkout                    | checkout              | GET, POST   | checkout.html         | None for GET
 POST accepts form data: customer_name (str), delivery_address (str), phone_number (str), payment_method (str)           | None                                 |
| /orders/active               | active_orders         | GET         | active_orders.html    | active_orders (list of dict), each with: order_id (int), restaurant_name (str), status (str), eta (str)                          | None                                 |
| /orders/track/&lt;int:order_id&gt;   | order_tracking        | GET         | order_tracking.html   | order (dict): order_id (int), customer_name (str), restaurant_name (str), order_date (str), total_amount (float), status (str), delivery_address (str), phone_number (str)
 delivery (dict): driver_name (str), driver_phone (str), vehicle_info (str), status (str), estimated_time (str)
 order_items (list of dict): item_name (str), quantity (int), price (float)                                | order_id (int)                      |
| /reviews                    | reviews               | GET         | reviews.html          | reviews (list of dict), each with: review_id (int), restaurant_name (str), customer_name (str), rating (int), review_text (str), review_date (str) | None                                 |
| /reviews/write              | write_review          | GET, POST   | write_review.html     | restaurants (list of dict), each with restaurant_id (int), name (str) for review form (GET)
 POST accepts form data: restaurant_id (int), customer_name (str), rating (int), review_text (str) | None                                 |

---

## Section 2: HTML Template Specifications

### templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Layout Overview: Main container div with featured restaurants section and three navigation buttons to restaurants listing, cart, and active orders.
- Element IDs and types:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Navigation Mappings:
  - browse-restaurants-button -> browse_restaurants
  - view-cart-button -> shopping_cart
  - active-orders-button -> active_orders

---

### templates/restaurants.html
- Page Title: Browse Restaurants
- Layout Overview: Container div with search input, cuisine filter, and grid of restaurant cards each with view button.
- Element IDs and types:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (dropdown/select)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button) - dynamic id pattern, e.g. add Jinja2: id="view-restaurant-button-{{ restaurant.restaurant_id }}"
- Navigation Mappings:
  - view-restaurant-button-{restaurant_id} -> restaurant_menu (route parameter: restaurant_id)

---

### templates/menu.html
- Page Title: Restaurant Menu
- Layout Overview: Container with restaurant name and info, grid of menu items each having add to cart and details buttons.
- Element IDs and types:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button) - dynamic with Jinja2: id="add-to-cart-button-{{ item.item_id }}"
  - view-item-details-{item_id} (button) - dynamic with Jinja2: id="view-item-details-{{ item.item_id }}"
- Navigation Mappings:
  - view-item-details-{item_id} -> item_details (route parameter: item_id)

---

### templates/item_details.html
- Page Title: Item Details
- Layout Overview: Container showing item name, description, price, quantity input and add to cart button.
- Element IDs and types:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input number)
  - add-to-cart-button (button)

---

### templates/cart.html
- Page Title: Shopping Cart
- Layout Overview: Container with table of cart items showing update quantity inputs, remove buttons, total amount and checkout button.
- Element IDs and types:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input number) - dynamic: id="update-quantity-{{ item.item_id }}"
  - remove-item-button-{item_id} (button) - dynamic: id="remove-item-button-{{ item.item_id }}"
  - proceed-checkout-button (button)
  - total-amount (div)
- Navigation Mappings:
  - proceed-checkout-button -> checkout

---

### templates/checkout.html
- Page Title: Checkout
- Layout Overview: Container form for user info input and order placement button.
- Element IDs and types:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (dropdown/select)
  - place-order-button (button)

---

### templates/active_orders.html
- Page Title: Active Orders
- Layout Overview: Container div listing active orders with status filter, track buttons and back to dashboard button.
- Element IDs and types:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button) - dynamic: id="track-order-button-{{ order.order_id }}"
  - status-filter (dropdown/select)
  - back-to-dashboard (button)
- Navigation Mappings:
  - track-order-button-{order_id} -> order_tracking (route parameter: order_id)
  - back-to-dashboard -> dashboard

---

### templates/order_tracking.html
- Page Title: Track Order
- Layout Overview: Container showing detailed order info, delivery driver info, item list, and back to orders button.
- Element IDs and types:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Navigation Mappings:
  - back-to-orders -> active_orders

---

### templates/reviews.html
- Page Title: Order Reviews
- Layout Overview: Container with list of reviews, filter by rating dropdown, write review button and back to dashboard button.
- Element IDs and types:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (dropdown/select)
  - back-to-dashboard (button)
- Navigation Mappings:
  - write-review-button -> write_review
  - back-to-dashboard -> dashboard

---

### templates/write_review.html
- Page Title: Write Review
- Layout Overview: Container form allowing user to select restaurant, enter customer name, rating and review text, and submit.
- Element IDs and types:
  - write-review-page (div)
  - restaurant-select (select) - dropdown to select restaurant by name
  - customer-name (input)
  - rating (dropdown/select) - options 1 to 5
  - review-text (textarea)
  - submit-review-button (button)
- Navigation Mappings:
  - No navigation buttons; form submit handled by POST on same route

---

## Section 3: Data Schemas

### data/restaurants.txt
- Fields (pipe-delimited):
  restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
- Purpose: Stores details about restaurants including location, rating, and delivery minimums.
- Data Types:
  - restaurant_id: int
  - name: string
  - cuisine: string
  - address: string
  - phone: string
  - rating: float
  - delivery_time: int (minutes)
  - min_order: float
- Example Rows:
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00

---

### data/menus.txt
- Fields (pipe-delimited):
  item_id|restaurant_id|item_name|category|description|price|availability
- Purpose: Contains menu items data linked to restaurants.
- Data Types:
  - item_id: int
  - restaurant_id: int
  - item_name: string
  - category: string
  - description: string
  - price: float
  - availability: int (0 or 1)
- Example Rows:
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1

---

### data/cart.txt
- Fields (pipe-delimited):
  cart_id|item_id|restaurant_id|quantity|added_date
- Purpose: Temporary storage for items added to shopping cart.
- Data Types:
  - cart_id: int
  - item_id: int
  - restaurant_id: int
  - quantity: int
  - added_date: date (YYYY-MM-DD)
- Example Rows:
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16

---

### data/orders.txt
- Fields (pipe-delimited):
  order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
- Purpose: Records finalized orders details.
- Data Types:
  - order_id: int
  - customer_name: string
  - restaurant_id: int
  - order_date: date (YYYY-MM-DD)
  - total_amount: float
  - status: string (e.g., "Delivered", "On the Way")
  - delivery_address: string
  - phone_number: string
- Example Rows:
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678

---

### data/order_items.txt
- Fields (pipe-delimited):
  order_item_id|order_id|item_id|quantity|price
- Purpose: Itemized list of ordered items per order.
- Data Types:
  - order_item_id: int
  - order_id: int
  - item_id: int
  - quantity: int
  - price: float
- Example Rows:
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99

---

### data/deliveries.txt
- Fields (pipe-delimited):
  delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
- Purpose: Delivery status and driver info for orders.
- Data Types:
  - delivery_id: int
  - order_id: int
  - driver_name: string
  - driver_phone: string
  - vehicle_info: string
  - status: string
  - estimated_time: datetime (YYYY-MM-DD HH:mm)
- Example Rows:
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30

---

### data/reviews.txt
- Fields (pipe-delimited):
  review_id|restaurant_id|customer_name|rating|review_text|review_date
- Purpose: Customer reviews of restaurants.
- Data Types:
  - review_id: int
  - restaurant_id: int
  - customer_name: string
  - rating: int (1-5)
  - review_text: string
  - review_date: date (YYYY-MM-DD)
- Example Rows:
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15

---

