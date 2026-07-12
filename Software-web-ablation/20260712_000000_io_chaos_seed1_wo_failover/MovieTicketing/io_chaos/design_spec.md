# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

1. **Root Route**
- Route Path: `/`
- Function Name: `root_redirect`
- HTTP Method: GET
- Redirects to: Dashboard Page route `/dashboard`
- Template: None (Redirect)
- Context Variables: None

2. **Dashboard Page**
- Route Path: `/dashboard`
- Function Name: `dashboard`
- HTTP Method: GET
- Template File: `dashboard.html`
- Context Variables:
  - `featured_movies`: list of dict
    - Fields per dict: `movie_id`(int), `title`(str), `genre`(str), `rating`(float), `duration`(int)

3. **Movie Catalog Page**
- Route Path: `/movies`
- Function Name: `movie_catalog`
- HTTP Method: GET
- Template File: `movie_catalog.html`
- Context Variables:
  - `movies`: list of dict
    - Fields per dict: `movie_id`(int), `title`(str), `genre`(str), `rating`(float), `duration`(int), `poster_url`(str)
  - `genres`: list of dict
    - Fields per dict: `genre_id`(int), `genre_name`(str)

4. **Movie Details Page**
- Route Path: `/movies/<int:movie_id>`
- Function Name: `movie_details`
- HTTP Method: GET
- Template File: `movie_details.html`
- Context Variables:
  - `movie`: dict
    - Fields: `movie_id`(int), `title`(str), `director`(str), `genre`(str), `rating`(float),
      `duration`(int), `description`(str)

5. **Showtime Selection Page**
- Route Path: `/movies/<int:movie_id>/showtimes`
- Function Name: `select_showtime`
- HTTP Method: GET
- Template File: `showtime_selection.html`
- Context Variables:
  - `movie_id`: int
  - `showtimes`: list of dict
    - Fields: `showtime_id`(int), `theater_name`(str), `showtime_date`(str), `showtime_time`(str), `price`(float)
  - `theaters`: list of dict
    - Fields: `theater_id`(int), `theater_name`(str)

6. **Seat Selection Page**
- Route Path: `/showtimes/<int:showtime_id>/seats`
- Function Name: `select_seats`
- HTTP Method: GET
- Template File: `seat_selection.html`
- Context Variables:
  - `showtime_id`: int
  - `seat_map`: list of dict
    - Fields: `seat_id`(int), `row`(str), `column`(int), `seat_type`(str), `status`(str) - Available or Booked
  - `selected_seats`: list of str (e.g., ["A1", "B3"])

7. **Booking Confirmation Page**
- Route Path: `/bookings/confirm`
- Function Name: `booking_confirmation`
- HTTP Methods: GET (viewing booking details), POST (submitting booking)
- Template File: `booking_confirmation.html`
- Context Variables (GET):
  - `booking_summary`: dict
    - Fields: `movie_title`(str), `showtime_date`(str), `showtime_time`(str), `seats`(list of str), `total_price`(float)
- POST Context Variables: None (form submission)

8. **Booking History Page**
- Route Path: `/bookings`
- Function Name: `booking_history`
- HTTP Method: GET
- Template File: `booking_history.html`
- Context Variables:
  - `bookings`: list of dict
    - Fields: `booking_id`(int), `movie_title`(str), `booking_date`(str), `seats`(list of str), `status`(str)

9. **Booking Details Page**
- Route Path: `/bookings/<int:booking_id>`
- Function Name: `booking_details`
- HTTP Method: GET
- Template File: `booking_details.html`
- Context Variables:
  - `booking`: dict
    - Fields: `booking_id`(int), `movie_title`(str), `showtime_date`(str), `showtime_time`(str), `seats`(list of str), `customer_name`(str), `customer_email`(str), `total_price`(float), `status`(str)

10. **Theater Information Page**
- Route Path: `/theaters`
- Function Name: `theater_information`
- HTTP Method: GET
- Template File: `theater_information.html`
- Context Variables:
  - `theaters`: list of dict
    - Fields: `theater_id`(int), `theater_name`(str), `location`(str), `city`(str), `screens`(int), `facilities`(str)

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Filename: `templates/dashboard.html`
- Page Title: `Movie Ticketing Dashboard`
- <h1> Title: `Movie Ticketing Dashboard`
- Element IDs:
  - `dashboard-page` (Div): Container for dashboard
  - `featured-movies` (Div): Display featured films
  - `browse-movies-button` (Button): Navigates to `movie_catalog` route
  - `view-bookings-button` (Button): Navigates to `booking_history` route
  - `showtimes-button` (Button): Navigates to `select_showtime` for a selected movie (dynamic navigation to be handled frontend/backend)

### 2. Movie Catalog Page
- Filename: `templates/movie_catalog.html`
- Page Title: `Movie Catalog`
- <h1> Title: `Movie Catalog`
- Element IDs:
  - `catalog-page` (Div): Container
  - `search-input` (Input): Search movies by title or genre
  - `genre-filter` (Dropdown): Filter by genre
  - `movies-grid` (Div): Grid for movie cards
  - `view-movie-button-{movie_id}` (Button): Each movie card's view details button, routes to `movie_details` with `movie_id`

### 3. Movie Details Page
- Filename: `templates/movie_details.html`
- Page Title: `Movie Details`
- <h1> Title: `Movie Details`
- Element IDs:
  - `movie-details-page` (Div): Container
  - `movie-title` (H1): Displays movie title
  - `movie-director` (Div): Displays director
  - `movie-rating` (Div): Displays rating
  - `movie-description` (Div): Displays description
  - `select-showtime-button` (Button): Navigates to `select_showtime` page for this `movie_id`

### 4. Showtime Selection Page
- Filename: `templates/showtime_selection.html`
- Page Title: `Select Showtime`
- <h1> Title: `Select Showtime`
- Element IDs:
  - `showtime-page` (Div): Container
  - `showtimes-list` (Div): List of showtimes
  - `theater-filter` (Dropdown): Filter showtimes by theater
  - `date-filter` (Input): Filter showtimes by date
  - `select-showtime-button-{showtime_id}` (Button): Select a showtime, routes to `select_seats` with `showtime_id`

### 5. Seat Selection Page
- Filename: `templates/seat_selection.html`
- Page Title: `Select Seats`
- <h1> Title: `Select Seats`
- Element IDs:
  - `seat-selection-page` (Div): Container
  - `seat-map` (Div): Interactive seat map
  - `selected-seats-display` (Div): Show currently selected seats
  - `seat-{row}{col}` (Button): Each seat button (e.g. `seat-A1`)
  - `proceed-booking-button` (Button): Proceed to `booking_confirmation`

### 6. Booking Confirmation Page
- Filename: `templates/booking_confirmation.html`
- Page Title: `Booking Confirmation`
- <h1> Title: `Booking Confirmation`
- Element IDs:
  - `confirmation-page` (Div): Container
  - `booking-summary` (Div): Summary details
  - `customer-name` (Input): Input customer name
  - `customer-email` (Input): Input customer email
  - `confirm-booking-button` (Button): Submit to confirm booking

### 7. Booking History Page
- Filename: `templates/booking_history.html`
- Page Title: `Booking History`
- <h1> Title: `Booking History`
- Element IDs:
  - `bookings-page` (Div): Container
  - `bookings-table` (Table): Show bookings with columns: Booking ID, Movie, Date, Seats, Status
  - `view-booking-button-{booking_id}` (Button): View booking details
  - `status-filter` (Dropdown): Filter by booking status
  - `back-to-dashboard` (Button): Navigate to `dashboard`

### 8. Booking Details Page
- Filename: `templates/booking_details.html`
- Page Title: `Booking Details`
- <h1> Title: `Booking Details`
- Element IDs:
  - `booking-details-page` (Div): Container
  - Displays booking details (no specific IDs for all fields, but fields to show:
    - Booking ID
    - Movie Title
    - Showtime Date & Time
    - Seats
    - Customer Name and Email
    - Total Price
    - Status
  - `back-to-dashboard` (Button): Navigate to `dashboard`

### 9. Theater Information Page
- Filename: `templates/theater_information.html`
- Page Title: `Theater Information`
- <h1> Title: `Theater Information`
- Element IDs:
  - `theater-page` (Div): Container
  - `theaters-list` (Div): List all theaters
  - `theater-location-filter` (Dropdown): Filter theaters by location
  - `facilities-display` (Div): Show facilities
  - `back-to-dashboard` (Button): Navigate to `dashboard`

---

## Section 3: Data File Schemas

1. **Movies Data**
- Filename: `data/movies.txt`
- Fields Order and Format:
  `movie_id|title|director|genre|rating|duration|description|release_date`
- Description: Stores movie details including identifiers, descriptive info, and release dates.
- Examples:
  ```
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23
  ```

2. **Theaters Data**
- Filename: `data/theaters.txt`
- Fields Order and Format:
  `theater_id|theater_name|location|city|screens|facilities`
- Description: Stores theaters details including location, number of screens, and facilities.
- Examples:
  ```
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge
  ```

3. **Showtimes Data**
- Filename: `data/showtimes.txt`
- Fields Order and Format:
  `showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats`
- Description: Stores showtime info linking movies and theaters with timing, price, and seat availability.
- Examples:
  ```
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95
  ```

4. **Seats Data**
- Filename: `data/seats.txt`
- Fields Order and Format:
  `seat_id|theater_id|screen_id|row|column|seat_type|status`
- Description: Stores seat details by theater and screen with status.
- Examples:
  ```
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked
  ```

5. **Bookings Data**
- Filename: `data/bookings.txt`
- Fields Order and Format:
  `booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked`
- Description: Stores booking info with customer and seat details.
- Examples:
  ```
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4
  ```

6. **Genres Data**
- Filename: `data/genres.txt`
- Fields Order and Format:
  `genre_id|genre_name|description`
- Description: Stores genres and their descriptions.
- Examples:
  ```
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
  ```

---

This completes the design specification to enable parallel backend and frontend development for the MovieTicketing web application.