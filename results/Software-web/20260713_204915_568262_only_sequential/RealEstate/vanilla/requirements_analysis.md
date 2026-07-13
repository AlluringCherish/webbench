# Requirements Analysis for 'RealEstate' Web Application

## 1. Overview
This document details the functional requirements for the 'RealEstate' web application as per the provided task description. It covers the pages, UI elements with exact IDs and types, user interactions, navigation flows, and data storage formats including file structure and example data.

---

## 2. Pages and Elements

### 2.1 Dashboard Page
- **Page Title:** Real Estate Dashboard
- **Elements:**
  | ID                      | Type   | Description                             |
  |-------------------------|--------|-------------------------------------|
  | dashboard-page          | Div    | Container for the dashboard page      |
  | featured-properties     | Div    | Display of featured property recommendations |
  | browse-properties-button| Button | Navigates to property search page     |
  | my-inquiries-button     | Button | Navigates to inquiries page           |
  | my-favorites-button     | Button | Navigates to favorites page           |

### 2.2 Property Search Page
- **Page Title:** Property Search
- **Elements:**
  | ID                        | Type    | Description                                  |
  |---------------------------|---------|----------------------------------------------|
  | search-page               | Div     | Container for the search page                 |
  | location-input            | Input   | Field to search properties by location/city |
  | price-range-min           | Input (number) | Minimum price filter                     |
  | price-range-max           | Input (number) | Maximum price filter                     |
  | property-type-filter      | Dropdown| Filter by property type (House, Apartment, Condo, Land) |
  | properties-grid           | Div     | Grid displaying property cards with image, location, price, beds/baths |
  | view-property-button-{property_id} | Button | Button to view specific property details (one per property) |

### 2.3 Property Details Page
- **Page Title:** Property Details
- **Elements:**
  | ID                     | Type   | Description                               |
  |------------------------|--------|-------------------------------------------|
  | property-details-page  | Div    | Container for the property details page   |
  | property-address      | H1     | Displays property address                  |
  | property-price        | Div    | Displays property price                    |
  | property-description  | Div    | Displays property description              |
  | property-features     | Div    | Displays property features (beds, baths, square footage) |
  | add-to-favorites-button | Button | Adds property to favorites                 |
  | submit-inquiry-button | Button | Submits inquiry for the property           |

### 2.4 Property Inquiry Page
- **Page Title:** Submit Property Inquiry
- **Elements:**
  | ID                   | Type     | Description                             |
  |----------------------|----------|-----------------------------------------|
  | inquiry-page         | Div      | Container for the inquiry page           |
  | select-property      | Dropdown | Select property to inquire about         |
  | inquiry-name         | Input    | Customer name input field                 |
  | inquiry-email        | Input (email) | Customer email input field            |
  | inquiry-phone        | Input (tel)  | Customer phone input field             |
  | inquiry-message      | Textarea | Inquiry message input field               |
  | submit-inquiry-button| Button   | Submit inquiry button                     |

### 2.5 My Inquiries Page
- **Page Title:** My Inquiries
- **Elements:**
  | ID                       | Type  | Description                             |
  |--------------------------|-------|-----------------------------------------|
  | inquiries-page          | Div   | Container for the inquiries page         |
  | inquiries-table         | Table | Displays inquiries (property, date, status, contact info) |
  | inquiry-status-filter   | Dropdown | Filter inquiries by status (All, Pending, Contacted, Resolved) |
  | delete-inquiry-button-{inquiry_id} | Button | Delete button for each inquiry      |
  | back-to-dashboard      | Button | Navigate back to dashboard               |

### 2.6 My Favorites Page
- **Page Title:** My Favorite Properties
- **Elements:**
  | ID                             | Type   | Description                             |
  |--------------------------------|--------|-----------------------------------------|
  | favorites-page                | Div    | Container for the favorites page        |
  | favorites-list                | Div    | List of favorite properties (address, price, actions) |
  | remove-from-favorites-button-{property_id} | Button | Remove from favorites button (per property) |
  | view-property-button-{property_id} | Button | View property details button (per property) |
  | back-to-dashboard             | Button | Navigate back to dashboard               |

### 2.7 Agent Directory Page
- **Page Title:** Real Estate Agents
- **Elements:**
  | ID                        | Type   | Description                             |
  |---------------------------|--------|-----------------------------------------|
  | agents-page              | Div    | Container for the agents page            |
  | agents-list              | Div    | List of agents with photo, name, specialization, contact |
  | agent-search             | Input  | Search agents by name                    |
  | contact-agent-button-{agent_id} | Button | Contact agent button (per agent)       |
  | back-to-dashboard        | Button | Navigate back to dashboard               |

### 2.8 Locations Page
- **Page Title:** Featured Locations
- **Elements:**
  | ID                        | Type    | Description                             |
  |---------------------------|---------|-----------------------------------------|
  | locations-page           | Div     | Container for the locations page         |
  | locations-list           | Div     | List of locations with name, property count, average price |
  | view-location-button-{location_id} | Button | View properties in location button (per location) |
  | location-sort            | Dropdown| Sort locations (By Name, By Properties Count, By Average Price) |
  | back-to-dashboard        | Button  | Navigate back to dashboard                 |

---

## 3. User Interaction Flows

- **Dashboard Page:**
  - Buttons:
    - `browse-properties-button`: Navigates to Property Search Page.
    - `my-inquiries-button`: Navigates to My Inquiries Page.
    - `my-favorites-button`: Navigates to My Favorites Page.

- **Property Search Page:**
  - Inputs:
    - `location-input`: Text input to filter properties by city/location.
    - `price-range-min` & `price-range-max`: Number inputs for minimum and maximum price filters.
    - `property-type-filter`: Dropdown to select property type filter.
  - Buttons:
    - `view-property-button-{property_id}`: Each property card includes this button, which navigates to Property Details Page for the given property.

- **Property Details Page:**
  - Buttons:
    - `add-to-favorites-button`: Adds the displayed property to favorite properties list.
    - `submit-inquiry-button`: Navigates to Submit Property Inquiry Page with the selected property pre-selected.

- **Property Inquiry Page:**
  - Inputs:
    - `select-property`: Dropdown to select property to inquire about.
    - `inquiry-name`: Text input for customer name.
    - `inquiry-email`: Email input for customer email.
    - `inquiry-phone`: Telephone input for customer phone.
    - `inquiry-message`: Text area for inquiry message.
  - Buttons:
    - `submit-inquiry-button`: Submits the inquiry data and stores it.

- **My Inquiries Page:**
  - Elements:
    - `inquiries-table`: Displays all submitted inquiries.
    - `inquiry-status-filter`: Dropdown to filter inquiries by their status.
  - Buttons:
    - `delete-inquiry-button-{inquiry_id}`: For deleting a specific inquiry.
    - `back-to-dashboard`: Navigates back to Dashboard Page.

- **My Favorites Page:**
  - Elements:
    - `favorites-list`: Lists all favorite properties.
  - Buttons:
    - `remove-from-favorites-button-{property_id}`: Remove that property from favorites.
    - `view-property-button-{property_id}`: View detailed property info.
    - `back-to-dashboard`: Navigate back to Dashboard Page.

- **Agent Directory Page:**
  - Inputs:
    - `agent-search`: Text input to search agents by name.
  - Buttons:
    - `contact-agent-button-{agent_id}`: Opens contact options for selected agent.
    - `back-to-dashboard`: Navigate back to Dashboard Page.

- **Locations Page:**
  - Elements:
    - `locations-list`: Displays popular locations with information.
  - Controls:
    - `location-sort`: Dropdown to sort locations based on criteria.
  - Buttons:
    - `view-location-button-{location_id}`: Navigates to show properties in the selected location.
    - `back-to-dashboard`: Navigate back to Dashboard Page.

---

## 4. Data Storage Formats

All data files are stored under the `data/` directory, pipe (`|`) delimited with the exact field order as below.

### 4.1 Properties Data
- **Filename:** `properties.txt`
- **Format:**
  ```
  property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
  ```
- **Example:**
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

### 4.2 Locations Data
- **Filename:** `locations.txt`
- **Format:**
  ```
  location_id|location_name|region|average_price|property_count|description
  ```
- **Example:**
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

### 4.3 Property Inquiries Data
- **Filename:** `inquiries.txt`
- **Format:**
  ```
  inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
  ```
- **Example:**
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

### 4.4 Favorite Properties Data
- **Filename:** `favorites.txt`
- **Format:**
  ```
  favorite_id|property_id|added_date
  ```
- **Example:**
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

### 4.5 Real Estate Agents Data
- **Filename:** `agents.txt`
- **Format:**
  ```
  agent_id|agent_name|specialization|email|phone|properties_sold
  ```
- **Example:**
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```

---

This concludes the detailed requirements analysis for the 'RealEstate' web application as provided in the user task description.