'''
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
app = Flask(__name__)
DATA_DIR = 'text'
def load_auctions():
    auctions = []
    filepath = os.path.join(DATA_DIR, 'auctions.txt')
    if not os.path.exists(filepath):
        return auctions
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 8:
                continue
            auction_id = parts[0]
            item_name = parts[1]
            category = parts[2]
            try:
                starting_price = float(parts[3])
                current_bid = float(parts[4])
                end_date = datetime.strptime(parts[5], '%Y-%m-%d %H:%M')
                status = parts[6].lower()
                image = parts[7]
            except Exception:
                continue
            auctions.append({
                'auction_id': auction_id,
                'item_name': item_name,
                'category': category,
                'starting_price': starting_price,
                'current_bid': current_bid,
                'end_date': end_date,
                'status': status,
                'image': image
            })
    return auctions
@app.route('/')
def dashboard():
    auctions = load_auctions()
    featured_auctions = [a for a in auctions if a['status'] == 'active'][:5]
    return render_template('dashboard.html',
                           featured_auctions=featured_auctions)
@app.route('/catalog')
def auction_catalog():
    auctions = load_auctions()
    category_filter = request.args.get('category', None)
    search_input = request.args.get('search', '').lower()
    filtered_auctions = auctions
    if category_filter and category_filter.lower() != 'all':
        filtered_auctions = [a for a in filtered_auctions if a['category'].lower() == category_filter.lower()]
    if search_input:
        filtered_auctions = [a for a in filtered_auctions if search_input in a['item_name'].lower()]
    return render_template('catalog.html',
                           auctions=filtered_auctions,
                           category_filter=category_filter,
                           search_input=search_input)
@app.route('/auction/<item_name>')
def auction_details(item_name):
    auctions = load_auctions()
    auction = next((a for a in auctions if a['item_name'].lower() == item_name.lower()), None)
    if not auction:
        return "Auction not found", 404
    # Load bid history for this auction
    bids = []
    bids_path = os.path.join(DATA_DIR, 'bids.txt')
    if os.path.exists(bids_path):
        with open(bids_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                bid_auction_id = parts[1]
                if bid_auction_id == auction['auction_id']:
                    bids.append({
                        'bid_id': parts[0],
                        'auction_id': parts[1],
                        'bidder_name': parts[2],
                        'bid_amount': float(parts[3]),
                        'bid_timestamp': parts[4]
                    })
    bids = sorted(bids, key=lambda x: x['bid_timestamp'], reverse=True)
    return render_template('auction_details.html',
                           auction=auction,
                           bids=bids)
@app.route('/place_bid/<item_name>', methods=['GET', 'POST'])
def place_bid(item_name):
    auctions = load_auctions()
    auction = next((a for a in auctions if a['item_name'].lower() == item_name.lower()), None)
    if not auction:
        return "Auction not found", 404
    error = None
    if request.method == 'POST':
        bidder_name = request.form.get('bidder_name', '').strip()
        bid_amount_str = request.form.get('bid_amount', '').strip()
        try:
            bid_amount = float(bid_amount_str)
        except ValueError:
            error = "Invalid bid amount."
            return render_template('place_bid.html', auction=auction, error=error)
        minimum_bid = auction['current_bid'] + 0.01
        if bid_amount < minimum_bid:
            error = f"Bid must be at least {minimum_bid:.2f}."
            return render_template('place_bid.html', auction=auction, error=error)
        if not bidder_name:
            error = "Bidder name is required."
            return render_template('place_bid.html', auction=auction, error=error)
        # Append bid to bids.txt
        bids_path = os.path.join(DATA_DIR, 'bids.txt')
        bid_id = 1
        if os.path.exists(bids_path):
            with open(bids_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    if last_line:
                        last_bid_id = int(last_line.split('|')[0])
                        bid_id = last_bid_id + 1
        bid_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        new_bid_line = f"{bid_id}|{auction['auction_id']}|{bidder_name}|{bid_amount:.2f}|{bid_timestamp}\n"
        with open(bids_path, 'a', encoding='utf-8') as f:
            f.write(new_bid_line)
        # Update current bid in auctions.txt
        auctions_path = os.path.join(DATA_DIR, 'auctions.txt')
        updated_lines = []
        with open(auctions_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) < 8:
                    updated_lines.append(line)
                    continue
                if parts[0] == auction['auction_id']:
                    parts[4] = f"{bid_amount:.2f}"
                    updated_line = '|'.join(parts) + '\n'
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line)
        with open(auctions_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        return redirect(url_for('auction_details', item_name=item_name))
    minimum_bid = auction['current_bid'] + 0.01
    return render_template('place_bid.html', auction=auction, minimum_bid=minimum_bid, error=error)
@app.route('/history')
def bid_history():
    bids = []
    bids_path = os.path.join(DATA_DIR, 'bids.txt')
    if os.path.exists(bids_path):
        with open(bids_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 5:
                    continue
                bids.append({
                    'bid_id': parts[0],
                    'auction_id': parts[1],
                    'bidder_name': parts[2],
                    'bid_amount': float(parts[3]),
                    'bid_timestamp': parts[4]
                })
    sort_by = request.args.get('sort', 'timestamp')
    if sort_by == 'amount':
        bids = sorted(bids, key=lambda x: x['bid_amount'], reverse=True)
    else:
        bids = sorted(bids, key=lambda x: x['bid_timestamp'], reverse=True)
    return render_template('history.html', bids=bids)
@app.route('/categories')
def categories():
    categories = []
    filepath = os.path.join(DATA_DIR, 'categories.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                categories.append({
                    'category_id': parts[0],
                    'category_name': parts[1],
                    'description': parts[2],
                    'item_count': parts[3]
                })
    return render_template('categories.html', categories=categories)
@app.route('/winners')
def winners():
    winners = []
    filepath = os.path.join(DATA_DIR, 'winners.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                winners.append({
                    'winner_id': parts[0],
                    'auction_id': parts[1],
                    'item_name': parts[2],
                    'winner_name': parts[3],
                    'winning_bid': float(parts[4]),
                    'win_date': parts[5]
                })
    filter_name = request.args.get('filter_name', '').lower()
    if filter_name:
        winners = [w for w in winners if filter_name in w['winner_name'].lower()]
    return render_template('winners.html', winners=winners, filter_name=filter_name)
@app.route('/trending')
def trending():
    trending_auctions = []
    filepath = os.path.join(DATA_DIR, 'trending.txt')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) < 6:
                    continue
                trending_auctions.append({
                    'auction_id': parts[0],
                    'item_name': parts[1],
                    'bid_count': int(parts[2]),
                    'current_bid': float(parts[3]),
                    'trending_rank': int(parts[4]),
                    'time_period': parts[5]
                })
    time_range = request.args.get('range', 'This Week')
    filtered = [t for t in trending_auctions if t['time_period'].lower() == time_range.lower()]
    if not filtered:
        filtered = trending_auctions
    filtered = sorted(filtered, key=lambda x: x['trending_rank'])
    return render_template('trending.html', trending=filtered, time_range=time_range)
@app.route('/status')
def auction_status():
    auctions = load_auctions()
    status_filter = request.args.get('status', 'All').lower()
    if status_filter != 'all':
        auctions = [a for a in auctions if a['status'] == status_filter]
    auctions = sorted(auctions, key=lambda x: x['end_date'])
    return render_template('status.html', auctions=auctions, status_filter=status_filter)
@app.route('/refresh_status')
def refresh_status():
    # This would normally update auction statuses based on current time
    # For simplicity, just redirect to status page
    return redirect(url_for('auction_status'))
if __name__ == '__main__':
    app.run(debug=True)
'''