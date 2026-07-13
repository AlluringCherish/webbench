# Detailed Requirements Analysis for 'OnlineAuction' Web Application

---

## Overview
This document provides a comprehensive requirements analysis for the 'OnlineAuction' web application based on the provided user task description. It covers all pages, templates, UI elements by their IDs, buttons, inputs, filters, navigation flows, and data file interactions.

The application starts at the **Dashboard Page** (start page).

---

# 1. Pages and UI Elements

## 1.1 Dashboard Page
- **Template Filename**: (Not explicitly stated, assumed `dashboard.html` or similar)
- **Page Title**: Auction Dashboard
- **Element IDs and Descriptions:**
  - `dashboard-page` (Div): Main container for the dashboard page.
  - `featured-auctions` (Div): Displays featured auction items.
  - `browse-auctions-button` (Button): Navigates to the Auction Catalog page.
  - `view-bids-button` (Button): Navigates to the Bid History page.
  - `trending-auctions-button` (Button): Navigates to the Trending Auctions page.

## 1.2 Auction Catalog Page
- **Template Filename**: (Not explicitly stated, assumed `catalog.html`)
- **Page Title**: Auction Catalog
- **Element IDs and Descriptions:**
  - `catalog-page` (Div): Container for the catalog page.
  - `search-input` (Input): Field to search auctions by item name, description, or item ID.
  - `category-filter` (Dropdown): Dropdown to filter auctions by category, options: Electronics, Collectibles, Furniture, Art, Other.
  - `auctions-grid` (Div): Grid that displays auction cards.
  - `view-auction-button-{auction_id}` (Button): One button per auction item to view detailed auction info. Dynamic ID pattern includes auction_id.

## 1.3 Auction Details Page
- **Template Filename**: (Not explicitly stated, assumed `auction_details.html`)
- **Page Title**: Auction Details
- **Element IDs and Descriptions:**
  - `auction-details-page` (Div): Container for auction details page.
  - `auction-title` (H1): Displays title of the auction item.
  - `auction-description` (Div): Shows the item description.
  - `current-bid` (Div): Shows current highest bid amount.
  - `place-bid-button` (Button): Button to proceed to place a new bid.
  - `bid-history` (Div): Section showing bid history with bidder names and amounts.

## 1.4 Place Bid Page
- **Template Filename**: (Not explicitly stated, assumed `place_bid.html`)
- **Page Title**: Place Bid
- **Element IDs and Descriptions:**
  - `place-bid-page` (Div): Container for the place bid page.
  - `bidder-name` (Input): Input field for bidder's name.
  - `bid-amount` (Input): Input field for bid amount.
  - `auction-name` (Div): Displays the auction item name.
  - `minimum-bid` (Div): Displays minimum acceptable bid amount.
  - `submit-bid-button` (Button): Button to submit the bid.

## 1.5 Bid History Page
- **Template Filename**: (Not explicitly stated, assumed `bid_history.html`)
- **Page Title**: Bid History
- **Element IDs and Descriptions:**
  - `bid-history-page` (Div): Container for the bid history page.
  - `bids-table` (Table): Table listing bids with columns for bid ID, auction name, bidder, amount, timestamp.
  - `filter-by-auction` (Dropdown): Dropdown to filter bids by auction.
  - `sort-by-amount` (Button): Button to sort bids by amount.
  - `back-to-dashboard` (Button): Navigates back to the Dashboard page.

## 1.6 Auction Categories Page
- **Template Filename**: (Not explicitly stated, assumed `categories.html`)
- **Page Title**: Auction Categories
- **Element IDs and Descriptions:**
  - `categories-page` (Div): Container for categories page.
  - `categories-list` (Div): List of categories including descriptions and item counts.
  - `category-card-{category_id}` (Div): Card for each category; dynamic ID includes category_id.
  - `view-category-button-{category_id}` (Button): Button for viewing items in that category; dynamic ID includes category_id.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.

## 1.7 Winners Page
- **Template Filename**: (Not explicitly stated, assumed `winners.html`)
- **Page Title**: Winning Items
- **Element IDs and Descriptions:**
  - `winners-page` (Div): Container for winners page.
  - `winners-list` (Div): List showing winning items, winner name, and winning bid amount.
  - `winner-card-{auction_id}` (Div): Card for each winning auction item; dynamic ID includes auction_id.
  - `filter-by-winner` (Input): Filter winners by name.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.

## 1.8 Trending Auctions Page
- **Template Filename**: (Not explicitly stated, assumed `trending.html`)
- **Page Title**: Trending Auctions
- **Element IDs and Descriptions:**
  - `trending-page` (Div): Container for trending auctions.
  - `trending-list` (Div): Ranked list showing rank, auction title, current bid, bid count.
  - `time-range-filter` (Dropdown): Filter by timeframe (Last 24 Hours, This Week, All Time).
  - `view-auction-button-{auction_id}` (Button): Button to view auction details; dynamic ID includes auction_id.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.

## 1.9 Auction Status Page
- **Template Filename**: (Not explicitly stated, assumed `status.html`)
- **Page Title**: Auction Status
- **Element IDs and Descriptions:**
  - `status-page` (Div): Container for auction status page.
  - `status-filter` (Dropdown): Filters auctions by status (All, Active, Closed, Upcoming).
  - `status-table` (Table): Lists auctions with columns for name, status, time remaining, current bid.
  - `refresh-status-button` (Button): Refreshes auction status data.
  - `back-to-dashboard` (Button): Navigates back to Dashboard.

---

# 2. Data Files and Usage
The application uses local text files stored in the `data` directory with the following mappings:

| Data File          | Data Format Fields                                   | Used By / UI Linkage                                           |
|--------------------|-----------------------------------------------------|---------------------------------------------------------------|
| `auctions.txt`     | auction_id, item_name, description, category, starting_bid, current_bid, end_time, status, image_url | Display in Auction Catalog, Auction Details, Auction Status, Trending Auctions 
| `categories.txt`   | category_id, category_name, description, item_count  | Used on Auction Categories Page for listing and filters       |
| `bids.txt`         | bid_id, auction_id, bidder_name, bid_amount, bid_timestamp | Used in Bid History and Auction Details (bid history section) 
| `winners.txt`      | winner_id, auction_id, item_name, winner_name, winning_bid, win_date | Used in Winners Page                                          |
| `bid_history.txt`  | history_id, auction_id, auction_name, bidder_name, bid_amount, bid_timestamp | Used in Auction Details (bid history) and Bid History Page     |
| `items.txt`        | item_id, auction_id, item_name, starting_price, category, condition, seller_name | May support Auction Catalog or details indirectly             |
| `trending.txt`     | auction_id, item_name, bid_count, current_bid, trending_rank, time_period | Used in Trending Auctions Page                               |

---

# 3. Navigation Flow

- The application starts at the **Dashboard Page**.

- From Dashboard:
  - `browse-auctions-button` → Auction Catalog Page
  - `view-bids-button` → Bid History Page
  - `trending-auctions-button` → Trending Auctions Page

- Auction Catalog (Catalog Page):
  - `view-auction-button-{auction_id}` → Auction Details Page for that auction

- Auction Details Page:
  - `place-bid-button` → Place Bid Page

- Place Bid Page:
  - On bid submission via `submit-bid-button` → likely returns to Auction Details (not explicitly stated)

- Bid History Page:
  - `back-to-dashboard` → Dashboard Page

- Auction Categories Page:
  - `view-category-button-{category_id}` → Auction Catalog Page filtered by that category (implied)
  - `back-to-dashboard` → Dashboard Page

- Winners Page:
  - `back-to-dashboard` → Dashboard Page

- Trending Auctions Page:
  - `view-auction-button-{auction_id}` → Auction Details Page
  - `back-to-dashboard` → Dashboard Page

- Auction Status Page:
  - `back-to-dashboard` → Dashboard Page

- Across pages with `back-to-dashboard` button, navigation is always back to Dashboard.

---

# 4. Summary
This detailed analysis documents every page, element ID, expected interactions including buttons and filters, and data file usage, enabling clear understanding for UI development and data integration for the 'OnlineAuction' web application.

---
