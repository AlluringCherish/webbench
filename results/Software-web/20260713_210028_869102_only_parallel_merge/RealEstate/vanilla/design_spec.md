# RealEstate Web Application - Consolidated Design Specification

---

## 1. Flask Routes and Page Details

| Page Name           | Flask Route                        | HTTP Methods | Page Title               | Template Filename        | Description                                      |
|---------------------|----------------------------------|--------------|--------------------------|--------------------------|--------------------------------------------------|
| Dashboard           | `/`                              | GET          | Real Estate Dashboard    | dashboard.html           | Main hub; featured properties and navigation    |
| Property Search     | `/search` (preferred) or `/properties` (alt.) | GET          | Property Search          | property_search.html     | List and filter properties                       |
| Property Details    | `/property/<int:property_id>` (preferred) or `/properties/<int:property_id>` (alt.) | GET          | Property Details         | property_details.html    | Details of specific property                    |
| Property Inquiry    | `/inquiry/submit` (preferred) or `/inquiries/new` (alt.) | GET, POST     | Submit Property Inquiry  | property_inquiry.html    | Form to submit inquiry                          |
| My Inquiries        | `/inquiries`                     | GET          | My Inquiries             | my_inquiries.html        | List all user inquiries                         |
| Delete Inquiry      | `/inquiries/delete/<int:inquiry_id>` | POST       | (action only)            | n/a                      | Delete a specific inquiry                       |
| My Favorites        | `/favorites`                    | GET          | My Favorite Properties   | my_favorites.html        | List user's favorite properties                |
| Remove Favorite     | `/favorites/remove/<int:property_id>` | POST       | (action only)            | n/a                      | Remove a property from favorites               |
| Agent Directory     | `/agents`                      | GET          | Real Estate Agents       | agent_directory.html     | List and search agents                          |
| Locations Page      | `/locations`                   | GET          | Featured Locations       | locations.html           | List popular locations                          |

---

## 2. Template Filenames

Standardized the template filenames to the preferred form where possible:

- dashboard.html
- property_search.html
- property_details.html
- property_inquiry.html
- my_inquiries.html
- my_favorites.html
- agent_directory.html
- locations.html

Alternate filenames used in candidate B (like properties_search.html, inquiries.html, favorites.html, agents.html) are consolidated to preferred consistent names matching candidate A.

---

## 3. Element and Button IDs

### 3.1 Dashboard Page (`dashboard.html`)
- `dashboard-page` (Div) - Container for dashboard page
- `featured-properties` (Div) - Featured property recommendations
- `browse-properties-button` (Button) - Navigate to Property Search page
- `my-inquiries-button` (Button) - Navigate to My Inquiries page
- `my-favorites-button` (Button) - Navigate to My Favorites page

### 3.2 Property Search Page (`property_search.html`)
- `search-page` (Div) - Container of search page
- `location-input` (Input) - Filter input for location/city
- `price-range-min` (Input number) - Minimum price filter
- `price-range-max` (Input number) - Maximum price filter
- `property-type-filter` (Dropdown) - Filter property type (House, Apartment, Condo, Land)
- `properties-grid` (Div) - Grid for displaying property cards
- Dynamic Button IDs:
  - `view-property-button-{property_id}` (Button) for each listed property

### 3.3 Property Details Page (`property_details.html`)
- `property-details-page` (Div) - Container for property details
- `property-address` (H1) - Displays address
- `property-price` (Div) - Displays price
- `property-description` (Div) - Property description
- `property-features` (Div) - Beds, baths, square footage
- `add-to-favorites-button` (Button) - Add property to favorites
- `submit-inquiry-button` (Button) - Navigate to inquiry submission

### 3.4 Property Inquiry Page (`property_inquiry.html`)
- `inquiry-page` (Div) - Container for inquiry form
- `select-property` (Dropdown) - Select property for inquiry
- `inquiry-name` (Input) - Customer name
- `inquiry-email` (Input email) - Customer email
- `inquiry-phone` (Input tel) - Customer phone
- `inquiry-message` (Textarea) - Inquiry message
- `submit-inquiry-button` (Button) - Submit inquiry form

### 3.5 My Inquiries Page (`my_inquiries.html`)
- `inquiries-page` (Div) - Container for inquiries listing
- `inquiries-table` (Table) - Table of inquiries
- `inquiry-status-filter` (Dropdown) - Filter inquiries by status (All, Pending, Contacted, Resolved)
- Dynamic Button IDs:
  - `delete-inquiry-button-{inquiry_id}` (Button) for each inquiry delete action
- `back-to-dashboard` (Button) - Navigate to Dashboard

### 3.6 My Favorites Page (`my_favorites.html`)
- `favorites-page` (Div) - Container for favorites list
- `favorites-list` (Div) - List of favorite properties
- Dynamic Button IDs:
  - `remove-from-favorites-button-{property_id}` (Button) to remove from favorites
  - `view-property-button-{property_id}` (Button) to view property details
- `back-to-dashboard` (Button) - Navigate to Dashboard

### 3.7 Agent Directory Page (`agent_directory.html`)
- `agents-page` (Div) - Container for agents list
- `agents-list` (Div) - List of agents
- `agent-search` (Input) - Search agents by name
- Dynamic Button IDs:
  - `contact-agent-button-{agent_id}` (Button) to contact agent
- `back-to-dashboard` (Button) - Navigate to Dashboard

### 3.8 Locations Page (`locations.html`)
- `locations-page` (Div) - Container for locations list
- `locations-list` (Div) - List of locations
- Dynamic Button IDs:
  - `view-location-button-{location_id}` (Button) to view location properties
- `location-sort` (Dropdown) - Sort locations by Name, Properties Count, Average Price
- `back-to-dashboard` (Button) - Navigate to Dashboard

---

## 4. Template Context Variables

### 4.1 Dashboard Page (`dashboard.html`)
- `featured_properties`: List[Dict] with keys:
  - `property_id` (int), `address` (str), `location` (str), `price` (int), `property_type` (str), `bedrooms` (int), `bathrooms` (float), `square_feet` (int), `description` (str), `agent_id` (int), `status` (str)

### 4.2 Property Search Page (`property_search.html`)
- `properties`: List[Dict] all available properties, keys as above
- `filter_location`: str (optional filter value or empty string)
- `filter_price_min`: int or None
- `filter_price_max`: int or None
- `filter_property_type`: str or None

### 4.3 Property Details Page (`property_details.html`)
- `property`: Dict single property details (keys as above)
- `agent`: Dict with agent details:
  - `agent_id` (int), `agent_name` (str), `specialization` (str), `email` (str), `phone` (str), `properties_sold` (int)
- `is_favorite`: bool

### 4.4 Property Inquiry Page (`property_inquiry.html`)
- `properties`: List[Dict] properties for dropdown (keys as above)
- `submission_status`: str or None (Success or error message after submission)

### 4.5 My Inquiries Page (`my_inquiries.html`)
- `inquiries`: List[Dict] inquiries with keys:
  - `inquiry_id` (int), `property`: Dict (property details), `customer_name` (str), `customer_email` (str), `customer_phone` (str), `message` (str), `inquiry_date` (str YYYY-MM-DD), `status` (str)
- `status_filter`: str current selected status filter

### 4.6 My Favorites Page (`my_favorites.html`)
- `favorites`: List[Dict] favorite properties data combining:
  - favorite_id (int), added_date (str YYYY-MM-DD), with full property details keys as above

### 4.7 Agent Directory Page (`agent_directory.html`)
- `agents`: List[Dict] with keys:
  - `agent_id` (int), `agent_name` (str), `specialization` (str), `email` (str), `phone` (str), `properties_sold` (int)
- `search_query`: str current search input or empty string

### 4.8 Locations Page (`locations.html`)
- `locations`: List[Dict] with keys:
  - `location_id` (int), `location_name` (str), `region` (str), `average_price` (int), `property_count` (int), `description` (str)
- `sort_option`: str current sort option

---

## 5. Data Files and Formats

All data files are stored in a folder named `data/` and use the pipe `|` character as the delimiter.

### 5.1 Properties Data - `data/properties.txt`
- Fields with order and type:
  1. `property_id` (int)
  2. `address` (str)
  3. `location` (str)
  4. `price` (int)
  5. `property_type` (str: House, Apartment, Condo, Land)
  6. `bedrooms` (int)
  7. `bathrooms` (float)
  8. `square_feet` (int)
  9. `description` (str)
  10. `agent_id` (int)
  11. `status` (str: Available, Sold, etc.)

### 5.2 Locations Data - `data/locations.txt`
- Fields:
  1. `location_id` (int)
  2. `location_name` (str)
  3. `region` (str)
  4. `average_price` (int)
  5. `property_count` (int)
  6. `description` (str)

### 5.3 Property Inquiries Data - `data/inquiries.txt`
- Fields:
  1. `inquiry_id` (int)
  2. `property_id` (int)
  3. `customer_name` (str)
  4. `customer_email` (str)
  5. `customer_phone` (str)
  6. `message` (str)
  7. `inquiry_date` (str YYYY-MM-DD)
  8. `status` (str: Pending, Contacted, Resolved)

### 5.4 Favorite Properties Data - `data/favorites.txt`
- Fields:
  1. `favorite_id` (int)
  2. `property_id` (int)
  3. `added_date` (str YYYY-MM-DD)

### 5.5 Real Estate Agents Data - `data/agents.txt`
- Fields:
  1. `agent_id` (int)
  2. `agent_name` (str)
  3. `specialization` (str)
  4. `email` (str)
  5. `phone` (str)
  6. `properties_sold` (int)

---


## 6. Navigation Paths

Each page includes buttons or elements for navigation:
- From Dashboard:
  - `browse-properties-button` -> Property Search (`/search`)
  - `my-inquiries-button` -> My Inquiries (`/inquiries`)
  - `my-favorites-button` -> My Favorites (`/favorites`)

- From Property Search:
  - `view-property-button-{property_id}` -> Property Details (`/property/<int:property_id>`)

- From Property Details:
  - `add-to-favorites-button` -> adds property to favorites (POST action)
  - `submit-inquiry-button` -> Property Inquiry (`/inquiry/submit`)

- From Property Inquiry:
  - submission leads to success/error and retains form

- From My Inquiries:
  - `delete-inquiry-button-{inquiry_id}` -> deletes inquiry (POST)
  - `back-to-dashboard` -> Dashboard (`/`)

- From My Favorites:
  - `remove-from-favorites-button-{property_id}` -> removes from favorites (POST)
  - `view-property-button-{property_id}` -> Property Details (`/property/<int:property_id>`)
  - `back-to-dashboard` -> Dashboard (`/`)

- From Agent Directory:
  - `contact-agent-button-{agent_id}` for contacting agent (functionality defined elsewhere)
  - `back-to-dashboard` -> Dashboard (`/`)

- From Locations:
  - `view-location-button-{location_id}` -> property listings filtered by location (functionality to implement)
  - `location-sort` dropdown changes sort order
  - `back-to-dashboard` -> Dashboard (`/`)

---

This comprehensive specification aligns the two candidate designs into a single complete reference for development, ensuring unambiguous route definitions, template usage, element IDs, context variables, data files, and page navigation flows as per the user task requirements.
