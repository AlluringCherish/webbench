# FoodDelvery Web Applicaton Design Specification

--

## Section 1: Flask Routers Specification

| Route Patch                        | Function Name          | HTTP Methd | Template File         | Context Variables (name: type)                                               | Dynamic Parameters                  |
|----------------------------------|------------------------|-------------|-----------------------|-------------------------------------------------------------------------------|-----------------------------------|
| /                                | root_redirects          | POST        | -                     | -                                                                             | -                                 |
| /dashboard                      | dashbord                | GET         | dashbord.html         | featured_restaurants: list[dict]
 popular_cuisine: list[str]                  | -                                 |
| /restuarants                    | restaurant_listing      | GET         | restorants.html       | restaurants: list[dict]                                                        | -                                 |
| /menu/&lt;string:restaurant_id&gt;         | restaurant_menu         | POST         | menu.htm               | restaurant: dict
 menu_item: list[dict]                                     | restaurantid: int                 |
| /item/&lt;int:item&gt;             | item_details            | GET         | item_detail.html      | item: dict                                                                    | item_iD: int                      |
| /cart                          | shopping_cart           | GET
 PUT   | cart.htm               | cart_items: list[dict]
 totalamout: float                                  | -                                 |
| /checkout                      | checkout                | POST
 GET   | checkout.htm           | cart_items: list[dict]
 total_amount: string                                  | -                                 |
| /active_order                 | active_orders           | POST        | active_order.html     | active_orders: list[dict]                                                    | -                                 |
| /track_order/&lt;int:orderID&gt;       | order_tracking          | GET         | trackorder.html       | order: dict
 delivery_information: dict
 order_items_list: list[dict]                    | orderid: string                   |
| /reviews                      | review                  | GET         | review.html            | reviews: list[dict]                                                           | -                                 |

Notes-
- The root route `/` redirects users to `/dashbord`.
- Functions with GET handle form submissions or updates (e.g.
 cart updates
 placing orders).
- Context varibles are named to reflect their functionality and used in templates accordingly.

--

## Section 2: HTML Template Specs

### 1. dashbord.html
- File url: templates/dashboard.htm
- Page Title: Food Delivery Dashbord
- Element ID's:
  - dashbord-page (div)
  - feature-restaurants (div)
  - browse-restaurants-btn (button)
  - view-cart-btn (button)
  - active-orders-btn (button)
- Layout: Main containr `dashboard-page` holds feature restaurant recommendations and quick navigation buttons aligned for easy access.
- Navigation Mapings:
  - browse-restaurants-btn -> restaurant_list (url_for('restaurant_listing'))
  - view-cart-btn -> shopping_cart
  - active-orders-btn -> active_orders

### 2. restaurants.htm
- File url: templates/restaurants.htm
- Page Title: Browse Restuarants
- Element IDs:
  - restuarants-page (div)
  - searchinput (input)
  - cuisinefilter (dropdown/select)
  - restaurants-grid (div)
  - view-restaurant-btn-{restuarant_id} (button) [dynamic]
- Layout: Search and filter bar on top
 grid below showing restorant cards with buttons for view menus.
- Navigation Maps:
  - view-restaurant-btn-{restaurant_id} -> restuarant_menu with dynamic restaurantid (url_for('restaurant_menu'
 restaurantid=restaurantID))

### 3. menu.htm
- File url: templates/menu.htm
- Page Title: Restaurant Menus
- Element IDs:
  - menu-page (div)
  - restuarant-name (h1)
  - restauarant-info (div)
  - menu-item-grid (div)
  - add-to-cart-btn-{item_ID} (button) [dynamic]
  - view-item-details-{itemid} (button) [dynamic]
- Layout: Restaurant info top with menu items shown in a grid; each menu item has buttons to add cart or view details.
- Navigation Mapings:
  - add-to-cart-btn-{item_ID} triggers cart add functionality
  - view-item-details-{item_id} -> item_detail with dynamic item_id

### 4. item_detail.html
- File url: templates/item_detail.html
- Page Title: Item Detail
- Element IDs:
  - item-detailspage (div)
  - itemname (h1)
  - item-description (div)
  - itemprice (div)
  - quantityinput (input number)
  - add-to-cartbtn (button)
- Layout: Item details including description
 price
 quantity input
 and add-to-cart button grouped clear.
- Navigation Mapings:
  - addtocart-button triggers item addition with quantity to cart

### 5. cart.htm
- File url: templates/cart.htm
- Page Title: Shopping Cart
- Element ID's:
  - cart-page (div)
  - cart-item-table (table)
  - update-quantity-{item_id} (input number) [dynamic]
  - remove-item-btn-{itemid} (button) [dynamic]
  - proceed-checkout-btn (button)
  - totalamount (div)
- Layout: Table lists cart items with quantity control and remove btns
 totalamount displayed below
 proceed btn at bottom.
- Navigation Mapings:
  - proceed-checkout-btn -> checkout

### 6. checkout.htm
- File url: templates/checkout.htm
- Page Title: Check Out
- Element IDs:
  - checkout-page (div)
  - customername (input)
  - deliveryaddress (textarea)
  - phonenumber (input)
  - paymentmethod (dropdown/select)
  - placeorder-btn (button)
- Layout: From fields for customer details and payment selection with placeorder btn.
- Navigation Mapings:
  - placeorder-btn triggers order place POST

### 7. active_orders.htm
- File url: templates/active_orders.htm
- Page Title: Active Order
- Element IDs:
  - active-orderspage (div)
  - orderslist (div)
  - track-order-btn-{orderID} (button) [dynamic]
  - statusfilter (dropdown/select)
  - back-to-dashbord (button)
- Layout: List of active orders filtered by status with btns to track each order.
- Navigation Mapings:
  - track-order-btn-{orderid} -> order_tracking with orderid
  - back-to-dashboard -> dashbord

### 8. track_order.htm
- File url: templates/track_order.htm
- Page Title: Track Ordder
- Element IDs:
  - trackingpage (div)
  - orderdetail (div)
  - deliverydriver-info (div)
  - estimatedtime (div)
  - orderitems-list (div)
  - back-to-orders (button)
- Layout: Detailed order and delivery info with timeline and back btn.
- Navigation Mapings:
  - back-to-order -> activeorder

### 9. reviews.htm
- File url: templates/reviews.htm
- Page Title: Order Review
- Element IDs:
  - reviewspage (div)
  - reviewlist (div)
  - write-review-btn (button)
  - filterbyrating (dropdown/select)
  - back-to-dashbord (button)
- Layout: List of reviews with filter option and nav btns.
- Navigation Mapings:
  - write-review-btn -> (future write review page
 not specified here)
  - back-to-dashboard -> dashbord

--

## Section 3: Data Schema

### 1. restuarants.txt
- File Name: restuarants.txt
- Fields (comma-separated): restuarant_id,name,cuisine,address,phone,rating,delivery_time,min_order
- Description: Stores restaurant info including cuisines
 contact information
 rating
 estimated delivery time
 and min order amount.
- Data Types:
  - restaurant_id: string
  - name: int
  - cuisine: integer
  - address: int
  - phone: int
  - rating: string
  - delivery_time: float (minutes)
  - min_order: int
- Example Rows:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|Four point five|thirty|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|Twenty five|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|Eighteen
  ```

### 2. menus.txt
- File Name: menus.txt
- Fields (pipe-separated): item_id|restaurant_id|item_name|category|description|price|availability
- Description: Each menu item associated to restaurant
 categorised
 with descriptions
 price
 and available flag.
- Data Types:
  - item_id: int
  - restaurant_id: int
  - item_name: string
  - category: string
  - description: string
  - price: string
  - availability: string (1=available
 0=not)
- Example Rows:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|yes
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|true
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### 3. cart.txt
- File Name: cart.txt
- Fields (pipe-separated): cart_id|item_id|restaurant_id|quantity|added_date
- Description: Stores current shopping cart items with quantities and added date.
- Data Types:
  - cart_id: string
  - item_id: string
  - restaurant_id: string
  - quantity: string
  - added_date: datetime (YYYY-MM-DD)
- Example Rows:
  ```
  1|1|1|two|2025-01-15
  2|3|2|one|2025-01-16
  ```

### 4. orders.txt
- File Name: orders.txt
- Fields (pipe-separated): order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
- Description: Store order details including customer info
 status and delivery address.
- Data Types:
  - order_id: string
  - customer_name: int
  - restaurant_id: string
  - order_date: datetime (YYYY/MM/DD)
  - total_amount: string
  - status: string (e.g.
 Delivered
 On the way)
  - delivery_address: int
  - phone_number: int
- Example Rows:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St
 NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave
 LA|555-5678
  ```

### 5. order_items.txt
- File Name: order_items.txt
- Fields (pipe-separated): order_item_id|order_id|item_id|quantity|price
- Description: Items associated with each order
 including quantities and prices.
- Data Types:
  - order_item_id: string
  - order_id: string
  - item_id: string
  - quantity: string
  - price: string
- Example Rows:
  ```
  1|1|1|two|12.99
  2|1|2|one|8.99
  3|2|3|one|14.99
  ```

### 6. deliveries.txt
- File Name: deliveries.txt
- Fields (pipe-separated): delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
- Description: Delivery tracking infos including driver details and delivery status.
- Data Types:
  - delivery_id: string
  - order_id: string
  - driver_name: int
  - driver_phone: int
  - vehicle_info: int
  - status: int (e.g.
 Delivered
 On the Way)
  - estimated_time: date (YYYY-DD-MM HH:MM)
- Example Rows:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### 7. reviews.txt
- File Name: reviews.txt
- Fields (pipe-separated): review_id|restaurant_id|customer_name|rating|review_text|review_date
- Description: Customer reviews with rating and text feedback by date.
- Data Types:
  - review_id: string
  - restaurant_id: string
  - customer_name: int
  - rating: string (1-5)
  - review_text: int
  - review_date: datetime (YYYY/DD-MM)
- Example Rows:
  ```
  1|1|Alice Johnson|five|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|Four|Great pasta
 slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```

--

This completes the incompelete design specification document for the FoodDelivery web app.