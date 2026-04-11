// ========================================
// TAB SWITCHING
// ========================================
function showTab(tabName, btn) {
    const tabs = document.querySelectorAll(".tab-content");
    const buttons = document.querySelectorAll(".tab-btn");

    tabs.forEach(tab => tab.classList.remove("active"));
    buttons.forEach(button => button.classList.remove("active"));

    document.getElementById(tabName + "-tab").classList.add("active");

    if (btn) {
        btn.classList.add("active");
    }
}

// ========================================
// MODAL FUNCTIONS
// ========================================
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// ========================================
// EDIT CATEGORY
// ========================================
function editCategory(categoryId) {
    // Fetch category details
    fetch(`/admin/api/category/${categoryId}`)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // Populate form
                document.getElementById('edit_cat_id').value = data.category.cat_id;
                document.getElementById('edit_cat_name').value = data.category.cat_name;
                
                // Open modal
                openModal('editCategoryModal');
            } else {
                showNotification('Error loading category', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Failed to load category', 'error');
        });
}

function submitEditCategory(event) {
    event.preventDefault();
    
    const catId = document.getElementById('edit_cat_id').value;
    const catName = document.getElementById('edit_cat_name').value;
    
    fetch(`/admin/category/edit/${catId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cat_name: catName })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            closeModal('editCategoryModal');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to update category', 'error');
    });
}

// ========================================
// DELETE CATEGORY
// ========================================
function deleteCategory(categoryId) {
    if (!confirm("Are you sure you want to delete this category?")) {
        return;
    }

    fetch(`/admin/category/delete/${categoryId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to delete category', 'error');
    });
}

// ========================================
// EDIT SUBCATEGORY
// ========================================
function editSubcategory(subcatId) {
    // Fetch subcategory details
    fetch(`/admin/api/subcategory/${subcatId}`)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // Populate form
                document.getElementById('edit_subcat_id').value = data.subcategory.subcat_id;
                document.getElementById('edit_subcat_name').value = data.subcategory.subcat_name;
                document.getElementById('edit_subcat_cat_id').value = data.subcategory.cat_id;
                
                // Open modal
                openModal('editSubcategoryModal');
            } else {
                showNotification('Error loading subcategory', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Failed to load subcategory', 'error');
        });
}

function submitEditSubcategory(event) {
    event.preventDefault();
    
    const subcatId = document.getElementById('edit_subcat_id').value;
    const subcatName = document.getElementById('edit_subcat_name').value;
    const catId = document.getElementById('edit_subcat_cat_id').value;
    
    fetch(`/admin/subcategory/edit/${subcatId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            subcat_name: subcatName,
            cat_id: catId
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            closeModal('editSubcategoryModal');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to update subcategory', 'error');
    });
}

// ========================================
// DELETE SUBCATEGORY
// ========================================
function deleteSubcategory(subcatId) {
    if (!confirm("Are you sure you want to delete this subcategory?")) {
        return;
    }

    fetch(`/admin/subcategory/delete/${subcatId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to delete subcategory', 'error');
    });
}

// ========================================
// NOTIFICATION SYSTEM
// ========================================
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 30px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #10B981, #34D399)' : 'linear-gradient(135deg, #EF4444, #DC2626)'};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 600;
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    notification.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> ${message}`;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ========================================
// ESC KEY CLOSE MODAL
// ========================================
document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
        document.querySelectorAll(".modal.active").forEach(modal => {
            modal.classList.remove("active");
        });
        document.body.style.overflow = "auto";
    }
});