# OnlineAuction Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                 | Function Name           | HTTP Method | Template to Render             | Context Variables Passed to Template                                   |
|----------------------------|------------------------|-------------|-------------------------------|------------------------------------------------------------------------|
| /                          | root_redirect           | GET         | Redirects to /dashboard        | None                                                                   |
| /dashboard                 | dashboard              | GET         | dashboard.html                | featured_auctions: list[dict{auction_id: int, item_name: str, current_bid: float, end_time: str, image_url: str}], trending_auctions: list[dict{auction_id: int, item_name: str, current_bid: float, bid_count: int, trending_rank: int}],  |
| /catalog                  | auction_catalog        | GET         | catalog.html                  | auctions: list[dict{auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str}], categories: list[str]  |
| /auction/<int:auction_id>  | auction_details        | GET         | auction_details.html          | auction: dict{auction_id: int, item_name: str, description: str, current_bid: float, end_time: str, status: str, image_url: str}, bid_history: list[dict{bidder_name: str, bid_amount: float, bid_timestamp: str}] |
| /place_bid/<int:auction_id>| place_bid             | GET         | place_bid.html                | auction: dict{auction_id: int, item_name: str, minimum_bid: float}     |
| /submit_bid/<int:auction_id>| submit_bid            | POST        | Redirect or re-render place_bid.html | None (process form submission)                                   |
| /bid_history               | bid_history            | GET         | bid_history.html              | bids: list[dict{bid_id: int, auction_name: str, bidder_name: str, bid_amount: float, bid_timestamp: str}], auctions: list[dict{auction_id: int, item_name: str}] |
| /categories                | auction_categories     | GET         | categories.html               | categories: list[dict{category_id: int, category_name: str, description: str, item_count: int}] |
| /category/<int:category_id>| category_items         | GET         | catalog.html (filtered view) | auctions: list[dict{auction_id: int, item_name: str, description: str, category: str, current_bid: float, end_time: str, image_url: str}] filtered by category |
| /winners                  | winners                | GET         | winners.html                  | winners: list[dict{winner_id: int, auction_id: int, item_name: str, winner_name: str, winning_bid: float}] |
| /trending                 | trending_auctions      | GET         | trending.html                 | trending_auctions: list[dict{auction_id: int, item_name: str, bid_count: int, current_bid: float, trending_rank: int, time_period: str}] |
| /auction_status           | auction_status         | GET         | auction_status.html           | auctions: list[dict{auction_id: int, item_name: str, status: str, end_time: str, current_bid: float}] |

---

## Section 2: HTML Templates Specification (Frontend)

### 1. Dashboard Page
- Template: templates/dashboard.html
- Page Title: Auction Dashboard
- Elements and IDs:
  - div#dashboard-page
  - div#featured-auctions
  - button#browse-auctions-button (navigates to auction_catalog)
  - button#view-bids-button (navigates to bid_history)
  - button#trending-auctions-button (navigates to trending_auctions)
- Navigation:
  - browse-auctions-button → url_for('auction_catalog')
  - view-bids-button → url_for('bid_history')
  - trending-auctions-button → url_for('trending_auctions')
- Context Variables:
  - featured_auctions: list of dicts {
      auction_id: int,
      item_name: str,
      current_bid: float,
      end_time: str,
      image_url: str
    }
  - trending_auctions: list of dicts {
      auction_id: int,
      item_name: str,
      current_bid: float,
      bid_count: int,
      trending_rank: int
    }

### 2. Auction Catalog Page
- Template: templates/catalog.html
- Page Title: Auction Catalog
- Elements and IDs:
  - div#catalog-page
  - input#search-input
  - select#category-filter (options: Electronics, Collectibles, Furniture, Art, Other)
  - div#auctions-grid
  - button#view-auction-button-{{ auction.auction_id }} (per auction card)
- Navigation:
  - view-auction-button-{{ auction.auction_id }} → url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - auctions: list of dicts {
      auction_id: int,
      item_name: str,
      description: str,
      category: str,
      current_bid: float,
      end_time: str,
      image_url: str
    }
  - categories: list[str]

### 3. Auction Details Page
- Template: templates/auction_details.html
- Page Title: Auction Details
- Elements and IDs:
  - div#auction-details-page
  - h1#auction-title
  - div#auction-description
  - div#current-bid
  - button#place-bid-button (links to place_bid page for this auction)
  - div#bid-history
- Navigation:
  - place-bid-button → url_for('place_bid', auction_id=auction.auction_id)
- Context Variables:
  - auction: dict {
      auction_id: int,
      item_name: str,
      description: str,
      current_bid: float,
      end_time: str,
      status: str,
      image_url: str
    }
  - bid_history: list of dicts {
      bidder_name: str,
      bid_amount: float,
      bid_timestamp: str
    }

### 4. Place Bid Page
- Template: templates/place_bid.html
- Page Title: Place Bid
- Elements and IDs:
  - div#place-bid-page
  - input#bidder-name
  - input#bid-amount
  - div#auction-name
  - div#minimum-bid
  - button#submit-bid-button
- Navigation:
  - submit-bid-button → form POST to /submit_bid/<auction_id>
- Context Variables:
  - auction: dict {
      auction_id: int,
      item_name: str,
      minimum_bid: float
    }

### 5. Bid History Page
- Template: templates/bid_history.html
- Page Title: Bid History
- Elements and IDs:
  - div#bid-history-page
  - table#bids-table
  - select#filter-by-auction (options populated with auctions)
  - button#sort-by-amount
  - button#back-to-dashboard
- Navigation:
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - bids: list of dicts {
      bid_id: int,
      auction_name: str,
      bidder_name: str,
      bid_amount: float,
      bid_timestamp: str
    }
  - auctions: list of dicts {
      auction_id: int,
      item_name: str
    }

### 6. Auction Categories Page
- Template: templates/categories.html
- Page Title: Auction Categories
- Elements and IDs:
  - div#categories-page
  - div#categories-list
  - div#category-card-{{ category.category_id }} (per category)
  - button#view-category-button-{{ category.category_id }} (per category)
  - button#back-to-dashboard
- Navigation:
  - back-to-dashboard → url_for('dashboard')
  - view-category-button-{{ category.category_id }} → url_for('category_items', category_id=category.category_id)
- Context Variables:
  - categories: list of dicts {
      category_id: int,
      category_name: str,
      description: str,
      item_count: int
    }

### 7. Winners Page
- Template: templates/winners.html
- Page Title: Winning Items
- Elements and IDs:
  - div#winners-page
  - div#winners-list
  - div#winner-card-{{ winner.auction_id }} (per winner card)
  - input#filter-by-winner
  - button#back-to-dashboard
- Navigation:
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - winners: list of dicts {
      winner_id: int,
      auction_id: int,
      item_name: str,
      winner_name: str,
      winning_bid: float
    }

### 8. Trending Auctions Page
- Template: templates/trending.html
- Page Title: Trending Auctions
- Elements and IDs:
  - div#trending-page
  - div#trending-list
  - select#time-range-filter (options: Last 24 Hours, This Week, All Time)
  - button#back-to-dashboard
  - button#view-auction-button-{{ auction.auction_id }} (per trending auction)
- Navigation:
  - back-to-dashboard → url_for('dashboard')
  - view-auction-button-{{ auction.auction_id }} → url_for('auction_details', auction_id=auction.auction_id)
- Context Variables:
  - trending_auctions: list of dicts {
      auction_id: int,
      item_name: str,
      bid_count: int,
      current_bid: float,
      trending_rank: int,
      time_period: str
    }

### 9. Auction Status Page
- Template: templates/auction_status.html
- Page Title: Auction Status
- Elements and IDs:
  - div#status-page
  - select#status-filter (options: All, Active, Closed, Upcoming)
  - table#status-table
  - button#refresh-status-button
  - button#back-to-dashboard
- Navigation:
  - back-to-dashboard → url_for('dashboard')
- Context Variables:
  - auctions: list of dicts {
      auction_id: int,
      item_name: str,
      status: str,
      end_time: str,
      current_bid: float
    }

---

## Section 3: Data File Schemas (Backend)

### 1. Auctions Data
- Path: data/auctions.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  1. auction_id (int)
  2. item_name (str)
  3. description (str)
  4. category (str)
  5. starting_bid (float)
  6. current_bid (float)
  7. end_time (str) - Format: YYYY-MM-DD HH:MM
  8. status (str) - Values: Active, Closed
  9. image_url (str)
- Purpose: Stores all auction items details with current status and bids.
- Example Rows:
  ```
  1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
  2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
  3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
  ```

### 2. Categories Data
- Path: data/categories.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  1. category_id (int)
  2. category_name (str)
  3. description (str)
  4. item_count (int)
- Purpose: Stores auction categories and brief descriptions.
- Example Rows:
  ```
  1|Electronics|Digital devices and gadgets|15
  2|Collectibles|Rare and valuable collector items|28
  3|Furniture|Household furniture and decor|12
  ```

### 3. Bids Data
- Path: data/bids.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  1. bid_id (int)
  2. auction_id (int)
  3. bidder_name (str)
  4. bid_amount (float)
  5. bid_timestamp (str) - Format: YYYY-MM-DD HH:MM
- Purpose: Records all bids made on auction items.
- Example Rows:
  ```
  1|1|Alice Johnson|45.50|2025-02-05 14:30
  2|2|Bob Williams|620.00|2025-02-05 15:45
  3|3|Charlie Brown|110.00|2025-02-04 10:15
  ```

### 4. Winners Data
- Path: data/winners.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  1. winner_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. winner_name (str)
  5. winning_bid (float)
  6. win_date (str) - Format: YYYY-MM-DD
- Purpose: Stores auction winners and winning bids.
- Example Rows:
  ```
  1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
  2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
  3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
  ```

### 5. Bid History Data
- Path: data/bid_history.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  1. history_id (int)
  2. auction_id (int)
  3. auction_name (str)
  4. bidder_name (str)
  5. bid_amount (float)
  6. bid_timestamp (str) - Format: YYYY-MM-DD HH:MM
- Purpose: Stores full bid history records.
- Example Rows:
  ```
  1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
  2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
  3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
  ```

### 6. Items Data
- Path: data/items.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  1. item_id (int)
  2. auction_id (int)
  3. item_name (str)
  4. starting_price (float)
  5. category (str)
  6. condition (str)
  7. seller_name (str)
- Purpose: Stores individual item details related to auctions.
- Example Rows:
  ```
  1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
  2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
  3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
  ```

### 7. Trending Data
- Path: data/trending.txt
- File Format: Pipe-delimited (|), no header line
- Fields (in order):
  1. auction_id (int)
  2. item_name (str)
  3. bid_count (int)
  4. current_bid (float)
  5. trending_rank (int)
  6. time_period (str)
- Purpose: Stores trending auction items ranked by bid activity within specific time periods.
- Example Rows:
  ```
  2|iPhone 14 Pro|12|620.00|1|This Week
  1|Vintage Leather Watch|8|45.50|2|This Week
  5|Vintage Camera|6|85.00|3|This Week
  ```

---

This design specification document enables Backend and Frontend teams to proceed with independent and parallel development of the OnlineAuction application based on the detailed Flask routes, HTML template requirements, and data file schemas provided above.