// Mobile menu toggle
document.getElementById('mobile-menu-button').addEventListener('click', function() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
});

// Detect OS and update download button text
function detectOS() {
    const userAgent = window.navigator.userAgent;
    const platform = window.navigator.platform;
    const osButton = document.getElementById('os-text');
    
    if (/Win/.test(platform)) {
        osButton.textContent = 'Windows';
    } else if (/Linux/.test(platform) || /Linux/.test(userAgent)) {
        osButton.textContent = 'Linux';
    } else if (/Mac/.test(platform)) {
        osButton.textContent = 'macOS';
    }
}

detectOS();

// Tab functionality
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active classes from all buttons and contents
        tabButtons.forEach(btn => {
            btn.classList.remove('border-primary-500', 'text-primary-500');
            btn.classList.add('border-transparent', 'text-gray-400');
        });
        tabContents.forEach(content => content.classList.add('hidden'));
        
        // Add active classes to clicked button and corresponding content
        button.classList.remove('border-transparent', 'text-gray-400');
        button.classList.add('border-primary-500', 'text-primary-500');
        
        const tabId = button.getAttribute('data-tab');
        document.getElementById(`${tabId}-tab`).classList.remove('hidden');
    });
});

// Scroll to top button
const scrollTopButton = document.getElementById('scroll-top');
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollTopButton.classList.remove('hidden');
        scrollTopButton.classList.add('block');
    } else {
        scrollTopButton.classList.remove('block');
        scrollTopButton.classList.add('hidden');
    }
});

scrollTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Intersection Observer for scroll animations
const fadeInElements = document.querySelectorAll('.fade-in');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0) scale(1)';
        }
    });
}, {
    threshold: 0.1
});

fadeInElements.forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(30px) scale(0.98)';
    element.style.transition = 'opacity 1s cubic-bezier(0.34, 1.56, 0.64, 1), transform 1s cubic-bezier(0.34, 1.56, 0.64, 1)';
    observer.observe(element);
});

// Feather icons
feather.replace();
