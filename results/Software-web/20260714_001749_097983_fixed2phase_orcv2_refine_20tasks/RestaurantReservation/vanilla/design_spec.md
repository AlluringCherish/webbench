# Design Specification Document for RestaurantReservation Web Application

---

## Section 1: Page Layout and Element IDs

### 1. Dashboard Page
- Page Title: Restaurant Dashboard
- Elements:
  - ID: dashboard-page - Div - Container for the dashboard page.
  - ID: welcome-message - H1 - Displays welcome message with username.
  - ID: make-reservation-button - Button - Navigates to Make Reservation page.
  - ID: view-menu-button - Button - Navigates to Menu page.
  - ID: back-to-dashboard - Button - Refreshes or reloads the Dashboard.
  - ID: my-reservations-button - Button - Navigates to My Reservations page.
  - ID: my-reviews-button - Button - Navigates to My Reviews page.
  - ID: waitlist-button - Button - Navigates to Waitlist page.
  - ID: profile-button - Button - Navigates to User Profile page.

### 2. Menu Page
- Page Title: Restaurant Menu
- Elements:
  - ID: menu-page - Div - Container for the menu page.
  - ID: menu-grid - Div - Displays dish cards (image, name, price, description).
  - ID: view-dish-button-{dish_id} - Button - Each button to view details of a specific dish.
  - ID: back-to-dashboard - Button - Navigates back to Dashboard.

### 3. Dish Details Page
- Page Title: Dish Details
- Elements:
  - ID: dish-details-page - Div - Container for dish details.
  - ID: dish-name - H1 - Displays dish name.
  - ID: dish-price - Div - Displays dish price.
  - ID: back-to-menu - Button - Navigates back to Menu page.

### 4. Make Reservation Page
- Page Title: Make Reservation
- Elements:
  - ID: reservation-page - Div - Container for the reservation page.
  - ID: guest-name - Input - Input field for guest name.
  - ID: party-size - Dropdown - Select party size (1-10).
  - ID: reservation-date - Input (date) - Select reservation date.
  - ID: submit-reservation-button - Button - Submits the reservation.
  - ID: back-to-dashboard - Button - Navigates back to Dashboard.

### 5. My Reservations Page
- Page Title: My Reservations
- Elements:
  - ID: my-reservations-page - Div - Container for reservations list.
  - ID: reservations-table - Table - Displays reservations with columns: date, time, party size, status.
  - ID: cancel-reservation-button-{reservation_id} - Button - Cancels a specific upcoming reservation.
  - ID: back-to-dashboard - Button - Navigates back to Dashboard.

### 6. Waitlist Page
- Page Title: Waitlist
- Elements:
  - ID: waitlist-page - Div - Container for the waitlist page.
  - ID: waitlist-party-size - Dropdown - Select party size for waitlist.
  - ID: join-waitlist-button - Button - Joins the waitlist.
  - ID: user-position - Div - Displays user's current position in waitlist.
  - ID: back-to-dashboard - Button - Navigates back to Dashboard.

### 7. My Reviews Page
- Page Title: My Reviews
- Elements:
  - ID: reviews-page - Div - Container for the reviews.
  - ID: reviews-list - Div - List of user's reviews showing dish name, rating, and review text.
  - ID: write-new-review-button - Button - Navigates to Write Review page.
  - ID: back-to-dashboard - Button - Navigates back to Dashboard.

### 8. Write Review Page
- Page Title: Write Review
- Elements:
  - ID: write-review-page - Div - Container for review writing.
  - ID: select-dish - Dropdown - Select dish to review.
  - ID: rating-input - Dropdown - Select rating from 1 to 5 stars.
  - ID: review-text - Textarea - Enter review text.
  - ID: submit-review-button - Button - Submit the review.
  - ID: back-to-reviews - Button - Navigate back to My Reviews page.

### 9. User Profile Page
- Page Title: My Profile
- Elements:
  - ID: profile-page - Div - Container for user profile.
  - ID: profile-username - Div - Displays username (non-editable).
  - ID: profile-email - Input - Update user email.
  - ID: update-profile-button - Button - Save profile changes.
  - ID: back-to-dashboard - Button - Navigate back to Dashboard.

---

## Section 2: Navigation Flow

- From Dashboard (Restaurant Dashboard):
  - make-reservation-button -> Make Reservation Page
  - view-menu-button -> Menu Page
  - my-reservations-button -> My Reservations Page
  - my-reviews-button -> My Reviews Page
  - waitlist-button -> Waitlist Page
  - profile-button -> User Profile Page
  - back-to-dashboard refreshes current Dashboard page

- From Menu Page:
  - view-dish-button-{dish_id} -> Dish Details Page for selected dish
  - back-to-dashboard -> Dashboard Page

- From Dish Details Page:
  - back-to-menu -> Menu Page

- From Make Reservation Page:
  - submit-reservation-button -> Processes reservation submission and navigates back to Dashboard
  - back-to-dashboard -> Dashboard Page

- From My Reservations Page:
  - cancel-reservation-button-{reservation_id} -> Cancels specified reservation and refreshes My Reservations
  - back-to-dashboard -> Dashboard Page

- From Waitlist Page:
  - join-waitlist-button -> Adds user to waitlist and updates user-position
  - back-to-dashboard -> Dashboard Page

- From My Reviews Page:
  - write-new-review-button -> Write Review Page
  - back-to-dashboard -> Dashboard Page

- From Write Review Page:
  - submit-review-button -> Submits review and navigates back to My Reviews
  - back-to-reviews -> My Reviews Page

- From User Profile Page:
  - update-profile-button -> Saves changes and remains/returns to Profile Page
  - back-to-dashboard -> Dashboard Page

---

## Section 3: Data File Schema Specification

### 1. User Data
- Filename: data/users.txt
- Fields: username|email|phone|full_name
- Field Types: string|string|string|string
- Example:
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie

### 2. Menu Items Data
- Filename: data/menu.txt
- Fields: dish_id|name|category|price|description|ingredients|dietary|avg_rating
- Field Types: int|string|string|float|string|string|string|float
- Example:
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6

### 3. Reservations Data
- Filename: data/reservations.txt
- Fields: reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
- Field Types: int|string|string|string|string|int|string|string|string|string
- Example:
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming

### 4. Waitlist Data
- Filename: data/waitlist.txt
- Fields: waitlist_id|username|party_size|join_time|status
- Field Types: int|string|int|string|string
- Example:
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active

### 5. Reviews Data
- Filename: data/reviews.txt
- Fields: review_id|username|dish_id|rating|review_text|review_date
- Field Types: int|string|int|int|string|string
- Example:
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19

---

End of design_spec.md
