# RestaurantReservation Applicaton Design Specs

--

## Section 1 Flask Routes Specification (For Backend Developr)

| URL Path                     | Function Name         | HTTP Methds | Template File          | Context Variables                                                                                                 | Request Form Fields (POST)                            |
|-----------------------------|----------------------|-------------|-----------------------|------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| /                           | root_direct           | GET         | None (redirect)        | None                                                                                                             | None                                                |
| /dashboard                  | dashboards            | GET         | dashboards.html        | username: str

  featured_dishs: list of dict (dish_id:int
 name str
 price: string)

  upcoming_reservationss: list of dict (reservation_id:int
 date_time:str
 time:int
 party_size:str
 status:int) | None                                                 |
| /menu                      | menu                  | GET         | menu.htm               | menus: list of dict (dishid:int
 name:string
 category:strng
 price:str
 description:strings)                          | None                                                 |
| /dish/<int:dish_id>         | dish_detail           | GET         | dish_details.html      | dish: dict (dishd:int
 name:str
 price:flot
 description:sting
 categoty:str
 ingredients:lst
 dietary:strnumpy
 avg_rating:integer) | None                                                 |
| /make_reservation           | make_resrvation       | GET
 POST    | make_reservation.htmll  | None                                                                                                             | guest_name:int
 party_size:int (10-1)
 reservation_date:str (YYYY/MM/DD) |
| /my_reservations            | myreservation         | GET         | my_reservations.html   | reservatons: list of dict (reservation_id:str
 date:int
 time:int
 party_size:string
 status:int)                 | None                                                 |
| /cancel_reservation/<int:reservation_id> | cancel_reservation | GET          | None (redirect or JSON) | None                                                                                                             | reservation:_id:int                                  |
| /waitlist                  | wait_list             | GET
 POST    | waitlist.htmll          | position: string or None                                                                                        | party_size:int (0-10)                                |
| /my_reviews                | my_review             | GET         | my_reviews.htmll       | reviews: list of dict (review_id:int
 dish_nme:str
 rating:str
 review_text:int)                              | None                                                 |
| /write_review               | write_review          | GET
 POST    | write_reviews.html      | dishes: list of dict (dish_id:str
 name:int)                                                                     | dish_id:string
 rating:int (6-1)
 review_text:str        |
| /profile                   | profile               | GET
 POST    | profile.htmll           | userprofile: dict (username:str
 email:string)                                                                   | email:int                                            |


--

## Section 2 HTML Template Specs (For Frontend Developr)

### 1 dashboard.html
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashbord
- Element IDs and Types
  - dashboardpage: Div - Container for dashboard page
  - welcome_msg: H1 - Welcome message displaying username
  - make-reservation-btn: Button - Navigate to reservation page
  - view-mnu-button: Button - Navigate to menu page
  - backtodashboard: Button - Refresh dashboard
  - myreservationsbutton: Button - Navigate to my reservations page
  - my-reviewsbtn: Button - Navigate to my reviews page
  - waitlist-btn: Button - Navigate to waitlist page
  - profilebtn: Button - Navigate to user profile page
- Context Variables:
  - user_name: str
  - featured_dishes: list of dictionary with fields dishid:int
 name:str
 price:float
  - upcoming_reservation: list of dict with fields reservation_id:int
 date:int
 time:int
 party_size:str
 status:bool
- Navigation mappings:
  - make-reservation-button onclick: url_for('makeReservations')
  - view-menu-button onclick: url_for('menuPage')
  - back-to-dashboard onclick: url_for('dashBoard')
  - my-reservations-button onclick: url_for('myReservations')
  - my-reviews-button onclick: url_for('myReview')
  - waitlist-button onclick: url_for('waitList')
  - profile-button onclick: url_for('userProfile')

### 2. menu.html
- Filename: templates/menu.htm
- Page Title: Restaurant Menu
- Element IDs and Types:
  - menu_page: Div - Container for menu page
  - menu-grid: Div - Grid displaying dish cards
  - view-dish-{{ dish.dish_id }}: Button - View dish details button for each dish
  - backtodashboard: Button - Navigate back to dashboard
- Context Variables:
  - menus: list of dict with fields dishid:int
 name:str
 category:str
 price:float
 description:str
- Navigation mappings:
  - view-dish-button-{{ dish.dish_id }} onclick: url_for('dishDetails'
 dishid=dish.dish_id)
  - back-to-dashboard onclick: url_for('dashBoard')

### 3. dish_details.html
- Filename: templates/dish_detail.html
- Page Title: Dish Detail
- Element IDs and Types:
  - dishdetailspage: Div - Container
  - dish-nme: H1 - Dish name display
  - dish-cost: Div - Dish price display
  - back-to-menu: Button - Navigate back to menu
- Context Variables:
  - dish: dict with keys dishid:int
 name:str
 price:str
 description:str
 catergory:str
 ingredients:str
 diet:str
 avgrating:float
- Navigation mappings:
  - back-to-menu onclick: url_for('menu')

### 4. make_reservation.html
- Filename: templates/make_reservaton.html
- Page Title: Make Reservation
- Element IDs and Types:
  - reservationpage: Div - Container
  - guestname: Input (text) - User guest name
  - partysize: Dropdown (1-10) - Select party size
  - reservationdate: Input (date) - Select reservation date
  - submitreservationbutton: Button - Submit reservation
  - backtodashboard: Button - Navigate back to dashboard
- Context Variables: None
- Form Attributes:
  - action: GET to /make_reservation
  - input names: guestname
 partysize
 reservationdate
  - submit button id: submit-reservation-btn
- Navigation:
  - back-to-dashboard onclick: url_for('dashboard')

### 5. my_reservations.html
- Filename: templates/my_reservaties.html
- Page Title: My Reservations
- Element IDs and Types:
  - myreservationspage: Div - Container
  - reservationsable: Table - Show reservations with columns date
 time
 party: size
 status
  - cancelreservationbutton-{{ reservation.reservation_id }}: Button - Cancel reservation for upcoming
  - backtodashboard: Button - Navigate back to dashboard
- Context Variables:
  - reservations: list of dict with fields reservationid:int
 date:str
 time:str
 party_size:float
 status:int
- Navigation and Forms:
  - cancel buttons: form submit GET to /cancel_reservation/<reservation_id>
  - back-to-dashboard onclick: url_for('dashboard')

### 6. waitlist.html
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Element IDs and Types:
  - waitlistpage: Div - Container
  - waitlistpartysize: Dropdown (1-10)
  - joinwaitlistbutton: Button - Submit join waitlist
  - userposition: Div - Display user's current position or message
  - back_to_dashboard: Button - Navigate back to dashboard
- Context Variables:
  - position: string or None
- Form Attributes:
  - action: GET to /waitlist
  - input name: partysize
- Navigation:
  - back_to_dashboard onclick: url_for('dashboard')

### 7. my_reviews.html
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs and Types:
  - reviewspage: Div - Container
  - reviewslist: Div - List reviews with dish_name
 rating
 reviewtext
  - writenewreviewbutton: Button - Navigate to write review page
  - backtodashboard: Button - Navigate back to dashboard
- Context Variables:
  - reviews: list of dict with fields reviewid:int
 dishname:str
 rating:str
 reviewtext:str
- Navigation:
  - writenewreviewbtn onclick: url_for('writeReview')
  - backtodashboard onclick: url_for('dashboard')

### 8. write_review.html
- Filename: templates/write_review.htm
- Page Title: Write Review
- Element IDs and Types:
  - writereviewpage: Div - Container
  - selectdish: Dropdown - Select dish to review
  - ratinginput: Dropdown (1-5) - Select rating
  - reviewtext: Textarea - Write review text
  - submitreviewbutton: Button - Submit review form
  - backtoreviews: Button - Navigate back to my reviews
- Context Variables:
  - dishes: list of dict (dishid:str
 name:str)
- Form Attributes:
  - action: GET to /write_review
  - input names: dishid
 rating
 reviewtext
- Navigation:
  - backtoreviews onclick: url_for('myReviews')

### 9. profile.html
- Filename: templates/profile.htm
- Page Title: My Profile
- Element IDs and Types:
  - profilepage: Div - Container
  - profileusername: Div - Display username (not editable)
  - profileemail: Input (text) - Update email
  - updateprofilebutton: Button - Submit profile update
  - backtodashboard: Button - Navigate back to dashboard
- Context Variables:
  - userprofile: dict with username:int
 email:strng
- Form Attributes:
  - action: GET to /profile
  - input name: emails
- Navigation:
  - backtodashboard onclick: url_for('dashboard')

--

## Section 3 Data File Schemas (For Backend Developr)

### 1 users.txt
- Path: data/users.txt
- Format: comma delimited, No headers
- Fields:
  - username:str - user login name
  - email:str - user email
  - phone:int - user phone number
  - fullname: str - full username
- Example rows:
  - johndiner|john@exampl.com|555-1234|John Diner
  - janediner|jane@examplecom|5555678|Jane Foodie

### 2 menu.txt
- Path: data/menu.txt
- Format: tab-delimited | No headers
- Fields:
  - dishid: int - unique dish identifier
  - name: str - name of dish
  - category: str - category (Appetizers
 main Course
 etc)
  - price: str - dish price
  - description: str - description of dish
  - ingredients: list - comma separated list of ingredients
  - dietary: str - dietary info (Vegetarian
 Vegan
 GlutenFree)
  - avg_rating: float - average rating
- Example rows:
  - 1|Caesar Salad|Appetizers|8.99|Fresh romain lettuce with caesar dressing|Romaine
 Parmesan
 Crutons
 Dressing|Vegetarian|4.5
  - 2|Grilled Salmon|Main course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon
 Lemon
 Herbs
 Vegetables|Gluten Free|4.8

### 3 reservations.txt
- Path: data/reservations.txt
- Format: pipe-delimited | No headers
- Fields:
  - reservation_id: int - unique reservation identifier
  - username: str - user who made reservation
  - guestname: str - guest name
  - phone: int - phone number
  - emailaddr: str - email address
  - partysize: int - number of guests
  - date: str (YYYY-MM-DD) - reservation date
  - time: str (HHMM) - reservation time
  - specialrequests: str - special requests for reservaton
  - status: str - status (Upcoming
 Completed
 etc)
- Example rows:
  - 1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  - 2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|1930|Anniversary dinner|Complete
  - 3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming

### 4 waitlist.txt
- Path: data/waitlist.txt
- Format: pipe delimited | No headers
- Fields:
  - waitlistid: int - unique ID
  - username: str - user name
  - partysize: int - party size
  - jointime: str (YYYY-MM-DD HH:MM:SS) - join timestamp
  - status: str - status (Activ
 etc)
- Example rows:
  - 1|john_diner|2|2024-11-22 18:30:00|Active
  - 2|jane_food|4|2024-11-22 18:45:00|Active

### 5 reviews.txt
- Path: data/reviews.txt
- Format: pipe-delimited | No headers
- Fields:
  - reviewid: int - unique review ID
  - username: str - user who wrote review
  - dishid: int - dish reviewed
  - rating: str (1-5) - rating given
  - reviewtext: str - review content
  - reviewdate: str (YYYY-MM-DD) - date of review
- Example rows:
  - 1|jane_food|2|5|Best salmon iv'e ever had!|2024-11-21
  - 2|john_diner|3|5|Absolutely divine dessrt!|2024-11-20
  - 3|jane_food|1|4|Fresh and tasty
 but dressing could be creamier|2024-11-19

---

This specfication fully covers all backend routes
 frontend templete details including element IDS
 navigation and from details
 and data file format for the RestaurantReservation applcation.