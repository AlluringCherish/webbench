from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

DATA_DIR = 'data'

# Simulate current user
CURRENT_USER = 'john_reader'

# --- Data seeding for test data ---

def seed_test_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Seed books.txt with book_id=1
    books_path = os.path.join(DATA_DIR, 'books.txt')
    if not os.path.exists(books_path) or os.stat(books_path).st_size == 0:
        with open(books_path, 'w', encoding='utf-8') as f:
            # book_id|title|author|isbn|genre|publisher|year|description|status|avg_rating
            line = "1|The Great Gatsby|F. Scott Fitzgerald|9780743273565|Fiction|Scribner|1925|A classic novel.|Available|4.5\n"
            f.write(line)
    
    # Seed users.txt with john_reader
    users_path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(users_path) or os.stat(users_path).st_size == 0:
        with open(users_path, 'w', encoding='utf-8') as f:
            # username|email|phone|address
            line = "john_reader|john@example.com|1234567890|123 Fiction St\n"
            f.write(line)

    # Seed borrowings.txt with one active borrowing for book_id=1 by john_reader
    borrowings_path = os.path.join(DATA_DIR, 'borrowings.txt')
    if not os.path.exists(borrowings_path) or os.stat(borrowings_path).st_size == 0:
        with open(borrowings_path, 'w', encoding='utf-8') as f:
            # borrow_id|username|book_id|borrow_date|due_date|return_date|status|fine_amount
            borrow_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
            due_date = (datetime.now() + timedelta(days=9)).strftime('%Y-%m-%d')
            # Status Active means currently borrowed
            line = f"1|john_reader|1|{borrow_date}|{due_date}||Active|0.0\n"
            f.write(line)

    # Seed reservations.txt (empty or basic test)
    reservations_path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(reservations_path):
        with open(reservations_path, 'w', encoding='utf-8') as f:
            pass  # empty file

    # Seed reviews.txt with a review by john_reader for book_id=1
    reviews_path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(reviews_path) or os.stat(reviews_path).st_size == 0:
        with open(reviews_path, 'w', encoding='utf-8') as f:
            # review_id|username|book_id|rating|review_text|review_date
            review_date = datetime.now().strftime('%Y-%m-%d')
            line = f"1|john_reader|1|5|Excellent book!|{review_date}\n"
            f.write(line)

    # Seed fines.txt with a fine for borrow_id=1 and john_reader
    fines_path = os.path.join(DATA_DIR, 'fines.txt')
    if not os.path.exists(fines_path) or os.stat(fines_path).st_size == 0:
        with open(fines_path, 'w', encoding='utf-8') as f:
            # fine_id|username|borrow_id|amount|status|date_issued
            date_issued = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            line = f"1|john_reader|1|15.0|Unpaid|{date_issued}\n"
            f.write(line)

# Call data seeding at startup
seed_test_data()

# The rest of the app.py follows...
# (all original functions unchanged)


# (The original utility functions and route handlers come here unchanged)


def read_books():
    books = []
    path = os.path.join(DATA_DIR, 'books.txt')
    if not os.path.exists(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                fields = line.split('|')
                book = {
                    'book_id': int(fields[0]),
                    'title': fields[1],
                    'author': fields[2],
                    'isbn': fields[3],
                    'genre': fields[4],
                    'publisher': fields[5],
                    'year': int(fields[6]),
                    'description': fields[7],
                    'status': fields[8],
                    'avg_rating': float(fields[9])
                }
                books.append(book)
    return books

def read_users():
    users = {}
    path = os.path.join(DATA_DIR, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                fields = line.split('|')
                user = {
                    'username': fields[0],
                    'email': fields[1],
                    'phone': fields[2],
                    'address': fields[3]
                }
                users[user['username']] = user
    return users

def read_borrowings():
    borrowings = []
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    if not os.path.exists(path):
        return borrowings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                fields = line.split('|')
                borrow = {
                    'borrow_id': int(fields[0]),
                    'username': fields[1],
                    'book_id': int(fields[2]),
                    'borrow_date': fields[3],
                    'due_date': fields[4],
                    'return_date': fields[5],
                    'status': fields[6],
                    'fine_amount': float(fields[7])
                }
                borrowings.append(borrow)
    return borrowings

def write_borrowings(borrowings):
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in borrowings:
            row = f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{b['return_date']}|{b['status']}|{b['fine_amount']}\n"
            f.write(row)

def read_reservations():
    reservations = []
    path = os.path.join(DATA_DIR, 'reservations.txt')
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                fields = line.split('|')
                res = {
                    'reservation_id': int(fields[0]),
                    'username': fields[1],
                    'book_id': int(fields[2]),
                    'reservation_date': fields[3],
                    'status': fields[4]
                }
                reservations.append(res)
    return reservations

def write_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            row = f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}\n"
            f.write(row)

def read_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                fields = line.split('|')
                review = {
                    'review_id': int(fields[0]),
                    'username': fields[1],
                    'book_id': int(fields[2]),
                    'rating': int(fields[3]),
                    'review_text': fields[4],
                    'review_date': fields[5]
                }
                reviews.append(review)
    return reviews

def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            row = f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
            f.write(row)

def read_fines():
    fines = []
    path = os.path.join(DATA_DIR, 'fines.txt')
    if not os.path.exists(path):
        return fines
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line:
                fields = line.split('|')
                fine = {
                    'fine_id': int(fields[0]),
                    'username': fields[1],
                    'borrow_id': int(fields[2]),
                    'amount': float(fields[3]),
                    'status': fields[4],
                    'date_issued': fields[5]
                }
                fines.append(fine)
    return fines

def write_fines(fines):
    path = os.path.join(DATA_DIR, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fine in fines:
            row = f"{fine['fine_id']}|{fine['username']}|{fine['borrow_id']}|{fine['amount']}|{fine['status']}|{fine['date_issued']}\n"
            f.write(row)

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    username = CURRENT_USER
    return render_template('dashboard.html', username=username)

@app.route('/catalog', methods=['GET', 'POST'])
def book_catalog():
    search_query = ''
    books = read_books()
    if request.method == 'POST':
        search_query = request.form.get('search-input', '').lower()
        if search_query:
            books = [b for b in books if search_query in b['title'].lower() or search_query in b['author'].lower() or search_query in b['genre'].lower()]
    return render_template('catalog.html', books=books, search_query=search_query)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404
    reviews_all = read_reviews()
    reviews = [r for r in reviews_all if r['book_id'] == book_id]
    user_can_borrow = (book['status'].lower() == 'available')
    return render_template('book_details.html', book=book, reviews=reviews, user_can_borrow=user_can_borrow)

@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_confirm(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404
    if book['status'].lower() != 'available':
        return redirect(url_for('book_details', book_id=book_id))

    if request.method == 'POST':
        borrowings = read_borrowings()
        new_borrow_id = max([b['borrow_id'] for b in borrowings], default=0) + 1
        borrow_date = datetime.now().strftime('%Y-%m-%d')
        due_date_dt = datetime.now() + timedelta(days=14)
        due_date = due_date_dt.strftime('%Y-%m-%d')
        new_borrow = {
            'borrow_id': new_borrow_id,
            'username': CURRENT_USER,
            'book_id': book_id,
            'borrow_date': borrow_date,
            'due_date': due_date,
            'return_date': '',
            'status': 'Active',
            'fine_amount': 0.0
        }
        borrowings.append(new_borrow)
        write_borrowings(borrowings)

        # Update book status
        for b in books:
            if b['book_id'] == book_id:
                b['status'] = 'Borrowed'
        write_books(books=books)

        return redirect(url_for('my_borrowings'))

    borrow_date_dt = datetime.now()
    due_date_dt = borrow_date_dt + timedelta(days=14)
    due_date = due_date_dt.strftime('%Y-%m-%d')

    return render_template('borrow_confirmation.html', book=book, due_date=due_date)

@app.route('/my-borrowings', methods=['GET', 'POST'])
def my_borrowings():
    filter_status = 'All'
    borrowings = read_borrowings()
    books = read_books()
    borrows = []
    for b in borrowings:
        if b['username'] != CURRENT_USER:
            continue
        book_title = next((bk['title'] for bk in books if bk['book_id'] == b['book_id']), 'Unknown')
        borrows.append({
            'borrow_id': b['borrow_id'],
            'title': book_title,
            'borrow_date': b['borrow_date'],
            'due_date': b['due_date'],
            'status': b['status']
        })

    if request.method == 'POST':
        filter_status = request.form.get('filter-status', 'All')
        if 'return-book-button-' in request.form:
            for key in request.form.keys():
                if key.startswith('return-book-button-'):
                    bid_str = key[len('return-book-button-'):]
                    try:
                        bid = int(bid_str)
                    except:
                        bid = None
                    if bid is not None:
                        borrowings = read_borrowings()
                        for b in borrowings:
                            if b['borrow_id'] == bid and b['username'] == CURRENT_USER and b['status'] == 'Active':
                                b['status'] = 'Returned'
                                b['return_date'] = datetime.now().strftime('%Y-%m-%d')
                                books = read_books()
                                for bk in books:
                                    if bk['book_id'] == b['book_id']:
                                        bk['status'] = 'Available'
                                write_books(books)
                                write_borrowings(borrowings)
                                break
                        return redirect(url_for('dashboard'))
    if filter_status != 'All':
        borrows = [b for b in borrows if b['status'] == filter_status]

    return render_template('my_borrowings.html', borrows=borrows, filter_status=filter_status)

@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = read_reservations()
    books = read_books()
    reservations_user = []
    for r in reservations:
        if r['username'] != CURRENT_USER:
            continue
        title = next((b['title'] for b in books if b['book_id'] == r['book_id']), 'Unknown')
        r_data = {
            'reservation_id': r['reservation_id'],
            'title': title,
            'reservation_date': r['reservation_date'],
            'status': r['status']
        }
        reservations_user.append(r_data)

    if request.method == 'POST':
        for key in request.form.keys():
            if key.startswith('cancel-reservation-button-'):
                rid_str = key[len('cancel-reservation-button-'):]
                try:
                    rid = int(rid_str)
                except:
                    rid = None
                if rid is not None:
                    reservations = read_reservations()
                    for r in reservations:
                        if r['reservation_id'] == rid and r['username'] == CURRENT_USER and r['status'] == 'Active':
                            r['status'] = 'Canceled'
                            break
                    write_reservations(reservations)
                    return redirect(url_for('dashboard'))

    return render_template('my_reservations.html', reservations=reservations_user)

@app.route('/my-reviews', methods=['GET', 'POST'])
def my_reviews():
    reviews_all = read_reviews()
    reviews = [r for r in reviews_all if r['username'] == CURRENT_USER]
    books = read_books()

    if request.method == 'POST':
        for key in request.form.keys():
            if key.startswith('edit-review-button-'):
                rid_str = key[len('edit-review-button-'):]
                try:
                    rid = int(rid_str)
                except:
                    rid = None
                if rid is not None:
                    review = next((r for r in reviews if r['review_id'] == rid), None)
                    if review:
                        return redirect(url_for('write_review', book_id=review['book_id']))
            elif key.startswith('delete-review-button-'):
                rid_str = key[len('delete-review-button-'):]
                try:
                    rid = int(rid_str)
                except:
                    rid = None
                if rid is not None:
                    reviews_all = read_reviews()
                    reviews_all = [r for r in reviews_all if r['review_id'] != rid]
                    write_reviews(reviews_all)
                    return redirect(url_for('my_reviews'))

    return render_template('my_reviews.html', reviews=reviews)

@app.route('/review/write/<int:book_id>', methods=['GET', 'POST'])
def write_review(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404

    reviews = read_reviews()
    review = next((r for r in reviews if r['book_id'] == book_id and r['username'] == CURRENT_USER), None)

    if request.method == 'POST':
        rating = int(request.form.get('rating-input', 0))
        review_text = request.form.get('review-text', '').strip()
        now_str = datetime.now().strftime('%Y-%m-%d')
        reviews_all = read_reviews()
        if review:
            for r in reviews_all:
                if r['review_id'] == review['review_id']:
                    r['rating'] = rating
                    r['review_text'] = review_text
                    r['review_date'] = now_str
                    break
        else:
            new_review_id = max([r['review_id'] for r in reviews_all], default=0) + 1
            new_review = {
                'review_id': new_review_id,
                'username': CURRENT_USER,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': now_str
            }
            reviews_all.append(new_review)
        write_reviews(reviews_all)
        return redirect(url_for('book_details', book_id=book_id))

    return render_template('write_review.html', book=book, review=review)

@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    users = read_users()
    user_info = users.get(CURRENT_USER)
    if not user_info:
        return "User not found", 404

    borrowings = read_borrowings()
    books = read_books()
    borrow_history = []
    for b in borrowings:
        if b['username'] == CURRENT_USER:
            book_title = next((bk['title'] for bk in books if bk['book_id'] == b['book_id']), 'Unknown')
            borrow_history.append({
                'borrow_id': b['borrow_id'],
                'title': book_title,
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'return_date': b['return_date'],
                'status': b['status']
            })

    if request.method == 'POST':
        email = request.form.get('profile-email', '').strip()
        if email:
            user_info['email'] = email
            users[CURRENT_USER] = user_info
            path = os.path.join(DATA_DIR, 'users.txt')
            with open(path, 'w', encoding='utf-8') as f:
                for u in users.values():
                    row = f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}\n"
                    f.write(row)

    return render_template('user_profile.html', user_info=user_info, borrow_history=borrow_history)

@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment_confirmation(fine_id):
    fines = read_fines()
    fine = next((f for f in fines if f['fine_id'] == fine_id and f['username'] == CURRENT_USER), None)
    if not fine:
        return "Fine not found", 404

    if request.method == 'POST':
        fine['status'] = 'Paid'
        write_fines(fines)
        return redirect(url_for('user_profile'))

    return render_template('payment_confirmation.html', fine=fine)

if __name__ == '__main__':
    app.run(debug=True)
