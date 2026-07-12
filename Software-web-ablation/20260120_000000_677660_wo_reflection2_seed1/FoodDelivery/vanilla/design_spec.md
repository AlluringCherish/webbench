# FoodDelivery Web Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path               | Function Name         | HTTP Method | Template File        | Context Variables                                                                                                              | Dynamic Parameters                 |
|--------------------------|-----------------------|-------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| /                        | root_redirect          | GET         | N/A (redirect)       | None                                                                                                                          | None                             |
| /dashboard               | dashboard             | GET         | dashboard.html       | featured_restaurants: List[Dict] (restaurant data), popular_cuisines: List[str]                                                | None                             |
| /restaurants             | restaurant_listing    | GET         | restaurants.html     | restaurants: List[Dict], cuisine_options: List[str]                                                                            | None                             |
| /menu/<int:restaurant_id>| restaurant_menu       | GET         | menu.html            | restaurant: Dict, menu_items: List[Dict]                                                                                       | restaurant_id: int               |
| /item/<int:item_id>      | item_details          | GET         | item_details.html    | item: Dict                                                                                                                     | item_id: int                    |
| /cart                   | shopping_cart          | GET, POST   | cart.html            | cart_items: List[Dict], total_amount: float                                                                                   | None                             |
| /cart/update            | update_cart            | POST        | N/A (redirect POST)  | None                                                                                                                          | None                             |
| /checkout               | checkout_page          | GET, POST   | checkout.html        | None for GET; for POST may have order confirmation or errors                                                                  | None                             |
| /orders/active          | active_orders          | GET         | active_orders.html   | active_orders: List[Dict], status_filter_options: List[str]                                                                    | None                             |
| /orders/track/<int:order_id> | order_tracking      | GET         | tracking.html        | order_details: Dict, delivery_driver_info: Dict, estimated_time: str, order_items: List[Dict]                                   | order_id: int                   |
| /reviews                | reviews_page           | GET         | reviews.html         | reviews: List[Dict], rating_filter_options: List[str]                                                                          | None                             |
| /reviews/write          | write_review           | GET, POST   | write_review.html    | None for GET; for POST may handle form submission result                                                                      | None                             |

---

## Section 2: HTML Template Specifications

### 1. dashboard.html
- File path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Elements:
  - div#dashboard-page
  - div#featured-restaurants
  - button#browse-restaurants-button
  - button#view-cart-button
  - button#active-orders-button
- Layout Overview: Main container holds featured restaurant recommendations and popular cuisine links with top-level navigation buttons.
- Navigation Mappings:
  - #browse-restaurants-button -> restaurant_listing
  - #view-cart-button -> shopping_cart
  - #active-orders-button -> active_orders

### 2. restaurants.html
- File path: templates/restaurants.html
- Page Title: Browse Restaurants
- Elements:
  - div#restaurants-page
  - input#search-input
  - select#cuisine-filter
  - div#restaurants-grid
  - button#view-restaurant-button-{restaurant_id} (dynamic for each restaurant)
- Layout Overview: Container with search and filter controls above a grid of restaurant cards each featuring their info and navigation button.
- Navigation Mappings:
  - #view-restaurant-button-{restaurant_id} -> restaurant_menu(restaurant_id)

### 3. menu.html
- File path: templates/menu.html
- Page Title: Restaurant Menu
- Elements:
  - div#menu-page
  - h1#restaurant-name
  - div#restaurant-info
  - div#menu-items-grid
  - button#add-to-cart-button-{item_id} (dynamic for each menu item)
  - button#view-item-details-{item_id} (dynamic for each menu item)
- Layout Overview: Displays restaurant details at top and a grid of menu items with add/view buttons for each.
- Navigation Mappings:
  - #add-to-cart-button-{item_id} triggers add to cart POST action
  - #view-item-details-{item_id} -> item_details(item_id)

### 4. item_details.html
- File path: templates/item_details.html
- Page Title: Item Details
- Elements:
  - div#item-details-page
  - h1#item-name
  - div#item-description
  - div#item-price
  - input#quantity-input (number)
  - button#add-to-cart-button
- Layout Overview: Shows detailed info about a menu item with quantity selector and add-to-cart button.
- Navigation Mappings:
  - #add-to-cart-button triggers add to cart POST action with quantity

### 5. cart.html
- File path: templates/cart.html
- Page Title: Shopping Cart
- Elements:
  - div#cart-page
  - table#cart-items-table
  - input#update-quantity-{item_id} (dynamic for each cart item)
  - button#remove-item-button-{item_id} (dynamic for each cart item)
  - button#proceed-checkout-button
  - div#total-amount
- Layout Overview: Displays a table of cart items with quantity update and remove buttons, total amount, and a checkout trigger.
- Navigation Mappings:
  - #proceed-checkout-button -> checkout_page

### 6. checkout.html
- File path: templates/checkout.html
- Page Title: Checkout
- Elements:
  - div#checkout-page
  - input#customer-name
  - textarea#delivery-address
  - input#phone-number
  - select#payment-method
  - button#place-order-button
- Layout Overview: Form for customer delivery details and payment method selection with order placement button.
- Navigation Mappings:
  - #place-order-button triggers order submission POST

### 7. active_orders.html
- File path: templates/active_orders.html
- Page Title: Active Orders
- Elements:
  - div#active-orders-page
  - div#orders-list
  - button#track-order-button-{order_id} (dynamic for each order)
  - select#status-filter
  - button#back-to-dashboard
- Layout Overview: Lists active orders with status filter and buttons for tracking, plus back to dashboard navigation.
- Navigation Mappings:
  - #track-order-button-{order_id} -> order_tracking(order_id)
  - #back-to-dashboard -> dashboard

### 8. tracking.html
- File path: templates/tracking.html
- Page Title: Track Order
- Elements:
  - div#tracking-page
  - div#order-details
  - div#delivery-driver-info
  - div#estimated-time
  - div#order-items-list
  - button#back-to-orders
- Layout Overview: Shows detailed order tracking with driver info and timeline.
- Navigation Mappings:
  - #back-to-orders -> active_orders

### 9. reviews.html
- File path: templates/reviews.html
- Page Title: Order Reviews
- Elements:
  - div#reviews-page
  - div#reviews-list
  - button#write-review-button
  - select#filter-by-rating
  - button#back-to-dashboard
- Layout Overview: Shows reviews list with filter and button to write new review, includes navigation back to dashboard.
- Navigation Mappings:
  - #write-review-button -> write_review
  - #back-to-dashboard -> dashboard

---

## Section 3: Data Schemas

| File Name        | Field Order                                                       | Purpose                                               | Data Types                          | Example Data Rows                                                                       |
|------------------|-------------------------------------------------------------------|-------------------------------------------------------|-----------------------------------|-----------------------------------------------------------------------------------------|
| restaurants.txt  | restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order   | Stores details of restaurants                       | int|string|string|string|string|float|int|float            | 1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00 |
| menus.txt        | item_id|restaurant_id|item_name|category|description|price|availability | Stores menu items by restaurant                     | int|int|string|string|string|float|int           | 1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1 |
| cart.txt         | cart_id|item_id|restaurant_id|quantity|added_date                   | Stores current shopping cart items                   | int|int|int|int|string                  | 1|1|1|2|2025-01-15
2|3|2|1|2025-01-16                                                         |
| orders.txt       | order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number | Stores placed orders                                | int|string|int|string|float|string|string|string        | 1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678             |
| order_items.txt  | order_item_id|order_id|item_id|quantity|price                     | Stores items within each order                        | int|int|int|int|float                        | 1|1|1|2|12.99
2|1|2|1|8.99
3|2|3|1|14.99                                                     |
| deliveries.txt   | delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time | Stores delivery info for orders                      | int|int|string|string|string|string|string              | 1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30                                   |
| reviews.txt      | review_id|restaurant_id|customer_name|rating|review_text|review_date | Stores customer reviews                              | int|int|string|int|string|string                        | 1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15         |

---

**Note:**
- All IDs are integers.
- Dates are stored as strings in ISO format (YYYY-MM-DD) or date+time as specified.
- Ratings are floats or ints depending on context.

---

This design specification fully covers all routes, templates, and data schemas to enable independent backend and frontend development based solely on this document.