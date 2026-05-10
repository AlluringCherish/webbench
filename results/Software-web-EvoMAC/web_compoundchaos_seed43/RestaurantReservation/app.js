/**
 * app.js
 * 
 * Frontend JavaScript for RestaurantReservation web application.
 * Handles client-side logic, page navigation, data fetching and submission via backend API routes,
 * event listeners, and UI updates.
 * 
 * All data interactions are done through backend API calls.
 */
const API_BASE = ''; // Base URL for API calls (same origin)
// Utility: Show only one page by id
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
    const page = document.getElementById(pageId);
    if (page) page.style.display = 'block';
}
// Utility: Format price as currency
function formatPrice(price) {
    return `$${parseFloat(price).toFixed(2)}`;
}
// Utility: Format date YYYY-MM-DD to readable
function formatDate(dateStr) {
    if (!dateStr) return '';
    const d = new Date(dateStr);
    if (isNaN(d)) return dateStr;
    return d.toLocaleDateString();
}
// Utility: Format time HH:mm to readable
function formatTime(timeStr) {
    if (!timeStr) return '';
    const [h, m] = timeStr.split(':');
    let hour = parseInt(h);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    hour = hour % 12 || 12;
    return `${hour}:${m} ${ampm}`;
}
// --- Dashboard Page ---
async function loadDashboard() {
    try {
        const res = await fetch(`${API_BASE}/api/user/current`);
        if (!res.ok) throw new Error('Failed to fetch current user');
        const user = await res.json();
        if (!user || !user.username) {
            alert('No user logged in.');
            return;
        }
        document.getElementById('welcome-message').textContent = `Welcome, ${user.full_name}`;
        showPage('dashboard-page');
    } catch (err) {
        alert('Error loading dashboard: ' + err.message);
    }
}
// --- Menu Page ---
async function loadMenu() {
    try {
        const res = await fetch(`${API_BASE}/api/menu`);
        if (!res.ok) throw new Error('Failed to fetch menu');
        const menu = await res.json();
        const menuGrid = document.getElementById('menu-grid');
        menuGrid.innerHTML = '';
        menu.forEach(dish => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <h3>${dish.name}</h3>
                <p><strong>Category:</strong> ${dish.category}</p>
                <p><strong>Price:</strong> ${formatPrice(dish.price)}</p>
                <p>${dish.description}</p>
                <button id="view-dish-button-${dish.dish_id}">View Details</button>
            `;
            menuGrid.appendChild(card);
            document.getElementById(`view-dish-button-${dish.dish_id}`).addEventListener('click', () => {
                loadDishDetails(dish.dish_id);
            });
        });
        showPage('menu-page');
    } catch (err) {
        alert('Error loading menu: ' + err.message);
    }
}
// --- Dish Details Page ---
async function loadDishDetails(dishId) {
    try {
        const res = await fetch(`${API_BASE}/api/menu/${dishId}`);
        if (!res.ok) throw new Error('Dish not found.');
        const dish = await res.json();
        document.getElementById('dish-name').textContent = dish.name;
        document.getElementById('dish-price').textContent = `Price: ${formatPrice(dish.price)}`;
        document.getElementById('dish-description').textContent = `Description: ${dish.description}`;
        document.getElementById('dish-ingredients').textContent = `Ingredients: ${dish.ingredients}`;
        document.getElementById('dish-dietary').textContent = `Dietary Info: ${dish.dietary}`;
        showPage('dish-details-page');
    } catch (err) {
        alert('Error loading dish details: ' + err.message);
    }
}
// --- Make Reservation Page ---
function loadMakeReservation() {
    document.getElementById('guest-name').value = '';
    document.getElementById('party-size').value = '';
    document.getElementById('reservation-date').value = '';
    document.getElementById('special-requests').value = '';
    showPage('reservation-page');
}
async function submitReservation(event) {
    event.preventDefault();
    const guestName = document.getElementById('guest-name').value.trim();
    const partySize = document.getElementById('party-size').value;
    const reservationDate = document.getElementById('reservation-date').value;
    const specialRequests = document.getElementById('special-requests').value.trim();
    if (!guestName || !partySize || !reservationDate) {
        alert('Please fill in guest name, party size, and reservation date.');
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/api/reservations`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                guest_name: guestName,
                party_size: parseInt(partySize),
                date: reservationDate,
                special_requests: specialRequests
            })
        });
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.message || 'Failed to submit reservation');
        }
        alert('Reservation submitted successfully.');
        loadDashboard();
    } catch (err) {
        alert('Error submitting reservation: ' + err.message);
    }
}
// --- My Reservations Page ---
async function loadMyReservations() {
    try {
        const res = await fetch(`${API_BASE}/api/reservations/my`);
        if (!res.ok) throw new Error('Failed to fetch reservations');
        const reservations = await res.json();
        const reservationsTableBody = document.querySelector('#reservations-table tbody');
        reservationsTableBody.innerHTML = '';
        if (reservations.length === 0) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.colSpan = 5;
            td.textContent = 'No reservations found.';
            tr.appendChild(td);
            reservationsTableBody.appendChild(tr);
        } else {
            reservations.forEach(r => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${formatDate(r.date)}</td>
                    <td>${formatTime(r.time)}</td>
                    <td>${r.party_size}</td>
                    <td>${r.status}</td>
                    <td></td>
                `;
                const actionTd = tr.querySelector('td:last-child');
                if (r.status.toLowerCase() === 'upcoming') {
                    const btn = document.createElement('button');
                    btn.textContent = 'Cancel';
                    btn.id = `cancel-reservation-button-${r.reservation_id}`;
                    btn.addEventListener('click', () => cancelReservation(r.reservation_id));
                    actionTd.appendChild(btn);
                } else {
                    actionTd.textContent = '-';
                }
                reservationsTableBody.appendChild(tr);
            });
        }
        showPage('my-reservations-page');
    } catch (err) {
        alert('Error loading reservations: ' + err.message);
    }
}
async function cancelReservation(reservationId) {
    if (!confirm('Are you sure you want to cancel this reservation?')) return;
    try {
        const res = await fetch(`${API_BASE}/api/reservations/${reservationId}`, {
            method: 'DELETE'
        });
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.message || 'Failed to cancel reservation');
        }
        alert('Reservation cancelled.');
        loadMyReservations();
    } catch (err) {
        alert('Error cancelling reservation: ' + err.message);
    }
}
// --- Waitlist Page ---
function loadWaitlist() {
    document.getElementById('waitlist-party-size').value = '';
    updateWaitlistPosition();
    showPage('waitlist-page');
}
async function updateWaitlistPosition() {
    try {
        const res = await fetch(`${API_BASE}/api/waitlist/my`);
        if (!res.ok) throw new Error('Failed to fetch waitlist position');
        const data = await res.json();
        const waitlistDiv = document.getElementById('user-position');
        if (!data || !data.position) {
            waitlistDiv.textContent = 'You are not currently on the waitlist.';
        } else {
            waitlistDiv.textContent = `You are on the waitlist for party size ${data.party_size}. Your position is ${data.position}. Status: ${data.status}`;
        }
    } catch (err) {
        alert('Error updating waitlist position: ' + err.message);
    }
}
async function joinWaitlist(event) {
    event.preventDefault();
    const partySize = document.getElementById('waitlist-party-size').value;
    if (!partySize) {
        alert('Please select party size.');
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/api/waitlist`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({party_size: parseInt(partySize)})
        });
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.message || 'Failed to join waitlist');
        }
        alert('You have joined the waitlist.');
        updateWaitlistPosition();
    } catch (err) {
        alert('Error joining waitlist: ' + err.message);
    }
}
// --- My Reviews Page ---
async function loadReviews() {
    try {
        const res = await fetch(`${API_BASE}/api/reviews/my`);
        if (!res.ok) throw new Error('Failed to fetch reviews');
        const reviews = await res.json();
        const reviewsList = document.getElementById('reviews-list');
        reviewsList.innerHTML = '';
        if (reviews.length === 0) {
            reviewsList.textContent = 'No reviews found.';
            showPage('reviews-page');
            return;
        }
        for (const r of reviews) {
            // Fetch dish name for each review
            let dishName = '';
            try {
                const dishRes = await fetch(`${API_BASE}/api/menu/${r.dish_id}`);
                if (dishRes.ok) {
                    const dish = await dishRes.json();
                    dishName = dish.name;
                }
            } catch {}
            const div = document.createElement('div');
            div.className = 'card';
            div.innerHTML = `
                <p><strong>Dish:</strong> ${dishName || r.dish_id}</p>
                <p><strong>Rating:</strong> ${r.rating}</p>
                <p>${r.review_text}</p>
                <p><em>${formatDate(r.review_date)}</em></p>
            `;
            reviewsList.appendChild(div);
        }
        showPage('reviews-page');
    } catch (err) {
        alert('Error loading reviews: ' + err.message);
    }
}
// --- Write Review Page ---
async function loadWriteReview() {
    try {
        const res = await fetch(`${API_BASE}/api/menu`);
        if (!res.ok) throw new Error('Failed to fetch menu');
        const menu = await res.json();
        const selectDish = document.getElementById('select-dish');
        selectDish.innerHTML = '<option value="" disabled selected>Select dish</option>';
        menu.forEach(dish => {
            const option = document.createElement('option');
            option.value = dish.dish_id;
            option.textContent = dish.name;
            selectDish.appendChild(option);
        });
        document.getElementById('rating-input').value = '';
        document.getElementById('review-text').value = '';
        showPage('write-review-page');
    } catch (err) {
        alert('Error loading write review page: ' + err.message);
    }
}
async function submitReview(event) {
    event.preventDefault();
    const dishId = document.getElementById('select-dish').value;
    const rating = document.getElementById('rating-input').value;
    const reviewText = document.getElementById('review-text').value.trim();
    if (!dishId || !rating || !reviewText) {
        alert('Please select dish, rating and write a review.');
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/api/reviews`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                dish_id: dishId,
                rating: parseInt(rating),
                review_text: reviewText
            })
        });
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.message || 'Failed to submit review');
        }
        alert('Review submitted.');
        loadReviews();
    } catch (err) {
        alert('Error submitting review: ' + err.message);
    }
}
// --- User Profile Page ---
async function loadProfile() {
    try {
        const res = await fetch(`${API_BASE}/api/user/current`);
        if (!res.ok) throw new Error('Failed to fetch user profile');
        const user = await res.json();
        if (!user || !user.username) {
            alert('No user logged in.');
            return;
        }
        document.getElementById('profile-username').textContent = `Username: ${user.username}`;
        document.getElementById('profile-email').value = user.email || '';
        showPage('profile-page');
    } catch (err) {
        alert('Error loading profile: ' + err.message);
    }
}
async function updateProfile(event) {
    event.preventDefault();
    const email = document.getElementById('profile-email').value.trim();
    if (!email) {
        alert('Email cannot be empty.');
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/api/user/profile`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email})
        });
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.message || 'Failed to update profile');
        }
        alert('Profile updated.');
        loadDashboard();
    } catch (err) {
        alert('Error updating profile: ' + err.message);
    }
}
// --- Event Listeners ---
function setupEventListeners() {
    // Dashboard buttons
    document.getElementById('make-reservation-button').addEventListener('click', loadMakeReservation);
    document.getElementById('view-menu-button').addEventListener('click', loadMenu);
    document.getElementById('back-to-dashboard').addEventListener('click', loadDashboard);
    document.getElementById('my-reservations-button').addEventListener('click', loadMyReservations);
    document.getElementById('my-reviews-button').addEventListener('click', loadReviews);
    document.getElementById('waitlist-button').addEventListener('click', loadWaitlist);
    document.getElementById('profile-button').addEventListener('click', loadProfile);
    // Menu page
    document.getElementById('back-to-dashboard').addEventListener('click', loadDashboard);
    // Dish details page
    document.getElementById('back-to-menu').addEventListener('click', loadMenu);
    // Make reservation page
    document.getElementById('reservation-form').addEventListener('submit', submitReservation);
    document.getElementById('back-to-dashboard').addEventListener('click', loadDashboard);
    // My reservations page
    document.getElementById('back-to-dashboard').addEventListener('click', loadDashboard);
    // Waitlist page
    document.getElementById('waitlist-form').addEventListener('submit', joinWaitlist);
    document.getElementById('back-to-dashboard').addEventListener('click', loadDashboard);
    // Reviews page
    document.getElementById('write-new-review-button').addEventListener('click', loadWriteReview);
    document.getElementById('back-to-dashboard').addEventListener('click', loadDashboard);
    // Write review page
    document.getElementById('write-review-form').addEventListener('submit', submitReview);
    document.getElementById('back-to-reviews').addEventListener('click', loadReviews);
    // Profile page
    document.getElementById('profile-form').addEventListener('submit', updateProfile);
    document.getElementById('back-to-dashboard').addEventListener('click', loadDashboard);
}
// --- Initialization ---
function init() {
    setupEventListeners();
    loadDashboard();
}
window.onload = init;