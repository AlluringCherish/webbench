# Frontend Design Specification for FoodDelivery Web Application

---

## Section 1: HTML Template Specifications

### 1. Dashboard Template
- **Filename:** dashboard.html (Jinja2 template)
- **Page Title:** Food Delivery Dashboard
- **Main Container ID:** dashboard-page (div)
- **UI Elements:**
  - featured-restaurants (div) : Show featured restaurants
  - browse-restaurants-button (button) : Navigate to Restaurant Listing page
  - view-cart-button (button) : Navigate to Shopping Cart page
  - active-orders-button (button) : Navigate to Active Orders page

### 2. Restaurant Listing Template
- **Filename:** restaurants.html
- **Page Title:** Browse Restaurants
- **Main Container ID:** restaurants-page (div)
- **UI Elements:**
  - search-input (input, text) : Enter restaurant name or cuisine for search
  - cuisine-filter (select/dropdown) : Filter restaurants by cuisine type
  - restaurants-grid (div) : Grid layout showing restaurant cards
  - view-restaurant-button-{{restaurant_id}} (button) : Button on each restaurant card to open Restaurant Menu page

### 3. Restaurant Menu Template
- **Filename:** menu.html
- **Page Title:** Restaurant Menu
- **Main Container ID:** menu-page (div)
- **UI Elements:**
  - restaurant-name (h1) : Display restaurant name
  - restaurant-info (div) : Show address, phone, and rating
  - menu-items-grid (div) : Grid of menu items
  - add-to-cart-button-{{item_id}} (button) : Add specific menu item to cart
  - view-item-details-{{item_id}} (button) : View details for menu item

### 4. Item Details Template
- **Filename:** item_details.html
- **Page Title:** Item Details
- **Main Container ID:** item-details-page (div)
- **UI Elements:**
  - item-name (h1) : Item name
  - item-description (div) : Description and ingredients
  - item-price (div) : Price display
  - quantity-input (input, number) : Quantity selection
  - add-to-cart-button (button) : Add the selected quantity to cart

### 5. Shopping Cart Template
- **Filename:** cart.html
- **Page Title:** Shopping Cart
- **Main Container ID:** cart-page (div)
- **UI Elements:**
  - cart-items-table (table) : Displays cart items with columns for name, quantity, price, subtotal
  - update-quantity-{{item_id}} (input, number) : Update quantity per cart item
  - remove-item-button-{{item_id}} (button) : Remove item from cart
  - proceed-checkout-button (button) : Proceed to checkout page
  - total-amount (div) : Shows total cart amount

### 6. Checkout Template
- **Filename:** checkout.html
- **Page Title:** Checkout
- **Main Container ID:** checkout-page (div)
- **UI Elements:**
  - customer-name (input, text) : Customer name input
  - delivery-address (textarea) : Delivery address input
  - phone-number (input, text) : Customer phone number input
  - payment-method (select/dropdown) : Payment method choice
  - place-order-button (button) : Submit order

### 7. Active Orders Template
- **Filename:** active_orders.html
- **Page Title:** Active Orders
- **Main Container ID:** active-orders-page (div)
- **UI Elements:**
  - orders-list (div) : List of active orders with order ID, restaurant, status, ETA
  - track-order-button-{{order_id}} (button) : View tracking details for each order
  - status-filter (select/dropdown) : Filter orders by status
  - back-to-dashboard (button) : Navigate back to Dashboard

### 8. Order Tracking Template
- **Filename:** tracking.html
- **Page Title:** Track Order
- **Main Container ID:** tracking-page (div)
- **UI Elements:**
  - order-details (div) : Display order summary and timeline
  - delivery-driver-info (div) : Show driver name, phone, vehicle info
  - estimated-time (div) : Estimated delivery time
  - order-items-list (div) : Items in the order
  - back-to-orders (button) : Navigate back to Active Orders page

### 9. Reviews Template
- **Filename:** reviews.html
- **Page Title:** Order Reviews
- **Main Container ID:** reviews-page (div)
- **UI Elements:**
  - reviews-list (div) : List of all reviews (restaurant name, rating, text)
  - write-review-button (button) : Navigate to write review page
  - filter-by-rating (select/dropdown) : Filter reviews by rating
  - back-to-dashboard (button) : Navigate back to Dashboard

---

## Section 2: Context Variables and Data Binding

### General Guidelines
- Context variables are passed as dictionaries and lists from backend (Python).
- Variable names are descriptive and match page context.
- Lists contain dicts/objects representing entities (restaurants, menu items, orders, reviews).

### 1. Dashboard Template
- featured_restaurants : `List[Dict]`
  - Each dict: {id: int, name: str, cuisine: str, rating: float, delivery_time: int, logo_url: str}
- Used to populate #featured-restaurants div with cards or list items.

### 2. Restaurant Listing Template
- restaurants : `List[Dict]`
  - Each dict: {id: int, name: str, cuisine: str, address: str, phone: str, rating: float, delivery_time: int, min_order: float}
- selected_cuisine : `str` or `None`
- search_term : `str` or empty
- Used to build restaurants-grid with cards showing name, cuisine, rating, delivery time.

### 3. Restaurant Menu Template
- restaurant : `Dict`
  - {id: int, name: str, address: str, phone: str, rating: float}
- menu_items : `List[Dict]`
  - Each dict: {item_id: int, name: str, category: str, description: str, price: float, availability: bool, photo_url: str (optional)}
- Render restaurant info and menu-items-grid accordingly.

### 4. Item Details Template
- item : `Dict`
  - {id: int, name: str, description: str, ingredients: str (optional), price: float}
- Quantity selected through input defaults to 1.

### 5. Shopping Cart Template
- cart_items : `List[Dict]`
  - Each dict: {item_id: int, name: str, quantity: int, price: float, subtotal: float}
- total_amount : float
- Used to populate cart-items-table rows and total-amount display.

### 6. Checkout Template
- No pre-filled fields unless persisted from cart checkout flow.

### 7. Active Orders Template
- active_orders : `List[Dict]`
  - Each dict: {order_id: int, restaurant_name: str, status: str, eta: str}
- filter_status : `str`

### 8. Order Tracking Template
- order_details : `Dict`
  - {order_id: int, date: str, total_amount: float, status: str}
- delivery_driver : `Dict`
  - {name: str, phone: str, vehicle_info: str}
- estimated_time : str
- order_items : `List[Dict]`
  - Each dict: {item_name: str, quantity: int, price: float}

### 9. Reviews Template
- reviews : `List[Dict]`
  - Each dict: {restaurant_name: str, rating: int, review_text: str, customer_name: str, review_date: str}
- selected_rating_filter : `str`

---

## Section 3: Navigation and User Flow

### Navigation Buttons and Links
- #browse-restaurants-button (Dashboard) -> /restaurants
- #view-cart-button (Dashboard) -> /cart
- #active-orders-button (Dashboard) -> /active-orders

- #view-restaurant-button-{{restaurant_id}} (Restaurants Listing) -> /menu/{{restaurant_id}}
- #add-to-cart-button-{{item_id}} (Menu) -> Add item to cart action (stay on page or update UI)
- #view-item-details-{{item_id}} (Menu) -> /item/{{item_id}}

- #add-to-cart-button (Item Details) -> Add selected quantity to cart

- #proceed-checkout-button (Cart) -> /checkout

- #place-order-button (Checkout) -> Submit order, redirect to Dashboard or confirmation page

- #track-order-button-{{order_id}} (Active Orders) -> /tracking/{{order_id}}
- #back-to-dashboard (Active Orders, Reviews) -> /dashboard
- #back-to-orders (Tracking) -> /active-orders

- #write-review-button (Reviews) -> /write-review (not detailed in requirements but implied)

### Filtering Controls
- #cuisine-filter (Restaurants) changes displayed restaurants
- #search-input (Restaurants) dynamically filters restaurants by name/cuisine
- #status-filter (Active Orders) filters orders by status
- #filter-by-rating (Reviews) filters reviews by rating

### Back Navigation
- Back buttons included on Active Orders, Tracking, Reviews to Dashboard or relevant previous pages.

---

This completes the detailed frontend interface and navigation design for the FoodDelivery application.