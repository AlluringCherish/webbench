'''
Utility module to load and parse text files from the 'data' directory.
Provides functions to read users, books, borrowings, reservations, reviews, and fines data.
All data is pipe-delimited and read from the 'data' folder.
'''
import os
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
def _read_file_lines(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    return [line for line in lines if line.strip()]
def load_users():
    '''
    Load users from users.txt
    Returns list of dicts with keys: username, email, phone, address
    '''
    lines = _read_file_lines('users.txt')
    users = []
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
def load_books():
    '''
    Load books from books.txt
    Returns list of dicts with keys:
    book_id, title, author, isbn, genre, publisher, year, description, status, avg_rating
    '''
    lines = _read_file_lines('books.txt')
    books = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 10:
            books.append({
                'book_id': parts[0],
                'title': parts[1],
                'author': parts[2],
                'isbn': parts[3],
                'genre': parts[4],
                'publisher': parts[5],
                'year': parts[6],
                'description': parts[7],
                'status': parts[8],
                'avg_rating': parts[9]
            })
    return books
def load_borrowings():
    '''
    Load borrowings from borrowings.txt
    Returns list of dicts with keys:
    borrow_id, username, book_id, borrow_date, due_date, return_date, status, fine_amount
    '''
    lines = _read_file_lines('borrowings.txt')
    borrowings = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 8:
            borrowings.append({
                'borrow_id': parts[0],
                'username': parts[1],
                'book_id': parts[2],
                'borrow_date': parts[3],
                'due_date': parts[4],
                'return_date': parts[5],
                'status': parts[6],
                'fine_amount': parts[7]
            })
    return borrowings
def load_reservations():
    '''
    Load reservations from reservations.txt
    Returns list of dicts with keys:
    reservation_id, username, book_id, reservation_date, status
    '''
    lines = _read_file_lines('reservations.txt')
    reservations = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 5:
            reservations.append({
                'reservation_id': parts[0],
                'username': parts[1],
                'book_id': parts[2],
                'reservation_date': parts[3],
                'status': parts[4]
            })
    return reservations
def load_reviews():
    '''
    Load reviews from reviews.txt
    Returns list of dicts with keys:
    review_id, username, book_id, rating, review_text, review_date
    '''
    lines = _read_file_lines('reviews.txt')
    reviews = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 6:
            reviews.append({
                'review_id': parts[0],
                'username': parts[1],
                'book_id': parts[2],
                'rating': parts[3],
                'review_text': parts[4],
                'review_date': parts[5]
            })
    return reviews
def load_fines():
    '''
    Load fines from fines.txt
    Returns list of dicts with keys:
    fine_id, username, borrow_id, amount, status, date_issued
    '''
    lines = _read_file_lines('fines.txt')
    fines = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 6:
            fines.append({
                'fine_id': parts[0],
                'username': parts[1],
                'borrow_id': parts[2],
                'amount': parts[3],
                'status': parts[4],
                'date_issued': parts[5]
            })
    return fines