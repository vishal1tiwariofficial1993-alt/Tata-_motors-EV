/**
 * Tata Motors EV Platform - Main JavaScript
 * Handles client-side interactions and API calls
 */

// ========================================
// UTILITY FUNCTIONS
// ========================================

/**
 * Format number as Indian currency (₹)
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0
    }).format(amount);
}

/**
 * Format large numbers with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Debounce function for optimizing API calls
 */
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

/**
 * Show loading spinner
 */
function showLoading() {
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.innerHTML = '<div class="spinner"></div>Loading...';
    document.body.appendChild(spinner);
}

/**
 * Hide loading spinner
 */
function hideLoading() {
    const spinner = document.querySelector('.loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

// ========================================
// MODAL FUNCTIONS
// ========================================

/**
 * Show modal dialog
 */
function showModal(title, message, type = 'info') {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-content ${type}">
            <div class="modal-header">
                <h2>${title}</h2>
                <button class="modal-close" onclick="closeModal(this)">&times;</button>
            </div>
            <div class="modal-body">
                ${message}
            </div>
            <div class="modal-footer">
                <button class="btn btn-primary" onclick="closeModal(this)">Close</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    
    // Close on background click
    modal.addEventListener('click', function(e) {
        if (e.target === this) closeModal(this);
    });
}

/**
 * Close modal dialog
 */
function closeModal(element) {
    const modal = element.closest('.modal-overlay');
    if (modal) modal.remove();
}

// ========================================
// API CALL FUNCTIONS
// ========================================

/**
 * Fetch models from backend
 */
async function fetchModels() {
    try {
        const response = await fetch('/api/models');
        if (!response.ok) throw new Error('Failed to fetch models');
        return await response.json();
    } catch (error) {
        console.error('Error fetching models:', error);
        return { models: [] };
    }
}

/**
 * Get EV recommendation
 */
async function getRecommendation(criteria) {
    try {
        showLoading();
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(criteria)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to get recommendation');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        showModal('Error', error.message, 'error');
        return null;
    } finally {
        hideLoading();
    }
}

/**
 * Calculate range
 */
async function calculateRange(data) {
    try {
        showLoading();
        const response = await fetch('/api/range', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Failed to calculate range');
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        showModal('Error', error.message, 'error');
        return null;
    } finally {
        hideLoading();
    }
}

/**
 * Compare costs
 */
async function compareCosts(data) {
    try {
        showLoading();
        const response = await fetch('/api/compare-cost', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) throw new Error('Failed to compare costs');
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        showModal('Error', error.message, 'error');
        return null;
    } finally {
        hideLoading();
    }
}

/**
 * Fetch charging stations
 */
async function fetchChargers(filters = {}) {
    try {
        const params = new URLSearchParams(filters);
        const response = await fetch(`/api/chargers?${params}`);
        if (!response.ok) throw new Error('Failed to fetch chargers');
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return { stations: [] };
    }
}

/**
 * Book test drive
 */
async function bookTestDrive(data) {
    try {
        showLoading();
        const response = await fetch('/api/testdrive/book', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to book test drive');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        showModal('Error', error.message, 'error');
        return null;
    } finally {
        hideLoading();
    }
}

/**
 * Send chat message
 */
async function sendChatMessage(message) {
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) throw new Error('Failed to send message');
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return { ai_response: 'Sorry, I encountered an error. Please try again.' };
    }
}

// ========================================
// DATA VALIDATION FUNCTIONS
// ========================================

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate phone number (India)
 */
function isValidPhone(phone) {
    const phoneRegex = /^[6-9]\d{9}$/;
    return phoneRegex.test(phone.replace(/\D/g, ''));
}

/**
 * Validate form data
 */
function validateForm(formData, rules) {
    const errors = {};
    
    for (const [field, rule] of Object.entries(rules)) {
        const value = formData[field];
        
        if (rule.required && !value) {
            errors[field] = `${rule.label} is required`;
        } else if (value && rule.type === 'email' && !isValidEmail(value)) {
            errors[field] = `${rule.label} is invalid`;
        } else if (value && rule.type === 'phone' && !isValidPhone(value)) {
            errors[field] = `${rule.label} is invalid`;
        } else if (rule.min && value < rule.min) {
            errors[field] = `${rule.label} must be at least ${rule.min}`;
        }
    }
    
    return errors;
}

// ========================================
// DISPLAY & FORMATTING FUNCTIONS
// ========================================

/**
 * Format recommendation for display
 */
function displayRecommendation(rec) {
    const model = rec.recommended_model;
    return `
        <div class="recommendation-card">
            <h3>${model.name}</h3>
            <div class="recommendation-details">
                <div class="detail-item">
                    <span class="label">Price:</span>
                    <span class="value">${formatCurrency(model.base_price)}</span>
                </div>
                <div class="detail-item">
                    <span class="label">Range:</span>
                    <span class="value">${model.range_km} km</span>
                </div>
                <div class="detail-item">
                    <span class="label">Charging Time:</span>
                    <span class="value">${model.charging_time.ac_7kw}h (AC)</span>
                </div>
                <div class="detail-item">
                    <span class="label">Best For:</span>
                    <span class="value">${model.best_for.join(', ')}</span>
                </div>
            </div>
            <div class="recommendation-reasoning">
                <h4>Why This Model?</h4>
                <p>${rec.reasoning}</p>
            </div>
            <div class="ai-insight">
                <h4>🤖 AI Insight</h4>
                <p>${rec.ai_insight}</p>
            </div>
        </div>
    `;
}

/**
 * Display charging station card
 */
function displayChargerCard(station) {
    const speedClass = station.charger_type === 'DC' ? 'fast' : 'slow';
    const speedColor = station.charger_type === 'DC' ? '#00a86b' : '#f39c12';
    
    return `
        <div class="station-card ${speedClass}">
            <div class="station-header">
                <h3>${station.name}</h3>
                <span class="charger-badge ${station.charger_type}">${station.charger_type}</span>
            </div>
            <p class="location">📍 ${station.location}, ${station.city}</p>
            <div class="station-details">
                <div class="detail">
                    <span class="label">Power:</span>
                    <span>${station.power_kw}kW</span>
                </div>
                <div class="detail">
                    <span class="label">Cost:</span>
                    <span>${formatCurrency(station.cost_per_kwh)}/kWh</span>
                </div>
                <div class="detail">
                    <span class="label">Speed:</span>
                    <span>${station.charging_speed}</span>
                </div>
                <div class="detail">
                    <span class="label">Status:</span>
                    <span class="available">${station.availability}</span>
                </div>
            </div>
        </div>
    `;
}

/**
 * Display cost comparison
 */
function displayCostComparison(comparison) {
    const ev = comparison.ev;
    const petrol = comparison.petrol;
    const savings = comparison.savings;
    
    return `
        <div class="comparison-container">
            <div class="cost-box">
                <h3>⛽ Petrol Vehicle</h3>
                <div class="cost-item">
                    <span>Fuel Cost</span>
                    <span>${formatCurrency(petrol.fuel_cost)}</span>
                </div>
                <div class="cost-item">
                    <span>Maintenance</span>
                    <span>${formatCurrency(petrol.maintenance_cost)}</span>
                </div>
                <div class="cost-item total">
                    <span>Total</span>
                    <span>${formatCurrency(petrol.fuel_cost + petrol.maintenance_cost)}</span>
                </div>
            </div>
            <div class="vs-section">VS</div>
            <div class="cost-box highlight">
                <h3>⚡ EV Vehicle</h3>
                <div class="cost-item">
                    <span>Electricity Cost</span>
                    <span>${formatCurrency(ev.electricity_cost)}</span>
                </div>
                <div class="cost-item">
                    <span>Maintenance Savings</span>
                    <span>-${formatCurrency(ev.maintenance_savings)}</span>
                </div>
                <div class="cost-item total">
                    <span>Total</span>
                    <span>${formatCurrency(ev.total_cost)}</span>
                </div>
            </div>
        </div>
        <div class="savings-highlight">
            <h3>💡 You Save</h3>
            <div class="savings-value">${formatCurrency(savings.total_savings)}</div>
            <p>${formatCurrency(savings.monthly_savings)}/month (${savings.savings_percentage.toFixed(1)}% savings)</p>
        </div>
    `;
}

// ========================================
// PAGE INITIALIZATION
// ========================================

/**
 * Initialize page on DOM ready
 */
document.addEventListener('DOMContentLoaded', function() {
    // Populate model selects
    const modelSelects = document.querySelectorAll('select[name="model"]');
    if (modelSelects.length > 0) {
        fetchModels().then(data => {
            modelSelects.forEach(select => {
                select.innerHTML = '';
                data.models.forEach(model => {
                    select.innerHTML += `<option>${model.name}</option>`;
                });
            });
        });
    }
    
    // Set minimum date to today for date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(input => {
        input.min = today;
    });
    
    // Initialize tooltips
    initializeTooltips();
    
    // Add smooth scroll behavior
    addSmoothScroll();
});

/**
 * Initialize tooltips (optional)
 */
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseover', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
        });
        
        element.addEventListener('mouseout', function() {
            const tooltips = document.querySelectorAll('.tooltip');
            tooltips.forEach(t => t.remove());
        });
    });
}

/**
 * Add smooth scroll behavior to internal links
 */
function addSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}

// ========================================
// EXPORT FUNCTIONS FOR TEMPLATES
// ========================================

// Make functions available globally for template usage
window.formatCurrency = formatCurrency;
window.formatNumber = formatNumber;
window.showModal = showModal;
window.closeModal = closeModal;
window.fetchModels = fetchModels;
window.getRecommendation = getRecommendation;
window.calculateRange = calculateRange;
window.compareCosts = compareCosts;
window.fetchChargers = fetchChargers;
window.bookTestDrive = bookTestDrive;
window.sendChatMessage = sendChatMessage;
window.validateForm = validateForm;
