from flask import Flask, request, redirect, url_for, render_template, abort, jsonify
import os
import threading
from datetime import datetime, date

app = Flask(__name__)

data_dir = 'data'

# File paths
users_file = os.path.join(data_dir, 'users.txt')
menu_file = os.path.join(data_dir, 'menu.txt')
reservations_file = os.path.join(data_dir, 'reservations.txt')
waitlist_file = os.path.join(data_dir, 'waitlist.txt')
reviews_file = os.path.join(data_dir, 'reviews.txt')

file_locks = {
    'users': threading.Lock(),
    'menu': threading.Lock(),
    'reservations': threading.Lock(),
    'waitlist': threading.Lock(),
    'reviews': threading.Lock()
}


# ------------------------ Helper Functions ------------------------ #

def read_file_to_dicts(filename, schema_keys):
    ''' Read entire file and parse lines into list of dicts with given schema keys '''
    entries = []
    if not os.path.exists(filename):
        return entries
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != len(schema_keys):
                continue  # skip malformed line
            entry = dict(zip(schema_keys, parts))
            entries.append(entry)
    return entries


def write_file_overwrite(filename, lines):
    ''' Overwrite the entire file with provided list of lines (strings) '''
    with open(filename, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


def append_line_to_file(filename, line):
    ''' Append one line to a file '''
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def get_next_id(entries, id_key):
    ''' Utility to get next integer ID given list of dict entries and id key as string '''
    max_id = 0
    for e in entries:
        try:
            eid = int(e.get(id_key, 0))
            if eid > max_id:
                max_id = eid
        except:
            pass
    return max_id + 1


def parse_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def parse_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default


def format_reservation_line(res):
    ''' Format reservation dict to line string in file format '''
    fields = [str(res.get('reservation_id', '')),
              res.get('username', ''),
              res.get('guest_name', ''),
              res.get('phone', ''),
              res.get('email', ''),
              str(res.get('party_size', '')), 
              res.get('date', ''),
              res.get('time', ''),
              res.get('special_requests', ''),
              res.get('status', '')]
    return '|'.join(fields)


def format_waitlist_line(wait):
    ''' Format waitlist dict to line string in file format '''
    fields = [str(wait.get('waitlist_id', '')),
              wait.get('username', ''),
              str(wait.get('party_size', '')),
              wait.get('join_time', ''),
              wait.get('status', '')]
    return '|'.join(fields)


def format_review_line(review):
    ''' Format review dict to line string in file format '''
    fields = [str(review.get('review_id', '')),
              review.get('username', ''),
              str(review.get('dish_id', '')),
              str(review.get('rating', '')),
              review.get('review_text', ''),
              review.get('review_date', '')]
    return '|'.join(fields)


def format_user_line(user):
    ''' Format user dict to line string in file format '''
    fields = [user.get('username', ''),
              user.get('email', ''),
              user.get('phone', ''),
              user.get('full_name', '')]
    return '|'.join(fields)


def format_menu_line(dish):
    ''' Format dish dict to line string in file format '''
    fields = [str(dish.get('dish_id', '')),
              dish.get('name', ''),
              dish.get('category', ''),
              str(dish.get('price', '')),
              dish.get('description', ''),
              dish.get('ingredients', ''),
              dish.get('dietary', ''),
              str(dish.get('avg_rating', ''))]
    return '|'.join(fields)


def get_user(username):
    ''' Returns user dict by username or None if not found '''
    users = read_file_to_dicts(users_file, ['username','email','phone','full_name'])
    for user in users:
        if user['username'] == username:
            return user
    return None


def update_user(updated_user):
    ''' Update user in users.txt by username '''
    with file_locks['users']:
        users = read_file_to_dicts(users_file, ['username','email','phone','full_name'])
        new_lines = []
        found = False
        for user in users:
            if user['username'] == updated_user['username']:
                new_lines.append(format_user_line(updated_user))
                found = True
            else:
                new_lines.append(format_user_line(user))
        if found:
            write_file_overwrite(users_file, new_lines)
            return True
        else:
            return False


def get_menu_items():
    ''' Load all menu dishes as list of dict '''
    dishes = read_file_to_dicts(menu_file, ['dish_id','name','category','price','description','ingredients','dietary','avg_rating'])
    for dish in dishes:
        dish['dish_id'] = parse_int(dish['dish_id'])
        dish['price'] = parse_float(dish['price'])
        dish['avg_rating'] = parse_float(dish['avg_rating'])
    return dishes


def get_menu_item_by_id(dish_id):
    ''' Get a single dish by dish_id or None if not found '''
    dishes = get_menu_items()
    for dish in dishes:
        if dish['dish_id'] == dish_id:
            return dish
    return None


def get_reservations():
    ''' Load all reservations as list of dict '''
    res_list = read_file_to_dicts(reservations_file, ['reservation_id','username','guest_name','phone','email','party_size','date','time','special_requests','status'])
    for r in res_list:
        r['reservation_id'] = parse_int(r['reservation_id'])
        r['party_size'] = parse_int(r['party_size'])
    return res_list


def get_user_reservations(username):
    ''' Get list of reservations for a username '''
    all_res = get_reservations()
    return [r for r in all_res if r['username'] == username]


def add_reservation(reservation):
    ''' Add a new reservation to reservations.txt with auto ID and status Upcoming '''
    with file_locks['reservations']:
        reservations = get_reservations()
        new_id = get_next_id(reservations, 'reservation_id')
        reservation['reservation_id'] = new_id
        reservation['status'] = 'Upcoming'
        line = format_reservation_line(reservation)
        append_line_to_file(reservations_file, line)
        return new_id


def update_reservations_list(reservations):
    ''' Overwrite all reservations with the provided list '''
    with file_locks['reservations']:
        lines = [format_reservation_line(r) for r in reservations]
        write_file_overwrite(reservations_file, lines)


def cancel_reservation_by_id(reservation_id, username):
    ''' Cancel a reservation by id if owned by user and status Upcoming '''
    reservations = get_reservations()
    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == username and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            updated = True
            break
    if updated:
        update_reservations_list(reservations)
    return updated


def get_waitlist():
    ''' Load all waitlist entries as list of dict '''
    waits = read_file_to_dicts(waitlist_file, ['waitlist_id','username','party_size','join_time','status'])
    for w in waits:
        w['waitlist_id'] = parse_int(w['waitlist_id'])
        w['party_size'] = parse_int(w['party_size'])
    return waits


def get_user_waitlist_entry(username):
    waits = get_waitlist()
    for w in waits:
        if w['username'] == username and w['status'] == 'Active':
            return w
    return None


def add_waitlist_entry(username, party_size):
    with file_locks['waitlist']:
        waits = get_waitlist()
        new_id = get_next_id(waits, 'waitlist_id')
        join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = {
            'waitlist_id': new_id,
            'username': username,
            'party_size': party_size,
            'join_time': join_time,
            'status': 'Active'
        }
        line = format_waitlist_line(entry)
        append_line_to_file(waitlist_file, line)
        return new_id


def update_waitlist(waitlist_entries):
    with file_locks['waitlist']:
        lines = [format_waitlist_line(w) for w in waitlist_entries]
        write_file_overwrite(waitlist_file, lines)


def get_reviews():
    ''' Load all reviews as list of dict '''
    reviews = read_file_to_dicts(reviews_file, ['review_id','username','dish_id','rating','review_text','review_date'])
    for rv in reviews:
        rv['review_id'] = parse_int(rv['review_id'])
        rv['dish_id'] = parse_int(rv['dish_id'])
        rv['rating'] = parse_int(rv['rating'])
    return reviews


def get_user_reviews(username):
    reviews = get_reviews()
    return [r for r in reviews if r['username'] == username]


def add_review(review):
    with file_locks['reviews']:
        reviews = get_reviews()
        new_id = get_next_id(reviews, 'review_id')
        review['review_id'] = new_id
        review['review_date'] = date.today().strftime('%Y-%m-%d')
        line = format_review_line(review)
        append_line_to_file(reviews_file, line)
        return new_id


# -------------------- Dummy User Identity / Session -------------------- #

# IMPORTANT: The design_spec.md does not specify how user identity is determined or authenticated.
# For backend functional completeness, we simulate user login identity through a query parameter (?user=) or
# a fixed dummy user assignment for demonstration purpose.

# This function extracts username from request, preferably via query param or header (for demo)
# In real app, would integrate with auth/session system.


def get_current_username():
    # Priority: form field 'username' or URL query param 'user' for simulation
    username = request.args.get('user')
    if not username:
        username = request.form.get('username')
    if not username:
        # Fallback dummy user for demo
        username = 'john_diner'
    return username


# ------------------------ Route Implementations ------------------------ #

@app.route('/dashboard', methods=['GET'])
def dashboard():
    ''' Dashboard page showing welcome and optional featured info '''
    username = get_current_username()
    user = get_user(username)
    if not user:
        abort(404, 'User not found')

    # Load upcoming reservations for user sorted by date/time
    reservations = get_user_reservations(username)
    upcoming_reservations = sorted(
        [r for r in reservations if r['status'] == 'Upcoming'],
        key=lambda x: (x['date'], x['time'])
    )

    # For demonstration, no featured dishes loaded (could be top rated dishes)
    featured_dishes = []

    # Return template with context
    return render_template('dashboard.html', username=username, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)


@app.route('/menu', methods=['GET'])
def menu():
    ''' Menu page with optional filtering by category or search text '''
    category = request.args.get('category', '').strip()
    search = request.args.get('search', '').strip().lower()

    dishes = get_menu_items()
    filtered = dishes

    if category:
        filtered = [d for d in filtered if d['category'].lower() == category.lower()]

    if search:
        filtered = [d for d in filtered if search in d['name'].lower() or search in d.get('description', '').lower()]

    # Provide only required fields to template
    menu_items = []
    for dish in filtered:
        menu_items.append({
            'dish_id': dish['dish_id'],
            'name': dish['name'],
            'category': dish['category'],
            'price': dish['price'],
            'description': dish['description'],
            'avg_rating': dish['avg_rating']
        })

    return render_template('menu.html', menu_items=menu_items)


@app.route('/menu/<int:dish_id>', methods=['GET'])
def dish_details(dish_id):
    ''' Show dish details by ID '''
    dish = get_menu_item_by_id(dish_id)
    if not dish:
        abort(404, 'Dish not found')

    return render_template('dish_details.html', dish=dish)


@app.route('/reservation/make', methods=['GET', 'POST'])
def make_reservation():
    ''' Make a new reservation: GET shows form, POST handles submission '''
    username = get_current_username()
    user = get_user(username)
    if not user:
        abort(404, 'User not found')

    possible_party_sizes = list(range(1, 11))

    if request.method == 'POST':
        guest_name = request.form.get('guest_name', '').strip()
        party_size = parse_int(request.form.get('party_size', '0'))
        reservation_date = request.form.get('reservation_date', '').strip()

        # Minimal validation
        errors = []
        if not guest_name:
            errors.append('Guest name is required.')
        if party_size < 1 or party_size > 10:
            errors.append('Party size must be between 1 and 10.')
        try:
            res_date_obj = datetime.strptime(reservation_date, '%Y-%m-%d').date()
            if res_date_obj < date.today():
                errors.append('Reservation date must not be in the past.')
        except ValueError:
            errors.append('Invalid reservation date format.')

        if errors:
            # Either could render template with errors, or just abort for now
            return render_template('make_reservation.html', possible_party_sizes=possible_party_sizes, guest_name=guest_name, errors=errors)

        # Create reservation record
        reservation = {
            'username': username,
            'guest_name': guest_name,
            'phone': user.get('phone', ''),
            'email': user.get('email', ''),
            'party_size': party_size,
            'date': reservation_date,
            'time': '18:00',  # Fixed time for simplicity
            'special_requests': '',
        }

        add_reservation(reservation)

        return redirect(url_for('dashboard', user=username))

    # GET
    guest_name_prefill = user.get('full_name', '')
    return render_template('make_reservation.html', possible_party_sizes=possible_party_sizes, guest_name=guest_name_prefill)


@app.route('/reservations/my', methods=['GET'])
def my_reservations():
    ''' List the logged in user's reservations '''
    username = get_current_username()
    user = get_user(username)
    if not user:
        abort(404, 'User not found')

    reservations = get_user_reservations(username)
    # Provide required fields to template
    reservations_for_template = []
    for r in reservations:
        reservations_for_template.append({
            'reservation_id': r['reservation_id'],
            'date': r['date'],
            'time': r['time'],
            'party_size': r['party_size'],
            'status': r['status']
        })

    return render_template('my_reservations.html', reservations=reservations_for_template)


@app.route('/reservations/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    ''' Cancel a reservation owned by the logged in user if status Upcoming '''
    username = get_current_username()
    user = get_user(username)
    if not user:
        abort(404, 'User not found')

    success = cancel_reservation_by_id(reservation_id, username)
    if not success:
        abort(403, 'Cancellation not allowed or reservation not found')

    return redirect(url_for('my_reservations', user=username))


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    ''' Show waitlist and allow user to join if POST '''
    username = get_current_username()
    user = get_user(username)
    if not user:
        abort(404, 'User not found')

    possible_party_sizes = list(range(1, 11))

    if request.method == 'POST':
        party_size = parse_int(request.form.get('party_size', '0'))
        if party_size < 1 or party_size > 10:
            party_size = 1

        current_entry = get_user_waitlist_entry(username)
        if current_entry is None:
            add_waitlist_entry(username, party_size)
        # else user already on waitlist - do nothing or refresh
        return redirect(url_for('waitlist', user=username))

    # GET
    current_entry = get_user_waitlist_entry(username)
    if current_entry:
        # Determine user position (1-based) by join_time ascending
        waits = get_waitlist()
        active_waits = sorted([w for w in waits if w['status'] == 'Active'], key=lambda x: x['join_time'])
        position = 1
        for idx, w in enumerate(active_waits):
            if w['username'] == username:
                position = idx + 1
                break
        user_position = position
    else:
        user_position = 'You are not currently on the waitlist.'

    return render_template('waitlist.html', possible_party_sizes=possible_party_sizes, user_position=user_position)


@app.route('/reviews/my', methods=['GET'])
def my_reviews():
    ''' Show reviews by user '''
    username = get_current_username()
    user = get_user(username)
    if not user:
        abort(404, 'User not found')

    reviews = get_user_reviews(username)
    dishes = {d['dish_id']: d['name'] for d in get_menu_items()}

    reviews_for_template = []
    for r in reviews:
        reviews_for_template.append({
            'dish_name': dishes.get(r['dish_id'], 'Unknown Dish'),
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    return render_template('my_reviews.html', reviews=reviews_for_template)


@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    ''' Write a new review GET renders form, POST submits review '''
    username = get_current_username()
    user = get_user(username)
    if not user:
        abort(404, 'User not found')

    if request.method == 'POST':
        dish_id = parse_int(request.form.get('dish_id', '0'))
        rating = parse_int(request.form.get('rating', '0'))
        review_text = request.form.get('review_text', '').strip()

        # Validate
        errors = []
        if dish_id == 0 or get_menu_item_by_id(dish_id) is None:
            errors.append('Invalid dish selected.')
        if rating < 1 or rating > 5:
            errors.append('Rating must be between 1 and 5.')
        if not review_text:
            errors.append('Review text cannot be empty.')

        if errors:
            dishes_for_review = [{'dish_id': d['dish_id'], 'name': d['name']} for d in get_menu_items()]
            return render_template('write_review.html', errors=errors, dishes_for_review=dishes_for_review)

        review = {
            'username': username,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text
        }

        add_review(review)
        return redirect(url_for('my_reviews', user=username))

    # GET
    dishes_for_review = [{'dish_id': d['dish_id'], 'name': d['name']} for d in get_menu_items()]
    return render_template('write_review.html', dishes_for_review=dishes_for_review)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    ''' Display and update user profile email '''
    username = get_current_username()
    user = get_user(username)
    if not user:
        abort(404, 'User not found')

    if request.method == 'POST':
        new_email = request.form.get('email', '').strip()
        # Here we only update email as per design
        if new_email and new_email != user.get('email', ''):
            user['email'] = new_email
            update_user(user)
        return render_template('profile.html', username=username, email=user.get('email', ''))

    # GET
    return render_template('profile.html', username=username, email=user.get('email', ''))


if __name__ == '__main__':
    # Run app on localhost debug mode
    app.run(debug=True)
