# FoodDelivery Web Application Design Specification

---

## 1. Flask Routes and HTTP Methods

| Route | HTTP Method | Function Name | Description |
|-------|-------------|---------------|-------------|
| /dashboard | GET | dashboard_view | Render Dashboard Page - start page |
| /restaurants | GET | restaurant_listing_view | Render Restaurant Listing Page |
| /menu/<int:restaurant_id> | GET | restaurant_menu_view | Render Restaurant Menu Page for given restaurant |
| /item/<int:item_id> | GET | item_details_view | Render Item Details Page for given menu item |
| /cart | GET, POST | shopping_cart_view | GET: Display cart contents; POST: update cart quantities or delete items |
| /add-to-cart | POST | add_to_cart | Add menu item to cart from Menu Page or Item Details Page |
| /checkout | GET, POST | checkout_view | GET: Display checkout form; POST: process order submission |
| /active-orders | GET | active_orders_view | Display current active orders with filter functionality |
| /track-order/<int:order_id> | GET | order_tracking_view | Display detailed tracking for a specific order |
| /reviews | GET, POST | reviews_view | GET: Display reviews with optional filter; POST: submit new review (if review writing enabled)

---

## 2. Template Files

| Template Filename | Description |
|-------------------|-------------|
| dashboard.html | Dashboard Page template |
| restaurants.html | Restaurant Listing Page template |
| menu.html | Restaurant Menu Page template |
| item_details.html | Item Details Page template |
| cart.html | Shopping Cart Page template |
| checkout.html | Checkout Page template |
| active_orders.html | Active Orders Page template |
| tracking.html | Order Tracking Page template |
| reviews.html | Reviews Page template |

---

## 3. UI Elements Specification

### 3.1 Dashboard Page (/dashboard)
- Container Div: `dashboard-page`
- Featured restaurants display Div: `featured-restaurants`
- Buttons:
  - `browse-restaurants-button`: Navigate to `/restaurants`
  - `view-cart-button`: Navigate to `/cart`
  - `active-orders-button`: Navigate to `/active-orders`

### 3.2 Restaurant Listing Page (/restaurants)
- Container Div: `restaurants-page`
- Search Input (text): `search-input` (searches by restaurant name or cuisine)
- Cuisine filter Dropdown: `cuisine-filter` (e.g., Chinese, Italian, Indian)
- Restaurants grid Div: `restaurants-grid` (contains cards)
- For each restaurant:
  - Button: `view-restaurant-button-{restaurant_id}` navigates to `/menu/{restaurant_id}`

### 3.3 Restaurant Menu Page (/menu/irstaurant_id)
- Container Div: `menu-page`
- Restaurant name H1: `restaurant-name`
- Restaurant info Div: `restaurant-info` (address, phone, rating)
- Menu items grid Div: `menu-items-grid`
- For each menu item:
  - Button: `add-to-cart-button-{item_id}` (adds item to cart)
  - Button: `view-item-details-{item_id}` (navigates to `/item/{item_id}`)

### 3.4 Item Details Page (/item/{item_id})
- Container Div: `item-details-page`
- Item name H1: `item-name`
- Item description Div: `item-description`
- Item price Div: `item-price`
- Quantity Input (number): `quantity-input` (default 1, min 1)
- Button: `add-to-cart-button` (adds selected quantity to cart)

### 3.5 Shopping Cart Page (/cart)
- Container Div: `cart-page`
- Cart items Table: `cart-items-table` with columns: item name, quantity, price, subtotal
- For each cart item:
  - Quantity Input (number): `update-quantity-{item_id}` (updates quantity)
  - Remove Button: `remove-item-button-{item_id}` (removes item from cart)
- Button: `proceed-checkout-button` navigates to `/checkout`
- Total amount Div: `total-amount`

### 3.6 Checkout Page (/checkout)
- Container Div: `checkout-page`
- Inputs:
  - `customer-name` (text input)
  - `delivery-address` (textarea)
  - `phone-number` (text input)
  - Payment method Dropdown: `payment-method` (Credit Card, Cash, PayPal)
- Button: `place-order-button` submits order

### 3.7 Active Orders Page (/active-orders)
- Container Div: `active-orders-page`
- Orders list Div: `orders-list` showing order ID, restaurant, status, ETA
- For each order:
  - Button: `track-order-button-{order_id}` navigates to `/track-order/{order_id}`
- Status filter Dropdown: `status-filter` (All, Preparing, On the Way, Delivered)
- Button: `back-to-dashboard` navigates to `/dashboard`

### 3.8 Order Tracking Page (/track-order/{order_id})
- Container Div: `tracking-page`
- Div: `order-details` (complete order and timeline details)
- Div: `delivery-driver-info` (driver name, phone, vehicle info)
- Div: `estimated-time` (ETA)
- Div: `order-items-list` (list of ordered items)
- Button: `back-to-orders` navigates to `/active-orders`

### 3.9 Reviews Page (/reviews)
- Container Div: `reviews-page`
- Div: `reviews-list` showing reviews with restaurant name, rating, text
- Button: `write-review-button` (navigate to write review page if implemented)
- Filter Dropdown: `filter-by-rating` (All, 5 stars, etc.)
- Button: `back-to-dashboard` navigates to `/dashboard`

---

## 4. Data File Access Contracts

All data files reside in `data/` directory.

### 4.1 restaurants.txt
- Fields:
  - restaurant_id (int)
  - name (string)
  - cuisine (string)
  - address (string)
  - phone (string)
  - rating (float)
  - delivery_time (int, minutes)
  - min_order (float)
- Usage: Read for Dashboard, Restaurant Listing, Restaurant Menu, Reviews

### 4.2 menus.txt
- Fields:
  - item_id (int)
  - restaurant_id (int)
  - item_name (string)
  - category (string)
  - description (string)
  - price (float)
  - availability (int: 1=available, 0=unavailable)
- Usage: Read for Restaurant Menu, Item Details

### 4.3 cart.txt
- Fields:
  - cart_id (int)
  - item_id (int)
  - restaurant_id (int)
  - quantity (int)
  - added_date (YYYY-MM-DD string)
- Usage:
  - Read on Shopping Cart Page
  - Write on add to cart actions and shopping cart updates

### 4.4 orders.txt
- Fields:
  - order_id (int)
  - customer_name (string)
  - restaurant_id (int)
  - order_date (YYYY-MM-DD string)
  - total_amount (float)
  - status (string: e.g. Preparing, On the Way, Delivered)
  - delivery_address (string)
  - phone_number (string)
- Usage:
  - Read on Active Orders, Order Tracking
  - Write on Checkout new orders

### 4.5 order_items.txt
- Fields:
  - order_item_id (int)
  - order_id (int)
  - item_id (int)
  - quantity (int)
  - price (float)
- Usage:
  - Read on Order Tracking
  - Write on Checkout new orders

### 4.6 deliveries.txt
- Fields:
  - delivery_id (int)
  - order_id (int)
  - driver_name (string)
  - driver_phone (string)
  - vehicle_info (string)
  - status (string)
  - estimated_time (datetime string YYYY-MM-DD HH:MM)
- Usage: Read on Order Tracking

### 4.7 reviews.txt
- Fields:
  - review_id (int)
  - restaurant_id (int)
  - customer_name (string)
  - rating (int 1-5)
  - review_text (string)
  - review_date (YYYY-MM-DD string)
- Usage:
  - Read and write on Reviews Page

---

## 5. Navigation and Interaction Flow

- **Dashboard Page** (`GET /dashboard`):
  - `browse-restaurants-button` -> Redirects to `/restaurants`
  - `view-cart-button` -> Redirects to `/cart`
  - `active-orders-button` -> Redirects to `/active-orders`

- **Restaurant Listing Page** (`GET /restaurants`):
  - Search input and `cuisine-filter` filter shown restaurants dynamically.
  - Clicking `view-restaurant-button-{restaurant_id}` redirects to `/menu/{restaurant_id}`

- **Restaurant Menu Page** (`GET /menu/<restaurant_id>`):
  - Clicking `add-to-cart-button-{item_id}` triggers `POST /add-to-cart` with item_id and quantity=1.
  - Clicking `view-item-details-{item_id}` redirects to `/item/{item_id}`

- **Item Details Page** (`GET /item/<item_id>`):
  - User sets quantity via `quantity-input`.
  - `add-to-cart-button` triggers `POST /add-to-cart` with item_id and selected quantity.

- **Shopping Cart Page** (`GET /cart`):
  - Update quantities via `update-quantity-{item_id}` inputs and submit POST `/cart` to update.
  - Remove items via `remove-item-button-{item_id}` POST action on `/cart`.
  - `proceed-checkout-button` redirects to `/checkout`

- **Checkout Page** (`GET /checkout`):
  - User inputs customer name, delivery address, phone, payment method.
  - `place-order-button` submits POST `/checkout` to create new order and order items, clears cart, redirects to `/active-orders`

- **Active Orders Page** (`GET /active-orders`):
  - Use `status-filter` dropdown to filter displayed orders dynamically.
  - Clicking `track-order-button-{order_id}` redirects to `/track-order/{order_id}`
  - `back-to-dashboard` button redirects to `/dashboard`

- **Order Tracking Page** (`GET /track-order/<order_id>`):
  - Displays real-time status and driver info.
  - `back-to-orders` button redirects to `/active-orders`

- **Reviews Page** (`GET /reviews`):
  - Filter reviews using `filter-by-rating` dropdown.
  - Clicking `write-review-button` navigates to a review submission page (route not specified in requirements; optionally add /write-review).
  - `back-to-dashboard` button redirects to `/dashboard`

---

*End of Design Specification*