# BookstoreOnline Application Design Specification

## Overview
BookstoreOnline is a Python-based local web application featuring book browsing, searching, purchasing, user account management, support chat, and administrative tools. Local JSON files store all data.

---

## Pages and UI Elements

### 1. Home Page (ID: page_home)
- **Purpose:** Welcome users, display featured books.
- **Elements:**
  - Header (id: header_home) with logo (logo_home) and navigation menu (nav_home).
  - Banner (banner_home) for promotions.
  - Featured Books section (featured_books) containing book cards (book_card_featured_{book_id}).
  - Footer (footer_home).

### 2. Book Catalog Page (ID: page_catalog)
- **Purpose:** Browse/search books by category.
- **Elements:**
  - Header (header_catalog), search bar (search_bar).
  - Sidebar with categories (sidebar_categories), category items (category_{name}).
  - Book list (book_list) with book cards (book_card_{book_id}).
  - Pagination (pagination_catalog).
  - Footer (footer_catalog).

### 3. Book Details Page (ID: page_book_details)
- **Purpose:** Show detailed info, reviews, and add to cart.
- **Elements:**
  - Header (header_book_details).
  - Cover image (book_cover), title (book_title), author (book_author), price (book_price), description (book_description).
  - Add to Cart button (btn_add_to_cart).
  - Reviews section (reviews_section) with review items (review_{review_id}).
  - Footer (footer_book_details).

### 4. Shopping Cart Page (ID: page_cart)
- **Purpose:** Manage cart items and proceed to checkout.
- **Elements:**
  - Header (header_cart).
  - Cart items list (cart_items), individual items (cart_item_{item_id}), quantity selectors (qty_selector_{item_id}), remove buttons (btn_remove_{item_id}).
  - Total price (cart_total).
  - Proceed to Checkout button (btn_checkout).
  - Footer (footer_cart).

### 5. User Account Page (ID: page_account)
- **Purpose:** User profile and order history management.
- **Elements:**
  - Header (header_account).
  - User info form (user_info) with inputs: name (input_name), email (input_email), password (input_password), save changes button (btn_save_account).
  - Order history section (order_history), order entries (order_{order_id}).
  - Logout button (btn_logout).
  - Footer (footer_account).

### 6. Checkout Page (ID: page_checkout)
- **Purpose:** Input shipping/payment info, finalize order.
- **Elements:**
  - Header (header_checkout).
  - Shipping info form (form_shipping): name (input_ship_name), address (input_ship_address), phone (input_ship_phone).
  - Payment info form (form_payment): card number (input_card_number), expiry (input_expiry), CVC (input_cvc).
  - Order summary (order_summary).
  - Confirm Purchase button (btn_confirm_purchase).
  - Footer (footer_checkout).

### 7. Order Confirmation Page (ID: page_order_confirmation)
- **Purpose:** Display order confirmation and details.
- **Elements:**
  - Header (header_order_confirmation).
  - Confirmation message (msg_confirmation), order number (order_number).
  - Order summary (order_summary).
  - Continue shopping link (link_continue_shopping).
  - Footer (footer_order_confirmation).

### 8. Support Chat Page (ID: page_support_chat)
- **Purpose:** Real-time chat support.
- **Elements:**
  - Header (header_support_chat).
  - Chat window (chat_window) with messages (message_{msg_id}).
  - Message input box (input_chat_message).
  - Send button (btn_send_message).
  - Footer (footer_support_chat).

### 9. Admin Dashboard Page (ID: page_admin_dashboard)
- **Purpose:** Manage inventory, orders, and users.
- **Elements:**
  - Header (header_admin_dashboard).
  - Navigation menu (nav_admin_menu) with: inventory (link_inventory), orders (link_orders), users (link_users).
  - Summary panels (panel_{panel_name}).
  - Content area (admin_main).
  - Footer (footer_admin_dashboard).

---

## Local Text Data Storage Format

Text content is stored in `local_text_data.json` supporting localization:

```json
{
  "page_home": {"welcome_message": "Welcome to BookstoreOnline!", "featured_books_title": "Featured Books"},
  "page_catalog": {"search_placeholder": "Search books...", "categories_title": "Categories"},
  "page_book_details": {"add_to_cart_button": "Add to Cart", "reviews_title": "Customer Reviews"},
  "page_cart": {"title": "Your Shopping Cart", "checkout_button": "Proceed to Checkout"},
  "page_account": {"profile_title": "Your Account", "logout_button": "Logout"},
  "page_checkout": {"shipping_info_title": "Shipping Information", "payment_info_title": "Payment Details", "confirm_purchase_button": "Confirm Purchase"},
  "page_order_confirmation": {"confirmation_message": "Thank you for your order!", "continue_shopping_link": "Continue Shopping"},
  "page_support_chat": {"chat_placeholder": "Type your message...", "send_button": "Send"},
  "page_admin_dashboard": {"inventory_link": "Manage Inventory", "orders_link": "Manage Orders", "users_link": "Manage Users"}
}
```

## Data Storage Files and Schemas

- `books.json`:
  - Fields: `book_id`, `title`, `author`, `category`, `price`, `description`, `cover_image_path`, `reviews` (list of `{review_id, username, rating, comment}`).

- `users.json`:
  - Fields: `user_id`, `name`, `email`, `password_hash`, `order_history` (list of order ids).

- `orders.json`:
  - Fields: `order_id`, `user_id`, `items` (list of `{book_id, quantity}`), `total_price`, `shipping_info` (object), `payment_info` (object), `status` (string).

---

## Notes
- All elements have unique, descriptive IDs.
- Responsive design and accessibility features will be key.
- Local JSON files allow easy data management and localization.

---

This document completes the BookstoreOnline design specification with full coverage of pages, UI elements, and data storage format.