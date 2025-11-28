# F1 Q&A — Documentación del proyecto

## 🏁 Propósito y alcance

Esta documentación describe el sistema **F1 Q&A**, una aplicación web contenerizada que responde preguntas en español sobre Fórmula 1.  
Su objetivo principal es exponer la arquitectura, los componentes clave, el flujo de datos y la funcionalidad del chatbot, así como servir como guía para desarrolladores que deseen instalar o contribuir al proyecto.

---

## ¿Qué es F1 Q&A?

F1 Q&A es una herramienta de “question-answering” que permite al usuario hacer preguntas en lenguaje natural (español) sobre la Fórmula 1 —por ejemplo, sobre pilotos, equipos, circuitos, motores, resultados de sesiones, etc.— y recibir respuestas construidas a partir de una red semántica. :contentReference[oaicite:1]{index=1}

La base de conocimientos (knowledge base) se representa como un grafo dirigido (usando NetworkX), donde los **nodos** representan entidades (pilotos, equipos, circuitos, motores, sesiones, etc.), y las **relaciones** representan vínculos semánticos como `conduce_para`, `usa_motor`, `ocurre_en`, entre otros. :contentReference[oaicite:3]{index=3}

### Casos de uso principales

| Tipo de pregunta | Ejemplo | Qué retorna el sistema |
|------------------|---------|------------------------|
| Información de piloto | “¿Quién es Max Verstappen?” | Datos del piloto: equipo, nacionalidad, número, etc. :contentReference[oaicite:4]{index=4} |
| Relación equipo-piloto | “¿Para qué equipo corre Lewis Hamilton?” | Afiliación del piloto a su escudería y datos relacionados. :contentReference[oaicite:5]{index=5} |
| Motor de un equipo | “¿Qué motor usa Red Bull?” | Información del proveedor de motor vía la relación equipo → motor. :contentReference[oaicite:6]{index=6} |
| Circuito | “¿Dónde está el circuito de Spa?” | País y detalles del circuito. :contentReference[oaicite:7]{index=7} |
| Resultados de sesiones / Grandes Premios | “¿Quién ganó el GP de Mónaco 2024?” | Ganador del evento, basado en relaciones sesión → piloto. :contentReference[oaicite:8]{index=8} |

La base se pobla usando datos de la OpenF1 API. En el arranque se cargan decenas de nodos (~100+) y relaciones (~200+). :contentReference[oaicite:10]{index=10}

---

## 📐 Arquitectura general

El sistema está dividido en dos servicios contenerizados: **backend** y **frontend**. :contentReference[oaicite:11]{index=11}

### Backend  

- `SemanticNetwork`: implementación del grafo semántico que maneja nodos y relaciones. :contentReference[oaicite:12]{index=12}  
- `KnowledgeBase`: módulo responsable de cargar datos desde la API externa (OpenF1) y poblar el grafo. :contentReference[oaicite:13]{index=13}  
- `QueryService`: procesa las preguntas del usuario, evalúa la confianza de resultados, y genera respuestas en lenguaje natural. :contentReference[oaicite:14]{index=14}  
- `NLPProcessor`: analiza texto en español, detecta entidades mencionadas (pilotos, equipos, circuitos, etc.), clasifica el tipo de pregunta y prepara la consulta. :contentReference[oaicite:15]{index=15}  
- `OpenF1Client`: cliente HTTP para consultar la API externa de datos de Fórmula 1. :contentReference[oaicite:16]{index=16}  
- Rutas API definidas con FastAPI — por ejemplo `/api/v1/ask` para enviar preguntas. :contentReference[oaicite:18]{index=18}  

### Frontend  

- Interfaz de chat (chat UI) en JavaScript que permite al usuario escribir preguntas y recibir respuestas. :contentReference[oaicite:19]{index=19}  
- Cliente HTTP para comunicarse con el backend. :contentReference[oaicite:20]{index=20}  
- Diseño responsivo con CSS, estilo tematizado acorde a F1. :contentReference[oaicite:21]{index=21}  
- Servido a través de un servidor web (por ejemplo Nginx) en un contenedor Docker. :contentReference[oaicite:22]{index=22}  

### Infraestructura / Deployment  

- Uso de **Docker** y **Docker Compose** para orquestar los contenedores backend y frontend. :contentReference[oaicite:23]{index=23}  
- Configuración vía variables de entorno (clave API, puertos, orígenes para CORS, nivel de logs, etc.). :contentReference[oaicite:24]{index=24}  

---

## 🧠 Procesamiento de preguntas & respuesta

1. El usuario envía una pregunta vía la interfaz de chat. :contentReference[oaicite:25]{index=25}  
2. El `NLPProcessor` analiza la pregunta: normaliza texto, extrae entidades (por ejemplo “Hamilton”, “Red Bull”, “Mónaco”), detecta tipo de intención/pregunta (piloto, equipo, circuito, resultado, etc.). :contentReference[oaicite:26]{index=26}  
3. El `QueryService` construye una consulta sobre el grafo semántico: busca nodos relevantes, relaciones apropiadas, calculando un puntaje de confianza según la coincidencia y completitud. :contentReference[oaicite:27]{index=27}  
4. Si la consulta es satisfactoria, genera una respuesta en español mediante plantillas, enriquecida con datos estructurados y entidades relacionadas. :contentReference[oaicite:28]{index=28}  
5. Resultado devuelto via API y mostrado en la interfaz de chat. Opcionalmente se pueden mostrar entidades relacionadas como contexto adicional. :contentReference[oaicite:29]{index=29}  

---

## 🧰 Tecnología usada (Stack)

- **Backend**  
  - Python 3.11+ :contentReference[oaicite:30]{index=30}  
  - FastAPI :contentReference[oaicite:31]{index=31}  
  - NetworkX — para grafo semántico :contentReference[oaicite:32]{index=32}  
  - Pydantic — validación y configuración :contentReference[oaicite:33]{index=33}  
  - httpx — cliente HTTP async para API externa :contentReference[oaicite:34]{index=34}  
  - unidecode — normalización de texto en español :contentReference[oaicite:35]{index=35}  
  - Uvicorn — servidor ASGI :contentReference[oaicite:36]{index=36}  

- **Frontend**  
  - HTML5 + CSS3 (diseño responsivo, estilos temáticos) :contentReference[oaicite:37]{index=37}  
  - JavaScript (ES6+) para lógica de cliente y comunicación con backend API :contentReference[oaicite:38]{index=38}  
  - Nginx (contenedor) como servidor web / reverse proxy para servir frontend y redirigir solicitudes API al backend. :contentReference[oaicite:39]{index=39}  

- **Infraestructura**  
  - Docker + Docker Compose para contenerización y orquestación de servicios. :contentReference[oaicite:40]{index=40}  

---

## 🚀 Cómo iniciar / Quick Start

Para ejecutar localmente:

1. Tener Docker 20.10+ y Docker Compose 2.0+ instalados. :contentReference[oaicite:41]{index=41}  
2. Crear un archivo `.env` en la raíz del proyecto con la variable `OPENF1_API_KEY=tu_clave` (necesaria para acceder a la API externa). :contentReference[oaicite:42]{index=42}  
3. Ejecutar `docker-compose up --build`. :contentReference[oaicite:43]{index=43}  
4. Luego accede a:  
   - Frontend: `http://localhost:3000`  
   - Backend API: `http://localhost:8000`  
   - Documentación de la API (OpenAPI / Swagger): `http://localhost:8000/docs` :contentReference[oaicite:44]{index=44}  

Para más detalles de instalación, configuración avanzada o despliegue, consultar la sección dedicada en la documentación. :contentReference[oaicite:45]{index=45}

---

## ✅ Características principales

- Soporte para preguntas en **español** sobre datos de Fórmula 1. :contentReference[oaicite:46]{index=46}  
- Representación de conocimiento mediante grafo semántico — lo que permite relaciones complejas entre entidades. :contentReference[oaicite:47]{index=47}  
- Procesamiento de lenguaje natural: extracción de entidades, clasificación de intención, manejo de variantes de nombres y texto con acentos. :contentReference[oaicite:48]{index=48}  
- Generación de respuestas en lenguaje natural + contexto enriquecido (entidades relacionadas). :contentReference[oaicite:49]{index=49}  
- Interfaz de chat amigable e interactiva. :contentReference[oaicite:50]{index=50}  
- Arquitectura modular y contenerizada, fácilmente desplegable vía Docker. :contentReference[oaicite:51]{index=51}  

---

## 📚 Estructura de documentación

La página wiki incluye las siguientes secciones:  
- Getting Started (inicio / configuración) :contentReference[oaicite:52]{index=52}  
- Installation and Running (instalación y ejecución) :contentReference[oaicite:53]{index=53}  
- Architecture (arquitectura general) :contentReference[oaicite:54]{index=54}  
- System Overview (visión general del sistema) :contentReference[oaicite:55]{index=55}  
- Backend Components (componentes del backend) :contentReference[oaicite:56]{index=56}  
- Frontend Components (componentes del frontend) :contentReference[oaicite:57]{index=57}  
- Data Flow and Processing (flujo de datos y procesamiento) :contentReference[oaicite:58]{index=58}  
- API Reference, Endpoints y modelos de request/response :contentReference[oaicite:59]{index=59}  
- Deployment and Operations (despliegue y operación) :contentReference[oaicite:60]{index=60}  
- Development Workflow & Guide (guía de desarrollo) para contribuir o extender el proyecto. :contentReference[oaicite:61]{index=61}  

---

## ✨ Conclusión

La documentación de **F1 Q&A** ofrece una visión clara y completa tanto para usuarios finales como para desarrolladores.  
Permite comprender cómo está estructurado el sistema, cómo se procesa una pregunta hasta devolver una respuesta, y cómo desplegar o contribuir al proyecto.  

Este enfoque estructurado facilita la mantenibilidad, escalabilidad y extensibilidad del chatbot — perfecto si planeas seguir agregando nuevas funciones (más datos, nuevos tipos de preguntas, mejoras de UI, etc.).

