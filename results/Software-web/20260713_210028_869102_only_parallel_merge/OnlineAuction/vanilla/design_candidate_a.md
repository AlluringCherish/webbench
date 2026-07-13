# Design Specification for OnlineAuction Web Application

---

## General Notes
- Application starts at **Dashboard Page**
- All data stored in local text files under `data/` directory.
- Data fields use pipe `|` delimiter consistently.
- Page navigation primarily via buttons with specific IDs.
- Flask routes adhere to RESTful conventions where applicable.

---

# 1. Dashboard Page

**Page Title (HTML and displayed):** Auction Dashboard

**Container Divs & IDs:**
- `dashboard-page` (main container div)
- `featured-auctions` (section with featured auction items)

**UI Elements:**
- Button: `browse-auctions-button` - Navigates to Auction Catalog Page
- Button: `view-bids-button` - Navigates to Bid History Page
- Button: `trending-auctions-button` - Navigates to Trending Auctions Page

**User Interactions & Navigation:**
- On click `browse-auctions-button` -> Route `/catalog` (GET)
- On click `view-bids-button` -> Route `/bid_history` (GET)
- On click `trending-auctions-button` -> Route `/trending` (GET)

**Data Used:**
- Loads `auctions.txt` to show featured auctions in `featured-auctions` div.
  - Typically select featured from top or manually flagged in code (not specified).

**Flask Route:**
```python
@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Load auctions.txt
    # Render dashboard.html with featured auctions
    pass
```


---

# 2. Auction Catalog Page

**Page Title:** Auction Catalog

**Container Divs & IDs:**
- `catalog-page` (main container)
- `search-input` (text input for search by name, description, or auction_id)
- `category-filter` (dropdown with options: Electronics, Collectibles, Furniture, Art, Other)
- `auctions-grid` (div grid to display multiple auction cards)
  - Each auction card includes:
    - Button with id `view-auction-button-{auction_id}` for viewing details

**User Interactions & Navigation:**
- Typing in `search-input` triggers search/filter (client-side JS or server-side request)
- Selecting option in `category-filter` filters auctions accordingly
- Clicking `view-auction-button-{auction_id}` directs to auction details page `/auction/{auction_id}`

**Data Used:**
- Reads `auctions.txt` with fields:
  - auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url
- Filter and search applies on item_name, description, auction_id, category

**Flask Routes:**
```python
@app.route('/catalog', methods=['GET'])
def catalog():
    # Retrieve optional query parameters for search and category
    # Load auctions.txt
    # Filter results accordingly
    # Render catalog.html with filtered auctions
    pass
```

```python
@app.route('/auction/<int:auction_id>', methods=['GET'])
def auction_details(auction_id):
    # Route to Auction Details Page (also serve details page)
    pass
```


---

# 3. Auction Details Page

**Page Title:** Auction Details

**Container Divs & IDs:**
- `auction-details-page` (main container)
- `auction-title` (H1 header showing item title)
- `auction-description` (div showing full description)
- `current-bid` (div showing current highest bid value)
- `place-bid-button` (button to place new bid)
- `bid-history` (div listing previous bids for this auction)

**User Interactions & Navigation:**
- Clicking `place-bid-button` navigates to Place Bid Page for this auction `/place_bid/<auction_id>`

**Data Used:**
- From `auctions.txt` select auction by `auction_id` for item_name, description, current_bid, status.
- From `bids.txt` select all bids with matching auction_id ordered by timestamp descending.

**Flask Routes:**
```python
@app.route('/auction/<int:auction_id>', methods=['GET'])
def auction_details(auction_id):
    # Load auction info and bids related to auction_id
    # Render auction_details.html with data
    pass
```


---

# 4. Place Bid Page

**Page Title:** Place Bid

**Container Divs & IDs:**
- `place-bid-page` (main container)
- `bidder-name` (input text box for bidder name)
- `bid-amount` (input text box for amount, numeric)
- `auction-name` (div displaying auction item name/title)
- `minimum-bid` (div displaying minimum acceptable bid amount - current highest bid + increment)
- `submit-bid-button` (button to submit new bid)

**User Interactions & Navigation:**
- Enter values into `bidder-name` and `bid-amount` inputs.
- Clicking `submit-bid-button` triggers bid submission.
- On success, redirect back to Auction Details page `/auction/<auction_id>`
- On failure (e.g., invalid bid amount), show validation error (client or server side).

**Data Used:**
- Uses `auctions.txt` to get auction info including current_bid to determine minimum bid.
- On submit, append new bid to `bids.txt` and also update `auctions.txt` current_bid for that auction.
- Also update `bid_history.txt` reflecting this new bid.

**Flask Routes:**
```python
@app.route('/place_bid/<int:auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id):
    if request.method == 'GET':
        # Load auction info for minimum bid and item name
        # Render place_bid.html
        pass
    elif request.method == 'POST':
        # Validate bidder_name and bid_amount
        # Validate bid_amount > current highest bid
        # Append new bid in bids.txt
        # Update auctions.txt
        # Append to bid_history.txt
        # Redirect to /auction/<auction_id>
        pass
```


---

# 5. Bid History Page

**Page Title:** Bid History

**Container Divs & IDs:**
- `bid-history-page` (main container)
- `bids-table` (table with columns: bid ID, auction name, bidder, amount, timestamp)
- `filter-by-auction` (dropdown to filter bids by auction)
- `sort-by-amount` (button to sort the bids ascending or descending by amount)
- `back-to-dashboard` (button to return to Dashboard)

**User Interactions & Navigation:**
- Selecting auction in `filter-by-auction` filters bids shown in `bids-table`.
- Clicking `sort-by-amount` toggles sorting of the bids list by amount.
- Clicking `back-to-dashboard` goes to `/dashboard`

**Data Used:**
- Reads `bids.txt` for all bid info.
- Reads `auctions.txt` for auction names to display.

**Flask Routes:**
```python
@app.route('/bid_history', methods=['GET'])
def bid_history():
    # Optionally take auction filter param
    # Load bids.txt and auctions.txt
    # Filter and sort as requested
    # Render bid_history.html
    pass
```


---

# 6. Auction Categories Page

**Page Title:** Auction Categories

**Container Divs & IDs:**
- `categories-page` (main container)
- `categories-list` (div containing all category cards)
  - Each category card has:
    - `category-card-{category_id}` (individual category card div)
    - Button `view-category-button-{category_id}` for viewing auctions in the category
- Button `back-to-dashboard` to return to Dashboard

**User Interactions & Navigation:**
- Clicking `view-category-button-{category_id}` navigates to `/category/{category_id}` showing auctions filtered by selected category.
- Clicking `back-to-dashboard` navigates to `/dashboard`

**Data Used:**
- Reads `categories.txt` fields:
  - category_id|category_name|description|item_count

**Flask Routes:**
```python
@app.route('/categories', methods=['GET'])
def categories():
    # Load categories.txt
    # Render categories.html
    pass
```

```python
@app.route('/category/<int:category_id>', methods=['GET'])
def category_auctions(category_id):
    # Load auctions.txt
    # Filter auctions by category matching category_id
    # Render filtered auctions page
    pass
```


---

# 7. Winners Page

**Page Title:** Winning Items

**Container Divs & IDs:**
- `winners-page` (main container)
- `winners-list` (div listing winning items cards)
  - Each winner card has `winner-card-{auction_id}`
- `filter-by-winner` (input text to filter winner names)
- `back-to-dashboard` button to return Dashboard

**User Interactions & Navigation:**
- Typing in `filter-by-winner` filters winners list by name.
- Clicking `back-to-dashboard` navigates to `/dashboard`

**Data Used:**
- Reads `winners.txt` file
  - winner_id|auction_id|item_name|winner_name|winning_bid|win_date

**Flask Routes:**
```python
@app.route('/winners', methods=['GET'])
def winners():
    # Load winners.txt
    # Apply any filter by winner name
    # Render winners.html
    pass
```


---

# 8. Trending Auctions Page

**Page Title:** Trending Auctions

**Container Divs & IDs:**
- `trending-page` (main container)
- `trending-list` (div showing ranked auctions with rank, title, current bid, bid count)
  - Buttons `view-auction-button-{auction_id}` on each item to view details
- `time-range-filter` (dropdown: Last 24 Hours, This Week, All Time)
- `back-to-dashboard` button to return Dashboard

**User Interactions & Navigation:**
- Selecting `time-range-filter` filters trending auctions by time period.
- Clicking `view-auction-button-{auction_id}` navigates to `/auction/{auction_id}`
- Clicking `back-to-dashboard` navigates to `/dashboard`

**Data Used:**
- Reads `trending.txt` fields:
  - auction_id|item_name|bid_count|current_bid|trending_rank|time_period

**Flask Routes:**
```python
@app.route('/trending', methods=['GET'])
def trending():
    # Accept time range parameter
    # Load trending.txt and filter
    # Render trending.html
    pass
```


---

# 9. Auction Status Page

**Page Title:** Auction Status

**Container Divs & IDs:**
- `status-page` (main container)
- `status-filter` (dropdown: All, Active, Closed, Upcoming)
- `status-table` (table with columns: name, status, time remaining, current bid)
- `refresh-status-button` (button to reload auction status data)
- `back-to-dashboard` button to return Dashboard

**User Interactions & Navigation:**
- Selecting `status-filter` filters auctions by status.
- Clicking `refresh-status-button` refreshes data.
- Clicking `back-to-dashboard` navigates to `/dashboard`

**Data Used:**
- Reads `auctions.txt` for all auction info including `status` and `end_time` (to compute time remaining).

**Flask Routes:**
```python
@app.route('/status', methods=['GET'])
def auction_status():
    # Load auctions.txt
    # Filter by status if provided
    # Render status.html
    pass
```


---

# Summary of Flask Routes and Methods

| Route Path                      | HTTP Method(s) | Description                                      |
|--------------------------------|----------------|--------------------------------------------------|
| /dashboard                     | GET            | Show Dashboard Page                              |
| /catalog                      | GET            | Show Auction Catalog Page (with optional filters)|
| /auction/&lt;auction_id&gt;      | GET            | Show Auction Details Page for auction_id        |
| /place_bid/&lt;auction_id&gt;   | GET, POST      | Show Place Bid form / Submit bid for auction_id  |
| /bid_history                   | GET            | Show Bid History Page                             |
| /categories                   | GET            | Show Auction Categories Page                      |
| /category/&lt;category_id&gt;   | GET            | Show auctions filtered by category_id             |
| /winners                      | GET            | Show Winners Page                                |
| /trending                     | GET            | Show Trending Auctions Page (filterable)         |
| /status                       | GET            | Show Auction Status Page                          |

---

# Data File Formats (Delimiters & Fields)

- auctions.txt:
  ```
  auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url
  ```
  - `auction_id` integer
  - `starting_bid`, `current_bid` decimal strings
  - `end_time` in `YYYY-MM-DD HH:MM` format
  - `status` in {Active, Closed, Upcoming}

- categories.txt:
  ```
  category_id|category_name|description|item_count
  ```

- bids.txt:
  ```
  bid_id|auction_id|bidder_name|bid_amount|bid_timestamp
  ```
  - `bid_timestamp` in `YYYY-MM-DD HH:MM` format

- winners.txt:
  ```
  winner_id|auction_id|item_name|winner_name|winning_bid|win_date
  ```

- bid_history.txt:
  ```
  history_id|auction_id|auction_name|bidder_name|bid_amount|bid_timestamp
  ```

- items.txt:
  ```
  item_id|auction_id|item_name|starting_price|category|condition|seller_name
  ```

- trending.txt:
  ```
  auction_id|item_name|bid_count|current_bid|trending_rank|time_period
  ```

---

# Navigation Flow Summary

- Start at `/dashboard` (Dashboard Page)
- From Dashboard:
  - `/catalog` (Auction Catalog)
  - `/bid_history` (Bid History)
  - `/trending` (Trending Auctions)
- From Auction Catalog:
  - `/auction/<auction_id>` (Auction Details)
- From Auction Details:
  - `/place_bid/<auction_id>` (Place Bid)
- From Place Bid:
  - On successful bid, redirect back to `/auction/<auction_id>`
- From Categories Page (`/categories`):
  - `/category/<category_id>` for auctions filtered by category
- Back buttons on Bid History, Categories, Winners, Trending, Status pages all go back to `/dashboard`

---

# End of Design Specification
