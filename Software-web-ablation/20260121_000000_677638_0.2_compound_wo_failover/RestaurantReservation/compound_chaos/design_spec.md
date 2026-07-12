# RestaurantReservation Web Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path                 | Function Name           | HTTP Methods | Template File                  | Context Variables                                                                                                     | Request Form Fields (POST)                         |
|--------------------------|-------------------------|--------------|-------------------------------|-----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| /                        | root_redirect            | GET          | None (redirects to /dashboard)| None                                                                                                                  | None                                             |
| /dashboard               | dashboard                | GET          | dashboard.html                | username: str
featured_dishes: list of dict {dish_id: int, name: str, price: float, description: str}
upcoming_reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
 | None                                             |
| /menu                    | menu                     | GET          | menu.html                     | menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str, dietary: str, avg_rating: float} | None                                             |
| /dish/<int:dish_id>      | dish_details             | GET          | dish_details.html             | dish: dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | None                                             |
| /make_reservation        | make_reservation         | GET, POST    | make_reservation.html         | None for GET; on GET show form
On POST return success/failure message or redirect accordingly                                  | guest_name: str
party_size: int (1-10)
reservation_date: str (YYYY-MM-DD) |
| /my_reservations         | my_reservations          | GET          | my_reservations.html          | reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
username: str             | None                                             |
| /cancel_reservation/<int:reservation_id> | cancel_reservation        | POST         | None (redirect or JSON response)| reservation_id: int (from URL)                                                                                         | None (reservation_id from URL)                    |
| /waitlist                | waitlist                 | GET, POST    | waitlist.html                 | waitlist_entries: list of dict {waitlist_id: int, username: str, party_size: int, join_time: str, status: str}
user_position: int or None if not in waitlist | party_size: int (POST only)                       |
| /my_reviews              | my_reviews               | GET          | my_reviews.html               | reviews: list of dict {review_id:int, dish_name: str, rating:int, review_text:str}
username: str                       | None                                             |
| /write_review            | write_review             | GET, POST    | write_review.html             | dishes: list of dict {dish_id: int, name: str}
On GET to render form; on POST show submission result or redirect         | dish_id: int
rating: int (1-5)
review_text: str                            |
| /profile                 | profile                  | GET, POST    | profile.html                  | profile: dict {username: str, email: str}                                                                             | email: str (for update)                           |


---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Element IDs:
  - dashboard-page (Div): Container for dashboard page
  - welcome-message (H1): Displays username welcome message
  - make-reservation-button (Button): Navigate to reservation page
  - view-menu-button (Button): Navigate to menu page
  - back-to-dashboard (Button): Refresh dashboard
  - my-reservations-button (Button): Navigate to my reservations page
  - my-reviews-button (Button): Navigate to my reviews page
  - waitlist-button (Button): Navigate to waitlist page
  - profile-button (Button): Navigate to profile page
- Context Variables:
  - username: str
  - featured_dishes: list of dict {dish_id, name, price, description}
  - upcoming_reservations: list of dict {reservation_id, date, time, party_size, status}
- Navigation (url_for function names):
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
  - menu-grid (Div): Grid displaying dish cards
  - view-dish-button-{{ dish.dish_id }} (Button): View dish details button for each dish
  - back-to-dashboard (Button): Back to dashboard
- Context Variables:
  - menus: list of dict {dish_id, name, category, price, description, dietary, avg_rating}
- Navigation:
  - view-dish-button-{{ dish.dish_id }}: url_for('dish_details', dish_id=dish.dish_id)
  - back-to-dashboard: url_for('dashboard')

### 3. Dish Details Page
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Element IDs:
  - dish-details-page (Div): Container
  - dish-name (H1): Dish name
  - dish-price (Div): Dish price
  - back-to-menu (Button): Back to menu
- Context Variables:
  - dish: dict {dish_id, name, category, price, description, ingredients, dietary, avg_rating}
- Navigation:
  - back-to-menu: url_for('menu')

### 4. Make Reservation Page
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Element IDs:
  - reservation-page (Div): Container
  - guest-name (Input, text): Guest name input
  - party-size (Dropdown): Party size select (1-10)
  - reservation-date (Input, date): Reservation date
  - submit-reservation-button (Button): Submit form
  - back-to-dashboard (Button): Navigate back
- Context Variables:
  - None for GET
- Form:
  - action: url_for('make_reservation')
  - method: POST
  - fields: guest_name, party_size, reservation_date
- Navigation:
  - back-to-dashboard: url_for('dashboard')

### 5. My Reservations Page
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Element IDs:
  - my-reservations-page (Div): Container
  - reservations-table (Table): Reservations list
  - cancel-reservation-button-{{ reservation.reservation_id }} (Button): Cancel button for each upcoming reservation
  - back-to-dashboard (Button): Back to dashboard
- Context Variables:
  - reservations: list of dict {reservation_id, date, time, party_size, status}
- Navigation:
  - cancel-reservation-button-{{ reservation.reservation_id }}: form action to /cancel_reservation/<reservation_id> POST
  - back-to-dashboard: url_for('dashboard')

### 6. Waitlist Page
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Element IDs:
  - waitlist-page (Div): Container
  - waitlist-party-size (Dropdown): Select party size
  - join-waitlist-button (Button): Submit join waitlist form
  - user-position (Div): Display user's current position or message if not in waitlist
  - back-to-dashboard (Button): Back to dashboard
- Context Variables:
  - waitlist_entries: list of dict {waitlist_id, username, party_size, join_time, status}
  - user_position: int or null
- Form:
  - action: url_for('waitlist')
  - method: POST
  - fields: party_size
- Navigation:
  - back-to-dashboard: url_for('dashboard')

### 7. My Reviews Page
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs:
  - reviews-page (Div): Container
  - reviews-list (Div): List of reviews
  - write-new-review-button (Button): Navigate to write review
  - back-to-dashboard (Button): Back to dashboard
- Context Variables:
  - reviews: list of dict {review_id, dish_name, rating, review_text}
- Navigation:
  - write-new-review-button: url_for('write_review')
  - back-to-dashboard: url_for('dashboard')

### 8. Write Review Page
- Filename: templates/write_review.html
- Page Title: Write Review
- Element IDs:
  - write-review-page (Div): Container
  - select-dish (Dropdown): Select dish to review
  - rating-input (Dropdown): Select rating 1-5 stars
  - review-text (Textarea): Review text input
  - submit-review-button (Button): Submit form
  - back-to-reviews (Button): Back to My Reviews
- Context Variables:
  - dishes: list of dict {dish_id, name}
- Form:
  - action: url_for('write_review')
  - method: POST
  - fields: dish_id, rating, review_text
- Navigation:
  - back-to-reviews: url_for('my_reviews')

### 9. User Profile Page
- Filename: templates/profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (Div): Container
  - profile-username (Div): Display username
  - profile-email (Input): Editable email field
  - update-profile-button (Button): Submit updated email
  - back-to-dashboard (Button): Back to dashboard
- Context Variables:
  - profile: dict {username, email}
- Form:
  - action: url_for('profile')
  - method: POST
  - fields: email
- Navigation:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format: pipe-delimited
- Fields:
  - username: str - unique user identifier
  - email: str - user email
  - phone: str - user phone number
  - full_name: str - user's full name
- Example rows:
  - john_diner|john@example.com|555-1234|John Diner
  - jane_food|jane@example.com|555-5678|Jane Foodie

### 2. menu.txt
- Path: data/menu.txt
- Format: pipe-delimited
- Fields:
  - dish_id: int - unique dish identifier
  - name: str - name of dish
  - category: str - category such as Appetizers, Main Course, Desserts, Beverages
  - price: float - price in dollars
  - description: str - brief description
  - ingredients: str - comma separated list of ingredients
  - dietary: str - dietary notes (e.g., Vegetarian, Vegan, Gluten-Free)
  - avg_rating: float - average rating
- Example rows:
  - 1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  - 2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  - 3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  - 4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6

### 3. reservations.txt
- Path: data/reservations.txt
- Format: pipe-delimited
- Fields:
  - reservation_id: int - unique reservation id
  - username: str - user who made the reservation
  - guest_name: str - name of guest
  - phone: str - phone number
  - email: str - email
  - party_size: int - number of guests
  - date: str (YYYY-MM-DD) - reservation date
  - time: str (HH:MM) - reservation time
  - special_requests: str - any special requests
  - status: str - e.g. Upcoming, Completed, Cancelled
- Example rows:
  - 1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  - 2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  - 3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming

### 4. waitlist.txt
- Path: data/waitlist.txt
- Format: pipe-delimited
- Fields:
  - waitlist_id: int - unique waitlist entry id
  - username: str - user who joined waitlist
  - party_size: int - party size
  - join_time: str (YYYY-MM-DD HH:MM:SS) - time joined
  - status: str - e.g. Active, Removed
- Example rows:
  - 1|john_diner|2|2024-11-22 18:30:00|Active
  - 2|jane_food|4|2024-11-22 18:45:00|Active

### 5. reviews.txt
- Path: data/reviews.txt
- Format: pipe-delimited
- Fields:
  - review_id: int - unique review id
  - username: str - user who made the review
  - dish_id: int - dish being reviewed
  - rating: int (1-5) - rating stars
  - review_text: str - review content
  - review_date: str (YYYY-MM-DD) - date of review
- Example rows:
  - 1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  - 2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  - 3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19

---

This design specification fully supports parallel and independent development of the backend and frontend components of the RestaurantReservation application, with detailed routes, template information, and data file schemas.
