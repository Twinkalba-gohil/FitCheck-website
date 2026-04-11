// Nav items
const navItems = document.querySelectorAll('.nav-item');
navItems.forEach(item => {
    item.addEventListener('click', function(e) {
        // e.preventDefault();
        navItems.forEach(i => i.classList.remove('active'));
        this.classList.add('active');
    });
});

// Animate stats
window.addEventListener('load', () => {
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(stat => {
        const value = stat.textContent.replace(/[^0-9]/g, '');
        let current = 0;
        const increment = value / 50;
        const symbol = stat.textContent.includes('$') ? '$' : '';
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= value) {
                stat.textContent = symbol + parseInt(value).toLocaleString();
                clearInterval(timer);
            } else {
                stat.textContent = symbol + parseInt(current).toLocaleString();
            }
        }, 20);
    });
});

// Search Functionality
const searchInput = document.querySelector('.search-bar input');
searchInput?.addEventListener('input', function(e) {
    console.log('Searching for:', e.target.value);
});

console.log('✨ FitCheck Admin Panel Loaded!');

// ========================================
// FILTER DROPDOWN TOGGLE
// ========================================

function toggleFilterDropdown() {
    const dropdown = document.getElementById('filterDropdown');
    const btn = document.querySelector('.filter-btn');
    
    dropdown.classList.toggle('active');
    btn.classList.toggle('active');
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('filterDropdown');
    const btn = document.querySelector('.filter-btn');
    
    if (dropdown && btn) {
        if (!dropdown.contains(event.target) && !btn.contains(event.target)) {
            dropdown.classList.remove('active');
            btn.classList.remove('active');
        }
    }
});

// Close dropdown on ESC key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const dropdown = document.getElementById('filterDropdown');
        const btn = document.querySelector('.filter-btn');
        
        if (dropdown && btn) {
            dropdown.classList.remove('active');
            btn.classList.remove('active');
        }
    }
});