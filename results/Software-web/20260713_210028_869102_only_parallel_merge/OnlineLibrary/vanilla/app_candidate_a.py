from flask import Flask, render_template, request, redirect, url_for, flash
import os
import datetime

app = Flask(__name__, template_folder='templates_candidate_a')
app.secret_key = 'supersecretkey'  # For session and flash messages

DATA_DIR = 'data'

# For demo purposes, setting a fixed logged-in user
LOGGED_IN_USERNAME = 'john_reader'


# Utility functions to read and write pipe-delimited data

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


def parse_users():
    users = []
    lines = read_file_lines('users.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 4:
            users.append({
                'username': parts[0],
                'email': parts[1],
                'phone': parts[2],
                'address': parts[3]
            })
    return users


def get_user(username):
    users = parse_users()
    for user in users:
        if user['username'] == username:
            return user
    return None


def update_user_email(username, new_email):
    users = parse_users()
    updated = False
    for user in users:
        if user['username'] == username:
            user['email'] = new_email
            updated = True
            break
    if updated:
        lines = [f"{u['username']}|{u['email']}|{u['phone']}|{u['address']}" for u in users]
        write_file_lines('users.txt', lines)
    return updated


def parse_books():
    books = []
    lines = read_file_lines('books.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 10:
            books.append({
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
            })
    return books


def get_book_by_id(book_id):
    books = parse_books()
    for b in books:
        if b['book_id'] == book_id:
            return b
    return None


def update_book_status(book_id, new_status):
    books = parse_books()
    changed = False
    for b in books:
        if b['book_id'] == book_id:
            b['status'] = new_status
            changed = True
            break
    if changed:
        lines = [
            f"{b['book_id']}|{b['title']}|{b['author']}|{b['isbn']}|{b['genre']}|{b['publisher']}|{b['year']}|{b['description']}|{b['status']}|{b['avg_rating']}"
            for b in books
        ]
        write_file_lines('books.txt', lines)
    return changed


def parse_borrowings():
    borrows = []
    lines = read_file_lines('borrowings.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 8:
            borrows.append({
                'borrow_id': int(parts[0]),
                'username': parts[1],
                'book_id': int(parts[2]),
                'borrow_date': parts[3],
                'due_date': parts[4],
                'return_date': parts[5],
                'status': parts[6],
                'fine_amount': parts[7]
            })
    return borrows


def write_borrowings(borrows):
    lines = [
        f"{b['borrow_id']}|{b['username']}|{b['book_id']}|{b['borrow_date']}|{b['due_date']}|{b['return_date']}|{b['status']}|{b['fine_amount']}"
        for b in borrows
    ]
    write_file_lines('borrowings.txt', lines)


def get_next_borrow_id():
    borrows = parse_borrowings()
    if not borrows:
        return 1
    return max(b['borrow_id'] for b in borrows) + 1


def parse_reservations():
    reservations = []
    lines = read_file_lines('reservations.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 5:
            reservations.append({
                'reservation_id': int(parts[0]),
                'username': parts[1],
                'book_id': int(parts[2]),
                'reservation_date': parts[3],
                'status': parts[4]
            })
    return reservations


def write_reservations(reservations):
    lines = [
        f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['reservation_date']}|{r['status']}"
        for r in reservations
    ]
    write_file_lines('reservations.txt', lines)


def parse_reviews():
    reviews = []
    lines = read_file_lines('reviews.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 6:
            try:
                reviews.append({
                    'review_id': int(parts[0]),
                    'username': parts[1],
                    'book_id': int(parts[2]),
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                })
            except ValueError:
                continue
    return reviews


def write_reviews(reviews):
    lines = [
        f"{r['review_id']}|{r['username']}|{r['book_id']}|{r['rating']}|{r['review_text']}|{r['review_date']}"
        for r in reviews
    ]
    write_file_lines('reviews.txt', lines)


def get_next_review_id():
    reviews = parse_reviews()
    if not reviews:
        return 1
    return max(r['review_id'] for r in reviews) + 1


def parse_fines():
    fines = []
    lines = read_file_lines('fines.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) == 6:
            try:
                fines.append({
                    'fine_id': int(parts[0]),
                    'username': parts[1],
                    'borrow_id': int(parts[2]),
                    'amount': parts[3],
                    'status': parts[4],
                    'date_issued': parts[5]
                })
            except ValueError:
                continue
    return fines


def write_fines(fines):
    lines = [
        f"{f['fine_id']}|{f['username']}|{f['borrow_id']}|{f['amount']}|{f['status']}|{f['date_issued']}"
        for f in fines
    ]
    write_file_lines('fines.txt', lines)


def get_next_fine_id():
    fines = parse_fines()
    if not fines:
        return 1
    return max(f['fine_id'] for f in fines) + 1


# Route: / and /dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    username = LOGGED_IN_USERNAME
    books = parse_books()
    # Featured books: show first 3 available or reserved or borrowed in order of book_id
    featured = sorted(books, key=lambda b: b['book_id'])[:3]
    featured_books = [{
        'book_id': b['book_id'],
        'title': b['title'],
        'author': b['author'],
        'status': b['status']
    } for b in featured]
    return render_template('dashboard.html', username=username, featured_books=featured_books)


# Route: /catalog
@app.route('/catalog')
def catalog():
    books = parse_books()
    search_query = request.args.get('search', '').strip()
    if search_query:
        sq_lower = search_query.lower()
        filtered_books = [b for b in books if sq_lower in b['title'].lower() or sq_lower in b['author'].lower()]
    else:
        filtered_books = books
    books_display = [{
        'book_id': b['book_id'],
        'title': b['title'],
        'author': b['author'],
        'status': b['status']
    } for b in filtered_books]
    return render_template('catalog.html', books=books_display, search_query=search_query)


# Route: /book/<int:book_id>
@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return "Book not found", 404
    reviews_all = parse_reviews()
    reviews = [
        {
            'review_id': r['review_id'],
            'username': r['username'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        }
        for r in reviews_all if r['book_id'] == book_id
    ]
    can_borrow = (book['status'] == 'Available')
    return render_template('book_details.html', book=book, reviews=reviews, can_borrow=can_borrow)


# Route: /borrow/<int:book_id>
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
        due_date = borrow_date + datetime.timedelta(days=14)
        return render_template('borrow_confirmation.html', book=book, due_date=due_date.strftime('%Y-%m-%d'))

    elif request.method == 'POST':
        # Confirm borrow
        if book['status'] != 'Available':
            flash('Book is not available for borrowing.')
            return redirect(url_for('book_details', book_id=book_id))

        borrow_id = get_next_borrow_id()
        borrow_date = datetime.date.today().strftime('%Y-%m-%d')
        due_date = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y-%m-%d')
        new_borrow = {
            'borrow_id': borrow_id,
            'username': LOGGED_IN_USERNAME,
            'book_id': book_id,
            'borrow_date': borrow_date,
            'due_date': due_date,
            'return_date': '',
            'status': 'Active',
            'fine_amount': '0'
        }

        borrows = parse_borrowings()
        borrows.append(new_borrow)
        write_borrowings(borrows)

        # Update book status to Borrowed
        update_book_status(book_id, 'Borrowed')

        flash('Book borrowed successfully!')
        return redirect(url_for('my_borrows'))


# Route: /my-borrows
@app.route('/my-borrows', methods=['GET', 'POST'])
def my_borrows():
    filter_status = request.args.get('filter', 'All')
    borrows = parse_borrowings()
    user_borrows = [b for b in borrows if b['username'] == LOGGED_IN_USERNAME]

    if filter_status and filter_status != 'All':
        user_borrows = [b for b in user_borrows if b['status'] == filter_status]

    # Join book titles
    books = parse_books()
    book_map = {b['book_id']: b['title'] for b in books}
    borrows_display = []
    for b in user_borrows:
        borrows_display.append({
            'borrow_id': b['borrow_id'],
            'book_title': book_map.get(b['book_id'], 'Unknown'),
            'borrow_date': b['borrow_date'],
            'due_date': b['due_date'],
            'status': b['status']
        })

    return render_template('my_borrowings.html', borrows=borrows_display, filter_status=filter_status)


# POST to handle returning a book
@app.route('/return-borrow/<int:borrow_id>', methods=['POST'])
def return_borrow(borrow_id):
    borrows = parse_borrowings()
    found = False
    for b in borrows:
        if b['borrow_id'] == borrow_id and b['username'] == LOGGED_IN_USERNAME and b['status'] == 'Active':
            b['return_date'] = datetime.date.today().strftime('%Y-%m-%d')
            b['status'] = 'Returned'
            # Update book status to Available
            update_book_status(b['book_id'], 'Available')
            found = True
            break
    if found:
        write_borrowings(borrows)
        flash('Book returned successfully.')
    else:
        flash('Borrow record not found or already returned.')
    return redirect(url_for('my_borrows'))


# Route: /my-reservations
@app.route('/my-reservations')
def my_reservations():
    reservations = parse_reservations()
    user_reservations = [r for r in reservations if r['username'] == LOGGED_IN_USERNAME]
    books = parse_books()
    book_map = {b['book_id']: b['title'] for b in books}

    reservations_display = []
    for r in user_reservations:
        reservations_display.append({
            'reservation_id': r['reservation_id'],
            'book_title': book_map.get(r['book_id'], 'Unknown'),
            'reservation_date': r['reservation_date'],
            'status': r['status']
        })
    return render_template('my_reservations.html', reservations=reservations_display)


# POST to cancel reservation
@app.route('/cancel-reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = parse_reservations()
    changed = False
    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == LOGGED_IN_USERNAME and r['status'] == 'Active':
            r['status'] = 'Cancelled'
            changed = True
            break
    if changed:
        write_reservations(reservations)
        flash('Reservation cancelled.')
    else:
        flash('Reservation not found or cannot be cancelled.')
    return redirect(url_for('my_reservations'))


# Route: /my-reviews
@app.route('/my-reviews')
def my_reviews():
    reviews = parse_reviews()
    user_reviews = [r for r in reviews if r['username'] == LOGGED_IN_USERNAME]
    books = parse_books()
    book_map = {b['book_id']: b['title'] for b in books}
    reviews_display = []
    for r in user_reviews:
        reviews_display.append({
            'review_id': r['review_id'],
            'book_title': book_map.get(r['book_id'], 'Unknown'),
            'rating': r['rating'],
            'review_text': r['review_text']
        })
    return render_template('my_reviews.html', reviews=reviews_display)


# POST to delete a review
@app.route('/delete-review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = parse_reviews()
    reviews_after_delete = [r for r in reviews if not (r['review_id'] == review_id and r['username'] == LOGGED_IN_USERNAME)]
    if len(reviews_after_delete) != len(reviews):
        write_reviews(reviews_after_delete)
        flash('Review deleted.')
    else:
        flash('Review not found or cannot be deleted.')
    return redirect(url_for('my_reviews'))


# Route: /write-review/<int:book_id>
@app.route('/write-review/<int:book_id>', methods=['GET', 'POST'])
def write_review(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return "Book not found", 404
    reviews = parse_reviews()
    existing_review = None
    for r in reviews:
        if r['book_id'] == book_id and r['username'] == LOGGED_IN_USERNAME:
            existing_review = r
            break
    if request.method == 'GET':
        return render_template('write_review.html', book=book, existing_review=existing_review)

    elif request.method == 'POST':
        rating = request.form.get('rating-input')
        review_text = request.form.get('review-text').strip() if request.form.get('review-text') else ''
        if not rating or not rating.isdigit() or int(rating) not in range(1,6):
            flash('Invalid rating selected.')
            return redirect(url_for('write_review', book_id=book_id))
        if len(review_text) == 0:
            flash('Review text cannot be empty.')
            return redirect(url_for('write_review', book_id=book_id))

        now_str = datetime.date.today().strftime('%Y-%m-%d')

        if existing_review:
            # Update existing review
            existing_review['rating'] = int(rating)
            existing_review['review_text'] = review_text
            existing_review['review_date'] = now_str
        else:
            # Add new review
            new_id = get_next_review_id()
            new_review = {
                'review_id': new_id,
                'username': LOGGED_IN_USERNAME,
                'book_id': book_id,
                'rating': int(rating),
                'review_text': review_text,
                'review_date': now_str
            }
            reviews.append(new_review)

        write_reviews(reviews)
        flash('Review saved successfully!')
        return redirect(url_for('book_details', book_id=book_id))


# Route: /profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = get_user(LOGGED_IN_USERNAME)
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        new_email = request.form.get('profile-email').strip() if request.form.get('profile-email') else ''
        if new_email:
            update_user_email(LOGGED_IN_USERNAME, new_email)
            flash('Profile updated successfully.')
        else:
            flash('Email cannot be empty.')
        return redirect(url_for('profile'))

    # GET method
    borrows = parse_borrowings()
    borrow_history = []
    books = parse_books()
    book_map = {b['book_id']: b['title'] for b in books}
    for b in borrows:
        if b['username'] == LOGGED_IN_USERNAME:
            borrow_history.append({
                'book_title': book_map.get(b['book_id'], 'Unknown'),
                'borrow_date': b['borrow_date'],
                'return_date': b['return_date'] if b['return_date'] else ''
            })

    return render_template('profile.html', username=LOGGED_IN_USERNAME, email=user['email'], borrow_history=borrow_history)


# Route: /payment/<int:fine_id>
@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment_confirmation(fine_id):
    fines = parse_fines()
    fine = None
    for f in fines:
        if f['fine_id'] == fine_id and f['username'] == LOGGED_IN_USERNAME:
            fine = f
            break
    if not fine:
        return "Fine not found", 404

    if request.method == 'POST':
        # Confirm payment
        if fine['status'] == 'Unpaid':
            fine['status'] = 'Paid'
            write_fines(fines)
            flash('Payment confirmed successfully.')
        else:
            flash('Fine already paid.')
        return redirect(url_for('profile'))

    # GET method
    return render_template('payment_confirmation.html', fine=fine)


if __name__ == '__main__':
    app.run(debug=True)
