from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

data_dir = 'data'

# Utilities for reading and writing pipe-delimited files

def read_data_file(filename):
    filepath = os.path.join(data_dir, filename)
    data = []
    if not os.path.exists(filepath):
        return data
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(line.split('|'))
    return data

def write_data_file(filename, data):
    filepath = os.path.join(data_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for entry in data:
            line = '|'.join(str(e) for e in entry)
            f.write(line + '\n')

# Read all books

def get_books():
    books_raw = read_data_file('books.txt')
    books = []
    for b in books_raw:
        books.append({
            'book_id': int(b[0]),
            'title': b[1],
            'author': b[2],
            'isbn': b[3],
            'category': b[4],
            'price': float(b[5]),
            'stock': int(b[6]),
            'description': b[7]
        })
    return books

# Get book by id

def get_book_by_id(book_id):
    books = get_books()
    for b in books:
        if b['book_id'] == book_id:
            return b
    return None

# Read all categories

def get_categories():
    categories_raw = read_data_file('categories.txt')
    categories = []
    for c in categories_raw:
        categories.append({
            'category_id': int(c[0]),
            'category_name': c[1],
            'description': c[2]
        })
    return categories

# Read cart items

def get_cart_items():
    cart_raw = read_data_file('cart.txt')
    cart_items = []
    for c in cart_raw:
        cart_items.append({
            'cart_id': int(c[0]),
            'book_id': int(c[1]),
            'quantity': int(c[2]),
            'added_date': c[3]
        })
    return cart_items

# Get cart items with book details

def get_cart_items_with_details():
    cart_items = get_cart_items()
    books = get_books()
    books_dict = {b['book_id']: b for b in books}
    items = []
    total_amount = 0.0

    for item in cart_items:
        book = books_dict.get(item['book_id'])
        if book:
            subtotal = book['price'] * item['quantity']
            items.append({
                'cart_id': item['cart_id'],
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'price': book['price'],
                'quantity': item['quantity'],
                'subtotal': subtotal
            })
            total_amount += subtotal
    return items, total_amount

# Write cart items

def write_cart_items(cart_items):
    # cart_items is list of dicts with keys: cart_id, book_id, quantity, added_date
    data = []
    for item in cart_items:
        data.append([item['cart_id'], item['book_id'], item['quantity'], item['added_date']])
    write_data_file('cart.txt', data)

# Get next ID for a file

def get_next_id(filename):
    data = read_data_file(filename)
    max_id = 0
    for d in data:
        try:
            id_val = int(d[0])
            if id_val > max_id:
                max_id = id_val
        except:
            continue
    return max_id + 1

# Read orders

def get_orders():
    orders_raw = read_data_file('orders.txt')
    orders = []
    for o in orders_raw:
        orders.append({
            'order_id': int(o[0]),
            'customer_name': o[1],
            'order_date': o[2],
            'total_amount': float(o[3]),
            'status': o[4],
            'shipping_address': o[5]
        })
    return orders

# Read order items

def get_order_items():
    items_raw = read_data_file('order_items.txt')
    items = []
    for i in items_raw:
        items.append({
            'order_item_id': int(i[0]),
            'order_id': int(i[1]),
            'book_id': int(i[2]),
            'quantity': int(i[3]),
            'price': float(i[4])
        })
    return items

# Read reviews

def get_reviews():
    reviews_raw = read_data_file('reviews.txt')
    reviews = []
    for r in reviews_raw:
        reviews.append({
            'review_id': int(r[0]),
            'book_id': int(r[1]),
            'customer_name': r[2],
            'rating': int(r[3]),
            'review_text': r[4],
            'review_date': r[5]
        })
    return reviews

# Write reviews

def write_reviews(reviews):
    data = []
    for r in reviews:
        data.append([r['review_id'], r['book_id'], r['customer_name'], r['rating'], r['review_text'], r['review_date']])
    write_data_file('reviews.txt', data)

# Read bestsellers

def get_bestsellers(period=None):
    bestsellers_raw = read_data_file('bestsellers.txt')
    bestsellers = []
    for b in bestsellers_raw:
        if period is None or b[2] == period:
            bestsellers.append({
                'book_id': int(b[0]),
                'sales_count': int(b[1]),
                'period': b[2]
            })
    return bestsellers


# ROUTES IMPLEMENTATION

@app.route('/')
@app.route('/dashboard')
def dashboard():
    # Featured books: Could be top 3 from books as example
    books = get_books()
    featured_books = books[:3] if len(books) >= 3 else books
    bestsellers = get_bestsellers(period='This Month')
    # Join bestseller with book titles
    books_dict = {b['book_id']: b for b in books}
    bestsellers_list = []
    for b in bestsellers:
        book = books_dict.get(b['book_id'])
        if book:
            bestsellers_list.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers_list)


@app.route('/catalog')
def book_catalog():
    books = get_books()
    categories = get_categories()
    selected_category = request.args.get('category')
    search_query = request.args.get('search')

    filtered_books = books
    if selected_category and selected_category != 'All':
        filtered_books = [b for b in filtered_books if b['category'] == selected_category]
    if search_query:
        sq = search_query.lower()
        filtered_books = [b for b in filtered_books if sq in b['title'].lower() or sq in b['author'].lower() or sq in b['isbn']]

    return render_template('catalog.html', books=filtered_books, categories=categories, selected_category=selected_category, search_query=search_query)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return "Book not found", 404

    if request.method == 'POST':
        # Add to cart logic
        quantity = 1  # Default to 1 for add to cart
        cart_items = get_cart_items()
        # Check if book already in cart
        existing = None
        for item in cart_items:
            if item['book_id'] == book_id:
                existing = item
                break
        if existing:
            existing['quantity'] += quantity
        else:
            new_cart_id = get_next_id('cart.txt')
            today_str = datetime.now().strftime('%Y-%m-%d')
            cart_items.append({
                'cart_id': new_cart_id,
                'book_id': book_id,
                'quantity': quantity,
                'added_date': today_str
            })
        write_cart_items(cart_items)
        # Redirect to cart page after adding
        return redirect(url_for('shopping_cart'))

    # GET - Load reviews for this book
    reviews_all = get_reviews()
    book_reviews = [r for r in reviews_all if r['book_id'] == book_id]

    return render_template('book_details.html', book=book, reviews=book_reviews)


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_items = get_cart_items()
    books = get_books()
    books_dict = {b['book_id']: b for b in books}

    if request.method == 'POST':
        # Possible post actions: update quantities or remove item
        form = request.form
        cart_items = get_cart_items()  # reload for safety

        # Remove item
        for key in form:
            if key.startswith('remove-item-button-'):
                cart_id_str = key.replace('remove-item-button-', '')
                try:
                    cart_id = int(cart_id_str)
                    cart_items = [item for item in cart_items if item['cart_id'] != cart_id]
                    write_cart_items(cart_items)
                    return redirect(url_for('shopping_cart'))
                except:
                    pass

        # Update quantities
        updated = False
        for key in form:
            if key.startswith('update-quantity-'):
                cart_id_str = key.replace('update-quantity-', '')
                try:
                    cart_id = int(cart_id_str)
                    new_quantity = int(form[key])
                    if new_quantity < 1:
                        new_quantity = 1
                    for item in cart_items:
                        if item['cart_id'] == cart_id:
                            item['quantity'] = new_quantity
                            updated = True
                    
                except:
                    pass
        if updated:
            write_cart_items(cart_items)
            return redirect(url_for('shopping_cart'))

    # GET
    cart_details = []
    total_amount = 0.0
    for item in cart_items:
        book = books_dict.get(item['book_id'])
        if book:
            subtotal = book['price'] * item['quantity']
            cart_details.append({
                'cart_id': item['cart_id'],
                'book_id': book['book_id'],
                'title': book['title'],
                'price': book['price'],
                'quantity': item['quantity'],
                'subtotal': subtotal
            })
            total_amount += subtotal

    return render_template('cart.html', cart_items=cart_details, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer-name')
        shipping_address = request.form.get('shipping-address')
        payment_method = request.form.get('payment-method')

        if not customer_name or not shipping_address or not payment_method:
            # Missing info, re-render form with error?
            return render_template('checkout.html', error='Please fill all required fields.')

        # Get cart items
        cart_items = get_cart_items()
        if not cart_items:
            return render_template('checkout.html', error='Cart is empty.')

        books = get_books()
        books_dict = {b['book_id']: b for b in books}

        total_amount = 0.0
        for item in cart_items:
            book = books_dict.get(item['book_id'])
            if book:
                total_amount += book['price'] * item['quantity']

        # Create new order
        orders = get_orders()
        new_order_id = get_next_id('orders.txt')
        order_date = datetime.now().strftime('%Y-%m-%d')
        status = 'Pending'

        orders.append([
            new_order_id,
            customer_name,
            order_date,
            '{:.2f}'.format(total_amount),
            status,
            shipping_address
        ])
        write_data_file('orders.txt', orders)

        # Write order items
        order_items = get_order_items()
        next_order_item_id = get_next_id('order_items.txt')
        for item in cart_items:
            book = books_dict.get(item['book_id'])
            if book:
                order_items.append([
                    next_order_item_id,
                    new_order_id,
                    book['book_id'],
                    item['quantity'],
                    '{:.2f}'.format(book['price'])
                ])
                next_order_item_id += 1
        write_data_file('order_items.txt', order_items)

        # Clear the cart
        write_cart_items([])

        return redirect(url_for('order_history'))

    # GET
    return render_template('checkout.html')


@app.route('/orders')
def order_history():
    orders = get_orders()
    filter_status = request.args.get('status', 'All')

    if filter_status and filter_status != 'All':
        orders = [o for o in orders if o['status'] == filter_status]

    return render_template('orders.html', orders=orders, filter_status=filter_status)


@app.route('/reviews')
def reviews():
    reviews = get_reviews()
    books = get_books()
    books_dict = {b['book_id']: b for b in books}

    filter_rating = request.args.get('rating', 'All')

    # Join book title
    joined_reviews = []
    for r in reviews:
        if filter_rating != 'All' and int(filter_rating) != r['rating']:
            continue
        book = books_dict.get(r['book_id'])
        if book:
            joined_reviews.append({
                'review_id': r['review_id'],
                'book_id': r['book_id'],
                'book_title': book['title'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'customer_name': r['customer_name'],
                'review_date': r['review_date']
            })

    return render_template('reviews.html', reviews=joined_reviews, filter_rating=filter_rating)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    # For this draft, purchased_books can be all books from orders (no auth)
    order_items = get_order_items()
    orders = get_orders()
    purchased_book_ids = set()
    for oi in order_items:
        purchased_book_ids.add(oi['book_id'])
    books = get_books()
    purchased_books = [b for b in books if b['book_id'] in purchased_book_ids]

    if request.method == 'POST':
        book_id = int(request.form.get('select-book'))
        rating = int(request.form.get('rating-select'))
        review_text = request.form.get('review-text')
        customer_name = 'Anonymous'  # No auth, placeholder
        review_date = datetime.now().strftime('%Y-%m-%d')

        reviews = get_reviews()
        new_review_id = get_next_id('reviews.txt')

        reviews.append({
            'review_id': new_review_id,
            'book_id': book_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        })

        write_reviews(reviews)

        return redirect(url_for('reviews'))

    return render_template('write_review.html', purchased_books=purchased_books)


@app.route('/bestsellers')
def bestsellers():
    time_period = request.args.get('period', 'This Month')
    bestsellers = get_bestsellers(period=time_period)
    books = get_books()
    books_dict = {b['book_id']: b for b in books}

    bestsellers_list = []
    for b in bestsellers:
        book = books_dict.get(b['book_id'])
        if book:
            bestsellers_list.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })

    return render_template('bestsellers.html', bestsellers=bestsellers_list, time_period=time_period)


if __name__ == '__main__':
    app.run(debug=True)
