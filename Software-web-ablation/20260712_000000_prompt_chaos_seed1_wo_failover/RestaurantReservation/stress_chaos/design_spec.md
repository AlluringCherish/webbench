# RestaurantReservation Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path               | Function Name         | HTTP Methods | Template File               | Context Variables                                                      | Request Form Fields (POST)                                  |
|------------------------|-----------------------|--------------|-----------------------------|------------------------------------------------------------------------|------------------------------------------------------------|
| /                      | root_redirect          | GET          | N/A (Redirect)               | N/A                                                                    | N/A                                                        |
| /dashboard             | dashboard             | GET          | dashboard.html              | username: str, featured_dishes: list of dict {dish_id: int, name: str, price: float, description: str, image_url: str}, upcoming_reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str} | N/A                                                        |
| /menu                  | menu                  | GET          | menu.html                   | menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | N/A                                                        |
| /dish/<int:dish_id>    | dish_details          | GET          | dish_details.html           | dish: dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | N/A                                                        |
| /make_reservation      | make_reservation      | GET, POST    | make_reservation.html       | N/A (GET: show empty form, POST: after submit perhaps redirect)       | guest_name: str, party_size: int, reservation_date: str (YYYY-MM-DD) |
| /my_reservations       | my_reservations       | GET          | my_reservations.html        | reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str} | N/A                                                        |
| /cancel_reservation/<int:reservation_id> | cancel_reservation    | POST         | N/A (redirect to /my_reservations) | N/A                                                                    | N/A                                                        |
| /waitlist              | waitlist              | GET, POST    | waitlist.html               | waitlist_entries: list of dict {waitlist_id: int, party_size: int, join_time: str, status: str}, user_position: int or None | party_size: int                                           |
| /my_reviews            | my_reviews            | GET          | my_reviews.html             | reviews: list of dict {review_id: int, dish_name: str, rating: int, review_text: str, review_date: str} | N/A                                                        |
| /write_review          | write_review          | GET, POST    | write_review.html           | dishes: list of dict {dish_id: int, name: str}                       | dish_id: int, rating: int (1-5), review_text: str          |
| /profile               | profile               | GET, POST    | profile.html                | user_profile: dict {username: str, email: str}                        | email: str                                                |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

---

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page
  - welcome-message (H1): Displays username welcome
  - make-reservation-button (Button): Navigate to /make_reservation
  - view-menu-button (Button): Navigate to /menu
  - back-to-dashboard (Button): Refresh the dashboard page (/dashboard)
  - my-reservations-button (Button): Navigate to /my_reservations
  - my-reviews-button (Button): Navigate to /my_reviews
  - waitlist-button (Button): Navigate to /waitlist
  - profile-button (Button): Navigate to /profile
- Context Variables:
  - username: str
  - featured_dishes: list of dict {dish_id: int, name: str, price: float, description: str, image_url: str}
  - upcoming_reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
- Navigation Mappings:
  - make-reservation-button -> url_for('make_reservation')
  - view-menu-button -> url_for('menu')
  - back-to-dashboard -> url_for('dashboard')
  - my-reservations-button -> url_for('my_reservations')
  - my-reviews-button -> url_for('my_reviews')
  - waitlist-button -> url_for('waitlist')
  - profile-button -> url_for('profile')

---

### 2. menu.html
- Filename: templates/menu.html
- Page Title: Restaurant Menu
- Element IDs:
  - menu-page (Div): Container for menu page
  - menu-grid (Div): Grid displaying dish cards
  - view-dish-button-{{ dish.dish_id }} (Button per dish): Button to view dish details
  - back-to-dashboard (Button): Navigate back to /dashboard
- Context Variables:
  - menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}
- Navigation Mappings:
  - Each view-dish-button-{{ dish.dish_id }} -> url_for('dish_details', dish_id=dish.dish_id)
  - back-to-dashboard -> url_for('dashboard')

---

### 3. dish_details.html
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Element IDs:
  - dish-details-page (Div): Container for dish details page
  - dish-name (H1): Display dish name
  - dish-price (Div): Display dish price
  - back-to-menu (Button): Navigate back to /menu
- Context Variables:
  - dish: dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}
- Navigation Mappings:
  - back-to-menu -> url_for('menu')

---

### 4. make_reservation.html
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Element IDs:
  - reservation-page (Div): Container for reservation page
  - guest-name (Input): Input for guest name (form field name="guest_name")
  - party-size (Dropdown): Select party size 1-10 (form field name="party_size")
  - reservation-date (Input type=date): Select reservation date (form field name="reservation_date")
  - submit-reservation-button (Button): Submit form
  - back-to-dashboard (Button): Navigate back to /dashboard
- Context Variables:
  - None (only form displayed)
- Navigation Mappings:
  - submit-reservation-button: Form POST action to /make_reservation
  - back-to-dashboard -> url_for('dashboard')

---

### 5. my_reservations.html
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Element IDs:
  - my-reservations-page (Div): Container for reservations page
  - reservations-table (Table): Table listing reservations
  - cancel-reservation-button-{{ reservation.reservation_id }} (Button per upcoming reservation): Cancel reservation
  - back-to-dashboard (Button): Navigate back to /dashboard
- Context Variables:
  - reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
- Navigation Mappings:
  - cancel-reservation-button-{{ reservation.reservation_id }}: Form POST to /cancel_reservation/<reservation_id>
  - back-to-dashboard -> url_for('dashboard')

---

### 6. waitlist.html
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Element IDs:
  - waitlist-page (Div): Container for waitlist page
  - waitlist-party-size (Dropdown): Select party size (form field name="party_size")
  - join-waitlist-button (Button): Submit form POST to join waitlist
  - user-position (Div): Displays current user's position in waitlist
  - back-to-dashboard (Button): Navigate back to /dashboard
- Context Variables:
  - waitlist_entries: list of dict {waitlist_id: int, party_size: int, join_time: str, status: str}
  - user_position: int or None
- Navigation Mappings:
  - join-waitlist-button: Form POST action to /waitlist
  - back-to-dashboard -> url_for('dashboard')

---

### 7. my_reviews.html
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs:
  - reviews-page (Div): Container for reviews page
  - reviews-list (Div): List of user reviews
  - write-new-review-button (Button): Navigate to /write_review
  - back-to-dashboard (Button): Navigate back to /dashboard
- Context Variables:
  - reviews: list of dict {review_id: int, dish_name: str, rating: int, review_text: str, review_date: str}
- Navigation Mappings:
  - write-new-review-button -> url_for('write_review')
  - back-to-dashboard -> url_for('dashboard')

---

### 8. write_review.html
- Filename: templates/write_review.html
- Page Title: Write Review
- Element IDs:
  - write-review-page (Div): Container for write review page
  - select-dish (Dropdown): Select dish to review (form field name="dish_id")
  - rating-input (Dropdown): Select rating 1-5 (form field name="rating")
  - review-text (Textarea): Enter review text (form field name="review_text")
  - submit-review-button (Button): Submit form
  - back-to-reviews (Button): Navigate back to /my_reviews
- Context Variables:
  - dishes: list of dict {dish_id: int, name: str}
- Navigation Mappings:
  - submit-review-button: Form POST action to /write_review
  - back-to-reviews -> url_for('my_reviews')

---

### 9. profile.html
- Filename: templates/profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (Div): Container for profile page
  - profile-username (Div): Display username (not editable)
  - profile-email (Input): Update user email (form field name="email")
  - update-profile-button (Button): Submit profile update
  - back-to-dashboard (Button): Navigate back to /dashboard
- Context Variables:
  - user_profile: dict {username: str, email: str}
- Navigation Mappings:
  - update-profile-button: Form POST action to /profile
  - back-to-dashboard -> url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

1. users.txt
- Path: data/users.txt
- Format (pipe-delimited):
  username|email|phone|full_name
- Description: Stores user account information
- Fields:
  - username: unique identifier string for user login
  - email: user email address
  - phone: user phone number
  - full_name: full name of user
- Example Rows:
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie

---

2. menu.txt
- Path: data/menu.txt
- Format (pipe-delimited):
  dish_id|name|category|price|description|ingredients|dietary|avg_rating
- Description: Stores all menu items with details
- Fields:
  - dish_id: integer unique dish identifier
  - name: dish name
  - category: dish category (e.g., Appetizers, Main Course, Desserts, Beverages)
  - price: dish price (float)
  - description: short description of dish
  - ingredients: comma-separated ingredients list
  - dietary: dietary information (e.g., Vegetarian, Gluten-Free, Vegan)
  - avg_rating: average rating (float)
- Example Rows:
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6

---

3. reservations.txt
- Path: data/reservations.txt
- Format (pipe-delimited):
  reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
- Description: Stores table reservation data
- Fields:
  - reservation_id: integer unique reservation identifier
  - username: user who made the reservation
  - guest_name: name of guest
  - phone: contact phone
  - email: contact email
  - party_size: number of guests in party (int)
  - date: reservation date (YYYY-MM-DD)
  - time: reservation time (HH:MM)
  - special_requests: optional special requests text
  - status: reservation status (e.g., Upcoming, Completed, Cancelled)
- Example Rows:
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming

---

4. waitlist.txt
- Path: data/waitlist.txt
- Format (pipe-delimited):
  waitlist_id|username|party_size|join_time|status
- Description: Stores waitlist entries
- Fields:
  - waitlist_id: integer unique waitlist entry ID
  - username: user on the waitlist
  - party_size: number of guests
  - join_time: datetime when joined (YYYY-MM-DD HH:MM:SS)
  - status: entry status (e.g., Active, Seated, Cancelled)
- Example Rows:
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active

---

5. reviews.txt
- Path: data/reviews.txt
- Format (pipe-delimited):
  review_id|username|dish_id|rating|review_text|review_date
- Description: Stores user reviews for dishes
- Fields:
  - review_id: integer unique review identifier
  - username: user who wrote review
  - dish_id: integer dish identifier
  - rating: integer 1-5
  - review_text: text of the review
  - review_date: date of review (YYYY-MM-DD)
- Example Rows:
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19

---


This specification document enables backend and frontend developers to work independently with clearly defined routes, templates, and data schemas matching all user task requirements.