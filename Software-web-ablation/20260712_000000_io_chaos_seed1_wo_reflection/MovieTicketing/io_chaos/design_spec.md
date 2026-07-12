# Design Specification for MovieTicketing Application

---

## Section 1: Flask Routes Specification

| Route Path                  | Function Name            | HTTP Method | Template                | Context Variables (Type)                                                                               |
|-----------------------------|--------------------------|-------------|-------------------------|-------------------------------------------------------------------------------------------------------|
| /                           | root_redirect             | GET         | None (redirect to dashboard)                 | None                                                                                                |
| /dashboard                  | dashboard                | GET         | dashboard.html          | featured_movies (list of dict with fields: movie_id(int), title(str), poster_url(str)), etc. not explicitly detailed in requirements here |
| /movies                    | movie_catalog            | GET         | movie_catalog.html      | movies (list of dict with fields: movie_id(int), title(str), genre(str), rating(float), duration(int), poster_url(str))                         |
| /movies/<int:movie_id>      | movie_details            | GET         | movie_details.html      | movie (dict with fields: movie_id(int), title(str), director(str), rating(float), description(str))                                                 |
| /movies/<int:movie_id>/showtimes | showtime_selection    | GET         | showtime_selection.html | showtimes (list of dict with: showtime_id(int), date(str), time(str), theater_name(str), price(float))                                                 |
| /showtimes/<int:showtime_id>/seats | seat_selection       | GET         | seat_selection.html     | seat_map (list of dict with seat_id(str), status(str)), selected_seats (list of str)                                                                   |
| /showtimes/<int:showtime_id>/seats | seat_selection_post  | POST        | seat_selection.html     | errors (str), seat_map (list of dict), selected_seats (list of str) (in case of errors, re-render)                                                |
| /booking/confirm            | booking_confirmation      | GET         | booking_confirmation.html| booking_summary (dict: movie(str), showtime(str), seats(list of str), total(float))                                                                   |
| /booking/confirm            | booking_confirmation_post | POST        | booking_confirmation.html| confirmation_status (str) or errors (str)                                                                                                     |
| /bookings                  | booking_history           | GET         | booking_history.html    | bookings (list of dict with fields: booking_id(int), movie(str), date(str), seats(str), status(str))                                              |
| /bookings/<int:booking_id> | booking_details           | GET         | booking_details.html    | booking (dict with booking details)                                                                                                            |
| /theaters                  | theater_information       | GET         | theater_information.html| theaters (list of dict: theater_id(int), name(str), location(str), screens(int), facilities(str))                                                    |

Note: The above routes capture all main pages plus dynamic routes for movies, showtimes, seats, bookings.


## Section 2: HTML Template Specifications

### dashboard.html
- Title: Movie Ticketing Dashboard
- H1: Movie Ticketing Dashboard
- Elements:
  - dashboard-page (Div): container for dashboard
  - featured-movies (Div): display featured movies
  - browse-movies-button (Button): navigates to movie_catalog
  - view-bookings-button (Button): navigates to booking_history
  - showtimes-button (Button): navigates to showtime_selection root or a general showtimes page if exists

### movie_catalog.html
- Title: Movie Catalog
- H1: Movie Catalog
- Elements:
  - catalog-page (Div): container for catalog
  - search-input (Input): search movies by title or genre
  - genre-filter (Dropdown): filter by genre
  - movies-grid (Div): grid to display movie cards
  - view-movie-button-{movie_id} (Button): view movie details, dynamic id by movie_id

### movie_details.html
- Title: Movie Details
- H1: Movie Details
- Elements:
  - movie-details-page (Div): container
  - movie-title (H1): display movie title
  - movie-director (Div): display movie director
  - movie-rating (Div): display movie rating
  - movie-description (Div): display description
  - select-showtime-button (Button): proceed to showtime selection

### showtime_selection.html
- Title: Select Showtime
- H1: Select Showtime
- Elements:
  - showtime-page (Div): container
  - showtimes-list (Div): list showtimes with date, time, theater, price
  - theater-filter (Dropdown): filter showtimes by theater
  - date-filter (Input): filter showtimes by date
  - select-showtime-button-{showtime_id} (Button): select this showtime, dynamic id

### seat_selection.html
- Title: Select Seats
- H1: Select Seats
- Elements:
  - seat-selection-page (Div): container
  - seat-map (Div): interactive seat map
  - selected-seats-display (Div): display selected seats
  - seat-{row}{col} (Button): individual seats, dynamic ids
  - proceed-booking-button (Button): proceed to booking confirmation

### booking_confirmation.html
- Title: Booking Confirmation
- H1: Booking Confirmation
- Elements:
  - confirmation-page (Div): container
  - booking-summary (Div): summary of booking
  - customer-name (Input): customer name input
  - customer-email (Input): customer email input
  - confirm-booking-button (Button): confirm and complete booking

### booking_history.html
- Title: Booking History
- H1: Booking History
- Elements:
  - bookings-page (Div): container
  - bookings-table (Table): displays bookings
  - view-booking-button-{booking_id} (Button): view booking details, dynamic id
  - status-filter (Dropdown): filter by status
  - back-to-dashboard (Button): navigate back

### theater_information.html
- Title: Theater Information
- H1: Theater Information
- Elements:
  - theater-page (Div): container
  - theaters-list (Div): list theaters
  - theater-location-filter (Dropdown): filter theaters
  - facilities-display (Div): display facilities
  - back-to-dashboard (Button): navigate back


## Section 3: Data File Schemas

### movies.txt (data/movies.txt)
- Fields: movie_id|title|director|genre|rating|duration|description|release_date
- Description: Movie details including title, director, genre, rating, duration in minutes, description, and release date
- Example Rows:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### theaters.txt (data/theaters.txt)
- Fields: theater_id|theater_name|location|city|screens|facilities
- Description: Theater details including location, number of screens and facilities
- Example Rows:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### showtimes.txt (data/showtimes.txt)
- Fields: showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Showtimes for movies at various theaters showing date, time, and pricing
- Example Rows:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### seats.txt (data/seats.txt)
- Fields: seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Seat layout with type and booking status
- Example Rows:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### bookings.txt (data/bookings.txt)
- Fields: booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Booking records with customer info and booked seats
- Example Rows:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### genres.txt (data/genres.txt)
- Fields: genre_id|genre_name|description
- Description: Different movie genres with descriptions
- Example Rows:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---