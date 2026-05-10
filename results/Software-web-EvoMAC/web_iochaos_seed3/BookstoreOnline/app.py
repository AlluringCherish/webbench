'''
Main backend application for BookstoreOnline web application.
Defines all routes including the root '/' route serving the Dashboard page,
ensuring compliance with the requirement that the website starts from the Dashboard page.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
app = Flask(__name__)
DATA_DIR = 'data'
def read_books():
    books = []
    try:
        with open(os.path.join(DATA_DIR, 'books.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 8:
                        book = {
                            'book_id': parts[0],
                            'title': parts[1],
                            'author': parts[2],
                            'isbn': parts[3],
                            'category': parts[4],
                            'price': float(parts[5]),
                            'stock': int(parts[6]),
                            'description': parts[7]
                        }
                        books.append(book)
    except FileNotFoundError:
        pass
    return books
def read_categories():
    categories = []
    try:
        with open(os.path.join(DATA_DIR, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 3:
                        category = {
                            'category_id': parts[0],
                            'category_name': parts[1],
                            'description': parts[2]
                        }
                        categories.append(category)
    except FileNotFoundError:
        pass
    return categories
def read_bestsellers(period='This Month'):
    bestsellers = []
    try:
        with open(os.path.join(DATA_DIR, 'bestsellers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 3 and parts[2] == period:
                        bestsellers.append({
                            'book_id': parts[0],
                            'sales_count': int(parts[1]),
                            'period': parts[2]
                        })
    except FileNotFoundError:
        pass
    return bestsellers
def get_book_by_id(book_id):
    books = read_books()
    for book in books:
        if book['book_id'] == str(book_id):
            return book
    return None
def read_cart():
    cart_items = []
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 4:
                        cart_items.append({
                            'cart_id': parts[0],
                            'book_id': parts[1],
                            'quantity': int(parts[2]),
                            'added_date': parts[3]
                        })
    except FileNotFoundError:
        pass
    return cart_items
def write_cart(cart_items):
    with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
        for item in cart_items:
            line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
            f.write(line)
def read_reviews(book_id=None, rating_filter=None):
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 6:
                        review = {
                            'review_id': parts[0],
                            'book_id': parts[1],
                            'customer_name': parts[2],
                            'rating': int(parts[3]),
                            'review_text': parts[4],
                            'review_date': parts[5]
                        }
                        if book_id and review['book_id'] != str(book_id):
                            continue
                        if rating_filter and rating_filter != 'All':
                            try:
                                rating_val = int(rating_filter[0])
                                if review['rating'] != rating_val:
                                    continue
                            except:
                                pass
                        reviews.append(review)
    except FileNotFoundError:
        pass
    return reviews
def read_orders(status_filter=None):
    orders = []
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 6:
                        order = {
                            'order_id': parts[0],
                            'customer_name': parts[1],
                            'order_date': parts[2],
                            'total_amount': float(parts[3]),
                            'status': parts[4],
                            'shipping_address': parts[5]
                        }
                        if status_filter and status_filter != 'All' and order['status'] != status_filter:
                            continue
                        orders.append(order)
    except FileNotFoundError:
        pass
    return orders
def read_order_items(order_id):
    items = []
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) == 5 and parts[1] == str(order_id):
                        items.append({
                            'order_item_id': parts[0],
                            'order_id': parts[1],
                            'book_id': parts[2],
                            'quantity': int(parts[3]),
                            'price': float(parts[4])
                        })
    except FileNotFoundError:
        pass
    return items
def get_next_id(filename):
    max_id = 0
    try:
        with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    try:
                        current_id = int(parts[0])
                        if current_id > max_id:
                            max_id = current_id
                    except:
                        pass
    except FileNotFoundError:
        pass
    return max_id + 1
@app.route('/')
def dashboard():
    '''
    Route for root URL '/' serving the Dashboard page.
    Loads featured books and bestsellers for display.
    '''
    books = read_books()
    # For featured books, pick first 3 books as example
    featured_books = books[:3]
    bestsellers_data = read_bestsellers('This Month')
    # Map bestsellers to book details
    bestsellers = []
    for bs in bestsellers_data:
        book = get_book_by_id(bs['book_id'])
        if book:
            bestsellers.append({
                'rank': len(bestsellers) + 1,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count']
            })
    return render_template('dashboard.html',
                           featured_books=featured_books,
                           bestsellers=bestsellers)
@app.route('/catalog')
def catalog():
    '''
    Book Catalog page with search and category filter.
    '''
    books = read_books()
    categories = read_categories()
    search_query = request.args.get('search', '').lower()
    category_filter = request.args.get('category', '')
    filtered_books = []
    for book in books:
        if search_query:
            if (search_query not in book['title'].lower() and
                search_query not in book['author'].lower() and
                search_query not in book['isbn'].lower()):
                continue
        if category_filter and category_filter != 'All':
            if book['category'] != category_filter:
                continue
        filtered_books.append(book)
    return render_template('catalog.html',
                           books=filtered_books,
                           categories=categories,
                           selected_category=category_filter,
                           search_query=search_query)
@app.route('/book/<book_id>')
def book_details(book_id):
    '''
    Book Details page showing detailed info and reviews.
    '''
    book = get_book_by_id(book_id)
    if not book:
        return "Book not found", 404
    reviews = read_reviews(book_id=book_id)
    return render_template('book_details.html',
                           book=book,
                           reviews=reviews)
@app.route('/add_to_cart/<book_id>', methods=['POST'])
def add_to_cart(book_id):
    '''
    Add a book to the shopping cart.
    '''
    cart_items = read_cart()
    # Check if book already in cart
    for item in cart_items:
        if item['book_id'] == book_id:
            item['quantity'] += 1
            break
    else:
        new_id = get_next_id('cart.txt')
        cart_items.append({
            'cart_id': str(new_id),
            'book_id': book_id,
            'quantity': 1,
            'added_date': datetime.date.today().isoformat()
        })
    write_cart(cart_items)
    return redirect(url_for('cart'))
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    '''
    Shopping Cart page with quantity update and item removal.
    '''
    cart_items = read_cart()
    books = read_books()
    book_dict = {b['book_id']: b for b in books}
    if request.method == 'POST':
        # Update quantities or remove items
        for item in cart_items[:]:
            qty_field = f'update-quantity-{item["cart_id"]}'
            remove_field = f'remove-item-button-{item["cart_id"]}'
            if remove_field in request.form:
                cart_items.remove(item)
            elif qty_field in request.form:
                try:
                    qty = int(request.form[qty_field])
                    if qty <= 0:
                        cart_items.remove(item)
                    else:
                        item['quantity'] = qty
                except:
                    pass
        write_cart(cart_items)
        return redirect(url_for('cart'))
    # Prepare cart display data
    display_items = []
    total_amount = 0.0
    for item in cart_items:
        book = book_dict.get(item['book_id'])
        if book:
            subtotal = book['price'] * item['quantity']
            total_amount += subtotal
            display_items.append({
                'cart_id': item['cart_id'],
                'title': book['title'],
                'quantity': item['quantity'],
                'price': book['price'],
                'subtotal': subtotal
            })
    return render_template('cart.html',
                           cart_items=display_items,
                           total_amount=total_amount)
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    '''
    Checkout page for entering shipping info and placing order.
    '''
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        shipping_address = request.form.get('shipping-address', '').strip()
        payment_method = request.form.get('payment-method', '').strip()
        if not customer_name or not shipping_address or not payment_method:
            error = "All fields are required."
            return render_template('checkout.html', error=error)
        cart_items = read_cart()
        if not cart_items:
            error = "Your cart is empty."
            return render_template('checkout.html', error=error)
        books = read_books()
        book_dict = {b['book_id']: b for b in books}
        total_amount = 0.0
        for item in cart_items:
            book = book_dict.get(item['book_id'])
            if book:
                total_amount += book['price'] * item['quantity']
        order_id = get_next_id('orders.txt')
        order_date = datetime.date.today().isoformat()
        status = 'Pending'
        # Save order
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'a', encoding='utf-8') as f:
            line = f"{order_id}|{customer_name}|{order_date}|{total_amount:.2f}|{status}|{shipping_address}\n"
            f.write(line)
        # Save order items
        order_item_id_start = get_next_id('order_items.txt')
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'a', encoding='utf-8') as f:
            order_item_id = order_item_id_start
            for item in cart_items:
                book = book_dict.get(item['book_id'])
                if book:
                    line = f"{order_item_id}|{order_id}|{book['book_id']}|{item['quantity']}|{book['price']:.2f}\n"
                    f.write(line)
                    order_item_id += 1
        # Clear cart
        write_cart([])
        return redirect(url_for('order_history'))
    return render_template('checkout.html')
@app.route('/orders')
def order_history():
    '''
    Order History page with status filter.
    '''
    status_filter = request.args.get('status', 'All')
    orders = read_orders(status_filter=status_filter)
    return render_template('orders.html',
                           orders=orders,
                           selected_status=status_filter)
@app.route('/order/<order_id>')
def order_details(order_id):
    '''
    View details of a specific order.
    '''
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404
    items = read_order_items(order_id)
    books = read_books()
    book_dict = {b['book_id']: b for b in books}
    detailed_items = []
    for item in items:
        book = book_dict.get(item['book_id'])
        if book:
            detailed_items.append({
                'title': book['title'],
                'quantity': item['quantity'],
                'price': item['price'],
                'subtotal': item['price'] * item['quantity']
            })
    return render_template('order_details.html',
                           order=order,
                           items=detailed_items)
@app.route('/reviews')
def reviews():
    '''
    Customer Reviews page with rating filter.
    '''
    rating_filter = request.args.get('rating', 'All')
    reviews = read_reviews(rating_filter=rating_filter)
    books = read_books()
    book_dict = {b['book_id']: b for b in books}
    # Add book title to each review
    for review in reviews:
        book = book_dict.get(review['book_id'])
        review['book_title'] = book['title'] if book else 'Unknown'
    return render_template('reviews.html',
                           reviews=reviews,
                           selected_rating=rating_filter)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    '''
    Write Review page for submitting new reviews.
    '''
    books = read_books()
    if request.method == 'POST':
        book_id = request.form.get('select-book')
        rating = request.form.get('rating-select')
        review_text = request.form.get('review-text', '').strip()
        customer_name = 'Anonymous'  # No authentication, so anonymous or could ask for name
        if not book_id or not rating or not review_text:
            error = "All fields are required."
            return render_template('write_review.html', books=books, error=error)
        review_id = get_next_id('reviews.txt')
        review_date = datetime.date.today().isoformat()
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a', encoding='utf-8') as f:
            line = f"{review_id}|{book_id}|{customer_name}|{rating}|{review_text}|{review_date}\n"
            f.write(line)
        return redirect(url_for('reviews'))
    return render_template('write_review.html', books=books)
@app.route('/bestsellers')
def bestsellers():
    '''
    Bestsellers page with time period filter.
    '''
    period = request.args.get('period', 'This Month')
    bestsellers_data = read_bestsellers(period)
    books = read_books()
    book_dict = {b['book_id']: b for b in books}
    bestsellers = []
    rank = 1
    for bs in bestsellers_data:
        book = book_dict.get(bs['book_id'])
        if book:
            bestsellers.append({
                'rank': rank,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count']
            })
            rank += 1
    return render_template('bestsellers.html',
                           bestsellers=bestsellers,
                           selected_period=period)
if __name__ == '__main__':
    app.run(debug=True)