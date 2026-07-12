from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions for file read/write and parsing

def read_books():
    books = []
    path = os.path.join(DATA_DIR, 'books.txt')
    if not os.path.isfile(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue
            try:
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
            except:
                continue
    return books


def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.isfile(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) !=3:
                continue
            try:
                # category_id = int(parts[0]) unused
                category_name = parts[1]
                categories.append(category_name)
            except:
                continue
    return categories


def read_cart():
    cart = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    if not os.path.isfile(path):
        return cart
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) !=4:
                continue
            try:
                item = {
                    'item_id': int(parts[0]),  # cart_id
                    'book_id': int(parts[1]),
                    'quantity': int(parts[2]),
                    'added_date': parts[3]
                }
                cart.append(item)
            except:
                continue
    return cart


def write_cart(cart):
    path = os.path.join(DATA_DIR, 'cart.txt')
    lines = []
    for item in cart:
        # cart_id|book_id|quantity|added_date
        line = f"{item['item_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}"
        lines.append(line)
    content = '\n'.join(lines)
    return content


def read_orders():
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    if not os.path.isfile(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                order = {
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'order_date': parts[2],
                    'total_amount': float(parts[3]),
                    'status': parts[4],
                    'shipping_address': parts[5]
                }
                orders.append(order)
            except:
                continue
    return orders


def write_orders(orders):
    path = os.path.join(DATA_DIR, 'orders.txt')
    lines = []
    for order in orders:
        line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['shipping_address']}"
        lines.append(line)
    content = '\n'.join(lines)
    return content


def read_order_items():
    items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    if not os.path.isfile(path):
        return items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            try:
                item = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'book_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                items.append(item)
            except:
                continue
    return items


def write_order_items(items):
    path = os.path.join(DATA_DIR, 'order_items.txt')
    lines = []
    for item in items:
        line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']}"
        lines.append(line)
    content = '\n'.join(lines)
    return content


def read_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    if not os.path.isfile(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            try:
                review = {
                    'review_id': int(parts[0]),
                    'book_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews.append(review)
            except:
                continue
    return reviews


def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    lines = []
    for review in reviews:
        line = f"{review['review_id']}|{review['book_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}"
        lines.append(line)
    content = '\n'.join(lines)
    return content


def read_bestsellers():
    bestsellers = []
    path = os.path.join(DATA_DIR, 'bestsellers.txt')
    if not os.path.isfile(path):
        return bestsellers
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            try:
                bestseller = {
                    'book_id': int(parts[0]),
                    'sales_count': int(parts[1]),
                    'period': parts[2]
                }
                bestsellers.append(bestseller)
            except:
                continue
    return bestsellers


# Section 1 routes implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    books = read_books()
    bestsellers_raw = read_bestsellers()

    # Prepare featured_books for dashboard (best for demo: top 5 highest stock books)
    featured_books_list = sorted(books, key=lambda b: b['stock'], reverse=True)[:5]
    featured_books = []
    for b in featured_books_list:
        featured_books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price']
        })

    # Prepare bestsellers list for dashboard (just pick top 5 from any period, sorted by sales_count desc)
    bestsellers_sorted = sorted(bestsellers_raw, key=lambda x: x['sales_count'], reverse=True)[:5]
    bestsellers = []
    for bs in bestsellers_sorted:
        b = next((book for book in books if book['book_id'] == bs['book_id']), None)
        if not b:
            continue
        bestsellers.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'sales_count': bs['sales_count']
        })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)


@app.route('/catalog')
def book_catalog():
    books_all = read_books()
    categories = read_categories()

    search_query = request.args.get('search_query', '').strip()
    selected_category = request.args.get('selected_category', '')

    # Filter books by search_query (title, author, isbn)
    filtered_books = []
    for b in books_all:
        if search_query:
            if (search_query.lower() not in b['title'].lower() and 
                search_query.lower() not in b['author'].lower() and
                search_query.lower() not in b['isbn'].lower()):
                continue
        if selected_category and selected_category != 'All':
            if b['category'] != selected_category:
                continue
        filtered_books.append(b)

    # Prepare books list with required fields
    books = []
    for b in filtered_books:
        books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price'],
            'category': b['category']
        })

    return render_template('catalog.html', books=books, categories=categories, search_query=search_query, selected_category=selected_category)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        # Book not found, redirect to catalog
        return redirect(url_for('book_catalog'))

    if request.method == 'POST':
        # Handle add to cart POST
        try:
            quantity = int(request.form.get('quantity', '1'))
            if quantity < 1:
                quantity = 1
        except:
            quantity = 1

        cart = read_cart()
        # Check if this book already in cart, then increase quantity else add new record
        max_cart_id = max([item['item_id'] for item in cart], default=0)
        today_str = datetime.today().strftime('%Y-%m-%d')

        found = False
        for item in cart:
            if item['book_id'] == book_id:
                item['quantity'] += quantity
                found = True
                break
        if not found:
            new_cart_id = max_cart_id + 1
            cart.append({
                'item_id': new_cart_id,
                'book_id': book_id,
                'quantity': quantity,
                'added_date': today_str
            })
        try:
            content = write_cart(cart)
            with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
                f.write(content)
        except:
            pass

        return redirect(url_for('book_details', book_id=book_id))

    # GET request
    reviews_raw = read_reviews()
    reviews = []
    for r in reviews_raw:
        if r['book_id'] == book_id:
            reviews.append({
                'review_id': r['review_id'],
                'customer_name': r['customer_name'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })

    # Prepare book dict with required fields
    book_info = {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'price': book['price'],
        'description': book['description'],
        'stock': book['stock']
    }

    return render_template('book_details.html', book=book_info, reviews=reviews)


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'POST':
        # Handle update or remove actions
        cart = read_cart()
        updated = False
        form = request.form

        # Detect remove first
        remove_item_id = form.get('remove_item_id')
        if remove_item_id:
            try:
                remove_item_id = int(remove_item_id)
                cart = [item for item in cart if item['item_id'] != remove_item_id]
                updated = True
            except:
                pass

        # Detect updates of quantities
        for key, val in form.items():
            if key.startswith('update_quantity_'):
                try:
                    item_id = int(key[len('update_quantity_'):])
                    quantity = int(val)
                    if quantity < 1:
                        quantity = 1
                    for item in cart:
                        if item['item_id'] == item_id:
                            item['quantity'] = quantity
                            updated = True
                except:
                    continue

        if updated:
            try:
                content = write_cart(cart)
                with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
                    f.write(content)
            except:
                pass

        return redirect(url_for('shopping_cart'))

    # GET request
    cart = read_cart()
    books = read_books()

    cart_items = []
    total_amount = 0.0
    for item in cart:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if not book:
            continue
        price = book['price']
        subtotal = price * item['quantity']
        total_amount += subtotal
        cart_items.append({
            'item_id': item['item_id'],
            'book_id': book['book_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': price,
            'subtotal': round(subtotal, 2)
        })
    total_amount = round(total_amount, 2)

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not shipping_address or not payment_method:
            # Missing info, re-render GET page
            return render_template('checkout.html')

        cart = read_cart()
        books = read_books()
        if not cart:
            # Empty cart, no orders
            return render_template('checkout.html')

        # Compute total_amount
        total_amount = 0.0
        for item in cart:
            book = next((b for b in books if b['book_id'] == item['book_id']), None)
            if not book:
                continue
            total_amount += book['price'] * item['quantity']
        total_amount = round(total_amount, 2)

        orders = read_orders()
        order_items = read_order_items()

        max_order_id = max([o['order_id'] for o in orders], default=0)
        max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)

        order_date = datetime.today().strftime('%Y-%m-%d')

        new_order_id = max_order_id + 1
        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }
        orders.append(new_order)

        # Add order items
        new_order_items = []
        for item in cart:
            book = next((b for b in books if b['book_id'] == item['book_id']), None)
            if not book:
                continue
            max_order_item_id += 1
            oi = {
                'order_item_id': max_order_item_id,
                'order_id': new_order_id,
                'book_id': book['book_id'],
                'quantity': item['quantity'],
                'price': book['price']
            }
            new_order_items.append(oi)
        order_items.extend(new_order_items)

        # Save all
        try:
            with open(os.path.join(DATA_DIR, 'orders.txt'), 'w', encoding='utf-8') as f:
                f.write(write_orders(orders))
            with open(os.path.join(DATA_DIR, 'order_items.txt'), 'w', encoding='utf-8') as f:
                f.write(write_order_items(order_items))
            # Clear cart
            with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
                f.write('')
        except:
            pass

        return redirect(url_for('order_history'))

    # GET
    return render_template('checkout.html')


@app.route('/order_history')
def order_history():
    orders = read_orders()
    selected_status = request.args.get('selected_status', '')

    if selected_status and selected_status != 'All':
        orders = [o for o in orders if o['status'] == selected_status]

    return render_template('order_history.html', orders=orders, selected_status=selected_status)


@app.route('/order/<int:order_id>')
def order_details(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return redirect(url_for('order_history'))

    order_items_all = read_order_items()
    books = read_books()

    order_items = []
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            book = next((b for b in books if b['book_id'] == oi['book_id']), None)
            order_items.append({
                'order_item_id': oi['order_item_id'],
                'book_id': oi['book_id'],
                'title': book['title'] if book else 'Unknown',
                'quantity': oi['quantity'],
                'price': oi['price']
            })

    return render_template('order_details.html', order=order, order_items=order_items)


@app.route('/reviews')
def reviews():
    reviews_all = read_reviews()
    books = read_books()

    filter_rating = request.args.get('filter_rating', 'All')

    filtered = []

    for r in reviews_all:
        if filter_rating != 'All':
            try:
                fr = int(filter_rating[0])  # e.g. "5 stars" -> 5
                if r['rating'] != fr:
                    continue
            except:
                # malformed filter
                pass
        book = next((b for b in books if b['book_id'] == r['book_id']), None)
        filtered.append({
            'title': book['title'] if book else 'Unknown',
            'rating': r['rating'],
            'review_text': r['review_text'],
            'customer_name': r['customer_name']
        })

    return render_template('reviews.html', reviews=filtered, filter_rating=filter_rating)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    books = read_books()
    purchased_books = []

    # Getting purchased books from orders
    orders = read_orders()
    order_items = read_order_items()

    purchased_book_ids = set()
    for oi in order_items:
        purchased_book_ids.add(oi['book_id'])

    for book in books:
        if book['book_id'] in purchased_book_ids:
            purchased_books.append({'book_id': book['book_id'], 'title': book['title']})

    if request.method == 'POST':
        try:
            book_id = int(request.form.get('book_id', '0'))
            customer_name = request.form.get('customer_name', '').strip()
            rating = int(request.form.get('rating', '0'))
            review_text = request.form.get('review_text', '').strip()

            if book_id == 0 or not customer_name or rating < 1 or rating > 5 or not review_text:
                raise ValueError('Invalid form data')

            reviews = read_reviews()
            max_review_id = max([r['review_id'] for r in reviews], default=0)
            review_date = datetime.today().strftime('%Y-%m-%d')

            new_review = {
                'review_id': max_review_id + 1,
                'book_id': book_id,
                'customer_name': customer_name,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }
            reviews.append(new_review)

            try:
                content = write_reviews(reviews)
                with open(os.path.join(DATA_DIR, 'reviews.txt'), 'w', encoding='utf-8') as f:
                    f.write(content)
            except:
                pass

            return redirect(url_for('reviews'))
        except:
            pass  # Ignore errors to show form again

    return render_template('write_review.html', purchased_books=purchased_books)


@app.route('/bestsellers')
def bestsellers():
    time_period = request.args.get('time_period', 'All Time')
    bestsellers_all = read_bestsellers()
    books = read_books()

    # Filter to time_period
    if time_period != 'All Time':
        filtered = [bs for bs in bestsellers_all if bs['period'] == time_period]
    else:
        filtered = bestsellers_all

    # Sort by sales_count desc
    filtered_sorted = sorted(filtered, key=lambda x: x['sales_count'], reverse=True)

    bestsellers = []
    for bs in filtered_sorted:
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if not book:
            continue
        bestsellers.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'sales_count': bs['sales_count'],
            'period': bs['period']
        })

    return render_template('bestsellers.html', bestsellers=bestsellers, time_period=time_period)


if __name__ == '__main__':
    app.run(debug=True)
