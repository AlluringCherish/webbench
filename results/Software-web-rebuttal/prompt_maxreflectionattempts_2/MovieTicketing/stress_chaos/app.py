from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Data loading functions

def load_movies():
    movies = []
    try:
        with open('data/movies.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
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
        with open('data/theaters.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
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
        with open('data/showtimes.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    showtime = {
                        'showtime_id': int(parts[0]),
                        'movie_id': int(parts[1]),
                        'theater_id': int(parts[2]),
                        'date': parts[3],
                        'time': parts[4],
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
                line = line.strip()
                if line:
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
        with open('data/bookings.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
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


def save_bookings(bookings):
    try:
        with open('data/bookings.txt', 'w', encoding='utf-8') as f:
            for b in bookings:
                line = '|'.join([
                    str(b['booking_id']),
                    str(b['showtime_id']),
                    b['customer_name'],
                    b['customer_email'],
                    b['booking_date'],
                    f"{b['total_price']:.2f}",
                    b['status'],
                    ','.join(b['seats_booked'])
                ])
                f.write(line + '\n')
        return True
    except Exception:
        return False


def load_genres():
    genres = []
    try:
        with open('data/genres.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
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


### ROUTES ###

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    movies = load_movies()
    # Select featured movies: choose first 3 by default
    featured_movies = [{'movie_id': m['movie_id'], 'title': m['title']} for m in movies[:3]]
    return render_template('dashboard.html', featured_movies=featured_movies)


@app.route('/movies', methods=['GET'])
def movie_catalog():
    movies = load_movies()
    movies_data = []
    for m in movies:
        movies_data.append({
            'movie_id': m['movie_id'],
            'title': m['title'],
            'genre': m['genre'],
            'rating': m['rating'],
            'duration': m['duration']
        })
    return render_template('movie_catalog.html', movies=movies_data)


@app.route('/movies/search', methods=['POST'])
def movie_search():
    search_text = request.form.get('search_input', '').strip().lower()
    movies = load_movies()
    filtered = []
    for m in movies:
        if search_text in m['title'].lower() or search_text in m['genre'].lower():
            filtered.append({
                'movie_id': m['movie_id'],
                'title': m['title'],
                'genre': m['genre'],
                'rating': m['rating'],
                'duration': m['duration']
            })
    return render_template('movie_catalog.html', movies=filtered)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id: int):
    movies = load_movies()
    movie = None
    for m in movies:
        if m['movie_id'] == movie_id:
            movie = {
                'movie_id': m['movie_id'],
                'title': m['title'],
                'director': m['director'],
                'rating': m['rating'],
                'description': m['description']
            }
            break
    if movie is None:
        # Could render 404 or simply redirect to catalog
        return redirect(url_for('movie_catalog'))
    return render_template('movie_details.html', movie=movie)


@app.route('/showtimes/<int:movie_id>', methods=['GET'])
def showtime_selection(movie_id: int):
    showtimes_all = load_showtimes()
    theaters = load_theaters()
    showtimes = []
    for s in showtimes_all:
        if s['movie_id'] == movie_id:
            # Find theater name
            theater_name = None
            for t in theaters:
                if t['theater_id'] == s['theater_id']:
                    theater_name = t['theater_name']
                    break
            showtime_dict = {
                'showtime_id': s['showtime_id'],
                'date': s['date'],
                'time': s['time'],
                'theater': theater_name if theater_name else '',
                'price': s['price']
            }
            showtimes.append(showtime_dict)
    return render_template('showtime_selection.html', showtimes=showtimes)


@app.route('/showtimes/filter', methods=['POST'])
def showtime_filter():
    theater_filter = request.form.get('theater_filter', '').strip().lower()
    date_filter = request.form.get('date_filter', '').strip()
    showtimes_all = load_showtimes()
    theaters = load_theaters()
    filtered = []
    for s in showtimes_all:
        theater_name = ''
        for t in theaters:
            if t['theater_id'] == s['theater_id']:
                theater_name = t['theater_name']
                break
        if theater_filter and theater_filter not in theater_name.lower():
            continue
        if date_filter and s['date'] != date_filter:
            continue
        showtime_dict = {
            'showtime_id': s['showtime_id'],
            'date': s['date'],
            'time': s['time'],
            'theater': theater_name,
            'price': s['price']
        }
        filtered.append(showtime_dict)
    return render_template('showtime_selection.html', showtimes=filtered)


@app.route('/seats/<int:showtime_id>', methods=['GET'])
def seat_selection(showtime_id: int):
    showtimes = load_showtimes()
    theaters = load_theaters()
    seats = load_seats()

    # Find showtime
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            showtime = s
            break
    if showtime is None:
        # Redirect to some page if showtime not found
        return redirect(url_for('dashboard'))

    # Find theater_id
    theater_id = showtime['theater_id']

    # For simplicity, assume screen_id = 1 (since showtimes.txt doesn't specify screen)
    # Get seats for that theater and screen 1
    seat_map = []
    for seat in seats:
        if seat['theater_id'] == theater_id and seat['screen_id'] == 1:
            seat_map.append({
                'seat_id': seat['seat_id'],
                'row': seat['row'],
                'column': seat['column'],
                'seat_type': seat['seat_type'],
                'status': seat['status']
            })

    selected_seats = []  # Initially no selection

    return render_template('seat_selection.html', seat_map=seat_map, selected_seats=selected_seats)


@app.route('/booking/confirm', methods=['GET'])
def booking_confirmation():
    # This route is a placeholder, normally would get details from session or form
    # Without session support and form data, we can't construct booking summary here
    # Render empty or redirect to dashboard
    booking_summary = {
        'movie': '',
        'showtime': '',
        'seats': [],
        'total': 0.0
    }
    return render_template('booking_confirmation.html', booking_summary=booking_summary)


@app.route('/booking/complete', methods=['POST'])
def booking_complete():
    # Get posted data
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    showtime_id_str = request.form.get('showtime_id', '').strip()
    seats_selected_str = request.form.get('seats_selected', '').strip()  # Expected seats like 'A1,A2'

    if not customer_name or not customer_email or not showtime_id_str or not seats_selected_str:
        return render_template('booking_confirmation.html', booking_status='Invalid booking details')

    try:
        showtime_id = int(showtime_id_str)
        seats_selected = seats_selected_str.split(',')
    except Exception:
        return render_template('booking_confirmation.html', booking_status='Invalid booking details')

    # Load showtimes and bookings
    showtimes = load_showtimes()
    bookings = load_bookings()

    # Find showtime
    showtime = None
    for s in showtimes:
        if s['showtime_id'] == showtime_id:
            showtime = s
            break
    if showtime is None:
        return render_template('booking_confirmation.html', booking_status='Showtime not found')

    # Check seat availability
    seats = load_seats()
    theater_id = showtime['theater_id']
    screen_id = 1  # assumed

    # Check seat status
    for seat_code in seats_selected:
        if len(seat_code) < 2:
            return render_template('booking_confirmation.html', booking_status='Invalid seat code')
        row_ = seat_code[0]
        try:
            col_ = int(seat_code[1:])
        except Exception:
            return render_template('booking_confirmation.html', booking_status='Invalid seat code')

        seat_found = False
        for seat in seats:
            if (seat['theater_id'] == theater_id and seat['screen_id'] == screen_id 
                and seat['row'] == row_ and seat['column'] == col_):
                seat_found = True
                if seat['status'].lower() != 'available':
                    return render_template('booking_confirmation.html', booking_status='One or more seats not available')
                break
        if not seat_found:
            return render_template('booking_confirmation.html', booking_status='Seat not found')

    # Calculate total price
    total_price = showtime['price'] * len(seats_selected)

    # Assign new booking_id
    booking_ids = [b['booking_id'] for b in bookings]
    next_booking_id = max(booking_ids) + 1 if booking_ids else 1

    # Compose new booking
    from datetime import datetime
    booking_date = datetime.now().strftime('%Y-%m-%d')
    new_booking = {
        'booking_id': next_booking_id,
        'showtime_id': showtime_id,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'booking_date': booking_date,
        'total_price': total_price,
        'status': 'Confirmed',
        'seats_booked': seats_selected
    }

    # Append and save bookings
    bookings.append(new_booking)
    success = save_bookings(bookings)
    if not success:
        return render_template('booking_confirmation.html', booking_status='Failed to save booking')

    # Update seat status
    for seat_code in seats_selected:
        row_ = seat_code[0]
        col_ = int(seat_code[1:])
        for seat in seats:
            if (seat['theater_id'] == theater_id and seat['screen_id'] == screen_id
                and seat['row'] == row_ and seat['column'] == col_):
                seat['status'] = 'Booked'

    # Save seat updates
    try:
        with open('data/seats.txt', 'w', encoding='utf-8') as f:
            for seat in seats:
                line = '|'.join([
                    str(seat['seat_id']),
                    str(seat['theater_id']),
                    str(seat['screen_id']),
                    seat['row'],
                    str(seat['column']),
                    seat['seat_type'],
                    seat['status']
                ])
                f.write(line + '\n')
    except Exception:
        return render_template('booking_confirmation.html', booking_status='Failed to update seats')

    return render_template('booking_confirmation.html', booking_status='Booking successful')


@app.route('/bookings', methods=['GET'])
def booking_history():
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    # Optional filter by status
    status_filter = request.args.get('status_filter', '').strip().lower()

    bookings_data = []
    for b in bookings:
        if status_filter and b['status'].lower() != status_filter:
            continue

        # find related movie and showtime date
        movie_title = ''
        showtime_date = ''

        for s in showtimes:
            if s['showtime_id'] == b['showtime_id']:
                showtime_date = s['date']
                movie_id = s['movie_id']
                # find movie title
                for m in movies:
                    if m['movie_id'] == movie_id:
                        movie_title = m['title']
                        break
                break

        bookings_data.append({
            'booking_id': b['booking_id'],
            'movie': movie_title,
            'date': showtime_date,
            'seats': b['seats_booked'],
            'status': b['status']
        })
    return render_template('booking_history.html', bookings=bookings_data)


@app.route('/bookings/<int:booking_id>', methods=['GET'])
def booking_details(booking_id: int):
    bookings = load_bookings()
    showtimes = load_showtimes()
    movies = load_movies()

    matched_booking = None
    for b in bookings:
        if b['booking_id'] == booking_id:
            matched_booking = b
            break
    if matched_booking is None:
        return redirect(url_for('booking_history'))

    movie_title = ''
    showtime_date = ''
    for s in showtimes:
        if s['showtime_id'] == matched_booking['showtime_id']:
            showtime_date = s['date']
            movie_id = s['movie_id']
            for m in movies:
                if m['movie_id'] == movie_id:
                    movie_title = m['title']
                    break
            break

    booking_data = {
        'booking_id': matched_booking['booking_id'],
        'movie': movie_title,
        'date': showtime_date,
        'seats': matched_booking['seats_booked'],
        'status': matched_booking['status']
    }
    return render_template('booking_history.html', booking=booking_data)


@app.route('/theaters', methods=['GET'])
def theater_info():
    theaters = load_theaters()
    # Optional location filter
    location_filter = request.args.get('theater_location_filter', '').strip().lower()
    filtered = []
    for t in theaters:
        if location_filter and location_filter not in t['location'].lower():
            continue
        filtered.append(t)
    return render_template('theater_info.html', theaters=filtered)


if __name__ == '__main__':
    app.run()  
