'''
Main backend Python file for the MovieTicketing web application.
Implements all routes and functionalities according to the requirements document,
including data loading from local text files, filtering, and rendering templates.
Ensures the application starts from the Dashboard page and supports all eight pages.
'''
from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data/'
# Utility functions to load data from files
def load_movies():
    movies = []
    with open(DATA_DIR + 'movies.txt', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            movie = {
                'movie_id': int(row[0]),
                'title': row[1],
                'director': row[2],
                'genre': row[3],
                'rating': float(row[4]),
                'duration': int(row[5]),
                'description': row[6],
                'release_date': row[7]
            }
            movies.append(movie)
    return movies
def load_theaters():
    theaters = []
    with open(DATA_DIR + 'theaters.txt', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            theater = {
                'theater_id': int(row[0]),
                'theater_name': row[1],
                'location': row[2],
                'city': row[3],
                'screens': int(row[4]),
                'facilities': [fac.strip() for fac in row[5].split(',')] if row[5].strip() else []
            }
            theaters.append(theater)
    return theaters
def load_showtimes():
    showtimes = []
    with open(DATA_DIR + 'showtimes.txt', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            showtime = {
                'showtime_id': int(row[0]),
                'movie_id': int(row[1]),
                'theater_id': int(row[2]),
                'showtime_date': row[3],
                'showtime_time': row[4],
                'price': float(row[5]),
                'available_seats': int(row[6])
            }
            showtimes.append(showtime)
    return showtimes
def load_seats():
    seats = []
    with open(DATA_DIR + 'seats.txt', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            seat = {
                'seat_id': int(row[0]),
                'theater_id': int(row[1]),
                'screen_id': int(row[2]),
                'row': row[3],
                'column': int(row[4]),
                'seat_type': row[5],
                'status': row[6]
            }
            seats.append(seat)
    return seats
def load_bookings():
    bookings = []
    with open(DATA_DIR + 'bookings.txt', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            booking = {
                'booking_id': int(row[0]),
                'showtime_id': int(row[1]),
                'customer_name': row[2],
                'customer_email': row[3],
                'booking_date': row[4],
                'total_price': float(row[5]),
                'status': row[6],
                'seats_booked': row[7].split(',') if row[7].strip() else []
            }
            bookings.append(booking)
    return bookings
def load_genres():
    genres = []
    with open(DATA_DIR + 'genres.txt', newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            genre = {
                'genre_id': int(row[0]),
                'genre_name': row[1],
                'description': row[2]
            }
            genres.append(genre)
    return genres
# Route: Dashboard page
@app.route('/')
def dashboard():
    """
    Dashboard page showing featured movies, upcoming releases,
    and navigation buttons to browse movies, showtimes, bookings, and theaters.
    """
    movies = load_movies()
    today = datetime.today().date()
    # Featured movies: top rated movies (rating >= 8.5) released before or on today
    featured_movies = [m for m in movies if m['rating'] >= 8.5 and datetime.strptime(m['release_date'], '%Y-%m-%d').date() <= today]
    featured_movies = sorted(featured_movies, key=lambda m: m['rating'], reverse=True)[:5]
    # Upcoming releases: movies with release_date in the future
    upcoming_releases = [m for m in movies if datetime.strptime(m['release_date'], '%Y-%m-%d').date() > today]
    upcoming_releases = sorted(upcoming_releases, key=lambda m: m['release_date'])[:5]
    return render_template('dashboard.html',
                           featured_movies=featured_movies,
                           upcoming_releases=upcoming_releases)
# Route: Movie catalog page with search and genre filter
@app.route('/catalog')
def movie_catalog():
    """
    Displays a catalog of movies with search by title or genre and genre filter dropdown.
    """
    search_query = request.args.get('search', '').strip().lower()
    genre_filter = request.args.get('genre', 'All')
    movies = load_movies()
    genres = [g['genre_name'] for g in load_genres()]
    genres = ['All'] + sorted(genres)
    filtered_movies = []
    for movie in movies:
        matches_search = (search_query in movie['title'].lower()) or (search_query in movie['genre'].lower()) if search_query else True
        matches_genre = (genre_filter == 'All' or movie['genre'] == genre_filter)
        if matches_search and matches_genre:
            filtered_movies.append(movie)
    return render_template('movie_catalog.html',
                           movies=filtered_movies,
                           genres=genres,
                           selected_genre=genre_filter,
                           search_query=search_query)
# Route: Movie details page
@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    """
    Displays detailed information about a specific movie.
    """
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html',
                           movie=movie)
# Route: Showtime selection page for a movie
@app.route('/movie/<int:movie_id>/showtimes')
def showtime_selection(movie_id):
    """
    Displays available showtimes for the selected movie with theater and date filters.
    """
    theater_filter = request.args.get('theater', 'All')
    date_filter = request.args.get('date', '').strip()
    showtimes = load_showtimes()
    theaters = load_theaters()
    movies = load_movies()
    # Validate movie exists
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    # Filter showtimes for this movie and upcoming dates
    today = datetime.today().date()
    filtered_showtimes = []
    for st in showtimes:
        if st['movie_id'] == movie_id:
            showtime_date_obj = datetime.strptime(st['showtime_date'], '%Y-%m-%d').date()
            if showtime_date_obj >= today:
                if theater_filter != 'All' and str(st['theater_id']) != theater_filter:
                    continue
                if date_filter and st['showtime_date'] != date_filter:
                    continue
                theater = next((t for t in theaters if t['theater_id'] == st['theater_id']), None)
                if theater:
                    st_copy = st.copy()
                    st_copy['theater_name'] = theater['theater_name']
                    filtered_showtimes.append(st_copy)
    # Prepare theater options for filter dropdown
    theater_options = [('All', 'All Theaters')] + [(str(t['theater_id']), t['theater_name']) for t in theaters]
    return render_template('showtime_selection.html',
                           movie=movie,
                           showtimes=filtered_showtimes,
                           theater_options=theater_options,
                           selected_theater=theater_filter,
                           selected_date=date_filter)
# New Route: General showtimes page with filtering options
@app.route('/showtimes')
def showtimes():
    """
    Displays all upcoming showtimes with filtering options (theater, date).
    """
    theater_filter = request.args.get('theater', 'All')
    date_filter = request.args.get('date', '').strip()
    showtimes = load_showtimes()
    theaters = load_theaters()
    movies = load_movies()
    today = datetime.today().date()
    filtered_showtimes = []
    for st in showtimes:
        showtime_date_obj = datetime.strptime(st['showtime_date'], '%Y-%m-%d').date()
        if showtime_date_obj >= today:
            if theater_filter != 'All' and str(st['theater_id']) != theater_filter:
                continue
            if date_filter and st['showtime_date'] != date_filter:
                continue
            theater = next((t for t in theaters if t['theater_id'] == st['theater_id']), None)
            movie = next((m for m in movies if m['movie_id'] == st['movie_id']), None)
            if theater and movie:
                st_copy = st.copy()
                st_copy['theater_name'] = theater['theater_name']
                st_copy['movie_title'] = movie['title']
                filtered_showtimes.append(st_copy)
    theater_options = [('All', 'All Theaters')] + [(str(t['theater_id']), t['theater_name']) for t in theaters]
    return render_template('showtimes.html',
                           showtimes=filtered_showtimes,
                           theater_options=theater_options,
                           selected_theater=theater_filter,
                           selected_date=date_filter)
# Route: Seat selection page for a showtime
@app.route('/showtime/<int:showtime_id>/seats')
def seat_selection(showtime_id):
    """
    Displays seat map for a showtime to allow seat selection.
    """
    showtimes = load_showtimes()
    showtime = next((st for st in showtimes if st['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    if not theater:
        return "Theater not found", 404
    seats = load_seats()
    # For simplicity, assume screen_id = 1 for all showtimes
    screen_id = 1
    theater_seats = [s for s in seats if s['theater_id'] == theater['theater_id'] and s['screen_id'] == screen_id]
    # Organize seats by row and column for display
    seat_map = {}
    for seat in theater_seats:
        row = seat['row']
        if row not in seat_map:
            seat_map[row] = []
        seat_map[row].append(seat)
    # Sort seats in each row by column
    for row in seat_map:
        seat_map[row].sort(key=lambda s: s['column'])
    return render_template('seat_selection.html',
                           showtime=showtime,
                           theater=theater,
                           seat_map=seat_map)
# Route: Booking confirmation page (GET to show form, POST to confirm booking)
@app.route('/showtime/<int:showtime_id>/confirm', methods=['GET', 'POST'])
def booking_confirmation(showtime_id):
    """
    Booking confirmation page to review booking details and complete purchase.
    """
    showtimes = load_showtimes()
    showtime = next((st for st in showtimes if st['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if not movie:
        return "Movie not found", 404
    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    if not theater:
        return "Theater not found", 404
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        seats_selected = request.form.get('seats_selected', '').strip()  # comma separated seat IDs like A1,A2
        if not customer_name or not customer_email or not seats_selected:
            error = "Please fill in all fields and select seats."
            return render_template('booking_confirmation.html',
                                   showtime=showtime,
                                   movie=movie,
                                   theater=theater,
                                   seats_selected=seats_selected,
                                   error=error)
        seats_list = [s.strip() for s in seats_selected.split(',') if s.strip()]
        # Calculate total price
        total_price = len(seats_list) * showtime['price']
        # Load existing bookings to generate new booking_id
        bookings = load_bookings()
        new_booking_id = max([b['booking_id'] for b in bookings], default=0) + 1
        # Booking date is today
        booking_date = datetime.today().strftime('%Y-%m-%d')
        # Append new booking to bookings.txt
        with open(DATA_DIR + 'bookings.txt', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            writer.writerow([
                new_booking_id,
                showtime_id,
                customer_name,
                customer_email,
                booking_date,
                f"{total_price:.2f}",
                'Confirmed',
                ','.join(seats_list)
            ])
        # Update seat status to Booked in seats.txt
        # Load all seats
        seats = load_seats()
        # Mark selected seats as Booked
        for seat in seats:
            seat_code = f"{seat['row']}{seat['column']}"
            if seat_code in seats_list and seat['theater_id'] == theater['theater_id'] and seat['screen_id'] == 1:
                seat['status'] = 'Booked'
        # Write back all seats
        with open(DATA_DIR + 'seats.txt', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            for seat in seats:
                writer.writerow([
                    seat['seat_id'],
                    seat['theater_id'],
                    seat['screen_id'],
                    seat['row'],
                    seat['column'],
                    seat['seat_type'],
                    seat['status']
                ])
        # Update available seats in showtimes.txt
        for st in showtimes:
            if st['showtime_id'] == showtime_id:
                st['available_seats'] = max(0, st['available_seats'] - len(seats_list))
        with open(DATA_DIR + 'showtimes.txt', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            for st in showtimes:
                writer.writerow([
                    st['showtime_id'],
                    st['movie_id'],
                    st['theater_id'],
                    st['showtime_date'],
                    st['showtime_time'],
                    f"{st['price']:.2f}",
                    st['available_seats']
                ])
        return redirect(url_for('booking_history'))
    else:
        # GET method: show booking confirmation page
        seats_selected = request.args.get('seats', '')
        seats_selected_list = [s.strip() for s in seats_selected.split(',')] if seats_selected else []
        total_price = len(seats_selected_list) * showtime['price'] if seats_selected_list else 0.0
        return render_template('booking_confirmation.html',
                               showtime=showtime,
                               movie=movie,
                               theater=theater,
                               seats_selected=seats_selected,
                               total_price=total_price,
                               error=None)
# Route: Booking history page with status filter
@app.route('/bookings')
def booking_history():
    """
    Displays all previous bookings with ticket information and status filter.
    """
    status_filter = request.args.get('status', 'All')
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()
    theaters = load_theaters()
    filtered_bookings = []
    for booking in bookings:
        if status_filter != 'All' and booking['status'] != status_filter:
            continue
        st = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
        if not st:
            continue
        movie = next((m for m in movies if m['movie_id'] == st['movie_id']), None)
        theater = next((t for t in theaters if t['theater_id'] == st['theater_id']), None)
        booking_copy = booking.copy()
        booking_copy['movie_title'] = movie['title'] if movie else 'Unknown'
        booking_copy['theater_name'] = theater['theater_name'] if theater else 'Unknown'
        booking_copy['showtime_date'] = st['showtime_date']
        booking_copy['showtime_time'] = st['showtime_time']
        filtered_bookings.append(booking_copy)
    statuses = ['All', 'Confirmed', 'Cancelled', 'Completed']
    return render_template('booking_history.html',
                           bookings=filtered_bookings,
                           selected_status=status_filter,
                           statuses=statuses)
# Route: Booking details page (view booking details)
@app.route('/booking/<int:booking_id>')
def booking_details(booking_id):
    """
    Displays detailed information about a specific booking.
    """
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404
    showtimes = load_showtimes()
    st = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
    if not st:
        return "Showtime not found", 404
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == st['movie_id']), None)
    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == st['theater_id']), None)
    return render_template('booking_details.html',
                           booking=booking,
                           showtime=st,
                           movie=movie,
                           theater=theater)
# Route: Theater information page with location filter
@app.route('/theaters/info')
def theater_information():
    """
    Displays information about theaters and their facilities with location filter.
    """
    location_filter = request.args.get('location', 'All')
    theaters = load_theaters()
    locations = sorted(set(t['location'] for t in theaters))
    locations = ['All'] + locations
    filtered_theaters = []
    for theater in theaters:
        if location_filter == 'All' or theater['location'] == location_filter:
            filtered_theaters.append(theater)
    return render_template('theater_information.html',
                           theaters=filtered_theaters,
                           locations=locations,
                           selected_location=location_filter)
# Route: Redirect buttons from dashboard to other pages
@app.route('/navigate/<string:page>')
def navigate(page):
    """
    Helper route to navigate from dashboard buttons to other pages.
    """
    if page == 'catalog':
        return redirect(url_for('movie_catalog'))
    elif page == 'bookings':
        return redirect(url_for('booking_history'))
    elif page == 'showtimes':
        # Redirect to the new general showtimes page
        return redirect(url_for('showtimes'))
    elif page == 'theaters':
        return redirect(url_for('theater_information'))
    else:
        return redirect(url_for('dashboard'))
# Run the app
if __name__ == '__main__':
    app.run(debug=True)