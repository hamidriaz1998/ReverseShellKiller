// DOM Elements
const body = document.body;
const themeSwitch = document.getElementById('theme-switch');
const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
const mainNav = document.getElementById('main-nav');
const header = document.querySelector('header');
const cursor = document.querySelector('.cursor');
const cursorFollower = document.querySelector('.cursor-follower');

// Theme Toggle
function toggleTheme() {
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
    }
}

// Check for saved theme preference
function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        body.classList.add('dark-mode');
        themeSwitch.checked = true;
    } else {
        body.classList.remove('dark-mode');
        themeSwitch.checked = false;
    }
}

// Mobile Navigation Toggle
function toggleMobileNav() {
    mobileNavToggle.classList.toggle('active');
    mainNav.classList.toggle('active');
    body.classList.toggle('nav-open');
}

// Header Scroll Effect
function handleScroll() {
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
}

// Custom Cursor
function updateCursor(e) {
    cursor.style.left = `${e.clientX}px`;
    cursor.style.top = `${e.clientY}px`;
    
    setTimeout(() => {
        cursorFollower.style.left = `${e.clientX}px`;
        cursorFollower.style.top = `${e.clientY}px`;
    }, 50);
}

// Cursor Hover Effects
function setupCursorEffects() {
    const interactiveElements = document.querySelectorAll('a, button, .feature-card, .faq-question, .tab-button, .copy-btn');
    
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.style.width = '16px';
            cursor.style.height = '16px';
            cursor.style.opacity = '0.5';
            cursorFollower.style.width = '40px';
            cursorFollower.style.height = '40px';
        });
        
        el.addEventListener('mouseleave', () => {
            cursor.style.width = '8px';
            cursor.style.height = '8px';
            cursor.style.opacity = '0.7';
            cursorFollower.style.width = '24px';
            cursorFollower.style.height = '24px';
        });
    });
}

// Tab Functionality
function setupTabs() {
    const tabGroups = document.querySelectorAll('.installation-tabs, .config-tabs');
    
    tabGroups.forEach(tabGroup => {
        const tabButtons = tabGroup.querySelectorAll('.tab-button');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Get tab group prefix
                const tabPrefix = button.getAttribute('data-tab').split('-')[0];
                
                // Remove active class from all buttons in this group
                tabGroup.querySelectorAll('.tab-button').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // Hide all related tab contents
                document.querySelectorAll(`.tab-content[id^="${tabPrefix}"]`).forEach(content => {
                    content.classList.remove('active');
                });
                
                // Add active class to clicked button and its content
                button.classList.add('active');
                document.getElementById(button.getAttribute('data-tab')).classList.add('active');
            });
        });
    });
}

// FAQ Toggle
function toggleFAQ(element) {
    const faqItem = element.parentElement;
    const wasActive = faqItem.classList.contains('active');
    
    // Close all other FAQ items
    document.querySelectorAll('.faq-item.active').forEach(item => {
        if (item !== faqItem) {
            item.classList.remove('active');
        }
    });
    
    // Toggle the clicked item
    if (wasActive) {
        faqItem.classList.remove('active');
    } else {
        faqItem.classList.add('active');
    }
}

// Copy to Clipboard
function copyToClipboard(button) {
    const codeBlock = button.parentElement.querySelector('pre').innerText;
    
    navigator.clipboard.writeText(codeBlock).then(() => {
        const originalIcon = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i>';
        
        setTimeout(() => {
            button.innerHTML = originalIcon;
        }, 2000);
    });
}

// Create Particles
function createParticles() {
    const container = document.querySelector('.particles-container');
    if (!container) return;
    
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // Random position around the shield
        const startX = Math.random() * 300 - 150;
        const startY = Math.random() * 300 - 150;
        
        // Random end position (moving outward)
        const angle = Math.random() * Math.PI * 2;
        const distance = 100 + Math.random() * 150;
        const endX = Math.cos(angle) * distance;
        const endY = Math.sin(angle) * distance;
        
        // Set particle properties
        particle.style.left = `calc(50% + ${startX}px)`;
        particle.style.top = `calc(50% + ${startY}px)`;
        particle.style.setProperty('--x', `${endX}px`);
        particle.style.setProperty('--y', `${endY}px`);
        
        // Random size
        const size = 2 + Math.random() * 4;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Random delay
        particle.style.animationDelay = `${Math.random() * 3}s`;
        
        // Random duration
        particle.style.animationDuration = `${2 + Math.random() * 3}s`;
        
        // Add to container
        container.appendChild(particle);
    }
}

// Animate Stats Counter
function animateStats() {
    const stats = document.querySelectorAll('.stat-number');
    
    stats.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-count'));
        const duration = 2000; // 2 seconds
        const step = target / (duration / 16); // 60fps
        let current = 0;
        
        const updateCounter = () => {
            current += step;
            if (current < target) {
                stat.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                stat.textContent = target;
            }
        };
        
        updateCounter();
    });
}

// Intersection Observer for Animations
function setupIntersectionObserver() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('aos-animate');
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('[data-aos]').forEach(element => {
        observer.observe(element);
    });
}

// Smooth Scroll
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Close mobile nav if open
                if (mainNav.classList.contains('active')) {
                    toggleMobileNav();
                }
            }
        });
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Load theme
    loadTheme();
    
    // Theme toggle event
    themeSwitch.addEventListener('change', toggleTheme);
    
    // Mobile nav toggle event
    mobileNavToggle.addEventListener('click', toggleMobileNav);
    
    // Scroll event
    window.addEventListener('scroll', handleScroll);
    
    // Custom cursor
    if (window.innerWidth > 768) {
        document.addEventListener('mousemove', updateCursor);
        setupCursorEffects();
    } else {
        cursor.style.display = 'none';
        cursorFollower.style.display = 'none';
    }
    
    // Setup tabs
    setupTabs();
    
    // Create particles
    createParticles();
    
    // Animate stats
    animateStats();
    
    // Setup intersection observer
    setupIntersectionObserver();
    
    // Setup smooth scroll
    setupSmoothScroll();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            cursor.style.display = 'block';
            cursorFollower.style.display = 'block';
            document.addEventListener('mousemove', updateCursor);
        } else {
            cursor.style.display = 'none';
            cursorFollower.style.display = 'none';
            document.removeEventListener('mousemove', updateCursor);
        }
    });
});