# Design Specification for RestaurantReservation Application

## Overview
This document outlines the frontend and backend design specifications for a Flask-based restaurant reservation application. The application manages dishes, reviews, reservations, waitlist, and user profiles. Data is stored locally in pipe-delimited text files inside a `data` folder.

---

## Data Files and Formats

- `menu.txt`: dish_id|name|category|price|description|ingredients|dietary|avg_rating
- `reviews.txt`: review_id|username|dish_id|rating|review_text|review_date
- `reservations.txt`: reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
- `waitlist.txt`: waitlist_id|username|party_size|join_time|status
- `users.txt`: username|email|phone|full_name

---

## Flask Routes

### 1. Dashboard (`/dashboard`)
- **Method:** GET
- **Description:** Display overview: list of dishes with average ratings, user's reservations, and waitlist status.
- **Context Variables:**
  - `dishes`: List of dicts with dish details.
  - `reservations`: List of user reservation dicts.
  - `waitlist_position`: int (if user in waitlist, else None)
- **Templates:** `dashboard.html`

### 2. Menu (`/menu`)
- **Method:** GET
- **Description:** Show all dishes in a grid with category filter dropdown.
- **Context Variables:**
  - `dishes`: List of dicts of all dishes.
  - `categories`: List of unique categories.
- **Templates:** `menu.html`

### 3. Dish Details (`/dish/<int:dish_id>`)
- **Method:** GET
- **Description:** Show details of a single dish including reviews.
- **Context Variables:**
  - `dish`: dict with dish data.
  - `reviews`: List of reviews for the dish.
- **Templates:** `dish_details.html`

### 4. My Reviews (`/my-reviews`)
- **Method:** GET
- **Description:** Display the logged-in user's reviews with edit/delete options.
- **Context Variables:**
  - `reviews`: List of review dicts by user.
- **Templates:** `my_reviews.html`

### 5. Write Review (`/write-review/<int:dish_id>`)
- **Method:** GET, POST
- **Description:** Form to create or edit a review for a dish.
- **Context Variables:**
  - `dish`: dict with dish info.
  - `review`: dict if editing existing review or None.
- **Templates:** `write_review.html`

### 6. Reservations (`/reservations`)
- **Method:** GET, POST
- **Description:** Show user's reservations. POST to create/cancel reservations.
- **Context Variables:**
  - `reservations`: List of user reservations.
- **Templates:** `reservations.html`

### 7. Waitlist (`/waitlist`)
- **Method:** GET, POST
- **Description:** Display waitlist status and allow joining/leaving waitlist.
- **Context Variables:**
  - `waitlist`: List of waitlist entries.
  - `user_position`: int or None.
- **Templates:** `waitlist.html`

### 8. Profile (`/profile`)
- **Method:** GET, POST
- **Description:** View and edit user profile information.
- **Context Variables:**
  - `user`: dict of user data.
- **Templates:** `profile.html`


---

## Common Elements and IDs

### Buttons
- `back-to-dashboard` - Navigate back to dashboard from detail pages.
- `menu-grid` - Container for menu dish cards.
- `view-dish-button-{{ dish.dish_id }}` - Button to navigate to dish details.
- `submit-reservation-button` - Submit reservation form.
- `cancel-reservation-button-{{ reservation.reservation_id }}` - Cancel a reservation.
- `join-waitlist-button` - Join the waitlist form submission.
- `back-to-menu` - Back to menu page button.
- `my-reviews-button` - Go to user's reviews page.
- `write-new-review-button` - To write a new review on a dish.
- `submit-review-button` - Submit review form.
- `profile-button` - Navigate to profile page.
- `back-to-reviews` - Back to reviews list.

### Containers and Divs
- `dashboard`: Container div for the dashboard page.
- `menu`: Grid container showing dishes.
- `reservations-table`: Table listing user reservations.
- `reviews-list`: List or container showing reviews.
- `waitlist`: Container showing waitlist queue.
- `reservation-date`: Date selection dropdown for reservations.
- `party-size`: Dropdown for party size in forms.
- `rating-input`: Input for rating in reviews (1-5 float).

---

## Templates Summary

### dashboard.html
- Displays overview with dishes, user's reservations, waitlist status.
- Contains buttons linking to menu, reservations, profile, waitlist.

### menu.html
- Shows dishes in grid with category filter dropdown.
- Each dish shows name, category, price.
- Buttons to view details.

### dish_details.html
- Shows detailed dish info: name, category, price, description, ingredients, dietary info.
- Shows reviews for this dish.
- Buttons to write/edit reviews, back to menu/dashboard.

### my_reviews.html
- Lists user’s reviews with ratings, text, date.
- Buttons for editing or deleting each review.
- Navigation buttons back to dashboard.

### write_review.html
- Form to write/edit a review: rating input (float 1-5), review text textarea.
- Buttons to submit/cancel.

### reservations.html
- Lists current user reservations in a table.
- Form to create new reservation with fields: guest name, phone, email, party size, date, time, special requests.
- Buttons for canceling existing reservations.

### waitlist.html
- Shows waitlist queue.
- Button to join or leave waitlist.

### profile.html
- Shows profile info editable form: full name, email, phone.
- Button to save changes.

---

## Backend Implementation Notes

- Use Flask standard routing
- Read and write to text files with pipe-delimited format.
- Parse files into list of dicts for use in routes.
- Use `url_for()` for URL generation.
- For POST requests, validate input thoroughly.
- Update files atomically (read, modify, write).

---

## Example Context Variable Structures

- `dish`:
  ```python
  {
      'dish_id': int,
      'name': str,
      'category': str,
      'price': float,
      'description': str,
      'ingredients': str,
      'dietary': str,
      'avg_rating': float
  }
  ```

- `review`:
  ```python
  {
      'review_id': int,
      'username': str,
      'dish_id': int,
      'rating': float,
      'review_text': str,
      'review_date': str
  }
  ```

- `reservation`:
  ```python
  {
      'reservation_id': int,
      'username': str,
      'guest_name': str,
      'phone': str,
      'email': str,
      'party_size': int,
      'date': str,
      'time': str,
      'special_requests': str,
      'status': str
  }
  ```

- `waitlist_entry`:
  ```python
  {
      'waitlist_id': int,
      'username': str,
      'party_size': int,
      'join_time': str,
      'status': str
  }
  ```

- `user`:
  ```python
  {
      'username': str,
      'email': str,
      'phone': str,
      'full_name': str
  }
  ```

---

End of Design Specification.