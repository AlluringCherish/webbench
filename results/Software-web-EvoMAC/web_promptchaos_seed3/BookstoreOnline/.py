LANGUAGE: Python
DOCSTRING
'''
This is the complete backend code file `app.py` for the 'BookstoreOnline' web application.
It implements all required routes, data reading/writing functions, and business logic
to support the features described in the project specification.
The application uses Flask and reads/writes data from local text files in the `data/` directory.
It supports browsing books, viewing details, managing a shopping cart, checkout, order history,
customer reviews, writing reviews, and viewing bestsellers.
All code is contained in this single file as requested.
'''
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'data'
# Utility functions to read/write data files
def read_books():
    """Read books data from books.txt and return a list of book dicts."""
    books = []
    path = os.path.join(DATA_DIR, 'books.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
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
    return books
def read_categories():
    """Read categories data from categories.txt and return a list of category dicts."""
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                category = {
                    'category_id': parts[0],
                    'category_name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
    return categories
def read_cart():
    """Read cart items from cart.txt and return a list of cart item dicts."""
    cart_items = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                item = {
                    'cart_id': parts[0],
                    'book_id': parts[1],
                    'quantity': int(parts[2]),
                    'added_date': parts[3]
                }
                cart_items.append(item)
    return cart_items
def write_cart(cart_items):
    """Write cart items list to cart.txt."""
    path = os.path.join(DATA_DIR, 'cart.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for item in cart_items:
            line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
            f.write(line)
def read_orders():
    """Read orders from orders.txt and return a list of order dicts."""
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                order = {
                    'order_id': parts[0],
                    'customer_name': parts[1],
                    'order_date': parts[2],
                    'total_amount': float(parts[3]),
                    'status': parts[4],
                    'shipping_address': parts[5]
                }
                orders.append(order)
    return orders
def write_orders(orders):
    """Write orders list to orders.txt."""
    path = os.path.join(DATA_DIR, 'orders.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for order in orders:
            line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']:.2f}|{order['status']}|{order['shipping_address']}\n"
            f.write(line)
def read_order_items():
    """Read order items from order_items.txt and return a list of order item dicts."""
    order_items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                item = {
                    'order_item_id': parts[0],
                    'order_id': parts[1],
                    'book_id': parts[2],
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(item)
    return order_items
def write_order_items(order_items):
    """Write order items list to order_items.txt."""
    path = os.path.join(DATA_DIR, 'order_items.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for item in order_items:
            line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']:.2f}\n"
            f.write(line)
def read_reviews():
    """Read reviews from reviews.txt and return a list of review dicts."""
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                review = {
                    'review_id': parts[0],
                    'book_id': parts[1],
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews.append(review)
    return reviews
def write_reviews(reviews):
    """Write reviews list to reviews.txt."""
    path = os.path.join(DATA_DIR, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for review in reviews:
            line = f"{review['review_id']}|{review['book_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}\n"
            f.write(line)
def read_bestsellers():
    """Read bestsellers from bestsellers.txt and return a list of bestseller dicts."""
    bestsellers = []
    path = os.path.join(DATA_DIR, 'bestsellers.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                bestseller = {
                    'book_id': parts[0],
                    'sales_count': int(parts[1]),
                    'period': parts[2]
                }
                bestsellers.append(bestseller)
    return bestsellers
def get_next_id(items, id_field):
    """Get next integer ID as string for a list of dicts with id_field."""
    max_id = 0
    for item in items:
        try:
            current_id = int(item[id_field])
            if current_id > max_id:
                max_id = current_id
        except:
            continue
    return str(max_id + 1)
# Routes
@app.route('/')
def dashboard():
    """Dashboard page showing featured books and bestsellers."""
    books = read_books()
    featured_books = books[:3]  # first 3 books as featured
    bestsellers_data = read_bestsellers()
    # Filter bestsellers for current month
    bestsellers_this_month = [b for b in bestsellers_data if b['period'] == 'Month']
    # Sort descending by sales_count
    bestsellers_this_month.sort(key=lambda x: x['sales_count'], reverse=True)
    books_dict = {b['book_id']: b for b in books}
    bestsellers = []
    for b in bestsellers_this_month:
        book = books_dict.get(b['book_id'])
        if book:
            bestsellers.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })
    return render_template('dashboard.html',
                           featured_books=featured_books,
                           bestsellers=bestsellers)
@app.route('/catalog')
def catalog():
    """Book catalog page with search and category filter."""
    books = read_books()
    categories = read_categories()
    search_query = request.args.get('search', '').strip().lower()
    selected_category = request.args.get('category', 'All')
    filtered_books = books
    if search_query:
        filtered_books = [b for b in filtered_books if search_query in b['title'].lower() or search_query in b['author'].lower() or search_query in b['isbn'].lower()]
    if selected_category and selected_category != 'All':
        filtered_books = [b for b in filtered_books if b['category'] == selected_category]
    return render_template('catalog.html',
                           books=filtered_books,
                           categories=categories,
                           selected_category=selected_category,
                           search_query=search_query)
@app.route('/book/<book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    """Book details page with add to cart functionality."""
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404
    reviews = read_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]
    if request.method == 'POST':
        quantity_str = request.form.get('quantity', '1')
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                quantity = 1
        except:
            quantity = 1
        cart_items = read_cart()
        # Check if book already in cart
        found = False
        for item in cart_items:
            if item['book_id'] == book_id:
                item['quantity'] += quantity
                found = True
                break
        if not found:
            new_cart_id = get_next_id(cart_items, 'cart_id')
            cart_items.append({
                'cart_id': new_cart_id,
                'book_id': book_id,
                'quantity': quantity,
                'added_date': datetime.now().strftime('%Y-%m-%d')
            })
        write_cart(cart_items)
        return redirect(url_for('cart'))
    return render_template('book_details.html',
                           book=book,
                           reviews=book_reviews)
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    """Shopping cart page with update and remove item functionality."""
    books = read_books()
    cart_items = read_cart()
    books_dict = {b['book_id']: b for b in books}
    if request.method == 'POST':
        form = request.form
        cart_changed = False
        for item in cart_items[:]:
            remove_key = f'remove-item-button-{item["cart_id"]}'
            qty_key = f'update-quantity-{item["cart_id"]}'
            if remove_key in form:
                cart_items.remove(item)
                cart_changed = True
                continue
            if qty_key in form:
                try:
                    new_qty = int(form[qty_key])
                    if new_qty < 1:
                        new_qty = 1
                    if new_qty != item['quantity']:
                        item['quantity'] = new_qty
                        cart_changed = True
                except:
                    pass
        if cart_changed:
            write_cart(cart_items)
        return redirect(url_for('cart'))
    display_items = []
    total_amount = 0.0
    for item in cart_items:
        book = books_dict.get(item['book_id'])
        if not book:
            continue
        subtotal = book['price'] * item['quantity']
        total_amount += subtotal
        display_items.append({
            'cart_id': item['cart_id'],
            'book_id': book['book_id'],
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
    """Checkout page to enter shipping and payment info and place order."""
    cart_items = read_cart()
    if not cart_items:
        return redirect(url_for('dashboard'))
    books = read_books()
    books_dict = {b['book_id']: b for b in books}
    total_amount = 0.0
    for item in cart_items:
        book = books_dict.get(item['book_id'])
        if book:
            total_amount += book['price'] * item['quantity']
    error = None
    customer_name = ''
    shipping_address = ''
    payment_method = ''
    if request.method == 'POST':
        customer_name = request.form.get('customer-name', '').strip()
        shipping_address = request.form.get('shipping-address', '').strip()
        payment_method = request.form.get('payment-method', '').strip()
        if not customer_name or not shipping_address or not payment_method:
            error = "Please fill in all required fields."
        else:
            orders = read_orders()
            order_items = read_order_items()
            new_order_id = get_next_id(orders, 'order_id')
            order_date = datetime.now().strftime('%Y-%m-%d')
            status = 'Pending'
            new_order = {
                'order_id': new_order_id,
                'customer_name': customer_name,
                'order_date': order_date,
                'total_amount': total_amount,
                'status': status,
                'shipping_address': shipping_address
            }
            orders.append(new_order)
            write_orders(orders)
            next_order_item_id = get_next_id(order_items, 'order_item_id')
            for item in cart_items:
                book = books_dict.get(item['book_id'])
                if not book:
                    continue
                order_item = {
                    'order_item_id': next_order_item_id,
                    'order_id': new_order_id,
                    'book_id': book['book_id'],
                    'quantity': item['quantity'],
                    'price': book['price']
                }
                order_items.append(order_item)
                next_order_item_id = str(int(next_order_item_id) + 1)
            write_order_items(order_items)
            # Clear cart after order placed
            write_cart([])
            return redirect(url_for('orders'))
    return render_template('checkout.html',
                           error=error,
                           customer_name=customer_name,
                           shipping_address=shipping_address,
                           payment_method=payment_method,
                           total_amount=total_amount)
@app.route('/orders')
def orders():
    """Order history page with optional status filter."""
    orders = read_orders()
    status_filter = request.args.get('status', 'All')
    if status_filter != 'All':
        filtered_orders = [o for o in orders if o['status'] == status_filter]
    else:
        filtered_orders = orders
    return render_template('order_history.html',
                           orders=filtered_orders,
                           selected_status=status_filter)
@app.route('/order/<order_id>')
def order_details(order_id):
    """View details of a specific order."""
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404
    order_items = read_order_items()
    books = read_books()
    books_dict = {b['book_id']: b for b in books}
    items = []
    for item in order_items:
        if item['order_id'] == order_id:
            book = books_dict.get(item['book_id'])
            if book:
                items.append({
                    'order_item_id': item['order_item_id'],
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'subtotal': item['price'] * item['quantity']
                })
    return render_template('order_details.html',
                           order=order,
                           items=items)
@app.route('/reviews')
def reviews():
    """Customer reviews page with rating filter."""
    reviews = read_reviews()
    books = read_books()
    books_dict = {b['book_id']: b for b in books}
    selected_rating = request.args.get('rating', 'All')
    filtered_reviews = reviews
    if selected_rating != 'All':
        try:
            rating_val = int(selected_rating[0])  # e.g. '5 stars' -> 5
            filtered_reviews = [r for r in reviews if r['rating'] == rating_val]
        except:
            pass
    display_reviews = []
    for r in filtered_reviews:
        book = books_dict.get(r['book_id'])
        if book:
            display_reviews.append({
                'review_id': r['review_id'],
                'book_title': book['title'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'customer_name': r['customer_name'],
                'review_date': r['review_date']
            })
    return render_template('reviews.html',
                           reviews=display_reviews,
                           selected_rating=selected_rating)
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    """Page to write a new review for a purchased book."""
    books = read_books()
    error = None
    selected_book = None
    selected_rating = None
    review_text = ''
    if request.method == 'POST':
        selected_book = request.form.get('select-book')
        rating_str = request.form.get('rating')
        review_text = request.form.get('review-text', '').strip()
        customer_name = request.form.get('customer-name', 'Anonymous').strip()
        if not customer_name:
            customer_name = 'Anonymous'
        if not selected_book or not rating_str or not review_text:
            error = "Please fill in all required fields."
        else:
            try:
                rating_int = int(rating_str)
                if rating_int < 1 or rating_int > 5:
                    raise ValueError()
            except:
                error = "Invalid rating value."
            if not error:
                reviews = read_reviews()
                new_review_id = get_next_id(reviews, 'review_id')
                review_date = datetime.now().strftime('%Y-%m-%d')
                new_review = {
                    'review_id': new_review_id,
                    'book_id': selected_book,
                    'customer_name': customer_name,
                    'rating': rating_int,
                    'review_text': review_text,
                    'review_date': review_date
                }
                reviews.append(new_review)
                write_reviews(reviews)
                return redirect(url_for('reviews'))
    return render_template('write_review.html',
                           books=books,
                           error=error,
                           selected_book=selected_book,
                           selected_rating=selected_rating,
                           review_text=review_text)
@app.route('/bestsellers')
def bestsellers():
    """Bestsellers page with time period filter."""
    books = read_books()
    bestsellers_data = read_bestsellers()
    time_period = request.args.get('time_period', 'Month')
    filtered_bestsellers = [b for b in bestsellers_data if b['period'] == time_period]
    filtered_bestsellers.sort(key=lambda x: x['sales_count'], reverse=True)
    books_dict = {b['book_id']: b for b in books}
    bestsellers = []
    for b in filtered_bestsellers:
        book = books_dict.get(b['book_id'])
        if book:
            bestsellers.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })
    return render_template('bestsellers.html',
                           bestsellers=bestsellers,
                           selected_period=time_period)
if __name__ == '__main__':
    app.run(debug=True)