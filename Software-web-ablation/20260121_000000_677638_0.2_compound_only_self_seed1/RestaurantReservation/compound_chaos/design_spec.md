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
| /menu                    | menu                    | GET          | menu.html                     | menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}                          | None                                             |
| /dish/<int:dish_id>      | dish_details            | GET          | dish_details.html             | dish: dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}                                   | None                                             |
| /make_reservation        | make_reservation        | GET, POST    | make_reservation.html         | None for GET
For POST, on validation error, re-render with errors dictionary {field_name: str}, and preserve entered values: guest_name: str, party_size: int, reservation_date: str | guest_name: str
party_size: int
reservation_date: str                                    |
| /my_reservations         | my_reservations         | GET          | my_reservations.html          | reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}                    | None                                             |
| /cancel_reservation/<int:reservation_id>| cancel_reservation      | POST         | None (redirects back to /my_reservations) | None                                                                                                                  | None                                             |
| /waitlist                | waitlist                | GET, POST    | waitlist.html                 | For GET:
user_position: int or None (if user not in waitlist)

For POST:
On join success, refresh with new position; if error, errors dict: {party_size: str}             | party_size: int                                  |
| /my_reviews              | my_reviews              | GET          | my_reviews.html               | reviews: list of dict {review_id: int, dish_name: str, rating: int, review_text: str, review_date: str}                 | None                                             |
| /write_review            | write_review            | GET, POST    | write_review.html             | dishes: list of dict {dish_id: int, name: str}
On POST with error, errors dict {rating: str, review_text: str}, preserve inputs: dish_id: int, rating: int, review_text: str   | dish_id: int
rating: int
review_text: str                                |
| /profile                 | profile                 | GET, POST    | profile.html                  | For GET:
user_profile: dict {username: str, email: str}
On POST with error, errors dict {email: str}, preserve input email: str                                   | email: str                                       |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Main <h1>: id="welcome-message"

**Element IDs:**
- dashboard-page (div): Container div for dashboard page
- welcome-message (h1): Displays "Welcome, {{ username }}!"
- make-reservation-button (button): Navigates to make_reservation (url_for 'make_reservation')
- view-menu-button (button): Navigates to menu (url_for 'menu')
- back-to-dashboard (button): Refresh current page (url_for 'dashboard')
- my-reservations-button (button): Navigates to my_reservations (url_for 'my_reservations')
- my-reviews-button (button): Navigates to my_reviews (url_for 'my_reviews')
- waitlist-button (button): Navigates to waitlist (url_for 'waitlist')
- profile-button (button): Navigates to profile (url_for 'profile')

**Context Variables:**
- username: str
- featured_dishes: list of dict {dish_id: int, name: str, price: float, description: str}
- upcoming_reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}

**Navigation Mappings:**
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
- Main <h1>: none specified

**Element IDs:**
- menu-page (div): Container for menu page
- menu-grid (div): Displays dish cards in a grid
- view-dish-button-{{ dish.dish_id }} (button): On each dish card, navigates to dish_details for that dish
- back-to-dashboard (button): Navigates to dashboard

**Context Variables:**
- menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}

**Navigation Mappings:**
- view-dish-button-{{ dish.dish_id }} -> url_for('dish_details', dish_id=dish.dish_id)
- back-to-dashboard -> url_for('dashboard')

---

### 3. dish_details.html
- Filename: templates/dish_details.html
- Page Title: Dish Details

**Element IDs:**
- dish-details-page (div): Container div
- dish-name (h1): Displays dish's name
- dish-price (div): Displays dish's price
- back-to-menu (button): Navigates back to menu

**Context Variables:**
- dish: dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}

**Navigation Mappings:**
- back-to-menu -> url_for('menu')

---

### 4. make_reservation.html
- Filename: templates/make_reservation.html
- Page Title: Make Reservation

**Element IDs:**
- reservation-page (div): Container
- guest-name (input, text): Input field for guest name (name="guest_name")
- party-size (select dropdown): Select field for party size (name="party_size", values 1-10)
- reservation-date (input, date): Input field for reservation date (name="reservation_date")
- submit-reservation-button (button, type submit): Submits reservation form
- back-to-dashboard (button): Navigates back to dashboard

**Context Variables:**
- For GET: none
- For POST errors: errors: dict with possible keys 'guest_name', 'party_size', 'reservation_date'
- Previously entered values (guest_name: str, party_size: int, reservation_date: str) to preserve form state

**Form Action and Method:**
- Form action="" (post to same route)
- Method: POST

**Navigation Mappings:**
- back-to-dashboard -> url_for('dashboard')

---

### 5. my_reservations.html
- Filename: templates/my_reservations.html
- Page Title: My Reservations

**Element IDs:**
- my-reservations-page (div): Container div
- reservations-table (table): Displays reservations list
- cancel-reservation-button-{{ reservation.reservation_id }} (button): Cancel button for each upcoming reservation
- back-to-dashboard (button): Navigates back to dashboard

**Context Variables:**
- reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}

**Navigation Mappings:**
- cancel-reservation-button-{{ reservation.reservation_id }}: POST form button to route /cancel_reservation/<int:reservation_id>
- back-to-dashboard -> url_for('dashboard')

---

### 6. waitlist.html
- Filename: templates/waitlist.html
- Page Title: Waitlist

**Element IDs:**
- waitlist-page (div): Container
- waitlist-party-size (select dropdown): Party size selector (name="party_size")
- join-waitlist-button (button, type submit): Join waitlist form button
- user-position (div): Displays user's current waitlist position or message if none
- back-to-dashboard (button): Navigates back to dashboard

**Context Variables:**
- user_position: int or None
- errors: dict (optional) keys related to party_size if POST validation fails

**Form Action and Method:**
- Form submits to same route with POST

**Navigation Mappings:**
- back-to-dashboard -> url_for('dashboard')

---

### 7. my_reviews.html
- Filename: templates/my_reviews.html
- Page Title: My Reviews

**Element IDs:**
- reviews-page (div): Container
- reviews-list (div): Displays list of user reviews
- write-new-review-button (button): Navigates to write_review
- back-to-dashboard (button): Navigates back to dashboard

**Context Variables:**
- reviews: list of dict {review_id: int, dish_name: str, rating: int, review_text: str, review_date: str}

**Navigation Mappings:**
- write-new-review-button -> url_for('write_review')
- back-to-dashboard -> url_for('dashboard')

---

### 8. write_review.html
- Filename: templates/write_review.html
- Page Title: Write Review

**Element IDs:**
- write-review-page (div): Container
- select-dish (select dropdown): Dropdown to select dish (name="dish_id")
- rating-input (select dropdown): Rating select (name="rating", values 1-5)
- review-text (textarea): Review text input (name="review_text")
- submit-review-button (button, type submit): Submit review form
- back-to-reviews (button): Navigate back to my_reviews

**Context Variables:**
- dishes: list of dict {dish_id: int, name: str}
- errors: dict (optional) keys: rating, review_text
- Previously entered values: dish_id, rating, review_text

**Form Action and Method:**
- Form POST to same route

**Navigation Mappings:**
- back-to-reviews -> url_for('my_reviews')

---

### 9. profile.html
- Filename: templates/profile.html
- Page Title: My Profile

**Element IDs:**
- profile-page (div): Container
- profile-username (div): Displays username (read-only)
- profile-email (input, text): Editable email field (name="email")
- update-profile-button (button, type submit): Submit profile update
- back-to-dashboard (button): Navigate back to dashboard

**Context Variables:**
- user_profile: dict {username: str, email: str}
- errors: dict (optional) for email validation
- Previously entered value: email

**Form Action and Method:**
- Form POST to same route

**Navigation Mappings:**
- back-to-dashboard -> url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format: pipe-delimited
  ```
  username|email|phone|full_name
  ```
- Description: Stores user account information
- Fields:
  - username: unique user identifier (str)
  - email: user's email address (str)
  - phone: user's phone number (str)
  - full_name: user's full name (str)
- Examples:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### 2. menu.txt
- Path: data/menu.txt
- Format: pipe-delimited
  ```
  dish_id|name|category|price|description|ingredients|dietary|avg_rating
  ```
- Description: Stores menu dish details
- Fields:
  - dish_id: unique dish identifier (int)
  - name: dish name (str)
  - category: menu category (str), e.g., Appetizers, Main Course
  - price: dish price in USD (float)
  - description: dish description (str)
  - ingredients: comma-separated ingredients (str)
  - dietary: dietary info (str), e.g., Vegetarian, Vegan
  - avg_rating: average rating (float)
- Examples:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### 3. reservations.txt
- Path: data/reservations.txt
- Format: pipe-delimited
  ```
  reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
  ```
- Description: Stores reservation details
- Fields:
  - reservation_id: unique reservation id (int)
  - username: user who made reservation (str)
  - guest_name: name of guest for reservation (str)
  - phone: guest phone number (str)
  - email: guest email (str)
  - party_size: number of guests (int)
  - date: reservation date (YYYY-MM-DD string)
  - time: reservation time (HH:MM 24h format string)
  - special_requests: additional notes (str)
  - status: reservation status (str), e.g., Upcoming, Completed
- Examples:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### 4. waitlist.txt
- Path: data/waitlist.txt
- Format: pipe-delimited
  ```
  waitlist_id|username|party_size|join_time|status
  ```
- Description: Stores current waitlist entries
- Fields:
  - waitlist_id: unique waitlist entry id (int)
  - username: user on waitlist (str)
  - party_size: size of party waiting (int)
  - join_time: timestamp when joined (YYYY-MM-DD HH:MM:SS string)
  - status: waitlist status (str), e.g. Active
- Examples:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### 5. reviews.txt
- Path: data/reviews.txt
- Format: pipe-delimited
  ```
  review_id|username|dish_id|rating|review_text|review_date
  ```
- Description: Stores user reviews for dishes
- Fields:
  - review_id: unique review id (int)
  - username: user who wrote review (str)
  - dish_id: dish being reviewed (int)
  - rating: rating 1-5 stars (int)
  - review_text: review content (str)
  - review_date: date of review (YYYY-MM-DD string)
- Examples:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

---

End of Design Specification Document.
