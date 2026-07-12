# OnlineAuction Design Specification Document

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                      | Function Name                 | HTTP Method | Template to Render       | Context Variables Passed to Template (Type Annotations)                                                                                                   |
|--------------------------------|-------------------------------|-------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| /                              | home_redirect                 | GET         | Redirect to /dashboard   | None                                                                                                                     |
| /dashboard                    | dashboard                    | GET         | dashboard.html          | featured_auctions (list of dict {auction_id: int, item_name: str, current_bid: float, end_time: str, image_url: str}), trending_auctions (list of dict {auction_id: int, item_name: str, current_bid: float, bid_count: int, trending_rank: int}), no additional variables |
| /catalog                     | auction_catalog              | GET         | catalog.html            | auctions (list of dict {auction_id: int, item_name: str, description: str, category: str, starting_bid: float, current_bid: float, end_time: str, status: str, image_url: str}), categories (list of dict {category_id: int, category_name: str, description: str, item_count: int}), selected_category (str), search_query (str) |
| /auction/<int:auction_id>    | auction_details              | GET         | auction_details.html    | auction (dict {auction_id: int, item_name: str, description: str, category: str, starting_bid: float, current_bid: float, end_time: str, status: str, image_url: str}), bids (list of dict {bid_id: int, auction_id: int, bidder_name: str, bid_amount: float, bid_timestamp: str})                                                           |
| /auction/<int:auction_id>/place_bid | place_bid               | GET, POST   | place_bid.html          | auction (dict {auction_id: int, item_name: str, starting_bid: float, current_bid: float}), minimum_bid (float, calculated as current_bid + minimal increment in backend)                                                                                             |
| /bid_history                 | bid_history                 | GET         | bid_history.html        | bids (list of dict {bid_id: int, auction_id: int, bidder_name: str, bid_amount: float, bid_timestamp: str}), auctions (list of dict {auction_id: int, item_name: str})                                                                                              |
| /categories                 | auction_categories          | GET         | categories.html         | categories (list of dict {category_id: int, category_name: str, description: str, item_count: int})                                                                                                                  |
| /winners                    | winners                    | GET         | winners.html            | winners (list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str})                                                                                         |
| /trending                   | trending_auctions           | GET         | trending.html           | trending_auctions (list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}), selected_time_range (str)                                               |
| /status                    | auction_status              | GET         | status.html             | auctions (list of dict {auction_id: int, item_name: str, status: str, end_time: str, current_bid: float}), selected_status_filter (str)                                                                              |

---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template: templates/dashboard.html
- Page Title: Auction Dashboard
- Elements (with exact IDs and types):
  - div#dashboard-page
  - div#featured-auctions
  - button#browse-auctions-button
  - button#view-bids-button
  - button#trending-auctions-button
- Navigation:
  - browse-auctions-button → url_for('auction_catalog')
  - view-bids-button → url_for('bid_history')
  - trending-auctions-button → url_for('trending_auctions')
- Context Variables:
  - featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, end_time: str, image_url: str}
  - trending_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, bid_count: int, trending_rank: int}

### 2. Auction Catalog Page
- Template: templates/catalog.html
- Page Title: Auction Catalog
- Elements:
  - div#catalog-page
  - input#search-input
  - select#category-filter
  - div#auctions-grid
  - button#view-auction-button-{{ auction.auction_id }} (dynamic per auction)
- Navigation:
  - view-auction-button-{{ auction.auction_id }} → url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - auctions: list of dict {auction_id, item_name, description, category, starting_bid, current_bid, end_time, status, image_url}
  - categories: list of dict {category_id, category_name, description, item_count}
  - selected_category: str
  - search_query: str

### 3. Auction Details Page
- Template: templates/auction_details.html
- Page Title: Auction Details
- Elements:
  - div#auction-details-page
  - h1#auction-title
  - div#auction-description
  - div#current-bid
  - button#place-bid-button
  - div#bid-history
- Navigation:
  - place-bid-button → url_for('place_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict {auction_id, item_name, description, category, starting_bid, current_bid, end_time, status, image_url}
  - bids: list of dict {bid_id, auction_id, bidder_name, bid_amount, bid_timestamp}

### 4. Place Bid Page
- Template: templates/place_bid.html
- Page Title: Place Bid
- Elements:
  - div#place-bid-page
  - input#bidder-name
  - input#bid-amount
  - div#auction-name
  - div#minimum-bid
  - button#submit-bid-button
- Navigation:
  - submit-bid-button → POST submission to /auction/<int:auction_id>/place_bid
- Context Variables:
  - auction: dict {auction_id, item_name, starting_bid, current_bid}
  - minimum_bid: float

### 5. Bid History Page
- Template: templates/bid_history.html
- Page Title: Bid History
- Elements:
  - div#bid-history-page
  - table#bids-table
  - select#filter-by-auction
  - button#sort-by-amount
  - button#back-to-dashboard
- Navigation:
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - bids: list of dict {bid_id, auction_id, bidder_name, bid_amount, bid_timestamp}
  - auctions: list of dict {auction_id, item_name}

### 6. Auction Categories Page
- Template: templates/categories.html
- Page Title: Auction Categories
- Elements:
  - div#categories-page
  - div#categories-list
  - div#category-card-{{ category.category_id }} (dynamic per category)
  - button#view-category-button-{{ category.category_id }} (dynamic per category)
  - button#back-to-dashboard
- Navigation:
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - categories: list of dict {category_id, category_name, description, item_count}

### 7. Winners Page
- Template: templates/winners.html
- Page Title: Winning Items
- Elements:
  - div#winners-page
  - div#winners-list
  - div#winner-card-{{ winner.auction_id }} (dynamic per winner)
  - input#filter-by-winner
  - button#back-to-dashboard
- Navigation:
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - winners: list of dict {winner_id, auction_id, item_name, winner_name, winning_bid, win_date}

### 8. Trending Auctions Page
- Template: templates/trending.html
- Page Title: Trending Auctions
- Elements:
  - div#trending-page
  - div#trending-list
  - select#time-range-filter
  - button#view-auction-button-{{ auction.auction_id }} (dynamic per trending auction)
  - button#back-to-dashboard
- Navigation:
  - back-to-dashboard → url_for('dashboard')
  - view-auction-button-{{ auction.auction_id }} → url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - trending_auctions: list of dict {auction_id, item_name, bid_count, current_bid, trending_rank, time_period}
  - selected_time_range: str

### 9. Auction Status Page
- Template: templates/status.html
- Page Title: Auction Status
- Elements:
  - div#status-page
  - select#status-filter
  - table#status-table
  - button#refresh-status-button
  - button#back-to-dashboard
- Navigation:
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - auctions: list of dict {auction_id, item_name, status, end_time, current_bid}
  - selected_status_filter: str

---

## Section 3: Data File Schemas (Backend)

### 1. Auctions Data
- Path: data/auctions.txt
- File format: pipe-delimited (|), no header line
- Fields in order:
  1. auction_id (int)
  2. item_name (str)
  3. description (str)
  4. category (str)
  5. starting_bid (float)
  6. current_bid (float)
  7. end_time (str, datetime format YYYY-MM-DD HH:MM)
  8. status (str: Active, Closed, Upcoming)
  9. image_url (str)
- Purpose: Stores all auction item details including current bids and status.
- Example rows:
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg

### 2. Categories Data
- Path: data/categories.txt
- File format: pipe-delimited (|), no header line
- Fields:
  1. category_id (int)
  2. category_name (str)
  3. description (str)
  4. item_count (int)
- Purpose: Stores auction categories metadata including item counts.
- Example rows:
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12

### 3. Bids Data
- Path: data/bids.txt
- File format: pipe-delimited (|), no header line
- Fields:
  1. bid_id (int)
  2. auction_id (int)
  3. bidder_name (str)
  4. bid_amount (float)
  5. bid_timestamp (str, datetime format YYYY-MM-DD HH:MM)
- Purpose: Stores individual bids placed with bidder details and timestamps.
- Example rows:
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15

### 4. Winners Data
- Path: data/winners.txt
- File format: pipe-delimited (|), no header line
- Fields:
  1. winner_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. winner_name (str)
  5. winning_bid (float)
  6. win_date (str, date format YYYY-MM-DD)
- Purpose: Stores winner information for auctions closed with winning bids.
- Example rows:
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01

### 5. Bid History Data
- Path: data/bid_history.txt
- File format: pipe-delimited (|), no header line
- Fields:
  1. history_id (int)
  2. auction_id (int)
  3. auction_name (str)
  4. bidder_name (str)
  5. bid_amount (float)
  6. bid_timestamp (str, datetime format YYYY-MM-DD HH:MM)
- Purpose: Stores historical bids across all auctions for display and review.
- Example rows:
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45

### 6. Items Data
- Path: data/items.txt
- File format: pipe-delimited (|), no header line
- Fields:
  1. item_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. starting_price (float)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Purpose: Stores detailed item listings related to auctions for extended metadata.
- Example rows:
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop

### 7. Trending Data
- Path: data/trending.txt
- File format: pipe-delimited (|), no header line
- Fields:
  1. auction_id (int)
  2. item_name (str)
  3. bid_count (int)
  4. current_bid (float)
  5. trending_rank (int)
  6. time_period (str: Last 24 Hours, This Week, All Time)
- Purpose: Stores trending auction items ranked for popularity and activity within time periods.
- Example rows:
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week

---

This design specification document provides backend developers with route and data format details, and frontend developers with template and element ID details to implement the OnlineAuction application independently and in parallel.