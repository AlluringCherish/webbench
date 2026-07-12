from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Data file paths
USERS_FILE = 'data/users.txt'
BOOKS_FILE = 'data/books.txt'
BORROWINGS_FILE = 'data/borrowings.txt'
RESERVATIONS_FILE = 'data/reservations.txt'
REVIEWS_FILE = 'data/reviews.txt'
FINES_FILE = 'data/fines.txt'

# Utility functions for file read/write with pipe-delimited format

def read_users():
    users = {}
    if not os.path.exists(USERS_FILE):
        return users
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            username, email, phone, address = line.split('|')
            users[username] = {
                'username': username,
                'email': email,
                'phone': phone,
                'address': address
            }
    return users

def write_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        for u in users.values():
            f.write('|'.join([u['username'], u['email'], u['phone'], u['address']]) + '\n')


def read_books():
    books = {}
    if not os.path.exists(BOOKS_FILE):
        return books
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
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
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        for b in books.values():
            line = '|'.join([
                str(b['book_id']), b['title'], b['author'], b['isbn'], b['genre'], b['publisher'],
                str(b['year']), b['description'], b['status'], str(b['avg_rating'])
            ])
            f.write(line + '\n')


def read_borrowings():
    borrowings = {}
    if not os.path.exists(BORROWINGS_FILE):
        return borrowings
    with open(BORROWINGS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
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
            return_date = parts[5] if parts[5] else None
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
    with open(BORROWINGS_FILE, 'w', encoding='utf-8') as f:
        for b in borrowings.values():
            line = '|'.join([
                str(b['borrow_id']), b['username'], str(b['book_id']), b['borrow_date'], b['due_date'],
                b['return_date'] if b['return_date'] else '', b['status'], f"{b['fine_amount']:.2f}"
            ])
            f.write(line + '\n')


def read_reservations():
    reservations = {}
    if not os.path.exists(RESERVATIONS_FILE):
        return reservations
    with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
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


def write_reservations(reservations):
    with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
        for r in reservations.values():
            line = '|'.join([
                str(r['reservation_id']), r['username'], str(r['book_id']), r['reservation_date'], r['status']
            ])
            f.write(line + '\n')


def read_reviews():
    reviews = {}
    if not os.path.exists(REVIEWS_FILE):
        return reviews
    with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            review_id = int(parts[0])
            username = parts[1]
            book_id = int(parts[2])
            try:
                rating = int(parts[3])
            except ValueError:
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


def write_reviews(reviews):
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        for r in reviews.values():
            line = '|'.join([
                str(r['review_id']), r['username'], str(r['book_id']), str(r['rating']), r['review_text'], r['review_date']
            ])
            f.write(line + '\n')


def read_fines():
    fines = {}
    if not os.path.exists(FINES_FILE):
        return fines
    with open(FINES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
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
    with open(FINES_FILE, 'w', encoding='utf-8') as f:
        for fine in fines.values():
            line = '|'.join([
                str(fine['fine_id']), fine['username'], str(fine['borrow_id']), f"{fine['amount']:.2f}", fine['status'], fine['date_issued']
            ])
            f.write(line + '\n')

# Helper functions

def get_next_id(data_dict):
    if not data_dict:
        return 1
    return max(data_dict.keys()) + 1


def calculate_due_date(borrow_date_str):
    try:
        borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d')
    except ValueError:
        borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    return due_date.strftime('%Y-%m-%d')


def get_current_date_str():
    return datetime.now().strftime('%Y-%m-%d')

# For simplicity, simulate a logged-in user (since no auth is described)
# In real app, integrate user session management
CURRENT_USER = 'john_reader'  # For demonstration, hardcoded username


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    books = read_books()
    featured_books = []
    # Let's define featured_books as first 5 books sorted by avg_rating descending
    sorted_books = sorted(books.values(), key=lambda b: b['avg_rating'], reverse=True)
    featured_books = sorted_books[:5]
    return render_template('dashboard.html', username=CURRENT_USER, featured_books=featured_books)


@app.route('/catalog')
def book_catalog():
    books = read_books()
    return render_template('catalog.html', books=list(books.values()))


@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    reviews_all = read_reviews()
    # Filter reviews for this book
    reviews = [r for r in reviews_all.values() if r['book_id'] == book_id]

    borrowings = read_borrowings()
    # Determine if user can borrow: if the book status is Available and user does not have an active borrow of this book
    user_active_borrows = [b for b in borrowings.values() if b['username'] == CURRENT_USER and b['book_id'] == book_id and b['status'] == 'Active']
    user_can_borrow = (book['status'] == 'Available' and len(user_active_borrows) == 0)

    return render_template('book_details.html', book=book, reviews=reviews, user_can_borrow=user_can_borrow)


@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_confirmation(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details', book_id=book_id))

    borrowings = read_borrowings()

    # Check if user already has active borrow of this book
    active_borrow_for_book = [b for b in borrowings.values() if b['username'] == CURRENT_USER and b['book_id'] == book_id and b['status'] == 'Active']
    if active_borrow_for_book:
        flash('You have already borrowed this book and not yet returned it.')
        return redirect(url_for('my_borrowings'))

    borrow_date = get_current_date_str()
    due_date = calculate_due_date(borrow_date)

    if request.method == 'POST':
        # Process borrowing
        borrow_id = get_next_id(borrowings)
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
        write_borrowings(borrowings)

        # Update book status to Borrowed
        book['status'] = 'Borrowed'
        books[book_id] = book
        write_books(books)

        flash('Book borrowed successfully. Due date: ' + due_date)
        return redirect(url_for('my_borrowings'))

    return render_template('borrow_confirmation.html', book=book, due_date=due_date)


@app.route('/my-borrows')
def my_borrowings():
    borrowings = read_borrowings()
    books = read_books()
    # Filter borrows of current user
    user_borrows = [b for b in borrowings.values() if b['username'] == CURRENT_USER]

    # Update statuses for overdue if needed
    today = datetime.now().date()
    updated = False
    for b in user_borrows:
        if b['status'] == 'Active' and b['due_date']:
            due_date_dt = datetime.strptime(b['due_date'], '%Y-%m-%d').date()
            if today > due_date_dt:
                b['status'] = 'Overdue'
                borrowings[b['borrow_id']]['status'] = 'Overdue'
                updated = True
    if updated:
        write_borrowings(borrowings)

    # Compose borrows list with book title
    borrows = []
    for b in user_borrows:
        book_title = books.get(b['book_id'], {}).get('title', 'Unknown')
        borrows.append({
            'borrow_id': b['borrow_id'],
            'book_title': book_title,
            'borrow_date': b['borrow_date'],
            'due_date': b['due_date'],
            'status': b['status']
        })

    return render_template('my_borrowings.html', borrows=borrows)


@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrowings = read_borrowings()
    borrow = borrowings.get(borrow_id)
    if not borrow or borrow['username'] != CURRENT_USER:
        flash('Borrow record not found or unauthorized.')
        return redirect(url_for('my_borrowings'))
    if borrow['status'] not in ('Active', 'Overdue'):
        flash('This borrow has already been returned or cancelled.')
        return redirect(url_for('my_borrowings'))

    books = read_books()
    book = books.get(borrow['book_id'])
    if not book:
        flash('Book record not found.')
        return redirect(url_for('my_borrowings'))

    # Calculate fine if overdue
    today_str = get_current_date_str()
    today = datetime.strptime(today_str, '%Y-%m-%d').date()
    due_date_dt = datetime.strptime(borrow['due_date'], '%Y-%m-%d').date()
    fine_amount = 0.0
    if today > due_date_dt:
        days_overdue = (today - due_date_dt).days
        # Assume fine is $1 per day overdue
        fine_amount = float(days_overdue)

    # Update borrow record
    borrow['return_date'] = today_str
    borrow['status'] = 'Returned'
    borrow['fine_amount'] = fine_amount
    borrowings[borrow_id] = borrow
    write_borrowings(borrowings)

    # Update book status to Available
    book['status'] = 'Available'
    books[borrow['book_id']] = book
    write_books(books)

    # If fine > 0 create fine record
    fines = read_fines()
    payment_success = False
    if fine_amount > 0:
        # Check if fine already exists for this borrow
        existing_fine = None
        for f in fines.values():
            if f['borrow_id'] == borrow_id and f['username'] == CURRENT_USER and f['status'] == 'Unpaid':
                existing_fine = f
                break
        if not existing_fine:
            fine_id = get_next_id(fines)
            new_fine = {
                'fine_id': fine_id,
                'username': CURRENT_USER,
                'borrow_id': borrow_id,
                'amount': fine_amount,
                'status': 'Unpaid',
                'date_issued': today_str
            }
            fines[fine_id] = new_fine
            write_fines(fines)
    else:
        payment_success = True

    return render_template('return_confirmation.html', borrow=borrow, fine_amount=fine_amount, return_success=True)


@app.route('/my-reservations')
def my_reservations():
    reservations = read_reservations()
    books = read_books()
    user_reservations = [r for r in reservations.values() if r['username'] == CURRENT_USER]
    reservations_list = []
    for r in user_reservations:
        book_title = books.get(r['book_id'], {}).get('title', 'Unknown')
        reservations_list.append({
            'reservation_id': r['reservation_id'],
            'book_title': book_title,
            'reservation_date': r['reservation_date'],
            'status': r['status']
        })
    return render_template('my_reservations.html', reservations=reservations_list)


@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    reservation = reservations.get(reservation_id)
    if not reservation or reservation['username'] != CURRENT_USER:
        flash('Reservation not found or unauthorized.')
        return redirect(url_for('my_reservations'))

    if reservation['status'] == 'Cancelled':
        cancel_success = False
    else:
        reservation['status'] = 'Cancelled'
        reservations[reservation_id] = reservation
        write_reservations(reservations)
        cancel_success = True

    return render_template('reservation_cancel.html', reservation_id=reservation_id, cancel_success=cancel_success)


@app.route('/my-reviews')
def my_reviews():
    reviews = read_reviews()
    books = read_books()
    user_reviews = [r for r in reviews.values() if r['username'] == CURRENT_USER]
    reviews_list = []
    for r in user_reviews:
        book_title = books.get(r['book_id'], {}).get('title', 'Unknown')
        reviews_list.append({
            'review_id': r['review_id'],
            'book_title': book_title,
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })
    return render_template('my_reviews.html', reviews=reviews_list)


@app.route('/write-review/<int:book_id>', methods=['GET', 'POST'])
def write_review(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    reviews = read_reviews()
    existing_review = None
    for r in reviews.values():
        if r['username'] == CURRENT_USER and r['book_id'] == book_id:
            existing_review = r
            break

    if request.method == 'POST':
        rating = request.form.get('rating')
        review_text = request.form.get('review_text', '').strip()

        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            flash('Rating must be an integer between 1 and 5.')
            return render_template('write_review.html', book=book, existing_review=existing_review)
        rating = int(rating)

        review_date = get_current_date_str()
        if existing_review:
            # Update existing
            existing_review['rating'] = rating
            existing_review['review_text'] = review_text
            existing_review['review_date'] = review_date
            reviews[existing_review['review_id']] = existing_review
            flash('Review updated successfully.')
        else:
            # Add new review
            review_id = get_next_id(reviews)
            new_review = {
                'review_id': review_id,
                'username': CURRENT_USER,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }
            reviews[review_id] = new_review
            flash('Review submitted successfully.')

        write_reviews(reviews)
        return redirect(url_for('book_details', book_id=book_id))

    return render_template('write_review.html', book=book, existing_review=existing_review)


@app.route('/edit-review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    reviews = read_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != CURRENT_USER:
        flash('Review not found or unauthorized.')
        return redirect(url_for('my_reviews'))

    books = read_books()
    book = books.get(review['book_id'])
    if not book:
        flash('Book not found.')
        return redirect(url_for('my_reviews'))

    if request.method == 'POST':
        rating = request.form.get('rating')
        review_text = request.form.get('review_text', '').strip()

        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            flash('Rating must be an integer between 1 and 5.')
            return render_template('write_review.html', book=book, existing_review=review)
        rating = int(rating)

        review['rating'] = rating
        review['review_text'] = review_text
        review['review_date'] = get_current_date_str()
        reviews[review_id] = review
        write_reviews(reviews)
        flash('Review updated successfully.')
        return redirect(url_for('my_reviews'))

    return render_template('write_review.html', book=book, existing_review=review)


@app.route('/delete-review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = read_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != CURRENT_USER:
        flash('Review not found or unauthorized.')
        return redirect(url_for('my_reviews'))

    del reviews[review_id]
    write_reviews(reviews)

    return render_template('review_delete_confirmation.html', review_id=review_id, delete_success=True)


@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    users = read_users()
    user = users.get(CURRENT_USER)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard_page'))

    if request.method == 'POST':
        new_email = request.form.get('email', '').strip()
        if new_email:
            user['email'] = new_email
            users[CURRENT_USER] = user
            write_users(users)
            flash('Email updated successfully.')
        else:
            flash('Email cannot be empty.')

    borrowings = read_borrowings()
    books = read_books()
    borrow_history = []
    for b in borrowings.values():
        if b['username'] == CURRENT_USER and b['status'] == 'Returned':
            book_title = books.get(b['book_id'], {}).get('title', 'Unknown')
            borrow_history.append({
                'book_title': book_title,
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })

    return render_template('profile.html', user=user, borrow_history=borrow_history)


@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment_confirmation(fine_id):
    fines = read_fines()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != CURRENT_USER:
        flash('Fine not found or unauthorized.')
        return redirect(url_for('user_profile'))

    payment_success = False
    if request.method == 'POST':
        if fine['status'] == 'Unpaid':
            fine['status'] = 'Paid'
            fines[fine_id] = fine
            write_fines(fines)
            payment_success = True
            flash('Payment successful.')
        else:
            flash('Fine has already been paid.')

    return render_template('payment_confirmation.html', fine=fine, payment_success=payment_success)


if __name__ == '__main__':
    app.run(debug=True)
