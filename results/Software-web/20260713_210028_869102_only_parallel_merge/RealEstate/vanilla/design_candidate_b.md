# RealEstate Web Application - Detailed Design Specification (Design Candidate B)

---

## Overview
This document presents a detailed design specification for the 'RealEstate' web application. It covers all required pages, Flask routes, HTML template mappings, element and button IDs, template context variables, and data file formats, fully compliant with the provided requirements.

---

## Table of Contents

1. Application Routing and Pages
2. Template Files
3. Element and Button IDs
4. Template Context Variables
5. Data Storage and Formats

---

## 1. Application Routing and Pages

| Page Name             | Flask Route                  | HTTP Method | Page Title             | Template File           | Description                               |
|-----------------------|------------------------------|-------------|------------------------|-------------------------|-------------------------------------------|
| Dashboard             | `/`                          | GET         | Real Estate Dashboard  | dashboard.html          | Main hub; featured properties & quick navigation|
| Property Search       | `/properties`                | GET         | Property Search        | properties_search.html  | List and filter properties                |
| Property Details      | `/properties/<int:property_id>`| GET       | Property Details       | property_details.html   | Details of specific property              |
| Property Inquiry      | `/inquiries/new`             | GET/POST    | Submit Property Inquiry| property_inquiry.html   | Form to submit inquiry                    |
| My Inquiries          | `/inquiries`                 | GET         | My Inquiries           | inquiries.html          | List all user inquiries                   |
| My Favorites          | `/favorites`                 | GET         | My Favorite Properties | favorites.html          | List user's favorite properties           |
| Agent Directory       | `/agents`                   | GET         | Real Estate Agents     | agents.html             | List and search agents                    |
| Locations             | `/locations`                 | GET         | Featured Locations     | locations.html          | List popular locations                    |


---

## 2. Template Files

All templates are HTML files stored in the `templates/` directory:

- dashboard.html
- properties_search.html
- property_details.html
- property_inquiry.html
- inquiries.html
- favorites.html
- agents.html
- locations.html

Each template corresponds to the Flask route pages outlined above.

---

## 3. Element and Button IDs

### 3.1 Dashboard Page (`dashboard.html`)
- `dashboard-page` (Div) - Container for dashboard.
- `featured-properties` (Div) - Displays featured property recommendations.
- `browse-properties-button` (Button) - Navigates to Property Search page.
- `my-inquiries-button` (Button) - Navigates to My Inquiries page.
- `my-favorites-button` (Button) - Navigates to My Favorites page.

### 3.2 Property Search Page (`properties_search.html`)
- `search-page` (Div) - Container for search page.
- `location-input` (Input) - Filter input for location/city.
- `price-range-min` (Input, number) - Minimum price filter.
- `price-range-max` (Input, number) - Maximum price filter.
- `property-type-filter` (Dropdown) - Filter by type (House, Apartment, Condo, Land).
- `properties-grid` (Div) - Grid container showing multiple properties.
- Dynamic Button IDs: `view-property-button-{property_id}` (Button) for each listed property.

### 3.3 Property Details Page (`property_details.html`)
- `property-details-page` (Div) - Container for property details.
- `property-address` (H1) - Displays address.
- `property-price` (Div) - Displays price.
- `property-description` (Div) - Property description.
- `property-features` (Div) - Beds, baths, square footage.
- `add-to-favorites-button` (Button) - Adds property to favorites.
- `submit-inquiry-button` (Button) - Navigates to inquiry submission.

### 3.4 Property Inquiry Page (`property_inquiry.html`)
- `inquiry-page` (Div) - Container for inquiry form.
- `select-property` (Dropdown) - Dropdown to select property (by address or ID).
- `inquiry-name` (Input) - Customer name.
- `inquiry-email` (Input, email) - Customer email.
- `inquiry-phone` (Input, tel) - Customer phone.
- `inquiry-message` (Textarea) - Text message content.
- `submit-inquiry-button` (Button) - Submit inquiry form.

### 3.5 My Inquiries Page (`inquiries.html`)
- `inquiries-page` (Div) - Container for inquiries listing.
- `inquiries-table` (Table) - Table showing inquiries.
- `inquiry-status-filter` (Dropdown) - Filter inquiries by status: All, Pending, Contacted, Resolved.
- Dynamic Button IDs: `delete-inquiry-button-{inquiry_id}` (Button) for deleting individual inquiries.
- `back-to-dashboard` (Button) - Navigates to Dashboard.

### 3.6 My Favorites Page (`favorites.html`)
- `favorites-page` (Div) - Container for favorites list.
- `favorites-list` (Div) - Container listing favorite properties.
- Dynamic Button IDs:
  - `remove-from-favorites-button-{property_id}` (Button) - Remove from favorites.
  - `view-property-button-{property_id}` (Button) - View property details.
- `back-to-dashboard` (Button) - Navigates to Dashboard.

### 3.7 Agent Directory Page (`agents.html`)
- `agents-page` (Div) - Container for agents list.
- `agents-list` (Div) - List all agents.
- `agent-search` (Input) - Search agents by name.
- Dynamic Button IDs: `contact-agent-button-{agent_id}` (Button) for contacting agents.
- `back-to-dashboard` (Button) - Navigates to Dashboard.

### 3.8 Locations Page (`locations.html`)
- `locations-page` (Div) - Container for locations list.
- `locations-list` (Div) - List of locations with details.
- Dynamic Button IDs: `view-location-button-{location_id}` (Button) to view properties for location.
- `location-sort` (Dropdown) - Sort locations by Name, Properties Count, Average Price.
- `back-to-dashboard` (Button) - Navigates to Dashboard.

---

## 4. Template Context Variables

Below are the context variables passed to templates from Flask views.

### 4.1 Dashboard Page
- `featured_properties`: List[Dict] - Each dict includes: `property_id` (int), `address` (str), `location` (str), `price` (int), `property_type` (str), `bedrooms` (int), `bathrooms` (float), `square_feet` (int), `description` (str), `agent_id` (int), `status` (str)

### 4.2 Property Search Page
- `properties`: List[Dict] - All available properties (same structure as above).
- `filter_location`: str - Pre-filled filter location (optional).
- `filter_price_min`: int or None - Minimum price filter.
- `filter_price_max`: int or None - Maximum price filter.
- `filter_property_type`: str or None - Filter property type.

### 4.3 Property Details Page
- `property`: Dict - Single property details with keys matching above.
- `agent`: Dict - Agent info for the property.
- `is_favorite`: bool - Indicates if property is in favorites.

### 4.4 Property Inquiry Page
- `properties`: List[Dict] - Properties list for `select-property` dropdown.

### 4.5 My Inquiries Page
- `inquiries`: List[Dict] - Each dict includes inquiry_id, property (dict as above), customer_name, customer_email, customer_phone, message, inquiry_date (str), status (str).
- `status_filter`: str - Current selected status filter.

### 4.6 My Favorites Page
- `favorites`: List[Dict] - Each dict includes property details, matching property keys and favorite_id (int), added_date (str).

### 4.7 Agent Directory Page
- `agents`: List[Dict] - Each dict with `agent_id` (int), `agent_name` (str), `specialization` (str), `email` (str), `phone` (str), `properties_sold` (int).

### 4.8 Locations Page
- `locations`: List[Dict] - Each dict includes `location_id` (int), `location_name` (str), `region` (str), `average_price` (int), `property_count` (int), `description` (str).
- `sort_option`: str - Current sorting selected.

---

## 5. Data Storage and Formats

Data files reside in a folder named `data/`, each in plain text with `|` pipe character as delimiter.

### 5.1 Properties Data (`properties.txt`)

- Format:
  ```
  property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
  ```
- Fields:
  - `property_id` (int): Unique property ID
  - `address` (str): Full address string
  - `location` (str): Location name e.g. neighborhood or city
  - `price` (int): Listed price in integer
  - `property_type` (str): One of House, Apartment, Condo, Land
  - `bedrooms` (int): Number of bedrooms
  - `bathrooms` (float): Number of bathrooms (can be fractional e.g. 1.5)
  - `square_feet` (int): Size in square feet
  - `description` (str): Text description
  - `agent_id` (int): Agent assigned by ID
  - `status` (str): Current status e.g. Available, Sold

- Example Line:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  ```

### 5.2 Locations Data (`locations.txt`)

- Format:
  ```
  location_id|location_name|region|average_price|property_count|description
  ```
- Fields:
  - `location_id` (int)
  - `location_name` (str)
  - `region` (str)
  - `average_price` (int)
  - `property_count` (int)
  - `description` (str)

- Example Line:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  ```

### 5.3 Property Inquiries Data (`inquiries.txt`)

- Format:
  ```
  inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
  ```
- Fields:
  - `inquiry_id` (int)
  - `property_id` (int)
  - `customer_name` (str)
  - `customer_email` (str)
  - `customer_phone` (str)
  - `message` (str)
  - `inquiry_date` (YYYY-MM-DD string)
  - `status` (str): Pending, Contacted, Resolved

- Example Line:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  ```

### 5.4 Favorite Properties Data (`favorites.txt`)

- Format:
  ```
  favorite_id|property_id|added_date
  ```
- Fields:
  - `favorite_id` (int)
  - `property_id` (int)
  - `added_date` (YYYY-MM-DD string)

- Example Line:
  ```
  1|1|2025-01-10
  ```

### 5.5 Real Estate Agents Data (`agents.txt`)

- Format:
  ```
  agent_id|agent_name|specialization|email|phone|properties_sold
  ```
- Fields:
  - `agent_id` (int)
  - `agent_name` (str)
  - `specialization` (str)
  - `email` (str)
  - `phone` (str)
  - `properties_sold` (int)

- Example Line:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  ```

---

This detailed design specification provides a clear roadmap for full implementation of the RealEstate web application as per functional and UI requirements, ensuring clarity for developers and testers alike.