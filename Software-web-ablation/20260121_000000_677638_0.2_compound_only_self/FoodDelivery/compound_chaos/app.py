from flask import Flask, render_template, request, redirect, url_for, abort
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

DATA_DIR = 'data'

# --- Helper functions for data loading and parsing ---

def load_restaurants():
    """Load restaurants from restaurants.txt as a list of dicts."""
    file_path = os.path.join(DATA_DIR, 'restaurants.txt')
    restaurants = []
    if not os.path.isfile(file_path):
        return restaurants
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 8:
                continue  # malformed line
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
    return restaurants


def load_menus():
    """Load menu items from menus.txt as a list of dicts."""
    file_path = os.path.join(DATA_DIR, 'menus.txt')
    menus = []
    if not os.path.isfile(file_path):
        return menus
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) !=7:
                continue
            try:
                menu_item = {
                    'item_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'item_name': parts[2],
                    'category': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': parts[6] in ['1', 'True', 'true']
                }
                menus.append(menu_item)
            except ValueError:
                continue
    return menus


def load_cart():
    """Load cart items from cart.txt as a list of dicts."""
    file_path = os.path.join(DATA_DIR, 'cart.txt')
    cart = []
    if not os.path.isfile(file_path):
        return cart
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=5:
                continue
            try:
                cart_item = {
                    'cart_id': int(parts[0]),
                    'item_id': int(parts[1]),
                    'restaurant_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'added_date': parts[4]  # as string, date in format YYYY-MM-DD
                }
                cart.append(cart_item)
            except ValueError:
                continue
    return cart


def load_orders():
    """Load orders from orders.txt as a list of dicts."""
    file_path = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    if not os.path.isfile(file_path):
        return orders
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=8:
                continue
            try:
                order = {
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'restaurant_id': int(parts[2]),
                    'order_date': parts[3],  # as string YYYY-MM-DD
                    'total_amount': float(parts[4]),
                    'status': parts[5],
                    'delivery_address': parts[6],
                    'phone_number': parts[7]
                }
                orders.append(order)
            except ValueError:
                continue
    return orders


def load_order_items():
    """Load order items from order_items.txt as a list of dicts."""
    file_path = os.path.join(DATA_DIR, 'order_items.txt')
    order_items = []
    if not os.path.isfile(file_path):
        return order_items
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=5:
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
    return order_items


def load_deliveries():
    """Load delivery info from deliveries.txt as a list of dicts."""
    file_path = os.path.join(DATA_DIR, 'deliveries.txt')
    deliveries = []
    if not os.path.isfile(file_path):
        return deliveries
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=7:
                continue
            try:
                delivery = {
                    'delivery_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'driver_name': parts[2],
                    'driver_phone': parts[3],
                    'vehicle_info': parts[4],
                    'status': parts[5],
                    'estimated_time': parts[6]  # datetime string
                }
                deliveries.append(delivery)
            except ValueError:
                continue
    return deliveries


def load_reviews():
    """Load reviews from reviews.txt as a list of dicts."""
    file_path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    if not os.path.isfile(file_path):
        return reviews
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts)!=6:
                continue
            try:
                review = {
                    'review_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]  # string date
                }
                reviews.append(review)
            except ValueError:
                continue
    return reviews


# --- ROUTE IMPLEMENTATIONS ---

# 1. `/` - redirect_to_dashboard
@app.route('/')
def redirect_to_dashboard():
    return redirect(url_for('show_dashboard'))

# 2. `/dashboard` - show_dashboard
@app.route('/dashboard')
def show_dashboard():
    restaurants = load_restaurants()
    featured_restaurants = sorted(restaurants, key=lambda x: x['rating'], reverse=True)[:3]
    popular_cuisines = sorted({r['cuisine'] for r in restaurants})
    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=popular_cuisines)

# 3. `/restaurants` - list_restaurants
@app.route('/restaurants')
def list_restaurants():
    restaurants = load_restaurants()
    search_query = request.args.get('search_query', '').strip()
    cuisine_filter = request.args.get('cuisine_filter', '').strip()

    filtered_restaurants = restaurants
    if search_query:
        filtered_restaurants = [r for r in filtered_restaurants if (search_query.lower() in r['name'].lower()) or (search_query.lower() in r['cuisine'].lower())]
    if cuisine_filter:
        filtered_restaurants = [r for r in filtered_restaurants if r['cuisine'].lower() == cuisine_filter.lower()]

    return render_template('restaurants.html', restaurants=filtered_restaurants, search_query=search_query, cuisine_filter=cuisine_filter)

# 4. `/restaurants/<int:restaurant_id>/menu` - show_menu
@app.route('/restaurants/<int:restaurant_id>/menu')
def show_menu(restaurant_id):
    restaurants = load_restaurants()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        abort(404)
    menus = load_menus()
    menu_items = [item for item in menus if item['restaurant_id'] == restaurant_id and item['availability']]
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

# 5. `/items/<int:item_id>` - show_item_details
@app.route('/items/<int:item_id>')
def show_item_details(item_id):
    menus = load_menus()
    item = next((i for i in menus if i['item_id'] == item_id), None)
    if not item:
        abort(404)
    return render_template('item_details.html', item=item)

# 6. `/cart` - show_cart
@app.route('/cart')
def show_cart():
    cart_items_raw = load_cart()
    menus = load_menus()
    cart_items = []
    total_amount = 0.0
    for c in cart_items_raw:
        menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
        if menu_item:
            item_total = menu_item['price'] * c['quantity']
            total_amount += item_total
            item_detail = {
                'item_id': menu_item['item_id'],
                'item_name': menu_item['item_name'],
                'quantity': c['quantity'],
                'price': menu_item['price'],
                'total': item_total
            }
            cart_items.append(item_detail)
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

# 7. `/cart/add/<int:item_id>` - add_to_cart
@app.route('/cart/add/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    cart = load_cart()
    menus = load_menus()
    menu_item = next((m for m in menus if m['item_id'] == item_id and m['availability']), None)
    if not menu_item:
        abort(404)
    # parse quantity optionally
    quantity_str = request.form.get('quantity', '1')
    try:
        quantity = int(quantity_str)
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    found = False
    for c in cart:
        if c['item_id'] == item_id:
            c['quantity'] += quantity
            found = True
            break
    if not found:
        new_cart_id = max([c['cart_id'] for c in cart], default=0) + 1
        today_str = datetime.now().strftime('%Y-%m-%d')
        cart.append({
            'cart_id': new_cart_id,
            'item_id': item_id,
            'restaurant_id': menu_item['restaurant_id'],
            'quantity': quantity,
            'added_date': today_str
        })
    write_cart(cart)
    return redirect(url_for('show_cart'))

# 8. `/cart/update/<int:item_id>` - update_cart_quantity
@app.route('/cart/update/<int:item_id>', methods=['POST'])
def update_cart_quantity(item_id):
    quantity_str = request.form.get('quantity', '').strip()
    try:
        quantity = int(quantity_str)
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        return abort(400)

    cart = load_cart()
    updated = False
    new_cart = []
    for c in cart:
        if c['item_id'] == item_id:
            if quantity > 0:
                c['quantity'] = quantity
                new_cart.append(c)
            updated = True
        else:
            new_cart.append(c)
    if not updated:
        abort(404)
    write_cart(new_cart)
    return redirect(url_for('show_cart'))

# 9. `/cart/remove/<int:item_id>` - remove_from_cart
@app.route('/cart/remove/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart = load_cart()
    new_cart = [c for c in cart if c['item_id'] != item_id]
    if len(new_cart) == len(cart):
        abort(404)
    write_cart(new_cart)
    return redirect(url_for('show_cart'))

# 10. `/checkout` - show checkout form on GET, process order on POST
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        return render_template('checkout.html')
    else:
        customer_name = request.form.get('customer_name', '').strip()
        delivery_address = request.form.get('delivery_address', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        payment_method = request.form.get('payment_method', '').strip()

        if not customer_name or not delivery_address or not phone_number or not payment_method:
            return abort(400)

        cart_items_raw = load_cart()
        if not cart_items_raw:
            return abort(400)

        menus = load_menus()
        total_amount = 0.0
        order_items = []
        unique_restaurant_ids = set()

        for c in cart_items_raw:
            menu_item = next((m for m in menus if m['item_id'] == c['item_id']), None)
            if not menu_item:
                continue
            total_amount += menu_item['price'] * c['quantity']
            order_items.append({
                'item_id': c['item_id'],
                'quantity': c['quantity'],
                'price': menu_item['price']
            })
            unique_restaurant_ids.add(menu_item['restaurant_id'])

        restaurant_id_for_order = next(iter(unique_restaurant_ids), 0)

        orders = load_orders()
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1
        today_str = datetime.now().strftime('%Y-%m-%d')

        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'restaurant_id': restaurant_id_for_order,
            'order_date': today_str,
            'total_amount': total_amount,
            'status': 'Pending',
            'delivery_address': delivery_address,
            'phone_number': phone_number
        }

        try:
            save_order(new_order)
            save_order_items(new_order_id, order_items)
            clear_cart()
        except Exception:
            abort(500)

        return render_template('order_confirmation.html', cart_items=order_items, total_amount=total_amount, order_confirmation=new_order)

# 11. `/orders` - list_active_orders
@app.route('/orders')
def list_active_orders():
    status_filter = request.args.get('status_filter', '').strip()
    orders = load_orders()
    if status_filter:
        filtered_orders = [o for o in orders if o['status'].lower() == status_filter.lower()]
    else:
        filtered_orders = orders
    return render_template('active_orders.html', active_orders=filtered_orders, status_filter=status_filter)

# 12. `/tracking/<int:order_id>` - track_order
@app.route('/tracking/<int:order_id>')
def track_order(order_id):
    orders = load_orders()
    order_details = next((o for o in orders if o['order_id'] == order_id), None)
    if not order_details:
        abort(404)
    deliveries = load_deliveries()
    delivery_driver_info = next((d for d in deliveries if d['order_id'] == order_id), None)

    # Load order items for this order with item names
    order_items_data = load_order_items()
    menus = load_menus()
    items = []
    for oi in order_items_data:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            item_name = menu_item['item_name'] if menu_item else 'Unknown Item'
            items.append({'item_name': item_name, 'quantity': oi['quantity']})

    estimated_time = delivery_driver_info['estimated_time'] if delivery_driver_info else '-'

    # Add items list to order_details dict for template display
    order_details = dict(order_details)  # make copy to not modify original
    order_details['items'] = items

    return render_template('tracking.html', order_details=order_details, delivery_driver_info=delivery_driver_info or {}, estimated_time=estimated_time)

# 13. `/reviews` - show_reviews
@app.route('/reviews')
def show_reviews():
    rating_filter = request.args.get('rating_filter', '').strip()
    reviews = load_reviews()
    if rating_filter:
        try:
            rating_filter_int = int(rating_filter)
            filtered_reviews = [r for r in reviews if r['rating'] == rating_filter_int]
        except ValueError:
            filtered_reviews = reviews
    else:
        filtered_reviews = reviews

    # Include restaurant names for reviews
    restaurants = load_restaurants()
    rest_dict = {r['restaurant_id']: r['name'] for r in restaurants}
    for review in filtered_reviews:
        review['restaurant_name'] = rest_dict.get(review['restaurant_id'], 'Unknown')

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter=rating_filter)

# 14. `/reviews/write` - write_review
@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    if request.method == 'GET':
        return render_template('write_review.html')
    else:
        try:
            restaurant_id_str = request.form.get('restaurant_id', '').strip()
            customer_name = request.form.get('customer_name', '').strip()
            rating_str = request.form.get('rating', '').strip()
            review_text = request.form.get('review_text', '').strip()

            restaurant_id = int(restaurant_id_str)
            rating = int(rating_str)

            if not customer_name or not review_text or rating < 1 or rating > 5:
                return abort(400)

            reviews = load_reviews()
            new_review_id = max([r['review_id'] for r in reviews], default=0) + 1
            today_str = datetime.now().strftime('%Y-%m-%d')

            new_review = {
                'review_id': new_review_id,
                'restaurant_id': restaurant_id,
                'customer_name': customer_name,
                'rating': rating,
                'review_text': review_text,
                'review_date': today_str
            }

            save_review(new_review)
            return redirect(url_for('show_reviews'))
        except (ValueError, TypeError):
            return abort(400)


# --- SAVE FUNCTIONS ---

def write_cart(cart_items):
    file_path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for c in cart_items:
                line = f"{c['cart_id']}|{c['item_id']}|{c['restaurant_id']}|{c['quantity']}|{c['added_date']}\n"
                f.write(line)
    except Exception:
        pass


def save_order(order):
    file_path = os.path.join(DATA_DIR, 'orders.txt')
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            line = f"{order['order_id']}|{order['customer_name']}|{order['restaurant_id']}|{order['order_date']}|{order['total_amount']}|{order['status']}|{order['delivery_address']}|{order['phone_number']}\n"
            f.write(line)
    except Exception:
        raise


def save_order_items(order_id, order_items):
    file_path = os.path.join(DATA_DIR, 'order_items.txt')
    existing_items = load_order_items()
    max_item_id = max([oi['order_item_id'] for oi in existing_items], default=0)
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            for oi in order_items:
                max_item_id += 1
                line = f"{max_item_id}|{order_id}|{oi['item_id']}|{oi['quantity']}|{oi['price']}\n"
                f.write(line)
    except Exception:
        raise


def clear_cart():
    file_path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('')
    except Exception:
        pass


def save_review(review):
    file_path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            line = f"{review['review_id']}|{review['restaurant_id']}|{review['customer_name']}|{review['rating']}|{review['review_text']}|{review['review_date']}\n"
            f.write(line)
    except Exception:
        raise


if __name__ == '__main__':
    app.run(debug=True, port=5000)
