from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'

# Load data from files into memory for simplicity

def load_reservations():
    reservations = []
    try:
        with open(os.path.join(DATA_DIR, 'reservations.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 10:
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
                        continue  # skip lines with invalid int conversion
    except FileNotFoundError:
        flash('Reservations data file not found.')
    return reservations


def load_waitlist():
    waitlist = []
    try:
        with open(os.path.join(DATA_DIR, 'waitlist.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    try:
                        waitlist.append({
                            'waitlist_id': int(parts[0]),
                            'username': parts[1],
                            'party_size': int(parts[2]),
                            'join_time': parts[3],
                            'status': parts[4],
                            'occasion': parts[5]
                        })
                    except ValueError:
                        continue  # skip lines with invalid int conversion
    except FileNotFoundError:
        flash('Waitlist data file not found.')
    return waitlist


def load_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
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
                        continue  # skip lines with invalid int conversion
    except FileNotFoundError:
        flash('Reviews data file not found.')
    return reviews


def load_menu():
    menu = []
    try:
        with open(os.path.join(DATA_DIR, 'menu.txt'), 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 8:
                    try:
                        menu.append({
                            'dish_id': int(parts[0]),
                            'name': parts[1],
                            'category': parts[2],
                            'price': float(parts[3]),
                            'description': parts[4],
                            'ingredients': parts[5].split(','),
                            'dietary': parts[6],
                            'avg_rating': float(parts[7])
                        })
                    except ValueError:
                        continue  # skip lines with invalid conversion
    except FileNotFoundError:
        flash('Menu data file not found.')
    return menu


@app.route('/')
def dashboard():
    reservations = load_reservations()
    waitlist = load_waitlist()
    return render_template('dashboard.html', reservations=reservations, waitlist=waitlist)


@app.route('/menu')
def menu_page():
    menu = load_menu()
    return render_template('menu.html', menu=menu)


@app.route('/dish/<int:dish_id>')
def dish_details(dish_id):
    menu = load_menu()
    dish = next((d for d in menu if d['dish_id'] == dish_id), None)
    reviews = load_reviews()
    dish_reviews = [r for r in reviews if r['dish_id'] == dish_id]
    return render_template('dish_details.html', dish=dish, reviews=dish_reviews)


@app.route('/my-reservations')
def my_reservations():
    # For example, assume user john_diner for demonstration
    user = 'john_diner'
    reservations = load_reservations()
    user_reservations = [r for r in reservations if r['username'] == user]
    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/my-reviews')
def my_reviews():
    user = 'john_diner'
    reviews = load_reviews()
    user_reviews = [r for r in reviews if r['username'] == user]
    menu = load_menu()
    return render_template('my_reviews.html', reviews=user_reviews, menu=menu)


@app.route('/waitlist')
def waitlist_page():
    waitlist = load_waitlist()
    return render_template('waitlist.html', waitlist=waitlist)


@app.route('/reservation/<int:reservation_id>/cancel', methods=['POST'])
def cancel_reservation(reservation_id):
    # Load reservations
    reservations = load_reservations()
    # Find reservation
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
    if reservation:
        # Update status to canceled
        reservation['status'] = 'canceled'
        # Rewrite file
        try:
            with open(os.path.join(DATA_DIR, 'reservations.txt'), 'w') as f:
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
            flash('Reservation canceled successfully.')
        except Exception as e:
            flash(f'Error saving reservation: {e}')
    else:
        flash('Reservation not found.')
    return redirect(url_for('my_reservations'))


@app.route('/review/<int:review_id>/update', methods=['POST'])
def update_review(review_id):
    new_rating = request.form.get('rating')
    new_text = request.form.get('review_text', '')
    if new_rating is None:
        flash('Rating is required.')
        return redirect(url_for('my_reviews'))

    try:
        new_rating = int(new_rating)
        if not (1 <= new_rating <= 5):
            raise ValueError()
    except ValueError:
        flash('Invalid rating value. Must be 1 to 5.')
        return redirect(url_for('my_reviews'))

    reviews = load_reviews()
    review = next((r for r in reviews if r['review_id'] == review_id), None)
    if review:
        review['rating'] = new_rating
        review['review_text'] = new_text
        # Rewrite file
        try:
            with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w') as f:
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
            flash('Review updated successfully.')
        except Exception as e:
            flash(f'Error saving review: {e}')
    else:
        flash('Review not found.')
    return redirect(url_for('my_reviews'))


if __name__ == '__main__':
    app.run(debug=True)
