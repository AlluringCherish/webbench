# MovieTicketing Design Specification Document

---

## Section 1: Flask Routes Specification

| Route Path | Function Name | HTTP Method | Template | Context Variables |
|------------|---------------|-------------|----------|------------------|
| / | root_redirect | GET | None (Redirects) | None |
| /dashboard | dashboard_page | GET | dashboard.html |
  - featured_movies: list of dict {movie_id (int), title (str), rating (float), genre (str)} (for featured & upcoming movies)
| /movies | movie_catalog | GET | movie_catalog.html |
  - movies: list of dict {movie_id (int), title (str), genre (str), rating (float), duration (int), poster_url (str)} (all movies)
  - genres: list of dict {genre_id (int), genre_name (str)} (for genre filter dropdown)
  - search_query: str (optional search term)
  - genre_filter: str (selected genre filter)
| /movies/<int:movie_id> | movie_details | GET | movie_details.html |
  - movie: dict {movie_id (int), title (str), director (str), rating (float), description (str), genre (str), duration (int), release_date (str)}
| /showtimes/<int:movie_id> | showtime_selection | GET | showtime_selection.html |
  - movie: dict as above (summary info for page heading)
  - showtimes: list of dict {showtime_id (int), theater_name (str), showtime_date (str), showtime_time (str), price (float)}
  - theaters: list of dict {theater_id (int), theater_name (str)} (for theater filter dropdown)
  - selected_theater: str (filter - optional)
  - selected_date: str (filter - optional)
| /seats/<int:showtime_id> | seat_selection | GET | seat_selection.html |
  - showtime: dict {showtime_id (int), movie_title (str), theater_name (str), showtime_date (str), showtime_time (str)}
  - seats: list of dict {seat_id (int), row (str), column (int), seat_type (str), status (str)}
  - selected_seats: list of str (initially empty or from previous selection)
| /booking_confirmation/<int:showtime_id> | booking_confirmation | GET | booking_confirmation.html |
  - showtime: dict same as seat_selection
  - selected_seats: list of str (seat identifiers like 'A1', 'B5')
  - total_price: float
| /booking_confirmation/<int:showtime_id> | confirm_booking | POST | None (redirect) |
  - Form data: customer_name (str), customer_email (str), seats (list of str)
| /bookings | booking_history | GET | booking_history.html |
  - bookings: list of dict {booking_id (int), movie_title (str), booking_date (str), seats_booked (list of str), status (str), total_price (float)}
  - status_filter: str (filter selected)
| /bookings/<int:booking_id> | booking_detail | GET | booking_detail.html |
  - booking: dict {booking_id (int), showtime_id (int), movie_title (str), customer_name (str), customer_email (str), booking_date (str), seats_booked (list of str), total_price (float), status (str)}
| /theaters | theater_information | GET | theater_information.html |
  - theaters: list of dict {theater_id (int), theater_name (str), location (str), city (str), screens (int), facilities (str)}
  - location_filter: str (filter selected)

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- <title>: "Movie Ticketing Dashboard"
- <h1>: "Movie Ticketing Dashboard"
- Element IDs:
  - dashboard-page (Div): Container for dashboard
  - featured-movies (Div): Featured movie recommendations display
  - browse-movies-button (Button): Navigate to movie_catalog, calls url_for('movie_catalog')
  - view-bookings-button (Button): Navigate to booking_history, calls url_for('booking_history')
  - showtimes-button (Button): Navigate to showtime_selection root or movie selection (e.g., url_for('showtime_selection', movie_id=some))

### 2. Movie Catalog Page
- Filename: templates/movie_catalog.html
- Page Title: Movie Catalog
- <title>: "Movie Catalog"
- <h1>: "Movie Catalog"
- Element IDs:
  - catalog-page (Div): Container for catalog
  - search-input (Input): Text input to search movies by title or genre
  - genre-filter (Dropdown): Select dropdown with genre options
  - movies-grid (Div): Grid container displaying movie cards
  - view-movie-button-{movie_id} (Button): One per movie, navigates to movie_details with movie_id

### 3. Movie Details Page
- Filename: templates/movie_details.html
- Page Title: Movie Details
- <title>: "Movie Details"
- <h1>: movie-title (dynamic movie title)
- Element IDs:
  - movie-details-page (Div): Container
  - movie-title (H1): Displays movie title
  - movie-director (Div): Displays director name
  - movie-rating (Div): Displays rating
  - movie-description (Div): Displays movie description
  - select-showtime-button (Button): Navigates to showtime_selection for movie_id

### 4. Showtime Selection Page
- Filename: templates/showtime_selection.html
- Page Title: Select Showtime
- <title>: "Select Showtime"
- <h1>: "Select Showtime for {movie_title}"
- Element IDs:
  - showtime-page (Div): Container
  - showtimes-list (Div): List of showtime entries
  - theater-filter (Dropdown): For filtering showtimes by theater
  - date-filter (Input): Date input for filtering
  - select-showtime-button-{showtime_id} (Button): For selecting showtime

### 5. Seat Selection Page
- Filename: templates/seat_selection.html
- Page Title: Select Seats
- <title>: "Select Seats"
- <h1>: "Select Seats for {movie_title} at {theater_name} on {showtime_date} {showtime_time}"
- Element IDs:
  - seat-selection-page (Div): Container
  - seat-map (Div): Interactive seat map
  - selected-seats-display (Div): Display selected seats
  - seat-{row}{col} (Button): Each seat button, e.g. seat-A1, seat-B3
  - proceed-booking-button (Button): Proceed to booking confirmation

### 6. Booking Confirmation Page
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- <title>: "Booking Confirmation"
- <h1>: "Booking Confirmation"
- Element IDs:
  - confirmation-page (Div): Container
  - booking-summary (Div): Summary of booking details
  - customer-name (Input): Input for customer name
  - customer-email (Input): Input for customer email
  - confirm-booking-button (Button): Confirm booking and POST to confirm_booking

### 7. Booking History Page
- Filename: templates/booking_history.html
- Page Title: Booking History
- <title>: "Booking History"
- <h1>: "Booking History"
- Element IDs:
  - bookings-page (Div): Container
  - bookings-table (Table): Table showing booking list with columns booking_id, movie, date, seats, status
  - view-booking-button-{booking_id} (Button): View details for booking
  - status-filter (Dropdown): Filter by status
  - back-to-dashboard (Button): Navigate to dashboard

### 8. Theater Information Page
- Filename: templates/theater_information.html
- Page Title: Theater Information
- <title>: "Theater Information"
- <h1>: "Theater Information"
- Element IDs:
  - theater-page (Div): Container
  - theaters-list (Div): List of theaters
  - theater-location-filter (Dropdown): Filter theaters by location
  - facilities-display (Div): Show facilities info
  - back-to-dashboard (Button): Navigate to dashboard

---

## Section 3: Data File Schemas

### 1. Movies Data File
- Filename: data/movies.txt
- Fields (pipe-delimited):
  movie_id|title|director|genre|rating|duration|description|release_date
- Description: Contains all movie records with details.
- Examples:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### 2. Theaters Data File
- Filename: data/theaters.txt
- Fields (pipe-delimited):
  theater_id|theater_name|location|city|screens|facilities
- Description: Contains theater records with location and facilities.
- Examples:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### 3. Showtimes Data File
- Filename: data/showtimes.txt
- Fields (pipe-delimited):
  showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Contains showtime info including price and seats available.
- Examples:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### 4. Seats Data File
- Filename: data/seats.txt
- Fields (pipe-delimited):
  seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Contains seats info per theater and screen with status.
- Examples:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### 5. Bookings Data File
- Filename: data/bookings.txt
- Fields (pipe-delimited):
  booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Contains booking records with seat info.
- Examples:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### 6. Genres Data File
- Filename: data/genres.txt
- Fields (pipe-delimited):
  genre_id|genre_name|description
- Description: Lists genres and their descriptions.
- Examples:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---

This design spec provides clear, exact naming for routes, function names, templates, element IDs, context variables, and data schemas to ensure complete parallel development for backend and frontend teams.