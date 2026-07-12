# RestaurantReservation Web Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path                 | Function Name           | HTTP Methods | Template File                  | Context Variables                                                                                                     | Request Form Fields (POST)                         |
|--------------------------|-------------------------|--------------|-------------------------------|-----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| /                        | root_redirect            | GET          | None (redirects to /dashboard)| None                                                                                                                  | None                                             |
| /dashboard               | dashboard               | GET          | dashboard.html                | username: str
featured_dishes: list of dict {dish_id: int, name: str, price: float, description: str}
upcoming_reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
 | None                                             |
| /menu                    | menu                    | GET          | menu.html                     | menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | None                                             |
| /dish/<int:dish_id>      | dish_details            | GET          | dish_details.html             | dish: dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | None                                             |
| /make_reservation        | make_reservation        | GET, POST    | make_reservation.html         | None on GET; On GET to render form
POST redirects or displays errors on failure                                              | guest_name: str
party_size: int (1-10)
reservation_date: str (YYYY-MM-DD) |
| /my_reservations         | my_reservations         | GET          | my_reservations.html          | reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}                     | None                                             |
| /cancel_reservation/<int:reservation_id> | cancel_reservation      | POST         | JSON or redirect               | None (cancels reservation by ID)                                                                                      | None (cancellation done by path param)            |
| /waitlist                | waitlist                | GET, POST    | waitlist.html                 | On GET:
waitlist_position: int or None
party_size_options: list of int (party size choices, typically 1-10)             | party_size: int (for join waitlist)               |
| /my_reviews              | my_reviews              | GET          | my_reviews.html               | reviews: list of dict {review_id: int, dish_name: str, rating: int, review_text: str}                                   | None                                             |
| /write_review            | write_review            | GET, POST    | write_review.html             | dishes: list of dict {dish_id: int, name: str}                                                                        | selected_dish_id: int
rating: int (1-5)
review_text: str |
| /profile                 | profile                 | GET, POST    | profile.html                  | user_profile: dict {username: str, email: str, phone: str, full_name: str}                                              | email: str (for update)                           |

Notes:
- The root route `/` redirects to `/dashboard` as per requirements.
- POST routes handle form submissions for reservations, waitlist joining, reviews, profile updates, and reservation cancellation.
- Context variables are comprehensive to support all dynamic page elements.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Element IDs & Descriptions:
  - dashboard-page (Div): Container for dashboard page.
  - welcome-message (H1): Displays welcome message with username.
  - make-reservation-button (Button): Navigate to /make_reservation
  - view-menu-button (Button): Navigate to /menu
  - back-to-dashboard (Button): Refresh or navigate to /dashboard
  - my-reservations-button (Button): Navigate to /my_reservations
  - my-reviews-button (Button): Navigate to /my_reviews
  - waitlist-button (Button): Navigate to /waitlist
  - profile-button (Button): Navigate to /profile
- Context Variables:
  - username (str)
  - featured_dishes (list of dict): {dish_id: int, name: str, price: float, description: str}
  - upcoming_reservations (list of dict): {reservation_id: int, date: str, time: str, party_size: int, status: str}
- Navigation Button Actions:
  - make-reservation-button => url_for('make_reservation')
  - view-menu-button => url_for('menu')
  - back-to-dashboard => url_for('dashboard')
  - my-reservations-button => url_for('my_reservations')
  - my-reviews-button => url_for('my_reviews')
  - waitlist-button => url_for('waitlist')
  - profile-button => url_for('profile')

### 2. menu.html
- Filename: templates/menu.html
- Page Title: Restaurant Menu
- Element IDs & Descriptions:
  - menu-page (Div): Container for menu.
  - menu-grid (Div): Grid displaying dish cards.
  - view-dish-button-{{ dish.dish_id }} (Button): Button to view dish details.
  - back-to-dashboard (Button): Navigate back to /dashboard
- Context Variables:
  - menus (list of dict): {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}
- Navigation Button Actions:
  - back-to-dashboard => url_for('dashboard')
  - Each view-dish-button => url_for('dish_details', dish_id=dish.dish_id)

### 3. dish_details.html
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Element IDs & Descriptions:
  - dish-details-page (Div): Container
  - dish-name (H1): Display dish name
  - dish-price (Div): Display dish price
  - back-to-menu (Button): Navigate back to /menu
- Context Variables:
  - dish (dict): {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}
- Navigation Button Actions:
  - back-to-menu => url_for('menu')

### 4. make_reservation.html
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Element IDs & Descriptions:
  - reservation-page (Div): Container for reservation page
  - guest-name (Input): Input field for guest's name (name="guest_name")
  - party-size (Dropdown): Select party size 1-10 (name="party_size")
  - reservation-date (Input date): Date picker (name="reservation_date")
  - submit-reservation-button (Button): Submit form
  - back-to-dashboard (Button): Navigate back to /dashboard
- Context Variables: None
- Form Action: POST to /make_reservation
- Navigation Button Actions:
  - back-to-dashboard => url_for('dashboard')

### 5. my_reservations.html
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Element IDs & Descriptions:
  - my-reservations-page (Div): Container
  - reservations-table (Table): Table with rows per reservation
  - cancel-reservation-button-{{ reservation.reservation_id }} (Button): Cancel reservation button per upcoming reservation
  - back-to-dashboard (Button): Navigate back to /dashboard
- Context Variables:
  - reservations (list of dict): {reservation_id: int, date: str, time: str, party_size: int, status: str}
- Form Actions:
  - Cancel buttons submit POST to /cancel_reservation/<reservation_id>
- Navigation Button Actions:
  - back-to-dashboard => url_for('dashboard')

### 6. waitlist.html
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Element IDs & Descriptions:
  - waitlist-page (Div): Container
  - waitlist-party-size (Dropdown): Select party size (name="party_size")
  - join-waitlist-button (Button): Submit join waitlist
  - user-position (Div): Display current waitlist position
  - back-to-dashboard (Button): Navigate back
- Context Variables:
  - waitlist_position (int or None)
  - party_size_options (list of int)
- Form Action: POST to /waitlist
- Navigation Button Actions:
  - back-to-dashboard => url_for('dashboard')

### 7. my_reviews.html
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs & Descriptions:
  - reviews-page (Div): Container
  - reviews-list (Div): List of reviews with dish name, rating, text
  - write-new-review-button (Button): Navigate to /write_review
  - back-to-dashboard (Button): Navigate back
- Context Variables:
  - reviews (list of dict): {review_id: int, dish_name: str, rating: int, review_text: str}
- Navigation Button Actions:
  - write-new-review-button => url_for('write_review')
  - back-to-dashboard => url_for('dashboard')

### 8. write_review.html
- Filename: templates/write_review.html
- Page Title: Write Review
- Element IDs & Descriptions:
  - write-review-page (Div): Container
  - select-dish (Dropdown): Select dish to review (name="selected_dish_id")
  - rating-input (Dropdown): Select rating 1-5 (name="rating")
  - review-text (Textarea): Review input (name="review_text")
  - submit-review-button (Button): Submit form
  - back-to-reviews (Button): Back to /my_reviews
- Context Variables:
  - dishes (list of dict): {dish_id: int, name: str}
- Form Action: POST to /write_review
- Navigation Button Actions:
  - back-to-reviews => url_for('my_reviews')

### 9. profile.html
- Filename: templates/profile.html
- Page Title: My Profile
- Element IDs & Descriptions:
  - profile-page (Div): Container
  - profile-username (Div): Display username (no input)
  - profile-email (Input): Update email (name="email")
  - update-profile-button (Button): Submit profile update
  - back-to-dashboard (Button): Navigate back
- Context Variables:
  - user_profile (dict): {username: str, email: str, phone: str, full_name: str}
- Form Action: POST to /profile
- Navigation Button Actions:
  - back-to-dashboard => url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format (pipe-delimited):
  ```
  username|email|phone|full_name
  ```
- Description: Stores user account info
- Fields:
  - username: unique user login ID (str)
  - email: user email (str)
  - phone: user phone number (str)
  - full_name: full name of user (str)
- Example rows:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### 2. menu.txt
- Path: data/menu.txt
- Format (pipe-delimited):
  ```
  dish_id|name|category|price|description|ingredients|dietary|avg_rating
  ```
- Description: Stores details about each dish in the menu
- Fields:
  - dish_id: unique dish integer ID
  - name: dish name
  - category: category e.g. Appetizers, Main Course
  - price: float price
  - description: descriptive text
  - ingredients: comma-separated list
  - dietary: dietary info e.g. Vegetarian
  - avg_rating: average float rating from reviews
- Example rows:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### 3. reservations.txt
- Path: data/reservations.txt
- Format (pipe-delimited):
  ```
  reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
  ```
- Description: Stores all reservation records
- Fields:
  - reservation_id: unique reservation integer ID
  - username: who made reservation
  - guest_name: name of guest for reservation
  - phone: guest's phone
  - email: guest's email
  - party_size: number of people
  - date: YYYY-MM-DD
  - time: HH:MM
  - special_requests: arbitrary text
  - status: reservation status e.g. Upcoming, Completed
- Example rows:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### 4. waitlist.txt
- Path: data/waitlist.txt
- Format (pipe-delimited):
  ```
  waitlist_id|username|party_size|join_time|status
  ```
- Description: Stores users waiting for tables
- Fields:
  - waitlist_id: unique integer ID
  - username: user in waitlist
  - party_size: int
  - join_time: timestamp YYYY-MM-DD HH:MM:SS
  - status: e.g. Active, Seated
- Example rows:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### 5. reviews.txt
- Path: data/reviews.txt
- Format (pipe-delimited):
  ```
  review_id|username|dish_id|rating|review_text|review_date
  ```
- Description: Stores user reviews for dishes
- Fields:
  - review_id: unique integer ID
  - username: reviewer username
  - dish_id: dish integer ID
  - rating: int 1-5
  - review_text: user text review
  - review_date: YYYY-MM-DD
- Example rows:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

---

This design specification fully supports independent backend and frontend development. All routes, templates, variables, element IDs, and data schemas align exactly with the user requirements.
