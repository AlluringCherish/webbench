/*
Client-side JavaScript for PetAdoptionCenter web application.
Handles navigation button clicks and basic interactivity.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Navigation buttons that refresh or go back
    const backToDashboardButtons = document.querySelectorAll('#back-to-dashboard');
    backToDashboardButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            window.location.href = '/back_to_dashboard';
        });
    });
    const browsePetsButton = document.getElementById('browse-pets-button');
    if (browsePetsButton) {
        browsePetsButton.addEventListener('click', function (e) {
            e.preventDefault();
            window.location.href = '/pets';
        });
    }
    const backToListingsButton = document.getElementById('back-to-listings');
    if (backToListingsButton) {
        backToListingsButton.addEventListener('click', function (e) {
            e.preventDefault();
            window.location.href = '/back_to_listings';
        });
    }
    const backToPetButtons = document.querySelectorAll('[id^="back-to-pet"]');
    backToPetButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            // The button should have a data attribute with pet_id
            const petId = button.getAttribute('data-pet-id');
            if (petId) {
                window.location.href = `/back_to_pet/${petId}`;
            } else {
                window.location.href = '/pets';
            }
        });
    });
    // Search and filter on Pet Listings Page
    const searchInput = document.getElementById('search-input');
    const filterSpecies = document.getElementById('filter-species');
    if (searchInput && filterSpecies) {
        // On change or enter key, reload page with query params
        function applyFilters() {
            const search = encodeURIComponent(searchInput.value.trim());
            const species = encodeURIComponent(filterSpecies.value);
            let url = `/pets?species=${species}`;
            if (search.length > 0) {
                url += `&search=${search}`;
            }
            window.location.href = url;
        }
        searchInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                applyFilters();
            }
        });
        filterSpecies.addEventListener('change', function () {
            applyFilters();
        });
    }
    // Toggle favorite buttons (if any)
    const favoriteToggleButtons = document.querySelectorAll('.toggle-favorite-button');
    favoriteToggleButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const petId = button.getAttribute('data-pet-id');
            if (!petId) return;
            // Create a form and submit POST to toggle favorite
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/favorites/toggle/${petId}`;
            document.body.appendChild(form);
            form.submit();
        });
    });
    // Send message button on Messages Page
    const sendMessageButton = document.getElementById('send-message-button');
    if (sendMessageButton) {
        sendMessageButton.addEventListener('click', function (e) {
            e.preventDefault();
            const form = sendMessageButton.closest('form');
            if (form) {
                form.submit();
            }
        });
    }
});