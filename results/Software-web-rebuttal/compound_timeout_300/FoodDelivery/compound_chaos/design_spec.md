# FoodDelivery Web Application - Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name           | HTTP Method(s) | Template File           | Context Variables (name : type)                                                                                                                                                  | Dynamic Parameters       |
|--------------------------------|-------------------------|----------------|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| /                              | root_redirect            | GET            | N/A (redirect)           | None                                                                                                                                                                            | None                     |
| /dashboard                     | dashboard_page           | GET            | dashboard.html           | featured_restaurants : list[dict], popular_cuisines : list[str]                                                                                                                  | None                     |
| /restaurants                   | browse_restaurants       | GET            | restaurants.html         | restaurants : list[dict] (fields: restaurant_id:int, name:str, cuisine:str, address:str, phone:str, rating:float, delivery_time:int, min_order:float),
cuisines : list[str]      | None                     |
| /menu/<int:restaurant_id>      | restaurant_menu          | GET            | menu.html                | restaurant : dict (restaurant_id:int, name:str, cuisine:str, address:str, phone:str, rating:float, delivery_time:int, min_order:float),
menu_items : list[dict] (fields: item_id:int, restaurant_id:int, item_name:str, category:str, description:str, price:float, availability:int) | restaurant_id:int          |
| /item/<int:item_id>             | item_details             | GET            | item_details.html        | item : dict (item_id:int, restaurant_id:int, item_name:str, category:str, description:str, price:float, availability:int),
quantity_default : int (usually 1)                                                                        | item_id:int               |
| /cart                         | shopping_cart            | GET, POST      | cart.html                | cart_items : list[dict] (item_id:int, item_name:str, quantity:int, price:float, subtotal:float),
total_amount : float                                                                                                    | None                     |
| /checkout                     | checkout                 | GET, POST      | checkout.html            | None (GET to display),
 on POST, form data: customer_name:str, delivery_address:str, phone_number:str, payment_method:str                                                                | None                     |
| /orders/active                | active_orders            | GET            | active_orders.html       | active_orders : list[dict] (order_id:int, restaurant_name:str, status:str, eta:str)                                                                                                  | None                     |
| /order/track/<int:order_id>    | order_tracking           | GET            | track_order.html         | order_details : dict (order_id:int, customer_name:str, restaurant_id:int, order_date:str, total_amount:float, status:str, delivery_address:str, phone_number:str),
delivery_info : dict (driver_name:str, driver_phone:str, vehicle_info:str),
estimated_time : str,
order_items : list[dict] (item_name:str, quantity:int, price:float)                  | order_id:int              |
| /reviews                     | reviews_page             | GET            | reviews.html             | reviews : list[dict] (review_id:int, restaurant_id:int, customer_name:str, rating:int, review_text:str, review_date:str),
filter_ratings : list[str] ('All', '5 stars', '4 stars', etc.)                                                  | None                     |
| /reviews/write               | write_review             | GET, POST      | write_review.html        | None (GET to display),
on POST, form data: restaurant_id:int, customer_name:str, rating:int, review_text:str                                                                      | None                     |


---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- File Path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Layout Overview: Main hub page with featured restaurants and quick navigation buttons.
- Element IDs:
  - dashboard-page (div)
  - featured-restaurants (div)
  - browse-restaurants-button (button)
  - view-cart-button (button)
  - active-orders-button (button)
- Navigation Mappings:
  - browse-restaurants-button → browse_restaurants (url_for('browse_restaurants'))
  - view-cart-button → shopping_cart (url_for('shopping_cart'))
  - active-orders-button → active_orders (url_for('active_orders'))

### 2. restaurants.html
- File Path: templates/restaurants.html
- Page Title: Browse Restaurants
- Layout Overview: Page with search input, cuisine filter dropdown, and grid of restaurants with buttons to view each menu.
- Element IDs:
  - restaurants-page (div)
  - search-input (input)
  - cuisine-filter (select dropdown)
  - restaurants-grid (div)
  - view-restaurant-button-{restaurant_id} (button) - dynamic, one per restaurant
- Navigation Mappings:
  - Each view-restaurant-button-{restaurant_id} → restaurant_menu (url_for('restaurant_menu', restaurant_id=restaurant_id))

### 3. menu.html
- File Path: templates/menu.html
- Page Title: Restaurant Menu
- Layout Overview: Displays restaurant details and menu items in a grid with buttons to add items to cart or view details.
- Element IDs:
  - menu-page (div)
  - restaurant-name (h1)
  - restaurant-info (div)
  - menu-items-grid (div)
  - add-to-cart-button-{item_id} (button) - dynamic, per menu item
  - view-item-details-{item_id} (button) - dynamic, per menu item
- Navigation Mappings:
  - add-to-cart-button-{item_id} triggers backend add to cart (via POST or AJAX, not a navigation link)
  - view-item-details-{item_id} → item_details (url_for('item_details', item_id=item_id))

### 4. item_details.html
- File Path: templates/item_details.html
- Page Title: Item Details
- Layout Overview: Detailed view of a menu item showing name, description, price, quantity input, and add to cart button.
- Element IDs:
  - item-details-page (div)
  - item-name (h1)
  - item-description (div)
  - item-price (div)
  - quantity-input (input number)
  - add-to-cart-button (button)
- Navigation Mappings:
  - add-to-cart-button triggers add to cart action (POST)

### 5. cart.html
- File Path: templates/cart.html
- Page Title: Shopping Cart
- Layout Overview: Table listing cart items with quantity inputs and remove buttons, plus total amount and checkout button.
- Element IDs:
  - cart-page (div)
  - cart-items-table (table)
  - update-quantity-{item_id} (input number) - dynamic per cart item
  - remove-item-button-{item_id} (button) - dynamic per cart item
  - proceed-checkout-button (button)
  - total-amount (div)
- Navigation Mappings:
  - proceed-checkout-button → checkout (url_for('checkout'))

### 6. checkout.html
- File Path: templates/checkout.html
- Page Title: Checkout
- Layout Overview: Form for customer delivery and payment details with place order button.
- Element IDs:
  - checkout-page (div)
  - customer-name (input)
  - delivery-address (textarea)
  - phone-number (input)
  - payment-method (select dropdown)
  - place-order-button (button)
- Navigation Mappings:
  - place-order-button submits checkout form (POST)

### 7. active_orders.html
- File Path: templates/active_orders.html
- Page Title: Active Orders
- Layout Overview: List of active orders with filter dropdown, each with track order button, plus back to dashboard.
- Element IDs:
  - active-orders-page (div)
  - orders-list (div)
  - track-order-button-{order_id} (button) - dynamic per order
  - status-filter (select dropdown)
  - back-to-dashboard (button)
- Navigation Mappings:
  - track-order-button-{order_id} → order_tracking (url_for('order_tracking', order_id=order_id))
  - back-to-dashboard → dashboard_page (url_for('dashboard_page'))

### 8. track_order.html
- File Path: templates/track_order.html
- Page Title: Track Order
- Layout Overview: Detailed tracking info with delivery driver details, order items list, and back to active orders button.
- Element IDs:
  - tracking-page (div)
  - order-details (div)
  - delivery-driver-info (div)
  - estimated-time (div)
  - order-items-list (div)
  - back-to-orders (button)
- Navigation Mappings:
  - back-to-orders → active_orders (url_for('active_orders'))

### 9. reviews.html
- File Path: templates/reviews.html
- Page Title: Order Reviews
- Layout Overview: List of reviews with filter dropdown and button to write new review.
- Element IDs:
  - reviews-page (div)
  - reviews-list (div)
  - write-review-button (button)
  - filter-by-rating (select dropdown)
  - back-to-dashboard (button)
- Navigation Mappings:
  - write-review-button → write_review (url_for('write_review'))
  - back-to-dashboard → dashboard_page (url_for('dashboard_page'))

---

## Section 3: Data Schemas

### 1. restaurants.txt
- Purpose: Stores restaurant information including contact and delivery details.
- Field Order (pipe-separated):
  restaurant_id | name | cuisine | address | phone | rating | delivery_time | min_order
- Field Types:
  - restaurant_id: int
  - name: string
  - cuisine: string
  - address: string
  - phone: string
  - rating: float
  - delivery_time: int (minutes)
  - min_order: float (dollar amount)
- Example Rows:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

### 2. menus.txt
- Purpose: Contains menu items for restaurants.
- Field Order (pipe-separated):
  item_id | restaurant_id | item_name | category | description | price | availability
- Field Types:
  - item_id: int
  - restaurant_id: int
  - item_name: string
  - category: string
  - description: string
  - price: float
  - availability: int (1 = available, 0 = not available)
- Example Rows:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### 3. cart.txt
- Purpose: Stores current shopping cart items.
- Field Order (pipe-separated):
  cart_id | item_id | restaurant_id | quantity | added_date
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
- Purpose: Stores completed and active orders.
- Field Order (pipe-separated):
  order_id | customer_name | restaurant_id | order_date | total_amount | status | delivery_address | phone_number
- Field Types:
  - order_id: int
  - customer_name: string
  - restaurant_id: int
  - order_date: date (YYYY-MM-DD)
  - total_amount: float
  - status: string (e.g. 'Preparing', 'On the Way', 'Delivered')
  - delivery_address: string
  - phone_number: string
- Example Rows:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

### 5. order_items.txt
- Purpose: Stores items linked to orders.
- Field Order (pipe-separated):
  order_item_id | order_id | item_id | quantity | price
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
- Purpose: Stores delivery and driver details per order.
- Field Order (pipe-separated):
  delivery_id | order_id | driver_name | driver_phone | vehicle_info | status | estimated_time
- Field Types:
  - delivery_id: int
  - order_id: int
  - driver_name: string
  - driver_phone: string
  - vehicle_info: string
  - status: string (e.g. 'Preparing', 'On the Way', 'Delivered')
  - estimated_time: datetime (YYYY-MM-DD HH:MM)
- Example Rows:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### 7. reviews.txt
- Purpose: Stores customer reviews for restaurants.
- Field Order (pipe-separated):
  review_id | restaurant_id | customer_name | rating | review_text | review_date
- Field Types:
  - review_id: int
  - restaurant_id: int
  - customer_name: string
  - rating: int (1 to 5)
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
