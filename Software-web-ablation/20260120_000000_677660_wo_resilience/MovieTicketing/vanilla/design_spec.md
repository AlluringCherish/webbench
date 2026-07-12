# Design Specification Document for MovieTicketing Application

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name            | HTTP Method | Template Rendered           | Context Variables (type)                                                                                                                  |
|-------------------------------|--------------------------|-------------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect             | GET         | Redirect to /dashboard       | None                                                                                                                                    |
| /dashboard                    | dashboard                | GET         | dashboard.html              | featured_movies (list of dict), upcoming_releases (list of dict)                                                                         |
| /movies                      | movie_catalog            | GET         | movie_catalog.html          | movies (list of dict), genres (list of dict), selected_genre (str), search_query (str)                                                   |
| /movies/<int:movie_id>       | movie_details            | GET         | movie_details.html          | movie (dict), movie_id (int)                                                                                                            |
| /movies/<int:movie_id>/showtimes | showtime_selection        | GET         | showtime_selection.html     | movie (dict), showtimes (list of dict), theaters (list of dict), selected_theater (str), selected_date (str)                            |
| /showtimes/select             | showtime_select          | POST        | redirect (seat selection)   | form: showtime_id (int)                                                                                                                  |
| /seats/<int:showtime_id>     | seat_selection           | GET         | seat_selection.html         | showtime (dict), seats_map (list of dict), selected_seats (list of str)                                                                  |
| /booking/confirm             | booking_confirmation_get  | GET         | booking_confirmation.html   | showtime (dict), selected_seats (list of str), price_total (float)                                                                       |
| /booking/confirm             | booking_confirmation_post | POST        | redirect (booking history)  | form: customer_name (str), customer_email (str), showtime_id (int), selected_seats (list of str)                                          |
| /bookings                   | booking_history          | GET         | booking_history.html        | bookings (list of dict), status_filter (str)                                                                                            |
| /bookings/<int:booking_id>  | booking_details          | GET         | booking_details.html (not in requirements but implied) | booking (dict)                                                                                                                       |
| /theaters                   | theater_info             | GET         | theater_info.html           | theaters (list of dict), locations (list of str), selected_location (str)                                                                |
| /theaters/back-to-dashboard | back_to_dashboard        | GET         | redirect /dashboard          | None                                                                                                                                    |

---

### Context Variables Details:

- featured_movies (list of dict): Each dict => {movie_id (int), title (str), rating (float), poster_url (str)}
- upcoming_releases (list of dict): Each dict => {movie_id (int), title (str), release_date (str)}
- movies (list of dict): {movie_id (int), title (str), director (str), genre (str), rating (float), duration (int), description (str), release_date (str)}
- genres (list of dict): {genre_id (int), genre_name (str), description (str)}
- movie (dict): same structure as movies elements
- showtimes (list of dict): {showtime_id (int), movie_id (int), theater_id (int), showtime_date (str), showtime_time (str), price (float), available_seats (int)}
- theaters (list of dict): {theater_id (int), theater_name (str), location (str), city (str), screens (int), facilities (str)}
- selected_genre (str)
- search_query (str)
- selected_theater (str)
- selected_date (str) e.g. '2025-02-01'
- showtime (dict): one showtime dict from showtimes
- seats_map (list of dict): {seat_id (int), theater_id (int), screen_id (int), row (str), column (str), seat_type (str), status (str)}
- selected_seats (list of str) seat IDs e.g. ['A1', 'B4']
- bookings (list of dict): {booking_id (int), showtime_id (int), customer_name (str), customer_email (str), booking_date (str), total_price (float), status (str), seats_booked (str)}
- status_filter (str) One of ('All', 'Confirmed', 'Cancelled', 'Completed')
- booking (dict): one booking dict from bookings
- locations (list of str) distinct city/location list derived from theaters
- selected_location (str)

---

## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- Page Title: "Movie Ticketing Dashboard"
- <h1>: "Movie Ticketing Dashboard"
- Element IDs:
  - dashboard-page (Div): Container
  - featured-movies (Div): Display featured movie recommendations
  - browse-movies-button (Button): Navigate to movie_catalog route (movie_catalog)
  - view-bookings-button (Button): Navigate to booking_history route (booking_history)
  - showtimes-button (Button): Navigate to showtime_selection root route /showtimes (or /movies/<movie_id>/showtimes - but here just showtimes page may redirect to catalog or dashboard for selection)

### 2. templates/movie_catalog.html
- Page Title: "Movie Catalog"
- <h1>: "Movie Catalog"
- Element IDs:
  - catalog-page (Div): Container
  - search-input (Input): Search box by title or genre
  - genre-filter (Dropdown): Filter by genre
  - movies-grid (Div): Grid of movie cards
  - view-movie-button-{movie_id} (Button): View movie details for each movie_id
- Navigation Mapping:
  - browse-movies-button: links to movie_catalog (route: /movies)
  - view-movie-button-{movie_id}: links to movie_details(movie_id)

### 3. templates/movie_details.html
- Page Title: "Movie Details"
- <h1>: movie-title (dynamic, movie title)
- Element IDs:
  - movie-details-page (Div): Container
  - movie-title (H1): Movie title display
  - movie-director (Div): Director
  - movie-rating (Div): Rating
  - movie-description (Div): Description
  - select-showtime-button (Button): Proceed to showtime selection (/movies/<movie_id>/showtimes)

### 4. templates/showtime_selection.html
- Page Title: "Select Showtime"
- <h1>: "Select Showtime"
- Element IDs:
  - showtime-page (Div): Container
  - showtimes-list (Div): List of showtimes with details
  - theater-filter (Dropdown): Filter by theater
  - date-filter (Input): Filter by date
  - select-showtime-button-{showtime_id} (Button): Select specific showtime

### 5. templates/seat_selection.html
- Page Title: "Select Seats"
- <h1>: "Select Seats"
- Element IDs:
  - seat-selection-page (Div): Container
  - seat-map (Div): Interactive seat map showing available and booked seats
  - selected-seats-display (Div): Display selected seats
  - seat-{row}{col} (Button): Individual seat buttons (e.g. seat-A1, seat-B3)
  - proceed-booking-button (Button): Proceed to booking confirmation (/booking/confirm)

### 6. templates/booking_confirmation.html
- Page Title: "Booking Confirmation"
- <h1>: "Booking Confirmation"
- Element IDs:
  - confirmation-page (Div): Container
  - booking-summary (Div): Summary of booking details
  - customer-name (Input): Input customer name
  - customer-email (Input): Input customer email
  - confirm-booking-button (Button): Confirm and complete booking

### 7. templates/booking_history.html
- Page Title: "Booking History"
- <h1>: "Booking History"
- Element IDs:
  - bookings-page (Div): Container
  - bookings-table (Table): Displays booking ID, movie, date, seats, and status
  - view-booking-button-{booking_id} (Button): View booking details
  - status-filter (Dropdown): Filter bookings by status
  - back-to-dashboard (Button): Navigate back to dashboard (/dashboard)

### 8. templates/theater_info.html
- Page Title: "Theater Information"
- <h1>: "Theater Information"
- Element IDs:
  - theater-page (Div): Container
  - theaters-list (Div): List of theaters with location, screens, and facilities
  - theater-location-filter (Dropdown): Filter by location
  - facilities-display (Div): Display facilities and amenities
  - back-to-dashboard (Button): Navigate back to dashboard (/dashboard)

---

## Section 3: Data File Schemas

### 1. Movies Data
- File: data/movies.txt
- Fields (pipe-delimited in exact order):
  movie_id|title|director|genre|rating|duration|description|release_date
- Description: Contains movie details with ID, title, director, genre, rating (float), duration (minutes), description, and release date.
- Examples:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### 2. Theaters Data
- File: data/theaters.txt
- Fields (pipe-delimited in exact order):
  theater_id|theater_name|location|city|screens|facilities
- Description: Lists theater information including location, number of screens, and amenities.
- Examples:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### 3. Showtimes Data
- File: data/showtimes.txt
- Fields (pipe-delimited in exact order):
  showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Showtimes for movies at various theaters with prices and seat availability.
- Examples:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### 4. Seats Data
- File: data/seats.txt
- Fields (pipe-delimited in exact order):
  seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Seat details including location within theater, seat type, and current availability status.
- Examples:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### 5. Bookings Data
- File: data/bookings.txt
- Fields (pipe-delimited in exact order):
  booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Records of bookings with customer info, date, total price, status, and seats booked.
- Examples:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### 6. Genres Data
- File: data/genres.txt
- Fields (pipe-delimited in exact order):
  genre_id|genre_name|description
- Description: List of movie genres with descriptions.
- Examples:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---

*End of Design Specification*