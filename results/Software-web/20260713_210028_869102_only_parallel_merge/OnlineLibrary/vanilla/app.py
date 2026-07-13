from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = 'supersecretkey'

DATA_DIR = 'data'

LOGGED_IN_USERNAME = 'john_reader'

# Utility functions

def read_file_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    return lines

def write_file_lines(filename, lines):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

# Users

def read_users_dict():
    users = {}
    lines = read_file_lines('users.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 4:
            users[parts[0]] = {
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3]
            }
    return users

def write_users_dict(users):
    lines = []
    for u in users.values():
        lines.append(f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}")
    write_file_lines('users.txt', lines)

def get_user(username):
    users = read_users_dict()
    return users.get(username)

def update_user_email(username, new_email):
    users = read_users_dict()
    if username in users:
        users[username]['email'] = new_email
        write_users_dict(users)
        return True
    return False

# Books

def read_books_dict():
    books = {}
    lines = read_file_lines('books.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 10:
            try:
                books[int(parts[0])] = {
                    'book_id': int(parts[0]),
                    'title': parts[1],
                    'author': parts[2],
                    'isbn': parts[3],
                    'genre': parts[4],
                    'publisher': parts[5],
                    'year': int(parts[6]),
                    'description': parts[7],
                    'status': parts[8],
                    'avg_rating': float(parts[9]) if parts[9] else 0.0
                }
            except ValueError:
                continue
    return books

def write_books_dict(books):
    lines = []
    for b in books.values():
        lines.append(f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['genre']}|{b['publisher']}|{b['year']}|{b['description']}|{b['status']}|{b['avg_rating']}")
    write_file_lines('books.txt', lines)

def get_book_by_id(book_id):
    books = read_books_dict()
    return books.get(book_id)

def update_book_status(book_id, new_status):
    books = read_books_dict()
    if book_id in books:
        books[book_id]['status'] = new_status
        write_books_dict(books)
        return True
    return False

# Borrowings

def read_borrowings_dict():
    borrows = {}
    lines = read_file_lines('borrowings.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 8:
            try:
                borrows[int(parts[0])] = {
                    'borrow_id': int(parts[0]),
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'borrow_date': parts[3],
                    'due_date': parts[4],
                    'return_date': parts[5],
                    'status': parts[6],
                    'fine_amount': parts[7]
                }
            except ValueError:
                continue
    return borrows

def write_borrowings_dict(borrows):
    lines = []
    for b in borrows.values():
        lines.append(f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{b['return_date']}|{b['status']}|{b['fine_amount']}")
    write_file_lines('borrowings.txt', lines)

def get_next_borrow_id():
    borrows = read_borrowings_dict()
    if borrows:
        return max(borrows.keys()) + 1
    else:
        return 1

# Reservations

def read_reservations_dict():
    reservations = {}
    lines = read_file_lines('reservations.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 5:
            try:
                reservations[int(parts[0])] = {
                    'reservation_id': int(parts[0]),
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'reservation_date': parts[3],
                    'status': parts[4]
                }
            except ValueError:
                continue
    return reservations

def write_reservations_dict(reservations):
    lines = []
    for r in reservations.values():
        lines.append(f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}")
    write_file_lines('reservations.txt', lines)

# Reviews

def read_reviews_dict():
    reviews = {}
    lines = read_file_lines('reviews.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 6:
            try:
                reviews[int(parts[0])] = {
                    'review_id': int(parts[0]),
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
            except ValueError:
                continue
    return reviews

def write_reviews_dict(reviews):
    lines = []
    for r in reviews.values():
        lines.append(f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}")
    write_file_lines('reviews.txt', lines)

def get_next_review_id():
    reviews = read_reviews_dict()
    if reviews:
        return max(reviews.keys()) + 1
    else:
        return 1

# Fines

def read_fines_dict():
    fines = {}
    lines = read_file_lines('fines.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 6:
            try:
                fines[int(parts[0])] = {
                    'fine_id': int(parts[0]),
                    'username': parts[1],
                    'borrow_id': int(parts[2]),
                    'amount': parts[3],
                    'status': parts[4],
                    'date_issued': parts[5]
                }
            except ValueError:
                continue
    return fines

def write_fines_dict(fines):
    lines = []
    for f in fines.values():
        lines.append(f"{f['fine_id']}|{f['username']}|{f['borrow_id']}|{f['amount']}|{f['status']}|{f['date_issued']}")
    write_file_lines('fines.txt', lines)

# Routes

@app.route('/')
@app.route('/dashboard')
def dashboard():
    username = LOGGED_IN_USERNAME
    books = read_books_dict()
    featured_books = []
    count = 0
    for b in sorted(books.values(), key=lambda x: x['book_id']):
        featured_books.append({'book_id': b['book_id'], 'title': b['title'], 'author': b['author'], 'status': b['status']})
        count += 1
        if count >= 3:
            break
    return render_template('dashboard.html', username=username, featured_books=featured_books)

@app.route('/catalog')
def catalog():
    books = read_books_dict()
    search_query = request.args.get('search', '').strip()
    filtered_books = []
    if search_query:
        sq = search_query.lower()
        for b in books.values():
            if sq in b['title'].lower() or sq in b['author'].lower():
                filtered_books.append({'book_id': b['book_id'], 'title': b['title'], 'author': b['author'], 'status': b['status']})
    else:
        for b in books.values():
            filtered_books.append({'book_id': b['book_id'], 'title': b['title'], 'author': b['author'], 'status': b['status']})
    return render_template('catalog.html', books=filtered_books, search_query=search_query)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return "Book not found", 404
    reviews = read_reviews_dict()
    filtered_reviews = []
    for r in reviews.values():
        if r['book_id'] == book_id:
            filtered_reviews.append({
                'review_id': r['review_id'],
                'username': r['username'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })
    can_borrow = book['status'] == 'Available'
    return render_template('book_details.html', book=book, reviews=filtered_reviews, can_borrow=can_borrow)

@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return "Book not found", 404
    if request.method == 'GET':
        if book['status'] != 'Available':
            flash('Book is not available for borrowing.')
            return redirect(url_for('book_details', book_id=book_id))
        borrow_date = datetime.date.today()
        due_date = (borrow_date + datetime.timedelta(days=14)).strftime('%Y-%m-%d')
        return render_template('borrow_confirmation.html', book=book, due_date=due_date)

    if request.method == 'POST':
        if book['status'] != 'Available':
            flash('Book is not available for borrowing.')
            return redirect(url_for('book_details', book_id=book_id))
        borrows = read_borrowings_dict()
        new_borrow_id = get_next_borrow_id()
        borrow_date = datetime.date.today().strftime('%Y-%m-%d')
        due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')
        borrows[new_borrow_id] = {
            'borrow_id': new_borrow_id,
            'username': LOGGED_IN_USERNAME,
            'book_id': book_id,
            'borrow_date': borrow_date,
            'due_date': due_date,
            'return_date': '',
            'status': 'Active',
            'fine_amount': '0'
        }
        write_borrowings_dict(borrows)
        update_book_status(book_id, 'Borrowed')
        flash('Book borrowed successfully!')
        return redirect(url_for('my_borrows'))

@app.route('/my-borrows', methods=['GET', 'POST'])
def my_borrows():
    username = LOGGED_IN_USERNAME
    borrows = read_borrowings_dict()
    books = read_books_dict()
    filter_status = request.args.get('filter', 'All')

    if request.method == 'POST':
        return_id = request.form.get('return_id')
        if return_id:
            try:
                return_id = int(return_id)
                b = borrows.get(return_id)
                if b and b['username'] == username and b['status'] == 'Active':
                    b['status'] = 'Returned'
                    b['return_date'] = datetime.date.today().strftime('%Y-%m-%d')
                    borrows[return_id] = b
                    write_borrowings_dict(borrows)
                    # Update book status
                    update_book_status(b['book_id'], 'Available')
                    flash('Book returned successfully.')
                    return redirect(url_for('my_borrows', filter=filter_status))
            except ValueError:
                pass

    filtered_borrows = []
    for b in borrows.values():
        if b['username'] != username:
            continue
        if filter_status != 'All' and b['status'] != filter_status:
            continue
        filtered_borrows.append({
            'borrow_id': b['borrow_id'],
            'book_title': books.get(b['book_id'], {}).get('title', 'Unknown'),
            'borrow_date': b['borrow_date'],
            'due_date': b['due_date'],
            'status': b['status']
        })
    return render_template('my_borrowings.html', borrows=filtered_borrows, filter_status=filter_status)

@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    username = LOGGED_IN_USERNAME
    reservations = read_reservations_dict()
    books = read_books_dict()

    if request.method == 'POST':
        cancel_id = request.form.get('cancel_id')
        if cancel_id:
            try:
                cancel_id = int(cancel_id)
                r = reservations.get(cancel_id)
                if r and r['username'] == username and r['status'] == 'Active':
                    r['status'] = 'Cancelled'
                    reservations[cancel_id] = r
                    write_reservations_dict(reservations)
                    flash('Reservation cancelled successfully.')
                    return redirect(url_for('my_reservations'))
            except ValueError:
                pass

    user_reservations = []
    for r in reservations.values():
        if r['username'] != username:
            continue
        user_reservations.append({
            'reservation_id': r['reservation_id'],
            'book_title': books.get(r['book_id'], {}).get('title', 'Unknown'),
            'reservation_date': r['reservation_date'],
            'status': r['status']
        })
    return render_template('my_reservations.html', reservations=user_reservations)

@app.route('/my-reviews', methods=['GET', 'POST'])
def my_reviews():
    username = LOGGED_IN_USERNAME
    reviews = read_reviews_dict()
    books = read_books_dict()

    if request.method == 'POST':
        delete_id = request.form.get('delete_id')
        if delete_id:
            try:
                delete_id = int(delete_id)
                r = reviews.get(delete_id)
                if r and r['username'] == username:
                    del reviews[delete_id]
                    write_reviews_dict(reviews)
                    flash('Review deleted successfully.')
                    return redirect(url_for('my_reviews'))
            except ValueError:
                pass

    user_reviews = []
    for r in reviews.values():
        if r['username'] != username:
            continue
        user_reviews.append({
            'review_id': r['review_id'],
            'book_title': books.get(r['book_id'], {}).get('title', 'Unknown'),
            'rating': r['rating'],
            'review_text': r['review_text']
        })
    return render_template('my_reviews.html', reviews=user_reviews)

@app.route('/write-review/<int:book_id>', methods=['GET', 'POST'])
def write_review(book_id):
    username = LOGGED_IN_USERNAME
    books = read_books_dict()
    book = books.get(book_id)
    if not book:
        return "Book not found", 404
    reviews = read_reviews_dict()
    existing_review = None
    for r in reviews.values():
        if r['book_id'] == book_id and r['username'] == username:
            existing_review = r
            break

    if request.method == 'POST':
        rating = request.form.get('rating') or request.form.get('rating-input')
        review_text = request.form.get('review_text') or request.form.get('review-text')
        if rating is None or not rating.isdigit() or int(rating) not in range(1,6):
            flash('Invalid rating selected.')
            return redirect(url_for('write_review', book_id=book_id))
        if not review_text or not review_text.strip():
            flash('Review text cannot be empty.')
            return redirect(url_for('write_review', book_id=book_id))
        rating = int(rating)
        review_text = review_text.strip()
        today_str = datetime.date.today().strftime('%Y-%m-%d')
        if existing_review:
            existing_review['rating'] = rating
            existing_review['review_text'] = review_text
            existing_review['review_date'] = today_str
        else:
            new_id = get_next_review_id()
            reviews[new_id] = {
                'review_id': new_id,
                'username': username,
                'book_id': book_id,
                'rating': rating,
                'review_text': review_text,
                'review_date': today_str
            }
        write_reviews_dict(reviews)
        flash('Review saved successfully!')
        return redirect(url_for('book_details', book_id=book_id))

    context_existing = None
    if existing_review:
        context_existing = {
            'review_id': existing_review['review_id'],
            'rating': existing_review['rating'],
            'review_text': existing_review['review_text']
        }
    return render_template('write_review.html', book=book, existing_review=context_existing)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = LOGGED_IN_USERNAME
    users = read_users_dict()
    user = users.get(username)
    if not user:
        return "User not found", 404
    if request.method == 'POST':
        email = request.form.get('profile_email') or request.form.get('profile-email')
        if not email or not email.strip():
            flash('Email cannot be empty.')
            return redirect(url_for('profile'))
        user['email'] = email.strip()
        users[username] = user
        write_users_dict(users)
        flash('Profile updated successfully.')
        return redirect(url_for('profile'))
    borrowings = read_borrowings_dict()
    books = read_books_dict()
    borrow_history = []
    for b in borrowings.values():
        if b['username'] == username:
            borrow_history.append({
                'book_title': books.get(b['book_id'], {}).get('title', 'Unknown'),
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date']
            })
    return render_template('profile.html', username=username, email=user['email'], borrow_history=borrow_history)

@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment_confirmation(fine_id):
    username = LOGGED_IN_USERNAME
    fines = read_fines_dict()
    fine = fines.get(fine_id)
    if not fine or fine['username'] != username:
        return "Fine not found", 404
    if request.method == 'POST':
        if fine['status'] == 'Unpaid':
            fine['status'] = 'Paid'
            write_fines_dict(fines)
            flash('Payment confirmed successfully.')
        else:
            flash('Fine already paid.')
        return redirect(url_for('profile'))
    return render_template('payment_confirmation.html', fine=fine)


if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True)
