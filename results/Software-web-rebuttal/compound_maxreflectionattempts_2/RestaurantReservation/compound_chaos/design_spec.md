# RestaurantReservation Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path                 | Function Name           | HTTP Methods | Template File                 | Context Variables (name:type)                                                                                 | Request Form Fields (POST)                                  |
|--------------------------|-------------------------|--------------|-------------------------------|---------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| /                        | root_redirect           | GET          | -                             | -                                                                                                             | -                                                          |
| /dashboard               | dashboard               | GET          | dashboard.html                | username:str, featured_dishes:list of dict (dish_id:int, name:str, price:float, description:str), 
|                          |                        |              |                               | upcoming_reservations:list of dict (reservation_id:int, date:str, time:str, party_size:int, status:str)       | -                                                          |
| /menu                    | menu                    | GET          | menu.html                     | menus:list of dict (dish_id:int, name:str, category:str, price:float, description:str, avg_rating:float)      | -                                                          |
| /dish/<int:dish_id>      | dish_details            | GET          | dish_details.html             | dish:dict (dish_id:int, name:str, price:float, description:str)                                               | -                                                          |
| /make-reservation        | make_reservation        | GET, POST    | make_reservation.html         | - (GET) or submission status (POST)                                                                           | guest_name:str, party_size:int (1-10), reservation_date:str |
| /my-reservations         | my_reservations         | GET          | my_reservations.html          | reservations:list of dict (reservation_id:int, date:str, time:str, party_size:int, status:str)                 | -                                                          |
| /cancel-reservation/<int:reservation_id> | cancel_reservation      | POST         | -                             | -                                                                                                             | none (reservation_id from URL)                             |
| /waitlist                | waitlist                | GET, POST    | waitlist.html                 | waitlist_position:int, user_party_size:int (for GET)                                                          | party_size:int (for POST)                                  |
| /my-reviews              | my_reviews              | GET          | my_reviews.html               | reviews:list of dict (review_id:int, dish_name:str, rating:int, review_text:str), username:str                  | -                                                          |
| /write-review            | write_review            | GET, POST    | write_review.html             | dishes:list of dict (dish_id:int, name:str) (GET), success_message:str or error_message:str (POST)            | select_dish:int (dish_id), rating:int (1-5), review_text:str |
| /profile                 | profile                 | GET, POST    | profile.html                  | user_profile: dict (username:str, email:str)                                                                   | profile_email:str                                          |

### Route Descriptions:
- **/** : Redirects to /dashboard.
- **/dashboard** : Displays main dashboard with user greeting, featured dishes, upcoming reservations, and navigation buttons.
- **/menu** : Shows full restaurant menu with dish cards.
- **/dish/<dish_id>** : Shows detail page for selected dish.
- **/make-reservation** : GET shows form; POST to submit reservation form.
- **/my-reservations** : Shows all reservations for logged-in user with cancel option.
- **/cancel-reservation/<reservation_id>** : POST endpoint to cancel a reservation.
- **/waitlist** : GET shows waitlist join form and current position; POST to join waitlist.
- **/my-reviews** : Displays all reviews by user.
- **/write-review** : GET shows form; POST submits new review.
- **/profile** : GET shows user profile; POST updates profile.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Element IDs:
  - dashboard-page (Div): Container for whole dashboard page
  - welcome-message (H1): Displays greeting with username
  - make-reservation-button (Button): Navigates to /make-reservation
  - view-menu-button (Button): Navigates to /menu
  - back-to-dashboard (Button): Refreshes dashboard (reload current page)
  - my-reservations-button (Button): Navigates to /my-reservations
  - my-reviews-button (Button): Navigates to /my-reviews
  - waitlist-button (Button): Navigates to /waitlist
  - profile-button (Button): Navigates to /profile
- Context Variables:
  - username: str
  - featured_dishes: list of dict {dish_id:int, name:str, price:float, description:str}
  - upcoming_reservations: list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str}
- Navigation:
  - make-reservation-button => url_for('make_reservation')
  - view-menu-button => url_for('menu')
  - back-to-dashboard => url_for('dashboard')
  - my-reservations-button => url_for('my_reservations')
  - my-reviews-button => url_for('my_reviews')
  - waitlist-button => url_for('waitlist')
  - profile-button => url_for('profile')

### 2. Menu Page
- Filename: templates/menu.html
- Page Title: Restaurant Menu
- Element IDs:
  - menu-page (Div): Container for menu page
  - menu-grid (Div): Shows dish cards
  - view-dish-button-{{ dish.dish_id }} (Button): Dynamic buttons on each dish card to view details
  - back-to-dashboard (Button): Navigates back to dashboard
- Context Variables:
  - menus: list of dict {dish_id:int, name:str, category:str, price:float, description:str, avg_rating:float}
- Navigation:
  - view-dish-button-{{ dish.dish_id }} => url_for('dish_details', dish_id=dish.dish_id)
  - back-to-dashboard => url_for('dashboard')

### 3. Dish Details Page
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Element IDs:
  - dish-details-page (Div): Container for dish details
  - dish-name (H1): Displays dish name
  - dish-price (Div): Displays dish price
  - back-to-menu (Button): Navigates to /menu
- Context Variables:
  - dish: dict {dish_id:int, name:str, price:float, description:str}
- Navigation:
  - back-to-menu => url_for('menu')

### 4. Make Reservation Page
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Element IDs:
  - reservation-page (Div): Container for reservation form
  - guest-name (Input): Text input for guest name, form field name="guest_name"
  - party-size (Dropdown): Select input for party size 1-10, form field name="party_size"
  - reservation-date (Input date): Date input, form field name="reservation_date"
  - submit-reservation-button (Button): Submits form
  - back-to-dashboard (Button): Navigates back to /dashboard
- Context Variables:
  - None (for GET)
- Navigation & Form:
  - form action="" method="POST"
  - submit-reservation-button submits form
  - back-to-dashboard => url_for('dashboard')

### 5. My Reservations Page
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Element IDs:
  - my-reservations-page (Div): Container
  - reservations-table (Table): Shows reservations rows with columns date, time, party size, status
  - cancel-reservation-button-{{ reservation.reservation_id }} (Button): Cancel upcoming reservation
  - back-to-dashboard (Button): Navigates back to /dashboard
- Context Variables:
  - reservations: list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str}
- Navigation & Form:
  - cancel-reservation-button-{{ reservation.reservation_id }} triggers POST to /cancel-reservation/{{ reservation.reservation_id }}
  - back-to-dashboard => url_for('dashboard')

### 6. Waitlist Page
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Element IDs:
  - waitlist-page (Div): Container
  - waitlist-party-size (Dropdown): Select input for party size, form field name="party_size"
  - join-waitlist-button (Button): Submits join waitlist form
  - user-position (Div): Displays user's current waitlist position
  - back-to-dashboard (Button): Navigates back to /dashboard
- Context Variables:
  - waitlist_position: int (user's current position in waitlist)
  - user_party_size: int (if prefilled/known)
- Navigation & Form:
  - form action="" method="POST"
  - join-waitlist-button submits form
  - back-to-dashboard => url_for('dashboard')

### 7. My Reviews Page
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs:
  - reviews-page (Div): Container
  - reviews-list (Div): Lists reviews with dish name, rating, review text
  - write-new-review-button (Button): Navigates to /write-review
  - back-to-dashboard (Button): Navigates back to /dashboard
- Context Variables:
  - reviews: list of dict {review_id:int, dish_name:str, rating:int, review_text:str}
  - username: str
- Navigation:
  - write-new-review-button => url_for('write_review')
  - back-to-dashboard => url_for('dashboard')

### 8. Write Review Page
- Filename: templates/write_review.html
- Page Title: Write Review
- Element IDs:
  - write-review-page (Div): Container
  - select-dish (Dropdown): Select dish to review, form field name="select_dish"
  - rating-input (Dropdown): Rating 1-5, form field name="rating"
  - review-text (Textarea): Text input area, form field name="review_text"
  - submit-review-button (Button): Submits review form
  - back-to-reviews (Button): Navigates back to /my-reviews
- Context Variables:
  - dishes: list of dict {dish_id:int, name:str} (all dishes for selection)
  - success_message: str (optional after POST)
  - error_message: str (optional after POST)
- Navigation & Form:
  - form action="" method="POST"
  - submit-review-button submits form
  - back-to-reviews => url_for('my_reviews')

### 9. User Profile Page
- Filename: templates/profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (Div): Container
  - profile-username (Div): Displays username (read-only)
  - profile-email (Input): Email update, form field name="profile_email"
  - update-profile-button (Button): Submit profile update
  - back-to-dashboard (Button): Navigates back to /dashboard
- Context Variables:
  - user_profile: dict {username:str, email:str}
- Navigation & Form:
  - form action="" method="POST"
  - update-profile-button submits form
  - back-to-dashboard => url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format: Pipe (|) delimited
- Fields & Order:
  - username (str): Unique user identifier
  - email (str): User email address
  - phone (str): User phone number
  - full_name (str): User full name
- Description: Stores registered user details
- Example rows:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

---

### 2. menu.txt
- Path: data/menu.txt
- Format: Pipe (|) delimited
- Fields & Order:
  - dish_id (int): Unique dish identifier
  - name (str): Dish name
  - category (str): Dish category (e.g. Appetizers, Main Course)
  - price (float): Dish price
  - description (str): Description of the dish
  - ingredients (str): Comma-separated list of ingredients
  - dietary (str): Dietary information (e.g. Vegetarian, Gluten-Free, Vegan)
  - avg_rating (float): Average rating for the dish
- Description: Stores menu items
- Example rows:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

---

### 3. reservations.txt
- Path: data/reservations.txt
- Format: Pipe (|) delimited
- Fields & Order:
  - reservation_id (int): Unique reservation id
  - username (str): Username who made reservation
  - guest_name (str): Guest's name
  - phone (str): Contact phone
  - email (str): Contact email
  - party_size (int): Number of people
  - date (str): Reservation date (YYYY-MM-DD)
  - time (str): Reservation time (HH:MM)
  - special_requests (str): Special requests text
  - status (str): Status of reservation (e.g., Upcoming, Completed, Cancelled)
- Description: Stores reservations
- Example rows:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

---

### 4. waitlist.txt
- Path: data/waitlist.txt
- Format: Pipe (|) delimited
- Fields & Order:
  - waitlist_id (int): Unique waitlist entry id
  - username (str): Username on waitlist
  - party_size (int): Party size on waitlist
  - join_time (str): DateTime string when joined (YYYY-MM-DD HH:MM:SS)
  - status (str): Status of waitlist entry (Active/Completed/Cancelled)
- Description: Stores waitlist entries
- Example rows:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

---

### 5. reviews.txt
- Path: data/reviews.txt
- Format: Pipe (|) delimited
- Fields & Order:
  - review_id (int): Unique review id
  - username (str): Username who wrote review
  - dish_id (int): Dish identifier for review
  - rating (int): Rating 1 to 5
  - review_text (str): Review content
  - review_date (str): Date review was written (YYYY-MM-DD)
- Description: Stores user reviews
- Example rows:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```