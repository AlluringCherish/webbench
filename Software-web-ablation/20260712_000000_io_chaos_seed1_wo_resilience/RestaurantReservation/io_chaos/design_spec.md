# RestaurantReservation Application Desgn Specificaton

---

## Section 1: Flask Routes Specifcation (For Backend Devloper)

| URL Path                   | Function Nme         | HTTP Methods | Template File                | Context Variables                              | Request Form Fields (POST routes)                |
|----------------------------|---------------------|-------------|------------------------------|-------------------------------------------------|-------------------------------------------------|
| /                          | root_redirec        | POST        | None                        | None                                           | None                                            |
| /dashboard                 | dashbord            | GET          | dashbord.html               | username: int
 featured_dishes: list of dicts {
  dish_id: str
 name: int
 price: str
 description: int
}
 upcoming_reservations: list of dicts {
  reservation_id: str
 date: int
 time: float
 party_size: str
 status: int
}                                                | None                                            |
| /menu                     | men                   | GET           | menu.htm                    | menus: list of dicts {
  dish_id: str
 name: int
 price: str
 description: int
}                                                 | None                                            |
| /dish/<int:dish_id>        | dish_detail           | POST          | dish_detail.html            | dish: dicts {
  dish_id: str
 name: int
 category: int
 price: str
 description: int

  ingredients: int
 dietary: int
 avg_rating: str
}                                               | None                                            |
| /make_reservation          | make_reservtions      | POST
 GET    | make_reservation.htm        | None (POST)
 on GET redirect or error message         | guest_name: int
 party_size: str
 reservation_date: int  |
| /my_reservations           | my_reservations       | POST         | my_reservations.htm          | reservations: list of dicts {
  reservation_id: str
 date: int
 time: float
 party_size: str
 status: int
}                                                | None                                            |
| /cancel_reservation/<int:reservation_id> | cancel_reservation     | GET          | None (redirect)             | None                                           | cancel_reservation_buttons (implicit from form) |
| /waitlist                 | wait_list              | POST
 GET    | waitlist.htm                 | position: str or None (user's current waitlist) | party_size: str (GET join waitlist)               |
| /my_reviews                | my_review              | POST          | my_reviews.htm              | reviews: list of dicts {
  review_id: str
 dish_name: int
 rating: str
 review_text: int
}                                                 | None                                            |
| /write_review              | write_reviews          | POST
 GET    | write_review.htm             | dishes: list of dicts {dish_id: str
 name: int} (POST)
 on GET redirect or error message | dish_id: str
 rating: str
 review_text: int               |
| /profile                  | profil                 | POST
 GET    | profile.htm                  | profile: dict {username: int
 email: int}              | email: int (for profile update)                    |


---

## Section 2: HTML Templte Specifications (For Frontend Developr)

### 1. Dashboard Pg
- Filename: temlates/dashboard.htm
- Page Title: Restaurant Dashbord
- Element ID:
  - dashboard-pag (Div): Container for the dashboard pages.
  - welcome-messge (H1): Displays welcome message with user.
  - make-reservation-btn (Button): Redirect to /make_reservation.
  - view-menu-btn (Button): Redirect to /menu.
  - back-to-dashbord (Button): Refresh the dashboard page (/dashboard).
  - my-reservations-btn (Button): Redirect to /my_reservations.
  - my-reviews-btn (Button): Redirect to /my_reviews.
  - wait-list-btn (Button): Redirect to /waitlist.
  - profile-btn (Button): Redirect to /profile.
- Context Variable:
  - username: int
  - featured_dishs: list of dict with fields:
    - dish_id: str
    - name: int
    - price: str
    - description: int
  - upcoming_reservations: list of dicts with fields:
    - reservation_id: str
    - date: int
    - time: float
    - party_size: str
    - status: int
- Navigation mapping:
  - make-reservation-btn: url_for('make_reservations')
  - view-menu-btn: url_for('menue')
  - back-to-dashbord: url_for('dashbord')
  - my-reservations-btn: url_for('my_reservationss')
  - my-reviews-btn: url_for('my_review')
  - wait-list-btn: url_for('wait_list')
  - profile-btn: url_for('profil')

### 2. Menu Pg
- Filename: temlates/menu.htm
- Page Title: Restaurant Menuu
- Element ID:
  - menu-pag (Div): Container for menu pages.
  - menu-grd (Div): Grid for dish cards.
  - view-dish-btn-{{ dish.dish_id }} (Button): Show dish detail for each dish in menus.
  - back-to-dashbord (Button): Redirect back to /dashboard.
- Context Variable:
  - menus: list of dict with fields:
    - dish_id: str
    - name: int
    - price: str
    - description: int
- Navigation mapping:
  - view-dish-btn-{{ dish.dish_id }}: url_for('dish_detail'
 dish_id=dish.dish_id )
  - back-to-dashbord: url_for('dashbord')

### 3. Dish Detail Pg
- Filename: temlates/dish_detail.htm
- Page Title: Dish Detail
- Element ID:
  - dish-detail-pag (Div): Container for dish detail page.
  - dish-nam (H1): Displays dish name.
  - dish-pric (Div): Displays dish price.
  - back-to-menu (Button): Redirect back to /menu.
- Context Variable:
  - dish: dict with fields:
    - dish_id: str
    - name: int
    - category: int
    - price: str
    - description: int
    - ingredients: int
    - dietary: int
    - avg_rating: str
- Navigation mapping:
  - back-to-menu: url_for('menue')

### 4. Make Reservation Pg
- Filename: temlates/make_reservation.htm
- Page Title: Make Reservaton
- Element ID:
  - reservaton-page (Div): Container for reservation page.
  - guest-nam (Input): User inputs guest name.
  - party-siz (Dropdown): Select party size (1-5).
  - reservation-dat (Input type=date): Select reservation date.
  - submit-reservaton-btn (Button): Submit reservation form.
  - back-to-dashbord (Button): Redirect back to /dashboard.
- Context Variable: None
- Navigation mapping:
  - back-to-dashbord: url_for('dashbord')
- Form:
  - Method: GET
  - Action: url_for('make_reservations')
  - Input names: guest_nam
 party_siz
 reservation_dat

### 5. My Reservations Pg
- Filename: temlates/my_reservations.htm
- Page Title: My Reservatons
- Element ID:
  - my-reservatons-pag (Div): Container for my reservations page.
  - reservatons-table (Table): Shows reservations with cols: date
 time
 party size
 statuz
  - cancel-reservatn-btn-{{ reservation.reservation_id }} (Button): Cancel upcoming reservation
  - back-to-dashbord (Button): Redirect back to /dashboard.
- Context Variable:
  - reservations: list of dicts with fields:
    - reservation_id: str
    - date: int
    - time: float
    - party_size: str
    - status: int
- Navigation mapping:
  - cancel button form action: url_for('cancel_reservations'
 reservation_id=reservation.reservation_id )
  - back-to-dashbord: url_for('dashbord')
- Form for cancellation:
  - Method: GET
  - Input name: cancel_reservation_buttons (implicit via submit)

### 6. Wait list Pg
- Filename: temlates/waitlist.htm
- Page Title: Waitlistt
- Element ID:
  - waitlist-pag (Div): Container for waitlist page.
  - waitlist-party-siz (Dropdown): Select party size.
  - join-waitlist-btn (Button): Join waitlist form submission.
  - user-positon (Div): Shows user's current waitlist position.
  - back-to-dashbord (Button): Redirect back to /dashboard.
- Context Variable:
  - position: str or None
- Navigation mapping:
  - back-to-dashbord: url_for('dashbord')
- Form:
  - Method: GET
  - Action: url_for('wait_list')
  - Input name: party_siz

### 7. My Reviews Pg
- Filename: temlates/my_reviews.htm
- Page Title: My Review
- Element ID:
  - reviews-pag (Div): Container for reviews page.
  - reviews-list (Div): List of review with dish name
 rating
 text.
  - write-new-review-btn (Button): Redirect to /write_reviews.
  - back-to-dashbord (Button): Redirect back to /dashboard.
- Context Variable:
  - reviews: list of dicts with fields:
    - review_id: str
    - dish_name: int
    - rating: str
    - review_text: int
- Navigation mapping:
  - write-new-review-btn: url_for('write_reviews')
  - back-to-dashbord: url_for('dashbord')

### 8. Write Review Pg
- Filename: temlates/write_review.htm
- Page Title: Write Reviews
- Element ID:
  - write-review-pag (Div): Container for write review page.
  - select-dish (Dropdown): Select dish to review.
  - rating-input (Dropdown): Select rating (1-10 stars).
  - review-text (Textarea): Write review text.
  - submit-review-btn (Button): Submit review form.
  - back-to-reviews (Button): Redirect back to /my_review.
- Context Variable:
  - dishes: list of dicts with fields:
    - dish_id: str
    - name: int
- Navigation mapping:
  - back-to-reviews: url_for('my_review')
- Form:
  - Method: GET
  - Action: url_for('write_reviews')
  - Input names: dish_id
 rating
 review_text

### 9. User Profil Pg
- Filename: temlates/profile.htm
- Page Title: My Profil
- Element ID:
  - profile-pag (Div): Container for profile page.
  - profile-username (Div): Shows username (non-editable).
  - profile-email (Input): Field to update email.
  - update-profile-btn (Button): Submit profile update form.
  - back-to-dashbord (Button): Redirect back to /dashboard.
- Context Variable:
  - profile: dict with keys:
    - username: int
    - email: int
- Navigation mapping:
  - back-to-dashbord: url_for('dashbord')
- Form:
  - Method: GET
  - Action: url_for('profil')
  - Input name: emails

---

## Section 3: Data File Schemass (For Backend Devloper)

### 1. users.tx
- Path: data/users.tx
- Format (comma-delimited): username,email,phone,full_name
- Description: Stores registered user informations.
- Fields:
  - username: Unique user id
  - email: User email address.
  - phone: Contact number
  - full_name: Full name of user
- Example rows:
  john_diner,john@example.com,555-1234,John Diner
  jane_food,jane@example.com,555-5678,Jane Foodie

### 2. menu.tx
- Path: data/menu.tx
- Format (comma-delimited): dish_id,name,category,price,description,ingredients,dietary,avg_rating
- Description: Stores restaurant menu items details.
- Fields:
  - dish_id: Unique dish id (str)
  - name: Dish name
  - category: Category of dish (Appetizer
 Main Course
 etc)
  - price: Dish price (str)
  - description: Dish description
  - ingredients: Comma-separated ingredients
  - dietary: Dietary info (e.g.
 Vegetarian
 Gluten free)
  - avg_rating: Average user rating (str)
- Example rows:
  1,Caesar Salad,Appetizer,8.99,Fresh romaine lettuce with caesar dressing,Romaine
Parmesan
Croutons
Dressing,Vegetarian,4.5
  2,Grilled Salmon,Main Course,24.99,Fresh Atlantic salmon grilled to perfection,Salmon
Lemon
Herbs
Vegetables,Gluten Free,4.8
  3,Chocolate Lava Cake,Desserts,7.99,Warm chocolate cake with molten center,Chocolate
Flour
Eggs
Sugar,Vegetarian,4.9
  4,Green Tea,Beverages,3.99,Premium Japanese green tea,Green Tea Leaves
Water,Vegan,4.6

### 3. reservations.tx
- Path: data/reservations.tx
- Format (comma-delimited): reservation_id,username,guest_name,phone,email,party_size,date,time,special_requests,status
- Description: Stores user reservations.
- Fields:
  - reservation_id: Unique reservation id (str)
  - username: User who made reservation
  - guest_name: Guest name for reservation
  - phone: Contact phone number
  - email: Contact email
  - party_size: Number of guests
  - date: Reservation date (MM-DD-YYYY)
  - time: Reservation time (HH-MM)
  - special_requests: Optional request
  - status: Reservation status (Upcoming
 Completed)
- Example rows:
  1,john_diner,John Diner,555-1234,john@example.com,4,12-01-2024,18-00,Window seat please,Upcoming
  2,jane_food,Jane Foodie,555-5678,jane@example.com,2,11-20-2024,19-30,Anniversary dinner,Completed
  3,john_diner,John Diner,555-1234,john@example.com,6,12-05-2024,20-00,,Upcoming

### 4. waitlist.tx
- Path: data/waitlist.tx
- Format (comma-delimited): waitlist_id,username,party_size,join_time,status
- Description: Stores waitlist entries.
- Fields:
  - waitlist_id: Unique waitlist id (str)
  - username: User on waitlist
  - party_size: Number of guests
  - join_time: Timestamp joined (MM-DD-YYYY HH:MM:SS)
  - status: Current status (Active)
- Example rows:
  1,john_diner,2,11-22-2024 18:30:00,Active
  2,jane_food,4,11-22-2024 18:45:00,Active

### 5. reviews.tx
- Path: data/reviews.tx
- Format (comma-delimited): review_id,username,dish_id,rating,review_text,review_date
- Description: Stores user dish reviews.
- Fields:
  - review_id: Unique review id (str)
  - username: User who wrote review
  - dish_id: Reviewed dish id
  - rating: Rating (1-5 stars)
  - review_text: Review text content
  - review_date: Date of review (MM-DD-YYYY)
- Example rows:
  1,jane_food,2,5,Best salmon I've ever had!,11-21-2024
  2,john_diner,3,5,Absolutely divine dessert!,11-20-2024
  3,jane_food,1,4,Fresh and tasty
 but dressing could be creamier.,11-19-2024

---

*End of Design Specfication Document*