# OnlineAuction Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                     | Function Name           | HTTP Method | Template File       | Context Variables                                                                                                  |
|-------------------------------|------------------------|-------------|---------------------|-------------------------------------------------------------------------------------------------------------------|
| /                             | root_redirect           | GET         | None (redirect)     | None                                                                                                              |
| /dashboard                    | dashboard               | GET         | dashboard.html      | featured_auctions: list[dict{auction_id: int, item_name: str, current_bid: float, end_time: str}], trending_auctions: list[dict{auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}] |
| /catalog                     | auction_catalog         | GET         | catalog.html        | auctions: list[dict{auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str}], categories: list[str] (e.g. Electronics, Collectibles, Furniture, Art, Other) |
| /auction/<int:auction_id>    | auction_details         | GET         | auction_details.html| auction: dict{auction_id: int, item_name: str, description: str, category: str, starting_bid: float, current_bid: float, end_time: str, status: str, image_url: str}, bids: list[dict{bidder_name: str, bid_amount: float, bid_timestamp: str}] |
| /place-bid/<int:auction_id>  | place_bid_page          | GET         | place_bid.html      | auction_name: str, minimum_bid: float                                                                             |
| /place-bid/<int:auction_id>  | submit_bid              | POST        | None                | None (handles bid submission and redirects)                                                                       |
| /bid-history                 | bid_history             | GET         | bid_history.html    | bids: list[dict{bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}], auctions: list[dict{auction_id: int, item_name: str}] (for filter dropdown) |
| /categories                  | categories              | GET         | categories.html     | categories: list[dict{category_id: int, category_name: str, description: str, item_count: int}]                   |
| /winners                    | winners                 | GET         | winners.html        | winners: list[dict{winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str}] |
| /trending                   | trending_auctions       | GET         | trending.html       | trending_list: list[dict{auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}] |
| /status                     | auction_status          | GET         | status.html         | auctions_status: list[dict{name: str, status: str, time_remaining: str, current_bid: float}]                      |

---

## Section 2: HTML Templates Specification (Frontend)

### Template: templates/dashboard.html
- Page Title (<title> and <h1>): Auction Dashboard
- Elements:
  - Div, id="dashboard-page" (container for dashboard page)
  - Div, id="featured-auctions" (displays featured auction items)
  - Button, id="browse-auctions-button", navigates to function: auction_catalog via url_for
  - Button, id="view-bids-button", navigates to function: bid_history via url_for
  - Button, id="trending-auctions-button", navigates to function: trending_auctions via url_for
- Context Variables available:
  - featured_auctions: list of dicts (auction_id: int, item_name: str, current_bid: float, end_time: str)
  - trending_auctions: list of dicts (auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str)

---

### Template: templates/catalog.html
- Page Title: Auction Catalog
- Elements:
  - Div, id="catalog-page" (container for catalog)
  - Input, id="search-input" (search auctions by item name, description, or item ID)
  - Dropdown, id="category-filter" (filter by category: Electronics, Collectibles, Furniture, Art, Other)
  - Div, id="auctions-grid" (grid displaying auction cards)
  - Button for each auction, id="view-auction-button-{{ auction.auction_id }}" (to view auction details), navigates to auction_details
- Context Variables:
  - auctions: list of dicts (auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str)
  - categories: list of str (Electronics, Collectibles, Furniture, Art, Other)

---

### Template: templates/auction_details.html
- Page Title: Auction Details
- Elements:
  - Div, id="auction-details-page" (container)
  - H1, id="auction-title" (auction item title)
  - Div, id="auction-description" (item description)
  - Div, id="current-bid" (current highest bid amount)
  - Button, id="place-bid-button", navigates to place_bid_page
  - Div, id="bid-history" (bid history section, list bidder names and amounts)
- Context Variables:
  - auction: dict (with keys auction_id: int, item_name: str, description: str, category: str, starting_bid: float, current_bid: float, end_time: str, status: str, image_url: str)
  - bids: list of dicts (bidder_name: str, bid_amount: float, bid_timestamp: str)

---

### Template: templates/place_bid.html
- Page Title: Place Bid
- Elements:
  - Div, id="place-bid-page" (container)
  - Input, id="bidder-name" (bidder name)
  - Input, id="bid-amount" (bid amount)
  - Div, id="auction-name" (auction item name)
  - Div, id="minimum-bid" (minimum acceptable bid amount)
  - Button, id="submit-bid-button"
- Context Variables:
  - auction_name: str
  - minimum_bid: float

---

### Template: templates/bid_history.html
- Page Title: Bid History
- Elements:
  - Div, id="bid-history-page" (container)
  - Table, id="bids-table" with columns bid_id, auction_name, bidder_name, bid_amount, bid_timestamp
  - Dropdown, id="filter-by-auction"
  - Button, id="sort-by-amount"
  - Button, id="back-to-dashboard" navigates to dashboard
- Context Variables:
  - bids: list of dicts (bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str)
  - auctions: list of dicts (auction_id: int, item_name: str) for filter dropdown

---

### Template: templates/categories.html
- Page Title: Auction Categories
- Elements:
  - Div, id="categories-page" (container)
  - Div, id="categories-list" (list categories with description and count)
  - Div, id="category-card-{{ category.category_id }}" for each category with name and count
  - Button, id="view-category-button-{{ category.category_id }}" navigates to auction_catalog filtered by category
  - Button, id="back-to-dashboard" navigates to dashboard
- Context Variables:
  - categories: list of dicts (category_id: int, category_name: str, description: str, item_count: int)

---

### Template: templates/winners.html
- Page Title: Winning Items
- Elements:
  - Div, id="winners-page" (container)
  - Input, id="filter-by-winner"
  - Div, id="winners-list" (list of winning items)
  - Div, id="winner-card-{{ winner.auction_id }}" for each winner card
  - Button, id="back-to-dashboard" navigates to dashboard
- Context Variables:
  - winners: list of dicts (winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str)

---

### Template: templates/trending.html
- Page Title: Trending Auctions
- Elements:
  - Div, id="trending-page" (container)
  - Div, id="trending-list" (ranked trending auctions list)
  - Dropdown, id="time-range-filter" (options: Last 24 Hours, This Week, All Time)
  - Button, id="view-auction-button-{{ trending.auction_id }}" navigates to auction_details
  - Button, id="back-to-dashboard" navigates to dashboard
- Context Variables:
  - trending_list: list of dicts (auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str)

---

### Template: templates/status.html
- Page Title: Auction Status
- Elements:
  - Div, id="status-page" (container)
  - Dropdown, id="status-filter" (options-All, Active, Closed, Upcoming)
  - Table, id="status-table" with columns name, status, time_remaining, current_bid
  - Button, id="refresh-status-button"
  - Button, id="back-to-dashboard" navigates to dashboard
- Context Variables:
  - auctions_status: list of dicts (name: str, status: str, time_remaining: str, current_bid: float)

---

## Section 3: Data File Schemas (Backend)

### File: data/auctions.txt
- Format: pipe-delimited (|), no header line
- Fields (in order): auction_id (int), item_name (str), description (str), category (str), starting_bid (float), current_bid (float), end_time (str), status (str), image_url (str)
- Description: Stores all auction items with details including current bids, status, end time, and image reference.
- Example rows:
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg

---

### File: data/categories.txt
- Format: pipe-delimited (|), no header line
- Fields: category_id (int), category_name (str), description (str), item_count (int)
- Description: Stores auction categories data with descriptions and item counts.
- Example rows:
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12

---

### File: data/bids.txt
- Format: pipe-delimited (|), no header line
- Fields: bid_id (int), auction_id (int), bidder_name (str), bid_amount (float), bid_timestamp (str)
- Description: Contains all bids placed by users with timestamp.
- Example rows:
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15

---

### File: data/winners.txt
- Format: pipe-delimited (|), no header line
- Fields: winner_id (int), auction_id (int), item_name (str), winner_name (str), winning_bid (float), win_date (str)
- Description: Stores winning auction items and winner details.
- Example rows:
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01

---

### File: data/bid_history.txt
- Format: pipe-delimited (|), no header line
- Fields: history_id (int), auction_id (int), auction_name (str), bidder_name (str), bid_amount (float), bid_timestamp (str)
- Description: Detailed record of all bids placed on auctions over time.
- Example rows:
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45

---

### File: data/items.txt
- Format: pipe-delimited (|), no header line
- Fields: item_id (int), auction_id (int), item_name (str), starting_price (float), category (str), condition (str), seller_name (str)
- Description: Contains detailed item information linked to auctions.
- Example rows:
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop

---

### File: data/trending.txt
- Format: pipe-delimited (|), no header line
- Fields: auction_id (int), item_name (str), bid_count (int), current_bid (float), trending_rank (int), time_period (str)
- Description: Stores trending auction data with rank and bid activity.
- Example rows:
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week

---

