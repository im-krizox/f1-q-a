# Plan de Trabajo Detallado: Sistema de Q&A con Redes Semánticas - Fórmula 1

## 📋 PLAN BACKEND (Python + FastAPI)

### **Fase 1: Configuración Inicial del Proyecto**

#### Paso 1.1: Estructura de Directorios
```
Crear la siguiente estructura exacta:
backend/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes.py
│   │   └── dependencies.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── semantic_network.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── nodes.py
│   │   └── schemas.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── openf1_client.py
│   │   ├── knowledge_base.py
│   │   └── nlp_processor.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── env/
│   ├── .env.example
│   └── .env
├── requirements.txt
├── Dockerfile
└── README.md
```

#### Paso 1.2: Archivo requirements.txt
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
httpx==0.25.2
python-dotenv==1.0.0
python-multipart==0.0.6
networkx==3.2.1
nltk==3.8.1
unidecode==1.3.7
```

#### Paso 1.3: Archivo .env.example
```env
OPENF1_BASE_URL=https://api.openf1.org/v1
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
LOG_LEVEL=INFO
```

---

### **Fase 2: Modelos de Datos (models/)**

#### Paso 2.1: models/nodes.py
```python
Crear las siguientes clases Pydantic para los nodos:

1. PilotoNode:
   - nombre: str
   - numero_piloto: int
   - nacionalidad: str
   - driver_number: int (campo adicional para API)

2. EquipoNode:
   - nombre_equipo: str
   - jefe_equipo: str
   - team_name: str (campo adicional para API)

3. MotorNode:
   - fabricante: str
   - proveedor_combustible: str

4. CircuitoNode:
   - nombre_oficial: str
   - pais: str
   - longitud_metros: float
   - circuit_key: int (campo adicional para API)
   - circuit_short_name: str (campo adicional para API)

5. SesionNode:
   - session_key: int
   - tipo: str  # 'R' (Race), 'Q' (Qualifying), 'P' (Practice)
   - fecha: str
   - session_name: str
   - year: int
   - location: str

Todas deben heredar de BaseModel y tener Config con from_attributes=True
```

#### Paso 2.2: models/schemas.py
```python
Crear esquemas para request/response:

1. QuestionRequest:
   - question: str
   - context: Optional[Dict] = None

2. AnswerResponse:
   - answer: str
   - confidence: float
   - related_entities: List[Dict]
   - query_type: str
   - metadata: Optional[Dict] = None

3. HealthResponse:
   - status: str
   - version: str
   - knowledge_base_loaded: bool
```

---

### **Fase 3: Cliente API OpenF1 (services/openf1_client.py)**

#### Paso 3.1: Clase OpenF1Client
```python
Implementar clase con httpx.AsyncClient que tenga los siguientes métodos:

1. __init__(self, base_url: str):
   - Inicializar cliente async
   - Guardar base_url

2. async def get_drivers(self, session_key: Optional[int] = None) -> List[Dict]:
   - Endpoint: /drivers
   - Filtrar por session_key si se proporciona
   - Retornar lista de pilotos

3. async def get_sessions(self, year: Optional[int] = None, session_name: Optional[str] = None) -> List[Dict]:
   - Endpoint: /sessions
   - Filtrar por año y nombre de sesión
   - Retornar lista de sesiones

4. async def get_meetings(self, year: Optional[int] = None) -> List[Dict]:
   - Endpoint: /meetings
   - Obtener información de circuitos/eventos
   - Retornar lista de meetings

5. async def get_session_results(self, session_key: int) -> List[Dict]:
   - Endpoint: /results
   - Obtener resultados de una sesión específica
   - Retornar ganadores y posiciones

6. async def close(self):
   - Cerrar cliente httpx

Manejo de errores:
- Try/except para httpx.HTTPError
- Logging de errores
- Retornar listas vacías en caso de error
```

---

### **Fase 4: Red Semántica (core/semantic_network.py)**

#### Paso 4.1: Clase SemanticNetwork
```python
Usar networkx.MultiDiGraph para implementar:

1. __init__(self):
   - Inicializar grafo dirigido: self.graph = nx.MultiDiGraph()
   - Diccionarios de índices: self.nodes_by_type = defaultdict(list)

2. add_node(self, node_id: str, node_type: str, attributes: Dict):
   - Agregar nodo al grafo con networkx
   - Almacenar tipo y atributos
   - Indexar por tipo en self.nodes_by_type

3. add_edge(self, source: str, target: str, relation: str, attributes: Dict = None):
   - Agregar arista con relación específica
   - Tipos de relaciones: "conduce_para", "usa_motor", "tiene_ganador", 
     "ocurre_en", "esta_en", "es_un_tipo_de"

4. query_by_relation(self, node_id: str, relation: str, direction: str = "outgoing") -> List[Dict]:
   - Buscar nodos conectados por una relación específica
   - direction: "outgoing" o "incoming"
   - Retornar lista de nodos con sus atributos

5. find_nodes_by_type(self, node_type: str, filters: Dict = None) -> List[Dict]:
   - Buscar todos los nodos de un tipo
   - Aplicar filtros opcionales a atributos
   - Retornar nodos que coincidan

6. get_node_details(self, node_id: str) -> Optional[Dict]:
   - Obtener todos los atributos de un nodo
   - Incluir relaciones salientes y entrantes

7. find_path(self, source: str, target: str, max_length: int = 5) -> List[List[str]]:
   - Encontrar caminos entre dos nodos
   - Usar nx.all_simple_paths
   - Limitar longitud máxima

8. get_related_entities(self, node_id: str, max_depth: int = 2) -> Dict:
   - Explorar vecindario del nodo
   - Retornar entidades relacionadas agrupadas por tipo
```

---

### **Fase 5: Base de Conocimiento (services/knowledge_base.py)**

#### Paso 5.1: Clase KnowledgeBase
```python
Implementar carga y población de la red semántica:

1. __init__(self, openf1_client: OpenF1Client):
   - Inicializar SemanticNetwork
   - Guardar referencia al cliente
   - self.loaded = False

2. async def load_data(self, year: int = 2024):
   - Cargar datos de OpenF1 para el año especificado
   - Llamar a métodos de población en orden
   - Marcar self.loaded = True

3. async def _populate_sessions(self, year: int):
   - Obtener sesiones del año
   - Crear nodos SesionNode para cada sesión
   - ID formato: "session_{session_key}"

4. async def _populate_drivers(self, sessions: List[Dict]):
   - Para cada sesión, obtener pilotos
   - Crear nodos PilotoNode únicos (evitar duplicados)
   - ID formato: "driver_{driver_number}"

5. async def _populate_circuits(self, meetings: List[Dict]):
   - Obtener información de circuitos
   - Crear nodos CircuitoNode
   - ID formato: "circuit_{circuit_key}"
   - Crear nodos de País si no existen
   - Crear arista "esta_en" entre circuito y país

6. async def _populate_teams(self, drivers_data: List[Dict]):
   - Extraer equipos únicos de datos de pilotos
   - Crear nodos EquipoNode
   - ID formato: "team_{nombre_normalizado}"
   - Hardcodear jefes de equipo principales (Christian Horner, Toto Wolff, etc.)

7. async def _populate_motors(self):
   - Crear nodos MotorNode para fabricantes conocidos
   - ID formato: "engine_{fabricante}"
   - Motores: Mercedes, Ferrari, Honda RBPT, Renault

8. async def _create_relationships(self):
   - Crear aristas "conduce_para" (piloto -> equipo)
   - Crear aristas "usa_motor" (equipo -> motor)
   - Crear aristas "tiene_ganador" (sesión -> piloto ganador)
   - Crear aristas "ocurre_en" (sesión -> circuito)
   - Crear aristas "es_un_tipo_de" (sesión -> tipo_evento)

9. def get_semantic_network(self) -> SemanticNetwork:
   - Retornar instancia de la red semántica
```

---

### **Fase 6: Procesador NLP (services/nlp_processor.py)**

#### Paso 6.1: Clase NLPProcessor
```python
Implementar análisis de preguntas en español:

1. __init__(self):
   - Definir patrones de preguntas
   - Diccionarios de sinónimos
   - Palabras clave por tipo de consulta

2. def normalize_text(self, text: str) -> str:
   - Convertir a minúsculas
   - Remover acentos con unidecode
   - Eliminar puntuación innecesaria
   - Retornar texto normalizado

3. def extract_query_type(self, question: str) -> str:
   - Identificar tipo de pregunta:
     * "pilot_info": ¿Quién es...?, ¿Qué piloto...?
     * "team_info": ¿Para qué equipo...?, ¿Qué equipo...?
     * "circuit_info": ¿Dónde...?, ¿En qué circuito...?
     * "session_info": ¿Cuándo...?, ¿Qué sesión...?
     * "winner_info": ¿Quién ganó...?, ¿Ganador de...?
     * "relationship": ¿Qué motor usa...?, ¿Qué piloto conduce...?
   - Usar regex y palabras clave

4. def extract_entities(self, question: str) -> Dict[str, List[str]]:
   - Buscar nombres de pilotos mencionados
   - Buscar nombres de equipos
   - Buscar nombres de circuitos/países
   - Buscar años o fechas
   - Retornar diccionario con entidades encontradas

5. def extract_intent(self, question: str) -> Dict:
   - Combinar query_type y entities
   - Determinar acción requerida
   - Retornar estructura:
     {
       "type": str,
       "entities": Dict,
       "filters": Dict,
       "action": str
     }
```

---

### **Fase 7: Servicio de Consultas (services/query_service.py)**

#### Paso 7.1: Crear nueva clase QueryService
```python
1. __init__(self, knowledge_base: KnowledgeBase, nlp_processor: NLPProcessor):
   - Guardar referencias
   - Inicializar caché de respuestas

2. async def process_question(self, question: str) -> AnswerResponse:
   - Normalizar pregunta con NLP
   - Extraer intent
   - Ejecutar consulta apropiada
   - Formatear respuesta
   - Calcular confidence score

3. def _query_pilot_info(self, entities: Dict, filters: Dict) -> Dict:
   - Buscar piloto en red semántica
   - Obtener equipo actual (relación "conduce_para")
   - Obtener nacionalidad
   - Retornar información completa

4. def _query_team_info(self, entities: Dict, filters: Dict) -> Dict:
   - Buscar equipo
   - Obtener pilotos (relación inversa "conduce_para")
   - Obtener motor (relación "usa_motor")
   - Retornar información del equipo

5. def _query_winner_info(self, entities: Dict, filters: Dict) -> Dict:
   - Buscar sesión por filtros
   - Obtener ganador (relación "tiene_ganador")
   - Retornar nombre del piloto ganador

6. def _query_circuit_info(self, entities: Dict, filters: Dict) -> Dict:
   - Buscar circuito
   - Obtener país (relación "esta_en")
   - Obtener sesiones (relación inversa "ocurre_en")
   - Retornar detalles del circuito

7. def _query_relationship(self, entities: Dict, action: str) -> Dict:
   - Navegar relaciones específicas en la red
   - Ejemplos: "qué motor usa X equipo", "para quién corre X piloto"
   - Retornar entidades relacionadas

8. def _calculate_confidence(self, results: Dict, intent: Dict) -> float:
   - Calcular confianza basada en:
     * Número de resultados encontrados
     * Coincidencia con entidades extraídas
     * Completitud de la información
   - Retornar valor entre 0.0 y 1.0

9. def _format_answer(self, results: Dict, query_type: str) -> str:
   - Generar respuesta en lenguaje natural
   - Usar plantillas por tipo de pregunta
   - Retornar string formateado en español
```

---

### **Fase 8: Configuración (core/config.py)**

#### Paso 8.1: Settings con Pydantic
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API OpenF1
    openf1_base_url: str = "https://api.openf1.org/v1"
    
    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Logging
    log_level: str = "INFO"
    
    # App
    app_name: str = "F1 Q&A System"
    app_version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

def get_settings() -> Settings:
    return Settings()
```

---

### **Fase 9: API Routes (api/routes.py)**

#### Paso 9.1: Endpoints FastAPI
```python
Crear router con los siguientes endpoints:

1. POST /api/v1/ask
   - Body: QuestionRequest
   - Response: AnswerResponse
   - Procesar pregunta con QueryService
   - Manejo de errores con try/except

2. GET /api/v1/health
   - Response: HealthResponse
   - Verificar estado del sistema
   - Verificar si knowledge base está cargada

3. GET /api/v1/entities/{entity_type}
   - Path param: entity_type (drivers, teams, circuits, sessions)
   - Query params opcionales: year, name, etc.
   - Retornar lista de entidades del tipo solicitado

4. GET /api/v1/network/explore/{node_id}
   - Path param: node_id
   - Query param: depth (default: 2)
   - Retornar vecindario del nodo en la red semántica

5. POST /api/v1/reload
   - Query param: year (default: 2024)
   - Recargar knowledge base con datos del año especificado
   - Requiere autenticación (opcional para v1)

Cada endpoint debe:
- Tener documentación con descripción y ejemplos
- Validar inputs con Pydantic
- Manejar errores con HTTPException
- Loggear operaciones importantes
```

---

### **Fase 10: Aplicación Principal (api/main.py)**

#### Paso 10.1: Configurar FastAPI App
```python
1. Crear app FastAPI con metadata (título, versión, descripción)

2. Configurar CORS middleware:
   - Permitir orígenes desde settings
   - Permitir credenciales
   - Permitir todos los métodos y headers

3. Crear evento startup:
   - Inicializar OpenF1Client
   - Crear KnowledgeBase
   - Cargar datos (await knowledge_base.load_data(2024))
   - Inicializar NLPProcessor
   - Crear QueryService
   - Guardar instancias en app.state

4. Crear evento shutdown:
   - Cerrar OpenF1Client
   - Limpiar recursos

5. Incluir router de routes.py

6. Configurar logging:
   - Formato con timestamp
   - Nivel desde settings

7. Agregar endpoint raíz GET / que retorne:
   {
     "message": "F1 Q&A API",
     "docs": "/docs",
     "health": "/api/v1/health"
   }
```

---

### **Fase 11: Dependencias (api/dependencies.py)**

#### Paso 11.1: Dependency Injection
```python
1. def get_knowledge_base(request: Request) -> KnowledgeBase:
   - Retornar app.state.knowledge_base

2. def get_nlp_processor(request: Request) -> NLPProcessor:
   - Retornar app.state.nlp_processor

3. def get_query_service(request: Request) -> QueryService:
   - Retornar app.state.query_service

4. def get_settings() -> Settings:
   - Retornar instancia de Settings

Usar estas funciones en routes.py con Depends()
```

---

### **Fase 12: Dockerfile Backend**

#### Paso 12.1: Crear Dockerfile optimizado
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Descargar datos de NLTK si se usan
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Copiar código fuente
COPY src/ ./src/
COPY env/.env .env

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

### **Fase 13: Testing y Validación**

#### Paso 13.1: Casos de Prueba
```python
Crear archivo tests/test_semantic_network.py con:

1. Test de creación de nodos
2. Test de creación de aristas
3. Test de consultas por relación
4. Test de búsqueda de caminos

Crear archivo tests/test_nlp_processor.py con:

1. Test de extracción de query_type
2. Test de extracción de entidades
3. Test de normalización de texto

Crear archivo tests/test_api.py con:

1. Test de endpoint /health
2. Test de endpoint /ask con diferentes preguntas
3. Test de manejo de errores

Ejecutar con pytest
```

---

## 🎨 PLAN FRONTEND (HTML/CSS/JavaScript)

### **Fase 1: Estructura del Proyecto Frontend**

#### Paso 1.1: Crear Estructura de Directorios
```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── css/
│   │   ├── main.css
│   │   ├── chat.css
│   │   └── components.css
│   ├── js/
│   │   ├── main.js
│   │   ├── api-client.js
│   │   ├── chat-ui.js
│   │   └── utils.js
│   └── assets/
│       ├── images/
│       └── icons/
├── nginx.conf
├── Dockerfile
└── README.md
```

---

### **Fase 2: HTML Base (public/index.html)**

#### Paso 2.1: Estructura HTML5 Semántica
```html
Crear documento HTML con:

1. DOCTYPE html5
2. Meta tags:
   - charset UTF-8
   - viewport responsive
   - description del proyecto
   - author

3. Enlaces a CSS:
   - main.css
   - chat.css
   - components.css
   - Google Fonts (Roboto o Inter)

4. Estructura del body:
   <header>
     - Logo/título "F1 Q&A System"
     - Subtítulo descriptivo
     - Indicador de estado de conexión
   </header>

   <main class="container">
     <section class="chat-container">
       <div class="welcome-screen" id="welcomeScreen">
         - Mensaje de bienvenida
         - Lista de preguntas ejemplo:
           * "¿Quién es Max Verstappen?"
           * "¿Para qué equipo corre Lewis Hamilton?"
           * "¿Quién ganó el GP de Mónaco 2024?"
           * "¿Qué motor usa Red Bull?"
           * "¿Dónde está el circuito de Spa?"
       </div>
       
       <div class="messages-container" id="messagesContainer">
         <!-- Mensajes dinámicos -->
       </div>
       
       <div class="input-container">
         <form id="questionForm">
           <input 
             type="text" 
             id="questionInput" 
             placeholder="Escribe tu pregunta sobre F1..."
             autocomplete="off"
             required
           />
           <button type="submit" id="sendButton">
             <span>Enviar</span>
             <svg><!-- Icono de enviar --></svg>
           </button>
         </form>
         <div class="typing-indicator" id="typingIndicator" style="display: none;">
           <span></span><span></span><span></span>
         </div>
       </div>
     </section>

     <aside class="info-panel" id="infoPanel">
       <h3>Información Adicional</h3>
       <div id="relatedEntities"></div>
       <div id="confidenceScore"></div>
     </aside>
   </main>

   <footer>
     - Créditos
     - Link a documentación
     - Versión del sistema
   </footer>

5. Scripts al final:
   - utils.js
   - api-client.js
   - chat-ui.js
   - main.js
```

---

### **Fase 3: Estilos CSS**

#### Paso 3.1: main.css (Estilos Globales)
```css
Implementar:

1. CSS Reset básico:
   - margin: 0, padding: 0
   - box-sizing: border-box

2. Variables CSS (--custom-properties):
   --primary-color: #E10600 (rojo F1)
   --secondary-color: #15151E (negro F1)
   --accent-color: #00D9FF (cyan tecnológico)
   --bg-primary: #FFFFFF
   --bg-secondary: #F5F5F5
   --text-primary: #15151E
   --text-secondary: #666666
   --shadow-sm: 0 2px 4px rgba(0,0,0,0.1)
   --shadow-md: 0 4px 8px rgba(0,0,0,0.15)
   --shadow-lg: 0 8px 16px rgba(0,0,0,0.2)
   --border-radius: 12px
   --transition: all 0.3s ease

3. Tipografía:
   - Font-family: 'Inter', 'Roboto', sans-serif
   - Tamaños responsivos con clamp()
   - Line-heights optimizados

4. Layout:
   - body con min-height: 100vh, display: flex, flex-direction: column
   - container con max-width: 1200px, margin auto, padding
   - Grid o flexbox para main layout

5. Header:
   - Background gradient con colores F1
   - Padding generoso
   - Box-shadow
   - Texto centrado
   - Estado de conexión con dot indicator

6. Footer:
   - Background color secundario
   - Padding moderado
   - Texto centrado pequeño
   - Links con hover effects
```

#### Paso 3.2: chat.css (Interfaz de Chat)
```css
Implementar:

1. .chat-container:
   - Background blanco
   - Border-radius
   - Box-shadow
   - Display flex column
   - Height: calc(100vh - header - footer - margins)
   - Max-height: 700px

2. .welcome-screen:
   - Centrado vertical y horizontal
   - Padding generoso
   - Fade-in animation
   - h2 con color primary
   - Lista de ejemplos:
     * Cada item con padding, border-left, hover effect
     * Cursor pointer
     * Transition suave

3. .messages-container:
   - Flex: 1 (grow para ocupar espacio)
   - Overflow-y: auto
   - Padding: 20px
   - Custom scrollbar styling:
     * Width: 8px
     * Track color: bg-secondary
     * Thumb color: primary con hover

4. .message:
   - Display: flex
   - Margin-bottom: 16px
   - Animation: slideIn
   
   .message.user:
   - Justify-content: flex-end
   - .message-bubble: background primary, color white, border-radius asimérico
   
   .message.assistant:
   - Justify-content: flex-start
   - .message-bubble: background secondary, color text-primary, border-radius asimérico

5. .message-bubble:
   - Max-width: 70%
   - Padding: 12px 16px
   - Box-shadow sm
   - Word-wrap: break-word
   
   .message-metadata:
   - Font-size: 0.75rem
   - Opacity: 0.7
   - Margin-top: 4px

6. .input-container:
   - Border-top: 1px solid border-color
   - Padding: 16px
   - Background: bg-secondary

7. #questionForm:
   - Display: flex
   - Gap: 12px
   
   #questionInput:
   - Flex: 1
   - Padding: 12px 16px
   - Border: 2px solid transparent
   - Border-radius: border-radius
   - Font-size: 1rem
   - Transition: border-color
   - Focus: border-color primary, outline none

   #sendButton:
   - Padding: 12px 24px
   - Background: primary
   - Color: white
   - Border: none
   - Border-radius: border-radius
   - Cursor: pointer
   - Display: flex, align-items: center, gap: 8px
   - Transition: transform, background
   - Hover: transform scale(1.05), background darker
   - Active: transform scale(0.95)
   - Disabled: opacity 0.5, cursor not-allowed

8. .typing-indicator:
   - Display: flex, gap: 4px
   - Padding: 8px 0
   
   span:
   - Width: 8px, height: 8px
   - Background: text-secondary
   - Border-radius: 50%
   - Animation: bounce 1.4s infinite ease-in-out

9. Animaciones:
   @keyframes slideIn - translate y fade
   @keyframes fadeIn - opacity
   @keyframes bounce - transform translateY para dots
```

#### Paso 3.3: components.css (Componentes Adicionales)
```css
Implementar:

1. .info-panel:
   - Background: bg-secondary
   - Border-radius
   - Padding: 20px
   - Box-shadow
   - Position: sticky o normal según layout
   
   h3:
   - Color: primary
   - Margin-bottom: 16px
   - Font-size: 1.25rem

2. .entity-card:
   - Background: white
   - Padding: 12px
   - Margin-bottom: 12px
   - Border-radius: 8px
   - Border-left: 3px solid accent-color
   - Transition: transform
   - Hover: transform translateX(4px)
   
   .entity-label:
   - Font-weight: 600
   - Color: text-primary
   - Font-size: 0.875rem
   - Text-transform: uppercase
   
   .entity-value:
   - Color: text-secondary
   - Margin-top: 4px

3. .confidence-meter:
   - Margin-top: 16px
   
   .confidence-bar:
   - Height: 8px
   - Background: bg-primary
   - Border-radius: 4px
   - Overflow: hidden
   
   .confidence-fill:
   - Height: 100%
   - Background: linear-gradient con colores según score
   - Transition: width 0.5s ease
   - Width: calculado dinámicamente

4. .status-indicator:
   - Display: inline-flex
   - Align-items: center
   - Gap: 8px
   - Font-size: 0.875rem
   
   .status-dot:
   - Width: 10px, height: 10px
   - Border-radius: 50%
   - Background: según estado (green/yellow/red)
   - Animation: pulse si está conectado

5. .error-message:
   - Background: #FFEBEE (rojo claro)
   - Color: #C62828 (rojo oscuro)
   - Padding: 12px 16px
   - Border-radius: 8px
   - Border-left: 4px solid #C62828
   - Margin: 16px 0

6. .loading-skeleton:
   - Background: linear-gradient animado (shimmer effect)
   - Border-radius: 8px
   - Height: variable según contenido
   - Animation: shimmer 1.5s infinite
   
   @keyframes shimmer:
   - Background-position animado de izquierda a derecha
   - Efecto de carga brillante

7. .button-secondary:
   - Background: transparent
   - Border: 2px solid primary
   - Color: primary
   - Padding: 8px 16px
   - Border-radius: border-radius
   - Cursor: pointer
   - Transition: all 0.3s
   - Hover: background primary, color white

8. .tooltip:
   - Position: relative
   
   .tooltip-text:
   - Visibility: hidden
   - Position: absolute
   - Background: #333
   - Color: white
   - Padding: 8px 12px
   - Border-radius: 6px
   - Font-size: 0.875rem
   - White-space: nowrap
   - Bottom: 125%
   - Left: 50%
   - Transform: translateX(-50%)
   - Opacity: 0
   - Transition: opacity 0.3s
   
   .tooltip:hover .tooltip-text:
   - Visibility: visible
   - Opacity: 1

9. Media Queries:
   @media (max-width: 768px):
   - .chat-container: height auto, max-height none
   - .message-bubble: max-width 85%
   - .info-panel: display none o posición diferente
   - Font sizes reducidos
   - Padding/margins ajustados
   
   @media (max-width: 480px):
   - Input y botón en columna si es necesario
   - Header con padding reducido
   - Mensajes: max-width 90%
```

---

### **Fase 4: JavaScript - Utilidades (js/utils.js)**

#### Paso 4.1: Funciones Helper
```javascript
Implementar funciones puras:

1. function formatDate(date):
   - Parámetro: Date object o string
   - Retornar formato: "DD/MM/YYYY HH:MM"
   - Usar Intl.DateTimeFormat o métodos nativos

2. function escapeHtml(text):
   - Prevenir XSS escapando HTML
   - Reemplazar <, >, &, ", '
   - Retornar string seguro

3. function debounce(func, delay):
   - Implementar debouncing
   - Retornar función debounced
   - Usar para evitar múltiples llamadas API

4. function generateId():
   - Generar ID único para mensajes
   - Usar timestamp + random
   - Retornar string

5. function scrollToBottom(element, smooth = true):
   - Scroll a bottom de elemento
   - Parámetro smooth para animación
   - Usar scrollIntoView o scrollTop

6. function copyToClipboard(text):
   - Copiar texto al portapapeles
   - Usar navigator.clipboard API
   - Fallback para navegadores antiguos
   - Retornar Promise<boolean>

7. function highlightCode(text):
   - Detectar bloques de código en texto
   - Aplicar syntax highlighting básico
   - Retornar HTML formateado

8. function truncateText(text, maxLength):
   - Truncar texto largo
   - Agregar "..." si excede
   - Retornar string truncado

9. function validateUrl(url):
   - Validar formato de URL
   - Usar regex o URL constructor
   - Retornar boolean

10. const CONSTANTS object:
    - API_BASE_URL: 'http://localhost:8000'
    - API_ENDPOINTS: { ASK: '/api/v1/ask', HEALTH: '/api/v1/health', ... }
    - MESSAGE_TYPES: { USER: 'user', ASSISTANT: 'assistant', SYSTEM: 'system' }
    - TYPING_DELAY: 1500
    - MAX_MESSAGE_LENGTH: 500
```

---

### **Fase 5: JavaScript - Cliente API (js/api-client.js)**

#### Paso 5.1: Clase APIClient
```javascript
Implementar clase para comunicación con backend:

class APIClient {
  1. constructor(baseURL):
     - this.baseURL = baseURL
     - this.headers = { 'Content-Type': 'application/json' }
     - this.timeout = 30000

  2. async request(endpoint, options = {}):
     - Método genérico para fetch
     - Combinar baseURL + endpoint
     - Aplicar headers por defecto
     - Implementar timeout con AbortController
     - Try/catch para errores de red
     - Verificar response.ok
     - Parsear JSON
     - Retornar data o lanzar error

  3. async askQuestion(question):
     - Endpoint: /api/v1/ask
     - Method: POST
     - Body: { question: string }
     - Retornar AnswerResponse
     - Manejo de errores específico:
       * 400: Pregunta inválida
       * 500: Error del servidor
       * Network: Error de conexión

  4. async checkHealth():
     - Endpoint: /api/v1/health
     - Method: GET
     - Retornar HealthResponse
     - Usar para verificar conexión

  5. async getEntities(entityType, filters = {}):
     - Endpoint: /api/v1/entities/{entityType}
     - Method: GET
     - Query params: filters
     - Retornar lista de entidades

  6. async exploreNetwork(nodeId, depth = 2):
     - Endpoint: /api/v1/network/explore/{nodeId}
     - Method: GET
     - Query param: depth
     - Retornar vecindario del nodo

  7. handleError(error):
     - Método privado
     - Parsear diferentes tipos de error
     - Retornar objeto estructurado:
       {
         message: string,
         type: 'network' | 'server' | 'client',
         statusCode: number | null
       }

  8. setAuthToken(token):
     - Para futuras implementaciones
     - Agregar Authorization header

  9. setTimeout(ms):
     - Configurar timeout personalizado
}

// Exportar instancia singleton
export default new APIClient(CONSTANTS.API_BASE_URL);
```

---

### **Fase 6: JavaScript - Interfaz de Chat (js/chat-ui.js)**

#### Paso 6.1: Clase ChatUI
```javascript
Implementar gestión de la interfaz:

class ChatUI {
  1. constructor(apiClient):
     - this.apiClient = apiClient
     - this.messages = []
     - this.elements = {} (referencias DOM)
     - this.isTyping = false
     - this.connectionStatus = 'checking'

  2. init():
     - Obtener referencias DOM:
       * welcomeScreen
       * messagesContainer
       * questionForm
       * questionInput
       * sendButton
       * typingIndicator
       * infoPanel
       * statusIndicator
     - Agregar event listeners
     - Verificar salud del backend
     - Cargar mensajes guardados del localStorage (opcional)

  3. bindEvents():
     - questionForm.onsubmit = handleSubmit
     - welcomeScreen clicks en ejemplos
     - Tecla Enter en input (sin shift)
     - Input change para validación
     - Window resize para ajustar layout

  4. async handleSubmit(event):
     - Prevenir default
     - Obtener texto del input
     - Validar: no vacío, no muy largo
     - Limpiar input
     - Agregar mensaje del usuario
     - Ocultar welcome screen
     - Mostrar typing indicator
     - Llamar apiClient.askQuestion
     - Ocultar typing indicator
     - Agregar respuesta del asistente
     - Actualizar info panel
     - Scroll to bottom
     - Manejo de errores

  5. addMessage(text, type, metadata = {}):
     - Crear objeto mensaje:
       {
         id: generateId(),
         text: text,
         type: type,
         timestamp: new Date(),
         metadata: metadata
       }
     - Agregar a this.messages
     - Renderizar mensaje
     - Guardar en localStorage (opcional)

  6. renderMessage(message):
     - Crear elementos DOM:
       <div class="message {type}">
         <div class="message-bubble">
           <div class="message-text">{escapedText}</div>
           <div class="message-metadata">{formattedTime}</div>
         </div>
       </div>
     - Agregar animación de entrada
     - Append a messagesContainer
     - Scroll to bottom

  7. showTypingIndicator():
     - this.isTyping = true
     - typingIndicator.style.display = 'flex'
     - Scroll to bottom

  8. hideTypingIndicator():
     - this.isTyping = false
     - typingIndicator.style.display = 'none'

  9. updateInfoPanel(data):
     - Limpiar panel actual
     - Si hay related_entities:
       * Crear entity cards
       * Renderizar con información
     - Si hay confidence:
       * Actualizar confidence meter
       * Cambiar color según score
     - Si hay metadata adicional:
       * Mostrar en formato adecuado

  10. renderEntityCard(entity):
      - Crear HTML:
        <div class="entity-card">
          <div class="entity-label">{type}</div>
          <div class="entity-value">{value}</div>
        </div>
      - Retornar elemento

  11. updateConfidenceMeter(score):
      - Calcular porcentaje
      - Actualizar width de .confidence-fill
      - Cambiar color:
        * > 0.8: green
        * 0.5 - 0.8: yellow
        * < 0.5: red
      - Agregar texto: "{score}% confianza"

  12. showError(message):
      - Crear elemento .error-message
      - Mostrar en messagesContainer o como toast
      - Auto-ocultar después de 5 segundos

  13. hideWelcomeScreen():
      - welcomeScreen.style.display = 'none'
      - Animar fade-out

  14. async checkBackendHealth():
      - Try/catch apiClient.checkHealth()
      - Actualizar this.connectionStatus
      - Actualizar UI del status indicator:
        * 'connected': dot verde, texto "Conectado"
        * 'error': dot rojo, texto "Desconectado"
        * 'checking': dot amarillo, texto "Verificando..."
      - Si está desconectado:
        * Mostrar mensaje al usuario
        * Deshabilitar input
        * Reintentar cada 10 segundos

  15. enableInput():
      - questionInput.disabled = false
      - sendButton.disabled = false

  16. disableInput():
      - questionInput.disabled = true
      - sendButton.disabled = true

  17. clearMessages():
      - this.messages = []
      - messagesContainer.innerHTML = ''
      - Mostrar welcome screen
      - Limpiar localStorage

  18. loadMessagesFromStorage():
      - Obtener de localStorage
      - Parsear JSON
      - Renderizar mensajes anteriores
      - Opcional: solo últimos N mensajes

  19. handleExampleClick(exampleText):
      - Poner texto en input
      - Trigger submit
}

export default ChatUI;
```

---

### **Fase 7: JavaScript - Inicialización (js/main.js)**

#### Paso 7.1: Entry Point
```javascript
Implementar inicialización de la aplicación:

1. Import statements:
   - import apiClient from './api-client.js'
   - import ChatUI from './chat-ui.js'
   - import { CONSTANTS, ... } from './utils.js'

2. DOMContentLoaded event listener:
   - Verificar que todos los elementos existen
   - Crear instancia de ChatUI
   - Inicializar chat UI
   - Configurar event listeners globales

3. window.addEventListener('DOMContentLoaded', async () => {
     - const chatUI = new ChatUI(apiClient)
     - await chatUI.init()
     - setupGlobalHandlers(chatUI)
     - console.log('F1 Q&A System initialized')
   })

4. function setupGlobalHandlers(chatUI):
   - Window beforeunload: confirmar si hay conversación activa
   - Window online/offline: actualizar estado de conexión
   - Document visibility change: pausar/reanudar polling
   - Global error handler: capturar errores no manejados
   - Service Worker registration (opcional para PWA)

5. function setupKeyboardShortcuts(chatUI):
   - Ctrl/Cmd + K: Focus en input
   - Ctrl/Cmd + L: Limpiar chat
   - Esc: Cancelar typing indicator si está activo
   - Arrow Up: Editar último mensaje (opcional)

6. Configuración de Service Worker (opcional):
   if ('serviceWorker' in navigator) {
     navigator.serviceWorker.register('/sw.js')
       .then(reg => console.log('SW registered'))
       .catch(err => console.log('SW error', err))
   }

7. Export para testing (opcional):
   export { chatUI, apiClient }
```

---

### **Fase 8: Mejoras Avanzadas (Opcional)**

#### Paso 8.1: Características Adicionales en chat-ui.js
```javascript
Agregar funcionalidades extra:

1. Markdown/Formatting Support:
   - Instalar/usar marked.js o escribir parser simple
   - Detectar **bold**, *italic*, `code`
   - Renderizar listas y links
   - Sanitizar HTML resultante

2. Code Syntax Highlighting:
   - Detectar bloques ```python, ```javascript
   - Usar highlight.js o prism.js
   - Agregar botón de copiar código

3. Message Actions:
   - Botón para copiar respuesta
   - Botón para regenerar respuesta
   - Botón para dar feedback (thumbs up/down)

4. Voice Input (opcional):
   - Botón de micrófono
   - Web Speech API
   - Transcribir a texto
   - Enviar pregunta

5. Export Conversation:
   - Botón para exportar chat
   - Formato: JSON, Markdown o PDF
   - Descargar archivo

6. Themes:
   - Toggle dark/light mode
   - Guardar preferencia en localStorage
   - CSS variables para fácil cambio

7. Suggestions:
   - Mientras el usuario escribe
   - Mostrar preguntas relacionadas
   - Autocompletar con entidades conocidas

8. History Search:
   - Buscar en mensajes anteriores
   - Filtrar por fecha o tipo
   - Resaltar resultados
```

---

### **Fase 9: Nginx Configuration**

#### Paso 9.1: nginx.conf
```nginx
Crear configuración para servir frontend:

server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    # Logs
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Comprimir respuestas
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Headers de seguridad
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Servir archivos estáticos
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Caché para assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy para API (si backend y frontend en mismo contenedor)
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "OK";
        add_header Content-Type text/plain;
    }
}
```

---

### **Fase 10: Dockerfile Frontend**

#### Paso 10.1: Multi-stage Dockerfile
```dockerfile
# Stage 1: Build (si usas bundler, sino skip a stage 2)
FROM node:18-alpine AS builder
WORKDIR /app
# Si decides usar bundler como Vite o Webpack:
# COPY package*.json ./
# RUN npm ci
# COPY . .
# RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Copiar archivos estáticos
COPY public/ /usr/share/nginx/html/
COPY src/ /usr/share/nginx/html/src/

# Copiar configuración nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Permisos
RUN chmod -R 755 /usr/share/nginx/html

# Exponer puerto
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

# Nginx en foreground
CMD ["nginx", "-g", "daemon off;"]
```

---

### **Fase 11: Docker Compose (Raíz del Proyecto)**

#### Paso 11.1: docker-compose.yml
```yaml
Crear en la raíz del proyecto:

version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: f1-qa-backend
    ports:
      - "8000:8000"
    environment:
      - OPENF1_BASE_URL=https://api.openf1.org/v1
      - CORS_ORIGINS=http://localhost:80,http://localhost:3000
    volumes:
      - ./backend/src:/app/src  # Hot reload en desarrollo
      - ./backend/env/.env:/app/.env
    networks:
      - f1-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: f1-qa-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    environment:
      - API_BASE_URL=http://backend:8000
    networks:
      - f1-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 5s
      retries: 3

networks:
  f1-network:
    driver: bridge

volumes:
  backend_data:
```

#### Paso 11.2: .dockerignore (Backend y Frontend)
```
Backend .dockerignore:
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
*.log
.git/
.gitignore
README.md
tests/
.pytest_cache/

Frontend .dockerignore:
node_modules/
.git/
.gitignore
README.md
*.log
.DS_Store
```

---

### **Fase 12: Scripts de Desarrollo**

#### Paso 12.1: Crear scripts útiles en package.json (raíz)
```json
Si decides usar npm para gestión de scripts:

{
  "name": "f1-qa-system",
  "version": "1.0.0",
  "scripts": {
    "dev": "docker-compose up --build",
    "dev:backend": "cd backend && uvicorn src.api.main:app --reload",
    "dev:frontend": "cd frontend && python -m http.server 8080",
    "start": "docker-compose up",
    "stop": "docker-compose down",
    "clean": "docker-compose down -v --rmi all",
    "logs": "docker-compose logs -f",
    "logs:backend": "docker-compose logs -f backend",
    "logs:frontend": "docker-compose logs -f frontend",
    "test:backend": "cd backend && pytest",
    "lint:backend": "cd backend && black src/ && flake8 src/",
    "health": "curl http://localhost:8000/api/v1/health"
  }
}
```

#### Paso 12.2: Makefile (alternativo)
```makefile
.PHONY: help build up down logs clean test

help:
	@echo "F1 Q&A System - Comandos disponibles:"
	@echo "  make build    - Construir imágenes Docker"
	@echo "  make up       - Iniciar contenedores"
	@echo "  make down     - Detener contenedores"
	@echo "  make logs     - Ver logs"
	@echo "  make clean    - Limpiar todo"
	@echo "  make test     - Ejecutar tests"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v --rmi all
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	cd backend && pytest -v

dev:
	docker-compose up --build

restart:
	docker-compose restart

health:
	@curl -s http://localhost:8000/api/v1/health | python -m json.tool
```

---

### **Fase 13: Documentación**

#### Paso 13.1: README.md Principal
```markdown
Crear README.md en la raíz con:

# F1 Q&A System - Sistema de Preguntas y Respuestas con Redes Semánticas

## 📋 Descripción
Sistema inteligente de Q&A sobre Fórmula 1 usando redes semánticas...

## 🏗️ Arquitectura
- Backend: Python + FastAPI
- Frontend: HTML/CSS/JavaScript
- Base de Conocimiento: API OpenF1
- Containerización: Docker

## 📁 Estructura del Proyecto
```
proyecto/
├── backend/
├── frontend/
├── docker-compose.yml
└── README.md
```

## 🚀 Instalación y Uso

### Prerrequisitos
- Docker 20.10+
- Docker Compose 2.0+

### Inicio Rápido
```bash
# Clonar repositorio
git clone <repo>

# Iniciar sistema
docker-compose up --build

# Acceder
# Frontend: http://localhost
# Backend API: http://localhost:8000/docs
```

## 🔧 Desarrollo Local

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

### Frontend
```bash
cd frontend
python -m http.server 8080
# O usar Live Server en VS Code
```

## 📊 Red Semántica

### Nodos
- Piloto, Equipo, Motor, Circuito, Sesión

### Relaciones
- conduce_para, usa_motor, tiene_ganador, ocurre_en, esta_en, es_un_tipo_de

## 🧪 Testing
```bash
make test
# o
cd backend && pytest
```

## 📝 Ejemplos de Preguntas
- "¿Quién es Max Verstappen?"
- "¿Para qué equipo corre Lewis Hamilton?"
- "¿Quién ganó el GP de Mónaco 2024?"
- "¿Qué motor usa Red Bull?"

## 🤝 Contribución
[Instrucciones de contribución]

## 📄 Licencia
[Tu licencia]
```

---

### **Fase 14: Testing Frontend**

#### Paso 14.1: Tests Básicos (tests/frontend/)
```javascript
Si quieres agregar tests con Jest o similar:

// tests/utils.test.js
import { formatDate, escapeHtml, generateId } from '../src/js/utils.js'

describe('Utils', () => {
  test('formatDate formats correctly', () => {
    const date = new Date('2024-01-01T12:00:00')
    expect(formatDate(date)).toMatch(/01\/01\/2024/)
  })

  test('escapeHtml prevents XSS', () => {
    const malicious = '<script>alert("xss")</script>'
    expect(escapeHtml(malicious)).not.toContain('<script>')
  })

  test('generateId creates unique IDs', () => {
    const id1 = generateId()
    const id2 = generateId()
    expect(id1).not.toBe(id2)
  })
})

// tests/api-client.test.js
import APIClient from '../src/js/api-client.js'

describe('APIClient', () => {
  let client

  beforeEach(() => {
    client = new APIClient('http://localhost:8000')
  })

  test('askQuestion sends correct payload', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ answer: 'Test', confidence: 0.9 })
      })
    )

    const response = await client.askQuestion('Test question')
    expect(response.answer).toBe('Test')
  })
})
```

---

### **Fase 15: Optimización y Performance**

#### Paso 15.1: Optimizaciones Frontend
```javascript
En main.js o archivo de configuración:

1. Lazy Loading de Módulos:
   - Cargar api-client solo cuando se necesita
   - Cargar componentes de info-panel on-demand

2. Request Caching:
   - Cache de respuestas frecuentes en memoria
   - Usar Map() para almacenar
   - TTL de 5 minutos

3. Debouncing de Input:
   - Aplicar debounce al input de búsqueda
   - Evitar requests mientras el usuario escribe

4. Image Optimization:
   - Usar WebP con fallback
   - Lazy loading de imágenes
   - Placeholder mientras carga

5. Code Splitting:
   - Si usas bundler, split por rutas
   - Async imports para features grandes

6. Service Worker (PWA):
   - Caché de assets estáticos
   - Offline fallback
   - Background sync para mensajes
```

---

### **Fase 16: Accesibilidad (a11y)**

#### Paso 16.1: Mejoras de Accesibilidad
```html
En index.html y CSS:

1. ARIA Labels:
   - role="main" en main
   - role="complementary" en aside
   - aria-label en botones sin texto
   - aria-live="polite" en messagesContainer

2. Keyboard Navigation:
   - Tab order lógico
   - Focus visible
   - Shortcuts con aria-keyshortcuts

3. Screen Reader Support:
   - Mensajes anunciados
   - Estado de loading anunciado
   - Errores anunciados

4. Color Contrast:
   - Verificar WCAG AA mínimo
   - Usar herramientas como axe

5. Focus Management:
   - Trap focus en modales
   - Return focus después de acciones
   - Skip links

Ejemplo:
<button 
  id="sendButton"
  type="submit"
  aria-label="Enviar pregunta"
  aria-keyshortcuts="Enter">
  <span aria-hidden="true">📤</span>
  <span>Enviar</span>
</button>
```

---

## 🎯 CHECKLIST FINAL DE IMPLEMENTACIÓN

### Backend
- [ ] Estructura de directorios creada
- [ ] Modelos de datos definidos
- [ ] Cliente OpenF1 implementado
- [ ] Red semántica con NetworkX
- [ ] Base de conocimiento poblada
- [ ] Procesador NLP funcional
- [ ] Servicio de consultas completo
- [ ] API endpoints creados
- [ ] CORS configurado
- [ ] Dockerfile backend
- [ ] Tests básicos

### Frontend
- [ ] HTML semántico estructurado
- [ ] CSS responsive y moderno
- [ ] Utils y helpers
- [ ] Cliente API
- [ ] Interfaz de chat funcional
- [ ] Manejo de errores
- [ ] Typing indicators
- [ ] Info panel con entidades
- [ ] Ejemplos de preguntas
- [ ] Dockerfile frontend
- [ ] Nginx configurado

### Docker & DevOps
- [ ] docker-compose.yml
- [ ] .dockerignore files
- [ ] Health checks
- [ ] Volúmenes configurados
- [ ] Network configurado
- [ ] Variables de entorno

### Documentación
- [ ] README principal
- [ ] Comentarios en código
- [ ] API documentation
- [ ] Ejemplos de uso

---

## 🚦 ORDEN DE EJECUCIÓN PARA CURSOR AGENT

### Para Backend (ejecutar en orden):
1. Crear estructura completa de directorios
2. Crear requirements.txt y .env.example
3. Implementar models/nodes.py y schemas.py
4. Implementar core/config.py
5. Implementar services/openf1_client.py
6. Implementar core/semantic_network.py
7. Implementar services/nlp_processor.py
8. Implementar services/knowledge_base.py
9. Implementar services/query_service.py
10. Implementar api/dependencies.py
11. Implementar api/routes.py
12. Implementar api/main.py
13. Crear Dockerfile
14. Probar localmente sin Docker
15. Probar con Docker

### Para Frontend (ejecutar en orden):
1. Crear estructura de directorios
2. Crear index.html completo
3. Crear main.css
4. Crear chat.css
5. Crear components.css
6. Crear utils.js
7. Crear api-client.js
8. Crear chat-ui.js
9. Crear main.js
10. Crear nginx.conf
11. Crear Dockerfile
12. Probar localmente
13. Probar con Docker

### Integración Final:
1. Crear docker-compose.yml
2. Crear README.md
3. Probar sistema completo
4. Ajustar CORS si es necesario
5. Testing end-to-end
6. Optimizaciones finales

---

## 📝 NOTAS IMPORTANTES PARA CURSOR AGENT

### Consideraciones Generales:

1. **Manejo de Errores Robusto:**
   - Cada función debe tener try/except o try/catch
   - Logging detallado de errores
   - Mensajes de error user-friendly
   - Fallbacks cuando sea posible

2. **Performance:**
   - Usar async/await en Python para I/O
   - Evitar N+1 queries
   - Implementar caché donde tenga sentido
   - Limitar profundidad de búsquedas en grafo

3. **Seguridad:**
   - Validar todos los inputs
   - Escapar HTML en frontend
   - CORS correctamente configurado
   - Rate limiting (opcional para v1)
   - No exponer información sensible en logs

4. **Código Limpio:**
   - Nombres descriptivos de variables
   - Funciones pequeñas y focalizadas
   - Comentarios donde sea necesario
   - Type hints en Python
   - JSDoc en JavaScript

5. **Testing:**
   - Tests unitarios para funciones críticas
   - Tests de integración para API
   - Tests E2E básicos
   - Coverage mínimo del 70%

---

## 🔍 DETALLES DE IMPLEMENTACIÓN CRÍTICOS

### Backend - Poblado de Red Semántica:

**Estrategia de Mapeo OpenF1 → Nodos:**

```python
# Ejemplo de mapeo de datos:

1. Pilotos (drivers):
   API Response → PilotoNode
   {
     "driver_number": 1,
     "full_name": "Max Verstappen",
     "country_code": "NED",
     "team_name": "Red Bull Racing"
   }
   →
   {
     "node_id": "driver_1",
     "nombre": "Max Verstappen",
     "numero_piloto": 1,
     "nacionalidad": "Países Bajos",  # Mapear código a nombre completo
     "driver_number": 1
   }

2. Sesiones (sessions):
   API Response → SesionNode
   {
     "session_key": 9158,
     "session_name": "Race",
     "date_start": "2024-03-02T15:00:00",
     "circuit_key": 7,
     "year": 2024
   }
   →
   {
     "node_id": "session_9158",
     "session_key": 9158,
     "tipo": "R",  # Extraer primera letra
     "fecha": "2024-03-02",
     "session_name": "Race",
     "year": 2024
   }

3. Circuitos (meetings):
   API Response → CircuitoNode
   {
     "circuit_key": 7,
     "circuit_short_name": "Bahrain",
     "country_name": "Bahrain",
     "location": "Sakhir"
   }
   →
   {
     "node_id": "circuit_7",
     "nombre_oficial": "Bahrain International Circuit",
     "pais": "Bahrain",
     "longitud_metros": 5412.0,  # Hardcodear o estimar
     "circuit_key": 7
   }
```

### Backend - Procesamiento NLP:

**Patrones de Preguntas en Español:**

```python
# Ejemplos de regex patterns:

PATTERNS = {
    'pilot_info': [
        r'¿quién es ([^?]+)\??',
        r'¿qué piloto.+número (\d+)',
        r'información.+piloto ([^?]+)',
        r'dame datos.+([A-Z][a-z]+ [A-Z][a-z]+)'
    ],
    'team_info': [
        r'¿para qué equipo.+(?:corre|conduce) ([^?]+)',
        r'¿qué equipo.+([^?]+)',
        r'¿en qué equipo está ([^?]+)',
        r'equipo de ([^?]+)'
    ],
    'winner_info': [
        r'¿quién ganó.+(?:GP|Gran Premio) de ([^?]+)',
        r'ganador.+([^?]+) (\d{4})',
        r'¿quién se llevó.+([^?]+)',
        r'resultado.+([^?]+)'
    ],
    'motor_info': [
        r'¿qué motor usa ([^?]+)',
        r'motor de ([^?]+)',
        r'¿qué motor tiene ([^?]+)',
        r'fabricante.+motor.+([^?]+)'
    ],
    'circuit_info': [
        r'¿dónde está.+circuito de ([^?]+)',
        r'ubicación.+([^?]+)',
        r'¿en qué país.+([^?]+)',
        r'circuito de ([^?]+)'
    ]
}

# Diccionario de sinónimos:
SYNONYMS = {
    'equipo': ['escudería', 'team', 'conjunto'],
    'piloto': ['corredor', 'driver', 'conductor'],
    'motor': ['propulsor', 'unidad de potencia', 'engine'],
    'circuito': ['pista', 'trazado', 'autódromo'],
    'ganó': ['venció', 'triunfó', 'se impuso']
}

# Nombres de pilotos conocidos (2024):
KNOWN_DRIVERS = [
    'Max Verstappen', 'Sergio Pérez', 'Lewis Hamilton',
    'George Russell', 'Charles Leclerc', 'Carlos Sainz',
    'Lando Norris', 'Oscar Piastri', 'Fernando Alonso',
    'Lance Stroll', 'Pierre Gasly', 'Esteban Ocon',
    # ... más pilotos
]

# Equipos conocidos:
KNOWN_TEAMS = {
    'Red Bull': 'Red Bull Racing',
    'Mercedes': 'Mercedes-AMG Petronas',
    'Ferrari': 'Scuderia Ferrari',
    'McLaren': 'McLaren Racing',
    'Aston Martin': 'Aston Martin Aramco',
    'Alpine': 'Alpine F1 Team',
    'Williams': 'Williams Racing',
    'AlphaTauri': 'Scuderia AlphaTauri',
    'Alfa Romeo': 'Alfa Romeo F1 Team',
    'Haas': 'Haas F1 Team'
}
```

### Backend - Relaciones en Red Semántica:

**Creación de Aristas:**

```python
# Pseudo-código para crear relaciones:

def _create_relationships(self):
    # 1. Conduce_para (Piloto → Equipo)
    for driver_node in self.network.find_nodes_by_type('piloto'):
        team_name = driver_node['attributes']['team_name']
        team_node_id = f"team_{normalize(team_name)}"
        self.network.add_edge(
            source=driver_node['id'],
            target=team_node_id,
            relation='conduce_para',
            attributes={'season': 2024}
        )
    
    # 2. Usa_motor (Equipo → Motor)
    TEAM_ENGINE_MAP = {
        'red_bull_racing': 'engine_honda_rbpt',
        'mercedes_amg_petronas': 'engine_mercedes',
        'scuderia_ferrari': 'engine_ferrari',
        'mclaren_racing': 'engine_mercedes',
        # ... más mapeos
    }
    for team_id, engine_id in TEAM_ENGINE_MAP.items():
        self.network.add_edge(
            source=f"team_{team_id}",
            target=engine_id,
            relation='usa_motor'
        )
    
    # 3. Tiene_ganador (Sesión → Piloto)
    for session in sessions_with_results:
        winner_driver_number = session['winner']
        self.network.add_edge(
            source=f"session_{session['session_key']}",
            target=f"driver_{winner_driver_number}",
            relation='tiene_ganador',
            attributes={'position': 1}
        )
    
    # 4. Ocurre_en (Sesión → Circuito)
    for session in all_sessions:
        self.network.add_edge(
            source=f"session_{session['session_key']}",
            target=f"circuit_{session['circuit_key']}",
            relation='ocurre_en'
        )
    
    # 5. Está_en (Circuito → País)
    for circuit in all_circuits:
        country_id = f"country_{normalize(circuit['country'])}"
        # Crear nodo país si no existe
        if not self.network.get_node_details(country_id):
            self.network.add_node(
                node_id=country_id,
                node_type='pais',
                attributes={'nombre': circuit['country']}
            )
        self.network.add_edge(
            source=f"circuit_{circuit['circuit_key']}",
            target=country_id,
            relation='esta_en'
        )
    
    # 6. Es_un_tipo_de (Sesión → Tipo)
    TYPE_NODES = ['tipo_race', 'tipo_qualifying', 'tipo_practice']
    for type_id in TYPE_NODES:
        if not self.network.get_node_details(type_id):
            self.network.add_node(
                node_id=type_id,
                node_type='tipo_evento',
                attributes={'nombre': type_id.split('_')[1].capitalize()}
            )
    
    for session in all_sessions:
        session_type = session['tipo']  # 'R', 'Q', 'P'
        type_map = {'R': 'tipo_race', 'Q': 'tipo_qualifying', 'P': 'tipo_practice'}
        self.network.add_edge(
            source=f"session_{session['session_key']}",
            target=type_map[session_type],
            relation='es_un_tipo_de'
        )
```

### Frontend - Estructura HTML Detallada:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Sistema de Q&A sobre Fórmula 1 con Redes Semánticas">
    <meta name="author" content="Tu Nombre">
    <title>F1 Q&A System</title>
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Stylesheets -->
    <link rel="stylesheet" href="/src/css/main.css">
    <link rel="stylesheet" href="/src/css/chat.css">
    <link rel="stylesheet" href="/src/css/components.css">
    
    <!-- Favicon -->
    <link rel="icon" href="/favicon.ico">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <div class="logo">
                <h1>🏎️ F1 Q&A System</h1>
                <p class="subtitle">Sistema Inteligente de Preguntas sobre Fórmula 1</p>
            </div>
            <div class="status-indicator" id="statusIndicator">
                <span class="status-dot"></span>
                <span class="status-text">Verificando conexión...</span>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container">
        <div class="main-layout">
            <!-- Chat Section -->
            <section class="chat-container" role="main">
                <!-- Welcome Screen -->
                <div class="welcome-screen" id="welcomeScreen">
                    <h2>¡Bienvenido al Sistema de Q&A de F1! 🏁</h2>
                    <p>Pregunta cualquier cosa sobre Fórmula 1 y obtén respuestas basadas en nuestra base de conocimiento.</p>
                    
                    <div class="example-questions">
                        <h3>Preguntas de ejemplo:</h3>
                        <ul class="example-list">
                            <li class="example-item" data-question="¿Quién es Max Verstappen?">
                                <span class="icon">👤</span>
                                <span>¿Quién es Max Verstappen?</span>
                            </li>
                            <li class="example-item" data-question="¿Para qué equipo corre Lewis Hamilton?">
                                <span class="icon">🏁</span>
                                <span>¿Para qué equipo corre Lewis Hamilton?</span>
                            </li>
                            <li class="example-item" data-question="¿Quién ganó el GP de Mónaco 2024?">
                                <span class="icon">🏆</span>
                                <span>¿Quién ganó el GP de Mónaco 2024?</span>
                            </li>
                            <li class="example-item" data-question="¿Qué motor usa Red Bull?">
                                <span class="icon">⚙️</span>
                                <span>¿Qué motor usa Red Bull?</span>
                            </li>
                            <li class="example-item" data-question="¿Dónde está el circuito de Spa?">
                                <span class="icon">📍</span>
                                <span>¿Dónde está el circuito de Spa?</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- Messages Container -->
                <div class="messages-container" id="messagesContainer" role="log" aria-live="polite" aria-atomic="false">
                    <!-- Messages will be inserted here dynamically -->
                </div>

                <!-- Typing Indicator -->
                <div class="typing-indicator" id="typingIndicator" style="display: none;">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>

                <!-- Input Container -->
                <div class="input-container">
                    <form id="questionForm" class="question-form">
                        <input 
                            type="text" 
                            id="questionInput" 
                            class="question-input"
                            placeholder="Escribe tu pregunta sobre F1..."
                            autocomplete="off"
                            maxlength="500"
                            required
                            aria-label="Campo de pregunta"
                        />
                        <button 
                            type="submit" 
                            id="sendButton" 
                            class="send-button"
                            aria-label="Enviar pregunta"
                        >
                            <span class="button-text">Enviar</span>
                            <svg class="send-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="22" y1="2" x2="11" y2="13"></line>
                                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                            </svg>
                        </button>
                    </form>
                </div>
            </section>

            <!-- Info Panel -->
            <aside class="info-panel" id="infoPanel" role="complementary">
                <h3>Información Adicional</h3>
                <div id="relatedEntities" class="related-entities">
                    <p class="empty-state">Las entidades relacionadas aparecerán aquí</p>
                </div>
                
                <div class="confidence-section" id="confidenceSection" style="display: none;">
                    <h4>Nivel de Confianza</h4>
                    <div class="confidence-meter">
                        <div class="confidence-bar">
                            <div class="confidence-fill" id="confidenceFill" style="width: 0%"></div>
                        </div>
                        <p class="confidence-text" id="confidenceText">0%</p>
                    </div>
                </div>
            </aside>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <p>&copy; 2024 F1 Q&A System | Proyecto Universitario</p>
            <p>
                <a href="/docs" target="_blank">Documentación</a> | 
                <a href="https://openf1.org" target="_blank">OpenF1 API</a> | 
                <span>v1.0.0</span>
            </p>
        </div>
    </footer>

    <!-- Scripts -->
    <script type="module" src="/src/js/utils.js"></script>
    <script type="module" src="/src/js/api-client.js"></script>
    <script type="module" src="/src/js/chat-ui.js"></script>
    <script type="module" src="/src/js/main.js"></script>
</body>
</html>
```

### Frontend - CSS Variables Completas:

```css
/* src/css/main.css - Variables */
:root {
    /* Colors - F1 Theme */
    --primary-color: #E10600;
    --primary-dark: #B30500;
    --primary-light: #FF1E00;
    --secondary-color: #15151E;
    --secondary-light: #2A2A3A;
    --accent-color: #00D9FF;
    --accent-dark: #00B8D4;
    
    /* Backgrounds */
    --bg-primary: #FFFFFF;
    --bg-secondary: #F5F5F5;
    --bg-tertiary: #EEEEEE;
    --bg-dark: #15151E;
    
    /* Text Colors */
    --text-primary: #15151E;
    --text-secondary: #666666;
    --text-tertiary: #999999;
    --text-light: #FFFFFF;
    
    /* Status Colors */
    --success-color: #4CAF50;
    --warning-color: #FFC107;
    --error-color: #F44336;
    --info-color: #2196F3;
    
    /* Shadows */
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
    --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.15);
    --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.2);
    --shadow-xl: 0 12px 24px rgba(0, 0, 0, 0.25);
    
    /* Border Radius */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    --radius-full: 9999px;
    
    /* Spacing */
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
    --spacing-2xl: 48px;
    
    /* Transitions */
    --transition-fast: 0.15s ease;
    --transition-base: 0.3s ease;
    --transition-slow: 0.5s ease;
    
    /* Typography */
    --font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-size-xs: 0.75rem;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    --font-size-2xl: 1.5rem;
    --font-size-3xl: 2rem;
    
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
    
    --line-height-tight: 1.25;
    --line-height-normal: 1.5;
    --line-height-relaxed: 1.75;
    
    /* Breakpoints (para referencia) */
    --breakpoint-sm: 640px;
    --breakpoint-md: 768px;
    --breakpoint-lg: 1024px;
    --breakpoint-xl: 1280px;
}

/* Dark mode variables (opcional) */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #1A1A1A;
        --bg-secondary: #2A2A2A;
        --bg-tertiary: #3A3A3A;
        --text-primary: #FFFFFF;
        --text-secondary: #CCCCCC;
        --text-tertiary: #999999;
    }
}
```

### Frontend - Ejemplo de Respuesta Formateada:

```javascript
// En chat-ui.js - renderMessage con formatting

renderMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${message.type}`;
    messageDiv.id = `message-${message.id}`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    
    // Format text (detectar links, bold, etc.)
    const formattedText = this.formatMessageText(message.text);
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.innerHTML = formattedText;
    
    const metaDiv = document.createElement('div');
    metaDiv.className = 'message-metadata';
    metaDiv.textContent = formatDate(message.timestamp);
    
    bubble.appendChild(textDiv);
    bubble.appendChild(metaDiv);
    messageDiv.appendChild(bubble);
    
    // Animation
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(10px)';
    
    this.elements.messagesContainer.appendChild(messageDiv);
    
    // Trigger animation
    requestAnimationFrame(() => {
        messageDiv.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
    });
    
    this.scrollToBottom();
}

formatMessageText(text) {
    // Escape HTML first
    let formatted = escapeHtml(text);
    
    // Detect and format URLs
    formatted = formatted.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank" rel="noopener">$1</a>'
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
    
    // Line breaks
    formatted = formatted.replace(/\n/g, '<br>');
    
    return formatted;
}
```

---

## 🚀 COMANDOS DE DESARROLLO RÁPIDO

### Setup Inicial Completo:

```bash
# 1. Crear estructura del proyecto
mkdir -p f1-qa-system/{backend/{src/{api,core,models,services,utils},env,tests},frontend/{public,src/{css,js,assets/{images,icons}}}}

# 2. Navegar al proyecto
cd f1-qa-system

# 3. Inicializar git
git init
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "node_modules/" >> .gitignore

# 4. Crear archivos vacíos necesarios
touch backend/requirements.txt
touch backend/Dockerfile
touch backend/README.md
touch frontend/Dockerfile
touch frontend/nginx.conf
touch frontend/README.md
touch docker-compose.yml
touch Makefile
touch README.md

# 5. Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 6. Instalar dependencias backend
pip install fastapi uvicorn pydantic pydantic-settings httpx python-dotenv networkx nltk unidecode pytest

# 7. Crear requirements.txt
pip freeze > requirements.txt

# 8. Frontend setup (si usas npm)
cd ../frontend
npm init -y
npm install --save-dev prettier eslint

# 9. Volver a raíz
cd ..

# 10. Iniciar desarrollo con Docker
docker-compose up --build
```

### Comandos de Testing:

```bash
# Backend tests
cd backend
pytest -v --cov=src

# Frontend tests (si usas Jest)
cd frontend
npm test

# Test de integración completo
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Quién es Max Verstappen?"}'

# Health check
curl http://localhost:8000/api/v1/health
```

---

## 📚 RECURSOS Y REFERENCIAS

### APIs y Documentación:
- OpenF1 API: https://openf1.org
- FastAPI Docs: https://fastapi.tiangolo.com
- NetworkX Docs: https://networkx.org/documentation
- MDN Web Docs: https://developer.mozilla.org

### Herramientas Útiles:
- Postman/Insomnia: Para testing de API
- Docker Desktop: Para gestión de contenedores
- VS Code Extensions:
  - Python
  - Pylance
  - Docker
  - Live Server
  - Prettier
  - ESLint

### Debugging:
- Backend: uvicorn logs, Python debugger (pdb)
- Frontend: Browser DevTools, Console logging
- Docker: `docker logs -f <container_name>`

---

## ✅ CRITERIOS DE ÉXITO

El proyecto estará completo cuando:

1. ✅ El backend carga exitosamente datos de OpenF1
2. ✅ La red semántica contiene todos los tipos de nodos
3. ✅ El NLP puede procesar preguntas en español
4. ✅ Las consultas retornan respuestas correctas
5. ✅ El frontend renderiza la interfaz de chat
6. ✅ Los mensajes se envían y reciben correctamente
7. ✅ El panel de información muestra entidades relacionadas
8. ✅ Docker compose levanta ambos servicios
9. ✅ Los health checks pasan correctamente
10. ✅ La aplicación funciona end-to-end

---

## 🎓 PARA CURSOR AGENT: INSTRUCCIONES FINALES

**Al implementar cada archivo:**
1. Lee el plan completo primero
2. Implementa paso a paso sin saltarte detalles
3. Agrega logging detallado
4. Incluye docstrings/comentarios
5. Maneja todos los casos de error
6. Valida inputs
7. Usa type hints (Python) y JSDoc (JavaScript)
8. Prueba cada componente antes de continuar

**Orden sugerido de implementación:**
1. Backend primero (día 1-2)
2. Testing del backend
3. Frontend después (día 3)
4. Integración (día 4)
5. Docker y deployment (día 4-5)
6. Testing final y optimizaciones

**Si encuentras errores:**
- Lee el traceback completo
- Verifica imports y dependencias
- Revisa la estructura de datos
- Usa print/console.log para debugging
- Consulta la documentación oficial

¡Buena suerte con la implementación! 🏎️💨