# RealEstate Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                  | HTTP Method | Function Name            | Template Rendered         | Context Variables (Name: Type)                                           | Form Data (POST)                                   |
|-----------------------------|-------------|-------------------------|---------------------------|--------------------------------------------------------------------------|---------------------------------------------------|
| /                           | GET         | root_redirect            | Redirects to /dashboard    | None                                                                     | None                                              |
| /dashboard                  | GET         | dashboard_page          | dashboard.html            | featured_properties: list of dict, recent_listings: list of dict        | None                                              |
| /properties/search          | GET         | property_search_page    | property_search.html       | properties: list of dict, filter_options: dict                           | None                                              |
| /properties/<int:property_id> | GET       | property_details_page    | property_details.html      | property: dict                                                          | None                                              |
| /inquiries/submit           | GET         | inquiry_form_page        | inquiry_form.html          | properties: list of dict                                               | None                                              |
| /inquiries/submit           | POST        | submit_inquiry          | Redirects after POST      | None                                                                     | property_id: int, customer_name: str, customer_email: str, customer_phone: str, inquiry_message: str |
| /inquiries                 | GET         | my_inquiries_page        | inquiries.html             | inquiries: list of dict                                                | None                                              |
| /inquiries/delete/<int:inquiry_id> | POST   | delete_inquiry          | Redirects after POST      | None                                                                     | inquiry_id: int                                    |
| /favorites                 | GET         | my_favorites_page        | favorites.html             | favorites: list of dict, properties_by_id: dict (property_id to dict)   | None                                              |
| /favorites/add/<int:property_id> | POST   | add_to_favorites        | Redirects after POST      | None                                                                     | property_id: int                                  |
| /favorites/remove/<int:property_id>| POST  | remove_from_favorites   | Redirects after POST      | None                                                                     | property_id: int                                  |
| /agents                    | GET         | agents_directory_page    | agents.html                | agents: list of dict                                                  | None                                              |
| /locations                 | GET         | locations_page           | locations.html             | locations: list of dict                                              | None                                              |

**Route Details Notes:**
- Root `/` route redirects to `/dashboard`.
- Routes with POST methods handle form submissions or favorites management.
- Context variables typically are lists of dictionaries representing data entries from files.

---

## Section 2: HTML Templates (Frontend)

---

### 1. dashboard.html
- Page Title: Real Estate Dashboard
- Element IDs:
  - dashboard-page (Div)
  - featured-properties (Div)
  - browse-properties-button (Button)
  - my-inquiries-button (Button)
  - my-favorites-button (Button)
- Context Variables:
  - featured_properties: list of dict (featured property data for display)
  - recent_listings: list of dict (recent property listings)
- Navigation Mappings:
  - browse-properties-button: url_for('property_search_page')
  - my-inquiries-button: url_for('my_inquiries_page')
  - my-favorites-button: url_for('my_favorites_page')
- Forms: None

---

### 2. property_search.html
- Page Title: Property Search
- Element IDs:
  - search-page (Div)
  - location-input (Input)
  - price-range-min (Input - number)
  - price-range-max (Input - number)
  - property-type-filter (Dropdown)
  - properties-grid (Div)
  - view-property-button-{property_id} (Button) dynamic per property
- Context Variables:
  - properties: list of dict (all property data to display)
  - filter_options: dict (property types and filter defaults if any)
- Navigation Mappings:
  - view-property-button-{property_id}: url_for('property_details_page', property_id=property_id)
- Forms: Search/filter form with inputs using above IDs; no separate submit button implied (could be via JS or on filter change)

---

### 3. property_details.html
- Page Title: Property Details
- Element IDs:
  - property-details-page (Div)
  - property-address (H1)
  - property-price (Div)
  - property-description (Div)
  - property-features (Div)
  - add-to-favorites-button (Button)
  - submit-inquiry-button (Button)
- Context Variables:
  - property: dict (detailed info of the selected property)
- Navigation Mappings:
  - add-to-favorites-button: form POST to url_for('add_to_favorites', property_id=property['property_id'])
  - submit-inquiry-button: url_for('inquiry_form_page') or a form submission
- Forms:
  - Form for adding to favorites (button inside form with action to POST favorite addition)
  - Form or link to submit inquiry page

---

### 4. inquiry_form.html
- Page Title: Submit Property Inquiry
- Element IDs:
  - inquiry-page (Div)
  - select-property (Dropdown)
  - inquiry-name (Input)
  - inquiry-email (Input - email)
  - inquiry-phone (Input - tel)
  - inquiry-message (Textarea)
  - submit-inquiry-button (Button)
- Context Variables:
  - properties: list of dict (properties available for inquiry)
- Navigation Mappings:
  - Form action: url_for('submit_inquiry') (POST)
- Forms:
  - Inquiry submission form with all input fields and submit button

---

### 5. inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - inquiries-page (Div)
  - inquiries-table (Table)
  - inquiry-status-filter (Dropdown)
  - delete-inquiry-button-{inquiry_id} (Button) dynamic per inquiry
  - back-to-dashboard (Button)
- Context Variables:
  - inquiries: list of dict (all inquiries with details and status)
- Navigation Mappings:
  - delete-inquiry-button-{inquiry_id}: form POST to url_for('delete_inquiry', inquiry_id=inquiry_id)
  - back-to-dashboard: url_for('dashboard_page')
- Forms:
  - Each delete button inside a form to POST delete

---

### 6. favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - favorites-page (Div)
  - favorites-list (Div)
  - remove-from-favorites-button-{property_id} (Button) dynamic
  - view-property-button-{property_id} (Button) dynamic
  - back-to-dashboard (Button)
- Context Variables:
  - favorites: list of dict (favorites entries)
  - properties_by_id: dict (property_id mapped to property data)
- Navigation Mappings:
  - remove-from-favorites-button-{property_id}: form POST to url_for('remove_from_favorites', property_id=property_id)
  - view-property-button-{property_id}: url_for('property_details_page', property_id=property_id)
  - back-to-dashboard: url_for('dashboard_page')
- Forms:
  - Remove buttons each inside a form for POST

---

### 7. agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - agents-page (Div)
  - agents-list (Div)
  - agent-search (Input)
  - contact-agent-button-{agent_id} (Button) dynamic
  - back-to-dashboard (Button)
- Context Variables:
  - agents: list of dict (all agents with details)
- Navigation Mappings:
  - contact-agent-button-{agent_id}: mailto link or contact form (not specified further)
  - back-to-dashboard: url_for('dashboard_page')
- Forms: None explicit

---

### 8. locations.html
- Page Title: Featured Locations
- Element IDs:
  - locations-page (Div)
  - locations-list (Div)
  - view-location-button-{location_id} (Button) dynamic
  - location-sort (Dropdown)
  - back-to-dashboard (Button)
- Context Variables:
  - locations: list of dict (location data with counts and averages)
- Navigation Mappings:
  - view-location-button-{location_id}: url_for('property_search_page') with location filter (implementation detail)
  - back-to-dashboard: url_for('dashboard_page')
- Forms:
  - Sorting dropdown form

---

## Section 3: Data File Schemas (Backend)

---

### 1. properties.txt
- File Path: data/properties.txt
- Fields (pipe-delimited):
  property_id | address | location | price | property_type | bedrooms | bathrooms | square_feet | description | agent_id | status
- Description: Stores details of each property including identification, location, price, type, specification, description, associated agent, and sale status.
- Example Rows:
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold

---

### 2. locations.txt
- File Path: data/locations.txt
- Fields (pipe-delimited):
  location_id | location_name | region | average_price | property_count | description
- Description: Stores popular locations with metadata including region, average property price, count of properties, and description.
- Example Rows:
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area

---

### 3. inquiries.txt
- File Path: data/inquiries.txt
- Fields (pipe-delimited):
  inquiry_id | property_id | customer_name | customer_email | customer_phone | message | inquiry_date | status
- Description: Records all inquiries submitted by customers per property including contact info, message, date, and inquiry status.
- Example Rows:
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved

---

### 4. favorites.txt
- File Path: data/favorites.txt
- Fields (pipe-delimited):
  favorite_id | property_id | added_date
- Description: Tracks properties marked as favorites including the date they were added.
- Example Rows:
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14

---

### 5. agents.txt
- File Path: data/agents.txt
- Fields (pipe-delimited):
  agent_id | agent_name | specialization | email | phone | properties_sold
- Description: Contains real estate agents information including contact details and specialization.
- Example Rows:
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
