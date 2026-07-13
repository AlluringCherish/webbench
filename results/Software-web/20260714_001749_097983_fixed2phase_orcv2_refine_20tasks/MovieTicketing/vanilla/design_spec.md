# MovieTicketing Web Application Design Specification

## Section 1: Page and UI Element Specification

### 1. Dashboard Page
- Page Title: Movie Ticketing Dashboard
- Container ID: dashboard-page (Div)
- UI Elements:
  - featured-movies (Div): Displays featured movie recommendations
  - browse-movies-button (Button): Navigates to Movie Catalog Page
  - view-bookings-button (Button): Navigates to Booking History Page
  - showtimes-button (Button): Navigates to Showtime Selection Page

### 2. Movie Catalog Page
- Page Title: Movie Catalog
- Container ID: catalog-page (Div)
- UI Elements:
  - search-input (Input): Search movies by title or genre
  - genre-filter (Dropdown): Filter movies by genre (Action, Comedy, Drama, Horror, etc.)
  - movies-grid (Div): Displays movie cards with poster, title, rating, duration
  - view-movie-button-{movie_id} (Button): View details for each movie (one per movie card)

### 3. Movie Details Page
- Page Title: Movie Details
- Container ID: movie-details-page (Div)
- UI Elements:
  - movie-title (H1): Displays movie title
  - movie-director (Div): Displays movie director
  - movie-rating (Div): Displays movie rating
  - movie-description (Div): Displays movie description
  - select-showtime-button (Button): Proceeds to Showtime Selection Page

### 4. Showtime Selection Page
- Page Title: Select Showtime
- Container ID: showtime-page (Div)
- UI Elements:
  - showtimes-list (Div): List of showtimes with date, time, theater, price
  - theater-filter (Dropdown): Filter showtimes by theater
  - date-filter (Input): Filter showtimes by date
  - select-showtime-button-{showtime_id} (Button): Select a specific showtime

### 5. Seat Selection Page
- Page Title: Select Seats
- Container ID: seat-selection-page (Div)
- UI Elements:
  - seat-map (Div): Interactive seat map showing available and booked seats
  - selected-seats-display (Div): Shows currently selected seats
  - seat-{row}{col} (Button): Individual seat (e.g., seat-A1, seat-B3, each a button)
  - proceed-booking-button (Button): Proceed to Booking Confirmation Page

### 6. Booking Confirmation Page
- Page Title: Booking Confirmation
- Container ID: confirmation-page (Div)
- UI Elements:
  - booking-summary (Div): Summary of booking details (movie, showtime, seats, total)
  - customer-name (Input): Enter customer name
  - customer-email (Input): Enter customer email
  - confirm-booking-button (Button): Confirm and complete booking

### 7. Booking History Page
- Page Title: Booking History
- Container ID: bookings-page (Div)
- UI Elements:
  - bookings-table (Table): Shows booking ID, movie, date, seats, status
  - view-booking-button-{booking_id} (Button): View details for each booking
  - status-filter (Dropdown): Filter bookings by status (All, Confirmed, Cancelled, Completed)
  - back-to-dashboard (Button): Navigate back to Dashboard Page

### 8. Theater Information Page
- Page Title: Theater Information
- Container ID: theater-page (Div)
- UI Elements:
  - theaters-list (Div): List theaters with location, screens, facilities
  - theater-location-filter (Dropdown): Filter theaters by location
  - facilities-display (Div): Display facilities and amenities
  - back-to-dashboard (Button): Navigate back to Dashboard Page

## Section 2: Navigation Flow

- Start Page: Dashboard Page (`dashboard-page`)
- From Dashboard:
  - browse-movies-button -> Movie Catalog Page (`catalog-page`)
  - view-bookings-button -> Booking History Page (`bookings-page`)
  - showtimes-button -> Showtime Selection Page (`showtime-page`)
- From Movie Catalog Page:
  - view-movie-button-{movie_id} -> Movie Details Page (`movie-details-page`)
- From Movie Details Page:
  - select-showtime-button -> Showtime Selection Page (`showtime-page`)
- From Showtime Selection Page:
  - select-showtime-button-{showtime_id} -> Seat Selection Page (`seat-selection-page`)
- From Seat Selection Page:
  - proceed-booking-button -> Booking Confirmation Page (`confirmation-page`)
- From Booking Confirmation Page:
  - confirm-booking-button -> Booking History Page (`bookings-page`)
- From Booking History Page:
  - view-booking-button-{booking_id} -> Booking Confirmation Page (`confirmation-page`) for detailed view
  - back-to-dashboard -> Dashboard Page (`dashboard-page`)
- From Theater Information Page:
  - back-to-dashboard -> Dashboard Page (`dashboard-page`)

## Section 3: Data Storage Formats

All data files are stored in the `data` directory.

### 1. movies.txt
- Fields (pipe `|` delimited):
  movie_id (int) | title (string) | director (string) | genre (string) | rating (float) | duration (int, minutes) | description (string) | release_date (YYYY-MM-DD)
- Example:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31

### 2. theaters.txt
- Fields (pipe `|` delimited):
  theater_id (int) | theater_name (string) | location (string) | city (string) | screens (int) | facilities (string, comma-separated)
- Examples:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### 3. showtimes.txt
- Fields (pipe `|` delimited):
  showtime_id (int) | movie_id (int) | theater_id (int) | showtime_date (YYYY-MM-DD) | showtime_time (HH:MM) | price (float) | available_seats (int)
- Example:
  1|1|1|2025-02-01|19:00|12.99|85

### 4. seats.txt
- Fields (pipe `|` delimited):
  seat_id (int) | theater_id (int) | screen_id (int) | row (string) | column (int) | seat_type (string) | status (string: Available or Booked)
- Example:
  1|1|1|A|1|Standard|Available

### 5. bookings.txt
- Fields (pipe `|` delimited):
  booking_id (int) | showtime_id (int) | customer_name (string) | customer_email (string) | booking_date (YYYY-MM-DD) | total_price (float) | status (string: Confirmed, Cancelled, Completed) | seats_booked (string, comma-separated seat identifiers e.g., A1,A2)
- Example:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2

### 6. genres.txt
- Fields (pipe `|` delimited):
  genre_id (int) | genre_name (string) | description (string)
- Examples:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---

This design specification fully describes the MovieTicketing web application pages, UI elements with their exact IDs, navigation flows between pages, and the local text file data storage formats with field orders and example data rows, as required for implementation.
