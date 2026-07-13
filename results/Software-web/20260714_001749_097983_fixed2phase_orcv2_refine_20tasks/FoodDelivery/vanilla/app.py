from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import os

app = Flask(__name__)

data_dir = 'data'

# Helper functions for data loading and saving

def read_restaurants():
    path = os.path.join(data_dir, 'restaurants.txt')
    restaurants = []
    if not os.path.exists(path):
        return restaurants
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
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
    return restaurants

def read_menus():
    path = os.path.join(data_dir, 'menus.txt')
    menus = []
    if not os.path.exists(path):
        return menus
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                menu = {
                    'item_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'item_name': parts[2],
                    'category': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': int(parts[6])
                }
                menus.append(menu)
    return menus


def read_cart():
    path = os.path.join(data_dir, 'cart.txt')
    cart = []
    if not os.path.exists(path):
        return cart
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                item = {
                    'cart_id': int(parts[0]),
                    'item_id': int(parts[1]),
                    'restaurant_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'added_date': parts[4]
                }
                cart.append(item)
    return cart

def write_cart(cart):
    path = os.path.join(data_dir, 'cart.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for item in cart:
            line = f"{item['cart_id']}|{item['item_id']}|{item['restaurant_id']}|{item['quantity']}|{item['added_date']}\n"
            f.write(line)


def read_orders():
    path = os.path.join(data_dir, 'orders.txt')
    orders = []
    if not os.path.exists(path):
        return orders
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
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
    return orders

def write_orders(orders):
    path = os.path.join(data_dir, 'orders.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for order in orders:
            line = f"{order['order_id']}|{order['customer_name']}|{order['restaurant_id']}|{order['order_date']}|{order['total_amount']:.2f}|{order['status']}|{order['delivery_address']}|{order['phone_number']}\n"
            f.write(line)


def read_order_items():
    path = os.path.join(data_dir, 'order_items.txt')
    order_items = []
    if not os.path.exists(path):
        return order_items
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                oi = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'item_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(oi)
    return order_items

def write_order_items(order_items):
    path = os.path.join(data_dir, 'order_items.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for oi in order_items:
            line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']:.2f}\n"
            f.write(line)


def read_deliveries():
    path = os.path.join(data_dir, 'deliveries.txt')
    deliveries = []
    if not os.path.exists(path):
        return deliveries
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
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
    return deliveries

def write_deliveries(deliveries):
    path = os.path.join(data_dir, 'deliveries.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for d in deliveries:
            line = f"{d['delivery_id']}|{d['order_id']}|{d['driver_name']}|{d['driver_phone']}|{d['vehicle_info']}|{d['status']}|{d['estimated_time']}\n"
            f.write(line)


def read_reviews():
    path = os.path.join(data_dir, 'reviews.txt')
    reviews = []
    if not os.path.exists(path):
        return reviews
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                review = {
                    'review_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews.append(review)
    return reviews

def write_reviews(reviews):
    path = os.path.join(data_dir, 'reviews.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for r in reviews:
            line = f"{r['review_id']}|{r['restaurant_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
            f.write(line)


@app.route('/')
def dashboard():
    restaurants = read_restaurants()
    # Featured restaurants: top 3 by rating
    featured = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    return render_template('dashboard.html', featured=featured)


@app.route('/restaurants')
def restaurant_listing():
    search = request.args.get('search', '').lower()
    cuisine_filter = request.args.get('cuisine', '').lower()
    restaurants = read_restaurants()
    # Filter by search
    if search:
        restaurants = [r for r in restaurants if search in r['name'].lower() or search in r['cuisine'].lower()]
    # Filter by cuisine
    if cuisine_filter and cuisine_filter != 'all':
        restaurants = [r for r in restaurants if r['cuisine'].lower() == cuisine_filter]
    cuisines = sorted(set(r['cuisine'] for r in read_restaurants()))
    return render_template('restaurants.html', restaurants=restaurants, cuisines=cuisines, selected_cuisine=cuisine_filter, search_text=search)


@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = read_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404
    menus = read_menus()
    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability'] == 1]
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)


@app.route('/item/<int:item_id>')
def item_details(item_id):
    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability'] == 1), None)
    if not item:
        return "Item not found or unavailable", 404
    return render_template('item_details.html', item=item)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = int(request.form['item_id'])
    quantity = int(request.form.get('quantity', 1))
    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability'] == 1), None)
    if not item:
        return "Item not found or unavailable", 404

    cart = read_cart()
    # Check if item already in cart
    existing = next((c for c in cart if c['item_id'] == item_id), None)
    if existing:
        existing['quantity'] += quantity
    else:
        new_cart_id = max([c['cart_id'] for c in cart], default=0) + 1
        today_str = datetime.today().strftime('%Y-%m-%d')
        cart.append({
            'cart_id': new_cart_id,
            'item_id': item_id,
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': today_str
        })
    write_cart(cart)

    # Redirect back to referring page
    return redirect(request.referrer or url_for('dashboard'))


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'POST':
        # Update quantities or remove items
        cart = read_cart()
        updated_cart = []
        for cart_item in cart:
            item_id_str = str(cart_item['item_id'])
            quantity_str = request.form.get(f'update-quantity-{item_id_str}')
            remove_str = request.form.get(f'remove-item-button-{item_id_str}')
            if remove_str:
                # Removing this item
                continue
            if quantity_str:
                try:
                    quantity = int(quantity_str)
                    if quantity > 0:
                        cart_item['quantity'] = quantity
                    else:
                        # quantity 0 or less means remove
                        continue
                except ValueError:
                    pass
            updated_cart.append(cart_item)
        write_cart(updated_cart)
        return redirect(url_for('shopping_cart'))

    cart = read_cart()
    menus = read_menus()
    detailed_cart = []
    total_amount = 0.0
    for c in cart:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            subtotal = menu_item['price'] * c['quantity']
            total_amount += subtotal
            detailed_cart.append({
                'cart_id': c['cart_id'],
                'item_id': c['item_id'],
                'name': menu_item['item_name'],
                'quantity': c['quantity'],
                'price': menu_item['price'],
                'subtotal': subtotal
            })
    return render_template('cart.html', cart_items=detailed_cart, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        customer_name = request.form['customer-name'].strip()
        delivery_address = request.form['delivery-address'].strip()
        phone_number = request.form['phone-number'].strip()
        payment_method = request.form['payment-method']

        cart = read_cart()
        if not cart:
            return redirect(url_for('shopping_cart'))

        menus = read_menus()
        orders = read_orders()
        order_items = read_order_items()

        # Calculate total amount
        total_amount = 0.0
        for c in cart:
            menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
            if menu_item:
                total_amount += menu_item['price'] * c['quantity']

        # Group cart items by restaurant (we assume single restaurant order, but to keep flexible we'll take first restaurant_id)
        restaurant_id = cart[0]['restaurant_id']

        # Assign new order_id
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        order_date = datetime.today().strftime('%Y-%m-%d')

        # Create new order
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
        write_orders(orders)

        # Add order items
        new_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1
        for c in cart:
            menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
            if menu_item:
                order_item = {
                    'order_item_id': new_order_item_id,
                    'order_id': new_order_id,
                    'item_id': c['item_id'],
                    'quantity': c['quantity'],
                    'price': menu_item['price']
                }
                order_items.append(order_item)
                new_order_item_id += 1
        write_order_items(order_items)

        # Clear cart after placing order
        write_cart([])

        # Add a delivery entry
        deliveries = read_deliveries()
        new_delivery_id = max([d['delivery_id'] for d in deliveries], default=0) + 1
        estimated_time = (datetime.now().replace(microsecond=0) + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M')
        delivery = {
            'delivery_id': new_delivery_id,
            'order_id': new_order_id,
            'driver_name': 'Assigned Driver',
            'driver_phone': 'N/A',
            'vehicle_info': 'N/A',
            'status': 'Preparing',
            'estimated_time': estimated_time
        }
        deliveries.append(delivery)
        write_deliveries(deliveries)

        return redirect(url_for('active_orders'))

    return render_template('checkout.html')


@app.route('/active_orders')
def active_orders():
    status_filter = request.args.get('status', 'All')
    orders = read_orders()
    restaurants = read_restaurants()
    deliveries = read_deliveries()

    filtered_orders = []
    for o in orders:
        if status_filter != 'All' and o['status'] != status_filter:
            continue
        restaurant = next((r for r in restaurants if r['restaurant_id'] == o['restaurant_id']), None)
        delivery = next((d for d in deliveries if d['order_id'] == o['order_id']), None)
        eta = delivery['estimated_time'] if delivery else 'N/A'
        filtered_orders.append({
            'order_id': o['order_id'],
            'customer_name': o['customer_name'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'status': o['status'],
            'eta': eta
        })

    return render_template('active_orders.html', orders=filtered_orders, selected_status=status_filter)


@app.route('/track_order/<int:order_id>')
def track_order(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return "Order not found", 404

    order_items = read_order_items()
    menus = read_menus()
    items_in_order = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items_in_order.append({
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    deliveries = read_deliveries()
    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)

    restaurants = read_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == order['restaurant_id']), None)

    return render_template('tracking.html', order=order, items=items_in_order, delivery=delivery, restaurant=restaurant)


@app.route('/reviews')
def reviews():
    rating_filter = request.args.get('rating', 'All')
    reviews = read_reviews()
    restaurants = read_restaurants()
    filtered_reviews = []
    for r in reviews:
        if rating_filter != 'All' and str(r['rating']) != rating_filter:
            continue
        restaurant = next((res for res in restaurants if res['restaurant_id'] == r['restaurant_id']), None)
        filtered_reviews.append({
            'review_id': r['review_id'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'rating': r['rating'],
            'review_text': r['review_text'],
            'customer_name': r['customer_name'],
            'review_date': r['review_date']
        })
    return render_template('reviews.html', reviews=filtered_reviews, selected_rating=rating_filter)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    restaurants = read_restaurants()
    if request.method == 'POST':
        restaurant_id = int(request.form['restaurant-select'])
        customer_name = request.form['customer-name-input'].strip()
        rating = int(request.form['rating-select'])
        review_text = request.form['review-textarea'].strip()

        reviews = read_reviews()
        new_review_id = max([r['review_id'] for r in reviews], default=0) + 1
        review_date = datetime.today().strftime('%Y-%m-%d')
        new_review = {
            'review_id': new_review_id,
            'restaurant_id': restaurant_id,
            'customer_name': customer_name,
            'rating': rating,
            'review_text': review_text,
            'review_date': review_date
        }
        reviews.append(new_review)
        write_reviews(reviews)
        return redirect(url_for('reviews'))

    return render_template('write_review.html', restaurants=restaurants)


if __name__ == '__main__':
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    app.run(debug=True)
