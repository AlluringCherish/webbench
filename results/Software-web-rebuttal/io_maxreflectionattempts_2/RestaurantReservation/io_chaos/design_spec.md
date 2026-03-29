# RestaurantReservation Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path                 | Function Name           | HTTP Methods | Template File                 | Context Variables (name:type)                                                                                 | Request Form Fields (POST)                                  |
|--------------------------|------------------------|--------------|-------------------------------|---------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| /                        | root_redirect          | GET          | -                             | -                                                                                                             | -                                                          |
| /dashboard               | dashboard_page          | GET          | dashboard.html                | username:str, featured_dishes:list of dict {dish_id:int, name:str, price:float}, upcoming_reservations:list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str} | -                                                          |
| /menu                    | menu_page               | GET          | menu.html                     | menus:list of dict {dish_id:int, name:str, category:str, price:float, description:str, ingredients:list of str, dietary:str, avg_rating:float}                         | -                                                          |
| /dish/<int:dish_id>       | dish_details_page       | GET          | dish_details.html             | dish:dict {dish_id:int, name:str, category:str, price:float, description:str, ingredients:list of str, dietary:str, avg_rating:float}                                  | -                                                          |
| /make_reservation        | make_reservation_page   | GET          | make_reservation.html         | -                                                                                                             | -                                                          |
| /submit_reservation      | submit_reservation      | POST         | redirect (to /my_reservations) | -                                                                                                             | guest_name:str, party_size:int, reservation_date:str (YYYY-MM-DD) |
| /my_reservations         | my_reservations_page    | GET          | my_reservations.html          | reservations:list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str}                                                         | -                                                          |
| /cancel_reservation/<int:reservation_id> | cancel_reservation      | POST         | redirect (to /my_reservations) | -                                                                                                             | -                                                          |
| /waitlist                | waitlist_page           | GET          | waitlist.html                 | user_position:int or None (position in waitlist if user active), party_size_options:list of int (1-10)                            | -                                                          |
| /join_waitlist           | join_waitlist           | POST         | redirect (to /waitlist)       | -                                                                                                             | party_size:int                                             |
| /my_reviews              | my_reviews_page         | GET          | my_reviews.html               | reviews:list of dict {review_id:int, dish_name:str, rating:int, review_text:str}, username:str                                                          | -                                                          |
| /write_review            | write_review_page       | GET          | write_review.html             | dishes:list of dict {dish_id:int, name:str}, username:str                                                                                           | -                                                          |
| /submit_review           | submit_review           | POST         | redirect (to /my_reviews)     | -                                                                                                             | dish_id:int, rating:int, review_text:str                    |
| /profile                 | profile_page            | GET          | profile.html                  | user_profile:dict {username:str, email:str}                                                                                                    | -                                                          |
| /update_profile          | update_profile          | POST         | redirect (to /profile)        | -                                                                                                             | email:str                                                 |

**Additional Notes:**
- The root route '/' should redirect to '/dashboard' using Flask's `redirect`.
- POST routes handle form submissions for reservations, cancellations, waitlist joining, reviews, and profile updates.
- Context variable structures mirror data file fields as appropriate.
- For lists, each item is a dict with specified fields and types.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Main <h1>: #welcome-message, shows "Welcome, {{ username }}!"
- Element IDs and types:
  - dashboard-page (Div): main container
  - welcome-message (H1): greeting with username
  - make-reservation-button (Button): navigate to 'make_reservation_page'
  - view-menu-button (Button): navigate to 'menu_page'
  - back-to-dashboard (Button): refresh dashboard (calls 'dashboard_page')
  - my-reservations-button (Button): navigate to 'my_reservations_page'
  - my-reviews-button (Button): navigate to 'my_reviews_page'
  - waitlist-button (Button): navigate to 'waitlist_page'
  - profile-button (Button): navigate to 'profile_page'
- Context Variables:
  - username: str
  - featured_dishes: list of dict {dish_id:int, name:str, price:float}
  - upcoming_reservations: list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str}
- Navigation mappings:
  - make-reservation-button: url_for('make_reservation_page')
  - view-menu-button: url_for('menu_page')
  - back-to-dashboard: url_for('dashboard_page')
  - my-reservations-button: url_for('my_reservations_page')
  - my-reviews-button: url_for('my_reviews_page')
  - waitlist-button: url_for('waitlist_page')
  - profile-button: url_for('profile_page')

### 2. Menu Page
- Filename: templates/menu.html
- Page Title: Restaurant Menu
- Main <h1>: Could be the page title or a header inside menu-page div
- Element IDs and types:
  - menu-page (Div): container
  - menu-grid (Div): holds dish cards
  - view-dish-button-{{ dish.dish_id }} (Button): view details (dynamic id)
  - back-to-dashboard (Button): go back
- Context Variables:
  - menus: list of dict {dish_id:int, name:str, category:str, price:float, description:str, ingredients:list of str, dietary:str, avg_rating:float}
- Navigation mappings:
  - view-dish-button-{{ dish.dish_id }}: url_for('dish_details_page', dish_id=dish.dish_id)
  - back-to-dashboard: url_for('dashboard_page')

### 3. Dish Details Page
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Element IDs and types:
  - dish-details-page (Div): main container
  - dish-name (H1): name of the dish
  - dish-price (Div): price
  - back-to-menu (Button): back to menu
- Context Variables:
  - dish: dict {dish_id:int, name:str, category:str, price:float, description:str, ingredients:list of str, dietary:str, avg_rating:float}
- Navigation mappings:
  - back-to-menu: url_for('menu_page')

### 4. Make Reservation Page
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Element IDs and types:
  - reservation-page (Div): container
  - guest-name (Input): text input for guest name
  - party-size (Dropdown): selection from 1 to 10
  - reservation-date (Input type=date): reservation date
  - submit-reservation-button (Button): submits form POST to '/submit_reservation'
  - back-to-dashboard (Button): go back
- Context Variables: None required
- Form:
  - action: url_for('submit_reservation')
  - method: POST
  - Input names: guest_name, party_size, reservation_date
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

### 5. My Reservations Page
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Element IDs and types:
  - my-reservations-page (Div): container
  - reservations-table (Table): displays reservations with columns date, time, party size, status
  - cancel-reservation-button-{{ reservation.reservation_id }} (Button): cancel upcoming reservation (dynamic id)
  - back-to-dashboard (Button): go back
- Context Variables:
  - reservations: list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str}
- Form for cancelling reservation:
  - method: POST
  - action url_for('cancel_reservation', reservation_id=reservation.reservation_id)
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

### 6. Waitlist Page
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Element IDs and types:
  - waitlist-page (Div): container
  - waitlist-party-size (Dropdown): select party size
  - join-waitlist-button (Button): submits form to join waitlist
  - user-position (Div): shows user position
  - back-to-dashboard (Button): go back
- Context Variables:
  - user_position: int or None
  - party_size_options: list of ints (1-10)
- Form:
  - method: POST
  - action: url_for('join_waitlist')
  - Input name: party_size
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

### 7. My Reviews Page
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs and types:
  - reviews-page (Div): container
  - reviews-list (Div): list reviews with dish name, rating, and review text
  - write-new-review-button (Button): navigate to write review page
  - back-to-dashboard (Button): go back
- Context Variables:
  - reviews: list of dict {review_id:int, dish_name:str, rating:int, review_text:str}
  - username: str
- Navigation mappings:
  - write-new-review-button: url_for('write_review_page')
  - back-to-dashboard: url_for('dashboard_page')

### 8. Write Review Page
- Filename: templates/write_review.html
- Page Title: Write Review
- Element IDs and types:
  - write-review-page (Div): container
  - select-dish (Dropdown): select dish to review
  - rating-input (Dropdown): select rating 1-5 stars
  - review-text (Textarea): text for review
  - submit-review-button (Button): submits form
  - back-to-reviews (Button): go back to my reviews
- Context Variables:
  - dishes: list of dict {dish_id:int, name:str}
  - username: str
- Form:
  - method: POST
  - action: url_for('submit_review')
  - Input names: dish_id, rating, review_text
- Navigation mappings:
  - back-to-reviews: url_for('my_reviews_page')

### 9. User Profile Page
- Filename: templates/profile.html
- Page Title: My Profile
- Element IDs and types:
  - profile-page (Div): container
  - profile-username (Div): display username (readonly)
  - profile-email (Input): editable email input
  - update-profile-button (Button): save form
  - back-to-dashboard (Button): go back
- Context Variables:
  - user_profile: dict {username:str, email:str}
- Form:
  - method: POST
  - action: url_for('update_profile')
  - Input name: email
- Navigation mappings:
  - back-to-dashboard: url_for('dashboard_page')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format: Pipe-delimited
- Fields: username | email | phone | full_name
- Description: Stores registered user profiles including contact information.
- Example rows:
```
john_diner|john@example.com|555-1234|John Diner
jane_food|jane@example.com|555-5678|Jane Foodie
```

### 2. menu.txt
- Path: data/menu.txt
- Format: Pipe-delimited
- Fields: dish_id | name | category | price | description | ingredients | dietary | avg_rating
  - dish_id: int unique dish identifier
  - name: dish name
  - category: category e.g. Appetizers, Main Course, Desserts, Beverages
  - price: float
  - description: text description
  - ingredients: comma separated list of ingredient names
  - dietary: dietary info string (e.g. Vegetarian, Gluten-Free, Vegan)
  - avg_rating: float (average star rating)
- Description: Stores all menu items and their details.
- Example rows:
```
1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
```

### 3. reservations.txt
- Path: data/reservations.txt
- Format: Pipe-delimited
- Fields: reservation_id | username | guest_name | phone | email | party_size | date | time | special_requests | status
  - reservation_id: int unique identifier
  - username: user who made the reservation
  - guest_name: name of guest
  - phone: contact phone
  - email: contact email
  - party_size: int
  - date: YYYY-MM-DD
  - time: HH:MM
  - special_requests: optional text
  - status: e.g. Upcoming, Completed, Cancelled
- Description: Stores all reservation data.
- Example rows:
```
1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
```

### 4. waitlist.txt
- Path: data/waitlist.txt
- Format: Pipe-delimited
- Fields: waitlist_id | username | party_size | join_time | status
  - waitlist_id: int unique waitlist entry id
  - username: user who joined waitlist
  - party_size: int
  - join_time: YYYY-MM-DD HH:MM:SS timestamp
  - status: e.g. Active, Seated, Cancelled
- Description: Stores current waitlist and status.
- Example rows:
```
1|john_diner|2|2024-11-22 18:30:00|Active
2|jane_food|4|2024-11-22 18:45:00|Active
```

### 5. reviews.txt
- Path: data/reviews.txt
- Format: Pipe-delimited
- Fields: review_id | username | dish_id | rating | review_text | review_date
  - review_id: int unique review identifier
  - username: user who wrote the review
  - dish_id: int menu dish id
  - rating: int 1 to 5
  - review_text: text content
  - review_date: YYYY-MM-DD
- Description: Stores all dish reviews by users.
- Example rows:
```
1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
```

---

This design specification enables backend and frontend developers to work independently and in parallel to implement the complete RestaurantReservation application with no ambiguity or missing details.
