# Design Specification Document for OnlineAuction Web Application

---

## Overview

This document specifies the full front-end layout, element identifiers, navigation flow, and local text file data schemas for the OnlineAuction application as described in the user requirements.

The web app consists of 9 main pages starting from the Dashboard, interconnected by navigation buttons. Data persistence uses structured text files stored locally.

---

## Pages Specification

### 1. Dashboard Page
- **Page Title:** Auction Dashboard
- **Overview:** Main hub showing featured auctions, trending auctions, and quick navigation buttons.
- **Container:** 
  - Div ID: `dashboard-page` - container for dashboard contents
- **Elements:**
  - Div ID: `featured-auctions` - displays featured auction items
  - Button ID: `browse-auctions-button` - navigates to Auction Catalog Page
  - Button ID: `view-bids-button` - navigates to Bid History Page
  - Button ID: `trending-auctions-button` - navigates to Trending Auctions Page

### 2. Auction Catalog Page
- **Page Title:** Auction Catalog
- **Overview:** Displays all auction items in grid form with search and category filter.
- **Container:**
  - Div ID: `catalog-page`
- **Elements:**
  - Input ID: `search-input` - search field to filter auctions by name, description, or item ID
  - Dropdown ID: `category-filter` - filter auctions by category (Electronics, Collectibles, Furniture, Art, Other)
  - Div ID: `auctions-grid` - grid of auction cards
  - Button ID format: `view-auction-button-{auction_id}` - one per auction card to view details

### 3. Auction Details Page
- **Page Title:** Auction Details
- **Overview:** Detailed view of a single auction item.
- **Container:** 
  - Div ID: `auction-details-page`
- **Elements:**
  - H1 ID: `auction-title` - auction item title
  - Div ID: `auction-description` - item description
  - Div ID: `current-bid` - current highest bid
  - Button ID: `place-bid-button` - navigates to Place Bid Page
  - Div ID: `bid-history` - displays bid history with bidder names and amounts

### 4. Place Bid Page
- **Page Title:** Place Bid
- **Overview:** Form for submitting a new bid for an auction item.
- **Container:**
  - Div ID: `place-bid-page`
- **Elements:**
  - Input ID: `bidder-name` - bidder's name input field
  - Input ID: `bid-amount` - bid amount input field
  - Div ID: `auction-name` - displays auction item name
  - Div ID: `minimum-bid` - displays minimum acceptable bid amount
  - Button ID: `submit-bid-button` - submits the bid

### 5. Bid History Page
- **Page Title:** Bid History
- **Overview:** Shows all bids with options to filter and sort.
- **Container:**
  - Div ID: `bid-history-page`
- **Elements:**
  - Table ID: `bids-table` - list bids with columns: bid ID, auction name, bidder, amount, timestamp
  - Dropdown ID: `filter-by-auction` - filter bids by auction
  - Button ID: `sort-by-amount` - sort bids by bid amount
  - Button ID: `back-to-dashboard` - navigates back to Dashboard Page

### 6. Auction Categories Page
- **Page Title:** Auction Categories
- **Overview:** Lists all auction categories with descriptions and item counts.
- **Container:**
  - Div ID: `categories-page`
- **Elements:**
  - Div ID: `categories-list` - list container for categories
  - Div ID format: `category-card-{category_id}` - one card per category
  - Button ID format: `view-category-button-{category_id}` - navigates to auctions in that category
  - Button ID: `back-to-dashboard` - navigates to Dashboard Page

### 7. Winners Page
- **Page Title:** Winning Items
- **Overview:** Lists auction items won by users including winner info.
- **Container:**
  - Div ID: `winners-page`
- **Elements:**
  - Div ID: `winners-list` - container for winner cards
  - Div ID format: `winner-card-{auction_id}` - one card per winning item
  - Input ID: `filter-by-winner` - filters winners by name
  - Button ID: `back-to-dashboard` - navigates to Dashboard Page

### 8. Trending Auctions Page
- **Page Title:** Trending Auctions
- **Overview:** Shows most active auctions ranked by bid activity.
- **Container:**
  - Div ID: `trending-page`
- **Elements:**
  - Div ID: `trending-list` - ranked list container
  - Dropdown ID: `time-range-filter` - filter trending auctions by time range (Last 24 Hours, This Week, All Time)
  - Button ID format: `view-auction-button-{auction_id}` - view details for trending auction
  - Button ID: `back-to-dashboard` - navigates to Dashboard Page

### 9. Auction Status Page
- **Page Title:** Auction Status
- **Overview:** Displays status overview of all auctions.
- **Container:**
  - Div ID: `status-page`
- **Elements:**
  - Dropdown ID: `status-filter` - filter auctions by status (All, Active, Closed, Upcoming)
  - Table ID: `status-table` - columns: auction name, status, time remaining, current bid
  - Button ID: `refresh-status-button` - refresh auction status data
  - Button ID: `back-to-dashboard` - navigates to Dashboard Page

---

## Navigation Flow

- Dashboard Page is the application entry page.
- Navigation buttons on Dashboard:
  - `browse-auctions-button` → Auction Catalog Page
  - `view-bids-button` → Bid History Page
  - `trending-auctions-button` → Trending Auctions Page
- Auction Catalog Page auction cards’ `view-auction-button-{auction_id}` → Auction Details Page
- Auction Details Page `place-bid-button` → Place Bid Page
- Place Bid Page `submit-bid-button` submits bid (no navigation specified, assumed to return or reload auction details)
- Bid History Page `back-to-dashboard` → Dashboard Page
- Auction Categories Page `back-to-dashboard` → Dashboard Page
- Winners Page `back-to-dashboard` → Dashboard Page
- Trending Auctions Page `back-to-dashboard` → Dashboard Page
- Auction Status Page `back-to-dashboard` → Dashboard Page

---

## Data Storage Contracts

All data stored in local text files under `data/` directory. All data fields and formats must be preserved as specified below.

### 1. Auctions Data
- **Filename:** `auctions.txt`
- **Schema:** 
```
auction_id|item_name|description|category|starting_bid|current_bid|end_time|status|image_url
```
- **Example:**
```
1|Vintage Leather Watch|Antique leather wristwatch from the 1950s|Collectibles|25.00|45.50|2025-02-15 18:00|Active|watch.jpg
2|iPhone 14 Pro|Latest Apple smartphone in excellent condition|Electronics|500.00|620.00|2025-02-10 12:00|Active|iphone.jpg
3|Wooden Desk|Beautiful oak wood desk with original finish|Furniture|75.00|110.00|2025-02-08 20:00|Closed|desk.jpg
```

### 2. Categories Data
- **Filename:** `categories.txt`
- **Schema:**
```
category_id|category_name|description|item_count
```
- **Example:**
```
1|Electronics|Digital devices and gadgets|15
2|Collectibles|Rare and valuable collector items|28
3|Furniture|Household furniture and decor|12
```

### 3. Bids Data
- **Filename:** `bids.txt`
- **Schema:**
```
bid_id|auction_id|bidder_name|bid_amount|bid_timestamp
```
- **Example:**
```
1|1|Alice Johnson|45.50|2025-02-05 14:30
2|2|Bob Williams|620.00|2025-02-05 15:45
3|3|Charlie Brown|110.00|2025-02-04 10:15
```

### 4. Winners Data
- **Filename:** `winners.txt`
- **Schema:**
```
winner_id|auction_id|item_name|winner_name|winning_bid|win_date
```
- **Example:**
```
1|3|Wooden Desk|Charlie Brown|110.00|2025-02-08
2|5|Victorian Mirror|Diana Prince|95.00|2025-02-03
3|7|Vintage Books Set|Eve Stewart|150.00|2025-02-01
```

### 5. Bid History Data
- **Filename:** `bid_history.txt`
- **Schema:**
```
history_id|auction_id|auction_name|bidder_name|bid_amount|bid_timestamp
```
- **Example:**
```
1|1|Vintage Leather Watch|Alice Johnson|40.00|2025-02-05 13:00
2|1|Vintage Leather Watch|Frank Miller|42.50|2025-02-05 13:45
3|2|iPhone 14 Pro|Bob Williams|620.00|2025-02-05 15:45
```

### 6. Items Data
- **Filename:** `items.txt`
- **Schema:**
```
item_id|auction_id|item_name|starting_price|category|condition|seller_name
```
- **Example:**
```
1|1|Vintage Leather Watch|25.00|Collectibles|Excellent|John Collector
2|2|iPhone 14 Pro|500.00|Electronics|Like New|Tech Store
3|3|Wooden Desk|75.00|Furniture|Good|Antique Shop
```

### 7. Trending Data
- **Filename:** `trending.txt`
- **Schema:**
```
auction_id|item_name|bid_count|current_bid|trending_rank|time_period
```
- **Example:**
```
2|iPhone 14 Pro|12|620.00|1|This Week
1|Vintage Leather Watch|8|45.50|2|This Week
5|Vintage Camera|6|85.00|3|This Week
```

---

End of Design Specification Document
