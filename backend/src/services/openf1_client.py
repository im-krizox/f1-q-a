"""
Cliente para la API de OpenF1
"""
import httpx
import logging
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


class OpenF1Client:
    """Cliente asíncrono para interactuar con la API de OpenF1"""
    
    def __init__(self, base_url: str):
        """
        Inicializa el cliente de OpenF1
        
        Args:
            base_url: URL base de la API de OpenF1
        """
        self.base_url = base_url.rstrip('/')
        self.client: Optional[httpx.AsyncClient] = None
        self.timeout = httpx.Timeout(30.0, connect=10.0)
        logger.info(f"OpenF1Client inicializado con base_url: {self.base_url}")
    
    async def __aenter__(self):
        """Context manager entry"""
        self.client = httpx.AsyncClient(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.close()
    
    async def _ensure_client(self):
        """Asegura que el cliente esté inicializado"""
        if self.client is None:
            self.client = httpx.AsyncClient(timeout=self.timeout)
    
    async def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Realiza una petición HTTP a la API
        
        Args:
            endpoint: Endpoint de la API (sin barra inicial)
            params: Parámetros de consulta opcionales
            
        Returns:
            Lista de diccionarios con los datos de respuesta
        """
        await self._ensure_client()
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            logger.debug(f"Realizando petición GET a: {url} con params: {params}")
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list):
                logger.info(f"Obtenidos {len(data)} elementos desde {endpoint}")
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                logger.warning(f"Respuesta inesperada de tipo {type(data)}")
                return []
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Error HTTP {e.response.status_code} en {url}: {e}")
            return []
        except httpx.RequestError as e:
            logger.error(f"Error de conexión en {url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado en petición a {url}: {e}")
            return []
    
    async def get_drivers(
        self, 
        session_key: Optional[int] = None,
        driver_number: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene información de pilotos
        
        Args:
            session_key: Clave de sesión para filtrar pilotos
            driver_number: Número de piloto específico
            
        Returns:
            Lista de diccionarios con información de pilotos
        """
        params = {}
        if session_key:
            params['session_key'] = session_key
        if driver_number:
            params['driver_number'] = driver_number
            
        return await self._make_request('drivers', params)
    
    async def get_sessions(
        self, 
        year: Optional[int] = None,
        session_name: Optional[str] = None,
        session_key: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene información de sesiones
        
        Args:
            year: Año para filtrar sesiones
            session_name: Nombre de sesión (Race, Qualifying, Practice, etc.)
            session_key: Clave de sesión específica
            
        Returns:
            Lista de diccionarios con información de sesiones
        """
        params = {}
        if year:
            params['year'] = year
        if session_name:
            params['session_name'] = session_name
        if session_key:
            params['session_key'] = session_key
            
        return await self._make_request('sessions', params)
    
    async def get_meetings(
        self, 
        year: Optional[int] = None,
        meeting_key: Optional[int] = None,
        country_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtiene información de eventos/circuitos (meetings)
        
        Args:
            year: Año para filtrar eventos
            meeting_key: Clave de evento específico
            country_name: Nombre del país
            
        Returns:
            Lista de diccionarios con información de eventos
        """
        params = {}
        if year:
            params['year'] = year
        if meeting_key:
            params['meeting_key'] = meeting_key
        if country_name:
            params['country_name'] = country_name
            
        return await self._make_request('meetings', params)
    
    async def get_session_results(
        self, 
        session_key: int
    ) -> List[Dict[str, Any]]:
        """
        Obtiene resultados de una sesión específica
        
        Args:
            session_key: Clave de la sesión
            
        Returns:
            Lista de diccionarios con resultados (posiciones, tiempos, etc.)
        """
        params = {'session_key': session_key}
        
        # La API puede no tener un endpoint específico de results
        # Intentamos con 'position' que suele tener la información de resultados
        results = await self._make_request('position', params)
        
        # Si no hay resultados, intentamos obtenerlos de 'stints' o 'laps'
        if not results:
            logger.info(f"No se encontraron resultados en 'position', intentando 'laps'")
            results = await self._make_request('laps', params)
        
        return results
    
    async def get_race_control(
        self,
        session_key: int
    ) -> List[Dict[str, Any]]:
        """
        Obtiene mensajes de control de carrera
        
        Args:
            session_key: Clave de la sesión
            
        Returns:
            Lista de mensajes de control de carrera
        """
        params = {'session_key': session_key}
        return await self._make_request('race_control', params)
    
    async def close(self):
        """Cierra el cliente HTTP"""
        if self.client:
            await self.client.aclose()
            self.client = None
            logger.info("OpenF1Client cerrado")

