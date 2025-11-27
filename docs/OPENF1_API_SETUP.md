# 🔑 Configuración de API Key para OpenF1

## 📌 Problema Identificado

La API de OpenF1 (`https://api.openf1.org/v1`) ahora **requiere autenticación** para acceder a los datos durante sesiones en vivo. 

**Error observado:**
```json
{
  "detail": "Session in progress, access is restricted to authenticated users. Sign up here: https://tally.so/r/w2yWDb"
}
```

**Impacto:**
- Sin API key, el sistema NO puede cargar:
  - ✗ Pilotos
  - ✗ Equipos
  - ✗ Circuitos
  - ✗ Sesiones/Carreras
- Solo funcionan datos hard-coded:
  - ✓ Motores (Mercedes, Ferrari, Honda RBPT, Renault)
  - ✓ Tipos de eventos (Race, Qualifying, Practice)

---

## ✅ Solución Implementada

Se ha agregado soporte completo para autenticación con API key en el sistema.

### Cambios Realizados

1. **Configuración (`backend/src/core/config.py`)**
   - Nueva variable: `OPENF1_API_KEY`

2. **Cliente OpenF1 (`backend/src/services/openf1_client.py`)**
   - Parámetro `api_key` en el constructor
   - Headers de autenticación: `Authorization: Bearer <API_KEY>`

3. **Docker Compose (`docker-compose.yml`)**
   - Variable de entorno: `OPENF1_API_KEY=${OPENF1_API_KEY:-}`
   - Se lee desde archivo `.env`

4. **Documentación actualizada**
   - README.md
   - QUICKSTART.md
   - Este archivo (OPENF1_API_SETUP.md)

---

## 🚀 Cómo Configurar

### Paso 1: Obtener API Key

1. Visita: https://tally.so/r/w2yWDb
2. Completa el formulario de registro
3. Recibirás tu API key por correo electrónico

### Paso 2: Configurar en el Proyecto

**Opción A: Archivo .env (Recomendado para Docker)**

```bash
# En la raíz del proyecto F1-Q&A/
echo "OPENF1_API_KEY=tu_api_key_real_aquí" > .env
```

**Opción B: Variable de entorno (Para ejecución local)**

```bash
export OPENF1_API_KEY="tu_api_key_real_aquí"
```

### Paso 3: Reiniciar el Sistema

```bash
# Detener contenedores actuales
docker-compose down

# Reconstruir y iniciar con la nueva configuración
docker-compose up --build
```

---

## 🧪 Verificar que Funciona

### 1. Verificar Health Check

```bash
curl http://localhost:8000/api/v1/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "knowledge_base_loaded": true
}
```

### 2. Verificar Estadísticas

```bash
curl http://localhost:8000/api/v1/stats
```

**Respuesta esperada con API key configurado:**
```json
{
  "status": "success",
  "stats": {
    "total_nodes": 150+,  // Muchos más nodos
    "total_edges": 200+,  // Muchas relaciones
    "nodes_by_type": {
      "piloto": 20+,
      "equipo": 10+,
      "circuito": 20+,
      "sesion": 60+,
      "motor": 4,
      "tipo_evento": 3,
      "pais": 20+
    }
  },
  "knowledge_base_loaded": true
}
```

**⚠️ Sin API key (solo datos hardcoded):**
```json
{
  "stats": {
    "total_nodes": 7,
    "total_edges": 0,
    "nodes_by_type": {
      "motor": 4,
      "tipo_evento": 3
    }
  }
}
```

### 3. Recargar Base de Conocimiento

```bash
curl -X POST "http://localhost:8000/api/v1/reload?year=2024" \
  -H "Content-Type: application/json"
```

### 4. Hacer una Pregunta de Prueba

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Quién es Max Verstappen?"}'
```

**Respuesta esperada CON API key:**
```json
{
  "answer": "Max Verstappen - Países Bajos, #1, Red Bull Racing",
  "confidence": 0.9,
  "related_entities": [
    {"type": "piloto", "name": "Max Verstappen", "id": "driver_1"},
    {"type": "equipo", "name": "Red Bull Racing", "id": "team_red_bull_racing"}
  ],
  "query_type": "pilot_info"
}
```

**Respuesta SIN API key:**
```json
{
  "answer": "No se encontró información del piloto",
  "confidence": 0.5,
  "related_entities": [],
  "query_type": "pilot_info"
}
```

---

## 🔍 Verificar Logs del Contenedor

```bash
# Ver logs del backend
docker logs f1-qa-backend --tail=50

# Ver logs en tiempo real
docker logs f1-qa-backend -f
```

**Con API key configurado correctamente:**
```
OpenF1Client inicializado con autenticación
Base URL: https://api.openf1.org/v1
Obtenidos 24 meetings
Obtenidas 75 sesiones
Agregados 20 pilotos
Agregados 10 equipos
```

**Sin API key:**
```
OpenF1Client inicializado SIN autenticación - puede fallar durante sesiones en vivo
Error HTTP 401 en https://api.openf1.org/v1/meetings
Obtenidos 0 meetings
Obtenidas 0 sesiones
```

---

## 🆘 Troubleshooting

### Problema: "No se encontró información del piloto"

**Causa:** API key no configurado o inválido

**Solución:**
1. Verifica que el archivo `.env` existe en la raíz del proyecto
2. Verifica que contiene `OPENF1_API_KEY=<tu_api_key>`
3. Reinicia los contenedores: `docker-compose restart`

### Problema: Error 401 Unauthorized en logs

**Causa:** API key inválido o expirado

**Solución:**
1. Verifica tu API key en el correo de registro
2. Actualiza el archivo `.env` con la key correcta
3. Reinicia: `docker-compose down && docker-compose up`

### Problema: Solo 7 nodos en las estadísticas

**Causa:** El sistema no puede cargar datos de la API

**Solución:**
1. Verifica la configuración del API key (pasos anteriores)
2. Verifica conectividad: `docker exec f1-qa-backend curl https://api.openf1.org/v1/meetings?year=2024`

---

## 📞 Soporte

Si tienes problemas para obtener tu API key:
- Contacta a OpenF1: https://tally.so/r/w2yWDb
- Revisa la documentación oficial de OpenF1 (si está disponible)

---

## 📝 Notas Técnicas

### Autenticación

El sistema usa autenticación Bearer Token:

```http
Authorization: Bearer <API_KEY>
```

### Variables de Entorno

Archivo `.env` en la raíz del proyecto:

```bash
# Requerido
OPENF1_API_KEY=tu_api_key

# Opcional
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://localhost,http://localhost:80
LOG_LEVEL=INFO
```

### Diagrama de Flujo

```
Usuario                Docker Compose           Backend                   OpenF1 API
  |                          |                      |                          |
  | 1. docker-compose up     |                      |                          |
  |------------------------->|                      |                          |
  |                          |  2. Inicializa       |                          |
  |                          |--------------------->|                          |
  |                          |                      | 3. Lee OPENF1_API_KEY    |
  |                          |                      | desde env                |
  |                          |                      |                          |
  |                          |                      | 4. GET /meetings         |
  |                          |                      | Header: Authorization    |
  |                          |                      |------------------------->|
  |                          |                      |                          |
  |                          |                      | 5. 200 OK + datos        |
  |                          |                      |<-------------------------|
  |                          |                      |                          |
  |                          |  6. Sistema listo    |                          |
  |                          |<---------------------|                          |
  | 7. http://localhost      |                      |                          |
  |<-------------------------|                      |                          |
```

---

