# RestaurantReservation Web Application - Design Candidate A

---

## 1. Dashboard Page

- **Route Path:** `/`
- **Template:** `dashboard.html`
- **Page Title:** Restaurant Dashboard
- **Container Element:**
  - Div with ID: `dashboard-page`
- **Elements:**
  - H1 with ID: `welcome-message` (Displays username welcome)
  - Button with ID: `make-reservation-button` (Navigate to `/make-reservation`)
  - Button with ID: `view-menu-button` (Navigate to `/menu`)
  - Button with ID: `back-to-dashboard` (Refresh current `/` route)
  - Button with ID: `my-reservations-button` (Navigate to `/my-reservations`)
  - Button with ID: `my-reviews-button` (Navigate to `/my-reviews`)
  - Button with ID: `waitlist-button` (Navigate to `/waitlist`)
  - Button with ID: `profile-button` (Navigate to `/profile`)

---

## 2. Menu Page

- **Route Path:** `/menu`
- **Template:** `menu.html`
- **Page Title:** Restaurant Menu
- **Container Element:**
  - Div with ID: `menu-page`
- **Elements:**
  - Div with ID: `menu-grid` (Grid containing dish cards)
  - Buttons per dish card: `view-dish-button-{dish_id}` (Navigate to `/dish/{dish_id}`)
  - Button with ID: `back-to-dashboard` (Navigate to `/`)

---

## 3. Dish Details Page

- **Route Path:** `/dish/<int:dish_id>`
- **Template:** `dish_details.html`
- **Page Title:** Dish Details
- **Container Element:**
  - Div with ID: `dish-details-page`
- **Elements:**
  - H1 with ID: `dish-name` (Display dish name)
  - Div with ID: `dish-price` (Display dish price)
  - Button with ID: `back-to-menu` (Navigate to `/menu`)


---

## 4. Make Reservation Page

- **Route Path:** `/make-reservation`
- **Template:** `make_reservation.html`
- **Page Title:** Make Reservation
- **Container Element:**
  - Div with ID: `reservation-page`
- **Input Elements:**
  - Input text with ID: `guest-name` (Guest name input)
  - Dropdown select with ID: `party-size` (Options 1-10)
  - Input date with ID: `reservation-date` (Date picker)
- **Buttons:**
  - Button with ID: `submit-reservation-button` (Submit reservation)
  - Button with ID: `back-to-dashboard` (Navigate to `/`)

---

## 5. My Reservations Page

- **Route Path:** `/my-reservations`
- **Template:** `my_reservations.html`
- **Page Title:** My Reservations
- **Container Element:**
  - Div with ID: `my-reservations-page`
- **Elements:**
  - Table with ID: `reservations-table` (Columns for date, time, party size, status)
  - Buttons per upcoming reservation row: `cancel-reservation-button-{reservation_id}` (Trigger cancel action)
  - Button with ID: `back-to-dashboard` (Navigate to `/`)

---

## 6. Waitlist Page

- **Route Path:** `/waitlist`
- **Template:** `waitlist.html`
- **Page Title:** Waitlist
- **Container Element:**
  - Div with ID: `waitlist-page`
- **Input Controls:**
  - Dropdown select with ID: `waitlist-party-size` (Select party size)
- **Buttons:**
  - Button with ID: `join-waitlist-button` (Join waitlist)
  - Button with ID: `back-to-dashboard` (Navigate to `/`)
- **Display:**
  - Div with ID: `user-position` (Show user's waitlist position)

---

## 7. My Reviews Page

- **Route Path:** `/my-reviews`
- **Template:** `my_reviews.html`
- **Page Title:** My Reviews
- **Container Element:**
  - Div with ID: `reviews-page`
- **Elements:**
  - Div with ID: `reviews-list` (List of reviews: dish name, rating, review text)
  - Button with ID: `write-new-review-button` (Navigate to `/write-review`)
  - Button with ID: `back-to-dashboard` (Navigate to `/`)

---

## 8. Write Review Page

- **Route Path:** `/write-review`
- **Template:** `write_review.html`
- **Page Title:** Write Review
- **Container Element:**
  - Div with ID: `write-review-page`
- **Input Controls:**
  - Dropdown select with ID: `select-dish` (Select dish to review)
  - Dropdown select with ID: `rating-input` (Select rating 1-5 stars)
  - Textarea with ID: `review-text` (Write review text)
- **Buttons:**
  - Button with ID: `submit-review-button` (Submit review)
  - Button with ID: `back-to-reviews` (Navigate to `/my-reviews`)

---

## 9. User Profile Page

- **Route Path:** `/profile`
- **Template:** `profile.html`
- **Page Title:** My Profile
- **Container Element:**
  - Div with ID: `profile-page`
- **Display/Input Elements:**
  - Div with ID: `profile-username` (Show username, not editable)
  - Input text with ID: `profile-email` (Update email)
- **Buttons:**
  - Button with ID: `update-profile-button` (Save changes)
  - Button with ID: `back-to-dashboard` (Navigate to `/`)

---

# Navigation Summary

- The Dashboard page (`/`) is the root and starting point.
- Menu page navigates to dish details with dish_id parameter.
- Back buttons navigate logically (e.g., dish details to menu, menu or others to dashboard).
- Write review page links back to My Reviews page.

# Data Interaction Notes

- Dish Details, Menu, and Write Review pages require dish_id references.
- My Reservations handling needs reservation_id for cancellation.
- Waitlist manages party size selection and user position display.
- Profile allows updating email only.

# Flask Render_template Usage Example

```python
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    return render_template('dish_details.html', dish_id=dish_id)

# and so forth for other routes...
```

---

This completes the detailed design candidate for the RestaurantReservation application covering all specified nine pages, navigation flows, container element IDs, and data handling as required.