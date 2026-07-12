from flask import Flask, redirect, url_for, render_template, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

DATA_PATH = 'data'

# Load users

def load_users():
    users = []
    path = os.path.join(DATA_PATH, 'users.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    username = parts[0]
                    email = parts[1]
                    users.append({
                        'username': username,
                        'email': email
                    })
    return users

# Load menu dishes

def load_menu():
    menus = []
    path = os.path.join(DATA_PATH, 'menu.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 6:
                    dish_id = parts[0]
                    name = parts[1]
                    category = parts[2]
                    price = parts[3]
                    description = parts[4]
                    avg_rating = parts[5]
                    menus.append({
                        'dish_id': dish_id,
                        'name': name,
                        'category': category,
                        'price': price,
                        'description': description,
                        'avg_rating': avg_rating
                    })
    return menus

# Load reservations

def load_reservations():
    reservations = []
    path = os.path.join(DATA_PATH, 'reservations.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 10:
                    reservation = {
                        'reservation_id': parts[0],
                        'username': parts[1],
                        'guest_name': parts[2],
                        'phone': parts[3],
                        'email': parts[4],
                        'party_size': parts[5],
                        'date': parts[6],
                        'time': parts[7],
                        'special_requests': parts[8],
                        'status': parts[9]
                    }
                    reservations.append(reservation)
    return reservations

# Load waitlist

def load_waitlist():
    waitlist = []
    path = os.path.join(DATA_PATH, 'waitlist.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    waitlist.append({
                        'waitlist_id': parts[0],
                        'username': parts[1],
                        'party_size': parts[2],
                        'join_time': parts[3],
                        'status': parts[4]
                    })
    return waitlist

# Load reviews

def load_reviews():
    reviews = []
    path = os.path.join(DATA_PATH, 'reviews.txt')
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 6:
                    reviews.append({
                        'review_id': parts[0],
                        'username': parts[1],
                        'dish_id': parts[2],
                        'rating': parts[3],
                        'review_text': parts[4],
                        'review_date': parts[5]
                    })
    return reviews

@app.route('/', methods=['GET', 'POST'])
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Get username from form or default to first user
    username = request.form.get('username')
    if not username:
        users = load_users()
        if users:
            username = users[0]['username']
        else:
            username = None

    # Load menu
    menu = load_menu()

    # Sort featured dishes by avg_rating descending
    def avg_rating_float(d):
        try:
            return float(d['avg_rating'])
        except:
            return 0.0

    featured_sorted = sorted(menu, key=avg_rating_float, reverse=True)[:3]
    featured_dishes = featured_sorted

    # Load reservations for user
    reservations = load_reservations()
    upcoming_reservations = []
    for r in reservations:
        if r['username'] == username and r['status'].lower() == 'upcoming':
            # Convert date string YYYY-MM-DD to int YYYYMMDD
            try:
                dt = datetime.datetime.strptime(r['date'], '%Y-%m-%d')
                date_int = int(dt.strftime('%Y%m%d'))
            except:
                date_int = 0

            # Convert time string HH:MM to int HHMM
            try:
                time_int = int(r['time'].replace(':', ''))
            except:
                time_int = 0

            upcoming_reservations.append({
                'reservation_id': r['reservation_id'],
                'date': date_int,
                'time': time_int,
                'party_size': r['party_size'],
                'status': r['status']
            })

    return render_template('dashboard.html', featured_dishes=featured_dishes, reservations=upcoming_reservations)

@app.route('/menu')
def menuPage():
    menus = load_menu()
    return render_template('menu.html', menus=menus)

@app.route('/dish/<int:dish_id>')
def dish_detail(dish_id):
    menu = load_menu()
    dish = None
    for m in menu:
        if int(m['dish_id']) == dish_id:
            dish = {
                'dish_id': m['dish_id'],
                'name': m['name'],
                'price': m['price'],
                'description': m['description']
            }
            break
    if dish is None:
        dish = {
            'dish_id': str(dish_id),
            'name': '',
            'price': '',
            'description': ''
        }
    return render_template('dish_detail.html', dish=dish)

@app.route('/make-reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'GET':
        return render_template('make_reservation.html')

    guestname = request.form.get('guestname')
    party_size = request.form.get('party_size')
    reservation_date = request.form.get('reservation_date')

    if not guestname or not party_size or not reservation_date:
        return render_template('make_reservation.html', error='Please fill in all required fields.')

    reservations = load_reservations()

    max_id = 0
    for r in reservations:
        try:
            cur_id = int(r['reservation_id'])
            if cur_id > max_id:
                max_id = cur_id
        except:
            continue
    new_id = str(max_id + 1)

    new_reservation = {
        'reservation_id': new_id,
        'username': guestname,  # placeholder for no auth
        'guest_name': guestname,
        'phone': '',
        'email': '',
        'party_size': party_size,
        'date': reservation_date,
        'time': '19:00',
        'special_requests': '',
        'status': 'Upcoming'
    }

    path = os.path.join(DATA_PATH, 'reservations.txt')
    with open(path, 'a') as f:
        line = ','.join([
            new_reservation['reservation_id'],
            new_reservation['username'],
            new_reservation['guest_name'],
            new_reservation['phone'],
            new_reservation['email'],
            new_reservation['party_size'],
            new_reservation['date'],
            new_reservation['time'],
            new_reservation['special_requests'],
            new_reservation['status']
        ]) + '\n'
        f.write(line)

    return redirect(url_for('dashboard'))

@app.route('/my-reservations')
def my_reservations():
    users = load_users()
    username = None
    if users:
        username = users[0]['username']

    reservations = load_reservations()
    user_reservations = []
    for r in reservations:
        if r['username'] == username:
            try:
                dt = datetime.datetime.strptime(r['date'], '%Y-%m-%d')
                date_int = int(dt.strftime('%Y%m%d'))
            except:
                date_int = 0
            try:
                time_int = int(r['time'].replace(':', ''))
            except:
                time_int = 0

            status_num = 0 if r['status'].lower() == 'upcoming' else 1
            user_reservations.append({
                'reservation_id': r['reservation_id'],
                'date': date_int,
                'time': time_int,
                'party_size': r['party_size'],
                'status': status_num
            })

    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/cancel-reservation/<int:reservation_id>', methods=['GET'])
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    for r in reservations:
        if int(r['reservation_id']) == reservation_id:
            r['status'] = 'Canceled'
            break

    path = os.path.join(DATA_PATH, 'reservations.txt')
    with open(path, 'w') as f:
        for r in reservations:
            line = ','.join([
                r['reservation_id'],
                r['username'],
                r['guest_name'],
                r['phone'],
                r['email'],
                r['party_size'],
                r['date'],
                r['time'],
                r['special_requests'],
                r['status']
            ]) + '\n'
            f.write(line)

    return redirect(url_for('dashboard'))

@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist_page():
    users = load_users()
    username = None
    if users:
        username = users[0]['username']

    waitlist = load_waitlist()
    user_waitlist_entry = None
    active_waitlist = [w for w in waitlist if w['status'].lower() == 'active']

    if request.method == 'POST':
        username_form = request.form.get('username')
        party_size_form = request.form.get('party_size')

        # Remove from waitlist?
        remove_id = request.form.get('remove_id')

        if remove_id:
            waitlist = [w for w in waitlist if w['waitlist_id'] != remove_id]
        else:
            if username_form and party_size_form:
                max_id = 0
                for w in waitlist:
                    try:
                        cur_id = int(w['waitlist_id'])
                        if cur_id > max_id:
                            max_id = cur_id
                    except:
                        continue
                new_id = str(max_id + 1)
                now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_entry = {
                    'waitlist_id': new_id,
                    'username': username_form,
                    'party_size': party_size_form,
                    'join_time': now_str,
                    'status': 'Active'
                }
                waitlist.append(new_entry)

        path = os.path.join(DATA_PATH, 'waitlist.txt')
        with open(path, 'w') as f:
            for w in waitlist:
                line = '|'.join([
                    w['waitlist_id'],
                    w['username'],
                    w['party_size'],
                    w['join_time'],
                    w['status']
                ]) + '\n'
                f.write(line)

    # Show user waitlist entry (if any)
    for w in waitlist:
        if w['username'] == username and w['status'].lower() == 'active':
            user_waitlist_entry = w
            break

    return render_template('waitlist.html', waitlist=active_waitlist, user_waitlist_entry=user_waitlist_entry)

@app.route('/my-reviews', methods=['GET'])
def my_reviews():
    users = load_users()
    username = None
    if users:
        username = users[0]['username']

    reviews = load_reviews()
    menu = load_menu()
    user_reviews = []
    for r in reviews:
        if r['username'] == username:
            dish_name = ''
            for m in menu:
                if m['dish_id'] == r['dish_id']:
                    dish_name = m['name']
                    break
            try:
                review_date_int = int(datetime.datetime.strptime(r['review_date'], '%Y-%m-%d').strftime('%Y%m%d'))
            except:
                review_date_int = 0

            user_reviews.append({
                'review_id': r['review_id'],
                'dish_name': dish_name,
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': review_date_int
            })

    return render_template('my_reviews.html', reviews=user_reviews)

@app.route('/write-review', methods=['GET', 'POST'])
def write_review():
    menu = load_menu()
    dishes = []
    for m in menu:
        dishes.append({
            'dish_id': m['dish_id'],
            'name': m['name']
        })

    if request.method == 'GET':
        return render_template('write_review.html', dishes=dishes)

    dish_id = request.form.get('dish_id')
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')

    if not dish_id or not rating or not review_text:
        return render_template('write_review.html', dishes=dishes, error='Please fill in all fields.')

    reviews = load_reviews()
    max_id = 0
    for r in reviews:
        try:
            cur_id = int(r['review_id'])
            if cur_id > max_id:
                max_id = cur_id
        except:
            continue
    new_id = str(max_id + 1)

    users = load_users()
    username = None
    if users:
        username = users[0]['username']

    new_review = {
        'review_id': new_id,
        'username': username,
        'dish_id': dish_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': datetime.datetime.now().strftime('%Y-%m-%d')
    }

    path = os.path.join(DATA_PATH, 'reviews.txt')
    with open(path, 'a') as f:
        line = ','.join([
            new_review['review_id'],
            new_review['username'],
            new_review['dish_id'],
            new_review['rating'],
            new_review['review_text'],
            new_review['review_date']
        ]) + '\n'
        f.write(line)

    return redirect(url_for('my_reviews'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = load_users()
    user_profile = None
    if users:
        user_profile = {'username': users[0]['username'], 'email': users[0]['email']}

    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')

        # Update users file
        updated = False
        path = os.path.join(DATA_PATH, 'users.txt')
        all_users = []
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        user_name = parts[0]
                        user_email = parts[1]
                        user_phone = parts[2] if len(parts) > 2 else ''
                        if user_name == username:
                            user_email = email
                            user_phone = phone
                            updated = True
                        all_users.append([user_name, user_email, user_phone])

        if updated:
            with open(path, 'w') as f:
                for u in all_users:
                    line = ','.join(u) + '\n'
                    f.write(line)

        user_profile = {'username': username, 'email': email}

    return render_template('profile.html', user_profile=user_profile)

if __name__ == '__main__':
    app.run(debug=True)
