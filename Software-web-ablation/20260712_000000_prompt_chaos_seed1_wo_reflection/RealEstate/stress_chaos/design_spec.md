# RealEstate Web Application Design Specification

---

## Section 1: Flask Routes Specification (Backend)

| Route Path                      | HTTP Method | Function Name           | Template Rendered          | Context Variables (Name:Type)                      | Form Data Expected (POST)                                  |
|---------------------------------|-------------|------------------------|----------------------------|--------------------------------------------------|-----------------------------------------------------------|
| /                               | GET         | root_redirect          | Redirects to /dashboard    | None                                             | None                                                      |
| /dashboard                      | GET         | dashboard              | dashboard.html             | featured_properties: list (of dict)                  | None                                                      |
| /search                        | GET         | property_search         | search.html                | properties: list (of dict),
  filter_location: str,
  filter_price_min: float|int or None,
  filter_price_max: float|int or None,
  filter_property_type: str or None             | None                                                      |
| /property/<int:property_id>    | GET         | property_details        | property_details.html      | property: dict,
  agent: dict,
  is_favorite: bool                    | None                                                      |
| /inquiry                      | GET         | inquiry_page            | inquiry.html               | properties: list (of dict)                            | None                                                      |
| /inquiry                      | POST        | submit_inquiry          | Redirects or same inquiry.html on error | inquiry_name: str, inquiry_email: str, inquiry_phone: str, inquiry_message: str, select_property: int (property_id) | inquiry_name, inquiry_email, inquiry_phone, inquiry_message, select_property (property_id) |
| /inquiries                    | GET         | my_inquiries            | inquiries.html             | inquiries: list (of dict), 
  status_filter: str                        | None                                                      |
| /inquiries/delete/<int:inquiry_id> | POST    | delete_inquiry          | Redirect to /inquiries    | None                                             | None                                                      |
| /favorites                   | GET         | my_favorites            | favorites.html             | favorites: list (of dict), properties: list (of dict) | None                                                      |
| /favorites/add/<int:property_id> | POST     | add_to_favorites        | Redirect to /property/<property_id> | None                                             | None                                                      |
| /favorites/remove/<int:property_id> | POST  | remove_from_favorites   | Redirect to /favorites    | None                                             | None                                                      |
| /agents                       | GET         | agents_directory        | agents.html                | agents: list (of dict), filter_name: str or None                | None                                                      |
| /locations                   | GET         | locations_page          | locations.html             | locations: list (of dict), sort_by: str or None                  | None                                                      |

---

## Section 2: HTML Templates (Frontend)

### 1. dashboard.html
- Page Title: Real Estate Dashboard
- Element IDs:
  - dashboard-page (div container)
  - featured-properties (div)
  - browse-properties-button (button)
  - my-inquiries-button (button)
  - my-favorites-button (button)
- Context Variables:
  - featured_properties (list of dict): List of featured property summaries
- Navigation Mappings:
  - browse-properties-button navigates to url_for('property_search')
  - my-inquiries-button navigates to url_for('my_inquiries')
  - my-favorites-button navigates to url_for('my_favorites')
- Forms: None

### 2. search.html
- Page Title: Property Search
- Element IDs:
  - search-page (div container)
  - location-input (input text)
  - price-range-min (input number)
  - price-range-max (input number)
  - property-type-filter (select dropdown with options: House, Apartment, Condo, Land)
  - properties-grid (div)
  - view-property-button-{property_id} (button) for each property
- Context Variables:
  - properties (list of dict): Properties matching search/filter
  - filter_location (str): current location filter value
  - filter_price_min (float|int or None): current minimum price filter
  - filter_price_max (float|int or None): current maximum price filter
  - filter_property_type (str or None): current property type filter
- Navigation Mappings:
  - view-property-button-{property_id} navigates to url_for('property_details', property_id=property_id)
- Forms:
  - Search/filter form with inputs: location-input, price-range-min, price-range-max, property-type-filter
  - Form submission via GET or button triggering request to /search

### 3. property_details.html
- Page Title: Property Details
- Element IDs:
  - property-details-page (div container)
  - property-address (h1)
  - property-price (div)
  - property-description (div)
  - property-features (div)
  - add-to-favorites-button (button)
  - submit-inquiry-button (button)
- Context Variables:
  - property (dict): Details of the property
  - agent (dict): Details of the agent for this property
  - is_favorite (bool): Whether property is in favorites
- Navigation Mappings:
  - add-to-favorites-button submits POST to url_for('add_to_favorites', property_id=property['property_id'])
  - submit-inquiry-button navigates to url_for('inquiry_page')
- Forms:
  - add-to-favorites-button is a POST form/button
  - submit-inquiry-button is a navigation button

### 4. inquiry.html
- Page Title: Submit Property Inquiry
- Element IDs:
  - inquiry-page (div container)
  - select-property (select dropdown with all properties)
  - inquiry-name (input text)
  - inquiry-email (input email)
  - inquiry-phone (input tel)
  - inquiry-message (textarea)
  - submit-inquiry-button (button)
- Context Variables:
  - properties (list of dict): Properties to select from
- Navigation Mappings:
  - Form posts to url_for('submit_inquiry')
- Forms:
  - Inquiry form with fields: select-property, inquiry-name, inquiry-email, inquiry-phone, inquiry-message
  - Submit button with id submit-inquiry-button

### 5. inquiries.html
- Page Title: My Inquiries
- Element IDs:
  - inquiries-page (div container)
  - inquiries-table (table)
  - inquiry-status-filter (select dropdown with options: All, Pending, Contacted, Resolved)
  - delete-inquiry-button-{inquiry_id} (button for each inquiry)
  - back-to-dashboard (button)
- Context Variables:
  - inquiries (list of dict): List of inquiries with details
  - status_filter (str): Current status filter value
- Navigation Mappings:
  - delete-inquiry-button-{inquiry_id} submits POST to url_for('delete_inquiry', inquiry_id=inquiry_id)
  - back-to-dashboard navigates to url_for('dashboard')
- Forms:
  - delete inquiry buttons are POST forms
  - Back to dashboard button

### 6. favorites.html
- Page Title: My Favorite Properties
- Element IDs:
  - favorites-page (div container)
  - favorites-list (div)
  - remove-from-favorites-button-{property_id} (button for each favorite property)
  - view-property-button-{property_id} (button for each favorite property)
  - back-to-dashboard (button)
- Context Variables:
  - favorites (list of dict): Favorite property entries
  - properties (list of dict): Corresponding property details
- Navigation Mappings:
  - remove-from-favorites-button-{property_id} submits POST to url_for('remove_from_favorites', property_id=property_id)
  - view-property-button-{property_id} navigates to url_for('property_details', property_id=property_id)
  - back-to-dashboard navigates to url_for('dashboard')
- Forms:
  - remove from favorites buttons are POST forms
  - Back to dashboard button

### 7. agents.html
- Page Title: Real Estate Agents
- Element IDs:
  - agents-page (div container)
  - agents-list (div)
  - agent-search (input text)
  - contact-agent-button-{agent_id} (button for each agent)
  - back-to-dashboard (button)
- Context Variables:
  - agents (list of dict): Agent details
  - filter_name (str or None): Current name filter
- Navigation Mappings:
  - contact-agent-button-{agent_id} could open contact modal or navigate elsewhere (implementation detail)
  - back-to-dashboard navigates to url_for('dashboard')
- Forms:
  - Search input form
  - Contact agent buttons (could be buttons triggering email or modal)

### 8. locations.html
- Page Title: Featured Locations
- Element IDs:
  - locations-page (div container)
  - locations-list (div)
  - view-location-button-{location_id} (button for each location)
  - location-sort (select dropdown with options: By Name, By Properties Count, By Average Price)
  - back-to-dashboard (button)
- Context Variables:
  - locations (list of dict): Location details
  - sort_by (str or None): Current sorting preference
- Navigation Mappings:
  - view-location-button-{location_id} navigates to url_for('property_search') filtered by location_id
  - back-to-dashboard navigates to url_for('dashboard')
- Forms:
  - Sort dropdown triggers sort/filter action

---

## Section 3: Data File Schemas (Backend)

### 1. data/properties.txt
- Fields (pipe-delimited):
  property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status
- Description: Contains properties listings with details including location, price, type, size, associated agent, and availability status.
- Example Rows:
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold

### 2. data/locations.txt
- Fields (pipe-delimited):
  location_id|location_name|region|average_price|property_count|description
- Description: Contains locations with metadata including average price, property count, region, and descriptions.
- Example Rows:
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area

### 3. data/inquiries.txt
- Fields (pipe-delimited):
  inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status
- Description: Stores inquiries submitted by customers regarding properties with contact info and status tracking.
- Example Rows:
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved

### 4. data/favorites.txt
- Fields (pipe-delimited):
  favorite_id|property_id|added_date
- Description: Tracks properties users have marked as favorites with the date added.
- Example Rows:
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14

### 5. data/agents.txt
- Fields (pipe-delimited):
  agent_id|agent_name|specialization|email|phone|properties_sold
- Description: Contains real estate agents' details including name, specialization, contact info, and properties sold count.
- Example Rows:
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
