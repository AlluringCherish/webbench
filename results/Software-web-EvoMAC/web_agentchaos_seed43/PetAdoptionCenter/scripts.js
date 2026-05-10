/*
JavaScript for PetAdoptionCenter web application.
Handles client-side interactivity including navigation buttons,
filtering, searching, and form validations.
*/
// Wait for DOM content to be loaded
document.addEventListener('DOMContentLoaded', function () {
    // Add event listeners for navigation buttons if needed
    // (Most navigation buttons use inline onclick handlers in templates)
    // Pet Listings Page: Enhance search and filter form
    const petListingsPage = document.getElementById('pet-listings-page');
    if (petListingsPage) {
        const searchInput = document.getElementById('search-input');
        const filterSpecies = document.getElementById('filter-species');
        const form = searchInput ? searchInput.closest('form') : null;
        // Optional: Add debounce for search input to auto-submit after typing
        if (searchInput && form) {
            let debounceTimeout;
            searchInput.addEventListener('input', function () {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(() => {
                    form.submit();
                }, 500);
            });
        }
        // Filter species dropdown already submits form on button click
        // No extra JS needed here
    }
    // Adoption Application Page: Validate form before submit
    const applicationPage = document.getElementById('application-page');
    if (applicationPage) {
        const form = applicationPage.querySelector('form');
        if (form) {
            form.addEventListener('submit', function (e) {
                const applicantName = form.querySelector('#applicant-name').value.trim();
                const applicantPhone = form.querySelector('#applicant-phone').value.trim();
                const housingType = form.querySelector('#housing-type').value;
                const reason = form.querySelector('#reason').value.trim();
                if (!applicantName || !applicantPhone || !housingType || !reason) {
                    e.preventDefault();
                    alert('Please fill in all required fields.');
                }
            });
        }
    }
    // Add Pet Page: Validate form before submit
    const addPetPage = document.getElementById('add-pet-page');
    if (addPetPage) {
        const form = addPetPage.querySelector('form');
        if (form) {
            form.addEventListener('submit', function (e) {
                const name = form.querySelector('#pet-name-input').value.trim();
                const species = form.querySelector('#pet-species-input').value;
                const breed = form.querySelector('#pet-breed-input').value.trim();
                const age = form.querySelector('#pet-age-input').value.trim();
                const gender = form.querySelector('#pet-gender-input').value;
                const size = form.querySelector('#pet-size-input').value;
                const description = form.querySelector('#pet-description-input').value.trim();
                if (!name || !species || !breed || !age || !gender || !size || !description) {
                    e.preventDefault();
                    alert('All fields are required.');
                }
            });
        }
    }
    // User Profile Page: Validate email format before submit
    const profilePage = document.getElementById('profile-page');
    if (profilePage) {
        const form = profilePage.querySelector('form');
        if (form) {
            form.addEventListener('submit', function (e) {
                const emailInput = form.querySelector('#profile-email');
                const email = emailInput.value.trim();
                if (!email) {
                    e.preventDefault();
                    alert('Email cannot be empty.');
                    return;
                }
                // Simple email regex validation
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(email)) {
                    e.preventDefault();
                    alert('Please enter a valid email address.');
                }
            });
        }
    }
    // Messages Page: Validate message form before submit
    const messagesPage = document.getElementById('messages-page');
    if (messagesPage) {
        const form = messagesPage.querySelector('form');
        if (form) {
            form.addEventListener('submit', function (e) {
                const recipient = form.querySelector('#recipient_username').value.trim();
                const subject = form.querySelector('#subject').value.trim();
                const message = form.querySelector('#message-input').value.trim();
                if (!recipient || !subject || !message) {
                    e.preventDefault();
                    alert('Please fill in all message fields.');
                }
            });
        }
    }
    // My Applications Page: Filter status dropdown auto-submit handled inline in template
    // Favorites Page: No special JS needed
    // Admin Panel Page: Confirmations handled inline in template for delete pet
    // Dashboard Page: Buttons use inline onclick handlers, no extra JS needed
});