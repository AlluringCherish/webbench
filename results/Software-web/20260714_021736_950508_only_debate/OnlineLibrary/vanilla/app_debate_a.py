from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATA_DIR = 'data'

# Utility functions to read/write pipe-delimited files

def read_file(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        data = [line.split('|') for line in lines if line.strip()]
    return data


def write_file(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        for entry in data:
            f.write('|'.join(entry) + '\n')


def find_user(username):
    users = read_file('users.txt')
    for user in users:
        if user[0] == username:
            return user
    return None


def find_book(book_id):
    books = read_file('books.txt')
    for book in books:
        if book[0] == str(book_id):
            return book
    return None


def find_borrowing(borrow_id):
    borrows = read_file('borrowings.txt')
    for borrow in borrows:
        if borrow[0] == str(borrow_id):
            return borrow
    return None


def find_reservation(reservation_id):
    reservations = read_file('reservations.txt')
    for res in reservations:
        if res[0] == str(reservation_id):
            return res
    return None


def find_review(review_id):
    reviews = read_file('reviews.txt')
    for review in reviews:
        if review[0] == str(review_id):
            return review
    return None


def find_fine(fine_id):
    fines = read_file('fines.txt')
    for fine in fines:
        if fine[0] == str(fine_id):
            return fine
    return None


def calculate_avg_rating(book_id):
    reviews = read_file('reviews.txt')
    ratings = [int(r[3]) for r in reviews if r[2] == str(book_id)]
    if not ratings:
        return '0'
    avg = sum(ratings) / len(ratings)
    return f'{avg:.2f}'


# Dummy current user
current_user = 'testuser'


@app.route('/')
@app.route('/dashboard')
def dashboard():
    user = find_user(current_user)
    username = user[0] if user else current_user
    return render_template('dashboard.html', username=username)


@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    books = read_file('books.txt')
    search_query = None
    if request.method == 'POST':
        search_query = request.form.get('search_input', '').lower()
        if search_query:
            books = [b for b in books if search_query in b[1].lower() or search_query in b[2].lower()]
    return render_template('catalog.html', books=books, search_query=search_query)


@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = find_book(book_id)
    if not book:
        return 'Book not found', 404
    reviews_raw = read_file('reviews.txt')
    reviews = [r for r in reviews_raw if r[2] == str(book_id)]
    return render_template('book_details.html', book=book, reviews=reviews)


@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
def borrow_book(book_id):
    book = find_book(book_id)
    if not book:
        return 'Book not found', 404
    if request.method == 'GET':
        due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        return render_template('borrow_confirmation.html', book=book, due_date=due_date)
    else:
        # Add borrow record
        borrows = read_file('borrowings.txt')
        borrow_id = 1
        if borrows:
            borrow_id = int(borrows[-1][0]) + 1
        borrow_date = datetime.now().strftime('%Y-%m-%d')
        due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        new_borrow = [str(borrow_id), current_user, str(book_id), borrow_date, due_date, '', 'Borrowed', '0']
        borrows.append(new_borrow)
        write_file('borrowings.txt', borrows)

        # Update book status
        books = read_file('books.txt')
        for b in books:
            if b[0] == str(book_id):
                b[8] = 'Borrowed'
                break
        write_file('books.txt', books)
        return redirect(url_for('my_borrows'))


@app.route('/my-borrows', methods=['GET', 'POST'])
def my_borrows():
    borrows = read_file('borrowings.txt')
    filter_status = None
    if request.method == 'POST':
        if 'filter_status' in request.form:
            filter_status = request.form.get('filter_status')
            if filter_status and filter_status != 'All':
                borrows = [b for b in borrows if b[6] == filter_status]
        elif 'return_borrow_id' in request.form:
            borrow_id = request.form.get('return_borrow_id')
            borrows_all = read_file('borrowings.txt')
            for b in borrows_all:
                if b[0] == borrow_id and b[1] == current_user and b[6] == 'Borrowed':
                    b[6] = 'Returned'
                    b[5] = datetime.now().strftime('%Y-%m-%d')
                    # Handle fine (set 0 for now)
                    b[7] = '0'
                    # Update book status back to Available
                    book_id = b[2]
                    books = read_file('books.txt')
                    for bk in books:
                        if bk[0] == book_id:
                            bk[8] = 'Available'
                            break
                    write_file('books.txt', books)
                    break
            write_file('borrowings.txt', borrows_all)
            return redirect(url_for('my_borrows'))

    # Show only current user
    borrows = [b for b in borrows if b[1] == current_user]

    return render_template('my_borrows.html', borrows=borrows, filter_status=filter_status)


@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = read_file('reservations.txt')

    if request.method == 'POST':
        reservation_id = request.form.get('cancel_reservation_id')
        reservations_all = read_file('reservations.txt')
        for r in reservations_all:
            if r[0] == reservation_id and r[1] == current_user and r[4] == 'Active':
                r[4] = 'Canceled'
                break
        write_file('reservations.txt', reservations_all)
        return redirect(url_for('my_reservations'))

    # Show only current user active reservations
    user_reservations = [r for r in reservations if r[1] == current_user and r[4] == 'Active']
    return render_template('my_reservations.html', reservations=user_reservations)


@app.route('/my-reviews', methods=['GET', 'POST'])
def my_reviews():
    reviews = read_file('reviews.txt')
    books = read_file('books.txt')

    if request.method == 'POST':
        delete_review_id = request.form.get('delete_review_id')
        if delete_review_id:
            reviews_all = read_file('reviews.txt')
            reviews_all = [r for r in reviews_all if not (r[0] == delete_review_id and r[1] == current_user)]
            write_file('reviews.txt', reviews_all)
            return redirect(url_for('my_reviews'))

    user_reviews = [r for r in reviews if r[1] == current_user]
    return render_template('my_reviews.html', reviews=user_reviews)


@app.route('/write-review/<int:book_id>', methods=['GET', 'POST'])
def write_review(book_id):
    book = find_book(book_id)
    if not book:
        return 'Book not found', 404
    reviews = read_file('reviews.txt')
    existing_review = None
    for r in reviews:
        if r[1] == current_user and r[2] == str(book_id):
            existing_review = r
            break

    if request.method == 'GET':
        return render_template('write_review.html', book=book, existing_review=existing_review)
    else:
        rating = request.form.get('rating_input')
        review_text = request.form.get('review_text')
        reviews_all = read_file('reviews.txt')
        review_date = datetime.now().strftime('%Y-%m-%d')

        if existing_review:
            # Update existing
            for r in reviews_all:
                if r[0] == existing_review[0]:
                    r[3] = rating
                    r[4] = review_text
                    r[5] = review_date
                    break
        else:
            review_id = 1
            if reviews_all:
                review_id = int(reviews_all[-1][0]) + 1
            new_review = [str(review_id), current_user, str(book_id), rating, review_text, review_date]
            reviews_all.append(new_review)

        write_file('reviews.txt', reviews_all)

        # Update book average rating
        books = read_file('books.txt')
        for b in books:
            if b[0] == str(book_id):
                b[9] = calculate_avg_rating(book_id)
                break
        write_file('books.txt', books)

        return redirect(url_for('book_details', book_id=book_id))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = find_user(current_user)
    if request.method == 'POST':
        new_email = request.form.get('profile_email')
        users = read_file('users.txt')
        for u in users:
            if u[0] == current_user:
                u[1] = new_email
                break
        write_file('users.txt', users)
        return redirect(url_for('profile'))

    email = user[1] if user else ''

    # Borrow history
    borrows = read_file('borrowings.txt')
    borrow_history = [b for b in borrows if b[1] == current_user]

    return render_template('profile.html', username=current_user, email=email, borrow_history=borrow_history)


@app.route('/payment/<int:fine_id>', methods=['GET', 'POST'])
def payment(fine_id):
    fine = find_fine(fine_id)
    if not fine:
        return 'Fine not found', 404
    if request.method == 'POST':
        # Mark fine as paid
        fines = read_file('fines.txt')
        for f in fines:
            if f[0] == str(fine_id):
                f[4] = 'Paid'
                break
        write_file('fines.txt', fines)
        return redirect(url_for('profile'))

    return render_template('payment_confirmation.html', fine=fine)


if __name__ == '__main__':
    app.run(debug=True)
