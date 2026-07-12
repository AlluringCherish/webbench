from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for file operations and data parsing

def read_file_lines(filename):
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def write_file_lines(filename, lines):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

# === Books ===
def load_books():
    books = []
    lines = read_file_lines('books.txt')
    for line in lines:
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
        except Exception:
            continue
    return books

def books_dict():
    books = load_books()
    return {b['book_id']: b for b in books}

# === Categories ===
def load_categories():
    categories = []
    lines = read_file_lines('categories.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 3:
            continue
        try:
            category = {
                'category_id': int(parts[0]),
                'category_name': parts[1],
                'description': parts[2]
            }
            categories.append(category)
        except Exception:
            continue
    return categories

# === Cart ===
def load_cart():
    cart = []
    lines = read_file_lines('cart.txt')
    for line in lines:
        parts = line.split('|')
        if len(parts) != 4:
            continue
        try:
            item = {
                'cart_id': int(parts[0]),
                'book_id': int(parts[1]),
                'quantity': int(parts[2]),
                'added_date': parts[3]
            }
            cart.append(item)
        except Exception:
            continue
    return cart

def save_cart(cart):
    lines = []
    for item in cart:
        line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}"
        lines.append(line)
    write_file_lines('cart.txt', lines)

# === Orders ===
def load_orders():
    orders = []
    lines = read_file_lines('orders.txt')
    for line in lines:
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
        except Exception:
            continue
    return orders

# === Order Items ===
def load_order_items():
    order_items = []
    lines = read_file_lines('order_items.txt')
    for line in lines:
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
            order_items.append(item)
        except Exception:
            continue
    return order_items

# === Reviews ===
def load_reviews():
    reviews = []
    lines = read_file_lines('reviews.txt')
    for line in lines:
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
        except Exception:
            continue
    return reviews

# === Bestsellers ===
def load_bestsellers():
    bestsellers = []
    lines = read_file_lines('bestsellers.txt')
    for line in lines:
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
        except Exception:
            continue
    return bestsellers

# === Helpers ===
def get_new_cart_id(cart):
    if not cart:
        return 1
    return max(item['cart_id'] for item in cart) + 1

def get_new_order_id(orders):
    if not orders:
        return 1
    return max(order['order_id'] for order in orders) + 1

def get_new_order_item_id(order_items):
    if not order_items:
        return 1
    return max(item['order_item_id'] for item in order_items) + 1

def get_new_review_id(reviews):
    if not reviews:
        return 1
    return max(review['review_id'] for review in reviews) + 1

# === Routes ===
@app.route('/')
def dashboard():
    books = load_books()
    featured_books = [{
        'book_id': b['book_id'],
        'title': b['title'],
        'author': b['author'],
        'price': b['price']
    } for b in books[:5]]
    return render_template('dashboard.html', featured_books=featured_books)


@app.route('/catalog', methods=['GET', 'POST'])
def book_catalog():
    books = load_books()
    categories = load_categories()
    selected_category = None
    search_query = ''

    if request.method == 'POST':
        # Synchronize form names with template
        selected_category = request.form.get('selected_category')
        search_query = request.form.get('search_query', '').strip()

    filtered_books = []
    for book in books:
        include = True
        if selected_category and selected_category != '':
            if book['category'] != selected_category:
                include = False
        if search_query and search_query.lower() not in book['title'].lower() and search_query.lower() not in book['author'].lower():
            include = False
        if include:
            filtered_books.append(book)

    books_for_template = [{
        'book_id': b['book_id'],
        'title': b['title'],
        'author': b['author'],
        'price': b['price']
    } for b in filtered_books]

    categories_for_template = [{
        'category_id': str(c['category_id']),
        'category_name': c['category_name']
    } for c in categories]

    return render_template('catalog.html', books=books_for_template, categories=categories_for_template, selected_category=selected_category if selected_category else None, search_query=search_query)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = books_dict()
    book = books.get(book_id)
    if not book:
        return "Book not found", 404

    reviews_all = load_reviews()
    reviews_for_book = [r for r in reviews_all if r['book_id'] == book_id]

    if request.method == 'POST':
        if 'add-to-cart-button' in request.form:
            cart = load_cart()
            existing = next((item for item in cart if item['book_id'] == book_id), None)
            if existing:
                existing['quantity'] += 1
            else:
                new_cart_id = get_new_cart_id(cart)
                today = datetime.now().strftime('%Y-%m-%d')
                cart.append({'cart_id': new_cart_id, 'book_id': book_id, 'quantity': 1, 'added_date': today})
            save_cart(cart)
            return redirect(url_for('shopping_cart'))

    book_template = {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'isbn': book['isbn'],
        'category': book['category'],
        'price': book['price'],
        'stock': book['stock'],
        'description': book['description']
    }

    return render_template('details.html', book=book_template, reviews=reviews_for_book)


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart = load_cart()
    books = books_dict()

    if request.method == 'POST':
        remove_item_id = request.form.get('remove-item')
        if remove_item_id:
            try:
                remove_item_id_int = int(remove_item_id)
                cart = [item for item in cart if item['cart_id'] != remove_item_id_int]
                save_cart(cart)
                return redirect(url_for('shopping_cart'))
            except Exception:
                pass

        updated = False
        for item in cart[:]:
            input_name = f'quantity-{item["cart_id"]}'
            if input_name in request.form:
                try:
                    new_qty = int(request.form[input_name])
                    if new_qty >= 0:
                        if new_qty == 0:
                            cart.remove(item)
                        else:
                            item['quantity'] = new_qty
                        updated = True
                except ValueError:
                    pass
        if updated:
            save_cart(cart)
            return redirect(url_for('shopping_cart'))

    cart_items = []
    total_amount = 0.0
    for item in cart:
        b = books.get(item['book_id'])
        if b:
            price = b['price']
            quantity = item['quantity']
            subtotal = price * quantity
            total_amount += subtotal
            cart_items.append({
                'item_id': item['cart_id'],
                'book_id': b['book_id'],
                'title': b['title'],
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        if 'place-order-button' in request.form:
            customer_name = request.form.get('customer_name', '').strip()
            shipping_address = request.form.get('shipping_address', '').strip()
            payment_method = request.form.get('payment_method', '').strip()

            if not customer_name or not shipping_address or not payment_method:
                return render_template('checkout.html')

            cart = load_cart()
            books = books_dict()
            if not cart:
                return render_template('checkout.html')

            total_amount = 0.0
            for item in cart:
                b = books.get(item['book_id'])
                if not b:
                    continue
                total_amount += b['price'] * item['quantity']

            orders = load_orders()
            order_items = load_order_items()

            new_order_id = get_new_order_id(orders)
            today = datetime.now().strftime('%Y-%m-%d')

            orders.append({
                'order_id': new_order_id,
                'customer_name': customer_name,
                'order_date': today,
                'total_amount': total_amount,
                'status': 'Pending',
                'shipping_address': shipping_address
            })

            next_order_item_id = get_new_order_item_id(order_items)
            for item in cart:
                b = books.get(item['book_id'])
                if not b:
                    continue
                order_items.append({
                    'order_item_id': next_order_item_id,
                    'order_id': new_order_id,
                    'book_id': b['book_id'],
                    'quantity': item['quantity'],
                    'price': b['price']
                })
                next_order_item_id += 1

            order_lines = []
            for o in orders:
                line = f"{o['order_id']}|{o['customer_name']}|{o['order_date']}|{o['total_amount']:.2f}|{o['status']}|{o['shipping_address']}"
                order_lines.append(line)
            write_file_lines('orders.txt', order_lines)

            order_items_lines = []
            for oi in order_items:
                line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['book_id']}|{oi['quantity']}|{oi['price']:.2f}"
                order_items_lines.append(line)
            write_file_lines('order_items.txt', order_items_lines)

            write_file_lines('cart.txt', [])

            return redirect(url_for('order_history'))

    return render_template('checkout.html')


@app.route('/orders', methods=['GET', 'POST'])
def order_history():
    orders = load_orders()
    status_filter = 'All'

    if request.method == 'POST':
        status_filter_input = request.form.get('status_filter')
        if status_filter_input:
            status_filter = status_filter_input

        view_order_button = next((key for key in request.form.keys() if key.startswith('view-order-button-')), None)
        if view_order_button:
            # View order route doesn't exist - disable action
            pass

    if status_filter and status_filter != 'All':
        orders_filtered = [o for o in orders if o['status'] == status_filter]
    else:
        orders_filtered = orders

    return render_template('history.html', orders=orders_filtered, status_filter=status_filter)


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    all_reviews = load_reviews()
    rating_filter = None

    if request.method == 'POST':
        if 'write-review-button' in request.form:
            return redirect(url_for('write_review'))

        rating_selected = request.form.get('filter-by-rating')
        if rating_selected:
            try:
                rating_val = int(rating_selected)
                if 1 <= rating_val <= 5:
                    rating_filter = rating_val
            except:
                pass

    if rating_filter:
        filtered_reviews = [r for r in all_reviews if r['rating'] == rating_filter]
    else:
        filtered_reviews = all_reviews

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter=str(rating_filter) if rating_filter is not None else '')


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    orders = load_orders()
    order_items = load_order_items()
    books = books_dict()

    purchased_book_ids = set()
    for oi in order_items:
        purchased_book_ids.add(oi['book_id'])

    purchased_books = []
    for book_id in purchased_book_ids:
        book = books.get(book_id)
        if book:
            purchased_books.append({'book_id': book['book_id'], 'title': book['title']})

    if request.method == 'POST':
        if 'submit-review-button' in request.form:
            selected_book_id = request.form.get('select-book')
            rating_select = request.form.get('rating-select')
            review_text = request.form.get('review-text', '').strip()

            try:
                book_id_int = int(selected_book_id)
                rating_int = int(rating_select)
                if book_id_int not in purchased_book_ids or not (1 <= rating_int <= 5) or not review_text:
                    raise ValueError('Invalid input')
            except:
                return render_template('write_review.html', purchased_books=purchased_books)

            reviews_all = load_reviews()
            new_review_id = get_new_review_id(reviews_all)
            today = datetime.now().strftime('%Y-%m-%d')
            reviews_all.append({'review_id': new_review_id, 'book_id': book_id_int, 'customer_name': 'Anonymous', 'rating': rating_int, 'review_text': review_text, 'review_date': today})

            review_lines = []
            for r in reviews_all:
                review_lines.append(f"{r['review_id']}|{r['book_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}")
            write_file_lines('reviews.txt', review_lines)

            return redirect(url_for('reviews'))

    return render_template('write_review.html', purchased_books=purchased_books)


@app.route('/bestsellers', methods=['GET', 'POST'])
def bestsellers():
    bestsellers_all = load_bestsellers()
    books = books_dict()
    time_period = 'All Time'

    if request.method == 'POST':
        time_period_filter = request.form.get('time-period-filter')
        if time_period_filter:
            time_period = time_period_filter

        view_book_button = next((key for key in request.form.keys() if key.startswith('view-book-button-')), None)
        if view_book_button:
            try:
                book_id = int(view_book_button.split('-')[-1])
                return redirect(url_for('book_details', book_id=book_id))
            except:
                pass

    filtered_bestsellers = [b for b in bestsellers_all if b['period'] == time_period]
    filtered_bestsellers.sort(key=lambda b: b['sales_count'], reverse=True)

    bestsellers_for_template = []
    for b in filtered_bestsellers:
        book = books.get(b['book_id'])
        if book:
            bestsellers_for_template.append({'book_id': book['book_id'], 'title': book['title'], 'author': book['author'], 'price': book['price'], 'sales_count': b['sales_count']})

    return render_template('bestsellers.html', bestsellers=bestsellers_for_template, time_period=time_period)


if __name__ == '__main__':
    app.run(debug=True)
