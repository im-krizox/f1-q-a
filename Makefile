.PHONY: help build up down logs clean restart health test backend-shell frontend-shell

help:
	@echo "F1 Q&A System - Comandos disponibles:"
	@echo ""
	@echo "🚀 Gestión de Servicios:"
	@echo "  make build          - Construir imágenes Docker"
	@echo "  make up             - Iniciar servicios"
	@echo "  make down           - Detener servicios"
	@echo "  make restart        - Reiniciar servicios"
	@echo "  make dev            - Iniciar en modo desarrollo (con logs)"
	@echo "  make prod           - Iniciar en modo producción"
	@echo ""
	@echo "📋 Logs y Monitoreo:"
	@echo "  make logs           - Ver logs en tiempo real"
	@echo "  make logs-backend   - Ver logs del backend"
	@echo "  make logs-frontend  - Ver logs del frontend"
	@echo ""
	@echo "🏥 Health & Testing:"
	@echo "  make health         - Verificar salud del sistema"
	@echo "  make test           - Ejecutar tests básicos"
	@echo "  make test-frontend  - Verificar frontend"
	@echo ""
	@echo "🐚 Acceso a Contenedores:"
	@echo "  make backend-shell  - Abrir shell en backend"
	@echo "  make frontend-shell - Abrir shell en frontend"
	@echo ""
	@echo "🧹 Limpieza:"
	@echo "  make clean          - Limpiar todo"
	@echo ""
	@echo "📚 URLs:"
	@echo "  Frontend:        http://localhost:3000"
	@echo "  Backend API:     http://localhost:8000/docs"
	@echo "  Backend Health:  http://localhost:8000/api/v1/health"
	@echo ""

build:
	@echo "🔨 Construyendo imágenes..."
	docker-compose build

up:
	@echo "🚀 Iniciando servicios..."
	docker-compose up -d
	@echo "✅ Servicios iniciados"
	@echo ""
	@echo "📱 Frontend disponible en:    http://localhost:3000"
	@echo "📖 Documentación API:         http://localhost:8000/docs"
	@echo "🏥 Health Check Backend:      http://localhost:8000/api/v1/health"
	@echo "🏥 Health Check Frontend:     http://localhost:3000/health"

down:
	@echo "🛑 Deteniendo servicios..."
	docker-compose down
	@echo "✅ Servicios detenidos"

logs:
	@echo "📋 Mostrando logs (Ctrl+C para salir)..."
	docker-compose logs -f

logs-backend:
	@echo "📋 Mostrando logs del backend..."
	docker-compose logs -f backend

logs-frontend:
	@echo "📋 Mostrando logs del frontend..."
	docker-compose logs -f frontend

restart:
	@echo "🔄 Reiniciando servicios..."
	docker-compose restart
	@echo "✅ Servicios reiniciados"

clean:
	@echo "🧹 Limpiando todo..."
	docker-compose down -v --rmi all
	@echo "✅ Limpieza completada"

health:
	@echo "🏥 Verificando salud del sistema..."
	@curl -s http://localhost:8000/api/v1/health | python -m json.tool

stats:
	@echo "📊 Obteniendo estadísticas..."
	@curl -s http://localhost:8000/api/v1/stats | python -m json.tool

test:
	@echo "🧪 Ejecutando tests básicos..."
	@echo "\n1. Health Check:"
	@curl -s http://localhost:8000/api/v1/health | python -m json.tool
	@echo "\n2. Pregunta de prueba:"
	@curl -s -X POST http://localhost:8000/api/v1/ask \
		-H "Content-Type: application/json" \
		-d '{"question": "¿Quién es Max Verstappen?"}' | python -m json.tool

backend-shell:
	@echo "🐚 Abriendo shell en backend..."
	docker-compose exec backend /bin/bash

frontend-shell:
	@echo "🐚 Abriendo shell en frontend..."
	docker-compose exec frontend /bin/sh

test-frontend:
	@echo "🧪 Verificando frontend..."
	@echo "\n1. Frontend Health Check:"
	@curl -s http://localhost/health
	@echo "\n2. Verificando archivos estáticos:"
	@curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost/
	@echo "✅ Frontend verificado"

dev:
	@echo "🚀 Iniciando en modo desarrollo..."
	docker-compose up --build

prod:
	@echo "🚀 Iniciando en modo producción..."
	docker-compose up -d --build

install:
	@echo "📦 Instalando dependencias locales..."
	cd backend && pip install -r requirements.txt

format:
	@echo "🎨 Formateando código..."
	cd backend && black src/
	@echo "✅ Código formateado"

# Ejemplos de consultas
example-pilot:
	@echo "Preguntando sobre un piloto..."
	@curl -s -X POST http://localhost:8000/api/v1/ask \
		-H "Content-Type: application/json" \
		-d '{"question": "¿Quién es Max Verstappen?"}' | python -m json.tool

example-team:
	@echo "Preguntando sobre equipos..."
	@curl -s -X POST http://localhost:8000/api/v1/ask \
		-H "Content-Type: application/json" \
		-d '{"question": "¿Para qué equipo corre Lewis Hamilton?"}' | python -m json.tool

example-motor:
	@echo "Preguntando sobre motores..."
	@curl -s -X POST http://localhost:8000/api/v1/ask \
		-H "Content-Type: application/json" \
		-d '{"question": "¿Qué motor usa Red Bull?"}' | python -m json.tool

example-entities:
	@echo "Listando pilotos..."
	@curl -s http://localhost:8000/api/v1/entities/drivers?limit=5 | python -m json.tool

