from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Utility functions to load data from files

def load_restaurants():
    path = os.path.join(DATA_DIR, 'restaurants.txt')
    restaurants = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
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
        pass
    return restaurants


def load_menus():
    path = os.path.join(DATA_DIR, 'menus.txt')
    menus = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                item = {
                    'item_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'item_name': parts[2],
                    'category': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': int(parts[6])  # 1=available, 0=unavailable
                }
                menus.append(item)
    except FileNotFoundError:
        pass
    return menus


def load_cart():
    path = os.path.join(DATA_DIR, 'cart.txt')
    cart_items = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                cart_item = {
                    'cart_id': int(parts[0]),
                    'item_id': int(parts[1]),
                    'restaurant_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'added_date': parts[4]  # string yyyy-MM-dd
                }
                cart_items.append(cart_item)
    except FileNotFoundError:
        pass
    return cart_items


def save_cart(cart_items):
    path = os.path.join(DATA_DIR, 'cart.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for ci in cart_items:
                line = f"{ci['cart_id']}|{ci['item_id']}|{ci['restaurant_id']}|{ci['quantity']}|{ci['added_date']}\n"
                f.write(line)
    except Exception:
        pass


def load_orders():
    path = os.path.join(DATA_DIR, 'orders.txt')
    orders = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                order = {
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'restaurant_id': int(parts[2]),
                    'order_date': parts[3],  # yyyy-MM-dd
                    'total_amount': float(parts[4]),
                    'status': parts[5],  # Preparing, On the Way, Delivered
                    'delivery_address': parts[6],
                    'phone_number': parts[7]
                }
                orders.append(order)
    except FileNotFoundError:
        pass
    return orders


def save_orders(orders):
    path = os.path.join(DATA_DIR, 'orders.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for o in orders:
                line = f"{o['order_id']}|{o['customer_name']}|{o['restaurant_id']}|{o['order_date']}|{o['total_amount']}|{o['status']}|{o['delivery_address']}|{o['phone_number']}\n"
                f.write(line)
    except Exception:
        pass


def load_order_items():
    path = os.path.join(DATA_DIR, 'order_items.txt')
    order_items = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                oi = {
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'item_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                }
                order_items.append(oi)
    except FileNotFoundError:
        pass
    return order_items


def save_order_items(order_items):
    path = os.path.join(DATA_DIR, 'order_items.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for oi in order_items:
                line = f"{oi['order_item_id']}|{oi['order_id']}|{oi['item_id']}|{oi['quantity']}|{oi['price']}\n"
                f.write(line)
    except Exception:
        pass


def load_deliveries():
    path = os.path.join(DATA_DIR, 'deliveries.txt')
    deliveries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
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
                    'estimated_time': parts[6]  # yyyy-MM-dd HH:mm
                }
                deliveries.append(delivery)
    except FileNotFoundError:
        pass
    return deliveries


def load_reviews():
    path = os.path.join(DATA_DIR, 'reviews.txt')
    reviews = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
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
                    'review_date': parts[5]  # yyyy-MM-dd
                }
                reviews.append(review)
    except FileNotFoundError:
        pass
    return reviews


def save_reviews(reviews):
    path = os.path.join(DATA_DIR, 'reviews.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for r in reviews:
                line = f"{r['review_id']}|{r['restaurant_id']}|{r['customer_name']}|{r['rating']}|{r['review_text']}|{r['review_date']}\n"
                f.write(line)
    except Exception:
        pass


# Root route redirect
@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


# Dashboard page
@app.route('/dashboard')
def dashboard_page():
    restaurants = load_restaurants()
    # Featured restaurants: Let's choose top 3 by rating descending
    featured_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)[:3]
    # Popular cuisines from all restaurants (unique)
    cuisines = sorted(list({r['cuisine'] for r in restaurants}))

    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=cuisines)


# Restaurants listing
@app.route('/restaurants')
def restaurant_listing():
    restaurants = load_restaurants()
    cuisines = sorted(list({r['cuisine'] for r in restaurants}))

    # The search and filter UI are placeholders; backend filtering not implemented as per requirements

    return render_template('restaurants.html', restaurants=restaurants, cuisines=cuisines)


# Restaurant menu page
@app.route('/menu/<int:restaurant_id>', methods=['GET', 'POST'])
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()

    # Find restaurant
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        abort(404)  # not found

    # Menu items for this restaurant with availability=1
    menu_items = [item for item in menus if item['restaurant_id'] == restaurant_id and item['availability'] == 1]

    if request.method == 'POST':
        # Add to cart from menu page
        try:
            item_id = int(request.form.get('item_id', ''))
        except ValueError:
            abort(400)

        item = next((i for i in menu_items if i['item_id'] == item_id), None)
        if not item:
            abort(400)

        cart_items = load_cart()
        cart_item = next((c for c in cart_items if c['item_id'] == item_id), None)
        if cart_item:
            cart_item['quantity'] += 1
        else:
            new_cart_id = max([c['cart_id'] for c in cart_items], default=0) + 1
            today_str = datetime.now().strftime('%Y-%m-%d')
            cart_items.append({
                'cart_id': new_cart_id,
                'item_id': item['item_id'],
                'restaurant_id': item['restaurant_id'],
                'quantity': 1,
                'added_date': today_str
            })
        save_cart(cart_items)

        return redirect(url_for('shopping_cart'))

    return render_template('restaurant_menu.html', restaurant=restaurant, menu_items=menu_items)


# Item details page
@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_details_page(item_id):
    menus = load_menus()
    item = next((i for i in menus if i['item_id'] == item_id and i['availability'] == 1), None)
    if not item:
        abort(404)  # item not found or unavailable

    quantity = 1

    if request.method == 'POST':
        # Adding item to cart with quantity
        form_quantity = request.form.get('quantity', '1').strip()
        try:
            quantity = int(form_quantity)
            if quantity <= 0:
                quantity = 1
        except ValueError:
            quantity = 1

        # Load cart
        cart_items = load_cart()

        # Find if item already in cart
        cart_item = next((c for c in cart_items if c['item_id'] == item_id), None)
        if cart_item:
            cart_item['quantity'] += quantity
        else:
            new_cart_id = max([c['cart_id'] for c in cart_items], default=0) + 1
            today_str = datetime.now().strftime('%Y-%m-%d')
            cart_items.append({
                'cart_id': new_cart_id,
                'item_id': item['item_id'],
                'restaurant_id': item['restaurant_id'],
                'quantity': quantity,
                'added_date': today_str
            })
        save_cart(cart_items)

        return redirect(url_for('shopping_cart'))

    return render_template('item_details.html', item=item, quantity=quantity)


# Shopping cart page and update
@app.route('/cart', methods=['GET', 'POST'])
def shopping_cart():
    cart_items = load_cart()
    menus = load_menus()

    # Join cart items with menu item details for display
    cart_display = []
    for ci in cart_items:
        menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
        if not menu_item:
            continue
        cart_display.append({
            'cart_id': ci['cart_id'],
            'item_id': ci['item_id'],
            'restaurant_id': ci['restaurant_id'],
            'item_name': menu_item['item_name'],
            'price': menu_item['price'],
            'quantity': ci['quantity'],
            'total_price': menu_item['price'] * ci['quantity']
        })
    
    if request.method == 'POST':
        # Handle updates to quantities or removals
        # Expected form keys in format update_quantity-{cart_id} or remove_item-{cart_id}
        new_cart_items = cart_items.copy()

        # Check removals
        remove_ids = []
        for key in request.form.keys():
            if key.startswith('remove_item-'):
                try:
                    cid = int(key[len('remove_item-'):])
                    remove_ids.append(cid)
                except ValueError:
                    pass
        # Remove items
        new_cart_items = [ci for ci in new_cart_items if ci['cart_id'] not in remove_ids]

        # Update quantities
        for key, val in request.form.items():
            if key.startswith('update_quantity-'):
                try:
                    cid = int(key[len('update_quantity-'):])
                    q = int(val)
                    if q <= 0:
                        # Remove if zero or less
                        new_cart_items = [ci for ci in new_cart_items if ci['cart_id'] != cid]
                    else:
                        # Update
                        for ci in new_cart_items:
                            if ci['cart_id'] == cid:
                                ci['quantity'] = q
                                break
                except ValueError:
                    pass

        save_cart(new_cart_items)

        return redirect(url_for('shopping_cart'))

    total_amount = round(sum(item['total_price'] for item in cart_display), 2)
    return render_template('cart.html', cart_items=cart_display, total_amount=total_amount)


# Checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        delivery_address = request.form.get('delivery_address', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        payment_method = request.form.get('payment_method', '').strip()  # Credit Card, Cash, PayPal

        # Basic validation
        if not customer_name or not delivery_address or not phone_number or payment_method not in ['Credit Card', 'Cash', 'PayPal']:
            # Re-render form with an error message - for now just abort 400
            abort(400)

        cart_items = load_cart()
        menus = load_menus()
        restaurants = load_restaurants()

        if not cart_items:
            # No items in cart
            abort(400)

        # Calculate total amount
        total_amount = 0
        # We'll assume all cart items belong to one restaurant for order (since from one restaurant per order)
        restaurant_ids = set(ci['restaurant_id'] for ci in cart_items)
        if len(restaurant_ids) != 1:
            # More than one restaurant items in cart not supported in spec
            abort(400)

        for ci in cart_items:
            menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
            if not menu_item:
                abort(400)
            total_amount += menu_item['price'] * ci['quantity']
        total_amount = round(total_amount, 2)

        restaurant_id = next(iter(restaurant_ids))

        # Load existing orders to assign new order_id
        orders = load_orders()
        new_order_id = max([o['order_id'] for o in orders], default=0) + 1

        today_str = datetime.now().strftime('%Y-%m-%d')

        # Create new order
        new_order = {
            'order_id': new_order_id,
            'customer_name': customer_name,
            'restaurant_id': restaurant_id,
            'order_date': today_str,
            'total_amount': total_amount,
            'status': 'Preparing',
            'delivery_address': delivery_address,
            'phone_number': phone_number
        }
        orders.append(new_order)
        save_orders(orders)

        # Save order items
        order_items = load_order_items()
        max_order_item_id = max([oi['order_item_id'] for oi in order_items], default=0)
        for ci in cart_items:
            max_order_item_id += 1
            menu_item = next((m for m in menus if m['item_id'] == ci['item_id']), None)
            if menu_item:
                order_items.append({
                    'order_item_id': max_order_item_id,
                    'order_id': new_order_id,
                    'item_id': ci['item_id'],
                    'quantity': ci['quantity'],
                    'price': menu_item['price']
                })
        save_order_items(order_items)

        # Clear cart
        save_cart([])

        # Redirect to active orders page
        return redirect(url_for('active_orders'))

    # GET request just render
    return render_template('checkout.html')


# Active orders page
@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    restaurants = load_restaurants()

    # Add restaurant name to order objects
    restaurant_map = {r['restaurant_id']: r['name'] for r in restaurants}

    enriched_orders = []
    for o in orders:
        order_copy = o.copy()
        order_copy['restaurant_name'] = restaurant_map.get(o['restaurant_id'], '')
        enriched_orders.append(order_copy)

    status_filter_options = ['All', 'Preparing', 'On the Way', 'Delivered']

    # Optional filtering by query param status
    status_filter = request.args.get('status', 'All')

    if status_filter not in status_filter_options:
        status_filter = 'All'

    if status_filter != 'All':
        filtered_orders = [o for o in enriched_orders if o['status'] == status_filter]
    else:
        filtered_orders = enriched_orders

    return render_template('active_orders.html', active_orders=filtered_orders, status_filter_options=status_filter_options, status_filter=status_filter)


# Order tracking page
@app.route('/orders/track/<int:order_id>')
def order_tracking_page(order_id):
    orders = load_orders()
    deliveries = load_deliveries()
    order_items = load_order_items()
    menus = load_menus()
    restaurants = load_restaurants()

    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        abort(404)

    # Add restaurant name
    restaurant = next((r for r in restaurants if r['restaurant_id'] == order['restaurant_id']), None)
    order = order.copy()
    order['restaurant_name'] = restaurant['name'] if restaurant else ''

    delivery_info = next((d for d in deliveries if d['order_id'] == order_id), None)

    # Format estimated time str or fallback empty
    estimated_time = delivery_info['estimated_time'] if delivery_info else ''

    # Items in this order
    items_in_order = []
    for oi in order_items:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                items_in_order.append({
                    'item_id': oi['item_id'],
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    return render_template('order_tracking.html', order=order, delivery_info=delivery_info or {}, estimated_time=estimated_time, order_items=items_in_order)


# Reviews page
@app.route('/reviews')
def reviews_page():
    reviews = load_reviews()
    rating_filter_options = ['All', '5 stars', '4 stars', '3 stars', '2 stars', '1 star']

    filter_param = request.args.get('rating', 'All')

    # Normalize filtering
    if filter_param not in rating_filter_options:
        filter_param = 'All'

    if filter_param == 'All':
        filtered_reviews = reviews
    else:
        star = int(filter_param[0])  # first char to int
        filtered_reviews = [r for r in reviews if r['rating'] == star]

    return render_template('reviews.html', reviews=filtered_reviews, rating_filter_options=rating_filter_options)


# Write review page
@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review_page():
    if request.method == 'POST':
        try:
            restaurant_id = int(request.form.get('restaurant_id', '').strip())
            customer_name = request.form.get('customer_name', '').strip()
            rating = int(request.form.get('rating', '').strip())
            review_text = request.form.get('review_text', '').strip()
            review_date = request.form.get('review_date', '').strip()

            # Validate
            if not customer_name or not review_text or rating < 1 or rating > 5:
                abort(400)
            # Validate date format yyyy-MM-dd
            datetime.strptime(review_date, '%Y-%m-%d')

            # Load restaurants to verify restaurant_id exists
            restaurants = load_restaurants()
            if not any(r['restaurant_id'] == restaurant_id for r in restaurants):
                abort(400)

            reviews = load_reviews()
            new_review_id = max([r['review_id'] for r in reviews], default=0) + 1

            new_review = {
                'review_id': new_review_id,
                'restaurant_id': restaurant_id,
                'customer_name': customer_name,
                'rating': rating,
                'review_text': review_text,
                'review_date': review_date
            }

            reviews.append(new_review)
            save_reviews(reviews)

            return redirect(url_for('reviews_page'))
        except Exception:
            # Any error leads to 400
            abort(400)
    # GET request
    return render_template('write_review.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
