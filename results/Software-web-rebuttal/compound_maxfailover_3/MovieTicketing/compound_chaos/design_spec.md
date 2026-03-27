# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                                   | Function Name                | HTTP Method | Template Rendered          | Context Variables                                                                                           |
|----------------------------------------------|------------------------------|-------------|----------------------------|-------------------------------------------------------------------------------------------------------------|
| `/`                                          | root_redirect                | GET         | N/A (Redirect to dashboard) | None                                                                                                        |
| `/dashboard`                                 | dashboard                   | GET         | dashboard.html             | featured_movies: list of dict {
  movie_id: int,
  title: str,
  rating: float,
  duration: int
}                                                                                           |
| `/movies`                                   | movie_catalog               | GET         | movie_catalog.html          | movies: list of dict {
  movie_id: int,
  title: str,
  genre: str,
  rating: float,
  duration: int
}                                                                                           |
| `/movies/search`                            | movie_search                | POST        | movie_catalog.html          | movies: list of dict (same as `/movies`), search_term: str, genre_filter: str                                  |
| `/movie/<int:movie_id>`                     | movie_details               | GET         | movie_details.html          | movie: dict {
  movie_id: int,
  title: str,
  director: str,
  genre: str,
  rating: float,
  duration: int,
  description: str,
  release_date: str (YYYY-MM-DD)
}                                                                              |
| `/movie/<int:movie_id>/showtimes`           | select_showtime             | GET         | showtime_selection.html     | showtimes: list of dict {
  showtime_id: int,
  theater_name: str,
  theater_id: int,
  showtime_date: str (YYYY-MM-DD),
  showtime_time: str (HH:MM),
  price: float,
  available_seats: int
}, theater_filter_options: list of str (theater names), selected_theater: str or None, date_filter: str or None |
| `/select_showtime/<int:showtime_id>/seats` | seat_selection             | GET         | seat_selection.html         | seat_map: list of dict {
  seat_id: int,
  row: str,
  column: int,
  seat_type: str,
  status: str (Available or Booked)
}, selected_showtime: dict {
  showtime_id: int,
  movie_title: str,
  theater_name: str,
  showtime_date: str,
  showtime_time: str,
  price: float
}                                                                 | 
| `/booking/confirm`                          | booking_confirmation        | GET         | booking_confirmation.html   | booking_summary: dict {
  movie_title: str,
  showtime_date: str,
  showtime_time: str,
  theater_name: str,
  seats: list of str (e.g., ["A1", "B3"]),
  total_price: float
}                                                                                          |
| `/booking/confirm`                          | confirm_booking             | POST        | booking_confirmation.html   | booking_success: bool, error_message: str (optional)                                                        |
| `/bookings`                                | booking_history             | GET         | booking_history.html        | bookings: list of dict {
  booking_id: int,
  movie_title: str,
  booking_date: str (YYYY-MM-DD),
  seats: list of str,
  status: str
}, status_filter_options: list of str (All, Confirmed, Cancelled, Completed), selected_status: str |
| `/booking/<int:booking_id>`                  | view_booking_details        | GET         | booking_details.html        | booking: dict {
  booking_id: int,
  movie_title: str,
  showtime_date: str,
  seats: list of str,
  status: str,
  customer_name: str,
  customer_email: str,
  total_price: float
}                                                         |
| `/theaters`                                | theater_information         | GET         | theater_information.html    | theaters: list of dict {
  theater_id: int,
  theater_name: str,
  location: str,
  city: str,
  screens: int,
  facilities: list of str
}, location_filter_options: list of str (cities), selected_location: str or None |

Notes:
- Root route `/` redirects to `/dashboard`.
- All dynamic route parameters are integers for IDs.
- Booking confirmation POST route accepts form data for finalizing booking.

---

## Section 2: HTML Template Specifications

### Template: dashboard.html
- Page Title: "Movie Ticketing Dashboard"
- <title> and <h1> content: "Movie Ticketing Dashboard"
- Elements:
  - ID: dashboard-page, Div, container for dashboard page
  - ID: featured-movies, Div, displays featured movie recommendations
  - ID: browse-movies-button, Button, navigates to movie_catalog route
  - ID: view-bookings-button, Button, navigates to booking_history route
  - ID: showtimes-button, Button, navigates to select_showtime route or showtimes listing (may go to /movies for selecting movie first)

### Template: movie_catalog.html
- Page Title: "Movie Catalog"
- <title> and <h1>: "Movie Catalog"
- Elements:
  - ID: catalog-page, Div, container for entire catalog page
  - ID: search-input, Input, text field to search movies by title or genre
  - ID: genre-filter, Dropdown (select), filter movies by genre
  - ID: movies-grid, Div, grid display of movie cards
  - ID pattern: view-movie-button-{movie_id}, Button, opens movie details page for that movie

### Template: movie_details.html
- Page Title: "Movie Details"
- <title> and <h1>: "Movie Details"
- Elements:
  - ID: movie-details-page, Div, container for movie details
  - ID: movie-title, H1, displays selected movie title
  - ID: movie-director, Div, displays movie director
  - ID: movie-rating, Div, displays movie rating
  - ID: movie-description, Div, displays movie description
  - ID: select-showtime-button, Button, navigates to select_showtime route for this movie

### Template: showtime_selection.html
- Page Title: "Select Showtime"
- <title> and <h1>: "Select Showtime"
- Elements:
  - ID: showtime-page, Div, container for showtime page
  - ID: showtimes-list, Div, list of available showtimes with date, time, theater, price
  - ID: theater-filter, Dropdown, filters showtimes by theater
  - ID: date-filter, Input (date), filters showtimes by date
  - ID pattern: select-showtime-button-{showtime_id}, Button, selects specific showtime and goes to seat selection

### Template: seat_selection.html
- Page Title: "Select Seats"
- <title> and <h1>: "Select Seats"
- Elements:
  - ID: seat-selection-page, Div, container for seat selection
  - ID: seat-map, Div, interactive seat map showing available/booked seats
  - ID: selected-seats-display, Div, display currently selected seats
  - ID pattern: seat-{row}{col}, Button, each seat selectable by row letter and column number (e.g., seat-A1)
  - ID: proceed-booking-button, Button, proceeds to booking confirmation

### Template: booking_confirmation.html
- Page Title: "Booking Confirmation"
- <title> and <h1>: "Booking Confirmation"
- Elements:
  - ID: confirmation-page, Div, container for confirmation page
  - ID: booking-summary, Div, summary of booking details (movie, showtime, seats, total price)
  - ID: customer-name, Input, field for customer name
  - ID: customer-email, Input, field for customer email
  - ID: confirm-booking-button, Button, confirms and completes booking

### Template: booking_history.html
- Page Title: "Booking History"
- <title> and <h1>: "Booking History"
- Elements:
  - ID: bookings-page, Div, container for bookings page
  - ID: bookings-table, Table, displays bookings with booking ID, movie, date, seats, status
  - ID pattern: view-booking-button-{booking_id}, Button, views details for selected booking
  - ID: status-filter, Dropdown, filters bookings by status (All, Confirmed, Cancelled, Completed)
  - ID: back-to-dashboard, Button, navigates to dashboard

### Template: booking_details.html
- Page Title: "Booking Details"
- <title> and <h1>: "Booking Details"
- Elements:
  - ID: booking-details-page, Div, container for booking detail page
  - ID: booking-id, Div or Span, displays booking ID
  - ID: movie-title, Div, shows movie title
  - ID: showtime-date, Div, shows showtime date/time
  - ID: seats, Div, lists booked seats
  - ID: status, Div, booking status
  - ID: customer-name, Div, customer name
  - ID: customer-email, Div, customer email
  - ID: total-price, Div, shows total price
  - ID: back-to-bookings-button, Button, navigates back to booking_history route

### Template: theater_information.html
- Page Title: "Theater Information"
- <title> and <h1>: "Theater Information"
- Elements:
  - ID: theater-page, Div, container for theater page
  - ID: theaters-list, Div, list of theaters with details (name, location, screens, facilities)
  - ID: theater-location-filter, Dropdown, filter theaters by location (city)
  - ID: facilities-display, Div, display theater facilities
  - ID: back-to-dashboard, Button, navigates to dashboard

---

## Section 3: Data File Schemas

### 1. Movies Data
- Filename & Path: `data/movies.txt`
- Fields (pipe-delimited, no headers):
  1. movie_id (int)
  2. title (str)
  3. director (str)
  4. genre (str)
  5. rating (float)
  6. duration (int, minutes)
  7. description (str)
  8. release_date (str, YYYY-MM-DD)
- Content Description: Stores all movie details including metadata and descriptions.
- Example Rows:
  ```
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23
  ```

### 2. Theaters Data
- Filename & Path: `data/theaters.txt`
- Fields (pipe-delimited, no headers):
  1. theater_id (int)
  2. theater_name (str)
  3. location (str)
  4. city (str)
  5. screens (int)
  6. facilities (str, comma-separated list)
- Content Description: Contains theaters information including location and amenities.
- Example Rows:
  ```
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge
  ```

### 3. Showtimes Data
- Filename & Path: `data/showtimes.txt`
- Fields (pipe-delimited, no headers):
  1. showtime_id (int)
  2. movie_id (int)
  3. theater_id (int)
  4. showtime_date (str, YYYY-MM-DD)
  5. showtime_time (str, HH:MM 24-hour format)
  6. price (float)
  7. available_seats (int)
- Content Description: Holds all showtime schedules with pricing and availability.
- Example Rows:
  ```
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95
  ```

### 4. Seats Data
- Filename & Path: `data/seats.txt`
- Fields (pipe-delimited, no headers):
  1. seat_id (int)
  2. theater_id (int)
  3. screen_id (int)
  4. row (str, letter)
  5. column (int)
  6. seat_type (str, e.g., Standard, Premium)
  7. status (str, Available or Booked)
- Content Description: Detail seating layout per theater screen including booking status.
- Example Rows:
  ```
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked
  ```

### 5. Bookings Data
- Filename & Path: `data/bookings.txt`
- Fields (pipe-delimited, no headers):
  1. booking_id (int)
  2. showtime_id (int)
  3. customer_name (str)
  4. customer_email (str)
  5. booking_date (str, YYYY-MM-DD)
  6. total_price (float)
  7. status (str, e.g., Confirmed, Cancelled, Completed)
  8. seats_booked (str, comma-separated seat identifiers, e.g., A1,A2)
- Content Description: Stores all ticket bookings with customer info and seat details.
- Example Rows:
  ```
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4
  ```

### 6. Genres Data
- Filename & Path: `data/genres.txt`
- Fields (pipe-delimited, no headers):
  1. genre_id (int)
  2. genre_name (str)
  3. description (str)
- Content Description: Lists possible movie genres with brief descriptions.
- Example Rows:
  ```
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
  ```

---

This specification fully aligns routes, templates, and data structures to enable backend and frontend teams to develop independently and in parallel, with no ambiguity or missing details.

