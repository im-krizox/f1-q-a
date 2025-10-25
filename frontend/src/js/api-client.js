/* ============================================
   F1 Q&A System - API Client
   Handles communication with the backend API
   ============================================ */

import { CONSTANTS, logError } from './utils.js';

/**
 * API Client class for communicating with the F1 Q&A backend
 */
class APIClient {
    /**
     * Create an API client instance
     * @param {string} baseURL - Base URL for the API
     */
    constructor(baseURL) {
        this.baseURL = baseURL;
        this.headers = {
            'Content-Type': 'application/json'
        };
        this.timeout = 30000; // 30 seconds
    }

    /**
     * Generic request method
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Fetch options
     * @returns {Promise<Object>} Response data
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        // Setup timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);
        
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...this.headers,
                    ...options.headers
                },
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            // Check if response is ok
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }
            
            // Parse JSON response
            const data = await response.json();
            return data;
            
        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                throw new Error('La solicitud tardó demasiado tiempo');
            }
            
            if (error instanceof TypeError && error.message.includes('fetch')) {
                throw new Error('Error de conexión: No se puede conectar al servidor');
            }
            
            throw error;
        }
    }

    /**
     * Ask a question to the backend
     * @param {string} question - Question to ask
     * @returns {Promise<Object>} Answer response
     */
    async askQuestion(question) {
        try {
            const response = await this.request(CONSTANTS.API_ENDPOINTS.ASK, {
                method: 'POST',
                body: JSON.stringify({ question })
            });
            
            return response;
            
        } catch (error) {
            logError('askQuestion', error);
            
            // Provide user-friendly error messages
            if (error.message.includes('400')) {
                throw new Error('Pregunta inválida. Por favor, reformula tu pregunta.');
            } else if (error.message.includes('500')) {
                throw new Error('Error del servidor. Por favor, intenta de nuevo más tarde.');
            } else if (error.message.includes('conexión')) {
                throw new Error('No se puede conectar al servidor. Verifica tu conexión.');
            }
            
            throw error;
        }
    }

    /**
     * Check backend health status
     * @returns {Promise<Object>} Health response
     */
    async checkHealth() {
        try {
            const response = await this.request(CONSTANTS.API_ENDPOINTS.HEALTH, {
                method: 'GET'
            });
            
            return response;
            
        } catch (error) {
            logError('checkHealth', error);
            throw new Error('No se puede verificar el estado del servidor');
        }
    }

    /**
     * Get entities of a specific type
     * @param {string} entityType - Type of entity (drivers, teams, circuits, sessions)
     * @param {Object} filters - Optional filters
     * @returns {Promise<Array>} List of entities
     */
    async getEntities(entityType, filters = {}) {
        try {
            const queryParams = new URLSearchParams(filters);
            const endpoint = `${CONSTANTS.API_ENDPOINTS.ENTITIES}/${entityType}?${queryParams}`;
            
            const response = await this.request(endpoint, {
                method: 'GET'
            });
            
            return response;
            
        } catch (error) {
            logError('getEntities', error);
            throw new Error(`No se pudieron obtener las entidades de tipo: ${entityType}`);
        }
    }

    /**
     * Explore network around a node
     * @param {string} nodeId - Node ID to explore
     * @param {number} depth - Depth of exploration
     * @returns {Promise<Object>} Network exploration result
     */
    async exploreNetwork(nodeId, depth = 2) {
        try {
            const endpoint = `${CONSTANTS.API_ENDPOINTS.EXPLORE}/${nodeId}?depth=${depth}`;
            
            const response = await this.request(endpoint, {
                method: 'GET'
            });
            
            return response;
            
        } catch (error) {
            logError('exploreNetwork', error);
            throw new Error('No se pudo explorar la red semántica');
        }
    }

    /**
     * Handle and format errors
     * @param {Error} error - Error object
     * @returns {Object} Formatted error object
     */
    handleError(error) {
        const errorObj = {
            message: error.message || 'Error desconocido',
            type: 'unknown',
            statusCode: null
        };
        
        if (error.message.includes('conexión') || error.message.includes('fetch')) {
            errorObj.type = 'network';
        } else if (error.message.includes('500')) {
            errorObj.type = 'server';
            errorObj.statusCode = 500;
        } else if (error.message.includes('400')) {
            errorObj.type = 'client';
            errorObj.statusCode = 400;
        }
        
        return errorObj;
    }

    /**
     * Set authentication token (for future use)
     * @param {string} token - Authentication token
     */
    setAuthToken(token) {
        if (token) {
            this.headers['Authorization'] = `Bearer ${token}`;
        } else {
            delete this.headers['Authorization'];
        }
    }

    /**
     * Set custom timeout
     * @param {number} ms - Timeout in milliseconds
     */
    setTimeout(ms) {
        this.timeout = ms;
    }

    /**
     * Get current timeout value
     * @returns {number} Current timeout in milliseconds
     */
    getTimeout() {
        return this.timeout;
    }

    /**
     * Test connection to backend
     * @returns {Promise<boolean>} Connection status
     */
    async testConnection() {
        try {
            await this.checkHealth();
            return true;
        } catch (error) {
            return false;
        }
    }
}

// Create and export singleton instance
const apiClient = new APIClient(CONSTANTS.API_BASE_URL);

export default apiClient;
export { APIClient };

