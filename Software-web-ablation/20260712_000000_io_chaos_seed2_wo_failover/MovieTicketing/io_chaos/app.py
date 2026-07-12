from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Helper functions to load data from files

def load_movies():
    movies = []
    try:
        with open('data/movies.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
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
        with open('data/theaters.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
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
        with open('data/showtimes.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
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
        with open('data/seats.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 7:
                    continue
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
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                booking = {
                    'booking_id': int(parts[0]),
                    'showtime_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'booking_date': parts[4],
                    'total_price': float(parts[5]),
                    'status': parts[6],
                    'seats_booked': parts[7].split(',') if parts[7] else []
                }
                bookings.append(booking)
    except Exception:
        pass
    return bookings


def load_genres():
    genres = []
    try:
        with open('data/genres.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                genre = {
                    'genre_id': int(parts[0]),
                    'genre_name': parts[1],
                    'description': parts[2]
                }
                genres.append(genre)
    except Exception:
        pass
    return genres

# Helper functions to save data to files

def save_bookings(bookings):
    try:
        lines = []
        for booking in bookings:
            line = '|'.join([
                str(booking['booking_id']),
                str(booking['showtime_id']),
                booking['customer_name'],
                booking['customer_email'],
                booking['booking_date'],
                f"{booking['total_price']:.2f}",
                booking['status'],
                ','.join(booking['seats_booked'])
            ])
            lines.append(line)
        with open('data/bookings.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return True
    except Exception:
        return False


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    movies = load_movies()
    today_str = datetime.today().strftime('%Y-%m-%d')

    # Featured movies: top 5 highest rating (descending order)
    featured_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)[:5]

    # Upcoming releases: movies releasing in future sorted by release_date ascending
    upcoming_releases = [m for m in movies if m['release_date'] > today_str]
    upcoming_releases = sorted(upcoming_releases, key=lambda x: x['release_date'])[:5]

    # Prepare movie dicts with required fields only
    def simple_movie_dict(m):
        return {
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration']
        }

    featured_movies = [simple_movie_dict(m) for m in featured_movies]
    upcoming_releases = [simple_movie_dict(m) for m in upcoming_releases]

    return render_template('dashboard.html', featured_movies=featured_movies, upcoming_releases=upcoming_releases)


@app.route('/movies')
def movie_catalog():
    movies = load_movies()
    genres = load_genres()

    # Provide only specified fields for movies
    movie_list = [{
        'movie_id': m['movie_id'],
        'title': m['title'],
        'genre': m['genre'],
        'rating': m['rating'],
        'duration': m['duration']
    } for m in movies]

    return render_template('movie_catalog.html', movies=movie_list, genres=genres)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if movie is None:
        return "Movie not found", 404

    return render_template('movie_details.html', movie=movie)


@app.route('/showtimes/select/<int:movie_id>')
def select_showtime(movie_id):
    showtimes = load_showtimes()
    # Filter showtimes for movie_id
    filtered_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]

    theaters = load_theaters()

    return render_template('showtime_selection.html', showtimes=filtered_showtimes, theaters=theaters)


@app.route('/seats/select/<int:showtime_id>')
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if showtime is None:
        return "Showtime not found", 404

    seats = load_seats()
    # Find theater_id from showtime
    theater_id = showtime['theater_id']
    # For simplicity assume screen_id is 1 (Not given explicitly in showtime data)
    screen_id = 1
    seat_map = [seat for seat in seats if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id]

    # Prepare selected_showtime dict with required fields
    selected_showtime = {
        'showtime_id': showtime['showtime_id'],
        'movie_id': showtime['movie_id'],
        'theater_id': showtime['theater_id'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'price': showtime['price']
    }

    return render_template('seat_selection.html', seat_map=seat_map, selected_showtime=selected_showtime)


@app.route('/booking/confirm/<int:showtime_id>', methods=['GET'])
def booking_confirmation(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if showtime is None:
        return "Showtime not found", 404

    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)
    if movie is None:
        return "Movie not found", 404

    # For simplicity, seats selected is expected as query parameters seats=comma separated seat names
    seat_names_str = request.args.get('seats', '')
    seats_selected = seat_names_str.split(',') if seat_names_str else []

    total_price = showtime['price'] * len(seats_selected)

    booking_summary = {
        'movie_title': movie['title'],
        'showtime_info': f"{showtime['showtime_date']} {showtime['showtime_time']} at Theater {showtime['theater_id']}",
        'seats_selected': seats_selected,
        'total_price': total_price
    }

    return render_template('booking_confirmation.html', booking_summary=booking_summary)


@app.route('/booking/confirm/<int:showtime_id>', methods=['POST'])
def process_booking(showtime_id):
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()

    if not customer_name or not customer_email:
        return "Customer name and email are required", 400

    seats_selected_str = request.args.get('seats', '')
    seats_selected = seats_selected_str.split(',') if seats_selected_str else []

    if not seats_selected:
        return "No seats selected", 400

    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if showtime is None:
        return "Showtime not found", 404

    bookings = load_bookings()

    # New booking id
    booking_id = max([b['booking_id'] for b in bookings], default=0) + 1

    booking_date = datetime.today().strftime('%Y-%m-%d')
    total_price = showtime['price'] * len(seats_selected)

    new_booking = {
        'booking_id': booking_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': seats_selected
    }

    # Append new booking
    bookings.append(new_booking)

    saved = save_bookings(bookings)
    if not saved:
        return "Failed to save booking", 500

    # Update seats status? The spec does not require seat update logic, so skip.

    # Redirect to booking confirmation page GET to show summary
    seats_query = ','.join(seats_selected)
    return redirect(url_for('booking_confirmation', showtime_id=showtime_id) + '?seats=' + seats_query)


@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    filter_status_options = ['All', 'Confirmed', 'Cancelled', 'Pending']

    # Get filter from query string
    filter_status = request.args.get('status', 'All')

    if filter_status != 'All':
        bookings = [b for b in bookings if b['status'] == filter_status]

    return render_template('booking_history.html', bookings=bookings, filter_status_options=filter_status_options)


@app.route('/bookings/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if booking is None:
        return "Booking not found", 404

    movies = load_movies()
    showtimes = load_showtimes()

    # Find movie for the booking
    showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
    if showtime is None:
        movie = None
    else:
        movie = next((m for m in movies if m['movie_id'] == showtime['movie_id']), None)

    return render_template('booking_details.html', booking=booking, movie=movie)


@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    # Extract unique locations for filter
    locations = sorted(list(set(t['location'] for t in theaters)))

    return render_template('theater_information.html', theaters=theaters, locations=locations)


if __name__ == '__main__':
    app.run()
