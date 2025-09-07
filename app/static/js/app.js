// app/static/js/app.js
console.log("E-Bug Tracker frontend JS loaded");

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.opacity = '0';
            setTimeout(function() {
                flash.remove();
            }, 600);
        }, 5000);
    });

    // Real-time code analysis for bug reporting
    const codeSnippetTextarea = document.getElementById('code_snippet');
    if (codeSnippetTextarea) {
        let analysisTimeout;
        
        codeSnippetTextarea.addEventListener('input', function() {
            clearTimeout(analysisTimeout);
            analysisTimeout = setTimeout(function() {
                const code = codeSnippetTextarea.value;
                if (code.length > 10) {
                    analyzeCode(code);
                }
            }, 1000);
        });
    }

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // Basic form validation
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    field.style.borderColor = 'red';
                    valid = false;
                    
                    // Reset border color after 2 seconds
                    setTimeout(function() {
                        field.style.borderColor = '';
                    }, 2000);
                }
            });
            
            if (!valid) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'error');
            }
        });
    });

    // Status and severity badge enhancements
    const statusBadges = document.querySelectorAll('.status, .severity');
    statusBadges.forEach(function(badge) {
        badge.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        badge.addEventListener('mouseout', function() {
            this.style.transform = '';
        });
    });

    // Copy to clipboard functionality for code snippets
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(function(block) {
        block.addEventListener('click', function() {
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(function() {
                showNotification('Code copied to clipboard', 'success');
            }).catch(function() {
                showNotification('Failed to copy code', 'error');
            });
        });
        
        // Add copy button hint on hover
        block.title = 'Click to copy to clipboard';
    });
});

// Function to analyze code (placeholder for AI integration)
function analyzeCode(code) {
    console.log('Analyzing code:', code.substring(0, 50) + '...');
    
    // This would be replaced with an actual API call to your backend
    // For now, we'll just simulate analysis
    const issues = detectCommonIssues(code);
    
    if (issues.length > 0) {
        showNotification(`Detected ${issues.length} potential issue(s) in your code`, 'info');
    }
}

// Simple pattern detection for common code issues
function detectCommonIssues(code) {
    const issues = [];
    
    // Check for common issues
    if (code.includes('TODO_BUG')) {
        issues.push('TODO_BUG placeholder found');
    }
    
    if (code.includes('console.log(') && !code.includes('// console.log(')) {
        issues.push('console.log statements found (might need removal)');
    }
    
    if (code.includes('eval(')) {
        issues.push('eval() function detected (security risk)');
    }
    
    if (code.includes('==') && !code.includes('===')) {
        issues.push('Using == instead of === (type coercion)');
    }
    
    return issues;
}

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `flash ${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '1000';
    notification.style.maxWidth = '300px';
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(function() {
        notification.style.opacity = '0';
        setTimeout(function() {
            notification.remove();
        }, 600);
    }, 3000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter to submit forms
    if (e.ctrlKey && e.key === 'Enter') {
        const activeForm = document.querySelector('form:focus-within');
        if (activeForm) {
            activeForm.dispatchEvent(new Event('submit', {cancelable: true}));
        }
    }
    
    // Escape key to clear forms
    if (e.key === 'Escape') {
        const focusedInput = document.querySelector('input:focus, textarea:focus');
        if (focusedInput) {
            focusedInput.value = '';
        }
    }
});

// Responsive navigation for mobile devices
function setupMobileNavigation() {
    const nav = document.querySelector('nav');
    if (window.innerWidth < 768 && nav) {
        // Create mobile menu button
        const menuButton = document.createElement('button');
        menuButton.textContent = '☰ Menu';
        menuButton.style.position = 'absolute';
        menuButton.style.top = '10px';
        menuButton.style.right = '10px';
        menuButton.style.zIndex = '100';
        
        // Toggle navigation visibility
        menuButton.addEventListener('click', function() {
            nav.style.display = nav.style.display === 'none' ? 'block' : 'none';
        });
        
        // Add button to page
        document.body.appendChild(menuButton);
        
        // Hide navigation by default on mobile
        nav.style.display = 'none';
    }
}

// Initialize on page load
window.addEventListener('load', function() {
    setupMobileNavigation();
});

// Handle window resize for responsive design
window.addEventListener('resize', function() {
    setupMobileNavigation();
});
