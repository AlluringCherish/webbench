# RestaurantReservation Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developers)

| URL Path                      | Function Name           | HTTP Methods | Template Filename        | Context Variables                                                                                                                 | Request Form Fields (POST)                                      |
|-------------------------------|------------------------|--------------|--------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| /                             | root_redirect           | GET          | N/A                      | N/A                                                                                                                              | N/A                                                            |
| /dashboard                    | dashboard              | GET          | dashboard.html           | username: str
featured_dishes: list of dict {dish_id: int, name: str, price: float, description: str}
upcoming_reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str} | N/A                                                            |
| /menu                        | menu                   | GET          | menu.html                | menus: list of dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float} | N/A                                                            |
| /dish/<int:dish_id>          | dish_details           | GET          | dish_details.html        | dish: dict {dish_id: int, name: str, price: float, description: str}                                                             | N/A                                                            |
| /make-reservation            | make_reservation       | GET, POST    | make_reservation.html    | N/A (GET)
On POST: redirect after processing or error feedback                                                                        | guest_name: str
party_size: int (1-10)
reservation_date: str (YYYY-MM-DD)                 |
| /my-reservations             | my_reservations        | GET          | my_reservations.html     | reservations: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}                                | N/A                                                            |
| /cancel-reservation/<int:reservation_id> | cancel_reservation    | POST         | N/A                      | N/A                                                                                                                              | N/A (reservation_id passed as URL parameter)                   |
| /waitlist                   | waitlist               | GET, POST    | waitlist.html            | user_position: int or None (GET)                                                                                                 | party_size: int                                               |
| /my-reviews                 | my_reviews             | GET          | my_reviews.html          | reviews: list of dict {review_id: int, dish_name: str, rating: int, review_text: str}                                              | N/A                                                            |
| /write-review               | write_review           | GET, POST    | write_review.html        | dishes: list of dict {dish_id: int, name: str} (GET)                                                                              | dish_id: int
rating: int (1-5)
review_text: str                                         |
| /profile                   | profile                | GET, POST    | profile.html             | username: str
email: str
optional success_message: str or error_message: str (for GET)                                          | email: str                                                    |

**Notes:**
- The root route `/` must redirect to `/dashboard`.
- All dynamic route parameters should be clearly typed as shown.
- POST routes handle form submissions with appropriate validation.

---

## Section 2: HTML Template Specifications (For Frontend Developers)

---

### templates/dashboard.html
- **Page Title:** Restaurant Dashboard
- **Element IDs with Types:**
  - `dashboard-page`: Div (container for the dashboard page)
  - `welcome-message`: H1 (welcome message showing username)
  - `make-reservation-button`: Button (navigates to Make Reservation page)
  - `view-menu-button`: Button (navigates to Menu page)
  - `back-to-dashboard`: Button (refreshes the dashboard)
  - `my-reservations-button`: Button (navigates to My Reservations page)
  - `my-reviews-button`: Button (navigates to My Reviews page)
  - `waitlist-button`: Button (navigates to Waitlist page)
  - `profile-button`: Button (navigates to User Profile page)
- **Context Variables:**
  - `username`: str
  - `featured_dishes`: list of dict {dish_id: int, name: str, price: float, description: str}
  - `upcoming_reservations`: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
- **Navigation Mappings:**
  - `make-reservation-button` → Flask route function `make_reservation`
  - `view-menu-button` → Flask route function `menu`
  - `back-to-dashboard` → Flask route function `dashboard`
  - `my-reservations-button` → Flask route function `my_reservations`
  - `my-reviews-button` → Flask route function `my_reviews`
  - `waitlist-button` → Flask route function `waitlist`
  - `profile-button` → Flask route function `profile`

---

### templates/menu.html
- **Page Title:** Restaurant Menu
- **Element IDs with Types:**
  - `menu-page`: Div (container for the menu page)
  - `menu-grid`: Div (grid displaying dish cards)
  - Dynamic buttons for each dish:
    - `view-dish-button-{{ dish.dish_id }}`: Button (view dish details)
  - `back-to-dashboard`: Button (navigate back to dashboard)
- **Context Variables:**
  - `menus`: list of dict {dish_id: int, name: str, category: str, price: float, description: str, ingredients: str, dietary: str, avg_rating: float}
- **Navigation Mappings:**
  - `view-dish-button-{{ dish.dish_id }}` → Flask route function `dish_details` with `dish_id`
  - `back-to-dashboard` → Flask route function `dashboard`
- **Dynamic Element ID Construction:**
  - Button IDs are constructed using Jinja2 syntax:
    ```jinja
    id="view-dish-button-{{ dish.dish_id }}"
    ```
- **Jinja2 Template Example:**
  ```jinja
  {% for dish in menus %}
    <div class="dish-card">
      <h2>{{ dish.name }}</h2>
      <p>{{ dish.description }}</p>
      <p>Price: ${{ dish.price }}</p>
      <button id="view-dish-button-{{ dish.dish_id }}" onclick="location.href='{{ url_for('dish_details', dish_id=dish.dish_id) }}'">View Details</button>
    </div>
  {% endfor %}
  ```

---

### templates/dish_details.html
- **Page Title:** Dish Details
- **Element IDs with Types:**
  - `dish-details-page`: Div (container for dish details page)
  - `dish-name`: H1 (shows dish name)
  - `dish-price`: Div (displays dish price)
  - `back-to-menu`: Button (go back to menu page)
- **Context Variables:**
  - `dish`: dict {dish_id: int, name: str, price: float, description: str}
- **Navigation Mappings:**
  - `back-to-menu` → Flask route function `menu`

---

### templates/make_reservation.html
- **Page Title:** Make Reservation
- **Element IDs with Types:**
  - `reservation-page`: Div (container for reservation page)
  - `guest-name`: Input (text)
  - `party-size`: Dropdown/select (values 1-10)
  - `reservation-date`: Input (date)
  - `submit-reservation-button`: Button (submit reservation form)
  - `back-to-dashboard`: Button (go back to dashboard)
- **Context Variables:**
  - No special variables required
- **Forms:**
  - Form method: POST
  - Form action: `/make-reservation`
  - Expected form fields:
    - `guest_name` (text)
    - `party_size` (int)
    - `reservation_date` (date string, YYYY-MM-DD)
- **Navigation Mappings:**
  - `back-to-dashboard` → Flask route function `dashboard`

---

### templates/my_reservations.html
- **Page Title:** My Reservations
- **Element IDs with Types:**
  - `my-reservations-page`: Div (container)
  - `reservations-table`: Table (shows reservations)
  - Dynamic cancel buttons:
    - `cancel-reservation-button-{{ reservation.reservation_id }}`: Button (cancel reservation)
  - `back-to-dashboard`: Button (go back to dashboard)
- **Context Variables:**
  - `reservations`: list of dict {reservation_id: int, date: str, time: str, party_size: int, status: str}
- **Form Actions:**
  - POST requests to `/cancel-reservation/<reservation_id>` when cancel button clicked
- **Navigation Mappings:**
  - `back-to-dashboard` → Flask route function `dashboard`

---

### templates/waitlist.html
- **Page Title:** Waitlist
- **Element IDs with Types:**
  - `waitlist-page`: Div (container)
  - `waitlist-party-size`: Dropdown/select
  - `join-waitlist-button`: Button
  - `user-position`: Div (shows user's position or status)
  - `back-to-dashboard`: Button (go back to dashboard)
- **Context Variables:**
  - `user_position`: int or None
- **Forms:**
  - Form method: POST
  - Form action: `/waitlist`
  - Field: `party_size` (int)
- **Navigation Mappings:**
  - `back-to-dashboard` → Flask route function `dashboard`

---

### templates/my_reviews.html
- **Page Title:** My Reviews
- **Element IDs with Types:**
  - `reviews-page`: Div (container)
  - `reviews-list`: Div (list of reviews)
  - `write-new-review-button`: Button (to write review page)
  - `back-to-dashboard`: Button (go back to dashboard)
- **Context Variables:**
  - `reviews`: list of dict {review_id: int, dish_name: str, rating: int, review_text: str}
- **Navigation Mappings:**
  - `write-new-review-button` → Flask route function `write_review`
  - `back-to-dashboard` → Flask route function `dashboard`

---

### templates/write_review.html
- **Page Title:** Write Review
- **Element IDs with Types:**
  - `write-review-page`: Div (container)
  - `select-dish`: Dropdown/select (dish options)
  - `rating-input`: Dropdown/select (1-5 star rating)
  - `review-text`: Textarea
  - `submit-review-button`: Button (submit form)
  - `back-to-reviews`: Button (go back to my reviews)
- **Context Variables:**
  - `dishes`: list of dict {dish_id: int, name: str}
- **Forms:**
  - Form method: POST
  - Form action: `/write-review`
  - Expected form fields:
    - `dish_id` (int)
    - `rating` (int, 1-5)
    - `review_text` (str)
- **Navigation Mappings:**
  - `back-to-reviews` → Flask route function `my_reviews`

---

### templates/profile.html
- **Page Title:** My Profile
- **Element IDs with Types:**
  - `profile-page`: Div (container)
  - `profile-username`: Div (display username)
  - `profile-email`: Input (text)
  - `update-profile-button`: Button (submit profile changes)
  - `back-to-dashboard`: Button (navigate back to dashboard)
- **Context Variables:**
  - `username`: str
  - `email`: str
  - Optional: `success_message` (str), `error_message` (str)
- **Forms:**
  - Form method: POST
  - Form action: `/profile`
  - Expected form field:
    - `email` (str)
- **Navigation Mappings:**
  - `back-to-dashboard` → Flask route function `dashboard`

---

## Section 3: Data File Schemas (For Backend Developers)

### 1. data/users.txt
- **File Path:** data/users.txt
- **Format:** Pipe-delimited
- **Description:** Stores registered user information.
- **Fields:**
  1. username (str) - Unique user identifier.
  2. email (str) - User's email address.
  3. phone (str) - User's phone number.
  4. full_name (str) - User's full name.
- **Example Rows:**
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

---

### 2. data/menu.txt
- **File Path:** data/menu.txt
- **Format:** Pipe-delimited
- **Description:** Stores details of menu items.
- **Fields:**
  1. dish_id (int) - Unique dish identifier.
  2. name (str) - Name of the dish.
  3. category (str) - Menu category (e.g., Appetizers, Main Course).
  4. price (float) - Price of the dish.
  5. description (str) - Description of the dish.
  6. ingredients (str) - Comma-separated list of ingredients.
  7. dietary (str) - Dietary information (e.g., Vegetarian, Vegan).
  8. avg_rating (float) - Average user rating.
- **Example Rows:**
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

---

### 3. data/reservations.txt
- **File Path:** data/reservations.txt
- **Format:** Pipe-delimited
- **Description:** Stores reservations made by users.
- **Fields:**
  1. reservation_id (int) - Unique reservation identifier.
  2. username (str) - User who made the reservation.
  3. guest_name (str) - Name of the guest for the reservation.
  4. phone (str) - Contact phone number.
  5. email (str) - Contact email.
  6. party_size (int) - Number of people in the party.
  7. date (str) - Reservation date (YYYY-MM-DD).
  8. time (str) - Reservation time (HH:MM).
  9. special_requests (str) - Any special requests (optional).
  10. status (str) - Reservation status (Upcoming, Completed, Cancelled).
- **Example Rows:**
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

---

### 4. data/waitlist.txt
- **File Path:** data/waitlist.txt
- **Format:** Pipe-delimited
- **Description:** Tracks users currently in the waitlist.
- **Fields:**
  1. waitlist_id (int) - Unique waitlist entry identifier.
  2. username (str) - User in the waitlist.
  3. party_size (int) - Number in party.
  4. join_time (str) - Timestamp user joined (YYYY-MM-DD HH:MM:SS).
  5. status (str) - Current status (Active, Removed).
- **Example Rows:**
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

---

### 5. data/reviews.txt
- **File Path:** data/reviews.txt
- **Format:** Pipe-delimited
- **Description:** Stores user reviews for dishes.
- **Fields:**
  1. review_id (int) - Unique review identifier.
  2. username (str) - User who wrote the review.
  3. dish_id (int) - Dish reviewed.
  4. rating (int) - Rating given (1-5).
  5. review_text (str) - Review content.
  6. review_date (str) - Date of review (YYYY-MM-DD).
- **Example Rows:**
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

---

# End of Specification
