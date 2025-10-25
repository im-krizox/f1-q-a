"""
Dependency Injection para FastAPI
"""
from fastapi import Request
from ..core.config import Settings, get_settings
from ..services.knowledge_base import KnowledgeBase
from ..services.nlp_processor import NLPProcessor
from ..services.query_service import QueryService


def get_knowledge_base(request: Request) -> KnowledgeBase:
    """
    Obtiene la instancia de KnowledgeBase del estado de la aplicación
    
    Args:
        request: Request de FastAPI
        
    Returns:
        Instancia de KnowledgeBase
    """
    return request.app.state.knowledge_base


def get_nlp_processor(request: Request) -> NLPProcessor:
    """
    Obtiene la instancia de NLPProcessor del estado de la aplicación
    
    Args:
        request: Request de FastAPI
        
    Returns:
        Instancia de NLPProcessor
    """
    return request.app.state.nlp_processor


def get_query_service(request: Request) -> QueryService:
    """
    Obtiene la instancia de QueryService del estado de la aplicación
    
    Args:
        request: Request de FastAPI
        
    Returns:
        Instancia de QueryService
    """
    return request.app.state.query_service


def get_settings_dependency() -> Settings:
    """
    Obtiene la configuración de la aplicación
    
    Returns:
        Instancia de Settings
    """
    return get_settings()

