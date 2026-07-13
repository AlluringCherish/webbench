from flask import Flask, request, jsonify, abort
from datetime import datetime, date
import os

app = Flask(__name__)
DATA_DIR = 'data'

# Helper Functions to read/write data files

def read_file_to_dict(filename, key_field_index=0, delimiter='|'):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return {}
    data = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(delimiter)
            key = int(parts[key_field_index])
            data[key] = parts
    return data


def write_file_from_dict(filename, data_dict, delimiter='|'):
    path = os.path.join(DATA_DIR, filename)
    lines = []
    for key in sorted(data_dict.keys()):
        line = delimiter.join(str(field) for field in data_dict[key])
        lines.append(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def append_line_to_file(filename, line, delimiter='|'):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def parse_restaurant(line):
    # 1|Dragon House|Chinese|123 Main St|555-0001|4.5|30|15.00
    parts = line.strip().split('|')
    return {
        'id': int(parts[0]),
        'name': parts[1],
        'cuisine': parts[2],
        'address': parts[3],
        'phone': parts[4],
        'rating': float(parts[5]),
        'delivery_time': int(parts[6]),
        'min_order': float(parts[7])
    }


def parse_menu(line):
    # 1|1|Fried Rice|Main Course|Steamed rice with vegetables and egg|12.99|1
    parts = line.strip().split('|')
    return {
        'item_id': int(parts[0]),
        'restaurant_id': int(parts[1]),
        'item_name': parts[2],
        'category': parts[3],
        'description': parts[4],
        'price': float(parts[5]),
        'availability': bool(int(parts[6]))
    }


def parse_cart(line):
    # 1|1|1|2|2025-01-15
    parts = line.strip().split('|')
    return {
        'cart_id': int(parts[0]),
        'item_id': int(parts[1]),
        'restaurant_id': int(parts[2]),
        'quantity': int(parts[3]),
        'added_date': parts[4]
    }


def parse_order(line):
    # 1|John Doe|1|2025-01-10|21.98|Delivered|123 Main St, NYC|555-1234
    parts = line.strip().split('|')
    return {
        'order_id': int(parts[0]),
        'customer_name': parts[1],
        'restaurant_id': int(parts[2]),
        'order_date': parts[3],
        'total_amount': float(parts[4]),
        'status': parts[5],
        'delivery_address': parts[6],
        'phone_number': parts[7]
    }


def parse_order_item(line):
    # 1|1|1|2|12.99
    parts = line.strip().split('|')
    return {
        'order_item_id': int(parts[0]),
        'order_id': int(parts[1]),
        'item_id': int(parts[2]),
        'quantity': int(parts[3]),
        'price': float(parts[4])
    }


def parse_delivery(line):
    # 1|1|Mike Johnson|555-9001|Bike|Delivered|2025-01-10 18:45
    parts = line.strip().split('|')
    return {
        'delivery_id': int(parts[0]),
        'order_id': int(parts[1]),
        'driver_name': parts[2],
        'driver_phone': parts[3],
        'vehicle_info': parts[4],
        'status': parts[5],
        'estimated_time': parts[6]
    }


def parse_review(line):
    # 1|1|Alice Johnson|5|Excellent food and fast delivery!|2025-01-12
    parts = line.strip().split('|')
    return {
        'review_id': int(parts[0]),
        'restaurant_id': int(parts[1]),
        'customer_name': parts[2],
        'rating': int(parts[3]),
        'review_text': parts[4],
        'review_date': parts[5]
    }


##### ROUTE HELPERS #####

def load_restaurants():
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    restaurants = []
    if not os.path.exists(path):
        return restaurants
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                restaurants.append(parse_restaurant(line))
    return restaurants


def load_menus():
    path = os.path.join(DATA_DIR, 'menus.txt')
    menus = []
    if not os.path.exists(path):
        return menus
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                menus.append(parse_menu(line))
    return menus


def load_cart():
    path = os.path.join(DATA_DIR, 'cart.txt')
    cart = []
    if not os.path.exists(path):
        return cart
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                cart.append(parse_cart(line))
    return cart


def load_orders():
    path = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                orders.append(parse_order(line))
    return orders


def load_order_items():
    path = os.path.join(DATA_DIR, 'order_items.txt')
    items = []
    if not os.path.exists(path):
        return items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                items.append(parse_order_item(line))
    return items


def load_deliveries():
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    deliveries = []
    if not os.path.exists(path):
        return deliveries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                deliveries.append(parse_delivery(line))
    return deliveries


def load_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                reviews.append(parse_review(line))
    return reviews


##### Utility to generate next IDs for each entity #####
def next_id(items, id_field):
    if not items:
        return 1
    return max(item[id_field] for item in items) + 1


##### ROUTES #####

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    # Retrieve featured restaurants (top 5 by rating descending) and popular cuisines (distinct cuisines sorted by count)
    restaurants = load_restaurants()
    featured = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:5]

    # Compose featured restaurants list with expected fields
    featured_restaurants = [{
        'id': r['id'],
        'name': r['name'],
        'cuisine': r['cuisine'],
        'rating': r['rating'],
        'delivery_time': r['delivery_time'],
        # logo_url is not specified in data, put placeholder or skip
        'logo_url': ''
    } for r in featured]

    # Popular cuisines by count
    cuisine_counts = {}
    for r in restaurants:
        cuisine_counts[r['cuisine']] = cuisine_counts.get(r['cuisine'], 0) + 1
    popular_cuisines = sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)
    popular_cuisines = [c[0] for c in popular_cuisines][:10]

    return jsonify({
        'featured_restaurants': featured_restaurants,
        'popular_cuisines': popular_cuisines
    })


@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    search = request.args.get('search', '').lower()
    cuisine = request.args.get('cuisine', '').lower()
    restaurants = load_restaurants()

    def match_restaurant(r):
        if search:
            if search not in r['name'].lower() and search not in r['cuisine'].lower():
                return False
        if cuisine:
            if cuisine != r['cuisine'].lower():
                return False
        return True

    filtered = [
        {
            'id': r['id'],
            'name': r['name'],
            'cuisine': r['cuisine'],
            'address': r['address'],
            'phone': r['phone'],
            'rating': r['rating'],
            'delivery_time': r['delivery_time'],
            'min_order': r['min_order']
        }
        for r in restaurants if match_restaurant(r)
    ]
    return jsonify(filtered)


@app.route('/api/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_menu_for_restaurant(restaurant_id):
    restaurants = load_restaurants()
    restaurant = next((r for r in restaurants if r['id'] == restaurant_id), None)
    if not restaurant:
        abort(404, description='Restaurant not found')

    menus = load_menus()
    items = [
        {
            'item_id': m['item_id'],
            'name': m['item_name'],
            'category': m['category'],
            'description': m['description'],
            'price': m['price'],
            'availability': m['availability'],
            # photo_url not specified, skipping
        }
        for m in menus if m['restaurant_id'] == restaurant_id
    ]

    restaurant_info = {
        'id': restaurant['id'],
        'name': restaurant['name'],
        'address': restaurant['address'],
        'phone': restaurant['phone'],
        'rating': restaurant['rating']
    }

    return jsonify({
        'restaurant': restaurant_info,
        'menu_items': items
    })


@app.route('/api/menu_items/<int:item_id>', methods=['GET'])
def get_menu_item_details(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item:
        abort(404, description='Menu item not found')

    # Compose item details including description, ingredients (not separately specified, so we include in description), nutritional info (none specified)
    item_details = {
        'id': item['item_id'],
        'name': item['item_name'],
        'description': item['description'],
        'ingredients': '',  # None specified in data
        'price': item['price']
    }
    return jsonify(item_details)


@app.route('/api/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'GET':
        cart_items_data = load_cart()
        menus = load_menus()
        # Build dict for quick menu lookup
        menu_dict = {m['item_id']: m for m in menus}

        cart_items = []
        total_amount = 0.0

        for c in cart_items_data:
            menu_item = menu_dict.get(c['item_id'])
            if not menu_item:
                continue
            subtotal = menu_item['price'] * c['quantity']
            total_amount += subtotal
            cart_items.append({
                'cart_id': c['cart_id'],
                'item_id': c['item_id'],
                'name': menu_item['item_name'],
                'quantity': c['quantity'],
                'price': menu_item['price'],
                'subtotal': subtotal
            })

        return jsonify({
            'cart_items': cart_items,
            'total_amount': round(total_amount, 2)
        })

    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, description='JSON body required')
        item_id = data.get('item_id')
        restaurant_id = data.get('restaurant_id')
        quantity = data.get('quantity')
        if not all([isinstance(item_id, int), isinstance(restaurant_id, int), isinstance(quantity, int)]) or quantity <= 0:
            abort(400, description='Invalid item_id, restaurant_id, or quantity')

        cart_items = load_cart()
        # Check if item already in cart (same item_id and restaurant_id), if yes update quantity
        for c in cart_items:
            if c['item_id'] == item_id and c['restaurant_id'] == restaurant_id:
                c['quantity'] += quantity
                break
        else:
            # Add new cart item
            new_cart_id = next_id(cart_items, 'cart_id')
            added_date = date.today().isoformat()
            cart_items.append({
                'cart_id': new_cart_id,
                'item_id': item_id,
                'restaurant_id': restaurant_id,
                'quantity': quantity,
                'added_date': added_date
            })

        # Write full cart back
        # Convert cart item dicts back to line lists
        lines_dict = {c['cart_id']: [
            str(c['cart_id']),
            str(c['item_id']),
            str(c['restaurant_id']),
            str(c['quantity']),
            c['added_date']
        ] for c in cart_items}
        write_file_from_dict('cart.txt', lines_dict)

        return jsonify({'message': 'Item added/updated to cart', 'cart_id': new_cart_id if 'new_cart_id' in locals() else None})


@app.route('/api/cart/<int:cart_id>', methods=['PUT', 'DELETE'])
def modify_cart_item(cart_id):
    cart_items = load_cart()
    idx = next((i for i, c in enumerate(cart_items) if c['cart_id'] == cart_id), None)
    if idx is None:
        abort(404, description='Cart item not found')

    if request.method == 'PUT':
        data = request.get_json()
        if not data or 'quantity' not in data:
            abort(400, description='Quantity required')
        quantity = data['quantity']
        if not isinstance(quantity, int) or quantity <= 0:
            abort(400, description='Invalid quantity')

        cart_items[idx]['quantity'] = quantity

        # Save back all cart
        lines_dict = {c['cart_id']: [
            str(c['cart_id']),
            str(c['item_id']),
            str(c['restaurant_id']),
            str(c['quantity']),
            c['added_date']
        ] for c in cart_items}
        write_file_from_dict('cart.txt', lines_dict)
        return jsonify({'message': 'Cart item quantity updated'})

    elif request.method == 'DELETE':
        cart_items.pop(idx)
        lines_dict = {c['cart_id']: [
            str(c['cart_id']),
            str(c['item_id']),
            str(c['restaurant_id']),
            str(c['quantity']),
            c['added_date']
        ] for c in cart_items}
        write_file_from_dict('cart.txt', lines_dict)
        return jsonify({'message': 'Cart item removed'})


@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    required_fields = ['customer_name', 'delivery_address', 'phone_number', 'payment_method']
    if not data or not all(field in data for field in required_fields):
        abort(400, description='Missing required order fields')

    customer_name = data['customer_name']
    delivery_address = data['delivery_address']
    phone_number = data['phone_number']
    payment_method = data['payment_method']  # not further processed

    cart_items = load_cart()
    if not cart_items:
        abort(400, description='Cart is empty')

    menus = load_menus()
    menu_dict = {m['item_id']: m for m in menus}
    restaurants = load_restaurants()
    restaurant_dict = {r['id']: r for r in restaurants}

    # Group ordered items by restaurant_id
    order_groups = {}
    for c in cart_items:
        rid = c['restaurant_id']
        if rid not in order_groups:
            order_groups[rid] = []
        menu_item = menu_dict.get(c['item_id'])
        if not menu_item or not menu_item['availability']:
            abort(400, description=f'Item {c["item_id"]} not available')
        order_groups[rid].append(c)

    # Validate minimum order amount for each restaurant
    for rid, items in order_groups.items():
        subtotal = 0.0
        for item in items:
            menu_item = menu_dict[item['item_id']]
            subtotal += menu_item['price'] * item['quantity']
        min_order = restaurant_dict[rid]['min_order']
        if subtotal < min_order:
            abort(400, description=f'Minimum order amount for restaurant id {rid} not met')

    orders = load_orders()
    order_items_db = load_order_items()

    new_order_ids = []

    # Create orders and order_items per restaurant group
    for rid, items in order_groups.items():
        total_amount = 0.0
        for item in items:
            menu_item = menu_dict[item['item_id']]
            total_amount += menu_item['price'] * item['quantity']

        new_order_id = next_id(orders, 'order_id')
        order_date = date.today().isoformat()
        status = 'Preparing'

        # Append to orders list
        orders.append({
            'order_id': new_order_id,
            'customer_name': customer_name,
            'restaurant_id': rid,
            'order_date': order_date,
            'total_amount': round(total_amount, 2),
            'status': status,
            'delivery_address': delivery_address,
            'phone_number': phone_number
        })
        # Add order items
        for item in items:
            order_item_id = next_id(order_items_db, 'order_item_id')
            menu_item = menu_dict[item['item_id']]
            order_items_db.append({
                'order_item_id': order_item_id,
                'order_id': new_order_id,
                'item_id': item['item_id'],
                'quantity': item['quantity'],
                'price': menu_item['price']
            })

        new_order_ids.append(new_order_id)

    # Write back orders and order_items
    orders_lines_dict = {o['order_id']: [
        str(o['order_id']),
        o['customer_name'],
        str(o['restaurant_id']),
        o['order_date'],
        f"{o['total_amount']:.2f}",
        o['status'],
        o['delivery_address'],
        o['phone_number']
    ] for o in orders}
    write_file_from_dict('orders.txt', orders_lines_dict)

    order_items_lines_dict = {oi['order_item_id']: [
        str(oi['order_item_id']),
        str(oi['order_id']),
        str(oi['item_id']),
        str(oi['quantity']),
        f"{oi['price']:.2f}"
    ] for oi in order_items_db}
    write_file_from_dict('order_items.txt', order_items_lines_dict)

    # Clear cart after placing order
    if os.path.exists(os.path.join(DATA_DIR, 'cart.txt')):
        open(os.path.join(DATA_DIR, 'cart.txt'), 'w').close()

    # Return one order ID for response (if multiple orders created, we return ids list as a string)
    if len(new_order_ids) == 1:
        return jsonify({'order_id': new_order_ids[0], 'status': 'Order placed successfully'})
    else:
        return jsonify({'order_ids': new_order_ids, 'status': 'Orders placed successfully'})


@app.route('/api/orders/active', methods=['GET'])
def get_active_orders():
    status_filter = request.args.get('status', 'All')

    orders = load_orders()
    restaurants = load_restaurants()
    restaurant_dict = {r['id']: r for r in restaurants}

    deliveries = load_deliveries()
    delivery_dict = {d['order_id']: d for d in deliveries}

    # Filter orders
    filtered_orders = []
    for o in orders:
        if o['status'] == 'Delivered':
            continue
        if status_filter != 'All' and status_filter != '':
            if o['status'] != status_filter:
                continue
        delivery = delivery_dict.get(o['order_id'])
        eta = delivery['estimated_time'] if delivery else ''
        filtered_orders.append({
            'order_id': o['order_id'],
            'restaurant_name': restaurant_dict[o['restaurant_id']]['name'] if o['restaurant_id'] in restaurant_dict else '',
            'status': o['status'],
            'eta': eta
        })

    return jsonify(filtered_orders)


@app.route('/api/orders/<int:order_id>/tracking', methods=['GET'])
def track_order(order_id):
    orders = load_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        abort(404, description='Order not found')

    deliveries = load_deliveries()
    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)

    order_items = load_order_items()
    menus = load_menus()
    menu_dict = {m['item_id']: m for m in menus}

    # Order items with item_name, quantity, price
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = menu_dict.get(oi['item_id'])
            if not menu_item:
                continue
            items.append({
                'item_name': menu_item['item_name'],
                'quantity': oi['quantity'],
                'price': oi['price']
            })

    delivery_driver = {}
    estimated_time = ''
    if delivery:
        delivery_driver = {
            'name': delivery['driver_name'],
            'phone': delivery['driver_phone'],
            'vehicle_info': delivery['vehicle_info']
        }
        estimated_time = delivery['estimated_time']

    order_details = {
        'order_id': order['order_id'],
        'date': order['order_date'],
        'total_amount': order['total_amount'],
        'status': order['status']
    }

    return jsonify({
        'order_details': order_details,
        'delivery_driver': delivery_driver,
        'estimated_time': estimated_time,
        'order_items': items
    })


@app.route('/api/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        rating_filter = request.args.get('rating')
        reviews_data = load_reviews()
        restaurants = load_restaurants()
        restaurant_dict = {r['id']: r['name'] for r in restaurants}

        filtered = []
        for r in reviews_data:
            if rating_filter:
                try:
                    r_filter_int = int(rating_filter)
                except:
                    r_filter_int = None
                if r_filter_int is not None and r['rating'] != r_filter_int:
                    continue
            filtered.append({
                'review_id': r['review_id'],
                'restaurant_name': restaurant_dict.get(r['restaurant_id'], ''),
                'rating': r['rating'],
                'review_text': r['review_text'],
                'customer_name': r['customer_name'],
                'review_date': r['review_date']
            })

        return jsonify(filtered)

    elif request.method == 'POST':
        data = request.get_json()
        required = ['restaurant_id', 'customer_name', 'rating', 'review_text']
        if not data or not all(field in data for field in required):
            abort(400, description='Missing review fields')

        restaurant_id = data['restaurant_id']
        customer_name = data['customer_name']
        rating = data['rating']
        review_text = data['review_text']

        # Validate rating
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            abort(400, description='Rating must be integer between 1 and 5')

        reviews_data = load_reviews()
        new_review_id = next_id(reviews_data, 'review_id')
        review_date = date.today().isoformat()

        reviews_data.append({
            'review_id': new_review_id,
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        })

        # Write back reviews
        reviews_lines_dict = {r['review_id']: [
            str(r['review_id']),
            str(r['restaurant_id']),
            r['customer_name'],
            str(r['rating']),
            r['review_text'],
            r['review_date']
        ] for r in reviews_data}

        write_file_from_dict('reviews.txt', reviews_lines_dict)

        return jsonify({'message': 'Review submitted', 'review_id': new_review_id})


if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    app.run(debug=True, port=5000)
