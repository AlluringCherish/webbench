# Frontend Design Specification for RestaurantReservation Web Application

---

## Section 1: Template and Page Specifications

### 1. Dashboard Page
- Template File: dashboard.html
- Page Title: "Restaurant Dashboard"
- Elements:
  - ID: dashboard-page - Div - Main container for dashboard content
  - ID: welcome-message - H1 - Display welcome message including username
  - ID: make-reservation-button - Button - Navigate to Make Reservation page
  - ID: view-menu-button - Button - Navigate to Menu page
  - ID: back-to-dashboard - Button - Refresh or reload Dashboard page
  - ID: my-reservations-button - Button - Navigate to My Reservations page
  - ID: my-reviews-button - Button - Navigate to My Reviews page
  - ID: waitlist-button - Button - Navigate to Waitlist page
  - ID: profile-button - Button - Navigate to User Profile page

---

### 2. Menu Page
- Template File: menu.html
- Page Title: "Restaurant Menu"
- Elements:
  - ID: menu-page - Div - Main container for menu content
  - ID: menu-grid - Div - Grid container for dish cards
  - ID Pattern: view-dish-button-{dish_id} - Button - View details of specific dish with dish_id
  - ID: back-to-dashboard - Button - Navigate back to Dashboard page

---

### 3. Dish Details Page
- Template File: dish_details.html
- Page Title: "Dish Details"
- Elements:
  - ID: dish-details-page - Div - Main container for dish details
  - ID: dish-name - H1 - Display the dish name
  - ID: dish-price - Div - Display the dish price
  - ID: back-to-menu - Button - Navigate back to Menu page

---

### 4. Make Reservation Page
- Template File: make_reservation.html
- Page Title: "Make Reservation"
- Elements:
  - ID: reservation-page - Div - Main container for reservation form
  - ID: guest-name - Input - Text input for guest name
  - ID: party-size - Dropdown - Select party size (1 to 10)
  - ID: reservation-date - Input (date) - Select reservation date
  - ID: submit-reservation-button - Button - Submit reservation form
  - ID: back-to-dashboard - Button - Navigate back to Dashboard page

---

### 5. My Reservations Page
- Template File: my_reservations.html
- Page Title: "My Reservations"
- Elements:
  - ID: my-reservations-page - Div - Main container for reservations list
  - ID: reservations-table - Table - Display list of user reservations with columns: date, time, party size, status
  - ID Pattern: cancel-reservation-button-{reservation_id} - Button - Cancel specific upcoming reservation
  - ID: back-to-dashboard - Button - Navigate back to Dashboard page

---

### 6. Waitlist Page
- Template File: waitlist.html
- Page Title: "Waitlist"
- Elements:
  - ID: waitlist-page - Div - Main container for waitlist content
  - ID: waitlist-party-size - Dropdown - Select party size for waitlist
  - ID: join-waitlist-button - Button - Join the waitlist
  - ID: user-position - Div - Display current user position in waitlist
  - ID: back-to-dashboard - Button - Navigate back to Dashboard page

---

### 7. My Reviews Page
- Template File: my_reviews.html
- Page Title: "My Reviews"
- Elements:
  - ID: reviews-page - Div - Main container for reviews list
  - ID: reviews-list - Div - List container of user reviews showing dish name, rating, and review text
  - ID: write-new-review-button - Button - Navigate to Write Review page
  - ID: back-to-dashboard - Button - Navigate back to Dashboard page

---

### 8. Write Review Page
- Template File: write_review.html
- Page Title: "Write Review"
- Elements:
  - ID: write-review-page - Div - Main container for review writing
  - ID: select-dish - Dropdown - Select dish for writing a review
  - ID: rating-input - Dropdown - Select rating (1 to 5 stars)
  - ID: review-text - Textarea - Input field for review content
  - ID: submit-review-button - Button - Submit review
  - ID: back-to-reviews - Button - Navigate back to My Reviews page

---

### 9. User Profile Page
- Template File: profile.html
- Page Title: "My Profile"
- Elements:
  - ID: profile-page - Div - Main container for profile information
  - ID: profile-username - Div - Display username (non-editable)
  - ID: profile-email - Input - Editable input for email address
  - ID: update-profile-button - Button - Save profile changes
  - ID: back-to-dashboard - Button - Navigate back to Dashboard page

---

## Section 2: Navigation and Context Variables

### Navigation Matrix (By Element IDs and Target Pages)

| From Page / Button ID             | To Page             |
|---------------------------------|---------------------|
| dashboard.html / make-reservation-button | make_reservation.html |
| dashboard.html / view-menu-button        | menu.html              |
| dashboard.html / back-to-dashboard (refresh) | dashboard.html      |
| dashboard.html / my-reservations-button  | my_reservations.html   |
| dashboard.html / my-reviews-button        | my_reviews.html       |
| dashboard.html / waitlist-button          | waitlist.html         |
| dashboard.html / profile-button           | profile.html          |

| menu.html / view-dish-button-{dish_id}    | dish_details.html (for selected dish) |
| menu.html / back-to-dashboard              | dashboard.html         |

| dish_details.html / back-to-menu           | menu.html              |

| make_reservation.html / submit-reservation-button | dashboard.html (after successful submit) |
| make_reservation.html / back-to-dashboard  | dashboard.html         |

| my_reservations.html / cancel-reservation-button-{reservation_id} | my_reservations.html (refresh after cancel) |
| my_reservations.html / back-to-dashboard   | dashboard.html         |

| waitlist.html / join-waitlist-button       | waitlist.html (refresh after join) |
| waitlist.html / back-to-dashboard           | dashboard.html         |

| my_reviews.html / write-new-review-button  | write_review.html      |
| my_reviews.html / back-to-dashboard         | dashboard.html        |

| write_review.html / submit-review-button   | my_reviews.html (after submit) |
| write_review.html / back-to-reviews        | my_reviews.html        |

| profile.html / update-profile-button        | profile.html (refresh after update) |
| profile.html / back-to-dashboard             | dashboard.html       |

---

### Context Variables for Each Template

1. **dashboard.html**
   - username: String (user's username for welcome message)
   - featured_dishes: List of dicts (optional, not specified but may be used for display)
   - upcoming_reservations: List of dicts (optional for summary)

2. **menu.html**
   - menu_items: List of dicts with keys:
       - dish_id (int or string)
       - name (string)
       - category (string)
       - price (float/string)
       - description (string)
       - avg_rating (float, optional)
   - This populates the menu-grid and button IDs

3. **dish_details.html**
   - dish: Dict with keys:
       - name (string)
       - price (float/string)
       - description (string, if shown)
       - category, ingredients, dietary info (optional)

4. **make_reservation.html**
   - possible_party_sizes: List[int] (1-10)
   - (guest-name input is empty or prefilled if logged in)

5. **my_reservations.html**
   - reservations: List of dicts with keys:
       - reservation_id
       - date
       - time
       - party_size
       - status
   - Only user's reservations are shown

6. **waitlist.html**
   - possible_party_sizes: List[int] (matching reservations dropdown)
   - user_position: Int or String (current position number in waitlist or message)

7. **my_reviews.html**
   - reviews: List of dicts with keys:
       - dish_name
       - rating
       - review_text
       - review_date (optional)

8. **write_review.html**
   - dishes_for_review: List of dicts with dish names and ids for dropdown

9. **profile.html**
   - username: String (display only)
   - email: String (prefilled for editing)

---

This frontend specification covers all HTML templates, static element IDs with their purposes, button flows for page navigation, and the essential context variables to dynamically render each template correctly according to the user_task_description. Frontend developers can rely solely on this document for implementation.
