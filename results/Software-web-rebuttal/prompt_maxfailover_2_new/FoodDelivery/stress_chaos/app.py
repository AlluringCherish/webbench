from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime, date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data from pipe delimited files

def load_restaurants():
    restaurants = []
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
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
                except Exception:
                    continue
    except IOError:
        # Could not read file
        return []
    return restaurants


def load_menus():
    menus = []
    path = os.path.join(DATA_DIR, 'menus.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                try:
                    item = {
                        'item_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
                        'item_name': parts[2],
                        'category': parts[3],
                        'description': parts[4],
                        'price': float(parts[5]),
                        'availability': int(parts[6])
                    }
                    # Add empty ingredients string to accommodate template expectation
                    item['ingredients'] = ''
                    menus.append(item)
                except Exception:
                    continue
    except IOError:
        return []
    return menus


def load_cart():
    cart_items = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                try:
                    cart_item = {
                        'cart_id': int(parts[0]),
                        'item_id': int(parts[1]),
                        'restaurant_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'added_date': parts[4]  # string date
                    }
                    cart_items.append(cart_item)
                except Exception:
                    continue
    except IOError:
        return []
    return cart_items


def load_orders():
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                try:
                    order = {
                        'order_id': int(parts[0]),
                        'customer_name': parts[1],
                        'restaurant_id': int(parts[2]),
                        'order_date': parts[3],  # string date
                        'total_amount': float(parts[4]),
                        'status': parts[5],
                        'delivery_address': parts[6],
                        'phone_number': parts[7],
                    }
                    orders.append(order)
                except Exception:
                    continue
    except IOError:
        return []
    return orders


def load_order_items():
    order_items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                try:
                    oi = {
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'item_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    }
                    order_items.append(oi)
                except Exception:
                    continue
    except IOError:
        return []
    return order_items


def load_deliveries():
    deliveries = []
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                try:
                    delivery = {
                        'delivery_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'driver_name': parts[2],
                        'driver_phone': parts[3],
                        'vehicle_info': parts[4],
                        'status': parts[5],
                        'estimated_time': parts[6]  # datetime string
                    }
                    deliveries.append(delivery)
                except Exception:
                    continue
    except IOError:
        return []
    return deliveries


def load_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                try:
                    review = {
                        'review_id': int(parts[0]),
                        'restaurant_id': int(parts[1]),
                        'customer_name': parts[2],
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5],
                    }
                    reviews.append(review)
                except Exception:
                    continue
    except IOError:
        return []
    return reviews


# Save cart data back to file
# We will overwrite entire cart.txt with updated content

def save_cart(cart_items):
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = f"{item['cart_id']}|{item['item_id']}|{item['restaurant_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
        return True
    except IOError:
        return False


# Save review
# We append new review to reviews.txt

def save_review(review):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        last_id = 0
        # Read last review_id
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts and parts[0].isdigit():
                    last_id = max(last_id, int(parts[0]))
    except IOError:
        # If file not found, will create new
        last_id = 0
    review_id = last_id + 1
    try:
        with open(path, 'a', encoding='utf-8') as f:
            line = f"{review_id}|{review['restaurant_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}\n"
            f.write(line)
        return True
    except IOError:
        return False


# Generate new cart_id

def get_next_cart_id(cart_items):
    if not cart_items:
        return 1
    return max(item['cart_id'] for item in cart_items) + 1


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    restaurants = load_restaurants()
    menus = load_menus()
    # Featured restaurants - choose top 5 by rating
    sorted_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)
    featured_restaurants = sorted_restaurants[:5]
    # Popular cuisines from all restaurants - unique sorted list
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    popular_cuisines = cuisines
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
    return render_template('restaurant_menu.html', restaurant=restaurant, menu_items=menu_items)


@app.route('/item/<int:item_id>')
def item_details_page(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability'] == 1), None)
    if not item:
        abort(404)
    quantity = 1
    return render_template('item_details.html', item=item, quantity=quantity)


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_items = load_cart()
    menus = load_menus()
    # Join cart items with menu item details
    detailed_cart_items = []
    for c in cart_items:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            item_detail = {
                'cart_id': c['cart_id'],
                'item_id': c['item_id'],
                'restaurant_id': c['restaurant_id'],
                'quantity': c['quantity'],
                'added_date': c['added_date'],
                'item_name': menu_item['item_name'],
                'price': menu_item['price']
            }
            detailed_cart_items.append(item_detail)

    if request.method == 'POST':
        # Update cart quantities or remove items
        # Expect form keys like quantity_<cart_id> or remove_<cart_id>
        updated_cart = []
        for item in detailed_cart_items:
            cart_id = item['cart_id']
            remove_flag = request.form.get(f'remove_{cart_id}')
            if remove_flag:
                # Skip this item (remove it)
                continue
            quantity_str = request.form.get(f'quantity_{cart_id}')
            try:
                quantity = int(quantity_str) if quantity_str else item['quantity']
                if quantity < 1:
                    continue  # skip item if invalid quantity
            except Exception:
                quantity = item['quantity']
            updated_cart.append({
                'cart_id': cart_id,
                'item_id': item['item_id'],
                'restaurant_id': item['restaurant_id'],
                'quantity': quantity,
                'added_date': item['added_date']
            })
        save_cart(updated_cart)
        
        # Refresh detailed cart items after save
        cart_items = load_cart()
        detailed_cart_items = []
        for c in cart_items:
            menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
            if menu_item:
                item_detail = {
                    'cart_id': c['cart_id'],
                    'item_id': c['item_id'],
                    'restaurant_id': c['restaurant_id'],
                    'quantity': c['quantity'],
                    'added_date': c['added_date'],
                    'item_name': menu_item['item_name'],
                    'price': menu_item['price']
                }
                detailed_cart_items.append(item_detail)

    total_amount = sum(item['price'] * item['quantity'] for item in detailed_cart_items)
    return render_template('cart.html', cart_items=detailed_cart_items, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    if request.method == 'GET':
        return render_template('checkout.html')
    # POST: create order after validating form data
    customer_name = request.form.get('customer_name', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    payment_method = request.form.get('payment_method', '').strip()

    if not customer_name or not delivery_address or not phone_number or payment_method not in ['Credit Card', 'Cash', 'PayPal']:
        # Invalid data, re-render page with error (could pass error message, but spec doesn't require)
        return render_template('checkout.html'), 400

    # Load cart
    cart_items = load_cart()
    if not cart_items:
        # No items in cart, cannot place order
        return render_template('checkout.html'), 400

    menus = load_menus()
    restaurants = load_restaurants()

    # Calculate total amount
    total_amount = 0.0
    # Also ensure all cart items are still available
    for c in cart_items:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id'] and m['availability'] == 1), None)
        if not menu_item:
            return render_template('checkout.html'), 400
        total_amount += menu_item['price'] * c['quantity']

    # Check restaurant_id consistency - all items must be from the same restaurant (since cart.txt has restaurant_id per item, we allow multiple? But design may need same restaurant order)
    restaurant_ids = set(c['restaurant_id'] for c in cart_items)
    if len(restaurant_ids) != 1:
        # Multiple restaurants in cart not allowed for single order
        return render_template('checkout.html'), 400

    restaurant_id = restaurant_ids.pop()

    # Load existing orders to get next order_id
    orders = load_orders()
    next_order_id = max((order['order_id'] for order in orders), default=0) + 1

    # Save new order
    order_date_str = date.today().strftime('%Y-%m-%d')

    # Append order to orders.txt
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'a', encoding='utf-8') as f:
            line = f"{next_order_id}|{customer_name}|{restaurant_id}|{order_date_str}|{total_amount:.2f}|Preparing|{delivery_address}|{phone_number}\n"
            f.write(line)
    except IOError:
        return render_template('checkout.html'), 500

    # Save order items to order_items.txt
    order_items = load_order_items()
    next_order_item_id = max((oi['order_item_id'] for oi in order_items), default=0) + 1
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'a', encoding='utf-8') as f:
            for c in cart_items:
                menu_item = next(m for m in menus if m['item_id'] == c['item_id'])
                line = f"{next_order_item_id}|{next_order_id}|{c['item_id']}|{c['quantity']}|{menu_item['price']:.2f}\n"
                f.write(line)
                next_order_item_id += 1
    except IOError:
        return render_template('checkout.html'), 500

    # Clear cart after order placed
    try:
        open(os.path.join(DATA_DIR, 'cart.txt'), 'w').close()
    except IOError:
        pass

    return redirect(url_for('active_orders'))


@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    # Harmonize status options
    # Backend status values are 'Preparing', 'On the Way', 'Delivered'
    # UI should show 'Preparing', 'On the Way' (same wording as backend), 'Delivered'
    # Active orders are 'Preparing' and 'On the Way'
    active_statuses = {'Preparing', 'On the Way'}
    active_orders = [o for o in orders if o['status'] in active_statuses]
    return render_template('active_orders.html', active_orders=active_orders)


@app.route('/orders/track/<int:order_id>')
def order_tracking(order_id):
    orders = load_orders()
    order_details = next((o for o in orders if o['order_id'] == order_id), None)
    if not order_details:
        abort(404)

    deliveries = load_deliveries()
    delivery_driver = next((d for d in deliveries if d['order_id'] == order_id), None)
    order_items_all = load_order_items()
    menus = load_menus()
    order_items = []
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                order_items.append({
                    'order_item_id': oi['order_item_id'],
                    'item_id': oi['item_id'],
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    # estimated_time from delivery_driver (may be missing)
    estimated_time = delivery_driver['estimated_time'] if delivery_driver else None

    return render_template('order_tracking.html', order_details=order_details, delivery_driver=delivery_driver, estimated_time=estimated_time, order_items=order_items)


@app.route('/reviews')
def reviews_page():
    reviews = load_reviews()
    filter_options = ['All', '5 stars', '4 stars', '3 stars', '2 stars', '1 star']
    return render_template('reviews.html', reviews=reviews, filter_options=filter_options)


@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review_page():
    if request.method == 'GET':
        return render_template('write_review.html')

    # POST: collect review data
    try:
        restaurant_id = int(request.form.get('restaurant_id', '').strip())
        customer_name = request.form.get('customer_name', '').strip()
        rating = int(request.form.get('rating', '').strip())
        review_text = request.form.get('review_text', '').strip()
    except Exception:
        return render_template('write_review.html'), 400

    # Validate
    if (not customer_name or not review_text or rating < 1 or rating > 5):
        return render_template('write_review.html'), 400

    # To check valid restaurant_id
    restaurants = load_restaurants()
    if not any(r['restaurant_id'] == restaurant_id for r in restaurants):
        return render_template('write_review.html'), 400

    # Prepare review data
    review_date = date.today().strftime('%Y-%m-%d')
    review = {
        'restaurant_id': restaurant_id,
        'customer_name': customer_name,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date
    }

    success = save_review(review)
    if not success:
        return render_template('write_review.html'), 500

    return redirect(url_for('reviews_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
