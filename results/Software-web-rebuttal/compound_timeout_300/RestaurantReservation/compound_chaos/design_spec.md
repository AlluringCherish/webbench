# RestaurantReservation Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path                 | Function Name           | HTTP Methods | Template File                 | Context Variables (name:type)                                                                                 | Request Form Fields (POST)                                  |
|--------------------------|-------------------------|--------------|-------------------------------|---------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| /                        | root_redirect            | GET          | -                             | -                                                                                                             | -                                                          |
| /dashboard               | dashboard               | GET          | dashboard.html                | username:str, featured_dishes:list of dict (dish_id:int, name:str, price:float, description:str), upcoming_reservations:list of dict (reservation_id:int, date:str, time:str, party_size:int, status:str) | -                                                          |
| /menu                    | menu                    | GET          | menu.html                     | menus:list of dict (dish_id:int, name:str, category:str, price:float, description:str, dietary:str, avg_rating:float)                                                                               | -                                                          |
| /dish/<int:dish_id>      | dish_details            | GET          | dish_details.html             | dish: dict (dish_id:int, name:str, price:float, description:str)                                               | -                                                          |
| /make-reservation        | make_reservation         | GET          | make_reservation.html         | -                                                                                                             | -                                                          |
| /make-reservation        | submit_reservation       | POST         | reservation_confirmation.html or redirect /my-reservations    | -                                                                                                             | guest_name:str, party_size:int (1-10), reservation_date:str (YYYY-MM-DD)                       |
| /my-reservations         | my_reservations          | GET          | my_reservations.html          | reservations:list of dict (reservation_id:int, date:str, time:str, party_size:int, status:str)                  | -                                                          |
| /cancel-reservation/<int:reservation_id> | cancel_reservation       | POST         | redirect /my-reservations     | -                                                                                                             | -                                                          |
| /waitlist                | waitlist                 | GET          | waitlist.html                 | user_position:int or None (user's place in waitlist if any)                                                    | -                                                          |
| /waitlist                | join_waitlist            | POST         | redirect /waitlist            | -                                                                                                             | party_size:int                                           |
| /my-reviews              | my_reviews               | GET          | my_reviews.html               | reviews:list of dict (review_id:int, dish_name:str, rating:int, review_text:str)                               | -                                                          |
| /write-review            | write_review             | GET          | write_review.html             | dishes:list of dict (dish_id:int, name:str)                                                                    | -                                                          |
| /write-review            | submit_review            | POST         | redirect /my-reviews          | -                                                                                                             | dish_id:int, rating:int (1-5), review_text:str             |
| /profile                 | profile                  | GET          | profile.html                  | username:str, email:str                                                                                         | -                                                          |
| /profile                 | update_profile           | POST         | redirect /profile             | -                                                                                                             | email:str                                                 |

**Route descriptions:**
- The root URL (`/`) redirects to `/dashboard`.
- `make_reservation` GET route serves the reservation form.
- Reservation submission and cancellation are POST routes.
- Waitlist page supports viewing and joining (GET and POST).
- Review write and submission handled by separate GET and POST routes.
- Profile page for viewing and updating user profile.


---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- **Filename:** templates/dashboard.html
- **Page Title:** Restaurant Dashboard
- **Element IDs:**
  - `dashboard-page` (Div): Main container for dashboard.
  - `welcome-message` (H1): Displays welcome with username.
  - `make-reservation-button` (Button): Navigate to make reservation page.
  - `view-menu-button` (Button): Navigate to menu page.
  - `back-to-dashboard` (Button): Refresh dashboard.
  - `my-reservations-button` (Button): Navigate to my reservations.
  - `my-reviews-button` (Button): Navigate to my reviews.
  - `waitlist-button` (Button): Navigate to waitlist page.
  - `profile-button` (Button): Navigate to profile page.

- **Context Variables:**
  - `username` (str)
  - `featured_dishes` (list of dict) with keys: dish_id (int), name (str), price (float), description (str)
  - `upcoming_reservations` (list of dict) with keys: reservation_id (int), date (str), time (str), party_size (int), status (str)

- **Navigation:**
  - `make-reservation-button` -> `url_for('make_reservation')`
  - `view-menu-button` -> `url_for('menu')`
  - `back-to-dashboard` -> reload current page
  - `my-reservations-button` -> `url_for('my_reservations')`
  - `my-reviews-button` -> `url_for('my_reviews')`
  - `waitlist-button` -> `url_for('waitlist')`
  - `profile-button` -> `url_for('profile')`


### 2. Menu Page
- **Filename:** templates/menu.html
- **Page Title:** Restaurant Menu
- **Element IDs:**
  - `menu-page` (Div): Container for menu page.
  - `menu-grid` (Div): Grid housing dish cards.
  - `view-dish-button-{{ dish.dish_id }}` (Button, dynamic): View details of each dish.
  - `back-to-dashboard` (Button): Navigate back to dashboard.

- **Context Variables:**
  - `menus` (list of dict) with keys: dish_id (int), name (str), category (str), price (float), description (str), dietary (str), avg_rating (float)

- **Navigation:**
  - Each `view-dish-button-{{ dish.dish_id }}` -> `url_for('dish_details', dish_id=dish.dish_id)`
  - `back-to-dashboard` -> `url_for('dashboard')`


### 3. Dish Details Page
- **Filename:** templates/dish_details.html
- **Page Title:** Dish Details
- **Element IDs:**
  - `dish-details-page` (Div): Container for dish details.
  - `dish-name` (H1): Name of dish.
  - `dish-price` (Div): Price display.
  - `back-to-menu` (Button): Navigate back to menu.

- **Context Variables:**
  - `dish` (dict): dish_id (int), name (str), price (float), description (str)

- **Navigation:**
  - `back-to-menu` -> `url_for('menu')`


### 4. Make Reservation Page
- **Filename:** templates/make_reservation.html
- **Page Title:** Make Reservation
- **Element IDs:**
  - `reservation-page` (Div): Container
  - `guest-name` (Input): For guest name input (name="guest_name")
  - `party-size` (Dropdown): Party size selection 1-10 (name="party_size")
  - `reservation-date` (Input type date): Reservation date (name="reservation_date")
  - `submit-reservation-button` (Button): Submit reservation form
  - `back-to-dashboard` (Button): Navigate back to dashboard

- **Context Variables:** None

- **Navigation:**
  - Form action: POST to `/make-reservation`
  - `back-to-dashboard` -> `url_for('dashboard')`


### 5. My Reservations Page
- **Filename:** templates/my_reservations.html
- **Page Title:** My Reservations
- **Element IDs:**
  - `my-reservations-page` (Div): Container
  - `reservations-table` (Table): Display reservations with columns: date, time, party size, status
  - `cancel-reservation-button-{{ reservation.reservation_id }}` (Button, dynamic): Cancel reservation
  - `back-to-dashboard` (Button): Navigate back to dashboard

- **Context Variables:**
  - `reservations` (list of dict): reservation_id (int), date (str), time (str), party_size (int), status (str)

- **Navigation:**
  - Cancel buttons form POST to `/cancel-reservation/<reservation_id>`
  - `back-to-dashboard` -> `url_for('dashboard')`


### 6. Waitlist Page
- **Filename:** templates/waitlist.html
- **Page Title:** Waitlist
- **Element IDs:**
  - `waitlist-page` (Div): Container
  - `waitlist-party-size` (Dropdown): Party size selection (name="party_size")
  - `join-waitlist-button` (Button): Submit join
  - `user-position` (Div): Display current user position or text if none
  - `back-to-dashboard` (Button): Navigate back to dashboard

- **Context Variables:**
  - `user_position` (int or None) 

- **Navigation:**
  - Form POST action to `/waitlist`
  - `back-to-dashboard` -> `url_for('dashboard')`


### 7. My Reviews Page
- **Filename:** templates/my_reviews.html
- **Page Title:** My Reviews
- **Element IDs:**
  - `reviews-page` (Div): Container
  - `reviews-list` (Div): List of reviews showing dish name, rating, and text
  - `write-new-review-button` (Button): Navigate to write review page
  - `back-to-dashboard` (Button): Navigate back to dashboard

- **Context Variables:**
  - `reviews` (list of dict): review_id (int), dish_name (str), rating (int), review_text (str)

- **Navigation:**
  - `write-new-review-button` -> `url_for('write_review')`
  - `back-to-dashboard` -> `url_for('dashboard')`


### 8. Write Review Page
- **Filename:** templates/write_review.html
- **Page Title:** Write Review
- **Element IDs:**
  - `write-review-page` (Div): Container
  - `select-dish` (Dropdown, name="dish_id"): List of dishes to select from
  - `rating-input` (Dropdown, name="rating"): Ratings 1 to 5
  - `review-text` (Textarea, name="review_text"): Text area for review
  - `submit-review-button` (Button): Submit review
  - `back-to-reviews` (Button): Navigate back to My Reviews

- **Context Variables:**
  - `dishes` (list of dict): dish_id (int), name (str)

- **Navigation:**
  - Form POST action to `/write-review`
  - `back-to-reviews` -> `url_for('my_reviews')`


### 9. User Profile Page
- **Filename:** templates/profile.html
- **Page Title:** My Profile
- **Element IDs:**
  - `profile-page` (Div): Container
  - `profile-username` (Div): Display username (not editable)
  - `profile-email` (Input, name="email"): Editable email field
  - `update-profile-button` (Button): Submit profile update
  - `back-to-dashboard` (Button): Navigate back to dashboard

- **Context Variables:**
  - `username` (str)
  - `email` (str)

- **Navigation:**
  - Form POST to `/profile`
  - `back-to-dashboard` -> `url_for('dashboard')`

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- **Path:** data/users.txt
- **Format:** pipe-delimited
- **Fields:** username|email|phone|full_name
- **Description:** Stores registered user credentials and contact info.
- **Example Rows:**
```
john_diner|john@example.com|555-1234|John Diner
jane_food|jane@example.com|555-5678|Jane Foodie
```


### 2. menu.txt
- **Path:** data/menu.txt
- **Format:** pipe-delimited
- **Fields:** dish_id|name|category|price|description|ingredients|dietary|avg_rating
- **Description:** Stores menu items data including category and average rating.
- **Example Rows:**
```
1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
```


### 3. reservations.txt
- **Path:** data/reservations.txt
- **Format:** pipe-delimited
- **Fields:** reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
- **Description:** Stores all table reservations with status (Upcoming, Completed, etc.).
- **Example Rows:**
```
1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
```


### 4. waitlist.txt
- **Path:** data/waitlist.txt
- **Format:** pipe-delimited
- **Fields:** waitlist_id|username|party_size|join_time|status
- **Description:** Stores waitlist entries with join timestamp and active status.
- **Example Rows:**
```
1|john_diner|2|2024-11-22 18:30:00|Active
2|jane_food|4|2024-11-22 18:45:00|Active
```


### 5. reviews.txt
- **Path:** data/reviews.txt
- **Format:** pipe-delimited
- **Fields:** review_id|username|dish_id|rating|review_text|review_date
- **Description:** Stores user reviews with ratings and review text.
- **Example Rows:**
```
1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
```

---

**End of Design Specification for RestaurantReservation Application**
