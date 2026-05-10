/*
JavaScript for PetAdoptionCenter client-side interactivity.
Includes navigation button handling and form validation.
*/
// Navigation button handlers can be added here if needed.
// Currently, navigation is handled inline via onclick attributes in HTML.
// Example form validation for Add Pet form
document.addEventListener('DOMContentLoaded', function () {
    const addPetForm = document.querySelector('#add-pet-page form');
    if (addPetForm) {
        addPetForm.addEventListener('submit', function (e) {
            const name = document.getElementById('pet-name-input').value.trim();
            const species = document.getElementById('pet-species-input').value;
            const breed = document.getElementById('pet-breed-input').value.trim();
            const age = document.getElementById('pet-age-input').value.trim();
            const gender = document.getElementById('pet-gender-input').value;
            const size = document.getElementById('pet-size-input').value;
            const description = document.getElementById('pet-description-input').value.trim();
            if (!name || !species || !breed || !age || !gender || !size || !description) {
                alert('Please fill in all required fields.');
                e.preventDefault();
            }
        });
    }
    // Example form validation for Adoption Application form
    const adoptionForm = document.querySelector('#application-page form');
    if (adoptionForm) {
        adoptionForm.addEventListener('submit', function (e) {
            const applicantName = document.getElementById('applicant-name').value.trim();
            const applicantPhone = document.getElementById('applicant-phone').value.trim();
            const housingType = document.getElementById('housing-type').value;
            const reason = document.getElementById('reason').value.trim();
            if (!applicantName || !applicantPhone || !housingType || !reason) {
                alert('Please fill in all required fields.');
                e.preventDefault();
            }
        });
    }
    // Example form validation for User Profile form
    const profileForm = document.querySelector('#profile-page form');
    if (profileForm) {
        profileForm.addEventListener('submit', function (e) {
            const email = document.getElementById('profile-email').value.trim();
            if (!email) {
                alert('Email cannot be empty.');
                e.preventDefault();
            } else {
                // Basic email format check
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(email)) {
                    alert('Please enter a valid email address.');
                    e.preventDefault();
                }
            }
        });
    }
    // Example form validation for Messages form
    const messagesForm = document.querySelector('#messages-page form');
    if (messagesForm) {
        messagesForm.addEventListener('submit', function (e) {
            const recipient = document.getElementById('recipient_username').value.trim();
            const subject = document.getElementById('subject').value.trim();
            const message = document.getElementById('message-input').value.trim();
            if (!recipient || !subject || !message) {
                alert('Please fill in all message fields.');
                e.preventDefault();
            }
        });
    }
});