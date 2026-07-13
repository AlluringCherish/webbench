# Flask Web Application Architecture for RestaurantReservation

---

## 1. Flask Routes

| Route Path                   | Function Name              | HTTP Methods | Template File                     | Context Variables                        |
|------------------------------|----------------------------|--------------|---------------------------------|-----------------------------------------|
| /                            | dashboard                  | GET          | templates/dashboard.html         | username                               |
| /dashboard                   | dashboard                  | GET          | templates/dashboard.html         | username                               |
| /menu                       | menu_page                  | GET          | templates/menu.html              | menu_items (list of dishes)            |
| /dish/<int:dish_id>          | dish_details               | GET          | templates/dish_details.html      | dish (selected dish details)           |
| /reservation                | make_reservation           | GET          | templates/make_reservation.html | None                                   |
| /reservation                | submit_reservation         | POST         | None                            | Processes form; redirect on success    |
| /my-reservations            | my_reservations            | GET          | templates/my_reservations.html  | reservations (user's reservations)    |
| /cancel-reservation/<int:reservation_id> | cancel_reservation           | POST         | None                            | Cancel reservation; redirect back      |
| /waitlist                   | waitlist_page              | GET          | templates/waitlist.html         | waitlist_position                      |
| /waitlist                   | join_waitlist              | POST         | None                            | Join waitlist action; redirect back    |
| /my-reviews                 | my_reviews                 | GET          | templates/my_reviews.html       | reviews (user's reviews)               |
| /write-review               | write_review               | GET          | templates/write_review.html     | dishes (list for select-dish dropdown) |
| /write-review               | submit_review              | POST         | None                            | Submit review; then redirect back       |
| /profile                   | user_profile               | GET          | templates/user_profile.html     | user_profile                          |
| /update-profile            | update_profile             | POST         | None                            | Update profile; then redirect back     |


---

## 2. Templates

### 2.1 `templates/dashboard.html`
- Page Title: `Restaurant Dashboard`
- Main Container ID: `dashboard-page`
- Elements:
  - `welcome-message` (H1): Welcome message with username.
  - `make-reservation-button` (Button): Navigate to `/reservation`.
  - `view-menu-button` (Button): Navigate to `/menu`.
  - `back-to-dashboard` (Button): Reload `/dashboard`.
  - `my-reservations-button` (Button): Navigate to `/my-reservations`.
  - `my-reviews-button` (Button): Navigate to `/my-reviews`.
  - `waitlist-button` (Button): Navigate to `/waitlist`.
  - `profile-button` (Button): Navigate to `/profile`.

### 2.2 `templates/menu.html`
- Page Title: `Restaurant Menu`
- Main Container ID: `menu-page`
- Elements:
  - `menu-grid` (Div): Contains dish cards.
  - Buttons per dish: `view-dish-button-{dish_id}` (Button): Navigate to `/dish/<dish_id>`.
  - `back-to-dashboard` (Button): Navigate to `/dashboard`.

### 2.3 `templates/dish_details.html`
- Page Title: `Dish Details`
- Main Container ID: `dish-details-page`
- Elements:
  - `dish-name` (H1): Dish name.
  - `dish-price` (Div): Dish price.
  - `back-to-menu` (Button): Navigate to `/menu`.

### 2.4 `templates/make_reservation.html`
- Page Title: `Make Reservation`
- Main Container ID: `reservation-page`
- Form Elements:
  - Input `guest-name`: name="guest_name", type="text"
  - Dropdown `party-size`: name="party_size", options 1 to 10
  - Input `reservation-date`: name="reservation_date", type="date"
- Buttons:
  - `submit-reservation-button` (Button): Submits form to `/reservation` POST
  - `back-to-dashboard` (Button): Navigate to `/dashboard`

### 2.5 `templates/my_reservations.html`
- Page Title: `My Reservations`
- Main Container ID: `my-reservations-page`
- Elements:
  - `reservations-table` (Table): Displays user reservations with columns: Date, Time, Party Size, Status, Cancel Button.
  - Cancel buttons: `cancel-reservation-button-{reservation_id}` (Button): POST to `/cancel-reservation/<reservation_id>`
  - `back-to-dashboard` (Button): Navigate to `/dashboard`

### 2.6 `templates/waitlist.html`
- Page Title: `Waitlist`
- Main Container ID: `waitlist-page`
- Form Elements:
  - Dropdown `waitlist-party-size`: name="party_size", options (e.g., 1-10)
- Buttons:
  - `join-waitlist-button` (Button): Submits form to `/waitlist` POST
  - `back-to-dashboard` (Button): Navigate to `/dashboard`
- Display:
  - `user-position` (Div): Show user's waitlist position dynamically.

### 2.7 `templates/my_reviews.html`
- Page Title: `My Reviews`
- Main Container ID: `reviews-page`
- Elements:
  - `reviews-list` (Div): Lists user's reviews showing dish name, rating, review text.
  - `write-new-review-button` (Button): Navigate to `/write-review`
  - `back-to-dashboard` (Button): Navigate to `/dashboard`

### 2.8 `templates/write_review.html`
- Page Title: `Write Review`
- Main Container ID: `write-review-page`
- Form Elements:
  - Dropdown `select-dish`: name="dish_id", options populated from menu data.
  - Dropdown `rating-input`: name="rating", options 1 to 5
  - Textarea `review-text`: name="review_text"
- Buttons:
  - `submit-review-button` (Button): Posts form to `/write-review` POST
  - `back-to-reviews` (Button): Navigate to `/my-reviews`

### 2.9 `templates/user_profile.html`
- Page Title: `My Profile`
- Main Container ID: `profile-page`
- Elements:
  - `profile-username` (Div): Display username (read-only)
  - Input `profile-email`: name="email", type="email"
- Buttons:
  - `update-profile-button` (Button): Posts form to `/update-profile` POST
  - `back-to-dashboard` (Button): Navigate to `/dashboard`

---

## 3. Forms

### 3.1 Make Reservation Form
- Inputs: `guest_name` (text), `party_size` (dropdown 1-10), `reservation_date` (date)
- Submit Button: `submit-reservation-button` submits POST to `/reservation`

### 3.2 Cancel Reservation Form
- Submit Button: `cancel-reservation-button-{reservation_id}` submits POST to `/cancel-reservation/<reservation_id>`

### 3.3 Join Waitlist Form
- Input: `party_size` (dropdown 1-10)
- Submit Button: `join-waitlist-button` submits POST to `/waitlist`

### 3.4 Write Review Form
- Inputs: `dish_id` (dropdown), `rating` (dropdown 1-5), `review_text` (textarea)
- Submit Button: `submit-review-button` submits POST to `/write-review`

### 3.5 Update Profile Form
- Input: `email` (email text field)
- Submit Button: `update-profile-button` submits POST to `/update-profile`

---

## 4. Data Files

| Filename         | Data Directory | Field Order & Meaning                                                                                                          | Usage Context                         |
|------------------|----------------|------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|
| users.txt        | data/          | username|email|phone|full_name                                                                                                             | User profile management             |
| menu.txt         | data/          | dish_id|name|category|price|description|ingredients|dietary|avg_rating                                                                                                  | Menu listings, dish details         |
| reservations.txt | data/          | reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status                                                                       | Manage reservations, cancellation  |
| waitlist.txt     | data/          | waitlist_id|username|party_size|join_time|status                                                                                                  | Waitlist management                 |
| reviews.txt      | data/          | review_id|username|dish_id|rating|review_text|review_date                                                                              | User reviews, write reviews         |

---

## 5. User Navigation Flow Summary

- `/` or `/dashboard`: Shows Dashboard page.
- From Dashboard:
  - `make-reservation-button` -> `/reservation`
  - `view-menu-button` -> `/menu`
  - `my-reservations-button` -> `/my-reservations`
  - `my-reviews-button` -> `/my-reviews`
  - `waitlist-button` -> `/waitlist`
  - `profile-button` -> `/profile`
  - `back-to-dashboard` reloads `/dashboard`
- From Menu:
  - `view-dish-button-{dish_id}` -> `/dish/<dish_id>`
  - `back-to-dashboard` -> `/dashboard`
- From Dish Details:
  - `back-to-menu` -> `/menu`
- From Make Reservation:
  - submit reservation form (POST) -> process and redirect to `/dashboard`
  - `back-to-dashboard` -> `/dashboard`
- From My Reservations:
  - cancel button submits POST to `/cancel-reservation/<reservation_id>`
  - `back-to-dashboard` -> `/dashboard`
- From Waitlist:
  - join form submits POST to `/waitlist`
  - `back-to-dashboard` -> `/dashboard`
  - display waitlist position in `user-position`
- From My Reviews:
  - `write-new-review-button` -> `/write-review`
  - `back-to-dashboard` -> `/dashboard`
- From Write Review:
  - submit review form POST to `/write-review`
  - `back-to-reviews` -> `/my-reviews`
- From User Profile:
  - update profile form POST to `/update-profile`
  - `back-to-dashboard` -> `/dashboard`

---

This design specification ensures clear backend routing and frontend structure separation, enabling independent development and consistent UI/UX.
