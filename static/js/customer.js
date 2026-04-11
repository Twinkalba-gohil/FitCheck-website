// Modal Functions
function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    document.body.style.overflow = 'auto';
}

// View Customer Details
function viewCustomer(customerId) {
    // In production, fetch customer data via AJAX
    // For now, using dummy data
    openModal('viewCustomerModal');
}

// Edit Customer
function editCustomer(customerId) {
    alert('Edit customer ID: ' + customerId);
    // Implement edit functionality
}

// Delete Customer
function deleteCustomer(customerId) {
    if (confirm('Are you sure you want to delete this customer?')) {
        window.location.href = '/admin/customer/delete/' + customerId;
    }
}

// Search Customers
// function searchCustomers() {
//     const input = document.getElementById('customerSearch');
//     const filter = input.value.toUpperCase();
//     const table = document.getElementById('customersTable');
//     const tr = table.getElementsByTagName('tr');

//     for (let i = 1; i < tr.length; i++) {
//         const tdName = tr[i].getElementsByTagName('td')[0];
//         const tdEmail = tr[i].getElementsByTagName('td')[1];
        
//         if (tdName || tdEmail) {
//             const nameValue = tdName.textContent || tdName.innerText;
//             const emailValue = tdEmail.textContent || tdEmail.innerText;
            
//             if (nameValue.toUpperCase().indexOf(filter) > -1 || 
//                 emailValue.toUpperCase().indexOf(filter) > -1) {
//                 tr[i].style.display = '';
//             } else {
//                 tr[i].style.display = 'none';
//             }
//         }
//     }
// }

// Filter Customers
function filterCustomers(type) {
    // Remove active class from all buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Add active class to clicked button
    event.target.closest('.filter-btn').classList.add('active');
    
    // Implement filtering logic
    console.log('Filtering by:', type);
}

// Close modal on escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
        document.body.style.overflow = 'auto';
    }
});


