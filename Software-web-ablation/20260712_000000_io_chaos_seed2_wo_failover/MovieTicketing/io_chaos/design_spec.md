# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                       | Function Name           | HTTP Method | Template Rendered          | Context Variables (type and description)                     |
|---------------------------------|-------------------------|-------------|----------------------------|---------------------------------------------------------------|
| /                               | root_redirect           | GET         | N/A (Redirect to /dashboard)| None                                                          |
| /dashboard                      | dashboard_page          | GET         | dashboard.html             | featured_movies (list of dict: {movie_id:int, title:str, genre:str, rating:float, duration:int}), upcoming_releases (list of dict: same structure as featured_movies) |
| /movies                        | movie_catalog           | GET         | movie_catalog.html          | movies (list of dict: {movie_id:int, title:str, genre:str, rating:float, duration:int}), genres (list of dict: {genre_id:int, genre_name:str, description:str})  |
| /movies/<int:movie_id>          | movie_details           | GET         | movie_details.html          | movie (dict: {movie_id:int, title:str, director:str, genre:str, rating:float, duration:int, description:str, release_date:str})                            |
| /showtimes/select/<int:movie_id>| select_showtime        | GET         | showtime_selection.html    | showtimes (list of dict: {showtime_id:int, movie_id:int, theater_id:int, showtime_date:str, showtime_time:str, price:float, available_seats:int}), theaters (list of dict: {theater_id:int, theater_name:str, location:str, city:str, screens:int, facilities:str}) |
| /seats/select/<int:showtime_id> | seat_selection          | GET         | seat_selection.html        | seat_map (list of dict: {seat_id:int, theater_id:int, screen_id:int, row:str, column:int, seat_type:str, status:str}), selected_showtime (dict: {showtime_id:int, movie_id:int, theater_id:int, showtime_date:str, showtime_time:str, price:float}) |
| /booking/confirm/<int:showtime_id>| booking_confirmation  | GET         | booking_confirmation.html  | booking_summary (dict including movie title, showtime info, seats selected (list of str), total_price:float) |
| /booking/confirm/<int:showtime_id>| process_booking       | POST        | booking_confirmation.html  | form data: customer_name (str), customer_email (str)                         |
| /bookings                      | booking_history          | GET         | booking_history.html       | bookings (list of dict: {booking_id:int, showtime_id:int, customer_name:str, customer_email:str, booking_date:str, total_price:float, status:str, seats_booked:list of str}), filter_status_options (list of str) |
| /bookings/<int:booking_id>      | booking_details          | GET         | booking_details.html       | booking (dict: {booking_id:int, showtime_id:int, customer_name:str, customer_email:str, booking_date:str, total_price:float, status:str, seats_booked:list of str}), movie (dict of movie details) |
| /theaters                      | theater_information      | GET         | theater_information.html   | theaters (list of dict: {theater_id:int, theater_name:str, location:str, city:str, screens:int, facilities:str}), locations (list of str)                 |

---

## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- H1 Title: Movie Ticketing Dashboard
- Element IDs:
  - dashboard-page (Div): Container
  - featured-movies (Div): Displays featured movie recommendations
  - browse-movies-button (Button): Navigate to movie_catalog page
  - view-bookings-button (Button): Navigate to booking_history page
  - showtimes-button (Button): Navigate to showtime_selection or broader showtimes page
- Navigation mapping:
  - browse-movies-button -> movie_catalog (url_for('movie_catalog'))
  - view-bookings-button -> booking_history (url_for('booking_history'))
  - showtimes-button -> select_showtime (url_for('select_showtime', movie_id=some_default_or_first_movie_id))

### 2. templates/movie_catalog.html
- Page Title: Movie Catalog
- H1 Title: Movie Catalog
- Element IDs:
  - catalog-page (Div): Container
  - search-input (Input): Text input for searching movies by title or genre
  - genre-filter (Dropdown): Filter movies by genre
  - movies-grid (Div): Grid displaying movie cards
  - view-movie-button-{movie_id} (Button): Button to view movie details dynamic by movie_id
- Navigation mapping:
  - view-movie-button-{movie_id} -> movie_details (url_for('movie_details', movie_id=movie_id))

### 3. templates/movie_details.html
- Page Title: Movie Details
- H1 Title: Movie Details
- Element IDs:
  - movie-details-page (Div): Container
  - movie-title (H1): Displays movie title
  - movie-director (Div): Displays director
  - movie-rating (Div): Displays rating
  - movie-description (Div): Displays description
  - select-showtime-button (Button): Proceed to select_showtime page
- Navigation mapping:
  - select-showtime-button -> select_showtime (url_for('select_showtime', movie_id=movie.movie_id))

### 4. templates/showtime_selection.html
- Page Title: Select Showtime
- H1 Title: Select Showtime
- Element IDs:
  - showtime-page (Div): Container
  - showtimes-list (Div): List of showtimes
  - theater-filter (Dropdown): Filter showtimes by theater
  - date-filter (Input): Filter showtimes by date
  - select-showtime-button-{showtime_id} (Button): Select specific showtime
- Navigation mapping:
  - select-showtime-button-{showtime_id} -> seat_selection (url_for('seat_selection', showtime_id=showtime_id))

### 5. templates/seat_selection.html
- Page Title: Select Seats
- H1 Title: Select Seats
- Element IDs:
  - seat-selection-page (Div): Container
  - seat-map (Div): Interactive seat map
  - selected-seats-display (Div): Shows currently selected seats
  - seat-{row}{col} (Button): Individual seats, with row letter and column number
  - proceed-booking-button (Button): Proceed to booking confirmation
- Navigation mapping:
  - proceed-booking-button -> booking_confirmation (url_for('booking_confirmation', showtime_id=selected_showtime.showtime_id))

### 6. templates/booking_confirmation.html
- Page Title: Booking Confirmation
- H1 Title: Booking Confirmation
- Element IDs:
  - confirmation-page (Div): Container
  - booking-summary (Div): Summary display of booking details
  - customer-name (Input): Input for customer name
  - customer-email (Input): Input for customer email
  - confirm-booking-button (Button): Confirm booking action
- Navigation mapping:
  - confirm-booking-button -> process_booking (POST to url_for('process_booking', showtime_id=showtime_id))

### 7. templates/booking_history.html
- Page Title: Booking History
- H1 Title: Booking History
- Element IDs:
  - bookings-page (Div): Container
  - bookings-table (Table): Displays bookings with booking ID, movie, date, seats, status
  - view-booking-button-{booking_id} (Button): View booking details dynamically
  - status-filter (Dropdown): Filter bookings by status
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation mapping:
  - view-booking-button-{booking_id} -> booking_details (url_for('booking_details', booking_id=booking_id))
  - back-to-dashboard -> dashboard_page (url_for('dashboard_page'))

### 8. templates/theater_information.html
- Page Title: Theater Information
- H1 Title: Theater Information
- Element IDs:
  - theater-page (Div): Container
  - theaters-list (Div): List of theaters
  - theater-location-filter (Dropdown): Filter theaters by location
  - facilities-display (Div): Facilities of selected theater
  - back-to-dashboard (Button): Navigate to dashboard
- Navigation mapping:
  - back-to-dashboard -> dashboard_page (url_for('dashboard_page'))

---

## Section 3: Data File Schemas

### 1. data/movies.txt
- Fields (pipe-delimited):
  movie_id|title|director|genre|rating|duration|description|release_date
- Description: Stores movie details with unique IDs and metadata.
- Examples:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### 2. data/theaters.txt
- Fields (pipe-delimited):
  theater_id|theater_name|location|city|screens|facilities
- Description: Stores theater information including facilities.
- Examples:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### 3. data/showtimes.txt
- Fields (pipe-delimited):
  showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Stores showtime scheduling and pricing.
- Examples:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### 4. data/seats.txt
- Fields (pipe-delimited):
  seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Stores individual seat information and availability.
- Examples:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### 5. data/bookings.txt
- Fields (pipe-delimited):
  booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Stores booking records with seat details.
- Examples:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### 6. data/genres.txt
- Fields (pipe-delimited):
  genre_id|genre_name|description
- Description: Stores movie genre information.
- Examples:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

