from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Data load/save functions for all data types from peer app_debate_a.py implementation

def load_users():
    users = {}
    filepath = os.path.join(DATA_DIR, 'users.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    username, email, phone, address = parts
                    users[username] = {'username': username, 'email': email, 'phone': phone, 'address': address}
    return users

def save_users(users):
    filepath = os.path.join(DATA_DIR, 'users.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for user in users.values():
            f.write('|'.join([user['username'], user['email'], user['phone'], user['address']]) + '\n')


def load_books():
    books = {}
    filepath = os.path.join(DATA_DIR, 'books.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 10:
                    book_id_str, title, author, isbn, genre, publisher, year, description, status, avg_rating_str = parts
                    book_id = int(book_id_str)
                    try:
                        avg_rating = float(avg_rating_str)
                    except:
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

def save_books(books):
    filepath = os.path.join(DATA_DIR, 'books.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for book in books.values():
            line = '|'.join([
                str(book['book_id']),
                book['title'],
                book['author'],
                book['isbn'],
                book['genre'],
                book['publisher'],
                book['year'],
                book['description'],
                book['status'],
                str(book['avg_rating'])
            ])
            f.write(line + '\n')


def load_borrowings():
    borrowings = {}
    filepath = os.path.join(DATA_DIR, 'borrowings.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    borrow_id_str, username, book_id_str, borrow_date, due_date, return_date, status, fine_amount_str = parts
                    borrow_id = int(borrow_id_str)
                    book_id = int(book_id_str)
                    try:
                        fine_amount = float(fine_amount_str)
                    except:
                        fine_amount = 0.0
                    borrowings[borrow_id] = {
                        'borrow_id': borrow_id,
                        'username': username,
                        'book_id': book_id,
                        'borrow_date': borrow_date,
                        'due_date': due_date,
                        'return_date': return_date if return_date != 'None' else None,
                        'status': status,
                        'fine_amount': fine_amount
                    }
    return borrowings

def save_borrowings(borrowings):
    filepath = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for bor in borrowings.values():
            line = '|'.join([
                str(bor['borrow_id']),
                bor['username'],
                str(bor['book_id']),
                bor['borrow_date'],
                bor['due_date'],
                bor['return_date'] if bor['return_date'] else 'None',
                bor['status'],
                str(bor['fine_amount'])
            ])
            f.write(line + '\n')


def load_reservations():
    reservations = {}
    filepath = os.path.join(DATA_DIR, 'reservations.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    reservation_id_str, username, book_id_str, reservation_date, status = parts
                    reservation_id = int(reservation_id_str)
                    book_id = int(book_id_str)
                    reservations[reservation_id] = {
                        'reservation_id': reservation_id,
                        'username': username,
                        'book_id': book_id,
                        'reservation_date': reservation_date,
                        'status': status
                    }
    return reservations

def save_reservations(reservations):
    filepath = os.path.join(DATA_DIR, 'reservations.txt')
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


def load_reviews():
    reviews = {}
    filepath = os.path.join(DATA_DIR, 'reviews.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    review_id_str, username, book_id_str, rating_str, review_text, review_date = parts
                    review_id = int(review_id_str)
                    book_id = int(book_id_str)
                    try:
                        rating = int(rating_str)
                    except:
                        rating = 0
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
    filepath = os.path.join(DATA_DIR, 'reviews.txt')
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


def load_fines():
    fines = {}
    filepath = os.path.join(DATA_DIR, 'fines.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    fine_id_str, username, borrow_id_str, amount_str, status, date_issued = parts
                    fine_id = int(fine_id_str)
                    borrow_id = int(borrow_id_str)
                    try:
                        amount = float(amount_str)
                    except:
                        amount = 0.0
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
    filepath = os.path.join(DATA_DIR, 'fines.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for fine in fines.values():
            line = '|'.join([
                str(fine['fine_id']),
                fine['username'],
                str(fine['borrow_id']),
                str(fine['amount']),
                fine['status'],
                fine['date_issued']
            ])
            f.write(line + '\n')


# Current user hardcoded as per design
CURRENT_USER = 'testuser'


@app.route('/')
@app.route('/dashboard')
def dashboard():
    users = load_users()
    user = users.get(CURRENT_USER, {'username': CURRENT_USER})
    return render_template('dashboard.html', username=user['username'])


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    books = load_books()
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        if search_query:
            filtered_books = {}
            for book_id, book in books.items():
                if search_query.lower() in book['title'].lower() or search_query.lower() in book['author'].lower():
                    filtered_books[book_id] = book
            books = filtered_books
    return render_template('catalog.html', books=books.values(), search_query=search_query)


@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        return "Book not found", 404

    reviews = load_reviews()
    book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]

    return render_template('book_details.html', book=book, reviews=book_reviews)


@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        return "Book not found", 404

    if request.method == 'POST':
        borrowings = load_borrowings()
        new_borrow_id = 1
        if borrowings:
            new_borrow_id = max(borrowings.keys()) + 1
        borrow_date = datetime.now().strftime('%Y-%m-%d')
        due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        new_borrow = {
            'borrow_id': new_borrow_id,
            'username': CURRENT_USER,
            'book_id': book_id,
            'borrow_date': borrow_date,
            'due_date': due_date,
            'return_date': None,
            'status': 'Borrowed',
            'fine_amount': 0.0
        }
        borrowings[new_borrow_id] = new_borrow
        save_borrowings(borrowings)

        book['status'] = 'Borrowed'
        books[book_id] = book
        save_books(books)

        return redirect(url_for('my_borrows'))

    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    return render_template('borrow_confirmation.html', book=book, due_date=due_date)


@app.route('/my-borrows', methods=['GET', 'POST'])
def my_borrows():
    filter_status = ''
    if request.method == 'POST':
        filter_status = request.form.get('filter_status', '')

    borrowings = load_borrowings()
    books = load_books()
    filtered_borrows = []
    for bor in borrowings.values():
        if bor['username'] == CURRENT_USER:
            if filter_status and bor['status'] != filter_status:
                continue
            bor_copy = bor.copy()
            bor_copy['book'] = books.get(bor['book_id'])
            filtered_borrows.append(bor_copy)

    return render_template('my_borrows.html', borrows=filtered_borrows, filter_status=filter_status)


@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrowings = load_borrowings()
    bor = borrowings.get(borrow_id)
    if not bor or bor['username'] != CURRENT_USER:
        return "Borrow record not found", 404

    if bor['status'] == 'Returned':
        return redirect(url_for('my_borrows'))

    return_date = datetime.now().strftime('%Y-%m-%d')
    bor['return_date'] = return_date
    bor['status'] = 'Returned'

    due_date_dt = datetime.strptime(bor['due_date'], '%Y-%m-%d')
    return_dt = datetime.strptime(return_date, '%Y-%m-%d')
    delta_days = (return_dt - due_date_dt).days
    fine_amount = 0.0
    if delta_days > 0:
        fine_amount = delta_days * 1.0

    bor['fine_amount'] = fine_amount
    borrowings[borrow_id] = bor
    save_borrowings(borrowings)

    books = load_books()
    book = books.get(bor['book_id'])
    if book:
        book['status'] = 'Available'
        books[book['book_id']] = book
        save_books(books)

    if fine_amount > 0:
        fines = load_fines()
        existing_fine_id = None
        for f in fines.values():
            if f['borrow_id'] == borrow_id and f['username'] == CURRENT_USER and f['status'] == 'Unpaid':
                existing_fine_id = f['fine_id']
                break
        if existing_fine_id is None:
            new_fine_id = 1 if not fines else max(fines.keys()) + 1
            new_fine = {
                'fine_id': new_fine_id,
                'username': CURRENT_USER,
                'borrow_id': borrow_id,
                'amount': fine_amount,
                'status': 'Unpaid',
                'date_issued': datetime.now().strftime('%Y-%m-%d')
            }
            fines[new_fine_id] = new_fine
            save_fines(fines)

    return redirect(url_for('my_borrows'))


@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = load_reservations()
    books = load_books()

    user_reservations = [r for r in reservations.values() if r['username'] == CURRENT_USER]

    if request.method == 'POST':
        for key in request.form.keys():
            if key.startswith('cancel-reservation-button-'):
                res_id = int(key.replace('cancel-reservation-button-', ''))
                if res_id in reservations and reservations[res_id]['username'] == CURRENT_USER:
                    reservations[res_id]['status'] = 'Cancelled'
                    save_reservations(reservations)
                    break
        return redirect(url_for('my_reservations'))

    enriched_reservations = []
    for r in user_reservations:
        rcp = r.copy()
        rcp['book'] = books.get(r['book_id'])
        enriched_reservations.append(rcp)

    return render_template('my_reservations.html', reservations=enriched_reservations)


@app.route('/my-reviews', methods=['GET', 'POST'])
def my_reviews():
    reviews = load_reviews()
    books = load_books()
    user_reviews = [r for r in reviews.values() if r['username'] == CURRENT_USER]

    if request.method == 'POST':
        for key in request.form.keys():
            if key.startswith('delete-review-button-'):
                review_id = int(key.replace('delete-review-button-', ''))
                if review_id in reviews and reviews[review_id]['username'] == CURRENT_USER:
                    del reviews[review_id]
                    save_reviews(reviews)
                    break
        return redirect(url_for('my_reviews'))

    enriched_reviews = []
    for r in user_reviews:
        rcp = r.copy()
        book = books.get(r['book_id'])
        rcp['book'] = book
        enriched_reviews.append(rcp)

    return render_template('my_reviews.html', reviews=enriched_reviews)


@app.route('/write-review/<int:book_id>', methods=['GET', 'POST'])
def write_review(book_id):
    books = load_books()
    book = books.get(book_id)
    if not book:
        return "Book not found", 404

    reviews = load_reviews()
    existing_review = None
    for r in reviews.values():
        if r['username'] == CURRENT_USER and r['book_id'] == book_id:
            existing_review = r
            break

    if request.method == 'POST':
        rating_str = request.form.get('rating', '0')
        review_text = request.form.get('review_text', '').strip()
        try:
            rating = int(rating_str)
        except:
            rating = 0

        if existing_review:
            existing_review['rating'] = rating
            existing_review['review_text'] = review_text
            existing_review['review_date'] = datetime.now().strftime('%Y-%m-%d')
        else:
            new_review_id = 1 if not reviews else max(reviews.keys()) + 1
            new_review = {
                'review_id': new_review_id,
                'username': CURRENT_USER,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': datetime.now().strftime('%Y-%m-%d')
            }
            reviews[new_review_id] = new_review

        save_reviews(reviews)

        book_reviews = [r for r in reviews.values() if r['book_id'] == book_id]
        if book_reviews:
            avg_rating = sum(r['rating'] for r in book_reviews) / len(book_reviews)
            book['avg_rating'] = round(avg_rating, 2)
            books[book_id] = book
            save_books(books)

        return redirect(url_for('book_details', book_id=book_id))

    return render_template('write_review.html', book=book, existing_review=existing_review)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = load_users()
    user = users.get(CURRENT_USER, {'username': CURRENT_USER, 'email': '', 'phone': '', 'address': ''})

    borrowings = load_borrowings()
    books = load_books()
    borrow_history = []
    for bor in borrowings.values():
        if bor['username'] == CURRENT_USER:
            b = books.get(bor['book_id'])
            entry = bor.copy()
            entry['book'] = b
            borrow_history.append(entry)

    if request.method == 'POST':
        new_email = request.form.get('profile-email', '').strip()
        if new_email:
            user['email'] = new_email
            users[CURRENT_USER] = user
            save_users(users)

        return redirect(url_for('profile'))

    return render_template('profile.html', username=user['username'], email=user.get('email', ''), borrow_history=borrow_history)


@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment(fine_id):
    fines = load_fines()
    fine = fines.get(fine_id)
    if not fine:
        return "Fine not found", 404

    if request.method == 'POST':
        if fine['status'] == 'Unpaid':
            fine['status'] = 'Paid'
            fines[fine_id] = fine
            save_fines(fines)
        return redirect(url_for('profile'))

    return render_template('payment_confirmation.html', fine=fine)


if __name__ == '__main__':
    app.run(debug=True)
