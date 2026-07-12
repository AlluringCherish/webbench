# MovieTicketing Application Design Specification

---

# Section 1: Flask Routes Specification

| Route Path | Function Name | HTTP Method | Template Rendered | Context Variables Passed (type) |
|------------|---------------|-------------|-------------------|-------------------------------|
| / | root_redirect | GET | None (Redirect to /dashboard) | None |
| /dashboard | dashboard | GET | dashboard.html | featured_movies (list of dict).
- featured_movies fields: movie_id (int), title (str), genre (str), rating (float), duration (int) |
| /movies | movie_catalog | GET | catalog.html | movies (list of dict), genres (list of dict).
- movies fields: movie_id (int), title (str), genre (str), rating (float), duration (int).
- genres fields: genre_id (int), genre_name (str) |
| /movies/<int:movie_id> | movie_details | GET | movie_details.html | movie (dict), showtimes (list of dict).
- movie fields: movie_id (int), title (str), director (str), genre (str), rating (float), duration (int), description (str), release_date (str)
- showtimes fields: showtime_id (int), theater_name (str), showtime_date (str), showtime_time (str), price (float) |
| /showtimes/select/<int:movie_id> | select_showtime | GET | showtime_selection.html | showtimes (list of dict), theaters (list of dict), selected_movie (dict).
- showtimes fields: showtime_id (int), theater_id (int), showtime_date (str), showtime_time (str), price (float), available_seats (int)
- theaters fields: theater_id (int), theater_name (str)
- selected_movie fields: movie_id (int), title (str) |
| /showtimes/select/<int:showtime_id>/seats | seat_selection | GET | seat_selection.html | seats_map (list of dict), selected_showtime (dict), selected_theater (dict)
- seats_map fields: seat_id (int), row (str), column (int), seat_type (str), status (str) for seats of the relevant theater and screen
- selected_showtime fields: showtime_id (int), movie_id (int), theater_id (int), showtime_date (str), showtime_time (str), price (float)
- selected_theater fields: theater_id (int), theater_name (str), location (str), city (str), screens (int), facilities (str) |
| /booking/confirm | booking_confirmation | GET, POST | booking_confirmation.html | On GET: booking_details (dict)
- booking_details fields: movie_title (str), showtime_date (str), showtime_time (str), theater_name (str), seats_selected (list of str), total_price (float)
On POST: success (bool), error_msg (str if any) |
| /bookings | booking_history | GET | booking_history.html | bookings (list of dict)
- bookings fields: booking_id (int), movie_title (str), booking_date (str), seats_booked (str), status (str) |
| /bookings/<int:booking_id> | booking_details | GET | booking_details.html | booking (dict), movie (dict), showtime (dict)
- booking fields: booking_id (int), customer_name (str), customer_email (str), booking_date (str), total_price (float), status (str), seats_booked (list of str)
- movie fields: movie_id (int), title (str)
- showtime fields: showtime_id (int), showtime_date (str), showtime_time (str), theater_name (str) |
| /theaters | theater_information | GET | theater_information.html | theaters (list of dict)
- theaters fields: theater_id (int), theater_name (str), location (str), city (str), screens (int), facilities (str) |

---

# Section 2: HTML Template Specifications

## 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Movie Ticketing Dashboard (for both <title> and <h1>)
- Element IDs:
  - dashboard-page (Div): Container for dashboard
  - featured-movies (Div): Display featured movie recommendations
  - browse-movies-button (Button): Navigates to movie_catalog route
  - view-bookings-button (Button): Navigates to booking_history route
  - showtimes-button (Button): Navigates to select_showtime page with movie selection (or landing)
- Navigation Mapping:
  - browse-movies-button -> 'movie_catalog'
  - view-bookings-button -> 'booking_history'
  - showtimes-button -> 'select_showtime' (with movie selection or general showtimes listing)

## 2. Movie Catalog Page
- Filename: templates/catalog.html
- Page Title: Movie Catalog
- Element IDs:
  - catalog-page (Div): Container
  - search-input (Input): Search input for movies by title or genre
  - genre-filter (Dropdown): Filter by genre
  - movies-grid (Div): Displays movie cards
  - view-movie-button-{movie_id} (Button): Button on each movie card to view its details
- Navigation Mapping:
  - view-movie-button-{movie_id} -> 'movie_details', with movie_id param

## 3. Movie Details Page
- Filename: templates/movie_details.html
- Page Title: Movie Details
- Element IDs:
  - movie-details-page (Div): Container
  - movie-title (H1): Movie title display
  - movie-director (Div): Director display
  - movie-rating (Div): Rating display
  - movie-description (Div): Description display
  - select-showtime-button (Button): Proceed to showtimes for that movie
- Navigation Mapping:
  - select-showtime-button -> 'select_showtime' with movie_id param

## 4. Showtime Selection Page
- Filename: templates/showtime_selection.html
- Page Title: Select Showtime
- Element IDs:
  - showtime-page (Div): Container
  - showtimes-list (Div): List of available showtimes
  - theater-filter (Dropdown): Filter showtimes by theater
  - date-filter (Input): Filter showtimes by date
  - select-showtime-button-{showtime_id} (Button): Button to select specific showtime
- Navigation Mapping:
  - select-showtime-button-{showtime_id} -> 'seat_selection' with showtime_id param

## 5. Seat Selection Page
- Filename: templates/seat_selection.html
- Page Title: Select Seats
- Element IDs:
  - seat-selection-page (Div): Container
  - seat-map (Div): Interactive seat map
  - selected-seats-display (Div): Shows currently selected seats
  - seat-{row}{col} (Button): Buttons representing seats by row and column
  - proceed-booking-button (Button): Proceed to booking confirmation
- Navigation Mapping:
  - proceed-booking-button -> 'booking_confirmation'

## 6. Booking Confirmation Page
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Element IDs:
  - confirmation-page (Div): Container
  - booking-summary (Div): Booking details summary
  - customer-name (Input): Input for customer name
  - customer-email (Input): Input for customer email
  - confirm-booking-button (Button): Confirm and complete booking
- Navigation Mapping:
  - confirm-booking-button -> POST to 'booking_confirmation'

## 7. Booking History Page
- Filename: templates/booking_history.html
- Page Title: Booking History
- Element IDs:
  - bookings-page (Div): Container
  - bookings-table (Table): Table displaying bookings
  - view-booking-button-{booking_id} (Button): Button to view booking details
  - status-filter (Dropdown): Filter bookings by status
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation Mapping:
  - view-booking-button-{booking_id} -> 'booking_details' with booking_id param
  - back-to-dashboard -> 'dashboard'

## 8. Theater Information Page
- Filename: templates/theater_information.html
- Page Title: Theater Information
- Element IDs:
  - theater-page (Div): Container
  - theaters-list (Div): List of theaters
  - theater-location-filter (Dropdown): Filter theaters by location
  - facilities-display (Div): Show facilities and amenities
  - back-to-dashboard (Button): Navigate back to dashboard
- Navigation Mapping:
  - back-to-dashboard -> 'dashboard'

---

# Section 3: Data File Schemas

## 1. movies.txt
- Path: data/movies.txt
- Fields (pipe-separated): movie_id|title|director|genre|rating|duration|description|release_date
- Description: Stores all movie records with detailed information.
- Examples:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

## 2. theaters.txt
- Path: data/theaters.txt
- Fields (pipe-separated): theater_id|theater_name|location|city|screens|facilities
- Description: Stores information about theaters and their facilities.
- Examples:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

## 3. showtimes.txt
- Path: data/showtimes.txt
- Fields (pipe-separated): showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Stores showtime listings for movies in theaters.
- Examples:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

## 4. seats.txt
- Path: data/seats.txt
- Fields (pipe-separated): seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Stores seat details and booking status for theater screens.
- Examples:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

## 5. bookings.txt
- Path: data/bookings.txt
- Fields (pipe-separated): booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Stores booking records with customer details and booked seats.
- Examples:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

## 6. genres.txt
- Path: data/genres.txt
- Fields (pipe-separated): genre_id|genre_name|description
- Description: Stores movie genre definitions and descriptions.
- Examples:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
