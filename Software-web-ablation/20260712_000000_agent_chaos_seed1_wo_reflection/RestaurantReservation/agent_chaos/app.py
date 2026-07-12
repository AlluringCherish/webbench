from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# --- Helper functions to load data from the files ---

DATA_DIR = 'data'


def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
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


def load_menu():
    menu_items = []
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    dish_id = int(parts[0])
                    name = parts[1]
                    category = parts[2]
                    try:
                        price = float(parts[3])
                    except ValueError:
                        price = 0.0
                    description = parts[4]
                    # ingredients = parts[5]  # not used
                    # dietary = parts[6]      # not used
                    # avg_rating = parts[7]   # not used here
                    menu_items.append({
                        'dish_id': dish_id,
                        'name': name,
                        'category': category,
                        'price': price,
                        'description': description
                    })
    except FileNotFoundError:
        pass
    return menu_items


def load_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    reservation_id = int(parts[0])
                    username = parts[1]
                    guest_name = parts[2]
                    phone = parts[3]
                    email = parts[4]
                    try:
                        party_size = int(parts[5])
                    except ValueError:
                        party_size = 1
                    date = parts[6]
                    time = parts[7]
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
    except FileNotFoundError:
        pass
    return reservations


def load_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    waitlist_id = int(parts[0])
                    username = parts[1]
                    try:
                        party_size = int(parts[2])
                    except ValueError:
                        party_size = 1
                    join_time = parts[3]
                    status = parts[4]
                    waitlist.append({
                        'waitlist_id': waitlist_id,
                        'username': username,
                        'party_size': party_size,
                        'join_time': join_time,
                        'status': status
                    })
    except FileNotFoundError:
        pass
    return waitlist


def load_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    review_id = int(parts[0])
                    username = parts[1]
                    try:
                        dish_id = int(parts[2])
                    except ValueError:
                        dish_id = 0
                    try:
                        rating = int(parts[3])
                    except ValueError:
                        rating = 0
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
    except FileNotFoundError:
        pass
    return reviews


# --- Helper functions to write data files ---

def save_reservations(reservations):
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w', encoding='utf-8') as f:
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
    except Exception:
        pass


def save_waitlist(waitlist):
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'w', encoding='utf-8') as f:
            for w in waitlist:
                line = '|'.join([
                    str(w['waitlist_id']),
                    w['username'],
                    str(w['party_size']),
                    w['join_time'],
                    w['status']
                ])
                f.write(line + '\n')
    except Exception:
        pass


def save_reviews(reviews):
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
            for rev in reviews:
                line = '|'.join([
                    str(rev['review_id']),
                    rev['username'],
                    str(rev['dish_id']),
                    str(rev['rating']),
                    rev['review_text'],
                    rev['review_date']
                ])
                f.write(line + '\n')
    except Exception:
        pass


# --- Dummy current user for demo purposes ---
# Since the spec does not mention login, we will assume a fixed user for session.
CURRENT_USERNAME = 'john_diner'

# Load all user info once to get user details
users_db = load_users()


@app.route('/')
def root_redirect():
    # Redirect to /dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Show dashboard page
    username = CURRENT_USERNAME

    menu_all = load_menu()

    # Featured dishes: pick 3 with highest avg rating from menu.txt
    # We need to reload full menu with avg ratings for this feature
    featured_dishes = []
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r', encoding='utf-8') as f:
            dishes = []
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    dish_id = int(parts[0])
                    name = parts[1]
                    price = float(parts[3])
                    description = parts[4]
                    avg_rating = float(parts[7])
                    dishes.append({'dish_id': dish_id, 'name': name, 'price': price,
                                   'description': description, 'avg_rating': avg_rating})
            # Sort by avg_rating desc
            dishes.sort(key=lambda x: x['avg_rating'], reverse=True)
            featured_dishes = [
                {'dish_id': d['dish_id'], 'name': d['name'], 'price': d['price'], 'description': d['description']}
                for d in dishes[:3]
            ]
    except FileNotFoundError:
        featured_dishes = []

    # Load reservations for user with status Upcoming
    reservations = load_reservations()
    upcoming_reservations = []
    for r in reservations:
        if r['username'] == username and r['status'] == 'Upcoming':
            upcoming_reservations.append({
                'reservation_id': r['reservation_id'],
                'date': r['date'],
                'time': r['time'],
                'party_size': r['party_size'],
                'status': r['status']
            })

    return render_template('dashboard.html', username=username, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)


@app.route('/menu')
def menu():
    menu_items = load_menu()
    return render_template('menu.html', menu_items=menu_items)


@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    dish = None
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    d_id = int(parts[0])
                    if d_id == dish_id:
                        dish = {
                            'dish_id': d_id,
                            'name': parts[1],
                            'price': float(parts[3]),
                            'description': parts[4]
                        }
                        break
    except FileNotFoundError:
        dish = None
    if dish is None:
        # Could add 404 handler but spec does not specify; fallback show empty detail
        dish = {'dish_id': dish_id, 'name': 'Unknown Dish', 'price': 0.0, 'description': 'No details available'}
    return render_template('dish_details.html', dish=dish)


@app.route('/reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'POST':
        guest_name = request.form.get('guest_name', '').strip()
        party_size_str = request.form.get('party_size', '1').strip()
        reservation_date = request.form.get('reservation_date', '').strip()

        try:
            party_size = int(party_size_str)
        except ValueError:
            party_size = 1

        # Validate party size
        if party_size < 1 or party_size > 10:
            party_size = 1

        # Validate date format YYYY-MM-DD
        try:
            datetime.strptime(reservation_date, '%Y-%m-%d')
        except ValueError:
            reservation_date = ''

        if guest_name and reservation_date:
            # Load existing reservations
            reservations = load_reservations()
            # Determine new reservation_id
            max_id = max((r['reservation_id'] for r in reservations), default=0)
            new_id = max_id + 1

            # Get user info
            user_info = users_db.get(CURRENT_USERNAME, {})
            phone = user_info.get('phone', '')
            email = user_info.get('email', '')

            # Default reservation time for this spec: hardcoded to 19:00
            reservation_time = '19:00'

            new_reservation = {
                'reservation_id': new_id,
                'username': CURRENT_USERNAME,
                'guest_name': guest_name,
                'phone': phone,
                'email': email,
                'party_size': party_size,
                'date': reservation_date,
                'time': reservation_time,
                'special_requests': '',
                'status': 'Upcoming'
            }
            reservations.append(new_reservation)
            save_reservations(reservations)
            return redirect(url_for('my_reservations'))

    # GET method or invalid POST
    return render_template('reservation.html')


@app.route('/my-reservations')
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


@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    changed = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == CURRENT_USERNAME and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            changed = True
            break
    if changed:
        save_reservations(reservations)
    return redirect(url_for('my_reservations'))


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    waitlist_entries = load_waitlist()

    # Filter active waitlist entries for the current user
    user_active_entries = [w for w in waitlist_entries if w['username'] == CURRENT_USERNAME and w['status'] == 'Active']

    if request.method == 'POST':
        party_size_str = request.form.get('party_size', '').strip()
        try:
            party_size = int(party_size_str)
            if party_size < 1:
                party_size = 1
        except ValueError:
            party_size = 1

        # If user already has an active waitlist entry, do not add another
        if not user_active_entries:
            max_id = max((w['waitlist_id'] for w in waitlist_entries), default=0)
            new_id = max_id + 1
            join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_entry = {
                'waitlist_id': new_id,
                'username': CURRENT_USERNAME,
                'party_size': party_size,
                'join_time': join_time,
                'status': 'Active'
            }
            waitlist_entries.append(new_entry)
            save_waitlist(waitlist_entries)

        return redirect(url_for('waitlist'))

    # GET method
    # Calculate position if user is in the waitlist
    active_waitlist_ordered = [w for w in waitlist_entries if w['status'] == 'Active']
    active_waitlist_ordered.sort(key=lambda x: x['join_time'])

    user_position = None
    for idx, entry in enumerate(active_waitlist_ordered, start=1):
        if entry['username'] == CURRENT_USERNAME:
            user_position = idx
            break

    return render_template('waitlist.html', user_position=user_position)


@app.route('/my-reviews')
def my_reviews():
    reviews_all = load_reviews()
    menu_all = load_menu()

    dish_id_to_name = {d['dish_id']: d['name'] for d in menu_all}

    user_reviews = []
    for rev in reviews_all:
        if rev['username'] == CURRENT_USERNAME:
            dish_name = dish_id_to_name.get(rev['dish_id'], 'Unknown Dish')
            user_reviews.append({
                'review_id': rev['review_id'],
                'dish_name': dish_name,
                'rating': rev['rating'],
                'review_text': rev['review_text']
            })

    return render_template('my_reviews.html', reviews=user_reviews)


@app.route('/write-review', methods=['GET', 'POST'])
def write_review():
    if request.method == 'POST':
        dish_id_str = request.form.get('dish_id', '').strip()
        rating_str = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()

        try:
            dish_id = int(dish_id_str)
        except ValueError:
            dish_id = None
        try:
            rating = int(rating_str)
        except ValueError:
            rating = None

        if dish_id is not None and rating is not None and 1 <= rating <= 5 and review_text:
            reviews_all = load_reviews()
            max_id = max((r['review_id'] for r in reviews_all), default=0)
            new_id = max_id + 1
            review_date = datetime.now().strftime('%Y-%m-%d')

            new_review = {
                'review_id': new_id,
                'username': CURRENT_USERNAME,
                'dish_id': dish_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }

            reviews_all.append(new_review)
            save_reviews(reviews_all)

            return redirect(url_for('my_reviews'))

    # GET fallback or invalid POST
    menu_all = load_menu()
    dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu_all]
    return render_template('write_review.html', dishes=dishes)


@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    user_info = users_db.get(CURRENT_USERNAME, {'username': CURRENT_USERNAME, 'email': ''})

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if email:
            # Update email for user
            users_db[CURRENT_USERNAME]['email'] = email
            # Save changes to users.txt file
            try:
                with open(os.path.join(DATA_DIR, 'users.txt'), 'w', encoding='utf-8') as f:
                    for u in users_db.values():
                        line = '|'.join([
                            u['username'],
                            u['email'],
                            u['phone'],
                            u['full_name']
                        ])
                        f.write(line + '\n')
            except Exception:
                pass
            user_info = users_db[CURRENT_USERNAME]

    return render_template('profile.html', user_info=user_info)


if __name__ == '__main__':
    app.run(debug=True)
