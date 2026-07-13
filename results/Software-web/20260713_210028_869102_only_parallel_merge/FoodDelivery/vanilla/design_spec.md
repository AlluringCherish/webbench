# Unified Design Specification for FoodDelivery Web Application

---

## 1. Unified Flask Routes and Navigation

| Route Path                 | HTTP Methods | Function Name       | Description & Context Variables                                         | Navigation / Button Actions                                               |
|----------------------------|--------------|--------------------|------------------------------------------------------------------------|--------------------------------------------------------------------------|
| `/`                        | GET          | `root_redirect`     | None                                                                   | Redirects to `/dashboard`                                                |
| `/dashboard`               | GET          | `dashboard`         | `featured_restaurants` (list of featured restaurant dicts)              | Buttons:
  - `browse-restaurants-button` → `/restaurants`
  - `view-cart-button` → `/cart`
  - `active-orders-button` → `/orders/active`
|
| `/restaurants`             | GET          | `restaurants`       | `restaurants` (list), `search_query`, `cuisine_filter`                  | Search input `search-input` filters by name or cuisine
Filter dropdown `cuisine-filter` for cuisine type
Button:
  - `view-restaurant-button-{restaurant_id}` → `/restaurant/<restaurant_id>`
|
| `/restaurant/<int:id>`     | GET          | `restaurant_menu`   | `restaurant` (dict), `menu_items` (list)                               | Buttons:
  - `add-to-cart-button-{item_id}` adds item to cart (POST/AJAX), stays on menu
  - `view-item-details-{item_id}` → `/item/<item_id>`
|
| `/item/<int:item_id>`      | GET, POST    | `item_details`      | `item` (dict)                                                         | Input quantity (`quantity-input`)
Button:
  - `add-to-cart-button` adds item(s) with quantity to cart, redirects to `/cart`
|
| `/cart`                    | GET          | `shopping_cart`     | `cart_items` (list), `total_amount`                                   | Buttons:
  - `update-quantity-{item_id}` update quantity
  - `remove-item-button-{item_id}` remove item
  - `proceed-checkout-button` → `/checkout`
|
| `/checkout`                | GET, POST    | `checkout`          | GET: None, POST: order submission confirmation                          | Form inputs: `customer-name`, `delivery-address`, `phone-number`, `payment-method`
Button:
  - `place-order-button` submits order, redirects to `/orders/active`
|
| `/orders/active`           | GET          | `active_orders`     | `orders` (list), `status_filter`                                      | Buttons:
  - `track-order-button-{order_id}` → `/order/track/<order_id>`
  - `back-to-dashboard` → `/dashboard`
|
| `/order/track/<int:id>`    | GET          | `order_tracking`    | `order` (dict), `delivery_info` (dict), `order_items`                  | Button:
  - `back-to-orders` → `/orders/active`
|
| `/reviews`                 | GET          | `reviews`           | `reviews` (list), `rating_filter`                                     | Buttons:
  - `write-review-button` → `/write-review` (page or modal, external)
  - `filter-by-rating` dropdown
  - `back-to-dashboard` → `/dashboard`

---

## 2. Page Titles and Element IDs

### 2.1 Dashboard Page
- **Page Title:** Food Delivery Dashboard
- **Element IDs:**
  - `dashboard-page` (Div) - Container for dashboard page
  - `featured-restaurants` (Div) - Display featured restaurants
  - `browse-restaurants-button` (Button) - Navigate to Restaurant Listing
  - `view-cart-button` (Button) - Navigate to Shopping Cart
  - `active-orders-button` (Button) - Navigate to Active Orders

### 2.2 Restaurant Listing Page
- **Page Title:** Browse Restaurants
- **Element IDs:**
  - `restaurants-page` (Div) - Container for restaurants listing
  - `search-input` (Input) - Search restaurants by name or cuisine
  - `cuisine-filter` (Dropdown) - Filter restaurants by cuisine type
  - `restaurants-grid` (Div) - Grid displaying restaurant cards
  - `view-restaurant-button-{restaurant_id}` (Button) - View menu for specific restaurant

### 2.3 Restaurant Menu Page
- **Page Title:** Restaurant Menu
- **Element IDs:**
  - `menu-page` (Div) - Container for menu page
  - `restaurant-name` (H1) - Name of the restaurant
  - `restaurant-info` (Div) - Address, phone, rating
  - `menu-items-grid` (Div) - Grid of menu items
  - `add-to-cart-button-{item_id}` (Button) - Add menu item to cart
  - `view-item-details-{item_id}` (Button) - Show detailed item info

### 2.4 Item Details Page
- **Page Title:** Item Details
- **Element IDs:**
  - `item-details-page` (Div) - Container for item details
  - `item-name` (H1) - Item name
  - `item-description` (Div) - Description and ingredients
  - `item-price` (Div) - Price
  - `quantity-input` (Input number) - Quantity selector
  - `add-to-cart-button` (Button) - Add item to cart with quantity

### 2.5 Shopping Cart Page
- **Page Title:** Shopping Cart
- **Element IDs:**
  - `cart-page` (Div) - Container for cart page
  - `cart-items-table` (Table) - Table listing cart items
  - `update-quantity-{item_id}` (Input number) - Update item quantity
  - `remove-item-button-{item_id}` (Button) - Remove item from cart
  - `proceed-checkout-button` (Button) - Proceed to checkout
  - `total-amount` (Div) - Display cart total amount

### 2.6 Checkout Page
- **Page Title:** Checkout
- **Element IDs:**
  - `checkout-page` (Div) - Container for checkout page
  - `customer-name` (Input) - Customer name input
  - `delivery-address` (Textarea) - Delivery address input
  - `phone-number` (Input) - Phone number input
  - `payment-method` (Dropdown) - Payment method selection
  - `place-order-button` (Button) - Confirm and place order

### 2.7 Active Orders Page
- **Page Title:** Active Orders
- **Element IDs:**
  - `active-orders-page` (Div) - Container for active orders
  - `orders-list` (Div) - List of active orders
  - `track-order-button-{order_id}` (Button) - View tracking for order
  - `status-filter` (Dropdown) - Filter orders by status
  - `back-to-dashboard` (Button) - Navigate to dashboard

### 2.8 Order Tracking Page
- **Page Title:** Track Order
- **Element IDs:**
  - `tracking-page` (Div) - Container for tracking page
  - `order-details` (Div) - Complete order details and timeline
  - `delivery-driver-info` (Div) - Driver name, phone, vehicle info
  - `estimated-time` (Div) - Estimated delivery time
  - `order-items-list` (Div) - List of ordered items
  - `back-to-orders` (Button) - Navigate back to active orders

### 2.9 Reviews Page
- **Page Title:** Order Reviews
- **Element IDs:**
  - `reviews-page` (Div) - Container for reviews
  - `reviews-list` (Div) - List of all reviews
  - `write-review-button` (Button) - Navigate to write review page (external)
  - `filter-by-rating` (Dropdown) - Filter reviews by rating
  - `back-to-dashboard` (Button) - Navigate to dashboard

---

## 3. Data Files and Usage

| File Name          | Fields (Pipe-Delimited)                                               | Purpose / Usage                                                   |
|--------------------|----------------------------------------------------------------------|-----------------------------------------------------------------|
| `restaurants.txt`   | `restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order` | Used on Dashboard (featured), Restaurant Listing, Restaurant Menu details. |
| `menus.txt`         | `item_id|restaurant_id|item_name|category|description|price|availability` | Used on Restaurant Menu pages, Item Details, and adding to Cart. |
| `cart.txt`          | `cart_id|item_id|restaurant_id|quantity|added_date`                   | Used on Shopping Cart page to display and manage cart contents.  |
| `orders.txt`        | `order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number` | Used on Active Orders, Order Tracking pages, and order management. |
| `order_items.txt`   | `order_item_id|order_id|item_id|quantity|price`                      | Used to provide detailed items list in orders and tracking.      |
| `deliveries.txt`    | `delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time` | Used on Order Tracking page to show delivery driver info and status. |
| `reviews.txt`       | `review_id|restaurant_id|customer_name|rating|review_text|review_date`| Used on Reviews page to display and filter customer reviews.      |

---

This unified design specification provides precise and consistent routing, page elements, data file usage, and navigation details for the FoodDelivery Flask web application, enabling development without ambiguity or further clarifications.
