from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'

# Data file paths
AUCTIONS_FILE = os.path.join(DATA_DIR, 'auctions.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
BIDS_FILE = os.path.join(DATA_DIR, 'bids.txt')
WINNERS_FILE = os.path.join(DATA_DIR, 'winners.txt')
TRENDING_FILE = os.path.join(DATA_DIR, 'trending.txt')
BID_HISTORY_FILE = os.path.join(DATA_DIR, 'bid_history.txt')

# Helper to load auctions

def read_auctions():
    auctions = []
    if os.path.exists(AUCTIONS_FILE):
        with open(AUCTIONS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 9:
                    auctions.append({
                        'auction_id': int(parts[0]),
                        'item_name': parts[1],
                        'description': parts[2],
                        'category': parts[3],
                        'starting_bid': float(parts[4]),
                        'current_bid': float(parts[5]),
                        'end_time': parts[6],
                        'status': parts[7],
                        'image_url': parts[8]
                    })
    return auctions

# Helper to load categories

def read_categories():
    categories = []
    if os.path.exists(CATEGORIES_FILE):
        with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    categories.append({
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2],
                        'item_count': int(parts[3])
                    })
    return categories

# Helper to load bids

def read_bids():
    bids = []
    if os.path.exists(BIDS_FILE):
        with open(BIDS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    bids.append({
                        'bid_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'bidder_name': parts[2],
                        'bid_amount': float(parts[3]),
                        'bid_timestamp': parts[4]
                    })
    return bids

# Helper to load winners

def read_winners():
    winners = []
    if os.path.exists(WINNERS_FILE):
        with open(WINNERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    winners.append({
                        'winner_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'item_name': parts[2],
                        'winner_name': parts[3],
                        'winning_bid': float(parts[4]),
                        'win_date': parts[5]
                    })
    return winners

# Helper to load bid history

def read_bid_history():
    bid_history = []
    if os.path.exists(BID_HISTORY_FILE):
        with open(BID_HISTORY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    bid_history.append({
                        'history_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'auction_name': parts[2],
                        'bidder_name': parts[3],
                        'bid_amount': float(parts[4]),
                        'bid_timestamp': parts[5]
                    })
    return bid_history

# Helper to load trending

def read_trending():
    trending = []
    if os.path.exists(TRENDING_FILE):
        with open(TRENDING_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 6:
                    trending.append({
                        'auction_id': int(parts[0]),
                        'item_name': parts[1],
                        'bid_count': int(parts[2]),
                        'current_bid': float(parts[3]),
                        'trending_rank': int(parts[4]),
                        'time_period': parts[5]
                    })
    return trending

# Helper to write bids and update auctions

def write_bid(bid_id, auction_id, bidder_name, bid_amount, bid_timestamp):
    # Append bid to bids.txt
    with open(BIDS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{bid_id}|{auction_id}|{bidder_name}|{bid_amount:.2f}|{bid_timestamp}\n")

    # Update auctions.txt current_bid
    auctions = read_auctions()
    with open(AUCTIONS_FILE, 'w', encoding='utf-8') as f:
        for auction in auctions:
            if auction['auction_id'] == auction_id:
                auction['current_bid'] = bid_amount
            f.write(f"{auction['auction_id']}|{auction['item_name']}|{auction['description']}|{auction['category']}|{auction['starting_bid']:.2f}|{auction['current_bid']:.2f}|{auction['end_time']}|{auction['status']}|{auction['image_url']}\n")

# Route 1: Dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    # Return dashboard with featured auctions
    auctions = read_auctions()
    featured = [a for a in auctions if a['status'] == 'Active']

    return render_template('dashboard.html', featured_auctions=featured)

# Route 2: Catalog
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    auctions = read_auctions()
    categories = ['Electronics', 'Collectibles', 'Furniture', 'Art', 'Other']
    search_query = ''
    category_filter = ''

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip().lower()
        category_filter = request.form.get('category_filter', '')

    filtered_auctions = []
    for a in auctions:
        if search_query and search_query not in a['item_name'].lower() and search_query not in a['description'].lower():
            continue
        if category_filter and category_filter != a['category']:
            continue
        filtered_auctions.append(a)

    return render_template('catalog.html', auctions=filtered_auctions, categories=categories, search_query=search_query, selected_category=category_filter)

# Route 3: Auction Details
@app.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    auctions = read_auctions()
    bids = read_bids()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    auction_bids = sorted(auction_bids, key=lambda x: datetime.strptime(x['bid_timestamp'], '%Y-%m-%d %H:%M'))

    return render_template('auction_details.html', auction=auction, bids=auction_bids)

# Route 4: Place Bid
@app.route('/place-bid/<int:auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    error_message = ''
    success_message = ''
    if request.method == 'POST':
        bidder_name = request.form.get('bidder_name', '').strip()
        bid_amount_str = request.form.get('bid_amount', '').strip()
        try:
            bid_amount = float(bid_amount_str)
        except ValueError:
            error_message = "Invalid bid amount."
        else:
            if not bidder_name:
                error_message = "Bidder name is required."
            elif bid_amount <= auction['current_bid']:
                error_message = f"Bid must be higher than current bid ({auction['current_bid']:.2f})."
            elif auction['status'] != 'Active':
                error_message = "Auction is not active."
            else:
                bids = read_bids()
                bid_ids = [b['bid_id'] for b in bids]
                next_bid_id = max(bid_ids, default=0) + 1
                bid_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                write_bid(next_bid_id, auction_id, bidder_name, bid_amount, bid_timestamp)
                success_message = "Bid placed successfully."
                auction['current_bid'] = bid_amount

    return render_template('place_bid.html', auction=auction, error_message=error_message, success_message=success_message)

# Route 5: Bid History
@app.route('/bid-history', methods=['GET', 'POST'])
def bid_history():
    bid_history = read_bid_history()
    auctions = read_auctions()
    filter_auction = None
    sort_by_amount = False

    if request.method == 'POST':
        filter_auction = request.form.get('filter_auction', '')
        sort_by_amount = ('sort_by_amount' in request.form)

    filtered_bids = bid_history
    if filter_auction:
        try:
            filter_auction_id = int(filter_auction)
            filtered_bids = [b for b in filtered_bids if b['auction_id'] == filter_auction_id]
        except ValueError:
            pass

    if sort_by_amount:
        filtered_bids = sorted(filtered_bids, key=lambda x: x['bid_amount'], reverse=True)

    auction_options = [(a['auction_id'], a['item_name']) for a in auctions]

    return render_template('bid_history.html', bids=filtered_bids, auction_options=auction_options, filter_auction=filter_auction, sort_by_amount=sort_by_amount)

# Route 6: Categories
@app.route('/categories')
def categories():
    categories = read_categories()
    return render_template('categories.html', categories=categories)

# Route 7: Winners
@app.route('/winners', methods=['GET', 'POST'])
def winners():
    winners = read_winners()
    filter_winner = ''
    if request.method == 'POST':
        filter_winner = request.form.get('filter_winner', '').strip().lower()

    filtered_winners = []
    if filter_winner:
        for w in winners:
            if filter_winner in w['winner_name'].lower():
                filtered_winners.append(w)
    else:
        filtered_winners = winners

    return render_template('winners.html', winners=filtered_winners, filter_winner=filter_winner)

# Route 8: Trending
@app.route('/trending', methods=['GET', 'POST'])
def trending():
    trending = read_trending()
    time_range = ''
    time_ranges = ['Last 24 Hours', 'This Week', 'All Time']
    if request.method == 'POST':
        time_range = request.form.get('time_range', '')

    if time_range:
        filtered_trending = [t for t in trending if t['time_period'] == time_range]
    else:
        filtered_trending = trending

    return render_template('trending.html', trending=filtered_trending, time_range=time_range, time_ranges=time_ranges)

# Route 9: Status
@app.route('/status', methods=['GET', 'POST'])
def status():
    auctions = read_auctions()
    status_filter = 'All'
    status_options = ['All', 'Active', 'Closed', 'Upcoming']

    if request.method == 'POST':
        status_filter = request.form.get('status_filter', 'All')

    if status_filter == 'All':
        filtered_auctions = auctions
    else:
        filtered_auctions = [a for a in auctions if a['status'] == status_filter]

    return render_template('status.html', auctions=filtered_auctions, status_filter=status_filter, status_options=status_options)

if __name__ == '__main__':
    app.run(debug=True)
