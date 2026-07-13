# RealEstate Web Application Design Specification

## Section 1: UI Pages and Navigation

### 1. Dashboard Page
- **Page Title**: Real Estate Dashboard
- **Element IDs:**
  - `dashboard-page`: Div container for the dashboard page.
  - `featured-properties`: Div to display featured property recommendations.
  - `browse-properties-button`: Button to navigate to Property Search page.
  - `my-inquiries-button`: Button to navigate to My Inquiries page.
  - `my-favorites-button`: Button to navigate to My Favorites page.

**Navigation:**
- Clicking `browse-properties-button` takes user to Property Search page.
- Clicking `my-inquiries-button` takes user to My Inquiries page.
- Clicking `my-favorites-button` takes user to My Favorites page.

### 2. Property Search Page
- **Page Title**: Property Search
- **Element IDs:**
  - `search-page`: Div container for the search page.
  - `location-input`: Input field to enter location or city for filtering properties.
  - `price-range-min`: Number input field to set minimum price filter.
  - `price-range-max`: Number input field to set maximum price filter.
  - `property-type-filter`: Dropdown to select property type filter (House, Apartment, Condo, Land).
  - `properties-grid`: Div to display property cards.
  - `view-property-button-{property_id}`: Button on each property card to view detailed property page.

**Navigation and Interactions:**
- User can input location, min price, max price, and select property type to filter displayed properties dynamically in `properties-grid`.
- Clicking `view-property-button-{property_id}` navigates to Property Details page of the selected property.

### 3. Property Details Page
- **Page Title**: Property Details
- **Element IDs:**
  - `property-details-page`: Div container.
  - `property-address`: H1 element displaying the property address.
  - `property-price`: Div displaying price.
  - `property-description`: Div with detailed description.
  - `property-features`: Div showing beds, baths, square footage.
  - `add-to-favorites-button`: Button to add this property to favorites list.
  - `submit-inquiry-button`: Button to navigate to Submit Property Inquiry page for this property.

**Interactions:**
- `add-to-favorites-button` adds the property id to `favorites.txt` data.
- `submit-inquiry-button` navigates to Property Inquiry page with property selected.

### 4. Property Inquiry Page
- **Page Title**: Submit Property Inquiry
- **Element IDs:**
  - `inquiry-page`: Div container.
  - `select-property`: Dropdown to select property for inquiry.
  - `inquiry-name`: Input for customer's name.
  - `inquiry-email`: Email input for customer email.
  - `inquiry-phone`: Tel input for phone number.
  - `inquiry-message`: Textarea for inquiry message.
  - `submit-inquiry-button`: Button to submit inquiry.

**Functionality:**
- User selects a property, fills contact info and message, submits.
- Submission appends new inquiry to `inquiries.txt` with status set to "Pending" and current date.

### 5. My Inquiries Page
- **Page Title**: My Inquiries
- **Element IDs:**
  - `inquiries-page`: Div container.
  - `inquiries-table`: Table displaying inquiries.
  - `inquiry-status-filter`: Dropdown to filter inquiries by status: All, Pending, Contacted, Resolved.
  - `delete-inquiry-button-{inquiry_id}`: Button to delete a specific inquiry.
  - `back-to-dashboard`: Button to navigate back to Dashboard page.

**Interactions:**
- Filtering updates the table display.
- Delete button removes inquiry entry from `inquiries.txt`.
- `back-to-dashboard` navigates to Dashboard.

### 6. My Favorites Page
- **Page Title**: My Favorite Properties
- **Element IDs:**
  - `favorites-page`: Div container.
  - `favorites-list`: Div listing all favorite properties.
  - `remove-from-favorites-button-{property_id}`: Button to remove property from favorites.
  - `view-property-button-{property_id}`: Button to go to Property Details page.
  - `back-to-dashboard`: Button to navigate back to Dashboard.

**Interactions:**
- Removing favorites updates `favorites.txt` by deleting corresponding favorite entry.
- View button navigates to Property Details page.
- Back to dashboard returns to Dashboard.

### 7. Agent Directory Page
- **Page Title**: Real Estate Agents
- **Element IDs:**
  - `agents-page`: Div container.
  - `agents-list`: Div listing all agents with photo and info.
  - `agent-search`: Input field to search agents by name.
  - `contact-agent-button-{agent_id}`: Button to contact a particular agent.
  - `back-to-dashboard`: Button to return to Dashboard.

**Interactions:**
- Agent search filters the agent list dynamically.
- Contact button can open a mailto or contact form.
- Back button returns to Dashboard.

### 8. Locations Page
- **Page Title**: Featured Locations
- **Element IDs:**
  - `locations-page`: Div container.
  - `locations-list`: Div showing popular locations.
  - `view-location-button-{location_id}`: Button to show properties in selected location.
  - `location-sort`: Dropdown to sort locations by Name, Property Count, or Average Price.
  - `back-to-dashboard`: Button to navigate back to Dashboard.

**Interactions:**
- Sorting option updates location listing order.
- View location button loads filtered property list by location.
- Back to dashboard returns to Dashboard.


## Section 2: User Interaction and Functionality

- **Search and Filter Properties:** On Property Search page, users enter location, minimum and maximum price, select property type. The results in `properties-grid` update live.
- **View Property Details:** Users can open a single property detail page via buttons from search results or favorites.
- **Submit Inquiries:** From Property Details or Inquiry page, users fill inquiry forms and submit. Data stored in `inquiries.txt` with status default "Pending".
- **Manage Favorites:** Add from Property Details, remove from Favorites page. Favorites tracked in `favorites.txt`.
- **View and Delete Inquiries:** Users view all inquiries on My Inquiries page; filter by status; can delete inquiries.
- **Contact Agents:** Search agents and use contact buttons.
- **Browse Locations:** View locations with counts and average prices; sort and navigate to property listings by location.
- **Navigation:** All pages have navigation buttons as specified to move between pages or back to Dashboard.


## Section 3: Data Storage Model

All data files are stored in the `data` directory.

### 1. Properties Data
- **File:** `properties.txt`
- **Format:** `property_id|address|location|price|property_type|bedrooms|bathrooms|square_feet|description|agent_id|status`
- **Sample:**
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

- Supports listings on Search, Favorites, Property Details pages; links to agents and locations.

### 2. Locations Data
- **File:** `locations.txt`
- **Format:** `location_id|location_name|region|average_price|property_count|description`
- **Sample:**
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

- Used in Locations page for displaying popular locations.

### 3. Property Inquiries Data
- **File:** `inquiries.txt`
- **Format:** `inquiry_id|property_id|customer_name|customer_email|customer_phone|message|inquiry_date|status`
- **Sample:**
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

- Supports inquiries listing, filtering, and status updates.

### 4. Favorite Properties Data
- **File:** `favorites.txt`
- **Format:** `favorite_id|property_id|added_date`
- **Sample:**
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

- Used to track user's favorite properties.

### 5. Real Estate Agents Data
- **File:** `agents.txt`
- **Format:** `agent_id|agent_name|specialization|email|phone|properties_sold`
- **Sample:**
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```

- Used to populate Agent Directory page and link to properties.

---

This design_spec.md fully covers all requirements specified by the user for the RealEstate application. It details the UI components, navigation flows, user interactions, and the local text file data storage models exactly as required.