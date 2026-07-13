from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'

# Utility Functions to read/write data files

def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

# Parse line by | delimiter

def parse_line(line):
    return line.split('|')

def join_line(fields):
    return '|'.join(str(field) for field in fields)

# Load all users into dict by username

def load_users():
    users = {}
    for line in read_file_lines('users.txt'):
        parts = parse_line(line)
        if len(parts) < 4:
            continue
        username, email, phone, address = parts
        users[username] = {'username': username, 'email': email, 'phone': phone, 'address': address}
    return users

# Load all books into dict by book_id

def load_books():
    books = {}
    for line in read_file_lines('books.txt'):
        parts = parse_line(line)
        if len(parts) < 10:
            continue
        book_id = parts[0]
        books[book_id] = {
            'book_id': book_id,
            'title': parts[1],
            'author': parts[2],
            'isbn': parts[3],
            'genre': parts[4],
            'publisher': parts[5],
            'year': parts[6],
            'description': parts[7],
            'status': parts[8],
            'avg_rating': parts[9],
        }
    return books

# Load borrowings by borrow_id

def load_borrowings():
    borrowings = {}
    for line in read_file_lines('borrowings.txt'):
        parts = parse_line(line)
        if len(parts) < 8:
            continue
        borrow_id = parts[0]
        borrowings[borrow_id] = {
            'borrow_id': borrow_id,
            'username': parts[1],
            'book_id': parts[2],
            'borrow_date': parts[3],
            'due_date': parts[4],
            'return_date': parts[5] if parts[5] else None,
            'status': parts[6],
            'fine_amount': float(parts[7]) if parts[7] else 0.0,
        }
    return borrowings

# Load reservations by reservation_id

def load_reservations():
    reservations = {}
    for line in read_file_lines('reservations.txt'):
        parts = parse_line(line)
        if len(parts) < 5:
            continue
        reservation_id = parts[0]
        reservations[reservation_id] = {
            'reservation_id': reservation_id,
            'username': parts[1],
            'book_id': parts[2],
            'reservation_date': parts[3],
            'status': parts[4],
        }
    return reservations

# Load reviews by review_id

def load_reviews():
    reviews = {}
    for line in read_file_lines('reviews.txt'):
        parts = parse_line(line)
        if len(parts) < 6:
            continue
        review_id = parts[0]
        reviews[review_id] = {
            'review_id': review_id,
            'username': parts[1],
            'book_id': parts[2],
            'rating': int(parts[3]),
            'review_text': parts[4],
            'review_date': parts[5],
        }
    return reviews

# Load fines by fine_id

def load_fines():
    fines = {}
    for line in read_file_lines('fines.txt'):
        parts = parse_line(line)
        if len(parts) < 6:
            continue
        fine_id = parts[0]
        fines[fine_id] = {
            'fine_id': fine_id,
            'username': parts[1],
            'borrow_id': parts[2],
            'amount': float(parts[3]),
            'status': parts[4],
            'date_issued': parts[5],
        }
    return fines

# Save all borrowings

def save_borrowings(borrowings):
    lines = []
    for b in borrowings.values():
        line = join_line([
            b['borrow_id'], b['username'], b['book_id'], b['borrow_date'], b['due_date'], b['return_date'] if b['return_date'] else '',
            b['status'], f"{b['fine_amount']:.2f}"
        ])
        lines.append(line)
    write_file_lines('borrowings.txt', lines)

# Save all reservations

def save_reservations(reservations):
    lines = []
    for r in reservations.values():
        line = join_line([
            r['reservation_id'], r['username'], r['book_id'], r['reservation_date'], r['status']
        ])
        lines.append(line)
    write_file_lines('reservations.txt', lines)

# Save all reviews

def save_reviews(reviews):
    lines = []
    for r in reviews.values():
        line = join_line([
            r['review_id'], r['username'], r['book_id'], str(r['rating']), r['review_text'], r['review_date']
        ])
        lines.append(line)
    write_file_lines('reviews.txt', lines)

# Save all fines

def save_fines(fines):
    lines = []
    for f in fines.values():
        line = join_line([
            f['fine_id'], f['username'], f['borrow_id'], f"{f['amount']:.2f}", f['status'], f['date_issued']
        ])
        lines.append(line)
    write_file_lines('fines.txt', lines)

# Save all users

def save_users(users):
    lines = []
    for u in users.values():
        line = join_line([
            u['username'], u['email'], u['phone'], u['address']
        ])
        lines.append(line)
    write_file_lines('users.txt', lines)

# Helpers

def get_next_id(items):
    # items is a dict with string-number keys
    if not items:
        return '1'
    max_id = max(int(k) for k in items.keys())
    return str(max_id + 1)

# Session management: For demo we fix login user
@app.before_request
def set_demo_user():
    if 'username' not in session:
        session['username'] = 'john_reader'  # demo logged in user

# Route: Dashboard
@app.route('/')
def dashboard():
    username = session['username']
    users = load_users()
    books = load_books()
    # featured books - for demo all books limited
    featured_books = list(books.values())[:5]
    return render_template('dashboard.html', username=username, featured_books=featured_books)

# Route: Book Catalog
@app.route('/catalog')
def catalog():
    username = session['username']
    query = request.args.get('search', '').lower()
    books = load_books()
    filtered_books = []
    if query:
        for b in books.values():
            if query in b['title'].lower() or query in b['author'].lower():
                filtered_books.append(b)
    else:
        filtered_books = list(books.values())
    return render_template('catalog.html', books=filtered_books, search_query=query)

# Route: Book Details
@app.route('/book/<book_id>')
def book_details(book_id):
    username = session['username']
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found')
        return redirect(url_for('catalog'))
    reviews = load_reviews()
    # Filter reviews for this book
    book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=book_reviews, username=username)

# Route: Borrow Confirmation
@app.route('/borrow/<book_id>', methods=['GET', 'POST'])
def borrow_book(book_id):
    username = session['username']
    books = load_books()
    book = books.get(book_id)
    if not book or book['status'] != 'Available':
        flash('Book not available for borrowing')
        return redirect(url_for('book_details', book_id=book_id))
    if request.method == 'POST':
        borrowings = load_borrowings()
        new_borrow_id = get_next_id(borrowings)
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=14)
        borrowings[new_borrow_id] = {
            'borrow_id': new_borrow_id,
            'username': username,
            'book_id': book_id,
            'borrow_date': borrow_date.isoformat(),
            'due_date': due_date.isoformat(),
            'return_date': None,
            'status': 'Active',
            'fine_amount': 0.0,
        }
        save_borrowings(borrowings)
        # Update book status to Borrowed
        book['status'] = 'Borrowed'
        books[book_id] = book
        # Save books
        lines = []
        for b in books.values():
            line = join_line([
                b['book_id'], b['title'], b['author'], b['isbn'], b['genre'], b['publisher'], b['year'], b['description'], b['status'], b['avg_rating']
            ])
            lines.append(line)
        write_file_lines('books.txt', lines)
        flash('Book borrowed successfully')
        return redirect(url_for('my_borrowings'))
    else:
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=14)
        return render_template('borrow_confirmation.html', book=book, borrow_date=borrow_date.isoformat(), due_date=due_date.isoformat())

# Route: My Borrowings
@app.route('/my_borrowings', methods=['GET', 'POST'])
def my_borrowings():
    username = session['username']
    borrowings = load_borrowings()
    books = load_books()
    filter_status = request.args.get('filter-status', 'All')
    # Filter borrowings for user
    user_borrows = [b for b in borrowings.values() if b['username'] == username]
    if filter_status != 'All':
        user_borrows = [b for b in user_borrows if b['status'] == filter_status]
    # If POST return book action
    if request.method == 'POST':
        ret_borrow_id = request.form.get('return_borrow_id')
        if ret_borrow_id and ret_borrow_id in borrowings:
            borrow = borrowings[ret_borrow_id]
            if borrow['status'] == 'Active':
                borrow['return_date'] = datetime.now().date().isoformat()
                borrow['status'] = 'Returned'
                borrowings[ret_borrow_id] = borrow
                save_borrowings(borrowings)
                # Update book status back to Available
                book_id = borrow['book_id']
                book = books.get(book_id)
                if book:
                    book['status'] = 'Available'
                    books[book_id] = book
                    # Save books
                    lines = []
                    for b in books.values():
                        line = join_line([
                            b['book_id'], b['title'], b['author'], b['isbn'], b['genre'], b['publisher'], b['year'], b['description'], b['status'], b['avg_rating']
                        ])
                        lines.append(line)
                    write_file_lines('books.txt', lines)
                    flash('Book returned successfully')
                    return redirect(url_for('my_borrowings'))
        flash('Invalid return request')
    return render_template('my_borrowings.html', borrowings=user_borrows, filter_status=filter_status, books=books)

# Route: My Reservations
@app.route('/my_reservations', methods=['GET', 'POST'])
def my_reservations():
    username = session['username']
    reservations = load_reservations()
    books = load_books()
    user_reservs = [r for r in reservations.values() if r['username'] == username]
    if request.method == 'POST':
        cancel_res_id = request.form.get('cancel_reservation_id')
        if cancel_res_id and cancel_res_id in reservations:
            r = reservations[cancel_res_id]
            if r['status'] == 'Active':
                r['status'] = 'Cancelled'
                reservations[cancel_res_id] = r
                save_reservations(reservations)
                flash('Reservation cancelled')
                return redirect(url_for('my_reservations'))
        flash('Invalid cancel request')
    return render_template('my_reservations.html', reservations=user_reservs, books=books)

# Route: My Reviews
@app.route('/my_reviews', methods=['GET', 'POST'])
def my_reviews():
    username = session['username']
    reviews = load_reviews()
    books = load_books()
    user_reviews = [r for r in reviews.values() if r['username'] == username]
    if request.method == 'POST':
        delete_review_id = request.form.get('delete_review_id')
        if delete_review_id and delete_review_id in reviews:
            r = reviews[delete_review_id]
            if r['username'] == username:
                del reviews[delete_review_id]
                save_reviews(reviews)
                flash('Review deleted')
                return redirect(url_for('my_reviews'))
        flash('Invalid delete request')
    return render_template('my_reviews.html', reviews=user_reviews, books=books)

# Route: Write Review
@app.route('/write_review/<book_id>', methods=['GET', 'POST'])
@app.route('/write_review/<book_id>/<review_id>', methods=['GET', 'POST'])
def write_review(book_id, review_id=None):
    username = session['username']
    books = load_books()
    book = books.get(book_id)
    if not book:
        flash('Book not found')
        return redirect(url_for('catalog'))

    reviews = load_reviews()
    is_edit = False
    review_data = {'rating': 1, 'review_text': ''}
    if review_id:
        review = reviews.get(review_id)
        if not review or review['username'] != username:
            flash('Review not found or access denied')
            return redirect(url_for('my_reviews'))
        is_edit = True
        review_data = review

    if request.method == 'POST':
        rating = int(request.form.get('rating-input', '1'))
        review_text = request.form.get('review-text', '').strip()
        if not review_text:
            flash('Review text cannot be empty')
            return render_template('write_review.html', book=book, review=review_data, is_edit=is_edit)
        curr_date = datetime.now().date().isoformat()

        if is_edit:
            reviews[review_id]['rating'] = rating
            reviews[review_id]['review_text'] = review_text
            reviews[review_id]['review_date'] = curr_date
        else:
            new_review_id = get_next_id(reviews)
            reviews[new_review_id] = {
                'review_id': new_review_id,
                'username': username,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': curr_date,
            }
        save_reviews(reviews)
        flash('Review submitted successfully')
        return redirect(url_for('book_details', book_id=book_id))

    return render_template('write_review.html', book=book, review=review_data, is_edit=is_edit)

# Route: User Profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session['username']
    users = load_users()
    borrowings = load_borrowings()
    user = users.get(username, {})
    user_borrows = [b for b in borrowings.values() if b['username'] == username ]

    if request.method == 'POST':
        new_email = request.form.get('profile-email','').strip()
        if new_email:
            user['email'] = new_email
            users[username] = user
            save_users(users)
            flash('Profile updated successfully')
        else:
            flash('Email cannot be empty')

    return render_template('profile.html', user=user, user_borrows=user_borrows)

# Route: Payment Confirmation
@app.route('/payment/<borrow_id>', methods=['GET', 'POST'])
def payment(borrow_id):
    username = session['username']
    borrowings = load_borrowings()
    borrow = borrowings.get(borrow_id)
    if not borrow or borrow['username'] != username:
        flash('Invalid fine payment request')
        return redirect(url_for('profile'))
    fines = load_fines()
    fine_to_pay = None
    for f in fines.values():
        if f['borrow_id'] == borrow_id and f['username'] == username and f['status'] == 'Unpaid':
            fine_to_pay = f
            break

    if not fine_to_pay or fine_to_pay['amount'] <= 0:
        flash('No unpaid fine for this borrow')
        return redirect(url_for('profile'))

    if request.method == 'POST':
        # Mark fine as paid
        fine_to_pay['status'] = 'Paid'
        fines[fine_to_pay['fine_id']] = fine_to_pay
        save_fines(fines)
        flash('Fine payment successful')
        return redirect(url_for('profile'))

    return render_template('payment_confirmation.html', fine=fine_to_pay)


if __name__ == '__main__':
    app.run(debug=True)
