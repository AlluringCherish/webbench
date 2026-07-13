# Requirements Analysis for FoodDelivery Web Application

## 1. Page Routes and Titles

| Page Name             | Route (implied)           | Page Title                |
|-----------------------|---------------------------|---------------------------|
| Dashboard             | /dashboard (start page)   | Food Delivery Dashboard   |
| Restaurant Listing    | /restaurants              | Browse Restaurants        |
| Restaurant Menu      | /menu/{restaurant_id}      | Restaurant Menu           |
| Item Details         | /item/{item_id}            | Item Details              |
| Shopping Cart        | /cart                     | Shopping Cart             |
| Checkout             | /checkout                 | Checkout                  |
| Active Orders        | /active-orders            | Active Orders             |
| Order Tracking       | /track-order/{order_id}    | Track Order               |
| Reviews              | /reviews                  | Order Reviews             |


## 2. UI Element IDs

### 1. Dashboard Page
- ID: `dashboard-page` (Div) - Container for dashboard page
- ID: `featured-restaurants` (Div) - Featured restaurant recommendations
- ID: `browse-restaurants-button` (Button) - Navigate to restaurant listing page
- ID: `view-cart-button` (Button) - Navigate to shopping cart page
- ID: `active-orders-button` (Button) - Navigate to active orders page

### 2. Restaurant Listing Page
- ID: `restaurants-page` (Div) - Container for restaurant listing
- ID: `search-input` (Input) - Search restaurants by name or cuisine
- ID: `cuisine-filter` (Dropdown) - Filter by cuisine type
- ID: `restaurants-grid` (Div) - Grid displaying restaurant cards
- ID pattern: `view-restaurant-button-{restaurant_id}` (Button) - View restaurant menu for each restaurant

### 3. Restaurant Menu Page
- ID: `menu-page` (Div) - Container for menu page
- ID: `restaurant-name` (H1) - Display restaurant name
- ID: `restaurant-info` (Div) - Restaurant info (address, phone, rating)
- ID: `menu-items-grid` (Div) - Grid showing menu items
- ID pattern: `add-to-cart-button-{item_id}` (Button) - Add menu item to cart
- ID pattern: `view-item-details-{item_id}` (Button) - View item details

### 4. Item Details Page
- ID: `item-details-page` (Div) - Container for item details page
- ID: `item-name` (H1) - Display item name
- ID: `item-description` (Div) - Item description and ingredients
- ID: `item-price` (Div) - Item price
- ID: `quantity-input` (Input number) - Quantity selection
- ID: `add-to-cart-button` (Button) - Add selected quantity to cart

### 5. Shopping Cart Page
- ID: `cart-page` (Div) - Container for cart page
- ID: `cart-items-table` (Table) - Display cart items with name, quantity, price, subtotal
- ID pattern: `update-quantity-{item_id}` (Input number) - Update quantity for each cart item
- ID pattern: `remove-item-button-{item_id}` (Button) - Remove item from cart
- ID: `proceed-checkout-button` (Button) - Proceed to checkout
- ID: `total-amount` (Div) - Display total cart amount

### 6. Checkout Page
- ID: `checkout-page` (Div) - Container for checkout page
- ID: `customer-name` (Input) - Customer name input
- ID: `delivery-address` (Textarea) - Delivery address input
- ID: `phone-number` (Input) - Phone number input
- ID: `payment-method` (Dropdown) - Payment method selection
- ID: `place-order-button` (Button) - Confirm and place order

### 7. Active Orders Page
- ID: `active-orders-page` (Div) - Container for active orders
- ID: `orders-list` (Div) - List of active orders with order ID, restaurant, status, ETA
- ID pattern: `track-order-button-{order_id}` (Button) - View detailed tracking for each order
- ID: `status-filter` (Dropdown) - Filter orders by status
- ID: `back-to-dashboard` (Button) - Navigate back to dashboard

### 8. Order Tracking Page
- ID: `tracking-page` (Div) - Container for tracking page
- ID: `order-details` (Div) - Display complete order details and timeline
- ID: `delivery-driver-info` (Div) - Delivery driver info
- ID: `estimated-time` (Div) - Estimated delivery time
- ID: `order-items-list` (Div) - List of items in order
- ID: `back-to-orders` (Button) - Navigate back to active orders

### 9. Reviews Page
- ID: `reviews-page` (Div) - Container for reviews page
- ID: `reviews-list` (Div) - List all reviews with restaurant name, rating, text
- ID: `write-review-button` (Button) - Navigate to write review page
- ID: `filter-by-rating` (Dropdown) - Filter reviews by rating
- ID: `back-to-dashboard` (Button) - Navigate back to dashboard


## 3. User Interaction Flows

- Starting point is the **Dashboard Page** (`/dashboard`):
  - From dashboard, users can navigate to:
    - Restaurant Listing Page (`/restaurants`) via `browse-restaurants-button`
    - Shopping Cart Page (`/cart`) via `view-cart-button`
    - Active Orders Page (`/active-orders`) via `active-orders-button`

- On **Restaurant Listing Page**:
  - Users can search and filter restaurants
  - Clicking a restaurant's `view-restaurant-button-{restaurant_id}` navigates to Restaurant Menu Page for that restaurant

- On **Restaurant Menu Page**:
  - Users view menu items
  - Can add items to cart using `add-to-cart-button-{item_id}`
  - Can view detailed item info via `view-item-details-{item_id}`, leading to Item Details Page

- On **Item Details Page**:
  - User selects quantity using `quantity-input` and clicks `add-to-cart-button` to add item to cart

- On **Shopping Cart Page**:
  - User can update quantities with `update-quantity-{item_id}`
  - Remove items with `remove-item-button-{item_id}`
  - Proceed to checkout with `proceed-checkout-button`

- On **Checkout Page**:
  - User inputs delivery information and payment method
  - Completes order by clicking `place-order-button`

- On **Active Orders Page**:
  - User views current orders
  - Filters orders with `status-filter`
  - Views order tracking by clicking `track-order-button-{order_id}` to go to Order Tracking Page
  - Returns to Dashboard via `back-to-dashboard`

- On **Order Tracking Page**:
  - Displays detailed tracking info
  - Returns to Active Orders Page with `back-to-orders`

- On **Reviews Page**:
  - User views and filters reviews
  - Navigate to write review page via `write-review-button`
  - Returns to Dashboard with `back-to-dashboard`


## 4. Data File References and Usage

| Data File             | Pages Reading Data                                       | Pages Writing Data      | Usage Context                                                                                 |
|-----------------------|---------------------------------------------------------|------------------------|-----------------------------------------------------------------------------------------------|
| restaurants.txt       | Dashboard (featured restaurants), Restaurant Listing, Restaurant Menu, Reviews Page | None                   | Stores restaurant info: id, name, cuisine, address, phone, rating, delivery time, min order  |
| menus.txt             | Restaurant Menu, Item Details                             | None                   | Stores menu items per restaurant: item details, descriptions, prices, availability           |
| cart.txt              | Shopping Cart                                           | Shopping Cart (update), Item Details (add), Restaurant Menu (add) | Stores items added to cart with quantities and dates                                        |
| orders.txt            | Active Orders, Order Tracking                            | Checkout (new order)   | Stores order info: id, customer, restaurant, date, amount, status, address, phone             |
| order_items.txt       | Order Tracking                                          | Checkout (new order)   | Stores items per order: quantities and prices                                                |
| deliveries.txt        | Order Tracking                                          | None                   | Stores delivery details, driver info, vehicle, status, ETA                                  |
| reviews.txt           | Reviews Page                                           | Reviews Page (new reviews) | Stores customer reviews including ratings, text, dates                                       |


---

*End of Requirements Analysis*