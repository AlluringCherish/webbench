'''
Backend application for OnlineAuction web application.
Defines all routes with matching navigation.
Serves Dashboard '/' as required.
Reads and writes data from/to local text files in 'data' directory.
'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
def read_auctions():
    auctions = []
    path = os.path.join(DATA_DIR, 'auctions.txt')
    if not os.path.exists(path):
        return auctions
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 9:
                continue
            auction = {
                'auction_id': parts[0],
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
def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            category = {
                'category_id': parts[0],
                'category_name': parts[1],
                'description': parts[2],
                'item_count': int(parts[3])
            }
            categories.append(category)
    return categories
def read_bids():
    bids = []
    path = os.path.join(DATA_DIR, 'bids.txt')
    if not os.path.exists(path):
        return bids
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue
            bid = {
                'bid_id': parts[0],
                'auction_id': parts[1],
                'bidder_name': parts[2],
                'bid_amount': float(parts[3]),
                'bid_timestamp': parts[4]
            }
            bids.append(bid)
    return bids
def read_winners():
    winners = []
    path = os.path.join(DATA_DIR, 'winners.txt')
    if not os.path.exists(path):
        return winners
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            winner = {
                'winner_id': parts[0],
                'auction_id': parts[1],
                'item_name': parts[2],
                'winner_name': parts[3],
                'winning_bid': float(parts[4]),
                'win_date': parts[5]
            }
            winners.append(winner)
    return winners
def read_bid_history():
    history = []
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    if not os.path.exists(path):
        return history
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            record = {
                'history_id': parts[0],
                'auction_id': parts[1],
                'auction_name': parts[2],
                'bidder_name': parts[3],
                'bid_amount': float(parts[4]),
                'bid_timestamp': parts[5]
            }
            history.append(record)
    return history
def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 6:
                continue
            record = {
                'auction_id': parts[0],
                'item_name': parts[1],
                'bid_count': int(parts[2]),
                'current_bid': float(parts[3]),
                'trending_rank': int(parts[4]),
                'time_period': parts[5]
            }
            trending.append(record)
    return trending
def read_items():
    items = []
    path = os.path.join(DATA_DIR, 'items.txt')
    if not os.path.exists(path):
        return items
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 7:
                continue
            item = {
                'item_id': parts[0],
                'auction_id': parts[1],
                'item_name': parts[2],
                'starting_price': float(parts[3]),
                'category': parts[4],
                'condition': parts[5],
                'seller_name': parts[6]
            }
            items.append(item)
    return items
@app.route('/')
def dashboard():
    auctions = read_auctions()
    # Pick featured auctions: for simplicity, pick first 3 active auctions
    featured = [a for a in auctions if a['status'].lower() == 'active'][:3]
    trending = read_trending()
    return render_template('dashboard.html',
                           page_title='Auction Dashboard',
                           featured_auctions=featured,
                           trending_auctions=trending)
@app.route('/auction_catalog')
def auction_catalog():
    auctions = read_auctions()
    categories = read_categories()
    category_id = request.args.get('category_id', '')
    if category_id:
        # Find category name by id
        category_name = None
        for c in categories:
            if c['category_id'] == category_id:
                category_name = c['category_name']
                break
        if category_name:
            auctions = [a for a in auctions if a['category'].lower() == category_name.lower()]
    return render_template('auction_catalog.html',
                           page_title='Auction Catalog',
                           auctions=auctions,
                           categories=categories,
                           selected_category=category_id)
@app.route('/auction_details/<auction_id>')
def auction_details(auction_id):
    auctions = read_auctions()
    bids = read_bids()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404
    # Get bids for this auction
    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    # Sort bids by timestamp ascending
    auction_bids.sort(key=lambda b: b['bid_timestamp'])
    return render_template('auction_details.html',
                           page_title='Auction Details',
                           auction=auction,
                           auction_bids=auction_bids)
@app.route('/place_bid/<auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404
    min_bid = max(auction['current_bid'], auction['starting_bid'])
    if request.method == 'POST':
        bidder_name = request.form.get('bidder-name', '').strip()
        bid_amount_str = request.form.get('bid-amount', '').strip()
        if not bidder_name:
            return render_template('place_bid.html',
                                   page_title='Place Bid',
                                   auction=auction,
                                   minimum_bid=min_bid,
                                   error='Bidder name is required.')
        try:
            bid_amount = float(bid_amount_str)
        except ValueError:
            return render_template('place_bid.html',
                                   page_title='Place Bid',
                                   auction=auction,
                                   minimum_bid=min_bid,
                                   error='Invalid bid amount.')
        if bid_amount <= min_bid:
            return render_template('place_bid.html',
                                   page_title='Place Bid',
                                   auction=auction,
                                   minimum_bid=min_bid,
                                   error=f'Bid amount must be greater than current bid ({min_bid}).')
        # Append to bid_history.txt
        bid_history_path = os.path.join(DATA_DIR, 'bid_history.txt')
        bid_history = read_bid_history()
        new_history_id = str(int(bid_history[-1]['history_id']) + 1) if bid_history else '1'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        with open(bid_history_path, 'a', encoding='utf-8') as f:
            f.write(f"{new_history_id}|{auction_id}|{auction['item_name']}|{bidder_name}|{bid_amount:.2f}|{timestamp}\n")
        # Append to bids.txt
        bids_path = os.path.join(DATA_DIR, 'bids.txt')
        bids = read_bids()
        new_bid_id = str(int(bids[-1]['bid_id']) + 1) if bids else '1'
        with open(bids_path, 'a', encoding='utf-8') as f:
            f.write(f"{new_bid_id}|{auction_id}|{bidder_name}|{bid_amount:.2f}|{timestamp}\n")
        # Update auctions.txt current_bid
        auctions_path = os.path.join(DATA_DIR, 'auctions.txt')
        updated_lines = []
        with open(auctions_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_strip = line.strip()
                if not line_strip:
                    updated_lines.append(line)
                    continue
                parts = line_strip.split('|')
                if len(parts) != 9:
                    updated_lines.append(line)
                    continue
                if parts[0] == auction_id:
                    parts[5] = f"{bid_amount:.2f}"
                    updated_line = '|'.join(parts) + '\n'
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line)
        with open(auctions_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        return redirect(url_for('auction_details', auction_id=auction_id))
    # GET request
    return render_template('place_bid.html',
                           page_title='Place Bid',
                           auction=auction,
                           minimum_bid=min_bid,
                           error=None)
@app.route('/bid_history')
def bid_history():
    bids = read_bid_history()
    auctions = read_auctions()
    auction_names = {a['auction_id']: a['item_name'] for a in auctions}
    # Add auction_name to bids if missing
    for bid in bids:
        if 'auction_name' not in bid or not bid['auction_name']:
            bid['auction_name'] = auction_names.get(bid['auction_id'], '')
    # Get unique auctions for filter dropdown
    unique_auctions = sorted(set(bid['auction_name'] for bid in bids if bid['auction_name']))
    return render_template('bid_history.html',
                           page_title='Bid History',
                           bids=bids,
                           auctions=unique_auctions)
@app.route('/auction_categories')
def auction_categories():
    categories = read_categories()
    return render_template('auction_categories.html',
                           page_title='Auction Categories',
                           categories=categories)
@app.route('/winners')
def winners():
    winners = read_winners()
    return render_template('winners.html',
                           page_title='Winning Items',
                           winners=winners)
@app.route('/trending_auctions')
def trending_auctions():
    trending = read_trending()
    return render_template('trending_auctions.html',
                           page_title='Trending Auctions',
                           trending_auctions=trending)
@app.route('/auction_status')
def auction_status():
    auctions = read_auctions()
    return render_template('auction_status.html',
                           page_title='Auction Status',
                           auctions=auctions)
if __name__ == '__main__':
    app.run(debug=True, port=5000)