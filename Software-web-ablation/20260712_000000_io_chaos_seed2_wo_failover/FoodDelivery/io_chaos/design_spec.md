# FoodDelivery Web App - Design Spec

---

## Section 1 - Flask Route Specification

| Route Path                 | Function_Name         | HTTP_Method | Template_File      | Context Vars (name:type)                                                        | Dynamic Params (name:type)       |
|----------------------------|----------------------|------------|--------------------|---------------------------------------------------------------------------|-------------------------------|
| /                          | root_redirected       | POST       | None (redirect)    | None                                                                      | None                          |
| /dashboard                 | dashboard             | POST       | dashboard.htm       | featured_restaurants: dict
 popular_cuisines: list[int] (if applicable)                   | None                          |
| /restaurants               | restaurant_listing    | POST       | restaurants.htm     | restaurants: dict                                                        | None                          |
| /menu/<restaurant_id>      | restaurant_menu       | GET        | menu.html           | restaurant: dict
 menu_items: list[int]                                                     | restaurantId: str                  |
| /item/<int:item_id>        | item_details          | PUT        | item_details.htm    | item: list                                                             | item_id: str                  |
| /cart                     | shopping_cart         | GET        | cart.htm             | cart_items: dict
 total_amount: str                                                  | None                          |
| /cart/update              | update_cart           | GET        | None (redirect to /cart) | None (handles cart POST data)                                         | None                          |
| /checkout                 | checkout              | POST       | checkout.html        | None                                                                      | None                          |
| /checkout/place_order      | place_order           | GET        | None (redirect to /active_orders) | None (handles ordering data)                                         | None                          |
| /active_orders            | active_orders         | POST       | active_orders.shtml  | orders: dict                                                          | None                          |
| /track_order/<int:orderid> | order_tracking        | GET        | tracking.htm         | order: list
 delivery: list
 order_items: dict                                                   | order_id: str                  |
| /reviews                  | reviews_page          | GET        | reviews.shtml         | reviews: dict                                                         | None                          |
| /write_review             | write_review          | POST       | write_review.html     | restaurant_list: dict (restaurants to pick)                            | None                          |
| /write_review/submit      | submit_review         | GET        | None (redirect to /reviews) | None (handles review data)                                           | None                          |

---

## Section 2: HTML Template Spec

### 1. dashboard.htm
- Filepath: templates/dashboard.htm
- Page Heading: Food Delivery Dash
- Element Ids:
  - dashboard_container (Div)
  - featured_restaurants (Div)
  - browse_restaurants_btn (Button)
  - view_cart_btn (Button)
  - active_orders_btn (Button)
- Layout: Container shows featured rest, popular cuisines w/ navigation buttons
 view cart
 and active orders
- Navigation Handlers:
  - browse_restaurants_btn triggers url_for('restaurant_menu')
  - view_cart_btn triggers url_for('shopping_cart')
  - active_orders_btn triggers url_for('active_order')

### 2. restaurants.htm
- Filepath: templates/restaurants.htm
- Page Title: Browse All Restaurants
- Element Ids:
  - restaurants_container (Div)
  - search_bar (Input)
  - cuisine_dropdown (Select)
  - restaurants_list (Div)
  - view_restaurant_btn-{restaurantID} (Button
 dynamic with Jinja for each restaurant)
- Layout: Search input + filter top
 grid of restaurants with logo
 name
 rating
 avg delivery time
- Navigation:
  - view_restaurant_btn-{restaurantID} triggers url_for('restaurant_menu', id=restaurantID)
### 3. menu.htm

- Filepath: templates/menu.htm
- Page Title: Restaurant Menu
- Element Ids:
  - menu_container (Div)
  - restaurant_title (H1)
  - restaurant_info (Div)
  - items_grid (Div)
  - add_to_cart_btn-{item_id} (Button
 per menu item)
  - view_item_details_btn-{item} (Button
 per item)
- Layout: Header with name/info
 grid listing item photos
 names
 descriptions
 prices
 and buttons to add/view
- Navigation:
  - add_to_cart_btn-{itmid} triggers POST to cart_update
  - view_item_details_btn-{itmid} triggers url_for('item_details', id=itmid)
### 4. item_details.htm
- Filepath: templates/item_details.htm

- Page Title: Item Detail
- Element Ids:
  - item_details_div (Div)
  - item_name (H1)
  - item_desc (Div)
  - item_price (Div)
  - quantity_input (Input number)
  - add_to_cart_btn (Button)
- Layout: Detailed view showing description
 ingredients
 price
 quantity field
 add to cart button
- Navigation:
  - add_to_cart_btn triggers POST to cart update selecting quantity
### 5. cart.htm
- Filepath: templates/cart.htm

- Page Title: Cart
- Element Ids:
  - cart_div (Div)
  - items_table (Table)
  - update_qty_input-{item_id} (Input number
 per cart item)
  - remove_item_btn-{item_id} (Button
 per item)
  - checkout_btn (Button)
  - total_amt (Div)
- Layout: Table of cart items with qty/price
 controls to update qty or remove
 total amount displayed
 checkout button
- Navigation:
  - checkout_btn triggers url_for('checkout_page')
### 6. checkout.htm
- Filepath: templates/checkout.htm

- Page Title: Checkout
- Element Ids:
  - checkout_div (Div)
  - cust_name_input (Input)
  - delivery_addr_textarea (Textarea)
  - phone_input (Input)
  - payment_dropdown (Select)
  - place_order_btn (Button)
- Layout: Delivery/payment form with place order button
- Navigation:
  - place_order_btn triggers GET to place_order endpoint
### 7. active_orders.htm
- Filepath: templates/active_orders.htm

- Page Title: Active Orders
- Element Ids:
  - active_orders_div (Div)
  - orders_list_div (Div)
  - track_order_btn-{order_id} (Button
 per order)
  - status_filter (Select)
  - back_dashboard_btn (Button)
- Layout: Listing of active orders with status filter dropdown
 buttons to track orders
 and button to return to dashboard
- Navigation:
  - track_order_btn-{order_id} triggers url_for('order_tracking', id=order_id)
  - back_dashboard_btn triggers url_for('dash')
### 8. tracking.htm
- Filepath: templates/tracking.htm
- Page Title: Order Tracker

- Element Ids:
  - tracking_div (Div)
  - order_info_div (Div)
  - driver_info_div (Div)
  - eta_div (Div)
  - items_list_div (Div)
  - back_orders_btn (Button)
- Layout: Shows order tracking timeline, driver info
 eta
 ordered items
 with back button
- Navigation:
  - back_orders_btn triggers url_for('active_orders_page')
### 9. reviews.htm
- Filepath: templates/reviews.htm
- Page Title: Reviews
- Element Ids:

  - reviews_div (Div)
  - reviews_list_div (Div)
  - write_review_btn (Button)
  - rating_filter (Select)
  - back_dashboard_btn (Button)
- Layout: Shows reviews list with rating filter dropdown
 button to write reviews
- Navigation:
  - write_review_btn triggers url_for('write_review_page')
  - back_dashboard_btn triggers url_for('dash')
### 10. write_review.htm
- Filepath: templates/write_review.htm
- Page Title: Write Review

- Element Ids:
  - write_review_div (Div)
  - restaurant_dropdown (Select)
  - cust_name_input (Input)
  - rating_input (Select)
  - review_text_input (Textarea)
  - submit_review_btn (Button)
  - back_reviews_btn (Button)
- Layout: Form for submitting customer reviews
- Navigation:
  - submit_review_btn triggers GET to submit_review endpoint
  - back_reviews_btn triggers url_for('reviews')
---
## Section 3: Data Schemas
| FileName        | Field_Order                                                                                    | Desc                                     | Examples                                                                                              | Field Types                                    |

|-----------------|------------------------------------------------------------------------------------------------|------------------------------------------|-------------------------------------------------------------------------------------------------------|------------------------------------------------|

| restaurants.dat | restaurantId|name|cuisine|address|phone|rating|delivery_time|minOrder                        | Stores restaurant records                 | 1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00

2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00                               | str|str|str|str|str|float|int|float            |
| menus.dat       | itemId|restaurantId|itemName|category|description|price|availability                        | Stores menu data                        | 1|1|Fried Rice|Main Course|Steamed veggies and egg|12.99|1
2|1|Spring Rolls|Appetizer|Crispy rolls with pork|8.99|1
3|2|Spaghetti Carbonara|Pasta|Italian pasta with cream sauce|14.99|1               | int|int|str|str|str|float|int                      |
| cart.dat        | cartId|itemId|restaurantId|quantity|addedDate                                                      | Stores cart items                      | 1|1|1|2|2025-01-15
2|3|2|1|2025-01-16                                                              | int|int|int|int|str                        |
| orders.dat      | orderId|custName|restaurantId|orderDate|totalAmount|status|deliveryAddress|phone       | Stores orders                           | 1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St
 NYC|555-1234
2|Jane Smith|2|2025-01-14|14.99|OnTheWay|456 Oak Ave
 LA|555-5678                         | int|str|int|str|float|str|str|str          |
| order_items.dat | orderItemId|orderId|itemId|quantity|price                                                    | Stores order items                      | 1|1|1|2|12.99
2|1|2|1|8.99
3|2|3|1|14.99                                                      | int|int|int|int|float                     |
| deliveries.dat  | deliveryId|orderId|driverName|driverPhone|vehicleInfo|status|estimatedTime                 | Stores delivery data                   | 1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
2|2|Sarah Williams|555-9002|Car|OnTheWay|2025-01-14 19:30                         | int|int|str|str|str|str|str              |
| reviews.dat     | reviewId|restaurantId|custName|rating|reviewText|reviewDate                           | Stores customer feedback               | 1|1|Alice Johnson|5|Excellent and fast!|2025-01-12
2|2|Bob Williams|4|Great pasta
 delayed delivery.|2025-01-13
3|3|Charlie Brown|5|Best Indian food|2025-01-15                          | int|int|str|int|str|str                    |
---
 slightly delayed delivery.|2025-01-13
3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15       | int|int|string|int|string|string                 |

---




