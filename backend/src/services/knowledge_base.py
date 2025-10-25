"""
Base de Conocimiento - Carga y pobla la red semántica con datos de F1
"""
import logging
from typing import Dict, List, Any, Optional
from ..core.semantic_network import SemanticNetwork
from .openf1_client import OpenF1Client

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Gestiona la carga y población de la red semántica"""
    
    # Mapeo de códigos de país a nombres completos
    COUNTRY_CODES = {
        'NED': 'Países Bajos',
        'MEX': 'México',
        'GBR': 'Reino Unido',
        'ESP': 'España',
        'MON': 'Mónaco',
        'CAN': 'Canadá',
        'AUS': 'Australia',
        'JPN': 'Japón',
        'FRA': 'Francia',
        'FIN': 'Finlandia',
        'CHN': 'China',
        'THA': 'Tailandia',
        'DEN': 'Dinamarca',
        'GER': 'Alemania',
        'USA': 'Estados Unidos',
        'NZL': 'Nueva Zelanda',
    }
    
    # Mapeo de equipos a motores
    TEAM_ENGINE_MAP = {
        'red bull racing': 'Honda RBPT',
        'mercedes-amg petronas': 'Mercedes',
        'scuderia ferrari': 'Ferrari',
        'mclaren racing': 'Mercedes',
        'aston martin aramco': 'Mercedes',
        'alpine f1 team': 'Renault',
        'williams racing': 'Mercedes',
        'scuderia alphatauri': 'Honda RBPT',
        'rb f1 team': 'Honda RBPT',
        'alfa romeo f1 team': 'Ferrari',
        'haas f1 team': 'Ferrari',
    }
    
    # Jefes de equipo conocidos
    TEAM_PRINCIPALS = {
        'red bull racing': 'Christian Horner',
        'mercedes-amg petronas': 'Toto Wolff',
        'scuderia ferrari': 'Frédéric Vasseur',
        'mclaren racing': 'Andrea Stella',
        'aston martin aramco': 'Mike Krack',
        'alpine f1 team': 'Bruno Famin',
        'williams racing': 'James Vowles',
        'scuderia alphatauri': 'Laurent Mekies',
        'rb f1 team': 'Laurent Mekies',
        'alfa romeo f1 team': 'Alessandro Alunni Bravi',
        'haas f1 team': 'Guenther Steiner',
    }
    
    def __init__(self, openf1_client: OpenF1Client):
        """
        Inicializa la base de conocimiento
        
        Args:
            openf1_client: Cliente para la API de OpenF1
        """
        self.client = openf1_client
        self.network = SemanticNetwork()
        self.loaded = False
        logger.info("KnowledgeBase inicializada")
    
    def _normalize_name(self, name: str) -> str:
        """Normaliza nombres para usar como IDs"""
        return name.lower().replace(' ', '_').replace('-', '_')
    
    async def load_data(self, year: int = 2024) -> None:
        """
        Carga datos de OpenF1 y pobla la red semántica
        
        Args:
            year: Año para cargar datos
        """
        logger.info(f"Iniciando carga de datos para el año {year}")
        
        try:
            # Cargar datos en orden
            meetings = await self.client.get_meetings(year=year)
            logger.info(f"Obtenidos {len(meetings)} meetings")
            
            sessions = await self.client.get_sessions(year=year)
            logger.info(f"Obtenidas {len(sessions)} sesiones")
            
            # Poblar red semántica
            await self._populate_circuits(meetings)
            await self._populate_sessions(sessions)
            await self._populate_drivers(sessions)
            await self._populate_teams()
            await self._populate_motors()
            await self._populate_types()
            await self._create_relationships(sessions)
            
            self.loaded = True
            stats = self.network.get_stats()
            logger.info(f"Base de conocimiento cargada exitosamente: {stats}")
            
        except Exception as e:
            logger.error(f"Error cargando base de conocimiento: {e}", exc_info=True)
            raise
    
    async def _populate_circuits(self, meetings: List[Dict[str, Any]]) -> None:
        """
        Pobla nodos de circuitos y países
        
        Args:
            meetings: Lista de meetings desde la API
        """
        logger.info("Poblando circuitos...")
        
        circuits_added = set()
        countries_added = set()
        
        for meeting in meetings:
            circuit_key = meeting.get('circuit_key')
            circuit_name = meeting.get('circuit_short_name', '')
            country_name = meeting.get('country_name', '')
            location = meeting.get('location', '')
            
            if not circuit_key or not circuit_name:
                continue
            
            circuit_id = f"circuit_{circuit_key}"
            
            # Agregar nodo de circuito solo una vez
            if circuit_id not in circuits_added:
                # Nombre oficial del circuito (puede requerir mapeo manual)
                official_name = f"{circuit_name} Circuit"
                if 'Monaco' in circuit_name:
                    official_name = "Circuit de Monaco"
                elif 'Silverstone' in circuit_name:
                    official_name = "Silverstone Circuit"
                
                self.network.add_node(
                    node_id=circuit_id,
                    node_type='circuito',
                    attributes={
                        'nombre_oficial': official_name,
                        'pais': country_name,
                        'longitud_metros': 5000.0,  # Valor por defecto
                        'circuit_key': circuit_key,
                        'circuit_short_name': circuit_name,
                        'location': location
                    }
                )
                circuits_added.add(circuit_id)
            
            # Agregar nodo de país
            if country_name:
                country_id = f"country_{self._normalize_name(country_name)}"
                
                if country_id not in countries_added:
                    self.network.add_node(
                        node_id=country_id,
                        node_type='pais',
                        attributes={
                            'nombre': country_name,
                            'codigo': ''
                        }
                    )
                    countries_added.add(country_id)
                
                # Crear relación circuito -> país
                self.network.add_edge(
                    source=circuit_id,
                    target=country_id,
                    relation='esta_en'
                )
        
        logger.info(f"Agregados {len(circuits_added)} circuitos y {len(countries_added)} países")
    
    async def _populate_sessions(self, sessions: List[Dict[str, Any]]) -> None:
        """
        Pobla nodos de sesiones
        
        Args:
            sessions: Lista de sesiones desde la API
        """
        logger.info("Poblando sesiones...")
        
        sessions_added = 0
        
        for session in sessions:
            session_key = session.get('session_key')
            session_name = session.get('session_name', '')
            date_start = session.get('date_start', '')
            year = session.get('year')
            circuit_key = session.get('circuit_key')
            location = session.get('location', '')
            
            if not session_key:
                continue
            
            # Determinar tipo de sesión
            tipo = 'P'  # Practice por defecto
            if 'Race' in session_name or 'Sprint' in session_name:
                tipo = 'R'
            elif 'Qualifying' in session_name:
                tipo = 'Q'
            
            session_id = f"session_{session_key}"
            
            # Extraer solo la fecha
            fecha = date_start.split('T')[0] if 'T' in date_start else date_start
            
            self.network.add_node(
                node_id=session_id,
                node_type='sesion',
                attributes={
                    'session_key': session_key,
                    'tipo': tipo,
                    'fecha': fecha,
                    'session_name': session_name,
                    'year': year or 2024,
                    'location': location,
                    'circuit_key': circuit_key
                }
            )
            
            # Crear relación sesión -> circuito
            if circuit_key:
                circuit_id = f"circuit_{circuit_key}"
                self.network.add_edge(
                    source=session_id,
                    target=circuit_id,
                    relation='ocurre_en'
                )
            
            sessions_added += 1
        
        logger.info(f"Agregadas {sessions_added} sesiones")
    
    async def _populate_drivers(self, sessions: List[Dict[str, Any]]) -> None:
        """
        Pobla nodos de pilotos
        
        Args:
            sessions: Lista de sesiones para obtener pilotos
        """
        logger.info("Poblando pilotos...")
        
        drivers_added = set()
        
        # Obtener pilotos de varias sesiones
        for session in sessions[:5]:  # Limitar a primeras 5 sesiones para optimizar
            session_key = session.get('session_key')
            if not session_key:
                continue
            
            drivers = await self.client.get_drivers(session_key=session_key)
            
            for driver in drivers:
                driver_number = driver.get('driver_number')
                full_name = driver.get('full_name', '')
                name_acronym = driver.get('name_acronym', '')
                team_name = driver.get('team_name', '')
                country_code = driver.get('country_code', '')
                
                if not driver_number or not full_name:
                    continue
                
                driver_id = f"driver_{driver_number}"
                
                # Agregar solo una vez
                if driver_id in drivers_added:
                    continue
                
                # Obtener nombre completo de país
                nacionalidad = self.COUNTRY_CODES.get(country_code, country_code)
                
                self.network.add_node(
                    node_id=driver_id,
                    node_type='piloto',
                    attributes={
                        'nombre': full_name,
                        'numero_piloto': driver_number,
                        'nacionalidad': nacionalidad,
                        'driver_number': driver_number,
                        'name_acronym': name_acronym,
                        'team_name': team_name,
                        'country_code': country_code
                    }
                )
                
                drivers_added.add(driver_id)
        
        logger.info(f"Agregados {len(drivers_added)} pilotos")
    
    async def _populate_teams(self) -> None:
        """Pobla nodos de equipos"""
        logger.info("Poblando equipos...")
        
        # Obtener equipos únicos de los pilotos ya agregados
        teams_from_drivers = set()
        
        for node_id in self.network.nodes_by_type.get('piloto', []):
            node_data = self.network.get_node_details(node_id)
            if node_data:
                team_name = node_data['attributes'].get('team_name', '')
                if team_name:
                    teams_from_drivers.add(team_name)
        
        # Agregar nodos de equipos
        for team_name in teams_from_drivers:
            team_id = f"team_{self._normalize_name(team_name)}"
            
            # Obtener jefe de equipo
            team_principal = self.TEAM_PRINCIPALS.get(team_name.lower(), '')
            
            self.network.add_node(
                node_id=team_id,
                node_type='equipo',
                attributes={
                    'nombre_equipo': team_name,
                    'jefe_equipo': team_principal,
                    'team_name': team_name
                }
            )
        
        logger.info(f"Agregados {len(teams_from_drivers)} equipos")
    
    async def _populate_motors(self) -> None:
        """Pobla nodos de motores"""
        logger.info("Poblando motores...")
        
        motors = [
            {'fabricante': 'Mercedes', 'proveedor_combustible': 'Petronas'},
            {'fabricante': 'Ferrari', 'proveedor_combustible': 'Shell'},
            {'fabricante': 'Honda RBPT', 'proveedor_combustible': 'ExxonMobil'},
            {'fabricante': 'Renault', 'proveedor_combustible': 'BP'},
        ]
        
        for motor in motors:
            motor_id = f"engine_{self._normalize_name(motor['fabricante'])}"
            
            self.network.add_node(
                node_id=motor_id,
                node_type='motor',
                attributes=motor
            )
        
        logger.info(f"Agregados {len(motors)} motores")
    
    async def _populate_types(self) -> None:
        """Pobla nodos de tipos de eventos"""
        logger.info("Poblando tipos de eventos...")
        
        types = [
            {'id': 'tipo_race', 'nombre': 'Race', 'descripcion': 'Carrera principal'},
            {'id': 'tipo_qualifying', 'nombre': 'Qualifying', 'descripcion': 'Sesión de clasificación'},
            {'id': 'tipo_practice', 'nombre': 'Practice', 'descripcion': 'Sesión de práctica'},
        ]
        
        for tipo in types:
            self.network.add_node(
                node_id=tipo['id'],
                node_type='tipo_evento',
                attributes={
                    'nombre': tipo['nombre'],
                    'descripcion': tipo['descripcion']
                }
            )
        
        logger.info(f"Agregados {len(types)} tipos de eventos")
    
    async def _create_relationships(self, sessions: List[Dict[str, Any]]) -> None:
        """
        Crea relaciones entre nodos
        
        Args:
            sessions: Lista de sesiones
        """
        logger.info("Creando relaciones...")
        
        relationships_count = 0
        
        # Relación piloto -> equipo (conduce_para)
        for driver_id in self.network.nodes_by_type.get('piloto', []):
            driver_data = self.network.get_node_details(driver_id)
            if driver_data:
                team_name = driver_data['attributes'].get('team_name', '')
                if team_name:
                    team_id = f"team_{self._normalize_name(team_name)}"
                    self.network.add_edge(
                        source=driver_id,
                        target=team_id,
                        relation='conduce_para',
                        attributes={'season': 2024}
                    )
                    relationships_count += 1
        
        # Relación equipo -> motor (usa_motor)
        for team_id in self.network.nodes_by_type.get('equipo', []):
            team_data = self.network.get_node_details(team_id)
            if team_data:
                team_name = team_data['attributes'].get('team_name', '').lower()
                engine = self.TEAM_ENGINE_MAP.get(team_name, '')
                if engine:
                    engine_id = f"engine_{self._normalize_name(engine)}"
                    self.network.add_edge(
                        source=team_id,
                        target=engine_id,
                        relation='usa_motor'
                    )
                    relationships_count += 1
        
        # Relación sesión -> tipo (es_un_tipo_de)
        for session_id in self.network.nodes_by_type.get('sesion', []):
            session_data = self.network.get_node_details(session_id)
            if session_data:
                tipo = session_data['attributes'].get('tipo', 'P')
                type_map = {'R': 'tipo_race', 'Q': 'tipo_qualifying', 'P': 'tipo_practice'}
                type_id = type_map.get(tipo, 'tipo_practice')
                
                self.network.add_edge(
                    source=session_id,
                    target=type_id,
                    relation='es_un_tipo_de'
                )
                relationships_count += 1
        
        # Nota: Las relaciones "tiene_ganador" se crearían con datos de resultados
        # que requieren consultas adicionales a la API
        
        logger.info(f"Creadas {relationships_count} relaciones")
    
    def get_semantic_network(self) -> SemanticNetwork:
        """Retorna la instancia de la red semántica"""
        return self.network

