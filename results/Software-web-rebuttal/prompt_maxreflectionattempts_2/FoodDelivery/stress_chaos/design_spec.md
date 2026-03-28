# FoodDelivery Design Specification

---

## 1. Flask Routes Specification

| Route Path                         | Function Name          | HTTP Method(s) | Template File Name         | Context Variables                                                                                                      |
|----------------------------------|------------------------|----------------|----------------------------|------------------------------------------------------------------------------------------------------------------------|
| /                                | redirect_dashboard     | GET            | None (Redirect)             | None                                                                                                                   |
| /dashboard                       | dashboard_page         | GET            | dashboard.html             | featured_restaurants (List[Dict])                                                                                      |
| /restaurants                    | restaurants_page       | GET            | restaurants.html            | restaurant_list (List[Dict]), filter_type (str / None)                                                                 |
| /menu/<int:restaurant_id>       | restaurant_menu_page   | GET            | menu.html                   | restaurant_info (Dict), menu_items (List[Dict])                                                                         |
| /item/<int:item_id>             | item_details_page      | GET            | item_details.html           | item_info (Dict)                                                                                                        |
| /cart                          | shopping_cart_page     | GET            | cart.html                   | cart_items (List[Dict]), total_amount (float)                                                                          |
| /checkout                      | checkout_page          | GET, POST      | checkout.html               | delivery_address (str), customer_name (str), phone_number (str), payment_method (str)                                   |
| /orders                       | orders_page            | GET            | active_orders.html          | active_orders (List[Dict]), filter_status (str)                                                                         |
| /tracking/<int:order_id>       | tracking_page          | GET            | tracking.html               | delivery_details (Dict), order_items (List[Dict]), estimated_time (str), order_timeline (List[Dict])                    |
| /reviews/<int:restaurant_id>   | reviews_page           | GET, POST      | reviews.html                | reviews_list (List[Dict]), restaurant_name (str)                                                                         |

---

## 2. HTML Template Specifications

### 1. Dashboard Page
- File path: templates/dashboard.html
- Page Title: Food Delivery Dashboard
- Elements:
  - ID: dashboard-page (Div)
  - ID: featured-restaurants (Div)
  - ID: browse-restaurants-button (Button) - Navigate to restaurants_page
  - ID: view-cart-button (Button) - Navigate to shopping_cart_page
  - ID: active-orders-button (Button) - Navigate to orders_page
- Layout Overview: Header with page title; main container displaying featured restaurants; navigation buttons for browsing restaurants, viewing cart, and active orders.
- Navigation Mappings:
  - browse-restaurants-button -> restaurants_page
  - view-cart-button -> shopping_cart_page
  - active-orders-button -> orders_page

### 2. Restaurant Listing Page
- File path: templates/restaurants.html
- Page Title: Browse Restaurants
- Elements:
  - ID: restaurants-page (Div)
  - ID: search-input (Input)
  - ID: cuisine-filter (Dropdown)
  - ID: restaurants-grid (Div)
  - ID Pattern: view-restaurant-button-{{ restaurant_id }} (Button)
- Layout Overview: Search input and cuisine filter dropdown on top; restaurants displayed in a grid below.
- Navigation Mappings:
  - view-restaurant-button-{{ restaurant_id }} -> restaurant_menu_page

### 3. Restaurant Menu Page
- File path: templates/menu.html
- Page Title: Restaurant Menu
- Elements:
  - ID: menu-page (Div)
  - ID: restaurant-name (H1)
  - ID: restaurant-info (Div)
  - ID: menu-items-grid (Div)
  - ID Pattern: add-to-cart-button-{{ item_id }} (Button)
  - ID Pattern: view-item-details-{{ item_id }} (Button)
- Layout Overview: Restaurant info on top; menu items presented in a grid with add to cart and details buttons.
- Navigation Mappings:
  - add-to-cart-button-{{ item_id }} -> shopping_cart_page (via add to cart action)
  - view-item-details-{{ item_id }} -> item_details_page

### 4. Item Details Page
- File path: templates/item_details.html
- Page Title: Item Details
- Elements:
  - ID: item-details-page (Div)
  - ID: item-name (H1)
  - ID: item-description (Div)
  - ID: item-price (Div)
  - ID: quantity-input (Input number)
  - ID: add-to-cart-button (Button)
- Layout Overview: Item information prominently displayed with quantity selector and add to cart button.
- Navigation Mappings:
  - add-to-cart-button -> shopping_cart_page (via add to cart action)

### 5. Shopping Cart Page
- File path: templates/cart.html
- Page Title: Shopping Cart
- Elements:
  - ID: cart-page (Div)
  - ID: cart-items-table (Table)
  - ID Pattern: update-quantity-{{ item_id }} (Input number)
  - ID Pattern: remove-item-button-{{ item_id }} (Button)
  - ID: proceed-checkout-button (Button)
  - ID: total-amount (Div)
- Layout Overview: Table listing cart items with quantity updates and remove options; total amount and checkout button at bottom.
- Navigation Mappings:
  - proceed-checkout-button -> checkout_page

### 6. Checkout Page
- File path: templates/checkout.html
- Page Title: Checkout
- Elements:
  - ID: checkout-page (Div)
  - ID: customer-name (Input)
  - ID: delivery-address (Textarea)
  - ID: phone-number (Input)
  - ID: payment-method (Dropdown)
  - ID: place-order-button (Button)
- Layout Overview: Form with fields for customer info and payment; place order button at bottom.
- Navigation Mappings:
  - place-order-button -> orders_page (after successful POST)

### 7. Active Orders Page
- File path: templates/active_orders.html
- Page Title: Active Orders
- Elements:
  - ID: active-orders-page (Div)
  - ID: orders-list (Div)
  - ID Pattern: track-order-button-{{ order_id }} (Button)
  - ID: status-filter (Dropdown)
  - ID: back-to-dashboard (Button)
- Layout Overview: List of active orders with filters; buttons to track individual orders; back button to dashboard.
- Navigation Mappings:
  - track-order-button-{{ order_id }} -> tracking_page
  - back-to-dashboard -> dashboard_page

### 8. Order Tracking Page
- File path: templates/tracking.html
- Page Title: Track Order
- Elements:
  - ID: tracking-page (Div)
  - ID: order-details (Div)
  - ID: delivery-driver-info (Div)
  - ID: estimated-time (Div)
  - ID: order-items-list (Div)
  - ID: back-to-orders (Button)
- Layout Overview: Detailed tracking with timeline, driver info, and items list.
- Navigation Mappings:
  - back-to-orders -> orders_page

### 9. Reviews Page
- File path: templates/reviews.html
- Page Title: Order Reviews
- Elements:
  - ID: reviews-page (Div)
  - ID: reviews-list (Div)
  - ID: write-review-button (Button)
  - ID: filter-by-rating (Dropdown)
  - ID: back-to-dashboard (Button)
- Layout Overview: Reviews listing with filter and write review button; back navigation.
- Navigation Mappings:
  - write-review-button -> write_review_page (if implemented)
  - back-to-dashboard -> dashboard_page

---

## 3. Data Schemas

### 1. restaurants.txt
- File Name: restaurants.txt
- Field Order & Names:
  ```
  restaurant_id|name|cuisine|address|phone|rating|delivery_time|min_order
  ```
- Description: Stores restaurant information including contact and delivery parameters.
- Data Types:
  - restaurant_id: int
  - name: string
  - cuisine: string
  - address: string
  - phone: string
  - rating: float
  - delivery_time: int (minutes)
  - min_order: float
- Example Data Rows:
  ```
  1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
  2|La Bella Italia|Italian|456 Oak Ave|555-0002|4.8|25|20.00
  3|Taj Mahal|Indian|789 Elm St|555-0003|4.6|35|18.00
  ```

### 2. menus.txt
- File Name: menus.txt
- Field Order & Names:
  ```
  item_id|restaurant_id|item_name|category|description|price|availability
  ```
- Description: Stores menu items for restaurants.
- Data Types:
  - item_id: int
  - restaurant_id: int
  - item_name: string
  - category: string
  - description: string
  - price: float
  - availability: int (1=available, 0=not)
- Example Data Rows:
  ```
  1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
  2|1|Spring Rolls|Appetizer|Crispy rolls with pork filling|8.99|1
  3|2|Spaghetti Carbonara|Pasta|Classic Italian pasta with cream sauce|14.99|1
  ```

### 3. cart.txt
- File Name: cart.txt
- Field Order & Names:
  ```
  cart_id|item_id|restaurant_id|quantity|added_date
  ```
- Description: Stores current shopping cart items.
- Data Types:
  - cart_id: int
  - item_id: int
  - restaurant_id: int
  - quantity: int
  - added_date: date string (YYYY-MM-DD)
- Example Data Rows:
  ```
  1|1|1|2|2025-01-15
  2|3|2|1|2025-01-16
  ```

### 4. orders.txt
- File Name: orders.txt
- Field Order & Names:
  ```
  order_id|customer_name|restaurant_id|order_date|total_amount|status|delivery_address|phone_number
  ```
- Description: Stores order details.
- Data Types:
  - order_id: int
  - customer_name: string
  - restaurant_id: int
  - order_date: date string (YYYY-MM-DD)
  - total_amount: float
  - status: string
  - delivery_address: string
  - phone_number: string
- Example Data Rows:
  ```
  1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
  2|Jane Smith|2|2025-01-14|14.99|On the Way|456 Oak Ave, LA|555-5678
  ```

### 5. order_items.txt
- File Name: order_items.txt
- Field Order & Names:
  ```
  order_item_id|order_id|item_id|quantity|price
  ```
- Description: Stores individual items within orders.
- Data Types:
  - order_item_id: int
  - order_id: int
  - item_id: int
  - quantity: int
  - price: float
- Example Data Rows:
  ```
  1|1|1|2|12.99
  2|1|2|1|8.99
  3|2|3|1|14.99
  ```

### 6. deliveries.txt
- File Name: deliveries.txt
- Field Order & Names:
  ```
  delivery_id|order_id|driver_name|driver_phone|vehicle_info|status|estimated_time
  ```
- Description: Stores delivery details including driver info and status.
- Data Types:
  - delivery_id: int
  - order_id: int
  - driver_name: string
  - driver_phone: string
  - vehicle_info: string
  - status: string
  - estimated_time: string (datetime)
- Example Data Rows:
  ```
  1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
  2|2|Sarah Williams|555-9002|Car|On the Way|2025-01-14 19:30
  ```

### 7. reviews.txt
- File Name: reviews.txt
- Field Order & Names:
  ```
  review_id|restaurant_id|customer_name|rating|review_text|review_date
  ```
- Description: Stores customer reviews for restaurants.
- Data Types:
  - review_id: int
  - restaurant_id: int
  - customer_name: string
  - rating: int
  - review_text: string
  - review_date: string (YYYY-MM-DD)
- Example Data Rows:
  ```
  1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
  2|2|Bob Williams|4|Great pasta, slightly delayed delivery.|2025-01-13
  3|3|Charlie Brown|5|Best Indian food in town!|2025-01-15
  ```
