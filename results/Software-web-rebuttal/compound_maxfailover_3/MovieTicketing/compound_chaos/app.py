from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'

# Utility functions to load data from files

def load_movies():
    path = os.path.join(DATA_DIR, 'movies.txt')
    movies = []
    if not os.path.isfile(path):
        return movies
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                movie_id, title, director, genre, rating, duration, description, release_date = parts
                try:
                    movies.append({
                        'movie_id': int(movie_id),
                        'title': title,
                        'director': director,
                        'genre': genre,
                        'rating': float(rating),
                        'duration': int(duration),
                        'description': description,
                        'release_date': release_date
                    })
                except ValueError:
                    continue
        return movies
    except Exception:
        return []


def load_theaters():
    path = os.path.join(DATA_DIR, 'theaters.txt')
    theaters = []
    if not os.path.isfile(path):
        return theaters
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                theater_id, theater_name, location, city, screens, facilities_str = parts
                try:
                    theaters.append({
                        'theater_id': int(theater_id),
                        'theater_name': theater_name,
                        'location': location,
                        'city': city,
                        'screens': int(screens),
                        'facilities': [f.strip() for f in facilities_str.split(',')] if facilities_str else []
                    })
                except ValueError:
                    continue
        return theaters
    except Exception:
        return []


def load_showtimes():
    path = os.path.join(DATA_DIR, 'showtimes.txt')
    showtimes = []
    if not os.path.isfile(path):
        return showtimes
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                showtime_id, movie_id, theater_id, showtime_date, showtime_time, price, available_seats = parts
                try:
                    showtimes.append({
                        'showtime_id': int(showtime_id),
                        'movie_id': int(movie_id),
                        'theater_id': int(theater_id),
                        'showtime_date': showtime_date,
                        'showtime_time': showtime_time,
                        'price': float(price),
                        'available_seats': int(available_seats)
                    })
                except ValueError:
                    continue
        return showtimes
    except Exception:
        return []


def load_seats():
    path = os.path.join(DATA_DIR, 'seats.txt')
    seats = []
    if not os.path.isfile(path):
        return seats
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                seat_id, theater_id, screen_id, row, column, seat_type, status = parts
                try:
                    seats.append({
                        'seat_id': int(seat_id),
                        'theater_id': int(theater_id),
                        'screen_id': int(screen_id),
                        'row': row,
                        'column': int(column),
                        'seat_type': seat_type,
                        'status': status
                    })
                except ValueError:
                    continue
        return seats
    except Exception:
        return []


def load_bookings():
    path = os.path.join(DATA_DIR, 'bookings.txt')
    bookings = []
    if not os.path.isfile(path):
        return bookings
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                booking_id, showtime_id, customer_name, customer_email, booking_date, total_price, status, seats_booked = parts
                try:
                    bookings.append({
                        'booking_id': int(booking_id),
                        'showtime_id': int(showtime_id),
                        'customer_name': customer_name,
                        'customer_email': customer_email,
                        'booking_date': booking_date,
                        'total_price': float(total_price),
                        'status': status,
                        'seats_booked': seats_booked.split(',') if seats_booked else []
                    })
                except ValueError:
                    continue
        return bookings
    except Exception:
        return []


def save_bookings(bookings):
    path = os.path.join(DATA_DIR, 'bookings.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for booking in bookings:
                f.write(f"{booking['booking_id']}|{booking['showtime_id']}|{booking['customer_name']}|{booking['customer_email']}|{booking['booking_date']}|{booking['total_price']}|{booking['status']}|{','.join(booking['seats_booked'])}\n")
    except Exception:
        pass


def save_seats(seats):
    path = os.path.join(DATA_DIR, 'seats.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for seat in seats:
                f.write(f"{seat['seat_id']}|{seat['theater_id']}|{seat['screen_id']}|{seat['row']}|{seat['column']}|{seat['seat_type']}|{seat['status']}\n")
    except Exception:
        pass


def load_genres():
    path = os.path.join(DATA_DIR, 'genres.txt')
    genres = []
    if not os.path.isfile(path):
        return genres
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 3:
                    continue
                genre_id, genre_name, description = parts
                try:
                    genres.append({
                        'genre_id': int(genre_id),
                        'genre_name': genre_name,
                        'description': description
                    })
                except ValueError:
                    continue
        return genres
    except Exception:
        return []

# Helper function: Validate email format

def is_valid_email(email):
    pattern = r'^\S+@\S+\.\S+$'
    return re.match(pattern, email) is not None

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    featured_movies = []
    try:
        sorted_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)
        for m in sorted_movies[:5]:
            featured_movies.append({
                'movie_id': m['movie_id'],
                'title': m['title'],
                'rating': m['rating'],
                'duration': m['duration']
            })
    except Exception:
        pass
    return render_template('dashboard.html', featured_movies=featured_movies)


@app.route('/movies', methods=['GET'])
def movie_catalog():
    movies = load_movies()
    movie_list = []
    try:
        for m in movies:
            movie_list.append({
                'movie_id': m['movie_id'],
                'title': m['title'],
                'genre': m['genre'],
                'rating': m['rating'],
                'duration': m['duration']
            })
    except Exception:
        pass
    return render_template('movie_catalog.html', movies=movie_list)


@app.route('/movies/search', methods=['POST'])
def movie_search():
    movies = load_movies()
    search_term = request.form.get('search_term', '').strip().lower()
    genre_filter = request.form.get('genre_filter', '').strip()
    filtered = []
    try:
        for m in movies:
            title_match = (search_term in m['title'].lower()) if search_term else True
            genre_match = (m['genre'] == genre_filter) if genre_filter else True
            if title_match and genre_match:
                filtered.append({
                    'movie_id': m['movie_id'],
                    'title': m['title'],
                    'genre': m['genre'],
                    'rating': m['rating'],
                    'duration': m['duration']
                })
    except Exception:
        pass
    return render_template('movie_catalog.html', movies=filtered, search_term=search_term, genre_filter=genre_filter)


@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    movies = load_movies()
    movie = None
    try:
        for m in movies:
            if m['movie_id'] == movie_id:
                movie = m
                break
    except Exception:
        pass
    if not movie:
        abort(404)
    return render_template('movie_details.html', movie=movie)


@app.route('/movie/<int:movie_id>/showtimes', methods=['GET'])
def select_showtime(movie_id):
    movies = load_movies()
    theaters = load_theaters()
    showtimes = load_showtimes()
    theater_filter = request.args.get('theater_filter')
    date_filter = request.args.get('date_filter')
    movie = None
    try:
        for m in movies:
            if m['movie_id'] == movie_id:
                movie = m
                break
    except Exception:
        pass
    if not movie:
        abort(404)
    filtered_showtimes = []
    for st in showtimes:
        try:
            if st['movie_id'] == movie_id:
                if theater_filter and theater_filter != '':
                    tname = None
                    for t in theaters:
                        if t['theater_id'] == st['theater_id']:
                            tname = t['theater_name']
                            break
                    if tname != theater_filter:
                        continue
                if date_filter and date_filter != '':
                    if st['showtime_date'] != date_filter:
                        continue
                tname = None
                for t in theaters:
                    if t['theater_id'] == st['theater_id']:
                        tname = t['theater_name']
                        break
                if tname is None:
                    continue
                filtered_showtimes.append({
                    'showtime_id': st['showtime_id'],
                    'theater_name': tname,
                    'theater_id': st['theater_id'],
                    'showtime_date': st['showtime_date'],
                    'showtime_time': st['showtime_time'],
                    'price': st['price'],
                    'available_seats': st['available_seats']
                })
        except Exception:
            continue
    theater_filter_options = [t['theater_name'] for t in theaters]
    selected_theater = theater_filter if theater_filter else None
    return render_template('showtime_selection.html', showtimes=filtered_showtimes, theater_filter_options=theater_filter_options, selected_theater=selected_theater, date_filter=date_filter)


@app.route('/select_showtime/<int:showtime_id>/seats', methods=['GET'])
def seat_selection(showtime_id):
    showtimes = load_showtimes()
    movies = load_movies()
    theaters = load_theaters()
    seats = load_seats()
    selected_showtime = None
    try:
        for st in showtimes:
            if st['showtime_id'] == showtime_id:
                selected_showtime = st
                break
    except Exception:
        pass
    if not selected_showtime:
        abort(404)
    movie_title = None
    for m in movies:
        if m['movie_id'] == selected_showtime['movie_id']:
            movie_title = m['title']
            break
    theater_name = None
    for t in theaters:
        if t['theater_id'] == selected_showtime['theater_id']:
            theater_name = t['theater_name']
            break
    if movie_title is None or theater_name is None:
        abort(404)
    selected_showtime_dict = {
        'showtime_id': selected_showtime['showtime_id'],
        'movie_title': movie_title,
        'theater_name': theater_name,
        'showtime_date': selected_showtime['showtime_date'],
        'showtime_time': selected_showtime['showtime_time'],
        'price': selected_showtime['price']
    }
    theater_id = selected_showtime['theater_id']
    screen_id = 1
    seat_map = []
    for seat in seats:
        if seat['theater_id'] == theater_id and seat['screen_id'] == screen_id:
            seat_map.append({
                'seat_id': seat['seat_id'],
                'row': seat['row'],
                'column': seat['column'],
                'seat_type': seat['seat_type'],
                'status': seat['status']
            })
    try:
        seat_map = sorted(seat_map, key=lambda s: (s['row'], s['column']))
    except Exception:
        pass
    return render_template('seat_selection.html', seat_map=seat_map, selected_showtime=selected_showtime_dict)


@app.route('/booking/confirm', methods=['GET', 'POST'])
def booking_confirmation():
    if request.method == 'GET':
        movie_title = request.args.get('movie_title')
        showtime_date = request.args.get('showtime_date')
        showtime_time = request.args.get('showtime_time')
        theater_name = request.args.get('theater_name')
        seats_str = request.args.get('seats')
        total_price_str = request.args.get('total_price')
        if not all([movie_title, showtime_date, showtime_time, theater_name, seats_str, total_price_str]):
            abort(400)
        seats = seats_str.split(',') if seats_str else []
        try:
            total_price = float(total_price_str)
        except ValueError:
            abort(400)
        booking_summary = {
            'movie_title': movie_title,
            'showtime_date': showtime_date,
            'showtime_time': showtime_time,
            'theater_name': theater_name,
            'seats': seats,
            'total_price': total_price
        }
        return render_template('booking_confirmation.html', booking_summary=booking_summary)
    else:
        customer_name = request.form.get('customer_name', '').strip()
        customer_email = request.form.get('customer_email', '').strip()
        movie_title = request.form.get('movie_title', '').strip()
        showtime_date = request.form.get('showtime_date', '').strip()
        showtime_time = request.form.get('showtime_time', '').strip()
        theater_name = request.form.get('theater_name', '').strip()
        seats_str = request.form.get('seats', '').strip()
        total_price_str = request.form.get('total_price', '').strip()
        error_message = ''
        if not customer_name or not customer_email or not movie_title or not showtime_date or not showtime_time or not theater_name or not seats_str or not total_price_str:
            error_message = 'Missing required booking information.'
            return render_template('booking_confirmation.html', booking_success=False, error_message=error_message)
        if not is_valid_email(customer_email):
            error_message = 'Invalid email format.'
            return render_template('booking_confirmation.html', booking_success=False, error_message=error_message)
        seats = [s.strip() for s in seats_str.split(',') if s.strip()]
        try:
            total_price = float(total_price_str)
        except ValueError:
            error_message = 'Invalid total price format.'
            return render_template('booking_confirmation.html', booking_success=False, error_message=error_message)
        showtimes = load_showtimes()
        theaters = load_theaters()
        matched_showtime = None
        showtime_id = None
        try:
            for st in showtimes:
                if st['showtime_date'] == showtime_date and st['showtime_time'] == showtime_time and abs(st['price'] - total_price) < 0.01:
                    tname = None
                    for t in theaters:
                        if t['theater_id'] == st['theater_id']:
                            tname = t['theater_name']
                            break
                    if tname == theater_name:
                        showtime_id = st['showtime_id']
                        matched_showtime = st
                        break
        except Exception:
            pass
        if showtime_id is None or matched_showtime is None:
            error_message = 'Invalid showtime information.'
            return render_template('booking_confirmation.html', booking_success=False, error_message=error_message)
        all_seats = load_seats()
        available_seats_map = {}
        for seat in all_seats:
            if seat['theater_id'] == matched_showtime['theater_id'] and seat['screen_id'] == 1:
                seat_identifier = seat['row'] + str(seat['column'])
                available_seats_map[seat_identifier] = seat
        seats_available = True
        for seat_id in seats:
            seat_obj = available_seats_map.get(seat_id)
            if not seat_obj or seat_obj['status'] != 'Available':
                seats_available = False
                break
        if not seats_available:
            error_message = 'One or more selected seats are not available.'
            return render_template('booking_confirmation.html', booking_success=False, error_message=error_message)
        for seat in all_seats:
            seat_ident = seat['row'] + str(seat['column'])
            if seat_ident in seats:
                if seat['status'] == 'Available':
                    seat['status'] = 'Booked'
        try:
            save_seats(all_seats)
        except Exception:
            error_message = 'Failed to update seat booking status.'
            return render_template('booking_confirmation.html', booking_success=False, error_message=error_message)
        bookings = load_bookings()
        new_booking_id = 1
        if bookings:
            new_booking_id = max(b['booking_id'] for b in bookings) + 1
        booking_date = datetime.now().strftime('%Y-%m-%d')
        new_booking = {
            'booking_id': new_booking_id,
            'showtime_id': showtime_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'booking_date': booking_date,
            'total_price': total_price,
            'status': 'Confirmed',
            'seats_booked': seats
        }
        bookings.append(new_booking)
        save_bookings(bookings)
        return render_template('booking_confirmation.html', booking_success=True)


@app.route('/bookings', methods=['GET'])
def booking_history():
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()
    status_filter = request.args.get('status_filter', 'All')
    filtered_bookings = []
    try:
        for b in bookings:
            movie_title = None
            # Find movie title by matching showtime_id from booking to showtime and then movie_id from showtime
            st = next((st for st in showtimes if st['showtime_id'] == b['showtime_id']), None)
            if st:
                mv = next((mv for mv in movies if mv['movie_id'] == st['movie_id']), None)
                movie_title = mv['title'] if mv else 'Unknown'
            else:
                movie_title = 'Unknown'
            if status_filter != 'All' and b['status'] != status_filter:
                continue
            filtered_bookings.append({
                'booking_id': b['booking_id'],
                'movie_title': movie_title,
                'booking_date': b['booking_date'],
                'seats': b['seats_booked'],
                'status': b['status']
            })
    except Exception:
        pass
    status_filter_options = ['All', 'Confirmed', 'Cancelled', 'Completed']
    selected_status = status_filter
    return render_template('booking_history.html', bookings=filtered_bookings, status_filter_options=status_filter_options, selected_status=selected_status)


@app.route('/booking/<int:booking_id>', methods=['GET'])
def view_booking_details(booking_id):
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()
    booking = None
    try:
        for b in bookings:
            if b['booking_id'] == booking_id:
                booking = b
                break
    except Exception:
        pass
    if not booking:
        abort(404)
    showtime_info = next((st for st in showtimes if st['showtime_id'] == booking['showtime_id']), None)
    if not showtime_info:
        abort(404)
    movie_title = None
    if showtime_info:
        for m in movies:
            if m['movie_id'] == showtime_info['movie_id']:
                movie_title = m['title']
                break
    if not movie_title:
        abort(404)
    result = {
        'booking_id': booking['booking_id'],
        'movie_title': movie_title,
        'showtime_date': showtime_info['showtime_date'] + ' ' + showtime_info['showtime_time'],
        'seats': booking['seats_booked'],
        'status': booking['status'],
        'customer_name': booking['customer_name'],
        'customer_email': booking['customer_email'],
        'total_price': booking['total_price']
    }
    return render_template('booking_details.html', booking=result)


@app.route('/theaters', methods=['GET'])
def theater_information():
    theaters = load_theaters()
    location_filter = request.args.get('location_filter')
    filtered_theaters = []
    try:
        for t in theaters:
            if location_filter and location_filter != '':
                if t['city'] != location_filter:
                    continue
            filtered_theaters.append(t)
    except Exception:
        pass
    location_filter_options = list(sorted(set(t['city'] for t in theaters)))
    selected_location = location_filter if location_filter else None
    return render_template('theater_information.html', theaters=filtered_theaters, location_filter_options=location_filter_options, selected_location=selected_location)


if __name__ == '__main__':
    app.run(debug=True)
