# RestaurantReservation Web Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path                 | Function Name           | HTTP Methods | Template File                  | Context Variables                                                                                                     | Request Form Fields (POST)                         |
|--------------------------|-------------------------|--------------|-------------------------------|-----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| /                        | root_redirect           | GET          | None (redirects to /dashboard)| None                                                                                                                  | None                                             |
| /dashboard               | dashboard               | GET          | dashboard.html                | username: str
featured_dishes: list of dict {dish_id: int, name: str, price: float, description: str}
upcoming_reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
 | None                                             |
| /menu                    | menu                    | GET          | menu.html                     | menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str, dietary: str, avg_rating: float} | None                                             |
| /dish/<int:dish_id>      | dish_details            | GET          | dish_details.html             | dish: dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | None                                             |
| /make_reservation        | make_reservation        | GET, POST    | make_reservation.html         | On GET: None
On POST (after submission): success flag? message? (handled internally, typically redirects or reloads)         | guest_name: str
party_size: int (1-10)
reservation_date: str (YYYY-MM-DD) |
| /my_reservations         | my_reservations         | GET          | my_reservations.html          | reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str, guest_name: str}      | None                                             |
| /cancel_reservation/<int:reservation_id> | cancel_reservation | POST         | None (redirects or JSON)      | None                                                                                                                  | None (reservation_id in URL)                     |
| /waitlist                | waitlist                | GET, POST    | waitlist.html                 | On GET: user_position: int or None
On POST: updated user_position after join                                            | party_size: int (for joining waitlist)           |
| /my_reviews              | my_reviews              | GET          | my_reviews.html               | reviews: list of dict {review_id: int, dish_name: str, rating: int, review_text: str, review_date: str}                  | None                                             |
| /write_review            | write_review            | GET, POST    | write_review.html             | On GET: dishes: list of dict {dish_id: int, name: str}
On POST: success or error handling                                   | dish_id: int
rating: int (1-5)
review_text: str   |
| /profile                 | profile                 | GET, POST    | profile.html                  | On GET: user_profile: dict {username: str, email: str, phone: str, full_name: str}
On POST: updated profile feedback        | email: str                                       |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - welcome-message (H1): Displays welcome message with username
  - make-reservation-button (Button): Navigate to make reservation page
  - view-menu-button (Button): Navigate to menu page
  - back-to-dashboard (Button): Refresh dashboard page
  - my-reservations-button (Button): Navigate to my reservations page
  - my-reviews-button (Button): Navigate to my reviews page
  - waitlist-button (Button): Navigate to waitlist page
  - profile-button (Button): Navigate to profile page
- Context Variables:
  - username (str): current logged in user
  - featured_dishes (list of dict): Each with dish_id (int), name (str), price (float), description (str)
  - upcoming_reservations (list of dict): reservation_id (int), date (str), time (str), party_size (int), status (str)
- Navigation Mappings:
  - make-reservation-button: url_for('make_reservation')
  - view-menu-button: url_for('menu')
  - back-to-dashboard: url_for('dashboard')
  - my-reservations-button: url_for('my_reservations')
  - my-reviews-button: url_for('my_reviews')
  - waitlist-button: url_for('waitlist')
  - profile-button: url_for('profile')

### 2. Menu Page
- Filename: templates/menu.html
- Page Title: Restaurant Menu
- Element IDs:
  - menu-page (Div): Container for menu page
  - menu-grid (Div): Grid container for dish cards
  - view-dish-button-{{dish.dish_id}} (Button): Button on each dish card to view details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - menus (list of dict): dish_id (int), name (str), category (str), price (float), description (str), dietary (str), avg_rating (float)
- Navigation Mappings:
  - view-dish-button-{{dish.dish_id}}: url_for('dish_details', dish_id=dish.dish_id)
  - back-to-dashboard: url_for('dashboard')

### 3. Dish Details Page
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Element IDs:
  - dish-details-page (Div): Container for dish details
  - dish-name (H1): Dish name
  - dish-price (Div): Dish price
  - back-to-menu (Button): Navigate back to menu
- Context Variables:
  - dish (dict): dish_id (int), name (str), category (str), price (float), description (str), ingredients (str), dietary (str), avg_rating (float)
- Navigation Mappings:
  - back-to-menu: url_for('menu')

### 4. Make Reservation Page
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Element IDs:
  - reservation-page (Div): Container for reservation page
  - guest-name (Input): Text input for guest name
  - party-size (Dropdown): Select party size 1-10
  - reservation-date (Input date): Date input
  - submit-reservation-button (Button): Submit reservation form
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables: None
- Form:
  - Method: POST
  - Fields: guest_name, party_size, reservation_date
  - Action: current route (/make_reservation)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

### 5. My Reservations Page
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Element IDs:
  - my-reservations-page (Div): Container
  - reservations-table (Table): Table showing reservations
  - cancel-reservation-button-{{reservation.reservation_id}} (Button): Cancel button per upcoming reservation
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - reservations (list of dict): reservation_id (int), date (str), time (str), party_size (int), status (str), guest_name (str)
- Form for cancellation:
  - Method: POST
  - Action: url_for('cancel_reservation', reservation_id=reservation.reservation_id)
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

### 6. Waitlist Page
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Element IDs:
  - waitlist-page (Div): Container
  - waitlist-party-size (Dropdown): Select party size
  - join-waitlist-button (Button): Join waitlist
  - user-position (Div): Display current user position
  - back-to-dashboard (Button): Navigate to dashboard
- Context Variables:
  - user_position (int or None): Current position or None if not on waitlist
- Form:
  - Method: POST
  - Fields: party_size
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

### 7. My Reviews Page
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs:
  - reviews-page (Div): Container
  - reviews-list (Div): List of reviews with dish name, rating, review text
  - write-new-review-button (Button): Navigate to write review page
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - reviews (list of dict): review_id (int), dish_name (str), rating (int), review_text (str), review_date (str)
- Navigation Mappings:
  - write-new-review-button: url_for('write_review')
  - back-to-dashboard: url_for('dashboard')

### 8. Write Review Page
- Filename: templates/write_review.html
- Page Title: Write Review
- Element IDs:
  - write-review-page (Div): Container
  - select-dish (Dropdown): Select dish to review
  - rating-input (Dropdown): Select rating 1-5
  - review-text (Textarea): Review text input
  - submit-review-button (Button): Submit review
  - back-to-reviews (Button): Navigate back to my reviews
- Context Variables:
  - dishes (list of dict): dish_id (int), name (str)
- Form:
  - Method: POST
  - Fields: dish_id, rating, review_text
- Navigation Mappings:
  - back-to-reviews: url_for('my_reviews')

### 9. User Profile Page
- Filename: templates/profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (Div): Container
  - profile-username (Div): Display username (non-editable)
  - profile-email (Input): Email update input
  - update-profile-button (Button): Submit profile updates
  - back-to-dashboard (Button): Navigate to dashboard
- Context Variables:
  - user_profile (dict): username (str), email (str), phone (str), full_name (str)
- Form:
  - Method: POST
  - Fields: email
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format: Pipe-delimited
- Fields:
  1. username: Unique user identifier (str)
  2. email: User's email address (str)
  3. phone: User's phone number (str)
  4. full_name: User's full name (str)
- Description: Stores registered user information.
- Example Rows:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### 2. menu.txt
- Path: data/menu.txt
- Format: Pipe-delimited
- Fields:
  1. dish_id: Unique dish identifier (int)
  2. name: Dish name (str)
  3. category: Dish category (str), e.g. Appetizers, Main Course
  4. price: Dish price (float)
  5. description: Description of the dish (str)
  6. ingredients: Comma-separated list of ingredients (str)
  7. dietary: Dietary info (str), e.g. Vegetarian, Gluten-Free
  8. avg_rating: Average rating (float)
- Description: Stores menu items data.
- Example Rows:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### 3. reservations.txt
- Path: data/reservations.txt
- Format: Pipe-delimited
- Fields:
  1. reservation_id: Unique reservation identifier (int)
  2. username: User who made reservation (str)
  3. guest_name: Name of guest (str)
  4. phone: Guest phone number (str)
  5. email: Guest email (str)
  6. party_size: Number of guests (int)
  7. date: Reservation date (YYYY-MM-DD str)
  8. time: Reservation time (HH:MM str)
  9. special_requests: Special requests text (str, optional)
  10. status: Reservation status (str) e.g. Upcoming, Completed
- Description: Stores all reservations.
- Example Rows:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### 4. waitlist.txt
- Path: data/waitlist.txt
- Format: Pipe-delimited
- Fields:
  1. waitlist_id: Unique waitlist entry id (int)
  2. username: User who joined waitlist (str)
  3. party_size: Number of guests (int)
  4. join_time: Timestamp of joining (YYYY-MM-DD HH:MM:SS str)
  5. status: Status of waitlist entry (str), e.g. Active
- Description: Stores current and past waitlist entries.
- Example Rows:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### 5. reviews.txt
- Path: data/reviews.txt
- Format: Pipe-delimited
- Fields:
  1. review_id: Unique review identifier (int)
  2. username: User who wrote the review (str)
  3. dish_id: Dish reviewed (int)
  4. rating: Rating given (int, 1-5)
  5. review_text: Text content of the review (str)
  6. review_date: Date of review (YYYY-MM-DD str)
- Description: Stores all user reviews.
- Example Rows:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

---

This design specification covers all necessary Flask routes, HTML templates, and local data schemas. Backend and frontend teams may work independently and in parallel with this detailed and exact specification.
