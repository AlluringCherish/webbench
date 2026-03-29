from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Helper functions to load data

def load_users():
    users = {}
    if os.path.exists('data/users.txt'):
        with open('data/users.txt', 'r', encoding='utf-8') as f:
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


def load_menu():
    menu = []
    if os.path.exists('data/menu.txt'):
        with open('data/menu.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        dish_id = int(parts[0])
                        name = parts[1]
                        category = parts[2]
                        price = float(parts[3])
                        description = parts[4]
                        ingredients = parts[5]  # unused in routes
                        dietary = parts[6]  # unused in routes
                        avg_rating = float(parts[7])  # unused in routes
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
    if os.path.exists('data/reservations.txt'):
        with open('data/reservations.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    try:
                        reservation_id = int(parts[0])
                        username = parts[1]
                        guest_name = parts[2]
                        phone = parts[3]
                        email = parts[4]
                        party_size = int(parts[5])
                        date = parts[6]
                        time_val = parts[7]
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
                            'time': time_val,
                            'special_requests': special_requests,
                            'status': status
                        })
                    except ValueError:
                        continue
    return reservations


def save_reservations(reservations):
    with open('data/reservations.txt', 'w', encoding='utf-8') as f:
        for r in reservations:
            line = f"{r['reservation_id']}|{r['username']}|{r['guest_name']}|{r['phone']}|{r['email']}|{r['party_size']}|{r['date']}|{r['time']}|{r['special_requests']}|{r['status']}\n"
            f.write(line)


def load_waitlist():
    waitlist = []
    if os.path.exists('data/waitlist.txt'):
        with open('data/waitlist.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    try:
                        waitlist_id = int(parts[0])
                        username = parts[1]
                        party_size = int(parts[2])
                        join_time = parts[3]
                        status = parts[4]
                        waitlist.append({
                            'waitlist_id': waitlist_id,
                            'username': username,
                            'party_size': party_size,
                            'join_time': join_time,
                            'status': status
                        })
                    except ValueError:
                        continue
    return waitlist


def save_waitlist(waitlist):
    with open('data/waitlist.txt', 'w', encoding='utf-8') as f:
        for entry in waitlist:
            line = f"{entry['waitlist_id']}|{entry['username']}|{entry['party_size']}|{entry['join_time']}|{entry['status']}\n"
            f.write(line)


def load_reviews():
    reviews = []
    if os.path.exists('data/reviews.txt'):
        with open('data/reviews.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
    with open('data/reviews.txt', 'w', encoding='utf-8') as f:
        for review in reviews:
            line = f"{review['review_id']}|{review['username']}|{review['dish_id']}|{review['rating']}|{review['review_text']}|{review['review_date']}\n"
            f.write(line)


# For simplicity, assume the logged-in user is john_diner
LOGGED_IN_USERNAME = 'john_diner'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    username = LOGGED_IN_USERNAME
    menu = load_menu()
    
    # featured_dishes: top 3 dishes by avg_rating desc
    def get_featured_dishes(menu):
        sorted_menu = sorted(menu, key=lambda x: x['avg_rating'], reverse=True)
        featured = []
        for dish in sorted_menu[:3]:
            featured.append({
                'dish_id': dish['dish_id'],
                'name': dish['name'],
                'price': dish['price']
            })
        return featured

    featured_dishes = get_featured_dishes(menu)

    reservations = load_reservations()
    from datetime import date as dt_date

    # upcoming reservations for user
    upcoming_reservations = []
    for r in reservations:
        if r['username'] == username and r['status'] == 'Upcoming':
            # Only show future or today reservations
            try:
                res_date = datetime.strptime(r['date'], '%Y-%m-%d').date()
                if res_date >= dt_date.today():
                    upcoming_reservations.append({
                        'reservation_id': r['reservation_id'],
                        'date': r['date'],
                        'time': r['time'],
                        'party_size': r['party_size']
                    })
            except:
                continue

    
    return render_template('dashboard.html', username=username, featured_dishes=featured_dishes, upcoming_reservations=upcoming_reservations)


@app.route('/menu')
def menu_page():
    menu = load_menu()
    menus = []
    for dish in menu:
        menus.append({
            'dish_id': dish['dish_id'],
            'name': dish['name'],
            'category': dish['category'],
            'price': dish['price'],
            'description': dish['description']
        })
    return render_template('menu.html', menus=menus)


@app.route('/dish/<int:dish_id>')
def dish_details_page(dish_id):
    menu = load_menu()
    dish = None
    for item in menu:
        if item['dish_id'] == dish_id:
            dish = {
                'dish_id': item['dish_id'],
                'name': item['name'],
                'price': item['price'],
                'description': item['description']
            }
            break
    if dish is None:
        # Could do abort 404 but not specified, redirect to menu
        return redirect(url_for('menu_page'))
    return render_template('dish_details.html', dish=dish)


@app.route('/reservation', methods=['GET', 'POST'])
def make_reservation_page():
    if request.method == 'GET':
        return render_template('make_reservation.html')
    # POST
    # Form fields: guest_name:str, party_size:int (1-10), reservation_date:str (YYYY-MM-DD)
    guest_name = request.form.get('guest_name', '').strip()
    party_size_str = request.form.get('party_size', '')
    reservation_date = request.form.get('reservation_date', '').strip()

    # Validate party size int 1-10
    try:
        party_size = int(party_size_str)
        if party_size < 1 or party_size > 10:
            raise ValueError()
    except:
        party_size = None

    if not guest_name or not reservation_date or party_size is None:
        # Invalid input, re-render form
        return render_template('make_reservation.html')

    # Create new reservation
    reservations = load_reservations()
    new_id = 1
    if reservations:
        new_id = max(r['reservation_id'] for r in reservations) + 1

    users = load_users()
    user_info = users.get(LOGGED_IN_USERNAME, {})
    phone = user_info.get('phone', '')
    email = user_info.get('email', '')

    # Set time to 19:00 by default (not specified)
    time_val = '19:00'

    new_reservation = {
        'reservation_id': new_id,
        'username': LOGGED_IN_USERNAME,
        'guest_name': guest_name,
        'phone': phone,
        'email': email,
        'party_size': party_size,
        'date': reservation_date,
        'time': time_val,
        'special_requests': '',
        'status': 'Upcoming'
    }

    reservations.append(new_reservation)
    save_reservations(reservations)

    return redirect(url_for('my_reservations_page'))


@app.route('/my-reservations')
def my_reservations_page():
    username = LOGGED_IN_USERNAME
    reservations = load_reservations()
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
    reservations = load_reservations()
    updated = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == LOGGED_IN_USERNAME and r['status'] == 'Upcoming':
            r['status'] = 'Cancelled'
            updated = True
            break
    if updated:
        save_reservations(reservations)
    return redirect(url_for('my_reservations_page'))


@app.route('/waitlist', methods=['GET', 'POST'])
def waitlist_page():
    username = LOGGED_IN_USERNAME
    waitlist = load_waitlist()

    # Get user's active waitlist entry if any
    user_entry = None
    for entry in waitlist:
        if entry['username'] == username and entry['status'] == 'Active':
            user_entry = entry
            break

    if request.method == 'POST':
        party_size_str = request.form.get('party_size', '')
        try:
            party_size = int(party_size_str)
            if party_size < 1 or party_size > 10:
                raise ValueError()
        except:
            party_size = None

        if party_size is not None:
            if user_entry is None:
                # Add user to waitlist
                new_id = 1
                if waitlist:
                    new_id = max(e['waitlist_id'] for e in waitlist) + 1
                join_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_waitlist_entry = {
                    'waitlist_id': new_id,
                    'username': username,
                    'party_size': party_size,
                    'join_time': join_time,
                    'status': 'Active'
                }
                waitlist.append(new_waitlist_entry)

                save_waitlist(waitlist)

                user_entry = new_waitlist_entry

    # Determine user position or None
    active_waitlist = [e for e in waitlist if e['status'] == 'Active']
    active_waitlist.sort(key=lambda x: datetime.strptime(x['join_time'], '%Y-%m-%d %H:%M:%S'))

    user_position = None
    if user_entry:
        for idx, entry in enumerate(active_waitlist, start=1):
            if entry['waitlist_id'] == user_entry['waitlist_id']:
                user_position = idx
                break

    return render_template('waitlist.html', user_position=user_position)


@app.route('/my-reviews')
def my_reviews_page():
    username = LOGGED_IN_USERNAME
    reviews_all = load_reviews()
    menu = load_menu()
    dish_map = {dish['dish_id']: dish['name'] for dish in menu}

    filtered_reviews = []
    for review in reviews_all:
        if review['username'] == username:
            dish_name = dish_map.get(review['dish_id'], 'Unknown Dish')
            filtered_reviews.append({
                'review_id': review['review_id'],
                'dish_name': dish_name,
                'rating': review['rating'],
                'review_text': review['review_text']
            })

    return render_template('my_reviews.html', reviews=filtered_reviews, username=username)


@app.route('/write-review', methods=['GET', 'POST'])
def write_review_page():
    username = LOGGED_IN_USERNAME
    menu = load_menu()
    if request.method == 'GET':
        dishes = []
        for dish in menu:
            dishes.append({
                'dish_id': dish['dish_id'],
                'name': dish['name']
            })
        return render_template('write_review.html', dishes=dishes)

    # POST
    dish_id_str = request.form.get('dish_id', '')
    rating_str = request.form.get('rating', '')
    review_text = request.form.get('review_text', '').strip()

    try:
        dish_id = int(dish_id_str)
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            raise ValueError()
    except:
        return render_template('write_review.html', dishes=[{'dish_id': d['dish_id'], 'name': d['name']} for d in menu])

    if not review_text:
        return render_template('write_review.html', dishes=[{'dish_id': d['dish_id'], 'name': d['name']} for d in menu])

    reviews_all = load_reviews()
    new_id = 1
    if reviews_all:
        new_id = max(r['review_id'] for r in reviews_all) + 1

    today_str = datetime.now().strftime('%Y-%m-%d')

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

    return redirect(url_for('my_reviews_page'))


@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    users = load_users()
    user_info = users.get(LOGGED_IN_USERNAME, {'username': LOGGED_IN_USERNAME, 'email': '', 'phone': '', 'full_name': ''})
    username = user_info.get('username', LOGGED_IN_USERNAME)
    email = user_info.get('email', '')

    if request.method == 'POST':
        new_email = request.form.get('email', '').strip()
        if new_email:
            # Update in users.txt
            users[username] = {
                'username': username,
                'email': new_email,
                'phone': user_info.get('phone', ''),
                'full_name': user_info.get('full_name', '')
            }
            # Save
            with open('data/users.txt', 'w', encoding='utf-8') as f:
                for u, info in users.items():
                    line = f"{info['username']}|{info['email']}|{info['phone']}|{info['full_name']}\n"
                    f.write(line)
            email = new_email

    return render_template('profile.html', username=username, email=email)


if __name__ == '__main__':
    app.run(debug=True)
