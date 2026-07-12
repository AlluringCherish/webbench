# Design Specification for RestaurantReservation Web Application

---

## 1. Flask Routes Specification

### Route: `/`
- **Function Name:** `root`
- **HTTP Methods:** GET
- **Template Rendered:** None (Redirect)
- **Behavior:** Redirects to `/dashboard`
- **Context Variables:** None
- **POST Form Fields:** None

---

### Route: `/dashboard`
- **Function Name:** `dashboard`
- **HTTP Methods:** GET
- **Template Rendered:** `dashboard.html`
- **Context Variables:**
  - `username`: str
  - `featured_dishes`: list of dict with keys:
    - `dish_id`: int
    - `name`: str
    - `price`: float
  - `upcoming_reservations`: list of dict with keys:
    - `reservation_id`: int
    - `date`: str (YYYY-MM-DD)
    - `time`: str (HH:MM)
    - `party_size`: int
    - `status`: str
- **POST Form Fields:** None

---

### Route: `/menu`
- **Function Name:** `menu`
- **HTTP Methods:** GET
- **Template Rendered:** `menu.html`
- **Context Variables:**
  - `menu_categories`: list of str
  - `menu_items`: list of dict with keys:
    - `dish_id`: int
    - `name`: str
    - `category`: str
    - `price`: float
    - `description`: str
- **POST Form Fields:** None

---

### Route: `/dish/<int:dish_id>`
- **Function Name:** `dish_details`
- **HTTP Methods:** GET
- **Template Rendered:** `dish_details.html`
- **Context Variables:**
  - `dish`: dict with keys:
    - `dish_id`: int
    - `name`: str
    - `price`: float
    - `description`: str
- **POST Form Fields:** None

---

### Route: `/make_reservation`
- **Function Name:** `make_reservation`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `make_reservation.html` (GET), Redirect or reload on POST
- **Context Variables:** None on GET
- **POST Form Fields:**
  - `guest_name`: str
  - `party_size`: int (values 1-10)
  - `reservation_date`: str (YYYY-MM-DD)

---

### Route: `/my_reservations`
- **Function Name:** `my_reservations`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `my_reservations.html`
- **Context Variables:**
  - `reservations`: list of dict with keys:
    - `reservation_id`: int
    - `date`: str (YYYY-MM-DD)
    - `time`: str (HH:MM)
    - `party_size`: int
    - `status`: str
- **POST Form Fields:**
  - `cancel_reservation_id`: int (reservation_id targeted for cancellation)

---

### Route: `/waitlist`
- **Function Name:** `waitlist`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `waitlist.html`
- **Context Variables:**
  - `user_position`: int or None (current waitlist position)
- **POST Form Fields:**
  - `party_size`: int

---

### Route: `/my_reviews`
- **Function Name:** `my_reviews`
- **HTTP Methods:** GET
- **Template Rendered:** `my_reviews.html`
- **Context Variables:**
  - `reviews`: list of dict with keys:
    - `review_id`: int
    - `dish_name`: str
    - `rating`: int
    - `review_text`: str
- **POST Form Fields:** None

---

### Route: `/write_review`
- **Function Name:** `write_review`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `write_review.html`
- **Context Variables:**
  - `dishes`: list of dict with keys:
    - `dish_id`: int
    - `name`: str
- **POST Form Fields:**
  - `dish_id`: int
  - `rating`: int (1-5)
  - `review_text`: str

---

### Route: `/profile`
- **Function Name:** `profile`
- **HTTP Methods:** GET, POST
- **Template Rendered:** `profile.html`
- **Context Variables:**
  - `user_info`: dict with keys:
    - `username`: str
    - `email`: str
- **POST Form Fields:**
  - `email`: str

---

## 2. HTML Template Specifications

### 2.1 Dashboard Page
- **Template Filename:** `templates/dashboard.html`
- **Page Title:** `Restaurant Dashboard`
- **Element IDs:**
  - `dashboard-page` (Div): Container for dashboard page.
  - `welcome-message` (H1): Displays welcome message with username.
  - `make-reservation-button` (Button): Navigate to Make Reservation page.
  - `view-menu-button` (Button): Navigate to Menu page.
  - `back-to-dashboard` (Button): Refreshes the dashboard.
  - `my-reservations-button` (Button): Navigate to My Reservations page.
  - `my-reviews-button` (Button): Navigate to My Reviews page.
  - `waitlist-button` (Button): Navigate to Waitlist page.
  - `profile-button` (Button): Navigate to User Profile page.
- **Context Variables:**
  - `username`: str
  - `featured_dishes`: list of dict with keys `dish_id` (int), `name` (str), `price` (float)
  - `upcoming_reservations`: list of dict with keys `reservation_id` (int), `date` (str), `time` (str), `party_size` (int), `status` (str)
- **Navigation/Button Metadata:**
  - `make-reservation-button` -> `url_for('make_reservation')`
  - `view-menu-button` -> `url_for('menu')`
  - `back-to-dashboard` -> `url_for('dashboard')`
  - `my-reservations-button` -> `url_for('my_reservations')`
  - `my-reviews-button` -> `url_for('my_reviews')`
  - `waitlist-button` -> `url_for('waitlist')`
  - `profile-button` -> `url_for('profile')`

---

### 2.2 Menu Page
- **Template Filename:** `templates/menu.html`
- **Page Title:** `Restaurant Menu`
- **Element IDs:**
  - `menu-page` (Div): Container for menu page.
  - `menu-grid` (Div): Grid displaying dish cards.
  - Dynamic buttons: `view-dish-button-{{ dish.dish_id }}` (Button) on each dish card.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Context Variables:**
  - `menu_categories`: list of str
  - `menu_items`: list of dict with keys `dish_id` (int), `name` (str), `category` (str), `price` (float), `description` (str)
- **Navigation/Button Metadata:**
  - Each `view-dish-button-{{ dish.dish_id }}` -> `url_for('dish_details', dish_id=dish.dish_id)`
  - `back-to-dashboard` -> `url_for('dashboard')`

---

### 2.3 Dish Details Page
- **Template Filename:** `templates/dish_details.html`
- **Page Title:** `Dish Details`
- **Element IDs:**
  - `dish-details-page` (Div): Container.
  - `dish-name` (H1): Display dish name.
  - `dish-price` (Div): Display dish price.
  - `back-to-menu` (Button): Navigate back to menu.
- **Context Variables:**
  - `dish`: dict with keys `dish_id` (int), `name` (str), `price` (float), `description` (str)
- **Navigation/Button Metadata:**
  - `back-to-menu` -> `url_for('menu')`

---

### 2.4 Make Reservation Page
- **Template Filename:** `templates/make_reservation.html`
- **Page Title:** `Make Reservation`
- **Element IDs:**
  - `reservation-page` (Div): Container.
  - `guest-name` (Input): Guest name input field.
  - `party-size` (Dropdown): Party size selection (1-10).
  - `reservation-date` (Input type=date): Reservation date picker.
  - `submit-reservation-button` (Button): Submit reservation.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Context Variables:** None (on GET)
- **Form Details:**
  - **Action:** POST to `url_for('make_reservation')`
  - **Fields:** `guest_name`, `party_size`, `reservation_date`
- **Navigation/Button Metadata:**
  - `back-to-dashboard` -> `url_for('dashboard')`

---

### 2.5 My Reservations Page
- **Template Filename:** `templates/my_reservations.html`
- **Page Title:** `My Reservations`
- **Element IDs:**
  - `my-reservations-page` (Div): Container.
  - `reservations-table` (Table): Displays reservations.
  - Dynamic buttons: `cancel-reservation-button-{{ reservation.reservation_id }}` (Button) for each upcoming reservation.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Context Variables:**
  - `reservations`: list of dict with keys `reservation_id` (int), `date` (str), `time` (str), `party_size` (int), `status` (str)
- **Form Details:**
  - **Action:** POST to `url_for('my_reservations')` for cancellation
  - **Fields:** `cancel_reservation_id`
- **Navigation/Button Metadata:**
  - `back-to-dashboard` -> `url_for('dashboard')`

---

### 2.6 Waitlist Page
- **Template Filename:** `templates/waitlist.html`
- **Page Title:** `Waitlist`
- **Element IDs:**
  - `waitlist-page` (Div): Container.
  - `waitlist-party-size` (Dropdown): Select party size.
  - `join-waitlist-button` (Button): Submit join waitlist.
  - `user-position` (Div): Display user's waitlist position.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Context Variables:**
  - `user_position`: int or None
- **Form Details:**
  - **Action:** POST to `url_for('waitlist')`
  - **Fields:** `party_size`
- **Navigation/Button Metadata:**
  - `back-to-dashboard` -> `url_for('dashboard')`

---

### 2.7 My Reviews Page
- **Template Filename:** `templates/my_reviews.html`
- **Page Title:** `My Reviews`
- **Element IDs:**
  - `reviews-page` (Div): Container.
  - `reviews-list` (Div): Displays list of reviews.
  - `write-new-review-button` (Button): Navigate to Write Review page.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Context Variables:**
  - `reviews`: list of dict with keys `review_id` (int), `dish_name` (str), `rating` (int), `review_text` (str)
- **Navigation/Button Metadata:**
  - `write-new-review-button` -> `url_for('write_review')`
  - `back-to-dashboard` -> `url_for('dashboard')`

---

### 2.8 Write Review Page
- **Template Filename:** `templates/write_review.html`
- **Page Title:** `Write Review`
- **Element IDs:**
  - `write-review-page` (Div): Container.
  - `select-dish` (Dropdown): Select dish to review.
  - `rating-input` (Dropdown): Select rating (1-5 stars).
  - `review-text` (Textarea): Review text input.
  - `submit-review-button` (Button): Submit review.
  - `back-to-reviews` (Button): Navigate back to My Reviews.
- **Context Variables:**
  - `dishes`: list of dict with keys `dish_id` (int), `name` (str)
- **Form Details:**
  - **Action:** POST to `url_for('write_review')`
  - **Fields:** `dish_id`, `rating`, `review_text`
- **Navigation/Button Metadata:**
  - `back-to-reviews` -> `url_for('my_reviews')`

---

### 2.9 User Profile Page
- **Template Filename:** `templates/profile.html`
- **Page Title:** `My Profile`
- **Element IDs:**
  - `profile-page` (Div): Container.
  - `profile-username` (Div): Display username (non-editable).
  - `profile-email` (Input): Email input field.
  - `update-profile-button` (Button): Submit profile updates.
  - `back-to-dashboard` (Button): Navigate back to dashboard.
- **Context Variables:**
  - `user_info`: dict with keys `username` (str), `email` (str)
- **Form Details:**
  - **Action:** POST to `url_for('profile')`
  - **Fields:** `email`
- **Navigation/Button Metadata:**
  - `back-to-dashboard` -> `url_for('dashboard')`

---

## 3. Data File Schemas

Data files stored in `data` directory, pipe (`|`) delimited, no header lines.

### 3.1 Users Data (`data/users.txt`)
- **Format:** `username|email|phone|full_name`
- **Fields:**
  - `username`: str
  - `email`: str
  - `phone`: str
  - `full_name`: str
- **Description:** Stores user registration and contact details.
- **Example Rows:**
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

---

### 3.2 Menu Items Data (`data/menu.txt`)
- **Format:** `dish_id|name|category|price|description|ingredients|dietary|avg_rating`
- **Fields:**
  - `dish_id`: int
  - `name`: str
  - `category`: str
  - `price`: float
  - `description`: str
  - `ingredients`: str (comma-separated list)
  - `dietary`: str
  - `avg_rating`: float
- **Description:** Stores all menu dishes with details.
- **Example Rows:**
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

---

### 3.3 Reservations Data (`data/reservations.txt`)
- **Format:** `reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status`
- **Fields:**
  - `reservation_id`: int
  - `username`: str
  - `guest_name`: str
  - `phone`: str
  - `email`: str
  - `party_size`: int
  - `date`: str (YYYY-MM-DD)
  - `time`: str (HH:MM)
  - `special_requests`: str (may be empty)
  - `status`: str
- **Description:** Stores all reservations made by users.
- **Example Rows:**
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

---

### 3.4 Waitlist Data (`data/waitlist.txt`)
- **Format:** `waitlist_id|username|party_size|join_time|status`
- **Fields:**
  - `waitlist_id`: int
  - `username`: str
  - `party_size`: int
  - `join_time`: str (YYYY-MM-DD HH:MM:SS)
  - `status`: str
- **Description:** Stores waitlist queue data.
- **Example Rows:**
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

---

### 3.5 Reviews Data (`data/reviews.txt`)
- **Format:** `review_id|username|dish_id|rating|review_text|review_date`
- **Fields:**
  - `review_id`: int
  - `username`: str
  - `dish_id`: int
  - `rating`: int (1-5)
  - `review_text`: str
  - `review_date`: str (YYYY-MM-DD)
- **Description:** Stores user reviews of dishes.
- **Example Rows:**
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

---

# End of Design Specification
