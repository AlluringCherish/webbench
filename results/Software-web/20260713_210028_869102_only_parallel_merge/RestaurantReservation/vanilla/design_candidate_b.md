# Alternative Design Candidate B for RestaurantReservation Web Application

## 1. Flask Routes and Template Mappings

| Page               | Route Path                  | Template Filename        |
|--------------------|-----------------------------|-------------------------|
| Dashboard          | `/dashboard`                | dashboard.html          |
| Menu               | `/menu`                     | menu.html               |
| Dish Details       | `/menu/dish/<int:dish_id>`  | dish_details.html       |
| Make Reservation   | `/reservation/make`         | make_reservation.html   |
| My Reservations    | `/reservations`             | my_reservations.html    |
| Waitlist           | `/waitlist`                 | waitlist.html           |
| My Reviews         | `/reviews`                  | my_reviews.html         |
| Write Review       | `/reviews/write`            | write_review.html       |
| User Profile       | `/profile`                  | profile.html            |

## 2. Detailed Page Structures and Elements

### Dashboard Page
- **Title**: Restaurant Dashboard
- **Route**: `/dashboard`
- **Template**: dashboard.html
- **Container ID**: `dashboard-page` (Div)
- **Elements:**
  - `welcome-message` (H1): Displays welcome greeting with username.
  - `make-reservation-button` (Button): Navigates to `/reservation/make`
  - `view-menu-button` (Button): Navigates to `/menu`
  - `my-reservations-button` (Button): Navigates to `/reservations`
  - `my-reviews-button` (Button): Navigates to `/reviews`
  - `waitlist-button` (Button): Navigates to `/waitlist`
  - `profile-button` (Button): Navigates to `/profile`
  - `refresh-dashboard-button` (Button): Reloads `/dashboard`

### Menu Page
- **Title**: Restaurant Menu
- **Route**: `/menu`
- **Template**: menu.html
- **Container ID**: `menu-page` (Div)
- **Elements:**
  - `menu-grid` (Div): Grid container for dish cards.
  - For each dish card:
    - `view-dish-button-{dish_id}` (Button): Navigates to dish details page `/menu/dish/<dish_id>`
  - `back-to-dashboard` (Button): Navigates back to `/dashboard`

### Dish Details Page
- **Title**: Dish Details
- **Route**: `/menu/dish/<int:dish_id>`
- **Template**: dish_details.html
- **Container ID**: `dish-details-page` (Div)
- **Elements:**
  - `dish-name` (H1): Dish name display
  - `dish-price` (Div): Dish price display
  - `dish-description` (Div): Dish description (extra for UI enhancement)
  - `back-to-menu` (Button): Navigates back to `/menu`

### Make Reservation Page
- **Title**: Make Reservation
- **Route**: `/reservation/make`
- **Template**: make_reservation.html
- **Container ID**: `reservation-page` (Div)
- **Elements:**
  - `guest-name` (Input): Text input for guest name
  - `party-size` (Dropdown): Party size select (1-10)
  - `reservation-date` (Input[type=date]): Reservation date
  - `reservation-time` (Input[type=time]): Reservation time (added for completeness)
  - `special-requests` (Textarea): Optional special requests
  - `submit-reservation-button` (Button): Submit reservation
  - `back-to-dashboard` (Button): Navigate to `/dashboard`

### My Reservations Page
- **Title**: My Reservations
- **Route**: `/reservations`
- **Template**: my_reservations.html
- **Container ID**: `my-reservations-page` (Div)
- **Elements:**
  - `reservations-table` (Table): Displays all user's reservations with columns for date, time, party size, and status
  - Each upcoming reservation row has:
    - `cancel-reservation-button-{reservation_id}` (Button): Cancels reservation
  - `back-to-dashboard` (Button): Navigate to `/dashboard`

### Waitlist Page
- **Title**: Waitlist
- **Route**: `/waitlist`
- **Template**: waitlist.html
- **Container ID**: `waitlist-page` (Div)
- **Elements:**
  - `waitlist-party-size` (Dropdown): Party size select
  - `join-waitlist-button` (Button): Join waitlist
  - `user-position` (Div): Displays current position in waitlist
  - `back-to-dashboard` (Button): Navigate to `/dashboard`

### My Reviews Page
- **Title**: My Reviews
- **Route**: `/reviews`
- **Template**: my_reviews.html
- **Container ID**: `reviews-page` (Div)
- **Elements:**
  - `reviews-list` (Div): List of user's reviews (dish name, rating, review text)
  - `write-new-review-button` (Button): Navigate to `/reviews/write`
  - `back-to-dashboard` (Button): Navigate to `/dashboard`

### Write Review Page
- **Title**: Write Review
- **Route**: `/reviews/write`
- **Template**: write_review.html
- **Container ID**: `write-review-page` (Div)
- **Elements:**
  - `select-dish` (Dropdown): Select dish to review
  - `rating-input` (Dropdown): Rating select (1-5 stars)
  - `review-text` (Textarea): Review text
  - `submit-review-button` (Button): Submit review
  - `back-to-reviews` (Button): Navigate to `/reviews`

### User Profile Page
- **Title**: My Profile
- **Route**: `/profile`
- **Template**: profile.html
- **Container ID**: `profile-page` (Div)
- **Elements:**
  - `profile-username` (Div): Display username (read-only)
  - `profile-email` (Input): Editable email field
  - `profile-phone` (Input): Editable phone number (added for completeness)
  - `update-profile-button` (Button): Save profile changes
  - `back-to-dashboard` (Button): Navigate to `/dashboard`

---

This design candidate maintains all required element IDs and page titles exactly as specified in the requirements but offers alternative route paths and some added UI element enhancements for usability (e.g., added reservation time and special requests input, profile phone number input, dish description in details).

Each page includes explicit navigation buttons with clear target links, and dynamic buttons include the required placeholders `{dish_id}` and `{reservation_id}` where relevant.

The routes start from `/dashboard` serving the Dashboard page as root, faithfully fulfilling the critical requirement.