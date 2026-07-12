from flask import Flask, request, render_template, redirect, url_for, flash, session
import datetime
import os

app = Flask(__name__)
app.secret_key = 'secret-key-for-session'

DATA_DIR = 'data'

# Utility: Read pipe-delimited file

def read_pipe_file(filename):
    filepath = os.path.join(DATA_DIR, filename)
    rows = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            rows = [line.strip().split('|') for line in f if line.strip()]
    return rows

def write_pipe_file(filename, rows):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write('|'.join(str(x) for x in row) + '\n')

# Current logged-in username

def current_username():
    return session.get('username', 'john_reader')

# USERS

def get_user(username):
    rows = read_pipe_file('users.txt')
    for r in rows:
        if r[0] == username:
            return {
                'username': r[0],
                'email': r[1],
                'phone': r[2],
                'address': r[3]
            }
    return None

# BOOKS

def get_all_books():
    rows = read_pipe_file('books.txt')
    books = []
    for r in rows:
        try:
            books.append({
                'book_id': int(r[0]),
                'title': r[1],
                'author': r[2],
                'isbn': r[3],
                'genre': r[4],
                'publisher': r[5],
                'year': int(r[6]),
                'description': r[7],
                'status': r[8],
                'avg_rating': float(r[9])
            })
        except Exception:
            continue
    return books

def get_book(book_id):
    for book in get_all_books():
        if book['book_id'] == book_id:
            return book
    return None

def update_book_status(book_id, status):
    rows = read_pipe_file('books.txt')
    updated = False
    for i, r in enumerate(rows):
        if int(r[0]) == book_id:
            r[8] = status
            rows[i] = r
            updated = True
            break
    if updated:
        write_pipe_file('books.txt', rows)
    return updated

# BORROWINGS

def get_all_borrowings():
    borrows = []
    rows = read_pipe_file('borrowings.txt')
    for r in rows:
        try:
            borrows.append({
                'borrow_id': int(r[0]),
                'username': r[1],
                'book_id': int(r[2]),
                'borrow_date': r[3],
                'due_date': r[4],
                'return_date': r[5],
                'status': r[6],
                'fine_amount': float(r[7])
            })
        except Exception:
            continue
    return borrows

def get_borrowing(borrow_id):
    for b in get_all_borrowings():
        if b['borrow_id'] == borrow_id:
            return b
    return None

def user_borrowings(username):
    return [b for b in get_all_borrowings() if b['username'] == username]

def add_borrowing(username, book_id):
    borrows = get_all_borrowings()
    next_id = max([b['borrow_id'] for b in borrows], default=0) + 1
    today = datetime.datetime.today()
    due = today + datetime.timedelta(days=14)
    new_borrow = {
        'borrow_id': next_id,
        'username': username,
        'book_id': book_id,
        'borrow_date': today.strftime('%Y-%m-%d'),
        'due_date': due.strftime('%Y-%m-%d'),
        'return_date': '',
        'status': 'Active',
        'fine_amount': 0.0
    }
    borrows.append(new_borrow)
    update_book_status(book_id, 'Borrowed')
    rows = []
    for b in borrows:
        rows.append([
            b['borrow_id'], b['username'], b['book_id'], b['borrow_date'], b['due_date'], b['return_date'], b['status'], f"{b['fine_amount']:.2f}"
        ])
    write_pipe_file('borrowings.txt', rows)
    return new_borrow

def update_borrowing(borrow_id, updates):
    borrows = get_all_borrowings()
    updated = False
    for b in borrows:
        if b['borrow_id'] == borrow_id:
            for k, v in updates.items():
                if k in b:
                    b[k] = v
                    updated = True
            break
    if updated:
        rows = []
        for b in borrows:
            rows.append([
                b['borrow_id'], b['username'], b['book_id'], b['borrow_date'], b['due_date'], b['return_date'], b['status'], f"{b['fine_amount']:.2f}"
            ])
        write_pipe_file('borrowings.txt', rows)
    return updated

# RESERVATIONS

def get_all_reservations():
    res_list = []
    rows = read_pipe_file('reservations.txt')
    for r in rows:
        try:
            res_list.append({
                'reservation_id': int(r[0]),
                'username': r[1],
                'book_id': int(r[2]),
                'reservation_date': r[3],
                'status': r[4]
            })
        except Exception:
            continue
    return res_list

def user_reservations(username):
    return [r for r in get_all_reservations() if r['username'] == username]

def update_reservation_status(reservation_id, status):
    rows = read_pipe_file('reservations.txt')
    updated = False
    for i, r in enumerate(rows):
        if int(r[0]) == reservation_id:
            r[4] = status
            rows[i] = r
            updated = True
            break
    if updated:
        write_pipe_file('reservations.txt', rows)
    return updated

# REVIEWS

def get_all_reviews():
    reviews = []
    rows = read_pipe_file('reviews.txt')
    for r in rows:
        try:
            reviews.append({
                'review_id': int(r[0]),
                'username': r[1],
                'book_id': int(r[2]),
                'rating': int(r[3]),
                'review_text': r[4],
                'review_date': r[5]
            })
        except Exception:
            continue
    return reviews

def get_user_book_review(username, book_id):
    for r in get_all_reviews():
        if r['username'] == username and r['book_id'] == book_id:
            return r
    return None

def add_or_update_review(username, book_id, rating, review_text):
    reviews = get_all_reviews()
    today_str = datetime.datetime.today().strftime('%Y-%m-%d')
    existing = get_user_book_review(username, book_id)
    if existing:
        for r in reviews:
            if r['review_id'] == existing['review_id']:
                r['rating'] = rating
                r['review_text'] = review_text
                r['review_date'] = today_str
                break
    else:
        new_id = max([r['review_id'] for r in reviews], default=0) + 1
        reviews.append({
            'review_id': new_id,
            'username': username,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': today_str
        })
    rows = []
    for r in reviews:
        rows.append([
            r['review_id'], r['username'], r['book_id'], r['rating'], r['review_text'], r['review_date']
        ])
    write_pipe_file('reviews.txt', rows)

# BORROW HISTORY

def get_borrow_history(username):
    history = []
    borrows = get_all_borrowings()
    for b in borrows:
        if b['username'] == username and b['status'] in ['Returned', 'Overdue']:
            book = get_book(b['book_id'])
            history.append({
                'book_title': book['title'] if book else 'Unknown',
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })
    return history


# ROUTES

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    username = current_username()
    books = get_all_books()
    return render_template('catalog.html', books=books, username=username)

@app.route('/catalog')
def book_catalog_page():
    books = get_all_books()
    return render_template('catalog.html', books=books)

@app.route('/book/<int:book_id>')
def book_details_page(book_id):
    book = get_book(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('dashboard_page'))
    reviews = [r for r in get_all_reviews() if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=reviews)

@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_confirmation_page(book_id):
    username = current_username()
    book = get_book(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('dashboard_page'))
    if request.method == 'GET':
        due_date = (datetime.datetime.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')
        simple_book = {'book_id': book['book_id'], 'title': book['title'], 'author': book['author']}
        return render_template('borrow_confirmation.html', book=simple_book, due_date=due_date)
    else:
        if book['status'] != 'Available':
            flash('Book is currently not available for borrowing.')
            return redirect(url_for('book_details_page', book_id=book_id))
        add_borrowing(username, book_id)
        flash('Book borrowing confirmed.')
        return redirect(url_for('book_details_page', book_id=book_id))

@app.route('/my_borrows')
def my_borrows_page():
    username = current_username()
    borrows = user_borrowings(username)
    today = datetime.datetime.today().date()
    for b in borrows:
        if b['status'] == 'Active':
            due = datetime.datetime.strptime(b['due_date'], '%Y-%m-%d').date()
            overdue_days = (today - due).days
            if overdue_days > 0:
                fine = overdue_days * 0.5
                b['fine_amount'] = fine
                b['status'] = 'Overdue'
                update_borrowing(b['borrow_id'], {'status': 'Overdue', 'fine_amount': fine})
        book = get_book(b['book_id'])
        b['book_title'] = book['title'] if book else 'Unknown'
    return render_template('my_borrows.html', borrows=borrows)

@app.route('/return_borrow/<int:borrow_id>', methods=['POST'])
def return_borrow(borrow_id):
    username = current_username()
    borrow = get_borrowing(borrow_id)
    if not borrow or borrow['username'] != username or borrow['status'] not in ['Active', 'Overdue']:
        flash('Invalid return request.')
        return redirect(url_for('my_borrows_page'))
    return_date = datetime.datetime.today().strftime('%Y-%m-%d')
    update_borrowing(borrow_id, {'return_date': return_date, 'status': 'Returned', 'fine_amount': 0.0})
    update_book_status(borrow['book_id'], 'Available')
    book = get_book(borrow['book_id'])
    confirmation_message = f'Book "{book["title"]}" returned successfully.'
    return render_template('return_confirmation.html', borrow_id=borrow_id, book_title=book['title'], confirmation_message=confirmation_message)

@app.route('/my_reservations')
def my_reservations_page():
    username = current_username()
    reservations = user_reservations(username)
    for r in reservations:
        book = get_book(r['book_id'])
        r['book_title'] = book['title'] if book else 'Unknown'
    return render_template('my_reservations.html', reservations=reservations)

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = current_username()
    reservations = user_reservations(username)
    target = None
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['status'] == 'Active':
            target = r
            break
    if not target:
        flash('Reservation not found or already cancelled.')
        return redirect(url_for('my_reservations_page'))
    update_reservation_status(reservation_id, 'Cancelled')
    flash('Reservation cancelled successfully.')
    return redirect(url_for('my_reservations_page'))

@app.route('/my_reviews', methods=['GET'])
def my_reviews_page():
    username = current_username()
    reviews = [r for r in get_all_reviews() if r['username'] == username]
    for r in reviews:
        book = get_book(r['book_id'])
        r['book_title'] = book['title'] if book else 'Unknown'
    return render_template('my_reviews.html', reviews=reviews)

@app.route('/write_review/<int:book_id>', methods=['GET', 'POST'])
def write_review_page(book_id):
    username = current_username()
    book = get_book(book_id)
    if not book:
        flash('Book not found.')
        return redirect(url_for('dashboard_page'))
    existing_review = get_user_book_review(username, book_id)
    if request.method == 'GET':
        return render_template('write_review.html', book=book, existing_review=existing_review)
    else:
        try:
            rating = int(request.form.get('rating'))
            review_text = request.form.get('review_text').strip()
            if rating < 1 or rating > 5:
                flash('Rating must be between 1 and 5.')
                return render_template('write_review.html', book=book, existing_review=existing_review)
            if not review_text:
                flash('Review text cannot be empty.')
                return render_template('write_review.html', book=book, existing_review=existing_review)
        except Exception:
            flash('Invalid input.')
            return render_template('write_review.html', book=book, existing_review=existing_review)
        add_or_update_review(username, book_id, rating, review_text)
        flash('Review submitted successfully.')
        return redirect(url_for('book_details_page', book_id=book_id))

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    username = current_username()
    user = get_user(username)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard_page'))
    if request.method == 'GET':
        borrow_history = get_borrow_history(username)
        return render_template('profile.html', user=user, borrow_history=borrow_history)
    else:
        new_email = request.form.get('email').strip()
        users = read_pipe_file('users.txt')
        updated = False
        for i, u in enumerate(users):
            if u[0] == username:
                u[1] = new_email
                users[i] = u
                updated = True
                break
        if updated:
            write_pipe_file('users.txt', users)
            flash('Profile updated successfully.')
        else:
            flash('User not found.')
        return redirect(url_for('profile_page'))

@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment_page(fine_id):
    username = current_username()
    fines = read_pipe_file('fines.txt')
    target_fine = None
    for i, f in enumerate(fines):
        if int(f[0]) == fine_id and f[1] == username and f[4] != 'Paid':
            target_fine = {'fine_id': int(f[0]), 'amount': float(f[3])}
            if request.method == 'POST':
                fines[i][4] = 'Paid'
                write_pipe_file('fines.txt', fines)
                flash('Payment successful.')
                return redirect(url_for('profile_page'))
            break
    if not target_fine:
        flash('Invalid or unauthorized payment.')
        return redirect(url_for('profile_page'))
    return render_template('payment_confirmation.html', fine=target_fine)

if __name__ == '__main__':
    app.run(debug=True)
