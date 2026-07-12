from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'
CURRENT_USER = 'john_diner'

# Helper functions

def load_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
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
    return users

def save_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for user in users.values():
            line = '|'.join([user['username'], user['email'], user['phone'], user['full_name']]) + '\n'
            f.write(line)


def load_menu():
    menu = []
    path = os.path.join(DATA_DIR, 'menu.txt')
    if not os.path.exists(path):
        return menu
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 8:
                try:
                    dish_id = int(parts[0])
                    price = float(parts[3])
                    avg_rating = float(parts[7])
                except ValueError:
                    continue
                menu.append({
                    'dish_id': dish_id,
                    'name': parts[1],
                    'category': parts[2],
                    'price': price,
                    'description': parts[4],
                    'ingredients': parts[5],
                    'dietary': parts[6],
                    'avg_rating': avg_rating
                })
    return menu

def load_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 10:
                try:
                    reservation_id = int(parts[0])
                    party_size = int(parts[5])
                except ValueError:
                    continue
                reservations.append({
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
                })
    return reservations

def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            line = '|'.join([
                str(r['reservation_id']), r['username'], r['guest_name'], r['phone'], r['email'], str(r['party_size']), r['date'], r['time'], r['special_requests'], r['status']
            ]) + '\n'
            f.write(line)


def load_waitlist():
    waitlist = []
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    if not os.path.exists(path):
        return waitlist
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 5:
                try:
                    waitlist_id = int(parts[0])
                    party_size = int(parts[2])
                except ValueError:
                    continue
                waitlist.append({
                    'waitlist_id': waitlist_id,
                    'username': parts[1],
                    'party_size': party_size,
                    'join_time': parts[3],
                    'status': parts[4]
                })
    return waitlist

def save_waitlist(waitlist):
    path = os.path.join(DATA_DIR, 'waitlist.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for w in waitlist:
            line = '|'.join([str(w['waitlist_id']), w['username'], str(w['party_size']), w['join_time'], w['status']]) + '\n'
            f.write(line)


def load_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 6:
                try:
                    review_id = int(parts[0])
                    dish_id = int(parts[2])
                    rating = int(parts[3])
                except ValueError:
                    continue
                reviews.append({
                    'review_id': review_id,
                    'username': parts[1],
                    'dish_id': dish_id,
                    'rating': rating,
                    'review_text': parts[4],
                    'review_date': parts[5]
                })
    return reviews

def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = '|'.join([str(r['review_id']), r['username'], str(r['dish_id']), str(r['rating']), r['review_text'], r['review_date']]) + '\n'
            f.write(line)


# Flask routes

@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = CURRENT_USER
    menu = load_menu()
    featured = sorted(menu, key=lambda d: d['avg_rating'], reverse=True)[:3]
    featured_dishes = [{'dish_id': d['dish_id'], 'name': d['name'], 'price': d['price']} for d in featured]

    reservations = load_reservations()
    upcoming_reservations = [r for r in reservations if r['username'] == username and r['status'] == 'Upcoming']

    def datetime_sort_key(r):
        try:
            return datetime.strptime(r['date'] + ' ' + r['time'], '%Y-%m-%d %H:%M')
        except Exception:
            return datetime.max

    upcoming_reservations = sorted(upcoming_reservations, key=datetime_sort_key)
    upcoming_reservations = [{
        'reservation_id': r['reservation_id'],
        'date': r['date'],
        'time': r['time'],
        'party_size': r['party_size'],
        'status': r['status']
    } for r in upcoming_reservations]

    return render_template('dashboard.html', username=username, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)


@app.route('/menu')
def menu():
    menu_items = load_menu()
    menu_categories = sorted(set(d['category'] for d in menu_items))
    menu_items_simple = [{
        'dish_id': d['dish_id'],
        'name': d['name'],
        'category': d['category'],
        'price': d['price'],
        'description': d['description']
    } for d in menu_items]
    return render_template('menu.html', menu_categories=menu_categories, menu_items=menu_items_simple)


@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu_items = load_menu()
    dish = None
    for d in menu_items:
        if d['dish_id'] == dish_id:
            dish = {
                'dish_id': d['dish_id'],
                'name': d['name'],
                'price': d['price'],
                'description': d['description']
            }
            break
    if dish is None:
        return redirect(url_for('menu'))
    return render_template('dish_details.html', dish=dish)


@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'POST':
        guest_name = request.form.get('guest_name', '').strip()
        party_size_str = request.form.get('party_size', '').strip()
        reservation_date = request.form.get('reservation_date', '').strip()

        try:
            party_size = int(party_size_str)
            if party_size < 1 or party_size > 10:
                party_size = None
        except Exception:
            party_size = None

        if not guest_name or not reservation_date or party_size is None:
            return render_template('make_reservation.html')

        users = load_users()
        user = users.get(CURRENT_USER)
        if not user:
            return render_template('make_reservation.html')

        reservations = load_reservations()
        max_id = max([r['reservation_id'] for r in reservations], default=0)
        new_id = max_id + 1

        new_reservation = {
            'reservation_id': new_id,
            'username': CURRENT_USER,
            'guest_name': guest_name,
            'phone': user['phone'],
            'email': user['email'],
            'party_size': party_size,
            'date': reservation_date,
            'time': '19:00',
            'special_requests': '',
            'status': 'Upcoming'
        }

        reservations.append(new_reservation)
        save_reservations(reservations)
        return redirect(url_for('dashboard'))

    return render_template('make_reservation.html')


@app.route('/my_reservations', methods=['GET', 'POST'])
def my_reservations():
    username = CURRENT_USER
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == username]

    if request.method == 'POST':
        cancel_id_str = request.form.get('cancel_reservation_id', '').strip()
        try:
            cancel_id = int(cancel_id_str)
        except Exception:
            cancel_id = None

        if cancel_id is not None:
            changed = False
            for r in reservations:
                if r['reservation_id'] == cancel_id and r['username'] == username:
                    if r['status'] not in ['Cancelled', 'Completed']:
                        r['status'] = 'Cancelled'
                        changed = True
                    break
            if changed:
                save_reservations(reservations)

            reservations = load_reservations()
            user_reservations = [r for r in reservations if r['username'] == username]

    def sort_key(r):
        try:
            return datetime.strptime(r['date'] + ' ' + r['time'], '%Y-%m-%d %H:%M')
        except Exception:
            return datetime.min

    user_reservations.sort(key=sort_key, reverse=True)
    reservations_list = [{
        'reservation_id': r['reservation_id'],
        'date': r['date'],
        'time': r['time'],
        'party_size': r['party_size'],
        'status': r['status']
    } for r in user_reservations]

    return render_template('my_reservations.html', reservations=reservations_list)


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist():
    username = CURRENT_USER
    waitlist = load_waitlist()

    user_entry = None
    for w in waitlist:
        if w['username'] == username and w['status'] == 'Active':
            user_entry = w
            break

    if request.method == 'POST':
        party_size_str = request.form.get('party_size', '').strip()
        try:
            party_size = int(party_size_str)
            if party_size < 1:
                party_size = None
        except Exception:
            party_size = None

        if party_size is not None and user_entry is None:
            max_id = max([w['waitlist_id'] for w in waitlist], default=0)
            new_id = max_id + 1
            join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_waitlist = {
                'waitlist_id': new_id,
                'username': username,
                'party_size': party_size,
                'join_time': join_time,
                'status': 'Active'
            }
            waitlist.append(new_waitlist)
            save_waitlist(waitlist)
            user_entry = new_waitlist

    user_position = None
    if user_entry is not None:
        active_waitlist = [w for w in waitlist if w['status'] == 'Active']
        def join_key(w):
            try:
                return datetime.strptime(w['join_time'], '%Y-%m-%d %H:%M:%S')
            except Exception:
                return datetime.max
        active_waitlist.sort(key=join_key)
        for idx, w in enumerate(active_waitlist, start=1):
            if w['waitlist_id'] == user_entry['waitlist_id']:
                user_position = idx
                break

    return render_template('waitlist.html', user_position=user_position)


@app.route('/my_reviews')
def my_reviews():
    username = CURRENT_USER
    reviews = load_reviews()
    menu = load_menu()

    user_reviews = [r for r in reviews if r['username'] == username]
    dish_map = {d['dish_id']: d['name'] for d in menu}
    reviews_list = [{
        'review_id': r['review_id'],
        'dish_name': dish_map.get(r['dish_id'], 'Unknown Dish'),
        'rating': r['rating'],
        'review_text': r['review_text']
    } for r in user_reviews]

    return render_template('my_reviews.html', reviews=reviews_list)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    username = CURRENT_USER
    menu = load_menu()
    dishes = [{'dish_id': d['dish_id'], 'name': d['name']} for d in menu]

    if request.method == 'POST':
        dish_id_str = request.form.get('dish_id', '').strip()
        rating_str = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()

        try:
            dish_id = int(dish_id_str)
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                rating = None
        except Exception:
            dish_id = None
            rating = None

        if dish_id is None or rating is None or not review_text:
            return render_template('write_review.html', dishes=dishes)

        reviews = load_reviews()
        max_id = max([r['review_id'] for r in reviews], default=0)
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

    return render_template('write_review.html', dishes=dishes)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = CURRENT_USER
    users = load_users()
    user = users.get(username, {'username': username, 'email': '', 'phone': '', 'full_name': ''})

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if email:
            user['email'] = email
            users[username] = user
            save_users(users)

    user_info = {
        'username': user.get('username', ''),
        'email': user.get('email', '')
    }
    return render_template('profile.html', user_info=user_info)


if __name__ == '__main__':
    app.run(debug=True)
