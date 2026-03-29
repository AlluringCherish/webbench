# RestaurantReservation Application Design Specification

---

## Section 1: Flask Routes Specification (For Backend Developer)

| URL Path                 | Function Name           | HTTP Methods | Template File                 | Context Variables (name:type)                                                                                 | Request Form Fields (POST)                                  |
|--------------------------|------------------------|--------------|------------------------------|---------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| /                        | root_redirect          | GET          | -                            | -                                                                                                             | -                                                          |
| /dashboard               | dashboard_page          | GET          | dashboard.html               | username:str, featured_dishes:list of dict {dish_id:int, name:str, price:float}, upcoming_reservations:list of dict {reservation_id:int, date:str, time:str, party_size:int} | -                                                          |
| /menu                    | menu_page               | GET          | menu.html                    | menus:list of dict {dish_id:int, name:str, category:str, price:float, description:str}                         | -                                                          |
| /dish/<int:dish_id>      | dish_details_page       | GET          | dish_details.html            | dish:dict {dish_id:int, name:str, price:float, description:str}                                               | -                                                          |
| /reservation             | make_reservation_page   | GET, POST    | make_reservation.html        | -                                                                                                             | guest_name:str, party_size:int (1-10), reservation_date:str (YYYY-MM-DD) |
| /my-reservations         | my_reservations_page    | GET          | my_reservations.html         | reservations:list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str}                | -                                                          |
| /cancel-reservation/<int:reservation_id> | cancel_reservation       | POST         | -                            | -                                                                                                             | -                                                          |
| /waitlist                | waitlist_page           | GET, POST    | waitlist.html                | user_position:int or None                                                                                      | party_size:int (1-10)                                      |
| /my-reviews              | my_reviews_page         | GET          | my_reviews.html              | reviews:list of dict {review_id:int, dish_name:str, rating:int, review_text:str}, username:str                  | -                                                          |
| /write-review            | write_review_page       | GET, POST    | write_review.html            | dishes:list of dict {dish_id:int, name:str}                                                                    | dish_id:int, rating:int (1-5), review_text:str             |
| /profile                 | profile_page            | GET, POST    | profile.html                 | username:str, email:str                                                                                         | email:str                                                  |


---

## Details:

- The root path `/` redirects to `/dashboard`, no template rendered.
- `dashboard_page` includes welcome message using `username` and lists featured dishes and upcoming reservations.
- `menu_page` lists all menu items with relevant fields.
- `dish_details_page` shows selected dish details.
- `make_reservation_page` on GET renders form, on POST handles reservation creation.
- `my_reservations_page` displays all reservations for the logged-in user.
- `cancel_reservation` POST endpoint cancels an upcoming reservation by reservation_id.
- `waitlist_page` GET shows current user position if on waitlist, POST joins waitlist.
- `my_reviews_page` lists all reviews by the user.
- `write_review_page` GET lists dishes to review, POST submits a new review.
- `profile_page` GET shows profile, POST updates email.

---

## Section 2: HTML Template Specifications (For Frontend Developer)

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Restaurant Dashboard
- Element IDs:
  - dashboard-page (Div): Container of the dashboard.
  - welcome-message (H1): Displays "Welcome, {{ username }}!"
  - make-reservation-button (Button): Navigate to make reservation page.
  - view-menu-button (Button): Navigate to menu page.
  - back-to-dashboard (Button): Refresh dashboard.
  - my-reservations-button (Button): Navigate to my reservations page.
  - my-reviews-button (Button): Navigate to my reviews page.
  - waitlist-button (Button): Navigate to waitlist page.
  - profile-button (Button): Navigate to profile page.
- Context Variables:
  - username: str
  - featured_dishes: list of dict {dish_id:int, name:str, price:float}
  - upcoming_reservations: list of dict {reservation_id:int, date:str, time:str, party_size:int}
- Navigation Mappings:
  - make-reservation-button -> url_for('make_reservation_page')
  - view-menu-button -> url_for('menu_page')
  - back-to-dashboard -> url_for('dashboard_page')
  - my-reservations-button -> url_for('my_reservations_page')
  - my-reviews-button -> url_for('my_reviews_page')
  - waitlist-button -> url_for('waitlist_page')
  - profile-button -> url_for('profile_page')

### 2. Menu Page
- Filename: templates/menu.html
- Page Title: Restaurant Menu
- Element IDs:
  - menu-page (Div): Container for menu page.
  - menu-grid (Div): Grid to display dishes.
  - view-dish-button-{{ dish.dish_id }} (Button): To view dish details for each dish.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Context Variables:
  - menus: list of dict {dish_id:int, name:str, category:str, price:float, description:str}
- Navigation Mappings:
  - view-dish-button-{{ dish.dish_id }} -> url_for('dish_details_page', dish_id=dish.dish_id)
  - back-to-dashboard -> url_for('dashboard_page')

### 3. Dish Details Page
- Filename: templates/dish_details.html
- Page Title: Dish Details
- Element IDs:
  - dish-details-page (Div): Container.
  - dish-name (H1): Displays dish.name
  - dish-price (Div): Displays dish.price
  - back-to-menu (Button): Navigate to menu page.
- Context Variables:
  - dish: dict {dish_id:int, name:str, price:float, description:str}
- Navigation Mappings:
  - back-to-menu -> url_for('menu_page')

### 4. Make Reservation Page
- Filename: templates/make_reservation.html
- Page Title: Make Reservation
- Element IDs:
  - reservation-page (Div): Container.
  - guest-name (Input): input text name='guest_name'
  - party-size (Dropdown): select name='party_size'; options 1-10
  - reservation-date (Input date): input type='date' name='reservation_date'
  - submit-reservation-button (Button): submits form
  - back-to-dashboard (Button): navigate back
- Context Variables: None
- Form:
  - method='POST' action url_for('make_reservation_page')
  - inputs: guest_name, party_size, reservation_date
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard_page')

### 5. My Reservations Page
- Filename: templates/my_reservations.html
- Page Title: My Reservations
- Element IDs:
  - my-reservations-page (Div): Container.
  - reservations-table (Table): Displays rows of reservations.
  - cancel-reservation-button-{{ reservation.reservation_id }} (Button): Cancel upcoming reservation.
  - back-to-dashboard (Button): navigate back.
- Context Variables:
  - reservations: list of dict {reservation_id:int, date:str, time:str, party_size:int, status:str}
- Form:
  - Each cancel button triggers POST to /cancel-reservation/<reservation_id>
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard_page')

### 6. Waitlist Page
- Filename: templates/waitlist.html
- Page Title: Waitlist
- Element IDs:
  - waitlist-page (Div): Container.
  - waitlist-party-size (Dropdown): select name='party_size' (1-10)
  - join-waitlist-button (Button): submit form to join waitlist
  - user-position (Div): Displays user's position or message if not on waitlist
  - back-to-dashboard (Button): navigate back
- Context Variables:
  - user_position: int or None
- Form:
  - method='POST' action url_for('waitlist_page')
  - input: party_size
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard_page')

### 7. My Reviews Page
- Filename: templates/my_reviews.html
- Page Title: My Reviews
- Element IDs:
  - reviews-page (Div): Container.
  - reviews-list (Div): List each review with dish name, rating, text.
  - write-new-review-button (Button): navigate to write review page
  - back-to-dashboard (Button): navigate back
- Context Variables:
  - reviews: list of dict {review_id:int, dish_name:str, rating:int, review_text:str}
  - username: str
- Navigation Mappings:
  - write-new-review-button -> url_for('write_review_page')
  - back-to-dashboard -> url_for('dashboard_page')

### 8. Write Review Page
- Filename: templates/write_review.html
- Page Title: Write Review
- Element IDs:
  - write-review-page (Div): Container.
  - select-dish (Dropdown): select name='dish_id'; options from dishes list
  - rating-input (Dropdown): select name='rating' options 1-5
  - review-text (Textarea): textarea name='review_text'
  - submit-review-button (Button): submit form
  - back-to-reviews (Button): navigate back to my reviews
- Context Variables:
  - dishes: list of dict {dish_id:int, name:str}
- Form:
  - method='POST' action url_for('write_review_page')
  - inputs: dish_id, rating, review_text
- Navigation Mappings:
  - back-to-reviews -> url_for('my_reviews_page')

### 9. User Profile Page
- Filename: templates/profile.html
- Page Title: My Profile
- Element IDs:
  - profile-page (Div): Container.
  - profile-username (Div): Displays username (non-editable)
  - profile-email (Input): input type='email' name='email'
  - update-profile-button (Button): submits form to update profile
  - back-to-dashboard (Button): navigate back
- Context Variables:
  - username: str
  - email: str
- Form:
  - method='POST' action url_for('profile_page')
  - input: email
- Navigation Mappings:
  - back-to-dashboard -> url_for('dashboard_page')

---

## Section 3: Data File Schemas (For Backend Developer)

### 1. users.txt
- Path: data/users.txt
- Format: pipe (`|`) delimited
- Fields: username | email | phone | full_name
- Description: Stores user account basic information
- Examples:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### 2. menu.txt
- Path: data/menu.txt
- Format: pipe (`|`) delimited
- Fields: dish_id | name | category | price | description | ingredients | dietary | avg_rating
  - dish_id: int, unique identifier
  - name: str
  - category: str (e.g., Appetizers, Main Course)
  - price: float
  - description: str
  - ingredients: str, comma separated list
  - dietary: str (e.g., Vegetarian, Gluten-Free, Vegan)
  - avg_rating: float (average rating of dish)
- Description: Stores menu items data
- Examples:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### 3. reservations.txt
- Path: data/reservations.txt
- Format: pipe (`|`) delimited
- Fields: reservation_id | username | guest_name | phone | email | party_size | date | time | special_requests | status
  - reservation_id: int, unique
  - username: str
  - guest_name: str
  - phone: str
  - email: str
  - party_size: int
  - date: str (YYYY-MM-DD)
  - time: str (HH:MM 24h format)
  - special_requests: str (optional)
  - status: str (e.g., Upcoming, Completed, Cancelled)
- Description: Stores table reservation details
- Examples:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### 4. waitlist.txt
- Path: data/waitlist.txt
- Format: pipe (`|`) delimited
- Fields: waitlist_id | username | party_size | join_time | status
  - waitlist_id: int, unique
  - username: str
  - party_size: int
  - join_time: str (YYYY-MM-DD HH:MM:SS)
  - status: str (e.g., Active, Seated, Cancelled)
- Description: Stores waitlist entries
- Examples:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### 5. reviews.txt
- Path: data/reviews.txt
- Format: pipe (`|`) delimited
- Fields: review_id | username | dish_id | rating | review_text | review_date
  - review_id: int, unique
  - username: str
  - dish_id: int
  - rating: int (1-5)
  - review_text: str
  - review_date: str (YYYY-MM-DD)
- Description: Stores user reviews of dishes
- Examples:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

---

This design specification provides full details for backend Flask route implementations, frontend HTML templates, and local data file schemas, enabling independent and parallel development by backend and frontend developers.
