/* ============================================
   F1 Q&A System - Chat UI
   Manages the chat interface and user interactions
   ============================================ */

import { 
    CONSTANTS, 
    formatDate, 
    generateId, 
    scrollToBottom, 
    formatMessageText,
    getFromStorage,
    saveToStorage,
    createToast,
    getConfidenceLevel,
    log,
    logError
} from './utils.js';

/**
 * ChatUI class - Manages the chat interface
 */
class ChatUI {
    /**
     * Create a ChatUI instance
     * @param {APIClient} apiClient - API client instance
     */
    constructor(apiClient) {
        this.apiClient = apiClient;
        this.messages = [];
        this.elements = {};
        this.isTyping = false;
        this.connectionStatus = 'checking';
        this.healthCheckInterval = null;
    }

    /**
     * Initialize the chat UI
     */
    async init() {
        log('Initializing ChatUI...');
        
        // Get DOM element references
        this.getElements();
        
        // Bind event listeners
        this.bindEvents();
        
        // Check backend health
        await this.checkBackendHealth();
        
        // Start periodic health checks
        this.startHealthChecks();
        
        // Load saved messages (optional)
        // this.loadMessagesFromStorage();
        
        log('ChatUI initialized successfully');
    }

    /**
     * Get references to DOM elements
     */
    getElements() {
        this.elements = {
            welcomeScreen: document.getElementById('welcomeScreen'),
            messagesContainer: document.getElementById('messagesContainer'),
            questionForm: document.getElementById('questionForm'),
            questionInput: document.getElementById('questionInput'),
            sendButton: document.getElementById('sendButton'),
            typingIndicator: document.getElementById('typingIndicator'),
            infoPanel: document.getElementById('infoPanel'),
            relatedEntities: document.getElementById('relatedEntities'),
            confidenceSection: document.getElementById('confidenceSection'),
            confidenceFill: document.getElementById('confidenceFill'),
            confidenceText: document.getElementById('confidenceText'),
            statusIndicator: document.getElementById('statusIndicator')
        };
        
        // Verify all elements exist
        for (const [key, element] of Object.entries(this.elements)) {
            if (!element) {
                console.error(`Element not found: ${key}`);
            }
        }
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Form submission
        this.elements.questionForm.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Example questions clicks
        const exampleItems = document.querySelectorAll('.example-item');
        exampleItems.forEach(item => {
            item.addEventListener('click', () => {
                const question = item.getAttribute('data-question');
                this.handleExampleClick(question);
            });
        });
        
        // Input validation
        this.elements.questionInput.addEventListener('input', (e) => {
            const length = e.target.value.length;
            if (length > CONSTANTS.MAX_MESSAGE_LENGTH) {
                e.target.value = e.target.value.substring(0, CONSTANTS.MAX_MESSAGE_LENGTH);
            }
        });
        
        // Online/offline events
        window.addEventListener('online', () => {
            createToast('Conexión restaurada', 'success');
            this.checkBackendHealth();
        });
        
        window.addEventListener('offline', () => {
            createToast('Sin conexión a internet', 'error');
            this.updateConnectionStatus('error');
        });
    }

    /**
     * Handle form submission
     * @param {Event} event - Submit event
     */
    async handleSubmit(event) {
        event.preventDefault();
        
        const question = this.elements.questionInput.value.trim();
        
        // Validate input
        if (!question) {
            return;
        }
        
        if (question.length > CONSTANTS.MAX_MESSAGE_LENGTH) {
            createToast(`La pregunta es demasiado larga (máx. ${CONSTANTS.MAX_MESSAGE_LENGTH} caracteres)`, 'warning');
            return;
        }
        
        // Disable input while processing
        this.disableInput();
        
        // Clear input
        this.elements.questionInput.value = '';
        
        // Hide welcome screen
        this.hideWelcomeScreen();
        
        // Add user message
        this.addMessage(question, CONSTANTS.MESSAGE_TYPES.USER);
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Call API
            log('Sending question:', question);
            const response = await this.apiClient.askQuestion(question);
            log('Received response:', response);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Add assistant response
            this.addMessage(response.answer, CONSTANTS.MESSAGE_TYPES.ASSISTANT, {
                confidence: response.confidence,
                relatedEntities: response.related_entities,
                queryType: response.query_type
            });
            
            // Update info panel
            this.updateInfoPanel(response);
            
        } catch (error) {
            logError('handleSubmit', error);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Show error message
            this.showError(error.message || 'Error al procesar tu pregunta');
            
        } finally {
            // Re-enable input
            this.enableInput();
            this.elements.questionInput.focus();
        }
    }

    /**
     * Add a message to the chat
     * @param {string} text - Message text
     * @param {string} type - Message type (user, assistant, system)
     * @param {Object} metadata - Additional metadata
     */
    addMessage(text, type, metadata = {}) {
        const message = {
            id: generateId(),
            text: text,
            type: type,
            timestamp: new Date(),
            metadata: metadata
        };
        
        this.messages.push(message);
        this.renderMessage(message);
        
        // Save to storage (optional)
        // this.saveMessagesToStorage();
    }

    /**
     * Render a message in the chat
     * @param {Object} message - Message object
     */
    renderMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${message.type}`;
        messageDiv.id = `message-${message.id}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        // Format text
        const formattedText = formatMessageText(message.text);
        
        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.innerHTML = formattedText;
        
        const metaDiv = document.createElement('div');
        metaDiv.className = 'message-metadata';
        metaDiv.textContent = formatDate(message.timestamp);
        
        bubble.appendChild(textDiv);
        bubble.appendChild(metaDiv);
        messageDiv.appendChild(bubble);
        
        // Add to container with animation
        messageDiv.style.opacity = '0';
        messageDiv.style.transform = 'translateY(10px)';
        
        this.elements.messagesContainer.appendChild(messageDiv);
        
        // Trigger animation
        requestAnimationFrame(() => {
            messageDiv.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            messageDiv.style.opacity = '1';
            messageDiv.style.transform = 'translateY(0)';
        });
        
        // Scroll to bottom
        scrollToBottom(this.elements.messagesContainer);
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        this.isTyping = true;
        this.elements.typingIndicator.style.display = 'flex';
        scrollToBottom(this.elements.messagesContainer);
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        this.isTyping = false;
        this.elements.typingIndicator.style.display = 'none';
    }

    /**
     * Update info panel with response data
     * @param {Object} data - Response data
     */
    updateInfoPanel(data) {
        // Clear previous content
        this.elements.relatedEntities.innerHTML = '';
        
        // Show related entities
        if (data.related_entities && data.related_entities.length > 0) {
            data.related_entities.forEach(entity => {
                const card = this.createEntityCard(entity);
                this.elements.relatedEntities.appendChild(card);
            });
        } else {
            this.elements.relatedEntities.innerHTML = '<p class="empty-state">No hay entidades relacionadas</p>';
        }
        
        // Update confidence meter
        if (typeof data.confidence === 'number') {
            this.updateConfidenceMeter(data.confidence);
            this.elements.confidenceSection.style.display = 'block';
        } else {
            this.elements.confidenceSection.style.display = 'none';
        }
    }

    /**
     * Create an entity card element
     * @param {Object} entity - Entity data
     * @returns {HTMLElement} Entity card element
     */
    createEntityCard(entity) {
        const card = document.createElement('div');
        card.className = 'entity-card';
        
        const label = document.createElement('div');
        label.className = 'entity-label';
        label.textContent = entity.type || 'Entidad';
        
        const value = document.createElement('div');
        value.className = 'entity-value';
        value.textContent = entity.name || entity.value || 'N/A';
        
        card.appendChild(label);
        card.appendChild(value);
        
        return card;
    }

    /**
     * Update confidence meter
     * @param {number} confidence - Confidence score (0-1)
     */
    updateConfidenceMeter(confidence) {
        const percentage = Math.round(confidence * 100);
        const level = getConfidenceLevel(confidence);
        
        // Update width
        this.elements.confidenceFill.style.width = `${percentage}%`;
        
        // Update class for color
        this.elements.confidenceFill.className = `confidence-fill ${level}`;
        
        // Update text
        this.elements.confidenceText.textContent = `${percentage}% de confianza`;
    }

    /**
     * Show error message
     * @param {string} message - Error message
     */
    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        this.elements.messagesContainer.appendChild(errorDiv);
        scrollToBottom(this.elements.messagesContainer);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => {
                    if (errorDiv.parentNode) {
                        errorDiv.parentNode.removeChild(errorDiv);
                    }
                }, 300);
            }
        }, 5000);
    }

    /**
     * Hide welcome screen
     */
    hideWelcomeScreen() {
        if (this.elements.welcomeScreen && this.elements.welcomeScreen.style.display !== 'none') {
            this.elements.welcomeScreen.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                this.elements.welcomeScreen.style.display = 'none';
            }, 300);
        }
    }

    /**
     * Check backend health
     */
    async checkBackendHealth() {
        try {
            log('Checking backend health...');
            const health = await this.apiClient.checkHealth();
            
            if (health.status === 'ok' || health.status === 'healthy') {
                this.updateConnectionStatus('connected');
                log('Backend is healthy:', health);
            } else {
                this.updateConnectionStatus('warning');
            }
            
        } catch (error) {
            logError('checkBackendHealth', error);
            this.updateConnectionStatus('error');
            
            // Disable input if backend is down
            this.disableInput();
        }
    }

    /**
     * Start periodic health checks
     */
    startHealthChecks() {
        // Check every 30 seconds
        this.healthCheckInterval = setInterval(() => {
            this.checkBackendHealth();
        }, 30000);
    }

    /**
     * Stop periodic health checks
     */
    stopHealthChecks() {
        if (this.healthCheckInterval) {
            clearInterval(this.healthCheckInterval);
            this.healthCheckInterval = null;
        }
    }

    /**
     * Update connection status indicator
     * @param {string} status - Status: 'connected', 'error', 'checking', 'warning'
     */
    updateConnectionStatus(status) {
        this.connectionStatus = status;
        
        const statusText = {
            connected: 'Conectado',
            error: 'Desconectado',
            checking: 'Verificando...',
            warning: 'Conexión inestable'
        };
        
        const statusDot = this.elements.statusIndicator.querySelector('.status-dot');
        const statusTextEl = this.elements.statusIndicator.querySelector('.status-text');
        
        this.elements.statusIndicator.className = `status-indicator ${status}`;
        statusTextEl.textContent = statusText[status] || 'Desconocido';
        
        // Enable/disable input based on status
        if (status === 'connected') {
            this.enableInput();
        } else if (status === 'error') {
            this.disableInput();
        }
    }

    /**
     * Enable input controls
     */
    enableInput() {
        this.elements.questionInput.disabled = false;
        this.elements.sendButton.disabled = false;
    }

    /**
     * Disable input controls
     */
    disableInput() {
        this.elements.questionInput.disabled = true;
        this.elements.sendButton.disabled = true;
    }

    /**
     * Handle example question click
     * @param {string} question - Example question text
     */
    handleExampleClick(question) {
        this.elements.questionInput.value = question;
        this.elements.questionForm.dispatchEvent(new Event('submit'));
    }

    /**
     * Clear all messages
     */
    clearMessages() {
        this.messages = [];
        this.elements.messagesContainer.innerHTML = '';
        this.elements.welcomeScreen.style.display = 'flex';
        this.elements.relatedEntities.innerHTML = '<p class="empty-state">Las entidades relacionadas aparecerán aquí</p>';
        this.elements.confidenceSection.style.display = 'none';
        
        // Clear storage
        saveToStorage(CONSTANTS.STORAGE_KEYS.MESSAGES, []);
    }

    /**
     * Load messages from storage
     */
    loadMessagesFromStorage() {
        const savedMessages = getFromStorage(CONSTANTS.STORAGE_KEYS.MESSAGES, []);
        
        if (savedMessages.length > 0) {
            this.hideWelcomeScreen();
            
            // Render saved messages (limit to last 50)
            savedMessages.slice(-50).forEach(message => {
                this.messages.push(message);
                this.renderMessage(message);
            });
        }
    }

    /**
     * Save messages to storage
     */
    saveMessagesToStorage() {
        saveToStorage(CONSTANTS.STORAGE_KEYS.MESSAGES, this.messages);
    }

    /**
     * Destroy and cleanup
     */
    destroy() {
        this.stopHealthChecks();
        this.messages = [];
        log('ChatUI destroyed');
    }
}

export default ChatUI;

