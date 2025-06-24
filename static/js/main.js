// Main JavaScript for Business Website

document.addEventListener('DOMContentLoaded', function() {
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('bg-dark');
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.classList.remove('bg-dark');
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading animation to cards
    const cards = document.querySelectorAll('.card');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('loading');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach(card => {
        observer.observe(card);
    });

    // Add loading animation to feature items
    const featureItems = document.querySelectorAll('.feature-item');
    featureItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
        item.classList.add('loading');
    });

    // Button click effects
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add CSS for ripple effect
    const style = document.createElement('style');
    style.textContent = `
        .btn {
            position: relative;
            overflow: hidden;
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Mobile menu toggle enhancement
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });

        // Close mobile menu when clicking on a link
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', function() {
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                }
            });
        });
    }

    // Parallax effect for hero section
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        }
    });

    // Counter animation for statistics (if you add them later)
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        function updateCounter() {
            start += increment;
            if (start < target) {
                element.textContent = Math.floor(start);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        }
        
        updateCounter();
    }

    // Form validation enhancement (for contact form)
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Show error message
                const errorDiv = document.createElement('div');
                errorDiv.className = 'alert alert-danger mt-3';
                errorDiv.textContent = 'Please fill in all required fields.';
                form.appendChild(errorDiv);
                
                setTimeout(() => {
                    errorDiv.remove();
                }, 3000);
            }
        });
    });

    // Lazy loading for images (if you add them later)
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Console welcome message
    console.log('%cWelcome to Your Business Website! 🚀', 'color: #ffc107; font-size: 20px; font-weight: bold;');
    console.log('%cBuilt with FastAPI and Jinja2', 'color: #667eea; font-size: 14px;');

    // Dark mode toggle logic
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkModeIcon = document.getElementById('darkModeIcon');
    function setDarkMode(enabled) {
        if (enabled) {
            document.body.classList.add('dark-mode');
            if (darkModeIcon) {
                darkModeIcon.classList.remove('fa-moon');
                darkModeIcon.classList.add('fa-sun');
            }
        } else {
            document.body.classList.remove('dark-mode');
            if (darkModeIcon) {
                darkModeIcon.classList.remove('fa-sun');
                darkModeIcon.classList.add('fa-moon');
            }
        }
    }
    if (darkModeToggle && darkModeIcon) {
        const darkPref = localStorage.getItem('darkMode') === 'true';
        setDarkMode(darkPref);
        darkModeToggle.addEventListener('click', () => {
            const enabled = !document.body.classList.contains('dark-mode');
            setDarkMode(enabled);
            localStorage.setItem('darkMode', enabled);
        });
    }
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced scroll performance
const optimizedScrollHandler = debounce(function() {
    // Add any scroll-based functionality here
}, 16);

window.addEventListener('scroll', optimizedScrollHandler); 