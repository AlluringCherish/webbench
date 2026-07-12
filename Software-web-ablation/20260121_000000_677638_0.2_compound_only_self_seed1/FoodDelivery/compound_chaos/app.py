from flask import Flask, render_template, redirect, url_for, request, abort
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

data_dir = 'data'

# Helper functions to load data from files

def load_restaurants():
    restaurants = []
    path = os.path.join(data_dir, 'restaurants.txt')
    if not os.path.exists(path):
        return restaurants
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                restaurants.append({
                    'restaurant_id': int(parts[0]),
                    'name': parts[1],
                    'cuisine': parts[2],
                    'address': parts[3],
                    'phone': parts[4],
                    'rating': float(parts[5]),
                    'delivery_time': int(parts[6]),
                    'min_order': float(parts[7])
                })
    except Exception:
        # Fail silently and return empty
        return []
    return restaurants


def load_menus():
    menus = []
    path = os.path.join(data_dir, 'menus.txt')
    if not os.path.exists(path):
        return menus
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                menus.append({
                    'item_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'item_name': parts[2],
                    'category': parts[3],
                    'description': parts[4],
                    'price': float(parts[5]),
                    'availability': int(parts[6])
                })
    except Exception:
        return []
    return menus


def load_cart():
    cart = []
    path = os.path.join(data_dir, 'cart.txt')
    if not os.path.exists(path):
        return cart
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                cart.append({
                    'cart_id': int(parts[0]),
                    'item_id': int(parts[1]),
                    'restaurant_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'added_date': parts[4]  # keep string date
                })
    except Exception:
        return []
    return cart


def save_cart(cart_items):
    # cart_items: list of dicts with keys matching cart.txt schema
    path = os.path.join(data_dir, 'cart.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for item in cart_items:
                line = '{}|{}|{}|{}|{}'.format(
                    item['cart_id'], item['item_id'], item['restaurant_id'], item['quantity'], item['added_date']
                )
                f.write(line + '\n')
    except Exception:
        pass


def load_orders():
    orders = []
    path = os.path.join(data_dir, 'orders.txt')
    if not os.path.exists(path):
        return orders
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 8:
                    continue
                orders.append({
                    'order_id': int(parts[0]),
                    'customer_name': parts[1],
                    'restaurant_id': int(parts[2]),
                    'order_date': parts[3],
                    'total_amount': float(parts[4]),
                    'status': parts[5],
                    'delivery_address': parts[6],
                    'phone_number': parts[7]
                })
    except Exception:
        return []
    return orders


def save_orders(orders):
    path = os.path.join(data_dir, 'orders.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for order in orders:
                line = '{}|{}|{}|{}|{:.2f}|{}|{}|{}'.format(
                    order['order_id'], order['customer_name'], order['restaurant_id'], order['order_date'],
                    order['total_amount'], order['status'], order['delivery_address'], order['phone_number'])
                f.write(line + '\n')
    except Exception:
        pass


def load_order_items():
    order_items = []
    path = os.path.join(data_dir, 'order_items.txt')
    if not os.path.exists(path):
        return order_items
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 5:
                    continue
                order_items.append({
                    'order_item_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'item_id': int(parts[2]),
                    'quantity': int(parts[3]),
                    'price': float(parts[4])
                })
    except Exception:
        return []
    return order_items


def load_deliveries():
    deliveries = []
    path = os.path.join(data_dir, 'deliveries.txt')
    if not os.path.exists(path):
        return deliveries
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 7:
                    continue
                deliveries.append({
                    'delivery_id': int(parts[0]),
                    'order_id': int(parts[1]),
                    'driver_name': parts[2],
                    'driver_phone': parts[3],
                    'vehicle_info': parts[4],
                    'status': parts[5],
                    'estimated_time': parts[6]  # string datetime
                })
    except Exception:
        return []
    return deliveries


def load_reviews():
    reviews = []
    path = os.path.join(data_dir, 'reviews.txt')
    if not os.path.exists(path):
        return reviews
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) != 6:
                    continue
                reviews.append({
                    'review_id': int(parts[0]),
                    'restaurant_id': int(parts[1]),
                    'customer_name': parts[2],
                    'rating': int(parts[3]),
                    'review_text': parts[4],
                    'review_date': parts[5]
                })
    except Exception:
        return []
    return reviews


def save_reviews(reviews):
    path = os.path.join(data_dir, 'reviews.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for r in reviews:
                line = '{}|{}|{}|{}|{}|{}'.format(
                    r['review_id'], r['restaurant_id'], r['customer_name'], r['rating'], r['review_text'], r['review_date'])
                f.write(line + '\n')
    except Exception:
        pass


# Utility to get new ID for any list of dicts with id_key

def get_next_id(records, id_key):
    if not records:
        return 1
    max_id = max(r[id_key] for r in records)
    return max_id + 1


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard_page'))


@app.route('/dashboard')
def dashboard_page():
    # featured_restaurants: example top 3 by rating descending
    restaurants = load_restaurants()
    sorted_restaurants = sorted(restaurants, key=lambda r: r['rating'], reverse=True)
    featured_restaurants = sorted_restaurants[:3]

    cuisines = list({r['cuisine'] for r in restaurants})
    popular_cuisines = sorted(cuisines)

    return render_template('dashboard.html', featured_restaurants=featured_restaurants, popular_cuisines=popular_cuisines)


@app.route('/restaurants')
def browse_restaurants():
    restaurants = load_restaurants()
    menus = load_menus()
    # Extract cuisines
    cuisines = sorted(list({r['cuisine'] for r in restaurants}))

    search_query = request.args.get('search_query', '').strip()
    filter_cuisine = request.args.get('filter_cuisine', '').strip()

    filtered = restaurants
    if search_query:
        filtered = [r for r in filtered if search_query.lower() in r['name'].lower()]
    if filter_cuisine:
        filtered = [r for r in filtered if r['cuisine'].lower() == filter_cuisine.lower()]

    return render_template('restaurants.html', restaurants=filtered, cuisines=cuisines, search_query=search_query, filter_cuisine=filter_cuisine)


@app.route('/restaurant/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurants = load_restaurants()
    menus = load_menus()
    restaurant = next((r for r in restaurants if r['restaurant_id'] == restaurant_id), None)
    if not restaurant:
        abort(404)
    menu_items = [m for m in menus if m['restaurant_id'] == restaurant_id and m['availability'] == 1]
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)


@app.route('/item/<int:item_id>')
def item_details(item_id):
    menus = load_menus()
    item = next((m for m in menus if m['item_id'] == item_id and m['availability'] == 1), None)
    if not item:
        abort(404)
    return render_template('item_details.html', item=item)


@app.route('/cart', methods=['GET','POST'])
def shopping_cart():
    # POST to add item to cart from menu/item with quantity
    if request.method == 'POST':
        try:
            item_id = int(request.form.get('item_id', 0))
            quantity = int(request.form.get('quantity', 0))
            if quantity <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            # Bad input, ignore request
            pass
        else:
            menus = load_menus()
            item = next((m for m in menus if m['item_id'] == item_id and m['availability'] == 1), None)
            if item:
                cart = load_cart()
                # Check if item already in cart
                existing = next((c for c in cart if c['item_id'] == item_id), None)
                if existing:
                    existing['quantity'] += quantity
                else:
                    new_cart_id = get_next_id(cart, 'cart_id')
                    added_date = datetime.now().strftime('%Y-%m-%d')
                    cart.append({
                        'cart_id': new_cart_id,
                        'item_id': item_id,
                        'restaurant_id': item['restaurant_id'],
                        'quantity': quantity,
                        'added_date': added_date
                    })
                save_cart(cart)

    # load cart to show
    cart = load_cart()
    menus = load_menus()
    cart_items = []
    total_amount = 0.0
    for citem in cart:
        menu_item = next((m for m in menus if m['item_id'] == citem['item_id']), None)
        if menu_item and menu_item['availability'] == 1:
            item_total = menu_item['price'] * citem['quantity']
            total_amount += item_total
            cart_items.append({
                'cart_id': citem['cart_id'],
                'item_id': citem['item_id'],
                'restaurant_id': citem['restaurant_id'],
                'quantity': citem['quantity'],
                'item_name': menu_item['item_name'],
                'price': menu_item['price'],
                'total_price': item_total
            })
    return render_template('cart.html', cart_items=cart_items, total_amount=round(total_amount, 2))


@app.route('/cart/update_quantity/<int:item_id>', methods=['POST'])
def update_cart_quantity(item_id):
    try:
        new_quantity = int(request.form.get('quantity', -1))
        if new_quantity < 0:
            abort(400)  # bad request
    except (ValueError, TypeError):
        abort(400)  # bad request

    cart = load_cart()
    modified = False
    for item in cart:
        if item['item_id'] == item_id:
            if new_quantity == 0:
                # remove item from cart
                cart.remove(item)
            else:
                item['quantity'] = new_quantity
            modified = True
            break

    if modified:
        save_cart(cart)
    return redirect(url_for('shopping_cart'))


@app.route('/cart/remove_item/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    cart = load_cart()
    new_cart = [item for item in cart if item['item_id'] != item_id]
    if len(new_cart) != len(cart):
        save_cart(new_cart)
    return redirect(url_for('shopping_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    if request.method == 'GET':
        return render_template('checkout.html')

    # POST: Place order
    customer_name = request.form.get('customer_name', '').strip()
    delivery_address = request.form.get('delivery_address', '').strip()
    phone_number = request.form.get('phone_number', '').strip()
    payment_method = request.form.get('payment_method', '').strip()

    if not customer_name or not delivery_address or not phone_number or not payment_method:
        # Missing form data - could render with error but spec doesn't specify - just render checkout again
        return render_template('checkout.html')

    # Load cart
    cart = load_cart()
    menus = load_menus()
    restaurants = load_restaurants()

    if not cart:
        # no items in cart; just render checkout again
        return render_template('checkout.html')

    # Group cart items by restaurant - but order.txt single restaurant_id required
    # Spec does not define multi-restaurant order behavior, use first found restaurant

    restaurant_id = cart[0]['restaurant_id']

    total_amount = 0.0
    for citem in cart:
        menu_item = next((m for m in menus if m['item_id'] == citem['item_id']), None)
        if not menu_item or menu_item['availability'] != 1:
            # invalid item, skip
            continue
        total_amount += menu_item['price'] * citem['quantity']

    total_amount = round(total_amount, 2)

    # Load existing orders to assign new order id
    orders = load_orders()
    new_order_id = get_next_id(orders, 'order_id')

    order_date = datetime.now().strftime('%Y-%m-%d')

    new_order = {
        'order_id': new_order_id,
        'customer_name': customer_name,
        'restaurant_id': restaurant_id,
        'order_date': order_date,
        'total_amount': total_amount,
        'status': 'Pending',
        'delivery_address': delivery_address,
        'phone_number': phone_number
    }

    orders.append(new_order)
    save_orders(orders)

    # Save order_items
    order_items_all = load_order_items()
    next_order_item_id = get_next_id(order_items_all, 'order_item_id')
    for citem in cart:
        menu_item = next((m for m in menus if m['item_id'] == citem['item_id']), None)
        if not menu_item:
            continue
        order_items_all.append({
            'order_item_id': next_order_item_id,
            'order_id': new_order_id,
            'item_id': citem['item_id'],
            'quantity': citem['quantity'],
            'price': menu_item['price']
        })
        next_order_item_id += 1

    # Save updated order_items
    path = os.path.join(data_dir, 'order_items.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for oi in order_items_all:
                line = '{}|{}|{}|{}|{:.2f}'.format(oi['order_item_id'], oi['order_id'], oi['item_id'], oi['quantity'], oi['price'])
                f.write(line + '\n')
    except Exception:
        pass

    # Clear cart after placing order
    save_cart([])

    return render_template('checkout.html', order_confirmation=new_order)


@app.route('/orders/active')
def active_orders():
    orders = load_orders()
    status_filter = request.args.get('status_filter', '').strip()

    filtered_orders = orders
    if status_filter:
        filtered_orders = [o for o in orders if o['status'].lower() == status_filter.lower()]

    return render_template('active_orders.html', orders=filtered_orders, status_filter=status_filter)


@app.route('/order/track/<int:order_id>')
def order_tracking(order_id):
    orders = load_orders()
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        abort(404)

    deliveries = load_deliveries()
    delivery_info = next((d for d in deliveries if d['order_id'] == order_id), None)

    order_items_all = load_order_items()
    menus = load_menus()
    order_items = []
    for oi in order_items_all:
        if oi['order_id'] == order_id:
            menu_item = next((m for m in menus if m['item_id'] == oi['item_id']), None)
            if menu_item:
                order_items.append({
                    'order_item_id': oi['order_item_id'],
                    'item_id': oi['item_id'],
                    'item_name': menu_item['item_name'],
                    'quantity': oi['quantity'],
                    'price': oi['price']
                })

    return render_template('order_tracking.html', order=order, delivery_info=delivery_info or {}, order_items=order_items)


@app.route('/reviews')
def reviews_page():
    all_reviews = load_reviews()
    filter_rating = request.args.get('filter_rating', '').strip()

    if filter_rating:
        try:
            rating_int = int(filter_rating)
            reviews = [r for r in all_reviews if r['rating'] == rating_int]
        except ValueError:
            reviews = all_reviews
    else:
        reviews = all_reviews

    return render_template('reviews.html', reviews=reviews, filter_rating=filter_rating)


@app.route('/reviews/write', methods=['GET', 'POST'])
def write_review():
    if request.method == 'GET':
        # Send restaurant list for selection
        restaurants = load_restaurants()
        return render_template('write_review.html', restaurants=restaurants)

    # POST processing
    restaurant_id = request.form.get('restaurant_id', '').strip()
    customer_name = request.form.get('customer_name', '').strip()
    rating = request.form.get('rating', '').strip()
    review_text = request.form.get('review_text', '').strip()

    if not restaurant_id or not customer_name or not rating or not review_text:
        restaurants = load_restaurants()
        # could add error msg but spec doesn't require it, just re-render form
        return render_template('write_review.html', restaurants=restaurants)

    try:
        restaurant_id = int(restaurant_id)
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError()
    except ValueError:
        restaurants = load_restaurants()
        return render_template('write_review.html', restaurants=restaurants)

    reviews = load_reviews()
    new_review_id = get_next_id(reviews, 'review_id')
    review_date = datetime.now().strftime('%Y-%m-%d')

    reviews.append({
        'review_id': new_review_id,
        'restaurant_id': restaurant_id,
        'customer_name': customer_name,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date
    })

    save_reviews(reviews)
    # After submit, redirect to reviews page
    return redirect(url_for('reviews_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
