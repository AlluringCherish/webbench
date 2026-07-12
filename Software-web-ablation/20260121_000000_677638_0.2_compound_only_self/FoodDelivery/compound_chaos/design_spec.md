# FoodDelivery Application Design Specification

---

## 1. Flask Routes Specification

| Route Path                               | Function Name           | HTTP Method | Template File          | Context Variables                                                                                         | Notes/Parameters                           |
|-----------------------------------------|-------------------------|-------------|------------------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------|
| `/`                                     | redirect_to_dashboard    | GET         | -                      | -                                                                                                        | Redirect root to `/dashboard`
| `/dashboard`                            | show_dashboard          | GET         | dashboard.html         | featured_restaurants: List[dict], popular_cuisines: List[str]                                            | Main landing page                         |
| `/restaurants`                         | list_restaurants        | GET         | restaurants.html       | restaurants: List[dict], search_query: str, cuisine_filter: str                                           | Browse restaurants, with filters          |
| `/restaurants/<int:restaurant_id>/menu`| show_menu              | GET         | menu.html              | restaurant: dict, menu_items: List[dict]                                                                 | Menu for a specific restaurant             |
| `/items/<int:item_id>`                 | show_item_details       | GET         | item_details.html      | item: dict                                                                                               | Item details view                         |
| `/cart`                               | show_cart               | GET         | cart.html              | cart_items: List[dict], total_amount: float                                                             | Show shopping cart                        |
| `/cart/add/<int:item_id>`              | add_to_cart             | POST        | -                      | -                                                                                                        | Add item to cart                          |
| `/cart/update/<int:item_id>`           | update_cart_quantity    | POST        | -                      | -                                                                                                        | Update item quantity in cart              |
| `/cart/remove/<int:item_id>`           | remove_from_cart        | POST        | -                      | -                                                                                                        | Remove item from cart                     |
| `/checkout`                           | proceed_checkout        | POST        | checkout.html          | cart_items: List[dict], total_amount: float, order_confirmation: dict (optional)                          | Checkout order placement                  |
| `/orders`                             | list_active_orders      | GET         | active_orders.html     | active_orders: List[dict], status_filter: str                                                           | List user's active orders                 |
| `/tracking/<int:order_id>`             | track_order            | GET         | tracking.html          | order_details: dict, delivery_driver_info: dict, estimated_time: str                                     | Order tracking page                       |
| `/reviews`                           | show_reviews            | GET         | reviews.html           | reviews: List[dict], rating_filter: str                                                                  | List and filter reviews                   |
| `/reviews/write`                     | write_review            | GET/POST    | write_review.html      | - (GET: form display, POST: submission processing)                                                       | Write new review page                     |

---

## 2. HTML Template Specifications

### dashboard.html
- File path: `templates/dashboard.html`
- Page Title: Food Delivery Dashboard
- Layout Overview: Div container `dashboard-page` with featured restaurants and navigation buttons
- Element IDs:
  - `dashboard-page` (div) - main dashboard container
  - `featured-restaurants` (div) - featured restaurant list
  - `browse-restaurants-button` (button) - navigate to `/restaurants`
  - `view-cart-button` (button) - navigate to `/cart`
  - `active-orders-button` (button) - navigate to `/orders`

### restaurants.html
- File path: `templates/restaurants.html`
- Page Title: Browse Restaurants
- Layout Overview: Div container `restaurants-page` wraps search/filter inputs and restaurants grid
- Element IDs:
  - `restaurants-page` (div)
  - `search-input` (input, text) - search box
  - `cuisine-filter` (dropdown)
  - `restaurants-grid` (div) - grid of restaurant cards
  - Dynamic button ID pattern: `view-restaurant-button-{restaurant_id}` (button) for each restaurant

### menu.html
- File path: `templates/menu.html`
- Page Title: Restaurant Menu
- Layout Overview: Div container `menu-page` with restaurant info and menu grid
- Element IDs:
  - `menu-page` (div)
  - `restaurant-name` (h1) - display restaurant name
  - `restaurant-info` (div) - address, phone, rating
  - `menu-items-grid` (div) - grid of menu items
  - Dynamic button ID patterns:
    - `add-to-cart-button-{item_id}` (button)
    - `view-item-details-{item_id}` (button)

### item_details.html
- File path: `templates/item_details.html`
- Page Title: Item Details
- Layout Overview: Div container `item-details-page` with item name, description, price, and cart controls
- Element IDs:
  - `item-details-page` (div)
  - `item-name` (h1)
  - `item-description` (div)
  - `item-price` (div)
  - `quantity-input` (input, number)
  - `add-to-cart-button` (button)

### cart.html
- File path: `templates/cart.html`
- Page Title: Shopping Cart
- Layout Overview: Div container `cart-page` with cart items table and controls
- Element IDs:
  - `cart-page` (div)
  - `cart-items-table` (table)
  - Per cart item dynamic IDs:
    - `update-quantity-{item_id}` (input, number)
    - `remove-item-button-{item_id}` (button)
  - `proceed-checkout-button` (button)
  - `total-amount` (div)

### checkout.html
- File path: `templates/checkout.html`
- Page Title: Checkout
- Layout Overview: Div container `checkout-page` with input fields for user info and order submission
- Element IDs:
  - `checkout-page` (div)
  - `customer-name` (input, text)
  - `delivery-address` (textarea)
  - `phone-number` (input, text)
  - `payment-method` (dropdown)
  - `place-order-button` (button)

### active_orders.html
- File path: `templates/active_orders.html`
- Page Title: Active Orders
- Layout Overview: Div container `active-orders-page` listing orders with filter controls
- Element IDs:
  - `active-orders-page` (div)
  - `orders-list` (div)
  - Dynamic button ID pattern: `track-order-button-{order_id}` (button)
  - `status-filter` (dropdown)
  - `back-to-dashboard` (button)

### tracking.html
- File path: `templates/tracking.html`
- Page Title: Track Order
- Layout Overview: Div container `tracking-page` with order details and delivery info
- Element IDs:
  - `tracking-page` (div)
  - `order-details` (div)
  - `delivery-driver-info` (div)
  - `estimated-time` (div)
  - `order-items-list` (div)
  - `back-to-orders` (button)

### reviews.html
- File path: `templates/reviews.html`
- Page Title: Order Reviews
- Layout Overview: Div container `reviews-page` for reviews list and filtering
- Element IDs:
  - `reviews-page` (div)
  - `reviews-list` (div)
  - `write-review-button` (button)
  - `filter-by-rating` (dropdown)
  - `back-to-dashboard` (button)

---

## 3. Data Schemas

| File Name         | Fields (pipe-delimited)                                                       | Data Types                                                  | Purpose                                  | Example Rows                                                                                                                       |
|-------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------|------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| `restaurants.txt`  | restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order               | int|string|string|string|string|float|int|float                   | Stores restaurant details               | 1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00                              |
| `menus.txt`       | item_id|restaurant_id|item_name|category|description|price|availability                   | int|int|string|string|string|float|bool                   | Stores menu items per restaurant        | 1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1                |
| `cart.txt`        | cart_id|item_id|restaurant_id|quantity|added_date                                | int|int|int|int|date                             | Stores shopping cart items              | 1|1|1|2|2025-01-15
2|3|2|1|2025-01-16                                                                                                    |
| `orders.txt`      | order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number | int|string|int|date|float|string|string|string         | Stores placed orders                    | 1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678               |
| `order_items.txt` | order_item_id|order_id|item_id|quantity|price                                  | int|int|int|int|float                             | Stores items in each order              | 1|1|1|2|12.99
2|1|2|1|8.99
3|2|3|1|14.99                                                                                                   |
| `deliveries.txt`  | delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time       | int|int|string|string|string|string|datetime                         | Stores delivery information            | 1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30                                               |
| `reviews.txt`     | review_id|restaurant_id|customer_name|rating|review_text|review_date               | int|int|string|int|string|date                             | Stores customer reviews                | 1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15                               |

---

This comprehensive design specification allows backend and frontend developers to work independently with unambiguous details covering routes, HTML templates, element IDs, context variables, and data schemas.