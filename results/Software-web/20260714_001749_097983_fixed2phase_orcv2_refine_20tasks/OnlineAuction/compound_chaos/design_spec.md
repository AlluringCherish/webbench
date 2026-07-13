# OnlineAuction Application Design Specification

---

## 1. Overview

The OnlineAuction web application allows users to browse auction items, place bids, view bid history, see winning items, and explore categories. The app is built with Python using Flask for the web framework and data is persisted locally in structured text files. The app starts from the Dashboard page.

---

## 2. Pages and Elements

### 2.1 Dashboard Page
- **Page Title:** Auction Dashboard
- **Container ID:** dashboard-page (Div)
- **Elements:**
  - featured-auctions (Div): Displays featured auction items.
  - browse-auctions-button (Button): Navigates to Auction Catalog Page.
  - view-bids-button (Button): Navigates to Bid History Page.
  - trending-auctions-button (Button): Navigates to Trending Auctions Page.

### 2.2 Auction Catalog Page
- **Page Title:** Auction Catalog
- **Container ID:** catalog-page (Div)
- **Elements:**
  - search-input (Input): Search field for auctions by item name, description, or item ID.
  - category-filter (Dropdown): Filter auctions by category (Electronics, Collectibles, Furniture, Art, Other).
  - auctions-grid (Div): Grid displaying auction cards.
  - view-auction-button-{auction_id} (Button): For each auction card, navigates to that auction's Auction Details Page.

### 2.3 Auction Details Page
- **Page Title:** Auction Details
- **Container ID:** auction-details-page (Div)
- **Elements:**
  - auction-title (H1): Display auction item title.
  - auction-description (Div): Display item description.
  - current-bid (Div): Display current highest bid amount.
  - place-bid-button (Button): Navigate to Place Bid Page for this auction.
  - bid-history (Div): Section showing bid history (bidder names and bid amounts) for the item.

### 2.4 Place Bid Page
- **Page Title:** Place Bid
- **Container ID:** place-bid-page (Div)
- **Elements:**
  - bidder-name (Input): Input field for bidder's name.
  - bid-amount (Input): Input field for bid amount.
  - auction-name (Div): Displays the name of the auction item.
  - minimum-bid (Div): Displays the minimum acceptable bid amount.
  - submit-bid-button (Button): Submits the bid.

### 2.5 Bid History Page
- **Page Title:** Bid History
- **Container ID:** bid-history-page (Div)
- **Elements:**
  - bids-table (Table): Displays bids with columns: Bid ID, Auction Name, Bidder, Amount, Timestamp.
  - filter-by-auction (Dropdown): Filter bids by auction.
  - sort-by-amount (Button): Sort bids by bid amount.
  - back-to-dashboard (Button): Navigates back to Dashboard.

### 2.6 Auction Categories Page
- **Page Title:** Auction Categories
- **Container ID:** categories-page (Div)
- **Elements:**
  - categories-list (Div): List of categories with descriptions and item counts.
  - category-card-{category_id} (Div): Card for each category, shows name and count.
  - view-category-button-{category_id} (Button): Views items in the category.
  - back-to-dashboard (Button): Navigates back to Dashboard.

### 2.7 Winners Page
- **Page Title:** Winning Items
- **Container ID:** winners-page (Div)
- **Elements:**
  - winners-list (Div): List of winning items with item name, winner, winning bid.
  - winner-card-{auction_id} (Div): Card for each winning item.
  - filter-by-winner (Input): Input field to filter winners by name.
  - back-to-dashboard (Button): Navigates back to Dashboard.

### 2.8 Trending Auctions Page
- **Page Title:** Trending Auctions
- **Container ID:** trending-page (Div)
- **Elements:**
  - trending-list (Div): Ranked list of trending auctions with rank, title, current bid, bid count.
  - time-range-filter (Dropdown): Filter trending auctions by time range (Last 24 Hours, This Week, All Time).
  - view-auction-button-{auction_id} (Button): View auction details.
  - back-to-dashboard (Button): Navigates back to Dashboard.

### 2.9 Auction Status Page
- **Page Title:** Auction Status
- **Container ID:** status-page (Div)
- **Elements:**
  - status-filter (Dropdown): Filter auctions by status (All, Active, Closed, Upcoming).
  - status-table (Table): Auctions with name, status, time remaining, current bid.
  - refresh-status-button (Button): Refresh auction statuses.
  - back-to-dashboard (Button): Navigates back to Dashboard.

---

## 3. Navigation Button Targets

| Button ID                     | Target Page          |
|-------------------------------|----------------------|
| browse-auctions-button         | Auction Catalog Page |
| view-bids-button               | Bid History Page     |
| trending-auctions-button       | Trending Auctions Page|
| view-auction-button-{auction_id}| Auction Details Page (for that auction) |
| place-bid-button               | Place Bid Page (for that auction) |
| submit-bid-button              | (Submits bid, stays or redirects to Bid History or Auction Details as designed) |
| back-to-dashboard (all pages) | Dashboard Page       |
| sort-by-amount                 | Bid History sorting action|
| view-category-button-{category_id}| Auction Catalog filtered by category |
| filter-by-auction              | Filter Bid History listings|
| filter-by-winner              | Filter Winners list|
| time-range-filter              | Filter Trending Auctions|
| refresh-status-button          | Refresh Auction Status data|

---

## 4. Data Storage Contract (Local Text Files)

All data files are stored under the 'data' directory with pipe-separated fields.

### 4.1 auctions.txt
- **Fields:**
  - auction_id (int)
  - item_name (string)
  - description (string)
  - category (string)
  - starting_bid (float)
  - current_bid (float)
  - end_time (datetime string in 'YYYY-MM-DD HH:mm' format)
  - status (string: Active, Closed, Upcoming)
  - image_url (string)
- **Example:**
```
1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
```

### 4.2 categories.txt
- **Fields:**
  - category_id (int)
  - category_name (string)
  - description (string)
  - item_count (int)
- **Example:**
```
1|Electronics|Digital devices and gadgets|15
2|Collectibles|Rare and valuable collector items|28
3|Furniture|Household furniture and decor|12
```

### 4.3 bids.txt
- **Fields:**
  - bid_id (int)
  - auction_id (int)
  - bidder_name (string)
  - bid_amount (float)
  - bid_timestamp (datetime string 'YYYY-MM-DD HH:mm')
- **Example:**
```
1|1|Alice Johnson|45.50|2025-02-05 14:30
2|2|Bob Williams|620.00|2025-02-05 15:45
3|3|Charlie Brown|110.00|2025-02-04 10:15
```

### 4.4 winners.txt
- **Fields:**
  - winner_id (int)
  - auction_id (int)
  - item_name (string)
  - winner_name (string)
  - winning_bid (float)
  - win_date (date string 'YYYY-MM-DD')
- **Example:**
```
1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
```

### 4.5 bid_history.txt
- **Fields:**
  - history_id (int)
  - auction_id (int)
  - auction_name (string)
  - bidder_name (string)
  - bid_amount (float)
  - bid_timestamp (datetime string 'YYYY-MM-DD HH:mm')
- **Example:**
```
1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
```

### 4.6 items.txt
- **Fields:**
  - item_id (int)
  - auction_id (int)
  - item_name (string)
  - starting_price (float)
  - category (string)
  - condition (string)
  - seller_name (string)
- **Example:**
```
1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
```

### 4.7 trending.txt
- **Fields:**
  - auction_id (int)
  - item_name (string)
  - bid_count (int)
  - current_bid (float)
  - trending_rank (int)
  - time_period (string)
- **Example:**
```
2|iPhone 14 Pro|12|620.00|1|This Week
1|Vintage Leather Watch|8|45.50|2|This Week
5|Vintage Camera|6|85.00|3|This Week
```

---

End of Design Specification
