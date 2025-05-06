document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    
    // Add fade-in animation to main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Products image gallery - switch main image on thumbnail click
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.getElementById('main-product-image');
    if (thumbnails.length > 0 && mainImage) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                // Update main image source
                mainImage.src = this.src;
                
                // Toggle active class
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
    
    // Product quantity buttons
    const decrementBtns = document.querySelectorAll('.decrement-btn');
    const incrementBtns = document.querySelectorAll('.increment-btn');
    const quantityInputs = document.querySelectorAll('.quantity-input');
    
    decrementBtns.forEach((btn, index) => {
        btn.addEventListener('click', function() {
            const input = quantityInputs[index];
            const currentValue = parseInt(input.value);
            if (currentValue > 1) {
                input.value = currentValue - 1;
                if (input.form) {
                    input.form.dispatchEvent(new Event('submit', { cancelable: true }));
                }
            }
        });
    });
    
    incrementBtns.forEach((btn, index) => {
        btn.addEventListener('click', function() {
            const input = quantityInputs[index];
            const currentValue = parseInt(input.value);
            const maxValue = parseInt(input.getAttribute('max') || 99);
            if (currentValue < maxValue) {
                input.value = currentValue + 1;
                if (input.form) {
                    input.form.dispatchEvent(new Event('submit', { cancelable: true }));
                }
            }
        });
    });
    
    // AJAX update cart (example implementation)
    const updateCartForms = document.querySelectorAll('.update-cart-form');
    updateCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update cart count in navbar
                    const cartCountElement = document.querySelector('.cart-count');
                    if (cartCountElement) {
                        cartCountElement.textContent = data.cart_count;
                    }
                    
                    // Update cart total
                    const cartTotalElement = document.querySelector('.cart-total');
                    if (cartTotalElement && data.cart_total) {
                        cartTotalElement.textContent = new Intl.NumberFormat('vi-VN').format(data.cart_total) + ' ₫';
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
    
    // Add to cart animation
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productCard = this.closest('.card');
            if (productCard) {
                productCard.classList.add('added-to-cart');
                setTimeout(() => {
                    productCard.classList.remove('added-to-cart');
                }, 1000);
            }
        });
    });
    
    // Product filter show/hide on mobile
    const filterToggleBtn = document.getElementById('filter-toggle');
    const filterSidebar = document.getElementById('filter-sidebar');
    if (filterToggleBtn && filterSidebar) {
        filterToggleBtn.addEventListener('click', function() {
            filterSidebar.classList.toggle('show');
        });
    }
    
    // Back to top button
    const backToTopBtn = document.getElementById('back-to-top');
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}); 