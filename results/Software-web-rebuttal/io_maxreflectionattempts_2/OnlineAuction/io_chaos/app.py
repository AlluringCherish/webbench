from flask import Flask, render_template, request, redirect, url_for, abort
import os
import datetime
import threading

app = Flask(__name__)
data_folder = 'data'

# Locks to prevent race conditions on file writes
bids_lock = threading.Lock()
auctions_lock = threading.Lock()

# Data loading functions

# Helper to parse datetime safely
def parse_datetime(dt_str):
    try:
        return datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def load_auctions():
    auctions = {}
    path = os.path.join(data_folder, 'auctions.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                # Expected order: id,title,description,category_id,start_price,current_price,end_time
                parts = line.strip().split('|')
                if len(parts) == 7:
                    id_, title, desc, cat_id, start_price, current_price, end_time = parts
                    auctions[id_] = {
                        'id': id_,
                        'title': title,
                        'description': desc,
                        'category_id': cat_id,
                        'start_price': float(start_price),
                        'current_price': float(current_price),
                        'end_time': end_time
                    }
    return auctions


def load_categories():
    categories = {}
    path = os.path.join(data_folder, 'categories.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                # Expected format: id|name
                parts = line.strip().split('|')
                if len(parts) == 2:
                    id_, name = parts
                    categories[id_] = name
    return categories


def load_bids():
    # bids.txt: bid_id|auction_id|user|bid_amount|bid_time
    bids = []
    path = os.path.join(data_folder, 'bids.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    bid_id, auction_id, user, bid_amount, bid_time = parts
                    bids.append({
                        'bid_id': bid_id,
                        'auction_id': auction_id,
                        'user': user,
                        'bid_amount': float(bid_amount),
                        'bid_time': bid_time
                    })
    return bids


def load_winners():
    # winners.txt: auction_id|user|bid_amount|bid_time
    winners = []
    path = os.path.join(data_folder, 'winners.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    auction_id, user, bid_amount, bid_time = parts
                    winners.append({
                        'auction_id': auction_id,
                        'user': user,
                        'bid_amount': float(bid_amount),
                        'bid_time': bid_time
                    })
    return winners


def load_bid_history():
    # bid_history.txt: auction_id|user|bid_amount|bid_time
    bid_history = []
    path = os.path.join(data_folder, 'bid_history.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    auction_id, user, bid_amount, bid_time = parts
                    bid_history.append({
                        'auction_id': auction_id,
                        'user': user,
                        'bid_amount': float(bid_amount),
                        'bid_time': bid_time
                    })
    return bid_history


def load_trending():
    # trending.txt: auction_id|title|bid_count
    trending = []
    path = os.path.join(data_folder, 'trending.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    auction_id, title, bid_count = parts
                    trending.append({
                        'auction_id': auction_id,
                        'title': title,
                        'bid_count': int(bid_count)
                    })
    return trending


# Save functions with locking for concurrency safety

def save_bid(new_bid):
    # Expect new_bid dict with keys: bid_id, auction_id, user, bid_amount, bid_time
    with bids_lock:
        path = os.path.join(data_folder, 'bids.txt')
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"{new_bid['bid_id']}|{new_bid['auction_id']}|{new_bid['user']}|{new_bid['bid_amount']}|{new_bid['bid_time']}\n")


def save_bid_history(new_bid):
    path = os.path.join(data_folder, 'bid_history.txt')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"{new_bid['auction_id']}|{new_bid['user']}|{new_bid['bid_amount']}|{new_bid['bid_time']}\n")


def save_trending(auction_id, title):
    # We update trending by reading all bids to count per auction
    trending_map = {}
    bids = load_bids()
    for b in bids:
        aid = b['auction_id']
        trending_map[aid] = trending_map.get(aid, 0) + 1

    # Also count the new auction if not in trending_map
    trending_map.setdefault(auction_id, 0)  # It will be added in next step

    path = os.path.join(data_folder, 'trending.txt')
    # Write all trending anew
    with open(path, 'w', encoding='utf-8') as f:
        for aid, count in sorted(trending_map.items(), key=lambda x: x[1], reverse=True):
            # Use title if aid matches, else try to find in auctions
            title_to_use = title
            if aid != auction_id:
                auctions = load_auctions()
                if aid in auctions:
                    title_to_use = auctions[aid]['title']
                else:
                    title_to_use = 'Unknown'
            f.write(f"{aid}|{title_to_use}|{count}\n")


@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    auctions = load_auctions()
    categories = load_categories()
    # Fix: Removed incorrect reference to 'auction_catalog_page' endpoint to avoid BuildError
    return render_template('dashboard.html', auctions=auctions, categories=categories)


@app.route('/catalog')
def catalog():
    categories = load_categories()
    return render_template('catalog.html', categories=categories)


@app.route('/auction/<id>')
def auction_detail(id):
    auctions = load_auctions()
    if id not in auctions:
        abort(404)
    auction = auctions[id]
    categories = load_categories()
    bids = [b for b in load_bids() if b['auction_id'] == id]
    bid_history = [bh for bh in load_bid_history() if bh['auction_id'] == id]
    return render_template('auction.html', auction=auction, categories=categories, bids=bids, bid_history=bid_history)


@app.route('/categories')
def categories_list():
    categories = load_categories()
    return render_template('categories.html', categories=categories)


@app.route('/categories/<id>')
def categories_detail(id):
    categories = load_categories()
    if id not in categories:
        abort(404)
    auctions = load_auctions()
    category_auctions = [a for a in auctions.values() if a['category_id'] == id]
    category_name = categories[id]
    return render_template('category.html', category_name=category_name, auctions=category_auctions)


@app.route('/bids')
def bids_list():
    bids = load_bids()
    return render_template('bids.html', bids=bids)


@app.route('/winners')
def winners_list():
    winners = load_winners()
    return render_template('winners.html', winners=winners)


@app.route('/trending')
def trending_list():
    trending = load_trending()
    return render_template('trending.html', trending=trending)


@app.route('/status')
def status():
    auctions = load_auctions()
    now = datetime.datetime.now()
    stats = {
        'total_auctions': len(auctions),
        'active': 0,
        'expired': 0
    }
    for a in auctions.values():
        end_time = parse_datetime(a['end_time'])
        if end_time and end_time > now:
            stats['active'] += 1
        else:
            stats['expired'] += 1
    return render_template('status.html', stats=stats)


@app.route('/place_bid/<auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = load_auctions()
    if auction_id not in auctions:
        abort(404)
    auction = auctions[auction_id]
    categories = load_categories()

    if request.method == 'GET':
        return render_template('place_bid.html', auction=auction, categories=categories, error=None)

    # POST handling to place a bid
    user = request.form.get('user', '').strip()
    bid_amount_str = request.form.get('bid_amount', '').strip()

    error = None
    if not user:
        error = 'User name is required.'
    try:
        bid_amount = float(bid_amount_str)
    except Exception:
        error = 'Invalid bid amount.'
        bid_amount = None

    minimum_bid = auction['current_price'] + 0.01
    if bid_amount is not None and bid_amount < minimum_bid:
        error = f'Bid must be at least {minimum_bid:.2f}'

    end_time = parse_datetime(auction['end_time'])
    if end_time and end_time < datetime.datetime.now():
        error = 'Auction has already ended.'

    if error:
        return render_template('place_bid.html', auction=auction, categories=categories, error=error)

    # Prepare new bid data
    bids = load_bids()
    new_bid_id = str(max((int(b['bid_id']) for b in bids), default=0) + 1)
    bid_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_bid = {
        'bid_id': new_bid_id,
        'auction_id': auction_id,
        'user': user,
        'bid_amount': bid_amount,
        'bid_time': bid_time_str
    }

    # Save the new bid with locking
    save_bid(new_bid)

    # Update auction current price with locking
    with auctions_lock:
        auctions[auction_id]['current_price'] = bid_amount
        path = os.path.join(data_folder, 'auctions.txt')
        with open(path, 'w', encoding='utf-8') as f:
            for a in auctions.values():
                f.write(f"{a['id']}|{a['title']}|{a['description']}|{a['category_id']}|{a['start_price']}|{a['current_price']}|{a['end_time']}\n")

    # Update bid_history.txt
    save_bid_history(new_bid)

    # Recalculate trending.txt
    save_trending(auction_id, auction['title'])

    return redirect(url_for('auction_detail', id=auction_id))


if __name__ == '__main__':
    app.run(debug=True)
