# 🚀 Inicio Rápido - F1 Q&A System

Esta guía te ayudará a tener el sistema funcionando en menos de 5 minutos.

## Prerrequisitos

- Docker y Docker Compose instalados
- Puerto 8000 disponible

## Pasos

### 0. ⚠️ Configurar API Key (REQUERIDO)

**IMPORTANTE**: Antes de iniciar el sistema, necesitas configurar tu API key de OpenF1.

```bash
# Crear archivo .env en la raíz del proyecto
echo "OPENF1_API_KEY=tu_api_key_aquí" > .env
```

**Cómo obtener tu API key:**
1. Regístrate en: https://tally.so/r/w2yWDb
2. Recibirás tu API key por correo electrónico
3. Reemplaza `tu_api_key_aquí` con tu API key real

**Sin el API key, el sistema NO funcionará correctamente** (no podrá cargar datos de F1).

### 1. Iniciar el Sistema

```bash
# Opción A: Usar Docker Compose directamente
docker-compose up --build

# Opción B: Usar Makefile (recomendado)
make dev
```

Espera a que aparezca el mensaje:
```
Sistema iniciado correctamente. Estadísticas: {...}
```

### 2. Verificar que Funciona

Abre tu navegador en: http://localhost:8000/docs

O ejecuta en otra terminal:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# O usa el Makefile
make health
```

### 3. Hacer una Pregunta

```bash
# Usando curl
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Quién es Max Verstappen?"}'

# O usa el script de prueba
python test_api.py

# O usa el Makefile
make example-pilot
```

## Comandos Útiles

```bash
# Ver logs
make logs

# Reiniciar
make restart

# Detener
make down

# Limpiar todo
make clean

# Ejemplos
make example-pilot    # Pregunta sobre piloto
make example-team     # Pregunta sobre equipo
make example-motor    # Pregunta sobre motor
```

## Endpoints Principales

- **Documentación**: http://localhost:8000/docs
- **Health**: http://localhost:8000/api/v1/health
- **Preguntar**: POST http://localhost:8000/api/v1/ask
- **Estadísticas**: http://localhost:8000/api/v1/stats

## Ejemplos de Preguntas

```bash
# Información de pilotos
"¿Quién es Max Verstappen?"
"¿Qué piloto tiene el número 44?"

# Equipos
"¿Para qué equipo corre Lewis Hamilton?"
"¿En qué equipo está Fernando Alonso?"

# Motores
"¿Qué motor usa Red Bull?"
"¿Qué motor utiliza Ferrari?"

# Circuitos
"¿Dónde está el circuito de Spa?"
"¿En qué país está Silverstone?"
```

## Solución de Problemas

### El puerto 8000 está ocupado

```bash
# Cambiar el puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usa el puerto 8001 en vez de 8000
```

### Error al cargar datos

- Verifica tu conexión a internet
- La API de OpenF1 debe estar accesible
- Revisa los logs: `make logs`

### El servicio no responde

```bash
# Reiniciar
make restart

# O reconstruir desde cero
make clean
make dev
```

## Próximos Pasos

1. Explora la documentación interactiva: http://localhost:8000/docs
2. Prueba diferentes tipos de preguntas
3. Revisa el código en `backend/src/`
4. Lee el README completo para más detalles

## Testing Completo

```bash
# Ejecutar suite de pruebas
python test_api.py

# O pruebas individuales
make test
make example-pilot
make example-team
make example-motor
```

## Detener el Sistema

```bash
# Detener servicios
make down

# O con docker-compose
docker-compose down
```

---

¿Problemas? Revisa los logs:
```bash
make logs
```

¿Todo funciona? ¡Empieza a hacer preguntas sobre F1! 🏎️

