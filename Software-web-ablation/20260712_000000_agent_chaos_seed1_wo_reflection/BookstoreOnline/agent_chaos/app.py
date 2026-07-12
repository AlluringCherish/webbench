from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and save data files

def load_books():
    path = os.path.join(DATA_DIR, 'books.txt')
    books = []
    if not os.path.exists(path):
        return books
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # book_id|title|author|isbn|category|price|stock|description
            if len(parts) != 8:
                continue
            book = {
                'book_id': int(parts[0]),
                'title': parts[1],
                'author': parts[2],
                'isbn': parts[3],
                'category': parts[4],
                'price': float(parts[5]),
                'stock': int(parts[6]),
                'description': parts[7],
            }
            books.append(book)
    return books

def load_categories():
    path = os.path.join(DATA_DIR, 'categories.txt')
    categories = []
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # category_id|category_name|description
            if len(parts) != 3:
                continue
            category = {
                'category_id': int(parts[0]),
                'category_name': parts[1],
                'description': parts[2],
            }
            categories.append(category)
    return categories

def load_cart():
    path = os.path.join(DATA_DIR, 'cart.txt')
    cart = []
    if not os.path.exists(path):
        return cart
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # cart_id|book_id|quantity|added_date
            if len(parts) != 4:
                continue
            item = {
                'cart_id': int(parts[0]),
                'book_id': int(parts[1]),
                'quantity': int(parts[2]),
                'added_date': parts[3],
            }
            cart.append(item)
    return cart

def save_cart(cart):
    path = os.path.join(DATA_DIR, 'cart.txt')
    lines = []
    for item in cart:
        line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def load_orders():
    path = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # order_id|customer_name|order_date|total_amount|status|shipping_address
            if len(parts) != 6:
                continue
            order = {
                'order_id': int(parts[0]),
                'customer_name': parts[1],
                'order_date': parts[2],
                'total_amount': float(parts[3]),
                'status': parts[4],
                'shipping_address': parts[5],
            }
            orders.append(order)
    return orders

def save_orders(orders):
    path = os.path.join(DATA_DIR, 'orders.txt')
    lines = []
    for order in orders:
        line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['shipping_address']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def load_order_items():
    path = os.path.join(DATA_DIR, 'order_items.txt')
    items = []
    if not os.path.exists(path):
        return items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # order_item_id|order_id|book_id|quantity|price
            if len(parts) != 5:
                continue
            item = {
                'order_item_id': int(parts[0]),
                'order_id': int(parts[1]),
                'book_id': int(parts[2]),
                'quantity': int(parts[3]),
                'price': float(parts[4]),
            }
            items.append(item)
    return items

def save_order_items(items):
    path = os.path.join(DATA_DIR, 'order_items.txt')
    lines = []
    for item in items:
        line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def load_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # review_id|book_id|customer_name|rating|review_text|review_date
            if len(parts) != 6:
                continue
            review = {
                'review_id': int(parts[0]),
                'book_id': int(parts[1]),
                'customer_name': parts[2],
                'rating': int(parts[3]),
                'review_text': parts[4],
                'review_date': parts[5],
            }
            reviews.append(review)
    return reviews

def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    lines = []
    for review in reviews:
        line = f"{review['review_id']}|{review['book_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}"
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def load_bestsellers():
    path = os.path.join(DATA_DIR, 'bestsellers.txt')
    bestsellers = []
    if not os.path.exists(path):
        return bestsellers
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            # book_id|sales_count|period
            if len(parts) != 3:
                continue
            bs = {
                'book_id': int(parts[0]),
                'sales_count': int(parts[1]),
                'period': parts[2],
            }
            bestsellers.append(bs)
    return bestsellers

# Routes

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    books = load_books()
    bestsellers_data = load_bestsellers()

    # Featured books: select 5 random or first 5 for demo
    featured_books = []
    for b in books[:5]:
        featured_books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price']
        })

    # bestsellers with rank
    # We can filter all time or recent but spec does not say here, so show bestsellers all time selected by period 'All Time' or any
    # We'll rank by sales_count desc. We will add rank field
    # Enhance bestsellers_data with book title and author.
    bestsellers = []
    # For demo, filter period as any (all)
    sorted_bs = sorted(bestsellers_data, key=lambda x: x['sales_count'], reverse=True)
    for idx, bs in enumerate(sorted_bs[:5]):
        book = next((b for b in books if b['book_id'] == bs['book_id']), None)
        if book:
            bestsellers.append({
                'rank': idx + 1,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count'],
                'period': bs['period']
            })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)

@app.route('/catalog')
def catalog():
    books = load_books()
    categories = load_categories()

    search_query = request.args.get('search', '').strip()
    selected_category = request.args.get('category', '').strip()

    # Filter books by search (title, author, isbn)
    filtered_books = books
    if search_query:
        sq = search_query.lower()
        filtered_books = [b for b in filtered_books if (sq in b['title'].lower() or sq in b['author'].lower() or sq in b['isbn'].lower())]

    # Filter books by category
    if selected_category:
        filtered_books = [b for b in filtered_books if b['category'] == selected_category]

    # Prepare book list for template
    book_list = []
    for b in filtered_books:
        book_list.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price'],
        })

    return render_template('catalog.html', books=book_list, categories=categories, selected_category=selected_category, search_query=search_query)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = load_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404

    if request.method == 'POST':
        # Add the book to cart with quantity=1
        cart = load_cart()
        exists = next((item for item in cart if item['book_id'] == book_id), None)
        if exists:
            exists['quantity'] += 1
        else:
            new_id = max([item['cart_id'] for item in cart], default=0) + 1
            cart.append({
                'cart_id': new_id,
                'book_id': book_id,
                'quantity': 1,
                'added_date': datetime.now().strftime('%Y-%m-%d')
            })
        save_cart(cart)
        return redirect(url_for('cart'))

    # GET method
    reviews = load_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]

    # Prepare reviews for template
    reviews_list = []
    for r in book_reviews:
        reviews_list.append({
            'review_id': r['review_id'],
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date'],
        })

    book_detail = {
        'book_id': book['book_id'],
        'title': book['title'],
        'author': book['author'],
        'price': book['price'],
        'description': book['description'],
    }

    return render_template('book_details.html', book=book_detail, reviews=reviews_list)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    books = load_books()
    cart_items = load_cart()

    if request.method == 'POST':
        # Handle quantity updates and removals
        updated_cart = cart_items.copy()

        # Remove items
        remove_ids = []
        for item in cart_items:
            remove_key = f'remove-item-button-{item["cart_id"]}'
            if remove_key in request.form:
                remove_ids.append(item['cart_id'])

        updated_cart = [item for item in updated_cart if item['cart_id'] not in remove_ids]

        # Update quantities
        for item in updated_cart:
            qty_key = f'update-quantity-{item["cart_id"]}'
            if qty_key in request.form:
                try:
                    qty = int(request.form[qty_key])
                    if qty > 0:
                        item['quantity'] = qty
                    else:
                        # Remove item if quantity 0 or less
                        remove_ids.append(item['cart_id'])
                except ValueError:
                    pass

        # Remove any with quantity 0 or less
        updated_cart = [item for item in updated_cart if item['cart_id'] not in remove_ids]

        save_cart(updated_cart)
        return redirect(url_for('cart'))

    # GET method
    cart_items = load_cart()
    cart_display = []
    books_dict = {b['book_id']: b for b in books}
    total_amount = 0.0
    for item in cart_items:
        book = books_dict.get(item['book_id'])
        if book:
            subtotal = book['price'] * item['quantity']
            total_amount += subtotal
            cart_display.append({
                'item_id': item['cart_id'],
                'book_id': book['book_id'],
                'title': book['title'],
                'quantity': item['quantity'],
                'price': book['price'],
                'subtotal': subtotal,
            })

    return render_template('cart.html', cart_items=cart_display, total_amount=total_amount)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not shipping_address or not payment_method:
            # Could add flash messages or error handling but not requested
            return render_template('checkout.html')

        cart = load_cart()
        if not cart:
            return render_template('checkout.html')  # no items to checkout

        books = load_books()
        books_dict = {b['book_id']: b for b in books}

        # Calculate total
        total_amount = 0.0
        for item in cart:
            book = books_dict.get(item['book_id'])
            if book:
                total_amount += book['price'] * item['quantity']

        # Create new order
        orders = load_orders()
        new_order_id = max([order['order_id'] for order in orders], default=0) + 1

        order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': datetime.now().strftime('%Y-%m-%d'),
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }
        orders.append(order)
        save_orders(orders)

        # Create order items
        order_items = load_order_items()
        max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)
        for item in cart:
            book = books_dict.get(item['book_id'])
            if book:
                max_order_item_id += 1
                order_item = {
                    'order_item_id': max_order_item_id,
                    'order_id': new_order_id,
                    'book_id': book['book_id'],
                    'quantity': item['quantity'],
                    'price': book['price'],
                }
                order_items.append(order_item)
        save_order_items(order_items)

        # Clear cart after order created
        save_cart([])

        return redirect(url_for('orders'))

    return render_template('checkout.html')

@app.route('/orders')
def orders():
    orders_data = load_orders()
    selected_status = request.args.get('status', 'All')

    if selected_status != 'All':
        filtered_orders = [o for o in orders_data if o['status'].lower() == selected_status.lower()]
    else:
        filtered_orders = orders_data

    return render_template('orders.html', orders=filtered_orders, selected_status=selected_status)

@app.route('/order/<int:order_id>')
def order_details(order_id):
    orders_data = load_orders()
    order = next((o for o in orders_data if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    order_items_data = load_order_items()
    books = load_books()
    books_dict = {b['book_id']: b for b in books}
    order_items = [
        {
            'book_id': item['book_id'],
            'title': books_dict.get(item['book_id'], {}).get('title', ''),
            'quantity': item['quantity'],
            'price': item['price']
        }
        for item in order_items_data if item['order_id'] == order_id
    ]

    return render_template('order_details.html', order=order, order_items=order_items)

@app.route('/reviews')
def reviews():
    reviews_data = load_reviews()
    books = load_books()
    books_dict = {b['book_id']: b for b in books}

    selected_rating = request.args.get('rating', 'All')

    filtered_reviews = reviews_data
    if selected_rating != 'All':
        try:
            rating_filter = int(selected_rating[0])  # '5 stars' -> 5
            filtered_reviews = [r for r in filtered_reviews if r['rating'] == rating_filter]
        except Exception:
            pass

    review_list = []
    for r in filtered_reviews:
        book_title = books_dict.get(r['book_id'], {}).get('title', '')
        review_list.append({
            'review_id': r['review_id'],
            'book_title': book_title,
            'rating': r['rating'],
            'review_text': r['review_text'],
            'customer_name': r['customer_name'],
            'review_date': r['review_date'],
        })

    return render_template('reviews.html', reviews=review_list, selected_rating=selected_rating)

@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    books = load_books()
    book_list = [{'book_id': b['book_id'], 'title': b['title']} for b in books]

    if request.method == 'POST':
        try:
            book_id = int(request.form.get('book_id'))
            rating = int(request.form.get('rating'))
            review_text = request.form.get('review_text', '').strip()
            customer_name = request.form.get('customer_name', '').strip()

            if not customer_name:
                customer_name = 'Anonymous'

            if book_id <= 0 or rating <= 0 or rating > 5 or not review_text:
                return render_template('write_review.html', books=book_list)

            reviews = load_reviews()
            new_review_id = max([r['review_id'] for r in reviews], default=0) + 1
            new_review = {
                'review_id': new_review_id,
                'book_id': book_id,
                'customer_name': customer_name,
                'rating': rating,
                'review_text': review_text,
                'review_date': datetime.now().strftime('%Y-%m-%d'),
            }
            reviews.append(new_review)
            save_reviews(reviews)
            return redirect(url_for('reviews'))
        except Exception:
            return render_template('write_review.html', books=book_list)

    return render_template('write_review.html', books=book_list)

@app.route('/bestsellers')
def bestsellers():
    period = request.args.get('period', 'All Time')
    bestsellers_data = load_bestsellers()
    books = load_books()
    books_dict = {b['book_id']: b for b in books}

    filtered_bs = [bs for bs in bestsellers_data if bs['period'] == period or period == 'All Time']

    sorted_bs = sorted(filtered_bs, key=lambda x: x['sales_count'], reverse=True)

    bestsellers_list = []
    for idx, bs in enumerate(sorted_bs):
        book = books_dict.get(bs['book_id'])
        if book:
            bestsellers_list.append({
                'rank': idx + 1,
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': bs['sales_count'],
                'period': bs['period'],
            })

    return render_template('bestsellers.html', bestsellers=bestsellers_list, selected_period=period)

if __name__ == '__main__':
    app.run(debug=True)
