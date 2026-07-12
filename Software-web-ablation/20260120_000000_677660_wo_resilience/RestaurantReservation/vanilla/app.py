from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from files

def load_users():
    users_path = os.path.join(DATA_DIR, 'users.txt')
    users = {}
    if os.path.exists(users_path):
        with open(users_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) < 4:
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
    menu_path = os.path.join(DATA_DIR, 'menu.txt')
    menus = []
    if os.path.exists(menu_path):
        with open(menu_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) < 8:
                        continue
                    dish_id_str, name, category, price_str, description, ingredients, dietary, avg_rating_str = parts
                    try:
                        dish_id = int(dish_id_str)
                        price = float(price_str)
                        avg_rating = float(avg_rating_str)
                    except ValueError:
                        continue
                    menus.append({
                        'dish_id': dish_id,
                        'name': name,
                        'category': category,
                        'price': price,
                        'description': description,
                        'ingredients': ingredients,
                        'dietary': dietary,
                        'avg_rating': avg_rating
                    })
    return menus


def load_reservations():
    reservations_path = os.path.join(DATA_DIR, 'reservations.txt')
    reservations = []
    if os.path.exists(reservations_path):
        with open(reservations_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) < 10:
                        continue
                    (reservation_id_str, username, guest_name, phone, email, party_size_str, 
                     date, time, special_requests, status) = parts
                    try:
                        reservation_id = int(reservation_id_str)
                        party_size = int(party_size_str)
                    except ValueError:
                        continue
                    reservations.append({
                        'reservation_id': reservation_id,
                        'username': username,
                        'guest_name': guest_name,
                        'phone': phone,
                        'email': email,
                        'party_size': party_size,
                        'date': date,
                        'time': time,
                        'special_requests': special_requests if special_requests else None,
                        'status': status
                    })
    return reservations


def load_waitlist():
    waitlist_path = os.path.join(DATA_DIR, 'waitlist.txt')
    waitlist = []
    if os.path.exists(waitlist_path):
        with open(waitlist_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) < 5:
                        continue
                    waitlist_id_str, username, party_size_str, join_time, status = parts
                    try:
                        waitlist_id = int(waitlist_id_str)
                        party_size = int(party_size_str)
                    except ValueError:
                        continue
                    waitlist.append({
                        'waitlist_id': waitlist_id,
                        'username': username,
                        'party_size': party_size,
                        'join_time': join_time,
                        'status': status
                    })
    return waitlist


def load_reviews():
    reviews_path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if os.path.exists(reviews_path):
        with open(reviews_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    if len(parts) < 6:
                        continue
                    review_id_str, username, dish_id_str, rating_str, review_text, review_date = parts
                    try:
                        review_id = int(review_id_str)
                        dish_id = int(dish_id_str)
                        rating = int(rating_str)
                    except ValueError:
                        continue
                    reviews.append({
                        'review_id': review_id,
                        'username': username,
                        'dish_id': dish_id,
                        'rating': rating,
                        'review_text': review_text,
                        'review_date': review_date
                    })
    return reviews


def save_reservations(reservations):
    reservations_path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(reservations_path, 'w', encoding='utf-8') as f:
        for res in reservations:
            special_requests = res['special_requests'] if res['special_requests'] else ''
            line = f"{res['reservation_id']}|{res['username']}|{res['guest_name']}|{res['phone']}|{res['email']}|{res['party_size']}|{res['date']}|{res['time']}|{special_requests}|{res['status']}\n"
            f.write(line)


def save_waitlist(waitlist):
    waitlist_path = os.path.join(DATA_DIR, 'waitlist.txt')
    with open(waitlist_path, 'w', encoding='utf-8') as f:
        for entry in waitlist:
            line = f"{entry['waitlist_id']}|{entry['username']}|{entry['party_size']}|{entry['join_time']}|{entry['status']}\n"
            f.write(line)


def save_reviews(reviews):
    reviews_path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(reviews_path, 'w', encoding='utf-8') as f:
        for rev in reviews:
            line = f"{rev['review_id']}|{rev['username']}|{rev['dish_id']}|{rev['rating']}|{rev['review_text']}|{rev['review_date']}\n"
            f.write(line)


def save_users(users):
    users_path = os.path.join(DATA_DIR, 'users.txt')
    with open(users_path, 'w', encoding='utf-8') as f:
        for user in users.values():
            line = f"{user['username']}|{user['email']}|{user['phone']}|{user['full_name']}\n"
            f.write(line)

# Dummy helper to get logged-in username
# Since no auth specified, hardcode or get from query param headers in production
# Here, we will hardcode a user for demo.
def get_logged_in_username():
    # For testing, we pick a single user from users.txt if exists
    users = load_users()
    if users:
        return next(iter(users.keys()))
    return 'john_diner'  # default fallback


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = get_logged_in_username()
    users = load_users()
    user = users.get(username)
    if not user:
        username = 'Guest'

    menus = load_menu()
    # Selected featured dishes: pick first 3 dishes sorted by avg_rating descending
    featured = sorted(menus, key=lambda x: x['avg_rating'], reverse=True)[:3]
    featured_dishes = [
        {'dish_id': d['dish_id'], 'name': d['name'], 'price': d['price']} for d in featured
    ]

    reservations = load_reservations()
    upcoming_reservations = []
    for res in reservations:
        if res['username'] == username and res['status'].lower() == 'upcoming':
            # For dashboard, provide reservation_id, date, time, party_size, status
            upcoming_reservations.append({
                'reservation_id': res['reservation_id'],
                'date': res['date'],
                'time': res['time'],
                'party_size': res['party_size'],
                'status': res['status']
            })

    return render_template('dashboard.html', username=username, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)


@app.route('/menu')
def menu():
    menus = load_menu()
    # Provide fields: dish_id, name, category, price, description
    context_menus = []
    for d in menus:
        context_menus.append({
            'dish_id': d['dish_id'],
            'name': d['name'],
            'category': d['category'],
            'price': d['price'],
            'description': d['description']
        })
    return render_template('menu.html', menus=context_menus)


@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menus = load_menu()
    dish = None
    for d in menus:
        if d['dish_id'] == dish_id:
            dish = {
                'dish_id': d['dish_id'],
                'name': d['name'],
                'price': d['price'],
                'description': d['description']
            }
            break
    if dish is None:
        return "Dish Not Found", 404
    return render_template('dish_details.html', dish=dish)


@app.route('/make-reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'GET':
        return render_template('make_reservation.html')
    # POST method processing
    form_state = {}
    username = get_logged_in_username()
    users = load_users()
    user = users.get(username)
    if not user:
        return render_template('make_reservation.html', form_state={'error': 'User not found'})

    guest_name = request.form.get('guest_name', '').strip()
    party_size_str = request.form.get('party_size', '').strip()
    reservation_date = request.form.get('reservation_date', '').strip()

    # Validate inputs
    error = None
    if not guest_name:
        error = 'Guest name is required.'
    try:
        party_size = int(party_size_str)
        if party_size < 1 or party_size > 10:
            error = 'Party size must be between 1 and 10.'
    except ValueError:
        error = 'Invalid party size.'

    # Validate date format and allow only dates today or future
    try:
        res_date_obj = datetime.strptime(reservation_date, '%Y-%m-%d').date()
        today = datetime.today().date()
        if res_date_obj < today:
            error = 'Reservation date must be today or in the future.'
    except ValueError:
        error = 'Invalid reservation date format.'

    if error:
        form_state = {
            'guest_name': guest_name,
            'party_size': party_size_str,
            'reservation_date': reservation_date,
            'error': error
        }
        return render_template('make_reservation.html', form_state=form_state)

    # Determine new reservation_id
    reservations = load_reservations()
    new_id = 1
    if reservations:
        new_id = max(r['reservation_id'] for r in reservations) + 1

    # For time, no input specified - assume fixed time 19:00 for new reservation
    reservation_time = '19:00'

    # Use user's contact info
    phone = user['phone']
    email = user['email']

    new_reservation = {
        'reservation_id': new_id,
        'username': username,
        'guest_name': guest_name,
        'phone': phone,
        'email': email,
        'party_size': party_size,
        'date': reservation_date,
        'time': reservation_time,
        'special_requests': None,
        'status': 'Upcoming'
    }

    reservations.append(new_reservation)
    save_reservations(reservations)

    # Redirect to my_reservations after successful reservation
    return redirect(url_for('my_reservations'))


@app.route('/my-reservations')
def my_reservations():
    username = get_logged_in_username()
    reservations = load_reservations()

    user_reservations = []
    for r in reservations:
        if r['username'] == username:
            # Provide reservation_id, date, time, party_size, status
            user_reservations.append({
                'reservation_id': r['reservation_id'],
                'date': r['date'],
                'time': r['time'],
                'party_size': r['party_size'],
                'status': r['status']
            })

    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = get_logged_in_username()
    reservations = load_reservations()
    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == username and r['status'].lower() == 'upcoming':
            r['status'] = 'Cancelled'
            updated = True
            break
    if updated:
        save_reservations(reservations)
    # Redirect back to my_reservations
    return redirect(url_for('my_reservations'))


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    username = get_logged_in_username()
    waitlist_entries = load_waitlist()

    user_entry = None
    for entry in waitlist_entries:
        if entry['username'] == username and entry['status'].lower() == 'active':
            user_entry = entry
            break

    if request.method == 'POST':
        party_size_str = request.form.get('party_size', '').strip()
        try:
            party_size = int(party_size_str)
            if party_size < 1 or party_size > 10:
                raise ValueError
        except ValueError:
            # Invalid party size input; re-render page with existing info
            waitlist_position = None
            user_party_size = None
            if user_entry:
                # Determine position
                active_entries = [e for e in waitlist_entries if e['status'].lower() == 'active']
                sorted_active = sorted(active_entries, key=lambda x: x['waitlist_id'])
                positions = {entry['username']: idx+1 for idx, entry in enumerate(sorted_active)}
                waitlist_position = positions.get(username)
                user_party_size = user_entry['party_size']
            return render_template('waitlist.html', waitlist_position=waitlist_position, user_party_size=user_party_size, waitlist_entries=waitlist_entries)

        if user_entry is None:
            # Add new waitlist entry
            new_id = 1
            if waitlist_entries:
                new_id = max(e['waitlist_id'] for e in waitlist_entries) + 1
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_entry = {
                'waitlist_id': new_id,
                'username': username,
                'party_size': party_size,
                'join_time': now_str,
                'status': 'Active'
            }
            waitlist_entries.append(new_entry)
            save_waitlist(waitlist_entries)
            user_entry = new_entry

        # After adding or if user already on waitlist, show position
        active_entries = [e for e in waitlist_entries if e['status'].lower() == 'active']
        sorted_active = sorted(active_entries, key=lambda x: x['waitlist_id'])
        positions = {entry['username']: idx+1 for idx, entry in enumerate(sorted_active)}
        waitlist_position = positions.get(username)
        user_party_size = user_entry['party_size']
        return render_template('waitlist.html', waitlist_position=waitlist_position, user_party_size=user_party_size, waitlist_entries=waitlist_entries)

    else:
        # GET method
        waitlist_position = None
        user_party_size = None
        if user_entry:
            # Determine position
            active_entries = [e for e in waitlist_entries if e['status'].lower() == 'active']
            sorted_active = sorted(active_entries, key=lambda x: x['waitlist_id'])
            positions = {entry['username']: idx+1 for idx, entry in enumerate(sorted_active)}
            waitlist_position = positions.get(username)
            user_party_size = user_entry['party_size']

        return render_template('waitlist.html', waitlist_position=waitlist_position, user_party_size=user_party_size, waitlist_entries=waitlist_entries)


@app.route('/my-reviews')
def my_reviews():
    username = get_logged_in_username()
    reviews_all = load_reviews()
    menus = load_menu()

    reviews = []
    for r in reviews_all:
        if r['username'] == username:
            dish_name = None
            for d in menus:
                if d['dish_id'] == r['dish_id']:
                    dish_name = d['name']
                    break
            reviews.append({
                'review_id': r['review_id'],
                'dish_name': dish_name if dish_name else 'Unknown',
                'rating': r['rating'],
                'review_text': r['review_text']
            })

    return render_template('my_reviews.html', reviews=reviews)


@app.route('/write-review', methods=['GET', 'POST'])
def write_review():
    username = get_logged_in_username()
    menus = load_menu()
    dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menus]

    if request.method == 'GET':
        return render_template('write_review.html', dishes=dishes)

    # POST method
    dish_id_str = request.form.get('dish_id', '').strip()
    rating_str = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()

    form_state = {}
    error = None

    try:
        dish_id = int(dish_id_str)
        dish_ids = [d['dish_id'] for d in dishes]
        if dish_id not in dish_ids:
            error = 'Selected dish not found.'
    except ValueError:
        error = 'Invalid dish selection.'

    try:
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            error = 'Rating must be between 1 and 5.'
    except ValueError:
        error = 'Invalid rating value.'

    if not review_text:
        error = 'Review text cannot be empty.'

    if error:
        form_state = {
            'dish_id': dish_id_str,
            'rating': rating_str,
            'review_text': review_text,
            'error': error
        }
        return render_template('write_review.html', dishes=dishes, form_state=form_state)

    # Add new review
    reviews_all = load_reviews()
    new_id = 1
    if reviews_all:
        new_id = max(r['review_id'] for r in reviews_all) + 1

    today_str = datetime.today().strftime('%Y-%m-%d')

    new_review = {
        'review_id': new_id,
        'username': username,
        'dish_id': dish_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': today_str
    }

    reviews_all.append(new_review)
    save_reviews(reviews_all)

    return redirect(url_for('my_reviews'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = get_logged_in_username()
    users = load_users()
    user = users.get(username)
    if user is None:
        return "User not found", 404

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        # Simple validation email presence
        if email:
            user['email'] = email
            users[username] = user
            save_users(users)
        # On success or no change, render page

    user_profile = {
        'username': user['username'],
        'email': user['email']
    }
    return render_template('profile.html', user_profile=user_profile)


if __name__ == '__main__':
    app.run(debug=True)
