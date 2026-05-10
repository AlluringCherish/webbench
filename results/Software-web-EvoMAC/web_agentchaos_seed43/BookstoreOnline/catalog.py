'''
Book Catalog page module for BookstoreOnline web application.
Displays all books with search and category filter.
'''
from flask import Blueprint, render_template, request
from utils import read_books, read_categories
catalog_bp = Blueprint('catalog', __name__, template_folder='templates')
@catalog_bp.route('/catalog')
def catalog():
    books = read_books()
    categories = read_categories()
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')
    filtered_books = books
    if search_query:
        filtered_books = [b for b in filtered_books if search_query in b['title'].lower() or search_query in b['author'].lower() or search_query in b['isbn']]
    if category_filter and category_filter != 'All':
        filtered_books = [b for b in filtered_books if b['category'] == category_filter]
    return render_template('catalog.html', books=filtered_books, categories=categories, selected_category=category_filter, search_query=search_query)