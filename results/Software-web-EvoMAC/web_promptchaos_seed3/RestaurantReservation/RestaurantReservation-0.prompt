# Requirements Document for 'RestaurantReservation' Web Application

## 1. Objective
Develop a comprehensive web application named 'RestaurantReservation' using Python, with data managed through local text files. The application enables users to browse restaurant menus, make table reservations, write reviews, check waitlist status, and manage their dining history. Note that the website should start from the Dashboard page.

## 2. Language
The required development language for the 'RestaurantReservation' application is Python.

## 3. Page Design

The 'RestaurantReservation' web application will consist of the following nine pages:

### 1. Dashboard Page
- **Page Title**: Restaurant Dashboard
- **Overview**: The main hub displaying featured dishes, upcoming reservations, and navigation to other functionalities.
- **Elements**:
  - **ID: dashboard-page** - Type: Div - Container for the dashboard page.
  - **ID: welcome-message** - Type: H1 - Welcome message displaying username.
  - **ID: make-reservation-button** - Type: Button - Button to navigate to reservation page.
  - **ID: view-menu-button** - Type: Button - Button to navigate to menu page.
  - **ID: back-to-dashboard** - Type: Button - Button to refresh dashboard.
  - **ID: my-reservations-button** - Type: Button - Button to navigate to my reservations page.
  - **ID: my-reviews-button** - Type: Button - Button to navigate to my reviews page.
  - **ID: waitlist-button** - Type: Button - Button to navigate to waitlist page.
  - **ID: profile-button** - Type: Button - Button to navigate to user profile page.

### 2. Menu Page
- **Page Title**: Restaurant Menu
- **Overview**: A page displaying the restaurant menu with categories and filtering.
- **Elements**:
  - **ID: menu-page** - Type: Div - Container for the menu page.
  - **ID: menu-grid** - Type: Div - Grid displaying dish cards with image, name, price, description.
  - **ID: view-dish-button-{dish_id}** - Type: Button - Button to view dish details (each card has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 3. Dish Details Page
- **Page Title**: Dish Details
- **Overview**: A page displaying detailed information about a specific dish.
- **Elements**:
  - **ID: dish-details-page** - Type: Div - Container for the dish details page.
  - **ID: dish-name** - Type: H1 - Display dish name.
  - **ID: dish-price** - Type: Div - Display dish price.
  - **ID: back-to-menu** - Type: Button - Button to navigate back to menu.

### 4. Make Reservation Page
- **Page Title**: Make Reservation
- **Overview**: A page for users to make a table reservation.
- **Elements**:
  - **ID: reservation-page** - Type: Div - Container for the reservation page.
  - **ID: guest-name** - Type: Input - Field to input guest name.
  - **ID: party-size** - Type: Dropdown - Dropdown to select party size (1-10).
  - **ID: reservation-date** - Type: Input (date) - Field to select reservation date.
  - **ID: submit-reservation-button** - Type: Button - Button to submit reservation.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 5. My Reservations Page
- **Page Title**: My Reservations
- **Overview**: A page displaying all reservations made by the user.
- **Elements**:
  - **ID: my-reservations-page** - Type: Div - Container for the my reservations page.
  - **ID: reservations-table** - Type: Table - Table displaying reservations with date, time, party size, status.
  - **ID: cancel-reservation-button-{reservation_id}** - Type: Button - Button to cancel reservation (each upcoming reservation has this).
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 6. Waitlist Page
- **Page Title**: Waitlist
- **Overview**: A page for users to join the waitlist and check their position.
- **Elements**:
  - **ID: waitlist-page** - Type: Div - Container for the waitlist page.
  - **ID: waitlist-party-size** - Type: Dropdown - Dropdown to select party size.
  - **ID: join-waitlist-button** - Type: Button - Button to join waitlist.
  - **ID: user-position** - Type: Div - Display user's current position in waitlist.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 7. My Reviews Page
- **Page Title**: My Reviews
- **Overview**: A page displaying all reviews written by the user.
- **Elements**:
  - **ID: reviews-page** - Type: Div - Container for the reviews page.
  - **ID: reviews-list** - Type: Div - List of reviews with dish name, rating, review text.
  - **ID: write-new-review-button** - Type: Button - Button to navigate to write review page.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

### 8. Write Review Page
- **Page Title**: Write Review
- **Overview**: A page for users to write a review for a dish.
- **Elements**:
  - **ID: write-review-page** - Type: Div - Container for the write review page.
  - **ID: select-dish** - Type: Dropdown - Dropdown to select dish to review.
  - **ID: rating-input** - Type: Dropdown - Dropdown to select rating (1-5 stars).
  - **ID: review-text** - Type: Textarea - Field to write review text.
  - **ID: submit-review-button** - Type: Button - Button to submit review.
  - **ID: back-to-reviews** - Type: Button - Button to navigate back to my reviews.

### 9. User Profile Page
- **Page Title**: My Profile
- **Overview**: A page for users to view and edit their profile information.
- **Elements**:
  - **ID: profile-page** - Type: Div - Container for the profile page.
  - **ID: profile-username** - Type: Div - Display username (not editable).
  - **ID: profile-email** - Type: Input - Field to update email.
  - **ID: update-profile-button** - Type: Button - Button to save profile changes.
  - **ID: back-to-dashboard** - Type: Button - Button to navigate back to dashboard.

## 4. Data Storage

The 'RestaurantReservation' application will store data locally in text files organized in the directory 'data'. The following data formats and examples are defined:

### 1. User Data
- **File Name**: `users.txt`
- **Data Format**:
  ```
  username|email|phone|full_name
  ```
- **Example Data**:
  ```
  john_diner|john@example.com|555-1234|John Diner
  jane_food|jane@example.com|555-5678|Jane Foodie
  ```

### 2. Menu Items Data
- **File Name**: `menu.txt`
- **Data Format**:
  ```
  dish_id|name|category|price|description|ingredients|dietary|avg_rating
  ```
- **Example Data**:
  ```
  1|Caesar Salad|Appetizers|8.99|Fresh romaine lettuce with caesar dressing|Romaine,Parmesan,Croutons,Dressing|Vegetarian|4.5
  2|Grilled Salmon|Main Course|24.99|Fresh Atlantic salmon grilled to perfection|Salmon,Lemon,Herbs,Vegetables|Gluten-Free|4.8
  3|Chocolate Lava Cake|Desserts|7.99|Warm chocolate cake with molten center|Chocolate,Flour,Eggs,Sugar|Vegetarian|4.9
  4|Green Tea|Beverages|3.99|Premium Japanese green tea|Green Tea Leaves,Water|Vegan|4.6
  ```

### 3. Reservations Data
- **File Name**: `reservations.txt`
- **Data Format**:
  ```
  reservation_id|username|guest_name|phone|email|party_size|date|time|special_requests|status
  ```
- **Example Data**:
  ```
  1|john_diner|John Diner|555-1234|john@example.com|4|2024-12-01|18:00|Window seat please|Upcoming
  2|jane_food|Jane Foodie|555-5678|jane@example.com|2|2024-11-20|19:30|Anniversary dinner|Completed
  3|john_diner|John Diner|555-1234|john@example.com|6|2024-12-05|20:00||Upcoming
  ```

### 4. Waitlist Data
- **File Name**: `waitlist.txt`
- **Data Format**:
  ```
  waitlist_id|username|party_size|join_time|status
  ```
- **Example Data**:
  ```
  1|john_diner|2|2024-11-22 18:30:00|Active
  2|jane_food|4|2024-11-22 18:45:00|Active
  ```

### 5. Reviews Data
- **File Name**: `reviews.txt`
- **Data Format**:
  ```
  review_id|username|dish_id|rating|review_text|review_date
  ```
- **Example Data**:
  ```
  1|jane_food|2|5|Best salmon I've ever had!|2024-11-21
  2|john_diner|3|5|Absolutely divine dessert!|2024-11-20
  3|jane_food|1|4|Fresh and tasty, but dressing could be creamier.|2024-11-19
  ```

All files will be saved in the `data` directory to ensure organization and easy access. The format uses a pipe (`|`) delimiter for better readability and parsing.
