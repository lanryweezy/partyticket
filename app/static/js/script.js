// PartyTicket Nigeria - JavaScript Functions

// Initialize tooltips and animations
document.addEventListener('DOMContentLoaded', function() {
  // Navbar scroll effect
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }
  
  // Intersection Observer for fade-in animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  // Observe all cards and sections
  document.querySelectorAll('.card, section').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
  
  // Enable Bootstrap tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  // Enable Bootstrap popovers
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
  
  // Handle print functionality
  const printButtons = document.querySelectorAll('[data-action="print"]');
  printButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      window.print();
    });
  });
  
  // Handle copy to clipboard
  const copyButtons = document.querySelectorAll('[data-action="copy"]');
  copyButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(button.dataset.target);
      if (target) {
        target.select();
        document.execCommand('copy');
        
        // Show feedback
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="bi bi-check-circle"></i> Copied!';
        setTimeout(() => {
          button.innerHTML = originalText;
        }, 2000);
      }
    });
  });
  
  // Handle scroll to top button
  const scrollToTopButton = document.createElement('div');
  scrollToTopButton.className = 'scroll-to-top';
  scrollToTopButton.innerHTML = '<i class="bi bi-arrow-up"></i>';
  document.body.appendChild(scrollToTopButton);
  
  window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
      scrollToTopButton.classList.add('show');
    } else {
      scrollToTopButton.classList.remove('show');
    }
  });
  
  scrollToTopButton.addEventListener('click', function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
  
  // Handle dark mode toggle
  const darkModeToggle = document.createElement('div');
  darkModeToggle.className = 'dark-mode-toggle';
  darkModeToggle.innerHTML = '<i class="bi bi-moon"></i>';
  document.body.appendChild(darkModeToggle);
  
  // Check for saved theme preference or respect OS preference
  const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
  const currentTheme = localStorage.getItem('theme');
  
  if (currentTheme === 'dark' || (!currentTheme && prefersDarkScheme.matches)) {
    document.documentElement.setAttribute('data-theme', 'dark');
    darkModeToggle.innerHTML = '<i class="bi bi-sun"></i>';
  }
  
  darkModeToggle.addEventListener('click', function() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    
    if (currentTheme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'light');
      localStorage.setItem('theme', 'light');
      darkModeToggle.innerHTML = '<i class="bi bi-moon"></i>';
    } else {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
      darkModeToggle.innerHTML = '<i class="bi bi-sun"></i>';
    }
  });
  
  // Handle form validation feedback
  const forms = document.querySelectorAll('.needs-validation');
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });
  
  // Handle quantity selector for tickets
  const quantitySelectors = document.querySelectorAll('[data-role="quantity-selector"]');
  quantitySelectors.forEach(selector => {
    const input = selector.querySelector('input[type="number"]');
    const minusBtn = selector.querySelector('[data-action="minus"]');
    const plusBtn = selector.querySelector('[data-action="plus"]');
    
    if (input && minusBtn && plusBtn) {
      minusBtn.addEventListener('click', function() {
        if (parseInt(input.value) > parseInt(input.min)) {
          input.value = parseInt(input.value) - 1;
          input.dispatchEvent(new Event('change'));
        }
      });
      
      plusBtn.addEventListener('click', function() {
        if (parseInt(input.value) < parseInt(input.max)) {
          input.value = parseInt(input.value) + 1;
          input.dispatchEvent(new Event('change'));
        }
      });
    }
  });
  
  // Handle image preview for uploads
  const imageUploads = document.querySelectorAll('[data-role="image-upload"]');
  imageUploads.forEach(upload => {
    const input = upload.querySelector('input[type="file"]');
    const preview = upload.querySelector('[data-role="preview"]');
    
    if (input && preview) {
      input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
          };
          reader.readAsDataURL(file);
        }
      });
    }
  });
  
  // Handle accordion toggle icons
  const accordions = document.querySelectorAll('.accordion');
  accordions.forEach(accordion => {
    accordion.addEventListener('show.bs.collapse', function(e) {
      const button = e.target.previousElementSibling.querySelector('.accordion-button');
      if (button) {
        button.classList.add('expanded');
      }
    });
    
    accordion.addEventListener('hide.bs.collapse', function(e) {
      const button = e.target.previousElementSibling.querySelector('.accordion-button');
      if (button) {
        button.classList.remove('expanded');
      }
    });
  });
  
  // Handle modal auto-focus
  const modals = document.querySelectorAll('.modal');
  modals.forEach(modal => {
    modal.addEventListener('shown.bs.modal', function() {
      const autofocus = modal.querySelector('[autofocus]');
      if (autofocus) {
        autofocus.focus();
      }
    });
  });
  
  // Handle flash messages auto-hide
  const flashMessages = document.querySelectorAll('.alert');
  flashMessages.forEach(function(flash) {
    setTimeout(function() {
      flash.classList.remove('show');
      setTimeout(function() {
        flash.remove();
      }, 150);
    }, 5000); // Hide after 5 seconds
  });
  
  // Handle smooth scrolling for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // Handle mobile menu toggle
  const mobileMenuToggle = document.querySelector('.navbar-toggler');
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', function() {
      const menu = document.querySelector('.navbar-collapse');
      if (menu) {
        menu.classList.toggle('show');
      }
    });
  }
  
  // Handle search form submission
  const searchForms = document.querySelectorAll('[data-role="search-form"]');
  searchForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      const input = form.querySelector('input[name="q"]');
      if (input && !input.value.trim()) {
        e.preventDefault();
        input.focus();
        return false;
      }
    });
  });
  
  // Handle newsletter subscription
  const newsletterForms = document.querySelectorAll('[data-role="newsletter-form"]');
  newsletterForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const emailInput = form.querySelector('input[type="email"]');
      const submitButton = form.querySelector('button[type="submit"]');
      
      if (emailInput && emailInput.value && validateEmail(emailInput.value)) {
        // Disable button and show loading state
        submitButton.disabled = true;
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Subscribing...';
        
        // Simulate API call
        setTimeout(() => {
          // Reset form and show success message
          form.reset();
          submitButton.disabled = false;
          submitButton.innerHTML = originalText;
          
          // Show success message
          const successMessage = document.createElement('div');
          successMessage.className = 'alert alert-success mt-2';
          successMessage.innerHTML = '<i class="bi bi-check-circle me-2"></i>Thank you for subscribing!';
          form.parentNode.insertBefore(successMessage, form.nextSibling);
          
          // Remove success message after 3 seconds
          setTimeout(() => {
            successMessage.remove();
          }, 3000);
        }, 1500);
      } else {
        // Show validation error
        const errorFeedback = document.createElement('div');
        errorFeedback.className = 'invalid-feedback d-block';
        errorFeedback.textContent = 'Please enter a valid email address';
        if (emailInput) {
          emailInput.classList.add('is-invalid');
          emailInput.parentNode.appendChild(errorFeedback);
        }
      }
    });
  });
  
  // Helper function to validate email
  function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }
  
  // Handle event card hover effects
  const eventCards = document.querySelectorAll('.event-card');
  eventCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-5px)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });
  
  // Handle countdown timers
  const countdowns = document.querySelectorAll('[data-countdown]');
  countdowns.forEach(countdown => {
    const targetDate = new Date(countdown.dataset.countdown).getTime();
    const daysElem = countdown.querySelector('[data-days]');
    const hoursElem = countdown.querySelector('[data-hours]');
    const minutesElem = countdown.querySelector('[data-minutes]');
    const secondsElem = countdown.querySelector('[data-seconds]');
    
    if (targetDate && daysElem && hoursElem && minutesElem && secondsElem) {
      const interval = setInterval(function() {
        const now = new Date().getTime();
        const distance = targetDate - now;
        
        if (distance < 0) {
          clearInterval(interval);
          countdown.innerHTML = '<div class="text-danger">Event has started!</div>';
          return;
        }
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        daysElem.textContent = days;
        hoursElem.textContent = hours;
        minutesElem.textContent = minutes;
        secondsElem.textContent = seconds;
      }, 1000);
    }
  });
  
  // Handle social sharing buttons
  const shareButtons = document.querySelectorAll('[data-share]');
  shareButtons.forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const platform = this.dataset.share;
      const url = encodeURIComponent(window.location.href);
      const title = encodeURIComponent(document.title);
      
      let shareUrl = '';
      switch (platform) {
        case 'facebook':
          shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
          break;
        case 'twitter':
          shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
          break;
        case 'linkedin':
          shareUrl = `https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}`;
          break;
        case 'whatsapp':
          shareUrl = `https://wa.me/?text=${title}%20${url}`;
          break;
        case 'email':
          shareUrl = `mailto:?subject=${title}&body=Check out this link: ${url}`;
          break;
        default:
          return;
      }
      
      window.open(shareUrl, '_blank', 'width=600,height=400');
    });
  });
});

// Global utility functions

// Format currency
function formatCurrency(amount, currency = '₦') {
  return `${currency}${parseFloat(amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`;
}

// Format date
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
}

// Format time
function formatTime(dateString) {
  const options = { hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleTimeString(undefined, options);
}

// Debounce function
function debounce(func, wait, immediate) {
  let timeout;
  return function() {
    const context = this, args = arguments;
    const later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}

// Throttle function
function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

// Cookie functions
function setCookie(name, value, days) {
  const expires = new Date();
  expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
  document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

function getCookie(name) {
  const nameEQ = `${name}=`;
  const ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
  }
  return null;
}

// Local storage functions
function setLocalStorage(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (e) {
    console.error('Error saving to localStorage:', e);
    return false;
  }
}

function getLocalStorage(key) {
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  } catch (e) {
    console.error('Error reading from localStorage:', e);
    return null;
  }
}

// Session storage functions
function setSessionStorage(key, value) {
  try {
    sessionStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch (e) {
    console.error('Error saving to sessionStorage:', e);
    return false;
  }
}

function getSessionStorage(key) {
  try {
    const item = sessionStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  } catch (e) {
    console.error('Error reading from sessionStorage:', e);
    return null;
  }
}

// AJAX helper function
function ajaxRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open(options.method || 'GET', url);
    
    // Set headers
    if (options.headers) {
      Object.keys(options.headers).forEach(key => {
        xhr.setRequestHeader(key, options.headers[key]);
      });
    }
    
    // Set timeout
    xhr.timeout = options.timeout || 10000;
    
    // Handle response
    xhr.onload = function() {
      if (xhr.status >= 200 && xhr.status < 300) {
        try {
          const response = JSON.parse(xhr.responseText);
          resolve(response);
        } catch (e) {
          resolve(xhr.responseText);
        }
      } else {
        reject(new Error(`Request failed with status ${xhr.status}`));
      }
    };
    
    // Handle errors
    xhr.onerror = function() {
      reject(new Error('Network error'));
    };
    
    xhr.ontimeout = function() {
      reject(new Error('Request timeout'));
    };
    
    // Send request
    xhr.send(options.body ? JSON.stringify(options.body) : null);
  });
}

// Show loading spinner
function showLoading(element) {
  if (element) {
    element.innerHTML = '<div class="d-flex justify-content-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
  }
}

// Hide loading spinner
function hideLoading(element, content) {
  if (element && content !== undefined) {
    element.innerHTML = content;
  }
}

// Show notification
function showNotification(message, type = 'info', duration = 5000) {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
  notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
  notification.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  
  // Add to body
  document.body.appendChild(notification);
  
  // Auto remove after duration
  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 150);
  }, duration);
}

// Validate form field
function validateField(field, rules) {
  const value = field.value.trim();
  let isValid = true;
  let errorMessage = '';
  
  // Required validation
  if (rules.required && !value) {
    isValid = false;
    errorMessage = 'This field is required';
  }
  
  // Email validation
  if (rules.email && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    isValid = false;
    errorMessage = 'Please enter a valid email address';
  }
  
  // Min length validation
  if (rules.minLength && value.length < rules.minLength) {
    isValid = false;
    errorMessage = `This field must be at least ${rules.minLength} characters`;
  }
  
  // Max length validation
  if (rules.maxLength && value.length > rules.maxLength) {
    isValid = false;
    errorMessage = `This field must be no more than ${rules.maxLength} characters`;
  }
  
  // Custom validation
  if (rules.custom && typeof rules.custom === 'function') {
    const customResult = rules.custom(value);
    if (customResult !== true) {
      isValid = false;
      errorMessage = customResult || 'This field is invalid';
    }
  }
  
  // Update UI
  if (isValid) {
    field.classList.remove('is-invalid');
    field.classList.add('is-valid');
    const feedback = field.parentNode.querySelector('.invalid-feedback');
    if (feedback) {
      feedback.remove();
    }
  } else {
    field.classList.remove('is-valid');
    field.classList.add('is-invalid');
    let feedback = field.parentNode.querySelector('.invalid-feedback');
    if (!feedback) {
      feedback = document.createElement('div');
      feedback.className = 'invalid-feedback';
      field.parentNode.appendChild(feedback);
    }
    feedback.textContent = errorMessage;
  }
  
  return isValid;
}

// Initialize form validation
function initFormValidation(formSelector, validationRules) {
  const form = document.querySelector(formSelector);
  if (!form) return;
  
  // Add validation to each field
  Object.keys(validationRules).forEach(fieldName => {
    const field = form.querySelector(`[name="${fieldName}"]`);
    if (field) {
      field.addEventListener('blur', function() {
        validateField(this, validationRules[fieldName]);
      });
      
      field.addEventListener('input', function() {
        if (this.classList.contains('is-invalid')) {
          validateField(this, validationRules[fieldName]);
        }
      });
    }
  });
  
  // Handle form submission
  form.addEventListener('submit', function(e) {
    let isFormValid = true;
    
    // Validate all fields
    Object.keys(validationRules).forEach(fieldName => {
      const field = form.querySelector(`[name="${fieldName}"]`);
      if (field) {
        const isValid = validateField(field, validationRules[fieldName]);
        if (!isValid) {
          isFormValid = false;
        }
      }
    });
    
    // Prevent submission if form is invalid
    if (!isFormValid) {
      e.preventDefault();
      showNotification('Please fix the errors in the form', 'danger');
    }
  });
}