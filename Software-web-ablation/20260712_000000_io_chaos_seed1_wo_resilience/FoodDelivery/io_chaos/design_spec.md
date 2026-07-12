# FoodDelivery Web Application Design Specfication

--

## Section 1 Flask Routes Specification

| Route Path                         | Function Name          | HTTP Method  | Tempalte File           | Context Variables name: type                                         | Dynamic Parameter              |
|----------------------------------|------------------------|-------------|------------------------|----------------------------------------------------------------------|-------------------------------|
| /                                | root_redirect          | POST         | N/A (Redirect to /dashboard) | N/A                                                                  | N/A                           |
| /dashboard                      | dashboard              | POST        | dashboards.html          | featured_restaurants: dict
 popular_cuisines list[str]           | N/A                           |
| /restaurants                   | restaurants_listing     | POST        | restaurants.html          | restaurants: dict
 cuisines: set[str]                       | N/A                           |
| /menu/<int:restaurantid>       | restaurant_menu        | GET         | menu.html                | restaurant: list
 menu_items list[dict]                        | restaurantId int               |
| /item/<string:item_id>          | item_details           | POST        | item_detail.html         | item: dict                                                           | item_id: str                   |
| /cart                         | shopping_cart          | POST        | cart.hmtl                | cart_items dict
 total_amount str                         | N/A                           |
| /cart/update                  | update_cart            | GET         | N/A                     | N/A                                                                  | N/A                           |
| /checkout                     | checkout               | GET
 GET   | checkout.html          | (GET) order_confirmation: dict
 (POST) None                           | N/A                           |
| /orders/active                | active_orders          | POST        | active_orders.html       | active_orders dict
 status_filter_options set[str]         | N/A                           |
| /order/track/<int:order_id>   | order_tracking         | POST        | track_order.html         | order_details list
 delivery_driver list
 order_items dict  | order_id: string               |
| /reviews                     | reviews_page           | POST        | reviews.html             | reviews dict
 rating_filter_options list[str]               | N/A                           |
| /reviews/write               | write_review           | POST
 GET   | write_review.html      | (GET) review_submission_status: bool
 (POST) None                           | N/A                           |

--

## Section Two: HTML Template Specifications

### 1- dashboard.html
- File Path: templates/dashboard.htm
- Page Title: Food Delivery DashBoard
- Element IDS and Types:
  - dashboard_page (div)
  - featured_restaurants (div)
  - browse_restaurants_button (button)
  - view_cart_button (button)
  - active_orders_button (button)
- Layout Overview: Main home page with sections featured restaurants & popular cuisines; quick navigation buttons at bottom.
- Navigation Mappings:
  - browse_restaurants_button -> restaurants_listings
  - view_cart_button -> shopping_cart
  - active_orders_button -> active_orders

### 2 restaurants.html
- File Path: templates/restuarants.html
- Page Title: Browse Restaurant
- Element IDS and Types:
  - restaurants-page (div)
  - search_input (input)
  - cuisine_filter (dropdown/select)
  - restaurants_grid (div)
  - view_restaurant_button_{restaurantid} (button
 dynamic with restaurantid)
- Layout Overview: Search & filter inputs at bottom; grid displaying clickable restaurant cards.
- Navigation Mappings:
  - view_restaurant_button_{restaurantid} -> restaurant_menu (requires restaurantId)

### 3 menu.html
- File Path: templates/menu.htm
- Page Title: Restaurant menus
- Element IDS and Types:
  - menu_page (div)
  - restaurant_name (h1)
  - restaurant_info (div)
  - menu_items_grid (div)
  - add_to_cart_button_{itemid} (button
 dynamic with itemid)
  - view_item_details_{itemid} (button
 dynamic with itemid)
- Layout Overview: Restaurant info at bottom; grid of menu items with add and detail buttons.
- Navigation Mappings:
  - add_to_cart_button_{itemid} -> Function call (AJAX/GET to add item to cart)
  - view_item_details_{itemid} -> item_details (requires itemid)

### 4 item_details.html
- File Path: templates/item_details.htm
- Page Title: Item detail
- Element IDS and Types:
  - item_details_page (div)
  - item_name (h1)
  - item_description (div)
  - item-price (div)
  - quantity_input (input
 text)
  - add_to_cart_button (button)
- Layout Overview: Detailed item info with quantity input & add to cart button.
- Navigation Mappings:
  - add_to_cart_button -> Function call (GET to add item with quantity)

### 5 cart.html
- File Path: templates/cart.htm
- Page Title: Shoping Cart
- Element IDS and Types:
  - cart_page (div)
  - cart_items_table (table)
  - update_quantity_{itemid} (input
 text
 dynamic with itemid)
  - remove_item_button_{itemid} (button
 dynamic with itemid)
  - proceed_checkout_button (button)
  - total_amount (span)
- Layout Overview: Tabular cart listing with quantity update and remove buttons; total amount & checkout button below.
- Navigation Mappings:
  - proceed_checkout_button -> checkout

### 6 checkout.html
- File Path: templates/checkout.htm
- Page Title: Checkout
- Element IDS and Types:
  - checkout_page (div)
  - customer_name (input)
  - delivery_address (textarea)
  - phone_number (input)
  - payment_method (dropdown/select)
  - place_order_button (button)
- Layout Overview: Form to fill delivery & payment info with submit button.
- Navigation Mappings:
  - place_order_button -> checkout (GET to place order)

### 7 active_orders.html
- File Path: templates/active_orders.htm
- Page Title: Active Order
- Element IDS and Types:
  - active_orders_page (div)
  - orders_list (div)
  - track_order_button_{orderid} (button
 dynamic with orderid)
  - status_filter (dropdown/select)
  - back_to_dashboard (button)
- Layout Overview: List of active orders with filtering
 track buttons
 and back buttons.
- Navigation Mappings:
  - track_order_button_{orderid} -> order_tracking (requires orderid)
  - back_to_dashboard -> dashboard

### 8 track_order.html
- File Path: templates/track_order.htm
- Page Title: Track Orders
- Element IDS and Types:
  - tracking_page (div)
  - order_details (div)
  - delivery_driver_info (div)
  - estimated_time (span)
  - order_items_list (div)
  - back_to_orders (button)
- Layout Overview: Detailed tracking details with delivery driver details and back button.
- Navigation Mappings:
  - back_to_orders -> active_orders

### 9 reviews.html
- File Path: templates/reviews.htm
- Page Title: Order Reviews
- Element IDS and Types:
  - reviews_page (div)
  - reviews_list (div)
  - write_review_button (button)
  - filter_by_rating (dropdown/select)
  - back_to_dashboard (button)
- Layout Overview: List of reviews with filter & navigation buttons.
- Navigation Mappings:
  - write_review_button -> write_review
  - back_to_dashboard -> dashboard

### 10 write_review.html
- File Path: templates/write_review.htm
- Page Title: Write a Review
- Element IDS and Types:
  - write_review_page (div)
  - restaurant_select (dropdown/select)
  - customer_name_input (input)
  - rating_select (dropdown/select)
  - review_text_area (textarea)
  - submit_review_button (button)
- Layout Overview: Form to enter review details and submit.
- Navigation Mappings:
  - submit_review_button -> write_review (GET to submit review)

--

## Section 3 Data Schemas

### 1 restaurants.txt
- Fields (comma-delimited):
  restaurant_id,name,cuisine,address,phone,rating,delivery_time,min_order
- Purpose: Stores details about each restaurant including contact
 cuisine type,
 rating,
 and delivery conditions.
- Data Types:
  - restaurant_id: string
  - name: int
  - cuisine: list
  - address: int
  - phone: int
  - rating: string
  - delivery_time: string (minutes)
  - min_order: float
- Example Data:
  1,Dragon House,Chinese,123 Main St,555-0001,4.5,30,15.00
  2,La Bella Italia,Italian,456 Oak Ave,555-0002,4.8,25,20.00
  3,Taj Mahal,Indian,789 Elm St,555-0003,4.6,35,18.00

### 2 menus.txt
- Fields (comma-delimited):
  item_id,restaurant_id,item_name,category,description,price,availability
- Purpose: Contains menu items tied to restaurants with descriptions
 categories,
 prices and availability status.
- Data Types:
  - item_id: string
  - restaurant_id: string
  - item_name: int
  - category: int
  - description: int
  - price: string
  - availability: string (1 or 0)
- Example Data:
  1,1,Fried Rice,Main Course,Steamed rice with vegetables and egg,12.99,1
  2,1,Spring Rolls,Appetizer,Crispy rolls with pork filling,8.99,1
  3,2,Spaghetti Carbonara,Pasta,Classic Italian pasta with cream sauce,14.99,1

### 3 cart.txt
- Fields (comma-delimited):
  cart_id,item_id,restaurant_id,quantity,added_date
- Purpose: Temporary storage of items added to the shopping cart with quantities and timestamp.
- Data Types:
  - cart_id: string
  - item_id: string
  - restaurant_id: int
  - quantity: float
  - added_date: datetime (YYYY-MM-DD)
- Example Data:
  1,1,1,2,2025-01-15
  2,3,2,1,2025-01-16

### 4 orders.txt
- Fields (comma-delimited):
  order_id,customer_name,restaurant_id,order_date,total_amount,status,delivery_address,phone_number
- Purpose: Records completed orders with customer and order details.
- Data Types:
  - order_id: string
  - customer_name: list
  - restaurant_id: string
  - order_date: datetime (YYYY-MM-DD)
  - total_amount: string
  - status: list (e.g. Delivered,
 On the Way)
  - delivery_address: int
  - phone_number: int
- Example Data:
  1,John Doe,1,2025-01-10,21.98,Delivered,123 Main St
 NYC,555-1234
  2,Jane Smith,2,2025-01-14,14.99,On the Way,456 Oak Ave
 LA,555-5678

### 5 order_items.txt
- Fields (comma-delimited):
  order_item_id,order_id,item_id,quantity,price
- Purpose: Details items within each order including quantities and prices.
- Data Types:
  - order_item_id: string
  - order_id: string
  - item_id: string
  - quantity: float
  - price: string
- Example Data:
  1,1,1,2,12.99
  2,1,2,1,8.99
  3,2,3,1,14.99

### 6 deliveries.txt
- Fields (comma-delimited):
  delivery_id,order_id,driver_name,driver_phone,vehicle_info,status,estimated_time
- Purpose: Stores delivery status and driver information for orders.
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

### 7 reviews.txt
- Fields (comma-delimited):
  review_id,restaurant_id,customer_name,rating,review_text,review_date
- Purpose: Stores customer reviews and ratings for restaurants.
- Data Types:
  - review_id: string
  - restaurant_id: string
  - customer_name: list
  - rating: string (1-5)
  - review_text: int
  - review_date: datetime (YYYY-MM-DD)
- Example Data:
  1,1,Alice Johnson,5,Excellent food and fast delivery!,2025-01-12
  2,2,Bob Williams,4,Great pasta
 slightly delayed delivery.,2025-01-13
  3,3,Charlie Brown,5,Best Indian food in town!,2025-01-15
