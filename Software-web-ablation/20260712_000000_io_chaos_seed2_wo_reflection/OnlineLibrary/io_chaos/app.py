from flask import Flask, render_template, redirect, url_for, request, flash
import os
import datetime

app = Flask(__name__)
app.secret_key = 'OnlineLibrarySecretKey'

# Data file paths
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
BORROWINGS_FILE = os.path.join(DATA_DIR, 'borrowings.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')
FINES_FILE = os.path.join(DATA_DIR, 'fines.txt')

# Simulated logged-in user (for demo purposes)
# In a real app, you'd have login and session management
LOGGED_IN_USERNAME = 'john_reader'

# Utility functions

def read_users():
    users = {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return users

def write_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            for u in users.values():
                line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
                f.write(line + '\n')
    except Exception as e:
        flash('Error writing users data: ' + str(e))


def read_books():
    books = {}
    try:
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
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
    except FileNotFoundError:
        pass
    return books

def write_books(books):
    try:
        with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
            for b in books.values():
                line = '|'.join([
                    str(b['book_id']),
                    b['title'],
                    b['author'],
                    b['isbn'],
                    b['genre'],
                    b['publisher'],
                    str(b['year']),
                    b['description'],
                    b['status'],
                    f"{b['avg_rating']:.1f}"
                ])
                f.write(line + '\n')
    except Exception as e:
        flash('Error writing books data: ' + str(e))


def read_borrowings():
    borrowings = {}
    try:
        with open(BORROWINGS_FILE, 'r', encoding='utf-8') as f:
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
                return_date = parts[5] if parts[5] else ''
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
                    'return_date': return_date if return_date else None,
                    'status': status,
                    'fine_amount': fine_amount
                }
    except FileNotFoundError:
        pass
    return borrowings

def write_borrowings(borrowings):
    try:
        with open(BORROWINGS_FILE, 'w', encoding='utf-8') as f:
            for b in borrowings.values():
                line = '|'.join([
                    str(b['borrow_id']),
                    b['username'],
                    str(b['book_id']),
                    b['borrow_date'],
                    b['due_date'],
                    b['return_date'] if b['return_date'] else '',
                    b['status'],
                    f"{b['fine_amount']:.2f}"
                ])
                f.write(line + '\n')
    except Exception as e:
        flash('Error writing borrowings data: ' + str(e))


def read_reservations():
    reservations = {}
    try:
        with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return reservations

def write_reservations(reservations):
    try:
        with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
            for r in reservations.values():
                line = '|'.join([
                    str(r['reservation_id']),
                    r['username'],
                    str(r['book_id']),
                    r['reservation_date'],
                    r['status']
                ])
                f.write(line + '\n')
    except Exception as e:
        flash('Error writing reservations data: ' + str(e))


def read_reviews():
    reviews = {}
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
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
    except FileNotFoundError:
        pass
    return reviews

def write_reviews(reviews):
    try:
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
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
    except Exception as e:
        flash('Error writing reviews data: ' + str(e))


def read_fines():
    fines = {}
    try:
        with open(FINES_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return fines

def write_fines(fines):
    try:
        with open(FINES_FILE, 'w', encoding='utf-8') as f:
            for fi in fines.values():
                line = '|'.join([
                    str(fi['fine_id']),
                    fi['username'],
                    str(fi['borrow_id']),
                    f"{fi['amount']:.2f}",
                    fi['status'],
                    fi['date_issued']
                ])
                f.write(line + '\n')
    except Exception as e:
        flash('Error writing fines data: ' + str(e))


def find_next_id(items_dict):
    if not items_dict:
        return 1
    return max(items_dict.keys()) + 1


def calculate_due_date(borrow_date_str):
    borrow_date = datetime.datetime.strptime(borrow_date_str, '%Y-%m-%d').date()
    due_date = borrow_date + datetime.timedelta(days=14)
    return due_date.strftime('%Y-%m-%d')


def today_str():
    return datetime.date.today().strftime('%Y-%m-%d')


def calculate_avg_rating(book_id, reviews):
    ratings = [r['rating'] for r in reviews.values() if r['book_id'] == book_id]
    if not ratings:
        return 0.0
    return round(sum(ratings) / len(ratings), 1)


def update_book_status(book_id, books, borrowings, reservations):
    # Priority: if book is currently borrowed (borrowings active and not returned) -> Borrowed
    # else if book is reserved by anyone active -> Reserved
    # else Available

    # Check active borrowings
    borrowed = False
    for b in borrowings.values():
        if b['book_id'] == book_id and b['status'] == 'Active':
            borrowed = True
            break

    if borrowed:
        books[book_id]['status'] = 'Borrowed'
        return

    # Check active reservations
    reserved = False
    for r in reservations.values():
        if r['book_id'] == book_id and r['status'] == 'Active':
            reserved = True
            break

    if reserved:
        books[book_id]['status'] = 'Reserved'
        return

    books[book_id]['status'] = 'Available'


def get_borrow_status(borrow):
    if borrow['status'] == 'Returned':
        return 'Returned'
    elif borrow['status'] == 'Overdue':
        return 'Overdue'
    elif borrow['status'] == 'Active':
        # Check if overdue by due date
        due = datetime.datetime.strptime(borrow['due_date'], '%Y-%m-%d').date()
        if datetime.date.today() > due:
            return 'Overdue'
        else:
            return 'Active'
    else:
        return borrow['status']


# ROUTES IMPLEMENTATION

# Route 1: Root Redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# Route 2: Dashboard Page
@app.route('/dashboard')
def dashboard():
    username = LOGGED_IN_USERNAME
    return render_template('dashboard.html', username=username)


# Route 3: Book Catalog Page
@app.route('/catalog')
def book_catalog():
    books = read_books()
    borrowings = read_borrowings()
    reservations = read_reservations()

    # Update all books' status
    for book_id in books:
        update_book_status(book_id, books, borrowings, reservations)

    # Prepare list of book dicts as specified
    books_list = []
    for book in books.values():
        books_list.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'status': book['status']
        })

    return render_template('catalog.html', books=books_list)


# Route 4: Book Details Page
@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    book = books[book_id]

    # Update status
    borrowings = read_borrowings()
    reservations = read_reservations()
    update_book_status(book_id, books, borrowings, reservations)

    # Get reviews for this book
    reviews_data = read_reviews()
    reviews = [
        {
            'review_id': r['review_id'],
            'username': r['username'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        }
        for r in reviews_data.values() if r['book_id'] == book_id
    ]

    return render_template('book_details.html', book=book, reviews=reviews)


# Route 5: Borrow Confirmation Page (GET)
@app.route('/borrow/<int:book_id>', methods=['GET'])
def borrow_book_get(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    book = books[book_id]

    # Check if the book status is available
    borrowings = read_borrowings()
    reservations = read_reservations()
    update_book_status(book_id, books, borrowings, reservations)

    if book['status'] != 'Available':
        flash('Book is not available to borrow.')
        return redirect(url_for('book_details', book_id=book_id))

    due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')

    return render_template('borrow_confirm.html', book=book, due_date=due_date)


# Route 6: Borrow Confirmation Page (POST)
@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book_post(book_id):
    books = read_books()
    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    book = books[book_id]
    borrowings = read_borrowings()
    reservations = read_reservations()
    update_book_status(book_id, books, borrowings, reservations)

    if book['status'] != 'Available':
        flash('Book is not available to borrow.')
        return redirect(url_for('book_details', book_id=book_id))

    username = LOGGED_IN_USERNAME

    # Create new borrow record
    borrow_date = today_str()
    due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')
    borrow_id = find_next_id(borrowings)

    new_borrow = {
        'borrow_id': borrow_id,
        'username': username,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }

    borrowings[borrow_id] = new_borrow

    # Update book status to borrowed
    books[book_id]['status'] = 'Borrowed'

    # Save data
    write_borrowings(borrowings)
    write_books(books)

    return render_template('borrow_confirmation.html', book=book, due_date=due_date, borrow_id=borrow_id)


# Route 7: My Borrowings Page
@app.route('/my-borrows')
def my_borrows():
    username = LOGGED_IN_USERNAME
    borrowings = read_borrowings()
    books = read_books()

    # Allow filter from query parameter
    filter_status = request.args.get('filter_status', 'All')

    # Update status if overdue
    for borrow in borrowings.values():
        if borrow['username'] == username and borrow['status'] == 'Active':
            due = datetime.datetime.strptime(borrow['due_date'], '%Y-%m-%d').date()
            if datetime.date.today() > due:
                borrow['status'] = 'Overdue'

    # Save updated statuses
    write_borrowings(borrowings)

    # Filter borrowings as per filter_status
    filtered_borrowings = []
    for borrow in borrowings.values():
        if borrow['username'] != username:
            continue
        status = get_borrow_status(borrow)
        if filter_status != 'All' and status != filter_status:
            continue
        # Get book title
        book_title = books.get(borrow['book_id'], {}).get('title', 'Unknown')

        filtered_borrowings.append({
            'borrow_id': borrow['borrow_id'],
            'book_title': book_title,
            'borrow_date': borrow['borrow_date'],
            'due_date': borrow['due_date'],
            'status': status
        })

    return render_template('my_borrows.html', borrowings=filtered_borrowings, filter_status=filter_status)


# Route 8: Return Borrowed Book (POST)
@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    username = LOGGED_IN_USERNAME
    borrowings = read_borrowings()
    books = read_books()

    if borrow_id not in borrowings:
        flash('Borrow record not found.')
        return redirect(url_for('my_borrows'))

    borrow = borrowings[borrow_id]
    if borrow['username'] != username:
        flash('You are not authorized to return this book.')
        return redirect(url_for('my_borrows'))

    if borrow['status'] == 'Returned':
        flash('This book has already been returned.')
        return redirect(url_for('my_borrows'))

    # Process return
    return_date = today_str()
    borrow['return_date'] = return_date
    borrow['status'] = 'Returned'

    # Update book status
    book_id = borrow['book_id']
    reservations = read_reservations()
    update_book_status(book_id, books, borrowings, reservations)

    # Save borrowings and books
    write_borrowings(borrowings)
    write_books(books)

    book_title = books.get(book_id, {}).get('title', 'Unknown')

    return render_template('return_confirmation.html', borrow_id=borrow_id, book_title=book_title, return_date=return_date)


# Route 9: My Reservations Page
@app.route('/my-reservations')
def my_reservations():
    username = LOGGED_IN_USERNAME
    reservations = read_reservations()
    books = read_books()

    user_reservations = []
    for res in reservations.values():
        if res['username'] == username:
            book_title = books.get(res['book_id'], {}).get('title', 'Unknown')
            user_reservations.append({
                'reservation_id': res['reservation_id'],
                'book_title': book_title,
                'reservation_date': res['reservation_date'],
                'status': res['status']
            })

    return render_template('my_reservations.html', reservations=user_reservations)


# Route 10: Cancel Reservation (POST)
@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = LOGGED_IN_USERNAME
    reservations = read_reservations()
    books = read_books()

    if reservation_id not in reservations:
        flash('Reservation not found.')
        return redirect(url_for('my_reservations'))

    reservation = reservations[reservation_id]
    if reservation['username'] != username:
        flash('You are not authorized to cancel this reservation.')
        return redirect(url_for('my_reservations'))

    if reservation['status'] == 'Cancelled':
        flash('Reservation is already cancelled.')
        return redirect(url_for('my_reservations'))

    # Mark as cancelled
    reservation['status'] = 'Cancelled'

    # Update book status
    book_id = reservation['book_id']
    borrowings = read_borrowings()
    update_book_status(book_id, books, borrowings, reservations)

    # Save changes
    write_reservations(reservations)
    write_books(books)

    book_title = books.get(book_id, {}).get('title', 'Unknown')

    return render_template('reservation_cancellation_confirmation.html', reservation_id=reservation_id, book_title=book_title)


# Route 11: My Reviews Page
@app.route('/my-reviews')
def my_reviews():
    username = LOGGED_IN_USERNAME
    reviews = read_reviews()
    books = read_books()

    user_reviews = []
    for r in reviews.values():
        if r['username'] == username:
            book_title = books.get(r['book_id'], {}).get('title', 'Unknown')
            user_reviews.append({
                'review_id': r['review_id'],
                'book_title': book_title,
                'rating': r['rating'],
                'review_text': r['review_text'],
                'book_id': r['book_id']
            })

    return render_template('my_reviews.html', reviews=user_reviews)


# Route 12: Write Review Page (GET)
@app.route('/write-review/<int:book_id>', methods=['GET'])
def write_review_get(book_id):
    username = LOGGED_IN_USERNAME
    books = read_books()
    reviews = read_reviews()

    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    book = books[book_id]

    # Check for existing review
    existing_review = None
    for r in reviews.values():
        if r['username'] == username and r['book_id'] == book_id:
            existing_review = {
                'review_id': r['review_id'],
                'rating': r['rating'],
                'review_text': r['review_text']
            }
            break

    return render_template('write_review.html', book=book, existing_review=existing_review)


# Route 13: Submit Review (POST)
@app.route('/write-review/<int:book_id>', methods=['POST'])
def write_review_post(book_id):
    username = LOGGED_IN_USERNAME
    books = read_books()
    reviews = read_reviews()

    if book_id not in books:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    book = books[book_id]

    rating_str = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()

    try:
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            raise ValueError
    except (ValueError, TypeError):
        flash('Invalid rating value. Must be an integer 1-5.')
        return redirect(url_for('write_review_get', book_id=book_id))

    if not review_text:
        flash('Review text cannot be empty.')
        return redirect(url_for('write_review_get', book_id=book_id))

    # Check existing review
    existing_review_id = None
    for r in reviews.values():
        if r['username'] == username and r['book_id'] == book_id:
            existing_review_id = r['review_id']
            break

    review_date = today_str()

    if existing_review_id is not None:
        # Update existing review
        reviews[existing_review_id]['rating'] = rating
        reviews[existing_review_id]['review_text'] = review_text
        reviews[existing_review_id]['review_date'] = review_date
        review_id = existing_review_id
    else:
        # Add new review
        review_id = find_next_id(reviews)
        reviews[review_id] = {
            'review_id': review_id,
            'username': username,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }

    # Save reviews
    write_reviews(reviews)

    # Update average rating for book
    avg_rating = calculate_avg_rating(book_id, reviews)
    books[book_id]['avg_rating'] = avg_rating
    write_books(books)

    return render_template('review_submission_confirmation.html', book=book, review_id=review_id)


# Route 14: User Profile Page (GET)
@app.route('/profile', methods=['GET'])
def user_profile():
    username = LOGGED_IN_USERNAME
    users = read_users()
    borrowings = read_borrowings()
    books = read_books()

    user_data = users.get(username)
    if not user_data:
        flash('User profile not found.')
        return redirect(url_for('dashboard'))

    # Build borrow history list: all borrowings with return_date or None
    borrow_history = []
    for borrow in borrowings.values():
        if borrow['username'] == username:
            book_title = books.get(borrow['book_id'], {}).get('title', 'Unknown')
            borrow_history.append({
                'book_title': book_title,
                'borrow_date': borrow['borrow_date'],
                'return_date': borrow['return_date']
            })

    return render_template('profile.html', username=username, email=user_data['email'], borrow_history=borrow_history)


# Route 15: Update User Profile (POST)
@app.route('/profile', methods=['POST'])
def update_profile():
    username = LOGGED_IN_USERNAME
    users = read_users()

    if username not in users:
        flash('User profile not found.')
        return redirect(url_for('dashboard'))

    email = request.form.get('email', '').strip()
    # We only update email as per spec
    if not email:
        flash('Email cannot be empty.')
        return redirect(url_for('user_profile'))

    users[username]['email'] = email
    write_users(users)

    return render_template('profile_update_confirmation.html', username=username, email=email)


# Route 16: Payment Confirmation Page (GET)
@app.route('/payment/<int:fine_id>', methods=['GET'])
def payment_confirmation_get(fine_id):
    username = LOGGED_IN_USERNAME
    fines = read_fines()

    if fine_id not in fines:
        flash('Fine record not found.')
        return redirect(url_for('user_profile'))

    fine = fines[fine_id]
    if fine['username'] != username:
        flash('You are not authorized to pay this fine.')
        return redirect(url_for('user_profile'))

    fine_info = {
        'fine_id': fine['fine_id'],
        'amount': fine['amount']
    }

    return render_template('payment_confirmation.html', fine=fine_info)


# Route 17: Payment Confirmation Page (POST)
@app.route('/payment/<int:fine_id>', methods=['POST'])
def payment_confirmation_post(fine_id):
    username = LOGGED_IN_USERNAME
    fines = read_fines()

    if fine_id not in fines:
        flash('Fine record not found.')
        return redirect(url_for('user_profile'))

    fine = fines[fine_id]
    if fine['username'] != username:
        flash('You are not authorized to pay this fine.')
        return redirect(url_for('user_profile'))

    # Mark fine as Paid
    fine['status'] = 'Paid'
    write_fines(fines)

    payment_status = 'Success'

    return render_template('payment_success.html', fine_id=fine_id, payment_status=payment_status)


if __name__ == '__main__':
    app.run(debug=True)
