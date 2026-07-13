# Backend Design for FoodDelivery Web Application

---

## Section 1: Flask Routes and APIs

### General Notes
- Base URL prefix for API endpoints: `/api`
- All endpoints support JSON request/response format unless otherwise noted.
- No user authentication is implemented as per requirements.

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
- **Input:**
  - `restaurant_id` in URL path
- **Response:** JSON list of menu items with availability flag.


### 4. Item Details Page
- **Route:** `/api/menu_items/<int:item_id>`
- **Method:** GET
- **Purpose:** Retrieve detailed information for a specific menu item.
- **Input:**
  - `item_id` in URL path
- **Response:** JSON with item details including ingredients and nutritional info (as included in description).


### 5. Shopping Cart Page
- **Route:** `/api/cart`
- **Method:** GET
- **Purpose:** Get all items currently in the cart.
- **Input:** None
- **Response:** JSON list of cart items.

- **Route:** `/api/cart`
- **Method:** POST
- **Purpose:** Add an item to the cart.
- **Input:** JSON with fields:
  - `item_id` (int)
  - `restaurant_id` (int)
  - `quantity` (int)
- **Response:** JSON confirmation with new cart item ID.

- **Route:** `/api/cart/<int:cart_id>`
- **Method:** PUT
- **Purpose:** Update quantity of a cart item.
- **Input:** JSON with updated `quantity` (int).
- **Response:** JSON confirmation.

- **Route:** `/api/cart/<int:cart_id>`
- **Method:** DELETE
- **Purpose:** Remove an item from the cart.
- **Input:** None
- **Response:** JSON confirmation.


### 6. Checkout Page
- **Route:** `/api/orders`
- **Method:** POST
- **Purpose:** Place an order with delivery information and cart content.
- **Input:** JSON with fields:
  - `customer_name` (string)
  - `delivery_address` (string)
  - `phone_number` (string)
  - `payment_method` (string, e.g., Credit Card, Cash, PayPal)
- **Process:** Reads cart, validates minimum order requirements, calculates total amount, creates order and order items.
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
- **Input:**
  - `order_id` in URL path
- **Response:** JSON with order details, delivery driver info, estimated time, and order items.


### 9. Reviews Page
- **Route:** `/api/reviews`
- **Method:** GET
- **Purpose:** Retrieve list of all reviews, with optional filter by rating.
- **Input (Query Parameter):**
  - `rating` (int, optional): Filter reviews by rating stars.
- **Response:** JSON list of reviews.

- **Route:** `/api/reviews`
- **Method:** POST
- **Purpose:** Submit a new review for a restaurant.
- **Input:** JSON with fields:
  - `restaurant_id` (int)
  - `customer_name` (string)
  - `rating` (int, 1-5)
  - `review_text` (string)
- **Response:** JSON confirmation with new review ID.


---

## Section 2: Data Models and Local Text File Schemas

### 1. Restaurants Data (restaurants.txt)
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


### 2. Menus Data (menus.txt)
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


### 3. Cart Data (cart.txt)
- **Schema:**
  - cart_id (int)
  - item_id (int)
  - restaurant_id (int)
  - quantity (int)
  - added_date (str, ISO date `YYYY-MM-DD`)
- **Delimiter:** `|`
- **Example:** `1|1|1|2|2025-01-15`


### 4. Orders Data (orders.txt)
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


### 5. Order Items Data (order_items.txt)
- **Schema:**
  - order_item_id (int)
  - order_id (int) — foreign key to orders
  - item_id (int)
  - quantity (int)
  - price (float)
- **Delimiter:** `|`
- **Example:** `1|1|1|2|12.99`


### 6. Deliveries Data (deliveries.txt)
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


### 7. Reviews Data (reviews.txt)
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


### Data Handling Logic (File Operations)
- Read operations:
  - Parse text files line by line.
  - Convert each line into dictionaries or data classes keyed by IDs.
- Write operations:
  - Overwrite or append in the text files as needed.
  - Use atomic write patterns (write temp then replace) if possible to avoid partial writes.
- Update operations:
  - Read all data,
  - Modify the relevant entry
  - Write back all the data.

- All file reads and writes are done synchronously within Flask route handlers.

---

## Section 3: Backend Data Validation and Business Logic

### Validation Rules
- Ensure quantity > 0 when adding or updating cart items.
- Validate restaurant and item IDs exist prior to operations.
- Check availability of menu item before adding to cart; reject if unavailable.
- Minimum order enforcement:
  - During checkout, sum item.prices * quantity per restaurant.
  - If sum < restaurant.min_order, disallow placing order for that restaurant.
- Validate correct data types and presence for all required fields on input.


### Business Logic
- Cart maintains items without authentication; it is session scoped or global depending on implementation.
- Orders:
  - Upon placement, generate unique incremental order_id.
  - Compute total_amount from order items.
  - Set order status as "Preparing" initially.
- Deliveries:
  - Linked to orders with statuses progressing through Preparing, On the Way, Delivered.
  - Estimated delivery times are tracked and updated in deliveries.txt.
- Reviews:
  - New reviews append with unique incremental review_id.
  - Ratings constrained between 1 and 5.


### Order Status and Delivery Tracking
- Order statuses: Preparing -> On the Way -> Delivered
- Delivery status in deliveries.txt mirrors order status.
- API endpoints provide filtered views and detailed tracking info.

---

# End of backend_design.md
