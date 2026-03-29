from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for file handling and data parsing

def read_pipe_delimited_file(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    rows = [line.split('|') for line in lines]
    return rows

# Section 3 Schemas Readers

def read_books():
    # Fields: book_id|title|author|isbn|category|price|stock|description
    filepath = os.path.join(DATA_DIR, 'books.txt')
    rows = read_pipe_delimited_file(filepath)
    books = []
    for r in rows:
        if len(r) < 8:
            continue
        try:
            book = {
                'book_id': int(r[0]),
                'title': r[1],
                'author': r[2],
                'isbn': r[3],
                'category': r[4],
                'price': float(r[5]),
                'stock': int(r[6]),
                'description': r[7]
            }
            books.append(book)
        except Exception:
            continue
    return books


def read_categories():
    # Fields: category_id|category_name|description
    filepath = os.path.join(DATA_DIR, 'categories.txt')
    rows = read_pipe_delimited_file(filepath)
    categories = []
    for r in rows:
        if len(r) < 3:
            continue
        try:
            cat = {
                'category_id': int(r[0]),
                'category_name': r[1],
                'description': r[2]
            }
            categories.append(cat)
        except Exception:
            continue
    return categories


def read_cart():
    # Fields: cart_id|book_id|quantity|added_date
    filepath = os.path.join(DATA_DIR, 'cart.txt')
    rows = read_pipe_delimited_file(filepath)
    cart_items = []
    for r in rows:
        if len(r) < 4:
            continue
        try:
            item = {
                'cart_id': int(r[0]),
                'book_id': int(r[1]),
                'quantity': int(r[2]),
                'added_date': r[3]
            }
            cart_items.append(item)
        except Exception:
            continue
    return cart_items


def write_cart(cart_items):
    # cart_items is list of dicts with cart_id,book_id,quantity,added_date
    filepath = os.path.join(DATA_DIR, 'cart.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in cart_items:
            line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
            f.write(line)


def read_orders():
    # order_id|customer_name|order_date|total_amount|status|shipping_address
    filepath = os.path.join(DATA_DIR, 'orders.txt')
    rows = read_pipe_delimited_file(filepath)
    orders = []
    for r in rows:
        if len(r) < 6:
            continue
        try:
            order = {
                'order_id': int(r[0]),
                'customer_name': r[1],
                'order_date': r[2],
                'total_amount': float(r[3]),
                'status': r[4],
                'shipping_address': r[5]
            }
            orders.append(order)
        except Exception:
            continue
    return orders


def write_orders(orders):
    filepath = os.path.join(DATA_DIR, 'orders.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for order in orders:
            line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']:.2f}|{order['status']}|{order['shipping_address']}\n"
            f.write(line)


def read_order_items():
    # order_item_id|order_id|book_id|quantity|price
    filepath = os.path.join(DATA_DIR, 'order_items.txt')
    rows = read_pipe_delimited_file(filepath)
    order_items = []
    for r in rows:
        if len(r) < 5:
            continue
        try:
            oi = {
                'order_item_id': int(r[0]),
                'order_id': int(r[1]),
                'book_id': int(r[2]),
                'quantity': int(r[3]),
                'price': float(r[4])
            }
            order_items.append(oi)
        except Exception:
            continue
    return order_items


def write_order_items(order_items):
    filepath = os.path.join(DATA_DIR, 'order_items.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for oi in order_items:
            line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['book_id']}|{oi['quantity']}|{oi['price']:.2f}\n"
            f.write(line)


def read_reviews():
    # review_id|book_id|customer_name|rating|review_text|review_date
    filepath = os.path.join(DATA_DIR, 'reviews.txt')
    rows = read_pipe_delimited_file(filepath)
    reviews = []
    for r in rows:
        if len(r) < 6:
            continue
        try:
            review = {
                'review_id': int(r[0]),
                'book_id': int(r[1]),
                'customer_name': r[2],
                'rating': int(r[3]),
                'review_text': r[4],
                'review_date': r[5]
            }
            reviews.append(review)
        except Exception:
            continue
    return reviews


def write_reviews(reviews):
    filepath = os.path.join(DATA_DIR, 'reviews.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = f"{r['review_id']}|{r['book_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
            f.write(line)


def read_bestsellers():
    # book_id|sales_count|period
    filepath = os.path.join(DATA_DIR, 'bestsellers.txt')
    rows = read_pipe_delimited_file(filepath)
    bestsellers = []
    for r in rows:
        if len(r) < 3:
            continue
        try:
            best = {
                'book_id': int(r[0]),
                'sales_count': int(r[1]),
                'period': r[2]
            }
            bestsellers.append(best)
        except Exception:
            continue
    return bestsellers


# Helper to get book by id

def get_book_by_id(book_id):
    books = read_books()
    for b in books:
        if b['book_id'] == book_id:
            return b
    return None

# Helper to get category by id

def get_category_by_id(category_id):
    categories = read_categories()
    for c in categories:
        if c['category_id'] == category_id:
            return c
    return None


# Implement Flask routes as per specification

@app.route('/', methods=['GET'])
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard', methods=['GET'])
def dashboard_page():
    # Featured books: simplest interpretation: first 4 books
    books = read_books()
    featured_books = []
    for b in books[:4]:
        featured_books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price']
        })

    # Read bestsellers for all periods together, aggregate sales_count by book
    bestsellers = read_bestsellers()
    sales_map = {}
    for b in bestsellers:
        sales_map[b['book_id']] = sales_map.get(b['book_id'], 0) + b['sales_count']

    bestselling_books = []
    for b in books:
        if b['book_id'] in sales_map:
            bestselling_books.append({
                'book_id': b['book_id'],
                'title': b['title'],
                'author': b['author'],
                'sales_count': sales_map[b['book_id']]
            })

    # Sort by sales_count descending
    bestselling_books.sort(key=lambda x: x['sales_count'], reverse=True)
    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestselling_books)


@app.route('/catalog', methods=['GET'])
def catalog_page():
    categories = read_categories()
    cat_map = {c['category_name']: c['category_id'] for c in categories}
    books_all = read_books()
    books = []
    for b in books_all:
        books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price'],
            'category': b['category'],
            'isbn': b['isbn']
        })
    return render_template('catalog.html', categories=categories, books=books)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details_page(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return "Book not found", 404

    if request.method == 'POST':
        # Add book to cart with quantity
        try:
            quantity = int(request.form.get('quantity', '1'))
            if quantity < 1:
                raise ValueError
        except Exception:
            return "Invalid quantity", 400

        cart_items = read_cart()
        max_cart_id = max([c['cart_id'] for c in cart_items], default=0)

        # Check if book already in cart: if yes, update quantity
        found = False
        for item in cart_items:
            if item['book_id'] == book_id:
                item['quantity'] += quantity
                found = True
                break

        if not found:
            today = datetime.today().strftime('%Y-%m-%d')
            new_cart_item = {
                'cart_id': max_cart_id + 1,
                'book_id': book_id,
                'quantity': quantity,
                'added_date': today
            }
            cart_items.append(new_cart_item)

        write_cart(cart_items)
        return redirect(url_for('cart_page'))

    # GET method
    reviews_all = read_reviews()
    reviews_for_book = []
    for r in reviews_all:
        if r['book_id'] == book_id:
            reviews_for_book.append({
                'review_id': r['review_id'],
                'customer_name': r['customer_name'],
                'rating': r['rating'],
                'review_text': r['review_text'],
                'review_date': r['review_date']
            })

    book_context = {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'price': book['price'],
        'description': book['description'],
        'isbn': book['isbn'],
        'category': book['category'],
        'stock': book['stock']
    }

    return render_template('book_details.html', book=book_context, reviews=reviews_for_book)


@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    # Read current cart and enrich with book details
    cart_items_raw = read_cart()
    books = read_books()
    books_map = {b['book_id']: b for b in books}

    if request.method == 'POST':
        # Process updates or removals
        cart_items = cart_items_raw.copy()
        changed = False

        for item in cart_items_raw:
            cart_id = item['cart_id']
            qty_field = f'update_quantity-{cart_id}'
            remove_field = f'remove_item-{cart_id}'

            if remove_field in request.form:
                # Remove item
                cart_items = [ci for ci in cart_items if ci['cart_id'] != cart_id]
                changed = True
                break  # handle one remove per submission

            elif qty_field in request.form:
                try:
                    new_qty = int(request.form[qty_field])
                    if new_qty < 1:
                        continue  # ignore invalid quantity
                    if new_qty != item['quantity']:
                        # update
                        for ci in cart_items:
                            if ci['cart_id'] == cart_id:
                                ci['quantity'] = new_qty
                                changed = True
                                break
                except Exception:
                    continue

        if changed:
            write_cart(cart_items)
        return redirect(url_for('cart_page'))

    # GET method, prepare data for template
    cart_items = []
    total_amount = 0.0
    for item in cart_items_raw:
        book = books_map.get(item['book_id'])
        if not book:
            continue
        price = book['price']
        subtotal = price * item['quantity']
        total_amount += subtotal
        cart_items.append({
            'cart_id': item['cart_id'],
            'book_id': item['book_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': price,
            'subtotal': subtotal
        })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    cart_items_raw = read_cart()
    books = read_books()
    books_map = {b['book_id']: b for b in books}

    cart_items_for_template = []
    total_amount = 0.0
    for item in cart_items_raw:
        book = books_map.get(item['book_id'])
        if not book:
            continue
        price = book['price']
        subtotal = price * item['quantity']
        total_amount += subtotal
        cart_items_for_template.append({
            'cart_id': item['cart_id'],
            'book_id': item['book_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': price,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not shipping_address or payment_method not in ["Credit Card", "PayPal", "Bank Transfer"]:
            return "Missing or invalid checkout information", 400

        orders = read_orders()
        max_order_id = max([o['order_id'] for o in orders], default=0)
        new_order_id = max_order_id + 1
        order_date = datetime.today().strftime('%Y-%m-%d')

        # Create new order entry
        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': "Pending",
            'shipping_address': shipping_address
        }
        orders.append(new_order)
        write_orders(orders)

        # Append order items
        order_items = read_order_items()
        max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)

        for item in cart_items_raw:
            book = books_map.get(item['book_id'])
            if not book:
                continue
            max_order_item_id += 1
            oi = {
                'order_item_id': max_order_item_id,
                'order_id': new_order_id,
                'book_id': item['book_id'],
                'quantity': item['quantity'],
                'price': book['price']
            }
            order_items.append(oi)

        write_order_items(order_items)

        # Clear cart
        write_cart([])

        return redirect(url_for('order_history_page'))

    # GET request
    return render_template('checkout.html', cart_items=cart_items_for_template, total_amount=total_amount)


@app.route('/order_history', methods=['GET'])
def order_history_page():
    orders = read_orders()
    # Optional status filter
    status_filter = request.args.get('status','')
    if status_filter:
        filtered = [o for o in orders if o['status'].lower() == status_filter.lower()]
    else:
        filtered = orders
    return render_template('order_history.html', orders=filtered)


@app.route('/order/<int:order_id>', methods=['GET'])
def order_details_page(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    order_items_all = read_order_items()
    order_items = []
    books_map = {b['book_id']: b for b in read_books()}
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            book = books_map.get(oi['book_id'])
            title = book['title'] if book else "Unknown"
            order_items.append({
                'order_item_id': oi['order_item_id'],
                'book_id': oi['book_id'],
                'title': title,
                'quantity': oi['quantity'],
                'price': oi['price']
            })

    return render_template('order_details.html', order=order, order_items=order_items)


@app.route('/reviews', methods=['GET'])
def reviews_page():
    reviews = read_reviews()
    # Optional rating filter
    rating_filter = request.args.get('rating')
    if rating_filter:
        try:
            rating_val = int(rating_filter)
            if rating_val in range(1,6):
                reviews = [r for r in reviews if r['rating'] == rating_val]
        except Exception:
            pass

    books_map = {b['book_id']: b for b in read_books()}
    reviews_out = []
    for r in reviews:
        book = books_map.get(r['book_id'])
        if not book:
            continue
        reviews_out.append({
            'review_id': r['review_id'],
            'book_id': r['book_id'],
            'title': book['title'],
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })
    return render_template('reviews.html', reviews=reviews_out)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review_page():
    if request.method == 'GET':
        books = [ { 'book_id': b['book_id'], 'title': b['title'] } for b in read_books() ]
        return render_template('write_review.html', books=books)

    # POST method
    try:
        book_id = int(request.form['book_id'])
        rating = int(request.form['rating'])
        review_text = request.form['review_text'].strip()
        customer_name = request.form['customer_name'].strip()
        if rating < 1 or rating > 5 or not review_text or not customer_name:
            raise ValueError
    except Exception:
        return "Invalid form data", 400

    reviews = read_reviews()
    new_id = 1 + max([r['review_id'] for r in reviews], default=0)
    review_date = datetime.today().strftime('%Y-%m-%d')
    new_review = {
        'review_id': new_id,
        'book_id': book_id,
        'customer_name': customer_name,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date
    }
    reviews.append(new_review)
    write_reviews(reviews)
    return redirect(url_for('reviews_page'))


@app.route('/bestsellers', methods=['GET'])
def bestsellers_page():
    period_filter = request.args.get('period','').strip()
    bestsellers = read_bestsellers()
    if period_filter:
        bestsellers = [b for b in bestsellers if b['period'].lower() == period_filter.lower()]

    # Now get books info for each bestseller
    books_map = {b['book_id']: b for b in read_books()}
    filtered_bestsellers = []
    for bs in bestsellers:
        book = books_map.get(bs['book_id'])
        if not book:
            continue
        filtered_bestsellers.append({
            'book_id': bs['book_id'],
            'title': book['title'],
            'author': book['author'],
            'sales_count': bs['sales_count'],
            'period': bs['period']
        })

    # Sort descending by sales_count
    filtered_bestsellers.sort(key=lambda x: x['sales_count'], reverse=True)

    return render_template('bestsellers.html', bestsellers=filtered_bestsellers)


if __name__ == '__main__':
    app.run(debug=True)
