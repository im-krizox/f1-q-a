"""
Aplicación Principal FastAPI - F1 Q&A System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import sys

from ..core.config import get_settings
from ..services.openf1_client import OpenF1Client
from ..services.knowledge_base import KnowledgeBase
from ..services.nlp_processor import NLPProcessor
from ..services.query_service import QueryService
from .routes import router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Obtener configuración
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación (startup y shutdown)
    """
    # Startup
    logger.info("Iniciando F1 Q&A System...")
    
    try:
        # Inicializar cliente OpenF1
        logger.info("Inicializando OpenF1Client...")
        openf1_client = OpenF1Client(
            base_url=settings.openf1_base_url,
            api_key=settings.openf1_api_key if settings.openf1_api_key else None
        )
        app.state.openf1_client = openf1_client
        
        # Inicializar base de conocimiento
        logger.info("Inicializando KnowledgeBase...")
        knowledge_base = KnowledgeBase(openf1_client)
        app.state.knowledge_base = knowledge_base
        
        # Cargar datos (puede tardar un poco)
        logger.info("Cargando datos desde OpenF1 API...")
        await knowledge_base.load_data(year=2024)
        logger.info("Datos cargados exitosamente")
        
        # Inicializar procesador NLP
        logger.info("Inicializando NLPProcessor...")
        nlp_processor = NLPProcessor()
        app.state.nlp_processor = nlp_processor
        
        # Inicializar servicio de consultas
        logger.info("Inicializando QueryService...")
        query_service = QueryService(knowledge_base, nlp_processor)
        app.state.query_service = query_service
        
        # Obtener estadísticas
        network = knowledge_base.get_semantic_network()
        stats = network.get_stats()
        logger.info(f"Sistema iniciado correctamente. Estadísticas: {stats}")
        
        yield
        
    except Exception as e:
        logger.error(f"Error durante el inicio: {e}", exc_info=True)
        raise
    
    # Shutdown
    logger.info("Cerrando F1 Q&A System...")
    
    try:
        # Cerrar cliente OpenF1
        if hasattr(app.state, 'openf1_client'):
            await app.state.openf1_client.close()
            logger.info("OpenF1Client cerrado")
        
        logger.info("Sistema cerrado correctamente")
        
    except Exception as e:
        logger.error(f"Error durante el cierre: {e}", exc_info=True)


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    Sistema de Preguntas y Respuestas sobre Fórmula 1 usando Redes Semánticas.
    
    ## Características
    
    * **Consultas en Español**: Procesa preguntas en lenguaje natural
    * **Red Semántica**: Utiliza grafos para representar conocimiento
    * **Datos en Tiempo Real**: Integración con OpenF1 API
    * **Múltiples Tipos de Consultas**: Pilotos, equipos, circuitos, sesiones y más
    
    ## Endpoints Principales
    
    * `/api/v1/ask` - Hacer preguntas sobre F1
    * `/api/v1/health` - Verificar estado del sistema
    * `/api/v1/entities/{type}` - Listar entidades
    * `/api/v1/network/explore/{node_id}` - Explorar red semántica
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router
app.include_router(router)


# Endpoint raíz
@app.get(
    "/",
    tags=["Root"],
    summary="Información de la API",
    description="Retorna información básica de la API y enlaces útiles"
)
async def root():
    """
    Endpoint raíz que proporciona información de la API
    """
    return {
        "message": "F1 Q&A API - Sistema de Preguntas y Respuestas sobre Fórmula 1",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health",
        "endpoints": {
            "ask": "/api/v1/ask",
            "entities": "/api/v1/entities/{type}",
            "explore": "/api/v1/network/explore/{node_id}",
            "stats": "/api/v1/stats"
        }
    }


# Manejador de errores global (opcional)
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Manejador global de excepciones no capturadas
    """
    logger.error(f"Error no manejado: {exc}", exc_info=True)
    return {
        "error": "Error interno del servidor",
        "detail": str(exc) if settings.log_level == "DEBUG" else "Ha ocurrido un error inesperado"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Ejecutar servidor
    uvicorn.run(
        "src.api.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True,
        log_level=settings.log_level.lower()
    )

