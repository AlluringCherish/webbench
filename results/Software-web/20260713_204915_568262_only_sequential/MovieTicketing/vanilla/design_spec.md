# MovieTicketing Web Application Design Specification

---

## 1. Flask Routes Specification

| URL Pattern                     | Function Name           | HTTP Method | Template File                | Context Variables (name:type)                      |
|--------------------------------|------------------------|-------------|-----------------------------|---------------------------------------------------|
| `/`                            | dashboard_page         | GET         | dashboard.html              | featured_movies:List[Movie], upcoming_releases:List[Movie] |
| `/catalog`                    | movie_catalog_page     | GET, POST   | catalog.html                | movies:List[Movie], genres:List[str], selected_genre:str, search_query:str |
| `/movie/<int:movie_id>`       | movie_details_page     | GET         | movie_details.html          | movie:Movie                                        |
| `/showtimes/<int:movie_id>`   | showtime_selection_page | GET, POST  | showtimes.html              | showtimes:List[Showtime], theaters:List[Theater], selected_theater:int or None, selected_date:str or None |
| `/seats/<int:showtime_id>`    | seat_selection_page    | GET, POST   | seat_selection.html         | seats:List[Seat], selected_seats:List[str], showtime:Showtime |
| `/booking/confirm`             | booking_confirmation_page | GET, POST| booking_confirmation.html  | booking_summary:dict, customer_name:str, customer_email:str |
| `/bookings`                   | booking_history_page   | GET         | booking_history.html        | bookings:List[Booking], selected_status:str        |
| `/booking/<int:booking_id>`   | booking_details_page   | GET         | booking_details.html        | booking:Booking                                    |
| `/theaters`                   | theater_information_page | GET        | theaters.html               | theaters:List[Theater], selected_location:str or None |

---

## 2. Pages and Element Specification

### 2.1 Dashboard Page
- Page Title: Movie Ticketing Dashboard
- Container ID: `dashboard-page` (Div)
- Elements:
  - `featured-movies` (Div)
  - `browse-movies-button` (Button)
  - `view-bookings-button` (Button)
  - `showtimes-button` (Button)

### 2.2 Movie Catalog Page
- Page Title: Movie Catalog
- Container ID: `catalog-page` (Div)
- Elements:
  - `search-input` (Input)
  - `genre-filter` (Dropdown)
  - `movies-grid` (Div)
  - Pattern `view-movie-button-{movie_id}` (Button)

### 2.3 Movie Details Page
- Page Title: Movie Details
- Container ID: `movie-details-page` (Div)
- Elements:
  - `movie-title` (H1)
  - `movie-director` (Div)
  - `movie-rating` (Div)
  - `movie-description` (Div)
  - `select-showtime-button` (Button)

### 2.4 Showtime Selection Page
- Page Title: Select Showtime
- Container ID: `showtime-page` (Div)
- Elements:
  - `showtimes-list` (Div)
  - `theater-filter` (Dropdown)
  - `date-filter` (Input)
  - Pattern `select-showtime-button-{showtime_id}` (Button)

### 2.5 Seat Selection Page
- Page Title: Select Seats
- Container ID: `seat-selection-page` (Div)
- Elements:
  - `seat-map` (Div)
  - `selected-seats-display` (Div)
  - Pattern `seat-{row}{col}` (Button)
  - `proceed-booking-button` (Button)

### 2.6 Booking Confirmation Page
- Page Title: Booking Confirmation
- Container ID: `confirmation-page` (Div)
- Elements:
  - `booking-summary` (Div)
  - `customer-name` (Input)
  - `customer-email` (Input)
  - `confirm-booking-button` (Button)

### 2.7 Booking History Page
- Page Title: Booking History
- Container ID: `bookings-page` (Div)
- Elements:
  - `bookings-table` (Table)
  - Pattern `view-booking-button-{booking_id}` (Button)
  - `status-filter` (Dropdown)
  - `back-to-dashboard` (Button)

### 2.8 Theater Information Page
- Page Title: Theater Information
- Container ID: `theater-page` (Div)
- Elements:
  - `theaters-list` (Div)
  - `theater-location-filter` (Dropdown)
  - `facilities-display` (Div)
  - `back-to-dashboard` (Button)

---

## 3. Navigation Flow

- Dashboard Page:
  - `browse-movies-button`: navigates to `url_for('movie_catalog_page')`
  - `view-bookings-button`: navigates to `url_for('booking_history_page')`
  - `showtimes-button`: navigates to `url_for('showtime_selection_page', movie_id=0)` or a suitable default handling of showtime page to choose movie.

- Movie Catalog Page:
  - `view-movie-button-{movie_id}`: navigates to `url_for('movie_details_page', movie_id=movie_id)`

- Movie Details Page:
  - `select-showtime-button`: navigates to `url_for('showtime_selection_page', movie_id=movie_id)`

- Showtime Selection Page:
  - `select-showtime-button-{showtime_id}`: navigates to `url_for('seat_selection_page', showtime_id=showtime_id)`

- Seat Selection Page:
  - `proceed-booking-button`: navigates to `url_for('booking_confirmation_page')`

- Booking Confirmation Page:
  - `confirm-booking-button`: posts booking data and redirects to booking history or confirmation

- Booking History Page:
  - `view-booking-button-{booking_id}`: navigates to `url_for('booking_details_page', booking_id=booking_id)`
  - `back-to-dashboard`: navigates to `url_for('dashboard_page')`

- Theater Information Page:
  - `back-to-dashboard`: navigates to `url_for('dashboard_page')`

---

## 4. Data Parsing Contracts

All data files are in `data/` directory, pipe `|` separated, no header lines.

### 4.1 movies.txt
- Filename: `data/movies.txt`
- Fields (in order): 
  - movie_id (int)
  - title (str)
  - director (str)
  - genre (str)
  - rating (float)
  - duration (int, minutes)
  - description (str)
  - release_date (YYYY-MM-DD, str)
- Example Rows:
  ```
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23
  ```

### 4.2 theaters.txt
- Filename: `data/theaters.txt`
- Fields (in order):
  - theater_id (int)
  - theater_name (str)
  - location (str)
  - city (str)
  - screens (int)
  - facilities (str, comma separated list allowed)
- Example Rows:
  ```
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge
  ```

### 4.3 showtimes.txt
- Filename: `data/showtimes.txt`
- Fields (in order):
  - showtime_id (int)
  - movie_id (int)
  - theater_id (int)
  - showtime_date (YYYY-MM-DD, str)
  - showtime_time (HH:MM, 24h str)
  - price (float)
  - available_seats (int)
- Example Rows:
  ```
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95
  ```

### 4.4 seats.txt
- Filename: `data/seats.txt`
- Fields (in order):
  - seat_id (int)
  - theater_id (int)
  - screen_id (int)
  - row (str, e.g., 'A')
  - column (int)
  - seat_type (str, e.g., Standard, Premium)
  - status (str, e.g., Available, Booked)
- Example Rows:
  ```
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked
  ```

### 4.5 bookings.txt
- Filename: `data/bookings.txt`
- Fields (in order):
  - booking_id (int)
  - showtime_id (int)
  - customer_name (str)
  - customer_email (str)
  - booking_date (YYYY-MM-DD, str)
  - total_price (float)
  - status (str, e.g., Confirmed, Cancelled, Completed)
  - seats_booked (str, comma-separated seat codes like A1,A2)
- Example Rows:
  ```
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4
  ```

### 4.6 genres.txt
- Filename: `data/genres.txt`
- Fields (in order):
  - genre_id (int)
  - genre_name (str)
  - description (str)
- Example Rows:
  ```
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts
  ```

---

# End of Design Specification
