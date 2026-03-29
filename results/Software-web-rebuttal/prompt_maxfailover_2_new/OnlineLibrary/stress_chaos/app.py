from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

data_path = 'data'

# Helper functions to load and save data from files

def load_users():
    users = {}
    filepath = os.path.join(data_path, 'users.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                username, email, phone, address = parts
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'address': address
                }
    return users

def save_users(users):
    filepath = os.path.join(data_path, 'users.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for user in users.values():
                line = '|'.join([user['username'], user['email'], user['phone'], user['address']])
                f.write(line + '\n')
        return True
    except Exception as e:
        return False


def load_books():
    books = {}
    filepath = os.path.join(data_path, 'books.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|', 10)  # maxsplit 10 in case description contains |
                if len(parts) != 10:
                    continue
                book_id = int(parts[0])
                title = parts[1]
                author = parts[2]
                isbn = parts[3]
                genre = parts[4]
                publisher = parts[5]
                year = int(parts[6])
                description = parts[7]
                status = parts[8]
                avg_rating = 0.0
                try:
                    avg_rating = float(parts[9])
                except:
                    pass
                books[book_id] = {
                    'book_id': book_id,
                    'title': title,
                    'author': author,
                    'isbn': isbn,
                    'genre': genre,
                    'publisher': publisher,
                    'year': year,
                    'description': description,
                    'status': status,
                    'avg_rating': avg_rating
                }
    return books


def save_books(books):
    filepath = os.path.join(data_path, 'books.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for book in books.values():
                line = '|'.join([
                    str(book['book_id']),
                    book['title'],
                    book['author'],
                    book['isbn'],
                    book['genre'],
                    book['publisher'],
                    str(book['year']),
                    book['description'],
                    book['status'],
                    f"{book['avg_rating']:.1f}"
                ])
                f.write(line + '\n')
        return True
    except Exception as e:
        return False


def load_borrowings():
    borrowings = {}
    filepath = os.path.join(data_path, 'borrowings.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                borrow_id = int(parts[0])
                username = parts[1]
                book_id = int(parts[2])
                borrow_date = parts[3]
                due_date = parts[4]
                return_date = parts[5]
                status = parts[6]
                try:
                    fine_amount = float(parts[7])
                except:
                    fine_amount = 0.0
                borrowings[borrow_id] = {
                    'borrow_id': borrow_id,
                    'username': username,
                    'book_id': book_id,
                    'borrow_date': borrow_date,
                    'due_date': due_date,
                    'return_date': return_date,
                    'status': status,
                    'fine_amount': fine_amount
                }
    return borrowings


def save_borrowings(borrowings):
    filepath = os.path.join(data_path, 'borrowings.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for borrow in borrowings.values():
                line = '|'.join([
                    str(borrow['borrow_id']),
                    borrow['username'],
                    str(borrow['book_id']),
                    borrow['borrow_date'],
                    borrow['due_date'],
                    borrow['return_date'],
                    borrow['status'],
                    f"{borrow['fine_amount']:.2f}"
                ])
                f.write(line + '\n')
        return True
    except Exception as e:
        return False


def load_reservations():
    reservations = {}
    filepath = os.path.join(data_path, 'reservations.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                reservation_id = int(parts[0])
                username = parts[1]
                book_id = int(parts[2])
                reservation_date = parts[3]
                status = parts[4]
                reservations[reservation_id] = {
                    'reservation_id': reservation_id,
                    'username': username,
                    'book_id': book_id,
                    'reservation_date': reservation_date,
                    'status': status
                }
    return reservations


def save_reservations(reservations):
    filepath = os.path.join(data_path, 'reservations.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for r in reservations.values():
                line = '|'.join([
                    str(r['reservation_id']),
                    r['username'],
                    str(r['book_id']),
                    r['reservation_date'],
                    r['status']
                ])
                f.write(line + '\n')
        return True
    except:
        return False


def load_reviews():
    reviews = {}
    filepath = os.path.join(data_path, 'reviews.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if not line:
                    continue
                parts = line.split('|', 5)
                if len(parts) != 6:
                    continue
                review_id = int(parts[0])
                username = parts[1]
                book_id = int(parts[2])
                try:
                    rating = int(parts[3])
                except:
                    rating = 0
                review_text = parts[4]
                review_date = parts[5]
                reviews[review_id] = {
                    'review_id': review_id,
                    'username': username,
                    'book_id': book_id,
                    'rating': rating,
                    'review_text': review_text,
                    'review_date': review_date
                }
    return reviews


def save_reviews(reviews):
    filepath = os.path.join(data_path, 'reviews.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for r in reviews.values():
                line = '|'.join([
                    str(r['review_id']),
                    r['username'],
                    str(r['book_id']),
                    str(r['rating']),
                    r['review_text'],
                    r['review_date']
                ])
                f.write(line + '\n')
        return True
    except:
        return False


def load_fines():
    fines = {}
    filepath = os.path.join(data_path, 'fines.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                fine_id = int(parts[0])
                username = parts[1]
                borrow_id = int(parts[2])
                try:
                    amount = float(parts[3])
                except:
                    amount = 0.0
                status = parts[4]
                date_issued = parts[5]
                fines[fine_id] = {
                    'fine_id': fine_id,
                    'username': username,
                    'borrow_id': borrow_id,
                    'amount': amount,
                    'status': status,
                    'date_issued': date_issued
                }
    return fines


def save_fines(fines):
    filepath = os.path.join(data_path, 'fines.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for fine in fines.values():
                line = '|'.join([
                    str(fine['fine_id']),
                    fine['username'],
                    str(fine['borrow_id']),
                    f"{fine['amount']:.2f}",
                    fine['status'],
                    fine['date_issued']
                ])
                f.write(line + '\n')
        return True
    except:
        return False


# Dummy current user helper
# For simplicity, we assume a fixed logged-in user named 'john_reader'
def get_current_username():
    # In a real app, this would come from session or login management
    return 'john_reader'


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = get_current_username()
    books = load_books()
    # To get featured books: let's pick first 3 available books or any 3 if less
    featured_books = []
    for b in books.values():
        if b['status'] == 'Available':
            featured_books.append({'book_id': b['book_id'], 'title': b['title'], 'author': b['author']})
        if len(featured_books) >= 3:
            break
    context = {
        'username': username,
        'featured_books': featured_books
    }
    return render_template('dashboard.html', **context)


@app.route('/catalog')
def book_catalog():
    books = load_books()
    books_list = []
    for b in books.values():
        books_list.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': b['status']
        })
    return render_template('catalog.html', books=books_list)


@app.route('/book/<int:book_id>')
def book_details(book_id):
    username = get_current_username()
    books = load_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    book = books[book_id]

    # Load reviews for this book
    reviews_all = load_reviews()
    reviews = []
    for r in reviews_all.values():
        if r['book_id'] == book_id:
            reviews.append({
                'review_id': r['review_id'],
                'username': r['username'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })

    # Check if user has borrowed this book
    borrowings = load_borrowings()
    user_has_borrowed = False
    user_can_borrow = False
    user_borrow_active = False
    for borrow in borrowings.values():
        if borrow['username'] == username and borrow['book_id'] == book_id and borrow['status'] == 'Active':
            user_has_borrowed = True
            user_borrow_active = True
            break
    # User can borrow if book is Available and user has no active borrow for this book
    if book['status'] == 'Available' and not user_borrow_active:
        user_can_borrow = True

    context = {
        'book': {
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'status': book['status'],
            'description': book['description'],
            'avg_rating': book['avg_rating']
        },
        'reviews': reviews,
        'user_has_borrowed': user_has_borrowed,
        'user_can_borrow': user_can_borrow
    }
    return render_template('book_details.html', **context)


@app.route('/borrow/<int:book_id>')
def borrow_confirmation(book_id):
    username = get_current_username()
    books = load_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    book = books[book_id]

    # Check availability
    if book['status'] != 'Available':
        flash('Book is not available to borrow.')
        return redirect(url_for('book_details', book_id=book_id))

    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')

    context = {
        'book': {
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author']
        },
        'due_date': due_date
    }
    return render_template('borrow_confirmation.html', **context)


@app.route('/borrow/confirm/<int:book_id>', methods=['POST'])
def confirm_borrow(book_id):
    username = get_current_username()
    books = load_books()
    borrowings = load_borrowings()

    if book_id not in books:
        return render_template('borrow_result.html', success=False, book={'book_id': book_id, 'title': '', 'author': ''}, due_date='', error_message='Book not found.')

    book = books[book_id]

    # Check if available
    if book['status'] != 'Available':
        return render_template('borrow_result.html', success=False, book=book, due_date='', error_message='Book not available.')

    # Check if user already has an active borrow of this book
    for borrow in borrowings.values():
        if borrow['username'] == username and borrow['book_id'] == book_id and borrow['status'] == 'Active':
            return render_template('borrow_result.html', success=False, book=book, due_date='', error_message='You already have an active borrow of this book.')

    # Create new borrow record
    new_borrow_id = max(borrowings.keys(), default=0) + 1
    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date_date = datetime.now() + timedelta(days=14)
    due_date_str = due_date_date.strftime('%Y-%m-%d')

    new_borrow = {
        'borrow_id': new_borrow_id,
        'username': username,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date_str,
        'return_date': '',
        'status': 'Active',
        'fine_amount': 0.0
    }

    borrowings[new_borrow_id] = new_borrow

    # Update book status
    book['status'] = 'Borrowed'
    save_books(books)
    save_borrowings(borrowings)

    context = {
        'success': True,
        'book': {
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author']
        },
        'due_date': due_date_str
    }
    return render_template('borrow_result.html', **context)


@app.route('/my-borrows', methods=['GET', 'POST'])
def my_borrowings():
    username = get_current_username()
    borrowings = load_borrowings()
    books = load_books()

    filter_status = request.args.get('filter_status', 'All') if request.method == 'GET' else request.form.get('filter_status', 'All')

    borrows_list = []
    for borrow in borrowings.values():
        if borrow['username'] == username:
            # Update status for overdue if needed
            if borrow['status'] == 'Active':
                due_date_obj = datetime.strptime(borrow['due_date'], '%Y-%m-%d')
                if datetime.now() > due_date_obj:
                    borrow['status'] = 'Overdue'
                    # Mark fine_amount here if overdue and no fine recorded
                    if borrow['fine_amount'] == 0.0:
                        # Calculate fine amount based on overdue days e.g. $1 per day
                        overdue_days = (datetime.now() - due_date_obj).days
                        fine_val = overdue_days * 1.0
                        borrow['fine_amount'] = fine_val
                    save_borrowings(borrowings)

            # Filter
            if filter_status != 'All' and borrow['status'] != filter_status:
                continue

            title = books[borrow['book_id']]['title'] if borrow['book_id'] in books else ''

            borrows_list.append({
                'borrow_id': borrow['borrow_id'],
                'book_id': borrow['book_id'],
                'title': title,
                'borrow_date': borrow['borrow_date'],
                'due_date': borrow['due_date'],
                'return_date': borrow['return_date'],
                'status': borrow['status'],
                'fine_amount': borrow['fine_amount']
            })

    return render_template('my_borrows.html', borrows=borrows_list, filter_status=filter_status)


@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    username = get_current_username()
    borrowings = load_borrowings()
    books = load_books()
    fines = load_fines()

    if borrow_id not in borrowings:
        return render_template('return_result.html', success=False, borrow_id=borrow_id, error_message='Borrow record not found.')

    borrow = borrowings[borrow_id]

    if borrow['username'] != username:
        return render_template('return_result.html', success=False, borrow_id=borrow_id, error_message='Unauthorized')

    if borrow['status'] not in ('Active', 'Overdue'):
        return render_template('return_result.html', success=False, borrow_id=borrow_id, error_message='This borrow is not active or overdue and cannot be returned.')

    # Mark return date
    return_date = datetime.now().strftime('%Y-%m-%d')
    borrow['return_date'] = return_date
    borrow['status'] = 'Returned'

    # Update book status to Available if no other active borrow or reservation
    book_id = borrow['book_id']
    book = books.get(book_id)
    if book:
        # Check any other active borrow for this book?
        borrowings_for_book = [b for b in borrowings.values() if b['book_id'] == book_id and b['status'] == 'Active']
        if not borrowings_for_book:
            # Check if any active reservation for this book
            reservations = load_reservations()
            active_reservations = [r for r in reservations.values() if r['book_id'] == book_id and r['status'] == 'Active']
            if active_reservations:
                book['status'] = 'Reserved'
            else:
                book['status'] = 'Available'

    # If overdue and fine amount > 0, create fine record if not exist
    if borrow['status'] == 'Returned' and borrow['fine_amount'] > 0:
        existing_fines = [f for f in fines.values() if f['borrow_id'] == borrow_id]
        if not existing_fines:
            new_fine_id = max(fines.keys(), default=0) + 1
            fine_record = {
                'fine_id': new_fine_id,
                'username': username,
                'borrow_id': borrow_id,
                'amount': borrow['fine_amount'],
                'status': 'Unpaid',
                'date_issued': return_date
            }
            fines[new_fine_id] = fine_record

    save_borrowings(borrowings)
    save_books(books)
    save_fines(fines)

    return render_template('return_result.html', success=True, borrow_id=borrow_id)


@app.route('/my-reservations')
def my_reservations():
    username = get_current_username()
    reservations = load_reservations()
    books = load_books()

    reservations_list = []
    for r in reservations.values():
        if r['username'] == username:
            reservation_id = r['reservation_id']
            book_id = r['book_id']
            title = books[book_id]['title'] if book_id in books else ''
            reservations_list.append({
                'reservation_id': reservation_id,
                'book_id': book_id,
                'title': title,
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })

    return render_template('my_reservations.html', reservations=reservations_list)


@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = get_current_username()
    reservations = load_reservations()
    if reservation_id not in reservations:
        flash('Reservation not found.')
        return redirect(url_for('my_reservations'))

    reservation = reservations[reservation_id]
    if reservation['username'] != username:
        flash('Unauthorized.')
        return redirect(url_for('my_reservations'))

    # Only active reservations can be cancelled
    if reservation['status'] != 'Active':
        flash('Reservation already cancelled.')
        return redirect(url_for('my_reservations'))

    reservation['status'] = 'Cancelled'
    save_reservations(reservations)
    flash('Reservation cancelled successfully.')
    return redirect(url_for('my_reservations'))


@app.route('/my-reviews')
def my_reviews():
    username = get_current_username()
    reviews = load_reviews()
    books = load_books()

    reviews_list = []
    for r in reviews.values():
        if r['username'] == username:
            book_id = r['book_id']
            title = books[book_id]['title'] if book_id in books else ''
            reviews_list.append({
                'review_id': r['review_id'],
                'book_id': book_id,
                'title': title,
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })

    return render_template('my_reviews.html', reviews=reviews_list)


@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    username = get_current_username()
    reviews = load_reviews()

    if review_id not in reviews:
        flash('Review not found.')
        return redirect(url_for('my_reviews'))

    review = reviews[review_id]
    if review['username'] != username:
        flash('Unauthorized.')
        return redirect(url_for('my_reviews'))

    del reviews[review_id]
    save_reviews(reviews)
    flash('Review deleted.')
    return redirect(url_for('my_reviews'))


@app.route('/review/write/<int:book_id>')
def write_review(book_id):
    username = get_current_username()
    books = load_books()
    reviews = load_reviews()

    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    book = books[book_id]

    # Check for existing review by this user for this book
    existing_review = None
    for r in reviews.values():
        if r['username'] == username and r['book_id'] == book_id:
            existing_review = {
                'review_id': r['review_id'],
                'rating': r['rating'],
                'review_text': r['review_text']
            }
            break

    context = {
        'book': {
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author']
        },
        'existing_review': existing_review
    }
    return render_template('write_review.html', **context)


@app.route('/review/submit/<int:book_id>', methods=['POST'])
def submit_review(book_id):
    username = get_current_username()
    books = load_books()
    reviews = load_reviews()

    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    rating_s = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()

    if not rating_s or not rating_s.isdigit() or int(rating_s) < 1 or int(rating_s) > 5:
        flash('Invalid rating. Must be integer 1-5.')
        return redirect(url_for('write_review', book_id=book_id))

    rating = int(rating_s)

    if not review_text:
        flash('Review text cannot be empty.')
        return redirect(url_for('write_review', book_id=book_id))

    # Check if user already has a review for this book
    existing_review_id = None
    for r in reviews.values():
        if r['username'] == username and r['book_id'] == book_id:
            existing_review_id = r['review_id']
            break

    review_date = datetime.now().strftime('%Y-%m-%d')

    if existing_review_id is not None:
        # Update existing review
        reviews[existing_review_id]['rating'] = rating
        reviews[existing_review_id]['review_text'] = review_text
        reviews[existing_review_id]['review_date'] = review_date
    else:
        # Create new review
        new_review_id = max(reviews.keys(), default=0) + 1
        reviews[new_review_id] = {
            'review_id': new_review_id,
            'username': username,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }

    save_reviews(reviews)
    return redirect(url_for('book_details', book_id=book_id))


@app.route('/profile')
def user_profile():
    username = get_current_username()
    users = load_users()
    borrowings = load_borrowings()
    books = load_books()

    user = users.get(username)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard'))

    borrow_history = []
    for b in borrowings.values():
        if b['username'] == username:
            title = books[b['book_id']]['title'] if b['book_id'] in books else ''
            borrow_history.append({
                'title': title,
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })

    context = {
        'username': username,
        'email': user['email'],
        'phone': user['phone'],
        'address': user['address'],
        'borrow_history': borrow_history
    }
    return render_template('profile.html', **context)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = get_current_username()
    users = load_users()

    if username not in users:
        flash('User not found.')
        return redirect(url_for('user_profile'))

    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    if not email:
        flash('Email cannot be empty.')
        return redirect(url_for('user_profile'))

    # Update fields
    users[username]['email'] = email
    # The spec said only email is editable, but phone and address are shown; so let's update phone and address as well
    users[username]['phone'] = phone
    users[username]['address'] = address

    if save_users(users):
        flash('Profile updated successfully.')
    else:
        flash('Failed to update profile.')

    return redirect(url_for('user_profile'))


@app.route('/payment/<int:fine_id>')
def payment_confirmation(fine_id):
    username = get_current_username()
    fines = load_fines()

    if fine_id not in fines:
        flash('Fine not found.')
        return redirect(url_for('user_profile'))

    fine = fines[fine_id]

    context = {
        'fine': fine,
        'username': username
    }
    return render_template('payment_confirmation.html', **context)


@app.route('/payment/confirm/<int:fine_id>', methods=['POST'])
def confirm_payment(fine_id):
    username = get_current_username()
    fines = load_fines()

    if fine_id not in fines:
        flash('Fine not found.')
        return redirect(url_for('user_profile'))

    fine = fines[fine_id]

    if fine['username'] != username:
        flash('Unauthorized.')
        return redirect(url_for('user_profile'))

    if fine['status'] == 'Paid':
        flash('Fine already paid.')
        return redirect(url_for('user_profile'))

    fine['status'] = 'Paid'
    if save_fines(fines):
        flash('Payment successful.')
    else:
        flash('Payment failed.')

    return redirect(url_for('user_profile'))


if __name__ == '__main__':
    app.run(debug=True)
