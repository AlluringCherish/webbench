# RestaurantReservation Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path                 | Function Name           | HTTP Methods | Template File             | Context Variables (name: type, details)                                                                                                                                      | Request Form Fields (POST)                              |
|--------------------------|------------------------|--------------|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| /                        | root_redirect           | GET          | None                      | None (Redirect to /dashboard)                                                                                                                                                 | None                                                   |
| /dashboard               | dashboard              | GET          | dashboard.html            | username: str; featured_dishes: list of dict{name:int dish_id, str name, float price, str description}, upcoming_reservations: list of dict{int reservation_id, str date, str time, int party_size, str status} | None                                                   |
| /menu                    | menu                   | GET          | menu.html                 | menus: list of dict{int dish_id, str name, str category, float price, str description}                                                                                          | None                                                   |
| /dish/<int:dish_id>      | dish_details           | GET          | dish_details.html         | dish: dict{int dish_id, str name, float price, str description}                                                                                                               | None                                                   |
| /make_reservation        | make_reservation       | GET, POST    | make_reservation.html     | None for GET; On POST redirect or reload after saving reservation                                                                                                            | guest_name: str, party_size: int, reservation_date: str (YYYY-MM-DD) |
| /my_reservations         | my_reservations        | GET          | my_reservations.html      | reservations: list of dict{int reservation_id, str date, str time, int party_size, str status} (user's reservations)                                                            | None                                                   |
| /cancel_reservation/<int:reservation_id> | cancel_reservation     | POST         | None (redirect)           | None                                                                                                                                                                        | None                                                   |
| /waitlist                | waitlist               | GET, POST    | waitlist.html             | position: int or None (current user position in waitlist); user_waitlist_active: bool                                                                                          | party_size: int                                         |
| /my_reviews              | my_reviews             | GET          | my_reviews.html           | reviews: list of dict{int review_id, str dish_name, int rating, str review_text, str review_date}                                                                             | None                                                   |
| /write_review            | write_review           | GET, POST    | write_review.html         | dishes: list of dict{int dish_id, str name} for dropdown                                                                                                                     | dish_id: int, rating: int(1-5), review_text: str         |
| /profile                 | profile                | GET, POST    | profile.html              | profile: dict{str username, str email}                                                                                                                                       | email: str                                             |

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Elements:
  - dashboard-page (div): Container for dashboard
  - welcome-message (h1): Welcome message showing username
  - make-reservation-button (button): Navigate to make_reservation (url_for('make_reservation'))
  - view-menu-button (button): Navigate to menu (url_for('menu'))
  - back-to-dashboard (button): Refresh dashboard (url_for('dashboard'))
  - my-reservations-button (button): Navigate to my_reservations (url_for('my_reservations'))
  - my-reviews-button (button): Navigate to my_reviews (url_for('my_reviews'))
  - waitlist-button (button): Navigate to waitlist (url_for('waitlist'))
  - profile-button (button): Navigate to profile (url_for('profile'))
- Context Variables:
  - username: str
  - featured_dishes: list of dict {dish_id, name, price, description}
  - upcoming_reservations: list of dict {reservation_id, date, time, party_size, status}
- Navigation:
  - All buttons link to routes as above

### 2. Menu Page
- Filename: templates/menu.html
- Page Title: Restaurant Menu
- Elements:
  - menu-page (div): Container for menu
  - menu-grid (div): Grid displaying dish cards
  - view-dish-button-{{ dish.dish_id }} (button): View details of dish
  - back-to-dashboard (button): Navigate to dashboard
- Context Variables:
  - menus: list of dict {dish_id, name, category, price, description}
- Navigation:
  - view-dish-button-{{ dish.dish_id }} links to url_for('dish_details', dish_id=dish.dish_id)
  - back-to-dashboard links to url_for('dashboard')

### 3. Dish Details Page
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Elements:
  - dish-details-page (div): Container
  - dish-name (h1): Display dish name
  - dish-price (div): Display dish price
  - back-to-menu (button): Navigate to menu
- Context Variables:
  - dish: dict {dish_id, name, price, description}
- Navigation:
  - back-to-menu links to url_for('menu')

### 4. Make Reservation Page
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Elements:
  - reservation-page (div): Container
  - guest-name (input): Name input field (name="guest_name")
  - party-size (dropdown): Select party size 1-10 (name="party_size")
  - reservation-date (input type="date"): Select date for reservation (name="reservation_date")
  - submit-reservation-button (button): Submit form
  - back-to-dashboard (button): Navigate to dashboard
- Context Variables: None
- Form:
  - Method: POST
  - Fields: guest_name, party_size, reservation_date
  - Action: url_for('make_reservation')
- Navigation:
  - back-to-dashboard links to url_for('dashboard')

### 5. My Reservations Page
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Elements:
  - my-reservations-page (div): Container
  - reservations-table (table): Table showing user's reservations
  - cancel-reservation-button-{{ reservation.reservation_id }} (button): Cancel a reservation
  - back-to-dashboard (button): Navigate to dashboard
- Context Variables:
  - reservations: list of dict {reservation_id, date, time, party_size, status}
- Form and Navigation:
  - cancel-reservation-button-{{ reservation.reservation_id }}: POST form or AJAX to /cancel_reservation/<reservation_id>
  - back-to-dashboard links to url_for('dashboard')

### 6. Waitlist Page
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Elements:
  - waitlist-page (div): Container
  - waitlist-party-size (dropdown): Select party size (name="party_size")
  - join-waitlist-button (button): Submit form
  - user-position (div): Shows user position or message if not in waitlist
  - back-to-dashboard (button): Navigate dashboard
- Context Variables:
  - position: int or None
  - user_waitlist_active: bool
- Form:
  - Method: POST
  - Fields: party_size
  - Action: url_for('waitlist')
- Navigation:
  - back-to-dashboard links to url_for('dashboard')

### 7. My Reviews Page
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Elements:
  - reviews-page (div): Container
  - reviews-list (div): List of reviews (dish name, rating, review text)
  - write-new-review-button (button): Navigate to write_review
  - back-to-dashboard (button): Navigate dashboard
- Context Variables:
  - reviews: list of dict {review_id, dish_name, rating, review_text, review_date}
- Navigation:
  - write-new-review-button links to url_for('write_review')
  - back-to-dashboard links to url_for('dashboard')

### 8. Write Review Page
- Filename: templates/write_review.html
- Page Title: Write Review
- Elements:
  - write-review-page (div): Container
  - select-dish (dropdown): Select dish to review (name="dish_id")
  - rating-input (dropdown): Select rating 1-5 (name="rating")
  - review-text (textarea): Write review (name="review_text")
  - submit-review-button (button): Submit form
  - back-to-reviews (button): Navigate back to my_reviews
- Context Variables:
  - dishes: list of dict {dish_id, name}
- Form:
  - Method: POST
  - Fields: dish_id, rating, review_text
  - Action: url_for('write_review')
- Navigation:
  - back-to-reviews links to url_for('my_reviews')

### 9. User Profile Page
- Filename: templates/profile.html
- Page Title: My Profile
- Elements:
  - profile-page (div): Container
  - profile-username (div): Displays username (read-only)
  - profile-email (input): Email update (name="email")
  - update-profile-button (button): Submit form
  - back-to-dashboard (button): Navigate dashboard
- Context Variables:
  - profile: dict {username, email}
- Form:
  - Method: POST
  - Fields: email
  - Action: url_for('profile')
- Navigation:
  - back-to-dashboard links to url_for('dashboard')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format (pipe-delimited): username|email|phone|full_name
- Description: Stores user account information
- Fields:
  - username: unique user identifier (str)
  - email: user email address (str)
  - phone: user phone number (str)
  - full_name: user full name (str)
- Examples:
  - john_diner|john@example.com|555-1234|John Diner
  - jane_food|jane@example.com|555-5678|Jane Foodie

### 2. menu.txt
- Path: data/menu.txt
- Format (pipe-delimited): dish_id|name|category|price|description|ingredients|dietary|avg_rating
- Description: Stores all menu dishes and their details
- Fields:
  - dish_id: integer identifier
  - name: dish name (str)
  - category: dish category (e.g. Appetizers, Main Course) (str)
  - price: dish price (float)
  - description: textual description (str)
  - ingredients: comma separated ingredients (str)
  - dietary: dietary info (str)
  - avg_rating: average rating (float)
- Examples:
  - 1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  - 2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8

### 3. reservations.txt
- Path: data/reservations.txt
- Format (pipe-delimited): reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
- Description: Records of table reservations
- Fields:
  - reservation_id: int unique identifier
  - username: user who made reservation (str)
  - guest_name: name of guest booking (str)
  - phone: contact phone (str)
  - email: contact email (str)
  - party_size: number of guests (int)
  - date: reservation date (YYYY-MM-DD) (str)
  - time: reservation time (HH:MM) (str)
  - special_requests: special notes (str, optional)
  - status: status of reservation (str) e.g., Upcoming, Completed
- Examples:
  - 1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  - 2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed

### 4. waitlist.txt
- Path: data/waitlist.txt
- Format (pipe-delimited): waitlist_id|username|party_size|join_time|status
- Description: Stores data on current waitlist entries
- Fields:
  - waitlist_id: int unique identifier
  - username: user on waitlist (str)
  - party_size: party size (int)
  - join_time: datetime joined (YYYY-MM-DD HH:MM:SS) (str)
  - status: status of waitlist entry (str) e.g., Active
- Examples:
  - 1|john_diner|2|2024-11-22 18:30:00|Active
  - 2|jane_food|4|2024-11-22 18:45:00|Active

### 5. reviews.txt
- Path: data/reviews.txt
- Format (pipe-delimited): review_id|username|dish_id|rating|review_text|review_date
- Description: User submitted reviews for dishes
- Fields:
  - review_id: int unique identifier
  - username: user who submitted review (str)
  - dish_id: dish identifier (int)
  - rating: rating score (int 1-5)
  - review_text: text content of review (str)
  - review_date: date review was submitted (YYYY-MM-DD) (str)
- Examples:
  - 1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  - 2|john_diner|3|5|Absolutely divine dessert!|2024-11-20

---

This completes the design specification document for the RestaurantReservation application, enabling parallel backend and frontend development with clear route, template, and data schema definitions.