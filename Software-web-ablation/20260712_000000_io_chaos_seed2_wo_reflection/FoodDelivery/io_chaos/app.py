from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Load restaurants

def load_restaurants():
    filepath = os.path.join(DATA_DIR, 'restaurants.txt')
    restaurants = []
    try:
        with open(filepath, 'r', encoding='utf8') as f:
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
                    'delivery_time': parts[6],
                    'min_order': float(parts[7])
                }
                restaurants.append(restaurant)
    except FileNotFoundError:
        return []
    return restaurants

# Load menu items

def load_menu_items():
    filepath = os.path.join(DATA_DIR, 'menus.txt')
    menu_items = []
    try:
        with open(filepath, 'r', encoding='utf8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                item = {
                    'item_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'name': parts[2],  # Corrected to 'name'
                    'category': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': parts[6] == '1'
                }
                menu_items.append(item)
    except FileNotFoundError:
        return []
    return menu_items

# Load cart items

def load_cart_items():
    filepath = os.path.join(DATA_DIR, 'cart.txt')
    cart_items = []
    try:
        with open(filepath, 'r', encoding='utf8') as f:
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
    except FileNotFoundError:
        return []
    return cart_items

# Save cart items (overwrite)

def save_cart_items(cart_items):
    filepath = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(filepath, 'w', encoding='utf8') as f:
            for c in cart_items:
                line = f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n"
                f.write(line)
    except Exception as e:
        raise e

# Load orders

def load_orders():
    filepath = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    try:
        with open(filepath, 'r', encoding='utf8') as f:
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
    except FileNotFoundError:
        return []
    return orders

# Load order items

def load_order_items(order_id):
    filepath = os.path.join(DATA_DIR, 'order_items.txt')
    order_items = []
    try:
        with open(filepath, 'r', encoding='utf8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 5:
                    continue
                if int(parts[1]) == order_id:
                    item = {
                        'order_item_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'item_id': int(parts[2]),
                        'quantity': int(parts[3]),
                        'price': float(parts[4])
                    }
                    order_items.append(item)
    except FileNotFoundError:
        return []
    return order_items

# Load delivery info

def load_delivery_info(order_id):
    filepath = os.path.join(DATA_DIR, 'deliveries.txt')
    delivery_info = {}
    try:
        with open(filepath, 'r', encoding='utf8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 7:
                    continue
                if int(parts[1]) == order_id:
                    delivery_info = {
                        'delivery_id': int(parts[0]),
                        'order_id': int(parts[1]),
                        'driver_name': parts[2],
                        'driver_phone': parts[3],
                        'vehicle_info': parts[4],
                        'status': parts[5],
                        'estimated_time': parts[6]
                    }
                    break
    except FileNotFoundError:
        return {}
    return delivery_info

# Load reviews

def load_reviews():
    filepath = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    try:
        with open(filepath, 'r', encoding='utf8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 6:
                    continue
                review = {
                    'review_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'reviewer_name': parts[2],  # Corrected key from customer_name
                    'rating': int(parts[3]),
                    'comment': parts[4],  # Corrected key from review_text
                    'review_date': parts[5]
                }
                reviews.append(review)
    except FileNotFoundError:
        return []
    return reviews

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    feature_restaurants = restaurants  # Just use all for simplicity
    cuisines = sorted(set(r['cuisine'] for r in restaurants))
    return render_template('dashboard.html',
                           page_title='Food Delivery Dashboard',
                           feature_restaurants=feature_restaurants,
                           popular_cuisines=cuisines)

@app.route('/restaurants', methods=['GET', 'POST'])
def browse_restaurants():
    restaurants = load_restaurants()
    search_query = ''
    cuisine_filter = ''
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        cuisine_filter = request.form.get('cuisine_filter', '').strip()

        filtered = []
        for r in restaurants:
            if search_query.lower() in r['name'].lower() or search_query.lower() in r['cuisine'].lower() or search_query == '':
                if cuisine_filter == '' or r['cuisine'].lower() == cuisine_filter.lower():
                    filtered.append(r)
        restaurants = filtered
    return render_template('restaurant.html',
                           page_title='Browse Restaurants',
                           restaurants=restaurants,
                           search_query=search_query,
                           cuisine_filter=cuisine_filter)

@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        abort(404)
    menu_items = [item for item in load_menu_items() if item['restaurant_id'] == restaurant_id and item['availability']]
    return render_template('menu.html',
                           page_title='Restaurant Menu',
                           restaurante=restaurant,
                           menu_items=menu_items)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    menu_items = load_menu_items()
    item = next((i for i in menu_items if i['item_id'] == item_id), None)
    if not item:
        abort(404)
    return render_template('item_detail.html',
                           page_title='Item Details',
                           item=item)

@app.route('/cart')
def shopping_cart():
    cart_items = load_cart_items()
    total_amount = 0.0
    menu_items = load_menu_items()
    # Enhance cart items with name and price for template usage
    enhanced_cart_items = []
    for cart_item in cart_items:
        menu_item = next((m for m in menu_items if m['item_id'] == cart_item['item_id']), None)
        if menu_item:
            cart_item_enhanced = cart_item.copy()
            cart_item_enhanced['name'] = menu_item['name']
            cart_item_enhanced['price'] = menu_item['price']
            enhanced_cart_items.append(cart_item_enhanced)
            total_amount += menu_item['price'] * cart_item['quantity']
    total_amount = f"{total_amount:.2f}"
    return render_template('cart.html',
                           page_title='Shopping Cart',
                           cartitems=enhanced_cart_items,
                           total_amount=total_amount)

@app.route('/cart/update', methods=['POST'])
def update_cart_quantity():
    item_id_str = request.form.get('item_id', '')
    quantity_str = request.form.get('quantity', '')
    if not item_id_str.isdigit() or not quantity_str.isdigit():
        abort(400)
    item_id = int(item_id_str)
    quantity = int(quantity_str)

    cart_items = load_cart_items()
    menu_items = load_menu_items()

    found = False
    for c in cart_items:
        if c['item_id'] == item_id:
            if quantity <= 0:
                cart_items.remove(c)
            else:
                c['quantity'] = quantity
            found = True
            break
    if not found and quantity > 0:
        menu_item = next((m for m in menu_items if m['item_id'] == item_id), None)
        if menu_item:
            # Generate a new cart_id
            new_cart_id = 1
            if cart_items:
                new_cart_id = max(c['cart_id'] for c in cart_items) + 1
            cart_items.append({
                'cart_id': new_cart_id,
                'item_id': item_id,
                'restaurant_id': menu_item['restaurant_id'],
                'quantity': quantity,
                'added_date': datetime.now().strftime('%Y-%m-%d')
            })
    save_cart_items(cart_items)
    return redirect(url_for('shopping_cart'))

@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_cartitem(item_id):
    cart_items = load_cart_items()
    cart_items = [c for c in cart_items if c['item_id'] != item_id]
    save_cart_items(cart_items)
    return redirect(url_for('shopping_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout_html():
    cart_items = load_cart_items()
    menu_items = load_menu_items()
    enhanced_cart_items = []
    total_amount = 0.0
    for cart_item in cart_items:
        menu_item = next((m for m in menu_items if m['item_id'] == cart_item['item_id']), None)
        if menu_item:
            cart_item_enhanced = cart_item.copy()
            cart_item_enhanced['name'] = menu_item['name']
            cart_item_enhanced['price'] = menu_item['price']
            enhanced_cart_items.append(cart_item_enhanced)
            total_amount += menu_item['price'] * cart_item['quantity']
    total_amount_str = f"{total_amount:.2f}"

    errors = {}
    form_submit_status = False

    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if customer_name == '':
            errors['customer_name'] = 'Customer name is required.'
        if address == '':
            errors['address'] = 'Address is required.'
        if phone == '':
            errors['phone'] = 'Phone number is required.'
        if payment_method not in ['Credit Card', 'Cash', 'PayPal']:
            errors['payment_method'] = 'Valid payment method is required.'

        if not errors:
            # Pretend saving order
            cart_items.clear()
            save_cart_items(cart_items)
            form_submit_status = True

    return render_template('checkout.html',
                           page_title='Checkout',
                           cart_items=enhanced_cart_items,
                           total_amount=total_amount_str,
                           form_submit_status=form_submit_status,
                           errors=errors)

@app.route('/orders/active')
def active_order():
    orders = load_orders()
    status_filter = request.args.get('status_filter', '').strip()
    filtered_orders = orders
    if status_filter:
        filtered_orders = [o for o in orders if o['status'].lower() == status_filter.lower()]
    return render_template('active_orders.html',
                           page_title='Active Orders',
                           active_orders=filtered_orders,
                           status_filter=status_filter)

@app.route('/track/<int:order_id>')
def track_orders(order_id):
    orders = load_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        abort(404)
    delivery_info = load_delivery_info(order_id)
    order_items_raw = load_order_items(order_id)

    menu_items = load_menu_items()
    order_items = []
    for oi in order_items_raw:
        menu_item = next((m for m in menu_items if m['item_id'] == oi['item_id']), None)
        if menu_item:
            order_items.append({
                'item_id': oi['item_id'],
                'name': menu_item['name'],
                'quantity': oi['quantity']
            })

    return render_template('trackorder.html',
                           page_title='Track Order',
                           order=order,
                           delivery_info=delivery_info,
                           order_items=order_items)

@app.route('/reviews')
def reviews():
    reviews = load_reviews()
    filter_ratings = request.args.get('filter_ratings', '').strip()
    filtered_reviews = reviews
    if filter_ratings:
        try:
            rating_val = int(filter_ratings)
            filtered_reviews = [r for r in reviews if r['rating'] >= rating_val]
        except ValueError:
            filtered_reviews = reviews
    return render_template('reviews.html',
                           page_title='Order Reviews',
                           reviews=filtered_reviews,
                           filter_ratings=filter_ratings)

@app.route('/reviews/write', methods=['GET', 'POST'])
def writ_review():
    submission_status = None
    errors = {}
    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment', '').strip()
        if not rating or not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            errors['rating'] = 'Rating must be an integer between 1 and 5.'
        if comment == '':
            errors['comment'] = 'Comment is required.'

        if not errors:
            try:
                filepath = os.path.join(DATA_DIR, 'reviews.txt')
                reviews_list = load_reviews()
                new_id = max((r['review_id'] for r in reviews_list), default=0) + 1
                user_name = request.form.get('reviewer_name', '').strip()
                review_line = f"{new_id}|0|{user_name}|{rating}|{comment}|{datetime.now().strftime('%Y-%m-%d')}"
                with open(filepath, 'a', encoding='utf8') as f:
                    f.write(review_line + '\n')
                submission_status = 1
            except Exception:
                submission_status = 0
        else:
            submission_status = 0

    return render_template('write_reviews.html',
                           page_title='Write Review',
                           submission_status=submission_status,
                           errors=errors)

if __name__ == '__main__':
    app.run(debug=False, port=5000)
