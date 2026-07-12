from flask import Flask, render_template, redirect, url_for, request, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from files with pipe-separated values

def load_restaurants():
    # Fields: restaurant_id (int), restaurant_name (str), cuisine (str), phone_number (str), rating (float), num_reviews (int), min_order (float)
    restaurants = []
    filepath = os.path.join(DATA_DIR, 'restaurants.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                restaurants.append({
                    'restaurant_id': int(parts[0]),
                    'restaurant_name': parts[1],
                    'cuisine': parts[2],
                    'phone_number': parts[3],
                    'rating': float(parts[4]),
                    'num_reviews': int(parts[5]),
                    'min_order': float(parts[6])
                })
    except IOError:
        pass
    return restaurants


def load_menu_items():
    # Fields: item_id (int), restaurant_id (int), category (str), item_name (str), description (str), price (float), availability (int)
    items = []
    filepath = os.path.join(DATA_DIR, 'menus.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                items.append({
                    'item_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'category': parts[2],
                    'item_name': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': int(parts[6])
                })
    except IOError:
        pass
    return items


def load_cart():
    # Fields: item_id (int), quantity (int)
    cart = []
    filepath = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 2:
                    continue
                cart.append({
                    'item_id': int(parts[0]),
                    'quantity': int(parts[1])
                })
    except IOError:
        pass
    return cart


def load_orders():
    # Fields: order_id (int), customer_name (str), restaurant_id (int), date (str), total_amount (float), status (str), delivery_address (str), phone (str), vehicle_info (str)
    orders = []
    filepath = os.path.join(DATA_DIR, 'orders.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 9:
                    continue
                orders.append({
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'restaurant_id': int(parts[2]),
                    'date': parts[3],
                    'total_amount': float(parts[4]),
                    'status': parts[5],
                    'delivery_address': parts[6],
                    'phone': parts[7],
                    'vehicle_info': parts[8]
                })
    except IOError:
        pass
    return orders


def load_order_items():
    # Fields: order_item_id (int), order_id (int), item_id (int), quantity (int), item_price (float)
    order_items = []
    filepath = os.path.join(DATA_DIR, 'order_items.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                order_items.append({
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'item_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'item_price': float(parts[4])
                })
    except IOError:
        pass
    return order_items


def load_reviews():
    # Fields: review_id (int), customer_name (str), restaurant_id (int), rating (int), review_text (str), added_date (str)
    reviews = []
    filepath = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                reviews.append({
                    'review_id': int(parts[0]),
                    'customer_name': parts[1],
                    'restaurant_id': int(parts[2]),
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'added_date': parts[5]
                })
    except IOError:
        pass
    return reviews


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    # Provide featured restaurants (just all for now as no spec) and overall metrics for dashboard
    # As per design spec, we do not add additional logic beyond loading
    return render_template('dashboard.html', restaurants=restaurants)


@app.route('/restaurants')
def browse_restaurants():
    restaurants = load_restaurants()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if restaurant is None:
        abort(404)
    menu_items = load_menu_items()
    restaurant_menu_items = [item for item in menu_items if item['restaurant_id'] == restaurant_id]
    return render_template('menu.html', restaurant=restaurant, menu_items=restaurant_menu_items)


@app.route('/menu/item/<int:item_id>')
def item_details(item_id):
    menu_items = load_menu_items()
    item = next((i for i in menu_items if i['item_id'] == item_id), None)
    if item is None:
        abort(404)
    return render_template('item_details.html', item=item)


@app.route('/cart')
def shopping_cart():
    cart_items = load_cart()
    menu_items = load_menu_items()
    # enrich cart data with item info
    enriched_cart = []
    for cart_item in cart_items:
        item = next((i for i in menu_items if i['item_id'] == cart_item['item_id']), None)
        if item:
            enriched_cart.append({
                'item': item,
                'quantity': cart_item['quantity'],
                'subtotal': item['price'] * cart_item['quantity']
            })
    return render_template('cart.html', cart_items=enriched_cart)


@app.route('/cart/update', methods=['POST'])
def update_cart():
    # Update cart quantities or remove items
    cart_items = load_cart()
    menu_items = load_menu_items()

    updated_cart = []
    # The form keys expected like 'quantity-<item_id>' or 'remove-<item_id>' check
    for key in request.form.keys():
        if key.startswith('quantity-'):
            try:
                item_id = int(key.split('-')[1])
                quantity = int(request.form[key])
                if quantity > 0:
                    updated_cart.append({'item_id': item_id, 'quantity': quantity})
            except Exception:
                pass
        elif key.startswith('remove-'):
            # Ignore the item in cart if remove is pressed
            pass

    # Overwrite cart.txt with updated_cart
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
            for ci in updated_cart:
                f.write(f"{ci['item_id']}|{ci['quantity']}\n")
    except IOError:
        abort(500)

    return redirect(url_for('shopping_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        cart_items = load_cart()
        menu_items = load_menu_items()
        enriched_cart = []
        total_amount = 0.0
        for cart_item in cart_items:
            item = next((i for i in menu_items if i['item_id'] == cart_item['item_id']), None)
            if item:
                subtotal = item['price'] * cart_item['quantity']
                total_amount += subtotal
                enriched_cart.append({
                    'item': item,
                    'quantity': cart_item['quantity'],
                    'subtotal': subtotal
                })
        return render_template('checkout.html', cart_items=enriched_cart, total_amount=total_amount)

    # POST - place order
    customer_name = request.form.get('customer_name', '').strip()
    phone = request.form.get('phone', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    vehicle_info = request.form.get('vehicle_info', '').strip()

    if not customer_name or not phone or not delivery_address or not vehicle_info:
        # Missing required fields
        return render_template('checkout.html', error='Please fill all required fields.')

    cart_items = load_cart()
    if not cart_items:
        return render_template('checkout.html', error='Your cart is empty.')

    menu_items = load_menu_items()
    total_amount = 0.0
    for cart_item in cart_items:
        item = next((i for i in menu_items if i['item_id'] == cart_item['item_id']), None)
        if item is None:
            return render_template('checkout.html', error='An item in your cart is unavailable.')
        total_amount += item['price'] * cart_item['quantity']

    orders = load_orders()
    if orders:
        max_order_id = max(order['order_id'] for order in orders)
    else:
        max_order_id = 0
    new_order_id = max_order_id + 1

    # For demo purposes, associate this order with the first restaurant in the cart
    restaurant_id = None
    if cart_items:
        first_item = next((i for i in menu_items if i['item_id'] == cart_items[0]['item_id']), None)
        if first_item:
            restaurant_id = first_item['restaurant_id']
    if restaurant_id is None:
        return render_template('checkout.html', error='Unable to find restaurant for your order.')

    import datetime
    order_date = datetime.date.today().isoformat()
    status = 'Preparing'

    # Persist new order to orders.txt
    try:
        with open(os.path.join(DATA_DIR, 'orders.txt'), 'a', encoding='utf-8') as f:
            f.write(f"{new_order_id}|{customer_name}|{restaurant_id}|{order_date}|{total_amount:.2f}|{status}|{delivery_address}|{phone}|{vehicle_info}\n")
    except IOError:
        abort(500)

    # Persist order_items to order_items.txt
    order_items = load_order_items()
    max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)
    try:
        with open(os.path.join(DATA_DIR, 'order_items.txt'), 'a', encoding='utf-8') as f:
            for cart_item in cart_items:
                item = next((i for i in menu_items if i['item_id'] == cart_item['item_id']), None)
                if item is None:
                    continue
                max_order_item_id += 1
                item_price = item['price']
                f.write(f"{max_order_item_id}|{new_order_id}|{item['item_id']}|{cart_item['quantity']}|{item_price:.2f}\n")
    except IOError:
        abort(500)

    # Clear cart after order placed
    try:
        with open(os.path.join(DATA_DIR, 'cart.txt'), 'w', encoding='utf-8') as f:
            pass
    except IOError:
        abort(500)

    return redirect(url_for('active_orders'))


@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    # Filter orders with status not delivered (case insensitive)
    active_orders_list = [o for o in orders if o['status'].lower() != 'delivered']
    restaurants = load_restaurants()
    # Enhance orders with restaurant name
    for order in active_orders_list:
        rest = next((r for r in restaurants if r['restaurant_id'] == order['restaurant_id']), None)
        order['restaurant_name'] = rest['restaurant_name'] if rest else 'Unknown'

    return render_template('active_orders.html', orders=active_orders_list)


@app.route('/orders/track/<int:order_id>')
def track_order(order_id):
    orders = load_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if order is None:
        abort(404)
    restaurants = load_restaurants()
    rest = next((r for r in restaurants if r['restaurant_id'] == order['restaurant_id']), None)
    order_items = load_order_items()
    menu_items = load_menu_items()

    # Get items for this order with item details
    items = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            item = next((i for i in menu_items if i['item_id'] == oi['item_id']), None)
            if item:
                items.append({
                    'item_id': item['item_id'],
                    'item_name': item['item_name'],
                    'quantity': oi['quantity'],
                    'item_price': oi['item_price'],
                    'subtotal': oi['quantity'] * oi['item_price']
                })

    return render_template('track_order.html', order=order, restaurant=rest, items=items)


@app.route('/reviews')
def reviews():
    reviews_list = load_reviews()
    restaurants = load_restaurants()
    # Enhance reviews with restaurant name
    for review in reviews_list:
        rest = next((r for r in restaurants if r['restaurant_id'] == review['restaurant_id']), None)
        review['restaurant_name'] = rest['restaurant_name'] if rest else 'Unknown'
    return render_template('reviews.html', reviews=reviews_list)


@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    if request.method == 'GET':
        restaurants = load_restaurants()
        return render_template('write_review.html', restaurants=restaurants)

    # POST: process submitted review
    customer_name = request.form.get('customer_name', '').strip()
    restaurant_id = request.form.get('restaurant_id', '').strip()
    rating = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()

    if not customer_name or not restaurant_id or not rating or not review_text:
        return render_template(
            'write_review.html',
            error='All fields are required.',
            restaurants=load_restaurants(),
            customer_name=customer_name,
            restaurant_id=restaurant_id,
            rating=rating,
            review_text=review_text
        )
    try:
        restaurant_id = int(restaurant_id)
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        return render_template(
            'write_review.html',
            error='Invalid restaurant or rating.',
            restaurants=load_restaurants(),
            customer_name=customer_name,
            restaurant_id=restaurant_id,
            rating=rating,
            review_text=review_text
        )

    reviews = load_reviews()
    if reviews:
        max_review_id = max(r['review_id'] for r in reviews)
    else:
        max_review_id = 0
    new_review_id = max_review_id + 1

    from datetime import datetime
    added_date = datetime.today().date().isoformat()

    # Append new review
    try:
        with open(os.path.join(DATA_DIR, 'reviews.txt'), 'a', encoding='utf-8') as f:
            f.write(f"{new_review_id}|{customer_name}|{restaurant_id}|{rating}|{review_text}|{added_date}\n")
    except IOError:
        abort(500)

    return redirect(url_for('reviews'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
