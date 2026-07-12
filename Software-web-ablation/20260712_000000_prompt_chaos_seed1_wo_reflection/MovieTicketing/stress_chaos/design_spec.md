# Design Specification Document for MovieTicketing Application

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name             | HTTP Method | Template Rendered           | Context Variables Passed to Template                                   |
|--------------------------------|---------------------------|-------------|-----------------------------|------------------------------------------------------------------------|
| /                              | root_redirect             | GET         | None (Redirect to /dashboard) | None                                                                   |
| /dashboard                    | dashboard_page            | GET         | dashboard.html              | featured_movies (list of dict: movie_id(int), title(str), genre(str), rating(float), duration(int)), upcoming_releases (list of dict: movie_id(int), title(str), genre(str), release_date(str)) |
| /movies                       | movie_catalog             | GET         | movie_catalog.html          | movies (list of dict: movie_id(int), title(str), genre(str), rating(float), duration(int)) |
| /movies/<int:movie_id>        | movie_details             | GET         | movie_details.html          | movie (dict: movie_id(int), title(str), director(str), genre(str), rating(float), duration(int), description(str), release_date(str)) |
| /showtimes/select/<int:movie_id> | select_showtime           | GET         | showtime_selection.html     | showtimes (list of dict: showtime_id(int), theater_id(int), theater_name(str), showtime_date(str), showtime_time(str), price(float)), theaters (list of dict: theater_id(int), theater_name(str)) |
| /showtimes/select/<int:showtime_id>/seats | seat_selection        | GET         | seat_selection.html         | seats (list of dict: seat_id(int), row(str), column(int), seat_type(str), status(str)), selected_showtime (dict: showtime_id(int), movie_title(str), theater_name(str), showtime_date(str), showtime_time(str), price(float)) |
| /booking/confirmation         | booking_confirmation      | GET         | booking_confirmation.html   | booking_summary (dict: movie_title(str), showtime_date(str), showtime_time(str), seats(list of str), total_price(float)) |
| /booking/confirmation         | confirm_booking           | POST        | None (redirect after booking completion) | form data: customer_name(str), customer_email(str), seats(list of str), showtime_id(int) |
| /bookings                    | booking_history           | GET         | booking_history.html        | bookings (list of dict: booking_id(int), movie_title(str), booking_date(str), seats(list of str), status(str)) |
| /bookings/<int:booking_id>    | view_booking_details      | GET         | booking_details.html        | booking (dict: booking_id(int), movie_title(str), showtime_date(str), seats(list of str), status(str), customer_name(str), customer_email(str), total_price(float)) |
| /theaters                    | theater_information       | GET         | theater_information.html    | theaters (list of dict: theater_id(int), theater_name(str), location(str), city(str), screens(int), facilities(str)) |

---

## Section 2: HTML Template Specifications

### 1. Dashboard Page
- Filename: templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- <h1> Title: Movie Ticketing Dashboard
- Element IDs:
  - dashboard-page (Div): Container for the dashboard page.
  - featured-movies (Div): Display featured movie recommendations.
  - browse-movies-button (Button): Navigates to movie_catalog.
  - view-bookings-button (Button): Navigates to booking_history.
  - showtimes-button (Button): Navigates to showtime_selection or pre-selection dashboard.
- Navigation Mapping of Buttons:
  - browse-movies-button -> movie_catalog
  - view-bookings-button -> booking_history
  - showtimes-button -> select_showtime (could lead to a selection or filtered view)

### 2. Movie Catalog Page
- Filename: templates/movie_catalog.html
- Page Title: Movie Catalog
- <h1> Title: Movie Catalog
- Element IDs:
  - catalog-page (Div): Container for the catalog page.
  - search-input (Input): Field to search movies by title or genre.
  - genre-filter (Dropdown): Filter movies by genre.
  - movies-grid (Div): Grid displaying movie cards.
  - view-movie-button-{movie_id} (Button): Button to view movie details; dynamic with movie_id.
- Navigation Mapping:
  - view-movie-button-{movie_id} -> movie_details(movie_id=movie_id)

### 3. Movie Details Page
- Filename: templates/movie_details.html
- Page Title: Movie Details
- <h1> Title: Movie Details
- Element IDs:
  - movie-details-page (Div): Container for movie details.
  - movie-title (H1): Display movie title.
  - movie-director (Div): Display movie director.
  - movie-rating (Div): Display movie rating.
  - movie-description (Div): Display movie description.
  - select-showtime-button (Button): Proceed to select_showtime with movie_id.
- Navigation Mapping:
  - select-showtime-button -> select_showtime(movie_id=movie_id)

### 4. Showtime Selection Page
- Filename: templates/showtime_selection.html
- Page Title: Select Showtime
- <h1> Title: Select Showtime
- Element IDs:
  - showtime-page (Div): Container for showtime page.
  - showtimes-list (Div): List of showtimes with details.
  - theater-filter (Dropdown): Filter showtimes by theater.
  - date-filter (Input): Filter by date.
  - select-showtime-button-{showtime_id} (Button): Select specific showtime; dynamic with showtime_id.
- Navigation Mapping:
  - select-showtime-button-{showtime_id} -> seat_selection(showtime_id=showtime_id)

### 5. Seat Selection Page
- Filename: templates/seat_selection.html
- Page Title: Select Seats
- <h1> Title: Select Seats
- Element IDs:
  - seat-selection-page (Div): Container for seat selection.
  - seat-map (Div): Interactive seat map.
  - selected-seats-display (Div): Display currently selected seats.
  - seat-{row}{col} (Button): Individual seat buttons; dynamic with row letter and column number.
  - proceed-booking-button (Button): Proceed to booking confirmation.
- Navigation Mapping:
  - proceed-booking-button -> booking_confirmation POST will occur with selection data

### 6. Booking Confirmation Page
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- <h1> Title: Booking Confirmation
- Element IDs:
  - confirmation-page (Div): Container for confirmation page.
  - booking-summary (Div): Display booking details summary.
  - customer-name (Input): Input for customer name.
  - customer-email (Input): Input for customer email.
  - confirm-booking-button (Button): Confirm and complete booking.
- Navigation Mapping:
  - confirm-booking-button -> confirm_booking POST

### 7. Booking History Page
- Filename: templates/booking_history.html
- Page Title: Booking History
- <h1> Title: Booking History
- Element IDs:
  - bookings-page (Div): Container for bookings page.
  - bookings-table (Table): Table displaying booking list.
  - view-booking-button-{booking_id} (Button): View booking details; dynamic with booking_id.
  - status-filter (Dropdown): Filter bookings by status.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation Mapping:
  - view-booking-button-{booking_id} -> view_booking_details(booking_id=booking_id)
  - back-to-dashboard -> dashboard_page

### 8. Theater Information Page
- Filename: templates/theater_information.html
- Page Title: Theater Information
- <h1> Title: Theater Information
- Element IDs:
  - theater-page (Div): Container for theater page.
  - theaters-list (Div): List of theaters details.
  - theater-location-filter (Dropdown): Filter theaters by location.
  - facilities-display (Div): Display theater facilities and amenities.
  - back-to-dashboard (Button): Navigate back to dashboard.
- Navigation Mapping:
  - back-to-dashboard -> dashboard_page

---

## Section 3: Data File Schemas

### 1. Movies Data
- Filename: data/movies.txt
- Fields Order:
  movie_id|title|director|genre|rating|duration|description|release_date
- Description: Contains movie details including metadata and description.
- Example Rows:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### 2. Theaters Data
- Filename: data/theaters.txt
- Fields Order:
  theater_id|theater_name|location|city|screens|facilities
- Description: Contains theaters with location and facilities info.
- Example Rows:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### 3. Showtimes Data
- Filename: data/showtimes.txt
- Fields Order:
  showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Shows schedules for movies in theaters.
- Example Rows:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### 4. Seats Data
- Filename: data/seats.txt
- Fields Order:
  seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Seat details and their availability status.
- Example Rows:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### 5. Bookings Data
- Filename: data/bookings.txt
- Fields Order:
  booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Records of ticket bookings with customer info.
- Example Rows:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### 6. Genres Data
- Filename: data/genres.txt
- Fields Order:
  genre_id|genre_name|description
- Description: List of movie genres with descriptions.
- Example Rows:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
