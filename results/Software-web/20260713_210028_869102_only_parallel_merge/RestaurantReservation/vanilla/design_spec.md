# Merged Design Specification for RestaurantReservation Web Application

---

## Routes and Templates

| Page               | Route Path                 | Template Filename       |
|--------------------|----------------------------|-------------------------|
| Dashboard          | `/`                        | dashboard.html          |
| Menu               | `/menu`                    | menu.html               |
| Dish Details       | `/dish/<int:dish_id>`      | dish_details.html       |
| Make Reservation   | `/make-reservation`        | make_reservation.html   |
| My Reservations    | `/my-reservations`         | my_reservations.html    |
| Waitlist           | `/waitlist`                | waitlist.html           |
| My Reviews         | `/my-reviews`              | my_reviews.html         |
| Write Review       | `/write-review`            | write_review.html       |
| User Profile       | `/profile`                 | profile.html            |

---

## Page Titles and Elements

### 1. Dashboard Page
- **Page Title:** Restaurant Dashboard
- **Route:** `/`
- **Template:** `dashboard.html`
- **Container Element:** Div with ID `dashboard-page`
- **Elements:**
  - H1 with ID `welcome-message` (Displays username welcome)
  - Button with ID `make-reservation-button` (Navigate to `/make-reservation`)
  - Button with ID `view-menu-button` (Navigate to `/menu`)
  - Button with ID `back-to-dashboard` (Refresh current `/` route)
  - Button with ID `my-reservations-button` (Navigate to `/my-reservations`)
  - Button with ID `my-reviews-button` (Navigate to `/my-reviews`)
  - Button with ID `waitlist-button` (Navigate to `/waitlist`)
  - Button with ID `profile-button` (Navigate to `/profile`)

### 2. Menu Page
- **Page Title:** Restaurant Menu
- **Route:** `/menu`
- **Template:** `menu.html`
- **Container Element:** Div with ID `menu-page`
- **Elements:**
  - Div with ID `menu-grid` (Grid containing dish cards with image, name, price, description)
  - Buttons per dish card: `view-dish-button-{dish_id}` (Navigate to `/dish/{dish_id}`)
  - Button with ID `back-to-dashboard` (Navigate to `/`)

### 3. Dish Details Page
- **Page Title:** Dish Details
- **Route:** `/dish/<int:dish_id>`
- **Template:** `dish_details.html`
- **Container Element:** Div with ID `dish-details-page`
- **Elements:**
  - H1 with ID `dish-name` (Display dish name)
  - Div with ID `dish-price` (Display dish price)
  - Button with ID `back-to-menu` (Navigate to `/menu`)

### 4. Make Reservation Page
- **Page Title:** Make Reservation
- **Route:** `/make-reservation`
- **Template:** `make_reservation.html`
- **Container Element:** Div with ID `reservation-page`
- **Elements:**
  - Input text with ID `guest-name` (Guest name input)
  - Dropdown select with ID `party-size` (Options 1-10)
  - Input date with ID `reservation-date` (Date picker)
  - Button with ID `submit-reservation-button` (Submit reservation)
  - Button with ID `back-to-dashboard` (Navigate to `/`)

### 5. My Reservations Page
- **Page Title:** My Reservations
- **Route:** `/my-reservations`
- **Template:** `my_reservations.html`
- **Container Element:** Div with ID `my-reservations-page`
- **Elements:**
  - Table with ID `reservations-table` (Columns for date, time, party size, status)
  - Buttons per upcoming reservation row: `cancel-reservation-button-{reservation_id}` (Trigger cancel action)
  - Button with ID `back-to-dashboard` (Navigate to `/`)

### 6. Waitlist Page
- **Page Title:** Waitlist
- **Route:** `/waitlist`
- **Template:** `waitlist.html`
- **Container Element:** Div with ID `waitlist-page`
- **Elements:**
  - Dropdown select with ID `waitlist-party-size` (Select party size)
  - Button with ID `join-waitlist-button` (Join waitlist)
  - Div with ID `user-position` (Show user's waitlist position)
  - Button with ID `back-to-dashboard` (Navigate to `/`)

### 7. My Reviews Page
- **Page Title:** My Reviews
- **Route:** `/my-reviews`
- **Template:** `my_reviews.html`
- **Container Element:** Div with ID `reviews-page`
- **Elements:**
  - Div with ID `reviews-list` (List of reviews: dish name, rating, review text)
  - Button with ID `write-new-review-button` (Navigate to `/write-review`)
  - Button with ID `back-to-dashboard` (Navigate to `/`)

### 8. Write Review Page
- **Page Title:** Write Review
- **Route:** `/write-review`
- **Template:** `write_review.html`
- **Container Element:** Div with ID `write-review-page`
- **Elements:**
  - Dropdown select with ID `select-dish` (Select dish to review)
  - Dropdown select with ID `rating-input` (Select rating 1-5 stars)
  - Textarea with ID `review-text` (Write review text)
  - Button with ID `submit-review-button` (Submit review)
  - Button with ID `back-to-reviews` (Navigate to `/my-reviews`)

### 9. User Profile Page
- **Page Title:** My Profile
- **Route:** `/profile`
- **Template:** `profile.html`
- **Container Element:** Div with ID `profile-page`
- **Elements:**
  - Div with ID `profile-username` (Show username, not editable)
  - Input text with ID `profile-email` (Update email)
  - Button with ID `update-profile-button` (Save changes)
  - Button with ID `back-to-dashboard` (Navigate to `/`)

---

## Navigation Flows

- Dashboard page (`/`) is the root and starting point.
- Buttons on dashboard navigate to respective pages using paths defined above.
- Menu page viewing dish details uses route `/dish/<dish_id>`.
- Back buttons navigate logically:
  - `back-to-menu` on Dish Details returns to `/menu`
  - `back-to-dashboard` on multiple pages returns to `/`
  - `back-to-reviews` on Write Review returns to `/my-reviews`
- Write review page accessible from My Reviews page via `write-new-review-button` and returns via `back-to-reviews`.

---

## Data Interfaces

- Dish Details and Menu pages utilize `dish_id` route parameter.
- My Reservations page's cancel buttons use `reservation_id` to identify which reservation to cancel.
- Waitlist page manages `party-size` input and shows user's `user-position`.
- Profile page displays username read-only and allows updating email through input.

---

This specification merges both design candidates maintaining the original user requirement fidelity and consistent naming conventions. Routing favors Candidate A's simpler base root path for Dashboard and the exact element IDs as required. Additions from Candidate B that are not explicitly required (e.g., reservation time, special requests, phone in profile, dish description) are omitted to preserve strict specification adherence. Paths are unified and consistent with the primary requirements.