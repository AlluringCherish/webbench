from flask import Flask, render_template, redirect, url_for, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data files

def load_restaurants():
    restaurants = []
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
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
                except ValueError:
                    continue
    except IOError:
        pass
    return restaurants


def load_menus():
    menus = []
    path = os.path.join(DATA_DIR, 'menus.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                try:
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
                except ValueError:
                    continue
    except IOError:
        pass
    return menus


def load_cart():
    cart_items = []
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                try:
                    cart_item = {
                        'cart_id': int(parts[0]),
                        'item_id': int(parts[1]),
                        'restaurant_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'added_date': parts[4]
                    }
                    cart_items.append(cart_item)
                except ValueError:
                    continue
    except IOError:
        pass
    return cart_items


def load_orders():
    orders = []
    path = os.path.join(DATA_DIR, 'orders.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
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
    except IOError:
        pass
    return orders


def load_order_items():
    order_items = []
    path = os.path.join(DATA_DIR, 'order_items.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
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
    except IOError:
        pass
    return order_items


def load_deliveries():
    deliveries = []
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
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
    except IOError:
        pass
    return deliveries


def load_reviews():
    reviews = []
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
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
    except IOError:
        pass
    return reviews


# Helper function to save cart back to data/cart.txt
# We persist all cart items

def save_cart(cart_items):
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = f"{item['cart_id']}|{item['item_id']}|{item['restaurant_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
    except IOError:
        pass


# Flask route implementations

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # featured_restaurants: id (int), name (str), cuisine (str), rating (float), delivery_time (int)
    restaurants = load_restaurants()
    # Let's define featured as top 5 rated restaurants
    featured = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:5]
    featured_restaurants = [
        {
            'id': r['restaurant_id'],
            'name': r['name'],
            'cuisine': r['cuisine'],
            'rating': r['rating'],
            'delivery_time': r['delivery_time']
        } for r in featured
    ]
    return render_template('dashboard.html', featured_restaurants=featured_restaurants)


@app.route('/restaurants')
def browse_restaurants():
    restaurants_raw = load_restaurants()
    # Context variable: restaurants with restaurant_id, name, cuisine, rating, delivery_time
    restaurants = [
        {
            'restaurant_id': r['restaurant_id'],
            'name': r['name'],
            'cuisine': r['cuisine'],
            'rating': r['rating'],
            'delivery_time': r['delivery_time']
        } for r in restaurants_raw
    ]
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()

    # Find restaurant
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404

    # menu_items: item_id, item_name, category, description, price, availability
    menu_items = []
    for mi in menus:
        if mi['restaurant_id'] == restaurant_id:
            menu_items.append({
                'item_id': mi['item_id'],
                'item_name': mi['item_name'],
                'category': mi['category'],
                'description': mi['description'],
                'price': mi['price'],
                'availability': mi['availability'],
            })

    # restaurant dict: restaurant_id, name, address, phone, rating, delivery_time
    restaurant_dict = {
        'restaurant_id': restaurant['restaurant_id'],
        'name': restaurant['name'],
        'address': restaurant['address'],
        'phone': restaurant['phone'],
        'rating': restaurant['rating'],
        'delivery_time': restaurant['delivery_time']
    }

    return render_template('menu.html', restaurant=restaurant_dict, menu_items=menu_items)


@app.route('/menu/item/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = next((mi for mi in menus if mi['item_id'] == item_id), None)
    if not item:
        return "Item not found", 404

    # item dict: item_id, item_name, category, description, price, availability
    item_dict = {
        'item_id': item['item_id'],
        'item_name': item['item_name'],
        'category': item['category'],
        'description': item['description'],
        'price': item['price'],
        'availability': item['availability']
    }

    return render_template('item_details.html', item=item_dict)


@app.route('/cart')
def shopping_cart():
    cart_items_raw = load_cart()
    menus = load_menus()

    cart_items = []
    total_amount = 0.0
    for cart_item in cart_items_raw:
        item = next((mi for mi in menus if mi['item_id'] == cart_item['item_id']), None)
        if not item or item['availability'] == 0:
            continue
        quantity = cart_item['quantity']
        price = item['price']
        subtotal = price * quantity
        total_amount += subtotal

        cart_items.append({
            'item_id': item['item_id'],
            'item_name': item['item_name'],
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal
        })

    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


@app.route('/cart/update', methods=['POST'])
def update_cart():
    try:
        item_id = int(request.form.get('item_id', ''))
        quantity = int(request.form.get('quantity', ''))
        if quantity < 0:
            return jsonify({'error': 'Quantity cannot be negative'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input'}), 400

    cart_items = load_cart()

    # Check if item exists in menus
    menus = load_menus()
    item = next((mi for mi in menus if mi['item_id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    # Update quantity or add new if not present
    found = False
    for citem in cart_items:
        if citem['item_id'] == item_id:
            found = True
            if quantity == 0:
                cart_items.remove(citem)
            else:
                citem['quantity'] = quantity
            break

    if not found and quantity > 0:
        # Generate new cart_id
        max_id = max([c['cart_id'] for c in cart_items], default=0)
        new_cart_id = max_id + 1
        today_str = datetime.now().strftime('%Y-%m-%d')
        cart_items.append({
            'cart_id': new_cart_id,
            'item_id': item_id,
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': today_str
        })

    save_cart(cart_items)

    return redirect(url_for('shopping_cart'))


@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    cart_items = load_cart()
    new_cart = [c for c in cart_items if c['item_id'] != item_id]
    if len(new_cart) == len(cart_items):
        # Item not found in cart
        return redirect(url_for('shopping_cart'))

    save_cart(new_cart)
    return redirect(url_for('shopping_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        cart_items_raw = load_cart()
        menus = load_menus()
        cart_items = []
        total_amount = 0.0
        for cart_item in cart_items_raw:
            item = next((mi for mi in menus if mi['item_id'] == cart_item['item_id']), None)
            if not item or item['availability'] == 0:
                continue
            quantity = cart_item['quantity']
            price = item['price']
            subtotal = price * quantity
            total_amount += subtotal
            cart_items.append({
                'item_id': item['item_id'],
                'item_name': item['item_name'],
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })
        return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)
    else:
        customer_name = request.form.get('customer_name', '').strip()
        delivery_address = request.form.get('delivery_address', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not delivery_address or not phone_number or not payment_method:
            return "Missing required fields", 400

        cart_items_raw = load_cart()
        if not cart_items_raw:
            return "Cart is empty", 400

        menus = load_menus()
        orders = load_orders()

        total_amount = 0.0
        for cart_item in cart_items_raw:
            item = next((mi for mi in menus if mi['item_id'] == cart_item['item_id']), None)
            if not item or item['availability'] == 0:
                continue
            quantity = cart_item['quantity']
            subtotal = item['price'] * quantity
            total_amount += subtotal

        if total_amount <= 0:
            return "No valid items in cart", 400

        max_order_id = max([o['order_id'] for o in orders], default=0)
        new_order_id = max_order_id + 1

        restaurant_ids = set([c['restaurant_id'] for c in cart_items_raw])
        if len(restaurant_ids) != 1:
            return "Cart items must be from one restaurant", 400
        restaurant_id = restaurant_ids.pop()

        order_date = datetime.now().strftime('%Y-%m-%d')

        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'restaurant_id': restaurant_id,
            'order_date': order_date,
            'total_amount': total_amount,
            'status': 'Preparing',
            'delivery_address': delivery_address,
            'phone_number': phone_number
        }
        orders.append(new_order)

        orders_path = os.path.join(DATA_DIR, 'orders.txt')
        try:
            with open(orders_path, 'w', encoding='utf-8') as f:
                for o in orders:
                    line = f"{o['order_id']}|{o['customer_name']}|{o['restaurant_id']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['delivery_address']}|{o['phone_number']}\n"
                    f.write(line)
        except IOError:
            return "Error saving order", 500

        order_items = load_order_items()
        max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)
        for cart_item in cart_items_raw:
            max_order_item_id += 1
            new_order_item = {
                'order_item_id': max_order_item_id,
                'order_id': new_order_id,
                'item_id': cart_item['item_id'],
                'quantity': cart_item['quantity'],
                'price': next(mi['price'] for mi in menus if mi['item_id'] == cart_item['item_id'])
            }
            order_items.append(new_order_item)

        order_items_path = os.path.join(DATA_DIR, 'order_items.txt')
        try:
            with open(order_items_path, 'w', encoding='utf-8') as f:
                for oi in order_items:
                    line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']}\n"
                    f.write(line)
        except IOError:
            return "Error saving order items", 500

        try:
            open(os.path.join(DATA_DIR, 'cart.txt'), 'w').close()
        except IOError:
            pass

        return redirect(url_for('active_orders'))


@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    restaurants = load_restaurants()

    active_orders_list = []
    for o in orders:
        if o['status'].lower() != 'delivered':
            restaurant = next((r for r in restaurants if r['restaurant_id'] == o['restaurant_id']), None)
            restaurant_name = restaurant['name'] if restaurant else 'Unknown'
            active_orders_list.append({
                'order_id': o['order_id'],
                'restaurant_name': restaurant_name,
                'status': o['status'],
                'eta': ''
            })

    return render_template('active_orders.html', active_orders=active_orders_list)


@app.route('/orders/track/<int:order_id>')
def order_tracking(order_id):
    orders = load_orders()
    order_items_all = load_order_items()
    deliveries = load_deliveries()
    restaurants = load_restaurants()
    menus = load_menus()

    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    restaurant = next((r for r in restaurants if r['restaurant_id'] == order['restaurant_id']), None)
    restaurant_name = restaurant['name'] if restaurant else 'Unknown'

    delivery_info = next((d for d in deliveries if d['order_id'] == order_id), None)

    order_items_filtered = [oi for oi in order_items_all if oi['order_id'] == order_id]
    order_items_list = []
    for oi in order_items_filtered:
        item = next((mi for mi in menus if mi['item_id'] == oi['item_id']), None)
        item_name = item['item_name'] if item else 'Unknown'
        order_items_list.append({
            'item_name': item_name,
            'quantity': oi['quantity'],
            'price': oi['price']
        })

    order_dict = {
        'order_id': order['order_id'],
        'customer_name': order['customer_name'],
        'restaurant_name': restaurant_name,
        'status': order['status'],
        'total_amount': order['total_amount'],
        'delivery_address': order['delivery_address'],
        'phone_number': order['phone_number']
    }

    delivery_dict = {
        'driver_name': delivery_info['driver_name'] if delivery_info else '',
        'driver_phone': delivery_info['driver_phone'] if delivery_info else '',
        'vehicle_info': delivery_info['vehicle_info'] if delivery_info else '',
        'status': delivery_info['status'] if delivery_info else '',
        'estimated_time': delivery_info['estimated_time'] if delivery_info else ''
    }

    return render_template('tracking.html', order=order_dict, delivery_info=delivery_dict, order_items=order_items_list)


@app.route('/reviews')
def reviews():
    reviews_raw = load_reviews()
    restaurants = load_restaurants()

    reviews_list = []
    for rev in reviews_raw:
        restaurant = next((r for r in restaurants if r['restaurant_id'] == rev['restaurant_id']), None)
        restaurant_name = restaurant['name'] if restaurant else 'Unknown'
        reviews_list.append({
            'review_id': rev['review_id'],
            'restaurant_name': restaurant_name,
            'customer_name': rev['customer_name'],
            'rating': rev['rating'],
            'review_text': rev['review_text'],
            'review_date': rev['review_date']
        })

    return render_template('reviews.html', reviews=reviews_list)


@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    if request.method == 'GET':
        restaurants = load_restaurants()
        return render_template('write_review.html', restaurants=restaurants)
    else:
        try:
            restaurant_id = int(request.form.get('restaurant_id', ''))
            customer_name = request.form.get('customer_name', '').strip()
            rating = int(request.form.get('rating', ''))
            review_text = request.form.get('review_text', '').strip()

            if restaurant_id < 1 or not customer_name or rating < 1 or rating > 5 or not review_text:
                return "Invalid input", 400

        except (ValueError, TypeError):
            return "Invalid input", 400

        reviews = load_reviews()
        max_review_id = max([r['review_id'] for r in reviews], default=0)
        new_review_id = max_review_id + 1
        review_date = datetime.now().strftime('%Y-%m-%d')

        new_review = {
            'review_id': new_review_id,
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }
        reviews.append(new_review)

        reviews_path = os.path.join(DATA_DIR, 'reviews.txt')
        try:
            with open(reviews_path, 'w', encoding='utf-8') as f:
                for rev in reviews:
                    line = f"{rev['review_id']}|{rev['restaurant_id']}|{rev['customer_name']}|{rev['rating']}|{rev['review_text']}|{rev['review_date']}\n"
                    f.write(line)
        except IOError:
            return "Error saving review", 500

        return redirect(url_for('reviews'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
