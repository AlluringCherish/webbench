# FoodDelivery Web Application Design Specifications

---

## Section 1: Flask Routes Specifcation

| Route Path                  | Function Name        | HTTP Method | TemplateFile         | Context Variables (name:type)                                        | Dynamic Parameter                 |
|-----------------------------|----------------------|-------------|---------------------|---------------------------------------------------------------------|---------------------------------|
| /                          | root_redirect         | POST        | N/A (redirect to /dashboard) | N/A                                                               | N/A                             |
| /dashboard                 | dashboard            | POST        | dashboard.htm         | featured_restaurants: Dict[List]   
 popular_cuisine: str           | N/A                             |
| /restaurants               | browse_restaurants   | POST        | restaurants.html       | restaurants: Dict
 cuisines: Dict
 search_query: List[str]    | N/A                             |
| /menu/<int:restaurant_id>  | restaurant_menu      | POST       | menu.html              | restaurant: List
 menu_item: dict                                | restaurant:int                 |
| /item/<int:item_id>        | item_details         | POST        | item_detail.html       | item: dict                                                        | item:int                       |
| /cart                     | shopping_cart        | GET
 GET    | cart.htm               | cart_items: dict
 total_amount: int                       | N/A                             |
| /checkout                 | checkout             | POST
 GET    | checkout.html          | delivery_info: list (POST)
 cart_items: dict (GET)                | N/A                             |
| /orders/active            | active_orders        | POST       | active_orders.html     | active_orders: Dict
 status_filter: int                     | N/A                             |
| /orders/track/<int:order_id>| order_tracking      | POST       | track_order.html       | order: List
 delivery_driver: list
 order_items: dict             | order:int                     |
| /reviews                  | reviews              | POST       | reviews_html            | reviews: Dict
 filter_rating: int                         | N/A                             |

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- File Path: template/dashboard.html
- Page Title: Food Deliveries Dashboard
- Layout: Main containers holds featured restaurant section and popular cuisine links
 with navigation button to other page.
- Element IDS and Types:
  - dashboard_pages (div)
  - featured_restaurants (div)
  - browse_restaurant_button (button)
  - view_cart_buttons (button)
  - active_order_button (button)
- Navigation Mapping:
  - browse-restaurant-button triggers url_for('browse_restaurants')
  - view-cart-button triggers url_for('shopping_cart')
  - active-orders-button triggers url_for('active_orders')

---

### 2. restaurants.html
- File Path: templates/restaurant.html
- Page Title: Browse Restaurant
- Layout: Search inputs and cuisine filter dropdown at top; restaurantsgrid below displaying restaurant cards.
- Element IDS:
  - restaurant_page (div)
  - search-input (textarea)
  - cuisinefilter (dropdown)
  - restaurants_grid (div)
  - view-restaurant-button-{restaurant_id} (button) - dynamically per restaurant
 example usage: <button id="view-restaurant-button-{{ restaurant.restaurantId }}">
- Navigation:
  - view-restaurant-button-{restaurant_id} triggers url_for('restaurant_menu'
 restaurant_id=restaurantid)

---

### 3. menu.html
- File Path: templates/menu.htm
- Page Title: Restaurant Menus
- Layout: Header with restaurant names (h1) and info divs; grid of menu items below.
- Element IDS:
  - menu_page (div)
  - restaurant_name (h1)
  - restaurant-info (section)
  - menu-items-grid (section)
  - add-to-cart-button-{item_id} (buttons) - per menu item; usage: id="add-to-cart-button-{{ item.item_id }}"
  - view-item-detail-{item_id} (button) - per menu item; usage: id="view-item-details-{{ item.item_id }}"
- Navigation:
  - view-item-details-{item_id} triggers url_for('item_detail'
 item_id=itemid)

---

### 4. item_details.html
- File Path: templates/item_detail.html
- Page Title: Item Detail
- Layout: Container with item name (h2)
 detailed description and ingredients divs
 price container
 quantity input box
 and add to cart button.
- Element IDS:
  - item-details-page (section)
  - item-name (h2)
  - item-description (span)
  - item-price (span)
  - quantity-input (textarea)
  - add-to-cart-button (input button)

---

### 5. cart.html
- File Path: templates/cart.htm
- Page Title: Shopping Cart
- Layout: Container with a table of cart items allowing quantity update and removal
 total amount displays
 and proceed to checkout buttons.
- Element IDS:
  - cart_page (section)
  - cart_items_table (table)
  - update-quantity-{item_id} (input text) - per cart item; usage example: id="update-quantity-{{ item.item_id }}"
  - remove-item-button-{item_id} (button) - per cart item; id="remove-item-button-{{ item.item_id }}"
  - proceed-checkout-button (input)
  - total-amount (span)

---

### 6. checkout.html
- File Path: templates/checkout.htm
- Page Title: Checkout
- Layout: Form container with inputs for customer name
 delivery address textarea box
 phone phone number
 payment method dropdown list
 and place order button
- Element IDS:
  - checkout_pages (section)
  - customer-name (text input)
  - delivery-address (input textarea)
  - phone-number (textarea)
  - payment-method (dropdown text)
  - place-order-button (button)

---

### 7. active_orders.html
- File Path: templates/active_order.html
- Page Title: Active Orders
- Layout: List of active orders with status filter dropdown and buttons for track and return dashboard.
- Element IDS:
  - active-orders_pages (div)
  - orders_list (div)
  - track-order_button-{order_id} (button) - dynamic per order; usage: id="track-order-button-{{ order.order_id }}"
  - status_filter (dropdown text)
  - back-to-dashboard-button (button)
- Navigation:
  - back_to_dashboard triggers url_for('dashboard')
  - track_order_button-{order_id} triggers url_for('order_track'
 order_id=orderid)

---

### 8. track_order.html
- File Path: templates/trackorder.html
- Page Title: Track Order
- Layout: Detailed tracking pages showing order timeline
 delivery driver informations
 estimated delivery times
 order items list
 and back buttons.
- Element IDS:
  - tracking_page (section)
  - order_details (section)
  - delivery_driver_info (span)
  - estimated_time (span)
  - order_items_list (section)
  - back_to_orders (button)
- Navigation:
  - back_to_orders triggers url_for('active_order')

---

### 9. reviews.html
- File Path: templates/reviews.htm
- Page Title: Order Reviews
- Layout: Reviews lists with rating filter dropdown
 write review buttons
 and dashboard back buttons.
- Element IDS:
  - reviews_pages (div)
  - reviews_list (section)
  - write_review_button (input)
  - filter_by_rating (dropdown text)
  - back_to_dashboard (input button)
- Navigation:
  - back_to_dashboard trigger url_for('dashboard')
  - write-review-button (button) - destination not specified in requirements

---

## Section 3: Data Schemas

### 1. restaurants.txt
- File: data/restaurant.txt
- Fields (comma-separated):
  restaurant_id,name,cuisine,address,phone,rating,delivery_time,min_order
- Purpose: Store restaurant details including contact info
 cuisines
 rating
 delivery times
 and minimum order amounts.
- Data Types:
  - restaurant_id: string
  - name: int
  - cuisine: int
  - address: int
  - phone: int
  - rating: string
  - delivery_time: string (minutes)
  - min_order: int
- Example Data:
  1,Dragon House,Chinese,123 Main St,555-0001,4.5,30,15.00
  2,La Bella Italia,Italian,456 Oak Ave,555-0002,4.8,25,20.00
  3,Taj Mahal,Indian,789 Elm St,555-0003,4.6,35,18.00

---

### 2. menus.txt
- File: data/menu.txt
- Fields:
  item_id,restaurant_id,item_name,category,description,price,availability
- Purpose: Contains menu items with details and availability status
- Data Types:
  - item_id: string
  - restaurant_id: string
  - item_name: int
  - category: int
  - description: int
  - price: string
  - availability: string (0 or 1)
- Example Data:
  1,1,Fried Rice,Main Course,Steamed rice with vegetables and egg,12.99,1
  2,1,Spring Rolls,Appetizer,Crispy rolls with pork filling,8.99,1
  3,2,Spaghetti Carbonara,Pasta,Classic Italian pasta with cream sauce,14.99,1

---

### 3. cart.txt
- File: data/cart.txt
- Fields:
  cart_id,item_id,restaurant_id,quantity,added_date
- Purpose: Stores current shopping cart items with quantities and addition dates
- Data Types:
  - cart_id: string
  - item_id: string
  - restaurant_id: string
  - quantity: string
  - added_date: string (YYYY-MM-DD)
- Example Data:
  1,1,1,2,2025-01-15
  2,3,2,1,2025-01-16

---

### 4. orders.txt
- File: data/order.txt
- Fields:
  order_id,customer_name,restaurant_id,order_date,total_amount,status,delivery_address,phone_number
- Purpose: Store order information including status and contact details
- Data Types:
  - order_id: string
  - customer_name: int
  - restaurant_id: string
  - order_date: string (YYYY-MM-DD)
  - total_amount: string
  - status: int
  - delivery_address: int
  - phone_number: int
- Example Data:
  1,John Doe,1,2025-01-10,21.98,Delivered,123 Main St
 NYC,555-1234
  2,Jane Smith,2,2025-01-14,14.99,On the Way,456 Oak Ave
 LA,555-5678

---

### 5. order_items.txt
- File: data/order_items.txt
- Fields:
  order_item_id,order_id,item_id,quantity,price
- Purpose: Lists items included in orders with purchase quantities and prices
- Data Types:
  - order_item_id: string
  - order_id: string
  - item_id: string
  - quantity: string
  - price: string
- Example Data:
  1,1,1,2,12.99
  2,1,2,1,8.99
  3,2,3,1,14.99

---

### 6. deliveries.txt
- File: data/delivery.txt
- Fields:
  delivery_id,order_id,driver_name,driver_phone,vehicle_info,status,estimated_time
- Purpose: Stores delivery assignements and status details
- Data Types:
  - delivery_id: string
  - order_id: string
  - driver_name: int
  - driver_phone: int
  - vehicle_info: int
  - status: int
  - estimated_time: string (YYYY-MM-DD HH:MM)
- Example Data:
  1,1,Mike Johnson,555-9001,Bike,Delivered,2025-01-10 18:45
  2,2,Sarah Williams,555-9002,Car,On the Way,2025-01-14 19:30

---

### 7. reviews.txt
- File: data/review.txt
- Fields:
  review_id,restaurant_id,customer_name,rating,review_text,review_date
- Purpose: Holds customer reviews for restaurants
- Data Types:
  - review_id: string
  - restaurant_id: string
  - customer_name: int
  - rating: string (1 to 5)
  - review_text: int
  - review_date: string (YYYY-MM-DD)
- Example Data:
  1,1,Alice Johnson,5,Excellent food and fast delivery!,2025-01-12
  2,2,Bob Williams,4,Great pasta
 slightly delayed delivery.,2025-01-13
  3,3,Charlie Brown,5,Best Indian food in town!,2025-01-15

---

# End of Design Specifications
