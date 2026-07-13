# Requirements Analysis for RestaurantReservation Web Application

## 1. Overview
This document details the requirements for the RestaurantReservation web application, including all user-visible pages, UI elements, user actions, navigation flows, and the data file schemas used by the system.

---

## 2. Pages and UI Elements

### 2.1 Dashboard Page
- **Page Title**: Restaurant Dashboard
- **Container ID**: `dashboard-page`
- **UI Elements**:
  - `welcome-message` (H1): Displays a welcome message including the username.
  - `make-reservation-button` (Button): Navigates to the Make Reservation page.
  - `view-menu-button` (Button): Navigates to the Menu page.
  - `back-to-dashboard` (Button): Refreshes or reloads the Dashboard page.
  - `my-reservations-button` (Button): Navigates to the My Reservations page.
  - `my-reviews-button` (Button): Navigates to the My Reviews page.
  - `waitlist-button` (Button): Navigates to the Waitlist page.
  - `profile-button` (Button): Navigates to the User Profile page.

### 2.2 Menu Page
- **Page Title**: Restaurant Menu
- **Container ID**: `menu-page`
- **UI Elements**:
  - `menu-grid` (Div): Displays the restaurant's dish cards, each showing image, name, price, and description.
  - `view-dish-button-{dish_id}` (Button, multiple): Each dish card has this button to view details of the dish identified by `dish_id`.
  - `back-to-dashboard` (Button): Navigates back to the Dashboard page.

### 2.3 Dish Details Page
- **Page Title**: Dish Details
- **Container ID**: `dish-details-page`
- **UI Elements**:
  - `dish-name` (H1): Displays the name of the dish.
  - `dish-price` (Div): Displays the price of the dish.
  - `back-to-menu` (Button): Navigates back to the Menu page.

### 2.4 Make Reservation Page
- **Page Title**: Make Reservation
- **Container ID**: `reservation-page`
- **UI Elements**:
  - `guest-name` (Input): Input field to accept guest's name.
  - `party-size` (Dropdown): Dropdown to select number of guests (1-10).
  - `reservation-date` (Input - date): Date picker for selecting reservation date.
  - `submit-reservation-button` (Button): Submits the reservation data.
  - `back-to-dashboard` (Button): Navigates back to the Dashboard page.

### 2.5 My Reservations Page
- **Page Title**: My Reservations
- **Container ID**: `my-reservations-page`
- **UI Elements**:
  - `reservations-table` (Table): Lists all reservations made by the user showing date, time, party size, and status.
  - `cancel-reservation-button-{reservation_id}` (Button, multiple): Button to cancel a specific upcoming reservation identified by `reservation_id`.
  - `back-to-dashboard` (Button): Navigates back to the Dashboard page.

### 2.6 Waitlist Page
- **Page Title**: Waitlist
- **Container ID**: `waitlist-page`
- **UI Elements**:
  - `waitlist-party-size` (Dropdown): Dropdown to select party size for the waitlist.
  - `join-waitlist-button` (Button): Button to join the waitlist.
  - `user-position` (Div): Displays the user's current position on the waitlist.
  - `back-to-dashboard` (Button): Navigates back to the Dashboard page.

### 2.7 My Reviews Page
- **Page Title**: My Reviews
- **Container ID**: `reviews-page`
- **UI Elements**:
  - `reviews-list` (Div): Lists the user's reviews including dish name, rating, and review text.
  - `write-new-review-button` (Button): Navigates to the Write Review page.
  - `back-to-dashboard` (Button): Navigates back to the Dashboard page.

### 2.8 Write Review Page
- **Page Title**: Write Review
- **Container ID**: `write-review-page`
- **UI Elements**:
  - `select-dish` (Dropdown): Dropdown to select the dish to be reviewed.
  - `rating-input` (Dropdown): Dropdown to select a rating from 1 to 5 stars.
  - `review-text` (Textarea): Text area to write the review body.
  - `submit-review-button` (Button): Submits the review.
  - `back-to-reviews` (Button): Navigates back to the My Reviews page.

### 2.9 User Profile Page
- **Page Title**: My Profile
- **Container ID**: `profile-page`
- **UI Elements**:
  - `profile-username` (Div): Displays the username (read-only).
  - `profile-email` (Input): Input field for the user to update their email address.
  - `update-profile-button` (Button): Saves the updated profile information.
  - `back-to-dashboard` (Button): Navigates back to the Dashboard page.

---

## 3. User Actions and Navigation Flows

### 3.1 From Dashboard Page
- Clicking `make-reservation-button`: Opens Make Reservation page.
- Clicking `view-menu-button`: Opens Menu page.
- Clicking `my-reservations-button`: Opens My Reservations page.
- Clicking `my-reviews-button`: Opens My Reviews page.
- Clicking `waitlist-button`: Opens Waitlist page.
- Clicking `profile-button`: Opens User Profile page.
- Clicking `back-to-dashboard`: Refreshes Dashboard page.

### 3.2 From Menu Page
- Clicking any `view-dish-button-{dish_id}`: Opens Dish Details page for the selected dish.
- Clicking `back-to-dashboard`: Returns to Dashboard page.

### 3.3 From Dish Details Page
- Clicking `back-to-menu`: Returns to Menu page.

### 3.4 From Make Reservation Page
- Enter guest name, select party size, select reservation date.
- Clicking `submit-reservation-button`: Submits reservation, validates data, then likely returns to Dashboard or confirmation screen.
- Clicking `back-to-dashboard`: Returns to Dashboard page.

### 3.5 From My Reservations Page
- Displays list of reservations.
- Clicking any `cancel-reservation-button-{reservation_id}`: Cancels the specified reservation, updates reservations data.
- Clicking `back-to-dashboard`: Returns to Dashboard page.

### 3.6 From Waitlist Page
- Select party size from `waitlist-party-size`.
- Clicking `join-waitlist-button`: Joins the waitlist, updates waitlist data.
- `user-position` dynamically shows current position in waitlist.
- Clicking `back-to-dashboard`: Returns to Dashboard page.

### 3.7 From My Reviews Page
- Displays list of user's reviews.
- Clicking `write-new-review-button`: Opens Write Review page.
- Clicking `back-to-dashboard`: Returns to Dashboard page.

### 3.8 From Write Review Page
- Select dish from `select-dish` dropdown.
- Select rating from `rating-input` dropdown.
- Enter review text in `review-text`.
- Clicking `submit-review-button`: Submits the review, updates reviews data.
- Clicking `back-to-reviews`: Returns to My Reviews page.

### 3.9 From User Profile Page
- Editing `profile-email` field.
- Clicking `update-profile-button`: Saves profile changes, updates user data.
- Clicking `back-to-dashboard`: Returns to Dashboard page.

---

## 4. Data File Schemas

All data files are stored in the `data` directory with pipe (`|`) delimited fields.

### 4.1 User Data (`users.txt`)
| Field Name | Description |
|----------------|-------------|
| username       | Unique user ID |
| email          | User email address |
| phone          | Phone number |
| full_name      | Full name of the user |

**Example:**
```
john_diner|john@example.com|555-1234|John Diner
jane_food|jane@example.com|555-5678|Jane Foodie
```

### 4.2 Menu Items Data (`menu.txt`)
| Field Name  | Description |
|-------------|-------------|
| dish_id     | Unique dish identifier |
| name        | Dish name |
| category    | Menu category (Appetizers, Main Course, Desserts, Beverages) |
| price       | Dish price (float) |
| description | Description of the dish |
| ingredients | Comma-separated list of ingredients |
| dietary     | Dietary info (e.g., Vegetarian, Gluten-Free, Vegan) |
| avg_rating  | Average rating (float) |

**Example:**
```
1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
```

### 4.3 Reservations Data (`reservations.txt`)
| Field Name       | Description |
|------------------|-------------|
| reservation_id   | Unique reservation ID |
| username          | User who made the reservation |
| guest_name        | Name of guest for reservation |
| phone             | Contact phone |
| email             | Contact email |
| party_size        | Number of guests |
| date              | Reservation date (YYYY-MM-DD) |
| time              | Reservation time (HH:MM) |
| special_requests  | Special requests if any |
| status            | Status of reservation (Upcoming, Completed, etc.) |

**Example:**
```
1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
```

### 4.4 Waitlist Data (`waitlist.txt`)
| Field Name   | Description |
|--------------|-------------|
| waitlist_id  | Unique waitlist entry ID |
| username     | User on the waitlist |
| party_size   | Number of people in party |
| join_time    | Timestamp when joined (YYYY-MM-DD HH:MM:SS) |
| status       | Status of entry (e.g., Active) |

**Example:**
```
1|john_diner|2|2024-11-22 18:30:00|Active
2|jane_food|4|2024-11-22 18:45:00|Active
```

### 4.5 Reviews Data (`reviews.txt`)
| Field Name  | Description |
|-------------|-------------|
| review_id   | Unique review ID |
| username   | User who wrote the review |
| dish_id    | ID of dish reviewed |
| rating     | Rating given (1-5) |
| review_text | Review content |
| review_date | Date of review (YYYY-MM-DD) |

**Example:**
```
1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
```

---

## 5. Summary
This requirements analysis captures:
- All user visible pages with container and element IDs.
- UI element types and descriptions.
- User actions including button clicks and navigation flows.
- Detailed data file formats and examples for all key data entities.

This document enables clear guidance for implementation and downstream architectural design.
