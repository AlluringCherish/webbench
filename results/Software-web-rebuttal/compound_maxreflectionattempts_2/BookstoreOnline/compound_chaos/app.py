from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions for reading and writing data files (pipe-delimited)

def read_books():
    books = []
    path = os.path.join(DATA_DIR, 'books.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 8:
                    continue
                try:
                    book_id = int(parts[0])
                    title = parts[1]
                    author = parts[2]
                    isbn = parts[3]
                    category = parts[4]
                    price = float(parts[5])
                    stock = int(parts[6])
                    description = parts[7]
                    books.append({
                        'book_id': book_id,
                        'title': title,
                        'author': author,
                        'isbn': isbn,
                        'category': category,
                        'price': price,
                        'stock': stock,
                        'description': description
                    })
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return books


def write_books(books):
    path = os.path.join(DATA_DIR, 'books.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for book in books:
                line = f"{book['book_id']}|{book['title']}|{book['author']}|{book['isbn']}|{book['category']}|{book['price']}|{book['stock']}|{book['description']}"
                f.write(line + '\n')
    except Exception:
        pass


def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                try:
                    category_id = int(parts[0])
                    category_name = parts[1]
                    description = parts[2]
                    categories.append({
                        'category_id': category_id,
                        'category_name': category_name,
                        'description': description
                    })
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return categories


def read_cart():
    cart = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                try:
                    cart_id = int(parts[0])
                    book_id = int(parts[1])
                    quantity = int(parts[2])
                    added_date = parts[3]
                    cart.append({
                        'cart_id': cart_id,
                        'book_id': book_id,
                        'quantity': quantity,
                        'added_date': added_date
                    })
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return cart


def write_cart(cart):
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for item in cart:
                line = f"{item['cart_id']}|{item['book_id']}|{item['quantity']}|{item['added_date']}"
                f.write(line + '\n')
    except Exception:
        pass


def read_orders():
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
                    order_id = int(parts[0])
                    customer_name = parts[1]
                    order_date = parts[2]
                    total_amount = float(parts[3])
                    status = parts[4]
                    shipping_address = parts[5]
                    orders.append({
                        'order_id': order_id,
                        'customer_name': customer_name,
                        'order_date': order_date,
                        'total_amount': total_amount,
                        'status': status,
                        'shipping_address': shipping_address
                    })
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return orders


def write_orders(orders):
    path = os.path.join(DATA_DIR, 'orders.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for order in orders:
                line = f"{order['order_id']}|{order['customer_name']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['shipping_address']}"
                f.write(line + '\n')
    except Exception:
        pass


def read_order_items():
    order_items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                try:
                    order_item_id = int(parts[0])
                    order_id = int(parts[1])
                    book_id = int(parts[2])
                    quantity = int(parts[3])
                    price = float(parts[4])
                    order_items.append({
                        'order_item_id': order_item_id,
                        'order_id': order_id,
                        'book_id': book_id,
                        'quantity': quantity,
                        'price': price
                    })
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return order_items


def write_order_items(order_items):
    path = os.path.join(DATA_DIR, 'order_items.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for item in order_items:
                line = f"{item['order_item_id']}|{item['order_id']}|{item['book_id']}|{item['quantity']}|{item['price']}"
                f.write(line + '\n')
    except Exception:
        pass


def read_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                try:
                    review_id = int(parts[0])
                    book_id = int(parts[1])
                    customer_name = parts[2]
                    rating = int(parts[3])
                    review_text = parts[4]
                    review_date = parts[5]
                    reviews.append({
                        'review_id': review_id,
                        'book_id': book_id,
                        'customer_name': customer_name,
                        'rating': rating,
                        'review_text': review_text,
                        'review_date': review_date
                    })
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return reviews


def write_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for review in reviews:
                line = f"{review['review_id']}|{review['book_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}"
                f.write(line + '\n')
    except Exception:
        pass


def read_bestsellers():
    bestsellers = []
    path = os.path.join(DATA_DIR, 'bestsellers.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 3:
                    continue
                try:
                    book_id = int(parts[0])
                    sales_count = int(parts[1])
                    period = parts[2]
                    bestsellers.append({
                        'book_id': book_id,
                        'sales_count': sales_count,
                        'period': period
                    })
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        pass
    return bestsellers


def write_bestsellers(bestsellers):
    path = os.path.join(DATA_DIR, 'bestsellers.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for entry in bestsellers:
                line = f"{entry['book_id']}|{entry['sales_count']}|{entry['period']}"
                f.write(line + '\n')
    except Exception:
        pass


# Route 1: Root Route - Redirect to /dashboard
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Route 2: Dashboard Page
@app.route('/dashboard')
def dashboard_page():
    # featured_books: We'll use all books with stock > 0 as featured (example logic)
    books = read_books()
    featured_books = [book for book in books if book['stock'] > 0][:10]

    # bestsellers: Get all bestsellers with period 'This Month' (example)
    bestsellers_raw = read_bestsellers()
    bestsellers_filtered = [b for b in bestsellers_raw if b['period'] == 'This Month']

    # For each bestseller, add title and author from books
    bestsellers = []
    for entry in bestsellers_filtered:
        book = next((b for b in books if b['book_id'] == entry['book_id']), None)
        if book:
            bestsellers.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': entry['sales_count'],
                'period': entry['period']
            })

    return render_template('dashboard.html', featured_books=featured_books, bestsellers=bestsellers)


# Route 3: Book Catalog Page
@app.route('/catalog', methods=['GET'])
def catalog_page():
    categories = read_categories()
    books = read_books()

    # Get query parameters
    search_query = request.args.get('search_query', '').strip()
    selected_category = request.args.get('category_filter', '').strip()

    filtered_books = books

    if search_query:
        search_lower = search_query.lower()
        filtered_books = [book for book in filtered_books if search_lower in book['title'].lower() or search_lower in book['author'].lower()]

    if selected_category:
        filtered_books = [book for book in filtered_books if book['category'] == selected_category]

    return render_template('catalog.html', categories=categories, books=filtered_books, search_query=search_query, selected_category=selected_category)


# Route 4: Book Details Page
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_details_page(book_id):
    books = read_books()
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        return "Book not found", 404

    # Handle POST: Add to cart
    if request.method == 'POST':
        quantity_str = request.form.get('quantity', '1')
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

        cart = read_cart()
        # Check if book is already in cart
        existing_item = next((item for item in cart if item['book_id'] == book_id), None)
        today_str = datetime.now().strftime('%Y-%m-%d')
        if existing_item:
            # Update quantity
            new_quantity = existing_item['quantity'] + quantity
            # Stock validation: do not exceed book stock
            new_quantity = min(new_quantity, book['stock'])
            existing_item['quantity'] = new_quantity
            existing_item['added_date'] = today_str
        else:
            # New cart id, find max existing
            max_id = max([item['cart_id'] for item in cart], default=0)
            new_cart_item = {
                'cart_id': max_id + 1,
                'book_id': book_id,
                'quantity': min(quantity, book['stock']),
                'added_date': today_str
            }
            cart.append(new_cart_item)

        write_cart(cart)
        return redirect(url_for('cart_page'))

    # GET method
    reviews_all = read_reviews()
    reviews = [r for r in reviews_all if r['book_id'] == book_id]
    # To conform to context variable names for reviews, map fields accordingly
    reviews_output = []
    for r in reviews:
        reviews_output.append({
            'review_id': r['review_id'],
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    return render_template('book_details.html', book=book, reviews=reviews_output)


# Route 5: Shopping Cart Page
@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    cart = read_cart()
    books = read_books()

    if request.method == 'POST':
        # Expect form data: cart_id and either quantity or remove action
        cart_id_str = request.form.get('cart_id')
        if cart_id_str is None:
            return redirect(url_for('cart_page'))
        try:
            cart_id = int(cart_id_str)
        except ValueError:
            return redirect(url_for('cart_page'))

        action = request.form.get('action', '')
        quantity_str = request.form.get('quantity')

        # Find cart item
        item = next((item for item in cart if item['cart_id'] == cart_id), None)
        if not item:
            return redirect(url_for('cart_page'))

        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if not book:
            # If book not found, remove cart item
            cart = [c for c in cart if c['cart_id'] != cart_id]
            write_cart(cart)
            return redirect(url_for('cart_page'))

        if action == 'remove':
            # Remove cart item
            cart = [c for c in cart if c['cart_id'] != cart_id]
            write_cart(cart)
            return redirect(url_for('cart_page'))

        elif action == 'update':
            try:
                quantity = int(quantity_str)
                if quantity < 1:
                    quantity = 1
            except (ValueError, TypeError):
                quantity = item['quantity']

            # Do not exceed stock
            quantity = min(quantity, book['stock'])
            item['quantity'] = quantity
            write_cart(cart)
            return redirect(url_for('cart_page'))

        # Unknown action, redirect
        return redirect(url_for('cart_page'))

    # GET method
    cart_items = []
    total_amount = 0.0
    for item in cart:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if not book:
            continue
        quantity = item['quantity']
        price = book['price']
        subtotal = round(quantity * price, 2)
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


# Route 6: Checkout Page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    cart = read_cart()
    books = read_books()

    cart_items = []
    total_amount = 0.0
    for item in cart:
        book = next((b for b in books if b['book_id'] == item['book_id']), None)
        if not book:
            continue
        quantity = item['quantity']
        price = book['price']
        subtotal = round(quantity * price, 2)
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

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        valid_payment_methods = ['Credit Card', 'PayPal', 'Bank Transfer']

        # Validate form data
        if not customer_name or not shipping_address or payment_method not in valid_payment_methods:
            # Render page with error - for simplicity, just show page again
            return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

        if not cart_items:
            # No items to checkout
            return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)

        # Create new order
        orders = read_orders()
        order_items = read_order_items()

        max_order_id = max([o['order_id'] for o in orders], default=0)
        new_order_id = max_order_id + 1
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

        max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)

        new_order_items = []
        for i, item in enumerate(cart_items):
            max_order_item_id += 1
            new_order_items.append({
                'order_item_id': max_order_item_id,
                'order_id': new_order_id,
                'book_id': item['book_id'],
                'quantity': item['quantity'],
                'price': item['price']
            })

        order_items.extend(new_order_items)

        # Write back orders and order items
        write_orders(orders)
        write_order_items(order_items)

        # Clear cart
        write_cart([])

        return redirect(url_for('orders_page'))

    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)


# Route 7: Order History Page
@app.route('/orders', methods=['GET'])
def orders_page():
    orders = read_orders()

    # Get status filter from query string
    status_filter = request.args.get('status_filter', 'All')
    if status_filter != 'All':
        orders = [o for o in orders if o['status'] == status_filter]

    return render_template('orders.html', orders=orders, status_filter=status_filter)


# Note: Route 8 (Order Details Page) is omitted per spec not required here


# Route 9: Reviews Page
@app.route('/reviews', methods=['GET'])
def reviews_page():
    reviews_all = read_reviews()
    books = read_books()

    rating_filter = request.args.get('rating_filter', 'All')

    if rating_filter != 'All':
        try:
            rating_value = int(rating_filter[0])  # e.g. '5 stars' starts with '5'
            reviews_filtered = [r for r in reviews_all if r['rating'] == rating_value]
        except (ValueError, IndexError):
            reviews_filtered = reviews_all
    else:
        reviews_filtered = reviews_all

    # Add book_title to each review
    reviews_output = []
    for r in reviews_filtered:
        book = next((b for b in books if b['book_id'] == r['book_id']), None)
        book_title = book['title'] if book else ''
        reviews_output.append({
            'review_id': r['review_id'],
            'book_id': r['book_id'],
            'book_title': book_title,
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    return render_template('reviews.html', reviews=reviews_output, rating_filter=rating_filter)


# Route 10: Write Review Page
@app.route('/write_review', methods=['GET', 'POST'])
def write_review_page():
    # Determine purchased books from orders and order_items
    orders = read_orders()
    order_items = read_order_items()
    books = read_books()

    # We gather unique book_ids from order_items linked to existing orders for all customers
    # Since no user management given, show all purchased books (books appearing in orders)
    purchased_book_ids = set()
    order_ids = set(order['order_id'] for order in orders)
    for item in order_items:
        if item['order_id'] in order_ids:
            purchased_book_ids.add(item['book_id'])

    purchased_books = []
    for book_id in purchased_book_ids:
        book = next((b for b in books if b['book_id'] == book_id), None)
        if book:
            purchased_books.append({'book_id': book['book_id'], 'title': book['title']})

    if request.method == 'POST':
        book_id_str = request.form.get('book_id', '')
        rating_str = request.form.get('rating', '')
        review_text = request.form.get('review_text', '').strip()

        try:
            book_id = int(book_id_str)
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            return render_template('write_review.html', purchased_books=purchased_books)

        if book_id not in purchased_book_ids:
            # User cannot review a book not purchased
            return render_template('write_review.html', purchased_books=purchased_books)

        reviews = read_reviews()
        max_review_id = max([r['review_id'] for r in reviews], default=0)
        new_review_id = max_review_id + 1
        # Use generic customer name, no user management so use "Anonymous"
        customer_name = "Anonymous"
        review_date = datetime.now().strftime('%Y-%m-%d')

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

    return render_template('write_review.html', purchased_books=purchased_books)


# Route 11: Bestsellers Page
@app.route('/bestsellers', methods=['GET'])
def bestsellers_page():
    bestsellers_all = read_bestsellers()
    books = read_books()

    time_period_filter = request.args.get('time_period_filter', 'This Week')
    filtered = [b for b in bestsellers_all if b['period'] == time_period_filter]

    # Sort descending by sales_count
    filtered.sort(key=lambda x: x['sales_count'], reverse=True)

    bestsellers = []
    for entry in filtered:
        book = next((b for b in books if b['book_id'] == entry['book_id']), None)
        if book:
            bestsellers.append({
                'book_id': book['book_id'],
                'title': book['title'],
                'author': book['author'],
                'sales_count': entry['sales_count'],
                'period': entry['period']
            })

    return render_template('bestsellers.html', bestsellers=bestsellers, time_period_filter=time_period_filter)


if __name__ == '__main__':
    app.run(debug=True)
