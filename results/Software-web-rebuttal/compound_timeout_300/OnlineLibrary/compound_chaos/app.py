from flask import Flask, render_template, redirect, url_for, request, flash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_sessions'

DATA_PATH = 'data'

# Helper functions to read/write pipe-delimited files

# 1. Users (username|email|phone|address)
def read_users():
    users = {}
    path = os.path.join(DATA_PATH, 'users.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                username,email,phone,address = line.split('|')
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
    path = os.path.join(DATA_PATH, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for user in users.values():
            f.write(f"{user['username']}|{user['email']}|{user['phone']}|{user['address']}\n")

# 2. Books (book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating)
def read_books():
    books = {}
    path = os.path.join(DATA_PATH, 'books.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                book_id = int(parts[0])
                books[book_id] = {
                    'book_id': book_id,
                    'title': parts[1],
                    'author': parts[2],
                    'isbn': parts[3],
                    'genre': parts[4],
                    'publisher': parts[5],
                    'year': int(parts[6]),
                    'description': parts[7],
                    'status': parts[8],
                    'avg_rating': float(parts[9])
                }
    except FileNotFoundError:
        pass
    return books

def write_books(books):
    path = os.path.join(DATA_PATH, 'books.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for book in books.values():
            f.write(f"{book['book_id']}|{book['title']}|{book['author']}|{book['isbn']}|{book['genre']}|{book['publisher']}|{book['year']}|{book['description']}|{book['status']}|{book['avg_rating']}\n")

# 3. Borrowings (borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount)
def read_borrowings():
    borrowings = {}
    path = os.path.join(DATA_PATH, 'borrowings.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                borrow_id = int(parts[0])
                borrowings[borrow_id] = {
                    'borrow_id': borrow_id,
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'borrow_date': parts[3],
                    'due_date': parts[4],
                    'return_date': parts[5] if parts[5] else None,
                    'status': parts[6],
                    'fine_amount': float(parts[7])
                }
    except FileNotFoundError:
        pass
    return borrowings

def write_borrowings(borrowings):
    path = os.path.join(DATA_PATH, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in borrowings.values():
            return_date_val = b['return_date'] if b['return_date'] else ''
            f.write(f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{return_date_val}|{b['status']}|{b['fine_amount']}\n")

# 4. Reservations (reservation_id|username|book_id|reservation_date|status)
def read_reservations():
    reservations = {}
    path = os.path.join(DATA_PATH, 'reservations.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                reservation_id = int(parts[0])
                reservations[reservation_id] = {
                    'reservation_id': reservation_id,
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'reservation_date': parts[3],
                    'status': parts[4]
                }
    except FileNotFoundError:
        pass
    return reservations

def write_reservations(reservations):
    path = os.path.join(DATA_PATH, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations.values():
            f.write(f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}\n")

# 5. Reviews (review_id|username|book_id|rating|review_text|review_date)
def read_reviews():
    reviews = {}
    path = os.path.join(DATA_PATH, 'reviews.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                review_id = int(parts[0])
                reviews[review_id] = {
                    'review_id': review_id,
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
    except FileNotFoundError:
        pass
    return reviews

def write_reviews(reviews):
    path = os.path.join(DATA_PATH, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for rev in reviews.values():
            f.write(f"{rev['review_id']}|{rev['username']}|{rev['book_id']}|{rev['rating']}|{rev['review_text']}|{rev['review_date']}\n")

# 6. Fines (fine_id|username|borrow_id|amount|status|date_issued)
def read_fines():
    fines = {}
    path = os.path.join(DATA_PATH, 'fines.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                fine_id = int(parts[0])
                fines[fine_id] = {
                    'fine_id': fine_id,
                    'username': parts[1],
                    'borrow_id': int(parts[2]),
                    'amount': float(parts[3]),
                    'status': parts[4],
                    'date_issued': parts[5]
                }
    except FileNotFoundError:
        pass
    return fines

def write_fines(fines):
    path = os.path.join(DATA_PATH, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fine in fines.values():
            f.write(f"{fine['fine_id']}|{fine['username']}|{fine['borrow_id']}|{fine['amount']}|{fine['status']}|{fine['date_issued']}\n")

# Session emulation: For this assignment, assume a fixed logged-in user "john_reader" for demonstration
LOGGED_IN_USER = 'john_reader'

# Route Implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    username = LOGGED_IN_USER
    return render_template('dashboard.html', username=username)

@app.route('/catalog')
def book_catalog():
    books_all = read_books()
    books = []
    for book in books_all.values():
        # status for template: Available, Borrowed, Reserved
        book_status = book['status']
        books.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'status': book_status
        })
    return render_template('catalog.html', books=books)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    reviews_all = read_reviews()
    reviews = []
    for review in reviews_all.values():
        if review['book_id'] == book_id:
            reviews.append({
                'review_id': review['review_id'],
                'username': review['username'],
                'rating': review['rating'],
                'review_text': review['review_text'],
                'review_date': review['review_date']
            })

    return render_template('book_details.html', book=book, reviews=reviews)

@app.route('/borrow/<int:book_id>')
def borrow_confirmation(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    if book['status'] != 'Available':
        flash('Book is not available for borrowing.')
        return redirect(url_for('book_details', book_id=book_id))

    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    book_brief = {'book_id': book['book_id'], 'title': book['title']}
    return render_template('borrow_confirmation.html', book=book_brief, due_date=due_date)

@app.route('/borrow/confirm', methods=['POST'])
def confirm_borrow():
    book_id = request.form.get('book_id')
    if not book_id or not book_id.isdigit():
        flash('Invalid book id.')
        return redirect(url_for('book_catalog'))
    book_id = int(book_id)

    books = read_books()
    book = books.get(book_id)
    if not book or book['status'] != 'Available':
        flash('Book not available.')
        return redirect(url_for('book_catalog'))

    borrowings = read_borrowings()
    # new borrow_id
    new_borrow_id = max(borrowings.keys(), default=0) + 1
    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')

    # create new borrow entry
    borrowings[new_borrow_id] = {
        'borrow_id': new_borrow_id,
        'username': LOGGED_IN_USER,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }

    # update book status to Borrowed
    books[book_id]['status'] = 'Borrowed'

    # Write back
    try:
        write_borrowings(borrowings)
        write_books(books)
        flash('Book borrowed successfully.')
    except Exception:
        flash('Error occurred while borrowing the book.')

    return redirect(url_for('my_borrowings'))

@app.route('/borrows')
def my_borrowings():
    borrowings_all = read_borrowings()
    books = read_books()
    borrows = []
    for borrow in borrowings_all.values():
        if borrow['username'] == LOGGED_IN_USER:
            # Calculate status dynamically
            status = borrow['status']

            # Overdue check
            if status == 'Active':
                due_date_obj = datetime.strptime(borrow['due_date'], '%Y-%m-%d')
                now = datetime.now()
                if now > due_date_obj:
                    status = 'Overdue'

            borrows.append({
                'borrow_id': borrow['borrow_id'],
                'title': books.get(borrow['book_id'], {}).get('title', 'Unknown'),
                'borrow_date': borrow['borrow_date'],
                'due_date': borrow['due_date'],
                'status': status,
                'fine_amount': borrow['fine_amount']
            })
    return render_template('my_borrowings.html', borrows=borrows)

@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrowings = read_borrowings()
    borrow = borrowings.get(borrow_id)
    if not borrow or borrow['username'] != LOGGED_IN_USER:
        flash('Borrow record not found or unauthorized.')
        return redirect(url_for('my_borrowings'))

    if borrow['status'] != 'Active' and borrow['status'] != 'Overdue':
        flash('Cannot return book. Borrow is not active or overdue.')
        return redirect(url_for('my_borrowings'))

    books = read_books()
    book = books.get(borrow['book_id'])
    if not book:
        flash('Book record not found.')
        return redirect(url_for('my_borrowings'))

    # Set return date
    return_date = datetime.now().strftime('%Y-%m-%d')
    borrow['return_date'] = return_date

    # Update status to Returned
    borrow['status'] = 'Returned'

    # Update book status to Available
    book['status'] = 'Available'

    # Calculate fine if overdue
    due_date_obj = datetime.strptime(borrow['due_date'], '%Y-%m-%d')
    return_date_obj = datetime.strptime(return_date, '%Y-%m-%d')
    overdue_days = (return_date_obj - due_date_obj).days
    fine_amount = 0.0
    if overdue_days > 0:
        fine_amount = overdue_days * 0.5  # Assuming $0.5 per day overdue
        borrow['fine_amount'] = fine_amount

        fines = read_fines()
        new_fine_id = max(fines.keys(), default=0) + 1
        fine_entry = {
            'fine_id': new_fine_id,
            'username': LOGGED_IN_USER,
            'borrow_id': borrow['borrow_id'],
            'amount': fine_amount,
            'status': 'Unpaid',
            'date_issued': return_date
        }
        fines[new_fine_id] = fine_entry
        try:
            write_fines(fines)
        except Exception:
            flash('Error saving fine information.')

    # Write back borrowings and books
    try:
        write_borrowings(borrowings)
        write_books(books)
        flash('Book returned successfully.')
    except Exception:
        flash('Error updating return.')

    return redirect(url_for('my_borrowings'))

@app.route('/reservations')
def my_reservations():
    reservations_all = read_reservations()
    books = read_books()
    reservations = []
    for res in reservations_all.values():
        if res['username'] == LOGGED_IN_USER:
            reservations.append({
                'reservation_id': res['reservation_id'],
                'title': books.get(res['book_id'], {}).get('title', 'Unknown'),
                'reservation_date': res['reservation_date'],
                'status': res['status']
            })
    return render_template('my_reservations.html', reservations=reservations)

@app.route('/reservation/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    reservation = reservations.get(reservation_id)
    if not reservation or reservation['username'] != LOGGED_IN_USER:
        flash('Reservation not found or unauthorized.')
        return redirect(url_for('my_reservations'))

    # Update status to Cancelled
    if reservation['status'] != 'Cancelled':
        reservation['status'] = 'Cancelled'
        try:
            write_reservations(reservations)
            flash('Reservation cancelled successfully.')
        except Exception:
            flash('Error cancelling reservation.')

    return redirect(url_for('my_reservations'))

@app.route('/reviews')
def my_reviews():
    reviews_all = read_reviews()
    books = read_books()
    reviews = []
    for rev in reviews_all.values():
        if rev['username'] == LOGGED_IN_USER:
            reviews.append({
                'review_id': rev['review_id'],
                'book_title': books.get(rev['book_id'], {}).get('title', 'Unknown'),
                'rating': rev['rating'],
                'review_text': rev['review_text']
            })
    return render_template('my_reviews.html', reviews=reviews)

@app.route('/review/write/<int:book_id>')
def write_review(book_id):
    books = read_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    return render_template('write_review.html', book={'book_id': book['book_id'], 'title': book['title']})

@app.route('/review/submit', methods=['POST'])
def submit_review():
    book_id = request.form.get('book_id')
    rating = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()
    review_id = request.form.get('review_id')  # Optional for editing

    if not book_id or not book_id.isdigit():
        flash('Invalid book id.')
        return redirect(url_for('book_catalog'))
    book_id = int(book_id)

    if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
        flash('Rating must be an integer between 1 and 5.')
        return redirect(url_for('book_details', book_id=book_id))
    rating = int(rating)

    reviews = read_reviews()
    now_str = datetime.now().strftime('%Y-%m-%d')

    if review_id and review_id.isdigit():
        # Edit existing review
        rid = int(review_id)
        if rid in reviews and reviews[rid]['username'] == LOGGED_IN_USER:
            reviews[rid]['rating'] = rating
            reviews[rid]['review_text'] = review_text
            reviews[rid]['review_date'] = now_str
            try:
                write_reviews(reviews)
                flash('Review updated successfully.')
            except Exception:
                flash('Error updating review.')
            return redirect(url_for('my_reviews'))
        else:
            flash('Review not found or unauthorized.')
            return redirect(url_for('my_reviews'))
    else:
        # New review
        new_review_id = max(reviews.keys(), default=0) + 1
        reviews[new_review_id] = {
            'review_id': new_review_id,
            'username': LOGGED_IN_USER,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': now_str
        }
        try:
            write_reviews(reviews)
            flash('Review submitted successfully.')
        except Exception:
            flash('Error saving review.')
        return redirect(url_for('my_reviews'))

@app.route('/review/edit/<int:review_id>')
def edit_review(review_id):
    reviews = read_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != LOGGED_IN_USER:
        flash('Review not found or unauthorized.')
        return redirect(url_for('my_reviews'))

    books = read_books()
    book = books.get(review['book_id'])
    if not book:
        flash('Book not found.')
        return redirect(url_for('my_reviews'))

    book_brief = {'book_id': book['book_id'], 'title': book['title']}
    review_brief = {
        'review_id': review['review_id'],
        'rating': review['rating'],
        'review_text': review['review_text']
    }

    return render_template('write_review.html', book=book_brief, review=review_brief)

@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = read_reviews()
    review = reviews.get(review_id)
    if not review or review['username'] != LOGGED_IN_USER:
        flash('Review not found or unauthorized.')
        return redirect(url_for('my_reviews'))

    del reviews[review_id]
    try:
        write_reviews(reviews)
        flash('Review deleted successfully.')
    except Exception:
        flash('Error deleting review.')

    return redirect(url_for('my_reviews'))

@app.route('/profile')
def user_profile():
    users = read_users()
    user = users.get(LOGGED_IN_USER)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard'))

    borrowings_all = read_borrowings()
    books = read_books()
    borrow_history = []
    for borrow in borrowings_all.values():
        if borrow['username'] == LOGGED_IN_USER and borrow['status'] == 'Returned':
            borrow_history.append({
                'book_title': books.get(borrow['book_id'], {}).get('title', 'Unknown'),
                'borrow_date': borrow['borrow_date'],
                'return_date': borrow['return_date'] if borrow['return_date'] else None
            })

    return render_template('profile.html', username=LOGGED_IN_USER, email=user['email'], borrow_history=borrow_history)

@app.route('/profile/update', methods=['POST'])
def update_profile():
    email = request.form.get('email', '').strip()
    if not email:
        flash('Email cannot be empty.')
        return redirect(url_for('user_profile'))

    users = read_users()
    if LOGGED_IN_USER in users:
        users[LOGGED_IN_USER]['email'] = email
        try:
            write_users(users)
            flash('Profile updated successfully.')
        except Exception:
            flash('Error updating profile.')

    else:
        flash('User not found.')

    return redirect(url_for('user_profile'))

@app.route('/payment/<int:fine_id>')
def payment_confirmation(fine_id):
    fines = read_fines()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != LOGGED_IN_USER:
        flash('Fine not found or unauthorized.')
        return redirect(url_for('user_profile'))

    return render_template('payment_confirmation.html', fine={'fine_id': fine['fine_id'], 'amount': fine['amount']})

@app.route('/payment/confirm/<int:fine_id>', methods=['POST'])
def confirm_payment(fine_id):
    fines = read_fines()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != LOGGED_IN_USER:
        flash('Fine not found or unauthorized.')
        return redirect(url_for('user_profile'))

    if fine['status'] != 'Paid':
        fine['status'] = 'Paid'
        try:
            write_fines(fines)
            flash('Payment confirmed. Thank you!')
        except Exception:
            flash('Error processing payment.')

    return redirect(url_for('user_profile'))

if __name__ == '__main__':
    app.run(debug=True)
