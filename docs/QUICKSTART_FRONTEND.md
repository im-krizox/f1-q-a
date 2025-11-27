# 🚀 Guía Rápida - F1 Q&A System (Completo)

Guía para levantar el sistema completo de F1 Q&A con frontend y backend.

## 📋 Prerequisitos

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM disponible
- Puerto 3000 y 8000 disponibles

## 🎯 Inicio Rápido (1 Comando)

Desde la raíz del proyecto:

```bash
docker-compose up --build
```

**Eso es todo!** 🎉

Espera 30-60 segundos mientras:
1. Se construyen las imágenes de Docker
2. El backend carga datos de OpenF1
3. El frontend se configura con Nginx

## 🌐 Acceso a la Aplicación

Una vez que los contenedores estén corriendo:

- **Frontend (Interfaz Web)**: http://localhost:3000
- **Backend API (Documentación)**: http://localhost:8000/docs
- **Backend Health Check**: http://localhost:8000/api/v1/health

## 🖥️ Uso de la Interfaz

### Pantalla de Bienvenida

Al abrir http://localhost:3000 verás:
- Título del sistema
- Estado de conexión (debe mostrar "Conectado" en verde)
- 5 preguntas de ejemplo clicables
- Campo de entrada para escribir preguntas

### Hacer Preguntas

**Ejemplos que puedes probar:**

```
¿Quién es Max Verstappen?
¿Para qué equipo corre Lewis Hamilton?
¿Quién ganó el GP de Mónaco 2024?
¿Qué motor usa Red Bull?
¿Dónde está el circuito de Spa?
¿Para quién corre Fernando Alonso?
¿Qué motor tiene Mercedes?
```

### Panel de Información

A la derecha verás:
- **Entidades Relacionadas**: Información adicional sobre pilotos, equipos, etc.
- **Nivel de Confianza**: Porcentaje que indica la certeza de la respuesta

## 🔍 Verificación del Sistema

### Verificar que todo está corriendo

```bash
# Ver estado de los contenedores
docker-compose ps

# Deberías ver algo como:
# NAME               STATUS        PORTS
# f1-qa-backend      Up 1 minute   0.0.0.0:8000->8000/tcp
# f1-qa-frontend     Up 1 minute   0.0.0.0:3000->80/tcp
```

### Ver logs en tiempo real

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Verificar health checks

```bash
# Backend
curl http://localhost:8000/api/v1/health

# Frontend
curl http://localhost:3000/health
```

## 🛠️ Comandos Útiles

### Reiniciar el sistema

```bash
docker-compose restart
```

### Detener el sistema

```bash
docker-compose down
```

### Reconstruir desde cero

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Limpiar todo (contenedores, imágenes, volúmenes)

```bash
docker-compose down -v --rmi all
```

## 🐛 Resolución de Problemas

### El frontend no carga

1. Verificar que el contenedor está corriendo:
   ```bash
   docker ps | grep f1-qa-frontend
   ```

2. Ver logs del frontend:
   ```bash
   docker logs f1-qa-frontend
   ```

3. Verificar que el puerto 3000 no está ocupado:
   ```bash
   # Linux/Mac
   lsof -i :3000
   
   # Windows
   netstat -ano | findstr :3000
   ```

### El backend no responde

1. Verificar que el contenedor está corriendo:
   ```bash
   docker ps | grep f1-qa-backend
   ```

2. Ver logs del backend:
   ```bash
   docker logs f1-qa-backend
   ```

3. Verificar conectividad:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

### Error de conexión en el frontend

Si ves "Desconectado" en el indicador de estado:

1. Verificar que el backend está corriendo
2. Verificar que no hay errores en la consola del navegador (F12)
3. Verificar la red Docker:
   ```bash
   docker network ls
   docker network inspect f1-qa_f1-network
   ```

### Puerto 3000 ocupado (Mac/Linux)

Si el puerto 3000 está ocupado, modifica `docker-compose.yml`:

```yaml
frontend:
  ports:
    - "8080:80"  # Cambiar de 3000 a 8080
```

Luego accede a: http://localhost:8080

### Datos no se cargan en el backend

El backend necesita tiempo para cargar datos de OpenF1. Espera 30-60 segundos después de iniciar.

Ver progreso:
```bash
docker logs -f f1-qa-backend
```

Deberías ver mensajes como:
```
INFO: Loading knowledge base data...
INFO: Loaded 20 drivers
INFO: Loaded 24 sessions
INFO: Created semantic network with X nodes
```

## 📊 Arquitectura del Sistema

```
┌─────────────────┐
│   Navegador     │
│ (localhost:3000)│
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  Nginx:80       │
│  (Frontend)     │
└────────┬────────┘
         │ Proxy /api/*
         ▼
┌─────────────────┐      ┌──────────────┐
│  FastAPI:8000   │──────▶│  OpenF1 API  │
│  (Backend)      │      │  (External)  │
└─────────────────┘      └──────────────┘
         │
         ▼
┌─────────────────┐
│ Red Semántica   │
│  (NetworkX)     │
└─────────────────┘
```

## 🎨 Características del Frontend

### Responsive Design
- ✅ Desktop (1920x1080+)
- ✅ Tablet (768px-1024px)
- ✅ Mobile (320px-767px)

### Atajos de Teclado
- `Ctrl/Cmd + K`: Focus en el campo de entrada
- `Ctrl/Cmd + L`: Limpiar conversación
- `Escape`: Cancelar/Desenfocar

### Estados Visuales
- ✅ Indicador de conexión en tiempo real
- ✅ Typing indicator mientras procesa
- ✅ Animaciones suaves en mensajes
- ✅ Error handling visual

## 📈 Datos Disponibles

El sistema carga automáticamente:
- **Pilotos**: ~20 pilotos activos de F1 2024
- **Equipos**: 10 escuderías
- **Circuitos**: 24+ circuitos del calendario
- **Sesiones**: Carreras, clasificaciones y prácticas
- **Motores**: Mercedes, Ferrari, Honda RBPT, Renault

## 🔒 Seguridad

Headers implementados:
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- CORS configurado correctamente

## 📱 Testing Rápido

### Test de Integración Completo

```bash
# 1. Verificar backend
curl http://localhost:8000/api/v1/health

# 2. Hacer una pregunta via API
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Quién es Max Verstappen?"}'

# 3. Verificar frontend
curl http://localhost:3000/health

# 4. Abrir navegador
open http://localhost:3000  # Mac
xdg-open http://localhost:3000  # Linux
start http://localhost:3000  # Windows
```

### Test de Preguntas

Prueba estas preguntas en la interfaz:

1. ✅ Información de piloto: "¿Quién es Max Verstappen?"
2. ✅ Equipo de piloto: "¿Para qué equipo corre Lewis Hamilton?"
3. ✅ Ganador de carrera: "¿Quién ganó el GP de Mónaco?"
4. ✅ Motor de equipo: "¿Qué motor usa Red Bull?"
5. ✅ Ubicación de circuito: "¿Dónde está el circuito de Spa?"

## 📚 Recursos Adicionales

- [README Principal](./README.md)
- [Documentación Backend](./backend/README.md)
- [Documentación Frontend](./frontend/README.md)
- [Plan de Proyecto](./f1_qa_project_plan.md)
- [Documentación API](http://localhost:8000/docs) (cuando esté corriendo)

## 🎯 Próximos Pasos

Una vez que todo esté funcionando:

1. **Explora la Interfaz**: Prueba diferentes preguntas
2. **Revisa la Documentación API**: http://localhost:8000/docs
3. **Inspecciona la Red Semántica**: Usa el endpoint `/api/v1/network/explore/{node_id}`
4. **Personaliza el Frontend**: Modifica colores en `frontend/src/css/main.css`

## 💡 Tips de Desarrollo

### Hot Reload Backend

El backend tiene hot reload habilitado. Modifica archivos en `backend/src/` y se recargará automáticamente.

### Modificar Frontend

Para cambios en el frontend:
```bash
# Detener frontend
docker-compose stop frontend

# Hacer cambios en frontend/

# Reconstruir y reiniciar
docker-compose build frontend
docker-compose up -d frontend
```

### Ver Logs en Tiempo Real

```bash
# Terminal 1: Backend
docker logs -f f1-qa-backend

# Terminal 2: Frontend
docker logs -f f1-qa-frontend
```

## ✅ Checklist de Funcionamiento

- [ ] `docker-compose up` ejecuta sin errores
- [ ] Backend responde en http://localhost:8000/api/v1/health
- [ ] Frontend carga en http://localhost:3000
- [ ] Indicador de conexión muestra "Conectado"
- [ ] Preguntas de ejemplo son clicables
- [ ] Se puede enviar una pregunta
- [ ] Se recibe una respuesta del asistente
- [ ] Panel de información muestra entidades
- [ ] Nivel de confianza se actualiza

## 🎉 ¡Listo!

Si todos los checks están ✅, tu sistema F1 Q&A está funcionando perfectamente.

**¡Disfruta explorando el mundo de la Fórmula 1! 🏎️💨**

---

¿Problemas? Revisa la sección de [Resolución de Problemas](#-resolución-de-problemas) o los logs de los contenedores.

