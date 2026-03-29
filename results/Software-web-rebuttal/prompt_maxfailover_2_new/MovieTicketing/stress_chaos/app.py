from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Utility functions for data loading and saving

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
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) !=6:
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
                parts=line.split('|')
                if len(parts)!=7:
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
                parts=line.split('|')
                if len(parts)!=7:
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
                parts=line.split('|')
                if len(parts)!=8:
                    continue
                seats_list = parts[7].split(',') if parts[7] else []
                booking = {
                    'booking_id': int(parts[0]),
                    'showtime_id': int(parts[1]),
                    'customer_name': parts[2],
                    'customer_email': parts[3],
                    'booking_date': parts[4],
                    'total_price': float(parts[5]),
                    'status': parts[6],
                    'seats': seats_list
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
                parts=line.split('|')
                if len(parts)!=3:
                    continue
                genres.append(parts[1])
    except Exception:
        pass
    return genres

def save_bookings(bookings):
    try:
        with open('data/bookings.txt', 'w', encoding='utf-8') as f:
            for b in bookings:
                seats_str = ','.join(b['seats']) if b.get('seats') else ''
                line = f"{b['booking_id']}|{b['showtime_id']}|{b['customer_name']}|{b['customer_email']}|{b['booking_date']}|{b['total_price']}|{b['status']}|{seats_str}\n"
                f.write(line)
    except Exception:
        pass

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    # Example featured movies: top 3 by rating
    featured_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)[:3]
    # Upcoming releases: release_date > today
    today_str = datetime.now().strftime('%Y-%m-%d')
    upcoming_releases = [m for m in movies if m['release_date'] > today_str]
    upcoming_releases = sorted(upcoming_releases, key=lambda m: m['release_date'])[:3]
    # Filter fields per spec
    featured_movies_data = [
        {
            'movie_id': fm['movie_id'],
            'title': fm['title'],
            'genre': fm['genre'],
            'rating': fm['rating']
        } for fm in featured_movies
    ]
    upcoming_releases_data = [
        {
            'movie_id': ur['movie_id'],
            'title': ur['title'],
            'release_date': ur['release_date']
        } for ur in upcoming_releases
    ]
    return render_template('dashboard.html', featured_movies=featured_movies_data, upcoming_releases=upcoming_releases_data)

@app.route('/movies')
def movies_catalog():
    movies = load_movies()
    genres = load_genres()
    # Only include subset of movie fields
    movies_data = [
        {
            'movie_id': m['movie_id'],
            'title': m['title'],
            'rating': m['rating'],
            'duration': m['duration'],
            'genre': m['genre']
        } for m in movies
    ]
    return render_template('movies_catalog.html', movies=movies_data, genres=genres)

@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    movies = load_movies()
    movie = next((m for m in movies if m['movie_id'] == movie_id), None)
    if not movie:
        return "Movie not found", 404
    return render_template('movie_details.html', movie=movie)

@app.route('/movies/<int:movie_id>/showtimes')
def showtime_selection(movie_id):
    showtimes = load_showtimes()
    theaters = load_theaters()
    # Filters from query parameters
    theater_filter = request.args.get('theater_filter', '')
    date_filter = request.args.get('date_filter', '')

    filtered_showtimes = [s for s in showtimes if s['movie_id'] == movie_id]
    if theater_filter:
        try:
            theater_filter_id = int(theater_filter)
            filtered_showtimes = [s for s in filtered_showtimes if s['theater_id'] == theater_filter_id]
        except ValueError:
            pass
    if date_filter:
        filtered_showtimes = [s for s in filtered_showtimes if s['showtime_date'] == date_filter]

    theaters_data = [
        {
            'theater_id': t['theater_id'],
            'theater_name': t['theater_name']
        } for t in theaters
    ]

    # Showtimes with required fields
    showtimes_data = [
        {
            'showtime_id': s['showtime_id'],
            'movie_id': s['movie_id'],
            'theater_id': s['theater_id'],
            'showtime_date': s['showtime_date'],
            'showtime_time': s['showtime_time'],
            'price': s['price']
        } for s in filtered_showtimes
    ]
    filters = {'theater_filter': theater_filter, 'date_filter': date_filter}
    return render_template('showtime_selection.html', showtimes=showtimes_data, theaters=theaters_data, filters=filters)

@app.route('/showtimes/<int:showtime_id>/seats', methods=['GET'])
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    theaters = load_theaters()
    theater = next((t for t in theaters if t['theater_id'] == showtime['theater_id']), None)
    if not theater:
        return "Theater not found", 404

    seats = load_seats()
    # Filter seats for this theater_id and screen_id (screen_id is not stored in showtime, assume screen_id=1 here to simplify)
    # The data schema does not specify screen selection from showtime, assume 1
    filtered_seats = [seat for seat in seats if seat['theater_id'] == theater['theater_id'] and seat['screen_id'] == 1]

    seat_map = []
    for seat in filtered_seats:
        seat_label = f"{seat['row']}{seat['column']}"
        seat_entry = {
            'seat_id': seat['seat_id'],
            'seat_label': seat_label,
            'seat_type': seat['seat_type'],
            'status': seat['status']
        }
        seat_map.append(seat_entry)

    # Initially no selected seats
    selected_seats = []

    return render_template('seat_selection.html', seat_map=seat_map, selected_seats=selected_seats)

@app.route('/showtimes/<int:showtime_id>/seats', methods=['POST'])
def select_seats(showtime_id):
    selected_seats = request.form.getlist('selected_seats')
    # Redirect to booking confirmation with selected seats info
    if not selected_seats:
        # If no seats selected, redirect back to seat selection
        return redirect(url_for('seat_selection', showtime_id=showtime_id))

    # Store selection in session or pass via query string, but spec does not mention session usage.
    # We'll redirect with parameters in query string.
    seats_param = ','.join(selected_seats)
    return redirect(url_for('booking_confirmation', selected_seats=seats_param, showtime_id=showtime_id))

@app.route('/booking/confirm', methods=['GET'])
def booking_confirmation():
    # Retrieve selected seats and showtime_id from query parameters
    seats_param = request.args.get('selected_seats', '')
    showtime_id = request.args.get('showtime_id', '')
    if not seats_param or not showtime_id:
        return redirect(url_for('dashboard'))
    selected_seats = seats_param.split(',')
    try:
        showtime_id_int = int(showtime_id)
    except:
        return redirect(url_for('dashboard'))

    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id_int), None)
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

    booking_summary = {
        'movie_title': movie['title'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'theater_name': theater['theater_name'],
        'seats': selected_seats,
        'total_price': round(len(selected_seats) * showtime['price'], 2)
    }

    return render_template('booking_confirmation.html', booking_summary=booking_summary)

@app.route('/booking/confirm', methods=['POST'])
def confirm_booking():
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()

    # Booking info sent probably with hidden fields or form data. We must parse booking info from the form.
    # The spec states: booking_info:dict[details from booking_summary plus seats] from POST data

    selected_seats_str = request.form.get('seats', '')
    showtime_id_str = request.form.get('showtime_id', '')
    try:
        showtime_id = int(showtime_id_str)
    except:
        return redirect(url_for('dashboard'))

    if not customer_name or not customer_email or not selected_seats_str:
        return redirect(url_for('dashboard'))

    selected_seats = selected_seats_str.split(',')

    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == showtime_id), None)
    if not showtime:
        return "Showtime not found", 404

    bookings = load_bookings()
    new_booking_id = max([b['booking_id'] for b in bookings], default=0) + 1

    # Create new booking entry
    new_booking = {
        'booking_id': new_booking_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': datetime.now().strftime('%Y-%m-%d'),
        'total_price': round(len(selected_seats)*showtime['price'], 2),
        'status': 'Confirmed',
        'seats': selected_seats
    }

    bookings.append(new_booking)
    save_bookings(bookings)

    return redirect(url_for('booking_history'))

@app.route('/bookings')
def booking_history():
    bookings = load_bookings()
    movies = load_movies()
    # Compose booking info with movie title
    enriched_bookings = []
    for b in bookings:
        movie = next((m for m in movies if m['movie_id'] == next((s['movie_id'] for s in load_showtimes() if s['showtime_id'] == b['showtime_id']), None)), None)
        movie_title = movie['title'] if movie else 'Unknown'
        booking_info = {
            'booking_id': b['booking_id'],
            'movie_title': movie_title,
            'booking_date': b['booking_date'],
            'seats': b['seats'],
            'status': b['status']
        }
        enriched_bookings.append(booking_info)
    return render_template('booking_history.html', bookings=enriched_bookings)

@app.route('/bookings/<int:booking_id>')
def booking_details(booking_id):
    bookings = load_bookings()
    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
    if not booking:
        return "Booking not found", 404

    showtimes = load_showtimes()
    showtime = next((s for s in showtimes if s['showtime_id'] == booking['showtime_id']), None)
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

    booking_detail = {
        'booking_id': booking['booking_id'],
        'movie_title': movie['title'],
        'showtime_date': showtime['showtime_date'],
        'showtime_time': showtime['showtime_time'],
        'theater_name': theater['theater_name'],
        'seats': booking['seats'],
        'status': booking['status']
    }

    return render_template('booking_details.html', booking=booking_detail)

@app.route('/theaters')
def theater_information():
    theaters = load_theaters()
    location_filter = request.args.get('location_filter', '')

    filtered_theaters = theaters
    if location_filter:
        filtered_theaters = [t for t in theaters if t['location'] == location_filter]

    theaters_data = [
        {
            'theater_id': t['theater_id'],
            'theater_name': t['theater_name'],
            'location': t['location'],
            'city': t['city'],
            'screens': t['screens'],
            'facilities': t['facilities']
        } for t in filtered_theaters
    ]

    return render_template('theater_information.html', theaters=theaters_data, location_filter=location_filter)


if __name__ == '__main__':
    app.run()
