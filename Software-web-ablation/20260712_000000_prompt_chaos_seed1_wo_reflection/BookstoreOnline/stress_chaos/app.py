import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions

def read_file_lines(filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def write_file_lines(filename, lines):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines) + '\n')

# Loaders

def load_books():
    books = []
    lines = read_file_lines('books.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) < 8:
            continue
        book = {
            'book_id': int(parts[0]),
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

def load_categories():
    categories = []
    lines = read_file_lines('categories.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 3:
            continue
        category = {
            'category_id': int(parts[0]),
            'category_name': parts[1],
            'description': parts[2]
        }
        categories.append(category)
    return categories

def load_cart():
    cart = []
    lines = read_file_lines('cart.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 4:
            continue
        item = {
            'cart_id': int(parts[0]),
            'book_id': int(parts[1]),
            'quantity': int(parts[2]),
            'added_date': parts[3]
        }
        cart.append(item)
    return cart

def save_cart(cart):
    lines = [f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}" for item in cart]
    write_file_lines('cart.txt', lines)

def load_orders():
    orders = []
    lines = read_file_lines('orders.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 6:
            continue
        order = {
            'order_id': int(parts[0]),
            'customer_name': parts[1],
            'order_date': parts[2],
            'total_amount': float(parts[3]),
            'status': parts[4],
            'shipping_address': parts[5]
        }
        orders.append(order)
    return orders

def save_orders(orders):
    lines = [f"{o['order_id']}|{o['customer_name']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['shipping_address']}" for o in orders]
    write_file_lines('orders.txt', lines)

def load_order_items():
    order_items = []
    lines = read_file_lines('order_items.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 5:
            continue
        item = {
            'order_item_id': int(parts[0]),
            'order_id': int(parts[1]),
            'book_id': int(parts[2]),
            'quantity': int(parts[3]),
            'price': float(parts[4])
        }
        order_items.append(item)
    return order_items

def save_order_items(order_items):
    lines = [f"{i['order_item_id']}|{i['order_id']}|{i['book_id']}|{i['quantity']}|{i['price']}" for i in order_items]
    write_file_lines('order_items.txt', lines)

def load_reviews():
    reviews = []
    lines = read_file_lines('reviews.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 6:
            continue
        review = {
            'review_id': int(parts[0]),
            'book_id': int(parts[1]),
            'customer_name': parts[2],
            'rating': int(parts[3]),
            'review_text': parts[4],
            'review_date': parts[5]
        }
        reviews.append(review)
    return reviews

def save_reviews(reviews):
    lines = [f"{r['review_id']}|{r['book_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}" for r in reviews]
    write_file_lines('reviews.txt', lines)

def load_bestsellers():
    bestsellers = []
    lines = read_file_lines('bestsellers.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 3:
            continue
        try:
            bs = {
                'book_id': int(parts[0]),
                'sales_count': int(parts[1]),
                'period': parts[2]
            }
            bestsellers.append(bs)
        except Exception:
            continue
    return bestsellers


# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    books = load_books()
    featured_books = books[:5]
    bestsellers_all = load_bestsellers()
    books_map = {b['book_id']: b for b in books}

    # Filter bestsellers for "This Month"
    bestsellers = []
    for bs in bestsellers_all:
        if bs['period'] == 'This Month':
            book = books_map.get(bs['book_id'])
            if book:
                bestsellers.append({
                    'book_id': book['book_id'],
                    'title': book['title'],
                    'author': book['author'],
                    'sales_count': bs['sales_count'],
                    'period': bs['period']
                })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)

@app.route('/catalog')
def book_catalog():
    categories = load_categories()
    books = load_books()

    selected_category = request.args.get('category_filter', '')
    search_query = request.args.get('search_query', '').strip().lower()

    if selected_category:
        try:
            selected_category_id = int(selected_category)
            books = [b for b in books if b['category'] == next((c['category_name'] for c in categories if c['category_id'] == selected_category_id), '')]
        except:
            pass

    if search_query:
        books = [b for b in books if search_query in b['title'].lower() or search_query in b['author'].lower()]

    return render_template('catalog.html', categories=categories, books=books, selected_category=selected_category, search_query=search_query)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = load_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404

    if request.method == 'POST':
        cart = load_cart()
        existing_item = next((item for item in cart if item['book_id'] == book_id), None)
        if existing_item:
            existing_item['quantity'] += 1
        else:
            new_id = max([item['cart_id'] for item in cart], default=0) + 1
            cart.append({
                'cart_id': new_id,
                'book_id': book_id,
                'quantity': 1,
                'added_date': datetime.now().strftime('%Y-%m-%d')
            })
        save_cart(cart)
        return redirect(url_for('shopping_cart'))

    reviews_all = load_reviews()
    reviews = [r for r in reviews_all if r['book_id'] == book_id]
    return render_template('book_details.html', book=book, reviews=reviews)

@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    books = load_books()
    books_map = {b['book_id']: b for b in books}
    cart = load_cart()

    if request.method == 'POST':
        # Update quantities
        updates = {int(k.split('_')[1]): int(v) for k, v in request.form.items() if k.startswith('quantity_')}
        new_cart = []
        for item in cart:
            new_qty = updates.get(item['book_id'], item['quantity'])
            if new_qty > 0:
                item['quantity'] = new_qty
                new_cart.append(item)
        save_cart(new_cart)
        return redirect(url_for('shopping_cart'))

    cart_items = []
    total_amount = 0.0
    for item in cart:
        book = books_map.get(item['book_id'])
        if not book:
            continue
        subtotal = item['quantity'] * book['price']
        total_amount += subtotal
        cart_items.append({
            'cart_id': item['cart_id'],
            'book_id': book['book_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': book['price'],
            'subtotal': subtotal
        })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not shipping_address or payment_method not in ['Credit Card', 'PayPal', 'Bank Transfer']:
            return "Please fill all required fields with valid payment method.", 400

        cart = load_cart()
        if not cart:
            return redirect(url_for('shopping_cart'))

        books = load_books()
        books_map = {b['book_id']: b for b in books}

        total_amount = 0.0
        for item in cart:
            book = books_map.get(item['book_id'])
            if not book:
                continue
            total_amount += item['quantity'] * book['price']

        orders = load_orders()
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        today_str = datetime.now().strftime('%Y-%m-%d')

        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': today_str,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }
        orders.append(new_order)
        save_orders(orders)

        order_items = load_order_items()
        max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)

        for i, item in enumerate(cart, start=1):
            book = books_map.get(item['book_id'])
            if not book:
                continue
            order_item = {
                'order_item_id': max_order_item_id + i,
                'order_id': new_order_id,
                'book_id': item['book_id'],
                'quantity': item['quantity'],
                'price': book['price']
            }
            order_items.append(order_item)

        save_order_items(order_items)

        # Clear cart after order
        save_cart([])

        return redirect(url_for('orders_page'))

    return render_template('checkout.html')

@app.route('/orders')
def orders_page():
    status_filter = request.args.get('status', 'All')
    orders = load_orders()
    if status_filter != 'All':
        orders = [o for o in orders if o['status'] == status_filter]
    return render_template('orders.html', orders=orders, status_filter=status_filter)

@app.route('/reviews')
def reviews_page():
    rating_filter = request.args.get('rating', 'All')
    reviews = load_reviews()
    books = load_books()
    books_map = {b['book_id']: b for b in books}
    if rating_filter != 'All':
        try:
            rating_val = int(rating_filter)
            reviews = [r for r in reviews if r['rating'] == rating_val]
        except:
            pass
    reviews_with_titles = []
    for r in reviews:
        book_title = books_map.get(r['book_id'], {}).get('title', 'Unknown')
        reviews_with_titles.append({
            'review_id': r['review_id'],
            'book_id': r['book_id'],
            'book_title': book_title,
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })
    return render_template('reviews.html', reviews=reviews_with_titles, rating_filter=rating_filter)

@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    books = load_books()
    if request.method == 'POST':
        try:
            book_id = int(request.form.get('book_id'))
            rating = int(request.form.get('rating'))
            if rating < 1 or rating > 5:
                raise ValueError('Rating must be between 1 and 5')
        except:
            return "Invalid rating or book ID", 400

        customer_name = request.form.get('customer_name', '').strip()
        review_text = request.form.get('review_text', '').strip()

        if not customer_name or not review_text:
            return "Name and review text are required", 400

        reviews = load_reviews()
        new_review_id = max([r['review_id'] for r in reviews], default=0) + 1
        today_str = datetime.now().strftime('%Y-%m-%d')

        new_review = {
            'review_id': new_review_id,
            'book_id': book_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': today_str
        }
        reviews.append(new_review)
        save_reviews(reviews)

        return redirect(url_for('reviews_page'))

    return render_template('write_review.html', books=books)

@app.route('/bestsellers')
def bestsellers_page():
    period = request.args.get('period', 'Month')
    bestsellers_all = load_bestsellers()
    books = load_books()
    books_map = {b['book_id']: b for b in books}

    filtered_bestsellers = [bs for bs in bestsellers_all if period in bs['period']]
    bestsellers = []

    for bs in filtered_bestsellers:
        book = books_map.get(bs['book_id'])
        if book:
            bestsellers.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count'],
                'period': bs['period']
            })

    return render_template('bestsellers.html', bestsellers=bestsellers, time_period=period)

if __name__ == '__main__':
    app.run(debug=True)
