// ========================================
// COMMON.JS - Shared functionality across all pages
// ========================================

// Navbar scroll effect
document.addEventListener('DOMContentLoaded', function() {
  const header = document.getElementById('header');
  
  if (header) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }
});


