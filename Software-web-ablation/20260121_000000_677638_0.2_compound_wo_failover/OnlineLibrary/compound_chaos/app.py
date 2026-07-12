from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'bq0 secret key 4b6 ufw57a9 54i0e23sdd'  # Configure secret key as specified

# Data file paths, as per Section 3 / design_spec.md expected names
DATA_DIR = 'data'
BOOKS_FILE = os.path.join(DATA_DIR, 'books.txt')
USERS_FILE = os.path.join(DATA_DIR, 'users.txt')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.txt')
FINES_FILE = os.path.join(DATA_DIR, 'fines.txt')


# Load data files into appropriate structures
def load_books():
    books = {}
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
            # Assuming fields: book_id|title|author|year|... in designed order
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    book_id = parts[0]
                    books[book_id] = {
                        'book_id': book_id,
                        'title': parts[1],
                        'author': parts[2],
                        'year': parts[3],
                    }
    return books


def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            # Assuming fields: username|fullname|... as specified
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    username = parts[0]
                    users[username] = {
                        'username': username,
                        'fullname': parts[1],
                    }
    return users


def load_reservations():
    reservations = []
    if os.path.exists(RESERVATIONS_FILE):
        with open(RESERVATIONS_FILE, 'r', encoding='utf-8') as f:
            # Assuming format: reservation_id|username|book_id|borrow_date|due_date|status
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    reservations.append({
                        'reservation_id': parts[0],
                        'username': parts[1],
                        'book_id': parts[2],
                        'borrow_date': parts[3],
                        'due_date': parts[4],
                        'status': parts[5],  # e.g. Borrowed, Overdue, Returned
                    })
    return reservations


def load_fines():
    fines = []
    if os.path.exists(FINES_FILE):
        with open(FINES_FILE, 'r', encoding='utf-8') as f:
            # Assuming format: fine_id|username|amount|paid|date
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 5:
                    fines.append({
                        'fine_id': parts[0],
                        'username': parts[1],
                        'amount': parts[2],
                        'paid': parts[3],  # 0 or 1
                        'date': parts[4],
                    })
    return fines


def write_books(books):
    lines = []
    for b in books.values():
        line = f"{b['book_id']}|{b['title']}|{b['author']}|{b['year']}\n"
        lines.append(line)
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def write_reservations(reservations):
    lines = []
    for r in reservations:
        line = f"{r['reservation_id']}|{r['username']}|{r['book_id']}|{r['borrow_date']}|{r['due_date']}|{r['status']}\n"
        lines.append(line)
    with open(RESERVATIONS_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def write_fines(fines):
    lines = []
    for fine in fines:
        line = f"{fine['fine_id']}|{fine['username']}|{fine['amount']}|{fine['paid']}|{fine['date']}\n"
        lines.append(line)
    with open(FINES_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)


# Utility for date parsing and formatting
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        return None


def format_date(date_obj):
    return date_obj.strftime('%Y-%m-%d')


# Calculate overdue and update reservation status if past due date
def update_reservation_statuses(reservations):
    today = datetime.today()
    for r in reservations:
        if r['status'] == 'Borrowed':
            due_date_obj = parse_date(r['due_date'])
            if due_date_obj and due_date_obj < today:
                r['status'] = 'Overdue'


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in to view the dashboard.', 'warning')
        return redirect(url_for('login'))

    username = session['username']

    books = load_books()
    reservations = load_reservations()
    fines = load_fines()

    # Update status for reservations on load
    update_reservation_statuses(reservations)
    write_reservations(reservations)  # Save updated statuses

    # Filter user data
    user_reservations = [r for r in reservations if r['username'] == username]
    user_fines = [f for f in fines if f['username'] == username]

    # Get book info for each reservation
    for r in user_reservations:
        r['book'] = books.get(r['book_id'], {})

    return render_template('dashboard.html', reservations=user_reservations, fines=user_fines, username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        users = load_users()
        if username in users:
            session['username'] = username
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username.', 'danger')
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/books', methods=['GET'])
def books():
    if 'username' not in session:
        flash('Please log in to search books.', 'warning')
        return redirect(url_for('login'))

    search_title = request.args.get('title', '').strip().lower()
    search_author = request.args.get('author', '').strip().lower()

    books = load_books()

    filtered_books = []
    for book in books.values():
        if search_title and search_title not in book['title'].lower():
            continue
        if search_author and search_author not in book['author'].lower():
            continue
        filtered_books.append(book)

    return render_template('books.html', books=filtered_books, title=search_title, author=search_author)


@app.route('/reserve/<book_id>', methods=['POST'])
def reserve(book_id):
    if 'username' not in session:
        flash('Please log in to reserve books.', 'warning')
        return redirect(url_for('login'))

    books = load_books()
    if book_id not in books:
        flash('Book not found.', 'danger')
        return redirect(url_for('books'))

    reservations = load_reservations()

    username = session['username']
    # Check if user already has this book reserved and not returned
    for r in reservations:
        if r['book_id'] == book_id and r['username'] == username and r['status'] in ('Borrowed', 'Overdue'):
            flash('You already have this book reserved.', 'info')
            return redirect(url_for('dashboard'))

    # Create new reservation
    borrow_date = datetime.today()
    due_date = borrow_date + timedelta(days=14)  # 2 weeks borrow

    new_reservation = {
        'reservation_id': str(len(reservations) + 1),
        'username': username,
        'book_id': book_id,
        'borrow_date': format_date(borrow_date),
        'due_date': format_date(due_date),
        'status': 'Borrowed',
    }

    reservations.append(new_reservation)
    write_reservations(reservations)
    flash('Book reserved successfully.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/return/<reservation_id>', methods=['POST'])
def return_book(reservation_id):
    if 'username' not in session:
        flash('Please log in to return books.', 'warning')
        return redirect(url_for('login'))

    username = session['username']
    reservations = load_reservations()

    for r in reservations:
        if r['reservation_id'] == reservation_id and r['username'] == username:
            if r['status'] in ('Borrowed', 'Overdue'):
                r['status'] = 'Returned'
                write_reservations(reservations)
                flash('Book returned successfully.', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Book already returned.', 'info')
                return redirect(url_for('dashboard'))

    flash('Reservation not found.', 'danger')
    return redirect(url_for('dashboard'))


@app.route('/fines/pay/<fine_id>', methods=['POST'])
def pay_fine(fine_id):
    if 'username' not in session:
        flash('Please log in to pay fines.', 'warning')
        return redirect(url_for('login'))

    username = session['username']
    fines = load_fines()
    updated = False
    for fine in fines:
        if fine['fine_id'] == fine_id and fine['username'] == username and fine['paid'] == '0':
            fine['paid'] = '1'
            write_fines(fines)
            updated = True
            flash('Fine paid successfully.', 'success')
            break

    if not updated:
        flash('Fine not found or already paid.', 'danger')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure data directory exists
    app.run(debug=True)
