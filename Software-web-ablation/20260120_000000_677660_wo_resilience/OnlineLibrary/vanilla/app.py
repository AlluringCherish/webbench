from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'

# Helper functions to load and save pipe-delimited data files

# Users: username | email | phone | address

def load_users():
    path = os.path.join(DATA_DIR, 'users.txt')
    users = []
    if not os.path.exists(path):
        return users
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            user = {
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3]
            }
            users.append(user)
    return users

def save_users(users):
    path = os.path.join(DATA_DIR, 'users.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for u in users:
            line = '|'.join([u['username'], u['email'], u['phone'], u['address']])
            f.write(line + '\n')

# Books: book_id | title | author | isbn | genre | publisher | year | description | status | avg_rating

def load_books():
    path = os.path.join(DATA_DIR, 'books.txt')
    books = []
    if not os.path.exists(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 10:
                continue
            try:
                book = {
                    'book_id': int(parts[0]),
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
            except:
                continue
            books.append(book)
    return books

def save_books(books):
    path = os.path.join(DATA_DIR, 'books.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in books:
            line = '|'.join([
                str(b['book_id']), b['title'], b['author'], b['isbn'], b['genre'], b['publisher'],
                str(b['year']), b['description'], b['status'], '{0:.1f}'.format(b['avg_rating'])])
            f.write(line + '\n')

# Borrowings: borrow_id | username | book_id | borrow_date | due_date | return_date | status | fine_amount

def load_borrowings():
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    borrowings = []
    if not os.path.exists(path):
        return borrowings
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            try:
                borrow = {
                    'borrow_id': int(parts[0]),
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'borrow_date': parts[3],
                    'due_date': parts[4],
                    'return_date': parts[5] if parts[5] else None,
                    'status': parts[6],
                    'fine_amount': float(parts[7])
                }
            except:
                continue
            borrowings.append(borrow)
    return borrowings

def save_borrowings(borrowings):
    path = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in borrowings:
            line = '|'.join([
                str(b['borrow_id']), b['username'], str(b['book_id']), b['borrow_date'], b['due_date'],
                b['return_date'] if b['return_date'] else '', b['status'], '{0:.2f}'.format(b['fine_amount'])])
            f.write(line + '\n')

# Reservations: reservation_id | username | book_id | reservation_date | status

def load_reservations():
    path = os.path.join(DATA_DIR, 'reservations.txt')
    reservations = []
    if not os.path.exists(path):
        return reservations
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                res = {
                    'reservation_id': int(parts[0]),
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'reservation_date': parts[3],
                    'status': parts[4]
                }
            except:
                continue
            reservations.append(res)
    return reservations

def save_reservations(reservations):
    path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reservations:
            line = '|'.join([
                str(r['reservation_id']), r['username'], str(r['book_id']), r['reservation_date'], r['status']])
            f.write(line + '\n')

# Reviews: review_id | username | book_id | rating | review_text | review_date

def load_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                rev = {
                    'review_id': int(parts[0]),
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
            except:
                continue
            reviews.append(rev)
    return reviews

def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = '|'.join([
                str(r['review_id']), r['username'], str(r['book_id']), str(r['rating']), r['review_text'], r['review_date']])
            f.write(line + '\n')

# Fines: fine_id | username | borrow_id | amount | status | date_issued

def load_fines():
    path = os.path.join(DATA_DIR, 'fines.txt')
    fines = []
    if not os.path.exists(path):
        return fines
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                fine = {
                    'fine_id': int(parts[0]),
                    'username': parts[1],
                    'borrow_id': int(parts[2]),
                    'amount': float(parts[3]),
                    'status': parts[4],
                    'date_issued': parts[5]
                }
            except:
                continue
            fines.append(fine)
    return fines

def save_fines(fines):
    path = os.path.join(DATA_DIR, 'fines.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for fobj in fines:
            line = '|'.join([
                str(fobj['fine_id']), fobj['username'], str(fobj['borrow_id']), '{0:.2f}'.format(fobj['amount']), fobj['status'], fobj['date_issued']])
            f.write(line + '\n')

# Utility functions

def get_next_id(list_of_dicts, key):
    if not list_of_dicts:
        return 1
    return max(d[key] for d in list_of_dicts) + 1


def current_username():
    # In a real app, get username from session
    # For this backend-only demo, we'll mock by a fixed username
    return session.get('username', 'john_reader')


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    username = current_username()
    books = load_books()
    # Featured books: Show first 5 books
    featured_books = []
    for b in books[:5]:
        featured_books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': b['status']
        })
    return render_template('dashboard.html', username=username, featured_books=featured_books)

@app.route('/catalog')
def book_catalog():
    books = load_books()
    query = request.args.get('query', '')
    # Filter by query if provided (case insensitive in title or author)
    filtered_books = []
    if query:
        query_lower = query.lower()
        for b in books:
            if query_lower in b['title'].lower() or query_lower in b['author'].lower():
                filtered_books.append({
                    'book_id': b['book_id'],
                    'title': b['title'],
                    'author': b['author'],
                    'status': b['status']
                })
    else:
        filtered_books = [{
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'status': b['status']
        } for b in books]
    return render_template('catalog.html', books=filtered_books, query=query)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    books = load_books()
    book = None
    for b in books:
        if b['book_id'] == book_id:
            book = b
            break
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    reviews = load_reviews()
    book_reviews = []
    for r in reviews:
        if r['book_id'] == book_id:
            book_reviews.append({
                'review_id': r['review_id'], 
                'username': r['username'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })
    return render_template('book_details.html', book=book, reviews=book_reviews)

@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_book(book_id):
    username = current_username()
    books = load_books()
    book = None
    for b in books:
        if b['book_id'] == book_id:
            book = {'book_id': b['book_id'], 'title': b['title'], 'author': b['author']}
            book_full = b
            break
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    if request.method == 'GET':
        due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        return render_template('borrow_confirmation.html', book=book, due_date=due_date)

    # POST: Confirm borrowing
    borrowings = load_borrowings()
    # Check if book status allows borrow
    # Allowed only if status is 'Available'
    if book_full['status'] != 'Available':
        return render_template('borrow_confirmation.html', book=book, due_date='',
                               borrow_success=False, error_message='Book is not available for borrowing.')

    # Check if user already has active borrow for this book
    for borrow in borrowings:
        if borrow['username'] == username and borrow['book_id'] == book_id and borrow['status'] == 'Active':
            return render_template('borrow_confirmation.html', book=book, due_date='',
                                   borrow_success=False, error_message='You have already borrowed this book and it is active.')

    next_id = get_next_id(borrowings, 'borrow_id')
    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    new_borrow = {
        'borrow_id': next_id,
        'username': username,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'return_date': None,
        'status': 'Active',
        'fine_amount': 0.0
    }
    borrowings.append(new_borrow)
    save_borrowings(borrowings)

    # Update book status to Borrowed
    for b in books:
        if b['book_id'] == book_id:
            b['status'] = 'Borrowed'
            break
    save_books(books)

    return render_template('borrow_confirmation.html', book=book, due_date=due_date, borrow_success=True)

@app.route('/my-borrows')
def my_borrowings():
    username = current_username()
    borrowings = load_borrowings()
    books = load_books()
    filter_status = request.args.get('filter_status', '')
    filtered = []
    for b in borrowings:
        if b['username'] == username:
            if filter_status and filter_status != b['status']:
                continue
            book_title = ''
            for book in books:
                if book['book_id'] == b['book_id']:
                    book_title = book['title']
                    break
            filtered.append({
                'borrow_id': b['borrow_id'],
                'book_id': b['book_id'],
                'title': book_title,
                'borrow_date': b['borrow_date'],
                'due_date': b['due_date'],
                'status': b['status']
            })
    return render_template('my_borrowings.html', borrows=filtered, filter_status=filter_status)

@app.route('/return/<int:borrow_id>', methods=['GET', 'POST'])
def return_book(borrow_id):
    username = current_username()
    borrowings = load_borrowings()
    borrow = None
    for b in borrowings:
        if b['borrow_id'] == borrow_id and b['username'] == username:
            borrow = b
            break
    if not borrow:
        flash('Borrowing record not found.')
        return redirect(url_for('my_borrowings'))

    books = load_books()
    book = None
    for bk in books:
        if bk['book_id'] == borrow['book_id']:
            book = {
                'book_id': bk['book_id'],
                'title': bk['title']
            }
            break
    if not book:
        flash('Book record not found.')
        return redirect(url_for('my_borrowings'))

    if request.method == 'GET':
        return render_template('return_confirmation.html', borrow=borrow, return_success=False)

    # POST - confirm return
    if borrow['status'] != 'Active' and borrow['status'] != 'Overdue':
        return render_template('return_confirmation.html', borrow=borrow, return_success=False,
                               error_message='This borrow is not active or overdue, cannot return.')

    now_date_str = datetime.now().strftime('%Y-%m-%d')
    borrow['return_date'] = now_date_str

    # Check overdue and fines
    borrow_date_obj = datetime.strptime(borrow['borrow_date'], '%Y-%m-%d')
    due_date_obj = datetime.strptime(borrow['due_date'], '%Y-%m-%d')
    now_date_obj = datetime.strptime(now_date_str, '%Y-%m-%d')

    fine_amount = 0.0
    if now_date_obj > due_date_obj:
        delta_days = (now_date_obj - due_date_obj).days
        fine_amount = delta_days * 0.50  # 50 cents per day overdue

    borrow['status'] = 'Returned'
    borrow['fine_amount'] = fine_amount

    save_borrowings(borrowings)

    # Update book status to Available (if no active borrows or reservation)
    active_found = False
    for b in borrowings:
        if b['book_id'] == borrow['book_id'] and b['status'] == 'Active':
            active_found = True
            break
    if not active_found:
        # Check reservations for this book
        reservations = load_reservations()
        reserved = False
        for r in reservations:
            if r['book_id'] == borrow['book_id'] and r['status'] == 'Active':
                reserved = True
                break
        for bk in books:
            if bk['book_id'] == borrow['book_id']:
                bk['status'] = 'Reserved' if reserved else 'Available'
                break
        save_books(books)

    # Add fine record if fine_amount > 0
    if fine_amount > 0.0:
        fines = load_fines()
        next_fine_id = get_next_id(fines, 'fine_id')
        new_fine = {
            'fine_id': next_fine_id,
            'username': username,
            'borrow_id': borrow['borrow_id'],
            'amount': fine_amount,
            'status': 'Unpaid',
            'date_issued': now_date_str
        }
        fines.append(new_fine)
        save_fines(fines)

    return render_template('return_confirmation.html', borrow=borrow, return_success=True)

@app.route('/my-reservations')
def my_reservations():
    username = current_username()
    reservations = load_reservations()
    books = load_books()
    filtered = []
    for r in reservations:
        if r['username'] == username:
            book_title = ''
            for bk in books:
                if bk['book_id'] == r['book_id']:
                    book_title = bk['title']
                    break
            filtered.append({
                'reservation_id': r['reservation_id'],
                'book_id': r['book_id'],
                'title': book_title,
                'reservation_date': r['reservation_date'],
                'status': r['status']
            })
    return render_template('my_reservations.html', reservations=filtered)

@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    username = current_username()
    reservations = load_reservations()
    found = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == username:
            if r['status'] != 'Cancelled':
                r['status'] = 'Cancelled'
                found = True
            break
    if found:
        save_reservations(reservations)
        flash('Reservation cancelled successfully.')
    else:
        flash('Reservation not found or already cancelled.')
    return redirect(url_for('my_reservations'))

@app.route('/my-reviews')
def my_reviews():
    username = current_username()
    reviews = load_reviews()
    books = load_books()
    filtered = []
    for r in reviews:
        if r['username'] == username:
            title = ''
            for bk in books:
                if bk['book_id'] == r['book_id']:
                    title = bk['title']
                    break
            filtered.append({
                'review_id': r['review_id'],
                'book_id': r['book_id'],
                'title': title,
                'rating': r['rating'],
                'review_text': r['review_text']
            })
    return render_template('my_reviews.html', reviews=filtered)

@app.route('/write-review/<int:book_id>', methods=['GET', 'POST'])
def write_review(book_id):
    username = current_username()
    books = load_books()
    book = None
    for b in books:
        if b['book_id'] == book_id:
            book = {'book_id': b['book_id'], 'title': b['title']}
            break
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))

    reviews = load_reviews()
    existing_review = None
    for r in reviews:
        if r['username'] == username and r['book_id'] == book_id:
            existing_review = {
                'review_id': r['review_id'],
                'rating': r['rating'],
                'review_text': r['review_text']
            }
            break

    if request.method == 'GET':
        return render_template('write_review.html', book=book, existing_review=existing_review, submit_success=False)

    # POST to create new or update existing
    try:
        rating = int(request.form.get('rating', 0))
        review_text = request.form.get('review_text', '').strip()
        if rating < 1 or rating > 5:
            raise ValueError('Rating must be between 1 and 5')
        if not review_text:
            raise ValueError('Review text cannot be empty')
    except Exception as e:
        return render_template('write_review.html', book=book, existing_review=existing_review, submit_success=False,
                               error_message=str(e))

    if existing_review:
        # Update existing
        for r in reviews:
            if r['review_id'] == existing_review['review_id']:
                r['rating'] = rating
                r['review_text'] = review_text
                r['review_date'] = datetime.now().strftime('%Y-%m-%d')
                break
    else:
        next_id = get_next_id(reviews, 'review_id')
        reviews.append({
            'review_id': next_id,
            'username': username,
            'book_id': book_id,
            'rating': rating,
            'review_text': review_text,
            'review_date': datetime.now().strftime('%Y-%m-%d')
        })
    save_reviews(reviews)
    return render_template('write_review.html', book=book, existing_review=None, submit_success=True)

@app.route('/edit-review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    username = current_username()
    reviews = load_reviews()
    review = None
    for r in reviews:
        if r['review_id'] == review_id and r['username'] == username:
            review = r
            break
    if not review:
        flash('Review not found.')
        return redirect(url_for('my_reviews'))

    books = load_books()
    book = None
    for b in books:
        if b['book_id'] == review['book_id']:
            book = {'book_id': b['book_id'], 'title': b['title']}
            break

    if request.method == 'GET':
        return render_template('write_review.html', review=review, book=book, submit_success=False)

    # POST to update
    try:
        rating = int(request.form.get('rating', 0))
        review_text = request.form.get('review_text', '').strip()
        if rating < 1 or rating > 5:
            raise ValueError('Rating must be between 1 and 5')
        if not review_text:
            raise ValueError('Review text cannot be empty')
    except Exception as e:
        return render_template('write_review.html', review=review, book=book, submit_success=False,
                               error_message=str(e))

    review['rating'] = rating
    review['review_text'] = review_text
    review['review_date'] = datetime.now().strftime('%Y-%m-%d')

    save_reviews(reviews)
    return render_template('write_review.html', review=review, book=book, submit_success=True)

@app.route('/delete-review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    username = current_username()
    reviews = load_reviews()
    new_reviews = [r for r in reviews if not (r['review_id'] == review_id and r['username'] == username)]
    if len(new_reviews) == len(reviews):
        flash('Review not found or cannot delete.')
    else:
        save_reviews(new_reviews)
        flash('Review deleted successfully.')
    return redirect(url_for('my_reviews'))

@app.route('/profile', methods=['GET', 'POST'])
def user_profile():
    username = current_username()
    users = load_users()
    user = None
    for u in users:
        if u['username'] == username:
            user = u
            break
    if not user:
        flash('User not found.')
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        # borrow_history: list of dict (book_id:int, title:str, borrow_date:str, return_date:str)
        borrowings = load_borrowings()
        books = load_books()
        history = []
        for b in borrowings:
            if b['username'] == username and b['status'] == 'Returned':
                title = ''
                for bk in books:
                    if bk['book_id'] == b['book_id']:
                        title = bk['title']
                        break
                history.append({
                    'book_id': b['book_id'],
                    'title': title,
                    'borrow_date': b['borrow_date'],
                    'return_date': b['return_date'] if b['return_date'] else ''
                })
        return render_template('profile.html', user=user, borrow_history=history)

    # POST: update profile email, phone, address
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    # Basic validation
    if not email or not phone or not address:
        flash('All fields are required.')
        return render_template('profile.html', user=user, borrow_history=[]) # borrow_history empty on just post error

    user['email'] = email
    user['phone'] = phone
    user['address'] = address
    save_users(users)
    flash('Profile updated successfully.')

    # After update reload borrow_history
    borrowings = load_borrowings()
    books = load_books()
    history = []
    for b in borrowings:
        if b['username'] == username and b['status'] == 'Returned':
            title = ''
            for bk in books:
                if bk['book_id'] == b['book_id']:
                    title = bk['title']
                    break
            history.append({
                'book_id': b['book_id'],
                'title': title,
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date'] if b['return_date'] else ''
            })
    return render_template('profile.html', user=user, borrow_history=history)

@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment_confirmation(fine_id):
    username = current_username()
    fines = load_fines()
    fine = None
    for f in fines:
        if f['fine_id'] == fine_id and f['username'] == username:
            fine = f
            break
    if not fine:
        flash('Fine record not found.')
        return redirect(url_for('user_profile'))

    if request.method == 'GET':
        return render_template('payment_confirmation.html', fine=fine, payment_success=False)

    # POST to confirm payment
    if fine['status'] == 'Paid':
        return render_template('payment_confirmation.html', fine=fine, payment_success=False, error_message='Fine is already paid.')

    fine['status'] = 'Paid'
    save_fines(fines)
    flash('Payment completed successfully.')
    return render_template('payment_confirmation.html', fine=fine, payment_success=True)

if __name__ == '__main__':
    app.run()