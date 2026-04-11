// Products Page JavaScript

// Modal functionality
const productModal = document.getElementById('productModal');
const addProductBtn = document.getElementById('addProductBtn');
const modalTitle = document.getElementById('modalTitle');
const productForm = document.getElementById('productForm');

// Open modal for adding new product
addProductBtn?.addEventListener('click', () => {
    modalTitle.textContent = 'Add New Product';
    productForm.reset();
    productModal.classList.add('active');
});

// Close modal
function closeModal() {
    productModal.classList.remove('active');
}

// Close modal when clicking outside
productModal?.addEventListener('click', (e) => {
    if (e.target === productModal) {
        closeModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && productModal.classList.contains('active')) {
        closeModal();
    }
});

// Edit product function
function editProduct(productId) {
    modalTitle.textContent = 'Edit Product';
    productModal.classList.add('active');
    
    // Here you would fetch product data and populate the form
    console.log('Editing product:', productId);
    
    // Example: You can populate form fields here
    // productForm.querySelector('input[type="text"]').value = 'Product Name';
}

// Delete product function
function deleteProduct(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        console.log('Deleting product:', productId);
        
        // Here you would make an API call to delete the product
        // Then remove the row from the table
        
        // Show success message
        showNotification('Product deleted successfully!', 'success');
    }
}

// Form submission
productForm?.addEventListener('submit', (e) => {
    // e.preventDefault();
    
    // Get form data
    const formData = new FormData(productForm);
    
    // Here you would send the data to your backend
    console.log('Form submitted');
    
    // Show success message
    showNotification('Product saved successfully!', 'success');
    
    // Close modal
    closeModal();
});

// Search functionality
const searchInput = document.getElementById('searchProducts');
const tableBody = document.getElementById('productsTableBody');

searchInput?.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const rows = tableBody.querySelectorAll('tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
});

// Notification function
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 30px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #10B981 0%, #34D399 100%)' : 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)'};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 600;
        z-index: 3000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Pagination
const pageButtons = document.querySelectorAll('.page-btn');
pageButtons.forEach(btn => {
    btn.addEventListener('click', function() {
        if (!this.disabled) {
            pageButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Here you would load the corresponding page data
            console.log('Loading page:', this.textContent);
        }
    });
});

// Filter functionality
const filterSelects = document.querySelectorAll('.filter-select');
filterSelects.forEach(select => {
    select.addEventListener('change', (e) => {
        console.log('Filter changed:', e.target.value);
        
        // Here you would filter the table based on selected filters
        // For now, just logging
    });
});

// File upload functionality
const fileUpload = document.querySelector('.file-upload');
const fileInput = fileUpload?.querySelector('input[type="file"]');

fileUpload?.addEventListener('click', () => {
    fileInput?.click();
});

fileInput?.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        console.log('File selected:', file.name);
        fileUpload.querySelector('p').textContent = `Selected: ${file.name}`;
        
        // Here you would upload the file or show preview
    }
});

// Drag and drop for file upload
fileUpload?.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUpload.style.borderColor = 'var(--primary)';
    fileUpload.style.background = 'rgba(99, 102, 241, 0.05)';
});

fileUpload?.addEventListener('dragleave', () => {
    fileUpload.style.borderColor = '';
    fileUpload.style.background = '';
});

fileUpload?.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUpload.style.borderColor = '';
    fileUpload.style.background = '';
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        console.log('File dropped:', file.name);
        fileUpload.querySelector('p').textContent = `Selected: ${file.name}`;
    }
});

console.log('✨ Products Page Loaded!');