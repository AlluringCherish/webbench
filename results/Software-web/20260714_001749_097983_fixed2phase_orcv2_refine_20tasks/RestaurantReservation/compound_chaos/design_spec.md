# RestaurantReservation Web Application Design Specification

---

## Page Layouts and Elements

### 1. Dashboard Page
- **Page Title**: Restaurant Dashboard
- **Element IDs:**
  - `dashboard-page` - Div - Container for the dashboard page.
  - `welcome-message` - H1 - Displays welcome message with username.
  - `make-reservation-button` - Button - Navigates to Make Reservation page.
  - `view-menu-button` - Button - Navigates to Menu page.
  - `back-to-dashboard` - Button - Refreshes or navigates to Dashboard page.
  - `my-reservations-button` - Button - Navigates to My Reservations page.
  - `my-reviews-button` - Button - Navigates to My Reviews page.
  - `waitlist-button` - Button - Navigates to Waitlist page.
  - `profile-button` - Button - Navigates to User Profile page.

### 2. Menu Page
- **Page Title**: Restaurant Menu
- **Element IDs:**
  - `menu-page` - Div - Container for the menu page.
  - `menu-grid` - Div - Grid displaying dish cards with image, name, price, and description.
  - `view-dish-button-{dish_id}` - Button - On each dish card; navigates to Dish Details page for that dish.
  - `back-to-dashboard` - Button - Navigates back to Dashboard page.

### 3. Dish Details Page
- **Page Title**: Dish Details
- **Element IDs:**
  - `dish-details-page` - Div - Container for the dish details page.
  - `dish-name` - H1 - Displays dish name.
  - `dish-price` - Div - Displays dish price.
  - `back-to-menu` - Button - Navigates back to Menu page.

### 4. Make Reservation Page
- **Page Title**: Make Reservation
- **Element IDs:**
  - `reservation-page` - Div - Container for the reservation page.
  - `guest-name` - Input - Field for guest name.
  - `party-size` - Dropdown - Select party size (1-10).
  - `reservation-date` - Input (date) - Select reservation date.
  - `submit-reservation-button` - Button - Submit reservation.
  - `back-to-dashboard` - Button - Navigate back to Dashboard.

### 5. My Reservations Page
- **Page Title**: My Reservations
- **Element IDs:**
  - `my-reservations-page` - Div - Container for the reservations page.
  - `reservations-table` - Table - Displays reservations with date, time, party size, status.
  - `cancel-reservation-button-{reservation_id}` - Button - Cancel a specific reservation.
  - `back-to-dashboard` - Button - Navigate back to Dashboard.

### 6. Waitlist Page
- **Page Title**: Waitlist
- **Element IDs:**
  - `waitlist-page` - Div - Container for the waitlist page.
  - `waitlist-party-size` - Dropdown - Select party size.
  - `join-waitlist-button` - Button - Join the waitlist.
  - `user-position` - Div - Displays user's current position on waitlist.
  - `back-to-dashboard` - Button - Navigate back to Dashboard.

### 7. My Reviews Page
- **Page Title**: My Reviews
- **Element IDs:**
  - `reviews-page` - Div - Container for the reviews page.
  - `reviews-list` - Div - Lists reviews with dish name, rating, and text.
  - `write-new-review-button` - Button - Navigate to Write Review page.
  - `back-to-dashboard` - Button - Navigate back to Dashboard.

### 8. Write Review Page
- **Page Title**: Write Review
- **Element IDs:**
  - `write-review-page` - Div - Container for write review page.
  - `select-dish` - Dropdown - Select dish to review.
  - `rating-input` - Dropdown - Select rating 1-5 stars.
  - `review-text` - Textarea - Input for review text.
  - `submit-review-button` - Button - Submit review.
  - `back-to-reviews` - Button - Navigate back to My Reviews page.

### 9. User Profile Page
- **Page Title**: My Profile
- **Element IDs:**
  - `profile-page` - Div - Container for profile page.
  - `profile-username` - Div - Display username (non-editable).
  - `profile-email` - Input - Update email.
  - `update-profile-button` - Button - Save profile changes.
  - `back-to-dashboard` - Button - Navigate back to Dashboard.

---

## Navigation Flow

- From Dashboard:
  - `make-reservation-button` -> Make Reservation page
  - `view-menu-button` -> Menu page
  - `my-reservations-button` -> My Reservations page
  - `my-reviews-button` -> My Reviews page
  - `waitlist-button` -> Waitlist page
  - `profile-button` -> User Profile page
  - `back-to-dashboard` refreshes Dashboard

- From Menu page:
  - `view-dish-button-{dish_id}` -> Dish Details page for selected dish
  - `back-to-dashboard` -> Dashboard page

- From Dish Details page:
  - `back-to-menu` -> Menu page

- From Make Reservation page:
  - `submit-reservation-button` -> Submit reservation and return to Dashboard
  - `back-to-dashboard` -> Dashboard page

- From My Reservations page:
  - `cancel-reservation-button-{reservation_id}` -> Cancel reservation (remains on page or refresh)
  - `back-to-dashboard` -> Dashboard page

- From Waitlist page:
  - `join-waitlist-button` -> Join waitlist (user stays on page to see position)
  - `back-to-dashboard` -> Dashboard page

- From My Reviews page:
  - `write-new-review-button` -> Write Review page
  - `back-to-dashboard` -> Dashboard page

- From Write Review page:
  - `submit-review-button` -> Submit review and return to My Reviews page
  - `back-to-reviews` -> My Reviews page

- From User Profile page:
  - `update-profile-button` -> Save changes (stay or return to Dashboard)
  - `back-to-dashboard` -> Dashboard page

---

## Data File Schemas

All data files are stored in the `data/` directory with pipe (`|`) delimited fields. Each line represents one record.

### 1. users.txt
- Fields: `username|email|phone|full_name`
- Types:
  - username: string
  - email: string
  - phone: string
  - full_name: string
- Example:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### 2. menu.txt
- Fields: `dish_id|name|category|price|description|ingredients|dietary|avg_rating`
- Types:
  - dish_id: integer
  - name: string
  - category: string
  - price: float
  - description: string
  - ingredients: string (comma-separated list)
  - dietary: string
  - avg_rating: float
- Example:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### 3. reservations.txt
- Fields: `reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status`
- Types:
  - reservation_id: integer
  - username: string
  - guest_name: string
  - phone: string
  - email: string
  - party_size: integer
  - date: date (YYYY-MM-DD)
  - time: time (HH:MM)
  - special_requests: string
  - status: string (e.g., Upcoming, Completed)
- Example:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### 4. waitlist.txt
- Fields: `waitlist_id|username|party_size|join_time|status`
- Types:
  - waitlist_id: integer
  - username: string
  - party_size: integer
  - join_time: datetime (YYYY-MM-DD HH:MM:SS)
  - status: string (e.g., Active)
- Example:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### 5. reviews.txt
- Fields: `review_id|username|dish_id|rating|review_text|review_date`
- Types:
  - review_id: integer
  - username: string
  - dish_id: integer
  - rating: integer (1-5)
  - review_text: string
  - review_date: date (YYYY-MM-DD)
- Example:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

---

This completes the design specification for the RestaurantReservation web application, covering page layouts, element IDs, navigation, and local data file schemas.