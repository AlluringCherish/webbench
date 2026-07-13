from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

DATA_DIR = 'data'


def read_auctions():
    auctions = []
    path = os.path.join(DATA_DIR, 'auctions.txt')
    if not os.path.exists(path):
        return auctions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 9:
                continue
            auctions.append({
                'auction_id': int(parts[0]),
                'item_name': parts[1],
                'description': parts[2],
                'category': parts[3],
                'starting_bid': parts[4],
                'current_bid': parts[5],
                'end_time': parts[6],
                'status': parts[7],
                'image_url': parts[8],
            })
    return auctions


def read_categories():
    categories = []
    path = os.path.join(DATA_DIR, 'categories.txt')
    if not os.path.exists(path):
        return categories
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 4:
                continue
            categories.append({
                'category_id': int(parts[0]),
                'category_name': parts[1],
                'description': parts[2],
                'item_count': int(parts[3]),
            })
    return categories


def read_bids():
    bids = []
    path = os.path.join(DATA_DIR, 'bids.txt')
    if not os.path.exists(path):
        return bids
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 5:
                continue
            try:
                bid_amount = float(parts[3])
            except:
                bid_amount = 0.0
            bids.append({
                'bid_id': int(parts[0]),
                'auction_id': int(parts[1]),
                'bidder_name': parts[2],
                'bid_amount': bid_amount,
                'bid_timestamp': parts[4],
            })
    return bids


def read_winners():
    winners = []
    path = os.path.join(DATA_DIR, 'winners.txt')
    if not os.path.exists(path):
        return winners
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            try:
                winning_bid = float(parts[4])
            except:
                winning_bid = 0.0
            winners.append({
                'winner_id': int(parts[0]),
                'auction_id': int(parts[1]),
                'item_name': parts[2],
                'winner_name': parts[3],
                'winning_bid': winning_bid,
                'win_date': parts[5],
            })
    return winners


def read_bid_history():
    history = []
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    if not os.path.exists(path):
        return history
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            try:
                bid_amount = float(parts[4])
            except:
                bid_amount = 0.0
            history.append({
                'history_id': int(parts[0]),
                'auction_id': int(parts[1]),
                'auction_name': parts[2],
                'bidder_name': parts[3],
                'bid_amount': bid_amount,
                'bid_timestamp': parts[5],
            })
    return history


def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            try:
                bid_count = int(parts[2])
                current_bid = float(parts[3])
                trending_rank = int(parts[4])
            except:
                bid_count, current_bid, trending_rank = 0, 0.0, 0
            trending.append({
                'auction_id': int(parts[0]),
                'item_name': parts[1],
                'bid_count': bid_count,
                'current_bid': current_bid,
                'trending_rank': trending_rank,
                'time_period': parts[5],
            })
    return trending


def save_bids(bids):
    path = os.path.join(DATA_DIR, 'bids.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for bid in bids:
                f.write(f"{bid['bid_id']}|{bid['auction_id']}|{bid['bidder_name']}|{bid['bid_amount']:.2f}|{bid['bid_timestamp']}\n")
    except Exception as e:
        print(f"Error saving bids: {e}")


def save_auctions(auctions):
    path = os.path.join(DATA_DIR, 'auctions.txt')
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for auction in auctions:
                f.write(f"{auction['auction_id']}|{auction['item_name']}|{auction['description']}|{auction['category']}|{auction['starting_bid']}|{auction['current_bid']}|{auction['end_time']}|{auction['status']}|{auction['image_url']}\n")
    except Exception as e:
        print(f"Error saving auctions: {e}")


def append_bid_history(new_entry):
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"{new_entry['history_id']}|{new_entry['auction_id']}|{new_entry['auction_name']}|{new_entry['bidder_name']}|{new_entry['bid_amount']:.2f}|{new_entry['bid_timestamp']}\n")
    except Exception as e:
        print(f"Error appending bid history: {e}")


@app.route('/')
def root_redirect():
    return redirect(url_for('dashboard'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    auctions = read_auctions()
    # For featured auctions, pick top 5 active auctions sorted by end_time asc
    featured = [a for a in auctions if a['status'] == 'Active']
    featured.sort(key=lambda x: x['end_time'])
    featured = featured[:5]
    return render_template('dashboard.html', featured_auctions=featured)


@app.route('/catalog', methods=['GET'])
def catalog():
    search = request.args.get('search', '').strip().lower()
    category_id = request.args.get('category_id', '').strip()

    auctions = read_auctions()
    categories = read_categories()
    # Map category_id to category_name for filtering
    category_name = None
    if category_id:
        try:
            cid = int(category_id)
            for c in categories:
                if c['category_id'] == cid:
                    category_name = c['category_name']
                    break
        except:
            category_name = None

    def match_search(a):
        if not search:
            return True
        return (search in a['item_name'].lower() or
                search in a['description'].lower() or
                search == str(a['auction_id']))

    def match_category(a):
        if not category_name:
            return True
        return a['category'] == category_name

    filtered_auctions = [a for a in auctions if match_search(a) and match_category(a)]

    return render_template('catalog.html', auctions=filtered_auctions, search=search, category_filter=category_name, categories=categories)


@app.route('/auction/<int:auction_id>', methods=['GET'])
def auction_details(auction_id):
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    bids = read_bids()
    bids_for_auction = [b for b in bids if b['auction_id'] == auction_id]
    bids_for_auction.sort(key=lambda x: x['bid_timestamp'], reverse=True)

    return render_template('auction_details.html', auction=auction, bids=bids_for_auction)


@app.route('/auction/<int:auction_id>/place_bid', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if not auction:
        return "Auction not found", 404

    if request.method == 'GET':
        try:
            current_bid_value = float(auction['current_bid'])
        except:
            current_bid_value = float(auction['starting_bid'])
        minimum_bid = current_bid_value + 1.00
        return render_template('place_bid.html', auction=auction, minimum_bid=minimum_bid, error=None)

    # POST method
    bidder_name = request.form.get('bidder_name', '').strip()
    bid_amount_str = request.form.get('bid_amount', '').strip()

    error = None
    if not bidder_name:
        error = 'Bidder name is required.'

    try:
        bid_amount = float(bid_amount_str)
    except:
        error = 'Invalid bid amount.'

    try:
        current_bid_value = float(auction['current_bid'])
    except:
        current_bid_value = float(auction['starting_bid'])

    minimum_bid = current_bid_value + 1.00

    if not error and bid_amount <= current_bid_value:
        error = f'Bid amount must be greater than current bid ({current_bid_value:.2f}).'

    if error:
        return render_template('place_bid.html', auction=auction, minimum_bid=minimum_bid, error=error)

    bids = read_bids()
    new_bid_id = 1 if not bids else max(b['bid_id'] for b in bids) + 1

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

    # Update current_bid in auctions
    for a in auctions:
        if a['auction_id'] == auction_id:
            a['current_bid'] = f"{bid_amount:.2f}"
            break
    save_auctions(auctions)

    # Append to bid_history.txt
    bid_history = read_bid_history()
    new_history_id = 1 if not bid_history else max(h['history_id'] for h in bid_history) + 1
    new_history_entry = {
        'history_id': new_history_id,
        'auction_id': auction_id,
        'auction_name': auction['item_name'],
        'bidder_name': bidder_name,
        'bid_amount': bid_amount,
        'bid_timestamp': now_str
    }
    append_bid_history(new_history_entry)

    return redirect(url_for('auction_details', auction_id=auction_id))


@app.route('/bids', methods=['GET'])
def bid_history():
    filter_auction_id = request.args.get('auction_id', '').strip()
    sort_order = request.args.get('sort', 'desc')

    bids = read_bids()
    auctions = read_auctions()
    auction_map = {a['auction_id']: a['item_name'] for a in auctions}

    filtered_bids = bids
    if filter_auction_id:
        try:
            aid = int(filter_auction_id)
            filtered_bids = [b for b in bids if b['auction_id'] == aid]
        except:
            filtered_bids = bids

    reverse = True if sort_order == 'desc' else False
    filtered_bids.sort(key=lambda b: b['bid_amount'], reverse=reverse)

    for b in filtered_bids:
        b['auction_name'] = auction_map.get(b['auction_id'], 'Unknown')

    return render_template('bid_history.html', bids=filtered_bids,
                           auctions=auctions,
                           filter_auction_id=filter_auction_id,
                           sort_order=sort_order)


@app.route('/categories', methods=['GET'])
def categories():
    categories = read_categories()
    return render_template('categories.html', categories=categories)


@app.route('/winners', methods=['GET'])
def winners():
    filter_name = request.args.get('filter_name', '').strip().lower()
    winners = read_winners()
    if filter_name:
        winners = [w for w in winners if filter_name in w['winner_name'].lower()]
    return render_template('winners.html', winners=winners, filter_name=filter_name)


@app.route('/trending', methods=['GET'])
def trending():
    time_range = request.args.get('time_range', 'This Week')
    trending_list = read_trending()
    filtered = [t for t in trending_list if t['time_period'] == time_range]
    filtered.sort(key=lambda x: x['trending_rank'])
    return render_template('trending.html', trending=filtered, time_range=time_range)


@app.route('/status', methods=['GET'])
def auction_status():
    status_filter = request.args.get('status', 'All')
    auctions = read_auctions()

    def filter_status(a):
        if status_filter == 'All':
            return True
        return a['status'] == status_filter

    filtered = [a for a in auctions if filter_status(a)]

    now = datetime.now()
    for a in filtered:
        try:
            end_dt = datetime.strptime(a['end_time'], '%Y-%m-%d %H:%M')
            delta = end_dt - now
            if delta.total_seconds() < 0:
                a['time_remaining'] = 'Ended'
            else:
                days = delta.days
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                a['time_remaining'] = f'{days}d {hours}h {minutes}m'
        except:
            a['time_remaining'] = 'Unknown'

    return render_template('status.html', auctions=filtered, status_filter=status_filter)


if __name__ == '__main__':
    app.run(debug=True)
