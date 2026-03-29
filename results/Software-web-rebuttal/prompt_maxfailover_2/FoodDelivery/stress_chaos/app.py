from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

DATA_DIR = 'data'
RESTAURANTS_FILE = os.path.join(DATA_DIR, 'restaurants.txt')
MENUS_FILE = os.path.join(DATA_DIR, 'menus.txt')
CART_FILE = os.path.join(DATA_DIR, 'cart.txt')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.txt')
ORDER_ITEMS_FILE = os.path.join(DATA_DIR, 'order_items.txt')
DELIVERIES_FILE = os.path.join(DATA_DIR, 'deliveries.txt')
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.txt')

# Helper functions

def load_restaurants():
    restaurants = []
    try:
        with open(RESTAURANTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
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
    except IOError:
        pass
    return restaurants


def load_menus():
    menus = []
    try:
        with open(MENUS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
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
    except IOError:
        pass
    return menus


def load_cart():
    cart_items = []
    try:
        with open(CART_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                cart_item = {
                    'cart_id': int(parts[0]),
                    'item_id': int(parts[1]),
                    'restaurant_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'added_date': parts[4]
                }
                cart_items.append(cart_item)
    except IOError:
        pass
    return cart_items


def save_cart(cart_items):
    try:
        with open(CART_FILE, 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = f"{item['cart_id']}|{item['item_id']}|{item['restaurant_id']}|{item['quantity']}|{item['added_date']}\n"
                f.write(line)
    except IOError:
        pass


def load_orders():
    orders = []
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
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
    except IOError:
        pass
    return orders


def load_order_items():
    order_items = []
    try:
        with open(ORDER_ITEMS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                order_item = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'item_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(order_item)
    except IOError:
        pass
    return order_items


def load_deliveries():
    deliveries = []
    try:
        with open(DELIVERIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
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
    except IOError:
        pass
    return deliveries


def load_reviews():
    reviews = []
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
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
    except IOError:
        pass
    return reviews

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    cuisine_counts = {}
    for r in restaurants:
        cuisine_counts[r['cuisine']] = cuisine_counts.get(r['cuisine'], 0) + 1
    popular_cuisines = sorted(cuisine_counts, key=cuisine_counts.get, reverse=True)

    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=popular_cuisines)

@app.route('/restaurants')
def restaurants():
    restaurants = load_restaurants()
    cuisine_options = sorted({r['cuisine'] for r in restaurants})

    selected_cuisine = request.args.get('cuisine', '')
    search_query = request.args.get('search_query', '').lower()

    filtered_restaurants = restaurants
    if selected_cuisine:
        filtered_restaurants = [r for r in filtered_restaurants if r['cuisine'] == selected_cuisine]
    if search_query:
        filtered_restaurants = [r for r in filtered_restaurants if search_query in r['name'].lower()]

    return render_template('restaurants.html', restaurants=filtered_restaurants, cuisine_options=cuisine_options, selected_cuisine=selected_cuisine, search_query=search_query)

@app.route('/restaurant/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        return "Restaurant not found", 404

    menus = load_menus()
    menu_items = [item for item in menus if item['restaurant_id'] == restaurant_id]

    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_details(item_id):
    menus = load_menus()
    item = next((i for i in menus if i['item_id'] == item_id), None)
    if not item:
        return "Item not found", 404

    if request.method == 'POST':
        # Add to cart logic
        quantity_str = request.form.get('quantity', '1')
        try:
            quantity = int(quantity_str)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

        cart_items = load_cart()
        # Check if item already in cart
        existing_item = next((ci for ci in cart_items if ci['item_id'] == item_id), None)
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            new_cart_id = max([ci['cart_id'] for ci in cart_items], default=0) + 1
            added_date = datetime.now().strftime('%Y-%m-%d')
            new_cart_item = {
                'cart_id': new_cart_id,
                'item_id': item_id,
                'restaurant_id': item['restaurant_id'],
                'quantity': quantity,
                'added_date': added_date
            }
            cart_items.append(new_cart_item)
        save_cart(cart_items)
        return redirect(url_for('shopping_cart'))

    return render_template('item.html', item=item)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id_str = request.form.get('item_id')
    quantity_str = request.form.get('quantity', '1')

    try:
        item_id = int(item_id_str)
        quantity = int(quantity_str)
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        return redirect(url_for('shopping_cart'))

    menus = load_menus()
    item = next((i for i in menus if i['item_id'] == item_id), None)
    if not item:
        return redirect(url_for('shopping_cart'))

    cart_items = load_cart()
    existing_item = next((ci for ci in cart_items if ci['item_id'] == item_id), None)
    if existing_item:
        existing_item['quantity'] += quantity
    else:
        new_cart_id = max([ci['cart_id'] for ci in cart_items], default=0) + 1
        added_date = datetime.now().strftime('%Y-%m-%d')
        new_cart_item = {
            'cart_id': new_cart_id,
            'item_id': item_id,
            'restaurant_id': item['restaurant_id'],
            'quantity': quantity,
            'added_date': added_date
        }
        cart_items.append(new_cart_item)
    save_cart(cart_items)
    return redirect(url_for('shopping_cart'))

@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_items = load_cart()
    menus = load_menus()

    if request.method == 'POST':
        # Handle remove and update quantity actions
        form_keys = list(request.form.keys())
        new_cart_items = cart_items.copy()
        action_handled = False

        # Remove item from cart
        for key in form_keys:
            if key.startswith('remove-item-button-'):
                try:
                    item_id = int(key.replace('remove-item-button-', ''))
                    new_cart_items = [ci for ci in new_cart_items if ci['item_id'] != item_id]
                    action_handled = True
                except ValueError:
                    pass

        # Update quantity
        for key in form_keys:
            if key.startswith('update-quantity-'):
                try:
                    item_id = int(key.replace('update-quantity-', ''))
                    quantity_str = request.form.get(key, '1')
                    quantity = int(quantity_str)
                    if quantity <= 0:
                        new_cart_items = [ci for ci in new_cart_items if ci['item_id'] != item_id]
                    else:
                        for ci in new_cart_items:
                            if ci['item_id'] == item_id:
                                ci['quantity'] = quantity
                    action_handled = True
                except ValueError:
                    pass

        if action_handled:
            save_cart(new_cart_items)
            return redirect(url_for('shopping_cart'))

    detailed_cart_items = []
    total_amount = 0.0
    for ci in cart_items:
        menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
        if menu_item:
            subtotal = menu_item['price'] * ci['quantity']
            total_amount += subtotal
            detailed_cart_items.append({
                'cart_id': ci['cart_id'],
                'item_id': ci['item_id'],
                'restaurant_id': ci['restaurant_id'],
                'item_name': menu_item['item_name'],
                'quantity': ci['quantity'],
                'price': menu_item['price'],
                'subtotal': subtotal
            })

    return render_template('cart.html', cart_items=detailed_cart_items, total_amount=total_amount)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form_fields = ['customer_name', 'delivery_address', 'phone_number', 'payment_method']
    errors = {}
    order_form = {field: '' for field in form_fields}

    if request.method == 'POST':
        for field in form_fields:
            order_form[field] = request.form.get(field, '').strip()
            if not order_form[field]:
                errors[field] = f'{field.replace("_", " ").capitalize()} is required.'

        cart_items = load_cart()
        if len(cart_items) == 0:
            errors['cart'] = 'Your cart is empty. Please add items before checkout.'

        if errors:
            return render_template('checkout.html', order_form=order_form, errors=errors)

        orders = load_orders()
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1

        # Check all items belong to same restaurant
        cart_restaurants = {ci['restaurant_id'] for ci in cart_items}
        if len(cart_restaurants) != 1:
            errors['cart'] = 'All items in cart must be from the same restaurant to proceed.'
            return render_template('checkout.html', order_form=order_form, errors=errors)

        restaurant_id = cart_restaurants.pop()
        order_date = datetime.now().strftime('%Y-%m-%d')
        total = 0
        menus = load_menus()
        for ci in cart_items:
            menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
            if menu_item:
                total += menu_item['price'] * ci['quantity']

        new_order = {
            'order_id': new_order_id,
            'customer_name': order_form['customer_name'],
            'restaurant_id': restaurant_id,
            'order_date': order_date,
            'total_amount': total,
            'status': 'Pending',
            'delivery_address': order_form['delivery_address'],
            'phone_number': order_form['phone_number']
        }

        try:
            with open(ORDERS_FILE, 'a', encoding='utf-8') as f:
                line = f"{new_order['order_id']}|{new_order['customer_name']}|{new_order['restaurant_id']}|{new_order['order_date']}|{new_order['total_amount']:.2f}|{new_order['status']}|{new_order['delivery_address']}|{new_order['phone_number']}\n"
                f.write(line)
        except IOError:
            errors['file'] = 'Failed to save order. Please try again later.'
            return render_template('checkout.html', order_form=order_form, errors=errors)

        order_items = load_order_items()
        new_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0) + 1
        try:
            with open(ORDER_ITEMS_FILE, 'a', encoding='utf-8') as f:
                for ci in cart_items:
                    menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
                    if menu_item:
                        line = f"{new_order_item_id}|{new_order['order_id']}|{menu_item['item_id']}|{ci['quantity']}|{menu_item['price']:.2f}\n"
                        f.write(line)
                        new_order_item_id += 1
        except IOError:
            errors['file'] = 'Failed to save order items. Please try again later.'
            return render_template('checkout.html', order_form=order_form, errors=errors)

        # Clear cart after order
        try:
            with open(CART_FILE, 'w', encoding='utf-8') as f:
                pass
        except IOError:
            pass

        return redirect(url_for('active_orders'))

    return render_template('checkout.html', order_form=order_form, errors=errors)

@app.route('/orders/active', methods=['GET', 'POST'])
def active_orders():
    orders = load_orders()
    status_options = sorted({o['status'] for o in orders})
    selected_status = request.args.get('status_filter', 'All')

    if selected_status == 'All':
        filtered_orders = orders
    else:
        filtered_orders = [o for o in orders if o['status'] == selected_status]

    return render_template('active_orders.html', active_orders=filtered_orders, status_options=status_options, selected_status=selected_status)

@app.route('/orders/track/<int:order_id>')
def order_tracking(order_id):
    orders = load_orders()
    deliveries = load_deliveries()
    order_items_data = load_order_items()
    menus = load_menus()

    order_details = next((o for o in orders if o['order_id'] == order_id), None)
    if not order_details:
        return "Order not found", 404

    delivery_driver = next((d for d in deliveries if d['order_id'] == order_id), None)
    estimated_time = delivery_driver['estimated_time'] if delivery_driver else ''

    order_items = []
    for oi in order_items_data:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                item_dict = {
                    'order_item_id': oi['order_item_id'],
                    'item_id': oi['item_id'],
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                }
                order_items.append(item_dict)

    return render_template('order_tracking.html', order_details=order_details, delivery_driver=delivery_driver, estimated_time=estimated_time, order_items=order_items)

@app.route('/reviews')
def reviews():
    reviews_data = load_reviews()
    rating_filter_options = ['All', '5', '4', '3', '2', '1']
    selected_rating_filter = request.args.get('rating_filter', 'All')

    if selected_rating_filter == 'All':
        filtered_reviews = reviews_data
    else:
        try:
            rating_val = int(selected_rating_filter)
            filtered_reviews = [r for r in reviews_data if r['rating'] == rating_val]
        except ValueError:
            filtered_reviews = reviews_data

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter_options=rating_filter_options, selected_rating_filter=selected_rating_filter)

if __name__ == '__main__':
    app.run(port=5000)
