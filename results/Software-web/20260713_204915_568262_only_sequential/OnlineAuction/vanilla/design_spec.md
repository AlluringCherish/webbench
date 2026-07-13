# Design Specification for 'OnlineAuction' Web Application

---

## 1. Flask Routes and Templates

| Page Name           | Route Path                | HTTP Method(s) | Route Function Name     | Template Filename      |
|---------------------|---------------------------|----------------|------------------------|------------------------|
| Root (Redirect)      | `/`                       | GET            | root_redirect           | N/A (redirect)           |
| Dashboard           | `/dashboard`              | GET            | dashboard               | dashboard.html          |
| Auction Catalog     | `/catalog`                | GET            | auction_catalog         | catalog.html            |
| Auction Details     | `/auction/<int:auction_id>`| GET            | auction_details         | auction_details.html    |
| Place Bid           | `/place_bid/<int:auction_id>` | GET, POST   | place_bid               | place_bid.html          |
| Bid History         | `/bid_history`            | GET            | bid_history             | bid_history.html        |
| Auction Categories  | `/categories`             | GET            | auction_categories      | categories.html         |
| Winners             | `/winners`                | GET            | winners                 | winners.html            |
| Trending Auctions   | `/trending`               | GET            | trending_auctions       | trending.html           |
| Auction Status      | `/status`                 | GET            | auction_status          | status.html             |


### Notes:
- The root route `/` **must redirect** (HTTP 302) to `/dashboard`.
- `place_bid` route handles both GET (form display) and POST (bid submission).
- Auction Details route uses path parameter `auction_id` to show specific auction.
- Dynamic element IDs and buttons (e.g., `view-auction-button-{auction_id}`) correspond to these route paths.

---

## 2. Page Titles and Element IDs

### 2.1 Dashboard Page
- **Page Title:** Auction Dashboard
- **Element IDs:**
  - `dashboard-page`: main container div.
  - `featured-auctions`: div displaying featured auction items.
  - `browse-auctions-button`: button to navigate to Auction Catalog page.
  - `view-bids-button`: button to navigate to Bid History page.
  - `trending-auctions-button`: button to navigate to Trending Auctions page.

### 2.2 Auction Catalog Page
- **Page Title:** Auction Catalog
- **Element IDs:**
  - `catalog-page`: container div.
  - `search-input`: input field for searching auctions by item name, description, or ID.
  - `category-filter`: dropdown to filter auctions by category (Electronics, Collectibles, Furniture, Art, Other).
  - `auctions-grid`: div displaying the auction cards.
  - `view-auction-button-{auction_id}`: button per auction item to view details.

### 2.3 Auction Details Page
- **Page Title:** Auction Details
- **Element IDs:**
  - `auction-details-page`: container div.
  - `auction-title`: h1 element showing auction item title.
  - `auction-description`: div showing item description.
  - `current-bid`: div showing current highest bid amount.
  - `place-bid-button`: button to place a new bid.
  - `bid-history`: div section showing bid history with bidder names and amounts.

### 2.4 Place Bid Page
- **Page Title:** Place Bid
- **Element IDs:**
  - `place-bid-page`: container div.
  - `bidder-name`: input field for bidder's name.
  - `bid-amount`: input field for bid amount.
  - `auction-name`: div displaying auction item name.
  - `minimum-bid`: div displaying minimum acceptable bid amount.
  - `submit-bid-button`: button to submit the bid.

### 2.5 Bid History Page
- **Page Title:** Bid History
- **Element IDs:**
  - `bid-history-page`: container div.
  - `bids-table`: table listing bids with columns: bid ID, auction name, bidder, amount, timestamp.
  - `filter-by-auction`: dropdown to filter bids by auction.
  - `sort-by-amount`: button to sort bids by amount.
  - `back-to-dashboard`: button to navigate back to Dashboard.

### 2.6 Auction Categories Page
- **Page Title:** Auction Categories
- **Element IDs:**
  - `categories-page`: container div.
  - `categories-list`: div list showing categories with descriptions and item counts.
  - `category-card-{category_id}`: div card per category.
  - `view-category-button-{category_id}`: button to view items in category.
  - `back-to-dashboard`: button to navigate back to Dashboard.

### 2.7 Winners Page
- **Page Title:** Winning Items
- **Element IDs:**
  - `winners-page`: container div.
  - `winners-list`: div list showing winning items with winner info.
  - `winner-card-{auction_id}`: div card per winning auction item.
  - `filter-by-winner`: input field to filter winners by name.
  - `back-to-dashboard`: button to navigate back to Dashboard.

### 2.8 Trending Auctions Page
- **Page Title:** Trending Auctions
- **Element IDs:**
  - `trending-page`: container div.
  - `trending-list`: ranked list div showing rank, auction title, current bid, bid count.
  - `time-range-filter`: dropdown to filter by timeframe (Last 24 Hours, This Week, All Time).
  - `view-auction-button-{auction_id}`: button to view auction details.
  - `back-to-dashboard`: button to navigate back to Dashboard.

### 2.9 Auction Status Page
- **Page Title:** Auction Status
- **Element IDs:**
  - `status-page`: container div.
  - `status-filter`: dropdown to filter auctions by status (All, Active, Closed, Upcoming).
  - `status-table`: table listing auctions with columns: name, status, time remaining, current bid.
  - `refresh-status-button`: button to refresh auction status data.
  - `back-to-dashboard`: button to navigate back to Dashboard.

---

## 3. Navigation Mappings

### Navigation from Dashboard Page
- `browse-auctions-button`: `url_for('auction_catalog')` → `/catalog`
- `view-bids-button`: `url_for('bid_history')` → `/bid_history`
- `trending-auctions-button`: `url_for('trending_auctions')` → `/trending`

### Navigation from Auction Catalog Page
- `view-auction-button-{auction_id}`: `url_for('auction_details', auction_id=auction_id)` → `/auction/<auction_id>`

### Navigation from Auction Details Page
- `place-bid-button`: `url_for('place_bid', auction_id=auction_id)` → `/place_bid/<auction_id>`

### Navigation from Place Bid Page
- After bid submission (POST), redirect to Auction Details page: `url_for('auction_details', auction_id=auction_id)`

### Navigation from Bid History Page
- `back-to-dashboard`: `url_for('dashboard')` → `/dashboard`

### Navigation from Auction Categories Page
- `view-category-button-{category_id}`: `url_for('auction_catalog')` with category filter applied (e.g., query string) → `/catalog?category=category_id`
- `back-to-dashboard`: `url_for('dashboard')` → `/dashboard`

### Navigation from Winners Page
- `back-to-dashboard`: `url_for('dashboard')` → `/dashboard`

### Navigation from Trending Auctions Page
- `view-auction-button-{auction_id}`: `url_for('auction_details', auction_id=auction_id)` → `/auction/<auction_id>`
- `back-to-dashboard`: `url_for('dashboard')` → `/dashboard`

### Navigation from Auction Status Page
- `back-to-dashboard`: `url_for('dashboard')` → `/dashboard`

---

## 4. Context Variables Passed to Templates

### Dashboard Page (`dashboard.html`)
- `featured_auctions`: list of featured auction dicts (with fields: auction_id, item_name, current_bid, image_url, etc.)

### Auction Catalog Page (`catalog.html`)
- `auctions`: list of auction dicts matching search/filter
- `categories`: list of category dicts (id, name) for category-filter dropdown
- `selected_category`: category filter value (optional)
- `search_query`: string entered in search-input

### Auction Details Page (`auction_details.html`)
- `auction`: dict with full auction data
- `bid_history`: list of dicts with bid histories for auction (bidder_name, bid_amount, timestamp)

### Place Bid Page (`place_bid.html`)
- `auction`: dict with auction info (auction_id, item_name, minimum_bid)
- `errors`: optional dict with form validation errors

### Bid History Page (`bid_history.html`)
- `bids`: list of bid dicts (bid_id, auction_name, bidder_name, bid_amount, bid_timestamp)
- `auctions`: list of auctions for filter dropdown
- `selected_auction_id`: selected auction filter value (optional)
- `sort_order_amount`: boolean indicating current sort order by amount

### Auction Categories Page (`categories.html`)
- `categories`: list of category dicts (category_id, category_name, description, item_count)

### Winners Page (`winners.html`)
- `winners`: list of winning item dicts (auction_id, item_name, winner_name, winning_bid)
- `filter_name`: filter string for winner name (optional)

### Trending Auctions Page (`trending.html`)
- `trending_auctions`: list of dicts (auction_id, item_name, bid_count, current_bid, trending_rank, time_period)
- `selected_time_range`: selected time range filter string

### Auction Status Page (`status.html`)
- `auctions`: list of auction dicts (name, status, time_remaining, current_bid)
- `status_filter`: selected status filter string

---

## 5. Data File Handling Conventions

All data files are stored in the `data` directory relative to the application root.

### 5.1 auctions.txt
- **Path:** `data/auctions.txt`
- **Fields (pipe `|` delimited):**
  `auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url`
- **Usage:** Auctions catalog, auction details, auction status, trending auctions
- **Example:**
  `1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg`

### 5.2 categories.txt
- **Path:** `data/categories.txt`
- **Fields:**
  `category_id|category_name|description|item_count`
- **Usage:** Auction categories page and filters
- **Example:**
  `1|Electronics|Digital devices and gadgets|15`

### 5.3 bids.txt
- **Path:** `data/bids.txt`
- **Fields:**
  `bid_id|auction_id|bidder_name|bid_amount|bid_timestamp`
- **Usage:** Bid History page and auction details (bid history)
- **Example:**
  `1|1|Alice Johnson|45.50|2025-02-05 14:30`

### 5.4 winners.txt
- **Path:** `data/winners.txt`
- **Fields:**
  `winner_id|auction_id|item_name|winner_name|winning_bid|win_date`
- **Usage:** Winners page
- **Example:**
  `1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08`

### 5.5 bid_history.txt
- **Path:** `data/bid_history.txt`
- **Fields:**
  `history_id|auction_id|auction_name|bidder_name|bid_amount|bid_timestamp`
- **Usage:** Auction details bid history and bid history page
- **Example:**
  `1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00`

### 5.6 items.txt
- **Path:** `data/items.txt`
- **Fields:**
  `item_id|auction_id|item_name|starting_price|category|condition|seller_name`
- **Usage:** Possibly used in auction catalog or details indirectly
- **Example:**
  `1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector`

### 5.7 trending.txt
- **Path:** `data/trending.txt`
- **Fields:**
  `auction_id|item_name|bid_count|current_bid|trending_rank|time_period`
- **Usage:** Trending auctions page
- **Example:**
  `2|iPhone 14 Pro|12|620.00|1|This Week`

---

# End of Design Specification
