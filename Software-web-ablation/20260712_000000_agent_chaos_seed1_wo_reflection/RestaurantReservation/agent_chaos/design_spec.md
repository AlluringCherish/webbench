# RestaurantReservation Design Specification

---

## 1. Flask Routes Specification (Backend Developer Focused)

| URL Path                         | Function Name           | HTTP Methods | Template Rendered           | Context Variables (Type & Structure)                                                                                                      | Expected POST Form Fields                                 |
|---------------------------------|-------------------------|--------------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| `/`                             | root_redirect           | GET          | Redirect to /dashboard      | None                                                                                                                                      | None                                                     |
| `/dashboard`                    | dashboard               | GET          | dashboard.html              | username (str), featured_dishes (List[Dict]): [{"dish_id": int, "name": str, "price": float, "description": str}], upcoming_reservations (List[Dict]): [{"reservation_id": int, "date": str, "time": str, "party_size": int, "status": str}] | None                                                     |
| `/menu`                        | menu                    | GET          | menu.html                   | menu_items (List[Dict]): [{"dish_id": int, "name": str, "category": str, "price": float, "description": str}]                    | None                                                     |
| `/dish/<int:dish_id>`          | dish_details            | GET          | dish_details.html           | dish (Dict): {"dish_id": int, "name": str, "price": float, "description": str}                                                     | None                                                     |
| `/reservation`                 | make_reservation        | GET, POST    | reservation.html (GET)      | None                                                                                                                                      | guest_name (str), party_size (int, 1-10), reservation_date (str, YYYY-MM-DD) |
| `/my-reservations`             | my_reservations         | GET          | my_reservations.html        | reservations (List[Dict]): [{"reservation_id": int, "date": str, "time": str, "party_size": int, "status": str}]                 | None                                                     |
| `/cancel-reservation/<int:reservation_id>` | cancel_reservation       | POST         | Redirect to /my-reservations | None                                                                                                                                    | None (triggered by button for specific reservation)       |
| `/waitlist`                   | waitlist                | GET, POST    | waitlist.html (GET)          | user_position (int or None)                                                                                                               | party_size (int)                                         |
| `/my-reviews`                 | my_reviews              | GET          | my_reviews.html             | reviews (List[Dict]): [{"review_id": int, "dish_name": str, "rating": int, "review_text": str}]                                    | None                                                     |
| `/write-review`               | write_review            | GET, POST    | write_review.html (GET)      | dishes (List[Dict]): [{"dish_id": int, "name": str}]                                                                                   | dish_id (int), rating (int, 1-5), review_text (str)       |
| `/profile`                   | user_profile            | GET, POST    | profile.html (GET)           | user_info (Dict): {"username": str, "email": str}                                                                                     | email (str)                                             |

---

## 2. HTML Template Specifications (Frontend Developer Focused)

### dashboard.html
- **Filename:** templates/dashboard.html
- **Page Title:** Restaurant Dashboard
- **Elements:**
  - ID: dashboard-page (Div) - Container for dashboard page
  - ID: welcome-message (H1) - Welcome message displaying username
  - ID: make-reservation-button (Button) - Navigate to make_reservation
  - ID: view-menu-button (Button) - Navigate to menu
  - ID: back-to-dashboard (Button) - Refresh dashboard
  - ID: my-reservations-button (Button) - Navigate to my_reservations
  - ID: my-reviews-button (Button) - Navigate to my_reviews
  - ID: waitlist-button (Button) - Navigate to waitlist
  - ID: profile-button (Button) - Navigate to user_profile
- **Context Variables:**
  - username (str)
  - featured_dishes (List of Dict): dish_id, name, price, description
  - upcoming_reservations (List of Dict): reservation_id, date, time, party_size, status
- **Navigation Mappings:**
  - make-reservation-button: url_for('make_reservation')
  - view-menu-button: url_for('menu')
  - back-to-dashboard: url_for('dashboard')
  - my-reservations-button: url_for('my_reservations')
  - my-reviews-button: url_for('my_reviews')
  - waitlist-button: url_for('waitlist')
  - profile-button: url_for('user_profile')

### menu.html
- **Filename:** templates/menu.html
- **Page Title:** Restaurant Menu
- **Elements:**
  - ID: menu-page (Div) - Container for menu page
  - ID: menu-grid (Div) - Displays dish cards
  - ID: view-dish-button-{dish_id} (Button) - Button to view dish details for each dish
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- **Context Variables:**
  - menu_items (List of Dict): dish_id, name, category, price, description
- **Navigation Mappings:**
  - view-dish-button-{dish_id}: url_for('dish_details', dish_id=dish_id)
  - back-to-dashboard: url_for('dashboard')

### dish_details.html
- **Filename:** templates/dish_details.html
- **Page Title:** Dish Details
- **Elements:**
  - ID: dish-details-page (Div) - Container for dish details page
  - ID: dish-name (H1) - Displays dish name
  - ID: dish-price (Div) - Displays dish price
  - ID: back-to-menu (Button) - Navigate back to menu
- **Context Variables:**
  - dish (Dict): dish_id, name, price, description
- **Navigation Mappings:**
  - back-to-menu: url_for('menu')

### reservation.html
- **Filename:** templates/reservation.html
- **Page Title:** Make Reservation
- **Elements:**
  - ID: reservation-page (Div) - Container for reservation page
  - ID: guest-name (Input) - Text input for guest name
  - ID: party-size (Dropdown) - Dropdown select 1-10 party size
  - ID: reservation-date (Input type=date) - Select reservation date
  - ID: submit-reservation-button (Button) - Submit reservation
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- **Form Action:** POST to url_for('make_reservation')
- **Input Field Names:**
  - guest_name
  - party_size
  - reservation_date
- **Navigation Mappings:**
  - back-to-dashboard: url_for('dashboard')

### my_reservations.html
- **Filename:** templates/my_reservations.html
- **Page Title:** My Reservations
- **Elements:**
  - ID: my-reservations-page (Div) - Container for my reservations page
  - ID: reservations-table (Table) - Displays reservations with columns date, time, party_size, status
  - ID: cancel-reservation-button-{reservation_id} (Button) - Cancel reservation for upcoming
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- **Context Variables:**
  - reservations (List of Dict): reservation_id, date, time, party_size, status
- **Form Actions:** Post cancel request to url_for('cancel_reservation', reservation_id=reservation_id)
- **Navigation Mappings:**
  - back-to-dashboard: url_for('dashboard')

### waitlist.html
- **Filename:** templates/waitlist.html
- **Page Title:** Waitlist
- **Elements:**
  - ID: waitlist-page (Div) - Container for waitlist page
  - ID: waitlist-party-size (Dropdown) - Dropdown to select party size
  - ID: join-waitlist-button (Button) - Join waitlist submit
  - ID: user-position (Div) - Display user's position in waitlist
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- **Form Action:** POST to url_for('waitlist')
- **Input Field Names:**
  - party_size
- **Context Variables:**
  - user_position (int or None)
- **Navigation Mappings:**
  - back-to-dashboard: url_for('dashboard')

### my_reviews.html
- **Filename:** templates/my_reviews.html
- **Page Title:** My Reviews
- **Elements:**
  - ID: reviews-page (Div) - Container for reviews page
  - ID: reviews-list (Div) - List of reviews with dish name, rating, review text
  - ID: write-new-review-button (Button) - Navigate to write_review
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- **Context Variables:**
  - reviews (List of Dict): review_id, dish_name, rating, review_text
- **Navigation Mappings:**
  - write-new-review-button: url_for('write_review')
  - back-to-dashboard: url_for('dashboard')

### write_review.html
- **Filename:** templates/write_review.html
- **Page Title:** Write Review
- **Elements:**
  - ID: write-review-page (Div) - Container for write review page
  - ID: select-dish (Dropdown) - Select dish to review
  - ID: rating-input (Dropdown) - Select rating 1-5
  - ID: review-text (Textarea) - Review text input
  - ID: submit-review-button (Button) - Submit review
  - ID: back-to-reviews (Button) - Navigate back to my_reviews
- **Form Action:** POST to url_for('write_review')
- **Input Field Names:**
  - dish_id
  - rating
  - review_text
- **Context Variables:**
  - dishes (List of Dict): dish_id, name
- **Navigation Mappings:**
  - back-to-reviews: url_for('my_reviews')

### profile.html
- **Filename:** templates/profile.html
- **Page Title:** My Profile
- **Elements:**
  - ID: profile-page (Div) - Container for profile page
  - ID: profile-username (Div) - Displays username (non-editable)
  - ID: profile-email (Input) - Email update
  - ID: update-profile-button (Button) - Save profile changes
  - ID: back-to-dashboard (Button) - Navigate back to dashboard
- **Form Action:** POST to url_for('user_profile')
- **Input Field Names:**
  - email
- **Context Variables:**
  - user_info (Dict): username, email
- **Navigation Mappings:**
  - back-to-dashboard: url_for('dashboard')

---

## 3. Data File Schemas (Backend Developer Focused)

### users.txt
- **File Path:** data/users.txt
- **Format:** Pipe-delimited (`|`)
  - username|email|phone|full_name
- **Data Description:** Stores registered user information.
- **Field Names & Descriptions:**
  - username: Unique user identifier
  - email: User's email address
  - phone: User's phone number
  - full_name: User's full name
- **Example Rows:**
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### menu.txt
- **File Path:** data/menu.txt
- **Format:** Pipe-delimited (`|`)
  - dish_id|name|category|price|description|ingredients|dietary|avg_rating
- **Data Description:** Stores restaurant menu items.
- **Field Names & Descriptions:**
  - dish_id: Unique dish identifier (int)
  - name: Name of the dish
  - category: Category of dish (Appetizers, Main Course, etc.)
  - price: Dish price (float)
  - description: Description of the dish
  - ingredients: Comma-separated ingredients list
  - dietary: Dietary attributes (e.g., Vegetarian, Gluten-Free)
  - avg_rating: Average user rating (float)
- **Example Rows:**
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### reservations.txt
- **File Path:** data/reservations.txt
- **Format:** Pipe-delimited (`|`)
  - reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
- **Data Description:** Stores reservation records.
- **Field Names & Descriptions:**
  - reservation_id: Unique reservation identifier (int)
  - username: User who made reservation
  - guest_name: Name of guest for reservation
  - phone: Contact phone
  - email: Contact email
  - party_size: Number of guests (int)
  - date: Reservation date (YYYY-MM-DD)
  - time: Reservation time (HH:MM)
  - special_requests: Optional special requests
  - status: Reservation status (Upcoming, Completed, Cancelled)
- **Example Rows:**
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### waitlist.txt
- **File Path:** data/waitlist.txt
- **Format:** Pipe-delimited (`|`)
  - waitlist_id|username|party_size|join_time|status
- **Data Description:** Stores waitlist entries.
- **Field Names & Descriptions:**
  - waitlist_id: Unique waitlist entry id (int)
  - username: User on waitlist
  - party_size: Number in party (int)
  - join_time: Timestamp when joined (YYYY-MM-DD HH:MM:SS)
  - status: Entry status (Active, Removed)
- **Example Rows:**
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### reviews.txt
- **File Path:** data/reviews.txt
- **Format:** Pipe-delimited (`|`)
  - review_id|username|dish_id|rating|review_text|review_date
- **Data Description:** Stores user reviews for dishes.
- **Field Names & Descriptions:**
  - review_id: Unique review id (int)
  - username: User who wrote review
  - dish_id: The dish being reviewed (int)
  - rating: Rating 1-5 (int)
  - review_text: Text of review
  - review_date: Date of review (YYYY-MM-DD)
- **Example Rows:**
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```
