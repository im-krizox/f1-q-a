"""
Esquemas para request/response de la API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class QuestionRequest(BaseModel):
    """Esquema para la petición de pregunta"""
    question: str = Field(..., description="Pregunta del usuario", min_length=1, max_length=500)
    context: Optional[Dict[str, Any]] = Field(default=None, description="Contexto adicional opcional")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "¿Quién es Max Verstappen?",
                    "context": {}
                }
            ]
        }
    }


class AnswerResponse(BaseModel):
    """Esquema para la respuesta a una pregunta"""
    answer: str = Field(..., description="Respuesta generada")
    confidence: float = Field(..., description="Nivel de confianza (0.0 a 1.0)", ge=0.0, le=1.0)
    related_entities: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="Entidades relacionadas encontradas"
    )
    query_type: str = Field(..., description="Tipo de consulta detectada")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadatos adicionales")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "Max Verstappen es un piloto neerlandés que corre para Red Bull Racing.",
                    "confidence": 0.95,
                    "related_entities": [
                        {"type": "piloto", "name": "Max Verstappen"},
                        {"type": "equipo", "name": "Red Bull Racing"}
                    ],
                    "query_type": "pilot_info",
                    "metadata": {"driver_number": 1}
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Esquema para la respuesta de health check"""
    status: str = Field(..., description="Estado del sistema")
    version: str = Field(..., description="Versión de la aplicación")
    knowledge_base_loaded: bool = Field(..., description="Indica si la base de conocimiento está cargada")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "version": "1.0.0",
                    "knowledge_base_loaded": True
                }
            ]
        }
    }


class EntityListResponse(BaseModel):
    """Esquema para respuesta de lista de entidades"""
    entity_type: str = Field(..., description="Tipo de entidad")
    count: int = Field(..., description="Número de entidades")
    entities: List[Dict[str, Any]] = Field(..., description="Lista de entidades")


class NetworkExploreResponse(BaseModel):
    """Esquema para respuesta de exploración de red"""
    node_id: str = Field(..., description="ID del nodo explorado")
    node_type: str = Field(..., description="Tipo del nodo")
    attributes: Dict[str, Any] = Field(..., description="Atributos del nodo")
    related_nodes: Dict[str, List[Dict[str, Any]]] = Field(
        default_factory=dict,
        description="Nodos relacionados agrupados por tipo"
    )


class ErrorResponse(BaseModel):
    """Esquema para respuestas de error"""
    error: str = Field(..., description="Mensaje de error")
    detail: Optional[str] = Field(default=None, description="Detalle adicional del error")
    code: Optional[int] = Field(default=None, description="Código de error")

