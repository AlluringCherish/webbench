from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# --- Helper functions to load data from files ---

def load_restaurants():
    restaurants = []
    try:
        with open(os.path.join(data_dir, 'restaurants.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                record = {
                    'restaurant_id': int(parts[0]),
                    'name': parts[1],
                    'cuisine': parts[2],
                    'address': parts[3],
                    'phone': parts[4],
                    'rating': float(parts[5]),
                    'delivery_time': int(parts[6]),
                    'min_order': float(parts[7])
                }
                restaurants.append(record)
    except FileNotFoundError:
        pass
    return restaurants


def load_menus():
    menu_items = []
    try:
        with open(os.path.join(data_dir, 'menus.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                record = {
                    'item_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'item_name': parts[2],
                    'category': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': int(parts[6])
                }
                menu_items.append(record)
    except FileNotFoundError:
        pass
    return menu_items


def load_cart():
    cart_items = []
    try:
        with open(os.path.join(data_dir, 'cart.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                record = {
                    'cart_id': int(parts[0]),
                    'item_id': int(parts[1]),
                    'restaurant_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'added_date': parts[4]
                }
                cart_items.append(record)
    except FileNotFoundError:
        pass
    return cart_items


def save_cart(cart_items):
    try:
        with open(os.path.join(data_dir, 'cart.txt'), 'w', encoding='utf-8') as f:
            for c in cart_items:
                line = f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n"
                f.write(line)
    except:
        pass


def load_orders():
    orders = []
    try:
        with open(os.path.join(data_dir, 'orders.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                record = {
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'restaurant_id': int(parts[2]),
                    'order_date': parts[3],
                    'total_amount': float(parts[4]),
                    'status': parts[5],
                    'delivery_address': parts[6],
                    'phone_number': parts[7]
                }
                orders.append(record)
    except FileNotFoundError:
        pass
    return orders


def load_order_items():
    order_items = []
    try:
        with open(os.path.join(data_dir, 'order_items.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                record = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'item_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(record)
    except FileNotFoundError:
        pass
    return order_items


def load_deliveries():
    deliveries = []
    try:
        with open(os.path.join(data_dir, 'deliveries.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                record = {
                    'delivery_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'driver_name': parts[2],
                    'driver_phone': parts[3],
                    'vehicle_info': parts[4],
                    'status': parts[5],
                    'estimated_time': parts[6]
                }
                deliveries.append(record)
    except FileNotFoundError:
        pass
    return deliveries


def load_reviews():
    reviews = []
    try:
        with open(os.path.join(data_dir, 'reviews.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                record = {
                    'review_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews.append(record)
    except FileNotFoundError:
        pass
    return reviews


def next_cart_id(cart_items):
    if not cart_items:
        return 1
    return max(c['cart_id'] for c in cart_items) + 1

def next_review_id(reviews):
    if not reviews:
        return 1
    return max(r['review_id'] for r in reviews) + 1

def next_order_id(orders):
    if not orders:
        return 1
    return max(o['order_id'] for o in orders) + 1

# --- Routes Implementation ---

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # Show featured restaurants: Let's take top 5 rated restaurants
    restaurants = load_restaurants()
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:5]
    # context: featured_restaurants: list of dict with (restaurant_id, name, cuisine, rating)
    featured_restaurants = [{
        'restaurant_id': r['restaurant_id'],
        'name': r['name'],
        'cuisine': r['cuisine'],
        'rating': r['rating']
    } for r in featured_restaurants]
    return render_template('dashboard.html', featured_restaurants=featured_restaurants)


@app.route('/restaurants')
def restaurants_page():
    restaurants = load_restaurants()
    # context: restaurants: list of dict with (restaurant_id, name, cuisine, rating, delivery_time)
    restaurants_view = [{
        'restaurant_id': r['restaurant_id'],
        'name': r['name'],
        'cuisine': r['cuisine'],
        'rating': r['rating'],
        'delivery_time': r['delivery_time']
    } for r in restaurants]
    return render_template('restaurants.html', restaurants=restaurants_view)


@app.route('/menu/<int:restaurant_id>')
def restaurant_menu_page(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()
    # Find restaurant by id
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        abort(404)
    # Find menu items for this restaurant
    menu_items = [
        {
            'item_id': m['item_id'],
            'item_name': m['item_name'],
            'category': m['category'],
            'description': m['description'],
            'price': m['price'],
            'availability': m['availability']
        }
        for m in menus if m['restaurant_id'] == restaurant_id
    ]
    # context: restaurant with keys (restaurant_id, name, address, phone, rating, delivery_time)
    # context: menu_items list of dicts
    restaurant_info = {
        'restaurant_id': restaurant['restaurant_id'],
        'name': restaurant['name'],
        'address': restaurant['address'],
        'phone': restaurant['phone'],
        'rating': restaurant['rating'],
        'delivery_time': restaurant['delivery_time']
    }
    return render_template('menu.html', restaurant=restaurant_info, menu_items=menu_items)


@app.route('/item/<int:item_id>')
def item_details_page(item_id):
    menus = load_menus()
    # Find item by id
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item:
        abort(404)
    # Ingredients field is optional, but not in schema, so assume no ingredients data
    item_data = {
        'item_id': item['item_id'],
        'item_name': item['item_name'],
        'description': item['description'],
        'price': item['price'],
        # 'ingredients': None  # No ingredients data provided in schema
    }
    return render_template('item_details.html', item=item_data, item_id=item_id)


@app.route('/cart')
def shopping_cart_page():
    cart_items_data = load_cart()
    menus = load_menus()
    # Build cart_items list with keys (item_id, item_name, quantity, price, subtotal)
    cart_items = []
    for c in cart_items_data:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            quantity = c['quantity']
            price = menu_item['price']
            subtotal = quantity * price
            cart_items.append({
                'item_id': menu_item['item_id'],
                'item_name': menu_item['item_name'],
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })
    return render_template('cart.html', cart_items=cart_items)


@app.route('/cart/update', methods=['POST'])
def update_cart():
    # Update cart quantities from form data
    cart_items_data = load_cart()
    menus = load_menus()
    updated_quantities = {}
    for key, value in request.form.items():
        if key.startswith('quantity-'):
            try:
                item_id = int(key.split('-')[1])
                quantity = int(value)
                if quantity < 0:
                    quantity = 0
                updated_quantities[item_id] = quantity
            except:
                continue
    # Update cart items quantities accordingly
    updated_cart = []
    for c in cart_items_data:
        item_id = c['item_id']
        if item_id in updated_quantities:
            new_qty = updated_quantities[item_id]
            if new_qty > 0:
                c['quantity'] = new_qty
                updated_cart.append(c)
            # else quantity=0 means remove the item from cart
        else:
            updated_cart.append(c)

    save_cart(updated_cart)
    return redirect(url_for('shopping_cart_page'))


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    cart_items_data = load_cart()
    # Remove item with matching item_id
    updated_cart = [c for c in cart_items_data if c['item_id'] != item_id]
    save_cart(updated_cart)
    return redirect(url_for('shopping_cart_page'))


@app.route('/checkout')
def checkout_page():
    # Display checkout form
    return render_template('checkout.html')


@app.route('/checkout/place_order', methods=['POST'])
def place_order():
    # Place order from form data
    customer_name = request.form.get('customer_name', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    payment_method = request.form.get('payment_method', '').strip()

    if not customer_name or not delivery_address or not phone_number or not payment_method:
        # Missing fields, reject with 400
        abort(400)

    cart_items_data = load_cart()
    menus = load_menus()
    if not cart_items_data:
        # Cart empty
        abort(400)

    # Calculate total amount
    total_amount = 0.0
    for c in cart_items_data:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            total_amount += c['quantity'] * menu_item['price']

    # Generate new order_id
    orders = load_orders()
    new_order_id = next_order_id(orders)
    order_date = datetime.now().strftime('%Y-%m-%d')

    # Create new order record
    new_order = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'restaurant_id': None,  # Determine later (multiple restaurants in cart could be problem, assume first one)
        'order_date': order_date,
        'total_amount': total_amount,
        'status': 'Processing',
        'delivery_address': delivery_address,
        'phone_number': phone_number
    }

    # Set restaurant_id to the restaurant_id of first cart item if any
    if cart_items_data:
        new_order['restaurant_id'] = cart_items_data[0]['restaurant_id']

    # Append new order to orders.txt
    try:
        with open(os.path.join(data_dir, 'orders.txt'), 'a', encoding='utf-8') as f:
            line = f"{new_order['order_id']}|{new_order['customer_name']}|{new_order['restaurant_id']}|{new_order['order_date']}|{new_order['total_amount']:.2f}|{new_order['status']}|{new_order['delivery_address']}|{new_order['phone_number']}\n"
            f.write(line)
    except:
        abort(500)

    # Save order items to order_items.txt
    order_items = load_order_items()
    next_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1

    try:
        with open(os.path.join(data_dir, 'order_items.txt'), 'a', encoding='utf-8') as f:
            for c in cart_items_data:
                menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
                if menu_item:
                    line = f"{next_order_item_id}|{new_order_id}|{c['item_id']}|{c['quantity']}|{menu_item['price']:.2f}\n"
                    f.write(line)
                    next_order_item_id += 1
    except:
        abort(500)

    # Clear cart since order placed
    try:
        with open(os.path.join(data_dir, 'cart.txt'), 'w', encoding='utf-8') as f:
            f.write('')
    except:
        abort(500)

    return redirect(url_for('checkout_page'))


@app.route('/orders/active')
def active_orders_page():
    orders = load_orders()
    restaurants = load_restaurants()
    deliveries = load_deliveries()
    # Active orders: filter statuses that are not Delivered or Cancelled (assuming these means inactive)
    active_statuses = {'Processing', 'On the Way', 'Preparing'}
    active_orders_raw = [o for o in orders if o['status'] in active_statuses]
    active_orders = []
    for o in active_orders_raw:
        restaurant_name = next((r['name'] for r in restaurants if r['restaurant_id'] == o['restaurant_id']), 'Unknown')
        delivery = next((d for d in deliveries if d['order_id'] == o['order_id']), None)
        eta = delivery['estimated_time'] if delivery else 'N/A'
        active_orders.append({
            'order_id': o['order_id'],
            'restaurant': restaurant_name,
            'status': o['status'],
            'eta': eta
        })
    return render_template('active_orders.html', active_orders=active_orders)


@app.route('/orders/track/<int:order_id>')
def order_tracking_page(order_id):
    orders = load_orders()
    deliveries = load_deliveries()
    order_items_all = load_order_items()
    menus = load_menus()

    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        abort(404)

    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)

    # Compose context: order_details
    order_details = {
        'order_id': order['order_id'],
        'customer_name': order['customer_name'],
        'restaurant_id': order['restaurant_id'],
        'order_date': order['order_date'],
        'total_amount': order['total_amount'],
        'status': order['status'],
        'delivery_address': order['delivery_address'],
        'phone_number': order['phone_number']
    }

    delivery_info = {
        'driver_name': delivery['driver_name'] if delivery else '',
        'driver_phone': delivery['driver_phone'] if delivery else '',
        'vehicle_info': delivery['vehicle_info'] if delivery else '',
        'status': delivery['status'] if delivery else '',
        'estimated_time': delivery['estimated_time'] if delivery else ''
    }

    order_items = []
    # Fetch order items for this order
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                order_items.append({
                    'item_id': menu_item['item_id'],
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    return render_template('track_order.html', order_details=order_details, delivery_info=delivery_info, order_items=order_items, order_id=order_id)


@app.route('/reviews')
def reviews_page():
    reviews = load_reviews()
    restaurants = load_restaurants()
    # Compose reviews with restaurant_name included
    reviews_view = []
    rest_map = {r['restaurant_id']: r['name'] for r in restaurants}
    for r in reviews:
        restaurant_name = rest_map.get(r['restaurant_id'], 'Unknown')
        reviews_view.append({
            'review_id': r['review_id'],
            'restaurant_name': restaurant_name,
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })
    return render_template('reviews.html', reviews=reviews_view)


@app.route('/reviews/write')
def write_review_page():
    # Provide list of restaurants with only restaurant_id and name
    restaurants = load_restaurants()
    rest_simple = [{'restaurant_id': r['restaurant_id'], 'name': r['name']} for r in restaurants]
    return render_template('write_review.html', restaurants=rest_simple)


@app.route('/reviews/submit', methods=['POST'])
def submit_review():
    restaurant_id_str = request.form.get('restaurant_id', '').strip()
    customer_name = request.form.get('customer_name', '').strip()
    rating_str = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()

    # Validate inputs
    try:
        restaurant_id = int(restaurant_id_str)
        rating = int(rating_str)
    except:
        abort(400)
    if not customer_name or rating < 1 or rating > 5 or not review_text:
        abort(400)

    reviews = load_reviews()
    new_review_id = next_review_id(reviews)
    review_date = datetime.now().strftime('%Y-%m-%d')

    # Append new review to reviews.txt
    try:
        with open(os.path.join(data_dir, 'reviews.txt'), 'a', encoding='utf-8') as f:
            line = f"{new_review_id}|{restaurant_id}|{customer_name}|{rating}|{review_text}|{review_date}\n"
            f.write(line)
    except:
        abort(500)

    return redirect(url_for('reviews_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
