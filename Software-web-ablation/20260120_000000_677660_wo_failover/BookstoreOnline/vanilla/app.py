from flask import Flask, render_template, redirect, url_for, request
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to read and write pipe-delimited files for each schema

def read_pipe_delimited(filename, fields_count):
    path = os.path.join(DATA_DIR, filename)
    data = []
    if not os.path.exists(path):
        return data
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != fields_count:
                    continue
                data.append(parts)
    except Exception:
        pass
    return data


def write_pipe_delimited(filename, rows):
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for row in rows:
                # Cast all elements to str and join with pipe
                f.write('|'.join(str(e) for e in row) + '\n')
    except Exception:
        pass

# Books
# 1. book_id (int)
# 2. title (str)
# 3. author (str)
# 4. isbn (str)
# 5. category (str)
# 6. price (float)
# 7. stock (int)
# 8. description (str)
def load_books():
    raw = read_pipe_delimited('books.txt', 8)
    books = []
    for r in raw:
        try:
            books.append({
                'book_id': int(r[0]),
                'title': r[1],
                'author': r[2],
                'isbn': r[3],
                'category': r[4],
                'price': float(r[5]),
                'stock': int(r[6]),
                'description': r[7]
            })
        except Exception:
            continue
    return books

def write_books(books):
    rows = []
    for b in books:
        rows.append([
            b['book_id'],
            b['title'],
            b['author'],
            b['isbn'],
            b['category'],
            '%.2f' % b['price'],
            b['stock'],
            b['description']
        ])
    write_pipe_delimited('books.txt', rows)

# Categories
# 1. category_id (int)
# 2. category_name (str)
# 3. description (str)
def load_categories():
    raw = read_pipe_delimited('categories.txt', 3)
    categories = []
    for r in raw:
        try:
            categories.append({
                'category_id': int(r[0]),
                'category_name': r[1],
                'description': r[2]
            })
        except Exception:
            continue
    return categories

# Cart
# 1. cart_id (int)
# 2. book_id (int)
# 3. quantity (int)
# 4. added_date (str - YYYY-MM-DD)
def load_cart():
    raw = read_pipe_delimited('cart.txt', 4)
    cart_items = []
    for r in raw:
        try:
            cart_items.append({
                'cart_id': int(r[0]),
                'book_id': int(r[1]),
                'quantity': int(r[2]),
                'added_date': r[3]
            })
        except Exception:
            continue
    return cart_items


def write_cart(cart_items):
    rows = []
    for item in cart_items:
        rows.append([
            item['cart_id'],
            item['book_id'],
            item['quantity'],
            item['added_date']
        ])
    write_pipe_delimited('cart.txt', rows)

# Orders
# 1. order_id (int)
# 2. customer_name (str)
# 3. order_date (str - YYYY-MM-DD)
# 4. total_amount (float)
# 5. status (str)
# 6. shipping_address (str)
def load_orders():
    raw = read_pipe_delimited('orders.txt', 6)
    orders = []
    for r in raw:
        try:
            orders.append({
                'order_id': int(r[0]),
                'customer_name': r[1],
                'order_date': r[2],
                'total_amount': float(r[3]),
                'status': r[4],
                'shipping_address': r[5]
            })
        except Exception:
            continue
    return orders


def write_orders(orders):
    rows = []
    for o in orders:
        rows.append([
            o['order_id'],
            o['customer_name'],
            o['order_date'],
            '%.2f' % o['total_amount'],
            o['status'],
            o['shipping_address']
        ])
    write_pipe_delimited('orders.txt', rows)

# Order Items
# 1. order_item_id (int)
# 2. order_id (int)
# 3. book_id (int)
# 4. quantity (int)
# 5. price (float)
def load_order_items():
    raw = read_pipe_delimited('order_items.txt', 5)
    order_items = []
    for r in raw:
        try:
            order_items.append({
                'order_item_id': int(r[0]),
                'order_id': int(r[1]),
                'book_id': int(r[2]),
                'quantity': int(r[3]),
                'price': float(r[4])
            })
        except Exception:
            continue
    return order_items


def write_order_items(order_items):
    rows = []
    for oi in order_items:
        rows.append([
            oi['order_item_id'],
            oi['order_id'],
            oi['book_id'],
            oi['quantity'],
            '%.2f' % oi['price']
        ])
    write_pipe_delimited('order_items.txt', rows)

# Reviews
# 1. review_id (int)
# 2. book_id (int)
# 3. customer_name (str)
# 4. rating (int) (1-5)
# 5. review_text (str)
# 6. review_date (str - YYYY-MM-DD)
def load_reviews():
    raw = read_pipe_delimited('reviews.txt', 6)
    reviews = []
    for r in raw:
        try:
            reviews.append({
                'review_id': int(r[0]),
                'book_id': int(r[1]),
                'customer_name': r[2],
                'rating': int(r[3]),
                'review_text': r[4],
                'review_date': r[5]
            })
        except Exception:
            continue
    return reviews


def write_reviews(reviews):
    rows = []
    for rev in reviews:
        rows.append([
            rev['review_id'],
            rev['book_id'],
            rev['customer_name'],
            rev['rating'],
            rev['review_text'],
            rev['review_date']
        ])
    write_pipe_delimited('reviews.txt', rows)

# Bestsellers
# 1. book_id (int)
# 2. sales_count (int)
# 3. period (str)
def load_bestsellers():
    raw = read_pipe_delimited('bestsellers.txt', 3)
    bestsellers = []
    for r in raw:
        try:
            bestsellers.append({
                'book_id': int(r[0]),
                'sales_count': int(r[1]),
                'period': r[2]
            })
        except Exception:
            continue
    return bestsellers


# 1. Root Route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# 2. Dashboard Page
@app.route('/dashboard')
def dashboard():
    # Featured books: we can choose first 5 books as featured
    books = load_books()
    featured_books = books[:5] if len(books) > 5 else books
    # Bestsellers for all time from bestsellers.txt filtered for period 'All Time' or fallback
    bestsellers_data = load_bestsellers()
    # Collect books info for bestsellers period 'All Time'
    bestsellers = []
    for b in bestsellers_data:
        if b['period'] == 'All Time':
            book_info = next((book for book in books if book['book_id'] == b['book_id']), None)
            if book_info:
                bdict = {
                    'book_id': book_info['book_id'],
                    'title': book_info['title'],
                    'author': book_info['author'],
                    'sales_count': b['sales_count']
                }
                bestsellers.append(bdict)
    # If no 'All Time' bestsellers found, fallback to any period.
    if not bestsellers and bestsellers_data:
        for b in bestsellers_data:
            book_info = next((book for book in books if book['book_id'] == b['book_id']), None)
            if book_info:
                bestsellers.append({
                    'book_id': book_info['book_id'],
                    'title': book_info['title'],
                    'author': book_info['author'],
                    'sales_count': b['sales_count']
                })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)

# 3. Book Catalog Page
@app.route('/catalog')
def catalog():
    books = load_books()
    categories = load_categories()
    search_query = request.args.get('search', '').strip()
    selected_category = request.args.get('category', '').strip()

    filtered_books = books
    if search_query:
        sq = search_query.lower()
        filtered_books = [b for b in filtered_books if sq in b['title'].lower() or sq in b['author'].lower() or sq in b['isbn'].lower()]
    if selected_category:
        filtered_books = [b for b in filtered_books if b['category'] == selected_category]

    return render_template('catalog.html', books=filtered_books, categories=categories, search_query=search_query, selected_category=selected_category)

# 4. Book Details Page
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details(book_id):
    books = load_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404

    reviews = load_reviews()
    book_reviews = [r for r in reviews if r['book_id'] == book_id]

    if request.method == 'POST':
        # Add to Cart
        try:
            quantity = int(request.form.get('quantity', '1'))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
        
        cart_items = load_cart()
        # Check if item already in cart
        found = False
        for item in cart_items:
            if item['book_id'] == book_id:
                item['quantity'] += quantity
                found = True
                break
        if not found:
            new_cart_id = max([item['cart_id'] for item in cart_items], default=0) + 1
            today_str = datetime.date.today().strftime('%Y-%m-%d')
            cart_items.append({
                'cart_id': new_cart_id,
                'book_id': book_id,
                'quantity': quantity,
                'added_date': today_str
            })
        write_cart(cart_items)
        return redirect(url_for('shopping_cart'))

    # GET
    return render_template('book_details.html', book=book, reviews=book_reviews)

# 5. Shopping Cart Page
@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_items = load_cart()
    books = load_books()

    if request.method == 'POST':
        # Handle update quantity or remove item
        try:
            cart_id = int(request.form.get('cart_id', '0'))
        except ValueError:
            return redirect(url_for('shopping_cart'))

        # Identify action: either 'update_quantity' or 'remove'
        quantity_str = request.form.get('quantity')
        remove = request.form.get('remove')

        cart_modified = False
        if remove == 'true':
            # Remove item
            cart_items = [item for item in cart_items if item['cart_id'] != cart_id]
            cart_modified = True
        else:
            try:
                new_quantity = int(quantity_str)
                if new_quantity < 1:
                    # Remove the item if quantity set less than 1
                    cart_items = [item for item in cart_items if item['cart_id'] != cart_id]
                else:
                    for item in cart_items:
                        if item['cart_id'] == cart_id:
                            item['quantity'] = new_quantity
                            break
                cart_modified = True
            except (ValueError, TypeError):
                pass

        if cart_modified:
            write_cart(cart_items)
        return redirect(url_for('shopping_cart'))

    # GET: Prepare cart_items list with book info
    display_cart_items = []
    total_amount = 0.0
    for item in cart_items:
        book_info = next((b for b in books if b['book_id'] == item['book_id']), None)
        if book_info:
            price = book_info['price']
            subtotal = price * item['quantity']
            total_amount += subtotal
            display_cart_items.append({
                'cart_id': item['cart_id'],
                'book_id': book_info['book_id'],
                'title': book_info['title'],
                'quantity': item['quantity'],
                'price': price,
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=display_cart_items, total_amount=total_amount)

# 6. Checkout Page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not shipping_address or not payment_method:
            # Missing fields, just re-render page with a message (not specified, so redirect back)
            return render_template('checkout.html')

        cart_items = load_cart()
        books = load_books()

        if not cart_items:
            # No items in cart, redirect back
            return redirect(url_for('shopping_cart'))

        # Calculate total amount
        total_amount = 0.0
        for item in cart_items:
            book_info = next((b for b in books if b['book_id'] == item['book_id']), None)
            if not book_info:
                continue
            total_amount += book_info['price'] * item['quantity']

        # Create new order
        orders = load_orders()
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        today_str = datetime.date.today().strftime('%Y-%m-%d')

        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'order_date': today_str,
            'total_amount': total_amount,
            'status': 'Pending',
            'shipping_address': shipping_address
        }
        orders.append(new_order)
        write_orders(orders)

        # Create order items
        order_items = load_order_items()
        max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)
        for item in cart_items:
            max_order_item_id += 1
            book_info = next((b for b in books if b['book_id'] == item['book_id']), None)
            if not book_info:
                continue
            order_items.append({
                'order_item_id': max_order_item_id,
                'order_id': new_order_id,
                'book_id': item['book_id'],
                'quantity': item['quantity'],
                'price': book_info['price']
            })
        write_order_items(order_items)

        # Clear cart
        write_cart([])

        return redirect(url_for('order_history'))

    # GET
    return render_template('checkout.html')

# 7. Order History Page
@app.route('/orders')
def order_history():
    status_filter = request.args.get('status', 'All')
    orders = load_orders()

    if status_filter and status_filter != 'All':
        filtered_orders = [o for o in orders if o['status'] == status_filter]
    else:
        filtered_orders = orders

    return render_template('orders.html', orders=filtered_orders, status_filter=status_filter)

# 8. View Order Details
@app.route('/orders/<int:order_id>')
def order_details(order_id):
    orders = load_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    order_items = load_order_items()
    books = load_books()
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            book_info = next((b for b in books if b['book_id'] == oi['book_id']), None)
            if book_info:
                item = {
                    'order_item_id': oi['order_item_id'],
                    'book_id': oi['book_id'],
                    'quantity': oi['quantity'],
                    'price': oi['price'],
                    'title': book_info['title']
                }
                items.append(item)

    return render_template('order_details.html', order=order, order_items=items)

# 9. Reviews Page
@app.route('/reviews')
def reviews():
    filter_rating = request.args.get('rating', 'All')
    reviews_list = load_reviews()
    books = load_books()

    filtered_reviews = []
    if filter_rating != 'All':
        try:
            rating_val = int(filter_rating)
            filtered_reviews = [r for r in reviews_list if r['rating'] == rating_val]
        except ValueError:
            filtered_reviews = reviews_list
    else:
        filtered_reviews = reviews_list

    # Add book title to each review dict for template
    reviews_with_title = []
    for r in filtered_reviews:
        book_info = next((b for b in books if b['book_id'] == r['book_id']), None)
        title = book_info['title'] if book_info else 'Unknown'
        reviews_with_title.append({
            'review_id': r['review_id'],
            'book_title': title,
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    return render_template('reviews.html', reviews_list=reviews_with_title, filter_rating=filter_rating)

# 10. Write Review Page
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    # Purchased books: only books that were ordered before
    orders = load_orders()
    order_items = load_order_items()
    books = load_books()
    purchased_book_ids = set()
    for oi in order_items:
        purchased_book_ids.add(oi['book_id'])

    purchased_books = [b for b in books if b['book_id'] in purchased_book_ids]

    if request.method == 'POST':
        book_id_str = request.form.get('book_id', '')
        rating_str = request.form.get('rating', '')
        review_text = request.form.get('review_text', '').strip()

        try:
            book_id = int(book_id_str)
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                rating = 5
        except ValueError:
            return render_template('write_review.html', purchased_books=purchased_books)

        if not review_text:
            return render_template('write_review.html', purchased_books=purchased_books)

        # Generate new review_id
        reviews = load_reviews()
        new_review_id = max([r['review_id'] for r in reviews], default=0) + 1
        today_str = datetime.date.today().strftime('%Y-%m-%d')

        # Using customer_name as 'Anonymous' since system doesn't track login
        new_review = {
            'review_id': new_review_id,
            'book_id': book_id,
            'customer_name': 'Anonymous',
            'rating': rating,
            'review_text': review_text,
            'review_date': today_str
        }
        reviews.append(new_review)
        write_reviews(reviews)

        return redirect(url_for('reviews'))

    return render_template('write_review.html', purchased_books=purchased_books)

# 11. Bestsellers Page
@app.route('/bestsellers')
def bestsellers():
    time_period = request.args.get('period', 'All Time')
    bestsellers_data = load_bestsellers()
    books = load_books()
    filtered = [b for b in bestsellers_data if b['period'] == time_period]

    bestsellers_list = []
    for b in filtered:
        book_info = next((book for book in books if book['book_id'] == b['book_id']), None)
        if book_info:
            bestsellers_list.append({
                'book_id': book_info['book_id'],
                'title': book_info['title'],
                'author': book_info['author'],
                'sales_count': b['sales_count']
            })

    return render_template('bestsellers.html', bestsellers_list=bestsellers_list, time_period=time_period)


if __name__ == '__main__':
    app.run(debug=True)
