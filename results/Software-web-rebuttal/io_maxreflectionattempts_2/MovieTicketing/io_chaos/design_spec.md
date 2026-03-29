# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

- **`/`**
  - Function Name: `root_redirect`
  - HTTP Method(s): GET
  - Behavior: Redirects to `/dashboard`
  - Template Rendered: None
  - Context Variables: None

- **`/dashboard`**
  - Function Name: `dashboard`
  - HTTP Method(s): GET
  - Template Rendered: `dashboard.html`
  - Context Variables:
    - `featured_movies`: list of dicts with fields:
      - `movie_id` (int)
      - `title` (str)
      - `rating` (float)

- **`/movies`**
  - Function Name: `movie_catalog`
  - HTTP Method(s): GET
  - Template Rendered: `movie_catalog.html`
  - Context Variables:
    - `movies`: list of dicts with fields:
      - `movie_id` (int)
      - `title` (str)
      - `genre` (str)
      - `rating` (float)
      - `duration` (int)
    - `genres`: list of dicts with fields:
      - `genre_name` (str)

- **`/movies/<int:movie_id>`**
  - Function Name: `movie_details`
  - HTTP Method(s): GET
  - Template Rendered: `movie_details.html`
  - Context Variables:
    - `movie`: dict with fields:
      - `movie_id` (int)
      - `title` (str)
      - `director` (str)
      - `genre` (str)
      - `rating` (float)
      - `duration` (int)
      - `description` (str)
      - `release_date` (str)

- **`/movies/<int:movie_id>/showtimes`**
  - Function Name: `select_showtime`
  - HTTP Method(s): GET
  - Template Rendered: `select_showtime.html`
  - Context Variables:
    - `movie`: same structure as above
    - `showtimes`: list of dicts with fields:
      - `showtime_id` (int)
      - `theater_name` (str)
      - `showtime_date` (str)
      - `showtime_time` (str)
      - `price` (float)
    - `theaters`: list of dicts with fields:
      - `theater_id` (int)
      - `theater_name` (str)
    - `selected_theater_filter` (str)
    - `selected_date_filter` (str)

- **`/showtimes/<int:showtime_id>/seats`**
  - Function Name: `seat_selection`
  - HTTP Method(s): GET
  - Template Rendered: `seat_selection.html`
  - Context Variables:
    - `showtime`: dict with fields:
      - `showtime_id` (int)
      - `movie_title` (str)
      - `theater_name` (str)
      - `showtime_date` (str)
      - `showtime_time` (str)
      - `price` (float)
    - `seats`: list of dicts with fields:
      - `seat_id` (int)
      - `row` (str)
      - `column` (int)
      - `seat_type` (str)
      - `status` (str)  # e.g., "Available", "Booked"
    - `selected_seats`: list of str (seat identifiers e.g. "A1")

- **`/showtimes/<int:showtime_id>/seats`**
  - Function Name: `submit_seat_selection`
  - HTTP Method(s): POST
  - Template Rendered: Redirects to `/booking/confirm`
  - Form Data:
    - `selected_seats`: list of strings (selected seat identifiers)

- **`/booking/confirm`**
  - Function Name: `booking_confirmation_get`
  - HTTP Method(s): GET
  - Template Rendered: `booking_confirmation.html`
  - Context Variables:
    - `booking_details`: dict with fields:
      - `movie_title` (str)
      - `showtime_date` (str)
      - `showtime_time` (str)
      - `seats` (list of str)
      - `total_price` (float)

- **`/booking/confirm`**
  - Function Name: `booking_confirmation_post`
  - HTTP Method(s): POST
  - Template Rendered: Redirects to `/bookings`
  - Form Data:
    - `customer_name` (str)
    - `customer_email` (str)
    - `selected_seats` (list of str)
    - `showtime_id` (int)

- **`/bookings`**
  - Function Name: `booking_history`
  - HTTP Method(s): GET
  - Template Rendered: `booking_history.html`
  - Context Variables:
    - `bookings`: list of dicts with fields:
      - `booking_id` (int)
      - `movie_title` (str)
      - `showtime_date` (str)
      - `seats` (list of str)
      - `status` (str)  # e.g., "Confirmed", "Cancelled", "Completed"
    - `status_filter` (str)

- **`/bookings/<int:booking_id>`**
  - Function Name: `view_booking`
  - HTTP Method(s): GET
  - Template Rendered: `booking_details.html`
  - Context Variables:
    - `booking`: dict with fields:
      - `booking_id` (int)
      - `movie_title` (str)
      - `showtime_date` (str)
      - `seats` (list of str)
      - `customer_name` (str)
      - `customer_email` (str)
      - `total_price` (float)
      - `status` (str)

- **`/theaters`**
  - Function Name: `theater_information`
  - HTTP Method(s): GET
  - Template Rendered: `theater_information.html`
  - Context Variables:
    - `theaters`: list of dicts with fields:
      - `theater_id` (int)
      - `theater_name` (str)
      - `location` (str)
      - `city` (str)
      - `screens` (int)
      - `facilities` (str)
    - `location_filter` (str)

---

## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- Title: "Movie Ticketing Dashboard"
- Header `<h1>`: "Movie Ticketing Dashboard"
- Element IDs:
  - `dashboard-page`: Div container for the dashboard page
  - `featured-movies`: Div showing featured movie recommendations
  - `browse-movies-button`: Button, onclick navigates to url_for('movie_catalog')
  - `view-bookings-button`: Button, onclick navigates to url_for('booking_history')
  - `showtimes-button`: Button, onclick navigates to url_for('select_showtime') or suitable route

### 2. templates/movie_catalog.html
- Title: "Movie Catalog"
- Header `<h1>`: "Movie Catalog"
- Element IDs:
  - `catalog-page`: Div container for the catalog page
  - `search-input`: Input field for searching movies by title or genre
  - `genre-filter`: Dropdown for filtering by genre
  - `movies-grid`: Div grid displaying movie cards
  - Dynamic buttons with ID pattern `view-movie-button-{movie_id}`: Button to navigate to movie details page for that `movie_id` using url_for('movie_details', movie_id=movie_id)

### 3. templates/movie_details.html
- Title: "Movie Details"
- Header `<h1>`: "Movie Details"
- Element IDs:
  - `movie-details-page`: Div container
  - `movie-title`: H1 element for movie title
  - `movie-director`: Div for director
  - `movie-rating`: Div for rating
  - `movie-description`: Div for description
  - `select-showtime-button`: Button to proceed to showtime selection page for current movie (url_for('select_showtime', movie_id=movie_id))

### 4. templates/select_showtime.html
- Title: "Select Showtime"
- Header `<h1>`: "Select Showtime"
- Element IDs:
  - `showtime-page`: Div container
  - `showtimes-list`: Div listing all available showtimes
  - `theater-filter`: Dropdown to filter showtimes by theater
  - `date-filter`: Input to filter by date
  - Dynamic buttons with ID pattern `select-showtime-button-{showtime_id}`: Button to select a showtime and proceed (url_for('seat_selection', showtime_id=showtime_id))

### 5. templates/seat_selection.html
- Title: "Select Seats"
- Header `<h1>`: "Select Seats"
- Element IDs:
  - `seat-selection-page`: Div container
  - `seat-map`: Div containing interactive seat map
  - `selected-seats-display`: Div showing seats currently selected
  - Dynamic buttons with ID pattern `seat-{row}{col}`: Individual seat buttons (e.g., `seat-A1`), reflecting seat status (Available or Booked)
  - `proceed-booking-button`: Button to submit seat selection and proceed to booking confirmation

### 6. templates/booking_confirmation.html
- Title: "Booking Confirmation"
- Header `<h1>`: "Booking Confirmation"
- Element IDs:
  - `confirmation-page`: Div container
  - `booking-summary`: Div displaying summary (movie, showtime, seats, total price)
  - `customer-name`: Input field for customer name
  - `customer-email`: Input field for customer email
  - `confirm-booking-button`: Button to confirm booking after form completion

### 7. templates/booking_history.html
- Title: "Booking History"
- Header `<h1>`: "Booking History"
- Element IDs:
  - `bookings-page`: Div container
  - `bookings-table`: Table displaying booking list including columns (Booking ID, Movie, Date, Seats, Status)
  - Dynamic buttons with ID pattern `view-booking-button-{booking_id}`: Button to view detailed booking information
  - `status-filter`: Dropdown to filter bookings by status
  - `back-to-dashboard`: Button to navigate back to dashboard (url_for('dashboard'))

### 8. templates/theater_information.html
- Title: "Theater Information"
- Header `<h1>`: "Theater Information"
- Element IDs:
  - `theater-page`: Div container
  - `theaters-list`: Div listing theaters along with location, screens, and facilities
  - `theater-location-filter`: Dropdown to filter theaters by location
  - `facilities-display`: Div showing theater facilities and amenities
  - `back-to-dashboard`: Button to navigate back to dashboard (url_for('dashboard'))

---

## Section 3: Data File Schemas

### data/movies.txt
- Filename: `data/movies.txt`
- Fields Order (pipe "|" delimited):
  - movie_id (int)
  - title (str)
  - director (str)
  - genre (str)
  - rating (float)
  - duration (int, minutes)
  - description (str)
  - release_date (str, YYYY-MM-DD)
- Description: Stores all movie information.
- Examples:
  - `1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31`
  - `2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16`
  - `3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23`

### data/theaters.txt
- Filename: `data/theaters.txt`
- Fields Order:
  - theater_id (int)
  - theater_name (str)
  - location (str)
  - city (str)
  - screens (int)
  - facilities (str, comma-separated list)
- Description: Contains theater details.
- Examples:
  - `1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access`
  - `2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking`
  - `3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge`

### data/showtimes.txt
- Filename: `data/showtimes.txt`
- Fields Order:
  - showtime_id (int)
  - movie_id (int)
  - theater_id (int)
  - showtime_date (str, YYYY-MM-DD)
  - showtime_time (str, HH:MM 24-hour)
  - price (float)
  - available_seats (int)
- Description: Contains showtime scheduling info.
- Examples:
  - `1|1|1|2025-02-01|19:00|12.99|85`
  - `2|1|1|2025-02-01|22:30|12.99|40`
  - `3|2|2|2025-02-01|18:00|14.99|95`

### data/seats.txt
- Filename: `data/seats.txt`
- Fields Order:
  - seat_id (int)
  - theater_id (int)
  - screen_id (int)
  - row (str, single character)
  - column (int)
  - seat_type (str)
  - status (str, e.g. "Available" or "Booked")
- Description: Contains seat attributes and status.
- Examples:
  - `1|1|1|A|1|Standard|Available`
  - `2|1|1|A|2|Standard|Available`
  - `3|1|1|B|5|Premium|Booked`

### data/bookings.txt
- Filename: `data/bookings.txt`
- Fields Order:
  - booking_id (int)
  - showtime_id (int)
  - customer_name (str)
  - customer_email (str)
  - booking_date (str, YYYY-MM-DD)
  - total_price (float)
  - status (str, e.g., "Confirmed", "Cancelled", "Completed")
  - seats_booked (str, comma-separated list of seat identifiers, e.g. "A1,A2")
- Description: Stores booking transactions.
- Examples:
  - `1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2`
  - `2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10`
  - `3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4`

### data/genres.txt
- Filename: `data/genres.txt`
- Fields Order:
  - genre_id (int)
  - genre_name (str)
  - description (str)
- Description: Contains movie genres.
- Examples:
  - `1|Action|Fast-paced movies with exciting sequences and combat`
  - `2|Drama|Character-driven stories exploring complex themes`
  - `3|Sci-Fi|Science fiction with futuristic technology and concepts`

---

*End of MovieTicketing Design Specification*