/*
JavaScript file for VirtualMuseum web application.
Provides client-side interactivity including button actions and form validations.
Supports all seven pages: Dashboard, Artifact Catalog, Exhibitions, Exhibition Details,
Visitor Tickets, Virtual Events, and Audio Guides.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Visitor Tickets Page: Form validation before submission
    const visitorTicketsForm = document.querySelector('#visitor-tickets-page form');
    if (visitorTicketsForm) {
        visitorTicketsForm.addEventListener('submit', function (event) {
            // Clear previous error messages
            const errorElements = document.querySelectorAll('.form-error');
            errorElements.forEach(el => el.remove());
            let valid = true;
            // Validate ticket type
            const ticketType = document.getElementById('ticket-type');
            if (!ticketType.value) {
                showError(ticketType, 'Please select a ticket type.');
                valid = false;
            }
            // Validate number of tickets
            const numberOfTickets = document.getElementById('number-of-tickets');
            if (!numberOfTickets.value || isNaN(numberOfTickets.value) || Number(numberOfTickets.value) <= 0) {
                showError(numberOfTickets, 'Please enter a valid number of tickets.');
                valid = false;
            }
            // Validate visitor name
            const visitorName = document.getElementById('visitor-name');
            if (!visitorName.value.trim()) {
                showError(visitorName, 'Visitor name is required.');
                valid = false;
            }
            // Validate visitor email
            const visitorEmail = document.getElementById('visitor-email');
            if (!visitorEmail.value.trim()) {
                showError(visitorEmail, 'Visitor email is required.');
                valid = false;
            } else if (!validateEmail(visitorEmail.value.trim())) {
                showError(visitorEmail, 'Please enter a valid email address.');
                valid = false;
            }
            // Validate visit date
            const visitDate = document.getElementById('visit-date');
            if (!visitDate.value) {
                showError(visitDate, 'Visit date is required.');
                valid = false;
            }
            // Validate visit time
            const visitTime = document.getElementById('visit-time');
            if (!visitTime.value) {
                showError(visitTime, 'Visit time is required.');
                valid = false;
            }
            if (!valid) {
                event.preventDefault();
            }
        });
    }
    // Artifact Catalog Page: Optional enhancement - clear search input on focus
    const searchArtifactInput = document.getElementById('search-artifact');
    if (searchArtifactInput) {
        searchArtifactInput.addEventListener('focus', function () {
            // Optionally clear input or select all text
            // this.value = '';
            this.select();
        });
    }
    // Audio Guides Page: Play Guide button - could be enhanced to play actual audio files
    // Currently handled inline with alert in template, but we can add audio playback support here
    const audioGuideButtons = document.querySelectorAll('[id^="play-guide-button-"]');
    audioGuideButtons.forEach(button => {
        button.addEventListener('click', function () {
            const guideId = this.id.replace('play-guide-button-', '');
            // If audio files are available in static/audio/, play them here
            // For now, just alert handled in template, so no action needed here
            // Example for future enhancement:
            // const audio = new Audio(`/static/audio/guide_${guideId}.mp3`);
            // audio.play();
        });
    });
    // Virtual Events Page: Confirm before canceling registration
    const cancelButtons = document.querySelectorAll('[id^="cancel-registration-button-"]');
    cancelButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const confirmed = confirm('Are you sure you want to cancel your registration for this event?');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
    // Exhibitions Page: No additional JS needed currently
    // Exhibition Details Page: No additional JS needed currently
    // Dashboard Page: No additional JS needed currently
});
// Helper function to show error message next to input element
function showError(element, message) {
    const error = document.createElement('div');
    error.className = 'form-error';
    error.style.color = 'red';
    error.style.fontSize = '0.9em';
    error.textContent = message;
    element.parentNode.insertBefore(error, element.nextSibling);
}
// Helper function to validate email format
function validateEmail(email) {
    // Simple email regex pattern
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}