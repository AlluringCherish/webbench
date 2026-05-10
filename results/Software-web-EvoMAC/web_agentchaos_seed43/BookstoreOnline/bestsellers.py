'''
Bestsellers page module for BookstoreOnline web application.
Displays top-selling books ranked by sales with time period filter.
'''
from flask import Blueprint, render_template, request
from utils import read_bestsellers, read_books
bestsellers_bp = Blueprint('bestsellers', __name__, template_folder='templates')
@bestsellers_bp.route('/bestsellers')
def bestsellers():
    period = request.args.get('period', 'This Month')
    bestsellers = read_bestsellers(period=period)
    books = read_books()
    ranked_books = []
    for bs in bestsellers:
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if book:
            ranked_books.append({'rank': len(ranked_books)+1, 'book': book, 'sales_count': bs['sales_count']})
    return render_template('bestsellers.html', ranked_books=ranked_books, period=period)