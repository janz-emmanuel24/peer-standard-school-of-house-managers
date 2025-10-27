// Main JavaScript for Peer Standard School of Maids

// API Configuration
const API_BASE_URL = '/api';
let authToken = localStorage.getItem('authToken');

// API Helper Functions
const api = {
    async request(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...(authToken && { 'Authorization': `Bearer ${authToken}` }),
                ...options.headers,
            },
            ...options,
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.detail || 'An error occurred');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            showNotification(error.message, 'error');
            throw error;
        }
    },

    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    },

    // Authentication
    async login(username, password) {
        const response = await this.post('/token/', { username, password });
        authToken = response.access;
        localStorage.setItem('authToken', authToken);
        return response;
    },

    async logout() {
        authToken = null;
        localStorage.removeItem('authToken');
    },

    // User Management
    async getCurrentUser() {
        return this.get('/accounts/users/me/');
    },

    async updateProfile(data) {
        return this.put('/accounts/users/update_profile/', data);
    },

    // Courses
    async getCourses(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.get(`/courses/courses/${queryString ? '?' + queryString : ''}`);
    },

    async getCourse(id) {
        return this.get(`/courses/courses/${id}/`);
    },

    // Students
    async getStudents(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.get(`/students/students/${queryString ? '?' + queryString : ''}`);
    },

    async getMyCourses() {
        return this.get('/students/students/me/enrollments/');
    },

    // Employers
    async getJobPostings(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.get(`/employers/job-postings/${queryString ? '?' + queryString : ''}`);
    },

    async applyForJob(jobId, data) {
        return this.post(`/employers/job-postings/${jobId}/apply/`, data);
    },

    // Certificates
    async getMyCertificates() {
        return this.get('/certifications/certificates/');
    },

    async verifyCertificate(code) {
        return this.get(`/certifications/certificates/verify/?code=${code}`);
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            const icon = this.querySelector('i');
            
            if (mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.remove('hidden');
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                mobileMenu.classList.add('hidden');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenu.contains(event.target) && !mobileMenuButton.contains(event.target)) {
                mobileMenu.classList.add('hidden');
                const icon = mobileMenuButton.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('[role="alert"]');
        alerts.forEach(function(alert) {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);

    // Add loading state to forms
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            var submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
                submitBtn.disabled = true;
            }
        });
    });

    // Smooth scrolling for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add animation classes to elements when they come into view
    var observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    var animateElements = document.querySelectorAll('.card, .stat-item, .feature-icon');
    animateElements.forEach(function(el) {
        observer.observe(el);
    });

    // Dashboard specific functionality
    if (document.body.classList.contains('dashboard-page')) {
        // Auto-refresh dashboard data every 5 minutes
        setInterval(function() {
            // You can implement AJAX calls here to refresh dashboard data
            console.log('Dashboard data refresh triggered');
        }, 300000);
    }

    // Form validation enhancement
    var inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });

    function validateField(field) {
        var isValid = field.checkValidity();
        var feedback = field.parentNode.querySelector('.invalid-feedback');
        
        if (!isValid) {
            field.classList.add('is-invalid');
            if (feedback) {
                feedback.style.display = 'block';
            }
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            if (feedback) {
                feedback.style.display = 'none';
            }
        }
    }

    // Search functionality
    var searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            var searchTerm = this.value.toLowerCase();
            var targetSelector = this.dataset.target;
            var items = document.querySelectorAll(targetSelector);
            
            items.forEach(function(item) {
                var text = item.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // Confirmation dialogs
    var deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // File upload preview
    var fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            var file = this.files[0];
            if (file) {
                var preview = this.parentNode.querySelector('.file-preview');
                if (preview) {
                    if (file.type.startsWith('image/')) {
                        var reader = new FileReader();
                        reader.onload = function(e) {
                            preview.innerHTML = '<img src="' + e.target.result + '" class="img-thumbnail" style="max-width: 200px;">';
                        };
                        reader.readAsDataURL(file);
                    } else {
                        preview.innerHTML = '<p class="text-muted">File: ' + file.name + '</p>';
                    }
                }
            }
        });
    });

    // Print functionality
    var printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            window.print();
        });
    });

    // Copy to clipboard functionality
    var copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var text = this.dataset.copy;
            navigator.clipboard.writeText(text).then(function() {
                // Show success message
                var toast = document.createElement('div');
                toast.className = 'toast align-items-center text-white bg-success border-0';
                toast.innerHTML = '<div class="d-flex"><div class="toast-body">Copied to clipboard!</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>';
                document.body.appendChild(toast);
                var bsToast = new bootstrap.Toast(toast);
                bsToast.show();
                setTimeout(function() {
                    document.body.removeChild(toast);
                }, 3000);
            });
        });
    });
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(date));
}

function showNotification(message, type = 'info') {
    var alertClass = 'alert-' + type;
    var notification = document.createElement('div');
    notification.className = 'alert ' + alertClass + ' alert-dismissible fade show position-fixed';
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = message + '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
    
    document.body.appendChild(notification);
    
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(notification);
        bsAlert.close();
    }, 5000);
}
