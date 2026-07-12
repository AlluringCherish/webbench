from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.secret_key = 'movie_ticketing_secret_key'

DATA_DIR = 'data'

# Utility functions to load data

def load_movies():
    movies = []
    try:
        with open(os.path.join(DATA_DIR, 'movies.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                movie = {
                    'movie_id': int(parts[0]),
                    'title': parts[1],
                    'director': parts[2],
                    'genre': parts[3],
                    'rating': float(parts[4]),
                    'duration': int(parts[5]),
                    'description': parts[6],
                    'release_date': parts[7]
                }
                movies.append(movie)
    except Exception:
        pass
    return movies


def load_theaters():
    theaters = []
    try:
        with open(os.path.join(DATA_DIR, 'theaters.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                theater = {
                    'theater_id': int(parts[0]),
                    'theater_name': parts[1],
                    'location': parts[2],
                    'city': parts[3],
                    'screens': int(parts[4]),
                    'facilities': parts[5]
                }
                theaters.append(theater)
    except Exception:
        pass
    return theaters


def load_showtimes():
    showtimes = []
    try:
        with open(os.path.join(DATA_DIR, 'showtimes.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                showtime = {
                    'showtime_id': int(parts[0]),
                    'movie_id': int(parts[1]),
                    'theater_id': int(parts[2]),
                    'showtime_date': parts[3],
                    'showtime_time': parts[4],
                    'price': float(parts[5]),
                    'available_seats': int(parts[6])
                }
                showtimes.append(showtime)
    except Exception:
        pass
    return showtimes


def load_seats():
    seats = []
    try:
        with open(os.path.join(DATA_DIR, 'seats.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                seat = {
                    'seat_id': int(parts[0]),
                    'theater_id': int(parts[1]),
                    'screen_id': int(parts[2]),
                    'row': parts[3],
                    'column': int(parts[4]),
                    'seat_type': parts[5],
                    'status': parts[6]
                }
                seats.append(seat)
    except Exception:
        pass
    return seats


def load_bookings():
    bookings = []
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                seats_list = parts[7].split(',') if parts[7] else []
                booking = {
                    'booking_id': int(parts[0]),
                    'showtime_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'booking_date': parts[4],
                    'total_price': float(parts[5]),
                    'status': parts[6],
                    'seats_booked': seats_list
                }
                bookings.append(booking)
    except Exception:
        pass
    return bookings


def load_genres():
    genres = []
    try:
        with open(os.path.join(DATA_DIR, 'genres.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                genre = {
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                }
                genres.append(genre)
    except Exception:
        pass
    return genres

# Utility save function for bookings

def save_bookings(bookings):
    lines = []
    for b in bookings:
        seats_str = ','.join(b['seats_booked'])
        line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']}|{b['status']}|{seats_str}"
        lines.append(line)
    try:
        with open(os.path.join(DATA_DIR, 'bookings.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception:
        pass

# Root redirect
@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard_page'))

# 2. Dashboard page
@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    movies = load_movies()
    # Filter featured & upcoming movies - for this example, featured are those with rating >= 8.5 released in future or recent
    today_str = datetime.datetime.now().date().isoformat()
    featured = []
    for movie in movies:
        if movie['rating'] >= 8.5:
            # Consider upcoming as release_date in future or within 30 days past
            try:
                rdate = datetime.datetime.strptime(movie['release_date'], '%Y-%m-%d').date()
                delta = (rdate - datetime.datetime.now().date()).days
                if delta >= 0 or delta >= -30:
                    featured.append({
                        'movie_id': movie['movie_id'],
                        'title': movie['title'],
                        'rating': movie['rating'],
                        'genre': movie['genre']
                    })
            except Exception:
                continue
    return render_template('dashboard.html', featured_movies=featured)

# 3. Movie Catalog
@app.route('/movies', methods=['GET'])
def movie_catalog():
    movies = load_movies()
    genres = load_genres()
    search_query = request.args.get('search_query', '').strip()
    genre_filter = request.args.get('genre_filter', '').strip()

    filtered_movies = movies
    if search_query:
        sq_lower = search_query.lower()
        filtered_movies = [m for m in filtered_movies if (sq_lower in m['title'].lower() or sq_lower in m['genre'].lower())]
    if genre_filter:
        filtered_movies = [m for m in filtered_movies if m['genre'].lower() == genre_filter.lower()]

    # Prepare the exact dictionary for movies context
    movies_context = []
    for m in filtered_movies:
        movies_context.append({
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration'],
            'poster_url': ''  # Not specified in data file, set empty string
        })

    # Prepare genres context
    genres_context = [{'genre_id': g['genre_id'], 'genre_name': g['genre_name']} for g in genres]

    return render_template('movie_catalog.html', movies=movies_context, genres=genres_context,
                           search_query=search_query, genre_filter=genre_filter)

# 4. Movie Details
@app.route('/movies/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)

# 5. Showtime Selection
@app.route('/showtimes/<int:movie_id>', methods=['GET'])
def showtime_selection(movie_id):
    movies = load_movies()
    theaters = load_theaters()
    showtimes = load_showtimes()

    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404

    selected_theater = request.args.get('selected_theater', '').strip()
    selected_date = request.args.get('selected_date', '').strip()

    filtered_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]
    if selected_theater:
        # Filter by theater name
        theater_ids = [t['theater_id'] for t in theaters if t['theater_name'].lower() == selected_theater.lower()]
        filtered_showtimes = [s for s in filtered_showtimes if s['theater_id'] in theater_ids]
    if selected_date:
        filtered_showtimes = [s for s in filtered_showtimes if s['showtime_date'] == selected_date]

    # Prepare showtimes with theater_name in context
    showtimes_context = []
    for s in filtered_showtimes:
        theater_name = next((t['theater_name'] for t in theaters if t['theater_id'] == s['theater_id']), '')
        showtimes_context.append({
            'showtime_id': s['showtime_id'],
            'theater_name': theater_name,
            'showtime_date': s['showtime_date'],
            'showtime_time': s['showtime_time'],
            'price': s['price']
        })

    theaters_context = [{'theater_id': t['theater_id'], 'theater_name': t['theater_name']} for t in theaters]

    return render_template('showtime_selection.html', movie=movie, showtimes=showtimes_context, theaters=theaters_context,
                           selected_theater=selected_theater, selected_date=selected_date)

# 6. Seat Selection
@app.route('/seats/<int:showtime_id>', methods=['GET'])
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    movies = load_movies()
    theaters = load_theaters()
    seats = load_seats()

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)

    # Compose showtime dict per specification
    showtime_context = {
        'showtime_id': showtime['showtime_id'],
        'movie_title': movie['title'] if movie else '',
        'theater_name': theater['theater_name'] if theater else '',
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time']
    }

    # Filter seats by theater_id and screen_id = 1 (assuming screen_id = 1 as no screen info in showtimes)
    # Seat identifiers formed as row + column
    seats_context = []
    for seat in seats:
        if seat['theater_id'] == showtime['theater_id'] and seat['screen_id'] == 1:
            seats_context.append({
                'seat_id': seat['seat_id'],
                'row': seat['row'],
                'column': seat['column'],
                'seat_type': seat['seat_type'],
                'status': seat['status']
            })

    selected_seats = []

    return render_template('seat_selection.html', showtime=showtime_context, seats=seats_context, selected_seats=selected_seats)

# Helper: get next booking id

def get_next_booking_id(bookings):
    if not bookings:
        return 1
    return max(b['booking_id'] for b in bookings) + 1

# 7. Booking Confirmation GET
@app.route('/booking_confirmation/<int:showtime_id>', methods=['GET'])
def booking_confirmation(showtime_id):
    showtimes = load_showtimes()
    movies = load_movies()
    theaters = load_theaters()

    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)

    showtime_context = {
        'showtime_id': showtime['showtime_id'],
        'movie_title': movie['title'] if movie else '',
        'theater_name': theater['theater_name'] if theater else '',
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time']
    }

    selected_seats = request.args.getlist('seats')
    total_price = showtime['price'] * len(selected_seats) if selected_seats else 0.0

    return render_template('booking_confirmation.html', showtime=showtime_context, selected_seats=selected_seats, total_price=total_price)

# 8. Confirm Booking POST
@app.route('/booking_confirmation/<int:showtime_id>', methods=['POST'])
def confirm_booking(showtime_id):
    customer_name = request.form.get('customer_name', '')
    customer_email = request.form.get('customer_email', '')
    seats = request.form.getlist('seats')

    if not customer_name or not customer_email or not seats:
        return "Missing information", 400

    bookings = load_bookings()
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    # Calculate total price
    total_price = showtime['price'] * len(seats)

    # Create new booking
    new_booking = {
        'booking_id': get_next_booking_id(bookings),
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': datetime.datetime.now().date().isoformat(),
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': seats
    }

    bookings.append(new_booking)
    save_bookings(bookings)

    # Redirect to booking history page
    return redirect(url_for('booking_history'))

# 9. Booking History
@app.route('/bookings', methods=['GET'])
def booking_history():
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    status_filter = request.args.get('status_filter', '').strip()

    filtered_bookings = bookings
    if status_filter:
        filtered_bookings = [b for b in filtered_bookings if b['status'].lower() == status_filter.lower()]

    bookings_context = []
    for b in filtered_bookings:
        showtime = next((s for s in showtimes if s['showtime_id'] == b['showtime_id']), None)
        movie_title = ''
        if showtime:
            movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
            if movie:
                movie_title = movie['title']
        bookings_context.append({
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'booking_date': b['booking_date'],
            'seats_booked': b['seats_booked'],
            'status': b['status'],
            'total_price': b['total_price']
        })

    return render_template('booking_history.html', bookings=bookings_context, status_filter=status_filter)

# 10. Booking Detail
@app.route('/bookings/<int:booking_id>', methods=['GET'])
def booking_detail(booking_id):
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
    movie_title = ''
    if showtime:
        movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
        if movie:
            movie_title = movie['title']

    booking_context = {
        'booking_id': booking['booking_id'],
        'showtime_id': booking['showtime_id'],
        'movie_title': movie_title,
        'customer_name': booking['customer_name'],
        'customer_email': booking['customer_email'],
        'booking_date': booking['booking_date'],
        'seats_booked': booking['seats_booked'],
        'total_price': booking['total_price'],
        'status': booking['status']
    }

    return render_template('booking_detail.html', booking=booking_context)

# 11. Theater Information
@app.route('/theaters', methods=['GET'])
def theater_information():
    theaters = load_theaters()
    location_filter = request.args.get('location_filter', '').strip()

    filtered_theaters = theaters
    if location_filter:
        filtered_theaters = [t for t in theaters if t['location'].lower() == location_filter.lower() or t['city'].lower() == location_filter.lower()]

    theaters_context = []
    for t in filtered_theaters:
        theaters_context.append({
            'theater_id': t['theater_id'],
            'theater_name': t['theater_name'],
            'location': t['location'],
            'city': t['city'],
            'screens': t['screens'],
            'facilities': t['facilities']
        })

    return render_template('theater_information.html', theaters=theaters_context, location_filter=location_filter)


if __name__ == '__main__':
    app.run()
