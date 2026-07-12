# OnlineAuction Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                     | Function Name         | HTTP Method(s) | Template Name         | Context Variables (with types)                                  |
|-------------------------------|-----------------------|----------------|-----------------------|----------------------------------------------------------------|
| `/`                           | `home`                | GET            | N/A (Redirect)         | N/A                                                            |
| `/dashboard`                  | `dashboard`           | GET            | `dashboard.html`      | `featured_auctions` (List[Dict]), `trending_auctions` (List[Dict])|
| `/auctions`                  | `auctions_list`       | GET            | `auctions.html`       | `auctions` (List[Dict]), `categories` (List[Dict])             |
| `/auction/<int:auction_id>`   | `auction_details`     | GET            | `auction_details.html` | `auction` (Dict), `bids` (List[Dict])                          |
| `/bid/place/<int:auction_id>` | `place_bid`           | GET, POST      | `place_bid.html`      | GET: `auction` (Dict); POST: bid submission data                |
| `/bid/history`               | `bid_history`         | GET            | `bid_history.html`    | `bids` (List[Dict])                                            |
| `/winners`                   | `winners`             | GET            | `winners.html`        | `winners` (List[Dict])                                        |
| `/categories`                | `categories_list`     | GET            | `categories.html`     | `categories` (List[Dict])                                      |
| `/trending`                  | `trending_auctions`   | GET            | `trending.html`       | `trending_auctions` (List[Dict])                              |
| `/status`                    | `auction_status`      | GET            | `status.html`         | `auctions` (List[Dict])                                       |

---

## Section 2: HTML Templates Specification (Frontend)

### Dashboard Page
- Template: `templates/dashboard.html`
- Page Title: "Auction Dashboard"
- `<h1>` text: "Auction Dashboard"
- Element IDs:
  - `dashboard-page` (div) - Container for dashboard
  - `featured-auctions` (div) - Display of featured auction items
  - `browse-auctions-button` (button) - Navigates to `auctions_list`
  - `view-bids-button` (button) - Navigates to `bid_history`
  - `trending-auctions-button` (button) - Navigates to `trending_auctions`
- Available Context Variables:
  - `featured_auctions`: List of featured auction dicts
  - `trending_auctions`: List of trending auction dicts

### Auction Catalog Page
- Template: `templates/auctions.html`
- Page Title: "Auction Catalog"
- `<h1>` text: "Auction Catalog"
- Element IDs:
  - `catalog-page` (div) - Container for catalog
  - `search-input` (input) - Field for search by item name, description, or ID
  - `category-filter` (dropdown) - Dropdown filtering by category
  - `auctions-grid` (div) - Grid showing auction cards
  - `view-auction-button-{{ auction.auction_id }}` (button) - View button per auction
- Context Variables:
  - `auctions`: List of auction dicts
  - `categories`: List of category dicts

### Auction Details Page
- Template: `templates/auction_details.html`
- Page Title: "Auction Details"
- `<h1>` text: "Auction Details"
- Elements:
  - `auction-details-page` (div)
  - `auction-title` (h1) - Auction item title
  - `auction-description` (div) - Item description
  - `current-bid` (div) - Current highest bid amount
  - `place-bid-button` (button) - Navigates to bid placement
  - `bid-history` (div) - Displays bid history with bidders and amounts
- Context Variables:
  - `auction`: Dict of auction item details
  - `bids`: List of bid dicts for the auction

### Place Bid Page
- Template: `templates/place_bid.html`
- Page Title: "Place Bid"
- `<h1>` text: "Place Bid"
- Elements:
  - `place-bid-page` (div)
  - `bidder-name` (input) - User inputs bidder name
  - `bid-amount` (input) - User inputs bid amount (float)
  - `auction-name` (div) - Display auction name
  - `minimum-bid` (div) - Display minimum acceptable bid
  - `submit-bid-button` (button) - Submit bid
- Context Variables:
  - `auction`: Auction details dict

### Bid History Page
- Template: `templates/bid_history.html`
- Page Title: "Bid History"
- `<h1>` text: "Bid History"
- Elements:
  - `bid-history-page` (div)
  - `bids-table` (table) - Columns: bid ID, auction name, bidder, amount, timestamp
  - `filter-by-auction` (dropdown) - Filter bids by auction
  - `sort-by-amount` (button) - Sort bids by bid amount
  - `back-to-dashboard` (button) - Navigates to dashboard
- Context Variables:
  - `bids`: List of bid records

### Auction Categories Page
- Template: `templates/categories.html`
- Page Title: "Auction Categories"
- `<h1>` text: "Auction Categories"
- Elements:
  - `categories-page` (div)
  - `categories-list` (div) - Contains category cards
  - `category-card-{{ category.category_id }}` (div) - Single category card
  - `view-category-button-{{ category.category_id }}` (button) - View auctions in category
  - `back-to-dashboard` (button) - Navigates to dashboard
- Context Variables:
  - `categories`: List of category dicts

### Winners Page
- Template: `templates/winners.html`
- Page Title: "Winning Items"
- `<h1>` text: "Winning Items"
- Elements:
  - `winners-page` (div)
  - `winners-list` (div) - Contains winning item cards
  - `winner-card-{{ winner.auction_id }}` (div) - Single winner card
  - `filter-by-winner` (input) - Filter winners by name
  - `back-to-dashboard` (button) - Navigates to dashboard
- Context Variables:
  - `winners`: List of winner dicts

### Trending Auctions Page
- Template: `templates/trending.html`
- Page Title: "Trending Auctions"
- `<h1>` text: "Trending Auctions"
- Elements:
  - `trending-page` (div)
  - `trending-list` (div) - Ranked list of trending auctions
  - `time-range-filter` (dropdown) - Filter trending by time range
  - `view-auction-button-{{ auction.auction_id }}` (button) - View auction detail
  - `back-to-dashboard` (button) - Navigates to dashboard
- Context Variables:
  - `trending_auctions`: List of trending auctions

### Auction Status Page
- Template: `templates/status.html`
- Page Title: "Auction Status"
- `<h1>` text: "Auction Status"
- Elements:
  - `status-page` (div)
  - `status-filter` (dropdown) - Filter auctions by status
  - `status-table` (table) - Auction name, status, time remaining, current bid
  - `refresh-status-button` (button) - Refresh auction status
  - `back-to-dashboard` (button) - Navigates to dashboard
- Context Variables:
  - `auctions`: List of auction dicts with status

---

## Section 3: Data File Schemas (Backend)

All data files are pipe (`|`) delimited with no header.

### 1. `auctions.txt`
- Path: `data/auctions.txt`
- Format: 
  `auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url`
- Fields and types:
  - `auction_id` (int): Unique auction ID
  - `item_name` (str): Auction item name
  - `description` (str): Auction item description
  - `category` (str): Category name
  - `starting_bid` (float): Starting bid amount
  - `current_bid` (float): Current highest bid
  - `end_time` (str in `YYYY-MM-DD HH:MM` format): Auction end timestamp
  - `status` (str): Auction status - Active, Closed, Upcoming
  - `image_url` (str): Item image filename or URL
- Sample Rows:
```
1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
```

### 2. `categories.txt`
- Path: `data/categories.txt`
- Format:
  `category_id|category_name|description|item_count`
- Fields and types:
  - `category_id` (int): Category identifier
  - `category_name` (str): Name of category
  - `description` (str): Category description
  - `item_count` (int): Number of items in the category
- Sample Rows:
```
1|Electronics|Digital devices and gadgets|15
2|Collectibles|Rare and valuable collector items|28
3|Furniture|Household furniture and decor|12
```

### 3. `bids.txt`
- Path: `data/bids.txt`
- Format:
  `bid_id|auction_id|bidder_name|bid_amount|bid_timestamp`
- Fields and types:
  - `bid_id` (int): Unique bid ID
  - `auction_id` (int): Auction reference
  - `bidder_name` (str): Name of bidder
  - `bid_amount` (float): Bid amount
  - `bid_timestamp` (str in `YYYY-MM-DD HH:MM` format): Bid time
- Sample Rows:
```
1|1|Alice Johnson|45.50|2025-02-05 14:30
2|2|Bob Williams|620.00|2025-02-05 15:45
3|3|Charlie Brown|110.00|2025-02-04 10:15
```

### 4. `winners.txt`
- Path: `data/winners.txt`
- Format:
  `winner_id|auction_id|item_name|winner_name|winning_bid|win_date`
- Fields and types:
  - `winner_id` (int): Winner record ID
  - `auction_id` (int): Auction reference
  - `item_name` (str): Item name
  - `winner_name` (str): Name of winner
  - `winning_bid` (float): Winning bid value
  - `win_date` (str date `YYYY-MM-DD`): Date won
- Sample Rows:
```
1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
```

### 5. `bid_history.txt`
- Path: `data/bid_history.txt`
- Format:
  `history_id|auction_id|auction_name|bidder_name|bid_amount|bid_timestamp`
- Fields and types:
  - `history_id` (int): Bid history record ID
  - `auction_id` (int): Auction reference
  - `auction_name` (str): Item name
  - `bidder_name` (str): Name of bidder
  - `bid_amount` (float): Bid amount
  - `bid_timestamp` (str datetime `YYYY-MM-DD HH:MM`): Timestamp
- Sample Rows:
```
1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
```

### 6. `items.txt`
- Path: `data/items.txt`
- Format:
  `item_id|auction_id|item_name|starting_price|category|condition|seller_name`
- Fields and types:
  - `item_id` (int): Unique item ID
  - `auction_id` (int): Auction reference
  - `item_name` (str): Item name
  - `starting_price` (float): Starting price
  - `category` (str): Category
  - `condition` (str): Item condition
  - `seller_name` (str): Seller name
- Sample Rows:
```
1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
```

### 7. `trending.txt`
- Path: `data/trending.txt`
- Format:
  `auction_id|item_name|bid_count|current_bid|trending_rank|time_period`
- Fields and types:
  - `auction_id` (int): Auction reference
  - `item_name` (str): Item name
  - `bid_count` (int): Number of bids in time period
  - `current_bid` (float): Current highest bid
  - `trending_rank` (int): Rank of trending popularity
  - `time_period` (str): Time range descriptor
- Sample Rows:
```
2|iPhone 14 Pro|12|620.00|1|This Week
1|Vintage Leather Watch|8|45.50|2|This Week
5|Vintage Camera|6|85.00|3|This Week
```

---

This design specification provides a complete and precise blueprint for backend Flask routes, frontend Jinja2 templates, and local data file schemas for the OnlineAuction application.
