/*
JavaScript file for OnlineCourse web application.
Handles client-side interactivity, UI behavior, button actions, and form validations.
Supports functionality and usability of all pages as per requirements.
*/
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Dashboard Page: browse-courses-button and my-courses-button already have inline onclick handlers, no extra JS needed.
    // Course Catalog Page: Search input validation (optional enhancement)
    const catalogPage = document.getElementById('catalog-page');
    if (catalogPage) {
        const searchForm = catalogPage.querySelector('form');
        const searchInput = document.getElementById('search-input');
        if (searchForm && searchInput) {
            searchForm.addEventListener('submit', function (e) {
                if (searchInput.value.trim() === '') {
                    e.preventDefault();
                    alert('Please enter a search term.');
                    searchInput.focus();
                }
            });
        }
    }
    // Course Details Page: Enroll button confirmation
    const courseDetailsPage = document.getElementById('course-details-page');
    if (courseDetailsPage) {
        const enrollButton = document.getElementById('enroll-button');
        if (enrollButton && !enrollButton.disabled) {
            enrollButton.addEventListener('click', function (e) {
                const confirmEnroll = confirm('Are you sure you want to enroll in this course?');
                if (!confirmEnroll) {
                    e.preventDefault();
                }
            });
        }
    }
    // My Courses Page: continue-learning-button-{course_id} buttons have inline onclick handlers, no extra JS needed.
    // Course Learning Page: mark-complete-button confirmation
    const learningPage = document.getElementById('learning-page');
    if (learningPage) {
        const markCompleteButton = document.getElementById('mark-complete-button');
        if (markCompleteButton && !markCompleteButton.disabled) {
            markCompleteButton.addEventListener('click', function (e) {
                const confirmComplete = confirm('Mark this lesson as completed?');
                if (!confirmComplete) {
                    e.preventDefault();
                }
            });
        }
    }
    // My Assignments Page: submit-assignment-button-{assignment_id} buttons have inline onclick handlers, no extra JS needed.
    // Submit Assignment Page: Validate submission text is not empty before submitting
    const submitPage = document.getElementById('submit-page');
    if (submitPage) {
        const submitForm = submitPage.querySelector('form');
        const submissionText = document.getElementById('submission-text');
        if (submitForm && submissionText) {
            submitForm.addEventListener('submit', function (e) {
                if (submissionText.value.trim() === '') {
                    e.preventDefault();
                    alert('Submission text cannot be empty.');
                    submissionText.focus();
                }
            });
        }
    }
    // Certificates Page: back-to-dashboard button has inline onclick handler, no extra JS needed.
    // User Profile Page: Validate email and fullname before submitting
    const profilePage = document.getElementById('profile-page');
    if (profilePage) {
        const profileForm = profilePage.querySelector('form');
        const emailInput = document.getElementById('profile-email');
        const fullnameInput = document.getElementById('profile-fullname');
        if (profileForm && emailInput && fullnameInput) {
            profileForm.addEventListener('submit', function (e) {
                const email = emailInput.value.trim();
                const fullname = fullnameInput.value.trim();
                if (email === '' || fullname === '') {
                    e.preventDefault();
                    alert('Email and Full name cannot be empty.');
                    if (email === '') {
                        emailInput.focus();
                    } else {
                        fullnameInput.focus();
                    }
                    return;
                }
                // Basic email format validation
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(email)) {
                    e.preventDefault();
                    alert('Please enter a valid email address.');
                    emailInput.focus();
                }
            });
        }
    }
});