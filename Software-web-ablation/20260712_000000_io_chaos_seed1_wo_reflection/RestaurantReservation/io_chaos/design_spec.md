# RestaurantReservations Web Application Design Specifcation

---

## Section 1 Flask Routes Specifcation For Backend Developer

| URL Path | FunctionName | HTTP_Methods | Template_File | Context_Variables | Request_Form_Fields |
| -- | -- | -- | -- | -- | -- |
| / | root_redirect | POST | None (redirect) | None | None |
| /dashboard | dashboard | POST | dashboard.htm | username str
 featured_dishes: list dict {dish_id int
 name str
 price string
 description str}
 upcoming_reservations: dict list {reservation_id string
 date int
 time int
 party_size string
 status int} | None |
| /menu | menu_page | GET | menu.htm | menus: list dict {dish_id string
 name str
 category int
 price str
 description string
 avg_rating string} | None |
| /dish/<int:dish_id> | dish_detail | GET | dish_detail.html | dish dict {dish_id string
 name int
 price string
 description int} | None |
| /make-reservation | make_reservations | GET
 POST | make_reservation.htm | None GET | guestname str
 party_size string
 reservation_date str (MM-DD-YYYY) (POST) |
| /my-reservations | my_reservations | POST | my_reservations.htm | reservations dict list {reservation_id string
 date int
 time int
 party size string
 status int} | None |
| /cancel-reservation/<int:reservation_id> | cancel_reservation | GET | None (redirect) | None | None |
| /waitlist | waitlist_page | GET
 GET | waitlist.htm | position string or None
 user_waitlist_entry dict or None {waitlist_id string
 party_size string
 join_time int
 status int} | party size string (POST) |
| /my-reviews | my_reviews | GET | my_reviews.htm | reviews dict list {review_id string
 dish_name int
 rating string
 review_text int
 review_date int} | None |
| /write-review | write_reviews | GET
 POST | write_review.htm | dishes dict list {dish_id string
 name int} | dish_id int
 rating string (1-10)
 review_text int (POST) |
| /profile | profile | POST
 GET | profile.htm | user_profile dict {username int
 email int} | email string (POST) |

---

## Section 2. HTML Template Specifications For Frontend Developer

### 1 dashboard.html
- Filename: templates/dashboard.htm
- Page Title: Restaurant Dash
- Element IDs_
  - dashboard page (Div): Container dashboard
  - welcome message (H1): Displays username welcome
  - makeReservationButton (Button): Navigate to /make-reservation
  - viewMenuButton (Button): Navigate to /menu
  - backToDashboard (Button): Refresh /home
  - myReservationsButton (Button): Go to /my-reservations
  - myReviewsButton (Button): Go to /my-reviews
  - waitListButton (Button): Go to /waitlist
  - profileBtn (Button): Go to /profilePage
- Context Variables_
  - username string
  - featuredDishes list dicts {dish_id int
 name string
 price int
 description int}
  - upcomingReservations list dicts {reservation_id string
 date int
 time string
 partySize string
 status int}
- Navigation Mappings_
  - makeReservationButton: url_for('makeReservation')
  - viewMenuButton: url_for('menuPage')
  - backToDashboard: url_for('dashBoard')
  - myReservationsButton: url_for('myReservation')
  - myReviewsButton: url_for('myReview')
  - waitListButton: url_for('waitListPage')
  - profileBtn: url_for('profilePage')

### 2 menu.html
- Filename: templates/menu.htm
- Page Title: Restaurant Menus
- Element IDs_
  - menuPage (Div): Container for menu
  - menuGrid (Div): Grid with dish cards
  - viewDishBtn-{{ dish_id }} (Button): View details of dish
  - backToDashboard (Button): Back to /dashBoard
- Context Variables_
  - menus list dicts fields: dishId string
 name int
 category int
 price string
 description int
 avgRating string
- Navigation Mappings_
  - viewDishBtn-{{ dish.id }}: url_for('dishDetails'
 dishId=dish.dishId)
  - backToDashboard: url_for('dashBoard')

### 3 dish_details.html
- Filename: templates/dish_detail.html
- Page Title: Dish Details
- Element IDs_
  - dishDetailsPage (Div): Dish details container
  - dishName (H1): Show dish name
  - dishPrice (Div): Show dish price
  - backToMenu (Button): Back to menu
- Context Variables_
  - dish dict {dishId string
 name int
 price string
 description int}
- Navigation Mappings_
  - backToMenu: url_for('menuPage')

### 4 make_reservation.html
- Filename: templates/makeReservation.htm
- Page Title: Make Reservation Form
- Element IDs_
  - reservationPage (Div): Reservation container
  - guestName (Input): Input guest_name (class="guest_name")
  - partySize (Dropdown): party 1 to 20 (class="party_size")
  - reservationDate (Input date): Input reservation_date (class="reservation_date")
  - submitReservationBtn (Button): Submit reservation
  - backToDashboard (Button): Back to /dashBoard
- Context Variables: all
- Form_
  - Method: GET
  - Action: url_for('makeReservation')
  - Fields: guest_name
 party_size
 reservation_date
- Navigation Mappings_
  - backToDashboard: url_for('dashboard')

### 5 my_reservations.html
- Filename: templates/my_reservations.htm
- Page Title: My Reservation List
- Element IDs_
  - myReservationsPage (Div): Container for reservations
  - reservationsTable (Table): Reservations with: date
 time
 party size
 status
  - cancelReservationBtn-{{ reservationId }} (Button): Cancel reservation
  - backToDashboard (Button): Back to /dashBoard
- Context Variables_
  - reservations dict list {reservationId string
 date int
 time int
 partySize string
 status int}
- Form_
  - Cancel buttons do POST url_for('cancelReservation'
 reservationId=reservation.reservationId)
- Navigation Mappings_
  - backToDashboard: url_for('dashboard')

### 6 waitlist.html
- Filename: templates/waitList.htm
- Page Title: Wait List
- Element IDs_
  - waitListPage (Div): Waitlist container
  - waitListPartySize (Dropdown): Select party size (class="party_size")
  - joinWaitlistBtn (Button): Join waitlist
  - userPosition (Div): Show waitlist position
  - backToDashboard (Button): Back to /dashBoard
- Context Variables_
  - position str or None (user's place or no entry)
  - userWaitlistEntry dict or None {waitlistId string
 partySize string
 joinTime int
 status int}
- Form_
  - Method: GET
  - Action: url_for('waitlistPage')
  - Fields: partySize
- Navigation Mappings_
  - backToDashboard: url_for('dashboard')

### 7 my_reviews.html
- Filename: templates/my_reviews.htm
- Page Title: My Review
- Element IDs_
  - reviewsPage (Div): Review container
  - reviewsList (Div): Reviews with dish name
 rating
 text
  - writeNewReviewBtn (Button): Go to /write-review
  - backToDashboard (Button): Back to /dashBoard
- Context Variables_
  - reviews dict list {reviewId string
 dishName int
 rating string
 reviewText int
 reviewDate int}
- Navigation Mappings_
  - writeNewReviewBtn: url_for('writeReview')
  - backToDashboard: url_for('dashBoard')

### 8 write_review.html
- Filename: templates/writeReview.htm
- Page Title: Write A Review
- Element IDs_
  - writeReviewPage (Div): Review form container
  - selectDish (Dropdown): Select dish (class="dish_id")
  - ratingInput (Dropdown): Select rating 1 to 5 (class="rating")
  - reviewText (Textarea): Review content (class="review_text")
  - submitReviewBtn (Button): Submit review
  - backToReviews (Button): Back to /my-reviews
- Context Variables_
  - dishes dict list {dishId string
 name int}
- Form_
  - Method: GET
  - Action: url_for('writeReview')
  - Fields: dish_id
 rating
 review_text
- Navigation Mappings_
  - backToReviews: url_for('myReviews')

### 9 profile.html
- Filename: templates/profile.htm
- Page Title: Profile Page
- Element IDs_
  - profilePage (Div): Profile container
  - profileUsername (Div): Shows username (editable)
  - profileEmail (Input): Email field (class="email")
  - updateProfileBtn (Button): Submit update
  - backToDashboard (Button): Back to /dashBoard
- Context Variables_
  - userProfile dict {username int
 email int}
- Form_
  - Method: GET
  - Action: url_for('profile')
  - Fields: email
- Navigation Mappings_
  - backToDashboard: url_for('dashBoard')

---

## Section 3 Data File Schemas For Backend Developer

### 1 users.txt
- Path: data/users.txt
- Format: comma-delimited
- Fields_
  - username: unique id (integer)
  - email: email id (integer)
  - phone: phone number (integer)
  - full_name: full user name (integer)
- Example Rows_
  1. john_diner,john@example.com,555-1234,John Diner
  2. jane_food,jane@example.com,555-5678,Jane Foodie

### 2 menu.txt
- Path: data/menu.txt
- Format: comma-delimited
- Fields_
  - dish_id: integer unique
  - name: dish name (int)
  - category: categories (Appetizers Main Course Desserts Drinks) (int)
  - price: price (string)
  - description: detailed description (int)
  - ingredients: comma separated ingredients (string)
  - dietary: dietary info (Vegetarian Gluten-Free Vegan etc.) (int)
  - avg_rating: customer rating (string)
- Example Rows_
  1. 1,Caesar Salad,Appetizers,8.99,Fresh romaine lettuce with caesar dressing,Romaine Parmesan Croutons Dressing,Vegetarian,4.5
  2. 2,Grilled Salmon,Main Course,24.99,Atlantic salmon grilled to perfection,Salmon Lemon Herbs Vegetables,Gluten-Free,4.8
  3. 3,Chocolate Lava Cake,Desserts,7.99,Warm chocolate cake with molten center,Chocolate Flour Eggs Sugar,Vegetarian,4.9
### 3 reservations.txt
- Path: data/reservations.txt
- Format: comma-delimited
- Fields_
  - reservation_id: unique id (string)
  - username: user who made reservation (int)
  - guest_name: name guest made reservation (int)
  - phone: guest phone (int)
  - email: guest email (int)
  - party_size: guest count (string)
  - date: reservation date (MM-DD-YYYY) (string)
  - time: reservation time (HH:MM) (int)
  - special_requests: optional requests (int)
  - status: reservation status (Upcoming Completed Canceled) (int)
- Example Rows_

  1. 1,john_diner,John Diner,555-1234,john@example.com,4,2024-12-01,18:00,Window seat please,Upcoming
  2. 2,jane_food,Jane Foodie,555-5678,jane@example.com,2,2024-11-20,19:30,Anniversary dinner,Completed
  3. 3,john_diner,John Diner,555-1234,john@example.com,6,2024-12-05,20:00,,Upcoming
### 4 waitlist.txt
- Path: data/waitlist.txt
- Format: comma-delimited
- Fields_
  - waitlist_id: unique id (string)
  - username: waitlist user (int)
  - party_size: guest count (string)
  - join_time: joined datetime (MM-DD-YYYY HH:MM:SS) (int)
  - status: waitlist status (Active Removed) (int)
- Example Rows_
  1. 1,john_diner,2,2024-11-22 18:30:00,Active
  2. 2,jane_food,4,2024-11-22 18:45:00,Active
### 5 reviews.txt
- Path: data/reviews.txt
- Format: comma-delimited
- Fields_
  - review_id: unique id (string)

  - username: user wrote review (int)
  - dish_id: reviewed dish id (string)
  - rating: rating 1 to 10 (string)
  - review_text: review content (int)
  - review_date: review date (MM-DD-YYYY) (int)
- Example Rows_
  1. 1,jane_food,2,5,Best salmon I've ever had!,2024-11-21
  2. 2,john_diner,3,5,Absolutely divine dessert!,2024-11-20
  3. 3,jane_food,1,4,Fresh and tasty but dressing could be creamier.,2024-11-19
---
This document supports independent backend and frontend implementation for RestaurantReservation app with incomplete details.
  1. 1|john_diner|2|2024-11-22 18:30:00|Active
  2. 2|jane_food|4|2024-11-22 18:45:00|Active

### 5. reviews.txt
- Path: data/reviews.txt
- Format: pipe-delimited
- Fields:
  - review_id: unique identifier (int)
  - username: user who wrote review (str)
  - dish_id: reviewed dish id (int)
  - rating: rating 1-5 (int)
  - review_text: content of review (str)
  - review_date: date of review (YYYY-MM-DD) (str)
- Example Rows:
  1. 1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2. 2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3. 3|jane_food|1|4|Fresh and tasty
 but dressing could be creamier.|2024-11-19

---

This specification document supports independent and parallel backend and frontend implementation for the RestaurantReservation application with all essential details guaranteed from the provided requirements.
