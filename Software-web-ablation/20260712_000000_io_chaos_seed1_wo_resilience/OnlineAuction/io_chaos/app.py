from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# Helper functions to load and save data files

def load_auctions():
    auctions = []
    path = os.path.join(DATA_DIR, 'auctions.txt')
    if not os.path.exists(path):
        return auctions
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

def save_auctions(auctions):
    path = os.path.join(DATA_DIR, 'auctions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for auction in auctions:
            line = f"{auction['auction_id']}|{auction['item_name']}|{auction['description']}|{auction['category']}|{auction['starting_bid']}|{auction['current_bid']}|{auction['end_time']}|{auction['status']}|{auction['image_url']}\n"
            f.write(line)


def load_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
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
    if not os.path.exists(path):
        return bids
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


def save_bids(bids):
    path = os.path.join(DATA_DIR, 'bids.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for bid in bids:
            line = f"{bid['bid_id']}|{bid['auction_id']}|{bid['bidder_name']}|{bid['bid_amount']}|{bid['bid_timestamp']}\n"
            f.write(line)


def load_winners():
    winners = []
    path = os.path.join(DATA_DIR, 'winners.txt')
    if not os.path.exists(path):
        return winners
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
    if not os.path.exists(path):
        return bid_history
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 6:
                record = {
                    'history_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'auction_name': parts[2],
                    'bidder_name': parts[3],
                    'bid_amount': float(parts[4]),
                    'bid_timestamp': parts[5]
                }
                bid_history.append(record)
    return bid_history


def load_items():
    items = []
    path = os.path.join(DATA_DIR, 'items.txt')
    if not os.path.exists(path):
        return items
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


def load_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 6:
                item = {
                    'auction_id': int(parts[0]),
                    'item_name': parts[1],
                    'bid_count': int(parts[2]),
                    'current_bid': float(parts[3]),
                    'trending_rank': int(parts[4]),
                    'time_period': parts[5]
                }
                trending.append(item)
    return trending


@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    auctions = load_auctions()
    trending = load_trending()

    # featured_auctions (list of dict {auction_id: int, item_name: str, current_bid: float, image_url: str})
    featured_auctions = []
    # For demo logic, pick top 3 active auctions with highest current_bid
    active_auctions = [a for a in auctions if a['status'].lower() == 'active']
    sorted_active = sorted(active_auctions, key=lambda x: x['current_bid'], reverse=True)
    for auc in sorted_active[:3]:
        featured_auctions.append({
            'auction_id': auc['auction_id'],
            'item_name': auc['item_name'],
            'current_bid': auc['current_bid'],
            'image_url': auc['image_url']
        })

    # trending_auctions (list of dict {auction_id: int, item_name: str, current_bid: float, bid_count: int, trending_rank: int, time_period: str})
    trending_auctions = trending

    return render_template('dashboard.html', featured_auctions=featured_auctions, trending_auctions=trending_auctions)


@app.route('/catalog')
def auction_catalog():
    auctions = load_auctions()
    categories = load_categories()
    # auctions context variables:
    # auctions (list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str})
    auctions_list = []
    for auc in auctions:
        auctions_list.append({
            'auction_id': auc['auction_id'],
            'item_name': auc['item_name'],
            'description': auc['description'],
            'category': auc['category'],
            'current_bid': auc['current_bid'],
            'end_time': auc['end_time'],
            'image_url': auc['image_url']
        })

    # categories (list of dict {category_id: int, category_name: str})
    categories_list = [{'category_id': c['category_id'], 'category_name': c['category_name']} for c in categories]

    return render_template('catalog.html', auctions=auctions_list, categories=categories_list)


@app.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    auctions = load_auctions()
    bid_history = load_bid_history()

    # Find auction by id
    auction = None
    for a in auctions:
        if a['auction_id'] == auction_id:
            auction = a
            break
    if auction is None:
        # Auction not found - render template with empty context or 404?
        # We render with auction None and empty bid_history
        auction = {
            'auction_id': auction_id,
            'item_name': '',
            'description': '',
            'current_bid': 0.0,
            'end_time': '',
            'status': '',
            'image_url': ''
        }

    # bid_history (list of dict {bid_id: int, bidder_name: str, bid_amount: float, bid_timestamp: str})
    # Note: design says bid_id but bid_history schema has history_id
    # We'll provide keys as per design spec for template usage
    bids = []
    for bh in bid_history:
        if bh['auction_id'] == auction_id:
            bids.append({
                'bid_id': bh['history_id'],
                'bidder_name': bh['bidder_name'],
                'bid_amount': bh['bid_amount'],
                'bid_timestamp': bh['bid_timestamp']
            })

    return render_template('auction_details.html', auction=auction, bid_history=bids)


@app.route('/auction/<int:auction_id>/place_bid', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = load_auctions()
    bids = load_bids()

    auction = None
    for a in auctions:
        if a['auction_id'] == auction_id:
            auction = a
            break
    if auction is None:
        # Auction not found, redirect to catalog
        return redirect(url_for('auction_catalog'))

    if request.method == 'GET':
        # auction (dict {auction_id: int, item_name: str, current_bid: float, minimum_bid: float})
        minimum_bid = max(auction['current_bid'], auction['starting_bid']) + 1.0
        auction_context = {
            'auction_id': auction['auction_id'],
            'item_name': auction['item_name'],
            'current_bid': auction['current_bid'],
            'minimum_bid': minimum_bid
        }
        return render_template('place_bid.html', auction=auction_context)
    else:
        # POST
        bidder_name = request.form.get('bidder-name', '').strip()
        bid_amount_raw = request.form.get('bid-amount', '').strip()
        error_message = None
        success = False

        # Validate bidder_name
        if not bidder_name:
            error_message = 'Bidder name is required.'

        try:
            bid_amount = float(bid_amount_raw)
        except ValueError:
            bid_amount = 0.0
            if error_message is None:
                error_message = 'Invalid bid amount.'

        minimum_bid = max(auction['current_bid'], auction['starting_bid']) + 1.0

        if error_message is None:
            if bid_amount < minimum_bid:
                error_message = f'Bid amount must be at least {minimum_bid:.2f}.'

        if error_message is None:
            # Place the bid
            # Generate new bid_id
            new_bid_id = 1
            if bids:
                new_bid_id = max(b['bid_id'] for b in bids) + 1
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            new_bid = {
                'bid_id': new_bid_id,
                'auction_id': auction_id,
                'bidder_name': bidder_name,
                'bid_amount': bid_amount,
                'bid_timestamp': now_str
            }
            bids.append(new_bid)
            save_bids(bids)

            # Update auction current_bid if bid_amount higher
            if bid_amount > auction['current_bid']:
                auction['current_bid'] = bid_amount
                # Save updated auctions
                save_auctions(auctions)

            success = True
            return render_template('place_bid.html', auction={
                'auction_id': auction['auction_id'],
                'item_name': auction['item_name'],
                'current_bid': auction['current_bid'],
                'minimum_bid': minimum_bid
            }, success=success)
        else:
            # On error, redisplay form with error
            return render_template('place_bid.html', auction={
                'auction_id': auction['auction_id'],
                'item_name': auction['item_name'],
                'current_bid': auction['current_bid'],
                'minimum_bid': minimum_bid
            }, success=False, error_message=error_message)


@app.route('/bid_history')
def bid_history():
    bid_history_data = load_bid_history()
    auctions = load_auctions()

    # bids (list of dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str})
    bids = []
    for bh in bid_history_data:
        bids.append({
            'bid_id': bh['history_id'],
            'auction_name': bh['auction_name'],
            'bidder_name': bh['bidder_name'],
            'bid_amount': bh['bid_amount'],
            'bid_timestamp': bh['bid_timestamp']
        })

    # auctions (list of dict {auction_id: int, item_name: str})
    auctions_list = [{'auction_id': a['auction_id'], 'item_name': a['item_name']} for a in auctions]

    return render_template('bid_history.html', bids=bids, auctions=auctions_list)


@app.route('/categories')
def auction_categories():
    categories = load_categories()
    # categories (list of dict {category_id: int, category_name: str, description: str, item_count: int})
    return render_template('categories.html', categories=categories)


@app.route('/winners')
def winners():
    winners = load_winners()

    # winners (list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str})
    return render_template('winners.html', winners=winners)


@app.route('/trending')
def trending_auctions():
    trending = load_trending()
    # trending_auctions (list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str})
    return render_template('trending.html', trending_auctions=trending)


@app.route('/status')
def auction_status():
    auctions = load_auctions()

    auctions_list = []
    for auc in auctions:
        # Calculate time_remaining
        time_remaining = ''
        try:
            end_dt = datetime.strptime(auc['end_time'], '%Y-%m-%d %H:%M')
            now_dt = datetime.now()
            diff = end_dt - now_dt
            if diff.total_seconds() > 0:
                days, seconds = diff.days, diff.seconds
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                time_remaining = f"{days}d {hours}h {minutes}m"
            else:
                time_remaining = 'Ended'
        except Exception:
            time_remaining = 'Unknown'

        auctions_list.append({
            'auction_id': auc['auction_id'],
            'item_name': auc['item_name'],
            'status': auc['status'],
            'time_remaining': time_remaining,
            'current_bid': auc['current_bid']
        })

    return render_template('status.html', auctions=auctions_list)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
