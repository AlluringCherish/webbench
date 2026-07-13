# MovieTicketing Web Application Design Specification

---

## Overview
The MovieTicketing web application enables users to seamlessly browse movies, view showtimes, select seats, book tickets, review booking history, and access theater information. The app uses local text files for data storage in a structured 'data' directory. It consists of eight main pages starting from the Dashboard.

---

## 1. Pages and Routes

### 1. Dashboard Page
- **Route Path**: `/`  
- **HTTP Verb**: GET  
- **Page Title**: Movie Ticketing Dashboard
- **Purpose**: Main hub displaying featured movies and navigation buttons.
- **Elements:**
  - `dashboard-page` (Div) - Main container
  - `featured-movies` (Div) - Featured movie recommendations
  - `browse-movies-button` (Button) - Navigates to Movie Catalog Page
  - `view-bookings-button` (Button) - Navigates to Booking History Page
  - `showtimes-button` (Button) - Navigates to Showtime Selection Page

### 2. Movie Catalog Page
- **Route Path**: `/catalog`  
- **HTTP Verb**: GET  
- **Page Title**: Movie Catalog
- **Purpose**: Browse all movies with search and genre filter functionality.
- **Elements:**
  - `catalog-page` (Div) - Main container
  - `search-input` (Input) - Field to search movies by title or genre
  - `genre-filter` (Dropdown) - Filter by genre (Action, Comedy, Drama, Horror, etc.)
  - `movies-grid` (Div) - Displays movie cards
  - `view-movie-button-{movie_id}` (Button) - Dynamic buttons for viewing movie details

### 3. Movie Details Page
- **Route Path**: `/movie/<int:movie_id>`  
- **HTTP Verb**: GET  
- **Page Title**: Movie Details
- **Purpose**: Display detailed information of the selected movie.
- **Elements:**
  - `movie-details-page` (Div) - Container
  - `movie-title` (H1) - Movie title
  - `movie-director` (Div) - Director name
  - `movie-rating` (Div) - Movie rating
  - `movie-description` (Div) - Movie description
  - `select-showtime-button` (Button) - Proceed to showtime selection

### 4. Showtime Selection Page
- **Route Path**: `/showtimes/<int:movie_id>`  
- **HTTP Verb**: GET  
- **Page Title**: Select Showtime
- **Purpose**: Show available showtimes for the selected movie with filters.
- **Elements:**
  - `showtime-page` (Div) - Container
  - `showtimes-list` (Div) - List of showtimes with date, time, theater, price
  - `theater-filter` (Dropdown) - Filter by theater
  - `date-filter` (Input) - Filter by date
  - `select-showtime-button-{showtime_id}` (Button) - Select a showtime

### 5. Seat Selection Page
- **Route Path**: `/seats/<int:showtime_id>`  
- **HTTP Verb**: GET  
- **Page Title**: Select Seats
- **Purpose**: Interactive seat map for seat selection.
- **Elements:**
  - `seat-selection-page` (Div) - Container
  - `seat-map` (Div) - Interactive seat map
  - `selected-seats-display` (Div) - Shows currently selected seats
  - `seat-{row}{col}` (Button) - Individual seat buttons, e.g., seat-A1
  - `proceed-booking-button` (Button) - Proceed to booking confirmation

### 6. Booking Confirmation Page
- **Route Path**: `/confirm-booking`  
- **HTTP Verb**: POST (submit booking), GET (display form)  
- **Page Title**: Booking Confirmation
- **Purpose**: Review booking details and complete purchase.
- **Elements:**
  - `confirmation-page` (Div) - Container
  - `booking-summary` (Div) - Details of movie, showtime, seats, total
  - `customer-name` (Input) - Input customer name
  - `customer-email` (Input) - Input customer email
  - `confirm-booking-button` (Button) - Confirm and finalize booking

### 7. Booking History Page
- **Route Path**: `/bookings`  
- **HTTP Verb**: GET  
- **Page Title**: Booking History
- **Purpose**: Display previous bookings with filters.
- **Elements:**
  - `bookings-page` (Div) - Container
  - `bookings-table` (Table) - List bookings with ID, movie, date, seats, status
  - `view-booking-button-{booking_id}` (Button) - View booking details
  - `status-filter` (Dropdown) - Filter by status (All, Confirmed, Cancelled, Completed)
  - `back-to-dashboard` (Button) - Navigate back to Dashboard

### 8. Theater Information Page
- **Route Path**: `/theaters`  
- **HTTP Verb**: GET  
- **Page Title**: Theater Information
- **Purpose**: Show theater details and facilities.
- **Elements:**
  - `theater-page` (Div) - Container
  - `theaters-list` (Div) - List theaters with location, screens, facilities
  - `theater-location-filter` (Dropdown) - Filter by location
  - `facilities-display` (Div) - Show amenities
  - `back-to-dashboard` (Button) - Navigate back to Dashboard

---

## 2. Navigation Flow

- The starting page is the Dashboard (`/`).
- From Dashboard:
  - `browse-movies-button` → Movie Catalog Page (`/catalog`)
  - `view-bookings-button` → Booking History Page (`/bookings`)
  - `showtimes-button` → Showtime Selection Page (if movie selected `/showtimes/<movie_id>`, else Catalog or Dashboard)

- From Movie Catalog:
  - `view-movie-button-{movie_id}` → Movie Details Page (`/movie/<movie_id>`)

- From Movie Details:
  - `select-showtime-button` → Showtime Selection Page (`/showtimes/<movie_id>`)

- From Showtime Selection:
  - `select-showtime-button-{showtime_id}` → Seat Selection Page (`/seats/<showtime_id>`)

- From Seat Selection:
  - `proceed-booking-button` → Booking Confirmation Page (`/confirm-booking`)

- From Booking Confirmation:
  - `confirm-booking-button` submits booking, redirect as needed

- From Booking History:
  - `view-booking-button-{booking_id}` shows details (modal or new page)
  - `back-to-dashboard` → Dashboard (`/`)

- From Theater Information:
  - `back-to-dashboard` → Dashboard (`/`)

---

## 3. Local Data Handling

All data are stored in text files in a `data` directory and use pipe `|` delimited formats.

- `movies.txt`: `movie_id|title|director|genre|rating|duration|description|release_date` (Used in Movie Catalog, Details, Showtime Selection)
- `theaters.txt`: `theater_id|theater_name|location|city|screens|facilities` (Used in Theater Information, Showtime Selection)
- `showtimes.txt`: `showtime_id|movie_id|theater_id|showtime_date|showtime_time|price|available_seats` (Used in Showtime Selection, Seat Selection, Booking Confirmation)
- `seats.txt`: `seat_id|theater_id|screen_id|row|column|seat_type|status` (Used in Seat Selection)
- `bookings.txt`: `booking_id|showtime_id|customer_name|customer_email|booking_date|total_price|status|seats_booked` (Used in Booking History, Confirmation)
- `genres.txt`: `genre_id|genre_name|description` (Used in Movie Catalog for genre filtering)

Data reading and writing should handle serialization and updates for seat availability and booking status.

---

## 4. UI Element Summary

### Dashboard Page (`/`)
| Element ID             | Type    | Description                       |
|-----------------------|---------|---------------------------------|
| dashboard-page        | Div     | Main container                   |
| featured-movies       | Div     | Show featured movies             |
| browse-movies-button  | Button  | Navigate to Movie Catalog        |
| view-bookings-button  | Button  | Navigate to Booking History      |
| showtimes-button      | Button  | Navigate to Showtimes            |

### Movie Catalog Page (`/catalog`)
| Element ID                 | Type     | Description                         |
|----------------------------|----------|-----------------------------------|
| catalog-page               | Div      | Main container                     |
| search-input               | Input    | Search by title or genre           |
| genre-filter               | Dropdown | Filter by genre                    |
| movies-grid                | Div      | Movie cards grid                   |
| view-movie-button-{movie_id}| Button  | View details of specific movie    |

### Movie Details Page (`/movie/<movie_id>`)
| Element ID            | Type    | Description                         |
|-----------------------|---------|-----------------------------------|
| movie-details-page     | Div     | Main container                     |
| movie-title            | H1      | Movie title                       |
| movie-director         | Div     | Director name                     |
| movie-rating           | Div     | Movie rating                      |
| movie-description      | Div     | Movie description                 |
| select-showtime-button | Button  | Proceed to showtime selection      |

### Showtime Selection Page (`/showtimes/<movie_id>`)
| Element ID                    | Type     | Description                       |
|------------------------------|----------|---------------------------------|
| showtime-page                | Div      | Main container                   |
| showtimes-list               | Div      | List of showtimes               |
| theater-filter               | Dropdown | Filter by theater              |
| date-filter                  | Input    | Filter by date                 |
| select-showtime-button-{showtime_id} | Button | Select specific showtime  |

### Seat Selection Page (`/seats/<showtime_id>`)
| Element ID            | Type     | Description                       |
|-----------------------|----------|---------------------------------|
| seat-selection-page    | Div      | Main container                   |
| seat-map               | Div      | Interactive seat map             |
| selected-seats-display | Div      | Display selected seats           |
| seat-{row}{col}        | Button   | Individual seat (e.g. seat-A1)   |
| proceed-booking-button | Button   | Proceed to booking confirmation  |

### Booking Confirmation Page (`/confirm-booking`)
| Element ID           | Type    | Description                       |
|----------------------|---------|---------------------------------|
| confirmation-page     | Div     | Main container                   |
| booking-summary      | Div     | Booking details summary          |
| customer-name        | Input   | Customer name input              |
| customer-email       | Input   | Customer email input             |
| confirm-booking-button | Button  | Confirm booking                  |

### Booking History Page (`/bookings`)
| Element ID               | Type     | Description                      |
|-------------------------|----------|--------------------------------|
| bookings-page           | Div      | Main container                  |
| bookings-table          | Table    | List of bookings                |
| view-booking-button-{booking_id} | Button  | View booking details          |
| status-filter           | Dropdown | Filter bookings by status       |
| back-to-dashboard       | Button   | Navigate to Dashboard           |

### Theater Information Page (`/theaters`)
| Element ID              | Type     | Description                     |
|------------------------|----------|--------------------------------|
| theater-page            | Div      | Main container                 |
| theaters-list           | Div      | List of theaters               |
| theater-location-filter | Dropdown | Filter theaters by location    |
| facilities-display      | Div      | Theater facilities             |
| back-to-dashboard       | Button   | Navigate to Dashboard          |

---

This concludes the consolidated and consistent design specification for the MovieTicketing web application.