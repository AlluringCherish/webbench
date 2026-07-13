# FoodDelivery Web Application Integrated Design Specification

---

## Section 1: Integrated Flask Routes and APIs

### General Notes
- Base URL prefix for API endpoints: `/api`
- All endpoints support JSON request/response format unless otherwise noted.
- No user authentication is implemented.

---

### 1. Dashboard Page
- **Route:** `/api/dashboard`
- **Method:** GET
- **Purpose:** Retrieve featured restaurants and popular cuisines for display.
- **Input:** None
- **Response:** JSON containing lists of featured restaurants and cuisine types.

### 2. Restaurant Listing Page
- **Route:** `/api/restaurants`
- **Method:** GET
- **Purpose:** Retrieve all restaurants with optional filters.
- **Input (Query Parameters):**
  - `search` (string, optional): Search term for restaurant name or cuisine.
  - `cuisine` (string, optional): Filter by cuisine type (e.g., Chinese, Italian).
- **Response:** JSON list of restaurants matching filters.

### 3. Restaurant Menu Page
- **Route:** `/api/restaurants/<int:restaurant_id>/menu`
- **Method:** GET
- **Purpose:** Retrieve menu items for specific restaurant.
- **Input:** `restaurant_id` in URL path
- **Response:** JSON list of menu items with availability flag.

### 4. Item Details Page
- **Route:** `/api/menu_items/<int:item_id>`
- **Method:** GET
- **Purpose:** Retrieve detailed information for a specific menu item.
- **Input:** `item_id` in URL path
- **Response:** JSON with item details including description, ingredients, and nutritional info.

### 5. Shopping Cart Page
- **Route:** `/api/cart`
  - GET: Retrieve all items in the cart.
    - Input: None
    - Response: JSON list of cart items.
  - POST: Add an item to the cart.
    - Input JSON: `item_id` (int), `restaurant_id` (int), `quantity` (int)
    - Response: JSON confirmation with new cart item ID.

- **Route:** `/api/cart/<int:cart_id>`
  - PUT: Update quantity of a cart item.
    - Input JSON: updated `quantity` (int)
    - Response: JSON confirmation.
  - DELETE: Remove an item from the cart.
    - Input: None
    - Response: JSON confirmation.

### 6. Checkout Page
- **Route:** `/api/orders`
- **Method:** POST
- **Purpose:** Place an order with delivery information and cart content.
- **Input JSON:**
  - `customer_name` (string)
  - `delivery_address` (string)
  - `phone_number` (string)
  - `payment_method` (string, e.g., Credit Card, Cash, PayPal)
- **Process:** Reads cart, validates minimum order requirements per restaurant, calculates total amount, creates order and order items.
- **Response:** JSON with new order ID and status.

### 7. Active Orders Page
- **Route:** `/api/orders/active`
- **Method:** GET
- **Purpose:** Retrieve all active orders (status != Delivered), with optional status filter.
- **Input (Query Parameter):**
  - `status` (string, optional): Filter by order status (Preparing, On the Way, Delivered, All defaults to all except Delivered)
- **Response:** JSON list of active orders with ETA.

### 8. Order Tracking Page
- **Route:** `/api/orders/<int:order_id>/tracking`
- **Method:** GET
- **Purpose:** Retrieve detailed tracking info for a specific order.
- **Input:** `order_id` in URL path
- **Response:** JSON with order details, delivery driver info, estimated time, and order items.

### 9. Reviews Page
- **Route:** `/api/reviews`
  - GET: Retrieve list of all reviews, optionally filtered by rating.
    - Input (Query Parameter): `rating` (int, optional)
    - Response: JSON list of reviews.
  - POST: Submit a new review for a restaurant.
    - Input JSON: `restaurant_id` (int), `customer_name` (string), `rating` (int, 1-5), `review_text` (string)
    - Response: JSON confirmation with new review ID.

---

## Section 2: Unified Data Model and Local Text Files Schema

### 1. Restaurants Data (`restaurants.txt`)
- **Schema:**
  - restaurant_id (int)
  - name (str)
  - cuisine (str)
  - address (str)
  - phone (str)
  - rating (float)
  - delivery_time (int, minutes)
  - min_order (float)
- **Delimiter:** `|`
- **Example:** `1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00`

### 2. Menus Data (`menus.txt`)
- **Schema:**
  - item_id (int)
  - restaurant_id (int) — foreign key to restaurants
  - item_name (str)
  - category (str)
  - description (str)
  - price (float)
  - availability (int as boolean, 1=available, 0=unavailable)
- **Delimiter:** `|`
- **Example:** `1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1`

### 3. Cart Data (`cart.txt`)
- **Schema:**
  - cart_id (int)
  - item_id (int)
  - restaurant_id (int)
  - quantity (int)
  - added_date (str, ISO date `YYYY-MM-DD`)
- **Delimiter:** `|`
- **Example:** `1|1|1|2|2025-01-15`

### 4. Orders Data (`orders.txt`)
- **Schema:**
  - order_id (int)
  - customer_name (str)
  - restaurant_id (int)
  - order_date (str, ISO date)
  - total_amount (float)
  - status (str: Preparing, On the Way, Delivered)
  - delivery_address (str)
  - phone_number (str)
- **Delimiter:** `|`
- **Example:** `1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234`

### 5. Order Items Data (`order_items.txt`)
- **Schema:**
  - order_item_id (int)
  - order_id (int) — foreign key to orders
  - item_id (int)
  - quantity (int)
  - price (float)
- **Delimiter:** `|`
- **Example:** `1|1|1|2|12.99`

### 6. Deliveries Data (`deliveries.txt`)
- **Schema:**
  - delivery_id (int)
  - order_id (int)
  - driver_name (str)
  - driver_phone (str)
  - vehicle_info (str)
  - status (str: Preparing, On the Way, Delivered)
  - estimated_time (str, datetime format e.g. `YYYY-MM-DD HH:MM`)
- **Delimiter:** `|`
- **Example:** `1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45`

### 7. Reviews Data (`reviews.txt`)
- **Schema:**
  - review_id (int)
  - restaurant_id (int)
  - customer_name (str)
  - rating (int, 1-5)
  - review_text (str)
  - review_date (str, ISO date)
- **Delimiter:** `|`
- **Example:** `1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12`

### Data Relationships
- Menus link to Restaurants via `restaurant_id`.
- Cart items link to Menu items and Restaurants via `item_id` and `restaurant_id`.
- Orders link to Restaurants.
- Order Items link to Orders and Menu Items.
- Deliveries link to Orders.
- Reviews link to Restaurants.

### Data Handling Logic
- File read/write operations are synchronous.
- Read: parse lines to dicts keyed by IDs.
- Write: overwrite or append with atomic pattern as feasible.
- Update: read all, modify, rewrite fully.

---

## Section 3: Combined Frontend Template and Navigation Specifications

### 1. HTML Templates and UI Elements

#### Dashboard Template
- **Filename:** dashboard.html
- **Page Title:** Food Delivery Dashboard
- **Main Container ID:** dashboard-page
- **UI Elements:**
  - featured-restaurants (div): Shows featured restaurant cards
  - browse-restaurants-button (button): Navigates to /restaurants
  - view-cart-button (button): Navigates to /cart
  - active-orders-button (button): Navigates to /active-orders

#### Restaurant Listing Template
- **Filename:** restaurants.html
- **Page Title:** Browse Restaurants
- **Main Container ID:** restaurants-page
- **UI Elements:**
  - search-input (input, text): Search restaurants by name or cuisine
  - cuisine-filter (select/dropdown): Filter restaurants by cuisine type
  - restaurants-grid (div): Grid showing restaurant cards with logo, name, rating, delivery time
  - view-restaurant-button-{{restaurant_id}} (button): Navigate to /menu/{{restaurant_id}}

#### Restaurant Menu Template
- **Filename:** menu.html
- **Page Title:** Restaurant Menu
- **Main Container ID:** menu-page
- **UI Elements:**
  - restaurant-name (h1): Restaurant name
  - restaurant-info (div): Address, phone, rating
  - menu-items-grid (div): Grid of menu items
  - add-to-cart-button-{{item_id}} (button): Adds item to cart
  - view-item-details-{{item_id}} (button): Navigate to /item/{{item_id}}

#### Item Details Template
- **Filename:** item_details.html
- **Page Title:** Item Details
- **Main Container ID:** item-details-page
- **UI Elements:**
  - item-name (h1): Item name
  - item-description (div): Description and ingredients
  - item-price (div): Price
  - quantity-input (input, number): Quantity selector, default 1
  - add-to-cart-button (button): Add item with selected quantity to cart

#### Shopping Cart Template
- **Filename:** cart.html
- **Page Title:** Shopping Cart
- **Main Container ID:** cart-page
- **UI Elements:**
  - cart-items-table (table): Cart items with columns name, quantity, price, subtotal
  - update-quantity-{{item_id}} (input, number): Update quantity for each item
  - remove-item-button-{{item_id}} (button): Remove item from cart
  - proceed-checkout-button (button): Navigate to /checkout
  - total-amount (div): Total cart amount

#### Checkout Template
- **Filename:** checkout.html
- **Page Title:** Checkout
- **Main Container ID:** checkout-page
- **UI Elements:**
  - customer-name (input, text)
  - delivery-address (textarea)
  - phone-number (input, text)
  - payment-method (select/dropdown)
  - place-order-button (button): Submit order

#### Active Orders Template
- **Filename:** active_orders.html
- **Page Title:** Active Orders
- **Main Container ID:** active-orders-page
- **UI Elements:**
  - orders-list (div): List of active orders with ID, restaurant, status, ETA
  - track-order-button-{{order_id}} (button): Navigate to /tracking/{{order_id}}
  - status-filter (select/dropdown): Filter orders by status
  - back-to-dashboard (button): Navigate to /dashboard

#### Order Tracking Template
- **Filename:** tracking.html
- **Page Title:** Track Order
- **Main Container ID:** tracking-page
- **UI Elements:**
  - order-details (div): Order summary and timeline
  - delivery-driver-info (div): Driver name, phone, vehicle info
  - estimated-time (div): Estimated delivery time
  - order-items-list (div): Items in order
  - back-to-orders (button): Navigate back to /active-orders

#### Reviews Template
- **Filename:** reviews.html
- **Page Title:** Order Reviews
- **Main Container ID:** reviews-page
- **UI Elements:**
  - reviews-list (div): List of reviews with restaurant name, rating, review text
  - write-review-button (button): Navigate to /write-review (implied)
  - filter-by-rating (select/dropdown): Filter reviews by rating
  - back-to-dashboard (button): Navigate to /dashboard

---

### 2. Context Variables and Data Binding

- Context variables passed from backend as dictionaries/lists.
- Variable names aligned with backend data fields.

#### Dashboard
- featured_restaurants: List[Dict]
  - Fields: id, name, cuisine, rating, delivery_time, logo_url

#### Restaurant Listing
- restaurants: List[Dict]
  - Fields: id, name, cuisine, address, phone, rating, delivery_time, min_order
- selected_cuisine: str or None
- search_term: str

#### Restaurant Menu
- restaurant: Dict {id, name, address, phone, rating}
- menu_items: List[Dict] {item_id, name, category, description, price, availability (bool), photo_url (optional)}

#### Item Details
- item: Dict {id, name, description, ingredients (optional), price}
- quantity defaults to 1

#### Shopping Cart
- cart_items: List[Dict] {item_id, name, quantity, price, subtotal}
- total_amount: float

#### Checkout
- No pre-filled context variables required

#### Active Orders
- active_orders: List[Dict] {order_id, restaurant_name, status, eta}
- filter_status: str

#### Order Tracking
- order_details: Dict {order_id, date, total_amount, status}
- delivery_driver: Dict {name, phone, vehicle_info}
- estimated_time: str
- order_items: List[Dict] {item_name, quantity, price}

#### Reviews
- reviews: List[Dict] {restaurant_name, rating, review_text, customer_name, review_date}
- selected_rating_filter: str

---

### 3. Navigation and User Flow Mapping

| UI Element ID                          | Action / Navigation                      | Backend Route Supported                  |
|--------------------------------------|----------------------------------------|-----------------------------------------|
| #browse-restaurants-button           | Navigate to Restaurant Listing page    | GET `/api/restaurants`                   |
| #view-cart-button                    | Navigate to Shopping Cart page          | GET `/api/cart`                          |
| #active-orders-button                | Navigate to Active Orders page          | GET `/api/orders/active`                 |
| #view-restaurant-button-{{restaurant_id}} | Navigate to Restaurant Menu for that restaurant | GET `/api/restaurants/<restaurant_id>/menu` |
| #add-to-cart-button-{{item_id}}     | Add menu item to cart (stay on page)   | POST `/api/cart`                         |
| #view-item-details-{{item_id}}      | Navigate to Item Details page           | GET `/api/menu_items/<item_id>`          |
| #add-to-cart-button (on Item Details) | Add selected quantity to cart           | POST `/api/cart`                         |
| #proceed-checkout-button             | Navigate to Checkout page               | POST `/api/orders` on submitting order  |
| #place-order-button                  | Submit order and confirm                | POST `/api/orders`                      |
| #track-order-button-{{order_id}}    | Navigate to Order Tracking page         | GET `/api/orders/<order_id>/tracking`   |
| #back-to-dashboard                   | Navigate back to Dashboard page         | GET `/api/dashboard` (if needed)        |
| #back-to-orders                     | Navigate back to Active Orders page     | GET `/api/orders/active`                 |
| #write-review-button                 | Navigate to Write Review page (implied)| POST `/api/reviews` (for submission)    |

### Filtering Controls
- #cuisine-filter filters restaurants using `/api/restaurants?cuisine=...`
- #search-input filters restaurants using `/api/restaurants?search=...`
- #status-filter filters active orders using `/api/orders/active?status=...`
- #filter-by-rating filters reviews using `/api/reviews?rating=...`

---

This comprehensive integration ensures consistent route naming, data schema, frontend element usage, context variables, and user navigation flows needed to develop the FoodDelivery web app.

# End of design_spec.md
