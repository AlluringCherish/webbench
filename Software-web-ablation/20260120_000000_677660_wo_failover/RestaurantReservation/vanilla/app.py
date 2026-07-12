from flask import Flask, render_template, redirect, url_for, request
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Utility functions for loading and saving data files
DATA_DIR = 'data'

# -------- DATA LOADING FUNCTIONS -------- #
def load_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = {}
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
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
    path = os.path.join(DATA_DIR, 'menu.txt')
    menu = []
    if not os.path.exists(path):
        return menu
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 8:
                continue
            dish_id = int(parts[0])
            name = parts[1]
            category = parts[2]
            try:
                price = float(parts[3])
            except ValueError:
                price = 0.0
            description = parts[4]
            ingredients = parts[5]
            dietary = parts[6]
            try:
                avg_rating = float(parts[7])
            except ValueError:
                avg_rating = 0.0
            dish = {
                'dish_id': dish_id,
                'name': name,
                'category': category,
                'price': price,
                'description': description,
                'ingredients': ingredients,
                'dietary': dietary,
                'avg_rating': avg_rating
            }
            menu.append(dish)
    return menu

def load_reservations():
    path = os.path.join(DATA_DIR, 'reservations.txt')
    reservations = []
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 10:
                continue
            try:
                reservation_id = int(parts[0])
                username = parts[1]
                guest_name = parts[2]
                phone = parts[3]
                email = parts[4]
                party_size = int(parts[5])
                date = parts[6]
                time_ = parts[7]
                special_requests = parts[8]
                status = parts[9]
            except Exception:
                continue
            reservations.append({
                'reservation_id': reservation_id,
                'username': username,
                'guest_name': guest_name,
                'phone': phone,
                'email': email,
                'party_size': party_size,
                'date': date,
                'time': time_,
                'special_requests': special_requests,
                'status': status
            })
    return reservations

def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
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

def load_waitlist():
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    waitlist = []
    if not os.path.exists(path):
        return waitlist
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 5:
                continue
            try:
                waitlist_id = int(parts[0])
                username = parts[1]
                party_size = int(parts[2])
                join_time = parts[3]
                status = parts[4]
            except Exception:
                continue
            waitlist.append({
                'waitlist_id': waitlist_id,
                'username': username,
                'party_size': party_size,
                'join_time': join_time,
                'status': status
            })
    return waitlist

def save_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
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

def load_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) < 6:
                continue
            try:
                review_id = int(parts[0])
                username = parts[1]
                dish_id = int(parts[2])
                rating = int(parts[3])
                review_text = parts[4]
                review_date = parts[5]
            except Exception:
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

def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
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

def save_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for username, u in users.items():
            line = '|'.join([
                u['username'],
                u['email'],
                u['phone'],
                u['full_name']
            ])
            f.write(line + '\n')

# Helper to get user profile from username
# For simplicity, we pick first user as logged-in user for this implementation
# as no authentication specified in design_spec

def get_logged_in_username():
    # We pick 'john_diner' as logged in user for demonstration
    return 'john_diner'

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    username = get_logged_in_username()
    users = load_users()
    menu = load_menu()
    reservations = load_reservations()

    # featured_dishes: pick top 3 dishes by avg_rating descending
    featured_dishes = sorted(menu, key=lambda d: d['avg_rating'], reverse=True)[:3]
    # reduce to needed dict keys
    featured_dishes_out = []
    for d in featured_dishes:
        featured_dishes_out.append({
            'dish_id': d['dish_id'],
            'name': d['name'],
            'price': d['price'],
            'description': d['description']
        })

    # upcoming_reservations for this user (status == Upcoming), sorted by date then time
    user_reservations = [r for r in reservations if r['username'] == username and r['status'] == 'Upcoming']
    user_reservations = sorted(user_reservations, key=lambda r: (r['date'], r['time']))
    upcoming_reservations = []
    for r in user_reservations:
        upcoming_reservations.append({
            'reservation_id': r['reservation_id'],
            'date': r['date'],
            'time': r['time'],
            'party_size': r['party_size'],
            'status': r['status']
        })

    return render_template('dashboard.html',
                           username=username,
                           featured_dishes=featured_dishes_out,
                           upcoming_reservations=upcoming_reservations)

@app.route('/menu')
def menu():
    menu_items = load_menu()
    reviews = load_reviews()

    # For each dish compute avg_rating from reviews if any, else use avg_rating from file
    dish_reviews = {}
    for r in reviews:
        dish_reviews.setdefault(r['dish_id'], []).append(r['rating'])

    menus_out = []
    for d in menu_items:
        ratings = dish_reviews.get(d['dish_id'], [])
        if ratings:
            avg_rating = round(sum(ratings) / len(ratings), 2)
        else:
            avg_rating = d['avg_rating']
        menus_out.append({
            'dish_id': d['dish_id'],
            'name': d['name'],
            'category': d['category'],
            'price': d['price'],
            'description': d['description'],
            'dietary': d['dietary'],
            'avg_rating': avg_rating
        })

    return render_template('menu.html', menus=menus_out)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu_items = load_menu()
    reviews = load_reviews()
    dish = None
    for d in menu_items:
        if d['dish_id'] == dish_id:
            dish = d
            break
    if dish is None:
        # Dish not found, render with dish as None or a 404
        return render_template('dish_details.html', dish=None), 404

    # Compute avg_rating from reviews for this dish
    ratings = [r['rating'] for r in reviews if r['dish_id'] == dish_id]
    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else dish['avg_rating']

    dish_out = {
        'dish_id': dish['dish_id'],
        'name': dish['name'],
        'category': dish['category'],
        'price': dish['price'],
        'description': dish['description'],
        'ingredients': dish['ingredients'],
        'dietary': dish['dietary'],
        'avg_rating': avg_rating
    }

    return render_template('dish_details.html', dish=dish_out)

@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    username = get_logged_in_username()
    users = load_users()
    # We will assume guest contact details from user profile
    user_profile = users.get(username, None)
    if request.method == 'GET':
        # Show form
        return render_template('make_reservation.html')
    else:
        # POST - handle form submission
        guest_name = request.form.get('guest_name', '').strip()
        party_size_str = request.form.get('party_size', '').strip()
        reservation_date = request.form.get('reservation_date', '').strip()

        error_message = None
        # Validate guest_name
        if not guest_name:
            error_message = "Guest name is required."
        # Validate party_size
        try:
            party_size = int(party_size_str)
            if not (1 <= party_size <= 10):
                error_message = "Party size must be between 1 and 10."
        except ValueError:
            error_message = "Invalid party size."
        # Validate reservation_date format YYYY-MM-DD
        try:
            datetime.datetime.strptime(reservation_date, '%Y-%m-%d')
        except ValueError:
            error_message = "Invalid date format, use YYYY-MM-DD."

        if error_message:
            # Normally we would re-render with error message context, but spec says handled internally
            # Here we reload the form
            return render_template('make_reservation.html', error=error_message)

        # Read existing reservations
        reservations = load_reservations()

        # Find max reservation_id for new ID
        max_id = max((r['reservation_id'] for r in reservations), default=0)
        new_reservation_id = max_id + 1

        phone = user_profile['phone'] if user_profile else ''
        email = user_profile['email'] if user_profile else ''

        # Time not specified in form, using default time 19:00 for all new reservations
        time_ = '19:00'

        new_reservation = {
            'reservation_id': new_reservation_id,
            'username': username,
            'guest_name': guest_name,
            'phone': phone,
            'email': email,
            'party_size': party_size,
            'date': reservation_date,
            'time': time_,
            'special_requests': '',
            'status': 'Upcoming'
        }
        reservations.append(new_reservation)
        save_reservations(reservations)

        # Redirect to my_reservations page to confirm
        return redirect(url_for('my_reservations'))

@app.route('/my_reservations')
def my_reservations():
    username = get_logged_in_username()
    reservations = load_reservations()

    user_reservations = [r for r in reservations if r['username'] == username]
    # sort by date then time
    user_reservations_sorted = sorted(user_reservations, key=lambda r: (r['date'], r['time']))

    reservations_out = []
    for r in user_reservations_sorted:
        reservations_out.append({
            'reservation_id': r['reservation_id'],
            'date': r['date'],
            'time': r['time'],
            'party_size': r['party_size'],
            'status': r['status'],
            'guest_name': r['guest_name']
        })

    return render_template('my_reservations.html', reservations=reservations_out)

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = get_logged_in_username()
    reservations = load_reservations()
    found = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == username:
            # Only allow cancel if status is Upcoming
            if r['status'] == 'Upcoming':
                r['status'] = 'Cancelled'
                found = True
            break
    if found:
        save_reservations(reservations)
        # Redirect back to my_reservations
        return redirect(url_for('my_reservations'))
    else:
        # Not found or not allowed
        return redirect(url_for('my_reservations'))

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    username = get_logged_in_username()
    waitlist_entries = load_waitlist()

    # Find if user is on waitlist with status Active
    user_entry = next((w for w in waitlist_entries if w['username'] == username and w['status'] == 'Active'), None)

    if request.method == 'GET':
        user_position = None
        if user_entry:
            # Sort active waitlist by join_time ascending
            active_waitlist = sorted([w for w in waitlist_entries if w['status'] == 'Active'], key=lambda w: w['join_time'])
            # Find position
            try:
                user_position = active_waitlist.index(user_entry) + 1
            except ValueError:
                user_position = None
        return render_template('waitlist.html', user_position=user_position)

    else:
        # POST - join waitlist
        party_size_str = request.form.get('party_size', '').strip()
        error_message = None
        try:
            party_size = int(party_size_str)
            if party_size < 1:
                error_message = "Party size must be positive integer."
        except ValueError:
            error_message = "Invalid party size."

        if error_message:
            # show current user position in GET style
            user_position = None
            if user_entry:
                active_waitlist = sorted([w for w in waitlist_entries if w['status'] == 'Active'], key=lambda w: w['join_time'])
                try:
                    user_position = active_waitlist.index(user_entry) + 1
                except ValueError:
                    user_position = None
            return render_template('waitlist.html', user_position=user_position, error=error_message)

        # Check if user already on waitlist active
        if user_entry:
            # Already on waitlist, do not add again
            user_position = None
            # find position
            active_waitlist = sorted([w for w in waitlist_entries if w['status'] == 'Active'], key=lambda w: w['join_time'])
            try:
                user_position = active_waitlist.index(user_entry) + 1
            except ValueError:
                user_position = None
            return render_template('waitlist.html', user_position=user_position)

        # Add new waitlist entry
        max_id = max((w['waitlist_id'] for w in waitlist_entries), default=0)
        new_id = max_id + 1
        join_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_entry = {
            'waitlist_id': new_id,
            'username': username,
            'party_size': party_size,
            'join_time': join_time,
            'status': 'Active'
        }
        waitlist_entries.append(new_entry)
        save_waitlist(waitlist_entries)

        # New position is at end of active waitlist
        active_waitlist = sorted([w for w in waitlist_entries if w['status'] == 'Active'], key=lambda w: w['join_time'])
        user_position = active_waitlist.index(new_entry) + 1

        return render_template('waitlist.html', user_position=user_position)

@app.route('/my_reviews')
def my_reviews():
    username = get_logged_in_username()
    reviews = load_reviews()
    menu = load_menu()

    # Filter user's reviews
    user_reviews = [r for r in reviews if r['username'] == username]

    # Map dish_id to dish_name
    dish_name_map = {d['dish_id']: d['name'] for d in menu}

    reviews_out = []
    for r in user_reviews:
        reviews_out.append({
            'review_id': r['review_id'],
            'dish_name': dish_name_map.get(r['dish_id'], 'Unknown Dish'),
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    return render_template('my_reviews.html', reviews=reviews_out)

@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    username = get_logged_in_username()
    menu = load_menu()
    reviews = load_reviews()

    if request.method == 'GET':
        dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu]
        return render_template('write_review.html', dishes=dishes)

    else:
        dish_id_str = request.form.get('dish_id', '').strip()
        rating_str = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()

        error_message = None

        try:
            dish_id = int(dish_id_str)
        except ValueError:
            error_message = "Invalid dish selection."

        try:
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                error_message = "Rating must be between 1 and 5."
        except ValueError:
            error_message = "Rating must be an integer between 1 and 5."

        if not review_text:
            error_message = "Review text cannot be empty."

        # Verify dish_id exists in menu
        if error_message is None:
            dish_ids = [d['dish_id'] for d in menu]
            if dish_id not in dish_ids:
                error_message = "Selected dish does not exist."

        if error_message:
            dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu]
            return render_template('write_review.html', dishes=dishes, error=error_message)

        reviews_list = reviews
        max_id = max((r['review_id'] for r in reviews_list), default=0)
        new_id = max_id + 1

        review_date = datetime.datetime.now().strftime('%Y-%m-%d')

        new_review = {
            'review_id': new_id,
            'username': username,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }

        reviews_list.append(new_review)
        save_reviews(reviews_list)

        return redirect(url_for('my_reviews'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = get_logged_in_username()
    users = load_users()
    user_profile = users.get(username, None)

    if request.method == 'GET':
        if user_profile is None:
            # guest profile default empty
            user_profile = {
                'username': username,
                'email': '',
                'phone': '',
                'full_name': ''
            }
        return render_template('profile.html', user_profile=user_profile)
    else:
        # POST update
        email = request.form.get('email', '').strip()
        error_message = None
        # Basic email validation (contains @)
        if '@' not in email or email.startswith('@') or email.endswith('@'):
            error_message = "Invalid email address."

        if error_message:
            return render_template('profile.html', user_profile=user_profile, error=error_message)

        # Update users.txt email for logged in user
        if user_profile:
            user_profile['email'] = email
            users[username] = user_profile
            save_users(users)

        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
