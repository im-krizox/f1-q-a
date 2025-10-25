# 🏎️ F1 Q&A System - Sistema de Preguntas y Respuestas con Redes Semánticas

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema inteligente de preguntas y respuestas sobre Fórmula 1 utilizando **redes semánticas**, **procesamiento de lenguaje natural** (NLP) y la **API de OpenF1**. Desarrollado con arquitectura moderna, containerizado con Docker y con una interfaz web interactiva.

<p align="center">
  <img src="https://via.placeholder.com/800x400/15151E/E10600?text=F1+Q%26A+System" alt="F1 Q&A System Demo">
</p>

## 📋 Descripción

Este proyecto implementa un **sistema completo de Q&A** que permite hacer preguntas en lenguaje natural en español sobre Fórmula 1 y obtener respuestas precisas e inteligentes basadas en una red semántica de conocimiento. 

### ¿Qué hace este sistema?

- 🤖 **Entiende preguntas en español** usando procesamiento de lenguaje natural
- 🕸️ **Representa conocimiento** mediante una red semántica (grafo de entidades y relaciones)
- 📊 **Consulta datos en tiempo real** desde la API oficial de OpenF1
- 💬 **Genera respuestas inteligentes** en lenguaje natural con contexto relevante
- 🌐 **Interfaz web moderna** tipo chat para interacción intuitiva

### Casos de Uso

- Consultar información sobre pilotos, equipos, circuitos y motores
- Descubrir relaciones entre entidades de F1
- Obtener datos actualizados de la temporada actual
- Explorar el grafo de conocimiento de Fórmula 1

## 🏗️ Arquitectura

```
F1-Q&A/
├── backend/                 # Backend FastAPI + Python
│   ├── src/
│   │   ├── api/            # Endpoints y rutas
│   │   ├── core/           # Red semántica y configuración
│   │   ├── models/         # Modelos de datos
│   │   ├── services/       # Lógica de negocio
│   │   └── utils/          # Utilidades
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Frontend Web
│   ├── public/            # HTML principal
│   ├── src/
│   │   ├── css/           # Estilos
│   │   └── js/            # Lógica cliente
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml      # Orquestación de servicios
└── README.md
```

### Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────────┐
│                      CLIENTE WEB                          │
│                    (Navegador)                            │
└───────────────────────┬──────────────────────────────────┘
                        │ HTTP
                        ▼
┌──────────────────────────────────────────────────────────┐
│                   FRONTEND LAYER                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Nginx:80 (Reverse Proxy)              │  │
│  │  • Servir HTML/CSS/JS estáticos                    │  │
│  │  • Proxy /api/* → Backend                          │  │
│  │  • Compresión gzip, Headers de seguridad           │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────┬──────────────────────────────────┘
                        │ Proxy Pass
                        ▼
┌──────────────────────────────────────────────────────────┐
│                   BACKEND LAYER                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │         FastAPI:8000 (REST API)                    │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │         NLP Processor                        │  │  │
│  │  │  • Análisis de preguntas en español          │  │  │
│  │  │  • Extracción de entidades                   │  │  │
│  │  │  • Clasificación de intenciones              │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │         Query Service                        │  │  │
│  │  │  • Consultas a la red semántica              │  │  │
│  │  │  • Generación de respuestas                  │  │  │
│  │  │  • Cálculo de confianza                      │  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────┐  │  │
│  │  │      Semantic Network (NetworkX)            │  │  │
│  │  │  • Grafo dirigido de entidades              │  │  │
│  │  │  • Nodos: Pilotos, Equipos, Circuitos, etc. │  │  │
│  │  │  • Relaciones: conduce_para, usa_motor, etc.│  │  │
│  │  └──────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────┬──────────────────────────────────┘
                        │ HTTP REST
                        ▼
┌──────────────────────────────────────────────────────────┐
│                   EXTERNAL API                            │
│              OpenF1 API (api.openf1.org)                  │
│  • Datos oficiales de F1                                  │
│  • Pilotos, Equipos, Sesiones, Circuitos                 │
└──────────────────────────────────────────────────────────┘
```

### Flujo de Datos

1. **Usuario hace una pregunta** → Frontend (HTML/JS)
2. **Frontend envía request** → Nginx proxy → Backend API
3. **Backend procesa con NLP** → Identifica intención y entidades
4. **Consulta red semántica** → Encuentra nodos y relaciones relevantes
5. **Genera respuesta inteligente** → Con confianza y metadatos
6. **Retorna JSON** → Frontend recibe y renderiza
7. **Usuario ve respuesta** → En interfaz de chat amigable

### Tecnologías Utilizadas

**Frontend:**
- HTML5 (Semantic markup)
- CSS3 (Variables CSS, Flexbox, Grid, Animations)
- JavaScript ES6+ (Modules, Fetch API)
- Nginx (Servidor web)

**Backend:**
- Python 3.11
- FastAPI (API REST)
- NetworkX (Redes Semánticas)
- Pydantic (Validación de datos)
- httpx (Cliente HTTP asíncrono)
- NLTK / unidecode (Procesamiento NLP)

**Datos:**
- OpenF1 API (Datos oficiales de F1)

**Infraestructura:**
- Docker & Docker Compose
- Uvicorn (Servidor ASGI)
- Nginx (Servidor web)

---

## 🛠️ Cómo se Construyó este Proyecto

### Metodología de Desarrollo

Este proyecto se desarrolló siguiendo una metodología incremental y modular:

#### Fase 1: Planificación y Diseño (Día 1)
1. **Análisis de Requisitos**
   - Definir funcionalidades del sistema de Q&A
   - Identificar tipos de preguntas a soportar
   - Diseñar estructura de la red semántica

2. **Arquitectura del Sistema**
   - Selección de tecnologías (FastAPI, NetworkX, etc.)
   - Diseño de la API REST
   - Definición de modelos de datos

#### Fase 2: Desarrollo del Backend (Días 2-7)

**2.1 Infraestructura Base**
- Configuración del entorno Python y dependencias
- Estructura modular del proyecto
- Sistema de configuración con variables de entorno

**2.2 Red Semántica (Core)**
```python
# Implementación con NetworkX
- Definición de tipos de nodos (Piloto, Equipo, Motor, etc.)
- Creación de relaciones semánticas
- Métodos de consulta y exploración del grafo
```

**2.3 Integración con OpenF1 API**
- Cliente HTTP asíncrono con `httpx`
- Carga automática de datos al iniciar
- Manejo robusto de errores y timeouts

**2.4 Procesador NLP**
- Análisis de preguntas en español
- Extracción de entidades (nombres, números, etc.)
- Clasificación de tipos de consulta
- Normalización de texto (acentos, mayúsculas)

**2.5 Servicio de Consultas**
- Motor de consultas a la red semántica
- Generación de respuestas en lenguaje natural
- Cálculo de nivel de confianza
- Inclusión de metadatos relevantes

**2.6 API REST con FastAPI**
- Endpoints documentados automáticamente (OpenAPI)
- Validación con Pydantic
- Manejo de CORS para frontend
- Health checks y estadísticas

#### Fase 3: Desarrollo del Frontend (Días 8-12)

**3.1 Diseño de la Interfaz**
- Sistema de diseño con tema de F1 (rojo #E10600)
- Variables CSS para consistencia
- Diseño responsive (mobile-first)

**3.2 Interfaz de Chat**
- Componente de mensajes con burbujas
- Indicador de "escribiendo..."
- Panel de información lateral
- Preguntas de ejemplo interactivas

**3.3 Cliente JavaScript**
- Módulos ES6 separados por responsabilidad
- Cliente HTTP con Fetch API
- Manejo de estados y errores
- Health checks automáticos

**3.4 Integración con Nginx**
- Servidor web de producción
- Reverse proxy al backend
- Compresión y caché
- Headers de seguridad

#### Fase 4: Integración y DevOps (Días 13-15)

**4.1 Containerización**
- Dockerfiles optimizados (multi-stage builds)
- Docker Compose para orquestación
- Variables de entorno configurables
- Volúmenes para persistencia

**4.2 Testing**
- Pruebas de integración con `test_api.py`
- Validación de endpoints
- Testing manual del flujo completo

**4.3 Documentación**
- README completos por componente
- Guías de inicio rápido
- Ejemplos de uso
- Troubleshooting

### Decisiones Técnicas Clave

#### ¿Por qué NetworkX para la Red Semántica?
- **Flexibilidad**: Soporta grafos dirigidos con atributos
- **Eficiencia**: Algoritmos optimizados para consultas
- **Simplicidad**: API intuitiva para trabajar con grafos
- **Escalabilidad**: Maneja cientos de nodos sin problemas

#### ¿Por qué FastAPI?
- **Rendimiento**: Uno de los frameworks más rápidos de Python
- **Type Hints**: Validación automática con Pydantic
- **Async**: Soporte nativo para operaciones asíncronas
- **Documentación**: Genera OpenAPI/Swagger automáticamente

#### ¿Por qué JavaScript Vanilla?
- **Sin dependencias**: No requiere build tools
- **Rápido**: Carga instantánea sin frameworks pesados
- **Mantenible**: Código simple y directo
- **Educativo**: Fácil de entender para otros desarrolladores

### Desafíos y Soluciones

| Desafío | Solución Implementada |
|---------|----------------------|
| **Análisis de preguntas en español** | NLP con normalización, análisis de patrones y keywords |
| **Ambigüedad en consultas** | Sistema de confianza basado en matches y contexto |
| **Datos inconsistentes de API** | Validación y limpieza con valores por defecto |
| **Latencia en respuestas** | Operaciones asíncronas y caché en memoria |
| **CORS entre frontend/backend** | Configuración CORS en FastAPI + Nginx proxy |

### Líneas de Código

```
Backend Python:     ~1,500 líneas
Frontend JS/CSS:    ~1,500 líneas
Documentación:      ~2,000 líneas
Tests:              ~200 líneas
──────────────────────────────
Total:              ~5,200 líneas
```

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker 20.10+
- Docker Compose 2.0+
- (Opcional) Python 3.11+ para desarrollo local

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd F1-Q&A
```

2. **Iniciar con Docker Compose**
```bash
docker-compose up --build
```

3. **Acceder a la aplicación**
- **Frontend (Interfaz Web)**: http://localhost
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Health Check Backend**: http://localhost:8000/api/v1/health
- **Health Check Frontend**: http://localhost/health

### 🎯 Uso Rápido

1. Abre tu navegador en http://localhost
2. Verás una interfaz de chat con preguntas de ejemplo
3. Haz clic en una pregunta ejemplo o escribe tu propia pregunta
4. ¡Obtén respuestas instantáneas sobre F1! 🏎️

#### Ejemplos de Preguntas:
- "¿Quién es Max Verstappen?"
- "¿Para qué equipo corre Lewis Hamilton?"
- "¿Quién ganó el GP de Mónaco 2024?"
- "¿Qué motor usa Red Bull?"
- "¿Dónde está el circuito de Spa?"

## 📊 Red Semántica

El sistema utiliza una red semántica (grafo dirigido) para representar el conocimiento sobre F1:

### Tipos de Nodos

- **Piloto**: Información de pilotos (nombre, número, nacionalidad)
- **Equipo**: Equipos de F1 (nombre, jefe de equipo)
- **Motor**: Fabricantes de motores (Mercedes, Ferrari, Honda RBPT, Renault)
- **Circuito**: Circuitos del calendario (ubicación, país)
- **Sesión**: Carreras, clasificaciones y prácticas
- **País**: Países donde se ubican los circuitos

### Relaciones

```
Piloto --[conduce_para]--> Equipo --[usa_motor]--> Motor
Sesión --[ocurre_en]--> Circuito --[esta_en]--> País
Sesión --[tiene_ganador]--> Piloto
Sesión --[es_un_tipo_de]--> TipoEvento
```

## 🔌 API Endpoints

### Consultas Principales

**POST /api/v1/ask**
```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Quién es Max Verstappen?"
  }'
```

**Respuesta:**
```json
{
  "answer": "Max Verstappen es un piloto de Fórmula 1 de nacionalidad Países Bajos con el número 1. Actualmente corre para Red Bull Racing.",
  "confidence": 0.95,
  "related_entities": [
    {"type": "piloto", "name": "Max Verstappen", "id": "driver_1"},
    {"type": "equipo", "name": "Red Bull Racing", "id": "team_red_bull_racing"}
  ],
  "query_type": "pilot_info",
  "metadata": {
    "pilot_name": "Max Verstappen",
    "team_name": "Red Bull Racing",
    "nationality": "Países Bajos"
  }
}
```

### Otros Endpoints

- `GET /api/v1/health` - Estado del sistema
- `GET /api/v1/stats` - Estadísticas de la red semántica
- `GET /api/v1/entities/{type}` - Listar entidades (drivers, teams, circuits, sessions)
- `GET /api/v1/network/explore/{node_id}` - Explorar vecindario de un nodo
- `POST /api/v1/reload` - Recargar base de conocimiento

## 💬 Ejemplos de Preguntas

### Información de Pilotos
```
¿Quién es Max Verstappen?
¿Qué piloto tiene el número 44?
Información sobre Lewis Hamilton
```

### Equipos
```
¿Para qué equipo corre Lewis Hamilton?
¿En qué equipo está Fernando Alonso?
Equipo de Charles Leclerc
```

### Motores
```
¿Qué motor usa Red Bull?
¿Qué motor utiliza Ferrari?
Motor de McLaren
```

### Circuitos
```
¿Dónde está el circuito de Spa?
¿En qué país está Silverstone?
Ubicación del circuito de Mónaco
```

## 🧪 Testing

### Probar el Backend

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Pregunta simple
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Quién es Max Verstappen?"}'

# Listar pilotos
curl http://localhost:8000/api/v1/entities/drivers?limit=5

# Estadísticas
curl http://localhost:8000/api/v1/stats
```

### Testing con Python

```python
import requests

# Cliente simple
class F1QAClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def ask(self, question):
        response = requests.post(
            f"{self.base_url}/api/v1/ask",
            json={"question": question}
        )
        return response.json()
    
    def get_entities(self, entity_type, limit=10):
        response = requests.get(
            f"{self.base_url}/api/v1/entities/{entity_type}",
            params={"limit": limit}
        )
        return response.json()

# Uso
client = F1QAClient()
result = client.ask("¿Para qué equipo corre Lewis Hamilton?")
print(result["answer"])
```

## 🛠️ Desarrollo

### Backend Local (sin Docker)

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Variables de Entorno

Crear archivo `.env` en `backend/env/`:

```env
OPENF1_BASE_URL=https://api.openf1.org/v1
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
LOG_LEVEL=INFO
```

## 📖 Documentación

### Documentación de la Aplicación
- **Frontend README**: [frontend/README.md](frontend/README.md)
- **Backend README**: [backend/README.md](backend/README.md)
- **Quickstart Completo**: [QUICKSTART_FRONTEND.md](QUICKSTART_FRONTEND.md)
- **Plan del Proyecto**: [f1_qa_project_plan.md](f1_qa_project_plan.md)

### Documentación de la API
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

### Resúmenes de Implementación
- **Frontend**: [FRONTEND_IMPLEMENTATION_SUMMARY.md](FRONTEND_IMPLEMENTATION_SUMMARY.md)
- **Backend**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## 🎯 Características Principales

✅ **Interfaz Web Moderna**
- Chat interactivo con diseño responsive
- Indicadores visuales de estado y typing
- Panel de información con entidades relacionadas
- Animaciones suaves y UX intuitiva
- Preguntas de ejemplo clicables
- Atajos de teclado

✅ **Procesamiento NLP en Español**
- Análisis de preguntas en lenguaje natural
- Extracción de entidades y clasificación de intenciones
- Soporte para sinónimos y variaciones

✅ **Red Semántica**
- Grafo de conocimiento con NetworkX
- Múltiples tipos de nodos y relaciones
- Consultas eficientes y exploración de vecindarios

✅ **Integración con OpenF1 API**
- Datos oficiales y actualizados
- Información de pilotos, equipos, circuitos y sesiones
- Carga automática al iniciar

✅ **API REST Completa**
- Endpoints documentados con OpenAPI
- Validación de datos con Pydantic
- Manejo robusto de errores
- CORS configurado

✅ **Respuestas Inteligentes**
- Generación de respuestas en lenguaje natural
- Nivel de confianza calculado
- Entidades relacionadas incluidas
- Metadata adicional

## 📈 Estadísticas del Sistema

Una vez iniciado, el sistema carga automáticamente:
- ~20 pilotos
- ~10 equipos
- ~4 fabricantes de motores
- ~20+ circuitos
- ~50+ sesiones (del año configurado)
- Múltiples países

Total: **100+ nodos** y **200+ relaciones**

## 🔧 Comandos Útiles

```bash
# Ver logs del backend
docker-compose logs -f backend

# Reiniciar servicios
docker-compose restart

# Detener todo
docker-compose down

# Detener y limpiar volúmenes
docker-compose down -v

# Reconstruir y reiniciar
docker-compose up --build --force-recreate
```

## 🐛 Troubleshooting

### El backend no inicia
```bash
# Ver logs detallados
docker-compose logs backend

# Verificar que el puerto 8000 esté libre
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows
```

### Error al cargar datos de OpenF1
- Verificar conexión a internet
- Verificar que la API de OpenF1 esté disponible: https://api.openf1.org/v1
- Revisar logs para ver detalles del error

### Respuestas con baja confianza
- Reformular la pregunta con más contexto
- Usar nombres completos (ej: "Lewis Hamilton" en vez de "Hamilton")
- Verificar que la entidad exista en el sistema

## 🚧 Roadmap

- [x] **Frontend web con interfaz de chat** ✅
- [x] **Diseño responsive y moderno** ✅
- [x] **Indicadores visuales y animaciones** ✅
- [ ] Más tipos de consultas (histórico, comparaciones)
- [ ] Soporte para otros idiomas
- [ ] Cache de respuestas frecuentes
- [ ] Datos de resultados de carreras
- [ ] Visualización de la red semántica
- [ ] Exportar conversaciones
- [ ] Dark mode
- [ ] PWA capabilities

## 🤝 Contribución

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📊 Estadísticas del Proyecto

### Métricas de Desarrollo

| Métrica | Valor |
|---------|-------|
| **Tiempo de desarrollo** | ~15 días |
| **Commits totales** | 32+ commits |
| **Líneas de código** | ~5,200 líneas |
| **Archivos fuente** | 25+ archivos |
| **Endpoints API** | 8 endpoints |
| **Tipos de consultas** | 5+ tipos soportados |
| **Entidades en red** | 100+ nodos |
| **Relaciones** | 200+ edges |

### Cobertura Funcional

- ✅ Preguntas sobre pilotos
- ✅ Preguntas sobre equipos
- ✅ Preguntas sobre motores
- ✅ Preguntas sobre circuitos
- ✅ Preguntas sobre ganadores
- ✅ Exploración de relaciones
- ✅ Interfaz web interactiva
- ⏳ Comparaciones entre entidades (roadmap)
- ⏳ Datos históricos (roadmap)
- ⏳ Visualización del grafo (roadmap)

---

## 🌟 Características Destacadas

### 1. Procesamiento de Lenguaje Natural Avanzado

El sistema entiende múltiples formas de hacer la misma pregunta:

```python
# Todas estas preguntas obtienen la misma respuesta
"¿Quién es Max Verstappen?"
"Quién es Max Verstappen"
"quien es max verstappen"  # Sin acentos
"max verstappen"           # Sin pregunta explícita
"información sobre Max Verstappen"
"dime sobre max"           # Nombre incompleto
```

### 2. Respuestas Contextuales Inteligentes

Las respuestas incluyen:
- **Texto en lenguaje natural**: Respuestas legibles y coherentes
- **Nivel de confianza**: Indicador de precisión (0.0 - 1.0)
- **Entidades relacionadas**: Enlaces a otros nodos del grafo
- **Metadatos**: Información adicional estructurada

Ejemplo de respuesta:
```json
{
  "answer": "Max Verstappen es un piloto de Fórmula 1...",
  "confidence": 0.95,
  "related_entities": [...],
  "metadata": {
    "team_name": "Red Bull Racing",
    "nationality": "Países Bajos",
    "driver_number": "1"
  }
}
```

### 3. Red Semántica Explorable

El grafo de conocimiento permite:
- **Consultas en profundidad**: "¿Qué motor usa el equipo de Lewis Hamilton?"
- **Exploración de vecindarios**: Ver todas las relaciones de una entidad
- **Caminos entre nodos**: Descubrir conexiones indirectas

### 4. Arquitectura Escalable

- **Microservicios**: Frontend y backend independientes
- **Containerización**: Fácil deployment en cualquier entorno
- **API REST**: Permite integración con otros sistemas
- **Documentación automática**: Swagger UI incluido

---

## 📖 Documentación Completa

### Documentación Técnica

- **[Plan de Desarrollo para GitHub](DESARROLLO_GITHUB_PLAN.md)** - Calendario de commits y estrategia de subida
- **[Backend README](backend/README.md)** - Documentación detallada del backend
- **[Frontend README](frontend/README.md)** - Documentación detallada del frontend
- **[Plan del Proyecto](f1_qa_project_plan.md)** - Planificación inicial
- **[Quickstart General](QUICKSTART.md)** - Guía rápida de inicio
- **[Quickstart Frontend](QUICKSTART_FRONTEND.md)** - Guía específica del frontend
- **[Resumen Backend](IMPLEMENTATION_SUMMARY.md)** - Detalles técnicos backend
- **[Resumen Frontend](FRONTEND_IMPLEMENTATION_SUMMARY.md)** - Detalles técnicos frontend

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 🔮 Roadmap Futuro

### v1.1 (Próxima versión)
- [ ] **Modo oscuro** para la interfaz
- [ ] **Caché de respuestas** frecuentes
- [ ] **Exportar conversaciones** a PDF/JSON
- [ ] **Voice input** con Web Speech API

### v1.2
- [ ] **Comparaciones**: "¿Quién es más rápido, Hamilton o Verstappen?"
- [ ] **Datos históricos**: Acceso a temporadas anteriores
- [ ] **Gráficos y estadísticas**: Visualizaciones de datos
- [ ] **Autenticación**: Sistema de usuarios

### v2.0
- [ ] **Visualización del grafo**: Interfaz interactiva del grafo
- [ ] **Machine Learning**: Mejora de respuestas con ML
- [ ] **Multiidioma**: Soporte para inglés, alemán, italiano
- [ ] **PWA**: Instalable como aplicación nativa
- [ ] **API GraphQL**: Alternativa a REST
- [ ] **Base de datos**: PostgreSQL para persistencia

---

## 💡 Casos de Uso y Ejemplos

### Para Fanáticos de F1
```
Usuario: "¿Para qué equipo corre Fernando Alonso?"
Sistema: "Fernando Alonso corre para Aston Martin F1 Team..."
```

### Para Analistas
```
Usuario: "¿Qué equipos usan motor Mercedes?"
Sistema: "Los equipos que usan motor Mercedes son: Mercedes-AMG, McLaren..."
```

### Para Educación
```
Usuario: "¿Dónde está el circuito de Monza?"
Sistema: "El circuito de Monza está ubicado en Italia..."
```

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Este proyecto es de código abierto.

### Cómo Contribuir

1. **Fork** el repositorio
2. Crea una **rama feature** (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

### Guía de Estilo

- **Python**: Seguir PEP 8
- **JavaScript**: Usar ESLint con configuración estándar
- **Commits**: Usar [Conventional Commits](https://www.conventionalcommits.org/)
- **Documentación**: Mantener README actualizados

### Áreas de Mejora

Busco contribuciones en:
- 🐛 **Bug fixes**: Reportar y corregir bugs
- ✨ **Nuevas features**: Implementar funcionalidades del roadmap
- 📝 **Documentación**: Mejorar guías y ejemplos
- 🌐 **Internacionalización**: Traducir a otros idiomas
- ⚡ **Performance**: Optimizar consultas y respuestas
- 🎨 **UI/UX**: Mejorar diseño e interacciones

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2024 [Tu Nombre]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👥 Autor

**[Tu Nombre]**

- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- LinkedIn: [tu-perfil](https://linkedin.com/in/tu-perfil)
- Email: tu.email@ejemplo.com

---

## 🙏 Agradecimientos

Este proyecto fue posible gracias a:

- **[OpenF1](https://openf1.org)** - Por proporcionar una API gratuita y completa de datos de F1
- **[FastAPI](https://fastapi.tiangolo.com/)** - Por el increíble framework web moderno
- **[NetworkX](https://networkx.org/)** - Por las herramientas de análisis de grafos
- **[unidecode](https://pypi.org/project/Unidecode/)** - Por la normalización de texto
- **Comunidad de F1** - Por la pasión y el conocimiento compartido
- **Desarrolladores Open Source** - Por las herramientas que hicieron esto posible

### Recursos y Referencias

- [Semantic Networks in AI](https://en.wikipedia.org/wiki/Semantic_network)
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [OpenF1 API Documentation](https://openf1.org/documentation)

---

## 📞 Soporte

¿Necesitas ayuda?

- 📖 **Documentación**: Lee los README y guías en este repositorio
- 🐛 **Issues**: [Abre un issue](https://github.com/tu-usuario/f1-qa-semantic-network/issues) en GitHub
- 💬 **Discussions**: Únete a las [discusiones](https://github.com/tu-usuario/f1-qa-semantic-network/discussions)
- 📧 **Email**: Contacta al autor directamente

---

## ⚠️ Disclaimer

Este proyecto es **educativo y de demostración**. No está afiliado con Formula 1®, FIA, o cualquier equipo oficial de F1. Los datos provienen de la API pública de OpenF1.

Formula 1® es una marca registrada de Formula One Licensing BV, una compañía de Formula One Group.

---

<p align="center">
  <strong>Desarrollado con ❤️ para la comunidad de Fórmula 1</strong>
  <br>
  <sub>Hecho con Python, FastAPI, NetworkX y mucho café ☕</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python" alt="Made with Python">
  <img src="https://img.shields.io/badge/Powered%20by-FastAPI-green?style=for-the-badge&logo=fastapi" alt="Powered by FastAPI">
  <img src="https://img.shields.io/badge/Data%20from-OpenF1-red?style=for-the-badge" alt="Data from OpenF1">
</p>

