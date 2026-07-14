from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'
AUCTIONS_FILE = os.path.join(DATA_DIR, 'auctions.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
BIDS_FILE = os.path.join(DATA_DIR, 'bids.txt')
WINNERS_FILE = os.path.join(DATA_DIR, 'winners.txt')
TRENDING_FILE = os.path.join(DATA_DIR, 'trending.txt')
BID_HISTORY_FILE = os.path.join(DATA_DIR, 'bid_history.txt')

def read_auctions():
    auctions = []
    if not os.path.exists(AUCTIONS_FILE):
        return auctions
    with open(AUCTIONS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 9:
                try:
                    auctions.append({
                        'auction_id': int(parts[0]),
                        'item_name': parts[1],
                        'description': parts[2],
                        'category': parts[3],
                        'starting_bid': float(parts[4]),
                        'current_bid': float(parts[5]),
                        'end_time': datetime.strptime(parts[6], '%Y-%m-%d %H:%M'),
                        'status': parts[7],
                        'image_url': parts[8]
                    })
                except Exception:
                    pass
    return auctions

def write_auctions(auctions):
    with open(AUCTIONS_FILE, 'w', encoding='utf-8') as f:
        for a in auctions:
            line = '|'.join([
                str(a['auction_id']),
                a['item_name'],
                a['description'],
                a['category'],
                f"{a['starting_bid']:.2f}",
                f"{a['current_bid']:.2f}",
                a['end_time'].strftime('%Y-%m-%d %H:%M'),
                a['status'],
                a['image_url']
            ])
            f.write(line + '\n')

def read_categories():
    categories = []
    if not os.path.exists(CATEGORIES_FILE):
        return categories
    with open(CATEGORIES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 4:
                try:
                    categories.append({
                        'category_id': int(parts[0]),
                        'category_name': parts[1],
                        'description': parts[2],
                        'item_count': int(parts[3])
                    })
                except Exception:
                    pass
    return categories

def read_bids():
    bids = []
    if not os.path.exists(BIDS_FILE):
        return bids
    with open(BIDS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 5:
                try:
                    bids.append({
                        'bid_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'bidder_name': parts[2],
                        'bid_amount': float(parts[3]),
                        'bid_timestamp': datetime.strptime(parts[4], '%Y-%m-%d %H:%M')
                    })
                except Exception:
                    pass
    return bids

def write_bids(bids):
    with open(BIDS_FILE, 'w', encoding='utf-8') as f:
        for b in bids:
            line = '|'.join([
                str(b['bid_id']),
                str(b['auction_id']),
                b['bidder_name'],
                f"{b['bid_amount']:.2f}",
                b['bid_timestamp'].strftime('%Y-%m-%d %H:%M')
            ])
            f.write(line + '\n')

def read_winners():
    winners = []
    if not os.path.exists(WINNERS_FILE):
        return winners
    with open(WINNERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 6:
                try:
                    winners.append({
                        'winner_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'item_name': parts[2],
                        'winner_name': parts[3],
                        'winning_bid': float(parts[4]),
                        'win_date': datetime.strptime(parts[5], '%Y-%m-%d').date()
                    })
                except Exception:
                    pass
    return winners

def read_bid_history():
    bid_history = []
    if not os.path.exists(BID_HISTORY_FILE):
        return bid_history
    with open(BID_HISTORY_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 6:
                try:
                    bid_history.append({
                        'history_id': int(parts[0]),
                        'auction_id': int(parts[1]),
                        'auction_name': parts[2],
                        'bidder_name': parts[3],
                        'bid_amount': float(parts[4]),
                        'bid_timestamp': parts[5]
                    })
                except Exception:
                    pass
    return bid_history

def read_trending():
    trending = []
    if not os.path.exists(TRENDING_FILE):
        return trending
    with open(TRENDING_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) == 6:
                try:
                    trending.append({
                        'auction_id': int(parts[0]),
                        'item_name': parts[1],
                        'bid_count': int(parts[2]),
                        'current_bid': float(parts[3]),
                        'trending_rank': int(parts[4]),
                        'time_period': parts[5]
                    })
                except Exception:
                    pass
    return trending

def write_bid(bid_id, auction_id, bidder_name, bid_amount, bid_timestamp):
    with open(BIDS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{bid_id}|{auction_id}|{bidder_name}|{bid_amount:.2f}|{bid_timestamp.strftime('%Y-%m-%d %H:%M')}\n")
    auctions = read_auctions()
    for auction in auctions:
        if auction['auction_id'] == auction_id:
            auction['current_bid'] = bid_amount
    write_auctions(auctions)

@app.route('/')
@app.route('/dashboard')
def dashboard():
    auctions = read_auctions()
    featured_auctions = [a for a in auctions if a['status'] == 'Active']
    return render_template('dashboard.html', featured_auctions=featured_auctions)

@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    auctions = read_auctions()
    categories = ['Electronics', 'Collectibles', 'Furniture', 'Art', 'Other']
    search_query = ''
    selected_category = ''

    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip().lower()
        selected_category = request.form.get('category_filter', '')

    filtered_auctions = auctions
    if search_query:
        filtered_auctions = [a for a in filtered_auctions if search_query in a['item_name'].lower() or search_query in a['description'].lower()]
    if selected_category and selected_category in categories:
        filtered_auctions = [a for a in filtered_auctions if a['category'] == selected_category]

    return render_template('catalog.html', auctions=filtered_auctions, categories=categories, selected_category=selected_category, search_query=search_query)

@app.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    auctions = read_auctions()
    bids = read_bids()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    auction_bids_sorted = sorted(auction_bids, key=lambda x: x['bid_timestamp'])
    return render_template('auction_details.html', auction=auction, bids=auction_bids_sorted)

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
                bid_timestamp = datetime.now()
                write_bid(next_bid_id, auction_id, bidder_name, bid_amount, bid_timestamp)
                return redirect(url_for('auction_details', auction_id=auction_id))

    minimum_bid = auction['current_bid'] + 0.01
    return render_template('place_bid.html', auction=auction, minimum_bid=minimum_bid, error=error_message)

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

@app.route('/categories')
def categories():
    categories = read_categories()
    return render_template('categories.html', categories=categories)

@app.route('/categories/<int:category_id>')
def category_view(category_id):
    categories = read_categories()
    auctions = read_auctions()
    category = next((c for c in categories if c['category_id'] == category_id), None)
    if not category:
        return "Category not found", 404
    category_name = category['category_name']

    filtered_auctions = [a for a in auctions if a['category'] == category_name]

    categories_list = [c['category_name'] for c in categories]

    return render_template('catalog.html', auctions=filtered_auctions, categories=categories_list, selected_category=category_name, search_query='')

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
