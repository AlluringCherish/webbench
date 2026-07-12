# OnlineAuction Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path               | Function Name           | HTTP Method | Template Rendered           | Context Variables                                                                                                   |
|--------------------------|-------------------------|-------------|-----------------------------|--------------------------------------------------------------------------------------------------------------------|
| /                        | index                   | GET         | Redirect to /dashboard       | None                                                                                                               |
| /dashboard               | dashboard               | GET         | dashboard.html              | featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, image_url: str},
                                                                 trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int},
                                                                 categories: list of dict {category_id: int, category_name: str, item_count: int}
| /catalog                 | auction_catalog         | GET         | catalog.html                | auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str},
                                                                 categories: list of dict {category_id: int, category_name: str}
| /auction/<int:auction_id>| auction_details         | GET         | auction_details.html        | auction: dict {auction_id: int, item_name: str, description: str, current_bid: float, end_time: str, status: str, image_url: str},
                                                                 bid_history: list of dict {bid_id: int, bidder_name: str, bid_amount: float, bid_timestamp: str}
| /place_bid/<int:auction_id>| place_bid             | GET         | place_bid.html              | auction: dict {auction_id: int, item_name: str, minimum_bid: float}
| /place_bid/<int:auction_id>| submit_bid            | POST        | place_bid.html (redirect or show errors) | auction: dict (same as GET), errors: dict (optional)
| /bid_history             | bid_history             | GET         | bid_history.html            | bids: list of dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str},
                                                                 auctions: list of dict {auction_id: int, item_name: str}
| /categories              | auction_categories      | GET         | categories.html             | categories: list of dict {category_id: int, category_name: str, description: str, item_count: int}
| /category/<int:category_id>| category_view          | GET         | category_items.html (not described in requirements, omit unless needed)
| /winners                 | winners                 | GET         | winners.html                | winners: list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float}
| /trending                | trending_auctions       | GET         | trending.html               | trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}
| /auction_status          | auction_status          | GET         | auction_status.html         | auctions: list of dict {auction_id: int, item_name: str, status: str, time_remaining: str, current_bid: float}


---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template: templates/dashboard.html
- Page Title: "Auction Dashboard"
- <title>: "Auction Dashboard"
- <h1>: "Auction Dashboard"
- Element IDs:
  - dashboard-page (Div)
  - featured-auctions (Div)
  - browse-auctions-button (Button)
  - view-bids-button (Button)
  - trending-auctions-button (Button)
- Navigation:
  - browse-auctions-button -> url_for('auction_catalog')
  - view-bids-button -> url_for('bid_history')
  - trending-auctions-button -> url_for('trending_auctions')
- Context Variables:
  - featured_auctions: list of dict {auction_id: int, item_name: str, current_bid: float, image_url: str}
  - trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int}
  - categories: list of dict {category_id: int, category_name: str, item_count: int}

### 2. Auction Catalog Page
- Template: templates/catalog.html
- Page Title: "Auction Catalog"
- <title>: "Auction Catalog"
- <h1>: "Auction Catalog"
- Element IDs:
  - catalog-page (Div)
  - search-input (Input)
  - category-filter (Dropdown)
  - auctions-grid (Div)
  - view-auction-button-{{auction.auction_id}} (Button, dynamic per auction)
- Navigation:
  - view-auction-button-{{auction.auction_id}} -> url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - auctions: list of dict {auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str}
  - categories: list of dict {category_id: int, category_name: str}

### 3. Auction Details Page
- Template: templates/auction_details.html
- Page Title: "Auction Details"
- <title>: "Auction Details"
- <h1>: auction.item_name
- Element IDs:
  - auction-details-page (Div)
  - auction-title (H1)
  - auction-description (Div)
  - current-bid (Div)
  - place-bid-button (Button)
  - bid-history (Div)
- Navigation:
  - place-bid-button -> url_for('place_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict {auction_id: int, item_name: str, description: str, current_bid: float, end_time: str, status: str, image_url: str}
  - bid_history: list of dict {bid_id: int, bidder_name: str, bid_amount: float, bid_timestamp: str}

### 4. Place Bid Page
- Template: templates/place_bid.html
- Page Title: "Place Bid"
- <title>: "Place Bid"
- <h1>: "Place Bid"
- Element IDs:
  - place-bid-page (Div)
  - bidder-name (Input)
  - bid-amount (Input)
  - auction-name (Div)
  - minimum-bid (Div)
  - submit-bid-button (Button)
- Navigation:
  - submit-bid-button -> POST to url_for('submit_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict {auction_id: int, item_name: str, minimum_bid: float}
  - errors: dict (optional) with validation error messages

### 5. Bid History Page
- Template: templates/bid_history.html
- Page Title: "Bid History"
- <title>: "Bid History"
- <h1>: "Bid History"
- Element IDs:
  - bid-history-page (Div)
  - bids-table (Table)
  - filter-by-auction (Dropdown)
  - sort-by-amount (Button)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - bids: list of dict {bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}
  - auctions: list of dict {auction_id: int, item_name: str}

### 6. Auction Categories Page
- Template: templates/categories.html
- Page Title: "Auction Categories"
- <title>: "Auction Categories"
- <h1>: "Auction Categories"
- Element IDs:
  - categories-page (Div)
  - categories-list (Div)
  - category-card-{{category.category_id}} (Div, dynamic per category)
  - view-category-button-{{category.category_id}} (Button, dynamic per category)
  - back-to-dashboard (Button)
- Navigation:
  - view-category-button-{{category.category_id}} -> (not specified, likely catalog filtered by category)
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - categories: list of dict {category_id: int, category_name: str, description: str, item_count: int}

### 7. Winners Page
- Template: templates/winners.html
- Page Title: "Winning Items"
- <title>: "Winning Items"
- <h1>: "Winning Items"
- Element IDs:
  - winners-page (Div)
  - winners-list (Div)
  - winner-card-{{winner.auction_id}} (Div, dynamic per winner)
  - filter-by-winner (Input)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - winners: list of dict {winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float}

### 8. Trending Auctions Page
- Template: templates/trending.html
- Page Title: "Trending Auctions"
- <title>: "Trending Auctions"
- <h1>: "Trending Auctions"
- Element IDs:
  - trending-page (Div)
  - trending-list (Div)
  - time-range-filter (Dropdown)
  - view-auction-button-{{auction.auction_id}} (Button, dynamic per trending auction)
  - back-to-dashboard (Button)
- Navigation:
  - view-auction-button-{{auction.auction_id}} -> url_for('auction_details', auction_id=auction.auction_id)
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - trending_auctions: list of dict {auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}

### 9. Auction Status Page
- Template: templates/auction_status.html
- Page Title: "Auction Status"
- <title>: "Auction Status"
- <h1>: "Auction Status"
- Element IDs:
  - status-page (Div)
  - status-filter (Dropdown)
  - status-table (Table)
  - refresh-status-button (Button)
  - back-to-dashboard (Button)
- Navigation:
  - back-to-dashboard -> url_for('dashboard')
- Context Variables:
  - auctions: list of dict {auction_id: int, item_name: str, status: str, time_remaining: str, current_bid: float}


---

## Section 3: Data File Schemas (Backend)

All files are pipe-delimited (|) with no header line. Directory is `data/`.

### 1. Auctions Data
- Path: data/auctions.txt
- Format: auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url
- Description: Stores auction items data including status and bidding info.
- Example Rows:
```
1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
```

### 2. Categories Data
- Path: data/categories.txt
- Format: category_id|category_name|description|item_count
- Description: Contains auction categories with descriptions and item counts.
- Example Rows:
```
1|Electronics|Digital devices and gadgets|15
2|Collectibles|Rare and valuable collector items|28
3|Furniture|Household furniture and decor|12
```

### 3. Bids Data
- Path: data/bids.txt
- Format: bid_id|auction_id|bidder_name|bid_amount|bid_timestamp
- Description: Records individual bid entries linked to auctions.
- Example Rows:
```
1|1|Alice Johnson|45.50|2025-02-05 14:30
2|2|Bob Williams|620.00|2025-02-05 15:45
3|3|Charlie Brown|110.00|2025-02-04 10:15
```

### 4. Winners Data
- Path: data/winners.txt
- Format: winner_id|auction_id|item_name|winner_name|winning_bid|win_date
- Description: Tracks auction winners and their winning bids.
- Example Rows:
```
1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
```

### 5. Bid History Data
- Path: data/bid_history.txt
- Format: history_id|auction_id|auction_name|bidder_name|bid_amount|bid_timestamp
- Description: Detailed history of all bids placed by users.
- Example Rows:
```
1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
```

### 6. Items Data
- Path: data/items.txt
- Format: item_id|auction_id|item_name|starting_price|category|condition|seller_name
- Description: Stores item details associated with auctions.
- Example Rows:
```
1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
```

### 7. Trending Data
- Path: data/trending.txt
- Format: auction_id|item_name|bid_count|current_bid|trending_rank|time_period
- Description: Contains trending auction items with ranking and bid activity data.
- Example Rows:
```
2|iPhone 14 Pro|12|620.00|1|This Week
1|Vintage Leather Watch|8|45.50|2|This Week
5|Vintage Camera|6|85.00|3|This Week
```

---

This specification document allows backend developers to implement all required Flask routes and handle data files accurately, and frontend developers to create all HTML templates with exact element IDs and navigation to build the complete OnlineAuction web application independently and in parallel.