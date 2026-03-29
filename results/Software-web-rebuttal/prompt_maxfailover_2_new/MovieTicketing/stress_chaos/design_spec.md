# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                | Function Name           | HTTP Method | Template Rendered          | Context Variables (name:type)                                 |
|---------------------------|-------------------------|-------------|----------------------------|----------------------------------------------------------------|
| /                         | root_redirect            | GET         | redirects to /dashboard    | none                                                           |
| /dashboard                | dashboard                | GET         | dashboard.html             | featured_movies:list[dict{movie_id:int, title:str, genre:str, rating:float}], upcoming_releases:list[dict{movie_id:int, title:str, release_date:str}], [button navigation handled in frontend] |
| /movies                   | movies_catalog           | GET         | movies_catalog.html        | movies:list[dict{movie_id:int, title:str, rating:float, duration:int, genre:str}], genres:list[str]                              |
| /movies/<int:movie_id>    | movie_details            | GET         | movie_details.html         | movie:dict{movie_id:int, title:str, director:str, genre:str, rating:float, duration:int, description:str, release_date:str}      |
| /movies/<int:movie_id>/showtimes | showtime_selection  | GET         | showtime_selection.html    | showtimes:list[dict{showtime_id:int, movie_id:int, theater_id:int, showtime_date:str, showtime_time:str, price:float}],
                                   theaters:list[dict{theater_id:int, theater_name:str}],
                                   filters:dict{theater_filter:str, date_filter:str}                                                          |
| /showtimes/<int:showtime_id>/seats | seat_selection    | GET         | seat_selection.html        | seat_map:list[dict{seat_id:int, seat_label:str, seat_type:str, status:str}], selected_seats:list[str]                           |
| /showtimes/<int:showtime_id>/seats | select_seats     | POST        | redirects to /booking/confirm | selected_seats:list[str], showtime_id:int  [sent in POST form data]                                                    |
| /booking/confirm          | booking_confirmation      | GET         | booking_confirmation.html  | booking_summary:dict{movie_title:str, showtime_date:str, showtime_time:str, theater_name:str, seats:list[str], total_price:float} |
| /booking/confirm          | confirm_booking           | POST        | redirects to /bookings     | customer_name:str, customer_email:str, booking_info:dict[details from booking_summary plus seats] [from POST data]            |
| /bookings                 | booking_history           | GET         | booking_history.html       | bookings:list[dict{booking_id:int, movie_title:str, booking_date:str, seats:list[str], status:str}]                            |
| /bookings/<int:booking_id> | booking_details          | GET         | booking_details.html       | booking:dict{booking_id:int, movie_title:str, showtime_date:str, showtime_time:str, theater_name:str, seats:list[str], status:str}|
| /theaters                 | theater_information       | GET         | theater_information.html   | theaters:list[dict{theater_id:int, theater_name:str, location:str, city:str, screens:int, facilities:str}],
                                   location_filter:str                                                                                  |


## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- H1 Title: Movie Ticketing Dashboard
- Elements:
  - `dashboard-page` (Div): Container for dashboard page
  - `featured-movies` (Div): Display featured movies
  - `browse-movies-button` (Button): Navigate to movies_catalog
  - `view-bookings-button` (Button): Navigate to booking_history
  - `showtimes-button` (Button): Navigate to showtime_selection (general showtimes page)

### 2. templates/movies_catalog.html
- Page Title: Movie Catalog
- H1 Title: Movie Catalog
- Elements:
  - `catalog-page` (Div): Container for catalog page
  - `search-input` (Input): Search movies by title or genre
  - `genre-filter` (Dropdown): Filter movies by genre
  - `movies-grid` (Div): Grid displaying movie cards
  - `view-movie-button-{movie_id}` (Button): View movie details for movie_id
    Navigation: /movies/<movie_id> (function movie_details)

### 3. templates/movie_details.html
- Page Title: Movie Details
- H1 Title: Movie Details
- Elements:
  - `movie-details-page` (Div): Container for movie details
  - `movie-title` (H1): Movie title
  - `movie-director` (Div): Movie director
  - `movie-rating` (Div): Movie rating
  - `movie-description` (Div): Movie description
  - `select-showtime-button` (Button): Proceed to showtime_selection for this movie
    Navigation: /movies/<movie_id>/showtimes (function showtime_selection)

### 4. templates/showtime_selection.html
- Page Title: Select Showtime
- H1 Title: Select Showtime
- Elements:
  - `showtime-page` (Div): Container
  - `theater-filter` (Dropdown): Filter showtimes by theater
  - `date-filter` (Input): Filter showtimes by date
  - `showtimes-list` (Div): List of showtimes
  - `select-showtime-button-{showtime_id}` (Button): Select this showtime
    Navigation: /showtimes/<showtime_id>/seats (function seat_selection POST or GET)

### 5. templates/seat_selection.html
- Page Title: Select Seats
- H1 Title: Select Seats
- Elements:
  - `seat-selection-page` (Div): Container
  - `seat-map` (Div): Interactive seat map
  - `seat-{row}{col}` (Button): Individual seat buttons (e.g., seat-A1)
  - `selected-seats-display` (Div): Display selected seats
  - `proceed-booking-button` (Button): Proceed to booking confirmation
    Navigation: POST selected seats to /showtimes/<showtime_id>/seats (function select_seats)

### 6. templates/booking_confirmation.html
- Page Title: Booking Confirmation
- H1 Title: Booking Confirmation
- Elements:
  - `confirmation-page` (Div): Container
  - `booking-summary` (Div): Summary of booking details
  - `customer-name` (Input): Input customer name
  - `customer-email` (Input): Input customer email
  - `confirm-booking-button` (Button): Confirm booking
    Navigation: POST to /booking/confirm (function confirm_booking)

### 7. templates/booking_history.html
- Page Title: Booking History
- H1 Title: Booking History
- Elements:
  - `bookings-page` (Div): Container
  - `status-filter` (Dropdown): Filter bookings by status
  - `bookings-table` (Table): Displays bookings
  - `view-booking-button-{booking_id}` (Button): View details for booking_id
    Navigation: /bookings/<booking_id> (function booking_details)
  - `back-to-dashboard` (Button): Navigate to /dashboard (function dashboard)

### 8. templates/booking_details.html
- Page Title: Booking Details
- H1 Title: Booking Details
- Elements:
  - `booking-details-page` (Div): Container
  - `booking-info` (Div): Detailed booking info
  - `back-to-bookings` (Button): Navigate to /bookings (function booking_history)

### 9. templates/theater_information.html
- Page Title: Theater Information
- H1 Title: Theater Information
- Elements:
  - `theater-page` (Div): Container
  - `theater-location-filter` (Dropdown): Filter theaters by location
  - `theaters-list` (Div): List theaters
  - `facilities-display` (Div): Display selected theater facilities
  - `back-to-dashboard` (Button): Navigate to /dashboard (function dashboard)


## Section 3: Data File Schemas

### 1. data/movies.txt
- Fields (pipe-delimited):
  `movie_id|title|director|genre|rating|duration|description|release_date`
- Description: Contains movie details including metadata and description.
- Example rows:
  ```
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23
  ```

### 2. data/theaters.txt
- Fields (pipe-delimited):
  `theater_id|theater_name|location|city|screens|facilities`
- Description: Information about theaters with location and available facilities.
- Example rows:
  ```
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge
  ```

### 3. data/showtimes.txt
- Fields (pipe-delimited):
  `showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats`
- Description: Showtimes for movies in different theaters including price and availability.
- Example rows:
  ```
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95
  ```

### 4. data/seats.txt
- Fields (pipe-delimited):
  `seat_id|theater_id|screen_id|row|column|seat_type|status`
- Description: Seat definitions in theaters/screens and their availability.
- Example rows:
  ```
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked
  ```

### 5. data/bookings.txt
- Fields (pipe-delimited):
  `booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked`
- Description: Records of ticket bookings including customer and seat info.
- Example rows:
  ```
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4
  ```

### 6. data/genres.txt
- Fields (pipe-delimited):
  `genre_id|genre_name|description`
- Description: List of movie genres with descriptions.
- Example rows:
  ```
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
  ```

---

This completes the design specification for parallel backend and frontend development of the MovieTicketing application.