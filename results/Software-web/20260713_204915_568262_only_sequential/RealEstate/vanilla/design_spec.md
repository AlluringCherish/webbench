# Design Specification for 'RealEstate' Flask Web Application

---

## 1. Flask Routes

| URL Path                 | Flask Function Name      | Methods       | Template Rendered             | Context Variables (Name: Type)                          |
|--------------------------|-------------------------|---------------|------------------------------|---------------------------------------------------------|
| /                        | root_redirect            | GET           | Redirect to /dashboard       | None                                                    |
| /dashboard               | dashboard_page          | GET           | dashboard.html               | featured_properties: list[dict]                         |
| /properties/search       | property_search_page     | GET, POST     | property_search.html         | properties: list[dict], filters: dict                   |
| /properties/<int:property_id> | property_details_page      | GET, POST    | property_details.html        | property: dict, favorite_status: bool                   |
| /inquiries/submit        | property_inquiry_page    | GET, POST     | property_inquiry.html        | properties: list[dict], inquiry_submitted: bool (POST) |
| /inquiries               | my_inquiries_page        | GET, POST     | my_inquiries.html            | inquiries: list[dict], status_filter: str               |
| /inquiries/delete/<int:inquiry_id> | delete_inquiry         | POST          | Redirect to /inquiries       | None                                                    |
| /favorites               | my_favorites_page        | GET, POST     | my_favorites.html            | favorites: list[dict]                                   |
| /favorites/remove/<int:property_id> | remove_favorite        | POST          | Redirect to /favorites       | None                                                    |
| /agents                  | agent_directory_page     | GET           | agents.html                  | agents: list[dict], search_query: str                   |
| /locations               | locations_page           | GET           | locations.html               | locations: list[dict], sort_by: str                      |
| /locations/<int:location_id>/properties | location_properties_page   | GET           | properties_by_location.html  | location: dict, properties: list[dict]                  |

---

## 2. Page Templates and Elements

### 2.1 Dashboard Page
- **Route:** `/dashboard`
- **Template:** `dashboard.html`
- **Page Title:** Real Estate Dashboard
- **Element IDs and Types:**
  | ID                      | Type   | Description                             |
  |-------------------------|--------|-------------------------------------|
  | dashboard-page          | Div    | Container for the dashboard page      |
  | featured-properties     | Div    | Display of featured property recommendations |
  | browse-properties-button| Button | Navigates to property search page     |
  | my-inquiries-button     | Button | Navigates to inquiries page           |
  | my-favorites-button     | Button | Navigates to favorites page           |

- **User Interactions & Navigation:**
  - `browse-properties-button`: Navigates to `/properties/search`
  - `my-inquiries-button`: Navigates to `/inquiries`
  - `my-favorites-button`: Navigates to `/favorites`

---

### 2.2 Property Search Page
- **Route:** `/properties/search`
- **Template:** `property_search.html`
- **Page Title:** Property Search
- **Element IDs and Types:**
  | ID                        | Type    | Description                                  |
  |---------------------------|---------|----------------------------------------------|
  | search-page               | Div     | Container for the search page                 |
  | location-input            | Input   | Field to search properties by location/city |
  | price-range-min           | Input (number) | Minimum price filter                     |
  | price-range-max           | Input (number) | Maximum price filter                     |
  | property-type-filter      | Dropdown| Filter by property type (House, Apartment, Condo, Land) |
  | properties-grid           | Div     | Grid displaying property cards with image, location, price, beds/baths |
  | view-property-button-{property_id} | Button | View specific property details (one per property) |

- **User Interactions & Navigation:**
  - Filters via `location-input`, `price-range-min`, `price-range-max`, `property-type-filter` included in form data
  - `view-property-button-{property_id}`: Navigates to `/properties/<property_id>`

---

### 2.3 Property Details Page
- **Route:** `/properties/<int:property_id>`
- **Template:** `property_details.html`
- **Page Title:** Property Details
- **Element IDs and Types:**
  | ID                     | Type   | Description                               |
  |------------------------|--------|-------------------------------------------|
  | property-details-page  | Div    | Container for the property details page   |
  | property-address      | H1     | Displays property address                  |
  | property-price        | Div    | Displays property price                    |
  | property-description  | Div    | Displays property description              |
  | property-features     | Div    | Displays property features (beds, baths, square footage) |
  | add-to-favorites-button | Button | Adds property to favorites                 |
  | submit-inquiry-button | Button | Navigates to Submit Property Inquiry Page with property pre-selected |

- **User Interactions & Navigation:**
  - `add-to-favorites-button`: POST action adds property to favorites
  - `submit-inquiry-button`: Navigates to `/inquiries/submit` with property pre-selected

---

### 2.4 Property Inquiry Page
- **Route:** `/inquiries/submit`
- **Template:** `property_inquiry.html`
- **Page Title:** Submit Property Inquiry
- **Element IDs and Types:**
  | ID                   | Type     | Description                             |
  |----------------------|----------|-----------------------------------------|
  | inquiry-page         | Div      | Container for the inquiry page           |
  | select-property      | Dropdown | Select property to inquire about         |
  | inquiry-name         | Input    | Customer name input field                 |
  | inquiry-email        | Input (email) | Customer email input field            |
  | inquiry-phone        | Input (tel)  | Customer phone input field             |
  | inquiry-message      | Textarea | Inquiry message input field               |
  | submit-inquiry-button| Button   | Submit inquiry button                     |

- **User Interactions & Navigation:**
  - Form fields for inquiry submission
  - On submit, inquiry data saved to `data/inquiries.txt`

---

### 2.5 My Inquiries Page
- **Route:** `/inquiries`
- **Template:** `my_inquiries.html`
- **Page Title:** My Inquiries
- **Element IDs and Types:**
  | ID                       | Type  | Description                             |
  |--------------------------|-------|-----------------------------------------|
  | inquiries-page          | Div   | Container for the inquiries page         |
  | inquiries-table         | Table | Displays inquiries (property, date, status, contact info) |
  | inquiry-status-filter   | Dropdown | Filter inquiries by status (All, Pending, Contacted, Resolved) |
  | delete-inquiry-button-{inquiry_id} | Button | Delete button for each inquiry      |
  | back-to-dashboard      | Button | Navigate back to dashboard               |

- **User Interactions & Navigation:**
  - `inquiry-status-filter` filters inquiries shown
  - `delete-inquiry-button-{inquiry_id}` removes inquiry
  - `back-to-dashboard` navigates to `/dashboard`

---

### 2.6 My Favorites Page
- **Route:** `/favorites`
- **Template:** `my_favorites.html`
- **Page Title:** My Favorite Properties
- **Element IDs and Types:**
  | ID                             | Type   | Description                             |
  |--------------------------------|--------|-----------------------------------------|
  | favorites-page                | Div    | Container for the favorites page        |
  | favorites-list                | Div    | List of favorite properties (address, price, actions) |
  | remove-from-favorites-button-{property_id} | Button | Remove from favorites button (per property) |
  | view-property-button-{property_id} | Button | View property details button (per property) |
  | back-to-dashboard             | Button | Navigate back to dashboard               |

- **User Interactions & Navigation:**
  - `remove-from-favorites-button-{property_id}` removes property from favorites
  - `view-property-button-{property_id}` views property details at `/properties/<property_id>`
  - `back-to-dashboard` navigates to `/dashboard`

---

### 2.7 Agent Directory Page
- **Route:** `/agents`
- **Template:** `agents.html`
- **Page Title:** Real Estate Agents
- **Element IDs and Types:**
  | ID                        | Type   | Description                             |
  |---------------------------|--------|-----------------------------------------|
  | agents-page              | Div    | Container for the agents page            |
  | agents-list              | Div    | List of agents with photo, name, specialization, contact |
  | agent-search             | Input  | Search agents by name                    |
  | contact-agent-button-{agent_id} | Button | Contact agent button (per agent)       |
  | back-to-dashboard        | Button | Navigate back to dashboard               |

- **User Interactions & Navigation:**
  - `agent-search` filters agents by name
  - `contact-agent-button-{agent_id}` opens contact options
  - `back-to-dashboard` navigates to `/dashboard`

---

### 2.8 Locations Page
- **Route:** `/locations`
- **Template:** `locations.html`
- **Page Title:** Featured Locations
- **Element IDs and Types:**
  | ID                        | Type    | Description                             |
  |---------------------------|---------|-----------------------------------------|
  | locations-page           | Div     | Container for the locations page         |
  | locations-list           | Div     | List of locations with name, property count, average price |
  | view-location-button-{location_id} | Button | View properties in location button (per location) |
  | location-sort            | Dropdown| Sort locations (By Name, By Properties Count, By Average Price) |
  | back-to-dashboard        | Button  | Navigate back to dashboard                 |

- **User Interactions & Navigation:**
  - `location-sort` controls sorting of the locations list
  - `view-location-button-{location_id}` navigates to `/locations/<location_id>/properties`
  - `back-to-dashboard` navigates to `/dashboard`

---

## 3. Data Files

All data files stored under `data/` directory, pipe (`|`) delimited. Field orders and descriptions are as follows:

### 3.1 Properties Data
- **File Path:** `data/properties.txt`
- **Fields (pipe-delimited):**
  1. property_id (int) - Unique property identifier
  2. address (string) - Property address
  3. location (string) - Location or city
  4. price (int) - Price in dollars
  5. property_type (string) - Type e.g., House, Apartment, Condo, Land
  6. bedrooms (int) - Number of bedrooms
  7. bathrooms (float) - Number of bathrooms
  8. square_feet (int) - Area in square feet
  9. description (string) - Text description
  10. agent_id (int) - Agent responsible
  11. status (string) - Availability status (Available, Sold, etc.)

- **Example Data:**
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

---

### 3.2 Locations Data
- **File Path:** `data/locations.txt`
- **Fields (pipe-delimited):**
  1. location_id (int) - Unique location identifier
  2. location_name (string) - Name of the location
  3. region (string) - Geographical region
  4. average_price (int) - Average property price
  5. property_count (int) - Number of properties in this location
  6. description (string) - Description of location

- **Example Data:**
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

---

### 3.3 Property Inquiries Data
- **File Path:** `data/inquiries.txt`
- **Fields (pipe-delimited):**
  1. inquiry_id (int) - Unique inquiry identifier
  2. property_id (int) - Property the inquiry is about
  3. customer_name (string) - Customer name
  4. customer_email (string) - Customer email
  5. customer_phone (string) - Customer phone
  6. message (string) - Inquiry message
  7. inquiry_date (string YYYY-MM-DD) - Date of inquiry
  8. status (string) - Inquiry status: Pending, Contacted, Resolved

- **Example Data:**
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

---

### 3.4 Favorite Properties Data
- **File Path:** `data/favorites.txt`
- **Fields (pipe-delimited):**
  1. favorite_id (int) - Unique favorite ID
  2. property_id (int) - Property marked as favorite
  3. added_date (string YYYY-MM-DD) - Date added to favorites

- **Example Data:**
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

---

### 3.5 Real Estate Agents Data
- **File Path:** `data/agents.txt`
- **Fields (pipe-delimited):**
  1. agent_id (int) - Unique agent identifier
  2. agent_name (string) - Agent's full name
  3. specialization (string) - Area of expertise
  4. email (string) - Email address
  5. phone (string) - Contact phone
  6. properties_sold (int) - Number of properties sold

- **Example Data:**
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```

---

This design specification provides a full and exact blueprint for both backend Flask routing and frontend template design along with precise data file contract definitions for the 'RealEstate' web application.