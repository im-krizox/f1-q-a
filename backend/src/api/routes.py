"""
Rutas de la API - Endpoints de FastAPI
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
import logging

from ..models.schemas import (
    QuestionRequest,
    AnswerResponse,
    HealthResponse,
    EntityListResponse,
    NetworkExploreResponse,
    ErrorResponse
)
from ..services.knowledge_base import KnowledgeBase
from ..services.query_service import QueryService
from .dependencies import get_knowledge_base, get_query_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["F1 Q&A"])


@router.post(
    "/ask",
    response_model=AnswerResponse,
    summary="Hacer una pregunta sobre F1",
    description="Procesa una pregunta en español sobre Fórmula 1 y retorna una respuesta basada en la red semántica",
    responses={
        200: {"description": "Respuesta exitosa"},
        400: {"description": "Pregunta inválida", "model": ErrorResponse},
        500: {"description": "Error del servidor", "model": ErrorResponse}
    }
)
async def ask_question(
    request: QuestionRequest,
    query_service: QueryService = Depends(get_query_service)
) -> AnswerResponse:
    """
    Endpoint principal para hacer preguntas sobre F1
    
    Args:
        request: Pregunta del usuario y contexto opcional
        query_service: Servicio de consultas (inyectado)
        
    Returns:
        AnswerResponse con la respuesta generada
    """
    try:
        logger.info(f"Recibida pregunta: {request.question}")
        
        if not request.question or len(request.question.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La pregunta no puede estar vacía"
            )
        
        response = await query_service.process_question(request.question)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error procesando pregunta: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al procesar la pregunta: {str(e)}"
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verifica el estado del sistema y la base de conocimiento"
)
async def health_check(
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base)
) -> HealthResponse:
    """
    Endpoint de health check
    
    Args:
        knowledge_base: Base de conocimiento (inyectada)
        
    Returns:
        HealthResponse con el estado del sistema
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        knowledge_base_loaded=knowledge_base.loaded
    )


@router.get(
    "/entities/{entity_type}",
    response_model=EntityListResponse,
    summary="Listar entidades",
    description="Obtiene una lista de entidades de un tipo específico (drivers, teams, circuits, sessions)",
    responses={
        200: {"description": "Lista de entidades"},
        400: {"description": "Tipo de entidad inválido", "model": ErrorResponse},
        404: {"description": "No se encontraron entidades", "model": ErrorResponse}
    }
)
async def get_entities(
    entity_type: str,
    year: Optional[int] = None,
    name: Optional[str] = None,
    limit: int = 50,
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base)
) -> EntityListResponse:
    """
    Obtiene entidades de un tipo específico
    
    Args:
        entity_type: Tipo de entidad (drivers, teams, circuits, sessions)
        year: Año para filtrar (opcional)
        name: Nombre para filtrar (opcional)
        limit: Límite de resultados
        knowledge_base: Base de conocimiento (inyectada)
        
    Returns:
        EntityListResponse con la lista de entidades
    """
    try:
        # Mapear tipo de entidad de plural a singular
        type_map = {
            'drivers': 'piloto',
            'teams': 'equipo',
            'circuits': 'circuito',
            'sessions': 'sesion',
            'motors': 'motor',
            'countries': 'pais'
        }
        
        node_type = type_map.get(entity_type.lower())
        
        if not node_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de entidad inválido: {entity_type}. Tipos válidos: {', '.join(type_map.keys())}"
            )
        
        # Construir filtros
        filters = {}
        if year:
            filters['year'] = year
        if name:
            filters['nombre'] = name
        
        # Obtener entidades
        network = knowledge_base.get_semantic_network()
        entities = network.find_nodes_by_type(node_type, filters if filters else None)
        
        # Limitar resultados
        entities = entities[:limit]
        
        if not entities:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron entidades de tipo {entity_type}"
            )
        
        # Formatear entidades
        formatted_entities = [
            {
                'id': entity['id'],
                'type': entity['type'],
                'attributes': entity['attributes']
            }
            for entity in entities
        ]
        
        logger.info(f"Retornadas {len(formatted_entities)} entidades de tipo {entity_type}")
        
        return EntityListResponse(
            entity_type=entity_type,
            count=len(formatted_entities),
            entities=formatted_entities
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo entidades: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener entidades: {str(e)}"
        )


@router.get(
    "/network/explore/{node_id}",
    response_model=NetworkExploreResponse,
    summary="Explorar red semántica",
    description="Explora el vecindario de un nodo en la red semántica",
    responses={
        200: {"description": "Vecindario del nodo"},
        404: {"description": "Nodo no encontrado", "model": ErrorResponse}
    }
)
async def explore_network(
    node_id: str,
    depth: int = 2,
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base)
) -> NetworkExploreResponse:
    """
    Explora el vecindario de un nodo en la red semántica
    
    Args:
        node_id: ID del nodo a explorar
        depth: Profundidad de exploración (default: 2)
        knowledge_base: Base de conocimiento (inyectada)
        
    Returns:
        NetworkExploreResponse con el nodo y sus nodos relacionados
    """
    try:
        network = knowledge_base.get_semantic_network()
        
        # Obtener detalles del nodo
        node_details = network.get_node_details(node_id)
        
        if not node_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nodo '{node_id}' no encontrado"
            )
        
        # Explorar vecindario
        related_entities = network.get_related_entities(node_id, max_depth=min(depth, 3))
        
        logger.info(f"Explorado nodo {node_id} con profundidad {depth}")
        
        return NetworkExploreResponse(
            node_id=node_id,
            node_type=node_details['type'],
            attributes=node_details['attributes'],
            related_nodes=related_entities
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error explorando red: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al explorar la red: {str(e)}"
        )


@router.post(
    "/reload",
    response_model=dict,
    summary="Recargar base de conocimiento",
    description="Recarga la base de conocimiento con datos del año especificado",
    responses={
        200: {"description": "Base de conocimiento recargada"},
        500: {"description": "Error al recargar", "model": ErrorResponse}
    }
)
async def reload_knowledge_base(
    year: int = 2024,
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base)
) -> dict:
    """
    Recarga la base de conocimiento con datos de un año específico
    
    Args:
        year: Año para cargar datos (default: 2024)
        knowledge_base: Base de conocimiento (inyectada)
        
    Returns:
        Diccionario con el estado de la recarga
    """
    try:
        logger.info(f"Recargando base de conocimiento para el año {year}")
        
        await knowledge_base.load_data(year=year)
        
        network = knowledge_base.get_semantic_network()
        stats = network.get_stats()
        
        return {
            "status": "success",
            "message": f"Base de conocimiento recargada para el año {year}",
            "stats": stats
        }
        
    except Exception as e:
        logger.error(f"Error recargando base de conocimiento: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al recargar base de conocimiento: {str(e)}"
        )


@router.get(
    "/stats",
    response_model=dict,
    summary="Estadísticas de la red",
    description="Obtiene estadísticas de la red semántica"
)
async def get_stats(
    knowledge_base: KnowledgeBase = Depends(get_knowledge_base)
) -> dict:
    """
    Obtiene estadísticas de la red semántica
    
    Args:
        knowledge_base: Base de conocimiento (inyectada)
        
    Returns:
        Diccionario con estadísticas
    """
    try:
        network = knowledge_base.get_semantic_network()
        stats = network.get_stats()
        
        return {
            "status": "success",
            "stats": stats,
            "knowledge_base_loaded": knowledge_base.loaded
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )

