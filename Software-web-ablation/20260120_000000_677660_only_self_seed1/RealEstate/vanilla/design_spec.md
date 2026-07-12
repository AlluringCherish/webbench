# Design Specification for RealEstate Web Application

---

## Section 1: Flask Routes Specification (Backend)

1. **Root Redirect**
- Route Path: `/`
- HTTP Method: GET
- Function Name: `root_redirect`
- Redirects to `/dashboard`
- Route Parameters: None
- Context Variables: None
- POST Data: None

2. **Dashboard Page**
- Route Path: `/dashboard`
- HTTP Method: GET
- Function Name: `dashboard_page`
- Template Rendered: `dashboard.html`
- Route Parameters: None
- Context Variables:
  - `featured_properties` : list of dict (each dict representing a featured property)
  - `recent_listings` : list of dict (each dict representing a recent listing)
- POST Data: None

3. **Property Search Page**
- Route Path: `/properties/search`
- HTTP Methods: GET, POST
- Function Names:
  - GET: `property_search`
  - POST: `property_search_filter`
- Template Rendered: `property_search.html`
- Route Parameters: None
- Context Variables:
  - `properties` : list of dict (properties matching current search/filter)
  - `filter_options` : dict, with key `property_types` (list of str) for dropdown filter options
- POST Data (on POST route):
  - `location_input` : str (location/city search)
  - `price_range_min` : float (minimum price filter)
  - `price_range_max` : float (maximum price filter)
  - `property_type_filter` : str (property type filter; e.g. House, Apartment, Condo, Land)

4. **Property Details Page**
- Route Path: `/property/<int:property_id>`
- HTTP Method: GET
- Function Name: `property_details`
- Template Rendered: `property_details.html`
- Route Parameters:
  - `property_id` : int
- Context Variables:
  - `property` : dict (details of the property)
  - `agent` : dict (agent details associated with the property)
- POST Data: None

5. **Property Inquiry Page**
- Route Path: `/property/inquiry`
- HTTP Methods: GET, POST
- Function Names:
  - GET: `property_inquiry_form`
  - POST: `submit_property_inquiry`
- Template Rendered: `property_inquiry.html`
- Route Parameters: None
- Context Variables:
  - `properties` : list of dict (all properties for inquiry selection dropdown)
  - `submission_status` : str (only on POST, status message for submission feedback)
- POST Data (on POST route):
  - `select_property` : int (property ID selected for inquiry)
  - `inquiry_name` : str (customer name)
  - `inquiry_email` : str (customer email)
  - `inquiry_phone` : str (customer phone)
  - `inquiry_message` : str (inquiry message content)

6. **My Inquiries Page**
- Route Path: `/inquiries`
- HTTP Method: GET
- Function Name: `my_inquiries`
- Template Rendered: `my_inquiries.html`
- Route Parameters: None
- Context Variables:
  - `inquiries` : list of dict (all inquiries)
  - `status_filter_options` : list of str (e.g. All, Pending, Contacted, Resolved)
- POST Data: None

7. **Inquiries Filter POST Route**
- Route Path: `/inquiries/filter`
- HTTP Method: POST
- Function Name: `filter_inquiries`
- Template Rendered: `my_inquiries.html`
- Route Parameters: None
- Context Variables:
  - `inquiries` : list of dict (inquiries filtered by status)
  - `status_filter_options` : list of str
  - `applied_filter` : str (current filter applied)
- POST Data:
  - `inquiry_status_filter` : str (filter value)

8. **Delete Inquiry POST Route**
- Route Path: `/inquiries/delete/<int:inquiry_id>`
- HTTP Method: POST
- Function Name: `delete_inquiry`
- Template Rendered: Redirect to `/inquiries`
- Route Parameters:
  - `inquiry_id` : int
- Context Variables: None
- POST Data: None

9. **My Favorites Page**
- Route Path: `/favorites`
- HTTP Method: GET
- Function Name: `my_favorites`
- Template Rendered: `my_favorites.html`
- Route Parameters: None
- Context Variables:
  - `favorite_properties` : list of dict (favorite properties with details)
- POST Data: None

10. **Remove Favorite POST Route**
- Route Path: `/favorites/remove/<int:property_id>`
- HTTP Method: POST
- Function Name: `remove_favorite`
- Template Rendered: Redirect to `/favorites`
- Route Parameters:
  - `property_id` : int
- Context Variables: None
- POST Data: None

11. **Agent Directory Page**
- Route Path: `/agents`
- HTTP Method: GET
- Function Name: `agent_directory`
- Template Rendered: `agents.html`
- Route Parameters: None
- Context Variables:
  - `agents` : list of dict (all agents with details)
- POST Data: None

12. **Locations Page**
- Route Path: `/locations`
- HTTP Method: GET
- Function Name: `locations_page`
- Template Rendered: `locations.html`
- Route Parameters: None
- Context Variables:
  - `locations` : list of dict (all locations with details)
  - `sort_options` : list of str (sort dropdown options: By Name, By Properties Count, By Average Price)
- POST Data: None

---

## Section 2: HTML Templates (Frontend)

Each template includes the specified element IDs, page titles, accessible context variables, navigation mappings, and form specifications.

---

1. **dashboard.html**
- Page Title: "Real Estate Dashboard"
- Element IDs:
  - `dashboard-page` (Div container)
  - `featured-properties` (Div showing featured property recommendations)
  - `browse-properties-button` (Button to navigate to Property Search page)
  - `my-inquiries-button` (Button to navigate to My Inquiries page)
  - `my-favorites-button` (Button to navigate to My Favorites page)
- Context Variables:
  - `featured_properties` : list of dict (to render featured properties)
  - `recent_listings` : list of dict (optional recent listings display if implemented)
- Navigation Mappings:
  - `browse-properties-button` -> `url_for('property_search')`
  - `my-inquiries-button` -> `url_for('my_inquiries')`
  - `my-favorites-button` -> `url_for('my_favorites')`
- Forms: None

---

2. **property_search.html**
- Page Title: "Property Search"
- Element IDs:
  - `search-page` (Div container)
  - `location-input` (Input text field for location search)
  - `price-range-min` (Input number field for min price)
  - `price-range-max` (Input number field for max price)
  - `property-type-filter` (Dropdown for property type filter)
  - `properties-grid` (Div container to display property cards)
  - `view-property-button-{property_id}` (Button for each property card to view details)
- Context Variables:
  - `properties` : list of dict (filtered properties to display)
  - `filter_options.property_types` : list of str (property types for dropdown)
- Navigation Mappings:
  - Buttons `view-property-button-{property_id}` link to `url_for('property_details', property_id=property_id)`
- Forms:
  - Search/filter form with inputs: `location-input`, `price-range-min`, `price-range-max`, `property-type-filter`
  - Submit button triggers POST to `url_for('property_search_filter')`

---

3. **property_details.html**
- Page Title: "Property Details"
- Element IDs:
  - `property-details-page` (Div container)
  - `property-address` (H1 displaying the address)
  - `property-price` (Div displaying price)
  - `property-description` (Div displaying description)
  - `property-features` (Div displaying features: beds, baths, square feet)
  - `add-to-favorites-button` (Button to add the property to favorites)
  - `submit-inquiry-button` (Button to submit inquiry for this property)
- Context Variables:
  - `property` : dict (property details)
  - `agent` : dict (agent details)
- Navigation Mappings:
  - No direct navigation buttons specified, can link `add-to-favorites-button` to a POST endpoint in backend
  - `submit-inquiry-button` could link to `url_for('property_inquiry_form')`
- Forms:
  - Form to add to favorites: button `add-to-favorites-button` triggers POST to `/favorites/add` or similar (not specified exactly, so the backend should handle)
  - Form or link via `submit-inquiry-button` to inquiry page

---

4. **property_inquiry.html**
- Page Title: "Submit Property Inquiry"
- Element IDs:
  - `inquiry-page` (Div container)
  - `select-property` (Dropdown to select property)
  - `inquiry-name` (Input text for customer name)
  - `inquiry-email` (Input email for customer email)
  - `inquiry-phone` (Input tel for customer phone)
  - `inquiry-message` (Textarea for inquiry message)
  - `submit-inquiry-button` (Button to submit inquiry)
- Context Variables:
  - `properties` : list of dict (for property selection dropdown)
  - `submission_status` : str (optional, display submission result message)
- Navigation Mappings:
  - None explicitly, but can include a link back to dashboard if needed
- Forms:
  - Form with inputs named exactly as the IDs above
  - Form POSTs to `url_for('submit_property_inquiry')`

---

5. **my_inquiries.html**
- Page Title: "My Inquiries"
- Element IDs:
  - `inquiries-page` (Div container)
  - `inquiries-table` (Table showing all inquiries with columns for property, date, status, contact info)
  - `inquiry-status-filter` (Dropdown to filter inquiries by status)
  - `delete-inquiry-button-{inquiry_id}` (Button for each inquiry to delete it)
  - `back-to-dashboard` (Button to navigate back)
- Context Variables:
  - `inquiries` : list of dict
  - `status_filter_options` : list of str
- Navigation Mappings:
  - `back-to-dashboard` linked to `url_for('dashboard_page')`
- Forms:
  - Filter form using `inquiry-status-filter` dropdown POSTing to `url_for('filter_inquiries')`
  - Delete inquiry buttons POST to `/inquiries/delete/<inquiry_id>`

---

6. **my_favorites.html**
- Page Title: "My Favorite Properties"
- Element IDs:
  - `favorites-page` (Div container)
  - `favorites-list` (Div showing list of favorite properties)
  - `remove-from-favorites-button-{property_id}` (Button per property to remove favorite)
  - `view-property-button-{property_id}` (Button per property to view details)
  - `back-to-dashboard` (Button to navigate back)
- Context Variables:
  - `favorite_properties` : list of dict
- Navigation Mappings:
  - `back-to-dashboard` linked to `url_for('dashboard_page')`
  - `view-property-button-{property_id}` links to `url_for('property_details', property_id=property_id)`
- Forms:
  - Remove button POSTs to `/favorites/remove/<property_id>`

---

7. **agents.html**
- Page Title: "Real Estate Agents"
- Element IDs:
  - `agents-page` (Div container)
  - `agents-list` (Div listing all agents)
  - `agent-search` (Input for searching agents by name)
  - `contact-agent-button-{agent_id}` (Button to contact each agent)
  - `back-to-dashboard` (Button to navigate back)
- Context Variables:
  - `agents` : list of dict
- Navigation Mappings:
  - `back-to-dashboard` linked to `url_for('dashboard_page')`
- Forms:
  - Search form with input `agent-search`

---

8. **locations.html**
- Page Title: "Featured Locations"
- Element IDs:
  - `locations-page` (Div container)
  - `locations-list` (Div listing all locations)
  - `view-location-button-{location_id}` (Button to view properties in location)
  - `location-sort` (Dropdown to sort locations)
  - `back-to-dashboard` (Button to navigate back)
- Context Variables:
  - `locations` : list of dict
  - `sort_options` : list of str
- Navigation Mappings:
  - `back-to-dashboard` linked to `url_for('dashboard_page')`
- Forms:
  - Sort dropdown form submits GET or POST for sorting if applicable

---

## Section 3: Data File Schemas (Backend)

1. **properties.txt**
- File Path: `data/properties.txt`
- Fields (pipe-delimited in order):
  - property_id
  - address
  - location
  - price
  - property_type
  - bedrooms
  - bathrooms
  - square_feet
  - description
  - agent_id
  - status
- Description: Stores all property listings with detailed attributes.
- Example Rows:
  - `1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available`
  - `2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available`
  - `3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold`

2. **locations.txt**
- File Path: `data/locations.txt`
- Fields (pipe-delimited in order):
  - location_id
  - location_name
  - region
  - average_price
  - property_count
  - description
- Description: Contains popular locations with their statistics.
- Example Rows:
  - `1|Downtown|Central|425000|45|Urban area with business district`
  - `2|Midtown|Central|380000|38|Mixed residential and commercial zone`
  - `3|Suburb|Outskirts|295000|52|Family-friendly residential area`

3. **inquiries.txt**
- File Path: `data/inquiries.txt`
- Fields (pipe-delimited in order):
  - inquiry_id
  - property_id
  - customer_name
  - customer_email
  - customer_phone
  - message
  - inquiry_date
  - status
- Description: Stores inquiries submitted by customers regarding properties.
- Example Rows:
  - `1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending`
  - `2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted`
  - `3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved`

4. **favorites.txt**
- File Path: `data/favorites.txt`
- Fields (pipe-delimited in order):
  - favorite_id
  - property_id
  - added_date
- Description: Stores favorite properties added by users.
- Example Rows:
  - `1|1|2025-01-10`
  - `2|2|2025-01-12`
  - `3|3|2025-01-14`

5. **agents.txt**
- File Path: `data/agents.txt`
- Fields (pipe-delimited in order):
  - agent_id
  - agent_name
  - specialization
  - email
  - phone
  - properties_sold
- Description: Contains real estate agent information.
- Example Rows:
  - `101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125`
  - `102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89`
  - `103|James Martinez|Luxury Homes|james@email.com|555-0003|67`


---

This design specification fully enables backend and frontend teams to work independently with clear route definitions, template details, and data schemas, consistent with the user requirements provided.