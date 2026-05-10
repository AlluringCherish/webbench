/*
JavaScript for PetAdoptionCenter web application.
Handles interactivity such as button actions, filtering, searching, and dynamic content updates.
*/
// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', function () {
    // Dashboard page buttons
    const browsePetsButton = document.getElementById('browse-pets-button');
    if (browsePetsButton) {
        browsePetsButton.addEventListener('click', function () {
            window.location.href = '/pets';
        });
    }
    const backToDashboardButtons = document.querySelectorAll('#back-to-dashboard');
    backToDashboardButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            window.location.href = '/';
        });
    });
    // Pet Listings Page: filtering and searching
    const petListingsPage = document.getElementById('pet-listings-page');
    if (petListingsPage) {
        const searchInput = document.getElementById('search-input');
        const filterSpecies = document.getElementById('filter-species');
        function updatePetListings() {
            const searchValue = searchInput.value.trim();
            const speciesValue = filterSpecies.value;
            // Build query string and reload page with parameters
            const params = new URLSearchParams();
            if (speciesValue && speciesValue !== 'All') {
                params.append('species', speciesValue);
            }
            if (searchValue) {
                params.append('search', searchValue);
            }
            window.location.href = '/pets?' + params.toString();
        }
        if (searchInput) {
            searchInput.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    updatePetListings();
                }
            });
        }
        if (filterSpecies) {
            filterSpecies.addEventListener('change', function () {
                updatePetListings();
            });
        }
        // Back to dashboard button
        const backToDashboardBtn = document.getElementById('back-to-dashboard');
        if (backToDashboardBtn) {
            backToDashboardBtn.addEventListener('click', function () {
                window.location.href = '/';
            });
        }
    }
    // Pet Details Page buttons
    const petDetailsPage = document.getElementById('pet-details-page');
    if (petDetailsPage) {
        const adoptButton = document.getElementById('adopt-button');
        if (adoptButton) {
            adoptButton.addEventListener('click', function () {
                const petId = adoptButton.getAttribute('data-pet-id');
                if (petId) {
                    window.location.href = '/adopt/' + petId;
                }
            });
        }
        const backToListingsBtn = document.getElementById('back-to-listings');
        if (backToListingsBtn) {
            backToListingsBtn.addEventListener('click', function () {
                window.location.href = '/pets';
            });
        }
    }
    // Add Pet Page buttons
    const addPetPage = document.getElementById('add-pet-page');
    if (addPetPage) {
        const backToDashboardBtn = document.getElementById('back-to-dashboard');
        if (backToDashboardBtn) {
            backToDashboardBtn.addEventListener('click', function () {
                window.location.href = '/';
            });
        }
    }
    // Adoption Application Page buttons
    const applicationPage = document.getElementById('application-page');
    if (applicationPage) {
        const backToPetBtn = document.getElementById('back-to-pet');
        if (backToPetBtn) {
            backToPetBtn.addEventListener('click', function () {
                const petId = backToPetBtn.getAttribute('data-pet-id');
                if (petId) {
                    window.location.href = '/pet/' + petId;
                }
            });
        }
    }
    // My Applications Page buttons and filter
    const myApplicationsPage = document.getElementById('my-applications-page');
    if (myApplicationsPage) {
        const filterStatus = document.getElementById('filter-status');
        if (filterStatus) {
            filterStatus.addEventListener('change', function () {
                const status = filterStatus.value;
                const params = new URLSearchParams();
                if (status && status !== 'All') {
                    params.append('status', status);
                }
                window.location.href = '/my_applications?' + params.toString();
            });
        }
        const backToDashboardBtn = document.getElementById('back-to-dashboard');
        if (backToDashboardBtn) {
            backToDashboardBtn.addEventListener('click', function () {
                window.location.href = '/';
            });
        }
    }
    // Favorites Page buttons
    const favoritesPage = document.getElementById('favorites-page');
    if (favoritesPage) {
        const backToDashboardBtn = document.getElementById('back-to-dashboard');
        if (backToDashboardBtn) {
            backToDashboardBtn.addEventListener('click', function () {
                window.location.href = '/';
            });
        }
        // Add event listeners for remove favorite buttons (if any)
        const removeFavButtons = favoritesPage.querySelectorAll('.remove-favorite-button');
        removeFavButtons.forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                const petId = btn.getAttribute('data-pet-id');
                if (!petId) return;
                // Send POST request to remove favorite
                fetch('/favorites/remove/' + petId, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                }).then(response => {
                    if (response.ok) {
                        // Reload page after removal
                        window.location.reload();
                    } else {
                        alert('Failed to remove favorite.');
                    }
                });
            });
        });
    }
    // Messages Page
    const messagesPage = document.getElementById('messages-page');
    if (messagesPage) {
        const backToDashboardBtn = document.getElementById('back-to-dashboard');
        if (backToDashboardBtn) {
            backToDashboardBtn.addEventListener('click', function () {
                window.location.href = '/';
            });
        }
        // Handle sending message form submission
        const sendMessageButton = document.getElementById('send-message-button');
        if (sendMessageButton) {
            sendMessageButton.addEventListener('click', function () {
                const recipientInput = document.getElementById('recipient-username');
                const subjectInput = document.getElementById('subject');
                const messageInput = document.getElementById('message-input');
                if (!recipientInput || !subjectInput || !messageInput) {
                    alert('Message form fields missing.');
                    return;
                }
                if (!recipientInput.value.trim() || !subjectInput.value.trim() || !messageInput.value.trim()) {
                    alert('Please fill all message fields.');
                    return;
                }
                // Submit the form
                document.getElementById('message-form').submit();
            });
        }
        // Mark messages as read on click
        const conversationList = document.getElementById('conversation-list');
        if (conversationList) {
            conversationList.addEventListener('click', function (e) {
                const target = e.target;
                if (target.classList.contains('message-item') && target.dataset.messageId) {
                    const messageId = target.dataset.messageId;
                    // Send POST request to mark message as read
                    fetch('/messages/mark_read/' + messageId, {
                        method: 'POST',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    }).then(response => {
                        if (response.ok) {
                            target.classList.remove('unread');
                        }
                    });
                }
            });
        }
    }
    // User Profile Page
    const profilePage = document.getElementById('profile-page');
    if (profilePage) {
        const backToDashboardBtn = document.getElementById('back-to-dashboard');
        if (backToDashboardBtn) {
            backToDashboardBtn.addEventListener('click', function () {
                window.location.href = '/';
            });
        }
        const updateProfileButton = document.getElementById('update-profile-button');
        if (updateProfileButton) {
            updateProfileButton.addEventListener('click', function () {
                const emailInput = document.getElementById('profile-email');
                if (!emailInput.value.trim()) {
                    alert('Email cannot be empty.');
                    return;
                }
                document.getElementById('profile-form').submit();
            });
        }
    }
    // Admin Panel Page
    const adminPanelPage = document.getElementById('admin-panel-page');
    if (adminPanelPage) {
        const backToDashboardBtn = document.getElementById('back-to-dashboard');
        if (backToDashboardBtn) {
            backToDashboardBtn.addEventListener('click', function () {
                window.location.href = '/';
            });
        }
        // Handle application status update buttons
        const statusUpdateForms = adminPanelPage.querySelectorAll('.application-status-form');
        statusUpdateForms.forEach(function (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                const formData = new FormData(form);
                fetch('/admin', {
                    method: 'POST',
                    body: formData
                }).then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert('Failed to update application status.');
                    }
                });
            });
        });
        // Handle pet delete buttons
        const deletePetForms = adminPanelPage.querySelectorAll('.delete-pet-form');
        deletePetForms.forEach(function (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                if (!confirm('Are you sure you want to delete this pet?')) {
                    return;
                }
                const formData = new FormData(form);
                fetch('/admin', {
                    method: 'POST',
                    body: formData
                }).then(response => {
                    if (response.ok) {
                        window.location.reload();
                    } else {
                        alert('Failed to delete pet.');
                    }
                });
            });
        });
        // Edit pet buttons currently not implemented, so no JS needed
    }
});