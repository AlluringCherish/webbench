# RestaurantReservation Application Design Specification

---

## Section 1: Flask Backend and Data Schemas

### Flask Route Specifications

| # | Page Name             | URL Path                          | HTTP Methods | Function Name          | Response Template       | Input Details                                    |
|---|-----------------------|---------------------------------|--------------|------------------------|-------------------------|--------------------------------------------------|
| 1 | Dashboard             | `/dashboard`                    | GET          | `dashboard()`          | `dashboard.html`        | None                                             |
| 2 | Menu                  | `/menu`                        | GET          | `menu()`               | `menu.html`             | Optional query params: `category`, `search`     |
| 3 | Dish Details          | `/menu/<int:dish_id>`           | GET          | `dish_details(dish_id)` | `dish_details.html`     | URL param: `dish_id`                             |
| 4 | Make Reservation      | `/reservation/make`             | GET, POST    | `make_reservation()`   | `make_reservation.html` | GET: None; POST: form data (`guest_name`, `party_size`, `reservation_date`), user identity|
| 5 | My Reservations       | `/reservations/my`              | GET          | `my_reservations()`    | `my_reservations.html`  | User identity                                    |
| 6 | Cancel Reservation    | `/reservations/cancel/<int:reservation_id>` | POST | `cancel_reservation(reservation_id)` | Redirect or status | URL param: `reservation_id`, user identity       |
| 7 | Waitlist              | `/waitlist`                    | GET, POST    | `waitlist()`           | `waitlist.html`         | GET: None; POST: form data (`party_size`), user identity |
| 8 | My Reviews            | `/reviews/my`                  | GET          | `my_reviews()`         | `my_reviews.html`       | User identity                                    |
| 9 | Write Review          | `/reviews/write`               | GET, POST    | `write_review()`       | `write_review.html`     | GET: None; POST: form data (`dish_id`, `rating`, `review_text`) |
| 10| User Profile          | `/profile`                    | GET, POST    | `profile()`            | `profile.html`          | GET: user identity; POST: form data (`email`)   |

---

### Data File Schemas and Examples

All data files are stored in the `data/` directory.

---

1. **users.txt**
- **Schema:** `username|email|phone|full_name`
- **Example:** `john_diner|john@example.com|555-1234|John Diner`
- Operations: read all or by username, update email/phone, add new user, delete user if needed

---

2. **menu.txt**
- **Schema:** `dish_id|name|category|price|description|ingredients|dietary|avg_rating`
- Types: `dish_id` int, `price` float, `avg_rating` float
- **Example:** `1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5`

---

3. **reservations.txt**
- **Schema:** `reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status`
- Types: `reservation_id` int, `party_size` int, `date` `YYYY-MM-DD`, `time` `HH:MM` 24h, status string
- **Example:** `1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming`

---

4. **waitlist.txt**
- **Schema:** `waitlist_id|username|party_size|join_time|status`
- Types: `waitlist_id` int, `party_size` int, `join_time` datetime string `YYYY-MM-DD HH:MM:SS`, `status` string
- **Example:** `1|john_diner|2|2024-11-22 18:30:00|Active`

---

5. **reviews.txt**
- **Schema:** `review_id|username|dish_id|rating|review_text|review_date`
- Types: `review_id` int, `dish_id` int, `rating` int 1-5, `review_date` `YYYY-MM-DD`
- **Example:** `1|jane_food|2|5|Best salmon I've ever had!|2024-11-21`

---

### File Handling Instructions

- All reads load entire file into memory, parsed by `|` into dictionaries
- Writes to add open file in append mode
- Updates/deletes read full file, modify in-memory, overwrite file
- Use file locking during write/update to prevent race conditions

---

## Section 2: Frontend Templates and Navigation

### Template and Page Specifications

1. **Dashboard Page**
- Template: `dashboard.html`
- Page Title: "Restaurant Dashboard"
- Elements:
  - `dashboard-page`: Div main container
  - `welcome-message`: H1 welcome including username
  - `make-reservation-button`: Button to Make Reservation page
  - `view-menu-button`: Button to Menu page
  - `back-to-dashboard`: Button to refresh dashboard
  - `my-reservations-button`: Button to My Reservations
  - `my-reviews-button`: Button to My Reviews
  - `waitlist-button`: Button to Waitlist
  - `profile-button`: Button to User Profile

2. **Menu Page**
- Template: `menu.html`
- Page Title: "Restaurant Menu"
- Elements:
  - `menu-page`: Div main container
  - `menu-grid`: Div grid container for dishes
  - `view-dish-button-{dish_id}`: Button to Dish Details page
  - `back-to-dashboard`: Button back to Dashboard

3. **Dish Details Page**
- Template: `dish_details.html`
- Page Title: "Dish Details"
- Elements:
  - `dish-details-page`: Div main container
  - `dish-name`: H1 dish name
  - `dish-price`: Div dish price
  - `back-to-menu`: Button back to Menu

4. **Make Reservation Page**
- Template: `make_reservation.html`
- Page Title: "Make Reservation"
- Elements:
  - `reservation-page`: Div main container
  - `guest-name`: Input for guest name
  - `party-size`: Dropdown 1-10
  - `reservation-date`: Input (date)
  - `submit-reservation-button`: Button submit form
  - `back-to-dashboard`: Button back to Dashboard

5. **My Reservations Page**
- Template: `my_reservations.html`
- Page Title: "My Reservations"
- Elements:
  - `my-reservations-page`: Div main container
  - `reservations-table`: Table listing reservations (date, time, party size, status)
  - `cancel-reservation-button-{reservation_id}`: Button to cancel reservation
  - `back-to-dashboard`: Button back to Dashboard

6. **Waitlist Page**
- Template: `waitlist.html`
- Page Title: "Waitlist"
- Elements:
  - `waitlist-page`: Div main container
  - `waitlist-party-size`: Dropdown party size
  - `join-waitlist-button`: Button to join waitlist
  - `user-position`: Div show user's waitlist position
  - `back-to-dashboard`: Button back to Dashboard

7. **My Reviews Page**
- Template: `my_reviews.html`
- Page Title: "My Reviews"
- Elements:
  - `reviews-page`: Div main container
  - `reviews-list`: Div list of user reviews
  - `write-new-review-button`: Button to go to Write Review
  - `back-to-dashboard`: Button back to Dashboard

8. **Write Review Page**
- Template: `write_review.html`
- Page Title: "Write Review"
- Elements:
  - `write-review-page`: Div main container
  - `select-dish`: Dropdown dish selection
  - `rating-input`: Dropdown rating 1-5
  - `review-text`: Textarea for review
  - `submit-review-button`: Button submit review
  - `back-to-reviews`: Button back to My Reviews

9. **User Profile Page**
- Template: `profile.html`
- Page Title: "My Profile"
- Elements:
  - `profile-page`: Div main container
  - `profile-username`: Div show username (non-editable)
  - `profile-email`: Input editable email
  - `update-profile-button`: Button save profile
  - `back-to-dashboard`: Button back to Dashboard

---

### Navigation Matrix (By Element IDs and Target Pages)

| From Page / Button ID                 | To Page                        |
|------------------------------------|-------------------------------|
| dashboard.html / make-reservation-button | make_reservation.html          |
| dashboard.html / view-menu-button         | menu.html                     |
| dashboard.html / back-to-dashboard         | dashboard.html                |
| dashboard.html / my-reservations-button   | my_reservations.html          |
| dashboard.html / my-reviews-button         | my_reviews.html               |
| dashboard.html / waitlist-button           | waitlist.html                 |
| dashboard.html / profile-button            | profile.html                  |
| menu.html / view-dish-button-{dish_id}     | dish_details.html (selected dish) |
| menu.html / back-to-dashboard               | dashboard.html                |
| dish_details.html / back-to-menu            | menu.html                    |
| make_reservation.html / submit-reservation-button | dashboard.html (after submit) |
| make_reservation.html / back-to-dashboard   | dashboard.html               |
| my_reservations.html / cancel-reservation-button-{reservation_id} | my_reservations.html (refresh) |
| my_reservations.html / back-to-dashboard    | dashboard.html               |
| waitlist.html / join-waitlist-button        | waitlist.html (refresh)      |
| waitlist.html / back-to-dashboard            | dashboard.html               |
| my_reviews.html / write-new-review-button   | write_review.html            |
| my_reviews.html / back-to-dashboard          | dashboard.html               |
| write_review.html / submit-review-button    | my_reviews.html (after submit) |
| write_review.html / back-to-reviews         | my_reviews.html              |
| profile.html / update-profile-button         | profile.html (refresh)       |
| profile.html / back-to-dashboard              | dashboard.html               |

---

### Context Variables per Template

1. **dashboard.html**
- `username`: String for user welcome
- Optional: `featured_dishes` list, `upcoming_reservations` list

2. **menu.html**
- `menu_items`: List of dishes dicts with `dish_id`, `name`, `category`, `price`, `description`, `avg_rating`

3. **dish_details.html**
- `dish`: Dict with keys `name`, `price`, `description`, optional `category`, `ingredients`, `dietary`

4. **make_reservation.html**
- `possible_party_sizes`: List[int] from 1 to 10
- `guest_name` input may be empty or prefilled if logged in

5. **my_reservations.html**
- `reservations`: List of dicts with `reservation_id`, `date`, `time`, `party_size`, `status`

6. **waitlist.html**
- `possible_party_sizes`: List[int]
- `user_position`: current position or message

7. **my_reviews.html**
- `reviews`: List of dicts with `dish_name`, `rating`, `review_text`, optional `review_date`

8. **write_review.html**
- `dishes_for_review`: List of dicts with dish names and ids

9. **profile.html**
- `username`: String display only
- `email`: String editable

---

This unified design specification aligns the backend Flask route design with the frontend template design including navigation, UI elements, and data schemas to deliver a consistent implementation roadmap for developers.
