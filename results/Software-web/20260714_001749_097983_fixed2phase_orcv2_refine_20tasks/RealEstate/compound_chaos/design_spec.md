# RealEstate Web Application Design Specification

## Section 1: UI Pages and Navigation

### 1. Dashboard Page
- Page Title: Real Estate Dashboard
- Elements:
  - ID: `dashboard-page` (Div) - Main container for dashboard content.
  - ID: `featured-properties` (Div) - Shows featured property recommendations with brief details.
  - ID: `browse-properties-button` (Button) - Navigates to Property Search Page.
  - ID: `my-inquiries-button` (Button) - Navigates to My Inquiries Page.
  - ID: `my-favorites-button` (Button) - Navigates to My Favorites Page.

### 2. Property Search Page
- Page Title: Property Search
- Elements:
  - ID: `search-page` (Div) - Container for search UI and results.
  - ID: `location-input` (Input) - Text field for user to enter location/city filter.
  - ID: `price-range-min` (Input number) - Input for minimum price filter.
  - ID: `price-range-max` (Input number) - Input for maximum price filter.
  - ID: `property-type-filter` (Dropdown) - Dropdown to select property type filter; options: House, Apartment, Condo, Land.
  - ID: `properties-grid` (Div) - Grid layout presenting property cards each showing image, location, price, beds/baths.
  - ID pattern: `view-property-button-{property_id}` (Button) - On each property card, button to navigate to Property Details Page for that property.

### 3. Property Details Page
- Page Title: Property Details
- Elements:
  - ID: `property-details-page` (Div) - Container for property full details.
  - ID: `property-address` (H1) - Shows the full address of the property.
  - ID: `property-price` (Div) - Shows the price prominently.
  - ID: `property-description` (Div) - Detailed textual description.
  - ID: `property-features` (Div) - Displays beds, baths, square footage.
  - ID: `add-to-favorites-button` (Button) - Adds the current property to favorites.
  - ID: `submit-inquiry-button` (Button) - Navigates to Property Inquiry Page to submit inquiry for this property.

### 4. Property Inquiry Page
- Page Title: Submit Property Inquiry
- Elements:
  - ID: `inquiry-page` (Div) - Container for inquiry form.
  - ID: `select-property` (Dropdown) - Dropdown to select the property for inquiry.
  - ID: `inquiry-name` (Input) - Input field for customer's name.
  - ID: `inquiry-email` (Input email) - Input field for customer's email.
  - ID: `inquiry-phone` (Input tel) - Input field for customer's phone number.
  - ID: `inquiry-message` (Textarea) - Field to enter message.
  - ID: `submit-inquiry-button` (Button) - Submits inquiry and saves data.

### 5. My Inquiries Page
- Page Title: My Inquiries
- Elements:
  - ID: `inquiries-page` (Div) - Container for inquiries list.
  - ID: `inquiries-table` (Table) - Displays list of inquiries showing property, date, status, contact info.
  - ID: `inquiry-status-filter` (Dropdown) - Allows filtering inquiries by status: All, Pending, Contacted, Resolved.
  - ID pattern: `delete-inquiry-button-{inquiry_id}` (Button) - Button to delete a specific inquiry.
  - ID: `back-to-dashboard` (Button) - Returns to Dashboard Page.

### 6. My Favorites Page
- Page Title: My Favorite Properties
- Elements:
  - ID: `favorites-page` (Div) - Container for favorite properties.
  - ID: `favorites-list` (Div) - Displays all favorite properties with address, price.
  - ID pattern: `remove-from-favorites-button-{property_id}` (Button) - Removes property from favorites.
  - ID pattern: `view-property-button-{property_id}` (Button) - Navigates to Property Details Page for the favorite property.
  - ID: `back-to-dashboard` (Button) - Returns to Dashboard Page.

### 7. Agent Directory Page
- Page Title: Real Estate Agents
- Elements:
  - ID: `agents-page` (Div) - Container for the agents list.
  - ID: `agents-list` (Div) - Displays agents with photo, name, specialization, contacts.
  - ID: `agent-search` (Input) - Input for searching agents by name.
  - ID pattern: `contact-agent-button-{agent_id}` (Button) - Button to contact the agent by opening an email link.
  - ID: `back-to-dashboard` (Button) - Returns to Dashboard Page.

### 8. Locations Page
- Page Title: Featured Locations
- Elements:
  - ID: `locations-page` (Div) - Container for locations listings.
  - ID: `locations-list` (Div) - Lists locations with name, property count, average price.
  - ID pattern: `view-location-button-{location_id}` (Button) - Views properties listed in that location.
  - ID: `location-sort` (Dropdown) - Sort locations by Name, Properties Count, Average Price.
  - ID: `back-to-dashboard` (Button) - Returns to Dashboard Page.


## Navigation Flows
- Dashboard buttons navigate to corresponding pages: Browse Properties -> Property Search, My Inquiries -> My Inquiries, My Favorites -> My Favorites.
- Property Search's property cards' `view-property-button-{property_id}` leads to Property Details Page.
- From Property Details Page, `submit-inquiry-button` navigates to Property Inquiry Page with selected property set.
- On inquiry submission via `submit-inquiry-button` on Inquiry Page, user is redirected to Dashboard Page after optional confirmation.
- My Inquiries and My Favorites pages have back buttons returning to Dashboard.
- Agent Directory and Locations Pages have back buttons returning to Dashboard.
- Favorites page's `view-property-button-{property_id}` and remove buttons allow property details viewing and favorite management.


## Section 2: User Interaction and Functionality

### Search and Filter
- Location input filters property list by location substring.
- Price range inputs filter by minimum and maximum price inclusive.
- Property type dropdown filters property type.
- Search filters dynamically update `properties-grid` contents.

### Property Details
- Selecting a property shows complete details with address, price, description, features.
- `add-to-favorites-button` appends property to favorites.txt if not already present.
- `submit-inquiry-button` leads to inquiry page with property pre-selected.

### Inquiry Submission
- User selects property from dropdown or it is pre-set.
- User fills name, email, phone, message, then submits.
- Submission creates new inquiry record in inquiries.txt with status 'Pending' and current date.
- After submission, user is redirected to Dashboard Page.

### Managing Inquiries
- My Inquiries page shows all inquiries.
- `inquiry-status-filter` filters inquiries by their status.
- `delete-inquiry-button-{inquiry_id}` removes inquiry entry from inquiries.txt.

### Managing Favorites
- My Favorites page lists favorites.
- `remove-from-favorites-button-{property_id}` removes property from favorites.txt.
- `view-property-button-{property_id}` navigates to Property Details page for the favorite property.

### Agents Interaction
- Agent Search input filters agents-list by name substring match.
- `contact-agent-button-{agent_id}` opens the user's default email client with the agent's email address.

### Locations Interaction
- `location-sort` dropdown sorts locations-list by selected criterion.
- `view-location-button-{location_id}` filters or navigates to a list of properties for that location.


## Section 3: Data Storage Model

All data is stored in the "data" directory in text files with pipe `|` separated fields.

### 1. Properties Data
- File: `properties.txt`
- Fields:
  - property_id
  - address
  - location
  - price (numeric)
  - property_type (House, Apartment, Condo, Land)
  - bedrooms (numeric)
  - bathrooms (numeric)
  - square_feet (numeric)
  - description
  - agent_id
  - status (Available, Sold, etc.)
- Example:
  ```
  1|123 Oak Street|Downtown|450000|House|3|2|2500|Beautiful family home with large yard|101|Available
  2|456 Park Avenue|Midtown|350000|Apartment|2|1.5|1200|Modern apartment with city view|102|Available
  3|789 Elm Road|Suburb|280000|Condo|2|2|1500|Cozy condo in quiet neighborhood|101|Sold
  ```

### 2. Locations Data
- File: `locations.txt`
- Fields:
  - location_id
  - location_name
  - region
  - average_price (numeric)
  - property_count (numeric)
  - description
- Example:
  ```
  1|Downtown|Central|425000|45|Urban area with business district
  2|Midtown|Central|380000|38|Mixed residential and commercial zone
  3|Suburb|Outskirts|295000|52|Family-friendly residential area
  ```

### 3. Property Inquiries Data
- File: `inquiries.txt`
- Fields:
  - inquiry_id
  - property_id
  - customer_name
  - customer_email
  - customer_phone
  - message
  - inquiry_date (YYYY-MM-DD)
  - status (Pending, Contacted, Resolved)
- Example:
  ```
  1|1|John Smith|john@email.com|555-1234|Interested in viewing this weekend|2025-01-15|Pending
  2|2|Sarah Johnson|sarah@email.com|555-5678|Can we schedule a showing?|2025-01-16|Contacted
  3|1|Mike Davis|mike@email.com|555-9012|What is the lowest offer?|2025-01-17|Resolved
  ```

### 4. Favorite Properties Data
- File: `favorites.txt`
- Fields:
  - favorite_id
  - property_id
  - added_date (YYYY-MM-DD)
- Example:
  ```
  1|1|2025-01-10
  2|2|2025-01-12
  3|3|2025-01-14
  ```

### 5. Real Estate Agents Data
- File: `agents.txt`
- Fields:
  - agent_id
  - agent_name
  - specialization
  - email
  - phone
  - properties_sold (numeric)
- Example:
  ```
  101|Robert Wilson|Residential Properties|robert@email.com|555-0001|125
  102|Emily Chen|Commercial Real Estate|emily@email.com|555-0002|89
  103|James Martinez|Luxury Homes|james@email.com|555-0003|67
  ```


---
This design specification fully describes the UI, navigation, user interaction, and data storage model for the RealEstate web application as required.
