# MovieTicketing Application Design Specification

## Section 1: Flask Routes Specification

| Route Path                  | Function Name            | HTTP Method | Template Rendered           | Context Variables Passed                                         |
|-----------------------------|--------------------------|-------------|-----------------------------|------------------------------------------------------------------|
| /                           | root_redirect             | GET         | None (redirect to /dashboard) | None                                                             |
| /dashboard                  | dashboard                | GET         | dashboard.html              | featured_movies (list of dict: movie_id:int, title:str, poster:str, rating:float), upcoming_releases (list of dict: movie_id:int, title:str, release_date:str) |
| /movies                    | movie_catalog            | GET         | catalog.html                | movies (list of dict: movie_id:int, title:str, genre:str, rating:float, duration:int, poster:str), genres (list of dict: genre_name:str)  |
| /movies/<int:movie_id>      | movie_details            | GET         | movie_details.html          | movie (dict: movie_id:int, title:str, director:str, genre:str, rating:float, duration:int, description:str, release_date:str)             |
| /showtimes/<int:movie_id>   | showtime_selection       | GET         | showtimes.html              | movie_id (int), showtimes (list of dict: showtime_id:int, theater_name:str, theater_id:int, showtime_date:str, showtime_time:str, price:float) , theaters (list of dict: theater_id:int, theater_name:str) |
| /seats/<int:showtime_id>    | seat_selection           | GET         | seat_selection.html         | showtime (dict: showtime_id:int, movie_id:int, theater_id:int, showtime_date:str, showtime_time:str, price:float), available_seats (int), seats (list of dict: seat_id:int, row:str, column:int, seat_type:str, status:str), selected_seats (list of str) |
| /booking/confirm            | booking_confirmation      | GET, POST  | confirmation.html           | If GET: booking_details (dict: movie:str, showtime_date:str, showtime_time:str, theater_name:str, seats (list of str), total_price:float)
If POST: success (bool), error_message (str) |
| /bookings                  | booking_history           | GET         | bookings.html               | bookings (list of dict: booking_id:int, movie:str, date:str, seats (list of str), status:str)                                |
| /bookings/<int:booking_id>  | view_booking_details      | GET         | booking_details.html        | booking (dict: booking_id:int, showtime_id:int, customer_name:str, customer_email:str, booking_date:str, total_price:float, status:str, seats_booked (list of str)) |
| /theaters                  | theater_information       | GET         | theater.html                | theaters (list of dict: theater_id:int, theater_name:str, location:str, city:str, screens:int, facilities:str)                 |

Notes:
- Root route '/' redirects to /dashboard handled by function root_redirect.
- All dynamic route parameters use <int:id> where applicable.
- POST method only on /booking/confirm for booking submission.

---

## Section 2: HTML Template Specifications

### templates/dashboard.html
- Page Title (<title> and <h1>): "Movie Ticketing Dashboard"
- Element IDs:
  - dashboard-page (Div): Container for dashboard page.
  - featured-movies (Div): Displays featured movie recommendations.
  - browse-movies-button (Button): Navigates to movie_catalog function.
  - view-bookings-button (Button): Navigates to booking_history function.
  - showtimes-button (Button): Navigates to showtime_selection - alternatively leads to showtimes page root or allow movie selection if needed.

### templates/catalog.html
- Page Title (<title> and <h1>): "Movie Catalog"
- Element IDs:
  - catalog-page (Div): Container for catalog page.
  - search-input (Input): Text input for searching by title or genre.
  - genre-filter (Dropdown): Filter movies by genre.
  - movies-grid (Div): Grid displaying movie cards.
  - view-movie-button-{movie_id} (Button): Button to view details, dynamic ID suffixed by movie_id.

- Navigation:
  - browse-movies-button: (not here but from dashboard) navigates to movie_catalog
  - view-movie-button-{movie_id}: links to movie_details(movie_id)

### templates/movie_details.html
- Page Title: "Movie Details"
- Element IDs:
  - movie-details-page (Div): Container for page.
  - movie-title (H1): Movie title display.
  - movie-director (Div): Director name.
  - movie-rating (Div): Movie rating.
  - movie-description (Div): Movie description.
  - select-showtime-button (Button): Navigate to showtime_selection(movie_id)

### templates/showtimes.html
- Page Title: "Select Showtime"
- Element IDs:
  - showtime-page (Div): Container for showtime page.
  - showtimes-list (Div): List of showtimes.
  - theater-filter (Dropdown): Filter by theater.
  - date-filter (Input): Filter by date.
  - select-showtime-button-{showtime_id} (Button): Select specific showtime, ID dynamic by showtime_id.

### templates/seat_selection.html
- Page Title: "Select Seats"
- Element IDs:
  - seat-selection-page (Div): Container.
  - seat-map (Div): Interactive seat buttons.
  - selected-seats-display (Div): Shows selected seats.
  - seat-{row}{col} (Button): Dynamic seat buttons, e.g. seat-A1.
  - proceed-booking-button (Button): Proceed to booking confirmation page.

### templates/confirmation.html
- Page Title: "Booking Confirmation"
- Element IDs:
  - confirmation-page (Div): Container.
  - booking-summary (Div): Summary of booking details.
  - customer-name (Input): Customer name input.
  - customer-email (Input): Customer email input.
  - confirm-booking-button (Button): Button to submit booking.

### templates/bookings.html
- Page Title: "Booking History"
- Element IDs:
  - bookings-page (Div): Container.
  - bookings-table (Table): Display table of bookings.
  - view-booking-button-{booking_id} (Button): View booking details, dynamic ID.
  - status-filter (Dropdown): Filter bookings by status.
  - back-to-dashboard (Button): Navigate to dashboard function.

### templates/booking_details.html
- Page Title: "Booking Details"
- Element IDs:
  - booking-details-page (Div): Container (assumed, not explicitly in requirements but logical)
  - detailed booking info presented (movie, seats, status, customer info) in structured divs or tables with appropriate IDs as required by frontend

### templates/theater.html
- Page Title: "Theater Information"
- Element IDs:
  - theater-page (Div): Container.
  - theaters-list (Div): List of theaters.
  - theater-location-filter (Dropdown): Filter by location.
  - facilities-display (Div): Shows facilities and amenities.
  - back-to-dashboard (Button): Navigate to dashboard function.

Navigation Summary:
- From dashboard, buttons to movie_catalog, booking_history, showtime_selection.
- From catalog, buttons to movie_details.
- From movie_details, button to showtime_selection.
- From showtimes, buttons to seat_selection.
- From seat_selection, button to booking_confirmation.
- From booking_confirmation submit to /booking/confirm POST.
- From booking_history, view booking details or back to dashboard.
- From theater info, back to dashboard.

---

## Section 3: Data File Schemas

### data/movies.txt
- Fields (pipe-delimited):
  movie_id|title|director|genre|rating|duration|description|release_date
- Description: Stores movie information including metadata and description.
- Examples:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### data/theaters.txt
- Fields (pipe-delimited):
  theater_id|theater_name|location|city|screens|facilities
- Description: Information about theaters including location and available facilities.
- Examples:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### data/showtimes.txt
- Fields (pipe-delimited):
  showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Showtime schedules for movies at theaters.
- Examples:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### data/seats.txt
- Fields (pipe-delimited):
  seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Seat layout and booking status per theater and screen.
- Examples:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### data/bookings.txt
- Fields (pipe-delimited):
  booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Booking records including customer and seat data.
- Examples:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### data/genres.txt
- Fields (pipe-delimited):
  genre_id|genre_name|description
- Description: Movie genre definitions.
- Examples:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---

This specification document completely defines the Flask routes, HTML template structures, and data file schemas to enable independent backend and frontend team development for the MovieTicketing application.