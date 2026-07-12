from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data from files

def load_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
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
    if not os.path.exists(path):
        return menu
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 8:
                continue
            dish_id_str, name, category, price_str, description, ingredients, dietary, avg_rating_str = parts
            try:
                dish_id = int(dish_id_str)
                price = float(price_str)
                avg_rating = float(avg_rating_str)
            except ValueError:
                continue
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
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 10:
                continue
            (res_id_str, username, guest_name, phone, email, party_size_str, date, time, special_requests, status) = parts
            try:
                reservation_id = int(res_id_str)
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
    waitlist = []
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    if not os.path.exists(path):
        return waitlist
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
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
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
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
        for username in users:
            u = users[username]
            line = '|'.join([
                u['username'],
                u['email'],
                u['phone'],
                u['full_name']
            ])
            f.write(line + '\n')


# Helpers for current user simulation
# For this implementation, we simulate logged-in user as 'john_diner'
# since no authentication mechanism specified
CURRENT_USERNAME = 'john_diner'


def get_current_user():
    users = load_users()
    return users.get(CURRENT_USERNAME, None)


# Routes Implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    if user is None:
        username = 'Guest'
    else:
        username = user['username']

    # Featured dishes: take top 5 by avg_rating descending
    menu = load_menu()
    featured = sorted(menu, key=lambda d: d['avg_rating'], reverse=True)[:5]
    featured_dishes = [{'dish_id': d['dish_id'], 'name': d['name'], 'price': d['price'], 'description': d['description']} for d in featured]

    # upcoming reservations for current user, status 'Upcoming', sorted by date & time
    all_reservations = load_reservations()
    upcoming = []
    for r in all_reservations:
        if r['username'] == CURRENT_USERNAME and r['status'] == 'Upcoming':
            upcoming.append({
                'reservation_id': r['reservation_id'],
                'date': r['date'],
                'time': r['time'],
                'party_size': r['party_size'],
                'status': r['status']
            })
    def dt_key(r):
        try:
            return datetime.strptime(r['date'] + ' ' + r['time'], '%Y-%m-%d %H:%M')
        except Exception:
            return datetime.max
    upcoming_reservations = sorted(upcoming, key=dt_key)

    return render_template('dashboard.html', username=username, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)


@app.route('/menu')
def menu():
    menu = load_menu()
    menus = []
    for d in menu:
        menus.append({
            'dish_id': d['dish_id'],
            'name': d['name'],
            'category': d['category'],
            'price': d['price'],
            'description': d['description'],
            'ingredients': d['ingredients'],
            'dietary': d['dietary'],
            'avg_rating': d['avg_rating']
        })
    return render_template('menu.html', menus=menus)


@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu = load_menu()
    dish = None
    for d in menu:
        if d['dish_id'] == dish_id:
            dish = d
            break
    if dish is None:
        # return 404 or render with error?
        return 'Dish not found', 404
    dish_info = {
        'dish_id': dish['dish_id'],
        'name': dish['name'],
        'category': dish['category'],
        'price': dish['price'],
        'description': dish['description'],
        'ingredients': dish['ingredients'],
        'dietary': dish['dietary'],
        'avg_rating': dish['avg_rating']
    }
    return render_template('dish_details.html', dish=dish_info)


@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    user = get_current_user()
    if user is None:
        # No user logged in; reject or redirect?
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        guest_name = request.form.get('guest_name', '').strip()
        party_size_str = request.form.get('party_size', '').strip()
        reservation_date = request.form.get('reservation_date', '').strip()

        # Validate inputs
        error = None
        if not guest_name:
            error = 'Guest name is required.'
        try:
            party_size = int(party_size_str)
            if not (1 <= party_size <= 10):
                error = 'Party size must be between 1 and 10.'
        except ValueError:
            error = 'Invalid party size.'

        try:
            datetime.strptime(reservation_date, '%Y-%m-%d')
        except Exception:
            error = 'Invalid reservation date.'

        if error:
            # For simplicity, re-render page with error message (not specified in spec, so not passed to template)
            return render_template('make_reservation.html')

        # Prepare new reservation_id
        reservations = load_reservations()
        if reservations:
            max_id = max(r['reservation_id'] for r in reservations)
        else:
            max_id = 0
        new_reservation_id = max_id + 1

        new_reservation = {
            'reservation_id': new_reservation_id,
            'username': user['username'],
            'guest_name': guest_name,
            'phone': user['phone'],
            'email': user['email'],
            'party_size': party_size,
            'date': reservation_date,
            'time': '19:00',  # default time since no time selection specified
            'special_requests': '',
            'status': 'Upcoming'
        }
        reservations.append(new_reservation)
        save_reservations(reservations)

        return redirect(url_for('my_reservations'))

    # GET method
    return render_template('make_reservation.html')


@app.route('/my_reservations')
def my_reservations():
    reservations = load_reservations()
    user_reservations = []
    for r in reservations:
        if r['username'] == CURRENT_USERNAME:
            user_reservations.append({
                'reservation_id': r['reservation_id'],
                'date': r['date'],
                'time': r['time'],
                'party_size': r['party_size'],
                'status': r['status']
            })
    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    cancelled = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == CURRENT_USERNAME and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            cancelled = True
            break
    if cancelled:
        save_reservations(reservations)
    # redirect back to my_reservations regardless
    return redirect(url_for('my_reservations'))


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    waitlist = load_waitlist()
    user_entry = None

    for entry in waitlist:
        if entry['username'] == CURRENT_USERNAME and entry['status'] == 'Active':
            user_entry = entry
            break

    if request.method == 'POST':
        if user_entry is None:
            # add user to waitlist
            party_size_str = request.form.get('party_size', '').strip()
            try:
                party_size = int(party_size_str)
                if party_size < 1:
                    party_size = 1
            except Exception:
                party_size = 1

            # Determine new waitlist_id
            if waitlist:
                max_id = max(w['waitlist_id'] for w in waitlist)
            else:
                max_id = 0
            new_id = max_id + 1
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_entry = {
                'waitlist_id': new_id,
                'username': CURRENT_USERNAME,
                'party_size': party_size,
                'join_time': now_str,
                'status': 'Active'
            }
            waitlist.append(new_entry)
            save_waitlist(waitlist)
            return redirect(url_for('waitlist'))
        else:
            # already in waitlist, POST has no effect
            return redirect(url_for('waitlist'))

    # GET method
    if user_entry is None:
        waitlist_position = None
    else:
        # Calculate position by join time ascending among active entries
        active_list = [w for w in waitlist if w['status'] == 'Active']
        active_list.sort(key=lambda x: datetime.strptime(x['join_time'], '%Y-%m-%d %H:%M:%S'))
        pos = 1
        for w in active_list:
            if w['username'] == CURRENT_USERNAME:
                waitlist_position = pos
                break
            pos += 1
        else:
            waitlist_position = None

    return render_template('waitlist.html', waitlist_position=waitlist_position)


@app.route('/my_reviews')
def my_reviews():
    reviews = load_reviews()
    menu = load_menu()
    # build dish_id->name map
    dish_name_map = {d['dish_id']: d['name'] for d in menu}

    user_reviews = []
    for r in reviews:
        if r['username'] == CURRENT_USERNAME:
            dish_name = dish_name_map.get(r['dish_id'], 'Unknown')
            user_reviews.append({
                'review_id': r['review_id'],
                'dish_id': r['dish_id'],
                'dish_name': dish_name,
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })

    return render_template('my_reviews.html', reviews=user_reviews)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    menu = load_menu()
    dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu]

    if request.method == 'POST':
        dish_id_str = request.form.get('dish_id', '').strip()
        rating_str = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()

        error = None
        try:
            dish_id = int(dish_id_str)
        except ValueError:
            dish_id = None
            error = 'Invalid dish selected.'
        try:
            rating = int(rating_str)
            if not (1 <= rating <= 5):
                error = 'Rating must be between 1 and 5.'
        except ValueError:
            rating = None
            error = 'Invalid rating.'

        if error:
            return render_template('write_review.html', dishes=dishes)

        reviews = load_reviews()
        if reviews:
            max_id = max(r['review_id'] for r in reviews)
        else:
            max_id = 0
        new_review_id = max_id + 1

        today_str = datetime.now().strftime('%Y-%m-%d')

        new_review = {
            'review_id': new_review_id,
            'username': CURRENT_USERNAME,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': today_str
        }
        reviews.append(new_review)
        save_reviews(reviews)

        return redirect(url_for('my_reviews'))

    # GET
    return render_template('write_review.html', dishes=dishes)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = load_users()
    user = users.get(CURRENT_USERNAME, None)
    if user is None:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        new_email = request.form.get('email', '').strip()
        if new_email:
            user['email'] = new_email
            users[CURRENT_USERNAME] = user
            save_users(users)

    user_profile = {
        'username': user['username'],
        'email': user['email']
    }

    return render_template('profile.html', user_profile=user_profile)


if __name__ == '__main__':
    app.run(debug=True)
