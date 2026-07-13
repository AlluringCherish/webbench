# Frontend Design for RealEstate Web Application

---

## Section 1: Template and Page Structure

| Template Filename          | Page Title              | Main Container ID       |
|----------------------------|-------------------------|------------------------|
| templates/dashboard.html    | Real Estate Dashboard    | dashboard-page         |
| templates/property_search.html | Property Search      | search-page            |
| templates/property_details.html | Property Details     | property-details-page  |
| templates/property_inquiry.html | Submit Property Inquiry | inquiry-page           |
| templates/my_inquiries.html | My Inquiries            | inquiries-page         |
| templates/my_favorites.html | My Favorite Properties  | favorites-page         |
| templates/agent_directory.html | Real Estate Agents    | agents-page            |
| templates/locations.html    | Featured Locations      | locations-page         |

**Layout Note:**
- Each page container (main div) holds the entire page content except for common navigation which is consistent across pages.
- Navigation is primarily through buttons with clear IDs to trigger page transitions.

---

## Section 2: UI Element and ID Specifications

### 1. Dashboard Page (dashboard.html)
- **dashboard-page** (Div): Main container for the dashboard.
- **featured-properties** (Div): Showcase of featured property recommendations.
- **browse-properties-button** (Button): Navigates to Property Search page.
- **my-inquiries-button** (Button): Navigates to My Inquiries page.
- **my-favorites-button** (Button): Navigates to My Favorites page.


### 2. Property Search Page (property_search.html)
- **search-page** (Div): Main container.
- **location-input** (Input text): For searching properties by location or city.
- **price-range-min** (Input number): Minimum price filter.
- **price-range-max** (Input number): Maximum price filter.
- **property-type-filter** (Select dropdown): Filter by property type (House, Apartment, Condo, Land).
- **properties-grid** (Div): Grid containing property cards.
- **view-property-button-{property_id}** (Button): One per property card, to view detailed page of that property.


### 3. Property Details Page (property_details.html)
- **property-details-page** (Div): Main container.
- **property-address** (H1): Displays property's address.
- **property-price** (Div): Displays property price.
- **property-description** (Div): Property description text.
- **property-features** (Div): Details like beds, baths, and square footage.
- **add-to-favorites-button** (Button): Adds the property to favorites.
- **submit-inquiry-button** (Button): Navigates to Inquiry Page or triggers inquiry submission.


### 4. Property Inquiry Page (property_inquiry.html)
- **inquiry-page** (Div): Main container.
- **select-property** (Select dropdown): Select property to inquire about.
- **inquiry-name** (Input text): Customer's name.
- **inquiry-email** (Input email): Customer's email.
- **inquiry-phone** (Input tel): Customer's phone number.
- **inquiry-message** (Textarea): Message content.
- **submit-inquiry-button** (Button): Submits the inquiry form.


### 5. My Inquiries Page (my_inquiries.html)
- **inquiries-page** (Div): Main container.
- **inquiries-table** (Table): Displays all inquiries with columns: Property, Date, Status, Contact Info.
- **inquiry-status-filter** (Select dropdown): Filter inquiries by status (All, Pending, Contacted, Resolved).
- **delete-inquiry-button-{inquiry_id}** (Button): One per inquiry row, to delete inquiry.
- **back-to-dashboard** (Button): Navigates back to Dashboard page.


### 6. My Favorites Page (my_favorites.html)
- **favorites-page** (Div): Main container.
- **favorites-list** (Div): List all favorite properties with relevant data.
- **remove-from-favorites-button-{property_id}** (Button): Remove property from favorites.
- **view-property-button-{property_id}** (Button): View property details.
- **back-to-dashboard** (Button): Navigate back to Dashboard page.


### 7. Agent Directory Page (agent_directory.html)
- **agents-page** (Div): Main container.
- **agents-list** (Div): Lists agents with photo, name, specialization, contact info.
- **agent-search** (Input text): Search agents by name.
- **contact-agent-button-{agent_id}** (Button): Contact a specific agent.
- **back-to-dashboard** (Button): Navigate back to Dashboard.


### 8. Locations Page (locations.html)
- **locations-page** (Div): Main container.
- **locations-list** (Div): Lists locations with name, property count, average price.
- **view-location-button-{location_id}** (Button): View properties in specific location.
- **location-sort** (Select dropdown): Sort locations by Name, Properties Count, or Average Price.
- **back-to-dashboard** (Button): Navigate back to Dashboard.

---

## Section 3: Navigation and User Interactions

### Navigation Buttons and Page Transitions:
- From **Dashboard Page**:
  - **browse-properties-button** → Property Search Page
  - **my-inquiries-button** → My Inquiries Page
  - **my-favorites-button** → My Favorites Page

- From **Property Search Page**:
  - **view-property-button-{property_id}** → Property Details Page for selected property

- From **Property Details Page**:
  - **add-to-favorites-button** → Adds current property to favorites list dynamically
  - **submit-inquiry-button** → Opens Property Inquiry Page with the current property pre-selected in select-property dropdown

- From **Property Inquiry Page**:
  - **submit-inquiry-button** → Submits inquiry form to backend

- From **My Inquiries Page**:
  - **delete-inquiry-button-{inquiry_id}** → Deletes inquiry and updates table dynamically
  - **back-to-dashboard** → Dashboard Page

- From **My Favorites Page**:
  - **remove-from-favorites-button-{property_id}** → Removes property from favorites and updates list
  - **view-property-button-{property_id}** → Property Details Page
  - **back-to-dashboard** → Dashboard Page

- From **Agent Directory Page**:
  - **contact-agent-button-{agent_id}** → Initiates contact action (e.g., open email or contact modal)
  - **back-to-dashboard** → Dashboard Page

- From **Locations Page**:
  - **view-location-button-{location_id}** → Navigates to Property Search Page filtered by location
  - **back-to-dashboard** → Dashboard Page

### Form Elements and Submission:
- Inquiry form inputs on Property Inquiry Page:
  - **select-property:** required dropdown selection
  - **inquiry-name:** required text input
  - **inquiry-email:** required email input
  - **inquiry-phone:** optional tel input
  - **inquiry-message:** required textarea
- Submit button on Inquiry page triggers form validation and submission.

---

## Layout and UI Grouping Notes
- Frequently related UI components are grouped in container divs for easier styling and scripting.
- Buttons with dynamic IDs follow pattern with their IDs suffixed by unique entity IDs (property_id, inquiry_id, agent_id, location_id).
- Back to dashboard buttons are consistently named and placed prominently at the bottom or header in user-facing list/detail pages.
- Dropdowns and filters appear at the top or side of listing pages for intuitive access.
- Property cards in grid/list views contain view buttons referencing their specific property.

---

This detailed frontend_design.md serves as the sole guide for developing the entire frontend HTML5 structure using Flask with Jinja2 templates for the RealEstate web application.