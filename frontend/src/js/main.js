/* ============================================
   F1 Q&A System - Main Entry Point
   Application initialization
   ============================================ */

import apiClient from './api-client.js';
import ChatUI from './chat-ui.js';
import { log, logError, createToast } from './utils.js';

/**
 * Main application instance
 */
let chatUI = null;

/**
 * Initialize the application
 */
async function initApp() {
    try {
        log('F1 Q&A System starting...');
        
        // Verify all required DOM elements exist
        const requiredElements = [
            'welcomeScreen',
            'messagesContainer',
            'questionForm',
            'questionInput',
            'sendButton',
            'typingIndicator',
            'infoPanel',
            'relatedEntities',
            'confidenceSection',
            'statusIndicator'
        ];
        
        const missingElements = requiredElements.filter(id => !document.getElementById(id));
        
        if (missingElements.length > 0) {
            throw new Error(`Missing required elements: ${missingElements.join(', ')}`);
        }
        
        // Create ChatUI instance
        chatUI = new ChatUI(apiClient);
        
        // Initialize ChatUI
        await chatUI.init();
        
        // Setup global event handlers
        setupGlobalHandlers(chatUI);
        
        // Setup keyboard shortcuts
        setupKeyboardShortcuts(chatUI);
        
        log('F1 Q&A System initialized successfully ✓');
        
    } catch (error) {
        logError('initApp', error);
        showFatalError(error.message);
    }
}

/**
 * Setup global event handlers
 * @param {ChatUI} chatUI - ChatUI instance
 */
function setupGlobalHandlers(chatUI) {
    // Handle page visibility change
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            log('Page hidden - pausing health checks');
            chatUI.stopHealthChecks();
        } else {
            log('Page visible - resuming health checks');
            chatUI.checkBackendHealth();
            chatUI.startHealthChecks();
        }
    });
    
    // Handle online/offline events (already handled in ChatUI, but log them)
    window.addEventListener('online', () => {
        log('Browser online');
    });
    
    window.addEventListener('offline', () => {
        log('Browser offline');
    });
    
    // Handle unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
        logError('Unhandled Promise Rejection', event.reason);
    });
    
    // Handle global errors
    window.addEventListener('error', (event) => {
        logError('Global Error', event.error);
    });
    
    // Handle before unload (optional - confirm if conversation is active)
    window.addEventListener('beforeunload', (event) => {
        if (chatUI.messages.length > 0) {
            // Uncomment to show confirmation dialog
            // event.preventDefault();
            // event.returnValue = '¿Estás seguro de que quieres salir? Tu conversación se perderá.';
        }
    });
}

/**
 * Setup keyboard shortcuts
 * @param {ChatUI} chatUI - ChatUI instance
 */
function setupKeyboardShortcuts(chatUI) {
    document.addEventListener('keydown', (event) => {
        // Ctrl/Cmd + K: Focus on input
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            chatUI.elements.questionInput.focus();
        }
        
        // Ctrl/Cmd + L: Clear chat
        if ((event.ctrlKey || event.metaKey) && event.key === 'l') {
            event.preventDefault();
            if (confirm('¿Quieres limpiar toda la conversación?')) {
                chatUI.clearMessages();
                createToast('Conversación limpiada', 'success');
            }
        }
        
        // Escape: Cancel typing indicator or blur input
        if (event.key === 'Escape') {
            if (chatUI.isTyping) {
                // Can't really cancel an ongoing request, but hide indicator
                chatUI.hideTypingIndicator();
            } else if (document.activeElement === chatUI.elements.questionInput) {
                chatUI.elements.questionInput.blur();
            }
        }
    });
}

/**
 * Show fatal error screen
 * @param {string} message - Error message
 */
function showFatalError(message) {
    const container = document.querySelector('.container');
    if (container) {
        container.innerHTML = `
            <div style="text-align: center; padding: 60px 20px;">
                <h1 style="color: var(--error-color); font-size: 2rem; margin-bottom: 20px;">
                    ⚠️ Error Fatal
                </h1>
                <p style="color: var(--text-secondary); font-size: 1.2rem; margin-bottom: 20px;">
                    No se pudo inicializar la aplicación.
                </p>
                <div style="background: var(--bg-secondary); padding: 20px; border-radius: 8px; margin: 0 auto; max-width: 600px;">
                    <p style="color: var(--text-primary); font-family: monospace;">
                        ${message}
                    </p>
                </div>
                <button onclick="location.reload()" style="margin-top: 30px; padding: 12px 24px; background: var(--primary-color); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 1rem;">
                    Recargar Página
                </button>
            </div>
        `;
    }
}

/**
 * Show loading screen while initializing
 */
function showLoadingScreen() {
    const container = document.querySelector('.container');
    if (container) {
        container.innerHTML = `
            <div style="display: flex; justify-content: center; align-items: center; height: 60vh; flex-direction: column;">
                <div class="spinner"></div>
                <p style="margin-top: 20px; color: var(--text-secondary);">
                    Cargando F1 Q&A System...
                </p>
            </div>
        `;
    }
}

/**
 * Check if browser is supported
 * @returns {boolean} Whether browser is supported
 */
function isBrowserSupported() {
    // Check for required features
    const requiredFeatures = [
        'fetch',
        'Promise',
        'localStorage',
        'addEventListener'
    ];
    
    return requiredFeatures.every(feature => feature in window);
}

/**
 * Show browser not supported message
 */
function showBrowserNotSupported() {
    const container = document.querySelector('.container');
    if (container) {
        container.innerHTML = `
            <div style="text-align: center; padding: 60px 20px;">
                <h1 style="color: var(--warning-color); font-size: 2rem; margin-bottom: 20px;">
                    ⚠️ Navegador No Soportado
                </h1>
                <p style="color: var(--text-secondary); font-size: 1.2rem;">
                    Por favor, utiliza un navegador moderno como Chrome, Firefox, Safari o Edge.
                </p>
            </div>
        `;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
    // Check browser support
    if (!isBrowserSupported()) {
        showBrowserNotSupported();
        return;
    }
    
    // Show loading screen briefly
    // showLoadingScreen();
    
    // Initialize app
    await initApp();
});

// Export for testing/debugging (optional)
if (typeof window !== 'undefined') {
    window.chatUI = chatUI;
    window.apiClient = apiClient;
}

export { chatUI, apiClient };

