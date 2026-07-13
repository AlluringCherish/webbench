from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)

data_dir = 'data'

# Utility functions

def read_auctions():
    auctions = []
    try:
        with open(os.path.join(data_dir, 'auctions.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 9:
                    continue
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
    except FileNotFoundError:
        pass
    return auctions

def write_auctions(auctions):
    try:
        with open(os.path.join(data_dir, 'auctions.txt'), 'w', encoding='utf-8') as f:
            for a in auctions:
                line = f"{a['auction_id']}|{a['item_name']}|{a['description']}|{a['category']}|{a['starting_bid']:.2f}|{a['current_bid']:.2f}|{a['end_time']}|{a['status']}|{a['image_url']}\n"
                f.write(line)
    except Exception:
        pass

def read_categories():
    categories = []
    try:
        with open(os.path.join(data_dir, 'categories.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 4:
                    continue
                category = {
                    'category_id': int(parts[0]),
                    'category_name': parts[1],
                    'description': parts[2],
                    'item_count': int(parts[3])
                }
                categories.append(category)
    except FileNotFoundError:
        pass
    return categories

def read_bids():
    bids = []
    try:
        with open(os.path.join(data_dir, 'bids.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 5:
                    continue
                bid = {
                    'bid_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'bidder_name': parts[2],
                    'bid_amount': float(parts[3]),
                    'bid_timestamp': parts[4]
                }
                bids.append(bid)
    except FileNotFoundError:
        pass
    return bids

def write_bids(bids):
    try:
        with open(os.path.join(data_dir, 'bids.txt'), 'w', encoding='utf-8') as f:
            for b in bids:
                line = f"{b['bid_id']}|{b['auction_id']}|{b['bidder_name']}|{b['bid_amount']:.2f}|{b['bid_timestamp']}\n"
                f.write(line)
    except Exception:
        pass

def read_winners():
    winners = []
    try:
        with open(os.path.join(data_dir, 'winners.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                winner = {
                    'winner_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'item_name': parts[2],
                    'winner_name': parts[3],
                    'winning_bid': float(parts[4]),
                    'win_date': parts[5]
                }
                winners.append(winner)
    except FileNotFoundError:
        pass
    return winners

def read_bid_history():
    history = []
    try:
        with open(os.path.join(data_dir, 'bid_history.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                item = {
                    'history_id': int(parts[0]),
                    'auction_id': int(parts[1]),
                    'auction_name': parts[2],
                    'bidder_name': parts[3],
                    'bid_amount': float(parts[4]),
                    'bid_timestamp': parts[5]
                }
                history.append(item)
    except FileNotFoundError:
        pass
    return history

def write_bid_history(history):
    try:
        with open(os.path.join(data_dir, 'bid_history.txt'), 'w', encoding='utf-8') as f:
            for h in history:
                line = f"{h['history_id']}|{h['auction_id']}|{h['auction_name']}|{h['bidder_name']}|{h['bid_amount']:.2f}|{h['bid_timestamp']}\n"
                f.write(line)
    except Exception:
        pass

def read_trending():
    trending = []
    try:
        with open(os.path.join(data_dir, 'trending.txt'), 'r', encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                item = {
                    'auction_id': int(parts[0]),
                    'item_name': parts[1],
                    'bid_count': int(parts[2]),
                    'current_bid': float(parts[3]),
                    'trending_rank': int(parts[4]),
                    'time_period': parts[5]
                }
                trending.append(item)
    except FileNotFoundError:
        pass
    return trending


@app.route('/')
@app.route('/dashboard', methods=['GET'])
def dashboard():
    auctions = read_auctions()
    # For featured auctions, let's pick top 3 auctions by current_bid descending
    featured = sorted(auctions, key=lambda a: a['current_bid'], reverse=True)[:3]
    return render_template('dashboard.html', page_title='Auction Dashboard', featured_auctions=featured)

@app.route('/catalog', methods=['GET'])
def catalog():
    search = request.args.get('search', '').strip().lower()
    category_id = request.args.get('category_id')

    auctions = read_auctions()
    categories = read_categories()
    category_name_map = {c['category_id']: c['category_name'] for c in categories}
    filter_category_name = None
    try:
        if category_id is not None:
            category_id_int = int(category_id)
            filter_category_name = category_name_map.get(category_id_int)
    except Exception:
        filter_category_name = None

    filtered_auctions = []
    for a in auctions:
        match_search = False
        if search == '':
            match_search = True
        else:
            if (
                search in str(a['auction_id']).lower() or
                search in a['item_name'].lower() or
                search in a['description'].lower()
            ):
                match_search = True
        match_category = True
        if filter_category_name is not None:
            match_category = (a['category'].lower() == filter_category_name.lower())
        if match_search and match_category:
            filtered_auctions.append(a)

    return render_template('catalog.html', page_title='Auction Catalog', auctions=filtered_auctions, 
                           search=search, selected_category=filter_category_name, categories=['Electronics', 'Collectibles', 'Furniture', 'Art', 'Other'])

@app.route('/auction/<int:auction_id>', methods=['GET'])
def auction_details(auction_id):
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if auction is None:
        return "Auction not found", 404

    bids = read_bids()
    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    # Sort descending by bid_timestamp
    auction_bids_sorted = sorted(auction_bids, key=lambda b: b['bid_timestamp'], reverse=True)

    return render_template('auction_details.html', page_title='Auction Details', auction=auction, bids=auction_bids_sorted)

@app.route('/auction/<int:auction_id>/place_bid', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = read_auctions()
    auction = next((a for a in auctions if a['auction_id'] == auction_id), None)
    if auction is None:
        return "Auction not found", 404

    if request.method == 'GET':
        minimum_bid = auction['current_bid'] + 0.01  # Minimal increment 0.01
        return render_template('place_bid.html', page_title='Place Bid', auction=auction, minimum_bid=minimum_bid)

    # POST - submit bid
    bidder_name = request.form.get('bidder_name', '').strip()
    bid_amount_str = request.form.get('bid_amount', '').strip()

    error = None
    # Validate bidder_name
    if not bidder_name:
        error = 'Bidder name is required.'
    # Validate bid_amount
    try:
        bid_amount = float(bid_amount_str)
    except ValueError:
        error = 'Invalid bid amount.'

    if not error:
        if bid_amount <= auction['current_bid']:
            error = f'Bid amount must be higher than current bid ({auction["current_bid"]:.2f}).'

    if error:
        minimum_bid = auction['current_bid'] + 0.01
        return render_template('place_bid.html', page_title='Place Bid', auction=auction, minimum_bid=minimum_bid, error=error, 
                               bidder_name=bidder_name, bid_amount=bid_amount_str)

    # Proceed to append new bid
    bids = read_bids()
    new_bid_id = max([b['bid_id'] for b in bids], default=0) + 1
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

    new_bid = {
        'bid_id': new_bid_id,
        'auction_id': auction_id,
        'bidder_name': bidder_name,
        'bid_amount': bid_amount,
        'bid_timestamp': now_str
    }

    bids.append(new_bid)
    write_bids(bids)

    # Update auctions.txt current_bid
    for a in auctions:
        if a['auction_id'] == auction_id:
            a['current_bid'] = bid_amount
    write_auctions(auctions)

    # Update bid_history.txt
    history = read_bid_history()
    new_history_id = max([h['history_id'] for h in history], default=0) + 1
    new_history_item = {
        'history_id': new_history_id,
        'auction_id': auction_id,
        'auction_name': auction['item_name'],
        'bidder_name': bidder_name,
        'bid_amount': bid_amount,
        'bid_timestamp': now_str
    }
    history.append(new_history_item)
    write_bid_history(history)

    return redirect(url_for('auction_details', auction_id=auction_id))

@app.route('/bids', methods=['GET'])
def bid_history():
    auction_filter = request.args.get('auction')
    sort_amount = request.args.get('sort_amount', 'desc').lower()  # 'asc' or 'desc'

    bids = read_bids()
    auctions = read_auctions()
    auction_name_map = {a['auction_id']: a['item_name'] for a in auctions}

    filtered_bids = []
    for b in bids:
        if auction_filter is None or str(b['auction_id']) == auction_filter:
            filtered_bids.append(b)

    reverse_sort = (sort_amount == 'desc')
    filtered_bids_sorted = sorted(filtered_bids, key=lambda b: b['bid_amount'], reverse=reverse_sort)

    return render_template('bid_history.html', page_title='Bid History', bids=filtered_bids_sorted, auctions=auctions, 
                           selected_auction=auction_filter, sort_order=sort_amount)

@app.route('/categories', methods=['GET'])
def categories():
    categories_list = read_categories()
    return render_template('categories.html', page_title='Auction Categories', categories=categories_list)

@app.route('/winners', methods=['GET'])
def winners():
    filter_name = request.args.get('filter_name', '').strip().lower()
    winners_list = read_winners()
    if filter_name:
        winners_list = [w for w in winners_list if filter_name in w['winner_name'].lower()]
    return render_template('winners.html', page_title='Winning Items', winners=winners_list, filter_name=filter_name)

@app.route('/trending', methods=['GET'])
def trending():
    time_range = request.args.get('time_range', 'This Week')

    trending_list = read_trending()
    filtered_trending = [t for t in trending_list if t['time_period'] == time_range]
    filtered_trending_sorted = sorted(filtered_trending, key=lambda t: t['trending_rank'])

    return render_template('trending.html', page_title='Trending Auctions', trending=filtered_trending_sorted, time_range=time_range)

@app.route('/status', methods=['GET'])
def auction_status():
    status_filter = request.args.get('status', 'All')
    auctions = read_auctions()

    now = datetime.now()

    filtered_auctions = []
    for a in auctions:
        if status_filter != 'All' and a['status'] != status_filter:
            continue
        # Calculate time remaining for active or upcoming auctions
        try:
            end_time_obj = datetime.strptime(a['end_time'], '%Y-%m-%d %H:%M')
            if a['status'] == 'Active':
                time_remaining_delta = end_time_obj - now
                if time_remaining_delta.total_seconds() < 0:
                    time_remaining = 'Ended'
                else:
                    days = time_remaining_delta.days
                    hours, rem = divmod(time_remaining_delta.seconds, 3600)
                    minutes, _ = divmod(rem, 60)
                    time_remaining = f'{days}d {hours}h {minutes}m'
            elif a['status'] == 'Upcoming':
                time_remaining_delta = end_time_obj - now
                if time_remaining_delta.total_seconds() < 0:
                    time_remaining = 'Started'
                else:
                    days = time_remaining_delta.days
                    hours, rem = divmod(time_remaining_delta.seconds, 3600)
                    minutes, _ = divmod(rem, 60)
                    time_remaining = f'{days}d {hours}h {minutes}m'
            else:
                time_remaining = 'Ended'
        except Exception:
            time_remaining = 'Unknown'

        filtered_auctions.append({
            'auction_id': a['auction_id'],
            'item_name': a['item_name'],
            'status': a['status'],
            'time_remaining': time_remaining,
            'current_bid': a['current_bid']
        })

    return render_template('status.html', page_title='Auction Status', auctions=filtered_auctions, status_filter=status_filter)


if __name__ == '__main__':
    app.run(debug=True)
