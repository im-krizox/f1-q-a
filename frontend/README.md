# 🏎️ F1 Q&A System - Frontend

[![HTML5](https://img.shields.io/badge/HTML5-Modern-orange.svg)](https://developer.mozilla.org/es/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-Flexbox%20%26%20Grid-blue.svg)](https://developer.mozilla.org/es/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow.svg)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![Nginx](https://img.shields.io/badge/Nginx-1.25-green.svg)](https://nginx.org/)

Interfaz web moderna, responsive y sin frameworks para el Sistema de Preguntas y Respuestas sobre Fórmula 1 con Redes Semánticas.

## 📋 Descripción

Frontend **sin dependencias** desarrollado con tecnologías web nativas (HTML5, CSS3 y JavaScript ES6+) que proporciona una interfaz de chat intuitiva y elegante para interactuar con el backend de análisis semántico de F1.

### ¿Por qué Sin Frameworks?

Esta decisión fue intencional y trae varios beneficios:

- ✅ **Carga instantánea**: Sin megabytes de librerías
- ✅ **Sin build steps**: No webpack, vite, ni npm
- ✅ **Código comprensible**: Fácil de entender y modificar
- ✅ **Mantenibilidad**: Sin dependencias que actualizar
- ✅ **Rendimiento**: JavaScript puro optimizado
- ✅ **Educativo**: Perfecto para aprender fundamentos web

## 🏗️ Arquitectura

```
frontend/
├── public/
│   └── index.html          # Página principal
├── src/
│   ├── css/
│   │   ├── main.css        # Estilos globales y variables
│   │   ├── chat.css        # Estilos de la interfaz de chat
│   │   └── components.css  # Componentes reutilizables
│   ├── js/
│   │   ├── utils.js        # Funciones utilitarias
│   │   ├── api-client.js   # Cliente HTTP para el backend
│   │   ├── chat-ui.js      # Lógica de la interfaz de chat
│   │   └── main.js         # Punto de entrada de la aplicación
│   └── assets/
│       ├── images/
│       └── icons/
├── nginx.conf              # Configuración de Nginx
├── Dockerfile              # Imagen Docker para producción
└── README.md
```

## 🚀 Características

- **Interfaz de Chat Moderna**: Diseño limpio e intuitivo similar a aplicaciones de mensajería
- **Responsive Design**: Funciona perfectamente en desktop, tablet y móvil
- **Real-time Updates**: Indicadores visuales de estado y typing
- **Panel de Información**: Muestra entidades relacionadas y nivel de confianza
- **Preguntas de Ejemplo**: Sugerencias interactivas para comenzar
- **Manejo de Errores**: Feedback visual claro para el usuario
- **Validación de Conexión**: Health checks automáticos del backend
- **Accesibilidad**: Implementación de ARIA labels y navegación por teclado

## 🎨 Tecnologías

- HTML5 (Semantic markup)
- CSS3 (Variables CSS, Flexbox, Grid, Animations)
- JavaScript ES6+ (Modules, Async/Await, Fetch API)
- Nginx (Servidor web de producción)
- Docker (Containerización)

## 📦 Instalación

### Desarrollo Local

Para ejecutar el frontend localmente sin Docker:

```bash
# 1. Navegar al directorio frontend
cd frontend

# 2. Servir con un servidor HTTP simple
python -m http.server 8080
# O con Node.js
npx http-server public -p 8080

# 3. Abrir en el navegador
# http://localhost:8080
```

**Nota**: Asegúrate de que el backend esté corriendo en `http://localhost:8000`

### Con Docker

```bash
# Construir la imagen
docker build -t f1-qa-frontend .

# Ejecutar el contenedor
docker run -d -p 80:80 --name f1-qa-frontend f1-qa-frontend

# Acceder a la aplicación
# http://localhost
```

### Con Docker Compose (Recomendado)

Desde la raíz del proyecto:

```bash
# Iniciar ambos servicios (backend + frontend)
docker-compose up -d

# Ver logs
docker-compose logs -f frontend

# Detener servicios
docker-compose down
```

## 🔧 Configuración

### Variables de API

El endpoint del backend se configura en `src/js/utils.js`:

```javascript
export const CONSTANTS = {
    API_BASE_URL: 'http://localhost:8000',
    // ...
};
```

Para producción, modifica esta URL o utiliza variables de entorno.

### Nginx

La configuración de Nginx en `nginx.conf` incluye:

- Proxy reverso para el backend
- Compresión gzip
- Headers de seguridad
- Caché de assets estáticos
- Health check endpoint

## 📱 Uso

### Interfaz Principal

1. **Pantalla de Bienvenida**: Muestra ejemplos de preguntas al cargar
2. **Campo de Entrada**: Escribe tu pregunta sobre F1
3. **Chat**: Visualiza el historial de conversación
4. **Panel de Información**: Entidades relacionadas y nivel de confianza

### Ejemplos de Preguntas

- "¿Quién es Max Verstappen?"
- "¿Para qué equipo corre Lewis Hamilton?"
- "¿Quién ganó el GP de Mónaco 2024?"
- "¿Qué motor usa Red Bull?"
- "¿Dónde está el circuito de Spa?"

### Atajos de Teclado

- `Ctrl/Cmd + K`: Enfocar el campo de entrada
- `Ctrl/Cmd + L`: Limpiar la conversación
- `Escape`: Cancelar/Desenfocar

## 🔍 Estructura del Código

### utils.js

Funciones utilitarias y constantes:
- Formateo de fechas
- Escape de HTML
- Debouncing
- Manejo de localStorage
- Generación de IDs únicos

### api-client.js

Cliente HTTP para comunicación con el backend:
- Método genérico `request()`
- `askQuestion()`: Enviar pregunta
- `checkHealth()`: Verificar estado del backend
- Manejo de timeouts y errores

### chat-ui.js

Lógica principal de la interfaz:
- Renderizado de mensajes
- Manejo de eventos
- Actualización del panel de información
- Health checks periódicos
- Estado de la conexión

### main.js

Punto de entrada de la aplicación:
- Inicialización de componentes
- Event listeners globales
- Keyboard shortcuts
- Manejo de errores fatales

## 🎨 Personalización

### Colores y Tema

Los colores se definen como variables CSS en `src/css/main.css`:

```css
:root {
    --primary-color: #E10600;      /* Rojo F1 */
    --secondary-color: #15151E;    /* Negro F1 */
    --accent-color: #00D9FF;       /* Cyan tecnológico */
    /* ... más variables */
}
```

Modifica estas variables para cambiar el tema completo.

### Componentes CSS

Todos los componentes están en `src/css/components.css`:
- Entity cards
- Confidence meter
- Badges
- Toasts
- Alerts
- Tooltips

## 🧪 Testing

### Pruebas Manuales

1. Verificar que la interfaz carga correctamente
2. Probar envío de preguntas
3. Verificar respuestas del backend
4. Comprobar manejo de errores
5. Validar responsive design en diferentes dispositivos

### Health Check

El endpoint `/health` de Nginx retorna:
```
GET http://localhost/health
Response: OK
```

## 🐛 Debugging

### Console Logs

La aplicación incluye logging detallado en desarrollo:

```javascript
// Habilitar logs en utils.js
export function log(...args) {
    // Logs están deshabilitados en producción
    console.log(`[${timestamp}]`, ...args);
}
```

### Herramientas de Desarrollo

- **Browser DevTools**: Console, Network, Elements
- **Nginx Logs**: `docker logs f1-qa-frontend`
- **Network Tab**: Verificar requests al backend

## 📊 Performance

### Optimizaciones Implementadas

- **Gzip Compression**: Archivos comprimidos por Nginx
- **Asset Caching**: Caché de 1 año para assets estáticos
- **Debouncing**: En inputs para evitar requests excesivos
- **Lazy Loading**: Componentes se cargan bajo demanda
- **Minified Assets**: En producción (opcional)

## 🔒 Seguridad

### Headers Implementados

- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: no-referrer-when-downgrade`

### Validación

- Escape de HTML para prevenir XSS
- Validación de inputs
- CORS configurado en el backend
- Sanitización de URLs

## 🌐 Navegadores Soportados

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

**Características requeridas**:
- Fetch API
- ES6 Modules
- CSS Grid/Flexbox
- LocalStorage

## 📝 Notas de Desarrollo

### Arquitectura Sin Build

Esta aplicación **no requiere** build steps (webpack, vite, etc.):
- JavaScript vanilla con ES6 modules
- CSS puro sin preprocesadores
- Sin dependencias de npm

Esto simplifica el desarrollo y deployment.

### Extensiones Futuras

Posibles mejoras:
- Dark mode
- Exportar conversaciones
- Voice input
- Markdown en respuestas
- Historial persistente
- PWA capabilities

## 🧠 Arquitectura Técnica Detallada

### Estructura de Módulos JavaScript

El código JavaScript está organizado en 4 módulos ES6:

```
src/js/
├── utils.js         # Funciones utilitarias y constantes
├── api-client.js    # Cliente HTTP para backend
├── chat-ui.js       # Lógica de la interfaz de chat
└── main.js          # Punto de entrada y orquestación
```

### 1. utils.js - Utilidades y Constantes

**Propósito**: Funciones reutilizables y configuración global

```javascript
// Constantes de configuración
export const CONSTANTS = {
    API_BASE_URL: 'http://localhost:8000',
    API_TIMEOUT: 30000,
    HEALTH_CHECK_INTERVAL: 30000
};

// Formateo de fechas
export function formatDate(date) {
    return new Date(date).toLocaleString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Escape HTML para prevenir XSS
export function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Debouncing para inputs
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

// Generador de IDs únicos
export function generateId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}
```

**Funciones principales**:
- `formatDate()`: Formato de hora español
- `escapeHtml()`: Prevención de XSS
- `debounce()`: Optimización de eventos
- `generateId()`: IDs únicos para mensajes
- `localStorage` helpers: Persistencia local

### 2. api-client.js - Cliente HTTP

**Propósito**: Comunicación con el backend

```javascript
class APIClient {
    constructor(baseURL, timeout = 30000) {
        this.baseURL = baseURL;
        this.timeout = timeout;
    }

    // Método genérico con timeout
    async request(endpoint, options = {}) {
        const controller = new AbortController();
        const timeoutId = setTimeout(
            () => controller.abort(),
            this.timeout
        );

        try {
            const response = await fetch(
                `${this.baseURL}${endpoint}`,
                {
                    ...options,
                    signal: controller.signal,
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    }
                }
            );
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error('Timeout: El servidor tardó demasiado');
            }
            throw error;
        }
    }

    // Enviar pregunta
    async askQuestion(question, context = {}) {
        return this.request('/api/v1/ask', {
            method: 'POST',
            body: JSON.stringify({ question, context })
        });
    }

    // Health check
    async checkHealth() {
        return this.request('/api/v1/health');
    }
}

export default APIClient;
```

**Características**:
- ✅ Timeout configurable con `AbortController`
- ✅ Manejo de errores HTTP
- ✅ Headers automáticos
- ✅ Métodos específicos por endpoint
- ✅ Retries opcionales (implementable)

### 3. chat-ui.js - Interfaz de Chat

**Propósito**: Manejo de la UI y eventos de chat

**Componentes principales**:

#### A) Renderizado de Mensajes

```javascript
class ChatUI {
    renderMessage(message, isBot = false) {
        const messageEl = document.createElement('div');
        messageEl.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
        
        messageEl.innerHTML = `
            <div class="message-content">
                <div class="message-avatar">
                    ${isBot ? '🤖' : '👤'}
                </div>
                <div class="message-bubble">
                    <p>${escapeHtml(message.text)}</p>
                    <span class="message-time">
                        ${formatDate(message.timestamp)}
                    </span>
                </div>
            </div>
        `;
        
        this.messagesContainer.appendChild(messageEl);
        this.scrollToBottom();
    }
}
```

#### B) Indicador de Typing

```javascript
showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = `
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    this.messagesContainer.appendChild(indicator);
}
```

#### C) Panel de Información

```javascript
updateInfoPanel(response) {
    const infoPanel = document.getElementById('info-panel');
    
    // Mostrar confianza
    this.renderConfidence(response.confidence);
    
    // Mostrar entidades relacionadas
    if (response.related_entities) {
        this.renderRelatedEntities(response.related_entities);
    }
    
    // Mostrar metadata
    if (response.metadata) {
        this.renderMetadata(response.metadata);
    }
}
```

#### D) Health Checks Periódicos

```javascript
startHealthChecks() {
    this.healthCheckInterval = setInterval(async () => {
        try {
            await this.apiClient.checkHealth();
            this.updateConnectionStatus('online');
        } catch (error) {
            this.updateConnectionStatus('offline');
        }
    }, 30000); // Cada 30 segundos
}
```

### 4. main.js - Orquestación

**Propósito**: Inicialización y coordinación global

```javascript
import APIClient from './api-client.js';
import ChatUI from './chat-ui.js';
import { CONSTANTS } from './utils.js';

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Crear instancias
        const apiClient = new APIClient(CONSTANTS.API_BASE_URL);
        const chatUI = new ChatUI(apiClient);
        
        // Inicializar UI
        await chatUI.init();
        
        // Configurar event listeners globales
        setupGlobalEventListeners(chatUI);
        
        // Atajos de teclado
        setupKeyboardShortcuts(chatUI);
        
        // Health check inicial
        await checkBackendHealth(apiClient);
        
    } catch (error) {
        console.error('Error de inicialización:', error);
        showFatalError(error);
    }
});

// Atajos de teclado
function setupKeyboardShortcuts(chatUI) {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K: Focus input
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            chatUI.focusInput();
        }
        
        // Ctrl/Cmd + L: Limpiar chat
        if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
            e.preventDefault();
            chatUI.clearChat();
        }
        
        // Escape: Cancelar
        if (e.key === 'Escape') {
            chatUI.handleEscape();
        }
    });
}
```

---

## 🎨 Sistema de Diseño CSS

### Variables CSS (Custom Properties)

Todas las variables están definidas en `main.css`:

```css
:root {
    /* Colores principales - Tema F1 */
    --primary-color: #E10600;        /* Rojo F1 oficial */
    --secondary-color: #15151E;      /* Negro F1 */
    --accent-color: #00D9FF;         /* Cyan tecnológico */
    
    /* Grises */
    --gray-50: #F9FAFB;
    --gray-100: #F3F4F6;
    --gray-200: #E5E7EB;
    --gray-700: #374151;
    --gray-900: #111827;
    
    /* Semánticos */
    --success-color: #10B981;
    --warning-color: #F59E0B;
    --error-color: #EF4444;
    --info-color: #3B82F6;
    
    /* Tipografía */
    --font-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-mono: 'SF Mono', Monaco, 'Cascadia Code', monospace;
    
    /* Espaciado */
    --spacing-xs: 0.25rem;   /* 4px */
    --spacing-sm: 0.5rem;    /* 8px */
    --spacing-md: 1rem;      /* 16px */
    --spacing-lg: 1.5rem;    /* 24px */
    --spacing-xl: 2rem;      /* 32px */
    
    /* Sombras */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    
    /* Animaciones */
    --transition-fast: 150ms ease-in-out;
    --transition-base: 300ms ease-in-out;
    --transition-slow: 500ms ease-in-out;
    
    /* Z-index */
    --z-dropdown: 1000;
    --z-sticky: 1020;
    --z-modal: 1050;
    --z-tooltip: 1070;
}
```

### Arquitectura CSS

```
src/css/
├── main.css         # Variables, reset, utilidades
├── chat.css         # Interfaz de chat específica
└── components.css   # Componentes reutilizables
```

**Metodología**: BEM (Block Element Modifier) adaptado

```css
/* Block */
.message { }

/* Element */
.message__content { }
.message__avatar { }
.message__bubble { }

/* Modifier */
.message--bot { }
.message--user { }
.message--error { }
```

### Componentes CSS Reutilizables

#### Card Component

```css
.card {
    background: white;
    border-radius: 8px;
    box-shadow: var(--shadow-md);
    padding: var(--spacing-md);
    transition: var(--transition-base);
}

.card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
}
```

#### Badge Component

```css
.badge {
    display: inline-flex;
    align-items: center;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
}

.badge--success { background: var(--success-color); color: white; }
.badge--warning { background: var(--warning-color); color: white; }
.badge--error { background: var(--error-color); color: white; }
```

#### Confidence Meter

```css
.confidence-meter {
    position: relative;
    width: 100%;
    height: 8px;
    background: var(--gray-200);
    border-radius: 4px;
    overflow: hidden;
}

.confidence-meter__fill {
    height: 100%;
    background: linear-gradient(90deg, 
        var(--error-color) 0%, 
        var(--warning-color) 50%, 
        var(--success-color) 100%
    );
    transition: width var(--transition-base);
}
```

### Responsive Design

```css
/* Mobile First */
.container {
    padding: var(--spacing-sm);
}

/* Tablet (768px+) */
@media (min-width: 768px) {
    .container {
        padding: var(--spacing-md);
    }
    
    .chat-layout {
        display: grid;
        grid-template-columns: 1fr 300px;
        gap: var(--spacing-lg);
    }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: var(--spacing-lg);
    }
}

/* Large Desktop (1440px+) */
@media (min-width: 1440px) {
    .container {
        max-width: 1400px;
    }
}
```

### Animaciones CSS

#### Typing Indicator

```css
@keyframes typing-dot {
    0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.7;
    }
    30% {
        transform: translateY(-10px);
        opacity: 1;
    }
}

.typing-dots span {
    animation: typing-dot 1.4s infinite;
}

.typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
}
```

#### Fade In Animation

```css
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message {
    animation: fadeIn var(--transition-base) ease-out;
}
```

---

## 🔧 Configuración de Nginx

**Archivo**: `nginx.conf`

### Características Implementadas

#### 1. Reverse Proxy al Backend

```nginx
location /api/ {
    proxy_pass http://backend:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

#### 2. Compresión Gzip

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types
    text/plain
    text/css
    text/javascript
    application/javascript
    application/json;
```

#### 3. Headers de Seguridad

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

#### 4. Caché de Assets

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

#### 5. Health Check Endpoint

```nginx
location /health {
    access_log off;
    return 200 "OK\n";
    add_header Content-Type text/plain;
}
```

---

## 📊 Performance

### Métricas

| Métrica | Valor | Objetivo |
|---------|-------|----------|
| **First Contentful Paint (FCP)** | < 1s | < 2s |
| **Time to Interactive (TTI)** | < 2s | < 3.5s |
| **Total Bundle Size** | ~50KB | < 100KB |
| **Images** | Ninguna | - |
| **Dependencies** | 0 | 0 |

### Optimizaciones

1. **CSS**:
   - Variables CSS en lugar de Sass/Less
   - Sin frameworks CSS (Bootstrap, Tailwind, etc.)
   - Minificación en producción

2. **JavaScript**:
   - ES6 Modules nativos
   - Sin transpilación
   - Code splitting por módulo

3. **Network**:
   - Gzip compression
   - Cache headers optimizados
   - HTTP/2 ready

4. **Runtime**:
   - Debouncing en inputs
   - Event delegation
   - RequestAnimationFrame para animaciones

---

## 🛡️ Seguridad

### Medidas Implementadas

#### 1. Prevención de XSS

```javascript
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Uso
messageEl.textContent = escapeHtml(userInput);
```

#### 2. CSP (Content Security Policy)

```nginx
add_header Content-Security-Policy 
    "default-src 'self'; 
     script-src 'self'; 
     style-src 'self' 'unsafe-inline'; 
     img-src 'self' data:;" 
    always;
```

#### 3. HTTPS Only (Producción)

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

#### 4. Input Validation

```javascript
function validateQuestion(question) {
    // Longitud
    if (question.length < 3) {
        throw new Error('Pregunta demasiado corta');
    }
    if (question.length > 500) {
        throw new Error('Pregunta demasiado larga');
    }
    
    // Caracteres permitidos
    const allowedPattern = /^[a-zA-ZÀ-ÿ0-9\s¿?¡!.,;:-]+$/;
    if (!allowedPattern.test(question)) {
        throw new Error('Caracteres no permitidos');
    }
    
    return true;
}
```

---

## 🤝 Contribución

Para contribuir al frontend:

1. **Mantén la filosofía**: Sin frameworks, código vanilla
2. **Sigue BEM**: Para nomenclatura CSS
3. **ES6 Modules**: Usa import/export
4. **Documenta**: Añade comentarios descriptivos
5. **Prueba**: En múltiples navegadores
6. **Responsive**: Mobile-first approach
7. **Accesibilidad**: ARIA labels y navegación por teclado

### Checklist de PR

- [ ] Código funciona sin build step
- [ ] Compatible con navegadores modernos
- [ ] Responsive en mobile/tablet/desktop
- [ ] Accesible (ARIA, keyboard navigation)
- [ ] Sin errores en consola
- [ ] Comentado apropiadamente
- [ ] README actualizado si es necesario

---

## 📄 Licencia

Este proyecto es parte del sistema F1 Q&A con redes semánticas. Ver [LICENSE](../LICENSE) para detalles.

---

## 🔗 Enlaces Útiles

- **[Backend README](../backend/README.md)** - Documentación del backend
- **[API Documentation](http://localhost:8000/docs)** - Swagger UI
- **[OpenF1 API](https://openf1.org)** - API de datos de F1
- **[MDN Web Docs](https://developer.mozilla.org/)** - Referencia web
- **[Can I Use](https://caniuse.com/)** - Compatibilidad de navegadores

---

## 🙏 Créditos

- **Tema de colores**: Inspirado en la identidad visual de F1
- **Iconos**: Emojis nativos del sistema
- **Fuentes**: System fonts para máximo rendimiento

---

<p align="center">
  <strong>Desarrollado con ❤️ para los fanáticos de la Fórmula 1</strong>
  <br>
  <sub>HTML5 + CSS3 + JavaScript ES6+ | Sin dependencias | Sin build tools</sub>
</p>

