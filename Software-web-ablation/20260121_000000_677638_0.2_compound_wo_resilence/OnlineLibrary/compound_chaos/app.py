from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

data_dir = 'data'

# Helper functions to convert date formats

def str_to_date(dstr):
    try:
        return datetime.strptime(dstr, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None

def date_to_str(dateobj):
    return dateobj.strftime('%Y-%m-%d')

# Read and write functions for data files

def read_books():
    books = []
    path = os.path.join(data_dir, 'books.txt')
    if not os.path.exists(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 10:
                continue
            try:
                books.append({
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
                })
            except ValueError:
                continue
    return books

def write_books(books):
    path = os.path.join(data_dir, 'books.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for book in books:
            line = '|'.join([
                str(book['book_id']),
                book['title'],
                book['author'],
                book['isbn'],
                book['genre'],
                book['publisher'],
                str(book['year']),
                book['description'],
                book['status'],
                f"{book['avg_rating']:.2f}"
            ])
            f.write(line + '\n')


def read_users():
    users = []
    path = os.path.join(data_dir, 'users.txt')
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 4:
                continue
            users.append({
                'username': fields[0],
                'email': fields[1],
                'phone': fields[2],
                'address': fields[3]
            })
    return users

def write_users(users):
    path = os.path.join(data_dir, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for user in users:
            line = '|'.join([
                user['username'],
                user['email'],
                user['phone'],
                user['address']
            ])
            f.write(line + '\n')


def read_borrowings():
    borrowings = []
    path = os.path.join(data_dir, 'borrowings.txt')
    if not os.path.exists(path):
        return borrowings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 8:
                continue
            try:
                borrowings.append({
                    'borrow_id': int(fields[0]),
                    'username': fields[1],
                    'book_id': int(fields[2]),
                    'borrow_date': fields[3],
                    'due_date': fields[4],
                    'return_date': fields[5],
                    'status': fields[6],
                    'fine_amount': float(fields[7])
                })
            except ValueError:
                continue
    return borrowings

def write_borrowings(borrowings):
    path = os.path.join(data_dir, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for borrow in borrowings:
            line = '|'.join([
                str(borrow['borrow_id']),
                borrow['username'],
                str(borrow['book_id']),
                borrow['borrow_date'],
                borrow['due_date'],
                borrow['return_date'],
                borrow['status'],
                f"{borrow['fine_amount']:.2f}"
            ])
            f.write(line + '\n')


def read_reservations():
    reservations = []
    path = os.path.join(data_dir, 'reservations.txt')
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 5:
                continue
            try:
                reservations.append({
                    'reservation_id': int(fields[0]),
                    'username': fields[1],
                    'book_id': int(fields[2]),
                    'reservation_date': fields[3],
                    'status': fields[4]
                })
            except ValueError:
                continue
    return reservations

def write_reservations(reservations):
    path = os.path.join(data_dir, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for res in reservations:
            line = '|'.join([
                str(res['reservation_id']),
                res['username'],
                str(res['book_id']),
                res['reservation_date'],
                res['status']
            ])
            f.write(line + '\n')


def read_reviews():
    reviews = []
    path = os.path.join(data_dir, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 6:
                continue
            try:
                reviews.append({
                    'review_id': int(fields[0]),
                    'username': fields[1],
                    'book_id': int(fields[2]),
                    'rating': int(fields[3]),
                    'review_text': fields[4],
                    'review_date': fields[5]
                })
            except ValueError:
                continue
    return reviews

def write_reviews(reviews):
    path = os.path.join(data_dir, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for review in reviews:
            line = '|'.join([
                str(review['review_id']),
                review['username'],
                str(review['book_id']),
                str(review['rating']),
                review['review_text'],
                review['review_date']
            ])
            f.write(line + '\n')


def read_fines():
    fines = []
    path = os.path.join(data_dir, 'fines.txt')
    if not os.path.exists(path):
        return fines
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split('|')
            if len(fields) != 6:
                continue
            try:
                fines.append({
                    'fine_id': int(fields[0]),
                    'username': fields[1],
                    'borrow_id': int(fields[2]),
                    'amount': float(fields[3]),
                    'status': fields[4],
                    'date_issued': fields[5]
                })
            except ValueError:
                continue
    return fines

def write_fines(fines):
    path = os.path.join(data_dir, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fine in fines:
            line = '|'.join([
                str(fine['fine_id']),
                fine['username'],
                str(fine['borrow_id']),
                f"{fine['amount']:.2f}",
                fine['status'],
                fine['date_issued']
            ])
            f.write(line + '\n')


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('book_catalog_page'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/catalog')
def book_catalog_page():
    books = read_books()
    simple_books = [{
        'book_id': b['book_id'],
        'title': b['title'],
        'author': b['author'],
        'status': b['status']
    } for b in books]
    return render_template('catalog.html', books=simple_books)

@app.route('/book/<int:book_id>')
def book_details_page(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if book is None:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))
    # Get reviews for this book
    reviews = read_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=book_reviews)

@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def process_borrow_request(book_id):
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))

    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if book is None or book['status'] != 'Available':
        flash('Book not available for borrowing.')
        return redirect(url_for('book_catalog_page'))

    if request.method == 'GET':
        # Show borrow confirmation page
        due_date = datetime.now().date() + timedelta(days=14)
        due_date_str = date_to_str(due_date)
        return render_template('borrow_confirmation.html', book=book, due_date=due_date_str)

    if request.method == 'POST':
        current_user = session['username']
        borrowings = read_borrowings()
        # Ensure user does not have an active borrow for this book
        active_borrow = next((b for b in borrowings if b['username'] == current_user and b['book_id'] == book_id and b['status'] == 'Active'), None)
        if active_borrow:
            flash('You already have an active borrow for this book.')
            return redirect(url_for('my_borrowings_page'))

        # Update book status
        for b in books:
            if b['book_id'] == book_id:
                b['status'] = 'Borrowed'
                break
        write_books(books)

        new_borrow_id = max([b['borrow_id'] for b in borrowings] or [0]) + 1
        borrow_date = datetime.now().date()
        due_date = borrow_date + timedelta(days=14)
        new_borrow = {
            'borrow_id': new_borrow_id,
            'username': current_user,
            'book_id': book_id,
            'borrow_date': date_to_str(borrow_date),
            'due_date': date_to_str(due_date),
            'return_date': '',
            'status': 'Active',
            'fine_amount': 0.0
        }
        borrowings.append(new_borrow)
        write_borrowings(borrowings)
        flash('Book borrowed successfully.')
        return redirect(url_for('my_borrowings_page'))

@app.route('/my_borrows')
def my_borrowings_page():
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))
    current_user = session['username']
    borrowings = read_borrowings()
    books = read_books()

    borrow_context = []
    today = datetime.now().date()

    for b in borrowings:
        if b['username'] != current_user:
            continue
        book_title = next((bk['title'] for bk in books if bk['book_id'] == b['book_id']), 'Unknown')
        # Update status if overdue
        if b['status'] == 'Active':
            due_date_obj = str_to_date(b['due_date'])
            if due_date_obj and today > due_date_obj:
                b['status'] = 'Overdue'
        borrow_context.append({
            'borrow_id': b['borrow_id'],
            'book_id': b['book_id'],
            'title': book_title,
            'borrow_date': b['borrow_date'],
            'due_date': b['due_date'],
            'status': b['status'],
            'fine_amount': b['fine_amount']
        })
    return render_template('my_borrows.html', borrows=borrow_context)

@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))
    current_user = session['username']
    borrowings = read_borrowings()
    books = read_books()
    borrow = next((b for b in borrowings if b['borrow_id'] == borrow_id and b['username'] == current_user), None)
    if borrow is None:
        flash('Borrowing record not found.')
        return redirect(url_for('my_borrowings_page'))
    if borrow['status'] not in ['Active', 'Overdue']:
        flash('This borrow is not active or overdue.')
        return redirect(url_for('my_borrowings_page'))

    # Update borrow's return_date
    return_date = datetime.now().date()
    borrow['return_date'] = date_to_str(return_date)
    borrow['status'] = 'Returned'

    # Update book status to Available
    for b in books:
        if b['book_id'] == borrow['book_id']:
            b['status'] = 'Available'
            break

    # Calculate fine if overdue
    due_date_obj = str_to_date(borrow['due_date'])
    days_overdue = 0
    if due_date_obj and return_date > due_date_obj:
        days_overdue = (return_date - due_date_obj).days
    fine_amount = days_overdue * 1.0  # $1 per day overdue
    borrow['fine_amount'] = fine_amount

    write_borrowings(borrowings)
    write_books(books)

    # Create or update fine record if needed
    fines = read_fines()
    existing_fine = next((f for f in fines if f['borrow_id'] == borrow_id and f['username'] == current_user), None)
    if fine_amount > 0:
        if existing_fine:
            existing_fine['amount'] = fine_amount
            existing_fine['status'] = 'Unpaid'
            existing_fine['date_issued'] = date_to_str(return_date)
        else:
            new_fine_id = max([f['fine_id'] for f in fines] or [0]) + 1
            fines.append({
                'fine_id': new_fine_id,
                'username': current_user,
                'borrow_id': borrow_id,
                'amount': fine_amount,
                'status': 'Unpaid',
                'date_issued': date_to_str(return_date)
            })
        write_fines(fines)
        flash(f'Book returned with a fine of ${fine_amount:.2f}. Please pay it promptly.')
    else:
        if existing_fine:
            fines.remove(existing_fine)
            write_fines(fines)
        flash('Book returned successfully with no fines.')

    return redirect(url_for('my_borrowings_page'))

@app.route('/my_reservations')
def my_reservations_page():
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))
    current_user = session['username']
    reservations = read_reservations()
    books = read_books()

    reservation_context = []
    for r in reservations:
        if r['username'] != current_user:
            continue
        title = next((bk['title'] for bk in books if bk['book_id'] == r['book_id']), 'Unknown')
        reservation_context.append({
            'reservation_id': r['reservation_id'],
            'book_id': r['book_id'],
            'title': title,
            'reservation_date': r['reservation_date'],
            'status': r['status']
        })
    return render_template('my_reservations.html', reservations=reservation_context)

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))
    current_user = session['username']
    reservations = read_reservations()
    reservation = next((r for r in reservations if r['reservation_id'] == reservation_id and r['username'] == current_user), None)
    if reservation is None:
        flash('Reservation not found.')
        return redirect(url_for('my_reservations_page'))
    if reservation['status'] != 'Active':
        flash('Only active reservations can be cancelled.')
        return redirect(url_for('my_reservations_page'))

    # Mark reservation as Cancelled
    reservation['status'] = 'Cancelled'
    write_reservations(reservations)
    flash('Reservation cancelled successfully.')
    return redirect(url_for('my_reservations_page'))

@app.route('/my_reviews')
def my_reviews_page():
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))
    current_user = session['username']
    reviews = read_reviews()
    books = read_books()

    reviews_context = []
    for r in reviews:
        if r['username'] != current_user:
            continue
        book_title = next((bk['title'] for bk in books if bk['book_id'] == r['book_id']), 'Unknown')
        reviews_context.append({
            'review_id': r['review_id'],
            'book_id': r['book_id'],
            'book_title': book_title,
            'rating': r['rating'],
            'review_text': r['review_text']
        })
    return render_template('my_reviews.html', reviews=reviews_context)

@app.route('/write_review/<int:book_id>', methods=['GET', 'POST'])
def write_review_page(book_id):
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))
    current_user = session['username']
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog_page'))

    reviews = read_reviews()
    existing_review = next((r for r in reviews if r['username'] == current_user and r['book_id'] == book_id), None)

    if request.method == 'POST':
        try:
            rating_raw = request.form.get('rating')
            rating = int(rating_raw) if rating_raw and rating_raw.isdigit() and 1 <= int(rating_raw) <= 5 else 0
        except ValueError:
            rating = 0
        review_text = request.form.get('review_text', '').strip()

        if rating == 0 or not review_text:
            flash('Please provide a rating between 1 and 5 and a review text.')
            return render_template('write_review.html', book=book, existing_review=existing_review)

        today_str = date_to_str(datetime.now().date())

        if existing_review:
            # Update existing review
            existing_review['rating'] = rating
            existing_review['review_text'] = review_text
            existing_review['review_date'] = today_str
        else:
            new_review_id = max([r['review_id'] for r in reviews] or [0]) + 1
            new_review = {
                'review_id': new_review_id,
                'username': current_user,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': today_str
            }
            reviews.append(new_review)

        write_reviews(reviews)
        flash('Review submitted successfully.')
        return redirect(url_for('my_reviews_page'))

    # GET
    return render_template('write_review.html', book=book, existing_review=existing_review)

@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))
    current_user = session['username']
    reviews = read_reviews()
    review = next((r for r in reviews if r['review_id'] == review_id and r['username'] == current_user), None)
    if not review:
        flash('Review not found.')
        return redirect(url_for('my_reviews_page'))
    reviews.remove(review)
    write_reviews(reviews)
    flash('Review deleted successfully.')
    return redirect(url_for('my_reviews_page'))

@app.route('/profile')
def user_profile_page():
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))
    current_user = session['username']
    users = read_users()
    user_profile = next((u for u in users if u['username'] == current_user), None)
    if not user_profile:
        flash('User profile not found.')
        return redirect(url_for('dashboard_page'))

    # Borrow history
    borrowings = read_borrowings()
    books = read_books()
    borrow_history_context = []
    for b in borrowings:
        if b['username'] != current_user:
            continue
        if b['status'] != 'Returned':
            continue
        book_title = next((bk['title'] for bk in books if bk['book_id'] == b['book_id']), 'Unknown')
        borrow_history_context.append({
            'book_id': b['book_id'],
            'title': book_title,
            'borrow_date': b['borrow_date'],
            'return_date': b['return_date']
        })

    return render_template('profile.html', user_profile=user_profile, borrow_history=borrow_history_context)

@app.route('/profile/update', methods=['POST'])
def update_profile():
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))
    current_user = session['username']

    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    if not email or not phone or not address:
        flash('Please fill all fields.')
        return redirect(url_for('user_profile_page'))

    users = read_users()
    user = next((u for u in users if u['username'] == current_user), None)
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard_page'))

    user['email'] = email
    user['phone'] = phone
    user['address'] = address
    write_users(users)
    flash('Profile updated successfully.')
    return redirect(url_for('user_profile_page'))

@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment_confirmation_page(fine_id):
    if 'username' not in session:
        flash('Please login first.')
        return redirect(url_for('dashboard_page'))
    current_user = session['username']
    fines = read_fines()
    fine = next((f for f in fines if f['fine_id'] == fine_id and f['username'] == current_user), None)
    if not fine:
        flash('Fine record not found.')
        return redirect(url_for('user_profile_page'))

    if request.method == 'POST':
        # Update fine status to Paid
        fine['status'] = 'Paid'
        write_fines(fines)
        flash('Fine payment successful!')
        return redirect(url_for('user_profile_page'))
    # GET
    return render_template('payment_confirmation.html', fine=fine)

if __name__ == '__main__':
    app.run(debug=True)
