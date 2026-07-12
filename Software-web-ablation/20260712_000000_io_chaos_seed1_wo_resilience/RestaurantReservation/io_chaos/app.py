import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
DATA_DIR = 'data'
CURRENT_USERNAME = 'john_diner'

# Helper functions to load data from files

def load_users():
    users = {}
    try:
        with open(os.path.join(DATA_DIR, 'users.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 4:
                    continue
                users[parts[0]] = {
                    'username': parts[0],
                    'email': parts[1],
                    'phone': parts[2],
                    'full_name': parts[3]
                }
    except FileNotFoundError:
        pass
    return users


def load_menu():
    menus = []
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 7:
                    continue
                dish = {
                    'dish_id': int(parts[0]),
                    'name': parts[1],
                    'category': parts[2],
                    'price': float(parts[3]),
                    'description': parts[4],
                    'ingredients': parts[5],
                    'dietary': parts[6]
                }
                menus.append(dish)
    except FileNotFoundError:
        pass
    return menus


def load_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 6:
                    continue
                review = {
                    'review_id': int(parts[0]),
                    'username': parts[1],
                    'dish_id': int(parts[2]),
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews.append(review)
    except FileNotFoundError:
        pass
    return reviews


def load_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 9:
                    continue
                reservation = {
                    'reservation_id': int(parts[0]),
                    'username': parts[1],
                    'guest_name': parts[2],
                    'phone': parts[3],
                    'email': parts[4],
                    'party_size': int(parts[5]),
                    'date': parts[6],
                    'time': parts[7],
                    'special_requests': parts[8],
                    'status': parts[9] if len(parts) > 9 else 'Upcoming'
                }
                reservations.append(reservation)
    except FileNotFoundError:
        pass
    return reservations


def load_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) < 5:
                    continue
                waitlist.append({
                    'waitlist_id': int(parts[0]),
                    'username': parts[1],
                    'party_size': int(parts[2]),
                    'join_time': parts[3],
                    'status': parts[4]
                })
    except FileNotFoundError:
        pass
    return waitlist


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    menus = load_menu()
    users = load_users()
    reservations = load_reservations()
    waitlist = load_waitlist()

    # Filter reservations for current user
    my_reservations = [r for r in reservations if r['username'] == CURRENT_USERNAME]
    upcoming_reservations = [r for r in my_reservations if r['status'] == 'Upcoming']

    # Prepare featured dishes (example: first 3 dishes)
    featured_dishes = menus[:3]

    return render_template('dashboard.html',
                           menus=menus,
                           featured_dishes=featured_dishes,
                           upcoming_reservations=upcoming_reservations,
                           my_reservations=my_reservations,
                           current_username=CURRENT_USERNAME)


@app.route('/menu')
def menu():
    menus = load_menu()
    return render_template('menu.html', menus=menus)


@app.route('/dish/<int:dish_id>')
def dish_detail(dish_id):
    menus = load_menu()
    dish = next((d for d in menus if d['dish_id'] == dish_id), None)
    if dish is None:
        return "Dish not found.", 404

    reviews = load_reviews()
    dish_reviews = [r for r in reviews if r['dish_id'] == dish_id]

    # Prepare dish name mapping for reviews display
    dish_name = dish['name']

    return render_template('dish_detail.html', dish=dish, reviews=dish_reviews, dish_name=dish_name)


@app.route('/my_reviews')
def my_reviews():
    reviews = load_reviews()
    my_reviews = [r for r in reviews if r['username'] == CURRENT_USERNAME]

    menus = load_menu()
    dish_id_to_name = {d['dish_id']: d['name'] for d in menus}

    # Prepare reviews list with dish names
    reviews_list = []
    for r in my_reviews:
        reviews_list.append({
            'review_id': r['review_id'],
            'dish_name': dish_id_to_name.get(r['dish_id'], 'Unknown'),
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    return render_template('my_reviews.html', reviews=reviews_list)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    if request.method == 'POST':
        dish_id = request.form.get('dish_id')
        rating = request.form.get('rating')
        review_text = request.form.get('review_text')

        if not dish_id or not rating or not review_text:
            flash('All fields are required.')
            return redirect(url_for('menu'))

        dish_id = int(dish_id)
        rating = int(rating)

        reviews = load_reviews()
        max_id = max([r['review_id'] for r in reviews], default=0) + 1

        new_review = {
            'review_id': max_id,
            'username': CURRENT_USERNAME,
            'dish_id': dish_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': datetime.now().strftime('%m-%d-%Y')
        }

        reviews.append(new_review)

        # Save reviews back to file
        try:
            with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w') as f:
                for r in reviews:
                    f.write(f"{r['review_id']},{r['username']},{r['dish_id']},{r['rating']},{r['review_text']},{r['review_date']}\n")
        except Exception as e:
            flash(f"Failed to save review: {str(e)}")
            return redirect(url_for('menu'))

        return redirect(url_for('my_reviews'))

    menus = load_menu()
    return render_template('write_review.html', menus=menus)


@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'POST':
        guest_name = request.form.get('guest_name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        party_size = request.form.get('party_size')
        reservation_date = request.form.get('reservation_date')
        reservation_time = request.form.get('reservation_time')
        special_requests = request.form.get('special_requests', '')

        if not guest_name or not phone or not email or not party_size or not reservation_date or not reservation_time:
            flash('Please fill in all required fields.')
            return redirect(url_for('make_reservation'))

        party_size = int(party_size)

        reservations = load_reservations()
        max_id = max([r['reservation_id'] for r in reservations], default=0) + 1

        new_reservation = {
            'reservation_id': max_id,
            'username': CURRENT_USERNAME,
            'guest_name': guest_name,
            'phone': phone,
            'email': email,
            'party_size': party_size,
            'date': reservation_date,
            'time': reservation_time,
            'special_requests': special_requests,
            'status': 'Upcoming'
        }

        reservations.append(new_reservation)

        # Save reservations back to file
        try:
            with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w') as f:
                for r in reservations:
                    f.write(f"{r['reservation_id']},{r['username']},{r['guest_name']},{r['phone']},{r['email']},{r['party_size']},{r['date']},{r['time']},{r['special_requests']},{r['status']}\n")
        except Exception as e:
            flash(f"Failed to save reservation: {str(e)}")
            return redirect(url_for('make_reservation'))

        return redirect(url_for('dashboard'))

    return render_template('make_reservation.html')


@app.route('/my_reservations')
def my_reservations():
    reservations = load_reservations()
    my_res = [r for r in reservations if r['username'] == CURRENT_USERNAME]
    return render_template('my_reservations.html', reservations=my_res)


@app.route('/cancel_reservation/<int:reservation_id>')
def cancel_reservation(reservation_id):
    reservations = load_reservations()
    updated_reservations = []
    found = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == CURRENT_USERNAME:
            r['status'] = 'Cancelled'
            found = True
        updated_reservations.append(r)

    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w') as f:
            for r in updated_reservations:
                f.write(f"{r['reservation_id']},{r['username']},{r['guest_name']},{r['phone']},{r['email']},{r['party_size']},{r['date']},{r['time']},{r['special_requests']},{r['status']}\n")
    except Exception as e:
        flash(f"Failed to update reservation: {str(e)}")
        return redirect(url_for('my_reservations'))

    if not found:
        flash('Reservation not found or not authorized.')

    return redirect(url_for('my_reservations'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = load_users()
    user = users.get(CURRENT_USERNAME, {'username': CURRENT_USERNAME, 'email': '', 'phone': '', 'full_name': ''})

    if request.method == 'POST':
        new_email = request.form.get('email')
        new_phone = request.form.get('phone')
        new_full_name = request.form.get('full_name')

        if not new_email or not new_phone or not new_full_name:
            flash('All profile fields are required.')
            return redirect(url_for('profile'))

        # Update user info
        users[CURRENT_USERNAME] = {
            'username': CURRENT_USERNAME,
            'email': new_email,
            'phone': new_phone,
            'full_name': new_full_name
        }

        # Save back to file
        try:
            with open(os.path.join(DATA_DIR, 'users.txt'), 'w') as f:
                for u in users.values():
                    f.write(f"{u['username']},{u['email']},{u['phone']},{u['full_name']}\n")
        except Exception as e:
            flash(f"Failed to update profile: {str(e)}")
            return redirect(url_for('profile'))

        flash('Profile updated successfully.')
        return redirect(url_for('dashboard'))

    return render_template('profile.html', user=user)


@app.route('/waitlist')
def wait_list():
    waitlist = load_waitlist()
    active_waitlist = [w for w in waitlist if w['status'] == 'Active']
    # Sort by join_time ascending
    active_waitlist.sort(key=lambda x: datetime.strptime(x['join_time'], '%H:%M:%S'))
    return render_template('waitlist.html', waitlist=active_waitlist)


if __name__ == '__main__':
    app.run(debug=True)
