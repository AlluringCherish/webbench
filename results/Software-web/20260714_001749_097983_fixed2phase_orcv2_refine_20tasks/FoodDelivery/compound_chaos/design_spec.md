# FoodDelivery Web Application Design Specification

---

## Section 1: Page Layouts and Element IDs

### 1. Dashboard Page
- Page Title: Food Delivery Dashboard
- Container ID: dashboard-page (Div)
- Elements:
  - featured-restaurants (Div): Displays featured restaurant recommendations.
  - browse-restaurants-button (Button): Navigates to Restaurant Listing Page.
  - view-cart-button (Button): Navigates to Shopping Cart Page.
  - active-orders-button (Button): Navigates to Active Orders Page.

### 2. Restaurant Listing Page
- Page Title: Browse Restaurants
- Container ID: restaurants-page (Div)
- Elements:
  - search-input (Input): Field to search restaurants by name or cuisine.
  - cuisine-filter (Dropdown): Filter restaurants by cuisine (Chinese, Italian, Indian, American, etc.).
  - restaurants-grid (Div): Grid for displaying restaurant cards.
  - view-restaurant-button-{restaurant_id} (Button): View restaurant menu; one per restaurant card.

### 3. Restaurant Menu Page
- Page Title: Restaurant Menu
- Container ID: menu-page (Div)
- Elements:
  - restaurant-name (H1): Displays restaurant name.
  - restaurant-info (Div): Displays restaurant address, phone, rating.
  - menu-items-grid (Div): Grid showing menu items with photos, names, descriptions, prices.
  - add-to-cart-button-{item_id} (Button): Add menu item to cart; one per menu item.
  - view-item-details-{item_id} (Button): View item details; one per menu item.

### 4. Item Details Page
- Page Title: Item Details
- Container ID: item-details-page (Div)
- Elements:
  - item-name (H1): Displays item name.
  - item-description (Div): Shows description and ingredients.
  - item-price (Div): Displays item price.
  - quantity-input (Input number): Quantity selection before adding to cart.
  - add-to-cart-button (Button): Adds item with quantity to cart.

### 5. Shopping Cart Page
- Page Title: Shopping Cart
- Container ID: cart-page (Div)
- Elements:
  - cart-items-table (Table): Displays cart items - name, quantity, price, subtotal.
  - update-quantity-{item_id} (Input number): Update quantity per cart item.
  - remove-item-button-{item_id} (Button): Remove item from cart.
  - proceed-checkout-button (Button): Proceed to checkout page.
  - total-amount (Div): Displays total cart amount.

### 6. Checkout Page
- Page Title: Checkout
- Container ID: checkout-page (Div)
- Elements:
  - customer-name (Input): Enter customer name.
  - delivery-address (Textarea): Enter delivery address.
  - phone-number (Input): Enter phone number.
  - payment-method (Dropdown): Select payment method (Credit Card, Cash, PayPal).
  - place-order-button (Button): Confirm and place the order.

### 7. Active Orders Page
- Page Title: Active Orders
- Container ID: active-orders-page (Div)
- Elements:
  - orders-list (Div): Displays active orders with order ID, restaurant, status, ETA.
  - track-order-button-{order_id} (Button): View tracking details.
  - status-filter (Dropdown): Filter orders by status (All, Preparing, On the Way, Delivered).
  - back-to-dashboard (Button): Return to dashboard.

### 8. Order Tracking Page
- Page Title: Track Order
- Container ID: tracking-page (Div)
- Elements:
  - order-details (Div): Shows complete order details and timeline.
  - delivery-driver-info (Div): Driver name, phone, vehicle info.
  - estimated-time (Div): Displays estimated delivery time.
  - order-items-list (Div): List of ordered items.
  - back-to-orders (Button): Return to Active Orders Page.

### 9. Reviews Page
- Page Title: Order Reviews
- Container ID: reviews-page (Div)
- Elements:
  - reviews-list (Div): List of reviews with restaurant name, rating, and text.
  - write-review-button (Button): Navigate to write review page.
  - filter-by-rating (Dropdown): Filter reviews by rating (All, 5 stars, 4 stars, etc.).
  - back-to-dashboard (Button): Return to dashboard.

---

## Section 2: Navigation Flow

- Application starts at Dashboard Page (dashboard-page).
- From Dashboard:
  - browse-restaurants-button -> Restaurant Listing Page (restaurants-page).
  - view-cart-button -> Shopping Cart Page (cart-page).
  - active-orders-button -> Active Orders Page (active-orders-page).

- From Restaurant Listing Page:
  - view-restaurant-button-{restaurant_id} -> Restaurant Menu Page (menu-page) for selected restaurant.

- From Restaurant Menu Page:
  - add-to-cart-button-{item_id} -> Adds item to Shopping Cart.
  - view-item-details-{item_id} -> Item Details Page (item-details-page) for selected item.

- From Item Details Page:
  - add-to-cart-button -> Add selected quantity to Shopping Cart.

- From Shopping Cart Page:
  - update-quantity-{item_id} -> Updates item quantity in cart.
  - remove-item-button-{item_id} -> Removes item from cart.
  - proceed-checkout-button -> Checkout Page (checkout-page).

- From Checkout Page:
  - place-order-button -> Places order and navigates to Active Orders Page.

- From Active Orders Page:
  - track-order-button-{order_id} -> Order Tracking Page (tracking-page).
  - status-filter -> Filters orders by status.
  - back-to-dashboard -> Dashboard Page.

- From Order Tracking Page:
  - back-to-orders -> Active Orders Page.

- From Reviews Page:
  - write-review-button -> Write Review Page (not detailed in initial requirements, assumed as separate or modal).
  - filter-by-rating -> Filters reviews.
  - back-to-dashboard -> Dashboard Page.

---

## Section 3: Data Storage Formats

### 1. Restaurants Data
- File Name: restaurants.txt
- Schema: restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
- Fields:
  - restaurant_id: integer
  - name: string
  - cuisine: string
  - address: string
  - phone: string
  - rating: float
  - delivery_time: integer (minutes)
  - min_order: float (currency)
- Example:
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00

### 2. Menus Data
- File Name: menus.txt
- Schema: item_id|restaurant_id|item_name|category|description|price|availability
- Fields:
  - item_id: integer
  - restaurant_id: integer
  - item_name: string
  - category: string
  - description: string
  - price: float
  - availability: boolean (1 for available, 0 for unavailable)
- Example:
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1

### 3. Cart Data
- File Name: cart.txt
- Schema: cart_id|item_id|restaurant_id|quantity|added_date
- Fields:
  - cart_id: integer
  - item_id: integer
  - restaurant_id: integer
  - quantity: integer
  - added_date: date (YYYY-MM-DD)
- Example:
  1|1|1|2|2025-01-15

### 4. Orders Data
- File Name: orders.txt
- Schema: order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
- Fields:
  - order_id: integer
  - customer_name: string
  - restaurant_id: integer
  - order_date: date (YYYY-MM-DD)
  - total_amount: float
  - status: string (e.g., Delivered, On the Way, Preparing)
  - delivery_address: string
  - phone_number: string
- Example:
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234

### 5. Order Items Data
- File Name: order_items.txt
- Schema: order_item_id|order_id|item_id|quantity|price
- Fields:
  - order_item_id: integer
  - order_id: integer
  - item_id: integer
  - quantity: integer
  - price: float
- Example:
  1|1|1|2|12.99

### 6. Deliveries Data
- File Name: deliveries.txt
- Schema: delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
- Fields:
  - delivery_id: integer
  - order_id: integer
  - driver_name: string
  - driver_phone: string
  - vehicle_info: string
  - status: string
  - estimated_time: datetime string (YYYY-MM-DD HH:MM)
- Example:
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45

### 7. Reviews Data
- File Name: reviews.txt
- Schema: review_id|restaurant_id|customer_name|rating|review_text|review_date
- Fields:
  - review_id: integer
  - restaurant_id: integer
  - customer_name: string
  - rating: integer (1-5)
  - review_text: string
  - review_date: date (YYYY-MM-DD)
- Example:
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12

---

This specification document fully defines the page structures, navigation logic, and local data formats for the FoodDelivery Python web application as required.