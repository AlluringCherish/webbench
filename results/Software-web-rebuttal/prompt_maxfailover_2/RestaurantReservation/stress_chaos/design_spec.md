# RestaurantReservation - Design Specification

---

## Section 1: Flask Routes Specification (Backend Developer)

| URL Path                     | Function Name          | HTTP Methods | Template File             | Context Variables (types & structures)                                                                                          | Request Form Fields (POST)                                                  |
|------------------------------|------------------------|--------------|---------------------------|------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| `/`                          | root                   | GET          | Redirects to `/dashboard` | None                                                                                                 | None                                                                       |
| `/dashboard`                 | dashboard              | GET          | `dashboard.html`          | username: str                                                                                        | None                                                                       |
| `/menu`                     | menu                   | GET          | `menu.html`               | dishes: list of dict with fields {dish_id: str, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | None                                                                       |
| `/dish/<string:dish_id>`     | dish_details           | GET          | `dish_details.html`       | dish: dict with fields {dish_id: str, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}          | None                                                                       |
| `/reservation`              | reservation            | GET, POST    | `reservation.html`        | None                                                                                                 | guest_name: str, party_size: int, reservation_date: str (date), phone: str, email: str, special_requests: str                           |
| `/my_reservations`          | my_reservations        | GET          | `my_reservations.html`    | reservations: list of dict with fields {reservation_id: str, username: str, guest_name: str, phone: str, email: str, party_size: int, date: str, time: str, special_requests: str, status: str} | None                                                                       |
| `/cancel_reservation/<string:reservation_id>` | cancel_reservation      | POST         | Redirects to `/my_reservations` | None                                                                                                 | None                                                                       |
| `/waitlist`                 | waitlist               | GET, POST    | `waitlist.html`           | waitlist: list of dict with fields {waitlist_id: str, username: str, party_size: int, join_time: str, status: str}; user_position: int (optional)       | party_size: int                                                            |
| `/my_reviews`               | my_reviews             | GET          | `my_reviews.html`         | reviews: list of dict with fields {review_id: str, username: str, dish_id: str, rating: int, review_text: str, review_date: str}                         | None                                                                       |
| `/write_review`             | write_review           | GET, POST    | `write_review.html`       | dishes: list of dict with fields {dish_id: str, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | dish_id: str, rating: int, review_text: str                                 |
| `/profile`                  | profile                | GET, POST    | `profile.html`            | user: dict with fields {username: str, email: str, phone: str, full_name: str}                                                                       | email: str                                                                 |

---

## Section 2: HTML Template Specifications (Frontend Developer)

### templates/dashboard.html
- Page Title: Restaurant Dashboard
- Main H1: Welcome message with username
- Element IDs:
  - `dashboard-page` (Div) - Container for the dashboard page
  - `welcome-message` (H1) - Displays welcome message with username
  - `make-reservation-button` (Button) - Navigate to `reservation` route
  - `view-menu-button` (Button) - Navigate to `menu` route
  - `my-reservations-button` (Button) - Navigate to `my_reservations` route
  - `my-reviews-button` (Button) - Navigate to `my_reviews` route
  - `waitlist-button` (Button) - Navigate to `waitlist` route
  - `profile-button` (Button) - Navigate to `profile` route
  - `back-to-dashboard` (Button) - Reload `dashboard` route
- Context Variables:
  - `username`: str
- Navigation Mappings:
  - `make-reservation-button` → `reservation`
  - `view-menu-button` → `menu`
  - `my-reservations-button` → `my_reservations`
  - `my-reviews-button` → `my_reviews`
  - `waitlist-button` → `waitlist`
  - `profile-button` → `profile`
  - `back-to-dashboard` → `dashboard`

### templates/menu.html
- Page Title: Restaurant Menu
- Main H1: Restaurant Menu
- Element IDs:
  - `menu-page` (Div) - Container for the menu page
  - `menu-grid` (Div) - Grid of dish cards
  - `view-dish-button-{{ dish.dish_id }}` (Button) - For each dish card, navigate to `dish_details` with dish_id
  - `back-to-dashboard` (Button) - Navigate to `dashboard` route
- Context Variables:
  - `dishes`: list of dicts (see Section 1)
- Navigation Mappings:
  - `view-dish-button-{{ dish.dish_id }}` → `dish_details`
  - `back-to-dashboard` → `dashboard`

### templates/dish_details.html
- Page Title: Dish Details
- Main H1: `dish.name`
- Element IDs:
  - `dish-details-page` (Div) - Container of dish details
  - `dish-name` (H1) - Displays dish name
  - `dish-price` (Div) - Displays dish price
  - `back-to-menu` (Button) - Navigate back to `menu` route
- Context Variables:
  - `dish`: dict (see Section 1)
- Navigation Mappings:
  - `back-to-menu` → `menu`

### templates/reservation.html
- Page Title: Make Reservation
- Main H1: Make Reservation
- Element IDs:
  - `reservation-page` (Div) - Container of reservation form
  - `guest-name` (Input text) - Input for guest name; name="guest_name"
  - `party-size` (Dropdown select) - Select party size 1-10; name="party_size"
  - `reservation-date` (Input date/time) - Input for date/time; name="reservation_date"
  - `phone` (Input text) - Input for phone number; name="phone"
  - `email` (Input text) - Input for email; name="email"
  - `special-requests` (Textarea) - Input for special requests; name="special_requests"
  - `submit-reservation-button` (Button) - Submit form
  - `back-to-dashboard` (Button) - Navigate to `dashboard` route
- Context Variables:
  - None
- Form Action:
  - Method: POST, action to `/reservation`
  - Inputs named as above
- Navigation Mappings:
  - `back-to-dashboard` → `dashboard`

### templates/my_reservations.html
- Page Title: My Reservations
- Main H1: My Reservations
- Element IDs:
  - `my-reservations-page` (Div) - Container
  - `reservations-table` (Table) - Displays rows of reservations with columns: Date, Time, Party Size, Status
  - `cancel-reservation-button-{{ reservation.reservation_id }}` (Button) - Cancel upcoming reservation
  - `back-to-dashboard` (Button) - Navigate to `dashboard`
- Context Variables:
  - `reservations`: list of dicts (see Section 1)
- Form Actions:
  - Cancel buttons: POST to `/cancel_reservation/<reservation_id>`
- Navigation Mappings:
  - `back-to-dashboard` → `dashboard`

### templates/waitlist.html
- Page Title: Waitlist
- Main H1: Waitlist
- Element IDs:
  - `waitlist-page` (Div) - Container of waitlist page
  - `waitlist-party-size` (Dropdown select) - Select party size; name="party_size"
  - `join-waitlist-button` (Button) - Submit form
  - `user-position` (Div) - Display user's position in waitlist
  - `back-to-dashboard` (Button) - Navigate to `dashboard`
- Context Variables:
  - `waitlist`: list of dicts (see Section 1)
  - `user_position`: int|null
- Form Action:
  - Method: POST, action to `/waitlist`
  - Input name: `party_size`
- Navigation Mappings:
  - `back-to-dashboard` → `dashboard`

### templates/my_reviews.html
- Page Title: My Reviews
- Main H1: My Reviews
- Element IDs:
  - `reviews-page` (Div) - Container
  - `reviews-list` (Div) - List of reviews; for each show dish name, rating, review text
  - `write-new-review-button` (Button) - Navigate to `write_review`
  - `back-to-dashboard` (Button) - Navigate to `dashboard`
- Context Variables:
  - `reviews`: list of dicts (see Section 1)
- Navigation Mappings:
  - `write-new-review-button` → `write_review`
  - `back-to-dashboard` → `dashboard`

### templates/write_review.html
- Page Title: Write Review
- Main H1: Write Review
- Element IDs:
  - `write-review-page` (Div) - Container
  - `select-dish` (Dropdown select) - Select dish; name="dish_id"
  - `rating-input` (Dropdown select) - Select rating; name="rating"; options 1-5
  - `review-text` (Textarea) - Input area; name="review_text"
  - `submit-review-button` (Button) - Submit form
  - `back-to-reviews` (Button) - Navigate to `my_reviews`
- Context Variables:
  - `dishes`: list of dicts (see Section 1)
- Form Action:
  - Method: POST, action to `/write_review`
- Navigation Mappings:
  - `back-to-reviews` → `my_reviews`

### templates/profile.html
- Page Title: My Profile
- Main H1: My Profile
- Element IDs:
  - `profile-page` (Div) - Container
  - `profile-username` (Div) - Display username (non-editable)
  - `profile-email` (Input text) - Edit email; name="email"
  - `update-profile-button` (Button) - Submit email update
  - `back-to-dashboard` (Button) - Navigate to `dashboard`
- Context Variables:
  - `user`: dict {username: str, email: str, phone: str, full_name: str}
- Form Action:
  - Method: POST, action to `/profile`
- Navigation Mappings:
  - `back-to-dashboard` → `dashboard`

---

## Section 3: Data File Schemas (Backend Developer)

### 1. User Data
- File Path: `data/users.txt`
- Pipe-delimited format: `username|email|phone|full_name`
- Description: Stores registered user information.
- Field Definitions:
  - `username` (str): Unique user identifier.
  - `email` (str): User's email address.
  - `phone` (str): User's phone number.
  - `full_name` (str): User's full personal name.

- Example Rows:
  - `john_diner|john@example.com|555-1234|John Diner`
  - `jane_food|jane@example.com|555-5678|Jane Foodie`

### 2. Menu Items Data
- File Path: `data/menu.txt`
- Pipe-delimited format: `dish_id|name|category|price|description|ingredients|dietary|avg_rating`
- Description: Contains menu dishes with details for display and filtering.
- Field Definitions:
  - `dish_id` (str): Unique dish identifier.
  - `name` (str): Dish name.
  - `category` (str): Menu category (e.g., Appetizers, Main Course).
  - `price` (float): Price of dish.
  - `description` (str): Dish description.
  - `ingredients` (str): Comma-separated list of ingredients.
  - `dietary` (str): Dietary tags (e.g., Vegetarian, Gluten-Free).
  - `avg_rating` (float): Average rating.

- Example Rows:
  - `1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5`
  - `2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8`
  - `3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9`
  - `4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6`

### 3. Reservations Data
- File Path: `data/reservations.txt`
- Pipe-delimited format: `reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status`
- Description: Stores reservation details made by users.
- Field Definitions:
  - `reservation_id` (str): Unique reservation identifier.
  - `username` (str): Username who made the reservation.
  - `guest_name` (str): Guest's full name.
  - `phone` (str): Contact phone number.
  - `email` (str): Contact email address.
  - `party_size` (int): Number of guests.
  - `date` (str): Reservation date (YYYY-MM-DD).
  - `time` (str): Reservation time (HH:MM).
  - `special_requests` (str): Any special requests from guest.
  - `status` (str): Reservation status (e.g., Upcoming, Completed, Cancelled).

- Example Rows:
  - `1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming`
  - `2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed`
  - `3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming`

### 4. Waitlist Data
- File Path: `data/waitlist.txt`
- Pipe-delimited format: `waitlist_id|username|party_size|join_time|status`
- Description: Stores users waiting for a table; tracks order and status.
- Field Definitions:
  - `waitlist_id` (str): Unique waitlist entry identifier.
  - `username` (str): Username on waitlist.
  - `party_size` (int): Number of guests in party.
  - `join_time` (str): Timestamp of joining (YYYY-MM-DD HH:MM:SS).
  - `status` (str): Entry status (e.g., Active, Seated, Cancelled).

- Example Rows:
  - `1|john_diner|2|2024-11-22 18:30:00|Active`
  - `2|jane_food|4|2024-11-22 18:45:00|Active`

### 5. Reviews Data
- File Path: `data/reviews.txt`
- Pipe-delimited format: `review_id|username|dish_id|rating|review_text|review_date`
- Description: Contains reviews users wrote for dishes.
- Field Definitions:
  - `review_id` (str): Unique review identifier.
  - `username` (str): Username who wrote review.
  - `dish_id` (str): Dish identifier reviewed.
  - `rating` (int): Rating from 1 to 5.
  - `review_text` (str): Text content of review.
  - `review_date` (str): Date of review (YYYY-MM-DD).

- Example Rows:
  - `1|jane_food|2|5|Best salmon I've ever had!|2024-11-21`
  - `2|john_diner|3|5|Absolutely divine dessert!|2024-11-20`
  - `3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19`

---

*End of Design Specification*