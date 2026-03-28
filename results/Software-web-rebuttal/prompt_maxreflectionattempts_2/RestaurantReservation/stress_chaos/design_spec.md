# Design Specification for RestaurantReservation Flask Application

---

## 1. Flask Routes Specification

| URL Path                 | Function Name           | HTTP Method(s) | Template File Rendered             | Context Variables Passed to Template                         | Request Form Fields Expected (POST)                      |
|--------------------------|-------------------------|----------------|----------------------------------|-------------------------------------------------------------|----------------------------------------------------------|
| /                        | root_redirect           | GET            | None (redirect 302 to /dashboard) | None                                                        | None                                                     |
| /dashboard               | dashboard               | GET            | dashboard.html                   | username (str), featured_dishes (list of dict), upcoming_reservations (list of dict) | None                                                     |
| /menu                    | menu_page               | GET            | menu.html                       | menus (list of dict)                                         | None                                                     |
| /menu/<int:dish_id>      | dish_details            | GET            | dish_details.html               | dish (dict)                                                | None                                                     |
| /make_reservation        | make_reservation        | GET, POST       | make_reservation.html           | None (GET), errors (dict) (POST failure)                   | guest_name (str), party_size (int), reservation_date (str), special_requests (str - optional) |
| /my_reservations         | my_reservations         | GET            | my_reservations.html            | reservations (list of dict)                                 | None                                                     |
| /cancel_reservation      | cancel_reservation      | POST           | None (redirect to /my_reservations) | None                                                     | reservation_id (int)                                      |
| /waitlist                | waitlist_page           | GET, POST       | waitlist.html                   | waitlist_position (int or None)                           | party_size (int)                                         |
| /my_reviews              | my_reviews              | GET            | my_reviews.html                 | reviews (list of dict)                                     | None                                                     |
| /write_review            | write_review            | GET, POST       | write_review.html               | menus (list of dict) (GET)                                 | dish_id (int), rating (int), review_text (str)           |
| /profile                 | profile                 | GET, POST       | profile.html                   | user_profile (dict)                                       | email (str), phone (str)                                 |

---

## 2. HTML Template Specifications

### 2.1 templates/dashboard.html
- Page Title: Restaurant Dashboard
- Element IDs:
  - dashboard-page (div): Main container
  - welcome-message (h1): Welcome message including username
  - make-reservation-button (button): Navigates to route 'make_reservation'
  - view-menu-button (button): Navigates to route 'menu_page'
  - back-to-dashboard (button): Refresh current dashboard
  - my-reservations-button (button): Navigates to route 'my_reservations'
  - my-reviews-button (button): Navigates to route 'my_reviews'
  - waitlist-button (button): Navigates to route 'waitlist_page'
  - profile-button (button): Navigates to route 'profile'
- Context Variables:
  - username (str)
  - featured_dishes (list of dict)
  - upcoming_reservations (list of dict)

### 2.2 templates/menu.html
- Page Title: Restaurant Menu
- Element IDs:
  - menu-page (div): Main container
  - menu-grid (div): Grid of dish cards
  - view-dish-button-{{ dish_id }} (button): Button to view dish details
  - back-to-dashboard (button): Navigates to 'dashboard'
- Context Variables:
  - menus (list of dict with keys: dish_id (int), name (str), category (str), price (float), description (str))

### 2.3 templates/dish_details.html
- Page Title: Dish Details
- Element IDs:
  - dish-details-page (div): Main container
  - dish-name (h1): Dish name
  - dish-price (div): Price
  - back-to-menu (button): Navigates to 'menu_page'
- Context Variables:
  - dish (dict with fields name (str), price (float), description (str))

### 2.4 templates/make_reservation.html
- Page Title: Make Reservation
- Element IDs:
  - reservation-page (div): Main container
  - guest-name (input text): Guest name input
  - party-size (select): Party size dropdown (1 to 10)
  - reservation-date (input date): Reservation date picker
  - submit-reservation-button (button): Submit reservation
  - back-to-dashboard (button): Navigate to 'dashboard'
- Context Variables:
  - errors (dict) (optional, if POST validation fails)
- POST Form Fields:
  - guest_name (str)
  - party_size (int)
  - reservation_date (str)
  - special_requests (str, optional)

### 2.5 templates/my_reservations.html
- Page Title: My Reservations
- Element IDs:
  - my-reservations-page (div): Main container
  - reservations-table (table): Display reservation list with date, time, party_size, status
  - cancel-reservation-button-{{ reservation_id }} (button): Cancel button
  - back-to-dashboard (button): Navigate to 'dashboard'
- Context Variables:
  - reservations (list of dict)

### 2.6 templates/waitlist.html
- Page Title: Waitlist
- Element IDs:
  - waitlist-page (div): Main container
  - waitlist-party-size (select): Dropdown for party size to join waitlist
  - join-waitlist-button (button): Join waitlist submit
  - user-position (div): Display user's current waitlist position
  - back-to-dashboard (button): Navigate to 'dashboard'
- Context Variables:
  - waitlist_position (int or None)
- POST Form Fields:
  - party_size (int)

### 2.7 templates/my_reviews.html
- Page Title: My Reviews
- Element IDs:
  - reviews-page (div): Container
  - reviews-list (div): List of reviews
  - write-new-review-button (button): Navigate to 'write_review'
  - back-to-dashboard (button): Navigate to 'dashboard'
- Context Variables:
  - reviews (list of dict with keys review_id (int), dish_name (str), rating (int), review_text (str))

### 2.8 templates/write_review.html
- Page Title: Write Review
- Element IDs:
  - write-review-page (div): Container
  - select-dish (select): Dropdown of dishes
  - rating-input (select): Rating dropdown 1-5 stars
  - review-text (textarea): Review text area
  - submit-review-button (button): Submit review
  - back-to-reviews (button): Navigate to 'my_reviews'
- Context Variables:
  - menus (list of dict)
- POST Form Fields:
  - dish_id (int)
  - rating (int)
  - review_text (str)

### 2.9 templates/profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (div): Container
  - profile-username (div): Display username (not editable)
  - profile-email (input text): Editable email input
  - profile-phone (input text): Editable phone input
  - update-profile-button (button): Save profile changes
  - back-to-dashboard (button): Navigate to 'dashboard'
- Context Variables:
  - user_profile (dict with keys username (str), email (str), phone (str))
- POST Form Fields:
  - email (str)
  - phone (str)

---

## 3. Data File Schemas

### 3.1 users.txt
- Relative Path: data/users.txt
- Format: username|email|phone|full_name
- Description: Stores user profile data.
- Fields:
  - username (string): Unique user identifier.
  - email (string): User email address.
  - phone (string): User phone number.
  - full_name (string): Full user name.
- Example Rows:
  ```
john_diner|john@example.com|555-1234|John Diner
jane_food|jane@example.com|555-5678|Jane Foodie
```

### 3.2 menu.txt
- Relative Path: data/menu.txt
- Format: dish_id|name|category|price|description|ingredients|dietary|avg_rating
- Description: Contains all menu dishes and details.
- Fields:
  - dish_id (int): Unique dish identifier.
  - name (string): Dish name.
  - category (string): Dish category.
  - price (float): Dish price.
  - description (string): Description of dish.
  - ingredients (string): Comma separated list of ingredients.
  - dietary (string): Dietary information (e.g. Vegetarian, Vegan).
  - avg_rating (float): Average rating.
- Example Rows:
  ```
1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
```

### 3.3 reservations.txt
- Relative Path: data/reservations.txt
- Format: reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
- Description: Stores reservations made by users.
- Fields:
  - reservation_id (int): Unique reservation identifier.
  - username (string): Username who made the reservation.
  - guest_name (string): Name of guest.
  - phone (string): Phone number.
  - email (string): Email address.
  - party_size (int): Number of guests.
  - date (string, YYYY-MM-DD): Reservation date.
  - time (string, HH:MM): Reservation time.
  - special_requests (string): Special requests.
  - status (string): Reservation status (Upcoming, Completed, Cancelled).
- Example Rows:
  ```
1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
```

### 3.4 waitlist.txt
- Relative Path: data/waitlist.txt
- Format: waitlist_id|username|party_size|join_time|status
- Description: Stores active and removed waitlist entries.
- Fields:
  - waitlist_id (int): Unique waitlist entry ID.
  - username (string): Username on waitlist.
  - party_size (int): Number of guests.
  - join_time (string, YYYY-MM-DD HH:MM:SS): Timestamp when joined.
  - status (string): Status, e.g. Active, Removed.
- Example Rows:
  ```
1|john_diner|2|2024-11-22 18:30:00|Active
2|jane_food|4|2024-11-22 18:45:00|Active
```

### 3.5 reviews.txt
- Relative Path: data/reviews.txt
- Format: review_id|username|dish_id|rating|review_text|review_date
- Description: Stores user reviews for dishes.
- Fields:
  - review_id (int): Unique review identifier.
  - username (string): Username who wrote the review.
  - dish_id (int): ID of dish reviewed.
  - rating (int): Rating (1-5 stars).
  - review_text (string): The review text.
  - review_date (string, YYYY-MM-DD): Date of review.
- Example Rows:
  ```
1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
```

---

# End of Design Specification
