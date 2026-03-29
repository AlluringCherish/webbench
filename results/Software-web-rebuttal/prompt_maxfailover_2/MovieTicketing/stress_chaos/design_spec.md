# MovieTicketing Application Design Specification

---

## Section 1: Flask Routes Specification

| Route Path                      | Function Name          | HTTP Method | Template Rendered          | Context Variables Passed to Template                             |
|--------------------------------|------------------------|-------------|----------------------------|-----------------------------------------------------------------| 
| /                              | root_redirect          | GET         | N/A (redirect)             | N/A                                                             |
| /dashboard                     | dashboard_page         | GET         | dashboard.html             | featured_movies (list of dict: movie_id:int, title:str, rating:float), upcoming_releases (list of dict: movie_id:int, title:str, release_date:str) |
| /movies                       | movie_catalog          | GET         | movie_catalog.html         | movies (list of dict: movie_id:int, title:str, genre:str, rating:float, duration:int, poster_url:str) |
| /movies/<int:movie_id>        | movie_details          | GET         | movie_details.html         | movie (dict: movie_id:int, title:str, director:str, genre:str, rating:float, duration:int, description:str, release_date:str) |
| /movies/<int:movie_id>/showtimes | showtime_selection    | GET         | showtime_selection.html    | showtimes (list of dict: showtime_id:int, date:str, time:str, theater_name:str, price:float), theaters (list of dict: theater_id:int, theater_name:str), filter_theater_id (int or None), filter_date (str or None) |
| /showtimes/select/<int:showtime_id> | select_showtime     | POST        | redirect to seat_selection.html (redirect) | N/A |
| /seat-selection/<int:showtime_id> | seat_selection      | GET         | seat_selection.html        | seat_map (list of dict: seat_id:int, row:str, column:int, seat_type:str, status:str), selected_seats (list of str seat IDs), showtime_id (int) |
| /booking/confirm/<int:showtime_id> | booking_confirmation | GET         | booking_confirmation.html  | showtime (dict: showtime_id:int, movie_title:str, theater_name:str, date:str, time:str, price:float), selected_seats (list of str), total_price (float) |
| /booking/confirm/<int:showtime_id> | confirm_booking      | POST        | redirect to booking_history.html (redirect) | N/A |
| /bookings                    | booking_history        | GET         | booking_history.html       | bookings (list of dict: booking_id:int, movie_title:str, booking_date:str, seats_booked:list of str, status:str) |
| /bookings/<int:booking_id>    | booking_details        | GET         | booking_details.html       | booking (dict: booking_id:int, showtime_id:int, customer_name:str, customer_email:str, booking_date:str, total_price:float, status:str, seats_booked:list of str) |
| /theaters                    | theater_information    | GET         | theater_information.html   | theaters (list of dict: theater_id:int, theater_name:str, location:str, city:str, screens:int, facilities:str), filter_location (str or None) |

---

## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- Main Heading (<h1>): Movie Ticketing Dashboard
- Elements:
  - ID: dashboard-page (Div) - Container for the dashboard page.
  - ID: featured-movies (Div) - Displays featured movie recommendations.
  - ID: browse-movies-button (Button) - Navigates to movie_catalog route (movie_catalog).
  - ID: view-bookings-button (Button) - Navigates to booking_history route (booking_history).
  - ID: showtimes-button (Button) - Navigates to showtime_selection root (redirect to /showtimes or dashboard to showtimes function).

### 2. templates/movie_catalog.html
- Page Title: Movie Catalog
- Main Heading (<h1>): Movie Catalog
- Elements:
  - ID: catalog-page (Div) - Container for the catalog page.
  - ID: search-input (Input) - Text field to search movies.
  - ID: genre-filter (Dropdown) - Dropdown to filter movies by genre.
  - ID: movies-grid (Div) - Grid displaying movie cards.
  - Dynamic Button ID: view-movie-button-{movie_id} (Button) - Button on each movie card to view details, navigates to movie_details with movie_id.

### 3. templates/movie_details.html
- Page Title: Movie Details
- Main Heading (<h1>): Movie Details
- Elements:
  - ID: movie-details-page (Div) - Container for movie details.
  - ID: movie-title (H1) - Displays the movie title.
  - ID: movie-director (Div) - Displays the movie director.
  - ID: movie-rating (Div) - Displays the movie rating.
  - ID: movie-description (Div) - Displays the movie description.
  - ID: select-showtime-button (Button) - Navigates to showtime_selection for this movie.

### 4. templates/showtime_selection.html
- Page Title: Select Showtime
- Main Heading (<h1>): Select Showtime
- Elements:
  - ID: showtime-page (Div) - Container for the showtime selection page.
  - ID: showtimes-list (Div) - List of available showtimes.
  - ID: theater-filter (Dropdown) - Filter showtimes by theater.
  - ID: date-filter (Input) - Filter showtimes by date.
  - Dynamic Button ID: select-showtime-button-{showtime_id} (Button) - Button to select a showtime, posts to select_showtime route.

### 5. templates/seat_selection.html
- Page Title: Select Seats
- Main Heading (<h1>): Select Seats
- Elements:
  - ID: seat-selection-page (Div) - Container for seat selection.
  - ID: seat-map (Div) - Interactive seat map.
  - ID: selected-seats-display (Div) - Shows selected seats.
  - Dynamic Button ID: seat-{row}{col} (Button) - Each seat button for seat selection.
  - ID: proceed-booking-button (Button) - Proceeds to booking confirmation.

### 6. templates/booking_confirmation.html
- Page Title: Booking Confirmation
- Main Heading (<h1>): Booking Confirmation
- Elements:
  - ID: confirmation-page (Div) - Container for confirmation details.
  - ID: booking-summary (Div) - Summary of the booking.
  - ID: customer-name (Input) - Input field for customer name.
  - ID: customer-email (Input) - Input field for customer email.
  - ID: confirm-booking-button (Button) - Confirms booking submission.

### 7. templates/booking_history.html
- Page Title: Booking History
- Main Heading (<h1>): Booking History
- Elements:
  - ID: bookings-page (Div) - Container for booking history.
  - ID: bookings-table (Table) - Displays all bookings.
  - Dynamic Button ID: view-booking-button-{booking_id} (Button) - To view individual booking details.
  - ID: status-filter (Dropdown) - Filter bookings by status.
  - ID: back-to-dashboard (Button) - Navigates back to dashboard.

### 8. templates/theater_information.html
- Page Title: Theater Information
- Main Heading (<h1>): Theater Information
- Elements:
  - ID: theater-page (Div) - Container for theater info.
  - ID: theaters-list (Div) - Displays list of theaters.
  - ID: theater-location-filter (Dropdown) - Filter theaters by location.
  - ID: facilities-display (Div) - Shows facilities of selected theater.
  - ID: back-to-dashboard (Button) - Navigates back to dashboard.


Navigation Summary:
- dashboard_page -> movie_catalog (browse-movies-button)
- dashboard_page -> booking_history (view-bookings-button)
- dashboard_page -> showtime_selection or showtimes page (showtimes-button)
- movie_catalog -> movie_details (view-movie-button-{movie_id})
- movie_details -> showtime_selection (select-showtime-button)
- showtime_selection -> seat_selection (select-showtime-button-{showtime_id})
- seat_selection -> booking_confirmation (proceed-booking-button)
- booking_confirmation -> booking_history (confirm-booking-button)
- booking_history -> booking_details (view-booking-button-{booking_id})
- booking_history -> dashboard_page (back-to-dashboard)
- theater_information -> dashboard_page (back-to-dashboard)

---

## Section 3: Data File Schemas

### 1. data/movies.txt
- Fields (pipe-delimited): movie_id|title|director|genre|rating|duration|description|release_date
- Description: Stores movie information.
- Example Rows:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### 2. data/theaters.txt
- Fields (pipe-delimited): theater_id|theater_name|location|city|screens|facilities
- Description: Stores theater information.
- Example Rows:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### 3. data/showtimes.txt
- Fields (pipe-delimited): showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Stores showtimes for movies at theaters.
- Example Rows:
  1|1|1|2025-02-01|19:00|12.99|85
  2|1|1|2025-02-01|22:30|12.99|40
  3|2|2|2025-02-01|18:00|14.99|95

### 4. data/seats.txt
- Fields (pipe-delimited): seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Stores seat information and booking status.
- Example Rows:
  1|1|1|A|1|Standard|Available
  2|1|1|A|2|Standard|Available
  3|1|1|B|5|Premium|Booked

### 5. data/bookings.txt
- Fields (pipe-delimited): booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Stores user bookings.
- Example Rows:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### 6. data/genres.txt
- Fields (pipe-delimited): genre_id|genre_name|description
- Description: Stores genre metadata.
- Example Rows:
  1|Action|Fast-paced movies with exciting sequences and combat
  2|Drama|Character-driven stories exploring complex themes
  3|Sci-Fi|Science fiction with futuristic technology and concepts

---

This design specification details all Flask routes, HTML templates, and data file schemas required to enable parallel development of backend and frontend for the MovieTicketing application. All names, types, and IDs are consistent across sections.
