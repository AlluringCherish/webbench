# Requirements Analysis for MovieTicketing Web Application

## 1. Pages and UI Elements

### 1. Dashboard Page
- Page Title: Movie Ticketing Dashboard
- Overview: Main hub displaying featured movies, upcoming releases, and quick navigation.
- Elements:
  - ID: dashboard-page - Type: Div - Container for the dashboard.
  - ID: featured-movies - Type: Div - Display featured movie recommendations.
  - ID: browse-movies-button - Type: Button - Navigate to Movie Catalog Page.
  - ID: view-bookings-button - Type: Button - Navigate to Booking History Page.
  - ID: showtimes-button - Type: Button - Navigate to Showtimes Page.

### 2. Movie Catalog Page
- Page Title: Movie Catalog
- Overview: Display all available movies with search and filters.
- Elements:
  - ID: catalog-page - Type: Div - Container for catalog.
  - ID: search-input - Type: Input - Search field for movie title or genre.
  - ID: genre-filter - Type: Dropdown - Filter by genre (e.g., Action, Comedy, Drama, Horror).
  - ID: movies-grid - Type: Div - Grid displaying movie cards.
  - ID Pattern: view-movie-button-{movie_id} - Type: Button - View details for specific movie.

### 3. Movie Details Page
- Page Title: Movie Details
- Overview: Detailed information about a specific movie.
- Elements:
  - ID: movie-details-page - Type: Div - Container for details.
  - ID: movie-title - Type: H1 - Display movie title.
  - ID: movie-director - Type: Div - Display director.
  - ID: movie-rating - Type: Div - Display rating.
  - ID: movie-description - Type: Div - Display description.
  - ID: select-showtime-button - Type: Button - Proceed to showtime selection.

### 4. Showtime Selection Page
- Page Title: Select Showtime
- Overview: Show available showtimes for selected movie in theaters.
- Elements:
  - ID: showtime-page - Type: Div - Container.
  - ID: showtimes-list - Type: Div - List showtimes with date, time, theater, price.
  - ID: theater-filter - Type: Dropdown - Filter showtimes by theater.
  - ID: date-filter - Type: Input - Filter showtimes by date.
  - ID Pattern: select-showtime-button-{showtime_id} - Type: Button - Select specific showtime.

### 5. Seat Selection Page
- Page Title: Select Seats
- Overview: Interactive seat map for selecting seats.
- Elements:
  - ID: seat-selection-page - Type: Div - Container.
  - ID: seat-map - Type: Div - Interactive seat map with availability.
  - ID: selected-seats-display - Type: Div - Display currently selected seats.
  - ID Pattern: seat-{row}{col} (e.g., seat-A1) - Type: Button - Individual seat selection.
  - ID: proceed-booking-button - Type: Button - Proceed to booking confirmation.

### 6. Booking Confirmation Page
- Page Title: Booking Confirmation
- Overview: Review and complete booking.
- Elements:
  - ID: confirmation-page - Type: Div - Container.
  - ID: booking-summary - Type: Div - Summary of booking (movie, showtime, seats, total).
  - ID: customer-name - Type: Input - Input customer name.
  - ID: customer-email - Type: Input - Input customer email.
  - ID: confirm-booking-button - Type: Button - Confirm and complete booking.

### 7. Booking History Page
- Page Title: Booking History
- Overview: Display previous bookings.
- Elements:
  - ID: bookings-page - Type: Div - Container.
  - ID: bookings-table - Type: Table - Displays booking ID, movie, date, seats, status.
  - ID Pattern: view-booking-button-{booking_id} - Type: Button - View booking details.
  - ID: status-filter - Type: Dropdown - Filter bookings by status (All, Confirmed, Cancelled, Completed).
  - ID: back-to-dashboard - Type: Button - Navigate back to Dashboard.

### 8. Theater Information Page
- Page Title: Theater Information
- Overview: Theater information and facilities.
- Elements:
  - ID: theater-page - Type: Div - Container.
  - ID: theaters-list - Type: Div - List theaters with location, screens, facilities.
  - ID: theater-location-filter - Type: Dropdown - Filter theaters by location.
  - ID: facilities-display - Type: Div - Display theater facilities and amenities.
  - ID: back-to-dashboard - Type: Button - Navigate back to Dashboard.

## 2. Data Entities and Storage

All data files are text files located in the 'data' directory, with fields separated by pipe (|) delimiter and no header lines stored in the file.

### 1. Movies Data (movies.txt)
- Fields: movie_id, title, director, genre, rating, duration, description, release_date
- Example:
  1|The Matrix|Lana Wachowski|Action|8.7|136|A computer hacker learns about the true nature of reality and his role in the war against its controllers.|1999-03-31

### 2. Theaters Data (theaters.txt)
- Fields: theater_id, theater_name, location, city, screens, facilities
- Example:
  1|Cinema Max|123 Main St|New York|10|IMAX, Dolby, Wheelchair Access

### 3. Showtimes Data (showtimes.txt)
- Fields: showtime_id, movie_id, theater_id, showtime_date, showtime_time, price, available_seats
- Example:
  1|1|1|2025-02-01|19:00|12.99|85

### 4. Seats Data (seats.txt)
- Fields: seat_id, theater_id, screen_id, row, column, seat_type, status
- Example:
  1|1|1|A|1|Standard|Available

### 5. Bookings Data (bookings.txt)
- Fields: booking_id, showtime_id, customer_name, customer_email, booking_date, total_price, status, seats_booked
- Example:
  1|1|John Doe|john@example.com|2025-01-15|25.98|Confirmed|A1,A2

### 6. Genres Data (genres.txt)
- Fields: genre_id, genre_name, description
- Example:
  1|Action|Fast-paced movies with exciting sequences and combat

## 3. Navigation and Functional Flow

- The website starts on the Dashboard Page (dashboard-page).
- Dashboard buttons navigate to:
  - Movie Catalog (browse-movies-button)
  - Booking History (view-bookings-button)
  - Showtimes Page (showtimes-button)

- Movie Catalog features:
  - Search (search-input) to filter movies by title or genre.
  - Genre filter dropdown (genre-filter).
  - Each movie card includes a button (view-movie-button-{movie_id}) to view details.

- Movie Details Page:
  - Displays detailed info with a button (select-showtime-button) to proceed to Showtime Selection.

- Showtime Selection Page:
  - Filters showtimes by theater (theater-filter) and date (date-filter).
  - Each showtime has a select button (select-showtime-button-{showtime_id}).

- Seat Selection Page:
  - Interactive seats with buttons (seat-{row}{col}) for selection.
  - Proceed booking button (proceed-booking-button) moves to Booking Confirmation.

- Booking Confirmation Page:
  - Takes customer name and email inputs.
  - Confirmation button (confirm-booking-button) finalizes booking.

- Booking History Page:
  - Filter by booking status (status-filter).
  - Each booking has a view button (view-booking-button-{booking_id}).
  - Back to dashboard button (back-to-dashboard).

- Theater Information Page:
  - Filter theaters by location (theater-location-filter).
  - Back to dashboard button (back-to-dashboard).

This concludes the detailed requirements analysis with all specified pages, UI elements, data files, and navigation flows documented for the MovieTicketing application.