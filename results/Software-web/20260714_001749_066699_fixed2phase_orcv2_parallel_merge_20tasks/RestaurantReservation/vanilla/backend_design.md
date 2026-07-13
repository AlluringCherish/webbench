# Backend Design Specification for RestaurantReservation

---

## Section 1: Flask Route Specifications

### 1. Dashboard Page
- **URL Path:** `/dashboard`
- **HTTP Methods:** GET
- **Function Name:** `dashboard()`
- **Input:** None
- **Response:** Renders `dashboard.html` template

### 2. Menu Page
- **URL Path:** `/menu`
- **HTTP Methods:** GET
- **Function Name:** `menu()`
- **Input:** Optional query parameters for category or filtering (e.g., `category`, `search`)
- **Response:** Renders `menu.html` template with menu items data

### 3. Dish Details Page
- **URL Path:** `/menu/<int:dish_id>`
- **HTTP Methods:** GET
- **Function Name:** `dish_details(dish_id)`
- **Input:** URL parameter `dish_id`
- **Response:** Renders `dish_details.html` template with dish details

### 4. Make Reservation Page
- **URL Path:** `/reservation/make`
- **HTTP Methods:** GET, POST
- **Function Name:** `make_reservation()`
- **Input (GET):** None
- **Input (POST):** Form data including `guest_name`, `party_size`, `reservation_date` (and user identity via session or authentication)
- **Response:** 
  - GET: Renders `make_reservation.html` template
  - POST: Processes reservation, saves to data file, redirects to dashboard or confirmation

### 5. My Reservations Page
- **URL Path:** `/reservations/my`
- **HTTP Methods:** GET
- **Function Name:** `my_reservations()`
- **Input:** User identity (e.g., session)
- **Response:** Renders `my_reservations.html` template with user's reservation list

### 6. Cancel Reservation (Action)
- **URL Path:** `/reservations/cancel/<int:reservation_id>`
- **HTTP Methods:** POST
- **Function Name:** `cancel_reservation(reservation_id)`
- **Input:** URL parameter reservation_id, user identity
- **Response:** Updates reservation status to "Cancelled" or removes if required, then redirects or responds with status

### 7. Waitlist Page
- **URL Path:** `/waitlist`
- **HTTP Methods:** GET, POST
- **Function Name:** `waitlist()`
- **Input (GET):** None
- **Input (POST):** Form data including `party_size` and user identity
- **Response:** 
  - GET: Renders `waitlist.html` with current user waitlist position if any
  - POST: Adds user to waitlist, updates file, redirects or shows position

### 8. My Reviews Page
- **URL Path:** `/reviews/my`
- **HTTP Methods:** GET
- **Function Name:** `my_reviews()`
- **Input:** User identity
- **Response:** Renders `my_reviews.html` with user's reviews

### 9. Write Review Page
- **URL Path:** `/reviews/write`
- **HTTP Methods:** GET, POST
- **Function Name:** `write_review()`
- **Input (GET):** None
- **Input (POST):** Form data including `dish_id`, `rating`, `review_text`
- **Response:** 
  - GET: Renders `write_review.html` with dishes list for selection
  - POST: Saves review, updates files, redirects to my reviews

### 10. User Profile Page
- **URL Path:** `/profile`
- **HTTP Methods:** GET, POST
- **Function Name:** `profile()`
- **Input (GET):** User identity
- **Input (POST):** Form data including `email`
- **Response:** 
  - GET: Renders `profile.html` with user details
  - POST: Updates user profile data in file, confirms update

---

## Section 2: Data File Schemas and Handling

All data files are stored in directory: `data/`

---

### 1. users.txt
- **Schema:**
  - Fields: `username|email|phone|full_name`
- **Example Row:**
  - `john_diner|john@example.com|555-1234|John Diner`
- **Operations:**
  - Read: load all users or find by username
  - Update: modify existing user email or phone by username
  - Write: add new user (append)
  - Delete: remove user by username (if needed)
- **Concurrency:** Single user app assumed, simple file lock if needed during write

---

### 2. menu.txt
- **Schema:**
  - Fields: `dish_id|name|category|price|description|ingredients|dietary|avg_rating`
  - Types: `dish_id` int, `price` float, `avg_rating` float
- **Example Row:**
  - `1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5`
- **Operations:**
  - Read: load all menu items or by dish_id
  - Write: (rare) update or add dish if admin functionality added
- **Concurrency:** Read mostly; writes controlled to prevent conflicts

---

### 3. reservations.txt
- **Schema:**
  - Fields: `reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status`
  - Types: `reservation_id` int, `party_size` int, `date` `YYYY-MM-DD`, `time` `HH:MM` 24h, `status` e.g. Upcoming, Completed, Cancelled
- **Example Row:**
  - `1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming`
- **Operations:**
  - Create: add new reservation with unique incremented reservation_id
  - Read: filter by username or reservation_id
  - Update: change status (e.g., cancel), modify details
  - Delete: typically mark status Cancelled, not remove to keep history
- **Concurrency:** File lock or transaction needed during write/update

---

### 4. waitlist.txt
- **Schema:**
  - Fields: `waitlist_id|username|party_size|join_time|status`
  - Types: `waitlist_id` int, `party_size` int, `join_time` datetime string `YYYY-MM-DD HH:MM:SS`, `status` e.g. Active
- **Example Row:**
  - `1|john_diner|2|2024-11-22 18:30:00|Active`
- **Operations:**
  - Add user to waitlist with incremented waitlist_id
  - Read: get all active waitlist users, filter by username to find position
  - Update: change status (e.g., removed from waitlist)
  - Delete: remove from list when seated or cancelled
- **Concurrency:** Require file lock during write/update

---

### 5. reviews.txt
- **Schema:**
  - Fields: `review_id|username|dish_id|rating|review_text|review_date`
  - Types: `review_id` int, `dish_id` int, `rating` int 1-5, `review_date` `YYYY-MM-DD`
- **Example Row:**
  - `1|jane_food|2|5|Best salmon I've ever had!|2024-11-21`
- **Operations:**
  - Add new review with incremented review_id
  - Read reviews by username, dish_id
  - Update or delete reviews typically not required but can be implemented if needed
- **Concurrency:** File lock required during write

---

## File Handling Instructions

- All read operations load entire file into memory, parse lines by `|` delimiter into objects/dictionaries.
- Writes for adding new entries open file in append mode.
- For update or delete operations, read entire file, modify in-memory, then overwrite file contents.
- To ensure consistency, implement file locking during write/update to prevent race conditions.

---

This specification enables backend developers to implement all RESTful routes and file-based data interactions for the RestaurantReservation app based on the described requirements, independent of frontend layouts or UI code.
