# RestaurantReservation Web Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path                 | Function Name           | HTTP Methods | Template File                  | Context Variables                                                                                                     | Request Form Fields (POST)                         |
|--------------------------|-------------------------|--------------|-------------------------------|-----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| /                        | root_redirect            | GET          | None (redirects to /dashboard)| None                                                                                                                  | None                                             |
| /dashboard               | dashboard               | GET          | dashboard.html                | username: str
featured_dishes: list of dict {dish_id: int, name: str, price: float}
upcoming_reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
  | None                                             |
| /menu                    | menu                    | GET          | menu.html                     | menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str}                           | None                                             |
| /dish/<int:dish_id>      | dish_details            | GET          | dish_details.html             | dish: dict {dish_id: int, name: str, price: float, description: str}                                                  | None                                             |
| /make-reservation        | make_reservation        | GET, POST    | make_reservation.html         | None (GET)
form_state: dict (on POST failure, optional)                                                          | guest_name: str
party_size: int
reservation_date: str (YYYY-MM-DD)          |
| /my-reservations         | my_reservations         | GET          | my_reservations.html          | reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}                    | None (POST handled on cancel route)               |
| /cancel-reservation/<int:reservation_id> | cancel_reservation      | POST         | None (redirect after POST)     | None                                                                                                                  | None (cancel action identified via URL param)    |
| /waitlist                | waitlist                | GET, POST    | waitlist.html                 | waitlist_position: int or None
user_party_size: int or None (to show dropdown initial state)
waitlist_entries: list of dict (internal use/not for template) | party_size: int           |
| /my-reviews              | my_reviews              | GET          | my_reviews.html               | reviews: list of dict {review_id:int, dish_name: str, rating:int, review_text: str}                                    | None                                             |
| /write-review            | write_review            | GET, POST    | write_review.html             | dishes: list of dict {dish_id: int, name: str}
form_state: dict (on POST failure, optional)                                                          | dish_id: int
rating: int (1-5)
review_text: str                          |
| /profile                 | profile                 | GET, POST    | profile.html                  | user_profile: dict {username: str, email: str}                                                                         | email: str                                       |

Notes:
- POST routes:
  - /make-reservation accepts new reservation data.
  - /cancel-reservation/<reservation_id> cancels a reservation.
  - /waitlist allows joining waitlist.
  - /write-review accepts new review submission.
  - /profile allows update of user email.
- All GET routes provide required context variables to render pages fully.
- Dynamic URLs use typed parameters as specified.
- The root '/' route redirects to '/dashboard'.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Element IDs:
  - dashboard-page (Div): Container for dashboard
  - welcome-message (H1): Displays "Welcome, {{ username }}!"
  - make-reservation-button (Button): Navigate to make reservation page
  - view-menu-button (Button): Navigate to menu page
  - back-to-dashboard (Button): Refresh dashboard (reload current page)
  - my-reservations-button (Button): Navigate to my reservations
  - my-reviews-button (Button): Navigate to my reviews
  - waitlist-button (Button): Navigate to waitlist
  - profile-button (Button): Navigate to user profile
- Context Variables:
  - username: str
  - featured_dishes: list of dict {dish_id: int, name: str, price: float}
  - upcoming_reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
- Navigation Mappings:
  - make-reservation-button -> url_for('make_reservation')
  - view-menu-button -> url_for('menu')
  - back-to-dashboard -> url_for('dashboard')
  - my-reservations-button -> url_for('my_reservations')
  - my-reviews-button -> url_for('my_reviews')
  - waitlist-button -> url_for('waitlist')
  - profile-button -> url_for('profile')

### 2. Menu Page
- Filename: templates/menu.html
- Page Title: Restaurant Menu
- Element IDs:
  - menu-page (Div): Container for menu page
  - menu-grid (Div): Grid container for dish cards
  - view-dish-button-{{ dish.dish_id }} (Button): Button on each dish card to view details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str}
- Navigation Mappings:
  - view-dish-button-{{ dish.dish_id }} -> url_for('dish_details', dish_id=dish.dish_id)
  - back-to-dashboard -> url_for('dashboard')

### 3. Dish Details Page
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Element IDs:
  - dish-details-page (Div): Container for dish details
  - dish-name (H1): Displays dish name
  - dish-price (Div): Displays dish price
  - back-to-menu (Button): Navigate back to menu
- Context Variables:
  - dish: dict {dish_id: int, name: str, price: float, description: str}
- Navigation Mappings:
  - back-to-menu -> url_for('menu')

### 4. Make Reservation Page
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Element IDs:
  - reservation-page (Div): Container
  - guest-name (Input): Text input for guest name (name="guest_name")
  - party-size (Dropdown): Select dropdown for party size (1-10) (name="party_size")
  - reservation-date (Input date): For reservation date (name="reservation_date")
  - submit-reservation-button (Button): Submit form
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - (optional) form_state: dict with previously submitted values for repopulating form in case of errors
- Form:
  - method="POST"
  - action=""
  - Inputs with names: guest_name, party_size, reservation_date
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard')

### 5. My Reservations Page
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Element IDs:
  - my-reservations-page (Div): Container
  - reservations-table (Table): Displays reservations with columns for date, time, party size, status
  - cancel-reservation-button-{{ reservation.reservation_id }} (Button): Cancel button for each upcoming reservation
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
- Form:
  - For each cancel button, a POST form or AJAX POST to /cancel-reservation/<reservation_id>
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard')

### 6. Waitlist Page
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Element IDs:
  - waitlist-page (Div): Container
  - waitlist-party-size (Dropdown): Select dropdown for party size (name="party_size")
  - join-waitlist-button (Button): Submit to join waitlist
  - user-position (Div): Display user's current waitlist position or message
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - waitlist_position: int or None
  - user_party_size: int or None
- Form:
  - method="POST"
  - action=""
  - Input name: party_size
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard')

### 7. My Reviews Page
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs:
  - reviews-page (Div): Container
  - reviews-list (Div): List of reviews, each displaying dish name, rating, review text
  - write-new-review-button (Button): Navigate to write review page
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - reviews: list of dict {review_id: int, dish_name: str, rating: int, review_text: str}
- Navigation Mappings:
  - write-new-review-button -> url_for('write_review')
  - back-to-dashboard -> url_for('dashboard')

### 8. Write Review Page
- Filename: templates/write_review.html
- Page Title: Write Review
- Element IDs:
  - write-review-page (Div): Container
  - select-dish (Dropdown): Select dish to review (name="dish_id")
  - rating-input (Dropdown): Select rating (1-5) stars (name="rating")
  - review-text (Textarea): Input review text (name="review_text")
  - submit-review-button (Button): Submit form
  - back-to-reviews (Button): Navigate back to my reviews
- Context Variables:
  - dishes: list of dict {dish_id: int, name: str}
  - (optional) form_state: dict for repopulating fields on POST error
- Form:
  - method="POST"
  - action=""
  - Inputs with names: dish_id, rating, review_text
- Navigation Mappings:
  - back-to-reviews -> url_for('my_reviews')

### 9. User Profile Page
- Filename: templates/profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (Div): Container
  - profile-username (Div): Displays username (not editable)
  - profile-email (Input): Input for email (name="email")
  - update-profile-button (Button): Submit updated profile info
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - user_profile: dict {username: str, email: str}
- Form:
  - method="POST"
  - action=""
  - Input name: email
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Pipe-delimited format:
  ```
  username|email|phone|full_name
  ```
- Description: Stores user account information.
- Fields:
  - username: Unique identifier for user (str)
  - email: User's email address (str)
  - phone: User's phone number (str)
  - full_name: Full name of the user (str)
- Example Rows:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### 2. menu.txt
- Path: data/menu.txt
- Pipe-delimited format:
  ```
  dish_id|name|category|price|description|ingredients|dietary|avg_rating
  ```
- Description: Stores menu items details.
- Fields:
  - dish_id: Unique dish identifier (int)
  - name: Dish name (str)
  - category: Dish category (e.g., Appetizers) (str)
  - price: Price in dollars (float)
  - description: Description of dish (str)
  - ingredients: Comma-separated list of ingredients (str)
  - dietary: Dietary info (e.g., Vegetarian, Gluten-Free) (str)
  - avg_rating: Average rating (float)
- Example Rows:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### 3. reservations.txt
- Path: data/reservations.txt
- Pipe-delimited format:
  ```
  reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
  ```
- Description: Stores reservation details.
- Fields:
  - reservation_id: Unique reservation identifier (int)
  - username: Username who made reservation (str)
  - guest_name: Guest name (str)
  - phone: Contact phone (str)
  - email: Contact email (str)
  - party_size: Number of guests (int)
  - date: Reservation date (YYYY-MM-DD) (str)
  - time: Reservation time (HH:MM, 24h) (str)
  - special_requests: Any special requests (str, nullable)
  - status: Reservation status (e.g., Upcoming, Completed) (str)
- Example Rows:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### 4. waitlist.txt
- Path: data/waitlist.txt
- Pipe-delimited format:
  ```
  waitlist_id|username|party_size|join_time|status
  ```
- Description: Stores waitlist entries.
- Fields:
  - waitlist_id: Unique waitlist entry ID (int)
  - username: Username (str)
  - party_size: Party size for waitlist (int)
  - join_time: Timestamp of joining (YYYY-MM-DD HH:MM:SS) (str)
  - status: Entry status (e.g., Active) (str)
- Example Rows:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### 5. reviews.txt
- Path: data/reviews.txt
- Pipe-delimited format:
  ```
  review_id|username|dish_id|rating|review_text|review_date
  ```
- Description: Stores user reviews for dishes.
- Fields:
  - review_id: Unique review ID (int)
  - username: Username of reviewer (str)
  - dish_id: Dish reviewed (int)
  - rating: Rating given (1-5) (int)
  - review_text: Text of review (str)
  - review_date: Date of review (YYYY-MM-DD) (str)
- Example Rows:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

---

This design specification provides detailed Flask routes, template structure with exact element IDs, and precise data file formats. Backend and frontend teams can implement their components independently and in parallel following these specifications without ambiguity.