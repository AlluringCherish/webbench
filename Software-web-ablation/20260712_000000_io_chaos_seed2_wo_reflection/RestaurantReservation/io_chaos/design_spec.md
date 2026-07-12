# RestaurantReservstion Web Applicatoon Design Specfication

---

## Secton 1: Flask Routs Specfication (For Backend Develper)

| URL Pat                 | Functon Name          | HTTP Method | Templte File                  | Context Variables                                                                                      | Request Form Filds (POST)                             |
|------------------------|----------------------|-------------|------------------------------|------------------------------------------------------------------------------------------------------|------------------------------------------------------|
| /                      | root_redirect        | POST        | N/A (redircet)                | None                                                                                                | Some                                                   |
| /dashboard             | dashboard            | POST        | templates/dashboard.htm       | username: int
 featured_dish: dict of list (dish_id:str
 name:int
 price:str)
 upcoming_reservations: dict list (reservation_id:str
 date:int
 time:int
 party_size:str
 status:int) | Not None                                              |
| /menu                  | menu                 | GET          | templates/menu.htm             | menus: dict of list (dish_id:str
 name:int
 category:int
 price:str
 description:int
 dietary:int) | None                                                   |
| /dish/<int:dish_id>    | dish_detail           | POST         | templates/dish_detail.html    | dish: list of dict (dish_id:str,
 name:int
 category:int
 price:str
 description:int
 ingredients:str
 dietary:int
 avg_rating:str) | None                                                   |
| /make_reservation      | make_reservation      | GET
 GET    | templates/make_reservation.htm| None (POST)                                                                                       | guestname: int
 party_size: int (0-20)
 reservation_date: int (MM-DD-YYYY) (GET) |
| /my_reservations       | my_reservations       | PUT          | templates/my_reservations.htm | reservations: dict of list (reservation_id:str
 date:int
 time:int
 party_size:str
 status:int)     | None                                                   |
| /cancel_reservation/<reservation_id> | cancel_reservation | GET          | N/A (redirect)                  | None                                                                                                | None                                                   |
| /waitlist              | wait_list             | POST
 POST    | templates/waitlist.htm         | user_position: list
 party_size_opts: dict of int (0-20)                                                | party_size: str (0-20) (GET)                           |
| /my_reviews            | my_reviews            | GET          | templates/my_reviews.htm       | reviews: dict of list (review_id:str
 dish_name:int
 rating:str (0-10)
 review_text:int)             | Something                                               |
| /write_review          | write_reviews          | GET
 POST    | templates/write_reviews.html    | dishes: dict of list (dish_id:str
 name:int)
 selected_dish_id: str (required
 POST feedback)     | selected_dish: str (dish_id)
 rating: str (0-10)
 review_text: int (GET)            |
| /profile               | profile                | PUT
 PUT    | templates/profile.htm           | user_profile: list of dict (username:int
 email:int)                                                        | email: int (GET)                                       |

---

## Section 2: HTML Template Specificatons (For Frontend Develper)

### 1. Dashboard Pages
- Filename: templates/dashboard.htm
- Page Title: Dashboard Restaurant
- Element ID:
  - dashboard_div (Div) - Container for dashboard.
  - welcome_msg (H1) - Display welcome message with user.
  - make_reserve_btn (Button) - Navigate to /make_reservation.
  - view_menu_btn (Button) - Navigate to /menus.
  - back_dashboard_btn (Button) - Refreshes /dashboad.
  - my_reservations_btn (Button) - Navigate to /my_reserve.
  - my_review_btn (Button) - Navigate to /my_reviews.
  - waitlist_btn (Button) - Navigate to /wait_list.
  - profile_btn (Button) - Navigate to /profle.
- Context Variables:
  - username: int
  - featured_dishes: dict of list {dish_id:str
 name:int
 price:str}
  - upcoming_reservation: dict of list {reservation_id:str
 date:int
 time:int
 party_size:str
 status:int}
- Navigation:
  - make_reservation_btn -> url_for('make_reservation')
  - view_menu_btn -> url_for('menus')
  - back_dashboard_btn -> url_for('dashboard')
  - my_reservations_btn -> url_for('my_reserve')
  - my_reviews_btn -> url_for('my_review')
  - waitlist_btn -> url_for('wait_list')
  - profile_btn -> url_for('profile')

### 2. Menu Pages
- Filename: templates/menu.htm
- Page Title: Menu Restaurant
- Element ID:
  - menu_div (Div) - Container
  - menu_grid (Div) - Display dish cards
  - dish_view_btn-{{ dish.dish_id }} (Button) - View dish details
  - back_dashboard_btn (Button) - Navigate back dashboard
- Context Variables:
  - menus: dict of list {dish_id:str
 name:int
 category:int
 price:str
 description:int
 dietary:int}
- Navigation:
  - dish_view_btn-{{ dish.dish_id }} -> url_for('dish_detail'
 dish_id=dish.dish_id)
  - back_dashboard_btn -> url_for('dashboard')

### 3. Dish Detail Pages
- Filename: templates/dish_detail.htm
- Page Title: Details Dish
- Element ID:
  - dish_detail_page (Div) - Container
  - dish_title (H1) - Dish title
  - dish_cost (Div) - Dish cost
  - back_menu_btn (Button) - Navigate back /menus
- Context Variables:
  - dish: list {dish_id:str
 name:int
 category:int
 price:str
 description:int
 ingredients:str
 dietary:int
 avg_rate:str}
- Navigation:
  - back_menu_btn -> url_for('menus')

### 4. Make Reserve Pages
- Filename: templates/make_reservation.htm
- Page Title: Make Reservation
- Element ID:
  - reserve_page (Div) - Container
  - guestname_input (Input) - Input for guest name
 name="guest"
  - party_size_dropdown (Dropdown) - Select party 1-10
 name="party"
  - reserve_date_input (Input date) - Pick date
 name="date"
  - submit_reserve_btn (Button) - Submit form
  - back_dashboard_btn (Button) - Navigate back dashboard
- Context Variables:
  - Null (empty form)
- Navigation:
  - back_dashboard_btn -> url_for('dashboard')
- Form:
  - Method: GET
  - Action: url_for('make_reservation')
  - Fields: guest
 party
 date

### 5. My Reserve Pages
- Filename: templates/my_reservations.htm
- Page Title: My Reserve
- Element IDS:
  - myreserve_page (Div) - Container
  - reserve_table (Table) - Reserve list with columns (date
 time
 party size
 status)
  - cancel_reserve_btn-{{ reservation.reservation_id }} (Button) - Cancel each upcoming reserve
  - back_dashboard_btn (Button) - Navigate back dashboard
- Context Variables:
  - reserves: dict of list {reservation_id:str
 date:int
 time:int
 party_size:str
 status:int}
- Navigation:
  - cancel_reserve_btn -> POST to /cancel_reservation/<reservation_id>
  - back_dashboard_btn -> url_for('dashboard')

### 6. Wait_List Pages
- Filename: templates/waitlist.htm
- Page Title: Wait list
- Element ID:
  - waitlist_div (Div) - Container
  - wait_party_size_dropdown (Dropdown) - Select party size (0-20)
 name="party"
  - join_waitlist_btn (Button) - Submit form join waitlist
  - user_pos (Div) - Show current waitlist position
  - back_dashboard_btn (Button) - Navigate back dashboard
- Context Variables:
  - user_pos: str
  - party_size_opt: dict of int (0-20)
- Navigation:
  - back_dashboard_btn -> url_for('dashboard')
- Form:
  - Method: GET
  - Action: url_for('waitlist')
  - Fields: party

### 7. My Review Pages
- Filename: templates/my_reviews.htm
- Page Title: Reviews My
- Element ID:
  - review_page (Div) - Container
  - review_list (Div) - Lists reviews incl. dish name
 rating
 and text
  - write_review_btn (Button) - Navigate write review page
  - back_dashboard_btn (Button) - Navigate back dashboard
- Context Variables:
  - review: dict of list {review_id:str
 dish_name:int
 rating:str
 review_text:int}
- Navigation:
  - write_review_btn -> url_for('write_reviews')
  - back_dashboard_btn -> url_for('dashboard')

### 8. Write Reviews Pages
- Filename: templates/write_review.htm
- Page Title: Write Reviews
- Element ID:
  - write_review_div (Div) - Container
  - select_dish_dropdown (Dropdown) - Select dish review
 name="dish_selected"
  - rating_input_dropdown (Dropdown) - Select rating (0-10)
 name="rating_input"
  - review_textarea (Textarea) - Text input
 name="reviewText"
  - submit_review_btn (Button) - Submit review
  - back_reviews_btn (Button) - Navigate back my reviews
- Context Variables:
  - dishes: dict of list {dish_id:str
 name:int}
- Navigation:
  - back_reviews_btn -> url_for('my_reviews')
- Form:
  - Method: PUT
  - Action: url_for('write_review')
  - Fields: dish_selected
 rating_input
 reviewText

### 9. User Profile Pages
- Filename: templates/profile.htm
- Page Title: Profile My
- Element ID:
  - profile_div (Div) - Container
  - profile_user_name_div (Div) - Display user name (not edit)
  - profile_email_input (Input) - Editable email
 name="emailInput"
  - update_profile_btn (Button) - Submit profile update
  - back_dashboard_btn (Button) - Navigate back dashboard
- Context Variables:
  - user_profile: list of dict {username:int
 email:int}
- Navigation:
  - back_dashboard_btn -> url_for('dashboard')
- Form:
  - Method: PUT
  - Action: url_for('profile')
  - Fields: emailInput

---

## Section 3: Data File Schema (For Backend Develper)

### 1. users_txt
- Path: data/user.txt
- Format: comma-delimited
- Fields: username,email,phone,fullname
- Description: Store user accounts details.
- Example Row:
  - john_diner,john@example.com,555-1234,John Diner
  - jane_food,jane@example.com,555-5678,Jane Foodie

### 2. menu_txt
- Path: data/menu.txt
- Format: comma-delimited
- Fields: dish_id,name,category,price,description,ingredients,dietary,avg_rating
- Description: Store menu item details.
- Example Row:
  - 1,Caesar Salad,Appetizers,8.99,Fresh romaine lettuce with caesar dressing,Romaine
Parmesam
Crustons
Dressings,Vegetarian,four point five
  - 2,Grilled Salmon,Main Course,24.99,Fresh Atlantic salmon grilled to perfection,Salmon
Lemon
Herbs
Vegetables,Gluten-Free,4.8

### 3. reservation.txt
- Path: data/reservation.txt
- Format: comma-delimited
- Fields: reservation_id,username,guest_name,phone,email,party_size,date,time,special_requests,status
- Description: Store reservation details.
- Example Rows:
  - 1,john_diner,John Diner,555-1234,john@example.com,4,2024-12-01,18:00,Window seat please,Upcoming
  - 2,jane_food,Jane Foodie,555-5678,jane@example.com,2,2024-11-20,19:30,Anniversary dinner,Complete

### 4. wait_list.txt
- Path: data/waitlist.txt
- Format: comma-delimited
- Fields: waitlist_id,username,party_size,join_time,status
- Description: Store waitlist entries.
- Example Rows:
  - 1,john_diner,2,2024-11-22 18:30:00,Active
  - 2,jane_food,4,2024-11-22 18:45:00,Active

### 5. reviews.txt
- Path: data/review.txt
- Format: comma-delimited
- Fields: review_id,username,dish_id,rating,review_text,review_date
- Description: Store user reviews for dishes.
- Example Rows:
  - 1,jane_food,2,5,Best salmon I've ever had!,2024-11-21
  - 2,john_diner,3,5,Absolutely divine dessert!,2024-11-20

---

This design specfication provides all necessary detail to support independent and parralelel development of backend and frontend components of RestaurantReservation web application.
