# FoodDelivery Web Application - Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                         | Function Name          | HTTP Method(s) | Template File          | Context Variables (name : type)                                                                                                                                                     | Dynamic Parameters           |
|----------------------------------|-----------------------|----------------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------|
| /                                | root_redirect          | GET            | None (redirect)         | None                                                                                                                                                                                 | None                        |
| /dashboard                      | dashboard_page         | GET            | dashboard.html          | featured_restaurants : list of dict, popular_cuisines : list of string                                                                                                              | None                        |
| /restaurants                    | browse_restaurants     | GET            | restaurants.html        | restaurants : list of dict, cuisine_options : list of string, selected_cuisine : string or None, search_query : string or None                                                        | None                        |
| /restaurant/<int:restaurant_id> | restaurant_menu        | GET            | menu.html               | restaurant : dict, menu_items : list of dict                                                                                                                                         | restaurant_id : int          |
| /item/<int:item_id>             | item_details           | GET            | item_details.html       | item : dict                                                                                                                                                                         | item_id : int               |
| /item/<int:item_id>/add_to_cart | add_item_to_cart       | POST           | None (redirect)         | None                                                                                                                                                                                 | item_id : int               |
| /cart                          | shopping_cart          | GET, POST      | cart.html               | cart_items : list of dict, total_amount : float                                                                                                                                      | None                        |
| /cart/update_quantity           | update_cart_quantity   | POST           | None (redirect)         | None                                                                                                                                                                                 | None                        |
| /cart/remove_item/<int:item_id> | remove_cart_item       | POST           | None (redirect)         | None                                                                                                                                                                                 | item_id : int               |
| /checkout                      | checkout_page          | GET            | checkout.html           | None                                                                                                                                                                                 | None                        |
| /checkout/place_order           | place_order            | POST           | None (redirect)         | None                                                                                                                                                                                 | None                        |
| /orders/active                  | active_orders          | GET            | active_orders.html      | active_orders : list of dict, status_filter_options : list of string, selected_status : string                                                                                         | None                        |
| /order/<int:order_id>/track     | order_tracking         | GET            | tracking.html           | order_details : dict, delivery_driver : dict, estimated_time : string, order_items : list of dict                                                                                      | order_id : int              |
| /reviews                       | reviews_page           | GET            | reviews.html            | reviews : list of dict, rating_filter_options : list of string, selected_rating : string                                                                                                | None                        |
| /reviews/write                 | write_review_page      | GET            | write_review.html       | restaurants : list of dict                                                                                                                                                            | None                        |
| /reviews/submit                | submit_review          | POST           | None (redirect)         | None                                                                                                                                                                                 | None                        |

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- File path: templates/dashboard.html
- Page title: Food Delivery Dashboard
- Elements:
  - div#dashboard-page
  - div#featured-restaurants
  - button#browse-restaurants-button
  - button#view-cart-button
  - button#active-orders-button
- Layout overview: Main container "dashboard-page" holds featured restaurant recommendations section and navigation buttons for browsing restaurants, viewing cart, and viewing active orders.
- Navigation mappings:
  - browse-restaurants-button -> url_for('browse_restaurants')
  - view-cart-button -> url_for('shopping_cart')
  - active-orders-button -> url_for('active_orders')

### 2. restaurants.html
- File path: templates/restaurants.html
- Page title: Browse Restaurants
- Elements:
  - div#restaurants-page
  - input#search-input
  - select#cuisine-filter
  - div#restaurants-grid
  - button#view-restaurant-button-{restaurant_id} (dynamic, where {restaurant_id} is restaurant's ID)
- Layout overview: Contains search input and cuisine filter dropdown above a grid listing restaurant cards, each with buttons to view restaurant menu.
- Navigation mappings:
  - view-restaurant-button-{restaurant_id} -> url_for('restaurant_menu', restaurant_id=restaurant_id)

### 3. menu.html
- File path: templates/menu.html
- Page title: Restaurant Menu
- Elements:
  - div#menu-page
  - h1#restaurant-name
  - div#restaurant-info
  - div#menu-items-grid
  - button#add-to-cart-button-{item_id} (dynamic, per menu item)
  - button#view-item-details-{item_id} (dynamic, per menu item)
- Layout overview: Shows restaurant name and info followed by menu item grid; each item has add to cart and view details buttons.
- Navigation mappings:
  - add-to-cart-button-{item_id} -> POST to add_item_to_cart route with item_id
  - view-item-details-{item_id} -> url_for('item_details', item_id=item_id)

### 4. item_details.html
- File path: templates/item_details.html
- Page title: Item Details
- Elements:
  - div#item-details-page
  - h1#item-name
  - div#item-description
  - div#item-price
  - input#quantity-input (type=number)
  - button#add-to-cart-button
- Layout overview: Displays detailed info about a menu item including description, price, and quantity selector with add to cart button.
- Navigation mappings:
  - add-to-cart-button -> POST to add_item_to_cart for selected quantity

### 5. cart.html
- File path: templates/cart.html
- Page title: Shopping Cart
- Elements:
  - div#cart-page
  - table#cart-items-table
  - input#update-quantity-{item_id} (dynamic, number input per cart item)
  - button#remove-item-button-{item_id} (dynamic, per cart item)
  - button#proceed-checkout-button
  - div#total-amount
- Layout overview: Table showing cart items with editable quantity fields, remove buttons, total amount display, and proceed to checkout button.
- Navigation mappings:
  - remove-item-button-{item_id} -> POST to remove_cart_item with item_id
  - proceed-checkout-button -> url_for('checkout_page')

### 6. checkout.html
- File path: templates/checkout.html
- Page title: Checkout
- Elements:
  - div#checkout-page
  - input#customer-name
  - textarea#delivery-address
  - input#phone-number
  - select#payment-method
  - button#place-order-button
- Layout overview: Form to enter customer delivery details and payment method with a button to place order.
- Navigation mappings:
  - place-order-button -> POST to place_order route

### 7. active_orders.html
- File path: templates/active_orders.html
- Page title: Active Orders
- Elements:
  - div#active-orders-page
  - div#orders-list
  - button#track-order-button-{order_id} (dynamic, per order)
  - select#status-filter
  - button#back-to-dashboard
- Layout overview: Displays list of active orders with status filter dropdown and buttons to track individual orders.
- Navigation mappings:
  - track-order-button-{order_id} -> url_for('order_tracking', order_id=order_id)
  - back-to-dashboard -> url_for('dashboard_page')

### 8. tracking.html
- File path: templates/tracking.html
- Page title: Track Order
- Elements:
  - div#tracking-page
  - div#order-details
  - div#delivery-driver-info
  - div#estimated-time
  - div#order-items-list
  - button#back-to-orders
- Layout overview: Detailed view of order tracking info including driver details, estimated delivery time, and order items with back button.
- Navigation mappings:
  - back-to-orders -> url_for('active_orders')

### 9. reviews.html
- File path: templates/reviews.html
- Page title: Order Reviews
- Elements:
  - div#reviews-page
  - div#reviews-list
  - button#write-review-button
  - select#filter-by-rating
  - button#back-to-dashboard
- Layout overview: Shows list of reviews with rating filter dropdown and button to write new reviews.
- Navigation mappings:
  - write-review-button -> url_for('write_review_page')
  - back-to-dashboard -> url_for('dashboard_page')

### 10. write_review.html
- File path: templates/write_review.html
- Page title: Write Review
- Elements:
  - div#write-review-page
  - select#select-restaurant
  - input#reviewer-name
  - select#rating-select
  - textarea#review-text
  - button#submit-review-button
- Layout overview: Form page to submit a new review for a restaurant.
- Navigation mappings:
  - submit-review-button -> POST to submit_review route

---

## Section 3: Data Schemas

| File Name         | Field Order (pipe-delimited)                                                       | Data Types (in order)                                                 | Purpose                                                                                         | Example Data Rows                                                                                          |
|-------------------|-----------------------------------------------------------------------------------|----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| restaurants.txt   | restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order              | int|string|string|string|string|float|int|float                          | Stores restaurant details including location, cuisine, contact, rating, delivery time and minimum order. | 1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00                                           |
| menus.txt         | item_id|restaurant_id|item_name|category|description|price|availability                       | int|int|string|string|string|float|int                     | Stores menu items for restaurants with details and availability flag.                                   | 1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1                        |
| cart.txt          | cart_id|item_id|restaurant_id|quantity|added_date                            | int|int|int|int|string (date)                 | Stores user cart items with quantity and date added.                                                   | 1|1|1|2|2025-01-15
2|3|2|1|2025-01-16                                                        |
| orders.txt        | order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number | int|string|int|string (date)|float|string|string|string               | Stores order details including customer, status, and delivery info.                                     | 1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678                                      |
| order_items.txt   | order_item_id|order_id|item_id|quantity|price                       | int|int|int|int|float                                | Stores items included in each order with quantity and price.                                          | 1|1|1|2|12.99
2|1|2|1|8.99
3|2|3|1|14.99                                                  |
| deliveries.txt    | delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time           | int|int|string|string|string|string|string                       | Contains delivery information including driver and vehicle info and status.                             | 1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30                                                     |
| reviews.txt       | review_id|restaurant_id|customer_name|rating|review_text|review_date             | int|int|string|int|string|string                                     | Stores customer reviews including rating and review text.                                             | 1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15                                            |

---

# End of Design Specification
