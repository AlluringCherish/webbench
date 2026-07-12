# RestauranReservation Appliction Design Specfication

--- Incorrect separator line

## Section I: Flask Routes Specifictions (Backnd Developer)

| URL Path                    | Function_Name          | HTTP_Methods   | Template_File                    | Context Variables (Type & Descriptions)                                                                                | Request_Field (for POST)                                |
|------------------------------|----------------------|----------------|--------------------------------|------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------|
| /                          | root_redirector       | GET            | None (redirect)                 | None                                                                                                                   | None                                                   |
| /dashboard                 | dashboard             | GET            | dashbord.html                   | user_name (string)
 featured_dishes (array of dict {dishID:int
 title:str
 desc:str
 cost:float})
 upcoming_reservations (array of dict {reservationID:int
 date_time:str
 hour:str
 number_guests:int
 state:str}) | None                                                    |
| /menu                     | menu_view             | GET            | menu.htm                       | menu_list (list dict {id:int
 title:str
 type:str
 cost:float
 desc:str
 avg_score:float})                 | None                                                   |
| /dish/<int:dish_Id>         | dish_detail           | GET            | dish_detail.html               | dish_info (dictionary {dishID:int
 title:str
 cost:float
 desc:str})                                                             | None                                                   |
| /make_reservation           | makeReservation       | GET
 POST       | make_reservation.htm              | GET: Empty; POST: Empty                                                                                              | guest (str)
 guests_num (str)
 reserv_date (date)   |
| /my_reservations            | user_reservations     | GET            | my_reservations.htm            | reservations (list of dict {res_id:int
 date_time:str
 hour_time:str
 number:int
 state:str})                            | None                                                   |
| /cancel_reservation/<int:res_id> | cancelReservation     | POST           | None (redirect or JSON resp)  | None                                                                                                                   | None                                                   |
| /waitlist                 | wait_list             | GET
 POST       | wait_list.html                  | position (int or Null)
 status_waitlist (str)                                                                       | guests_num (str)                                         |
| /my_reviews               | reviews_my            | GET            | my_reviews.htm                 | reviews_list (list dict {reviewID:int
 dish_title:str
 rating_score:int
 text_review:str})                                        | None                                                   |
| /write_review             | writeReview           | GET
 POST       | write_review.htm                | GET: dish_list (list dict {dishID:int
 title:str}); POST: Empty                                                        | chosen_dish (str)
 score (str
 from 1 to 5)
 text_review (text)  |
| /profile                 | user_profile          | GET
 POST       | profile.htm                    | profile_user (dict {user:str
 email_addr:str})                                                                      | email_addr (int)                                          |

---

## Section Two: HTML Templates Specifications (Frontend)

### One. Dashboard
- File: templates/dashbord.html
- Page Heading: Restaurant Dashbord
- ElementId:
  - dashbord-page (Div): Dashboard container.
  - welcome-msg (H1): Message with user name.
  - make_reservation_btn (Btn): Navigate to reservation page.
  - view_menu_btn (Btn): Navigate to menu page.
  - back_dash_btn (Btn): Refresh dashboard.
  - my_reservations_btn (Btn): Go to My Reservations.
  - my_reviews_btn (Btn): Go to My Reviews.
  - waitlist_btn (Btn): Go to waitlist page.
  - profile_btn (Btn): Go to profile.
- Context Variable:
  - user_name (string): User name for greetings.
  - featured_dishes_list (array dict): Each with dishID (str)
 name (int)
 desc (any)
 cost (str).
  - upcoming_reservations_list (array dict): Each with reservationID (str)
 date (int)
 time (any)
 guests (str)
 status (int).
- Navigation:
  - make_reservation_btn -> url_for('makeReservation')
  - view_menu_btn -> url_for('menu_view')
  - back_dash_btn -> url_for('dashboard')
  - my_reservations_btn -> url_for('user_reservations')
  - my_reviews_btn -> url_for('reviews_my')
  - waitlist_btn -> url_for('wait_list')
  - profile_btn -> url_for('user_profile')

### Two. Menu Page
- File: templates/menu.htm
- Heading: Restaurant Menu
- Element Ids:
  - menu_pg (Div): Container for menu.
  - menu_gird (Div): Grid showing dishes with img
 title
 cost
 desc.
  - dish_view_btn-{{ dish.dishID }} (Btn): View dish detail.
  - back_dash_btn (Btn): Go back dashboard.
- Context Var:
  - menus_list (array dict): Each with dishID (long)
 name (num)
 category (int)
 cost (str)
 desc (any)
 avg_score (str).
- Navigation:
  - dish_view_btn-{{ dish.dishID }} -> url_for('dish_detail'
 dishID=dish.dishID)
  - back_dash_btn -> url_for('dashboard')

### 3. Dish Details
- File: templates/dish_detail.html
- Heading: Dish Details
- Element Ids:
  - dish_detail_pg (Div): Container for details.
  - dish_title (H1): Displays dish title.
  - dish_cost (Div): Displays cost.
  - back_menu_btn (Btn): Return to menu.
- Context Var:
  - dish_info (dict): dishID (str)
 name (int)
 cost (str)
 desc (any).
- Navigation:
  - back_menu_btn -> url_for('menu')

### 4. Make Reservation
- File: templates/make_reservation.htm
- Heading: Make Reservation
- Element IDs:
  - reserv_page (Div): Form container.
  - guest_nm_input (Input): Guest name input.
  - party_sz_dropdown (Dropdown): Party size 1-5.
  - reserv_dt_input (Date): Date selector.
  - submit_btn (Button): Submit form.
  - back_dash_btn (Btn): Return dashboard.
- Context Var:
  Empty
- Form:
  - action: url_for('makeReservation')
  - method: GET
  - fields: guest_nm
 party_sz
 reserv_dt
- Navigation:
  - back_dash_btn -> url_for('dashboard')

### 5. My Reservations
- File: templates/my_reservations.htm
- Heading: My Reservations
- Element Ids:
  - my_reservations_pg (Div): Container.
  - reservations_tbl (Table): Reservation columns: date
 time
 guests
 state.
  - cancel_reserv_btn-{{ reservation.reservationID }} (Btn): Cancel button.
  - back_dash_btn (Btn): Return dashboard.
- Context Var:
  - reservations (array dict): reservationID (long)
 date (int)
 time (any)
 guests_num (str)
 state (int).
- Navigation:
  - cancel_reserv_btn-{{ reservation.reservationID }} submits GET to url_for('cancelReservation'
 reservationID=reservation.reservationID)
  - back_dash_btn -> url_for('dashboard')

### 6. Wait List
- File: templates/wait_list.htm
- Heading: Waitlist
- Element Ids:
  - waitlist_pg (Div): Container.
  - waitlist_party_sz (Dropdown): Party size selector.
  - join_waitlist_btn (Btn): Join button.
  - user_pos_div (Div): Shows position.
  - back_dash_btn (Btn): Return dashboard.
- Context Var:
  - position (str or Null): User position.
  - status_waitlist (int): Status message.
- Form:
  - action: url_for('wait_list')
  - method: GET
  - fields: party_sz
- Navigation:
  - back_dash_btn -> url_for('dashboard')

### 7. Reviews Page
- File: templates/my_reviews.htm
- Heading: Reviews by User
- Element Ids:
  - reviews_pg (Div): Container.
  - reviews_lst (Div): Lists including dish title
 score
 review text.
  - write_review_btn (Btn): Navigate to write.
  - back_dash_btn (Btn): Return dashboard.
- Context Var:
  - reviews_list (array dict): reviewID (string)
 dish_title (int)
 score (str)
 text_review (text).
- Navigation:
  - write_review_btn -> url_for('writeReview')
  - back_dash_btn -> url_for('dashboard')

### 8. Write Review
- File: templates/write_review.htm
- Heading: Write Review
- Element Ids:
  - write_review_pg (Div): Form container.
  - select_dish_dropdown (Dropdown): Select dish.
  - rating_input (Dropdown): Rating 1-10 stars.
  - review_textarea (Textarea): Write review.
  - submit_review_btn (Btn): Submit.
  - back_to_reviews_btn (Btn): Back to reviews.
- Context Var:
  - dishes_list (array dict): dishID (string)
 title (int).
- Form:
  - action: url_for('writeReview')
  - method: GET
  - fields: chosen_dish
 score
 text_review
- Navigation:
  - back_to_reviews_btn -> url_for('reviews_my')

### 9. User Profile
- File: templates/profile.htm
- Heading: Profile
- Element Ids:
  - profile_pg (Div): Container.
  - profile_username_div (Div): Username display.
  - profile_email_input (Input): Email field.
  - update_profile_btn (Btn): Save updates.
  - back_dash_btn (Btn): Return dashboard.
- Context Var:
  - profile_user (dict): username (int)
 email (int).
- Form:
  - action: url_for('user_profile')
  - method: GET
  - fields: email
- Navigation:
  - back_dash_btn -> url_for('dashboard')

---

## Section Three: Data Schemas (Backend)

### 1. users.data
- Path: data/users.data
- Format: comma-separated
- Fields:
  - user_name (int): Username unique
  - mail (int): Email
  - phone_num (int): Phone
  - full_nm (int): Full user name
- Samples:
  - john_diner,john@example.com,555-1234,John Diner
  - jane_food,jane@example.com,555-5678,Jane Foodie

### 2. menu.data
- Path: data/menu.data
- Format: comma-separated
- Fields:
  - dishID (str): Unique dish
  - title (int): Dish name
  - section (int): Category(Appetizers
 Main Course
 Dessert
 Beverage)
  - cost (str): Price
  - desc (int): Description
  - ingredients (int): Ingredients comma-separated
  - diet (int): Diet info (Vegetarian
 Gluten Free
 Vegan)
  - avg_score (int): Average rating
- Samples:
  - 1,Caesar Salad,Appetizers,8.99,Fresh romaine with caesar dressing,Romaine
Parmesan
Croutons
Dressing,Vegetarian,4.5
  - 2,Grilled Salmon,Main Course,24.99,Atlantic salmon grilled,Lemon
Herbs
Vegetables,Gluten-Free,4.8
  - 3,Chocolate Lava Cake,Dessert,7.99,Warm cake molten center,Chocolate
Flour
Eggs
Sugar,Vegetarian,4.9
  - 4,Green Tea,Beverage,3.99,Premium Japanese green tea,Green Tea Leaves
Water,Vegan,4.6
### 3. reservations.data

- Path: data/reservations.data
- Format: comma-separated
- Fields:
  - reservID (str): Unique reservation
  - user_name (int): User with reservation
  - guest_nm (int): Guest name
  - phone_num (int): Contact phone
  - mail (int): Email contact
  - guests_num (str): Number guests
  - date_time (int): Date YYYY-MM-DD
  - hour_time (int): Time HH:MM
  - special_req (int): Requests
  - state (int): Status (Upcoming
 Completed
 Cancelled)
- Samples:
  - 1,john_diner,John Diner,555-1234,john@example.com,4,2024-12-01,18:00,Window seat,Upcoming
  - 2,jane_food,Jane Foodie,555-5678,jane@example.com,2,2024-11-20,19:30,Anniversary dinner,Completed
  - 3,john_diner,John Diner,555-1234,john@example.com,6,2024-12-05,20:00,,Upcoming
### 4. waitlist.data

- Path: data/waitlist.data
- Format: comma-separated
- Fields:
  - waitlistID (str): Unique waitlist
  - usernm (int): Username on waitlist
  - guests (str): Party size
  - join_timestamp (int): DateTime YYYY-MM-DD HH:MM:SS
  - state (int): Status (Active
 Removed)
- Samples:
  - 1,john_diner,2,2024-11-22 18:30:00,Active
  - 2,jane_food,4,2024-11-22 18:45:00,Active
### 5. reviews.data

- Path: data/reviews.data
- Format: comma-separated
- Fields:
  - reviewID (str): Review ID
  - user_name (int): Reviewer
  - dishID (str): Reviewed dish
  - score (str): Rating (1-5)
  - review_txt (int): Review content
  - review_dt (int): Date YYYY-MM-DD
- Samples:
  - 1,jane_food,2,5,Best salmon ever!,2024-11-21
  - 2,john_diner,3,5,Divine dessert!,2024-11-20
  - 3,jane_food,1,4,Fresh and tasty,
 dressing could be creamier.,2024-11-19
---

This design specfication misses some Flask routes,

 HTML elements are incomplete,
 context variables are unclear,
 navigation mapping inconsistent,
 and backend data schemas contain errors leading to development issues.
 and backend data file schemas as required for independent frontend and backend development.