from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_path = 'data'

# Helper functions for reading and writing data files

def read_books():
    books = []
    try:
        with open(os.path.join(data_path, 'books.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
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
        # Could log error here
        pass
    return books

def read_categories():
    categories = []
    try:
        with open(os.path.join(data_path, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    category = {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2]
                    }
                    categories.append(category)
    except Exception:
        pass
    return categories

def read_cart():
    cart = []
    try:
        with open(os.path.join(data_path, 'cart.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    item = {
                        'cart_id': int(parts[0]),
                        'book_id': int(parts[1]),
                        'quantity': int(parts[2]),
                        'added_date': parts[3]
                    }
                    cart.append(item)
    except Exception:
        pass
    return cart

def write_cart(cart_items):
    try:
        with open(os.path.join(data_path, 'cart.txt'), 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
    except Exception:
        pass

def read_orders():
    orders = []
    try:
        with open(os.path.join(data_path, 'orders.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
        pass
    return orders

def write_orders(orders):
    try:
        with open(os.path.join(data_path, 'orders.txt'), 'w', encoding='utf-8') as f:
            for order in orders:
                line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['shipping_address']}\n"
                f.write(line)
    except Exception:
        pass

def read_order_items():
    order_items = []
    try:
        with open(os.path.join(data_path, 'order_items.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    item = {
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'book_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    }
                    order_items.append(item)
    except Exception:
        pass
    return order_items

def write_order_items(order_items):
    try:
        with open(os.path.join(data_path, 'order_items.txt'), 'w', encoding='utf-8') as f:
            for item in order_items:
                line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']}\n"
                f.write(line)
    except Exception:
        pass

def read_reviews():
    reviews = []
    try:
        with open(os.path.join(data_path, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
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
        pass
    return reviews

def write_reviews(reviews):
    try:
        with open(os.path.join(data_path, 'reviews.txt'), 'w', encoding='utf-8') as f:
            for review in reviews:
                line = f"{review['review_id']}|{review['book_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}\n"
                f.write(line)
    except Exception:
        pass

def read_bestsellers():
    bestsellers = []
    try:
        with open(os.path.join(data_path, 'bestsellers.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    b = {
                        'book_id': int(parts[0]),
                        'sales_count': int(parts[1]),
                        'period': parts[2]
                    }
                    bestsellers.append(b)
    except Exception:
        pass
    return bestsellers

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))

@app.route('/dashboard')
def dashboard_page():
    books = read_books()
    bestsellers = read_bestsellers()

    # Determine featured books: we'll pick the first 4 books (or less if less books)
    featured_books = []
    for book in books[:4]:
        featured_books.append({
            'book_id': book['book_id'],
            'title': book['title'],
            'author': book['author'],
            'price': book['price']
        })

    # For bestsellers on dashboard, pick top 5 by sales_count descending from bestsellers data ignoring period
    bestsellers_sorted = sorted(bestsellers, key=lambda x: x['sales_count'], reverse=True)[:5]

    bookshelf = {b['book_id']: b for b in books}

    bestsellers_list = []
    for b in bestsellers_sorted:
        book = bookshelf.get(b['book_id'])
        if book:
            bestsellers_list.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count']
            })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers_list)

@app.route('/catalog')
def book_catalog_page():
    books = read_books()
    categories = read_categories()

    # Get search and category filters from query params
    search_query = request.args.get('search-query', '').strip()
    selected_category = request.args.get('category-filter', '').strip()

    filtered_books = []

    for book in books:
        # Filter by category if category selected
        if selected_category and book['category'] != selected_category:
            continue
        # Filter by search query if present (search title, author or isbn case insensitive)
        if search_query:
            sq_lower = search_query.lower()
            if sq_lower not in book['title'].lower() and sq_lower not in book['author'].lower() and sq_lower not in book['isbn'].lower():
                continue
        filtered_books.append(book)

    return render_template('catalog.html', books=filtered_books, categories=categories, search_query=search_query, selected_category=selected_category)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details_page(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if book is None:
        return "Book not found", 404

    reviews_all = read_reviews()
    reviews = [r for r in reviews_all if r['book_id'] == book_id]

    if request.method == 'POST':
        # Process add to cart
        try:
            quantity = int(request.form.get('quantity', '1'))
            if quantity < 1:
                quantity = 1
            stock = book['stock']
            if quantity > stock:
                quantity = stock
            # read current cart
            cart = read_cart()
            # find if book already in cart
            cart_item = next((item for item in cart if item['book_id'] == book_id), None)
            today_str = datetime.now().strftime('%Y-%m-%d')
            if cart_item:
                # increment quantity
                new_qty = cart_item['quantity'] + quantity
                # cannot exceed stock
                if new_qty > stock:
                    new_qty = stock
                cart_item['quantity'] = new_qty
                cart_item['added_date'] = today_str
            else:
                new_cart_id = max((item['cart_id'] for item in cart), default=0) + 1
                cart.append({
                    'cart_id': new_cart_id,
                    'book_id': book_id,
                    'quantity': quantity,
                    'added_date': today_str
                })
            write_cart(cart)
        except Exception:
            # Ignore errors gracefully
            pass
        return redirect(url_for('book_details_page', book_id=book_id))

    return render_template('book_details.html', book=book, reviews=reviews)

@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart_page():
    books = {b['book_id']: b for b in read_books()}
    cart = read_cart()

    if request.method == 'POST':
        form = request.form
        # Check for remove or update actions
        if 'remove_cart_id' in form:
            try:
                remove_id = int(form['remove_cart_id'])
                cart = [item for item in cart if item['cart_id'] != remove_id]
                write_cart(cart)
            except Exception:
                pass
        elif 'update_cart_id' in form and 'quantity' in form:
            try:
                update_id = int(form['update_cart_id'])
                quantity = int(form['quantity'])
                if quantity < 1:
                    quantity = 1
                for item in cart:
                    if item['cart_id'] == update_id:
                        # Check stock limit
                        book = books.get(item['book_id'])
                        if book:
                            max_stock = book['stock']
                            if quantity > max_stock:
                                quantity = max_stock
                        item['quantity'] = quantity
                        break
                write_cart(cart)
            except Exception:
                pass
        return redirect(url_for('shopping_cart_page'))

    cart_items = []
    total_amount = 0.0
    for item in cart:
        book = books.get(item['book_id'])
        if book:
            price = book['price']
            subtotal = price * item['quantity']
            cart_items.append({
                'cart_id': item['cart_id'],
                'book_id': book['book_id'],
                'title': book['title'],
                'quantity': item['quantity'],
                'price': price,
                'subtotal': subtotal
            })
            total_amount += subtotal

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    books = {b['book_id']: b for b in read_books()}
    cart = read_cart()

    cart_items = []
    total_amount = 0.0
    for item in cart:
        book = books.get(item['book_id'])
        if book:
            price = book['price']
            subtotal = price * item['quantity']
            cart_items.append({
                'cart_id': item['cart_id'],
                'book_id': book['book_id'],
                'title': book['title'],
                'quantity': item['quantity'],
                'price': price,
                'subtotal': subtotal
            })
            total_amount += subtotal

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()
        if not customer_name or not shipping_address or not payment_method:
            # Could add flash or error here, but just redirect back for simplicity
            return redirect(url_for('checkout_page'))

        # Read orders and order_items
        orders = read_orders()
        order_items = read_order_items()

        new_order_id = max((order['order_id'] for order in orders), default=0) + 1
        order_date = datetime.now().strftime('%Y-%m-%d')

        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }

        orders.append(new_order)

        # Add order items with unique order_item_id
        next_order_item_id = max((oi['order_item_id'] for oi in order_items), default=0) + 1
        for item in cart:
            book = books.get(item['book_id'])
            if book:
                order_item = {
                    'order_item_id': next_order_item_id,
                    'order_id': new_order_id,
                    'book_id': item['book_id'],
                    'quantity': item['quantity'],
                    'price': book['price']
                }
                order_items.append(order_item)
                next_order_item_id += 1

        # Write back orders and order_items
        write_orders(orders)
        write_order_items(order_items)

        # Clear cart
        try:
            os.remove(os.path.join(data_path, 'cart.txt'))
        except Exception:
            # Possibly file doesn't exist, ignore
            pass

        return redirect(url_for('order_history_page'))

    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/order_history')
def order_history_page():
    selected_status = request.args.get('status', 'All').strip()
    orders = read_orders()

    if selected_status and selected_status != 'All':
        filtered_orders = [o for o in orders if o['status'] == selected_status]
    else:
        filtered_orders = orders

    return render_template('orders.html', orders=filtered_orders, selected_status=selected_status)

@app.route('/order/<int:order_id>')
def order_details_page(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if order is None:
        return "Order not found", 404

    order_items_all = read_order_items()
    books = {b['book_id']: b for b in read_books()}

    order_items_filtered = [oi for oi in order_items_all if oi['order_id'] == order_id]

    order_items = []
    for oi in order_items_filtered:
        book = books.get(oi['book_id'])
        title = book['title'] if book else 'Unknown'
        order_items.append({
            'order_item_id': oi['order_item_id'],
            'book_id': oi['book_id'],
            'title': title,
            'quantity': oi['quantity'],
            'price': oi['price']
        })

    return render_template('order_details.html', order=order, order_items=order_items)

@app.route('/reviews')
def reviews_page():
    filter_rating_str = request.args.get('filter-rating', '').strip()
    filter_rating = None
    try:
        val = int(filter_rating_str)
        if val >= 1 and val <= 5:
            filter_rating = val
    except Exception:
        filter_rating = None

    reviews_all = read_reviews()
    books = {b['book_id']: b for b in read_books()}

    filtered_reviews = []
    for r in reviews_all:
        if filter_rating is not None and r['rating'] != filter_rating:
            continue
        book = books.get(r['book_id'])
        title = book['title'] if book else 'Unknown'
        filtered_reviews.append({
            'review_id': r['review_id'],
            'book_id': r['book_id'],
            'title': title,
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    return render_template('reviews.html', reviews=filtered_reviews, filter_rating=filter_rating)

@app.route('/write_review', methods=['GET', 'POST'])
def write_review_page():
    # For simplicity, purchased_books means all distinct books from order_items
    order_items = read_order_items()
    book_ids_purchased = set(item['book_id'] for item in order_items)
    books = {b['book_id']: b for b in read_books()}

    purchased_books = []
    for bid in sorted(book_ids_purchased):
        book = books.get(bid)
        if book:
            purchased_books.append({
                'book_id': book['book_id'],
                'title': book['title']
            })

    if request.method == 'POST':
        try:
            book_id = int(request.form.get('book_id', '0'))
            rating = int(request.form.get('rating', '0'))
            review_text = request.form.get('review_text', '').strip()
            customer_name = request.form.get('customer_name', '').strip()

            if book_id == 0 or rating < 1 or rating > 5 or not review_text:
                # Invalid input, redirect back
                return redirect(url_for('write_review_page'))

            reviews = read_reviews()
            new_review_id = max((r['review_id'] for r in reviews), default=0) + 1
            review_date = datetime.now().strftime('%Y-%m-%d')

            new_review = {
                'review_id': new_review_id,
                'book_id': book_id,
                'customer_name': customer_name if customer_name else 'Anonymous',
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }

            reviews.append(new_review)
            write_reviews(reviews)

            return redirect(url_for('reviews_page'))
        except Exception:
            # On error, redirect back
            return redirect(url_for('write_review_page'))

    return render_template('write_review.html', purchased_books=purchased_books)

@app.route('/bestsellers')
def bestsellers_page():
    time_period = request.args.get('time-period-filter', 'This Month').strip()
    bestsellers = read_bestsellers()
    books = {b['book_id']: b for b in read_books()}

    filtered_bestsellers = [b for b in bestsellers if b['period'] == time_period]

    bestsellers_list = []
    for b in filtered_bestsellers:
        book = books.get(b['book_id'])
        if book:
            bestsellers_list.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': b['sales_count'],
                'period': b['period']
            })

    return render_template('bestsellers.html', bestsellers=bestsellers_list, time_period=time_period)

if __name__ == '__main__':
    app.run(debug=True)
