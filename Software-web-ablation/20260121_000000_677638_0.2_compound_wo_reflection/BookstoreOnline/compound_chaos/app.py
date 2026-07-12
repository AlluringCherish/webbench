from flask import Flask, render_template, redirect, url_for, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions for data handling

def read_books():
    books = []
    path = os.path.join(DATA_DIR, 'books.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # Fields: book_id|title|author|isbn|category|price|stock|description
                parts = line.split('|')
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
                    'description': parts[7]
                }
                books.append(book)
    except Exception:
        pass
    return books


def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # Fields: category_id|name|description
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                category = {
                    'category_id': int(parts[0]),
                    'name': parts[1],
                    'description': parts[2]
                }
                categories.append(category)
    except Exception:
        pass
    return categories


def read_bestsellers():
    bestsellers = []
    path = os.path.join(DATA_DIR, 'bestsellers.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # Fields: rank|book_id|title|sales_count|time_period
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                bestseller = {
                    'rank': int(parts[0]),
                    'book_id': int(parts[1]),
                    'title': parts[2],
                    'sales_count': int(parts[3]),
                    'time_period': parts[4]
                }
                bestsellers.append(bestseller)
    except Exception:
        pass
    return bestsellers

# 1. Root Route
@app.route('/', methods=['GET'])
def pi7c4p1otpzj5o1():
    # redirect to /dashboard
    return redirect(url_for('dashboard'))

# 2. Dashboard route
@app.route('/dashboard', methods=['GET'])
def dashboard():
    # featured_books: dict with keys book_id (int), title (str), author (str), price (float)
    # bestsellers: list of dict with keys: title (str), sales_count (int)
    books = read_books()
    # Simplify featured_books as first 5 books for example
    featured_books = []
    for b in books[:5]:
        featured_books.append({
            'book_id': b['book_id'],
            'title': b['title'],
            'author': b['author'],
            'price': b['price']
        })

    bestsellers_data = read_bestsellers()
    # only title and sales_count keys for bestsellers context
    bestsellers = [{'title': b['title'], 'sales_count': b['sales_count']} for b in bestsellers_data[:5]]

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)

# 3. Catalog route
@app.route('/catalog', methods=['GET'])
def e3mk1vqfe():
    books = read_books()
    categories = read_categories()

    # Get selected category from query params
    selected_category_id = request.args.get('category')
    selected_category = None
    filtered_books = books
    if selected_category_id:
        try:
            selected_category_id_int = int(selected_category_id)
            filtered_books = [b for b in books if b['category'] == next((c['name'] for c in categories if c['category_id'] == selected_category_id_int), None)]
            selected_category = selected_category_id_int
        except ValueError:
            selected_category = None
    # Prepare books list for context with keys: book_id (int), title (str), price (float), author (str)
    context_books = [{
        'book_id': b['book_id'],
        'title': b['title'],
        'price': b['price'],
        'author': b['author']
    } for b in filtered_books]
    # categories (list of dicts)
    # selected_category (int or None)
    return render_template('catalog.html', books=context_books, categories=categories, selected_category=selected_category)

# 4. Book details route
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        # Render 404 or redirect to catalog
        return redirect(url_for('e3mk1vqfe'))

    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            # Fields of reviews.txt: review_id|book_id|customer_name|rating|review_text|review_date
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                r_id = int(parts[0])
                r_book_id = int(parts[1])
                if r_book_id == book_id:
                    review = {
                        'review_id': r_id,
                        'customer_name': parts[2],
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    }
                    reviews.append(review)
    except Exception:
        pass

    if request.method == 'POST':
        # Add one copy of this book to the cart
        # Cart file fields: cart_item_id|book_id|quantity|date_added (we infer/increment cart_item_id locally)
        try:
            cart_path = os.path.join(DATA_DIR, 'cart.txt')
            cart_items = []
            max_cart_id = 0
            if os.path.exists(cart_path):
                with open(cart_path, 'r', encoding='utf-8') as cartf:
                    for line in cartf:
                        line=line.strip()
                        if not line:
                            continue
                        parts = line.split('|')
                        if len(parts) != 4:
                            continue
                        c_id = int(parts[0])
                        c_book_id = int(parts[1])
                        c_quantity = int(parts[2])
                        c_date_added = parts[3]
                        cart_items.append({'cart_id': c_id, 'book_id': c_book_id, 'quantity': c_quantity, 'date_added': c_date_added})
                        if c_id > max_cart_id:
                            max_cart_id = c_id
            # Check if book already in cart
            found = False
            for item in cart_items:
                if item['book_id'] == book_id:
                    item['quantity'] += 1
                    found = True
                    break
            if not found:
                cart_items.append({'cart_id': max_cart_id+1, 'book_id': book_id, 'quantity': 1, 'date_added': '2025-01-01'})  # date_added fixed placeholder
            # Write back
            with open(cart_path, 'w', encoding='utf-8') as cartf:
                for item in cart_items:
                    line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['date_added']}\n"
                    cartf.write(line)
        except Exception:
            pass
        return redirect(url_for('0wou48'))

    return render_template('book_details.html', book=book, reviews=reviews)

# 5. Cart route
@app.route('/cart', methods=['GET', 'POST'])
def 0wou48():
    from datetime import datetime
    books = read_books()
    book_map = {b['book_id']: b for b in books}

    cart_path = os.path.join(DATA_DIR, 'cart.txt')
    cart_items = []
    if os.path.exists(cart_path):
        try:
            with open(cart_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line=line.strip()
                    if not line:
                        continue
                    parts = line.split('|')
                    if len(parts) != 4:
                        continue
                    cart_id = int(parts[0])
                    book_id = int(parts[1])
                    quantity = int(parts[2])
                    date_added = parts[3]
                    cart_items.append({'cart_id': cart_id, 'book_id': book_id, 'quantity': quantity, 'date_added': date_added})
        except Exception:
            pass

    if request.method == 'POST':
        form = request.form
        # Check if any update quantity
        for item in cart_items:
            q_key = f"update-quantity-{item['cart_id']}"
            if q_key in form:
                try:
                    new_q = int(form[q_key])
                    if new_q > 0:
                        item['quantity'] = new_q
                    else:
                        # quantity 0 or less means remove
                        cart_items = [i for i in cart_items if i['cart_id'] != item['cart_id']]
                except Exception:
                    pass
                break
        # Check if remove item
        for item in cart_items:
            remove_key = f"remove-item-button-{item['cart_id']}"
            if remove_key in form:
                cart_items = [i for i in cart_items if i['cart_id'] != item['cart_id']]
                break
        # Check proceed to checkout
        if 'proceed-checkout-button' in form:
            return redirect(url_for('tkwgm6g'))

        # rewrite cart file
        try:
            with open(cart_path, 'w', encoding='utf-8') as f:
                for item in cart_items:
                    f.write(f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['date_added']}\n")
        except Exception:
            pass

    # Calculate total_amount
    total_amount = 0.0
    cart_display = []
    for item in cart_items:
        book = book_map.get(item['book_id'])
        if not book:
            continue
        amount = book['price'] * item['quantity']
        total_amount += amount
        cart_display.append({
            'cart_id': item['cart_id'],
            'book_id': item['book_id'],
            'title': book['title'],
            'quantity': item['quantity'],
            'price': book['price'],
            'total_price': amount
        })

    return render_template('cart.html', cart_items=cart_display, total_amount=total_amount)

# 6. Checkout route
@app.route('/checkout', methods=['GET', 'POST'])
def tkwgm6g():
    # No specific context variables needed (rxha empty/dflt)
    cart_path = os.path.join(DATA_DIR, 'cart.txt')
    cart_items = []
    if os.path.exists(cart_path):
        try:
            with open(cart_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line=line.strip()
                    if not line:
                        continue
                    parts = line.split('|')
                    if len(parts) != 4:
                        continue
                    cart_id = int(parts[0])
                    book_id = int(parts[1])
                    quantity = int(parts[2])
                    date_added = parts[3]
                    cart_items.append({'cart_id': cart_id, 'book_id': book_id, 'quantity': quantity, 'date_added': date_added})
        except Exception:
            pass

    if request.method == 'POST':
        form = request.form
        customer_name = form.get('customer-name', '').strip()
        payment_method = form.get('payment-method', '').strip()  # Possible values: PayPal, Transfer
        shipping_address = form.get('shipping-address', '').strip() if 'shipping-address' in form else ''
        if customer_name and payment_method:
            # Create order
            import datetime

            orders_path = os.path.join(DATA_DIR, 'orders.txt')
            order_items_path = os.path.join(DATA_DIR, 'order_items.txt')

            # Load existing orders to get max order_id
            orders = []
            max_order_id = 0
            if os.path.exists(orders_path):
                try:
                    with open(orders_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line=line.strip()
                            if not line:
                                continue
                            parts = line.split('|')
                            if len(parts) != 5:
                                continue
                            curr_order_id = int(parts[0])
                            if curr_order_id > max_order_id:
                                max_order_id = curr_order_id
                            orders.append(parts)  # save raw parts
                except Exception:
                    pass

            # Calculate total_amount
            books = read_books()
            book_map = {b['book_id']: b for b in books}
            total_amount = 0.0
            for c_item in cart_items:
                b = book_map.get(c_item['book_id'])
                if b:
                    total_amount += b['price'] * c_item['quantity']

            # Add order entry
            new_order_id = max_order_id + 1
            order_date = datetime.datetime.now().strftime('%Y-%m-%d')

            try:
                with open(orders_path, 'a', encoding='utf-8') as f_order:
                    f_order.write(f"{new_order_id}|{customer_name}|{order_date}|{total_amount}|Pending|{shipping_address}\n")
            except Exception:
                pass

            # Append order items
            max_order_item_id = 0
            order_items = []
            if os.path.exists(order_items_path):
                try:
                    with open(order_items_path, 'r', encoding='utf-8') as f_items:
                        for line in f_items:
                            line=line.strip()
                            if not line:
                                continue
                            parts = line.split('|')
                            if len(parts) != 5:
                                continue
                            curr_item_id = int(parts[0])
                            if curr_item_id > max_order_item_id:
                                max_order_item_id = curr_item_id
                            order_items.append(parts)  # raw
                except Exception:
                    pass

            try:
                with open(order_items_path, 'a', encoding='utf-8') as f_items_a:
                    next_order_item_id = max_order_item_id + 1
                    for c_item in cart_items:
                        b = book_map.get(c_item['book_id'])
                        if b:
                            f_items_a.write(f"{next_order_item_id}|{new_order_id}|{c_item['book_id']}|{c_item['quantity']}|{b['price']}\n")
                            next_order_item_id += 1
            except Exception:
                pass

            # Clear cart
            try:
                open(cart_path, 'w').close()
            except Exception:
                pass

            return redirect(url_for('7dzgv3drh0oal33'))

    return render_template('checkout.html', rxha={})

# 7. Orders page
@app.route('/orders', methods=['GET', 'POST'])
def 7dzgv3drh0oal33():
    orders_path = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    filter_status = None
    if request.method == 'POST':
        filter_status = request.form.get('order-status-filter')

    try:
        with open(orders_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                # Fields order_id|customer_name|order_date|total_amount|status|shipping_address
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                o_status = parts[4]
                if filter_status and filter_status != o_status:
                    continue
                order = {
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'order_date': parts[2],
                    'total_amount': float(parts[3]),
                    'status': o_status,
                    'shipping_address': parts[5]
                }
                orders.append(order)
    except Exception:
        pass

    selected_status = filter_status
    return render_template('orders.html', orders=orders, selected_status=selected_status)

# 8. Order details page
@app.route('/orders/<int:order_id>', methods=['GET'])
def 7j0tt847qmc36jj(order_id):
    order_path = os.path.join(DATA_DIR, 'orders.txt')
    order_items_path = os.path.join(DATA_DIR, 'order_items.txt')
    order = None
    order_items = []
    # Read order
    try:
        with open(order_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                curr_order_id = int(parts[0])
                if curr_order_id == order_id:
                    order = {
                        'order_id': curr_order_id,
                        'customer_name': parts[1],
                        'order_date': parts[2],
                        'total_amount': float(parts[3]),
                        'status': parts[4],
                        'shipping_address': parts[5]
                    }
                    break
    except Exception:
        pass

    # Read order items
    try:
        with open(order_items_path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                order_item_id = int(parts[0])
                o_id = int(parts[1])
                if o_id == order_id:
                    item = {
                        'order_item_id': order_item_id,
                        'order_id': o_id,
                        'book_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    }
                    order_items.append(item)
    except Exception:
        pass

    if not order:
        return redirect(url_for('7dzgv3drh0oal33'))

    return render_template('order_details.html', order=order, order_items=order_items)

if __name__ == '__main__':
    app.run(debug=True)
