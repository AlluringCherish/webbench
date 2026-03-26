/*
JavaScript functionality for OnlineLibrary web application.
Handles client-side interactivity, form validations, and dynamic behaviors.
Supports all frontend pages and enhances user experience.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Dashboard Page: No specific JS needed currently
    // Book Catalog Page
    const bookCatalogPage = document.getElementById('catalog-page');
    if (bookCatalogPage) {
        const searchInput = document.getElementById('search-input');
        const bookGrid = document.getElementById('book-grid');
        // Optional: Add instant search/filtering on input (if desired)
        // But since search is handled by form POST, no dynamic filtering here
    }
    // Book Details Page
    const bookDetailsPage = document.getElementById('book-details-page');
    if (bookDetailsPage) {
        const borrowButton = document.getElementById('borrow-button');
        const writeReviewButton = document.getElementById('write-review-button');
        // Disable borrow button if book is not available
        const bookStatusDiv = document.getElementById('book-status');
        if (bookStatusDiv && borrowButton) {
            const statusText = bookStatusDiv.textContent.trim().toLowerCase();
            if (statusText !== 'available') {
                borrowButton.disabled = true;
                borrowButton.title = 'Book is not available for borrowing';
            }
        }
    }
    // Borrow Confirmation Page
    const borrowPage = document.getElementById('borrow-page');
    if (borrowPage) {
        const confirmButton = document.getElementById('confirm-borrow-button');
        const cancelButton = document.getElementById('cancel-borrow-button');
        // Confirm borrow button click handled by form submit, no extra JS needed
        // Cancel button click handled by form submit, no extra JS needed
    }
    // My Borrowings Page
    const myBorrowsPage = document.getElementById('my-borrows-page');
    if (myBorrowsPage) {
        const filterStatus = document.getElementById('filter-status');
        if (filterStatus) {
            filterStatus.addEventListener('change', function () {
                // On filter change, reload page with filter-status query param
                const selected = filterStatus.value;
                const url = new URL(window.location.href);
                url.searchParams.set('filter-status', selected);
                window.location.href = url.toString();
            });
        }
        // Return book buttons are forms with POST, no extra JS needed
    }
    // My Reservations Page
    const reservationsPage = document.getElementById('reservations-page');
    if (reservationsPage) {
        // Cancel reservation buttons are forms with POST, no extra JS needed
    }
    // My Reviews Page
    const reviewsPage = document.getElementById('reviews-page');
    if (reviewsPage) {
        // Edit and delete review buttons are forms with POST, no extra JS needed
    }
    // Write Review Page
    const writeReviewPage = document.getElementById('write-review-page');
    if (writeReviewPage) {
        const submitButton = document.getElementById('submit-review-button');
        const ratingInput = document.getElementById('rating-input');
        const reviewText = document.getElementById('review-text');
        // Client-side validation on submit
        submitButton.addEventListener('click', function (event) {
            let valid = true;
            let messages = [];
            if (!ratingInput.value || isNaN(ratingInput.value) || ratingInput.value < 1 || ratingInput.value > 5) {
                valid = false;
                messages.push('Please select a valid rating between 1 and 5.');
            }
            if (!reviewText.value.trim()) {
                valid = false;
                messages.push('Review text cannot be empty.');
            }
            if (!valid) {
                event.preventDefault();
                alert(messages.join('\n'));
            }
        });
    }
    // User Profile Page
    const profilePage = document.getElementById('profile-page');
    if (profilePage) {
        const updateProfileButton = document.getElementById('update-profile-button');
        const emailInput = document.getElementById('profile-email');
        updateProfileButton.addEventListener('click', function (event) {
            if (!emailInput.value.trim()) {
                event.preventDefault();
                alert('Email cannot be empty.');
            }
        });
    }
    // Payment Confirmation Page
    const paymentPage = document.getElementById('payment-page');
    if (paymentPage) {
        // Confirm payment and back to profile buttons handled by form submit, no extra JS needed
    }
});