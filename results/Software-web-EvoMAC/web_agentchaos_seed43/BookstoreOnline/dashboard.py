'''
Dashboard page module for BookstoreOnline web application.
Displays featured books, bestsellers, and navigation buttons.
'''
import os
from flask import Blueprint, render_template, redirect, url_for
from utils import read_books, read_bestsellers
dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')
@dashboard_bp.route('/')
def dashboard():
    # Load featured books (e.g., top 3 bestsellers this month)
    bestsellers = read_bestsellers(period='This Month')
    books = read_books()
    featured_books = []
    for bs in bestsellers[:3]:
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if book:
            featured_books.append(book)
    return render_template('dashboard.html', featured_books=featured_books)