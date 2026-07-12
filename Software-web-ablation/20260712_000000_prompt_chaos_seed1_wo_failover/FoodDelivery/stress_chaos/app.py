from flask import Flask, render_template, redirect, url_for, request, abort, flash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data from files

def load_restaurants():
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    restaurants = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        restaurant = {
                            'restaurant_id': int(parts[0]),
                            'name': parts[1],
                            'cuisine': parts[2],
                            'address': parts[3],
                            'phone': parts[4],
                            'rating': float(parts[5]),
                            'delivery_time': int(parts[6]),
                            'min_order': float(parts[7])
                        }
                        restaurants.append(restaurant)
                    except ValueError:
                        continue
    except (IOError, FileNotFoundError):
        # file not found or other IO error
        restaurants = []
    return restaurants


def load_menus():
    path = os.path.join(DATA_DIR, 'menus.txt')
    menus = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    try:
                        menu_item = {
                            'item_id': int(parts[0]),
                            'restaurant_id': int(parts[1]),
                            'item_name': parts[2],
                            'name': parts[2],  # For template compatibility
                            'category': parts[3],
                            'description': parts[4],
                            'price': float(parts[5]),
                            'availability': int(parts[6])
                        }
                        menus.append(menu_item)
                    except ValueError:
                        continue
    except (IOError, FileNotFoundError):
        menus = []
    return menus


def load_cart():
    path = os.path.join(DATA_DIR, 'cart.txt')
    cart = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    try:
                        cart_item = {
                            'cart_id': int(parts[0]),
                            'item_id': int(parts[1]),
                            'restaurant_id': int(parts[2]),
                            'quantity': int(parts[3]),
                            'added_date': parts[4]
                        }
                        cart.append(cart_item)
                    except ValueError:
                        continue
    except (IOError, FileNotFoundError):
        cart = []
    return cart


def load_orders():
    path = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 8:
                    try:
                        order = {
                            'order_id': int(parts[0]),
                            'customer_name': parts[1],
                            'restaurant_id': int(parts[2]),
                            'order_date': parts[3],
                            'total_amount': float(parts[4]),
                            'status': parts[5],
                            'delivery_address': parts[6],
                            'phone_number': parts[7]
                        }
                        orders.append(order)
                    except ValueError:
                        continue
    except (IOError, FileNotFoundError):
        orders = []
    return orders


def load_order_items():
    path = os.path.join(DATA_DIR, 'order_items.txt')
    order_items = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    try:
                        order_item = {
                            'order_item_id': int(parts[0]),
                            'order_id': int(parts[1]),
                            'item_id': int(parts[2]),
                            'quantity': int(parts[3]),
                            'price': float(parts[4])
                        }
                        order_items.append(order_item)
                    except ValueError:
                        continue
    except (IOError, FileNotFoundError):
        order_items = []
    return order_items


def load_deliveries():
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    deliveries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    try:
                        delivery = {
                            'delivery_id': int(parts[0]),
                            'order_id': int(parts[1]),
                            'driver_name': parts[2],
                            'driver_phone': parts[3],
                            'vehicle_info': parts[4],
                            'status': parts[5],
                            'estimated_time': parts[6]
                        }
                        deliveries.append(delivery)
                    except ValueError:
                        continue
    except (IOError, FileNotFoundError):
        deliveries = []
    return deliveries


def load_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    try:
                        review = {
                            'review_id': int(parts[0]),
                            'restaurant_id': int(parts[1]),
                            'customer_name': parts[2],
                            'rating': int(parts[3]),
                            'review_text': parts[4],
                            'review_date': parts[5]
                        }
                        reviews.append(review)
                    except ValueError:
                        continue
    except (IOError, FileNotFoundError):
        reviews = []
    return reviews

# Helper function to write cart back to file
# Overwrites entire cart.txt

def save_cart(cart):
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for item in cart:
                line = f"{item['cart_id']}|{item['item_id']}|{item['restaurant_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
        return True
    except (IOError, OSError):
        return False


# Route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    # Select featured restaurants: for simplicity, top 3 by rating
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]

    # popular cuisines - distinct cuisines sorted by frequency in the list
    cuisine_count = {}
    for r in restaurants:
        cuisine_count[r['cuisine']] = cuisine_count.get(r['cuisine'], 0) + 1
    popular_cuisines = sorted(cuisine_count, key=lambda k: cuisine_count[k], reverse=True)[:5]

    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=popular_cuisines)


@app.route('/restaurants')
def restaurant_listing():
    restaurants = load_restaurants()
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    return render_template('restaurants.html', restaurants=restaurants, cuisines=cuisines)


@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()

    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        abort(404)
    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability'] == 1]

    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)


@app.route('/item/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability'] == 1), None)
    if not item:
        abort(404)
    return render_template('item_details.html', item=item)


@app.route('/item/<int:item_id>/add', methods=['POST'])
def add_item_to_cart(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability'] == 1), None)
    if not item:
        abort(404)

    try:
        quantity = int(request.form.get('quantity', '1'))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1

    cart = load_cart()

    # Check if item already in cart, update quantity
    existing = next((c for c in cart if c['item_id'] == item_id), None)
    if existing:
        existing['quantity'] += quantity
    else:
        cart_id = max([c['cart_id'] for c in cart], default=0) + 1
        now_date = datetime.now().strftime('%Y-%m-%d')
        cart.append({
            'cart_id': cart_id,
            'item_id': item_id,
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': now_date
        })

    saved = save_cart(cart)
    if not saved:
        abort(500, description='Failed to save cart')

    return redirect(url_for('shopping_cart'))


@app.route('/cart')
def shopping_cart():
    cart = load_cart()
    menus = load_menus()

    cart_items = []
    total_amount = 0.0

    for c in cart:
        item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if item:
            item_total = item['price'] * c['quantity']
            total_amount += item_total
            cart_items.append({
                'cart_id': c['cart_id'],
                'item_id': c['item_id'],
                'restaurant_id': c['restaurant_id'],
                'quantity': c['quantity'],
                'name': item['item_name'],  # corrected key for template
                'price': item['price'],
                'total_price': item_total
            })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


@app.route('/cart/update', methods=['POST'])
def update_cart():
    cart = load_cart()
    updated = False

    for key in request.form:
        if key.startswith('quantity_'):
            try:
                cart_id = int(key.split('_')[1])
                new_qty = int(request.form[key])
                if new_qty < 1:
                    new_qty = 1
                for c in cart:
                    if c['cart_id'] == cart_id:
                        c['quantity'] = new_qty
                        updated = True
                        break
            except (IndexError, ValueError):
                continue

    if updated:
        saved = save_cart(cart)
        if not saved:
            abort(500, description='Failed to save cart updates')

    return redirect(url_for('shopping_cart'))


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    cart = load_cart()
    new_cart = [c for c in cart if c['item_id'] != item_id]
    if len(new_cart) == len(cart):
        # Item not found in cart
        abort(404)

    saved = save_cart(new_cart)
    if not saved:
        abort(500, description='Failed to save cart after removal')

    return redirect(url_for('shopping_cart'))


@app.route('/checkout')
def checkout():
    return render_template('checkout.html', errors=None, previous_input=None)


@app.route('/checkout/place_order', methods=['POST'])
def place_order():
    customer_name = request.form.get('customer_name', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    payment_method = request.form.get('payment_method', '').strip()

    errors = {}

    # Validate inputs
    if not customer_name:
        errors['customer_name'] = 'Customer name is required.'
    if not delivery_address:
        errors['delivery_address'] = 'Delivery address is required.'
    if not phone_number:
        errors['phone_number'] = 'Phone number is required.'
    if not payment_method:
        errors['payment_method'] = 'Payment method is required.'

    cart = load_cart()
    if not cart:
        errors['cart'] = 'Your cart is empty.'

    if errors:
        return render_template('checkout.html', errors=errors, previous_input=request.form)

    menus = load_menus()

    # Calculate total amount
    total_amount = 0.0
    for c in cart:
        item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if not item:
            errors['cart'] = 'Invalid item in cart.'
            break
        total_amount += item['price'] * c['quantity']

    if errors:
        return render_template('checkout.html', errors=errors, previous_input=request.form)

    # Find restaurant_id - for simplicity, if multiple items from different restaurants, pick the first one
    restaurant_id = cart[0]['restaurant_id'] if cart else None

    # Assign new order_id
    orders = load_orders()
    new_order_id = max([o['order_id'] for o in orders], default=0) + 1

    # Current date
    order_date = datetime.now().strftime('%Y-%m-%d')

    # Save new order to orders.txt
    order_line = f"{new_order_id}|{customer_name}|{restaurant_id}|{order_date}|{total_amount:.2f}|Pending|{delivery_address}|{phone_number}\n"
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'a', encoding='utf-8') as f:
            f.write(order_line)
    except (IOError, OSError):
        abort(500, description='Failed to place order')

    # Save order items
    order_items = load_order_items()
    current_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1

    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'a', encoding='utf-8') as f:
            for c in cart:
                item = next((m for m in menus if m['item_id'] == c['item_id']), None)
                if not item:
                    continue
                line = f"{current_order_item_id}|{new_order_id}|{c['item_id']}|{c['quantity']}|{item['price']:.2f}\n"
                f.write(line)
                current_order_item_id += 1
    except (IOError, OSError):
        abort(500, description='Failed to record order items')

    # Clear the cart (overwrite with empty)
    save_cart([])

    return redirect(url_for('active_orders'))


@app.route('/orders/active')
def active_orders():
    orders = load_orders()

    # Get all possible statuses dynamically from orders data
    statuses = sorted(set([o['status'] for o in orders]))
    # Insert 'All' at the front for filtering
    statuses.insert(0, 'All')

    # Get filter status from query param
    status_filter = request.args.get('status', 'All')

    if status_filter and status_filter != 'All':
        filtered_orders = [o for o in orders if o['status'].lower() == status_filter.lower() and o['status'].lower() != 'delivered']
    else:
        filtered_orders = [o for o in orders if o['status'].lower() != 'delivered']

    return render_template('active_orders.html', active_orders=filtered_orders, statuses=statuses, status_filter=status_filter)


@app.route('/orders/track/<int:order_id>')
def order_tracking(order_id):
    orders = load_orders()
    deliveries = load_deliveries()
    menus = load_menus()
    order_items = load_order_items()

    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        abort(404)

    delivery_info = next((d for d in deliveries if d['order_id'] == order_id), None)

    # Gather items in the order with details
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if item:
                items.append({
                    'name': item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    order['items'] = items

    return render_template('tracking.html', order=order, delivery_driver=delivery_info, order_items=items)


@app.route('/reviews')
def reviews():
    reviews_list = load_reviews()
    return render_template('reviews.html', reviews=reviews_list)


@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    if request.method == 'GET':
        restaurants = load_restaurants()
        return render_template('write_review.html', restaurants=restaurants, errors=None, previous_input=None)

    # POST - save the review
    restaurant_id = request.form.get('restaurant_id')
    customer_name = request.form.get('customer_name', '').strip()
    rating_raw = request.form.get('rating')
    review_text = request.form.get('review_text', '').strip()
    review_date = request.form.get('review_date', '').strip()

    errors = {}

    # Validate inputs
    try:
        restaurant_id = int(restaurant_id)
    except (TypeError, ValueError):
        errors['restaurant_id'] = 'Invalid restaurant selection.'

    try:
        rating = int(rating_raw)
        if rating < 1 or rating > 5:
            errors['rating'] = 'Rating must be between 1 and 5.'
    except (TypeError, ValueError):
        errors['rating'] = 'Invalid rating value.'

    if not customer_name:
        errors['customer_name'] = 'Your name is required.'
    if not review_text:
        errors['review_text'] = 'Review text is required.'
    if not review_date:
        errors['review_date'] = 'Review date is required.'
    else:
        # Validate review_date format YYYY-MM-DD
        try:
            datetime.strptime(review_date, '%Y-%m-%d')
        except ValueError:
            errors['review_date'] = 'Invalid date format. Use YYYY-MM-DD.'

    if errors:
        restaurants = load_restaurants()
        return render_template('write_review.html', restaurants=restaurants, errors=errors, previous_input=request.form)

    # Determine new review_id
    reviews = load_reviews()
    new_review_id = max([r['review_id'] for r in reviews], default=0) + 1

    new_line = f"{new_review_id}|{restaurant_id}|{customer_name}|{rating}|{review_text}|{review_date}\n"

    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a', encoding='utf-8') as f:
            f.write(new_line)
    except (IOError, OSError):
        abort(500, description='Failed to save review')

    return redirect(url_for('reviews'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
