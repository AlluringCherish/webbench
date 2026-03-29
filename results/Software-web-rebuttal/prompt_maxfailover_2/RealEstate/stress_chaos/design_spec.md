# RealEstate Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                        | HTTP Method(s) | Function Name           | Template Rendered       | Context Variables (name:type)                                                            | Form Data (POST)                                           |
|---------------------------------|----------------|------------------------|-------------------------|-----------------------------------------------------------------------------------------|------------------------------------------------------------|
| /                               | GET            | root_redirect           | None (redirects to dashboard) | None                                                                                | None                                                       |
| /dashboard                      | GET            | dashboard_page          | dashboard.html          | featured_properties: list of dict (property info), recent_listings: list of dict (property info) | None                                                       |
| /search                        | GET            | property_search_page    | property_search.html    | properties: list of dict (all available properties), filter_options: dict (location:str, price_min:int, price_max:int, property_type:str) | None                                                       |
| /property/<int:property_id>     | GET            | property_details_page   | property_details.html   | property: dict (detailed property info), is_favorite: bool                                | None                                                       |
| /inquiry                       | GET            | property_inquiry_page   | inquiry.html            | properties: list of dict (available properties for dropdown)                            | None                                                       |
| /inquiry                       | POST           | submit_property_inquiry | inquiry.html            | errors: list of str (validation errors, if any)                                        | property_id (int), customer_name (str), customer_email (str), customer_phone (str), message (str) |
| /my-inquiries                 | GET            | my_inquiries_page       | my_inquiries.html       | inquiries: list of dict (user inquiries info), status_filter_options: list of str       | None                                                       |
| /my-inquiries/delete/<int:inquiry_id> | POST    | delete_inquiry          | my_inquiries.html       | None                                                                                | inquiry_id (int)                                           |
| /my-favorites                 | GET            | my_favorites_page       | my_favorites.html       | favorites: list of dict (favorite properties info)                                    | None                                                       |
| /my-favorites/add/<int:property_id> | POST     | add_to_favorites        | None (redirect or JSON) | None                                                                                | property_id (int)                                           |
| /my-favorites/remove/<int:property_id> | POST  | remove_from_favorites   | None (redirect or JSON) | None                                                                                | property_id (int)                                           |
| /agents                       | GET            | agents_page             | agents.html             | agents: list of dict (agent info)                                                    | None                                                       |
| /locations                   | GET            | locations_page          | locations.html          | locations: list of dict (location info), sort_option: str                             | None                                                       |

Notes:
- The root route '/' performs a redirect to '/dashboard'.
- POST routes that modify data (add/remove favorites, delete inquiry) expect form data as specified.
- GET routes only render template with specified context variables.

---

## Section 2: HTML Templates (Frontend)

### 1. dashboard.html
- Page Title: Real Estate Dashboard
- <title> and <h1> contain: "Real Estate Dashboard"
- Element IDs:
  - dashboard-page (Div - container)
  - featured-properties (Div - displays featured property recommendations)
  - browse-properties-button (Button - navigates to property search page)
  - my-inquiries-button (Button - navigates to inquiries page)
  - my-favorites-button (Button - navigates to favorites page)
- Context Variables:
  - featured_properties: list of dict (each dict contains property_id:int, address:str, price:float, image_url:str)
  - recent_listings: list of dict (each dict contains property_id:int, address:str, price:float, image_url:str)
- Navigation Links:
  - browse-properties-button: url_for('property_search_page')
  - my-inquiries-button: url_for('my_inquiries_page')
  - my-favorites-button: url_for('my_favorites_page')
- No forms on this page

### 2. property_search.html
- Page Title: Property Search
- <title> and <h1>: "Property Search"
- Element IDs:
  - search-page (Div - container)
  - location-input (Input - for location/city search)
  - price-range-min (Number Input - minimum price filter)
  - price-range-max (Number Input - maximum price filter)
  - property-type-filter (Dropdown - filter by property type: House, Apartment, Condo, Land)
  - properties-grid (Div - grid displaying property cards)
  - view-property-button-{property_id} (Button for each property card)
- Context Variables:
  - properties: list of dict (property_id:int, address:str, location:str, price:float, bedrooms:int, bathrooms:float, property_type:str, image_url:str)
  - filter_options: dict (location:str, price_min:int, price_max:int, property_type:str)
- Navigation Links:
  - Each view-property-button-{property_id} links to url_for('property_details_page', property_id=property_id)
- No forms on this page for POST

### 3. property_details.html
- Page Title: Property Details
- <title> and <h1>: "Property Details"
- Element IDs:
  - property-details-page (Div - container)
  - property-address (H1 - address display)
  - property-price (Div - price display)
  - property-description (Div - description)
  - property-features (Div - beds, baths, sqft)
  - add-to-favorites-button (Button to add property to favorites)
  - submit-inquiry-button (Button to submit inquiry)
- Context Variables:
  - property: dict (property_id:int, address:str, location:str, price:float, property_type:str, bedrooms:int, bathrooms:float, square_feet:int, description:str, agent_id:int, status:str)
  - is_favorite: bool
- Navigation Links:
  - add-to-favorites-button posts to '/my-favorites/add/<property_id>'
  - submit-inquiry-button links to url_for('property_inquiry_page')

### 4. inquiry.html
- Page Title: Submit Property Inquiry
- <title> and <h1>: "Submit Property Inquiry"
- Element IDs:
  - inquiry-page (Div - container)
  - select-property (Dropdown - select property for inquiry)
  - inquiry-name (Input - customer name)
  - inquiry-email (Input email - customer email)
  - inquiry-phone (Input tel - customer phone)
  - inquiry-message (Textarea - inquiry message)
  - submit-inquiry-button (Button to submit inquiry)
- Context Variables:
  - properties: list of dict (property_id:int, address:str)
  - errors: list of str (optional validation error messages) if POST with errors
- Forms:
  - Form with method POST, action url_for('submit_property_inquiry')
  - Inputs: select-property (dropdown), inquiry-name (text), inquiry-email (email), inquiry-phone (tel), inquiry-message (textarea)
  - Submit button: submit-inquiry-button

### 5. my_inquiries.html
- Page Title: My Inquiries
- <title> and <h1>: "My Inquiries"
- Element IDs:
  - inquiries-page (Div - container)
  - inquiries-table (Table - displays inquiries with columns: Property, Date, Status, Contact Info)
  - inquiry-status-filter (Dropdown - filter by status: All, Pending, Contacted, Resolved)
  - delete-inquiry-button-{inquiry_id} (Button to delete specific inquiry)
  - back-to-dashboard (Button to navigate back to dashboard)
- Context Variables:
  - inquiries: list of dict (inquiry_id:int, property_address:str, inquiry_date:str, status:str, customer_name:str, customer_email:str, customer_phone:str, message:str)
  - status_filter_options: list of str (All, Pending, Contacted, Resolved)
- Navigation Links:
  - back-to-dashboard: url_for('dashboard_page')
- Forms:
  - Delete inquiry buttons post to '/my-inquiries/delete/<inquiry_id>' with method POST

### 6. my_favorites.html
- Page Title: My Favorite Properties
- <title> and <h1>: "My Favorite Properties"
- Element IDs:
  - favorites-page (Div - container)
  - favorites-list (Div - list of favorite properties)
  - remove-from-favorites-button-{property_id} (Button to remove property from favorites)
  - view-property-button-{property_id} (Button to view property details)
  - back-to-dashboard (Button to navigate back to dashboard)
- Context Variables:
  - favorites: list of dict (property_id:int, address:str, price:float, image_url:str)
- Navigation Links:
  - back-to-dashboard: url_for('dashboard_page')
  - view-property-button-{property_id}: url_for('property_details_page', property_id=property_id)
- Forms:
  - Remove from favorites buttons post to '/my-favorites/remove/<property_id>' with method POST

### 7. agents.html
- Page Title: Real Estate Agents
- <title> and <h1>: "Real Estate Agents"
- Element IDs:
  - agents-page (Div - container)
  - agents-list (Div - list of agents)
  - agent-search (Input - search agents by name)
  - contact-agent-button-{agent_id} (Button to contact agent)
  - back-to-dashboard (Button to navigate back to dashboard)
- Context Variables:
  - agents: list of dict (agent_id:int, agent_name:str, specialization:str, email:str, phone:str, properties_sold:int, photo_url:str optional)
- Navigation Links:
  - back-to-dashboard: url_for('dashboard_page')
- Forms:
  - Contact agent buttons may link to mailto or external contact, no backend route required

### 8. locations.html
- Page Title: Featured Locations
- <title> and <h1>: "Featured Locations"
- Element IDs:
  - locations-page (Div - container)
  - locations-list (Div - list of locations)
  - view-location-button-{location_id} (Button to view properties in a location)
  - location-sort (Dropdown - sort locations by (By Name, By Properties Count, By Average Price))
  - back-to-dashboard (Button to navigate back to dashboard)
- Context Variables:
  - locations: list of dict (location_id:int, location_name:str, region:str, average_price:float, property_count:int, description:str)
  - sort_option: str
- Navigation Links:
  - back-to-dashboard: url_for('dashboard_page')
- Forms:
  - view-location-button-{location_id} link or button triggers property search filtered by location, no direct backend route specified

---

## Section 3: Data File Schemas (Backend)

### 1. properties.txt
- Data File Path: data/properties.txt
- Pipe-delimited Fields in Order:
  1. property_id (int)
  2. address (str)
  3. location (str)
  4. price (float)
  5. property_type (str)
  6. bedrooms (int)
  7. bathrooms (float)
  8. square_feet (int)
  9. description (str)
  10. agent_id (int)
  11. status (str)
- Description: Stores detailed information about properties listed for sale.
- Example Rows:
  - 1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  - 2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  - 3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold

### 2. locations.txt
- Data File Path: data/locations.txt
- Pipe-delimited Fields in Order:
  1. location_id (int)
  2. location_name (str)
  3. region (str)
  4. average_price (float)
  5. property_count (int)
  6. description (str)
- Description: Stores information about featured locations with property count and average price.
- Example Rows:
  - 1|Downtown|Central|425000|45|Urban area with business district
  - 2|Midtown|Central|380000|38|Mixed residential and commercial zone
  - 3|Suburb|Outskirts|295000|52|Family-friendly residential area

### 3. inquiries.txt
- Data File Path: data/inquiries.txt
- Pipe-delimited Fields in Order:
  1. inquiry_id (int)
  2. property_id (int)
  3. customer_name (str)
  4. customer_email (str)
  5. customer_phone (str)
  6. message (str)
  7. inquiry_date (str, YYYY-MM-DD)
  8. status (str)
- Description: Stores submitted property inquiries with customer contact and status.
- Example Rows:
  - 1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  - 2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  - 3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved

### 4. favorites.txt
- Data File Path: data/favorites.txt
- Pipe-delimited Fields in Order:
  1. favorite_id (int)
  2. property_id (int)
  3. added_date (str, YYYY-MM-DD)
- Description: Stores user's favorite properties with the date they were added.
- Example Rows:
  - 1|1|2025-01-10
  - 2|2|2025-01-12
  - 3|3|2025-01-14

### 5. agents.txt
- Data File Path: data/agents.txt
- Pipe-delimited Fields in Order:
  1. agent_id (int)
  2. agent_name (str)
  3. specialization (str)
  4. email (str)
  5. phone (str)
  6. properties_sold (int)
- Description: Stores real estate agents' details and contact information.
- Example Rows:
  - 101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  - 102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  - 103|James Martinez|Luxury Homes|james@email.com|555-0003|67
