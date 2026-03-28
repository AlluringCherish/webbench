from flask import Flask, render_template, redirect, url_for, request
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

def read_auctions():
    auctions = []
    filename = 'data/auctions.txt'
    if not os.path.exists(filename):
        return auctions
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 9:
                continue
            try:
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
            except:
                continue
    return auctions

def write_auctions(auctions):
    filename = 'data/auctions.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for auction in auctions:
            line = f"{auction['auction_id']}|{auction['item_name']}|{auction['description']}|{auction['category']}|{auction['starting_bid']}|{auction['current_bid']}|{auction['end_time']}|{auction['status']}|{auction['image_url']}\n"
            f.write(line)

def read_categories():
    categories = []
    filename = 'data/categories.txt'
    if not os.path.exists(filename):
        return categories
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 4:
                continue
            try:
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2],
                    'item_count': int(parts[3])
                }
                categories.append(category)
            except:
                continue
    return categories

def read_bids():
    bids = []
    filename = 'data/bids.txt'
    if not os.path.exists(filename):
        return bids
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 5:
                continue
            try:
                bid = {
                    'bid_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'bidder_name': parts[2],
                    'bid_amount': float(parts[3]),
                    'bid_timestamp': parts[4]
                }
                bids.append(bid)
            except:
                continue
    return bids

def write_bids(bids):
    filename = 'data/bids.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for bid in bids:
            line = f"{bid['bid_id']}|{bid['auction_id']}|{bid['bidder_name']}|{bid['bid_amount']}|{bid['bid_timestamp']}\n"
            f.write(line)

def read_winners():
    winners = []
    filename = 'data/winners.txt'
    if not os.path.exists(filename):
        return winners
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                winner = {
                    'winner_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'item_name': parts[2],
                    'winner_name': parts[3],
                    'winning_bid': float(parts[4]),
                    'win_date': parts[5]
                }
                winners.append(winner)
            except:
                continue
    return winners

def read_bid_history():
    bid_history = []
    filename = 'data/bid_history.txt'
    if not os.path.exists(filename):
        return bid_history
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                history = {
                    'history_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'auction_name': parts[2],
                    'bidder_name': parts[3],
                    'bid_amount': float(parts[4]),
                    'bid_timestamp': parts[5]
                }
                bid_history.append(history)
            except:
                continue
    return bid_history

def read_trending():
    trending = []
    filename = 'data/trending.txt'
    if not os.path.exists(filename):
        return trending
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 6:
                continue
            try:
                trend = {
                    'auction_id': int(parts[0]),
                    'item_name': parts[1],
                    'bid_count': int(parts[2]),
                    'current_bid': float(parts[3]),
                    'trending_rank': int(parts[4]),
                    'time_period': parts[5]
                }
                trending.append(trend)
            except:
                continue
    return trending

def read_items():
    items = []
    filename = 'data/items.txt'
    if not os.path.exists(filename):
        return items
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) != 7:
                continue
            try:
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
            except:
                continue
    return items

@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # featured_auctions: list of dict{auction_id: int, item_name: str, current_bid: float, end_time: str}
    # trending_auctions: list of dict{auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}

    auctions = read_auctions()
    trending = read_trending()

    # Select featured auctions - no specific rule given, so let's pick auctions with status Active and soonest ending time - top 5
    featured_auctions = []
    active_auctions = [a for a in auctions if a['status'].lower() == 'active']
    # Sort by end_time ascending
    try:
        active_auctions.sort(key=lambda x: datetime.strptime(x['end_time'], '%Y-%m-%d %H:%M'))
    except:
        pass
    for a in active_auctions[:5]:
        featured_auctions.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'current_bid': a['current_bid'],
            'end_time': a['end_time']
        })

    # trending_auctions from trending.txt as is
    trending_auctions = trending  # already list of dicts with correct keys

    return render_template('dashboard.html', featured_auctions=featured_auctions, trending_auctions=trending_auctions)

@app.route('/catalog')
def auction_catalog():
    auctions = read_auctions()
    categories_data = read_categories()
    categories = [c['category_name'] for c in categories_data]

    # For catalog listing: auctions with auction_id, item_name, description, category, current_bid, end_time
    auction_list = []
    for a in auctions:
        auction_list.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'description': a['description'],
            'category': a['category'],
            'current_bid': a['current_bid'],
            'end_time': a['end_time']
        })

    return render_template('catalog.html', auctions=auction_list, categories=categories)

@app.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    auctions = read_auctions()
    bids = read_bids()

    auction = None
    for a in auctions:
        if a['auction_id'] == auction_id:
            auction = a
            break
    if auction is None:
        return "Auction not found", 404

    # bids: list of bids for this auction with keys bidder_name, bid_amount, bid_timestamp
    auction_bids = []
    for bid in bids:
        if bid['auction_id'] == auction_id:
            auction_bids.append({
                'bidder_name': bid['bidder_name'],
                'bid_amount': bid['bid_amount'],
                'bid_timestamp': bid['bid_timestamp']
            })

    # sort bids by bid_timestamp ascending
    try:
        auction_bids.sort(key=lambda x: datetime.strptime(x['bid_timestamp'], '%Y-%m-%d %H:%M'))
    except:
        pass

    return render_template('auction_details.html', auction=auction, bids=auction_bids)

@app.route('/place-bid/<int:auction_id>', methods=['GET'])
def place_bid_page(auction_id):
    auctions = read_auctions()
    auction = None
    for a in auctions:
        if a['auction_id'] == auction_id:
            auction = a
            break
    if auction is None:
        return "Auction not found", 404

    minimum_bid = auction['current_bid'] if auction['current_bid'] > 0 else auction['starting_bid']

    return render_template('place_bid.html', auction_name=auction['item_name'], minimum_bid=minimum_bid)

@app.route('/place-bid/<int:auction_id>', methods=['POST'])
def submit_bid(auction_id):
    bidder_name = request.form.get('bidder-name')
    bid_amount_str = request.form.get('bid-amount')

    if not bidder_name or not bid_amount_str:
        return "Missing bidder name or bid amount", 400

    try:
        bid_amount = float(bid_amount_str)
    except ValueError:
        return "Invalid bid amount", 400

    auctions = read_auctions()
    auction = None
    for a in auctions:
        if a['auction_id'] == auction_id:
            auction = a
            break
    if auction is None:
        return "Auction not found", 404

    minimum_bid = auction['current_bid'] if auction['current_bid'] > 0 else auction['starting_bid']
    if bid_amount < minimum_bid:
        return "Bid amount too low", 400

    # Read bids to find next bid_id
    bids = read_bids()
    next_bid_id = 1
    if bids:
        next_bid_id = max(bid['bid_id'] for bid in bids) + 1

    # Current timestamp string
    bid_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Append new bid
    new_bid = {
        'bid_id': next_bid_id,
        'auction_id': auction_id,
        'bidder_name': bidder_name,
        'bid_amount': bid_amount,
        'bid_timestamp': bid_timestamp
    }
    bids.append(new_bid)
    write_bids(bids)

    # Update auctions.txt with new current_bid for this auction
    for a in auctions:
        if a['auction_id'] == auction_id:
            a['current_bid'] = bid_amount
            break
    write_auctions(auctions)

    # Also append to bid_history.txt with history_id
    bid_history = read_bid_history()
    next_history_id = 1
    if bid_history:
        next_history_id = max(h['history_id'] for h in bid_history) + 1

    new_history = {
        'history_id': next_history_id,
        'auction_id': auction_id,
        'auction_name': auction['item_name'],
        'bidder_name': bidder_name,
        'bid_amount': bid_amount,
        'bid_timestamp': bid_timestamp
    }
    bid_history.append(new_history)
    # Write bid_history back
    filename = 'data/bid_history.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for h in bid_history:
            line = f"{h['history_id']}|{h['auction_id']}|{h['auction_name']}|{h['bidder_name']}|{h['bid_amount']}|{h['bid_timestamp']}\n"
            f.write(line)

    return redirect(url_for('auction_details', auction_id=auction_id))

@app.route('/bid-history')
def bid_history():
    bids = read_bid_history()
    auctions = read_auctions()
    # bids context: list of dict{bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}
    # auctions context: list of dict{auction_id: int, item_name: str} for filter dropdown
    bids_list = []
    for b in bids:
        bids_list.append({
            'bid_id': b['history_id'],
            'auction_name': b['auction_name'],
            'bidder_name': b['bidder_name'],
            'bid_amount': b['bid_amount'],
            'bid_timestamp': b['bid_timestamp']
        })

    auctions_list = []
    for a in auctions:
        auctions_list.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name']
        })

    return render_template('bid_history.html', bids=bids_list, auctions=auctions_list)

@app.route('/categories')
def categories():
    categories_data = read_categories()
    # For template: categories: list of dict{category_id: int, category_name: str, description: str, item_count: int}
    return render_template('categories.html', categories=categories_data)

@app.route('/winners')
def winners():
    winners_data = read_winners()
    return render_template('winners.html', winners=winners_data)

@app.route('/trending')
def trending_auctions():
    trending_data = read_trending()
    return render_template('trending.html', trending_list=trending_data)

@app.route('/status')
def auction_status():
    auctions = read_auctions()
    auctions_status = []
    for a in auctions:
        auctions_status.append({
            'name': a['item_name'],
            'status': a['status'],
            'time_remaining': a['end_time'],  # Specification requires time_remaining; but we only have end_time. We'll provide end_time string as is.
            'current_bid': a['current_bid']
        })
    return render_template('status.html', auctions_status=auctions_status)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
