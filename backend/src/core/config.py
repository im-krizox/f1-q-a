"""
Configuración de la aplicación usando Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API OpenF1
    openf1_base_url: str = "https://api.openf1.org/v1"
    openf1_api_key: str = ""  # API key para OpenF1 (opcional, requerido durante sesiones en vivo)
    
    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8080,http://localhost"
    
    # Logging
    log_level: str = "INFO"
    
    # App
    app_name: str = "F1 Q&A System"
    app_version: str = "1.0.0"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convierte la cadena de orígenes CORS en una lista"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


def get_settings() -> Settings:
    """
    Retorna una instancia de Settings
    Esta función puede ser usada como dependencia en FastAPI
    """
    return Settings()

