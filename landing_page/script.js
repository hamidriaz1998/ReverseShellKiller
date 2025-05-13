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
    faqItem.classList.toggle('active');
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

// Create SVG shield image dynamically
// Add CSS animations to head
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

document.addEventListener('DOMContentLoaded', function() {
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
    
    // Handle resize events to reset mobile nav state when switching to desktop view
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768 && document.getElementById('main-nav').classList.contains('active')) {
            document.getElementById('main-nav').classList.remove('active');
            document.getElementById('mobile-nav-toggle').classList.remove('active');
            document.querySelector('.overlay').classList.remove('active');
            document.body.classList.remove('nav-open');
            document.getElementById('mobile-nav-toggle').innerHTML = '<i class="fas fa-bars"></i>';
        }
    });
    
    // Initialize tab functionality for all tab groups
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
    
    const shieldImg = document.getElementById('shield-img');
    if (shieldImg) {
        const svgContent = `
        <svg width="350" height="350" viewBox="0 0 350 350" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="shieldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#2962ff" />
                    <stop offset="100%" stop-color="#0039cb" />
                </linearGradient>
                <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#000" flood-opacity="0.3"/>
                </filter>
            </defs>
            
            <!-- Shield Base -->
            <path d="M175,30 L300,75 C300,75 300,160 300,200 C300,280 175,320 175,320 C175,320 50,280 50,200 C50,160 50,75 50,75 L175,30 Z" 
                  fill="url(#shieldGradient)" filter="url(#shadow)"/>
            
            <!-- Shield Inner -->
            <path d="M175,50 L275,85 C275,85 275,155 275,190 C275,250 175,290 175,290 C175,290 75,250 75,190 C75,155 75,85 75,85 L175,50 Z" 
                  fill="#ffffff" opacity="0.2"/>
            
            <!-- Shield Icon -->
            <circle cx="175" cy="170" r="60" fill="#ffffff"/>
            
            <!-- Lock Icon -->
            <rect x="155" y="165" width="40" height="35" rx="5" fill="#2962ff"/>
            <rect x="165" y="140" width="20" height="30" rx="10" stroke="#2962ff" stroke-width="8" fill="none"/>
            
            <!-- Alert Badge -->
            <circle cx="235" cy="115" r="25" fill="#d32f2f"/>
            <text x="235" y="125" font-family="Arial" font-size="30" font-weight="bold" fill="#ffffff" text-anchor="middle">!</text>
        </svg>
        `;
        shieldImg.outerHTML = svgContent;
    }
    
    // Add scroll behavior
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
    
    // Add header scroll effect
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.padding = '10px 0';
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.padding = '20px 0';
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    });
});