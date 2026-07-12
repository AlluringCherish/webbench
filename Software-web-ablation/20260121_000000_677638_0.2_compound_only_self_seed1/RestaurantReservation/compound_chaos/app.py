from flask import Flask, render_template, redirect, url_for, request
import os
from threading import Lock
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

_file_lock = Lock()

CURRENT_USERNAME = 'guest'  # Placeholder for authentication system

# Utility functions

def read_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                username, email, phone, full_name = parts
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'full_name': full_name
                }
    except FileNotFoundError:
        pass
    return users


def read_menu():
    dishes = []
    path = os.path.join(DATA_DIR, 'menu.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                try:
                    dish_id = int(parts[0])
                    price = float(parts[3])
                    avg_rating = float(parts[7])
                    dish = {
                        'dish_id': dish_id,
                        'name': parts[1],
                        'category': parts[2],
                        'price': price,
                        'description': parts[4],
                        'ingredients': parts[5],
                        'dietary': parts[6],
                        'avg_rating': avg_rating
                    }
                    dishes.append(dish)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return dishes


def read_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 10:
                    continue
                try:
                    reservation_id = int(parts[0])
                    party_size = int(parts[5])
                    reservation = {
                        'reservation_id': reservation_id,
                        'username': parts[1],
                        'guest_name': parts[2],
                        'phone': parts[3],
                        'email': parts[4],
                        'party_size': party_size,
                        'date': parts[6],
                        'time': parts[7],
                        'special_requests': parts[8],
                        'status': parts[9]
                    }
                    reservations.append(reservation)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return reservations


def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with _file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            for r in reservations:
                line = '|'.join([
                    str(r['reservation_id']),
                    r['username'],
                    r['guest_name'],
                    r['phone'],
                    r['email'],
                    str(r['party_size']),
                    r['date'],
                    r['time'],
                    r['special_requests'],
                    r['status']
                ])
                f.write(line + '\n')


def read_waitlist():
    waitlist = []
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                try:
                    waitlist_id = int(parts[0])
                    party_size = int(parts[2])
                    join_time = parts[3]
                    status = parts[4]
                    entry = {
                        'waitlist_id': waitlist_id,
                        'username': parts[1],
                        'party_size': party_size,
                        'join_time': join_time,
                        'status': status
                    }
                    waitlist.append(entry)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return waitlist


def write_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    with _file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            for w in waitlist:
                line = '|'.join([
                    str(w['waitlist_id']),
                    w['username'],
                    str(w['party_size']),
                    w['join_time'],
                    w['status']
                ])
                f.write(line + '\n')


def read_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
                    review_id = int(parts[0])
                    dish_id = int(parts[2])
                    rating = int(parts[3])
                    review = {
                        'review_id': review_id,
                        'username': parts[1],
                        'dish_id': dish_id,
                        'rating': rating,
                        'review_text': parts[4],
                        'review_date': parts[5]
                    }
                    reviews.append(review)
                except ValueError:
                    continue
    except FileNotFoundError:
        pass
    return reviews


def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with _file_lock:
        with open(path, 'w', encoding='utf-8') as f:
            for r in reviews:
                line = '|'.join([
                    str(r['review_id']),
                    r['username'],
                    str(r['dish_id']),
                    str(r['rating']),
                    r['review_text'],
                    r['review_date']
                ])
                f.write(line + '\n')


@app.route('/')
def home():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    menu_data = read_menu()
    featured_dishes = [
        {'dish_id': d['dish_id'], 'name': d['name'], 'price': d['price'], 'description': d['description']}
        for d in menu_data[:3]
    ]
    reservations = read_reservations()
    upcoming_reservations = [
        {
            "reservation_id": r["reservation_id"],
            "date": r["date"],
            "time": r["time"],
            "party_size": r["party_size"],
            "status": r["status"]
        }
        for r in reservations
        if r["username"] == CURRENT_USERNAME and r["status"] == "Upcoming"
    ]
    return render_template('dashboard.html', username=CURRENT_USERNAME, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)


@app.route('/menu')
def menu():
    menus = read_menu()
    return render_template('menu.html', menus=menus)


@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu_list = read_menu()
    dish = next((d for d in menu_list if d['dish_id'] == dish_id), None)
    if dish is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish)


@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'POST':
        guest_name = request.form.get('guest_name', '').strip()
        party_size_str = request.form.get('party_size', '').strip()
        reservation_date_str = request.form.get('reservation_date', '').strip()

        errors = {}

        if not guest_name:
            errors['guest_name'] = 'Guest name is required.'

        try:
            party_size = int(party_size_str)
            if party_size < 1 or party_size > 10:
                errors['party_size'] = 'Party size must be between 1 and 10.'
        except ValueError:
            errors['party_size'] = 'Invalid party size.'

        try:
            reservation_date = datetime.strptime(reservation_date_str, '%Y-%m-%d').date()
            if reservation_date < datetime.now().date():
                errors['reservation_date'] = 'Reservation date cannot be in the past.'
        except ValueError:
            errors['reservation_date'] = 'Invalid date format.'

        if errors:
            return render_template('make_reservation.html', errors=errors, guest_name=guest_name, party_size=party_size_str, reservation_date=reservation_date_str)

        users = read_users()
        user = users.get(CURRENT_USERNAME, {'username': CURRENT_USERNAME, 'email': '', 'phone': '', 'full_name': ''})
        reservations = read_reservations()
        new_id = max([r['reservation_id'] for r in reservations], default=0) + 1

        new_reservation = {
            'reservation_id': new_id,
            'username': CURRENT_USERNAME,
            'guest_name': guest_name,
            'phone': user.get('phone', ''),
            'email': user.get('email', ''),
            'party_size': party_size,
            'date': reservation_date.strftime('%Y-%m-%d'),
            'time': '19:00',  # fixed reservation time
            'special_requests': '',
            'status': 'Upcoming'
        }

        reservations.append(new_reservation)
        write_reservations(reservations)

        return redirect(url_for('my_reservations'))

    return render_template('make_reservation.html')


@app.route('/my_reservations')
def my_reservations():
    reservations = read_reservations()
    user_reservations = [r for r in reservations if r['username'] == CURRENT_USERNAME]
    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    changed = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == CURRENT_USERNAME:
            if r['status'] != 'Canceled':
                r['status'] = 'Canceled'
                changed = True
            break
    if changed:
        write_reservations(reservations)
    return redirect(url_for('my_reservations'))


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    waitlist = read_waitlist()
    user_active = any(w for w in waitlist if w['username'] == CURRENT_USERNAME and w['status'] == 'Active')

    if request.method == 'POST':
        errors = {}
        party_size_str = request.form.get('party_size', '').strip()
        try:
            party_size = int(party_size_str)
            if party_size < 1 or party_size > 10:
                errors['party_size'] = 'Party size must be between 1 and 10.'
        except ValueError:
            errors['party_size'] = 'Invalid party size.'

        if errors:
            return render_template('waitlist.html', errors=errors, user_active=user_active)

        if not user_active:
            max_id = max([w['waitlist_id'] for w in waitlist], default=0)
            new_id = max_id + 1
            join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_entry = {
                'waitlist_id': new_id,
                'username': CURRENT_USERNAME,
                'party_size': party_size,
                'join_time': join_time,
                'status': 'Active'
            }
            waitlist.append(new_entry)
            write_waitlist(waitlist)
            user_active = True

        waitlist_active_sorted = sorted([w for w in waitlist if w['status'] == 'Active'], key=lambda w: w['join_time'])
        user_position = None
        for idx, w in enumerate(waitlist_active_sorted, start=1):
            if w['username'] == CURRENT_USERNAME:
                user_position = idx
                break

        return render_template('waitlist.html', user_active=user_active, user_position=user_position)

    # GET request
    waitlist_active_sorted = sorted([w for w in waitlist if w['status'] == 'Active'], key=lambda w: w['join_time'])
    user_position = None
    for idx, w in enumerate(waitlist_active_sorted, start=1):
        if w['username'] == CURRENT_USERNAME:
            user_position = idx
            break

    return render_template('waitlist.html', user_active=user_active, user_position=user_position)


@app.route('/my_reviews')
def my_reviews():
    reviews = read_reviews()
    menu = read_menu()
    dish_names = {d['dish_id']: d['name'] for d in menu}
    user_reviews = [r for r in reviews if r['username'] == CURRENT_USERNAME]
    return render_template('my_reviews.html', reviews=user_reviews, dish_names=dish_names)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    menu = read_menu()

    if request.method == 'POST':
        dish_id_str = request.form.get('dish_id', '').strip()
        rating_str = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()

        errors = {}

        try:
            dish_id = int(dish_id_str)
            if dish_id not in [d['dish_id'] for d in menu]:
                errors['dish_id'] = 'Please select a valid dish.'
        except ValueError:
            errors['dish_id'] = 'Please select a valid dish.'

        try:
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                errors['rating'] = 'Rating must be between 1 and 5.'
        except ValueError:
            errors['rating'] = 'Rating must be an integer between 1 and 5.'

        if not review_text:
            errors['review_text'] = 'Review text is required.'

        if errors:
            return render_template('write_review.html', errors=errors, dish_id=dish_id_str, rating=rating_str, review_text=review_text, dishes=menu)

        reviews = read_reviews()
        new_id = max([r['review_id'] for r in reviews], default=0) + 1
        today = datetime.now().strftime('%Y-%m-%d')

        new_review = {
            'review_id': new_id,
            'username': CURRENT_USERNAME,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': today
        }

        reviews.append(new_review)
        write_reviews(reviews)

        return redirect(url_for('my_reviews'))

    return render_template('write_review.html', dishes=menu)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = read_users()
    user_profile = users.get(CURRENT_USERNAME, {'username': CURRENT_USERNAME, 'email': '', 'phone': '', 'full_name': ''})

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        errors = {}
        if not email or '@' not in email or '.' not in email or len(email) < 5:
            errors['email'] = 'Please enter a valid email address.'

        if errors:
            return render_template('profile.html', errors=errors, user_profile={'username': user_profile['username'], 'email': email})

        users = read_users()
        users[CURRENT_USERNAME]['email'] = email

        path = os.path.join(DATA_DIR, 'users.txt')
        with _file_lock:
            with open(path, 'w', encoding='utf-8') as f:
                for u in users.values():
                    line = '|'.join([u['username'], u.get('email', ''), u.get('phone', ''), u.get('full_name', '')])
                    f.write(line + '\n')

        return redirect(url_for('profile'))

    return render_template('profile.html', user_profile=user_profile)


if __name__ == '__main__':
    app.run(debug=True)
