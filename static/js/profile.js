// ========================================
// PROFILE.JS - FitCheck Profile Page
// Fixed to use Database API
// ========================================
 
// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', function() {
    updateDatabaseCounts(); // Changed from localStorage to database
    setupPasswordValidation();
});
 
// ========== TAB SWITCHING ==========
function showTab(tabName) {
    // Remove active class from all nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Add active class to clicked nav item
    event.preventDefault();
    event.currentTarget.classList.add('active');
}
 
// ========== UPDATE DATABASE COUNTS (FIXED) ==========
function updateDatabaseCounts() {
    // Update wishlist count from database
    fetch('/api/wishlist')
        .then(res => res.json())
        .then(wishlist => {
            const wishlistCount = document.getElementById('wishlistCount');
            if (wishlistCount) {
                wishlistCount.textContent = wishlist.length;
            }
        })
        .catch(error => {
            console.error('Error fetching wishlist:', error);
            const wishlistCount = document.getElementById('wishlistCount');
            if (wishlistCount) {
                wishlistCount.textContent = '0';
            }
        });
    
    // Update cart count from database
    fetch('/api/cart')
        .then(res => res.json())
        .then(cart => {
            const cartCount = document.getElementById('cartCount');
            if (cartCount) {
                // Calculate total items (sum of quantities)
                const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
                cartCount.textContent = totalItems;
            }
        })
        .catch(error => {
            console.error('Error fetching cart:', error);
            const cartCount = document.getElementById('cartCount');
            if (cartCount) {
                cartCount.textContent = '0';
            }
        });
}
 
// ========== EDIT PROFILE ==========
function toggleEdit() {
    const form = document.getElementById('profileForm');
    const inputs = form.querySelectorAll('input');
    const formActions = document.querySelector('.form-actions');
    const editBtn = document.querySelector('.btn-edit');
    
    // Enable all inputs except username and email
    inputs.forEach(input => {
        if (input.name !== 'username' && input.name !== 'email') {
            input.disabled = false;
        }
    });
    
    // Show form actions
    formActions.style.display = 'flex';
    
    // Hide edit button
    editBtn.style.display = 'none';
}
 
function cancelEdit() {
    const form = document.getElementById('profileForm');
    const inputs = form.querySelectorAll('input');
    const formActions = document.querySelector('.form-actions');
    const editBtn = document.querySelector('.btn-edit');
    
    // Disable all inputs
    inputs.forEach(input => {
        input.disabled = true;
    });
    
    // Hide form actions
    formActions.style.display = 'none';
    
    // Show edit button
    editBtn.style.display = 'flex';
    
    // Reset form to original values
    form.reset();
}
 
// ========== PASSWORD VALIDATION ==========
function setupPasswordValidation() {
    const passwordForm = document.getElementById('passwordForm');
    
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const currentPassword = document.querySelector('input[name="current_password"]').value;
            const newPassword = document.querySelector('input[name="new_password"]').value;
            const confirmPassword = document.querySelector('input[name="confirm_password"]').value;
            
            // Validate passwords match
            if (newPassword !== confirmPassword) {
                showMessage('Passwords do not match', 'error');
                return;
            }
            
            // Validate password length
            if (newPassword.length < 6) {
                showMessage('Password must be at least 6 characters', 'error');
                return;
            }
            
            // Submit form
            this.submit();
        });
    }
}
 
// ========== SHOW MESSAGE TOAST ==========
function showMessage(message, type = 'success') {
    const toast = document.getElementById('messageToast');
    const messageText = document.getElementById('messageText');
    
    if (toast && messageText) {
        messageText.textContent = message;
        toast.classList.remove('error');
        
        if (type === 'error') {
            toast.classList.add('error');
        }
        
        toast.classList.add('show');
        
        // Hide after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}
 
// ========== CONTACT NUMBER VALIDATION ==========
document.addEventListener('DOMContentLoaded', function() {
    const contactInput = document.querySelector('input[name="contact"]');
    if (contactInput) {
        contactInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }
    
    const pincodeInput = document.querySelector('input[name="pincode"]');
    if (pincodeInput) {
        pincodeInput.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }
});


document.getElementById("stateSelect").addEventListener("change", function () {
    const stateId = this.value;

    fetch(`/get-cities/${stateId}`)
        .then(response => response.json())
        .then(data => {
            const citySelect = document.getElementById("citySelect");

            // Clear old cities
            citySelect.innerHTML = '<option value="">Select City</option>';

            // Add new cities
            data.forEach(city => {
                const option = document.createElement("option");
                option.value = city.city_id;
                option.textContent = city.city_name;
                citySelect.appendChild(option);
            });
        })
        .catch(error => console.error("Error:", error));
});


function cancelOrder(orderId) {
    if (!confirm('Are you sure you want to cancel this order?')) {
        return;
    }

    fetch(`/api/order/${orderId}/cancel`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert('Order cancelled successfully');
            location.reload(); // refresh page
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to cancel order');
    });
}
