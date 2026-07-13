from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime, timedelta
import threading

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

DATA_DIR = 'data'

lock = threading.Lock()

# Utility functions to read and write data files

def read_auctions():
    auctions = []
    path = os.path.join(DATA_DIR, 'auctions.txt')
    if not os.path.exists(path):
        return auctions
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
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
                continue
    return auctions


def write_auctions(auctions):
    path = os.path.join(DATA_DIR, 'auctions.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for a in auctions:
            line = f"{a['auction_id']}|{a['item_name']}|{a['description']}|{a['category']}|{a['starting_bid']:.2f}|{a['current_bid']:.2f}|{a['end_time'].strftime('%Y-%m-%d %H:%M')}|{a['status']}|{a['image_url']}"
            f.write(line + '\n')


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
            try:
                categories.append({
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2],
                    'item_count': int(parts[3])
                })
            except Exception:
                continue
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
            try:
                bids.append({
                    'bid_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'bidder_name': parts[2],
                    'bid_amount': float(parts[3]),
                    'bid_timestamp': datetime.strptime(parts[4], '%Y-%m-%d %H:%M')
                })
            except Exception:
                continue
    return bids


def write_bids(bids):
    path = os.path.join(DATA_DIR, 'bids.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for b in bids:
            line = f"{b['bid_id']}|{b['auction_id']}|{b['bidder_name']}|{b['bid_amount']:.2f}|{b['bid_timestamp'].strftime('%Y-%m-%d %H:%M')}"
            f.write(line + '\n')


def read_winners():
    winners = []
    path = os.path.join(DATA_DIR, 'winners.txt')
    if not os.path.exists(path):
        return winners
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
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
                continue
    return winners


def read_bid_history():
    history = []
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    if not os.path.exists(path):
        return history
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            try:
                history.append({
                    'history_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'auction_name': parts[2],
                    'bidder_name': parts[3],
                    'bid_amount': float(parts[4]),
                    'bid_timestamp': datetime.strptime(parts[5], '%Y-%m-%d %H:%M')
                })
            except Exception:
                continue
    return history


def write_bid_history(history):
    path = os.path.join(DATA_DIR, 'bid_history.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for h in history:
            line = f"{h['history_id']}|{h['auction_id']}|{h['auction_name']}|{h['bidder_name']}|{h['bid_amount']:.2f}|{h['bid_timestamp'].strftime('%Y-%m-%d %H:%M')}"
            f.write(line + '\n')


def read_trending():
    trending = []
    path = os.path.join(DATA_DIR, 'trending.txt')
    if not os.path.exists(path):
        return trending
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
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
                continue
    return trending


def write_categories(categories):
    path = os.path.join(DATA_DIR, 'categories.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for c in categories:
            line = f"{c['category_id']}|{c['category_name']}|{c['description']}|{c['item_count']}"
            f.write(line + '\n')


def get_new_bid_id(bids):
    if not bids:
        return 1
    return max(b['bid_id'] for b in bids) + 1


def get_new_history_id(history):
    if not history:
        return 1
    return max(h['history_id'] for h in history) + 1


def update_auction_current_bid(auction_id, new_bid):
    auctions = read_auctions()
    updated = False
    for a in auctions:
        if a['auction_id'] == auction_id:
            if new_bid > a['current_bid']:
                a['current_bid'] = new_bid
                updated = True
            break
    if updated:
        write_auctions(auctions)
    return updated


# Helper to get auction by id

def get_auction_by_id(auction_id):
    auctions = read_auctions()
    for a in auctions:
        if a['auction_id'] == auction_id:
            return a
    return None


def get_category_by_id(category_id):
    categories = read_categories()
    for c in categories:
        if c['category_id'] == category_id:
            return c
    return None


# Route 1: Dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    trending = read_trending()
    featured_auctions = [t for t in trending if t['time_period'] == 'This Week']
    featured_auctions.sort(key=lambda x: (-x['bid_count'], -x['current_bid']))
    trending_auctions = featured_auctions
    return render_template('dashboard.html', featured_auctions=featured_auctions)

# Route 2: Auction Catalog
@app.route('/auctions')
def auction_catalog():
    search = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()
    auctions = read_auctions()
    categories = read_categories()
    if search:
        auctions = [a for a in auctions if (search in a['item_name'].lower() or search in a['description'].lower() or search in str(a['auction_id']))]
    if category_filter:
        auctions = [a for a in auctions if a['category'].lower() == category_filter.lower()]
    return render_template('auction_catalog.html', auctions=auctions, categories=categories)

# Route 3: Auction Details
@app.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    auction = get_auction_by_id(auction_id)
    if not auction:
        return "Auction not found", 404
    bid_history = read_bid_history()
    bid_history = [b for b in bid_history if b['auction_id'] == auction_id]
    bid_history.sort(key=lambda x: x['bid_timestamp'], reverse=True)
    return render_template('auction_details.html', auction=auction, bid_history=bid_history)

# Route 4: Place Bid
@app.route('/auction/<int:auction_id>/place_bid', methods=['GET', 'POST'])
def place_bid(auction_id):
    auction = get_auction_by_id(auction_id)
    if not auction:
        return "Auction not found", 404
    min_bid = max(auction['current_bid'], auction['starting_bid'])
    if request.method == 'GET':
        return render_template('place_bid.html', auction=auction, minimum_bid=min_bid)

    bidder_name = request.form.get('bidder_name', '').strip()
    bid_amount_raw = request.form.get('bid_amount', '').strip()

    if not bidder_name:
        flash('Bidder name is required.')
        return render_template('place_bid.html', auction=auction, minimum_bid=min_bid)

    try:
        bid_amount = float(bid_amount_raw)
    except ValueError:
        flash('Invalid bid amount.')
        return render_template('place_bid.html', auction=auction, minimum_bid=min_bid)

    if bid_amount <= min_bid:
        flash(f'Bid amount must be greater than current bid ({min_bid:.2f}).')
        return render_template('place_bid.html', auction=auction, minimum_bid=min_bid)

    with lock:
        bids = read_bids()
        bid_history = read_bid_history()
        auctions = read_auctions()
        auction_recheck = None
        for a in auctions:
            if a['auction_id'] == auction_id:
                auction_recheck = a
                break
        if not auction_recheck:
            flash('Auction not found during bid processing.')
            return render_template('place_bid.html', auction=auction, minimum_bid=min_bid)

        current_bid_check = auction_recheck['current_bid']
        min_bid_check = max(auction_recheck['starting_bid'], current_bid_check)
        if bid_amount <= min_bid_check:
            flash(f'Bid amount must be greater than current bid ({min_bid_check:.2f}) in latest check.')
            return render_template('place_bid.html', auction=auction_recheck, minimum_bid=min_bid_check)

        new_bid_id = get_new_bid_id(bids)
        timestamp = datetime.now()
        new_bid = {
            'bid_id': new_bid_id,
            'auction_id': auction_id,
            'bidder_name': bidder_name,
            'bid_amount': bid_amount,
            'bid_timestamp': timestamp
        }
        bids.append(new_bid)
        write_bids(bids)
        for a in auctions:
            if a['auction_id'] == auction_id:
                a['current_bid'] = bid_amount
                break
        write_auctions(auctions)
        new_history_id = get_new_history_id(bid_history)
        new_history_entry = {
            'history_id': new_history_id,
            'auction_id': auction_id,
            'auction_name': auction_recheck['item_name'],
            'bidder_name': bidder_name,
            'bid_amount': bid_amount,
            'bid_timestamp': timestamp
        }
        bid_history.append(new_history_entry)
        write_bid_history(bid_history)

    flash('Bid placed successfully.')
    return redirect(url_for('auction_details', auction_id=auction_id))

# Route 5: Bid History
@app.route('/bid_history')
def bid_history():
    auction_id_filter = request.args.get('auction_id', '').strip()
    sort_by_amount = request.args.get('sort', '') == 'amount'
    bid_history = read_bid_history()
    auctions = read_auctions()
    if auction_id_filter:
        try:
            filter_id = int(auction_id_filter)
            bid_history = [b for b in bid_history if b['auction_id'] == filter_id]
        except ValueError:
            pass
    if sort_by_amount:
        bid_history.sort(key=lambda x: x['bid_amount'], reverse=True)
    else:
        bid_history.sort(key=lambda x: x['bid_timestamp'], reverse=True)
    return render_template('bid_history.html', bids=bid_history, auctions=auctions)

# Route 6: Auction Categories
@app.route('/categories')
def auction_categories():
    categories = read_categories()
    auctions = read_auctions()
    counts = {}
    for c in categories:
        counts[c['category_name'].lower()] = 0
    for a in auctions:
        cat_lower = a['category'].lower()
        if cat_lower in counts:
            counts[cat_lower] += 1
    for c in categories:
        c['item_count'] = counts.get(c['category_name'].lower(), 0)
    write_categories(categories)
    return render_template('auction_categories.html', categories=categories)

# Route 7: View Items by Category
@app.route('/category/<int:category_id>/items')
def category_items(category_id):
    category = get_category_by_id(category_id)
    if not category:
        return "Category not found", 404
    auctions = read_auctions()
    filtered_auctions = [a for a in auctions if a['category'].lower() == category['category_name'].lower()]
    return render_template('category_items.html', auctions=filtered_auctions, category=category)

# Route 8: Winners Page
@app.route('/winners')
def winners():
    winner_name_filter = request.args.get('name', '').strip().lower()
    winners = read_winners()
    if winner_name_filter:
        winners = [w for w in winners if winner_name_filter in w['winner_name'].lower()]
    winners.sort(key=lambda x: x['win_date'], reverse=True)
    return render_template('winners.html', winners=winners)

# Route 9: Trending Auctions
@app.route('/trending')
def trending_auctions():
    time_range = request.args.get('time_range', 'This Week')
    trending = read_trending()
    filtered = [t for t in trending if t['time_period'].lower() == time_range.lower()]
    filtered.sort(key=lambda x: x['trending_rank'])
    return render_template('trending_auctions.html', trending_auctions=filtered, time_range=time_range)

# Route 10: Auction Status
@app.route('/status')
def auction_status():
    status_filter = request.args.get('status', 'All').strip().lower()
    auctions = read_auctions()
    now = datetime.now()
    filtered_auctions = []
    for a in auctions:
        a_copy = a.copy()
        if a['status'].lower() in ['active', 'upcoming']:
            time_remaining = a['end_time'] - now
            if time_remaining.total_seconds() < 0:
                time_remaining = timedelta(seconds=0)
            a_copy['time_remaining'] = time_remaining
        else:
            a_copy['time_remaining'] = timedelta(seconds=0)
        if status_filter == 'all' or a['status'].lower() == status_filter:
            filtered_auctions.append(a_copy)
    return render_template('auction_status.html', auctions_status=filtered_auctions, status_filter=status_filter)


if __name__ == '__main__':
    app.run(debug=True)
