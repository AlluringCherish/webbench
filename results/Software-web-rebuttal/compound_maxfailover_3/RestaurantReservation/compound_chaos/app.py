from flask import Flask, render_template, redirect, request, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

def read_users():
    users = []
    try:
        with open('data/users.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    users.append({
                        'username': parts[0],
                        'phone': parts[1],
                        'email': parts[2],
                        'full_name': parts[3]
                    })
    except FileNotFoundError:
        pass
    return users

def read_menu():
    menu = []
    try:
        with open('data/menu.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        menu.append({
                            'dish_id': int(parts[0]),
                            'name': parts[1],
                            'category': parts[2],
                            'price': float(parts[3]),
                            'description': parts[4],
                            'ingredients': parts[5],
                            'dietary': parts[6],
                            'avg_rating': float(parts[7])
                        })
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return menu

def read_reservations():
    reservations = []
    try:
        with open('data/reservations.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    try:
                        reservations.append({
                            'reservation_id': int(parts[0]),
                            'username': parts[1],
                            'guest_name': parts[2],
                            'phone': parts[3],
                            'email': parts[4],
                            'party_size': int(parts[5]),
                            'date': parts[6],
                            'time': parts[7],
                            'special_requests': parts[8],
                            'status': parts[9]
                        })
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return reservations

def save_reservations(reservations):
    try:
        with open('data/reservations.txt', 'w') as f:
            for r in reservations:
                line = "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                    r['reservation_id'], r['username'], r['guest_name'], r['phone'], r['email'],
                    r['party_size'], r['date'], r['time'], r['special_requests'], r['status'])
                f.write(line)
    except Exception:
        pass

def read_waitlist():
    waitlist = []
    try:
        with open('data/waitlist.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    try:
                        waitlist.append({
                            'waitlist_id': int(parts[0]),
                            'username': parts[1],
                            'party_size': int(parts[2]),
                            'join_time': parts[3],
                            'status': parts[4]
                        })
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return waitlist

def save_waitlist(waitlist):
    try:
        with open('data/waitlist.txt', 'w') as f:
            for w in waitlist:
                line = "{}|{}|{}|{}|{}\n".format(w['waitlist_id'], w['username'], w['party_size'], w['join_time'], w['status'])
                f.write(line)
    except Exception:
        pass

def read_reviews():
    reviews = []
    try:
        with open('data/reviews.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    try:
                        reviews.append({
                            'review_id': int(parts[0]),
                            'username': parts[1],
                            'dish_id': int(parts[2]),
                            'rating': int(parts[3]),
                            'review_text': parts[4],
                            'review_date': parts[5]
                        })
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return reviews

def save_reviews(reviews):
    try:
        with open('data/reviews.txt', 'w') as f:
            for r in reviews:
                line = "{}|{}|{}|{}|{}|{}\n".format(
                    r['review_id'], r['username'], r['dish_id'], r['rating'], r['review_text'], r['review_date'])
                f.write(line)
    except Exception:
        pass

def read_user(username):
    users = read_users()
    for user in users:
        if user['username'] == username:
            return user
    return None

def get_next_reservation_id():
    reservations = read_reservations()
    if not reservations:
        return 1
    return max(r['reservation_id'] for r in reservations) + 1

def get_next_waitlist_id():
    waitlist = read_waitlist()
    if not waitlist:
        return 1
    return max(w['waitlist_id'] for w in waitlist) + 1

def get_next_review_id():
    reviews = read_reviews()
    if not reviews:
        return 1
    return max(r['review_id'] for r in reviews) + 1

def get_current_username():
    # Placeholder for authentication
    users = read_users()
    if users:
        return users[0]['username']
    return 'guest'

def get_current_user():
    username = get_current_username()
    return read_user(username)

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    username = get_current_username()
    menu = read_menu()
    featured_dishes = []
    for dish in menu[:3]:
        featured_dishes.append({
            'dish_id': dish['dish_id'],
            'name': dish['name'],
            'price': dish['price'],
            'description': dish['description']
        })
    reservations = read_reservations()
    upcoming_reservations = []
    today = datetime.now().strftime('%Y-%m-%d')
    for r in reservations:
        if r['username'] == username and r['status'] != 'Completed' and r['date'] >= today:
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
    menus = read_menu()
    return render_template('menu.html', menus=menus)

@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu = read_menu()
    dish_found = None
    for dish in menu:
        if dish['dish_id'] == dish_id:
            dish_found = dish
            break
    if dish_found is None:
        return "Dish not found", 404
    return render_template('dish_details.html', dish=dish_found)

@app.route('/make-reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'GET':
        return render_template('make_reservation.html')
    errors = []
    guest_name = request.form.get('guest_name', '').strip()
    party_size_str = request.form.get('party_size', '').strip()
    reservation_date = request.form.get('reservation_date', '').strip()

    if not guest_name:
        errors.append('Guest name is required.')
    try:
        party_size = int(party_size_str)
        if party_size < 1 or party_size > 10:
            errors.append('Party size must be between 1 and 10.')
    except ValueError:
        errors.append('Party size must be a number.')
    try:
        datetime.strptime(reservation_date, '%Y-%m-%d')
    except ValueError:
        errors.append('Reservation date must be in YYYY-MM-DD format.')

    if errors:
        return render_template('make_reservation.html', error_message=' '.join(errors))

    user = get_current_user()
    phone = user['phone'] if user and 'phone' in user else ''
    email = user['email'] if user and 'email' in user else ''

    reservations = read_reservations()
    new_reservation_id = get_next_reservation_id()
    reservation_time = "19:00"

    new_reservation = {
        'reservation_id': new_reservation_id,
        'username': get_current_username(),
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

    return redirect(url_for('dashboard'))

@app.route('/my-reservations')
def my_reservations():
    username = get_current_username()
    reservations = read_reservations()
    user_reservations = []
    for r in reservations:
        if r['username'] == username:
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
    username = get_current_username()
    reservations = read_reservations()
    changed = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == username and r['status'] != 'Cancelled':
            r['status'] = 'Cancelled'
            changed = True
            break
    if changed:
        save_reservations(reservations)
    return redirect(url_for('my_reservations'))

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist_view():
    username = get_current_username()
    waitlist = read_waitlist()
    user_entry = None
    if request.method == 'GET':
        for e in waitlist:
            if e['username'] == username and e['status'] == 'Active':
                user_entry = e
                break
        user_position = None
        if user_entry:
            active_entries = [x for x in waitlist if x['status'] == 'Active']
            active_entries.sort(key=lambda x: x['join_time'])
            for idx, e in enumerate(active_entries):
                if e['username'] == username:
                    user_position = idx + 1
                    break
        return render_template('waitlist.html', user_position=user_position)
    elif request.method == 'POST':
        party_size_str = request.form.get('party_size', '').strip()
        try:
            party_size = int(party_size_str)
            if party_size < 1:
                return render_template('waitlist.html', user_position=None, error_message='Party size must be at least 1.')
        except ValueError:
            return render_template('waitlist.html', user_position=None, error_message='Party size must be a number.')
        for e in waitlist:
            if e['username'] == username and e['status'] == 'Active':
                return render_template('waitlist.html', user_position=None, error_message='You already have an active waitlist entry.')
        new_waitlist_id = get_next_waitlist_id()
        join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = {
            'waitlist_id': new_waitlist_id,
            'username': username,
            'party_size': party_size,
            'join_time': join_time,
            'status': 'Active'
        }
        waitlist.append(new_entry)
        save_waitlist(waitlist)
        active_entries = [x for x in waitlist if x['status'] == 'Active']
        active_entries.sort(key=lambda x: x['join_time'])
        user_position = None
        for idx, e in enumerate(active_entries):
            if e['username'] == username:
                user_position = idx + 1
                break
        return render_template('waitlist.html', user_position=user_position)

@app.route('/my-reviews')
def my_reviews():
    username = get_current_username()
    reviews = read_reviews()
    menu = read_menu()
    dish_id_to_name = {d['dish_id']: d['name'] for d in menu}
    user_reviews = []
    for r in reviews:
        if r['username'] == username:
            dish_name = dish_id_to_name.get(r['dish_id'], 'Dish')
            user_reviews.append({
                'review_id': r['review_id'],
                'dish_name': dish_name,
                'rating': r['rating'],
                'review_text': r['review_text']
            })
    return render_template('my_reviews.html', reviews=user_reviews)

@app.route('/write-review', methods=['GET', 'POST'])
def write_review():
    username = get_current_username()
    menu = read_menu()
    if request.method == 'GET':
        dishes = [d for d in menu]
        return render_template('write_review.html', dishes=dishes)
    errors = []
    dish_id_str = request.form.get('dish_id', '').strip()
    rating_str = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()
    try:
        dish_id = int(dish_id_str)
        if not any(d['dish_id'] == dish_id for d in menu):
            errors.append('Selected dish is invalid.')
    except ValueError:
        errors.append('Dish must be a valid integer.')
    try:
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            errors.append('Rating must be between 1 and 5.')
    except ValueError:
        errors.append('Rating must be a valid integer.')
    if not review_text:
        errors.append('Review text cannot be empty.')
    if errors:
        dishes = [d for d in menu]
        return render_template('write_review.html', errors=errors, dishes=dishes)
    reviews = read_reviews()
    new_review_id = get_next_review_id()
    review_date = datetime.now().strftime('%Y-%m-%d')
    new_review = {
        'review_id': new_review_id,
        'username': username,
        'dish_id': dish_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date
    }
    reviews.append(new_review)
    save_reviews(reviews)
    return redirect(url_for('my_reviews'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = get_current_username()
    user = read_user(username)
    if request.method == 'POST':
        new_email = request.form.get('email', '').strip()
        if not new_email:
            return render_template('profile.html', username=username, email=user['email'], error_message='Email cannot be empty.')
        users = read_users()
        updated = False
        for u in users:
            if u['username'] == username:
                u['email'] = new_email
                updated = True
                break
        if updated:
            try:
                with open('data/users.txt', 'w') as f:
                    for u in users:
                        line = '|'.join([u['username'], u['phone'], u['email'], u['full_name']]) + '\n'
                        f.write(line)
                return render_template('profile.html', username=username, email=new_email, success_message='Profile successfully updated.')
            except Exception:
                return render_template('profile.html', username=username, email=user['email'], error_message='Failed to save profile.')
        else:
            return render_template('profile.html', username=username, email=user['email'], error_message='User not found.')
    return render_template('profile.html', username=username, email=user['email'] if user else '')

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    app.run(debug=True)
