from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'some_secret_key_for_sessions'

DATA_DIR = 'data'

# File paths
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
BORROWINGS_FILE = os.path.join(DATA_DIR, 'borrowings.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
FINES_FILE = os.path.join(DATA_DIR, 'fines.txt')

# Helper functions to load and write data

def load_users():
    users = {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username, email, phone, address = line.split('|')
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'address': address
                }
    except FileNotFoundError:
        pass
    return users


def load_books():
    books = {}
    try:
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                (book_id, title, author, isbn, genre, publisher, year, description, status, avg_rating) = line.split('|')
                book_id = int(book_id)
                avg_rating = float(avg_rating)
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
    except FileNotFoundError:
        pass
    return books


def load_borrowings():
    borrowings = {}
    try:
        with open(BORROWINGS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                (borrow_id, username, book_id, borrow_date, due_date, return_date, status, fine_amount) = line.split('|')
                borrow_id = int(borrow_id)
                book_id = int(book_id)
                fine_amount = float(fine_amount) if fine_amount else 0.0
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
    except FileNotFoundError:
        pass
    return borrowings


def load_reservations():
    reservations = {}
    try:
        with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                reservation_id, username, book_id, reservation_date, status = line.split('|')
                reservation_id = int(reservation_id)
                book_id = int(book_id)
                reservations[reservation_id] = {
                    'reservation_id': reservation_id,
                    'username': username,
                    'book_id': book_id,
                    'reservation_date': reservation_date,
                    'status': status
                }
    except FileNotFoundError:
        pass
    return reservations


def load_reviews():
    reviews = {}
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                review_id, username, book_id, rating, review_text, review_date = line.split('|')
                review_id = int(review_id)
                book_id = int(book_id)
                rating = int(rating)
                reviews[review_id] = {
                    'review_id': review_id,
                    'username': username,
                    'book_id': book_id,
                    'rating': rating,
                    'review_text': review_text,
                    'review_date': review_date
                }
    except FileNotFoundError:
        pass
    return reviews


def load_fines():
    fines = {}
    try:
        with open(FINES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                fine_id, username, borrow_id, amount, status, date_issued = line.split('|')
                fine_id = int(fine_id)
                borrow_id = int(borrow_id)
                amount = float(amount)
                fines[fine_id] = {
                    'fine_id': fine_id,
                    'username': username,
                    'borrow_id': borrow_id,
                    'amount': amount,
                    'status': status,
                    'date_issued': date_issued
                }
    except FileNotFoundError:
        pass
    return fines


def write_users(users):
    lines = []
    for u in users.values():
        line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
        lines.append(line)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def write_books(books):
    lines = []
    for b in books.values():
        line = '|'.join([
            str(b['book_id']), b['title'], b['author'], b['isbn'], b['genre'], b['publisher'],
            b['year'], b['description'], b['status'], str(b['avg_rating'])
        ])
        lines.append(line)
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def write_borrowings(borrowings):
    lines = []
    for b in borrowings.values():
        line = '|'.join([
            str(b['borrow_id']), b['username'], str(b['book_id']), b['borrow_date'], b['due_date'],
            b['return_date'] if b['return_date'] else '', b['status'], f"{b['fine_amount']:.2f}"
        ])
        lines.append(line)
    with open(BORROWINGS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def write_reservations(reservations):
    lines = []
    for r in reservations.values():
        line = '|'.join([
            str(r['reservation_id']), r['username'], str(r['book_id']), r['reservation_date'], r['status']
        ])
        lines.append(line)
    with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def write_reviews(reviews):
    lines = []
    for r in reviews.values():
        line = '|'.join([
            str(r['review_id']), r['username'], str(r['book_id']), str(r['rating']), r['review_text'], r['review_date']
        ])
        lines.append(line)
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def write_fines(fines):
    lines = []
    for f in fines.values():
        line = '|'.join([
            str(f['fine_id']), f['username'], str(f['borrow_id']), f"{f['amount']:.2f}", f['status'], f['date_issued']
        ])
        lines.append(line)
    with open(FINES_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


# Utility functions

def get_next_id(items):
    if not items:
        return 1
    return max(items) + 1



def calculate_due_date(borrow_date_str):
    try:
        borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d')
        due_date = borrow_date + timedelta(days=14)
        return due_date.strftime('%Y-%m-%d')
    except Exception:
        return ''



def get_current_username():
    # For simplicity, assuming a fixed logged-in user for now
    # In real case, would rely on session or auth system
    # Here we just return a fixed username 'john_reader'
    return 'john_reader'



def find_reviews_for_book(book_id):
    reviews = load_reviews()
    book_reviews = []
    for r in reviews.values():
        if r['book_id'] == book_id:
            book_reviews.append({
                'review_id': r['review_id'],
                'username': r['username'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })
    return sorted(book_reviews, key=lambda x: x['review_date'], reverse=True)


def find_borrowings_for_user(username, filter_status='All'):
    borrowings = load_borrowings()
    books = load_books()
    result = []
    for b in borrowings.values():
        if b['username'] == username:
            if filter_status != 'All' and b['status'] != filter_status:
                continue
            book_title = books.get(b['book_id'], {}).get('title', 'Unknown')
            result.append({
                'borrow_id': b['borrow_id'],
                'book_title': book_title,
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'status': b['status'],
                'fine_amount': b['fine_amount']
            })
    return result


def find_reservations_for_user(username):
    reservations = load_reservations()
    books = load_books()
    result = []
    for r in reservations.values():
        if r['username'] == username and r['status'] == 'Active':
            book_title = books.get(r['book_id'], {}).get('title', 'Unknown')
            result.append({
                'reservation_id': r['reservation_id'],
                'book_title': book_title,
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })
    return result


def find_reviews_for_user(username):
    reviews = load_reviews()
    books = load_books()
    result = []
    for r in reviews.values():
        if r['username'] == username:
            book_title = books.get(r['book_id'], {}).get('title', 'Unknown')
            result.append({
                'review_id': r['review_id'],
                'book_title': book_title,
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })
    return result


def find_borrow_history_for_user(username):
    borrowings = load_borrowings()
    books = load_books()
    result = []
    for b in borrowings.values():
        if b['username'] == username:
            book_title = books.get(b['book_id'], {}).get('title', 'Unknown')
            result.append({
                'book_title': book_title,
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date'],
                'status': b['status']
            })
    return sorted(result, key=lambda x: x['borrow_date'], reverse=True)


def max_borrow_id():
    borrowings = load_borrowings()
    if not borrowings:
        return 0
    return max(borrowings.keys())


def max_reservation_id():
    reservations = load_reservations()
    if not reservations:
        return 0
    return max(reservations.keys())


def max_review_id():
    reviews = load_reviews()
    if not reviews:
        return 0
    return max(reviews.keys())


def max_fine_id():
    fines = load_fines()
    if not fines:
        return 0
    return max(fines.keys())

# Route Implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    username = get_current_username()
    books = load_books()
    # featured_books: Let's take first 3 books sorted by book_id for demo
    featured_books = []
    for b in sorted(books.values(), key=lambda x: x['book_id'])[:3]:
        featured_books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': b['status']
        })
    return render_template('dashboard.html', username=username, featured_books=featured_books)


@app.route('/catalog', methods=['GET'])
def book_catalog_page():
    search_query = request.args.get('search', '').strip()
    books = load_books()
    filtered_books = []
    if search_query:
        lower_q = search_query.lower()
        for b in books.values():
            if (lower_q in b['title'].lower() or lower_q in b['author'].lower() or lower_q in b['genre'].lower() or lower_q in b['description'].lower()):
                filtered_books.append({
                    'book_id': b['book_id'],
                    'title': b['title'],
                    'author': b['author'],
                    'status': b['status']
                })
    else:
        for b in books.values():
            filtered_books.append({
                'book_id': b['book_id'],
                'title': b['title'],
                'author': b['author'],
                'status': b['status']
            })
    return render_template('catalog.html', books=filtered_books, search_query=search_query)


@app.route('/book/<int:book_id>', methods=['GET'])
def book_details_page(book_id):
    username = get_current_username()
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))

    reviews = find_reviews_for_book(book_id)

    return render_template('book_details.html', book=book, reviews=reviews, username=username)


@app.route('/borrow/<int:book_id>', methods=['GET'])
def borrow_confirmation_page(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))

    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    return render_template('borrow_confirmation.html', book=book, due_date=due_date)


@app.route('/borrow/<int:book_id>/confirm', methods=['POST'])
def confirm_borrow(book_id):
    username = get_current_username()
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))

    if book['status'] != 'Available':
        message = 'Book is not available for borrowing.'
        return render_template('borrow_confirmation.html', book=book, due_date=(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'), message=message)

    borrowings = load_borrowings()
    # Enforce rule: user can't borrow the same book multiple times active
    for b in borrowings.values():
        if b['username'] == username and b['book_id'] == book_id and b['status'] == 'Active':
            message = 'You already have this book borrowed and active.'
            return render_template('borrow_confirmation.html', book=book, due_date=(datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'), message=message)

    borrow_id = get_next_id(borrowings)
    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    new_borrow = {
        'borrow_id': borrow_id,
        'username': username,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'return_date': '',
        'status': 'Active',
        'fine_amount': 0.0
    }
    borrowings[borrow_id] = new_borrow

    # Update book status to Borrowed
    book['status'] = 'Borrowed'
    books[book_id] = book

    write_borrowings(borrowings)
    write_books(books)

    message = 'Borrowing successful. Enjoy the book!'
    return render_template('borrow_success.html', book=book, borrow_id=borrow_id, due_date=due_date, message=message)


@app.route('/borrow/<int:book_id>/cancel', methods=['POST'])
def cancel_borrow(book_id):
    return redirect(url_for('book_details_page', book_id=book_id))


@app.route('/my-borrows', methods=['GET'])
def my_borrowings_page():
    username = get_current_username()
    filter_status = request.args.get('filter_status', 'All')
    borrows = find_borrowings_for_user(username, filter_status)
    return render_template('my_borrows.html', borrows=borrows, filter_status=filter_status)


@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    username = get_current_username()
    borrowings = load_borrowings()
    books = load_books()
    fines = load_fines()

    borrow = borrowings.get(borrow_id)
    if not borrow or borrow['username'] != username:
        flash('Borrow record not found.')
        borrows = find_borrowings_for_user(username)
        return render_template('my_borrows.html', borrows=borrows, filter_status='All')

    if borrow['status'] != 'Active' and borrow['status'] != 'Overdue':
        flash('This book cannot be returned.')
        borrows = find_borrowings_for_user(username)
        return render_template('my_borrows.html', borrows=borrows, filter_status='All')

    # Update return information
    borrow['return_date'] = datetime.now().strftime('%Y-%m-%d')
    borrow['status'] = 'Returned'

    # Update book status to Available
    book_id = borrow['book_id']
    book = books.get(book_id)
    if book:
        book['status'] = 'Available'
        books[book_id] = book

    # Update borrowings
    borrowings[borrow_id] = borrow

    write_borrowings(borrowings)
    write_books(books)

    message = 'Book returned successfully.'
    return render_template('return_confirmation.html', borrow_id=borrow_id, message=message)


@app.route('/my-reservations', methods=['GET'])
def my_reservations_page():
    username = get_current_username()
    reservations = find_reservations_for_user(username)
    return render_template('my_reservations.html', reservations=reservations)


@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = get_current_username()
    reservations = load_reservations()
    reservation = reservations.get(reservation_id)
    if not reservation or reservation['username'] != username:
        flash('Reservation not found or not authorized.')
        return redirect(url_for('my_reservations_page'))

    if reservation['status'] != 'Active':
        flash('Reservation cannot be cancelled.')
        return redirect(url_for('my_reservations_page'))

    reservation['status'] = 'Cancelled'
    reservations[reservation_id] = reservation
    write_reservations(reservations)

    flash('Reservation cancelled successfully.')
    return redirect(url_for('my_reservations_page'))


@app.route('/my-reviews', methods=['GET'])
def my_reviews_page():
    username = get_current_username()
    reviews = find_reviews_for_user(username)
    return render_template('my_reviews.html', reviews=reviews)


@app.route('/review/edit/<int:review_id>', methods=['GET'])
def edit_review_page(review_id):
    username = get_current_username()
    reviews = load_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != username:
        flash('Review not found or not authorized.')
        return redirect(url_for('my_reviews_page'))

    books = load_books()
    book = books.get(review['book_id'])
    if not book:
        flash('Associated book not found.')
        return redirect(url_for('my_reviews_page'))

    review_data = {
        'review_id': review['review_id'],
        'book_id': review['book_id'],
        'rating': review['rating'],
        'review_text': review['review_text']
    }

    return render_template('write_review.html', review=review_data, book=book)


@app.route('/review/edit/<int:review_id>', methods=['POST'])
def submit_review_edit(review_id):
    username = get_current_username()
    reviews = load_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != username:
        flash('Review not found or not authorized.')
        return redirect(url_for('my_reviews_page'))

    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        message = 'Rating must be an integer between 1 and 5.'
        books = load_books()
        book = books.get(review['book_id'])
        review_data = {
            'review_id': review['review_id'],
            'book_id': review['book_id'],
            'rating': review['rating'],
            'review_text': review['review_text']
        }
        return render_template('write_review.html', review=review_data, book=book, message=message)

    review['rating'] = int(rating)
    review['review_text'] = review_text
    review['review_date'] = datetime.now().strftime('%Y-%m-%d')

    reviews[review_id] = review
    write_reviews(reviews)

    flash('Review updated successfully.')
    return redirect(url_for('my_reviews_page'))


@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    username = get_current_username()
    reviews = load_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != username:
        flash('Review not found or not authorized.')
        return redirect(url_for('my_reviews_page'))

    del reviews[review_id]
    write_reviews(reviews)

    flash('Review deleted successfully.')
    return redirect(url_for('my_reviews_page'))


@app.route('/review/write/<int:book_id>', methods=['GET'])
def write_review_page(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))

    return render_template('write_review.html', book=book, review=None)


@app.route('/review/write/<int:book_id>', methods=['POST'])
def submit_review(book_id):
    username = get_current_username()
    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        message = 'Rating must be an integer between 1 and 5.'
        books = load_books()
        book = books.get(book_id)
        return render_template('write_review.html', book=book, message=message)

    reviews = load_reviews()
    review_id = get_next_id(reviews)
    review_date = datetime.now().strftime('%Y-%m-%d')

    new_review = {
        'review_id': review_id,
        'username': username,
        'book_id': book_id,
        'rating': int(rating),
        'review_text': review_text,
        'review_date': review_date
    }
    reviews[review_id] = new_review
    write_reviews(reviews)

    flash('Review submitted successfully.')
    return redirect(url_for('book_details_page', book_id=book_id))


@app.route('/profile', methods=['GET'])
def user_profile_page():
    username = get_current_username()
    users = load_users()
    user = users.get(username)
    if not user:
        flash('User not found.')
        user = {'username': username, 'email': '', 'phone': '', 'address': ''}
    borrow_history = find_borrow_history_for_user(username)
    reservations = find_reservations_for_user(username)
    fines = [fine for fine in load_fines().values() if fine['username'] == username and fine['status'] != 'Paid']
    return render_template('profile.html', user=user, borrow_history=borrow_history, reservations=reservations, fines=fines)


@app.route('/profile/update', methods=['POST'])
def update_profile():
    username = get_current_username()
    users = load_users()
    user = users.get(username)
    if not user:
        flash('User not found.')
        return redirect(url_for('user_profile_page'))

    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    if not email or not phone or not address:
        message = 'Email, phone and address are required.'
        borrow_history = find_borrow_history_for_user(username)
        reservations = find_reservations_for_user(username)
        fines = [fine for fine in load_fines().values() if fine['username'] == username and fine['status'] != 'Paid']
        return render_template('profile.html', user=user, borrow_history=borrow_history, reservations=reservations, fines=fines, message=message)

    user['email'] = email
    user['phone'] = phone
    user['address'] = address

    users[username] = user
    write_users(users)

    message = 'Profile updated successfully.'
    borrow_history = find_borrow_history_for_user(username)
    reservations = find_reservations_for_user(username)
    fines = [fine for fine in load_fines().values() if fine['username'] == username and fine['status'] != 'Paid']
    return render_template('profile.html', user=user, borrow_history=borrow_history, reservations=reservations, fines=fines, message=message)


@app.route('/payment/<int:fine_id>', methods=['GET'])
def payment_confirmation_page(fine_id):
    fines = load_fines()
    fine = fines.get(fine_id)
    if not fine:
        flash('Fine record not found.')
        return redirect(url_for('user_profile_page'))

    return render_template('payment_confirmation.html', fine=fine)


@app.route('/payment/<int:fine_id>/confirm', methods=['POST'])
def confirm_payment(fine_id):
    fines = load_fines()
    fine = fines.get(fine_id)
    if not fine:
        message = 'Fine record not found.'
        return render_template('payment_confirmation.html', fine=None, message=message)

    if fine['status'] == 'Paid':
        message = 'Fine is already paid.'
        return render_template('payment_confirmation.html', fine=fine, message=message)

    fine['status'] = 'Paid'
    fines[fine_id] = fine
    write_fines(fines)

    message = 'Payment successful.'
    # After payment, redirect user to profile page with message
    users = load_users()  # For context refresh
    username = fine['username']
    user = users.get(username, None)
    borrow_history = find_borrow_history_for_user(username)
    reservations = find_reservations_for_user(username)
    fines = [fine for fine in load_fines().values() if fine['username'] == username and fine['status'] != 'Paid']

    return render_template('profile.html', user=user, borrow_history=borrow_history, reservations=reservations, fines=fines, message=message)


if __name__ == '__main__':
    app.run(debug=True)
