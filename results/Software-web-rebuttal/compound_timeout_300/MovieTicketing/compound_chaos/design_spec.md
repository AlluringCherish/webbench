# MovieTicketing Application Design Specification

---

## 1. Flask Routes Specification

| Route Path                 | Function Name           | HTTP Method(s) | Template Rendered            | Context Variables (Name: Type and Description)                                   |
|----------------------------|------------------------|----------------|------------------------------|----------------------------------------------------------------------------------|
| /                          | root_redirect          | GET            | None (Redirect to /dashboard) | None                                                                             |
| /dashboard                 | dashboard_page         | GET            | dashboard.html               | featured_movies: list of dict (movie_id: int, title: str, poster_url: str, rating: float, duration: int), upcoming_releases: list of dict (same structure), navigation_links: dict (browse_movies: str, booking_history: str, showtimes: str) |
| /movies                    | movie_catalog          | GET            | movie_catalog.html           | movies: list of dict (movie_id: int, title: str, poster_url: str, rating: float, duration: int, genre: str), genres: list of str (genre names) |
| /movies/<int:movie_id>     | movie_details          | GET            | movie_details.html           | movie: dict (movie_id: int, title: str, director: str, rating: float, description: str, duration: int, genre: str, release_date: str "YYYY-MM-DD") |
| /showtimes/<int:movie_id>  | showtime_selection     | GET            | showtime_selection.html      | showtimes: list of dict (showtime_id: int, theater_name: str, showtime_date: str "YYYY-MM-DD", showtime_time: str "HH:MM", price: float), theaters: list of dict (theater_id: int, theater_name: str), filters: dict (selected_theater_id: int or None, selected_date: str or None) |
| /select-seats/<int:showtime_id> | seat_selection   | GET            | seat_selection.html          | seats: list of dict (seat_id: int, row: str, column: int, seat_type: str, status: str [Available|Booked]), selected_seats: list of str (seat IDs, e.g. "A1"), showtime_info: dict (showtime_id: int, movie_title: str, theater_name: str, showtime_date: str, showtime_time: str) |
| /booking-confirmation/<int:showtime_id> | booking_confirmation | GET, POST | booking_confirmation.html   | showtime_info: dict (showtime_id: int, movie_title: str, theater_name: str, showtime_date: str, showtime_time: str, price: float), selected_seats: list of str; on POST receives form data: customer_name: str, customer_email: str |
| /bookings                  | booking_history        | GET            | booking_history.html         | bookings: list of dict (booking_id: int, movie_title: str, booking_date: str, seats_booked: list of str seat codes (e.g. "A1"), status: str), status_filter_options: list of str (All, Confirmed, Cancelled, Completed) |
| /bookings/<int:booking_id> | booking_details        | GET            | booking_detail.html          | booking: dict (booking_id: int, showtime_id: int, movie_title: str, customer_name: str, customer_email: str, booking_date: str, total_price: float, status: str, seats_booked: list of str) |
| /theaters                  | theater_info           | GET            | theater_info.html            | theaters: list of dict (theater_id: int, theater_name: str, location: str, city: str, screens: int, facilities: list of str), location_filter_options: list of str |

### Notes:
- Root route `/` redirects (HTTP 302) to `/dashboard` handled by function `root_redirect`.
- Route `/movies/<int:movie_id>` expects valid movie_id.
- Route `/showtimes/<int:movie_id>` filters showtimes of given movie.
- Route `/select-seats/<int:showtime_id>` provides seat map for the selected showtime.
- Booking confirmation supports GET (display) and POST (submission).
- Booking details page `/bookings/<booking_id>` to view specific booking record.

---

## 2. HTML Template Specifications

### templates/dashboard.html
- Page Title: "Movie Ticketing Dashboard"
- Main H1: "Movie Ticketing Dashboard"
- HTML Element IDs:
  - dashboard-page: Div; Container for dashboard page
  - featured-movies: Div; Display of featured movies
  - browse-movies-button: Button; Navigates to movie catalog page (url_for('movie_catalog'))
  - view-bookings-button: Button; Navigates to booking history page (url_for('booking_history'))
  - showtimes-button: Button; Navigates to showtime selection general page or initial page (could link to /showtimes/<some_movie_id> or to movie catalog if not specified)

### templates/movie_catalog.html
- Page Title: "Movie Catalog"
- Main H1: "Movie Catalog"
- HTML Element IDs:
  - catalog-page: Div; Container for catalog
  - search-input: Input; Text input for movie title or genre search
  - genre-filter: Dropdown select; For filtering movies by genre (options from genres context variable)
  - movies-grid: Div; Grid container for movie cards
  - Dynamic button IDs: view-movie-button-{movie_id}: Button; Each movie card's "View Details" button links to route url_for('movie_details', movie_id=movie_id)

### templates/movie_details.html
- Page Title: "Movie Details"
- Main H1: "Movie Details"
- HTML Element IDs:
  - movie-details-page: Div; Container for movie details
  - movie-title: H1; Displays movie title
  - movie-director: Div; Displays movie director
  - movie-rating: Div; Displays movie rating
  - movie-description: Div; Displays movie description
  - select-showtime-button: Button; Navigates to showtime selection page for this movie (url_for('showtime_selection', movie_id=movie.movie_id))

### templates/showtime_selection.html
- Page Title: "Select Showtime"
- Main H1: "Select Showtime"
- HTML Element IDs:
  - showtime-page: Div; Container for showtime selection
  - showtimes-list: Div; List or table of showtimes each with date, time, theater, and price
  - theater-filter: Dropdown; Filter showtimes by theater (options from theaters list)
  - date-filter: Input (date type); Filter showtimes by date
  - Dynamic button IDs: select-showtime-button-{showtime_id}: Button; To select each showtime, navigates to seat selection (url_for('seat_selection', showtime_id=showtime_id))

### templates/seat_selection.html
- Page Title: "Select Seats"
- Main H1: "Select Seats"
- HTML Element IDs:
  - seat-selection-page: Div; Container for seat selection
  - seat-map: Div; Interactive seat map with seat buttons
  - Dynamic seat button IDs: seat-{row}{col} (e.g., seat-A1): Button; Individual seat buttons
  - selected-seats-display: Div; Shows currently selected seats
  - proceed-booking-button: Button; Proceed to booking confirmation (url_for('booking_confirmation', showtime_id=showtime_id))

### templates/booking_confirmation.html
- Page Title: "Booking Confirmation"
- Main H1: "Booking Confirmation"
- HTML Element IDs:
  - confirmation-page: Div; Container for confirmation
  - booking-summary: Div; Summary of booking, including movie, showtime, seats, total price
  - customer-name: Input (text); User inputs name
  - customer-email: Input (email); User inputs email
  - confirm-booking-button: Button; Submits booking confirmation form

### templates/booking_history.html
- Page Title: "Booking History"
- Main H1: "Booking History"
- HTML Element IDs:
  - bookings-page: Div; Container for bookings page
  - bookings-table: Table; Displays bookings with columns: Booking ID, Movie, Date, Seats, Status
  - status-filter: Dropdown; Filter bookings by status (options: All, Confirmed, Cancelled, Completed)
  - Dynamic button IDs: view-booking-button-{booking_id}: Button; View details for each booking (url_for('booking_details', booking_id=booking_id))
  - back-to-dashboard: Button; Navigate back to dashboard (url_for('dashboard_page'))

### templates/booking_detail.html
- Page Title: "Booking Details"
- Main H1: "Booking Details"
- HTML Element IDs:
  - booking-detail-page: Div; Container for booking detail
  - booking-info: Div; Detailed information about the booking
  - back-to-bookings: Button; Navigate back to booking history (url_for('booking_history'))

### templates/theater_info.html
- Page Title: "Theater Information"
- Main H1: "Theater Information"
- HTML Element IDs:
  - theater-page: Div; Container for theater information
  - theaters-list: Div; List all theaters
  - theater-location-filter: Dropdown; Filter theaters by location (cities available from theaters data)
  - facilities-display: Div; Show facilities for selected theater
  - back-to-dashboard: Button; Navigate back to dashboard (url_for('dashboard_page'))

---

## 3. Data File Schemas

### data/movies.txt
- Path: data/movies.txt
- Format (pipe-delimited, no headers):
  movie_id|title|director|genre|rating|duration|description|release_date

- Description: Lists all movies with their attributes.
- Example rows:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### data/theaters.txt
- Path: data/theaters.txt
- Format: 
  theater_id|theater_name|location|city|screens|facilities

- Description: Contains theater details including facilities as comma-separated string.
- Example rows:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### data/showtimes.txt
- Path: data/showtimes.txt
- Format:
  showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats

- Description: Showtimes for movies with availability and pricing.
- Example rows:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### data/seats.txt
- Path: data/seats.txt
- Format:
  seat_id|theater_id|screen_id|row|column|seat_type|status

- Description: Seat layout by theater and screen with status (Available or Booked).
- Example rows:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### data/bookings.txt
- Path: data/bookings.txt
- Format:
  booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked

- Description: Booking records with associated seats booked as comma-separated seat codes.
- Example rows:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### data/genres.txt
- Path: data/genres.txt
- Format:
  genre_id|genre_name|description

- Description: Genre definitions with descriptions.
- Example rows:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---

# End of design_spec.md
