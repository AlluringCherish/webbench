# Design Specification Document for RestaurantReservation Web Application

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path                  | Function Name           | HTTP Methods | Template File            | Context Variables                                                                                        | Request Form Fields (POST)                                   |
|---------------------------|-------------------------|--------------|--------------------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| /                         | root_redirect           | GET          | None (redirect)           | None                                                                                                     | None                                                        |
| /dashboard                | dashboard               | GET          | dashboard.html           | username: str, featured_dishes: list of dict {dish_id:int, name:str, price:float}, upcoming_reservations: list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str} | None                                                        |
| /menu                    | menu                    | GET          | menu.html                | menu: list of dict {dish_id:int, name:str, category:str, price:float, description:str}                   | None                                                        |
| /dish/<int:dish_id>       | dish_details            | GET          | dish_details.html        | dish: dict {dish_id:int, name:str, price:float, description:str}                                        | None                                                        |
| /make_reservation          | make_reservation        | GET, POST    | make_reservation.html    | None (GET)                                                                                               | guest_name:str, party_size:int (1-10), reservation_date:str  |
| /my_reservations          | my_reservations         | GET          | my_reservations.html     | reservations: list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str}          | None                                                        |
| /cancel_reservation/<int:reservation_id> | cancel_reservation      | POST         | None (redirect to my_reservations) | None                                                                                                     | None                                                        |
| /waitlist                | waitlist                | GET, POST    | waitlist.html            | position: int or None (user's current waitlist position if any)                                         | party_size:int                                              |
| /my_reviews              | my_reviews              | GET          | my_reviews.html          | reviews: list of dict {review_id:int, dish_name:str, rating:int, review_text:str}                        | None                                                        |
| /write_review             | write_review            | GET, POST    | write_review.html        | dishes: list of dict {dish_id:int, name:str}                                                            | dish_id:int, rating:int (1-5), review_text:str              |
| /profile                 | profile                 | GET, POST    | profile.html             | user: dict {username:str, email:str}                                                                    | email:str                                                   |

Notes:
- Root route '/' redirects to '/dashboard'.
- POST routes handle data submissions for reservations, cancellations, waitlist joins, reviews, and profile updates.
- Context variables support all required page elements with specified types and structures.
- Dynamic route parameters explicitly typed.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Element IDs:
  - dashboard-page (Div): Main container
  - welcome-message (H1): Displays "Welcome, {{ username }}!"
  - make-reservation-button (Button): Navigates to make_reservation
  - view-menu-button (Button): Navigates to menu
  - back-to-dashboard (Button): Refreshes dashboard
  - my-reservations-button (Button): Navigates to my_reservations
  - my-reviews-button (Button): Navigates to my_reviews
  - waitlist-button (Button): Navigates to waitlist
  - profile-button (Button): Navigates to profile
- Context Variables:
  - username: str
  - featured_dishes: list of dict {dish_id:int, name:str, price:float}
  - upcoming_reservations: list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str}
- Navigation:
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
- Element IDs:
  - menu-page (Div): Main container
  - menu-grid (Div): Grid of dish cards
  - view-dish-button-{{ dish.dish_id }} (Button): View dish details
  - back-to-dashboard (Button): Navigate back to dashboard
- Context Variables:
  - menu: list of dict {dish_id:int, name:str, category:str, price:float, description:str}
- Navigation:
  - view-dish-button-{{ dish.dish_id }} => url_for('dish_details', dish_id=dish.dish_id)
  - back-to-dashboard => url_for('dashboard')

### 3. dish_details.html
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Element IDs:
  - dish-details-page (Div): Main container
  - dish-name (H1): Displays dish['name']
  - dish-price (Div): Displays dish['price'] formatted
  - back-to-menu (Button): Navigate back to menu
- Context Variables:
  - dish: dict {dish_id:int, name:str, price:float, description:str}
- Navigation:
  - back-to-menu => url_for('menu')

### 4. make_reservation.html
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Element IDs:
  - reservation-page (Div): Main container
  - guest-name (Input:text): Guest name input
  - party-size (Dropdown): Select 1-10
  - reservation-date (Input:date): Select date
  - submit-reservation-button (Button): Submit form
  - back-to-dashboard (Button): Navigate back
- Context Variables:
  - None
- Form:
  - action = url_for('make_reservation'), method = POST
  - Form fields: guest_name, party_size, reservation_date
- Navigation:
  - back-to-dashboard => url_for('dashboard')

### 5. my_reservations.html
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Element IDs:
  - my-reservations-page (Div): Main container
  - reservations-table (Table): Displays reservations with columns: date, time, party_size, status
  - cancel-reservation-button-{{ reservation.reservation_id }} (Button): Cancel upcoming reservation
  - back-to-dashboard (Button): Navigate back
- Context Variables:
  - reservations: list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str}
- Navigation:
  - cancel-reservation-button actions trigger POST to /cancel_reservation/<reservation_id>
  - back-to-dashboard => url_for('dashboard')

### 6. waitlist.html
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Element IDs:
  - waitlist-page (Div): Main container
  - waitlist-party-size (Dropdown): Select party size
  - join-waitlist-button (Button): Join waitlist
  - user-position (Div): Show current user position or "Not in waitlist"
  - back-to-dashboard (Button): Navigate back
- Context Variables:
  - position: int or None
- Form:
  - action = url_for('waitlist'), method = POST
  - Form fields: party_size
- Navigation:
  - back-to-dashboard => url_for('dashboard')

### 7. my_reviews.html
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs:
  - reviews-page (Div): Main container
  - reviews-list (Div): List reviews with dish_name, rating, review_text
  - write-new-review-button (Button): Navigate to write_review
  - back-to-dashboard (Button): Navigate back
- Context Variables:
  - reviews: list of dict {review_id:int, dish_name:str, rating:int, review_text:str}
- Navigation:
  - write-new-review-button => url_for('write_review')
  - back-to-dashboard => url_for('dashboard')

### 8. write_review.html
- Filename: templates/write_review.html
- Page Title: Write Review
- Element IDs:
  - write-review-page (Div): Main container
  - select-dish (Dropdown): Select dish to review
  - rating-input (Dropdown): Select rating 1-5 stars
  - review-text (Textarea): Write review
  - submit-review-button (Button): Submit form
  - back-to-reviews (Button): Navigate back to my_reviews
- Context Variables:
  - dishes: list of dict {dish_id:int, name:str}
- Form:
  - action = url_for('write_review'), method = POST
  - Form fields: dish_id, rating, review_text
- Navigation:
  - back-to-reviews => url_for('my_reviews')

### 9. profile.html
- Filename: templates/profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (Div): Main container
  - profile-username (Div): Display username (read-only)
  - profile-email (Input:text): Update email
  - update-profile-button (Button): Submit form
  - back-to-dashboard (Button): Navigate back
- Context Variables:
  - user: dict {username:str, email:str}
- Form:
  - action = url_for('profile'), method = POST
  - Form fields: email
- Navigation:
  - back-to-dashboard => url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format (pipe-delimited): username|email|phone|full_name
- Description: Stores user profile information.
- Fields:
  - username: Unique user login name (str)
  - email: User email address (str)
  - phone: User phone number (str)
  - full_name: Full name of the user (str)
- Example Rows:
  - john_diner|john@example.com|555-1234|John Diner
  - jane_food|jane@example.com|555-5678|Jane Foodie

### 2. menu.txt
- Path: data/menu.txt
- Format (pipe-delimited): dish_id|name|category|price|description|ingredients|dietary|avg_rating
- Description: Stores restaurant menu items.
- Fields:
  - dish_id: Unique integer identifier for dish
  - name: Name of dish (str)
  - category: Category of dish (Appetizers, Main Course, Desserts, Beverages) (str)
  - price: Price in dollars (float)
  - description: Description of dish (str)
  - ingredients: Comma-separated list of ingredients (str)
  - dietary: Dietary designation (Vegetarian, Gluten-Free, Vegan, etc.) (str)
  - avg_rating: Average rating from all reviews (float)
- Example Rows:
  - 1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  - 2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  - 3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  - 4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6

### 3. reservations.txt
- Path: data/reservations.txt
- Format (pipe-delimited): reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
- Description: Stores reservations data.
- Fields:
  - reservation_id: Unique integer ID
  - username: User who made reservation (str)
  - guest_name: Name of guest (str)
  - phone: Contact phone (str)
  - email: Contact email (str)
  - party_size: Number of guests (int)
  - date: Reservation date (YYYY-MM-DD) (str)
  - time: Reservation time (HH:MM) (str)
  - special_requests: Optional special requests (str)
  - status: Reservation status (Upcoming, Completed, Cancelled) (str)
- Example Rows:
  - 1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  - 2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  - 3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming

### 4. waitlist.txt
- Path: data/waitlist.txt
- Format (pipe-delimited): waitlist_id|username|party_size|join_time|status
- Description: Stores waitlist entries.
- Fields:
  - waitlist_id: Unique integer ID
  - username: User on waitlist (str)
  - party_size: Number of guests (int)
  - join_time: Timestamp of joining (YYYY-MM-DD HH:MM:SS) (str)
  - status: Entry status (Active, Completed) (str)
- Example Rows:
  - 1|john_diner|2|2024-11-22 18:30:00|Active
  - 2|jane_food|4|2024-11-22 18:45:00|Active

### 5. reviews.txt
- Path: data/reviews.txt
- Format (pipe-delimited): review_id|username|dish_id|rating|review_text|review_date
- Description: Stores user reviews for dishes.
- Fields:
  - review_id: Unique integer ID
  - username: User who wrote review (str)
  - dish_id: Dish reviewed (int)
  - rating: Rating 1 to 5 (int)
  - review_text: Text of review (str)
  - review_date: Date of review (YYYY-MM-DD) (str)
- Example Rows:
  - 1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  - 2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  - 3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19

---

*This specification fully supports independent backend and frontend implementation of the RestaurantReservation web application as per given requirements.*
