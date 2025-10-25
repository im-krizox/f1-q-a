/* ============================================
   F1 Q&A System - Utility Functions
   Helper functions and constants
   ============================================ */

// Constants
export const CONSTANTS = {
    API_BASE_URL: 'http://localhost:8000',
    API_ENDPOINTS: {
        ASK: '/api/v1/ask',
        HEALTH: '/api/v1/health',
        ENTITIES: '/api/v1/entities',
        EXPLORE: '/api/v1/network/explore'
    },
    MESSAGE_TYPES: {
        USER: 'user',
        ASSISTANT: 'assistant',
        SYSTEM: 'system'
    },
    TYPING_DELAY: 1500,
    MAX_MESSAGE_LENGTH: 500,
    STORAGE_KEYS: {
        MESSAGES: 'f1_qa_messages',
        SETTINGS: 'f1_qa_settings'
    }
};

/**
 * Format a date object to a readable string
 * @param {Date|string} date - Date to format
 * @returns {string} Formatted date string
 */
export function formatDate(date) {
    if (!(date instanceof Date)) {
        date = new Date(date);
    }
    
    const options = {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    return new Intl.DateTimeFormat('es-ES', options).format(date);
}

/**
 * Escape HTML to prevent XSS attacks
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
export function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    
    return text.replace(/[&<>"']/g, (m) => map[m]);
}

/**
 * Debounce function to limit rate of function calls
 * @param {Function} func - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, delay) {
    let timeoutId;
    
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

/**
 * Generate a unique ID
 * @returns {string} Unique ID
 */
export function generateId() {
    return `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Scroll an element to bottom
 * @param {HTMLElement} element - Element to scroll
 * @param {boolean} smooth - Use smooth scrolling
 */
export function scrollToBottom(element, smooth = true) {
    if (!element) return;
    
    if (smooth) {
        element.scrollTo({
            top: element.scrollHeight,
            behavior: 'smooth'
        });
    } else {
        element.scrollTop = element.scrollHeight;
    }
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 * @returns {Promise<boolean>} Success status
 */
export async function copyToClipboard(text) {
    try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(text);
            return true;
        } else {
            // Fallback for older browsers
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            const success = document.execCommand('copy');
            document.body.removeChild(textarea);
            return success;
        }
    } catch (error) {
        console.error('Failed to copy to clipboard:', error);
        return false;
    }
}

/**
 * Highlight code in text (basic implementation)
 * @param {string} text - Text to process
 * @returns {string} HTML with highlighted code
 */
export function highlightCode(text) {
    // Detect code blocks with ```
    return text.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
        return `<pre><code class="language-${lang || 'plaintext'}">${escapeHtml(code)}</code></pre>`;
    });
}

/**
 * Truncate text to a maximum length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export function truncateText(text, maxLength) {
    if (text.length <= maxLength) {
        return text;
    }
    return text.substring(0, maxLength - 3) + '...';
}

/**
 * Validate URL format
 * @param {string} url - URL to validate
 * @returns {boolean} Whether URL is valid
 */
export function validateUrl(url) {
    try {
        new URL(url);
        return true;
    } catch (error) {
        return false;
    }
}

/**
 * Format message text with basic markdown-like formatting
 * @param {string} text - Text to format
 * @returns {string} Formatted HTML
 */
export function formatMessageText(text) {
    let formatted = escapeHtml(text);
    
    // Format URLs
    formatted = formatted.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );
    
    // Format **bold**
    formatted = formatted.replace(
        /\*\*([^*]+)\*\*/g,
        '<strong>$1</strong>'
    );
    
    // Format *italic*
    formatted = formatted.replace(
        /\*([^*]+)\*/g,
        '<em>$1</em>'
    );
    
    // Format line breaks
    formatted = formatted.replace(/\n/g, '<br>');
    
    return formatted;
}

/**
 * Get data from localStorage
 * @param {string} key - Storage key
 * @param {*} defaultValue - Default value if key not found
 * @returns {*} Stored value or default
 */
export function getFromStorage(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
        console.error('Error reading from localStorage:', error);
        return defaultValue;
    }
}

/**
 * Save data to localStorage
 * @param {string} key - Storage key
 * @param {*} value - Value to store
 * @returns {boolean} Success status
 */
export function saveToStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.error('Error saving to localStorage:', error);
        return false;
    }
}

/**
 * Remove data from localStorage
 * @param {string} key - Storage key
 * @returns {boolean} Success status
 */
export function removeFromStorage(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (error) {
        console.error('Error removing from localStorage:', error);
        return false;
    }
}

/**
 * Check if user is online
 * @returns {boolean} Online status
 */
export function isOnline() {
    return navigator.onLine;
}

/**
 * Create a toast notification element
 * @param {string} message - Message to display
 * @param {string} type - Type of notification (success, error, warning, info)
 * @param {number} duration - Duration in milliseconds (0 = no auto-hide)
 * @returns {HTMLElement} Toast element
 */
export function createToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    if (duration > 0) {
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, duration);
    }
    
    return toast;
}

/**
 * Wait for a specified amount of time
 * @param {number} ms - Milliseconds to wait
 * @returns {Promise} Promise that resolves after delay
 */
export function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Sanitize filename for download
 * @param {string} filename - Filename to sanitize
 * @returns {string} Sanitized filename
 */
export function sanitizeFilename(filename) {
    return filename.replace(/[^a-z0-9_\-\.]/gi, '_');
}

/**
 * Calculate confidence level category
 * @param {number} confidence - Confidence score (0-1)
 * @returns {string} Category: 'low', 'medium', or 'high'
 */
export function getConfidenceLevel(confidence) {
    if (confidence >= 0.8) return 'high';
    if (confidence >= 0.5) return 'medium';
    return 'low';
}

/**
 * Log with timestamp
 * @param {...any} args - Arguments to log
 */
export function log(...args) {
    // Enable logs in development (always enabled in browser)
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}]`, ...args);
}

/**
 * Log error with context
 * @param {string} context - Context where error occurred
 * @param {Error} error - Error object
 */
export function logError(context, error) {
    console.error(`[${context}]`, error);
    if (error.stack) {
        console.error('Stack trace:', error.stack);
    }
}

// Export all utilities as default
export default {
    CONSTANTS,
    formatDate,
    escapeHtml,
    debounce,
    generateId,
    scrollToBottom,
    copyToClipboard,
    highlightCode,
    truncateText,
    validateUrl,
    formatMessageText,
    getFromStorage,
    saveToStorage,
    removeFromStorage,
    isOnline,
    createToast,
    sleep,
    sanitizeFilename,
    getConfidenceLevel,
    log,
    logError
};

