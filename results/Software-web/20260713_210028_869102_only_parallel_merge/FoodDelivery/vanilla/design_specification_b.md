# Design Specification B for FoodDelivery Web Application

---

## Overview

This document specifies the detailed backend Flask routes, page titles, element IDs, data file usage, and user navigation pathways for the FoodDelivery app with nine pages, all based on provided requirements. It is intended for developers to implement the application precisely.

---

# 1. Flask Routes and Views

| Route Path               | Function Name          | HTTP Methods | Template Used             | Description & Context Variables                                       |
|--------------------------|-----------------------|--------------|---------------------------|------------------------------------------------------------------------|
| `/`                      | `root_redirect`        | GET          | N/A                       | Redirects to `/dashboard`                                             |
| `/dashboard`             | `dashboard`           | GET          | `dashboard.html`          | Featured restaurants, popular cuisines
Context: featured_restaurants (list of dicts)                    |
| `/restaurants`           | `restaurants`         | GET          | `restaurants.html`        | Search and filter restaurants
Context: restaurants (list), search_query, cuisine_filter                |
| `/restaurant/<int:id>`   | `restaurant_menu`     | GET          | `menu.html`               | Menu items for restaurant
Context: restaurant (dict), menu_items (list)                                   |
| `/item/<int:item_id>`    | `item_details`        | GET, POST    | `item_details.html`       | Detailed menu item info
Context: item (dict)                                                       |
| `/cart`                  | `shopping_cart`       | GET          | `cart.html`               | Items in cart
Context: cart_items (list), total_amount                                      |
| `/checkout`              | `checkout`            | GET, POST    | `checkout.html`           | Delivery info form
Context: form fields (prefill if needed)                                    |
| `/orders/active`         | `active_orders`       | GET          | `active_orders.html`      | List of active orders with filter
Context: orders (list), status_filter                      |
| `/order/track/<int:id>`  | `order_tracking`      | GET          | `tracking.html`           | Detailed tracking info
Context: order (dict), delivery_info (dict), order_items                  |
| `/reviews`               | `reviews`             | GET          | `reviews.html`            | Reviews and filter
Context: reviews (list), rating_filter                                  |

---

# 2. Pages Titles and Elements

Each page specifies a page title (for `<title>` and `<h1>` or main header) plus element IDs.

---

## 2.1 Dashboard Page
- **Page Title:** Food Delivery Dashboard
- **Element IDs:**
  - `dashboard-page` (Div container for the dashboard)
  - `featured-restaurants` (Div for featured restaurants display)
  - `browse-restaurants-button` (Button to `/restaurants`)
  - `view-cart-button` (Button to `/cart`)
  - `active-orders-button` (Button to `/orders/active`)

Navigation:
- Clicking `browse-restaurants-button` leads to `/restaurants`
- Clicking `view-cart-button` leads to `/cart`
- Clicking `active-orders-button` leads to `/orders/active`

---

## 2.2 Restaurant Listing Page
- **Page Title:** Browse Restaurants
- **Element IDs:**
  - `restaurants-page` (Div container)
  - `search-input` (Input for search queries)
  - `cuisine-filter` (Dropdown for cuisine types)
  - `restaurants-grid` (Div holding restaurant cards)
  - `view-restaurant-button-{restaurant_id}` (Buttons to view menus)

Navigation:
- Search and cuisine filter update restaurants shown
- Clicking `view-restaurant-button-{restaurant_id}` goes to `/restaurant/<restaurant_id>`

---

## 2.3 Restaurant Menu Page
- **Page Title:** Restaurant Menu
- **Element IDs:**
  - `menu-page` (Div container)
  - `restaurant-name` (H1 showing restaurant name)
  - `restaurant-info` (Div for address, phone, rating)
  - `menu-items-grid` (Div with menu item cards)
  - `add-to-cart-button-{item_id}` (Buttons to add items to cart)
  - `view-item-details-{item_id}` (Buttons to see item details)

Navigation:
- `add-to-cart-button-{item_id}` adds item to cart and stays on menu
- `view-item-details-{item_id}` navigates to `/item/<item_id>`

---

## 2.4 Item Details Page
- **Page Title:** Item Details
- **Element IDs:**
  - `item-details-page` (Div container)
  - `item-name` (H1 item name)
  - `item-description` (Div with description, ingredients)
  - `item-price` (Div price display)
  - `quantity-input` (Input number to select quantity)
  - `add-to-cart-button` (Button to add selected quantity to cart)

Navigation:
- `add-to-cart-button` adds item(s) to cart and redirects to `/cart`

---

## 2.5 Shopping Cart Page
- **Page Title:** Shopping Cart
- **Element IDs:**
  - `cart-page` (Div container)
  - `cart-items-table` (Table with cart items: name, qty, price, subtotal)
  - `update-quantity-{item_id}` (Input number to update quantity)
  - `remove-item-button-{item_id}` (Button to remove item)
  - `proceed-checkout-button` (Button to go to `/checkout`)
  - `total-amount` (Div showing cart total)

Navigation:
- Quantity updates and removals modify cart
- `proceed-checkout-button` navigates to `/checkout`

---

## 2.6 Checkout Page
- **Page Title:** Checkout
- **Element IDs:**
  - `checkout-page` (Div container)
  - `customer-name` (Input for name)
  - `delivery-address` (Textarea for address)
  - `phone-number` (Input for phone)
  - `payment-method` (Dropdown for payment choices)
  - `place-order-button` (Button to place order)

Navigation:
- `place-order-button` submits order and redirects to `/orders/active`

---

## 2.7 Active Orders Page
- **Page Title:** Active Orders
- **Element IDs:**
  - `active-orders-page` (Div container)
  - `orders-list` (Div listing active orders)
  - `track-order-button-{order_id}` (Buttons to track each order)
  - `status-filter` (Dropdown to filter orders by status)
  - `back-to-dashboard` (Button to `/dashboard`)

Navigation:
- Clicking `track-order-button-{order_id}` goes to `/order/track/<order_id>`
- `back-to-dashboard` navigates back to `/dashboard`

---

## 2.8 Order Tracking Page
- **Page Title:** Track Order
- **Element IDs:**
  - `tracking-page` (Div container)
  - `order-details` (Div with order details and timeline)
  - `delivery-driver-info` (Div with driver name, phone, vehicle)
  - `estimated-time` (Div with estimated delivery time)
  - `order-items-list` (Div listing ordered items)
  - `back-to-orders` (Button to `/orders/active`)

Navigation:
- `back-to-orders` returns to Active Orders page

---

## 2.9 Reviews Page
- **Page Title:** Order Reviews
- **Element IDs:**
  - `reviews-page` (Div container)
  - `reviews-list` (Div with list of reviews)
  - `write-review-button` (Button to navigate to review writing page - external page not described)
  - `filter-by-rating` (Dropdown to filter reviews by star rating)
  - `back-to-dashboard` (Button to `/dashboard`)

Navigation:
- `write-review-button`: (Note: Not specified in requirements - assumed navigates to some review form page or modal)
- `back-to-dashboard` navigates to dashboard

---

# 3. Data File Usage by Page

### General Notes on Data Files:
- All data files are located in `data/` folder.
- Fields separated by pipe `|` character.

### 3.1 Dashboard Page
- Uses `restaurants.txt` to show featured restaurants (subset selected by developer or based on ratings).
- Fields used: `restaurant_id`, `name`, `cuisine`, `rating`, `delivery_time` for display.

### 3.2 Restaurant Listing Page
- Uses `restaurants.txt` for full list.
- Fields used: `restaurant_id`, `name`, `cuisine`, `rating`, `delivery_time`.
- Search and filter apply on `name` and `cuisine`.

### 3.3 Restaurant Menu Page
- Uses `restaurants.txt` to get restaurant info by `restaurant_id`.
- Uses `menus.txt` filtered by `restaurant_id` and `availability=1` for menu items.
- Fields for menu items: `item_id`, `item_name`, `category`, `description`, `price`.

### 3.4 Item Details Page
- Uses `menus.txt` filtered by `item_id` for item details.
- Fields: `item_name`, `description`, `price`, plus additional assumed ingredient and nutrition info loaded?
(Alert: Not defined in data, assume can extend menus.txt or static data.)

### 3.5 Shopping Cart Page
- Uses `cart.txt` filtered for current session/user cart.
- Uses `menus.txt` and `restaurants.txt` to get item and restaurant details.
- Displays cart items with quantity, price, subtotal.

### 3.6 Checkout Page
- Does not require data file reads prior to order placement.
- On place order, writes new entry to `orders.txt`, and corresponding items to `order_items.txt`.

### 3.7 Active Orders Page
- Uses `orders.txt` for current orders filtering by status (Preparing, On the Way).
- Uses `restaurants.txt` to show restaurant names by `restaurant_id`.

### 3.8 Order Tracking Page
- Uses `orders.txt` for order details by `order_id`.
- Uses `deliveries.txt` for delivery driver and status info by `order_id`.
- Uses `order_items.txt` for items in order.
- Uses `menus.txt` for item names/prices in order.

### 3.9 Reviews Page
- Uses `reviews.txt` for all reviews.
- Uses `restaurants.txt` to display restaurant names associated with reviews.

---

# 4. User Navigation Pathways Summary

- Landing `/` redirects to `/dashboard`.
- Dashboard buttons lead to `/restaurants`, `/cart`, `/orders/active`.
- Restaurant Listing: search/filter updates the displayed list. Each restaurant button leads to `/restaurant/<id>`.
- Restaurant Menu: buttons to add to cart (same page) or view item details `/item/<item_id>`.
- Item Details: add item to cart (redirect to `/cart`).
- Cart page: update quantities, remove items, proceed to `/checkout`.
- Checkout: submit order, then redirect to `/orders/active`.
- Active Orders: filter by status, track order leads to `/order/track/<order_id>`, back button returns to dashboard.
- Tracking page: back to active orders.
- Reviews: back to dashboard; write review button navigates to review form (not covered in requirements).

---

# End of Design Specification B
