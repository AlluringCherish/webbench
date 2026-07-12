from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATA_DIR = 'data'

# Helper functions for file read/write

def read_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = {}
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 4:
                username, email, phone, address = parts
                users[username] = {
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'address': address
                }
    return users


def write_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users.values():
            line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
            f.write(line + '\n')


def read_books():
    path = os.path.join(DATA_DIR, 'books.txt')
    books = {}
    if not os.path.exists(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 10:
                book_id = int(parts[0])
                title = parts[1]
                author = parts[2]
                isbn = parts[3]
                genre = parts[4]
                publisher = parts[5]
                year = int(parts[6])
                description = parts[7]
                status = parts[8]
                try:
                    avg_rating = float(parts[9])
                except ValueError:
                    avg_rating = 0.0
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


def write_books(books):
    path = os.path.join(DATA_DIR, 'books.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in books.values():
            line = '|'.join([
                str(b['book_id']), b['title'], b['author'], b['isbn'], b['genre'], b['publisher'],
                str(b['year']), b['description'], b['status'], f"{b['avg_rating']:.2f}"
            ])
            f.write(line + '\n')


def read_borrowings():
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    borrowings = {}
    if not os.path.exists(path):
        return borrowings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 8:
                borrow_id = int(parts[0])
                username = parts[1]
                book_id = int(parts[2])
                borrow_date = parts[3]
                due_date = parts[4]
                return_date = parts[5] if parts[5] != '' else None
                status = parts[6]
                try:
                    fine_amount = float(parts[7])
                except ValueError:
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


def write_borrowings(borrowings):
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in borrowings.values():
            ret_date = b['return_date'] if b['return_date'] is not None else ''
            line = '|'.join([
                str(b['borrow_id']), b['username'], str(b['book_id']),
                b['borrow_date'], b['due_date'], ret_date, b['status'], f"{b['fine_amount']:.2f}"
            ])
            f.write(line + '\n')


def read_reservations():
    path = os.path.join(DATA_DIR, 'reservations.txt')
    reservations = {}
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 5:
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


def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations.values():
            line = '|'.join([
                str(r['reservation_id']), r['username'], str(r['book_id']), r['reservation_date'], r['status']
            ])
            f.write(line + '\n')


def read_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = {}
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 6:
                review_id = int(parts[0])
                username = parts[1]
                book_id = int(parts[2])
                rating = int(parts[3])
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


def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews.values():
            line = '|'.join([
                str(r['review_id']), r['username'], str(r['book_id']), str(r['rating']), r['review_text'], r['review_date']
            ])
            f.write(line + '\n')


def read_fines():
    path = os.path.join(DATA_DIR, 'fines.txt')
    fines = {}
    if not os.path.exists(path):
        return fines
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 6:
                fine_id = int(parts[0])
                username = parts[1]
                borrow_id = int(parts[2])
                try:
                    amount = float(parts[3])
                except ValueError:
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


def write_fines(fines):
    path = os.path.join(DATA_DIR, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fi in fines.values():
            line = '|'.join([
                str(fi['fine_id']), fi['username'], str(fi['borrow_id']), f"{fi['amount']:.2f}", fi['status'], fi['date_issued']
            ])
            f.write(line + '\n')


# NOTE: The specification does not define how to manage login or current user sessions explicitly.
# Assuming for implementation, current logged-in user is fixed or from a query argument or similar for demonstration.
# For now, simulate a fixed current user for demonstration (e.g., 'john_reader').

CURRENT_USER = 'john_reader'


@app.route('/')
def root_redirect():
    # Redirect root to dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    username = CURRENT_USER
    return render_template('dashboard.html', username=username)


@app.route('/catalog')
def book_catalog():
    books_dict = read_books()
    # For catalog, only present book_id, title, author, status
    books = []
    for b in books_dict.values():
        books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': b['status']
        })
    return render_template('catalog.html', books=books)


@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    reviews_dict = read_reviews()
    reviews = []
    for r in reviews_dict.values():
        if r['book_id'] == book_id:
            reviews.append({
                'review_id': r['review_id'],
                'username': r['username'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })

    # Compute average rating again as safeguard if needed
    if reviews:
        avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
    else:
        avg_rating = 0.0

    if abs(book['avg_rating'] - avg_rating) > 0.01:
        # update avg_rating in books data
        book['avg_rating'] = round(avg_rating, 2)
        # Save update
        books[book_id]['avg_rating'] = book['avg_rating']
        write_books(books)

    return render_template('book_details.html', book=book, reviews=reviews)


@app.route('/borrow/<int:book_id>', methods=['GET'])
def borrow_confirmation(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details', book_id=book_id))

    due_date_obj = datetime.now().date() + timedelta(days=14)
    due_date = due_date_obj.isoformat()

    return render_template('borrow_confirmation.html', book=book, due_date=due_date)


@app.route('/borrow/<int:book_id>', methods=['POST'])
def confirm_borrow(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    if book['status'] != 'Available':
        flash('Book is not available to borrow.')
        return redirect(url_for('book_details', book_id=book_id))

    borrowings = read_borrowings()
    # Create new borrow_id
    if borrowings:
        borrow_id = max(borrowings.keys()) + 1
    else:
        borrow_id = 1

    now_date = datetime.now().date()
    borrow_date = now_date.isoformat()
    due_date_obj = now_date + timedelta(days=14)
    due_date = due_date_obj.isoformat()

    new_borrow = {
        'borrow_id': borrow_id,
        'username': CURRENT_USER,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }

    borrowings[borrow_id] = new_borrow

    # Update book status to Borrowed
    book['status'] = 'Borrowed'
    books[book_id] = book

    write_borrowings(borrowings)
    write_books(books)

    flash('Book borrowed successfully.')
    return redirect(url_for('my_borrowings'))


@app.route('/my_borrows')
def my_borrowings():
    borrowings = read_borrowings()
    books = read_books()

    user_borrows = []
    today = datetime.now().date()

    for b in borrowings.values():
        if b['username'] == CURRENT_USER:
            # Update status if overdue
            if b['status'] == 'Active' and b['return_date'] is None:
                due_date_obj = datetime.fromisoformat(b['due_date']).date()
                if today > due_date_obj:
                    b['status'] = 'Overdue'
            # Calculate fine_amount (should be stored already but we keep it updated here)
            # Let's keep fine amount from the borrowings.txt directly
            title = books.get(b['book_id'], {}).get('title', 'Unknown')
            user_borrows.append({
                'borrow_id': b['borrow_id'],
                'book_id': b['book_id'],
                'title': title,
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'status': b['status'],
                'fine_amount': b['fine_amount']
            })

    # Save any status updates
    # This only saves statuses updated to Overdue
    write_borrowings(borrowings)

    return render_template('my_borrows.html', borrowings=user_borrows)


@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrowings = read_borrowings()
    books = read_books()
    fines = read_fines()

    borrow = borrowings.get(borrow_id)
    if not borrow or borrow['username'] != CURRENT_USER:
        flash('Borrow record not found.')
        return redirect(url_for('my_borrowings'))

    if borrow['status'] not in ('Active', 'Overdue') or borrow['return_date'] is not None:
        flash('This book cannot be returned.')
        return redirect(url_for('my_borrowings'))

    now_date = datetime.now().date()
    return_date = now_date.isoformat()
    borrow['return_date'] = return_date

    due_date_obj = datetime.fromisoformat(borrow['due_date']).date()

    # Calculate fine if overdue
    fine_amount = 0.0
    if now_date > due_date_obj:
        days_overdue = (now_date - due_date_obj).days
        fine_amount = days_overdue * 1.0  # Suppose $1 per day overdue

    borrow['fine_amount'] = fine_amount

    # Update status
    borrow['status'] = 'Returned'

    # Update book status to Available
    book = books.get(borrow['book_id'])
    if book:
        book['status'] = 'Available'
        books[borrow['book_id']] = book

    # Add fine to fines.txt if fine_amount > 0
    if fine_amount > 0:
        if fines:
            fine_id = max(fines.keys()) + 1
        else:
            fine_id = 1
        fine_record = {
            'fine_id': fine_id,
            'username': CURRENT_USER,
            'borrow_id': borrow_id,
            'amount': fine_amount,
            'status': 'Unpaid',
            'date_issued': now_date.isoformat()
        }
        fines[fine_id] = fine_record

    write_borrowings(borrowings)
    write_books(books)
    write_fines(fines)

    flash('Book returned successfully.')
    return redirect(url_for('my_borrowings'))


@app.route('/my_reservations')
def my_reservations():
    reservations = read_reservations()
    books = read_books()

    user_reservations = []
    for r in reservations.values():
        if r['username'] == CURRENT_USER:
            title = books.get(r['book_id'], {}).get('title', 'Unknown')
            user_reservations.append({
                'reservation_id': r['reservation_id'],
                'book_id': r['book_id'],
                'title': title,
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })

    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    reservation = reservations.get(reservation_id)
    if not reservation or reservation['username'] != CURRENT_USER:
        flash('Reservation not found.')
        return redirect(url_for('my_reservations'))

    if reservation['status'] != 'Active':
        flash('Reservation cannot be cancelled.')
        return redirect(url_for('my_reservations'))

    reservation['status'] = 'Cancelled'
    reservations[reservation_id] = reservation
    write_reservations(reservations)
    flash('Reservation cancelled successfully.')
    return redirect(url_for('my_reservations'))


@app.route('/my_reviews')
def my_reviews():
    reviews = read_reviews()
    books = read_books()

    user_reviews = []
    for r in reviews.values():
        if r['username'] == CURRENT_USER:
            title = books.get(r['book_id'], {}).get('title', 'Unknown')
            user_reviews.append({
                'review_id': r['review_id'],
                'book_id': r['book_id'],
                'title': title,
                'rating': r['rating'],
                'review_text': r['review_text']
            })

    return render_template('my_reviews.html', reviews=user_reviews)


@app.route('/review/<int:book_id>', methods=['GET'])
def write_review(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    reviews = read_reviews()
    existing_review = None
    for r in reviews.values():
        if r['book_id'] == book_id and r['username'] == CURRENT_USER:
            existing_review = {
                'review_id': r['review_id'],
                'rating': r['rating'],
                'review_text': r['review_text']
            }
            break

    return render_template('write_review.html', book={'book_id': book['book_id'], 'title': book['title']}, existing_review=existing_review)


@app.route('/review/<int:book_id>', methods=['POST'])
def submit_review(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    # Validate rating
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError()
    except (ValueError, TypeError):
        flash('Rating must be an integer between 1 and 5.')
        return redirect(url_for('write_review', book_id=book_id))

    reviews = read_reviews()
    existing_review = None
    for r in reviews.values():
        if r['book_id'] == book_id and r['username'] == CURRENT_USER:
            existing_review = r
            break

    now_date = datetime.now().date().isoformat()

    if existing_review:
        # Update existing review
        existing_review['rating'] = rating
        existing_review['review_text'] = review_text
        existing_review['review_date'] = now_date
        reviews[existing_review['review_id']] = existing_review
    else:
        # Add new review
        if reviews:
            review_id = max(reviews.keys()) + 1
        else:
            review_id = 1
        new_review = {
            'review_id': review_id,
            'username': CURRENT_USER,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': now_date
        }
        reviews[review_id] = new_review

    write_reviews(reviews)

    # Recalculate and update avg_rating in books
    book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
    if book_reviews:
        avg_rating = sum(r['rating'] for r in book_reviews) / len(book_reviews)
    else:
        avg_rating = 0.0
    books[book_id]['avg_rating'] = round(avg_rating, 2)
    write_books(books)

    flash('Review submitted successfully.')
    return redirect(url_for('book_details', book_id=book_id))


@app.route('/profile', methods=['GET'])
def profile():
    users = read_users()
    borrowings = read_borrowings()
    books = read_books()

    user = users.get(CURRENT_USER)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard'))

    borrow_history = []
    for b in borrowings.values():
        if b['username'] == CURRENT_USER:
            title = books.get(b['book_id'], {}).get('title', 'Unknown')
            return_date = b['return_date'] if b['return_date'] is not None else None
            borrow_history.append({
                'borrow_id': b['borrow_id'],
                'book_id': b['book_id'],
                'title': title,
                'borrow_date': b['borrow_date'],
                'return_date': return_date
            })

    return render_template('profile.html', username=CURRENT_USER, email=user['email'], borrow_history=borrow_history)


@app.route('/profile', methods=['POST'])
def update_profile():
    email = request.form.get('email', '').strip()
    if not email:
        flash('Email cannot be empty.')
        return redirect(url_for('profile'))

    users = read_users()
    if CURRENT_USER not in users:
        flash('User not found.')
        return redirect(url_for('dashboard'))

    users[CURRENT_USER]['email'] = email
    write_users(users)

    flash('Profile updated successfully.')
    return redirect(url_for('profile'))


@app.route('/payment/<int:fine_id>', methods=['GET'])
def payment_confirmation(fine_id):
    fines = read_fines()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != CURRENT_USER:
        flash('Fine not found.')
        return redirect(url_for('profile'))

    return render_template('payment_confirmation.html', fine=fine)


@app.route('/payment/<int:fine_id>', methods=['POST'])
def confirm_payment(fine_id):
    fines = read_fines()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != CURRENT_USER:
        flash('Fine not found.')
        return redirect(url_for('profile'))

    fine['status'] = 'Paid'
    write_fines(fines)

    flash('Payment successful.')
    return redirect(url_for('profile'))


if __name__ == '__main__':
    app.run(debug=True)
