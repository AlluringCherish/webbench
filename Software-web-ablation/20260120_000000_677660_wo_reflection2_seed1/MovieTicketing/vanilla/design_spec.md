# MovieTicketing Application Design Specification

## Section 1: Flask Routes Specification

| Route Path                  | Function Name            | HTTP Method | Template Rendered           | Context Variables Passed                                         |
|-----------------------------|--------------------------|-------------|-----------------------------|------------------------------------------------------------------|
| /                           | root_redirect             | GET         | None (redirect to /dashboard) | None                                                             |
| /dashboard                  | dashboard                | GET         | dashboard.html              | featured_movies (list of dict: movie_id:int, title:str, poster:str, rating:float), upcoming_releases (list of dict: movie_id:int, title:str, release_date:str) |
| /movies                    | movie_catalog            | GET         | catalog.html                | movies (list of dict: movie_id:int, title:str, genre:str, rating:float, duration:int, poster:str) |
| /movies/<int:movie_id>     | movie_details            | GET         | movie_details.html          | movie (dict: movie_id:int, title:str, director:str, genre:str, rating:float, duration:int, description:str, release_date:str) |
| /showtimes/<int:movie_id>  | showtime_selection       | GET         | showtime.html               | showtimes (list of dict: showtime_id:int, movie_id:int, theater_id:int, showtime_date:str (YYYY-MM-DD), showtime_time:str (HH:mm), price:float), theaters (list of dict: theater_id:int, theater_name:str), movie_title:str |
| /select_seats/<int:showtime_id> | seat_selection        | GET         | seat_selection.html         | seat_map (list of dict: seat_id:int, row:str, column:int, seat_type:str, status:str), selected_showtime (dict: showtime_id:int, movie_id:int, theater_id:int, showtime_date:str, showtime_time:str, price:float) |
| /confirm_booking/<int:showtime_id> | booking_confirmation | GET         | confirmation.html           | booking_summary (dict: movie_title:str, showtime_date:str, showtime_time:str, theater_name:str, seats_selected (list of str), total_price:float) |
| /confirm_booking/<int:showtime_id> | confirm_booking      | POST        | None (redirect or re-render) | booking_data (customer_name:str, customer_email:str, seats_selected:list of str, showtime_id:int) |
| /bookings                  | booking_history          | GET         | bookings.html               | bookings (list of dict: booking_id:int, movie_title:str, booking_date:str, seats_booked (list of str), status:str) |
| /bookings/<int:booking_id> | booking_details          | GET         | booking_details.html        | booking (dict: booking_id:int, showtime_id:int, customer_name:str, customer_email:str, booking_date:str, total_price:float, status:str, seats_booked (list of str)), movie_title:str |
| /theaters                  | theater_information      | GET         | theater.html                | theaters (list of dict: theater_id:int, theater_name:str, location:str, city:str, screens:int, facilities:str) |

### Notes:
- Root route '/' redirects to /dashboard using HTTP 302 redirect.
- For routes with POST (e.g., confirming booking), no template is rendered but redirects back to confirmation or bookings page depending on outcome.
- Context list-of-dict fields detail explicit key types for frontend parsing.

---

## Section 2: HTML Template Specifications

### 1. templates/dashboard.html
- Page Title: Movie Ticketing Dashboard
- <title> and <h1> text: "Movie Ticketing Dashboard"
- Element IDs:
  - dashboard-page: Div container for entire dashboard page
  - featured-movies: Div container displaying featured movies recommendations
  - browse-movies-button: Button to navigate to movie_catalog()
  - view-bookings-button: Button to navigate to booking_history()
  - showtimes-button: Button to navigate to showtime_selection() (base page or some default route)
- Navigation:
  - browse-movies-button: url_for('movie_catalog')
  - view-bookings-button: url_for('booking_history')
  - showtimes-button: url_for('showtime_selection', movie_id=some_default_or_first_movie) [frontend picks default movie_id or first movie]

### 2. templates/catalog.html
- Page Title: Movie Catalog
- <title> and <h1> text: "Movie Catalog"
- Element IDs:
  - catalog-page: Div container for catalog
  - search-input: Input field to search movies by title or genre
  - genre-filter: Dropdown for genre filtering
  - movies-grid: Div grid containing movie cards
  - view-movie-button-{movie_id}: Button on each movie card to view details
- Navigation:
  - view-movie-button-{movie_id}: url_for('movie_details', movie_id=movie_id)

### 3. templates/movie_details.html
- Page Title: Movie Details
- <title> and <h1> text: "Movie Details"
- Element IDs:
  - movie-details-page: Div container
  - movie-title: H1 with movie title
  - movie-director: Div showing director
  - movie-rating: Div showing rating
  - movie-description: Div showing description
  - select-showtime-button: Button to proceed to showtime_selection for this movie
- Navigation:
  - select-showtime-button: url_for('showtime_selection', movie_id=movie_id) using current movie_id

### 4. templates/showtime.html
- Page Title: Select Showtime
- <title> and <h1> text: "Select Showtime"
- Element IDs:
  - showtime-page: Div container
  - showtimes-list: Div showing showtimes (each item includes date, time, theater name, price)
  - theater-filter: Dropdown to filter shows by theater
  - date-filter: Input date field
  - select-showtime-button-{showtime_id}: Button to select showtime
- Navigation:
  - select-showtime-button-{showtime_id}: url_for('seat_selection', showtime_id=showtime_id)

### 5. templates/seat_selection.html
- Page Title: Select Seats
- <title> and <h1> text: "Select Seats"
- Element IDs:
  - seat-selection-page: Div container
  - seat-map: Div for interactive seat map
  - selected-seats-display: Div showing chosen seats dynamically
  - seat-{row}{col}: Button for each seat (row: alphabetic, col: numeric)
  - proceed-booking-button: Button to proceed to booking confirmation
- Navigation:
  - proceed-booking-button: url_for('booking_confirmation', showtime_id=showtime_id) with selected seats passed via form or session

### 6. templates/confirmation.html
- Page Title: Booking Confirmation
- <title> and <h1> text: "Booking Confirmation"
- Element IDs:
  - confirmation-page: Div container
  - booking-summary: Div showing movie, showtime, seats, total price
  - customer-name: Input text field
  - customer-email: Input text field
  - confirm-booking-button: Button to submit booking confirmation (POST)
- Navigation:
  - confirm-booking-button: form POST to url_for('confirm_booking', showtime_id=showtime_id)

### 7. templates/bookings.html
- Page Title: Booking History
- <title> and <h1> text: "Booking History"
- Element IDs:
  - bookings-page: Div container
  - bookings-table: Table listing booking_id, movie title, booking date, seats, status
  - view-booking-button-{booking_id}: Button to view booking details
  - status-filter: Dropdown filter (All, Confirmed, Cancelled, Completed)
  - back-to-dashboard: Button to go back to dashboard
- Navigation:
  - view-booking-button-{booking_id}: url_for('booking_details', booking_id=booking_id)
  - back-to-dashboard: url_for('dashboard')

### 8. templates/booking_details.html
- Page Title: Booking Details
- <title> and <h1> text: "Booking Details"
- Element IDs:
  - booking-details-page: Div container
  - booking-info: Div showing detailed booking info
- Navigation:
  - back-to-bookings-button (optional): url_for('booking_history')

### 9. templates/theater.html
- Page Title: Theater Information
- <title> and <h1> text: "Theater Information"
- Element IDs:
  - theater-page: Div container
  - theaters-list: Div listing all theaters (location, screens, facilities)
  - theater-location-filter: Dropdown filter by location
  - facilities-display: Div showing amenities of selected theater
  - back-to-dashboard: Button to go back to dashboard
- Navigation:
  - back-to-dashboard: url_for('dashboard')

---

## Section 3: Data File Schemas

Each data file is pipe-delimited with NO header line. Fields are exact and in order.

### 1. data/movies.txt
- Fields: movie_id|title|director|genre|rating|duration|description|release_date
- Description: Movie details including metadata for catalog and details page
- Examples:
  - 1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31
  - 2|Inception|Christopher Nolan|Sci-Fi|8.8|148|A skilled thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea.|2010-07-16
  - 3|The Shawshank Redemption|Frank Darabont|Drama|9.3|142|Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.|1994-09-23

### 2. data/theaters.txt
- Fields: theater_id|theater_name|location|city|screens|facilities
- Description: Information about theaters
- Examples:
  - 1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access
  - 2|Galaxy Cinemas|456 Broadway|Los Angeles|8|3D, Premium Sound, Parking
  - 3|Starlight Theater|789 Park Ave|Chicago|6|Luxury Seating, Restaurant, VIP Lounge

### 3. data/showtimes.txt
- Fields: showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats
- Description: Showtimes for movies at theaters
- Examples:
  - 1|1|1|2025-02-01|19:00|12.99|85
  - 2|1|1|2025-02-01|22:30|12.99|40
  - 3|2|2|2025-02-01|18:00|14.99|95

### 4. data/seats.txt
- Fields: seat_id|theater_id|screen_id|row|column|seat_type|status
- Description: Seating map and booking status
- Examples:
  - 1|1|1|A|1|Standard|Available
  - 2|1|1|A|2|Standard|Available
  - 3|1|1|B|5|Premium|Booked

### 5. data/bookings.txt
- Fields: booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked
- Description: Bookings and ticket details
- Examples:
  - 1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2
  - 2|2|Jane Smith|jane@example.com|2025-01-16|12.99|Confirmed|F10
  - 3|3|Robert Johnson|robert@example.com|2025-01-17|29.98|Confirmed|C3,C4

### 6. data/genres.txt
- Fields: genre_id|genre_name|description
- Description: Genre metadata for filtering and display
- Examples:
  - 1|Action|Fast-paced movies with exciting sequences and combat
  - 2|Drama|Character-driven stories exploring complex themes
  - 3|Sci-Fi|Science fiction with futuristic technology and concepts

---

This document fully specifies Flask routes, HTML templates, and data file schemas for the MovieTicketing web application to enable independent parallel frontend and backend development.
