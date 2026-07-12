from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper function to read pipe-delimited files with no header
# Returns list of list of strings

def read_data_file(filename):
    path = os.path.join(DATA_DIR, filename)
    lines = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line.split('|'))
    except FileNotFoundError:
        return []
    except Exception:
        return []
    return lines

# Helper function to write pipe-delimited data to file with no header
# data_list is list of list of strings

def write_data_file(filename, data_list):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for row in data_list:
                f.write('|'.join(str(x) for x in row)+'\n')
        return True
    except Exception:
        return False

# Read books.txt
# Returns list of dicts with keys:
# book_id(int), title(str), author(str), isbn(str), category(str), price(float), stock(int), description(str)
def read_books():
    entries = read_data_file('books.txt')
    books = []
    for row in entries:
        if len(row) != 8:
            continue
        try:
            book = {
                'book_id': int(row[0]),
                'title': row[1],
                'author': row[2],
                'isbn': row[3],
                'category': row[4],
                'price': float(row[5]),
                'stock': int(row[6]),
                'description': row[7]
            }
            books.append(book)
        except Exception:
            continue
    return books

# Read categories.txt
# Returns list of dicts with keys:
# category_id(int), category_name(str), description(str)
def read_categories():
    entries = read_data_file('categories.txt')
    categories = []
    for row in entries:
        if len(row) != 3:
            continue
        try:
            category = {
                'category_id': int(row[0]),
                'category_name': row[1],
                'description': row[2]
            }
            categories.append(category)
        except Exception:
            continue
    return categories

# Read cart.txt
# Returns list of dicts with keys:
# cart_id(int), book_id(int), quantity(int), added_date(str)
def read_cart():
    entries = read_data_file('cart.txt')
    cart = []
    for row in entries:
        if len(row) != 4:
            continue
        try:
            item = {
                'cart_id': int(row[0]),
                'book_id': int(row[1]),
                'quantity': int(row[2]),
                'added_date': row[3]
            }
            cart.append(item)
        except Exception:
            continue
    return cart

# Write cart.txt
# Accepts list of dict with keys cart_id, book_id, quantity, added_date
# Writes with exact field order

def write_cart(cart_items):
    data = []
    for item in cart_items:
        data.append([
            str(item['cart_id']),
            str(item['book_id']),
            str(item['quantity']),
            item['added_date']
        ])
    return write_data_file('cart.txt', data)

# Read orders.txt
# Returns list of dicts with keys:
# order_id(int), customer_name(str), order_date(str), total_amount(float), status(str), shipping_address(str)
def read_orders():
    entries = read_data_file('orders.txt')
    orders = []
    for row in entries:
        if len(row) != 6:
            continue
        try:
            order = {
                'order_id': int(row[0]),
                'customer_name': row[1],
                'order_date': row[2],
                'total_amount': float(row[3]),
                'status': row[4],
                'shipping_address': row[5]
            }
            orders.append(order)
        except Exception:
            continue
    return orders

# Write orders.txt
# Accepts list of dict with keys: order_id, customer_name, order_date, total_amount, status, shipping_address
# Writes with exact field order

def write_orders(orders):
    data = []
    for o in orders:
        data.append([
            str(o['order_id']),
            o['customer_name'],
            o['order_date'],
            '{:.2f}'.format(o['total_amount']),
            o['status'],
            o['shipping_address']
        ])
    return write_data_file('orders.txt', data)

# Read order_items.txt
# Returns list of dicts with keys:
# order_item_id(int), order_id(int), book_id(int), quantity(int), price(float)
def read_order_items():
    entries = read_data_file('order_items.txt')
    items = []
    for row in entries:
        if len(row) != 5:
            continue
        try:
            item = {
                'order_item_id': int(row[0]),
                'order_id': int(row[1]),
                'book_id': int(row[2]),
                'quantity': int(row[3]),
                'price': float(row[4])
            }
            items.append(item)
        except Exception:
            continue
    return items

# Write order_items.txt
# Accepts list of dict with keys: order_item_id, order_id, book_id, quantity, price
# Writes with exact field order

def write_order_items(items):
    data = []
    for i in items:
        data.append([
            str(i['order_item_id']),
            str(i['order_id']),
            str(i['book_id']),
            str(i['quantity']),
            '{:.2f}'.format(i['price'])
        ])
    return write_data_file('order_items.txt', data)

# Read reviews.txt
# Returns list of dicts with keys:
# review_id(int), book_id(int), customer_name(str), rating(int), review_text(str), review_date(str)
def read_reviews():
    entries = read_data_file('reviews.txt')
    reviews = []
    for row in entries:
        if len(row) != 6:
            continue
        try:
            review = {
                'review_id': int(row[0]),
                'book_id': int(row[1]),
                'customer_name': row[2],
                'rating': int(row[3]),
                'review_text': row[4],
                'review_date': row[5]
            }
            reviews.append(review)
        except Exception:
            continue
    return reviews

# Write reviews.txt
# Accepts list of dict with keys: review_id, book_id, customer_name, rating, review_text, review_date
# Writes with exact field order

def write_reviews(reviews):
    data = []
    for r in reviews:
        data.append([
            str(r['review_id']),
            str(r['book_id']),
            r['customer_name'],
            str(r['rating']),
            r['review_text'],
            r['review_date']
        ])
    return write_data_file('reviews.txt', data)

# Read bestsellers.txt
# Returns list of dicts with keys:
# book_id(int), sales_count(int), period(str)
def read_bestsellers():
    entries = read_data_file('bestsellers.txt')
    bestsellers = []
    for row in entries:
        if len(row) != 3:
            continue
        try:
            bs = {
                'book_id': int(row[0]),
                'sales_count': int(row[1]),
                'period': row[2]
            }
            bestsellers.append(bs)
        except Exception:
            continue
    return bestsellers


# Route 1: root_redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


# Route 2: dashboard
@app.route('/dashboard')
def dashboard():
    books = read_books()
    # For featured_books: selected the first 4 books (without filters specified)
    featured_books = []
    for b in books[:4]:
        featured_books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price']
        })

    # bestsellers: from bestsellers.txt filtered by latest period e.g. All Time; if multiple periods, choose All Time if present else the period with maximum sales_count sum
    bestsellers_data = read_bestsellers()
    # We'll pick bestsellers for 'All Time' or fallback if none
    bestsellers_filtered = [bs for bs in bestsellers_data if bs['period'] == 'All Time']
    if not bestsellers_filtered:
        # fallback get all and order by sales_count descending
        bestsellers_filtered = sorted(bestsellers_data, key=lambda x: x['sales_count'], reverse=True)
    
    # for each bestseller, add title and author from books
    bestsellers = []
    for bs in bestsellers_filtered[:5]:
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if book:
            bestsellers.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count']
            })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)


# Route 3: catalog
@app.route('/catalog')
def catalog():
    books = read_books()
    categories = read_categories()

    # Get query parameters for filtering
    search_query = request.args.get('search', '').strip()
    selected_cat_id_str = request.args.get('category')
    
    selected_category_id = None
    if selected_cat_id_str and selected_cat_id_str.isdigit():
        selected_category_id = int(selected_cat_id_str)

    # For filtering on category string by category_name matching selected_category_id
    selected_category_name = None
    if selected_category_id is not None:
        cat = next((c for c in categories if c['category_id'] == selected_category_id), None)
        if cat:
            selected_category_name = cat['category_name']

    # Filter books by category if selected
    filtered_books = books
    if selected_category_name:
        filtered_books = [b for b in books if b['category'] == selected_category_name]

    # Further filter by search_query on title or author case-insensitive
    if search_query:
        query_lower = search_query.lower()
        filtered_books = [b for b in filtered_books if query_lower in b['title'].lower() or query_lower in b['author'].lower()]

    # Prepare books for template dicts with book_id, title, author, price, category
    books_for_template = []
    for b in filtered_books:
        books_for_template.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price'],
            'category': b['category']
        })

    return render_template('catalog.html', books=books_for_template, categories=categories, 
                           search_query=search_query, selected_category_id=selected_category_id)


# Route 4: book_details
from flask import abort
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        abort(404)

    if request.method == 'POST':
        # add book to cart.txt with quantity=1 or update quantity
        cart = read_cart()
        # search for existing cart item for this book
        cart_item = next((item for item in cart if item['book_id'] == book_id), None)
        today_str = datetime.today().strftime('%Y-%m-%d')
        if cart_item:
            cart_item['quantity'] += 1
        else:
            # create new cart item
            new_cart_id = max([item['cart_id'] for item in cart], default=0) + 1
            cart.append({
                'cart_id': new_cart_id,
                'book_id': book_id,
                'quantity': 1,
                'added_date': today_str
            })
        write_cart(cart)
        return redirect(url_for('cart_page'))

    # GET processing
    reviews_all = read_reviews()
    # filter reviews for this book
    reviews_book = [r for r in reviews_all if r['book_id'] == book_id]

    # Convert review_date strings to sort by date desc
    reviews_book_sorted = sorted(reviews_book, key=lambda r: r['review_date'], reverse=True)

    # Compose review dicts with keys: review_id, customer_name, rating, review_text, review_date
    reviews_for_template = []
    for r in reviews_book_sorted:
        reviews_for_template.append({
            'review_id': r['review_id'],
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    book_for_template = {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'price': book['price'],
        'description': book['description'],
        'stock': book['stock']
    }

    return render_template('book_details.html', book=book_for_template, reviews=reviews_for_template)


# Route 5: cart_page
@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    if request.method == 'POST':
        cart = read_cart()
        # request.form may contain keys to update quantities or to remove items
        form_keys = request.form.keys()

        # Remove item buttons have names: remove-item-{cart_id}
        removed_cart_ids = []
        for key in form_keys:
            if key.startswith('remove-item-'):
                cid_str = key[len('remove-item-'):]
                if cid_str.isdigit():
                    removed_cart_ids.append(int(cid_str))

        # Remove these items
        cart = [item for item in cart if item['cart_id'] not in removed_cart_ids]

        # Update quantity inputs named update-quantity-{cart_id}
        for key in form_keys:
            if key.startswith('update-quantity-'):
                cid_str = key[len('update-quantity-'):]
                if cid_str.isdigit():
                    cart_id = int(cid_str)
                    quantity_val = request.form.get(key, '').strip()
                    if quantity_val.isdigit():
                        quantity = int(quantity_val)
                        if quantity < 1:
                            quantity = 1
                        # Update quantity if item present
                        for item in cart:
                            if item['cart_id'] == cart_id:
                                item['quantity'] = quantity
                                break

        write_cart(cart)
        return redirect(url_for('cart_page'))

    # GET method handling
    cart = read_cart()
    books = read_books()
    cart_items = []
    total_amount = 0.0

    for item in cart:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if book:
            price = book['price']
            quantity = item['quantity']
            subtotal = price * quantity
            total_amount += subtotal
            cart_items.append({
                'cart_id': item['cart_id'],
                'book_id': book['book_id'],
                'title': book['title'],
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })

    total_amount = round(total_amount, 2)

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


# Route 6: checkout
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not shipping_address or not payment_method:
            # If missing info, re-render empty form
            return render_template('checkout.html')

        # Read cart
        cart = read_cart()
        if not cart:
            # Cart empty, cannot place order, reload checkout form
            return render_template('checkout.html')

        books = read_books()

        # Calculate total amount
        total_amount = 0.0
        for item in cart:
            book = next((b for b in books if b['book_id'] == item['book_id']), None)
            if book:
                total_amount += book['price'] * item['quantity']
        total_amount = round(total_amount, 2)

        # Read existing orders and order_items to find next IDs
        orders = read_orders()
        order_items = read_order_items()

        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        new_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1

        order_date = datetime.today().strftime('%Y-%m-%d')

        # Create new order
        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }
        orders.append(new_order)

        # Create order items
        new_order_items = []
        for item in cart:
            book = next((b for b in books if b['book_id'] == item['book_id']), None)
            if book:
                new_order_items.append({
                    'order_item_id': new_order_item_id,
                    'order_id': new_order_id,
                    'book_id': book['book_id'],
                    'quantity': item['quantity'],
                    'price': book['price']
                })
                new_order_item_id += 1

        order_items.extend(new_order_items)

        # Save orders and order_items
        write_orders(orders)
        write_order_items(order_items)

        # Clear cart
        write_cart([])

        # Redirect to order_history
        return redirect(url_for('order_history'))

    # GET method: render empty checkout form
    return render_template('checkout.html')


# Route 7: order_history
@app.route('/order_history')
def order_history():
    filter_status = request.args.get('status', 'All')
    orders = read_orders()

    if filter_status != 'All':
        orders = [o for o in orders if o['status'] == filter_status]

    # No specific sorting mentioned, we can sort by order_date desc
    orders_sorted = sorted(orders, key=lambda o: o['order_date'], reverse=True)

    return render_template('order_history.html', orders=orders_sorted, filter_status=filter_status)


# Route 8: reviews_page
@app.route('/reviews')
def reviews_page():
    filter_rating = request.args.get('rating', 'All')
    reviews = read_reviews()
    books = read_books()

    # Compose reviews with book_title
    reviews_with_titles = []
    for r in reviews:
        book = next((b for b in books if b['book_id'] == r['book_id']), None)
        book_title = book['title'] if book else 'Unknown'
        reviews_with_titles.append({
            'review_id': r['review_id'],
            'book_title': book_title,
            'rating': r['rating'],
            'review_text': r['review_text'],
            'customer_name': r['customer_name'],
            'review_date': r['review_date']
        })

    if filter_rating != 'All':
        try:
            rating_filter_int = int(filter_rating)
            reviews_with_titles = [rv for rv in reviews_with_titles if rv['rating'] == rating_filter_int]
        except ValueError:
            pass

    # Sort reviews by review_date desc
    reviews_sorted = sorted(reviews_with_titles, key=lambda r: r['review_date'], reverse=True)

    return render_template('reviews.html', reviews=reviews_sorted, filter_rating=filter_rating)


# Route 9: write_review
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    if request.method == 'POST':
        book_id_str = request.form.get('book_id', '').strip()
        rating_str = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()

        if not (book_id_str.isdigit() and rating_str.isdigit() and review_text):
            # missing or invalid input
            purchased_books = []
            # Attempt to get purchased_books for GET fallback
            # Just read books
            books = read_books()
            # For simplicity, all books in orders (assuming purchased) - not instructed otherwise
            purchased_books = [{'book_id': b['book_id'], 'title': b['title']} for b in books]
            return render_template('write_review.html', purchased_books=purchased_books)

        book_id = int(book_id_str)
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            # invalid rating
            books = read_books()
            purchased_books = [{'book_id': b['book_id'], 'title': b['title']} for b in books]
            return render_template('write_review.html', purchased_books=purchased_books)

        # Read reviews
        reviews = read_reviews()
        new_review_id = max([r['review_id'] for r in reviews], default=0) + 1

        # Hardcode customer_name as empty (no user auth) per spec, but spec requires customer_name field in reviews
        # We do not know customer name from form; we will put 'Anonymous' as placeholder
        customer_name = 'Anonymous'
        review_date = datetime.today().strftime('%Y-%m-%d')

        new_review = {
            'review_id': new_review_id,
            'book_id': book_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }
        reviews.append(new_review)
        write_reviews(reviews)
        return redirect(url_for('reviews_page'))

    # GET handling
    # Spec says purchased_books are books user can review
    # We don't have user system, so we consider all books from orders
    orders = read_orders()
    order_items = read_order_items()
    books = read_books()

    purchased_book_ids = set()
    for oi in order_items:
        purchased_book_ids.add(oi['book_id'])

    # books filtered by purchased_book_ids
    purchased_books = []
    for b in books:
        if b['book_id'] in purchased_book_ids:
            purchased_books.append({'book_id': b['book_id'], 'title': b['title']})

    return render_template('write_review.html', purchased_books=purchased_books)


# Route 10: bestsellers_page
@app.route('/bestsellers')
def bestsellers_page():
    time_period = request.args.get('period', 'All Time')
    bestsellers_data = read_bestsellers()
    books = read_books()

    filtered_bestsellers = [bs for bs in bestsellers_data if bs['period'] == time_period]
    if not filtered_bestsellers:
        # fallback show all periods sorted by sales_count descending
        filtered_bestsellers = sorted(bestsellers_data, key=lambda x: x['sales_count'], reverse=True)

    bestsellers = []
    for bs in filtered_bestsellers:
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if book:
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
