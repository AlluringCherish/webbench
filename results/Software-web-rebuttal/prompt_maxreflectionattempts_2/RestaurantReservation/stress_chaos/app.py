from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data

def load_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 4:
                    continue
                username, email, phone, full_name = parts
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'full_name': full_name
                }
    return users


def load_menu():
    menu = []
    path = os.path.join(DATA_DIR, 'menu.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                try:
                    dish_id = int(parts[0])
                    name = parts[1]
                    category = parts[2]
                    price = float(parts[3])
                    description = parts[4]
                    ingredients = parts[5]  # Not used in templates, but read for completeness
                    dietary = parts[6]
                    avg_rating = float(parts[7])
                    menu.append({
                        'dish_id': dish_id,
                        'name': name,
                        'category': category,
                        'price': price,
                        'description': description,
                        'ingredients': ingredients,
                        'dietary': dietary,
                        'avg_rating': avg_rating
                    })
                except ValueError:
                    continue
    return menu


def load_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 10:
                    continue
                try:
                    reservation_id = int(parts[0])
                    username = parts[1]
                    guest_name = parts[2]
                    phone = parts[3]
                    email = parts[4]
                    party_size = int(parts[5])
                    date = parts[6]  # YYYY-MM-DD
                    time = parts[7]  # HH:MM
                    special_requests = parts[8]
                    status = parts[9]
                    reservations.append({
                        'reservation_id': reservation_id,
                        'username': username,
                        'guest_name': guest_name,
                        'phone': phone,
                        'email': email,
                        'party_size': party_size,
                        'date': date,
                        'time': time,
                        'special_requests': special_requests,
                        'status': status
                    })
                except ValueError:
                    continue
    return reservations


def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure data dir exists
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
                r.get('special_requests', ''),
                r['status']
            ])
            f.write(line + '\n')


def load_waitlist():
    entries = []
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                try:
                    waitlist_id = int(parts[0])
                    username = parts[1]
                    party_size = int(parts[2])
                    join_time = parts[3]
                    status = parts[4]
                    entries.append({
                        'waitlist_id': waitlist_id,
                        'username': username,
                        'party_size': party_size,
                        'join_time': join_time,
                        'status': status
                    })
                except ValueError:
                    continue
    return entries


def save_waitlist(entries):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure data dir exists
    with open(path, 'w', encoding='utf-8') as f:
        for e in entries:
            line = '|'.join([
                str(e['waitlist_id']),
                e['username'],
                str(e['party_size']),
                e['join_time'],
                e['status']
            ])
            f.write(line + '\n')


def load_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                try:
                    review_id = int(parts[0])
                    username = parts[1]
                    dish_id = int(parts[2])
                    rating = int(parts[3])
                    review_text = parts[4]
                    review_date = parts[5]
                    reviews.append({
                        'review_id': review_id,
                        'username': username,
                        'dish_id': dish_id,
                        'rating': rating,
                        'review_text': review_text,
                        'review_date': review_date
                    })
                except ValueError:
                    continue
    return reviews


def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure data dir exists
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


# Mock current user (no authentication specified) use a default user
CURRENT_USERNAME = 'john_diner'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = CURRENT_USERNAME
    users = load_users()
    user_profile = users.get(username, {})

    # Load menu and pick featured dishes (we choose top 3 highest avg_rating for featured)
    menu = load_menu()
    featured_dishes = sorted(menu, key=lambda d: d['avg_rating'], reverse=True)[:3]
    # Prepare featured_dishes as dict of keys needed for template
    featured_list = []
    for dish in featured_dishes:
        featured_list.append({
            'dish_id': dish['dish_id'],
            'name': dish['name'],
            'category': dish['category'],
            'price': dish['price'],
            'description': dish['description']
        })

    # Load upcoming reservations for user (status == Upcoming, sort by date and time ascending)
    reservations = load_reservations()
    upcoming_res = [r for r in reservations if r['username'] == username and r['status'] == 'Upcoming']
    upcoming_res_sorted = sorted(upcoming_res, key=lambda r: (r['date'], r['time']))

    return render_template('dashboard.html', username=username, featured_dishes=featured_list, upcoming_reservations=upcoming_res_sorted)


@app.route('/menu')
def menu_page():
    menu = load_menu()
    # We provide all data for template in exact keys
    menus = []
    for dish in menu:
        menus.append({
            'dish_id': dish['dish_id'],
            'name': dish['name'],
            'category': dish['category'],
            'price': dish['price'],
            'description': dish['description'],
        })
    return render_template('menu.html', menus=menus)


@app.route('/menu/<int:dish_id>')
def dish_details(dish_id):
    menu = load_menu()
    dish = None
    for d in menu:
        if d['dish_id'] == dish_id:
            dish = {
                'name': d['name'],
                'price': d['price'],
                'description': d['description']
            }
            break
    if dish is None:
        # If dish not found, redirect to menu page (graceful handling)
        return redirect(url_for('menu_page'))
    return render_template('dish_details.html', dish=dish)


@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    errors = {}
    if request.method == 'POST':
        guest_name = request.form.get('guest_name', '').strip()
        party_size_raw = request.form.get('party_size', '').strip()
        reservation_date = request.form.get('reservation_date', '').strip()
        special_requests = request.form.get('special_requests', '').strip()

        # Validate guest_name
        if not guest_name:
            errors['guest_name'] = 'Guest name is required.'

        # Validate party_size
        try:
            party_size = int(party_size_raw)
            if party_size < 1 or party_size > 10:
                errors['party_size'] = 'Party size must be between 1 and 10.'
        except ValueError:
            errors['party_size'] = 'Party size must be an integer.'

        # Validate reservation_date format (YYYY-MM-DD) and future date
        try:
            res_date_obj = datetime.strptime(reservation_date, '%Y-%m-%d').date()
            if res_date_obj < datetime.now().date():
                errors['reservation_date'] = 'Reservation date must be today or in the future.'
        except ValueError:
            errors['reservation_date'] = 'Invalid date format.'

        if not errors:
            # Save new reservation
            reservations = load_reservations()
            users = load_users()
            username = CURRENT_USERNAME
            user_profile = users.get(username, {})

            # Generate new reservation_id
            max_id = 0
            for r in reservations:
                if r['reservation_id'] > max_id:
                    max_id = r['reservation_id']
            new_id = max_id + 1

            # Use default time 19:00 for all new reservations
            new_reservation = {
                'reservation_id': new_id,
                'username': username,
                'guest_name': guest_name,
                'phone': user_profile.get('phone', ''),
                'email': user_profile.get('email', ''),
                'party_size': party_size,
                'date': reservation_date,
                'time': '19:00',
                'special_requests': special_requests,
                'status': 'Upcoming'
            }
            reservations.append(new_reservation)
            save_reservations(reservations)

            return redirect(url_for('my_reservations'))

        return render_template('make_reservation.html', errors=errors)

    return render_template('make_reservation.html')


@app.route('/my_reservations')
def my_reservations():
    username = CURRENT_USERNAME
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == username]
    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    reservation_id_raw = request.form.get('reservation_id', '').strip()
    try:
        reservation_id = int(reservation_id_raw)
    except ValueError:
        return redirect(url_for('my_reservations'))

    reservations = load_reservations()
    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == CURRENT_USERNAME and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            updated = True
            break

    if updated:
        save_reservations(reservations)

    return redirect(url_for('my_reservations'))


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist_page():
    username = CURRENT_USERNAME
    waitlist = load_waitlist()
    # Find active waitlist entry for user
    active_entry = None
    for e in waitlist:
        if e['username'] == username and e['status'] == 'Active':
            active_entry = e
            break

    if request.method == 'POST':
        party_size_raw = request.form.get('party_size', '').strip()
        try:
            party_size = int(party_size_raw)
            if party_size < 1:
                party_size = 1
        except ValueError:
            party_size = 1

        if active_entry is not None:
            # Already in waitlist, do not add again
            pass
        else:
            # Add new waitlist entry
            max_id = 0
            for w in waitlist:
                if w['waitlist_id'] > max_id:
                    max_id = w['waitlist_id']
            new_id = max_id + 1
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_entry = {
                'waitlist_id': new_id,
                'username': username,
                'party_size': party_size,
                'join_time': now_str,
                'status': 'Active'
            }
            waitlist.append(new_entry)
            save_waitlist(waitlist)
            active_entry = new_entry

    waitlist_position = None
    if active_entry is not None:
        # Calculate position in active waitlist, ordered by join_time
        active_waitlist = [e for e in waitlist if e['status'] == 'Active']
        active_waitlist_sorted = sorted(active_waitlist, key=lambda a: a['join_time'])
        for idx, e in enumerate(active_waitlist_sorted, start=1):
            if e['waitlist_id'] == active_entry['waitlist_id']:
                waitlist_position = idx
                break

    return render_template('waitlist.html', waitlist_position=waitlist_position)


@app.route('/my_reviews')
def my_reviews():
    username = CURRENT_USERNAME
    reviews = load_reviews()
    menu = load_menu()
    dish_map = {d['dish_id']: d['name'] for d in menu}

    user_reviews = []
    for r in reviews:
        if r['username'] == username:
            user_reviews.append({
                'review_id': r['review_id'],
                'dish_name': dish_map.get(r['dish_id'], 'Unknown Dish'),
                'rating': r['rating'],
                'review_text': r['review_text']
            })

    return render_template('my_reviews.html', reviews=user_reviews)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    username = CURRENT_USERNAME
    menu = load_menu()

    if request.method == 'POST':
        dish_id_raw = request.form.get('dish_id', '').strip()
        rating_raw = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()

        errors = {}

        try:
            dish_id = int(dish_id_raw)
        except ValueError:
            errors['dish_id'] = 'Invalid dish selection.'
            dish_id = None

        try:
            rating = int(rating_raw)
            if rating < 1 or rating > 5:
                errors['rating'] = 'Rating must be between 1 and 5.'
        except ValueError:
            errors['rating'] = 'Invalid rating value.'
            rating = None

        if not review_text:
            errors['review_text'] = 'Review text cannot be empty.'

        # Check dish_id exists
        dish_ids = {d['dish_id'] for d in menu}
        if dish_id is not None and dish_id not in dish_ids:
            errors['dish_id'] = 'Selected dish does not exist.'

        if not errors:
            reviews = load_reviews()
            max_id = 0
            for r in reviews:
                if r['review_id'] > max_id:
                    max_id = r['review_id']
            new_id = max_id + 1

            new_review = {
                'review_id': new_id,
                'username': username,
                'dish_id': dish_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': datetime.now().strftime('%Y-%m-%d')
            }
            reviews.append(new_review)
            save_reviews(reviews)

            return redirect(url_for('my_reviews'))

        # On errors, re-render form with menu and errors
        return render_template('write_review.html', menus=menu, errors=errors)

    # GET method
    return render_template('write_review.html', menus=menu)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = CURRENT_USERNAME
    users = load_users()
    user = users.get(username)

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()

        # Update user data and save
        if user is None:
            # Create new user if missing (unlikely in spec but safe guard)
            user = {
                'username': username,
                'email': email,
                'phone': phone,
                'full_name': ''
            }
            users[username] = user
        else:
            user['email'] = email
            user['phone'] = phone

        # Write back to users.txt
        path = os.path.join(DATA_DIR, 'users.txt')
        os.makedirs(DATA_DIR, exist_ok=True)  # Ensure data dir exists
        with open(path, 'w', encoding='utf-8') as f:
            for u in users.values():
                line = '|'.join([u['username'], u['email'], u['phone'], u.get('full_name', '')])
                f.write(line + '\n')

        return redirect(url_for('profile'))

    # Prepare context
    user_profile = {
        'username': username,
        'email': user['email'] if user else '',
        'phone': user['phone'] if user else ''
    }
    return render_template('profile.html', user_profile=user_profile)


if __name__ == '__main__':
    app.run(debug=True)
