from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

# Utility functions to read/write data files

def read_restaurants():
    restaurants = []
    try:
        with open(os.path.join(DATA_DIR, 'restaurants.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    restaurants.append({
                        'restaurant_id': parts[0],
                        'name': parts[1],
                        'cuisine': parts[2],
                        'address': parts[3],
                        'phone': parts[4],
                        'rating': float(parts[5]),
                        'delivery_time': int(parts[6]),
                        'min_order': float(parts[7])
                    })
    except FileNotFoundError:
        pass
    return restaurants


def read_menus():
    menus = []
    try:
        with open(os.path.join(DATA_DIR, 'menus.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    menus.append({
                        'item_id': parts[0],
                        'restaurant_id': parts[1],
                        'item_name': parts[2],
                        'category': parts[3],
                        'description': parts[4],
                        'price': float(parts[5]),
                        'availability': parts[6] == '1'
                    })
    except FileNotFoundError:
        pass
    return menus


def read_cart():
    cart = []
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    cart.append({
                        'cart_id': parts[0],
                        'item_id': parts[1],
                        'restaurant_id': parts[2],
                        'quantity': int(parts[3]),
                        'added_date': parts[4]
                    })
    except FileNotFoundError:
        pass
    return cart


def write_cart(cart):
    with open(os.path.join(DATA_DIR, 'cart.txt'), 'w') as f:
        for entry in cart:
            line = '|'.join([
                entry['cart_id'],
                entry['item_id'],
                entry['restaurant_id'],
                str(entry['quantity']),
                entry['added_date']
            ])
            f.write(line + '\n')


def read_orders():
    orders = []
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    orders.append({
                        'order_id': parts[0],
                        'customer_name': parts[1],
                        'restaurant_id': parts[2],
                        'order_date': parts[3],
                        'total_amount': float(parts[4]),
                        'status': parts[5],
                        'delivery_address': parts[6],
                        'phone_number': parts[7]
                    })
    except FileNotFoundError:
        pass
    return orders


def read_order_items():
    order_items = []
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    order_items.append({
                        'order_item_id': parts[0],
                        'order_id': parts[1],
                        'item_id': parts[2],
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    })
    except FileNotFoundError:
        pass
    return order_items


def read_deliveries():
    deliveries = []
    try:
        with open(os.path.join(DATA_DIR, 'deliveries.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    deliveries.append({
                        'delivery_id': parts[0],
                        'order_id': parts[1],
                        'driver_name': parts[2],
                        'driver_phone': parts[3],
                        'vehicle_info': parts[4],
                        'status': parts[5],
                        'estimated_time': parts[6]
                    })
    except FileNotFoundError:
        pass
    return deliveries


def read_reviews():
    reviews = []
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    reviews.append({
                        'review_id': parts[0],
                        'restaurant_id': parts[1],
                        'customer_name': parts[2],
                        'rating': int(parts[3]),
                        'review_text': parts[4],
                        'review_date': parts[5]
                    })
    except FileNotFoundError:
        pass
    return reviews


@app.route('/')
def dashboard():
    restaurants = read_restaurants()
    # Featured restaurants: top 3 by rating
    featured = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    return render_template('dashboard.html', featured_restaurants=featured)


@app.route('/restaurants')
def restaurants_page():
    cuisine_filter = request.args.get('cuisine')
    search_query = request.args.get('search')
    restaurants = read_restaurants()
    # Filtering
    if cuisine_filter and cuisine_filter != 'All':
        restaurants = [r for r in restaurants if r['cuisine'].lower() == cuisine_filter.lower()]
    if search_query:
        sq = search_query.lower()
        restaurants = [r for r in restaurants if sq in r['name'].lower() or sq in r['cuisine'].lower()]

    cuisines = sorted(list(set(r['cuisine'] for r in read_restaurants())))

    return render_template('restaurants.html', restaurants=restaurants, cuisines=cuisines, selected_cuisine=cuisine_filter or 'All', search_query=search_query or '')


@app.route('/restaurant/<restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = read_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return 'Restaurant not found', 404
    menus = [m for m in read_menus() if m['restaurant_id'] == restaurant_id and m['availability']]
    return render_template('menu.html', restaurant=restaurant, menus=menus)


@app.route('/item/<item_id>', methods=['GET', 'POST'])
def item_details(item_id):
    menus = read_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability']), None)
    if not item:
        return 'Item not found', 404

    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))
        if quantity <= 0:
            quantity = 1
        cart = read_cart()
        # Check if item already in cart
        existing = next((c for c in cart if c['item_id'] == item_id), None)
        now_str = datetime.now().strftime('%Y-%m-%d')
        if existing:
            existing['quantity'] += quantity
        else:
            cart_id = str(len(cart) + 1) if cart else '1'
            cart.append({
                'cart_id': cart_id,
                'item_id': item_id,
                'restaurant_id': item['restaurant_id'],
                'quantity': quantity,
                'added_date': now_str
            })
        write_cart(cart)
        return redirect(url_for('shopping_cart'))

    return render_template('item_details.html', item=item)


@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart = read_cart()
    menus = read_menus()
    # Join cart items with menu info
    detailed_cart = []
    total_amount = 0
    for c in cart:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            subtotal = menu_item['price'] * c['quantity']
            detailed_cart.append({
                'cart_id': c['cart_id'],
                'item_id': c['item_id'],
                'item_name': menu_item['item_name'],
                'price': menu_item['price'],
                'quantity': c['quantity'],
                'subtotal': subtotal
            })
            total_amount += subtotal

    if request.method == 'POST':
        # Update quantities or remove items based on form
        updated = False
        for c in detailed_cart:
            qty_key = f'update-quantity-{c["item_id"]}'
            remove_key = f'remove-item-button-{c["item_id"]}'
            if remove_key in request.form:
                cart = [item for item in cart if item['item_id'] != c['item_id']]
                updated = True
                break
            elif qty_key in request.form:
                try:
                    new_qty = int(request.form.get(qty_key))
                    if new_qty <= 0:
                        cart = [item for item in cart if item['item_id'] != c['item_id']]
                    else:
                        for item in cart:
                            if item['item_id'] == c['item_id']:
                                item['quantity'] = new_qty
                    updated = True
                except ValueError:
                    pass
        if updated:
            write_cart(cart)
        return redirect(url_for('shopping_cart'))

    return render_template('cart.html', cart_items=detailed_cart, total_amount=total_amount)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = read_cart()
    if not cart:
        return redirect(url_for('shopping_cart'))

    menus = read_menus()
    detailed_cart = []
    total_amount = 0
    for c in cart:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            subtotal = menu_item['price'] * c['quantity']
            detailed_cart.append({
                'item_id': c['item_id'],
                'item_name': menu_item['item_name'],
                'quantity': c['quantity'],
                'price': menu_item['price'],
                'subtotal': subtotal
            })
            total_amount += subtotal

    if request.method == 'POST':
        customer_name = request.form.get('customer-name')
        delivery_address = request.form.get('delivery-address')
        phone_number = request.form.get('phone-number')
        payment_method = request.form.get('payment-method')

        if not customer_name or not delivery_address or not phone_number or not payment_method:
            error = 'Please fill out all fields.'
            return render_template('checkout.html', cart_items=detailed_cart, total_amount=total_amount, error=error)

        orders = read_orders()
        restaurants = read_restaurants()
        order_id = str(len(orders) + 1) if orders else '1'
        order_date = datetime.now().strftime('%Y-%m-%d')

        # Check all items belong to same restaurant
        restaurant_ids = set(item['restaurant_id'] for item in cart)
        if len(restaurant_ids) > 1:
            error = 'All items in the cart must be from the same restaurant to place an order.'
            return render_template('checkout.html', cart_items=detailed_cart, total_amount=total_amount, error=error)
        restaurant_id = restaurant_ids.pop()

        # Check minimum order
        restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
        if restaurant and total_amount < restaurant['min_order']:
            error = f'Minimum order amount for {restaurant["name"]} is ${restaurant["min_order"]:.2f}.'
            return render_template('checkout.html', cart_items=detailed_cart, total_amount=total_amount, error=error)

        # Save new order
        new_order_line = '|'.join([
            order_id,
            customer_name,
            restaurant_id,
            order_date,
            str(total_amount),
            'Preparing',
            delivery_address,
            phone_number
        ]) + '\n'

        with open(os.path.join(DATA_DIR, 'orders.txt'), 'a') as f:
            f.write(new_order_line)

        # Save order items
        order_items = read_order_items()
        current_max_id = max([int(oi['order_item_id']) for oi in order_items], default=0)
        order_item_id = current_max_id + 1
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'a') as f:
            for item in cart:
                menu_item = next((m for m in menus if m['item_id'] == item['item_id']), None)
                if menu_item:
                    line = '|'.join([
                        str(order_item_id),
                        order_id,
                        item['item_id'],
                        str(item['quantity']),
                        str(menu_item['price'])
                    ]) + '\n'
                    f.write(line)
                    order_item_id += 1

        # Clear cart
        write_cart([])

        return redirect(url_for('active_orders'))

    return render_template('checkout.html', cart_items=detailed_cart, total_amount=total_amount)


@app.route('/active_orders')
def active_orders():
    orders = read_orders()
    deliveries = read_deliveries()
    restaurants = read_restaurants()
    status_filter = request.args.get('status', 'All')

    if status_filter != 'All':
        orders = [o for o in orders if o['status'] == status_filter]

    # Join orders with restaurant name and delivery info
    detailed_orders = []
    for o in orders:
        restaurant = next((r for r in restaurants if r['restaurant_id'] == o['restaurant_id']), None)
        delivery = next((d for d in deliveries if d['order_id'] == o['order_id']), None)
        detailed_orders.append({
            'order_id': o['order_id'],
            'customer_name': o['customer_name'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'order_date': o['order_date'],
            'total_amount': o['total_amount'],
            'status': o['status'],
            'delivery_address': o['delivery_address'],
            'phone_number': o['phone_number'],
            'driver_name': delivery['driver_name'] if delivery else '',
            'driver_phone': delivery['driver_phone'] if delivery else '',
            'vehicle_info': delivery['vehicle_info'] if delivery else '',
            'estimated_time': delivery['estimated_time'] if delivery else ''
        })

    statuses = ['All', 'Preparing', 'On the Way', 'Delivered']

    return render_template('active_orders.html', orders=detailed_orders, statuses=statuses, selected_status=status_filter)


@app.route('/track_order/<order_id>')
def track_order(order_id):
    orders = read_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return 'Order not found', 404

    order_items = read_order_items()
    menus = read_menus()
    deliveries = read_deliveries()

    order_items_list = [oi for oi in order_items if oi['order_id'] == order_id]
    detailed_items = []
    for oi in order_items_list:
        menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
        if menu_item:
            detailed_items.append({
                'item_name': menu_item['item_name'],
                'quantity': oi['quantity'],
                'price': oi['price']
            })

    delivery = next((d for d in deliveries if d['order_id'] == order_id), None)

    return render_template('tracking.html', order=order, items=detailed_items, delivery=delivery)


@app.route('/reviews')
def reviews():
    reviews = read_reviews()
    restaurants = read_restaurants()

    # Join review with restaurant name
    detailed_reviews = []
    for r in reviews:
        restaurant = next((res for res in restaurants if res['restaurant_id'] == r['restaurant_id']), None)
        detailed_reviews.append({
            'review_id': r['review_id'],
            'restaurant_name': restaurant['name'] if restaurant else 'Unknown',
            'customer_name': r['customer_name'],
            'rating': r['rating'],
            'review_text': r['review_text'],
            'review_date': r['review_date']
        })

    rating_filter = request.args.get('rating', 'All')
    if rating_filter != 'All':
        try:
            rating_value = int(rating_filter[0])  # '5 stars' -> 5
            detailed_reviews = [rev for rev in detailed_reviews if rev['rating'] == rating_value]
        except Exception:
            pass

    ratings = ['All', '5 stars', '4 stars', '3 stars', '2 stars', '1 star']

    return render_template('reviews.html', reviews=detailed_reviews, ratings=ratings, selected_rating=rating_filter)


@app.route('/write_review/<restaurant_id>', methods=['GET', 'POST'])
def write_review(restaurant_id):
    restaurants = read_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return 'Restaurant not found', 404

    if request.method == 'POST':
        customer_name = request.form.get('customer-name')
        rating = request.form.get('rating')
        review_text = request.form.get('review-text')

        if not customer_name or not rating or not review_text:
            error = 'Please fill out all fields.'
            return render_template('write_review.html', restaurant=restaurant, error=error)

        reviews = read_reviews()
        review_id = str(len(reviews) + 1) if reviews else '1'
        review_date = datetime.now().strftime('%Y-%m-%d')

        new_review_line = '|'.join([
            review_id,
            restaurant_id,
            customer_name,
            rating,
            review_text,
            review_date
        ]) + '\n'

        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a') as f:
            f.write(new_review_line)

        return redirect(url_for('reviews'))

    return render_template('write_review.html', restaurant=restaurant)


if __name__ == '__main__':
    app.run(debug=True)
