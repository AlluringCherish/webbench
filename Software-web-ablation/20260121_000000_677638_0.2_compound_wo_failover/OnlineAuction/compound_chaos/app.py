from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load data

def load_auctions():
    auctions = []
    path = os.path.join(DATA_DIR, 'auctions.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    auction = {
                        'auction_id': int(parts[0]),
                        'item_name': parts[1],
                        'description': parts[2],
                        'category': parts[3],
                        'starting_bid': float(parts[4]),
                        'current_bid': float(parts[5]),
                        'end_time': parts[6],
                        'status': parts[7],
                        'image_url': parts[8]
                    }
                    auctions.append(auction)
    return auctions


def load_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    category = {
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2],
                        'item_count': int(parts[3])
                    }
                    categories.append(category)
    return categories


def load_bids():
    bids = []
    path = os.path.join(DATA_DIR, 'bids.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    bid = {
                        'bid_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'bidder_name': parts[2],
                        'bid_amount': float(parts[3]),
                        'bid_timestamp': parts[4]
                    }
                    bids.append(bid)
    return bids


def load_winners():
    winners = []
    path = os.path.join(DATA_DIR, 'winners.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    winner = {
                        'winner_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'item_name': parts[2],
                        'winner_name': parts[3],
                        'winning_bid': float(parts[4]),
                        'win_date': parts[5]
                    }
                    winners.append(winner)
    return winners


def load_bid_history():
    bid_history = []
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    history = {
                        'history_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'auction_name': parts[2],
                        'bidder_name': parts[3],
                        'bid_amount': float(parts[4]),
                        'bid_timestamp': parts[5]
                    }
                    bid_history.append(history)
    return bid_history


def load_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    t = {
                        'auction_id': int(parts[0]),
                        'item_name': parts[1],
                        'bid_count': int(parts[2]),
                        'current_bid': float(parts[3]),
                        'trending_rank': int(parts[4]),
                        'time_period': parts[5]
                    }
                    trending.append(t)
    return trending


def load_items():
    items = []
    path = os.path.join(DATA_DIR, 'items.txt')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    item = {
                        'item_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'item_name': parts[2],
                        'starting_price': float(parts[3]),
                        'category': parts[4],
                        'condition': parts[5],
                        'seller_name': parts[6]
                    }
                    items.append(item)
    return items


def save_auctions(auctions):
    path = os.path.join(DATA_DIR, 'auctions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in auctions:
            line = '|'.join([
                str(a['auction_id']),
                a['item_name'],
                a['description'],
                a['category'],
                f'{a['starting_bid']:.2f}',
                f'{a['current_bid']:.2f}',
                a['end_time'],
                a['status'],
                a['image_url']
            ])
            f.write(line + '\n')

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    auctions = load_auctions()
    trending = load_trending()

    # Featured auctions: let's define featured as auctions that are Active and nearest to end_time
    # Sort by end_time ascending and take first 5 active
    active_auctions = [a for a in auctions if a['status'].lower() == 'active']
    try:
        active_auctions.sort(key=lambda x: datetime.strptime(x['end_time'], '%Y-%m-%d %H:%M'))
    except Exception:
        pass
    featured_auctions = []
    for a in active_auctions[:5]:
        featured_auctions.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'current_bid': a['current_bid'],
            'end_time': a['end_time']
        })

    # trending_auctions: from trending.txt list, limited to top 5
    trending_auctions = []
    trending_sorted = sorted(trending, key=lambda t: t['trending_rank'])[:5]
    for t in trending_sorted:
        trending_auctions.append({
            'auction_id': t['auction_id'],
            'item_name': t['item_name'],
            'current_bid': t['current_bid'],
            'bid_count': t['bid_count']
        })

    return render_template('dashboard.html', featured_auctions=featured_auctions, trending_auctions=trending_auctions)

@app.route('/catalog')
def auction_catalog():
    auctions = load_auctions()
    categories = load_categories()
    context_auctions = []
    for a in auctions:
        context_auctions.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'description': a['description'],
            'category': a['category'],
            'current_bid': a['current_bid'],
            'end_time': a['end_time'],
            'image_url': a['image_url']
        })
    context_categories = []
    for c in categories:
        context_categories.append({
            'category_id': c['category_id'],
            'category_name': c['category_name']
        })
    return render_template('catalog.html', auctions=context_auctions, categories=context_categories)

@app.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    auctions = load_auctions()
    bids = load_bid_history()

    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if auction is None:
        # If not found, redirect to catalog
        return redirect(url_for('auction_catalog'))

    bid_history = []
    for bid in bids:
        if bid['auction_id'] == auction_id:
            bid_history.append({
                'bidder_name': bid['bidder_name'],
                'bid_amount': bid['bid_amount'],
                'bid_timestamp': bid['bid_timestamp']
            })

    auction_context = {
        'auction_id': auction['auction_id'],
        'item_name': auction['item_name'],
        'description': auction['description'],
        'current_bid': auction['current_bid'],
        'end_time': auction['end_time'],
        'status': auction['status'],
        'image_url': auction['image_url']
    }

    return render_template('auction_details.html', auction=auction_context, bid_history=bid_history)

@app.route('/place_bid/<int:auction_id>')
def place_bid(auction_id):
    auctions = load_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if auction is None or auction['status'].lower() != 'active':
        # If auction doesn't exist or not active, redirect to catalog
        return redirect(url_for('auction_catalog'))

    auction_context = {
        'auction_id': auction['auction_id'],
        'item_name': auction['item_name'],
        'minimum_bid': max(auction['current_bid'], auction['starting_bid']) + 0.01
    }

    return render_template('place_bid.html', auction=auction_context)

@app.route('/submit_bid/<int:auction_id>', methods=['POST'])
def submit_bid(auction_id):
    bidder_name = request.form.get('bidder_name', '').strip()
    bid_amount_str = request.form.get('bid_amount', '').strip()

    # Validate bid amount
    try:
        bid_amount = float(bid_amount_str)
    except (ValueError, TypeError):
        return redirect(url_for('place_bid', auction_id=auction_id))

    if not bidder_name or bid_amount <= 0:
        return redirect(url_for('place_bid', auction_id=auction_id))

    auctions = load_auctions()
    bids = load_bids()
    bid_history = load_bid_history()

    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if auction is None or auction['status'].lower() != 'active':
        return redirect(url_for('auction_catalog'))

    minimum_bid = max(auction['current_bid'], auction['starting_bid']) + 0.01
    if bid_amount < minimum_bid:
        return redirect(url_for('place_bid', auction_id=auction_id))

    # Compute next bid_id and history_id
    next_bid_id = 1
    if bids:
        next_bid_id = max(b['bid_id'] for b in bids) + 1
    next_history_id = 1
    if bid_history:
        next_history_id = max(h['history_id'] for h in bid_history) + 1

    # Timestamp for bid
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Append to bids.txt
    bid_line = '|'.join([
        str(next_bid_id),
        str(auction_id),
        bidder_name,
        f'{bid_amount:.2f}',
        now
    ])
    bids_path = os.path.join(DATA_DIR, 'bids.txt')
    with open(bids_path, 'a', encoding='utf-8') as f:
        f.write(bid_line + '\n')

    # Append to bid_history.txt
    history_line = '|'.join([
        str(next_history_id),
        str(auction_id),
        auction['item_name'],
        bidder_name,
        f'{bid_amount:.2f}',
        now
    ])
    bid_history_path = os.path.join(DATA_DIR, 'bid_history.txt')
    with open(bid_history_path, 'a', encoding='utf-8') as f:
        f.write(history_line + '\n')

    # Update current_bid in auction
    for a in auctions:
        if a['auction_id'] == auction_id:
            a['current_bid'] = bid_amount
            break
    save_auctions(auctions)

    return redirect(url_for('auction_details', auction_id=auction_id))

@app.route('/bid_history')
def bid_history():
    bids = load_bids()
    auctions = load_auctions()

    # Build auction id to name map
    auction_map = {a['auction_id']: a['item_name'] for a in auctions}

    bids_context = []
    for b in bids:
        auction_name = auction_map.get(b['auction_id'], 'Unknown Auction')
        bids_context.append({
            'bid_id': b['bid_id'],
            'auction_name': auction_name,
            'bidder_name': b['bidder_name'],
            'bid_amount': b['bid_amount'],
            'bid_timestamp': b['bid_timestamp']
        })

    auctions_context = []
    for a in auctions:
        auctions_context.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name']
        })

    return render_template('bid_history.html', bids=bids_context, auctions=auctions_context)

@app.route('/categories')
def auction_categories():
    categories = load_categories()

    categories_context = []
    for c in categories:
        categories_context.append({
            'category_id': c['category_id'],
            'category_name': c['category_name'],
            'description': c['description'],
            'item_count': c['item_count']
        })

    return render_template('categories.html', categories=categories_context)

@app.route('/category/<int:category_id>')
def category_auctions(category_id):
    auctions = load_auctions()
    categories = load_categories()

    category_obj = next((c for c in categories if c['category_id'] == category_id), None)
    if category_obj is None:
        # Redirect to catalog if category doesn't exist
        return redirect(url_for('auction_catalog'))

    # Filter auctions by category name (not category_id directly, since auctions store category str name)
    auctions_filtered = [a for a in auctions if a['category'].lower() == category_obj['category_name'].lower()]

    context_auctions = []
    for a in auctions_filtered:
        context_auctions.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'description': a['description'],
            'category': a['category'],
            'current_bid': a['current_bid'],
            'end_time': a['end_time'],
            'image_url': a['image_url']
        })

    context_categories = []
    for c in categories:
        context_categories.append({
            'category_id': c['category_id'],
            'category_name': c['category_name']
        })

    return render_template('catalog.html', auctions=context_auctions, categories=context_categories)

@app.route('/winners')
def winners():
    winners = load_winners()

    winners_context = []
    for w in winners:
        winners_context.append({
            'auction_id': w['auction_id'],
            'item_name': w['item_name'],
            'winner_name': w['winner_name'],
            'winning_bid': w['winning_bid'],
            'win_date': w['win_date']
        })

    return render_template('winners.html', winners=winners_context)

@app.route('/trending')
def trending_auctions():
    trending = load_trending()

    trending_context = sorted(trending, key=lambda t: t['trending_rank'])
    return render_template('trending.html', trending_auctions=trending_context)

@app.route('/auction_status')
def auction_status():
    auctions = load_auctions()

    context_auctions = []
    for a in auctions:
        context_auctions.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'status': a['status'],
            'end_time': a['end_time'],
            'current_bid': a['current_bid']
        })

    return render_template('auction_status.html', auctions=context_auctions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
