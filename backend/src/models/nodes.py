"""
Modelos de datos para los nodos de la red semántica
"""
from pydantic import BaseModel, Field
from typing import Optional


class PilotoNode(BaseModel):
    """Modelo para nodo de Piloto"""
    nombre: str = Field(..., description="Nombre completo del piloto")
    numero_piloto: int = Field(..., description="Número del piloto en la temporada")
    nacionalidad: str = Field(..., description="Nacionalidad del piloto")
    driver_number: int = Field(..., description="Número del piloto para API")
    
    model_config = {"from_attributes": True}


class EquipoNode(BaseModel):
    """Modelo para nodo de Equipo"""
    nombre_equipo: str = Field(..., description="Nombre del equipo")
    jefe_equipo: str = Field(default="", description="Jefe del equipo")
    team_name: str = Field(..., description="Nombre del equipo para API")
    
    model_config = {"from_attributes": True}


class MotorNode(BaseModel):
    """Modelo para nodo de Motor"""
    fabricante: str = Field(..., description="Fabricante del motor")
    proveedor_combustible: str = Field(default="", description="Proveedor de combustible")
    
    model_config = {"from_attributes": True}


class CircuitoNode(BaseModel):
    """Modelo para nodo de Circuito"""
    nombre_oficial: str = Field(..., description="Nombre oficial del circuito")
    pais: str = Field(..., description="País donde se ubica el circuito")
    longitud_metros: float = Field(default=0.0, description="Longitud del circuito en metros")
    circuit_key: int = Field(..., description="Clave del circuito para API")
    circuit_short_name: str = Field(..., description="Nombre corto del circuito")
    
    model_config = {"from_attributes": True}


class SesionNode(BaseModel):
    """Modelo para nodo de Sesión"""
    session_key: int = Field(..., description="Clave única de la sesión")
    tipo: str = Field(..., description="Tipo de sesión: R (Race), Q (Qualifying), P (Practice)")
    fecha: str = Field(..., description="Fecha de la sesión")
    session_name: str = Field(..., description="Nombre de la sesión")
    year: int = Field(..., description="Año de la sesión")
    location: str = Field(default="", description="Ubicación de la sesión")
    
    model_config = {"from_attributes": True}


class PaisNode(BaseModel):
    """Modelo para nodo de País"""
    nombre: str = Field(..., description="Nombre del país")
    codigo: str = Field(default="", description="Código del país")
    
    model_config = {"from_attributes": True}


class TipoEventoNode(BaseModel):
    """Modelo para nodo de Tipo de Evento"""
    nombre: str = Field(..., description="Nombre del tipo de evento")
    descripcion: str = Field(default="", description="Descripción del tipo de evento")
    
    model_config = {"from_attributes": True}

