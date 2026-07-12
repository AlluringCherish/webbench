

---

## 1:

Route Path Function | Method | Template File Dynamic Route Params
|--------------------------------|-----------------------|-------------|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
/ | | GET (redirect)
dashboard | GET dashboard.html of dict fields: (str), (float), |
| | | restaurants of restaurant_id (int), (str), cuisine (float),
| | GET (int), name (str), address (str), rating
item_id (int), category (str), (float), restaurant_id |
| /item/&lt;int:item_id&gt; item_details | item_details.html | menu_item (dict): (str), description (str) item_id (int)
| | | | None | (int)
| | | cart_items of (int), (str), quantity (float),
total_amount
(redirect) None | None
| remove_cart_item (redirect) | |
| checkout.html None None
| (redirect) | | |
| active_orders | orders (list of dict): (int), status | |
/orders/&lt;int:order_id&gt;/track | GET | (dict): order_id (int), (str), restaurant_id (int), order_date total_amount (float), status (str),
driver_phone vehicle_info
(list of item_id item_name (float) |
reviews_page GET | reviews.html (list (int), restaurant_name customer_name rating (int), review_text (str), |
| /reviews/write | N/A (redirect) None None |



## Template Specifications


- templates/dashboard.html
- Page Delivery
- Main featured quick action buttons navigation.
- Element
- dashboard-page
featured-restaurants (div)
-
-
(button)


- (route:
- active-orders-button url_for('active_orders') /orders)

###
- File path:
Page Title: Browse
- Layout Overview: and a
& Types:
-

cuisine-filter (dropdown/select)
restaurants-grid (div)
restaurant)
-
view-restaurant-button-{restaurant_id} restaurant_id=restaurant_id)

menu.html
path:
- Page Title: Restaurant Menu
- Displays restaurant information respective action
- &
menu-page
restaurant-name
-
menu-items-grid
dynamic)
- (button, dynamic)
mappings:
to url_for('add_item_to_cart',
- view-item-details-{item_id}

item_details.html
- File
- Page Title: Item Details
Overview: Detailed item information page with quantity cart
- Element Types:
- (div)

- (div)
-
- (input
add-to-cart-button
Navigation
- url_for('add_item_to_cart',

cart.html
- File

cart and total and checkout button.
Element
- (div)
- cart-items-table
- update-quantity-{item_id} (input
dynamic)
proceed-checkout-button
(div)
mappings:
proceed-checkout-button (route: /checkout)


File
Page
for capturing customer payment with place
- IDs
- (div)
- customer-name
- (textarea)
-
payment-method (dropdown/select)
-
- mappings:
- place-order-button POST /checkout/place_order)

###
- File path:
- Active Orders
Layout current with status each order
- IDs
- (div)
orders-list
-
status-filter
(button)
- Navigation
track-order-button-{order_id}




Order
Overview: order tracking
IDs &

- order-details
- (div)

(div)

-
- url_for('active_orders')

reviews.html
File
- Title: Order
write a new
- Element &
reviews-page
(div)
- (button)

- back-to-dashboard (button)

- url_for('write_review')




3: Schemas


Name: restaurants.txt
- Field order:
- restaurants with key details as contact

restaurant_id:
- name:
cuisine: string
address: string
- phone:
- rating:
(minutes)
- float
-
-
- Bella Italia|Italian|456
- Elm St|555-0003|4.6|35|18.00


menus.txt

Purpose: availability.
Types:
item_id:
int
- item_name:
- string

- price:
(1=available,
-
Rice|Main egg|12.99|1
2|1|Spring rolls with filling|8.99|1
Carbonara|Pasta|Classic pasta sauce|14.99|1

3. cart.txt
File Name:
Field cart_id|item_id|restaurant_id|quantity|added_date
- cart
Types:
cart_id: int
- item_id:
restaurant_id: int
quantity: int
-
Example
-
-

### orders.txt
File
Field order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
Purpose: Stores details.

-
-
- restaurant_id: int
-
-
-
-

- Example
St,
Smith|2|2025-01-14|14.99|On Way|456 Ave,

### 5. order_items.txt
- File Name:
- Field order_item_id|order_id|item_id|quantity|price
of items in order.

- order_item_id: int



price:
Example
1|1|1|2|12.99
- 2|1|2|1|8.99
- 3|2|3|1|14.99


File Name:
- Field order: delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
Delivery and info.
Data
delivery_id:
int
- driver_name: string
- driver_phone:

-
estimated_time: datetime (YYYY-MM-DD
Example
1|1|Mike
2|2|Sarah the 19:30


- reviews.txt
- order: review_id|restaurant_id|customer_name|rating|review_text|review_date
ratings restaurants.
Data Types:
review_id:
restaurant_id:

(1
-

- Example rows:
- Johnson|5|Excellent fast delivery!|2025-01-12
delayed delivery.|2025-01-13
3|3|Charlie Brown|5|Best food



Specification
