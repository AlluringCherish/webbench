from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATA_DIR = 'data'

# Helper functions to read and write data

def read_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def write_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

# Load users as dict by username

def load_users():
    lines = read_lines('users.txt')
    users = {}
    for line in lines:
        parts = line.split('|')
        if len(parts) >= 4:
            username, email, phone, address = parts
            users[username] = {
                'username': username,
                'email': email,
                'phone': phone,
                'address': address
            }
    return users

# Save users

def save_users(users):
    lines = []
    for u in users.values():
        line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
        lines.append(line)
    write_lines('users.txt', lines)

# Load books as dict by book_id

def load_books():
    lines = read_lines('books.txt')
    books = {}
    for line in lines:
        parts = line.split('|')
        if len(parts) >= 10:
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
                'avg_rating': float(parts[9]) if parts[9] else 0
            }
    return books

# Save books

def save_books(books):
    lines = []
    for b in books.values():
        line = '|'.join([
            b['book_id'], b['title'], b['author'], b['isbn'], b['genre'],
            b['publisher'], b['year'], b['description'], b['status'],
            '{:.1f}'.format(b['avg_rating'])
        ])
        lines.append(line)
    write_lines('books.txt', lines)

# Load borrowings as dict by borrow_id

def load_borrowings():
    lines = read_lines('borrowings.txt')
    borrowings = {}
    for line in lines:
        parts = line.split('|')
        if len(parts) >= 8:
            borrow_id = parts[0]
            borrowings[borrow_id] = {
                'borrow_id': borrow_id,
                'username': parts[1],
                'book_id': parts[2],
                'borrow_date': parts[3],
                'due_date': parts[4],
                'return_date': parts[5] if parts[5] else None,
                'status': parts[6],
                'fine_amount': float(parts[7])
            }
    return borrowings

# Save borrowings

def save_borrowings(borrowings):
    lines = []
    for b in borrowings.values():
        line = '|'.join([
            b['borrow_id'], b['username'], b['book_id'], b['borrow_date'],
            b['due_date'], b['return_date'] if b['return_date'] else '', b['status'],
            '{:.2f}'.format(b['fine_amount'])
        ])
        lines.append(line)
    write_lines('borrowings.txt', lines)

# Load reservations as dict by reservation_id

def load_reservations():
    lines = read_lines('reservations.txt')
    reservations = {}
    for line in lines:
        parts = line.split('|')
        if len(parts) >= 5:
            reservation_id = parts[0]
            reservations[reservation_id] = {
                'reservation_id': reservation_id,
                'username': parts[1],
                'book_id': parts[2],
                'reservation_date': parts[3],
                'status': parts[4]
            }
    return reservations

# Save reservations

def save_reservations(reservations):
    lines = []
    for r in reservations.values():
        line = '|'.join([
            r['reservation_id'], r['username'], r['book_id'], r['reservation_date'], r['status']
        ])
        lines.append(line)
    write_lines('reservations.txt', lines)

# Load reviews as dict by review_id

def load_reviews():
    lines = read_lines('reviews.txt')
    reviews = {}
    for line in lines:
        parts = line.split('|')
        if len(parts) >= 6:
            review_id = parts[0]
            reviews[review_id] = {
                'review_id': review_id,
                'username': parts[1],
                'book_id': parts[2],
                'rating': int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5]
            }
    return reviews

# Save reviews

def save_reviews(reviews):
    lines = []
    for r in reviews.values():
        line = '|'.join([
            r['review_id'], r['username'], r['book_id'], str(r['rating']), r['review_text'], r['review_date']
        ])
        lines.append(line)
    write_lines('reviews.txt', lines)

# Load fines as dict by fine_id

def load_fines():
    lines = read_lines('fines.txt')
    fines = {}
    for line in lines:
        parts = line.split('|')
        if len(parts) >= 6:
            fine_id = parts[0]
            fines[fine_id] = {
                'fine_id': fine_id,
                'username': parts[1],
                'borrow_id': parts[2],
                'amount': float(parts[3]),
                'status': parts[4],
                'date_issued': parts[5]
            }
    return fines

# Save fines

def save_fines(fines):
    lines = []
    for f in fines.values():
        line = '|'.join([
            f['fine_id'], f['username'], f['borrow_id'], '{:.2f}'.format(f['amount']), f['status'], f['date_issued']
        ])
        lines.append(line)
    write_lines('fines.txt', lines)

# Util: Get logged in username

def get_username():
    return session.get('username', None)

# Util: Require login

def require_login():
    if get_username() is None:
        return redirect(url_for('login'))

# Route: Simulated login (just enter username)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        users = load_users()
        if username in users:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Username not found')
    return render_template('login.html')

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# 1. Dashboard Page
@app.route('/')
@app.route('/dashboard')
def dashboard():
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    books = load_books()
    # Show some featured books (first 5)
    featured_books = list(books.values())[:5]
    return render_template('dashboard.html', username=username, featured_books=featured_books)

# 2. Book Catalog Page
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    books = load_books()
    search_term = ''
    filtered_books = list(books.values())
    if request.method == 'POST':
        search_term = request.form.get('search-input', '').strip().lower()
        if search_term:
            filtered_books = [b for b in filtered_books if search_term in b['title'].lower() or search_term in b['author'].lower()]
    return render_template('catalog.html', books=filtered_books, search_term=search_term)

# 3. Book Details Page
@app.route('/book/<book_id>')
def book_details(book_id):
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    books = load_books()
    book = books.get(book_id)
    if not book:
        return 'Book not found', 404
    reviews = load_reviews()
    book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=book_reviews)

# 4. Borrow Confirmation Page
@app.route('/borrow/<book_id>', methods=['GET', 'POST'])
def borrow_confirm(book_id):
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    books = load_books()
    book = books.get(book_id)
    if not book:
        return 'Book not found', 404
    if request.method == 'POST':
        # Confirm borrow
        borrowings = load_borrowings()
        new_id = str(max([int(k) for k in borrowings.keys()] + [0]) + 1)
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=14)
        borrowings[new_id] = {
            'borrow_id': new_id,
            'username': username,
            'book_id': book_id,
            'borrow_date': borrow_date.isoformat(),
            'due_date': due_date.isoformat(),
            'return_date': None,
            'status': 'Active',
            'fine_amount': 0.0
        }
        # Update book status
        book['status'] = 'Borrowed'
        save_borrowings(borrowings)
        books[book_id] = book
        save_books(books)
        return redirect(url_for('my_borrowings'))
    due_date_display = (datetime.now() + timedelta(days=14)).date()
    return render_template('borrow_confirmation.html', book=book, due_date=due_date_display)

# 5. My Borrowings Page
@app.route('/my-borrows', methods=['GET', 'POST'])
def my_borrows():
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    borrowings = load_borrowings()
    books = load_books()
    user_borrows = [b for b in borrowings.values() if b['username'] == username]

    filter_status = 'All'
    filtered_borrows = user_borrows
    if request.method == 'POST':
        filter_status = request.form.get('filter-status', 'All')
        if filter_status != 'All':
            filtered_borrows = [b for b in user_borrows if b['status'] == filter_status]

    # Enrich with book title
    for b in filtered_borrows:
        b['title'] = books.get(b['book_id'], {}).get('title', 'Unknown')
    return render_template('my_borrows.html', borrows=filtered_borrows, filter_status=filter_status)

# Return book
@app.route('/return/<borrow_id>', methods=['POST'])
def return_book(borrow_id):
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    borrowings = load_borrowings()
    books = load_books()
    borrowing = borrowings.get(borrow_id)
    if borrowing and borrowing['username'] == username and borrowing['status'] == 'Active':
        borrowing['status'] = 'Returned'
        borrowing['return_date'] = datetime.now().date().isoformat()
        borrowings[borrow_id] = borrowing

        # Update book status if no other active borrows
        active_borrows_for_book = [b for b in borrowings.values() if b['book_id'] == borrowing['book_id'] and b['status'] == 'Active']
        if not active_borrows_for_book:
            book = books.get(borrowing['book_id'])
            if book:
                book['status'] = 'Available'
                books[book['book_id']] = book
                save_books(books)

        save_borrowings(borrowings)
    return redirect(url_for('my_borrows'))

# 6. My Reservations Page
@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    reservations = load_reservations()
    books = load_books()
    user_reservations = [r for r in reservations.values() if r['username'] == username]
    
    # Handle cancel reservation post
    if request.method == 'POST':
        cancel_id = request.form.get('cancel_reservation_id')
        if cancel_id and cancel_id in reservations:
            reservations[cancel_id]['status'] = 'Cancelled'
            save_reservations(reservations)
            return redirect(url_for('my_reservations'))
    
    # Enrich
    for r in user_reservations:
        r['title'] = books.get(r['book_id'], {}).get('title', 'Unknown')
    return render_template('my_reservations.html', reservations=user_reservations)

# 7. My Reviews Page
@app.route('/my-reviews', methods=['GET'])
def my_reviews():
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    reviews = load_reviews()
    books = load_books()
    user_reviews = [r for r in reviews.values() if r['username'] == username]
    for r in user_reviews:
        r['title'] = books.get(r['book_id'], {}).get('title', 'Unknown')
    
    return render_template('my_reviews.html', reviews=user_reviews)

# Delete review
@app.route('/delete-review/<review_id>', methods=['POST'])
def delete_review(review_id):
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    reviews = load_reviews()
    if review_id in reviews and reviews[review_id]['username'] == username:
        del reviews[review_id]
        save_reviews(reviews)
    return redirect(url_for('my_reviews'))

# 8. Write Review Page
@app.route('/write-review/<book_id>', methods=['GET', 'POST'])
@app.route('/write-review/<book_id>/<review_id>', methods=['GET', 'POST'])
def write_review(book_id, review_id=None):
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    books = load_books()
    book = books.get(book_id)
    if not book:
        return 'Book not found', 404
    reviews = load_reviews()
    if review_id and review_id in reviews and reviews[review_id]['username'] == username:
        review = reviews[review_id]
    else:
        review = None

    if request.method == 'POST':
        rating = int(request.form.get('rating-input', 1))
        review_text = request.form.get('review-text', '').strip()
        review_date = datetime.now().date().isoformat()

        if review:  # Editing
            review['rating'] = rating
            review['review_text'] = review_text
            review['review_date'] = review_date
            reviews[review_id] = review
        else:  # New
            new_id = str(max([int(rid) for rid in reviews.keys()] + [0]) + 1)
            reviews[new_id] = {
                'review_id': new_id,
                'username': username,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }
        save_reviews(reviews)
        return redirect(url_for('book_details', book_id=book_id))

    return render_template('write_review.html', book=book, review=review)

# 9. User Profile Page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    users = load_users()
    user = users.get(username)

    if request.method == 'POST':
        # update email only
        new_email = request.form.get('profile-email', '').strip()
        if new_email and user:
            user['email'] = new_email
            users[username] = user
            save_users(users)
            flash('Profile updated successfully')
            return redirect(url_for('profile'))

    # Borrow history
    borrowings = load_borrowings()
    books = load_books()
    borrow_history = [b for b in borrowings.values() if b['username'] == username]
    for b in borrow_history:
        b['title'] = books.get(b['book_id'], {}).get('title', 'Unknown')
    return render_template('profile.html', user=user, borrow_history=borrow_history)

# 10. Payment Confirmation Page
@app.route('/payment/<borrow_id>', methods=['GET', 'POST'])
def payment_confirmation(borrow_id):
    username = get_username()
    if not username:
        return redirect(url_for('login'))
    borrowings = load_borrowings()
    fines = load_fines()
    borrowing = borrowings.get(borrow_id)
    if not borrowing or borrowing['username'] != username:
        return 'Borrowing not found or access denied', 404

    # Find unpaid fine for this borrow
    fine_to_pay = None
    for f in fines.values():
        if f['borrow_id'] == borrow_id and f['status'] == 'Unpaid':
            fine_to_pay = f
            break

    if not fine_to_pay:
        flash('No unpaid fine for this borrowing')
        return redirect(url_for('profile'))

    if request.method == 'POST':
        # Confirm payment
        fine_to_pay['status'] = 'Paid'
        save_fines(fines)
        return redirect(url_for('profile'))

    return render_template('payment_confirmation.html', fine=fine_to_pay)

if __name__ == '__main__':
    app.run(debug=True)
