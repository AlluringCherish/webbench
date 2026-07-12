import os
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, request, flash, redirect

app = Flask(__name__)
app.secret_key = 'replace_with_a_strong_secret_key'

DATA_DIR = 'data'
CURRENT_USERNAME = 'john_reader'

# Data reading/writing helper functions

def read_users():
    users_path = os.path.join(DATA_DIR, 'users.txt')
    users = []
    if os.path.exists(users_path):
        with open(users_path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    users.append({'username': parts[0], 'email': parts[1]})
    return users

def write_users(users):
    users_path = os.path.join(DATA_DIR, 'users.txt')
    with open(users_path, 'w') as f:
        for user in users:
            f.write(f"{user['username']}|{user['email']}\n")

def read_books():
    books_path = os.path.join(DATA_DIR, 'books.txt')
    books = []
    if os.path.exists(books_path):
        with open(books_path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    books.append({
                        'book_id': parts[0],
                        'title': parts[1],
                        'author': parts[2],
                        'description': parts[3],
                        'status': parts[4]
                    })
    return books

def read_borrowings():
    borrowings_path = os.path.join(DATA_DIR, 'borrowings.txt')
    borrowings = []
    if os.path.exists(borrowings_path):
        with open(borrowings_path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    borrowings.append({
                        'borrow_id': int(parts[0]),
                        'username': parts[1],
                        'book_id': parts[2],
                        'borrow_date': parts[3],
                        'due_date': parts[4],
                        'status': parts[5],
                        'book_title': parts[6]
                    })
    return borrowings

def write_borrowings(borrowings):
    borrowings_path = os.path.join(DATA_DIR, 'borrowings.txt')
    with open(borrowings_path, 'w') as f:
        for borrow in borrowings:
            f.write(f"{borrow['borrow_id']}|{borrow['username']}|{borrow['book_id']}|{borrow['borrow_date']}|{borrow['due_date']}|{borrow['status']}|{borrow['book_title']}\n")

def read_reservations():
    reservations_path = os.path.join(DATA_DIR, 'reservations.txt')
    reservations = []
    if os.path.exists(reservations_path):
        with open(reservations_path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    reservations.append({
                        'reservation_id': int(parts[0]),
                        'username': parts[1],
                        'book_id': parts[2],
                        'reservation_date': parts[3],
                        'status': parts[4]
                    })
    return reservations

def write_reservations(reservations):
    reservations_path = os.path.join(DATA_DIR, 'reservations.txt')
    with open(reservations_path, 'w') as f:
        for res in reservations:
            f.write(f"{res['reservation_id']}|{res['username']}|{res['book_id']}|{res['reservation_date']}|{res['status']}\n")

def read_reviews():
    reviews_path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if os.path.exists(reviews_path):
        with open(reviews_path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    reviews.append({
                        'review_id': int(parts[0]),
                        'username': parts[1],
                        'book_id': parts[2],
                        'review_date': parts[3],
                        'rating': int(parts[4]),
                        'review_text': parts[5]
                    })
    return reviews

def write_reviews(reviews):
    reviews_path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(reviews_path, 'w') as f:
        for rev in reviews:
            f.write(f"{rev['review_id']}|{rev['username']}|{rev['book_id']}|{rev['review_date']}|{rev['rating']}|{rev['review_text']}\n")

def read_fines():
    fines_path = os.path.join(DATA_DIR, 'fines.txt')
    fines = []
    if os.path.exists(fines_path):
        with open(fines_path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    fines.append({
                        'fine_id': int(parts[0]),
                        'username': parts[1],
                        'amount': float(parts[2]),
                        'paid': parts[3] == 'True'
                    })
    return fines

def write_fines(fines):
    fines_path = os.path.join(DATA_DIR, 'fines.txt')
    with open(fines_path, 'w') as f:
        for fine in fines:
            f.write(f"{fine['fine_id']}|{fine['username']}|{fine['amount']}|{fine['paid']}\n")

def next_borrow_id():
    borrowings = read_borrowings()
    if borrowings:
        return max(b['borrow_id'] for b in borrowings) + 1
    return 1

def next_review_id():
    reviews = read_reviews()
    if reviews:
        return max(r['review_id'] for r in reviews) + 1
    return 1

def next_fine_id():
    fines = read_fines()
    if fines:
        return max(f['fine_id'] for f in fines) + 1
    return 1

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    books = read_books()
    featured_books = books[:5]  # showcase first 5 as featured
    return render_template('dashboard.html', featured_books=featured_books, ihwkqe73po=CURRENT_USERNAME)

@app.route('/book_catalog')
def book_catalog():
    books = read_books()
    return render_template('catalog.html', books=books)

@app.route('/book/<book_id>')
def book_details(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    reviews = read_reviews()
    book_reviews = [rev for rev in reviews if rev['book_id'] == book_id]
    # Sort reviews by review_date descending
    book_reviews.sort(key=lambda r: r['review_date'], reverse=True)
    return render_template('book_details.html', title=book['title'], author=book['author'], description=book['description'], status=book['status'], reviews=book_reviews, book_id=book_id)

@app.route('/borrow/<book_id>')
def borrow(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    return render_template('borrow.html', book_details=book, due_date=due_date)

@app.route('/confirm_borrow', methods=['POST'])
def confirm_borrow():
    book_id = request.args.get('book_id')
    if not book_id:
        flash('No book selected for borrowing.')
        return redirect(url_for('book_catalog'))
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    borrowings = read_borrowings()
    # Create new borrow record
    borrow_id = next_borrow_id()
    borrow_date = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    borrowings.append({
        'borrow_id': borrow_id,
        'username': CURRENT_USERNAME,
        'book_id': book_id,
        'borrow_date': borrow_date,
        'due_date': due_date,
        'status': 'borrowed',
        'book_title': book['title']
    })
    write_borrowings(borrowings)
    flash('Borrow confirmed successfully.')
    return redirect(url_for('my_borrows'))

@app.route('/cancel_borrow', methods=['POST'])
def cancel_borrow():
    return redirect(url_for('book_catalog'))

@app.route('/my_borrows')
def my_borrows():
    borrowings = read_borrowings()
    my_borrows_list = [b for b in borrowings if b['username'] == CURRENT_USERNAME and b['status'] == 'borrowed']
    return render_template('my_borrows.html', borrows=my_borrows_list)

@app.route('/return_book/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    borrowings = read_borrowings()
    for borrow in borrowings:
        if borrow['borrow_id'] == borrow_id and borrow['username'] == CURRENT_USERNAME:
            borrow['status'] = 'returned'
            write_borrowings(borrowings)
            flash('Book returned successfully.')
            break
    else:
        flash('Borrow record not found.')
    return redirect(url_for('my_borrows'))

@app.route('/my_reservations')
def my_reservations():
    reservations = read_reservations()
    my_reservations_list = [r for r in reservations if r['username'] == CURRENT_USERNAME]
    return render_template('my_reservations.html', reservations=my_reservations_list)

@app.route('/cancel_reservation/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    reservations = read_reservations()
    for res in reservations:
        if res['reservation_id'] == reservation_id and res['username'] == CURRENT_USERNAME:
            res['status'] = 'canceled'
            write_reservations(reservations)
            flash('Reservation canceled successfully.')
            break
    else:
        flash('Reservation record not found.')
    return redirect(url_for('my_reservations'))

@app.route('/my_reviews')
def my_reviews():
    reviews = read_reviews()
    books = read_books()
    my_reviews_list = []
    for rev in reviews:
        if rev['username'] == CURRENT_USERNAME:
            book_title = next((b['title'] for b in books if b['book_id'] == rev['book_id']), 'Unknown')
            my_reviews_list.append({
                'review_id': rev['review_id'],
                'book_title': book_title,
                'review_text': rev['review_text']
            })
    return render_template('my_reviews.html', reviews=my_reviews_list)

@app.route('/write_review/<book_id>')
def write_review(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        flash('Book not found.')
        return redirect(url_for('book_catalog'))
    return render_template('write_review.html', book_id=book_id, review=None)

@app.route('/submit_write_review/<book_id>', methods=['POST'])
def submit_write_review(book_id):
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')
    if not rating or not review_text:
        flash('Please fill in all review fields.')
        return redirect(url_for('write_review', book_id=book_id))
    reviews = read_reviews()
    review_id = next_review_id()
    review_date = datetime.now().strftime('%Y-%m-%d')
    reviews.append({
        'review_id': review_id,
        'username': CURRENT_USERNAME,
        'book_id': book_id,
        'review_date': review_date,
        'rating': int(rating),
        'review_text': review_text
    })
    write_reviews(reviews)
    flash('Review submitted successfully.')
    return redirect(url_for('book_details', book_id=book_id))

@app.route('/edit_review/<int:review_id>')
def edit_review_page(review_id):
    reviews = read_reviews()
    review = next((r for r in reviews if r['review_id'] == review_id and r['username'] == CURRENT_USERNAME), None)
    if not review:
        flash('Review not found.')
        return redirect(url_for('my_reviews'))
    return render_template('write_review.html', review=review, book_id=review['book_id'])

@app.route('/submit_edit_review/<int:review_id>', methods=['POST'])
def submit_edit_review(review_id):
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')
    reviews = read_reviews()
    for review in reviews:
        if review['review_id'] == review_id and review['username'] == CURRENT_USERNAME:
            review['rating'] = int(rating)
            review['review_text'] = review_text
            review['review_date'] = datetime.now().strftime('%Y-%m-%d')
            write_reviews(reviews)
            flash('Review updated successfully.')
            return redirect(url_for('my_reviews'))
    flash('Review not found.')
    return redirect(url_for('my_reviews'))

@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    reviews = read_reviews()
    initial_len = len(reviews)
    reviews = [r for r in reviews if not (r['review_id'] == review_id and r['username'] == CURRENT_USERNAME)]
    if len(reviews) < initial_len:
        write_reviews(reviews)
        flash('Review deleted successfully.')
    else:
        flash('Review not found.')
    return redirect(url_for('my_reviews'))

@app.route('/payment_confirmation')
def payment_confirmation():
    return render_template('payment_confirmation.html')

if __name__ == '__main__':
    app.run(debug=False)
