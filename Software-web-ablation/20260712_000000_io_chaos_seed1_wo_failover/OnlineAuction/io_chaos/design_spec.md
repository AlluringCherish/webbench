# OnlineAuction Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path               | Function Name            | HTTP Method | Template Rendered         | Context Variables Passed                                                                              |
|--------------------------|--------------------------|-------------|---------------------------|-----------------------------------------------------------------------------------------------------|
| /                        | root_redirect            | GET         | Redirect to `/dashboard`  | None                                                                                                |
| /dashboard               | dashboard_view           | GET         | dashboard.html            | featured_auctions: list of dict{auction_id: int, item_name: str, current_bid: float},
|                          |                          |             |                           | trending_auctions: list of dict{auction_id: int, item_name: str, current_bid: float, bid_count: int},
|                          |                          |             |                           | (additional navigation elements no context needed)                                                |
| /catalog                 | auction_catalog          | GET         | catalog.html              | auctions: list of dict{
|                          |                          |             |                           | auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str (datetime in str), image_url: str
|                          |                          |             |                           | },
|                          |                          |             |                           | categories: list of dict{category_id: int, category_name: str} (for category filter options)         |
| /auction/<int:auction_id>| auction_details          | GET         | auction_details.html      | auction: dict{
|                          |                          |             |                           | auction_id: int, item_name: str, description: str, current_bid: float, end_time: str, status: str
|                          |                          |             |                           | },
|                          |                          |             |                           | bid_history: list of dict{bidder_name: str, bid_amount: float, bid_timestamp: str}                    |
| /auction/<int:auction_id>/place_bid | place_bid           | GET         | place_bid.html            | auction: dict{auction_id: int, item_name: str, minimum_bid: float}                                  |
| /auction/<int:auction_id>/place_bid | submit_bid          | POST        | place_bid.html            | auction: dict{auction_id: int, item_name: str, minimum_bid: float}, error_message: str (optional)     |
| /bids                    | bid_history_view         | GET         | bid_history.html          | bids: list of dict{
|                          |                          |             |                           | bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str
|                          |                          |             |                           | },
|                          |                          |             |                           | auctions: list of dict{auction_id: int, auction_name: str} (for filter dropdown)                      |
| /categories              | categories_view          | GET         | categories.html           | categories: list of dict{category_id: int, category_name: str, description: str, item_count: int}     |
| /winners                 | winners_view             | GET         | winners.html              | winners: list of dict{auction_id: int, item_name: str, winner_name: str, winning_bid: float}          |
| /trending                | trending_auctions_view   | GET         | trending.html             | trending_auctions: list of dict{
|                          |                          |             |                           | auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str
|                          |                          |             |                           | }                                                                                                   |
| /status                  | auction_status_view      | GET         | status.html               | auctions_status: list of dict{
|                          |                          |             |                           | auction_id: int, item_name: str, status: str, time_remaining: str, current_bid: float
|                          |                          |             |                           | }                                                                                                   |

---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template: templates/dashboard.html
- Page Title: Auction Dashboard
- Elements:
  - Div container with id="dashboard-page"
  - Div with id="featured-auctions" (displays featured auction items)
  - Button with id="browse-auctions-button" (navigates to auction_catalog)
  - Button with id="view-bids-button" (navigates to bid_history_view)
  - Button with id="trending-auctions-button" (navigates to trending_auctions_view)
- Navigation:
  - browse-auctions-button: url_for('auction_catalog')
  - view-bids-button: url_for('bid_history_view')
  - trending-auctions-button: url_for('trending_auctions_view')
- Context Variables:
  - featured_auctions: list of dict{auction_id: int, item_name: str, current_bid: float}
  - trending_auctions: list of dict{auction_id: int, item_name: str, current_bid: float, bid_count: int}

---

### 2. Auction Catalog Page
- Template: templates/catalog.html
- Page Title: Auction Catalog
- Elements:
  - Div container with id="catalog-page"
  - Input with id="search-input"
  - Dropdown with id="category-filter" with options: Electronics, Collectibles, Furniture, Art, Other
  - Div grid with id="auctions-grid" containing auction cards
  - Buttons with dynamic id="view-auction-button-{{ auction.auction_id }}" for each auction card
- Navigation:
  - view-auction-button-{{ auction.auction_id }}: url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - auctions: list of dict{auction_id, item_name, description, category, current_bid, end_time, image_url}
  - categories: list of dict{category_id, category_name}

---

### 3. Auction Details Page
- Template: templates/auction_details.html
- Page Title: Auction Details
- Elements:
  - Div container with id="auction-details-page"
  - H1 with id="auction-title"
  - Div with id="auction-description"
  - Div with id="current-bid"
  - Button with id="place-bid-button" (navigates to place_bid)
  - Div with id="bid-history" showing bidder names and amounts
- Navigation:
  - place-bid-button: url_for('place_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict{auction_id, item_name, description, current_bid, end_time, status}
  - bid_history: list of dict{bidder_name, bid_amount, bid_timestamp}

---

### 4. Place Bid Page
- Template: templates/place_bid.html
- Page Title: Place Bid
- Elements:
  - Div container with id="place-bid-page"
  - Input with id="bidder-name"
  - Input with id="bid-amount"
  - Div with id="auction-name"
  - Div with id="minimum-bid"
  - Button with id="submit-bid-button"
- Navigation:
  - submit-bid-button posts to url_for('submit_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict{auction_id, item_name, minimum_bid}
  - error_message: str (optional, shown on failed bid attempts)

---

### 5. Bid History Page
- Template: templates/bid_history.html
- Page Title: Bid History
- Elements:
  - Div container with id="bid-history-page"
  - Table with id="bids-table" containing columns: bid ID, auction name, bidder, amount, timestamp
  - Dropdown with id="filter-by-auction" to filter bids by auction
  - Button with id="sort-by-amount" to sort bids by amount
  - Button with id="back-to-dashboard" (navigates to dashboard_view)
- Navigation:
  - back-to-dashboard: url_for('dashboard_view')
- Context Variables:
  - bids: list of dict{bid_id, auction_name, bidder_name, bid_amount, bid_timestamp}
  - auctions: list of dict{auction_id, auction_name} for filter dropdown

---

### 6. Auction Categories Page
- Template: templates/categories.html
- Page Title: Auction Categories
- Elements:
  - Div container with id="categories-page"
  - Div with id="categories-list" containing category cards
  - Div with dynamic id="category-card-{{ category.category_id }}" for each category
  - Button with dynamic id="view-category-button-{{ category.category_id }}" for each category
  - Button with id="back-to-dashboard" (navigates to dashboard_view)
- Navigation:
  - view-category-button-{{ category.category_id }}: url_for('auction_catalog') filtered by category
  - back-to-dashboard: url_for('dashboard_view')
- Context Variables:
  - categories: list of dict{category_id, category_name, description, item_count}

---

### 7. Winners Page
- Template: templates/winners.html
- Page Title: Winning Items
- Elements:
  - Div container with id="winners-page"
  - Div with id="winners-list" containing winner cards
  - Div with dynamic id="winner-card-{{ winner.auction_id }}" for each winning item
  - Input with id="filter-by-winner" to filter by winner name
  - Button with id="back-to-dashboard" (navigates to dashboard_view)
- Navigation:
  - back-to-dashboard: url_for('dashboard_view')
- Context Variables:
  - winners: list of dict{auction_id, item_name, winner_name, winning_bid}

---

### 8. Trending Auctions Page
- Template: templates/trending.html
- Page Title: Trending Auctions
- Elements:
  - Div container with id="trending-page"
  - Div with id="trending-list" listing ranked auctions
  - Dropdown with id="time-range-filter" with options: Last 24 Hours, This Week, All Time
  - Buttons with dynamic id="view-auction-button-{{ auction.auction_id }}" for each trending item
  - Button with id="back-to-dashboard" (navigates to dashboard_view)
- Navigation:
  - view-auction-button-{{ auction.auction_id }}: url_for('auction_details', auction_id=auction.auction_id)
  - back-to-dashboard: url_for('dashboard_view')
- Context Variables:
  - trending_auctions: list of dict{auction_id, item_name, bid_count, current_bid, trending_rank, time_period}

---

### 9. Auction Status Page
- Template: templates/status.html
- Page Title: Auction Status
- Elements:
  - Div container with id="status-page"
  - Dropdown with id="status-filter" with options: All, Active, Closed, Upcoming
  - Table with id="status-table" showing auctions with columns: name, status, time remaining, current bid
  - Button with id="refresh-status-button" to refresh statuses
  - Button with id="back-to-dashboard" (navigates to dashboard_view)
- Navigation:
  - back-to-dashboard: url_for('dashboard_view')
- Context Variables:
  - auctions_status: list of dict{auction_id, item_name, status, time_remaining, current_bid}

---

## Section 3: Data File Schemas (Backend)

### 1. Auctions Data
- Path: data/auctions.txt
- Format: Pipe-delimited (|), no header line
- Fields:
  1. auction_id (int)
  2. item_name (str)
  3. description (str)
  4. category (str)
  5. starting_bid (float)
  6. current_bid (float)
  7. end_time (str: "YYYY-MM-DD HH:MM")
  8. status (str: "Active", "Closed", etc.)
  9. image_url (str)
- Purpose: Stores all auction items with details and current bidding status.
- Examples:
  - 1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  - 2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  - 3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg

---

### 2. Categories Data
- Path: data/categories.txt
- Format: Pipe-delimited (|), no header line
- Fields:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
  4. item_count (int)
- Purpose: Contains all auction categories with descriptions and counts.
- Examples:
  - 1|Electronics|Digital devices and gadgets|15
  - 2|Collectibles|Rare and valuable collector items|28
  - 3|Furniture|Household furniture and decor|12

---

### 3. Bids Data
- Path: data/bids.txt
- Format: Pipe-delimited (|), no header line
- Fields:
  1. bid_id (int)
  2. auction_id (int)
  3. bidder_name (str)
  4. bid_amount (float)
  5. bid_timestamp (str: "YYYY-MM-DD HH:MM")
- Purpose: Records all bids placed with details.
- Examples:
  - 1|1|Alice Johnson|45.50|2025-02-05 14:30
  - 2|2|Bob Williams|620.00|2025-02-05 15:45
  - 3|3|Charlie Brown|110.00|2025-02-04 10:15

---

### 4. Winners Data
- Path: data/winners.txt
- Format: Pipe-delimited (|), no header line
- Fields:
  1. winner_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. winner_name (str)
  5. winning_bid (float)
  6. win_date (str: "YYYY-MM-DD")
- Purpose: Lists auction winning items with winner details.
- Examples:
  - 1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  - 2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  - 3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01

---

### 5. Bid History Data
- Path: data/bid_history.txt
- Format: Pipe-delimited (|), no header line
- Fields:
  1. history_id (int)
  2. auction_id (int)
  3. auction_name (str)
  4. bidder_name (str)
  5. bid_amount (float)
  6. bid_timestamp (str: "YYYY-MM-DD HH:MM")
- Purpose: Tracks all bid events historically.
- Examples:
  - 1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  - 2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  - 3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45

---

### 6. Items Data
- Path: data/items.txt
- Format: Pipe-delimited (|), no header line
- Fields:
  1. item_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. starting_price (float)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Purpose: Stores detailed item information associated with auctions.
- Examples:
  - 1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  - 2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  - 3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop

---

### 7. Trending Data
- Path: data/trending.txt
- Format: Pipe-delimited (|), no header line
- Fields:
  1. auction_id (int)
  2. item_name (str)
  3. bid_count (int)
  4. current_bid (float)
  5. trending_rank (int)
  6. time_period (str: e.g. "This Week")
- Purpose: Contains ranked trending auction information.
- Examples:
  - 2|iPhone 14 Pro|12|620.00|1|This Week
  - 1|Vintage Leather Watch|8|45.50|2|This Week
  - 5|Vintage Camera|6|85.00|3|This Week

---

# End of Design Specification Document
