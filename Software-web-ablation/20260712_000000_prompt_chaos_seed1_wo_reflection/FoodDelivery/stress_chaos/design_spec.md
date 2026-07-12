# FoodDelivery Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name           | HTTP Method | Template File           | Context Variables (Name: Type)                                                                                   | Dynamic Parameters                      |
|-------------------------------|------------------------|-------------|------------------------|---------------------------------------------------------------------------------------------------------------|--------------------------------------|
| /                             | root_redirect           | GET         | -                      | - Redirects to /dashboard                                                                                      | -                                    |
| /dashboard                    | dashboard_page          | GET         | dashboard.html          | featured_restaurants: list[dict], each with keys (restaurant_id:int, name:str, cuisine:str, rating:float)       | -                                    |
| /restaurants                  | restaurants_page        | GET         | restaurants.html        | restaurants: list[dict], each with (restaurant_id:int, name:str, cuisine:str, rating:float, delivery_time:int)  | -                                    |
| /menu/<int:restaurant_id>     | restaurant_menu_page    | GET         | menu.html               | restaurant: dict (restaurant_id:int, name:str, address:str, phone:str, rating:float, delivery_time:int)         |
|                               |                        |             |                        | menu_items: list[dict] with (item_id:int, item_name:str, category:str, description:str, price:float, availability:int) |                                       | 
| /item/<int:item_id>           | item_details_page       | GET         | item_details.html       | item: dict (item_id:int, item_name:str, description:str, price:float, ingredients:str optional)                 | item_id:int                         |
| /cart                        | shopping_cart_page      | GET         | cart.html               | cart_items: list[dict], each with (item_id:int, item_name:str, quantity:int, price:float, subtotal:float)       | -                                    |
| /cart/update                 | update_cart             | POST        | cart.html (redirect)    | -                                                                                                             | -                                    |
| /cart/remove/<int:item_id>   | remove_cart_item        | POST        | cart.html (redirect)    | -                                                                                                             | item_id:int                         |
| /checkout                    | checkout_page           | GET         | checkout.html           | -                                                                                                             | -                                    |
| /checkout/place_order        | place_order             | POST        | checkout.html (redirect) | -                                                                                                             | -                                    |
| /orders/active               | active_orders_page      | GET         | active_orders.html      | active_orders: list[dict], each with (order_id:int, restaurant:str, status:str, eta:str)                       | -                                    |
| /orders/track/<int:order_id> | order_tracking_page     | GET         | track_order.html        | order_details: dict (order_id:int, customer_name:str, restaurant_id:int, order_date:str, total_amount:float, status:str, delivery_address:str, phone_number:str) | order_id:int                        |
|                               |                        |             |                        | delivery_info: dict (driver_name:str, driver_phone:str, vehicle_info:str, status:str, estimated_time:str)        |
|                               |                        |             |                        | order_items: list[dict], each with (item_id:int, item_name:str, quantity:int, price:float)                     |                                      |
| /reviews                    | reviews_page            | GET         | reviews.html            | reviews: list[dict], each with (review_id:int, restaurant_name:str, customer_name:str, rating:int, review_text:str, review_date:str) | -                                    |
| /reviews/write              | write_review_page       | GET         | write_review.html       | restaurants: list[dict], each with (restaurant_id:int, name:str)                                               | -                                    |
| /reviews/submit             | submit_review           | POST        | reviews.html (redirect) | -                                                                                                             | -                                    |

---

## Section 2: HTML Template Specifications

### Template: dashboard.html
- File path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Layout Overview: Main container dividing featured restaurant recommendations and navigation buttons below
- Element IDs and Types:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Navigation Mappings:
  - browse-restaurants-button: url_for('restaurants_page')
  - view-cart-button: url_for('shopping_cart_page')
  - active-orders-button: url_for('active_orders_page')

---

### Template: restaurants.html
- File path: templates/restaurants.html
- Page Title: Browse Restaurants
- Layout Overview: Search and cuisine filter on top, grid listing restaurant cards below
- Element IDs and Types:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (dropdown/select)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button) (dynamic per restaurant)
- Navigation Mappings:
  - Each view-restaurant-button-{restaurant_id}: url_for('restaurant_menu_page', restaurant_id=restaurant_id)

---

### Template: menu.html
- File path: templates/menu.html
- Page Title: Restaurant Menu
- Layout Overview: Restaurant info and menu items grid with add/view buttons
- Element IDs and Types:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button) (dynamic per menu item)
  - view-item-details-{item_id} (button) (dynamic per menu item)
- Navigation Mappings:
  - add-to-cart-button-{item_id}: POST to add item to cart
  - view-item-details-{item_id}: url_for('item_details_page', item_id=item_id)

---

### Template: item_details.html
- File path: templates/item_details.html
- Page Title: Item Details
- Layout Overview: Display of detailed item description with quantity input and add button
- Element IDs and Types:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input, number)
  - add-to-cart-button (button)
- Navigation Mappings:
  - add-to-cart-button: POST to add item with quantity to cart

---

### Template: cart.html
- File path: templates/cart.html
- Page Title: Shopping Cart
- Layout Overview: Table of cart items with update quantity and remove buttons, total amount and checkout
- Element IDs and Types:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input, number) (dynamic per cart item)
  - remove-item-button-{item_id} (button) (dynamic per cart item)
  - proceed-checkout-button (button)
  - total-amount (div)
- Navigation Mappings:
  - proceed-checkout-button: url_for('checkout_page')

---

### Template: checkout.html
- File path: templates/checkout.html
- Page Title: Checkout
- Layout Overview: Form for customer details, address, phone, payment method, and place order button
- Element IDs and Types:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (dropdown/select)
  - place-order-button (button)
- Navigation Mappings:
  - place-order-button: POST to place order endpoint

---

### Template: active_orders.html
- File path: templates/active_orders.html
- Page Title: Active Orders
- Layout Overview: List of active orders with filter dropdown and tracking buttons
- Element IDs and Types:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button) (dynamic per order)
  - status-filter (dropdown/select)
  - back-to-dashboard (button)
- Navigation Mappings:
  - track-order-button-{order_id}: url_for('order_tracking_page', order_id=order_id)
  - back-to-dashboard: url_for('dashboard_page')

---

### Template: track_order.html
- File path: templates/track_order.html
- Page Title: Track Order
- Layout Overview: Detailed view showing order timeline and delivery driver info
- Element IDs and Types:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Navigation Mappings:
  - back-to-orders: url_for('active_orders_page')

---

### Template: reviews.html
- File path: templates/reviews.html
- Page Title: Order Reviews
- Layout Overview: List of reviews with rating filter and write review button
- Element IDs and Types:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (dropdown/select)
  - back-to-dashboard (button)
- Navigation Mappings:
  - write-review-button: url_for('write_review_page')
  - back-to-dashboard: url_for('dashboard_page')

---

### Template: write_review.html
- File path: templates/write_review.html
- Page Title: Write Review
- Layout Overview: Form to submit a review for a selected restaurant
- Element IDs and Types:
  - write-review-page (div)
  - restaurant-select (dropdown/select) - Select restaurant to review
  - customer-name-input (input)
  - rating-input (dropdown/select)
  - review-textarea (textarea)
  - submit-review-button (button)
- Navigation Mappings:
  - submit-review-button: POST to submit_review endpoint

---

## Section 3: Data Schemas

### restaurants.txt
- File name: restaurants.txt
- Field order and names:
  restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
- Description: Stores details of restaurants available in the system.
- Example rows:
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
- Field Data Types:
  restaurant_id: int
  name: string
  cuisine: string
  address: string
  phone: string
  rating: float
  delivery_time: int (minutes)
  min_order: float

---

### menus.txt
- File name: menus.txt
- Field order and names:
  item_id|restaurant_id|item_name|category|description|price|availability
- Description: Stores menu items for each restaurant.
- Example rows:
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
- Field Data Types:
  item_id: int
  restaurant_id: int
  item_name: string
  category: string
  description: string
  price: float
  availability: int (1=available, 0=not available)

---

### cart.txt
- File name: cart.txt
- Field order and names:
  cart_id|item_id|restaurant_id|quantity|added_date
- Description: Stores current cart items.
- Example rows:
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
- Field Data Types:
  cart_id: int
  item_id: int
  restaurant_id: int
  quantity: int
  added_date: date (YYYY-MM-DD)

---

### orders.txt
- File name: orders.txt
- Field order and names:
  order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
- Description: Stores placed orders.
- Example rows:
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
- Field Data Types:
  order_id: int
  customer_name: string
  restaurant_id: int
  order_date: date (YYYY-MM-DD)
  total_amount: float
  status: string
  delivery_address: string
  phone_number: string

---

### order_items.txt
- File name: order_items.txt
- Field order and names:
  order_item_id|order_id|item_id|quantity|price
- Description: Stores items included in each order.
- Example rows:
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
- Field Data Types:
  order_item_id: int
  order_id: int
  item_id: int
  quantity: int
  price: float

---

### deliveries.txt
- File name: deliveries.txt
- Field order and names:
  delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
- Description: Stores delivery details for orders.
- Example rows:
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
- Field Data Types:
  delivery_id: int
  order_id: int
  driver_name: string
  driver_phone: string
  vehicle_info: string
  status: string
  estimated_time: string (YYYY-MM-DD HH:MM)

---

### reviews.txt
- File name: reviews.txt
- Field order and names:
  review_id|restaurant_id|customer_name|rating|review_text|review_date
- Description: Stores customer reviews for restaurants.
- Example rows:
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
- Field Data Types:
  review_id: int
  restaurant_id: int
  customer_name: string
  rating: int (1-5)
  review_text: string
  review_date: date (YYYY-MM-DD)

---

# End of Design Specification
