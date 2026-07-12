from flask import Flask, render_template, redirect, url_for, request, flash
import os
import datetime
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

DATA_DIR = 'data'

# File paths
AUCTIONS_FILE = os.path.join(DATA_DIR, 'auctions.txt')
BIDS_FILE = os.path.join(DATA_DIR, 'bids.txt')
CATEGORIES_FILE = os.path.join(DATA_DIR, 'categories.txt')
WINNERS_FILE = os.path.join(DATA_DIR, 'winners.txt')
TRENDING_FILE = os.path.join(DATA_DIR, 'trending.txt')
BID_HISTORY_FILE = os.path.join(DATA_DIR, 'bid_history.txt')


# Util functions for reading and writing pipe-delimited files

def read_pipe_delimited_file(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = [line.strip() for line in f if line.strip()]
    return content


def write_pipe_delimited_file(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')


# Data loading/parsing functions

def load_auctions():
    """
    Loads auctions from auctions.txt
    Format: id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url
    """
    lines = read_pipe_delimited_file(AUCTIONS_FILE)
    auctions = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 9:
            id_, item_name, description, category, starting_bid, current_bid, end_time, status, image_url = parts
            auctions.append({
                'id': id_,
                'item_name': item_name,
                'description': description,
                'category': category,
                'starting_bid': float(starting_bid),
                'current_bid': float(current_bid),
                'end_time': end_time,
                'status': status,
                'image_url': image_url
            })
    return auctions


def write_auctions(auctions):
    lines = []
    for a in auctions:
        line = '|'.join([
            a['id'],
            a['item_name'],
            a['description'],
            a['category'],
            f"{a['starting_bid']:.2f}",
            f"{a['current_bid']:.2f}",
            a['end_time'],
            a['status'],
            a['image_url']
        ])
        lines.append(line)
    write_pipe_delimited_file(AUCTIONS_FILE, lines)


def load_bids():
    """
    Loads bids from bids.txt
    Format: bid_id|auction_id|user|bid_amount|timestamp
    """
    lines = read_pipe_delimited_file(BIDS_FILE)
    bids = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 5:
            bid_id, auction_id, user, bid_amount, timestamp = parts
            bids.append({
                'bid_id': int(bid_id),
                'auction_id': auction_id,
                'user': user,
                'bid_amount': float(bid_amount),
                'timestamp': timestamp
            })
    return bids


def write_bids(bids):
    lines = []
    for b in bids:
        line = '|'.join([
            str(b['bid_id']),
            b['auction_id'],
            b['user'],
            f"{b['bid_amount']:.2f}",
            b['timestamp']
        ])
        lines.append(line)
    write_pipe_delimited_file(BIDS_FILE, lines)


def load_categories():
    lines = read_pipe_delimited_file(CATEGORIES_FILE)
    categories = [line for line in lines]
    return categories


def load_winners():
    lines = read_pipe_delimited_file(WINNERS_FILE)
    winners = []
    for line in lines:
        parts = line.split('|')
        if len(parts) >= 2:
            winners.append(parts)
    return winners


def load_trending():
    lines = read_pipe_delimited_file(TRENDING_FILE)
    trending = []
    for line in lines:
        parts = line.split('|')
        trending.append(parts)
    return trending


def load_bid_history():
    lines = read_pipe_delimited_file(BID_HISTORY_FILE)
    hist = []
    for line in lines:
        parts = line.split('|')
        hist.append(parts)
    return hist


def time_remaining(end_time):
    try:
        end_dt = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return "Invalid date"
    now = datetime.datetime.now()
    delta = end_dt - now
    if delta.total_seconds() <= 0:
        return "Ended"
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0 or days > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return ' '.join(parts)


@app.route('/')
def root():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    auctions = load_auctions()
    # Update auction status if ended
    now = datetime.datetime.now()
    updated = False
    for auction in auctions:
        try:
            end_dt = datetime.datetime.strptime(auction['end_time'], '%Y-%m-%d %H:%M:%S')
            if now > end_dt and auction['status'] != 'ended':
                auction['status'] = 'ended'
                updated = True
        except ValueError:
            continue
        auction['time_remaining'] = time_remaining(auction['end_time'])
    if updated:
        write_auctions(auctions)
    return render_template('dashboard.html', auctions=auctions)


@app.route('/catalog')
def catalog():
    auctions = load_auctions()
    categories = load_categories()
    # Build category dropdown and auction listing
    return render_template('catalog.html', auctions=auctions, categories=categories)


@app.route('/auction/<auction_id>', methods=['GET'])
def auction_detail(auction_id):
    auctions = load_auctions()
    bids = load_bids()
    auction = next((a for a in auctions if a['id'] == auction_id), None)
    if auction is None:
        flash('Auction not found.')
        return redirect(url_for('catalog'))
    auction_bids = [b for b in bids if b['auction_id'] == auction_id]
    auction_bids.sort(key=lambda b: b['timestamp'])
    return render_template('auction_detail.html', auction=auction, bids=auction_bids)


@app.route('/auction/<auction_id>/bid', methods=['GET', 'POST'])
def place_bid(auction_id):
    auctions = load_auctions()
    bids = load_bids()
    auction = next((a for a in auctions if a['id'] == auction_id), None)
    if auction is None:
        flash('Auction not found.')
        return redirect(url_for('catalog'))

    if request.method == 'POST':
        user = request.form.get('user', '').strip()
        bid_amount_str = request.form.get('bid_amount', '').strip()
        if not user or not bid_amount_str:
            flash('User and bid amount are required.')
            return redirect(url_for('place_bid', auction_id=auction_id))

        try:
            bid_amount = float(bid_amount_str)
        except ValueError:
            flash('Invalid bid amount.')
            return redirect(url_for('place_bid', auction_id=auction_id))

        if auction['status'] == 'ended':
            flash('Auction has ended. No more bids accepted.')
            return redirect(url_for('auction_detail', auction_id=auction_id))

        min_bid = max(auction['starting_bid'], auction['current_bid'])
        if bid_amount <= min_bid:
            flash(f'Bid must be greater than current bid (${min_bid:.2f}).')
            return redirect(url_for('place_bid', auction_id=auction_id))

        # Determine new bid id
        max_bid_id = max((b['bid_id'] for b in bids), default=0)
        new_bid_id = max_bid_id + 1
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_bid = {
            'bid_id': new_bid_id,
            'auction_id': auction_id,
            'user': user,
            'bid_amount': bid_amount,
            'timestamp': timestamp
        }
        bids.append(new_bid)
        # Update current bid
        auction['current_bid'] = bid_amount

        # Write updated bids and auctions
        write_bids(bids)
        write_auctions(auctions)

        flash('Bid placed successfully!')
        return redirect(url_for('auction_detail', auction_id=auction_id))

    return render_template('place_bid.html', auction=auction)


if __name__ == '__main__':
    app.run(debug=True)
