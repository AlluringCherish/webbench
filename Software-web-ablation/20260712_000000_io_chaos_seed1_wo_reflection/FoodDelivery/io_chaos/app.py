from flask import Flask, render_template, redirect, url_for, request, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_secret_key'

DATA_DIR = 'data'

# Helper functions to load data

def load_restaurants():
    filepath = os.path.join(DATA_DIR, 'restaurants.txt')
    restaurants = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                restaurant = {
                    'restaurant_id': parts[0],
                    'name': parts[1],
                    'cuisine': parts[2],
                    'address': parts[3],
                    'phone': parts[4],
                    'rating': float(parts[5]),
                    'delivery_time': parts[6],
                    'min_order': parts[7]
                }
                restaurants.append(restaurant)
    except IOError:
        restaurants = []
    return restaurants

def load_menus():
    filepath = os.path.join(DATA_DIR, 'menus.txt')
    menus = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                menu_item = {
                    'item_id': parts[0],
                    'restaurant_id': parts[1],
                    'item_name': parts[2],
                    'category': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': parts[6]
                }
                menus.append(menu_item)
    except IOError:
        menus = []
    return menus

def load_cart():
    filepath = os.path.join(DATA_DIR, 'cart.txt')
    cart_items = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                cart_item = {
                    'cart_id': parts[0],
                    'item_id': parts[1],
                    'restaurant_id': parts[2],
                    'quantity': parts[3],
                    'added_date': parts[4]
                }
                cart_items.append(cart_item)
    except IOError:
        cart_items = []
    return cart_items

def load_orders():
    filepath = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    continue
                order = {
                    'order_id': parts[0],
                    'customer_name': parts[1],
                    'restaurant_id': parts[2],
                    'order_date': parts[3],
                    'total_amount': float(parts[4]),
                    'status': parts[5],
                    'delivery_address': parts[6],
                    'phone_number': parts[7]
                }
                orders.append(order)
    except IOError:
        orders = []
    return orders

def load_order_items():
    filepath = os.path.join(DATA_DIR, 'order_items.txt')
    order_items = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                order_item = {
                    'order_item_id': parts[0],
                    'order_id': parts[1],
                    'item_id': parts[2],
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(order_item)
    except IOError:
        order_items = []
    return order_items

def load_deliveries():
    filepath = os.path.join(DATA_DIR, 'deliveries.txt')
    deliveries = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                delivery = {
                    'delivery_id': parts[0],
                    'order_id': parts[1],
                    'driver_name': parts[2],
                    'driver_phone': parts[3],
                    'vehicle_info': parts[4],
                    'status': parts[5],
                    'estimated_time': parts[6]
                }
                deliveries.append(delivery)
    except IOError:
        deliveries = []
    return deliveries

def load_reviews():
    filepath = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                review = {
                    'review_id': parts[0],
                    'restaurant_id': parts[1],
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                }
                reviews.append(review)
    except IOError:
        reviews = []
    return reviews

# ROUTES

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    sorted_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)
    featured_restaurants = sorted_restaurants[:2]
    cuisine_set = {r['cuisine'] for r in restaurants}
    popular_cuisines = list(cuisine_set)
    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=popular_cuisines)

@app.route('/restaurants')
def restaurant_listing():
    restaurants = load_restaurants()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/menu/<restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if restaurant is None:
        abort(404)
    menus = load_menus()
    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability'] in ['1', 'true', 'yes']]
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

@app.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item:
        abort(404)
    if request.method == 'POST':
        # Handle add to cart
        quantity = request.form.get('quantity', '1')
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 1
        # Load cart
        cart_items = load_cart()

        import datetime
        added_date = datetime.datetime.now().strftime('%Y-%m-%d')
        # Generate new cart_id
        new_cart_id = 1
        if cart_items:
            existing_ids = [int(c['cart_id']) for c in cart_items if c['cart_id'].isdigit()]
            if existing_ids:
                new_cart_id = max(existing_ids) + 1
        new_cart_item = {
            'cart_id': str(new_cart_id),
            'item_id': item['item_id'],
            'restaurant_id': item['restaurant_id'],
            'quantity': str(quantity),
            'added_date': added_date
        }
        # Append to cart.txt
        filepath = os.path.join(DATA_DIR, 'cart.txt')
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"{new_cart_item['cart_id']}|{new_cart_item['item_id']}|{new_cart_item['restaurant_id']}|{new_cart_item['quantity']}|{new_cart_item['added_date']}\n")
        return redirect(url_for('shopping_cart'))

    return render_template('item_detail.html', item=item)

@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_items = load_cart()
    menus = load_menus()

    detailed_cart_items = []
    total_amount = 0.0

    def qty_to_int(qty_str):
        try:
            return int(qty_str)
        except ValueError:
            return 0

    if request.method == 'POST':
        # Handle quantity updates or removals
        action = request.form.get('action')
        item_id = request.form.get('item_id')
        if action == 'update_quantity' and item_id:
            new_qty = request.form.get('quantity', '0')
            try:
                new_qty_int = int(new_qty)
            except ValueError:
                new_qty_int = 0
            # Update cart.txt
            updated_cart = []
            for ci in cart_items:
                if ci['item_id'] == item_id:
                    if new_qty_int > 0:
                        ci['quantity'] = str(new_qty_int)
                        updated_cart.append(ci)
                    # else remove it by not adding
                else:
                    updated_cart.append(ci)
            filepath = os.path.join(DATA_DIR, 'cart.txt')
            with open(filepath, 'w', encoding='utf-8') as f:
                for ci in updated_cart:
                    f.write(f"{ci['cart_id']}|{ci['item_id']}|{ci['restaurant_id']}|{ci['quantity']}|{ci['added_date']}\n")
        elif action == 'remove_item' and item_id:
            updated_cart = [ci for ci in cart_items if ci['item_id'] != item_id]
            filepath = os.path.join(DATA_DIR, 'cart.txt')
            with open(filepath, 'w', encoding='utf-8') as f:
                for ci in updated_cart:
                    f.write(f"{ci['cart_id']}|{ci['item_id']}|{ci['restaurant_id']}|{ci['quantity']}|{ci['added_date']}\n")
        return redirect(url_for('shopping_cart'))

    for ci in cart_items:
        menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
        if not menu_item:
            continue
        qty = qty_to_int(ci['quantity'])
        price = menu_item['price']
        amount = qty * price
        total_amount += amount
        detailed_cart_items.append({
            'cart_id': ci['cart_id'],
            'item_id': ci['item_id'],
            'restaurant_id': ci['restaurant_id'],
            'quantity': qty,
            'item_name': menu_item['item_name'],
            'price': price,
            'amount': f'{amount:.2f}'
        })

    return render_template('cart.html', cart_items=detailed_cart_items, total_amount=f'{total_amount:.2f}')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        cart_items_raw = load_cart()
        menus = load_menus()
        cart_items = []
        total_amount = 0.0

        def qty_to_int(qty_str):
            try:
                return int(qty_str)
            except ValueError:
                return 0

        for ci in cart_items_raw:
            menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
            if not menu_item:
                continue
            qty = qty_to_int(ci['quantity'])
            price = menu_item['price']
            amount = qty * price
            total_amount += amount
            cart_items.append({
                'cart_id': ci['cart_id'],
                'item_id': ci['item_id'],
                'restaurant_id': ci['restaurant_id'],
                'quantity': qty,
                'item_name': menu_item['item_name'],
                'price': price,
                'amount': f'{amount:.2f}'
            })

        return render_template('checkout.html', cart_items=cart_items, total_amount=f'{total_amount:.2f}')
    else:
        # Process order placement form
        customer_name = request.form.get('customer_name', '').strip()
        delivery_address = request.form.get('delivery_address', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        # Basic input validation
        error_message = None
        if not customer_name:
            error_message = 'Please enter your name.'
        elif not delivery_address:
            error_message = 'Please enter your delivery address.'
        elif not phone_number:
            error_message = 'Please enter your phone number.'
        elif not payment_method:
            error_message = 'Please select a payment method.'

        cart_items = load_cart()
        menus = load_menus()

        if error_message:
            # Reload checkout page with error message
            return render_template('checkout.html', cart_items=[], total_amount='0.00', error=error_message)

        # Calculate total amount
        total_amount = 0.0
        for ci in cart_items:
            menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
            if menu_item:
                qty = int(ci['quantity'])
                total_amount += qty * menu_item['price']

        # Simulate order creation (No data persistence as per spec)
        # After placing order, clear cart
        filepath = os.path.join(DATA_DIR, 'cart.txt')
        open(filepath, 'w').close()

        confirmation_message = f'Thank you {customer_name}, your order has been placed!'

        return render_template('order_confirmation.html', message=confirmation_message)

@app.route('/active_orders', methods=['GET'])
def active_orders():
    orders = load_orders()
    status_filter = request.args.get('status', 'all').lower()
    if status_filter == 'all':
        filtered_orders = [o for o in orders if o['status'].lower() != 'delivered']
    else:
        filtered_orders = [o for o in orders if o['status'].lower() == status_filter]
    return render_template('active_orders.html', active_orders=filtered_orders, status_filter=status_filter)

@app.route('/track_order/<int:order_id>', methods=['GET'])
def order_tracking(order_id):
    orders = load_orders()
    order = next((o for o in orders if int(o['order_id']) == order_id), None)
    if not order:
        abort(404)
    deliveries = load_deliveries()
    delivery_information = next((d for d in deliveries if int(d['order_id']) == order_id), None)
    order_items = load_order_items()
    order_items_list = [oi for oi in order_items if int(oi['order_id']) == order_id]
    return render_template('order_tracking.html', order=order, delivery_information=delivery_information, order_items_list=order_items_list)

@app.route('/reviews', methods=['GET'])
def reviews():
    reviews = load_reviews()
    return render_template('reviews.html', reviews=reviews)

if __name__ == '__main__':
    app.run(debug=False, port=5000)
