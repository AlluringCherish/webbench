from flask import Flask, render_template, redirect, url_for, request, abort
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

# Data file paths
RESTAURANTS_FILE = 'data/restaurants.txt'
MENUS_FILE = 'data/menus.txt'
CART_FILE = 'data/cart.txt'
ORDERS_FILE = 'data/orders.txt'
ORDER_ITEMS_FILE = 'data/order_items.txt'
DELIVERIES_FILE = 'data/deliveries.txt'
REVIEWS_FILE = 'data/reviews.txt'

# Helper loading functions

def load_restaurants():
    restaurants = []
    try:
        with open(RESTAURANTS_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        # Graceful fallback to empty list
        pass
    return restaurants


def load_menus():
    menus = []
    try:
        with open(MENUS_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return menus


def load_cart():
    cart_items = []
    try:
        with open(CART_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return cart_items


def load_orders():
    orders = []
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return orders


def load_order_items():
    order_items = []
    try:
        with open(ORDER_ITEMS_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return order_items


def load_deliveries():
    deliveries = []
    try:
        with open(DELIVERIES_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return deliveries


def load_reviews():
    reviews = []
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        pass
    return reviews


# Root redirect route
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

# /dashboard GET
@app.route('/dashboard')
def dashboard():
    restaurants = load_restaurants()
    featured_restaurants = [r for r in restaurants if r['rating'] >= 4.5]
    featured_restaurants.sort(key=lambda x: x['rating'], reverse=True)
    popular_cuisines = sorted(list({r['cuisine'] for r in restaurants}))
    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=popular_cuisines)

# /restaurants GET
@app.route('/restaurants')
def restaurant_listing():
    restaurants = load_restaurants()
    cuisine_options = sorted(list({r['cuisine'] for r in restaurants}))
    return render_template('restaurants.html', restaurants=restaurants, cuisine_options=cuisine_options)

# /menu/<int:restaurant_id> GET
@app.route('/menu/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        abort(404)
    menus = load_menus()
    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability'] == 1]
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

# /item/<int:item_id> GET
@app.route('/item/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id), None)
    if not item:
        abort(404)
    return render_template('item_details.html', item=item)

# Implemented add_to_cart route to fix missing endpoint
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Form fields: item_id and quantity
    item_id = request.form.get('item_id')
    quantity_str = request.form.get('quantity', '1')
    if not item_id:
        abort(400)
    try:
        item_id = int(item_id)
    except ValueError:
        abort(400)
    try:
        quantity = int(quantity_str)
    except ValueError:
        quantity = 1
    if quantity < 1:
        quantity = 1
    cart_items = load_cart()
    existing_entry = next((c for c in cart_items if c['item_id'] == item_id), None)
    if existing_entry:
        existing_entry['quantity'] += quantity
    else:
        new_cart_id = max((c['cart_id'] for c in cart_items), default=0) + 1
        menus = load_menus()
        menu_item = next((m for m in menus if m['item_id'] == item_id), None)
        if not menu_item:
            abort(400)
        new_entry = {
            'cart_id': new_cart_id,
            'item_id': item_id,
            'restaurant_id': menu_item['restaurant_id'],
            'quantity': quantity,
            'added_date': datetime.now().strftime('%Y-%m-%d')
        }
        cart_items.append(new_entry)
    try:
        with open(CART_FILE, 'w', encoding='utf-8') as f:
            for c in cart_items:
                line = f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n"
                f.write(line)
    except Exception:
        abort(500)
    return redirect(url_for('shopping_cart'))

# /cart GET, POST
@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    if request.method == 'POST':
        return redirect(url_for('shopping_cart'))
    cart_items_raw = load_cart()
    menus = load_menus()
    cart_items = []
    total_amount = 0.0
    for ci in cart_items_raw:
        menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
        if not menu_item or menu_item['availability'] != 1:
            continue
        ci_dict = {
            'cart_id': ci['cart_id'],
            'item_id': ci['item_id'],
            'restaurant_id': ci['restaurant_id'],
            'quantity': ci['quantity'],
            'added_date': ci['added_date'],
            'item_name': menu_item['item_name'],
            'price': menu_item['price'],
            'description': menu_item['description'],
            'total_price': menu_item['price'] * ci['quantity']
        }
        total_amount += ci_dict['total_price']
        cart_items.append(ci_dict)
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

# /cart/update POST
@app.route('/cart/update', methods=['POST'])
def update_cart():
    cart_items = load_cart()
    form = request.form
    # Process removals (button named remove_item_id)
    if 'remove_item_id' in form:
        try:
            remove_item_id = int(form.get('remove_item_id'))
        except Exception:
            return abort(400)
        cart_items = [c for c in cart_items if c['item_id'] != remove_item_id]
    else:
        for c in cart_items[:]:
            quantity_field = f'quantity_{c["item_id"]}'
            if quantity_field in form:
                try:
                    qty = int(form.get(quantity_field))
                    if qty < 1:
                        cart_items = [x for x in cart_items if x['item_id'] != c['item_id']]
                    else:
                        c['quantity'] = qty
                except Exception:
                    return abort(400)
    try:
        with open(CART_FILE, 'w', encoding='utf-8') as f:
            for c in cart_items:
                line = f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n"
                f.write(line)
    except Exception:
        abort(500)
    return redirect(url_for('shopping_cart'))

# /checkout GET, POST
@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    if request.method == 'GET':
        return render_template('checkout.html')
    customer_name = request.form.get('customer_name', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    payment_method = request.form.get('payment_method', '').strip()
    errors = []
    if not customer_name:
        errors.append('Customer name is required.')
    if not delivery_address:
        errors.append('Delivery address is required.')
    if not phone_number:
        errors.append('Phone number is required.')
    if not payment_method:
        errors.append('Payment method is required.')
    cart_items = load_cart()
    if not cart_items:
        errors.append('Cart is empty. Please add items before checkout.')
    if errors:
        return render_template('checkout.html', errors=errors), 400
    menus = load_menus()
    total_amount = 0.0
    for ci in cart_items:
        menu_item = next((m for m in menus if m['item_id'] == ci['item_id'] and m['availability'] == 1), None)
        if not menu_item:
            errors.append(f"Item with id {ci['item_id']} is not available anymore.")
        else:
            total_amount += menu_item['price'] * ci['quantity']
    if errors:
        return render_template('checkout.html', errors=errors), 400
    orders = load_orders()
    new_order_id = max((o['order_id'] for o in orders), default=0) + 1
    restaurant_ids = set(ci['restaurant_id'] for ci in cart_items)
    if len(restaurant_ids) != 1:
        errors.append('All items in cart must be from the same restaurant for ordering.')
        return render_template('checkout.html', errors=errors), 400
    restaurant_id = restaurant_ids.pop()
    order_date = datetime.now().strftime('%Y-%m-%d')
    new_order = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'restaurant_id': restaurant_id,
        'order_date': order_date,
        'total_amount': total_amount,
        'status': 'Placed',
        'delivery_address': delivery_address,
        'phone_number': phone_number
    }
    orders.append(new_order)
    try:
        with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
            for o in orders:
                line = f"{o['order_id']}|{o['customer_name']}|{o['restaurant_id']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['delivery_address']}|{o['phone_number']}\n"
                f.write(line)
    except Exception:
        errors.append('Failed to save the order. Please try again later.')
        return render_template('checkout.html', errors=errors), 500
    order_items_all = load_order_items()
    max_order_item_id = max((oi['order_item_id'] for oi in order_items_all), default=0)
    menus_dict = {m['item_id']: m for m in load_menus()}
    for ci in cart_items:
        max_order_item_id += 1
        price_per_item = menus_dict[ci['item_id']]['price']
        order_item = {
            'order_item_id': max_order_item_id,
            'order_id': new_order_id,
            'item_id': ci['item_id'],
            'quantity': ci['quantity'],
            'price': price_per_item
        }
        order_items_all.append(order_item)
    try:
        with open(ORDER_ITEMS_FILE, 'w', encoding='utf-8') as f:
            for oi in order_items_all:
                line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']}\n"
                f.write(line)
    except Exception:
        errors.append('Failed to save order items. Please try again later.')
        return render_template('checkout.html', errors=errors), 500
    try:
        with open(CART_FILE, 'w', encoding='utf-8') as f:
            pass  # overwrite with empty content
    except Exception:
        pass
    confirmation_message = f"Order #{new_order_id} placed successfully."
    return render_template('checkout.html', confirmation_message=confirmation_message)

# /orders/active GET
@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    active_orders = [o for o in orders if o['status'].lower() not in ('delivered', 'cancelled')]
    status_filter_options = ['Placed', 'On the Way', 'Delivered', 'Cancelled']
    return render_template('active_orders.html', active_orders=active_orders, status_filter_options=status_filter_options)

# /orders/track/<int:order_id> GET
@app.route('/orders/track/<int:order_id>')
def order_tracking(order_id):
    orders = load_orders()
    order_details = next((o for o in orders if o['order_id'] == order_id), None)
    if not order_details:
        abort(404)
    deliveries = load_deliveries()
    delivery_driver_info = next((d for d in deliveries if d['order_id'] == order_id), None)
    if not delivery_driver_info:
        delivery_driver_info = {
            'driver_name': 'Not Assigned',
            'driver_phone': '',
            'vehicle_info': '',
            'status': 'Pending',
            'estimated_time': ''
        }
    estimated_time = delivery_driver_info.get('estimated_time', '')
    order_items_all = load_order_items()
    menus = load_menus()
    order_items = []
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if not menu_item:
                continue
            order_items.append({
                'item_id': oi['item_id'],
                'item_name': menu_item['item_name'],
                'quantity': oi['quantity'],
                'price': oi['price']
            })
    return render_template('tracking.html', order_details=order_details, delivery_driver_info=delivery_driver_info, estimated_time=estimated_time, order_items=order_items)

# /reviews GET
@app.route('/reviews')
def reviews_page():
    reviews = load_reviews()
    rating_filter_options = ['1', '2', '3', '4', '5']
    return render_template('reviews.html', reviews=reviews, rating_filter_options=rating_filter_options)

# /reviews/write GET, POST
@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    if request.method == 'GET':
        return render_template('write_review.html')
    try:
        restaurant_id_str = request.form.get('restaurant_id', '').strip()
        customer_name = request.form.get('customer_name', '').strip()
        rating_str = request.form.get('rating', '').strip()
        review_text = request.form.get('review_text', '').strip()
    except Exception:
        return render_template('write_review.html', error='Invalid form submission.'), 400
    errors = []
    try:
        restaurant_id = int(restaurant_id_str)
    except ValueError:
        errors.append('Invalid restaurant ID.')
        restaurant_id = None
    if not customer_name:
        errors.append('Customer name is required.')
    try:
        rating = int(rating_str)
        if rating < 1 or rating > 5:
            errors.append('Rating must be between 1 and 5.')
    except ValueError:
        errors.append('Rating must be an integer between 1 and 5.')
    if not review_text:
        errors.append('Review text is required.')
    if restaurant_id is not None:
        restaurants = load_restaurants()
        if not any(r['restaurant_id'] == restaurant_id for r in restaurants):
            errors.append('Restaurant does not exist.')
    if errors:
        return render_template('write_review.html', errors=errors), 400
    reviews = load_reviews()
    new_review_id = max((r['review_id'] for r in reviews), default=0) + 1
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
    try:
        with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
            for r in reviews:
                line = f"{r['review_id']}|{r['restaurant_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
                f.write(line)
    except Exception:
        return render_template('write_review.html', error='Failed to save review. Please try again later.'), 500
    confirmation_message = 'Review submitted successfully.'
    return render_template('write_review.html', confirmation_message=confirmation_message)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
