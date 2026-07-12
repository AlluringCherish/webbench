# Design Specification Document for MovieTicketing Application

---

## Section 1: Flask Routes Specification

| Route Path                     | Function Name            | HTTP Method | Template Rendered           | Context Variables (type)                                                                                                                  |
|-------------------------------|--------------------------|-------------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect             | GET         | Redirect to /dashboard       | None                                                                                                                                    |
| /dashboard                    | dashboard                | GET         | dashboard.html              | featured_movies (list of dict), upcoming_releases (list of dict)                                                                         |
| /movies                      | movie_catalog            | GET         | movie_catalog.html          | movies (list of dict), genres (list of dict), selected_genre (str), search_query (str)                                                   |
| /movies/<int:movie_id>       | movie_details            | GET         | movie_details.html          | movie (dict), genres (list of dict)                                                                                                    |
| /showtimes/<int:movie_id>    | showtime_selection       | GET         | showtime_selection.html     | movie (dict), showtimes (list of dict), theaters (list of dict), selected_theater (str), selected_date (str)                            |
| /select-seats/<int:showtime_id> | seat_selection         | GET         | seat_selection.html         | showtime (dict), seats (list of dict), selected_seats (list of str)                                                                      |
| /confirm-booking/<int:showtime_id> | booking_confirmation  | GET         | booking_confirmation.html   | showtime (dict), movie (dict), selected_seats (list of str), total_price (float)                                                        |
| /confirm-booking/<int:showtime_id> | confirm_booking       | POST        | booking_confirmation.html   | form data: customer_name (str), customer_email (str), selected_seats (list of str)                                                       |
| /bookings                    | booking_history          | GET         | booking_history.html        | bookings (list of dict), selected_status (str)                                                                                        |
| /bookings/<int:booking_id>   | view_booking_details     | GET         | booking_details.html        | booking (dict), movie (dict), showtime (dict)                                                                                          |
| /theaters                    | theater_information       | GET         | theater_information.html    | theaters (list of dict), selected_location (str)                                                                                       |

### Context Variable Field Structures

- featured_movies, upcoming_releases:
  - list of dict with fields: movie_id (int), title (str), rating (float), duration (int), poster_url (str, optional if posters are used)

- movies:
  - list of dict with fields: movie_id (int), title (str), director (str), genre (str), rating (float), duration (int), description (str), release_date (str)

- genres:
  - list of dict with fields: genre_id (int), genre_name (str), description (str)

- movie:
  - dict with fields: movie_id (int), title (str), director (str), genre (str), rating (float), duration (int), description (str), release_date (str)

- showtimes:
  - list of dict with fields: showtime_id (int), movie_id (int), theater_id (int), showtime_date (str), showtime_time (str), price (float), available_seats (int)

- theaters:
  - list of dict with fields: theater_id (int), theater_name (str), location (str), city (str), screens (int), facilities (str)

- selected_seats:
  - list of str, e.g., ['A1', 'A2']

- seats:
  - list of dict with fields: seat_id (int), theater_id (int), screen_id (int), row (str), column (str), seat_type (str), status (str)

- bookings:
  - list of dict with fields: booking_id (int), showtime_id (int), customer_name (str), customer_email (str), booking_date (str), total_price (float), status (str), seats_booked (list of str parsed from comma-separated)

- booking:
  - dict same structure as above but single booking record

## Section 2: HTML Template Specifications

### 1. dashboard.html
- Filename: templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- <h1> text: Movie Ticketing Dashboard
- Elements:
  - ID: dashboard-page (Div) - Main container
  - ID: featured-movies (Div) - Featured movie recommendations display
  - ID: browse-movies-button (Button) - Navigates to movie_catalog function (route: /movies)
  - ID: view-bookings-button (Button) - Navigates to booking_history function (route: /bookings)
  - ID: showtimes-button (Button) - Navigates to showtime_selection root page or requires movie context? (Navigates to /showtimes/<movie_id> presumed? Since showtimes needs movie_id, from dashboard we direct to catalog first to pick movie anyway or to movie catalog)

### 2. movie_catalog.html
- Filename: templates/movie_catalog.html
- Page Title: Movie Catalog
- <h1> text: Movie Catalog
- Elements:
  - ID: catalog-page (Div) - Main container
  - ID: search-input (Input) - Search field for movie title or genre
  - ID: genre-filter (Dropdown) - Filter movies by genre
  - ID: movies-grid (Div) - Grid containing movie cards
  - ID (pattern): view-movie-button-{movie_id} (Button) - For each movie card: button to view movie details
- Navigation:
  - view-movie-button-{movie_id} links to movie_details function (/movies/<movie_id>)

### 3. movie_details.html
- Filename: templates/movie_details.html
- Page Title: Movie Details
- <h1> text: Movie Details
- Elements:
  - ID: movie-details-page (Div) - Main container
  - ID: movie-title (H1) - Displays movie title
  - ID: movie-director (Div) - Displays director
  - ID: movie-rating (Div) - Displays rating
  - ID: movie-description (Div) - Displays description
  - ID: select-showtime-button (Button) - Navigates to showtime_selection function (/showtimes/<movie_id>)

### 4. showtime_selection.html
- Filename: templates/showtime_selection.html
- Page Title: Select Showtime
- <h1> text: Select Showtime
- Elements:
  - ID: showtime-page (Div) - Main container
  - ID: theater-filter (Dropdown) - Filter showtimes by theater
  - ID: date-filter (Input) - Filter showtimes by date
  - ID: showtimes-list (Div) - Lists showtimes
  - ID (pattern): select-showtime-button-{showtime_id} (Button) - Select specific showtime
- Navigation:
  - select-showtime-button-{showtime_id} links to seat_selection function (/select-seats/<showtime_id>)

### 5. seat_selection.html
- Filename: templates/seat_selection.html
- Page Title: Select Seats
- <h1> text: Select Seats
- Elements:
  - ID: seat-selection-page (Div) - Main container
  - ID: seat-map (Div) - Interactive seat map
  - ID: selected-seats-display (Div) - Shows selected seats
  - ID (pattern): seat-{row}{col} (Button) - Individual seats
  - ID: proceed-booking-button (Button) - Proceeds to booking confirmation
- Navigation:
  - proceed-booking-button triggers POST or redirects to booking_confirmation function with selected seats

### 6. booking_confirmation.html
- Filename: templates/booking_confirmation.html
- Page Title: Booking Confirmation
- <h1> text: Booking Confirmation
- Elements:
  - ID: confirmation-page (Div) - Main container
  - ID: booking-summary (Div) - Summary of booking details: movie, showtime, seats, total
  - ID: customer-name (Input) - Input field for customer name
  - ID: customer-email (Input) - Input field for customer email
  - ID: confirm-booking-button (Button) - Completes booking

### 7. booking_history.html
- Filename: templates/booking_history.html
- Page Title: Booking History
- <h1> text: Booking History
- Elements:
  - ID: bookings-page (Div) - Main container
  - ID: bookings-table (Table) - Displays bookings
  - ID (pattern): view-booking-button-{booking_id} (Button) - View booking details
  - ID: status-filter (Dropdown) - Filter bookings by status
  - ID: back-to-dashboard (Button) - Navigates to dashboard

### 8. theater_information.html
- Filename: templates/theater_information.html
- Page Title: Theater Information
- <h1> text: Theater Information
- Elements:
  - ID: theater-page (Div) - Main container
  - ID: theaters-list (Div) - List of theaters
  - ID: theater-location-filter (Dropdown) - Filter theaters by location
  - ID: facilities-display (Div) - Displays facilities
  - ID: back-to-dashboard (Button) - Navigates to dashboard

---

## Section 3: Data File Schemas

1. movies.txt (data/movies.txt)
- Fields: movie_id|title|director|genre|rating|duration|description|release_date
- Description: Stores details of all movies.
- Examples:
  - 1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  - 2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  - 3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

2. theaters.txt (data/theaters.txt)
- Fields: theater_id|theater_name|location|city|screens|facilities
- Description: Stores theater information.
- Examples:
  - 1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  - 2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  - 3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

3. showtimes.txt (data/showtimes.txt)
- Fields: showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Stores showtime schedules.
- Examples:
  - 1|1|1|2025-02-01|19:00|12.99|85
  - 2|1|1|2025-02-01|22:30|12.99|40
  - 3|2|2|2025-02-01|18:00|14.99|95

4. seats.txt (data/seats.txt)
- Fields: seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Stores seating plan and availability.
- Examples:
  - 1|1|1|A|1|Standard|Available
  - 2|1|1|A|2|Standard|Available
  - 3|1|1|B|5|Premium|Booked

5. bookings.txt (data/bookings.txt)
- Fields: booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Stores booking records.
- Examples:
  - 1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  - 2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  - 3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

6. genres.txt (data/genres.txt)
- Fields: genre_id|genre_name|description
- Description: Stores movie genre information.
- Examples:
  - 1|Action|Fast-paced movies with exciting sequences and combat
  - 2|Drama|Character-driven stories exploring complex themes
  - 3|Sci-Fi|Science fiction with futuristic technology and concepts

---

This specification fully covers all the routes, frontend interface design elements, data file formats and fields, and mapping needed to enable fully parallel backend and frontend development for the 'MovieTicketing' application.