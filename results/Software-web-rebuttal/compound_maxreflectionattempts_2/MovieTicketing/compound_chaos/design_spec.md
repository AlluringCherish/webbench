# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name              | HTTP Methods | Template Rendered          | Context Variables (name: type)                                           | Context Variable Details                                                                                              |
|--------------------------------|----------------------------|--------------|----------------------------|-------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| `/`                            | root_redirect               | GET          | None (redirect)             | None                                                                    | Redirects to dashboard route `/dashboard`                                                                            |
| `/dashboard`                   | dashboard_page             | GET          | dashboard.html             | `featured_movies: list[dict]`, `upcoming_releases: list[dict]`          | Each dict in lists: {movie_id: int, title: str, poster_url: str} or other minimal details for display                  |
| `/movies`                     | movie_catalog              | GET          | movie_catalog.html         | `movies: list[dict]`, `genres: list[str]`, `search_query: str`, `selected_genre: str` | movies dict: {movie_id: int, title: str, genre: str, rating: float, duration: int, poster_url: str}                      |
| `/movies/<int:movie_id>`       | movie_details              | GET          | movie_details.html         | `movie: dict`                                                           | movie dict: {movie_id: int, title: str, director: str, genre: str, rating: float, duration: int, description: str, release_date: str}
| `/movies/<int:movie_id>/showtimes` | select_showtime            | GET          | select_showtime.html       | `movie: dict`, `showtimes: list[dict]`, `selected_theater: int or None`, `selected_date: str or None`, `theaters: list[dict]` | showtimes dict: {showtime_id: int, theater_id: int, showtime_date: str, showtime_time: str, price: float, available_seats: int}
| `/movies/<int:movie_id>/showtimes/select/<int:showtime_id>` | seat_selection           | GET          | seat_selection.html        | `showtime: dict`, `seats_map: list[dict]`                              | seats_map dict: {seat_id: int, row: str, column: int, seat_type: str, status: str}                                     |
| `/movies/<int:movie_id>/showtimes/select/<int:showtime_id>/booking` | booking_confirmation     | GET, POST    | booking_confirmation.html  | GET: `booking_details: dict`
POST: form data processing | booking_details dict: {movie_title: str, showtime_date: str, showtime_time: str, theater_name: str, seats_selected: list[str], total_price: float}
| `/bookings`                   | booking_history            | GET          | booking_history.html       | `bookings: list[dict]`, `status_filter: str`                          | bookings dict: {booking_id: int, movie_title: str, booking_date: str, seats_booked: list[str], status: str}             |
| `/bookings/<int:booking_id>`   | booking_details            | GET          | booking_details.html       | `booking: dict`                                                        | booking dict: {booking_id: int, movie_title: str, showtime_date: str, showtime_time: str, theater_name: str, seats_booked: list[str], total_price: float, status: str, customer_name: str, customer_email: str}
| `/theaters`                   | theater_information        | GET          | theater_information.html   | `theaters: list[dict]`, `selected_location: str or None`              | theaters dict: {theater_id: int, theater_name: str, location: str, city: str, screens: int, facilities: str}             |

---

## Section 2: HTML Template Specifications

### Template: dashboard.html
- Filename: templates/dashboard.html
- Page Title: "Movie Ticketing Dashboard"
- H1 Heading: "Movie Ticketing Dashboard"
- Element IDs:
  - dashboard-page (div) - container of dashboard page
  - featured-movies (div) - display featured movie recommendations
  - browse-movies-button (button) - navigate to movie_catalog
  - view-bookings-button (button) - navigate to booking_history
  - showtimes-button (button) - navigate to select_showtime landing (could redirect to select showtimes page or movies page)
- Navigation Mappings:
  - browse-movies-button: url_for('movie_catalog')
  - view-bookings-button: url_for('booking_history')
  - showtimes-button: url_for('select_showtime') (Note: needs target movie selection in practice; may redirect to movies or a showtime selection page.)

### Template: movie_catalog.html
- Filename: templates/movie_catalog.html
- Page Title: "Movie Catalog"
- H1 Heading: "Movie Catalog"
- Element IDs:
  - catalog-page (div) - container of movie catalog page
  - search-input (input) - search movies by title or genre
  - genre-filter (select) - filter by genre dropdown
  - movies-grid (div) - grid displaying movie cards
  - view-movie-button-{movie_id} (button) - on each movie card for viewing details
- Navigation Mappings:
  - view-movie-button-{movie_id}: url_for('movie_details', movie_id=movie_id)

### Template: movie_details.html
- Filename: templates/movie_details.html
- Page Title: "Movie Details"
- H1 Heading: "Movie Details"
- Element IDs:
  - movie-details-page (div) - container of movie details page
  - movie-title (h1) - displays movie title
  - movie-director (div) - displays movie director
  - movie-rating (div) - displays movie rating
  - movie-description (div) - displays movie description
  - select-showtime-button (button) - proceed to showtime selection
- Navigation Mappings:
  - select-showtime-button: url_for('select_showtime', movie_id=movie_id)

### Template: select_showtime.html
- Filename: templates/select_showtime.html
- Page Title: "Select Showtime"
- H1 Heading: "Select Showtime"
- Element IDs:
  - showtime-page (div) - container of showtime selection page
  - showtimes-list (div) - list of available showtimes
  - theater-filter (select) - filter showtimes by theater
  - date-filter (input) - filter showtimes by date
  - select-showtime-button-{showtime_id} (button) - select specific showtime
- Navigation Mappings:
  - select-showtime-button-{showtime_id}: url_for('seat_selection', movie_id=movie_id, showtime_id=showtime_id)

### Template: seat_selection.html
- Filename: templates/seat_selection.html
- Page Title: "Select Seats"
- H1 Heading: "Select Seats"
- Element IDs:
  - seat-selection-page (div) - container of seat selection page
  - seat-map (div) - interactive seat map
  - selected-seats-display (div) - display of selected seats
  - seat-{row}{col} (button) - individual seat buttons (e.g., seat-A1)
  - proceed-booking-button (button) - proceed to booking confirmation
- Navigation Mappings:
  - proceed-booking-button: url_for('booking_confirmation', movie_id=movie_id, showtime_id=showtime_id)

### Template: booking_confirmation.html
- Filename: templates/booking_confirmation.html
- Page Title: "Booking Confirmation"
- H1 Heading: "Booking Confirmation"
- Element IDs:
  - confirmation-page (div) - container of booking confirmation page
  - booking-summary (div) - summary of booking details
  - customer-name (input) - customer name input
  - customer-email (input) - customer email input
  - confirm-booking-button (button) - confirm and complete booking
- Navigation Mappings:
  - confirm-booking-button: submits POST to url_for('booking_confirmation', movie_id=movie_id, showtime_id=showtime_id)

### Template: booking_history.html
- Filename: templates/booking_history.html
- Page Title: "Booking History"
- H1 Heading: "Booking History"
- Element IDs:
  - bookings-page (div) - container of booking history page
  - bookings-table (table) - table displaying bookings
  - view-booking-button-{booking_id} (button) - view booking details
  - status-filter (select) - filter bookings by status
  - back-to-dashboard (button) - navigate back to dashboard
- Navigation Mappings:
  - view-booking-button-{booking_id}: url_for('booking_details', booking_id=booking_id)
  - back-to-dashboard: url_for('dashboard_page')

### Template: booking_details.html
- Filename: templates/booking_details.html
- Page Title: "Booking Details"
- H1 Heading: "Booking Details"
- Element IDs:
  - booking-details-page (div) - container for booking details
  - booking-id (div) - shows booking ID
  - movie-title (div) - shows movie title
  - showtime-date (div) - shows showtime date
  - showtime-time (div) - shows showtime time
  - theater-name (div) - shows theater name
  - seats-booked (div) - shows seats booked
  - total-price (div) - shows total booking price
  - status (div) - shows booking status
  - customer-name (div) - shows customer name
  - customer-email (div) - shows customer email
  - back-to-bookings (button) - navigates back to booking history
- Navigation Mappings:
  - back-to-bookings: url_for('booking_history')

### Template: theater_information.html
- Filename: templates/theater_information.html
- Page Title: "Theater Information"
- H1 Heading: "Theater Information"
- Element IDs:
  - theater-page (div) - container of theater information page
  - theaters-list (div) - list of all theaters
  - theater-location-filter (select) - filter theaters by location
  - facilities-display (div) - display theater facilities and amenities
  - back-to-dashboard (button) - navigate back to dashboard
- Navigation Mappings:
  - back-to-dashboard: url_for('dashboard_page')

---

## Section 3: Data File Schemas

### data/movies.txt
- Fields (pipe `|` delimited):
  `movie_id|title|director|genre|rating|duration|description|release_date`
- Description: Stores movie details including metadata and synopsis.
- Examples:
  ```
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23
  ```

### data/theaters.txt
- Fields (pipe `|` delimited):
  `theater_id|theater_name|location|city|screens|facilities`
- Description: Stores theaters with their details and amenities.
- Examples:
  ```
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge
  ```

### data/showtimes.txt
- Fields (pipe `|` delimited):
  `showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats`
- Description: Stores scheduled showtimes per movie and theater.
- Examples:
  ```
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95
  ```

### data/seats.txt
- Fields (pipe `|` delimited):
  `seat_id|theater_id|screen_id|row|column|seat_type|status`
- Description: Stores seat layout, types, and booking status per theater screen.
- Examples:
  ```
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked
  ```

### data/bookings.txt
- Fields (pipe `|` delimited):
  `booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked`
- Description: Stores completed bookings with customers and seat info.
- Examples:
  ```
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4
  ```

### data/genres.txt
- Fields (pipe `|` delimited):
  `genre_id|genre_name|description`
- Description: Stores movie genres and their descriptions.
- Examples:
  ```
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
  ```

---

*End of design_spec.md*