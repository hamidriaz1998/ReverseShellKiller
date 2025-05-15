// Toggle dark/light mode
function toggleDarkMode(inputElement) {
    const isDark = document.body.getAttribute('data-theme') === 'dark';
    if (isDark) {
        document.body.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        
        // Sync the other checkbox if this was triggered from one of the theme toggles
        if (inputElement) {
            const otherId = inputElement.id === 'theme-toggle' ? 'theme-toggle-mobile' : 'theme-toggle';
            document.getElementById(otherId).checked = false;
        }
    } else {
        document.body.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        
        // Sync the other checkbox if this was triggered from one of the theme toggles
        if (inputElement) {
            const otherId = inputElement.id === 'theme-toggle' ? 'theme-toggle-mobile' : 'theme-toggle';
            document.getElementById(otherId).checked = true;
        }
    }
}

// Toggle mobile navigation
function toggleMobileNav() {
    const nav = document.getElementById('main-nav');
    const toggle = document.getElementById('mobile-nav-toggle');
    const body = document.body;
    const overlay = document.querySelector('.overlay');
    
    // Toggle classes
    nav.classList.toggle('active');
    toggle.classList.toggle('active');
    body.classList.toggle('nav-open');
    overlay.classList.toggle('active');
    
    // Add animation class
    if (nav.classList.contains('active')) {
        nav.style.animation = 'slideIn 0.3s forwards';
        toggle.innerHTML = '<i class="fas fa-times"></i>';
    } else {
        nav.style.animation = 'slideOut 0.3s forwards';
        toggle.innerHTML = '<i class="fas fa-bars"></i>';
        // Reset nav position after animation completes
        setTimeout(() => {
            if (!nav.classList.contains('active')) {
                nav.style.animation = '';
            }
        }, 300);
    }
}

// Toggle FAQ items
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

// Copy code to clipboard
function copyToClipboard(button) {
    const codeBlock = button.parentElement.querySelector('pre').innerText;
    navigator.clipboard.writeText(codeBlock).then(() => {
        const originalText = button.innerText;
        button.innerText = 'Copied!';
        button.style.backgroundColor = 'rgba(0, 200, 83, 0.3)';
        
        setTimeout(() => {
            button.innerText = originalText;
            button.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
        }, 2000);
    });
}

// Create particles for shield animation
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

// Animate stats counter
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

// Intersection Observer for animations
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

// Add animation styles
function addAnimationStyles() {
    const styleEl = document.createElement('style');
    styleEl.textContent = `
        @keyframes slideIn {
            from { right: -100%; }
            to { right: 0; }
        }
        
        @keyframes slideOut {
            from { right: 0; }
            to { right: -100%; }
        }
    `;
    document.head.appendChild(styleEl);
}

// Smooth scroll for navigation links
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Add header scroll effect
function setupHeaderScroll() {
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.padding = '10px 0';
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.padding = '15px 0';
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    });
}

// Initialize tab functionality
function setupTabs() {
    document.querySelectorAll('.installation-tabs, .config-tabs').forEach(tabGroup => {
        const tabButtons = tabGroup.querySelectorAll('.tab-button');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                // Find sibling tab buttons in this group
                const siblingButtons = tabGroup.querySelectorAll('.tab-button');
                
                // Remove active class from all buttons in this group
                siblingButtons.forEach(btn => btn.classList.remove('active'));
                
                // Find all related content tabs
                const contentId = button.getAttribute('data-tab');
                const allTabContents = document.querySelectorAll(`.tab-content[id^="${contentId.split('-')[0]}"]`);
                
                // Hide all related tab contents
                allTabContents.forEach(content => {
                    content.classList.remove('active');
                });
                
                // Add active class to clicked button and its content
                button.classList.add('active');
                const selectedContent = document.getElementById(contentId);
                if (selectedContent) {
                    selectedContent.classList.add('active');
                }
            });
        });
        
        // Set first tab in each group as active by default
        if (tabButtons.length > 0) {
            tabButtons[0].click();
        }
    });
}

// Handle resize events
function setupResizeHandler() {
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768 && document.getElementById('main-nav').classList.contains('active')) {
            document.getElementById('main-nav').classList.remove('active');
            document.getElementById('mobile-nav-toggle').classList.remove('active');
            document.querySelector('.overlay').classList.remove('active');
            document.body.classList.remove('nav-open');
            document.getElementById('mobile-nav-toggle').innerHTML = '<i class="fas fa-bars"></i>';
        }
        
        // Hide/show custom cursor based on screen size
        const cursor = document.querySelector('.cursor');
        const cursorFollower = document.querySelector('.cursor-follower');
        
        if (window.innerWidth <= 768) {
            if (cursor) cursor.style.display = 'none';
            if (cursorFollower) cursorFollower.style.display = 'none';
        } else {
            if (cursor) cursor.style.display = 'block';
            if (cursorFollower) cursorFollower.style.display = 'block';
        }
    });
}

// Add active class to navigation links based on scroll position
function setupScrollSpy() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (window.pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Custom cursor
    const cursor = document.querySelector('.cursor');
    const cursorFollower = document.querySelector('.cursor-follower');
    
    document.addEventListener('mousemove', function(e) {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
        
        // Add a slight delay to the follower for a smooth effect
        setTimeout(() => {
            cursorFollower.style.left = e.clientX + 'px';
            cursorFollower.style.top = e.clientY + 'px';
        }, 50);
    });
    
    // Hover effects for interactive elements
    const interactiveElements = document.querySelectorAll('a, button, .feature-card, .faq-question, .tab-button, .copy-btn');
    
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.style.width = '20px';
            cursor.style.height = '20px';
            cursor.style.opacity = '0.5';
            cursorFollower.style.width = '40px';
            cursorFollower.style.height = '40px';
        });
        
        el.addEventListener('mouseleave', () => {
            cursor.style.width = '10px';
            cursor.style.height = '10px';
            cursor.style.opacity = '0.7';
            cursorFollower.style.width = '30px';
            cursorFollower.style.height = '30px';
        });
    });
    
    // Hide cursor on mobile devices
    if (window.innerWidth <= 768) {
        cursor.style.display = 'none';
        cursorFollower.style.display = 'none';
    }
    
    // Add animation styles
    addAnimationStyles();
    
    // Set up overlay click handler
    document.querySelector('.overlay').addEventListener('click', toggleMobileNav);
    
    // Check for saved theme preference or respect OS preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.setAttribute('data-theme', 'dark');
        document.getElementById('theme-toggle').checked = true;
        document.getElementById('theme-toggle-mobile').checked = true;
    }
    
    // Set up theme toggle listeners
    document.getElementById('theme-toggle').addEventListener('change', function() {
        toggleDarkMode(this);
    });
    
    document.getElementById('theme-toggle-mobile').addEventListener('change', function() {
        toggleDarkMode(this);
    });
    
    // Set up mobile navigation toggle
    document.getElementById('mobile-nav-toggle').addEventListener('click', toggleMobileNav);
    
    // Close mobile nav when clicking on a link
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768 && document.getElementById('main-nav').classList.contains('active')) {
                toggleMobileNav();
            }
        });
    });
    
    // Initialize tabs
    setupTabs();
    
    // Create particles for shield animation
    createParticles();
    
    // Animate stats counter
    animateStats();
    
    // Setup intersection observer for animations
    setupIntersectionObserver();
    
    // Setup smooth scroll
    setupSmoothScroll();
    
    // Setup header scroll effect
    setupHeaderScroll();
    
    // Setup resize handler
    setupResizeHandler();
    
    // Setup scroll spy
    setupScrollSpy();
});