# OnlineAuction Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                          | Function Name         | HTTP Method(s) | Template to Render       | Context Variables (Type Annotations)                                                                                                  |
|-----------------------------------|-----------------------|----------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| /                                 | index                 | GET            | N/A (redirect to dashboard) | None                                                                                                                           |
| /dashboard                        | dashboard             | GET            | templates/dashboard.html | featured_auctions: List[Dict[str, Any]] (auction_id: int, item_name: str, current_bid: float, end_time: str, image_url: str)             |
| /auction/catalog                  | auction_catalog       | GET            | templates/catalog.html   | auctions: List[Dict[str, Any]] (auction_id: int, item_name: str, current_bid: float, end_time: str, image_url: str), 
                                                                               categories: List[Dict[str, Any]] (category_id: int, category_name: str)                                                            |
| /auction/<int:auction_id>         | auction_details       | GET            | templates/auction_details.html | auction: Dict[str, Any] (auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, status: str, image_url: str),
                                                                       bid_history: List[Dict[str, Any]] (bid_id: int, bidder_name: str, bid_amount: float, bid_timestamp: str),
                                                                       highest_bid: float                                                      |
| /auction/<int:auction_id>/place_bid | place_bid          | GET, POST      | templates/place_bid.html  | auction: Dict[str, Any] (auction_id: int, item_name: str, current_bid: float), minimum_bid: float
 POST form data: bidder_name: str, bid_amount: float                                                             |
| /bid/history                     | bid_history           | GET            | templates/bid_history.html | bids: List[Dict[str, Any]] (bid_id: int, auction_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str), 
                                               selected_auction_id: int or None                                                                                          |
| /categories                     | categories            | GET            | templates/categories.html| categories: List[Dict[str, Any]] (category_id: int, category_name: str, description: str, item_count: int)                             |
| /winners                       | winners               | GET            | templates/winners.html   | winners: List[Dict[str, Any]] (winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float, win_date: str),
                                   filter_name: str (optional)                                                                                   |
| /trending                      | trending_auctions     | GET            | templates/trending.html  | trending_auctions: List[Dict[str, Any]] (auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str),
                                               time_range: str                                                                                      |
| /status                        | status                | GET            | templates/status.html    | auctions: List[Dict[str, Any]] (auction_id: int, item_name: str, status: str, end_time: str, current_bid: float),
                                               status_filter: str (optional)                                                                    |

---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template file: templates/dashboard.html
- Page Title: Auction Dashboard
- IDs and Elements:
  - div id="dashboard-page"
  - div id="featured-auctions"
  - button id="browse-auctions-button" (navigates to auction_catalog function)
  - button id="view-bids-button" (navigates to bid_history function)
  - button id="trending-auctions-button" (navigates to trending_auctions function)
- Context variables:
  - featured_auctions: List[Dict[str, Any]] (auction_id: int, item_name: str, current_bid: float, end_time: str, image_url: str)

### 2. Auction Catalog Page
- Template file: templates/catalog.html
- Page Title: Auction Catalog
- IDs and Elements:
  - div id="catalog-page"
  - input id="search-input" (text input for search)
  - select id="category-filter" (dropdown for category filter)
  - div id="auctions-grid" (grid displaying auctions)
  - buttons with dynamic ids e.g. id="view-auction-button-{{ auction.auction_id }}" (navigate to auction_details)
- Context variables:
  - auctions: List[Dict[str, Any]]
  - categories: List[Dict[str, Any]]

### 3. Auction Details Page
- Template file: templates/auction_details.html
- Page Title: Auction Details
- IDs and Elements:
  - div id="auction-details-page"
  - h1 id="auction-title"
  - div id="auction-description"
  - div id="current-bid"
  - button id="place-bid-button" (links to place_bid page)
  - div id="bid-history"
- Context variables:
  - auction: Dict[str, Any]
  - bid_history: List[Dict[str, Any]]
  - highest_bid: float

### 4. Place Bid Page
- Template file: templates/place_bid.html
- Page Title: Place Bid
- IDs and Elements:
  - div id="place-bid-page"
  - input id="bidder-name" (text)
  - input id="bid-amount" (number)
  - div id="auction-name"
  - div id="minimum-bid"
  - button id="submit-bid-button"
- Context variables:
  - auction: Dict[str, Any]
  - minimum_bid: float

### 5. Bid History Page
- Template file: templates/bid_history.html
- Page Title: Bid History
- IDs and Elements:
  - div id="bid-history-page"
  - table id="bids-table" (columns: bid ID, auction name, bidder, amount, timestamp)
  - select id="filter-by-auction"
  - button id="sort-by-amount"
  - button id="back-to-dashboard"
- Context variables:
  - bids: List[Dict[str, Any]]
  - selected_auction_id: Optional[int]

### 6. Auction Categories Page
- Template file: templates/categories.html
- Page Title: Auction Categories
- IDs and Elements:
  - div id="categories-page"
  - div id="categories-list"
  - div id="category-card-{{ category.category_id }}" (for each category)
  - button id="view-category-button-{{ category.category_id }}"
  - button id="back-to-dashboard"
- Context variables:
  - categories: List[Dict[str, Any]]

### 7. Winners Page
- Template file: templates/winners.html
- Page Title: Winning Items
- IDs and Elements:
  - div id="winners-page"
  - div id="winners-list"
  - div id="winner-card-{{ winner.auction_id }}" (for each winner)
  - input id="filter-by-winner"
  - button id="back-to-dashboard"
- Context variables:
  - winners: List[Dict[str, Any]]
  - filter_name: Optional[str]

### 8. Trending Auctions Page
- Template file: templates/trending.html
- Page Title: Trending Auctions
- IDs and Elements:
  - div id="trending-page"
  - div id="trending-list"
  - select id="time-range-filter"
  - buttons with ids "view-auction-button-{{ auction.auction_id }}"
  - button id="back-to-dashboard"
- Context variables:
  - trending_auctions: List[Dict[str, Any]]
  - time_range: str

### 9. Auction Status Page
- Template file: templates/status.html
- Page Title: Auction Status
- IDs and Elements:
  - div id="status-page"
  - select id="status-filter"
  - table id="status-table" (columns: auction name, status, time remaining, current bid)
  - button id="refresh-status-button"
  - button id="back-to-dashboard"
- Context variables:
  - auctions: List[Dict[str, Any]]
  - status_filter: Optional[str]

---

## Section 3: Data File Schemas (Backend)

All files are stored in `data/` directory and pipe-delimited (|) with no header line.

### auctions.txt
- **Fields:** auction_id (int) | item_name (str) | description (str) | category (str) | starting_bid (float) | current_bid (float) | end_time (str, datetime format YYYY-MM-DD HH:MM) | status (str) | image_url (str)
- **Description:** Stores details of auction items.
- **Example rows:**
```
1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
```

### categories.txt
- **Fields:** category_id (int) | category_name (str) | description (str) | item_count (int)
- **Description:** Stores auction categories and counts.
- **Example rows:**
```
1|Electronics|Digital devices and gadgets|15
2|Collectibles|Rare and valuable collector items|28
3|Furniture|Household furniture and decor|12
```

### bids.txt
- **Fields:** bid_id (int) | auction_id (int) | bidder_name (str) | bid_amount (float) | bid_timestamp (str, datetime format YYYY-MM-DD HH:MM)
- **Description:** Stores bids placed on auctions.
- **Example rows:**
```
1|1|Alice Johnson|45.50|2025-02-05 14:30
2|2|Bob Williams|620.00|2025-02-05 15:45
3|3|Charlie Brown|110.00|2025-02-04 10:15
```

### winners.txt
- **Fields:** winner_id (int) | auction_id (int) | item_name (str) | winner_name (str) | winning_bid (float) | win_date (str, datetime format YYYY-MM-DD)
- **Description:** Stores winners of auctions.
- **Example rows:**
```
1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
```

### bid_history.txt
- **Fields:** history_id (int) | auction_id (int) | auction_name (str) | bidder_name (str) | bid_amount (float) | bid_timestamp (str, datetime format YYYY-MM-DD HH:MM)
- **Description:** Historical record of bids.
- **Example rows:**
```
1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
```

### items.txt
- **Fields:** item_id (int) | auction_id (int) | item_name (str) | starting_price (float) | category (str) | condition (str) | seller_name (str)
- **Description:** Stores details about auction items including condition and seller information.
- **Example rows:**
```
1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
```

### trending.txt
- **Fields:** auction_id (int) | item_name (str) | bid_count (int) | current_bid (float) | trending_rank (int) | time_period (str)
- **Description:** Stores auction trending data.
- **Example rows:**
```
2|iPhone 14 Pro|12|620.00|1|This Week
1|Vintage Leather Watch|8|45.50|2|This Week
5|Vintage Camera|6|85.00|3|This Week
```

---

End of specification.
