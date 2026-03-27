from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data

def load_restaurants():
    filepath = os.path.join(DATA_DIR, 'restaurants.txt')
    restaurants = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
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
        restaurants = []
    return restaurants


def load_menus():
    filepath = os.path.join(DATA_DIR, 'menus.txt')
    menus = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                menu_item = {
                    'item_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'item_name': parts[2],
                    'category': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': int(parts[6])
                }
                menus.append(menu_item)
    except Exception:
        menus = []
    return menus


def load_cart():
    filepath = os.path.join(DATA_DIR, 'cart.txt')
    cart_items = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                cart_item = {
                    'cart_id': int(parts[0]),
                    'item_id': int(parts[1]),
                    'restaurant_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'added_date': parts[4]
                }
                cart_items.append(cart_item)
    except Exception:
        cart_items = []
    return cart_items


def load_orders():
    filepath = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
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
    except Exception:
        orders = []
    return orders


def load_order_items():
    filepath = os.path.join(DATA_DIR, 'order_items.txt')
    order_items = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                order_item = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'item_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(order_item)
    except Exception:
        order_items = []
    return order_items


def load_deliveries():
    filepath = os.path.join(DATA_DIR, 'deliveries.txt')
    deliveries = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
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
    except Exception:
        deliveries = []
    return deliveries


def load_reviews():
    filepath = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                review = {
                    'review_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews.append(review)
    except Exception:
        reviews = []
    return reviews


# Flask Routes Implementation

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    sorted_by_rating = sorted(restaurants, key=lambda r: r['rating'], reverse=True)
    featured_restaurants = sorted_by_rating[:4] if len(sorted_by_rating) >= 4 else sorted_by_rating

    cuisine_counts = {}
    for r in restaurants:
        cuisine_counts[r['cuisine']] = cuisine_counts.get(r['cuisine'], 0) + 1
    popular_cuisines = [c for c, _ in sorted(cuisine_counts.items(), key=lambda x: (-x[1], x[0]))]

    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=popular_cuisines)


@app.route('/restaurants')
def browse_restaurants():
    restaurants = load_restaurants()
    cuisine_options = sorted(set(r['cuisine'] for r in restaurants))
    return render_template('restaurants.html', restaurants=restaurants, cuisine_options=cuisine_options)


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


@app.route('/cart')
def view_cart():
    cart_items = load_cart()
    menus = load_menus()
    menu_dict = {m['item_id']: m for m in menus}
    detailed_cart_items = []
    total_amount = 0.0
    for ci in cart_items:
        item = menu_dict.get(ci['item_id'])
        if not item:
            continue
        total_amount += item['price'] * ci['quantity']
        detailed_cart_items.append({
            'cart_id': ci['cart_id'],
            'item_id': ci['item_id'],
            'restaurant_id': ci['restaurant_id'],
            'quantity': ci['quantity'],
            'item_name': item['item_name'],
            'price': item['price'],
            'total_price': item['price'] * ci['quantity']
        })
    return render_template('cart.html', cart_items=detailed_cart_items, total_amount=total_amount)


@app.route('/cart/update', methods=['POST'])
def update_cart():
    cart_items = load_cart()
    cart_dict = {ci['cart_id']: ci for ci in cart_items}
    # Update quantities
    for key in request.form:
        if key.startswith('quantity_'):
            try:
                cart_id = int(key.split('_')[1])
                if cart_id in cart_dict:
                    qty_str = request.form.get(key, '0')
                    quantity = int(qty_str) if qty_str.isdigit() else 0
                    if quantity < 0:
                        quantity = 0
                    cart_dict[cart_id]['quantity'] = quantity
            except Exception:
                continue
        elif key.startswith('remove_'):
            try:
                cart_id = int(key.split('_')[1])
                if cart_id in cart_dict:
                    cart_dict[cart_id]['quantity'] = 0
            except Exception:
                continue
    # Remove items with quantity zero
    new_cart_items = [ci for ci in cart_dict.values() if ci['quantity'] > 0]
    filepath = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            for ci in new_cart_items:
                line = f"{ci['cart_id']}|{ci['item_id']}|{ci['restaurant_id']}|{ci['quantity']}|{ci['added_date']}\n"
                f.write(line)
    except Exception:
        pass
    return redirect(url_for('view_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        return render_template('checkout.html')

    customer_name = request.form.get('customer_name', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    payment_method = request.form.get('payment_method', '').strip()

    if not all([customer_name, delivery_address, phone_number, payment_method]):
        return render_template('checkout.html', order_confirmation=None)

    cart_items = load_cart()
    if not cart_items:
        return render_template('checkout.html', order_confirmation=None)

    menus = load_menus()
    menu_dict = {m['item_id']: m for m in menus}

    total_amount = 0.0
    restaurant_ids = set()
    for ci in cart_items:
        item = menu_dict.get(ci['item_id'])
        if not item or item['availability'] != 1:
            continue
        total_amount += item['price'] * ci['quantity']
        restaurant_ids.add(ci['restaurant_id'])

    if len(restaurant_ids) != 1:
        return render_template('checkout.html', order_confirmation=None)

    restaurant_id = restaurant_ids.pop()

    orders = load_orders()
    max_order_id = max((o['order_id'] for o in orders), default=0)
    new_order_id = max_order_id + 1

    order_date = datetime.now().strftime('%Y-%m-%d')
    order_line = f"{new_order_id}|{customer_name}|{restaurant_id}|{order_date}|{total_amount:.2f}|Pending|{delivery_address}|{phone_number}\n"

    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'a', encoding='utf-8') as f:
            f.write(order_line)
    except Exception:
        return render_template('checkout.html', order_confirmation=None)

    order_items = load_order_items()
    max_order_item_id = max((oi['order_item_id'] for oi in order_items), default=0)
    current_order_item_id = max_order_item_id + 1

    order_items_data = []
    for ci in cart_items:
        item = menu_dict.get(ci['item_id'])
        if not item or item['availability'] != 1:
            continue
        line = f"{current_order_item_id}|{new_order_id}|{ci['item_id']}|{ci['quantity']}|{item['price']:.2f}\n"
        order_items_data.append(line)
        current_order_item_id += 1

    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'a', encoding='utf-8') as f:
            f.writelines(order_items_data)
    except Exception:
        return render_template('checkout.html', order_confirmation=None)

    try:
        open(os.path.join(DATA_DIR, 'cart.txt'), 'w').close()
    except Exception:
        pass

    order_confirmation = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'restaurant_id': restaurant_id,
        'order_date': order_date,
        'total_amount': total_amount,
        'status': 'Pending',
        'delivery_address': delivery_address,
        'phone_number': phone_number
    }

    return render_template('checkout.html', order_confirmation=order_confirmation)


@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    active_orders = [o for o in orders if o['status'].lower() not in ['delivered', 'cancelled']]
    status_options = sorted(set(o['status'] for o in active_orders))
    return render_template('active_orders.html', active_orders=active_orders, status_options=status_options)


@app.route('/orders/track/<int:order_id>')
def track_order(order_id):
    orders = load_orders()
    deliveries = load_deliveries()
    order_items = load_order_items()
    menus = load_menus()

    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        abort(404)

    delivery_info = next((d for d in deliveries if d['order_id'] == order_id), None) or {}

    order_items_list = [oi for oi in order_items if oi['order_id'] == order_id]
    item_map = {m['item_id']: m for m in menus}

    detailed_items = []
    for oi in order_items_list:
        item = item_map.get(oi['item_id'])
        if item:
            detailed_items.append({
                'order_item_id': oi['order_item_id'],
                'item_id': oi['item_id'],
                'item_name': item['item_name'],
                'quantity': oi['quantity'],
                'price': oi['price']
            })

    return render_template('track_order.html', order=order, delivery_info=delivery_info, order_items=detailed_items)


@app.route('/reviews')
def reviews():
    reviews_data = load_reviews()
    rating_filter_options = sorted(set(r['rating'] for r in reviews_data))
    return render_template('reviews.html', reviews=reviews_data, rating_filter_options=rating_filter_options)


@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    submission_status = None
    restaurants = load_restaurants()
    if request.method == 'POST':
        try:
            restaurant_id = int(request.form.get('restaurant_id', '0'))
        except:
            restaurant_id = 0
        customer_name = request.form.get('customer_name', '').strip()
        try:
            rating = int(request.form.get('rating', '0'))
        except:
            rating = 0
        review_text = request.form.get('review_text', '').strip()

        if (restaurant_id <= 0 or not any(r['restaurant_id'] == restaurant_id for r in restaurants) or
            not customer_name or not review_text or rating < 1 or rating > 5):
            submission_status = False
        else:
            reviews = load_reviews()
            max_review_id = max((r['review_id'] for r in reviews), default=0)
            new_review_id = max_review_id + 1
            review_date = datetime.now().strftime('%Y-%m-%d')
            review_line = f"{new_review_id}|{restaurant_id}|{customer_name}|{rating}|{review_text}|{review_date}\n"
            try:
                with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a', encoding='utf-8') as f:
                    f.write(review_line)
                submission_status = True
            except Exception:
                submission_status = False
    return render_template('write_review.html', submission_status=submission_status, restaurants=restaurants)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
