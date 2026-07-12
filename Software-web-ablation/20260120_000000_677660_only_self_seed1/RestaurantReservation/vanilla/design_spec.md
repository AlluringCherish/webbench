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
| /menu                    | menu                    | GET          | menu.html                     | menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | None                                             |
| /dish/<int:dish_id>      | dish_details            | GET          | dish_details.html             | dish: dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | None                                             |
| /make_reservation        | make_reservation        | GET, POST    | make_reservation.html         | None                                                                                                                  | guest_name: str
party_size: int
reservation_date: str (YYYY-MM-DD) |
| /my_reservations         | my_reservations         | GET          | my_reservations.html          | reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}                     | None                                             |
| /cancel_reservation/<int:reservation_id> | cancel_reservation       | POST         | None (redirects back to /my_reservations) | None                                                                                                                  | None (but POST request triggers cancellation)    |
| /waitlist                | waitlist                | GET, POST    | waitlist.html                 | waitlist_position: int or None (None if user not in waitlist)                                                         | party_size: int                                   |
| /my_reviews              | my_reviews              | GET          | my_reviews.html               | reviews: list of dict {review_id: int, dish_id: int, dish_name: str, rating: int, review_text: str, review_date: str}    | None                                             |
| /write_review            | write_review            | GET, POST    | write_review.html             | dishes: list of dict {dish_id: int, name: str}                                                                         | dish_id: int
rating: int (1-5)
review_text: str           |
| /profile                 | profile                 | GET, POST    | profile.html                  | user_profile: dict {username: str, email: str}                                                                          | email: str                                       |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Context Variables:
  - username: str
  - featured_dishes: list of dict {dish_id: int, name: str, price: float, description: str}
  - upcoming_reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
- Element IDs:
  - dashboard-page (Div): Container for dashboard page
  - welcome-message (H1): Displays welcome message with username
  - make-reservation-button (Button): Navigate to /make_reservation
  - view-menu-button (Button): Navigate to /menu
  - back-to-dashboard (Button): Refresh dashboard (/dashboard)
  - my-reservations-button (Button): Navigate to /my_reservations
  - my-reviews-button (Button): Navigate to /my_reviews
  - waitlist-button (Button): Navigate to /waitlist
  - profile-button (Button): Navigate to /profile
- Navigation mappings:
  - make-reservation-button: url_for('make_reservation')
  - view-menu-button: url_for('menu')
  - back-to-dashboard: url_for('dashboard')
  - my-reservations-button: url_for('my_reservations')
  - my-reviews-button: url_for('my_reviews')
  - waitlist-button: url_for('waitlist')
  - profile-button: url_for('profile')


### 2. menu.html
- Filename: templates/menu.html
- Page Title: Restaurant Menu
- Context Variables:
  - menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}
- Element IDs:
  - menu-page (Div): Container for menu page
  - menu-grid (Div): grid displaying dish cards
  - view-dish-button-{dish_id} (Button): Button to view dish details (dynamic id per dish)
  - back-to-dashboard (Button): Navigate to /dashboard
- Navigation mappings:
  - view-dish-button-{dish_id}: url_for('dish_details', dish_id=dish.dish_id)
  - back-to-dashboard: url_for('dashboard')


### 3. dish_details.html
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Context Variables:
  - dish: dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}
- Element IDs:
  - dish-details-page (Div): Container for dish details
  - dish-name (H1): Display dish name
  - dish-price (Div): Display dish price
  - back-to-menu (Button): Navigate back to /menu
- Navigation mappings:
  - back-to-menu: url_for('menu')


### 4. make_reservation.html
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Context Variables: None
- Element IDs:
  - reservation-page (Div): container for reservation form
  - guest-name (Input): input for guest name
  - party-size (Dropdown): dropdown with options 1-10
  - reservation-date (Input type=date): date input
  - submit-reservation-button (Button): submits the POST to /make_reservation
  - back-to-dashboard (Button): navigate to /dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Form action:
  - POST to /make_reservation
  - Form fields: guest_name, party_size, reservation_date


### 5. my_reservations.html
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Context Variables:
  - reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
- Element IDs:
  - my-reservations-page (Div): container for reservations page
  - reservations-table (Table): table with columns date, time, party size, status
  - cancel-reservation-button-{reservation_id} (Button): button to cancel reservation dynamically
  - back-to-dashboard (Button): navigate to /dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Cancel request:
  - POST /cancel_reservation/<reservation_id> triggered by each cancel button


### 6. waitlist.html
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Context Variables:
  - waitlist_position: int or None
- Element IDs:
  - waitlist-page (Div): container for waitlist page
  - waitlist-party-size (Dropdown): select party size
  - join-waitlist-button (Button): join waitlist (POST submit)
  - user-position (Div): shows user’s position or "Not in waitlist"
  - back-to-dashboard (Button): navigate to /dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Form action:
  - POST to /waitlist
  - Form fields: party_size


### 7. my_reviews.html
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Context Variables:
  - reviews: list of dict {review_id: int, dish_id: int, dish_name: str, rating: int, review_text: str, review_date: str}
- Element IDs:
  - reviews-page (Div): container for reviews
  - reviews-list (Div): list container for review entries
  - write-new-review-button (Button): navigate to /write_review
  - back-to-dashboard (Button): navigate to /dashboard
- Navigation mappings:
  - write-new-review-button: url_for('write_review')
  - back-to-dashboard: url_for('dashboard')


### 8. write_review.html
- Filename: templates/write_review.html
- Page Title: Write Review
- Context Variables:
  - dishes: list of dict {dish_id: int, name: str}
- Element IDs:
  - write-review-page (Div): container for review form
  - select-dish (Dropdown): select dish by dish_id
  - rating-input (Dropdown): select rating 1-5
  - review-text (Textarea): textarea for review
  - submit-review-button (Button): submit form
  - back-to-reviews (Button): navigate back to /my_reviews
- Navigation mappings:
  - back-to-reviews: url_for('my_reviews')
- Form action:
  - POST to /write_review
  - Form fields: dish_id, rating, review_text


### 9. profile.html
- Filename: templates/profile.html
- Page Title: My Profile
- Context Variables:
  - user_profile: dict {username: str, email: str}
- Element IDs:
  - profile-page (Div): container for profile page
  - profile-username (Div): display username (readonly)
  - profile-email (Input): input for email update
  - update-profile-button (Button): submits form
  - back-to-dashboard (Button): navigate to /dashboard
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard')
- Form action:
  - POST to /profile
  - Form fields: email


---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format: pipe-delimited
- Description: Stores user profile information.
- Fields:
  - username: str - Unique user identifier
  - email: str - User email address
  - phone: str - User phone number
  - full_name: str - User’s full name
- Example rows:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### 2. menu.txt
- Path: data/menu.txt
- Format: pipe-delimited
- Description: Stores restaurant menu items.
- Fields:
  - dish_id: int - Unique dish identifier
  - name: str - Dish name
  - category: str - Category (Appetizers, Main Course, Desserts, Beverages)
  - price: float - Price of the dish
  - description: str - Description of the dish
  - ingredients: str - Comma-separated ingredients
  - dietary: str - Dietary info (Vegetarian, Gluten-Free, Vegan, etc.)
  - avg_rating: float - Average rating
- Example rows:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### 3. reservations.txt
- Path: data/reservations.txt
- Format: pipe-delimited
- Description: Stores table reservations.
- Fields:
  - reservation_id: int - Unique reservation identifier
  - username: str - User who made reservation
  - guest_name: str - Name of the guest for reservation
  - phone: str - Guest phone number
  - email: str - Guest email
  - party_size: int - Number of people
  - date: str - Reservation date (YYYY-MM-DD)
  - time: str - Reservation time (HH:MM)
  - special_requests: str - Any special requests (optional)
  - status: str - Reservation status (Upcoming, Completed, Cancelled)
- Example rows:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### 4. waitlist.txt
- Path: data/waitlist.txt
- Format: pipe-delimited
- Description: Stores waitlist entries.
- Fields:
  - waitlist_id: int - Unique waitlist entry ID
  - username: str - User who joined waitlist
  - party_size: int - Number of people
  - join_time: str - Timestamp when joined (YYYY-MM-DD HH:MM:SS)
  - status: str - Status (Active, Removed)
- Example rows:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### 5. reviews.txt
- Path: data/reviews.txt
- Format: pipe-delimited
- Description: Stores user reviews of dishes.
- Fields:
  - review_id: int - Unique review identifier
  - username: str - Reviewer username
  - dish_id: int - Dish reviewed
  - rating: int - Star rating (1-5)
  - review_text: str - Review content
  - review_date: str - Date of review (YYYY-MM-DD)
- Example rows:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

---

This specification fully enables backend and frontend developers to independently implement the RestaurantReservation application with clear API routes, expected data structures, and UI element mappings.
