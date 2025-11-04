"""
Procesador de Lenguaje Natural para analizar preguntas en español
"""
import re
import logging
from typing import Dict, List, Any, Optional
from unidecode import unidecode
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


class NLPProcessor:
    """Procesador NLP para analizar preguntas sobre F1 en español"""
    
    def __init__(self):
        """Inicializa el procesador NLP con patrones y diccionarios"""
        self._init_patterns()
        self._init_synonyms()
        self._init_known_entities()
        logger.info("NLPProcessor inicializado")
    
    def _init_patterns(self):
        """Define patrones de regex para diferentes tipos de preguntas"""
        self.patterns = {
            'pilot_info': [
                r'(?:quién es|quien es|quíen es|dime (?:sobre|quién es)|información (?:sobre|de)|háblame (?:de|sobre))\s+([A-ZÁ-Ú][a-záéíóúñ]+(?:\s+[A-ZÁ-Ú][a-záéíóúñ]+)*)',
                r'(?:qué|que) piloto.*(?:número|numero)\s+(\d+)',
                r'piloto.*(?:número|numero)\s+(\d+)',
                r'datos.*piloto\s+([A-ZÁ-Ú][a-záéíóúñ]+(?:\s+[A-ZÁ-Ú][a-záéíóúñ]+)*)',
            ],
            'team_info': [
                r'(?:para qué|para que|en qué|en que)\s+equipo.*(?:corre|conduce|está|esta|pilota)\s+([A-ZÁ-Ú][a-záéíóúñ]+(?:\s+[A-ZÁ-Ú][a-záéíóúñ]+)*)',
                r'(?:qué|que)\s+equipo.*([A-ZÁ-Ú][a-záéíóúñ]+(?:\s+[A-ZÁ-Ú][a-záéíóúñ]+)*)',
                r'equipo\s+de\s+([A-ZÁ-Ú][a-záéíóúñ]+(?:\s+[A-ZÁ-Ú][a-záéíóúñ]+)*)',
                r'(?:qué|que|cuál|cual).*(?:escudería|escuderia).*([A-ZÁ-Ú][a-záéíóúñ]+)',
            ],
            'winner_info': [
                r'(?:quién ganó|quien ganó|quíen gano|ganador (?:de|del))\s+(?:el\s+)?(?:GP|Gran Premio|gp)\s+(?:de\s+)?([A-ZÁ-Ú][a-záéíóúñ]+)(?:\s+(\d{4}))?',
                r'(?:quién se llevó|quien se llevo).*(?:GP|Gran Premio)\s+(?:de\s+)?([A-ZÁ-Ú][a-záéíóúñ]+)',
                r'resultado.*(?:GP|Gran Premio)\s+(?:de\s+)?([A-ZÁ-Ú][a-záéíóúñ]+)(?:\s+(\d{4}))?',
                r'(?:quién triunfó|quien triunfo|quién venció|quien vencio).*([A-ZÁ-Ú][a-záéíóúñ]+)',
            ],
            'motor_info': [
                r'(?:qué|que)\s+motor\s+(?:usa|utiliza|tiene)\s+([A-ZÁ-Ú][a-záéíóúñ]+(?:\s+[A-ZÁ-Ú][a-záéíóúñ]+)*)',
                r'motor\s+(?:de|del)\s+([A-ZÁ-Ú][a-záéíóúñ]+(?:\s+[A-ZÁ-Ú][a-záéíóúñ]+)*)',
                r'(?:qué|que).*(?:fabricante|proveedor).*motor.*([A-ZÁ-Ú][a-záéíóúñ]+)',
                r'(?:propulsor|unidad de potencia).*([A-ZÁ-Ú][a-záéíóúñ]+)',
            ],
            'circuit_info': [
                r'(?:dónde|donde)\s+(?:está|esta|queda|se encuentra).*circuito\s+(?:de\s+)?([A-ZÁ-Ú][a-záéíóúñ]+)',
                r'(?:en qué país|en que pais).*circuito.*([A-ZÁ-Ú][a-záéíóúñ]+)',
                r'ubicación.*circuito.*([A-ZÁ-Ú][a-záéíóúñ]+)',
                r'circuito\s+(?:de|en)\s+([A-ZÁ-Ú][a-záéíóúñ]+)',
                r'(?:pista|trazado)\s+(?:de\s+)?([A-ZÁ-Ú][a-záéíóúñ]+)',
            ],
            'session_info': [
                r'(?:cuándo|cuando).*(?:GP|Gran Premio|carrera)\s+(?:de\s+)?([A-ZÁ-Ú][a-záéíóúñ]+)',
                r'fecha.*(?:GP|Gran Premio).*([A-ZÁ-Ú][a-záéíóúñ]+)',
                r'(?:qué|que)\s+sesión.*([A-ZÁ-Ú][a-záéíóúñ]+)',
            ]
        }
    
    def _init_synonyms(self):
        """Define diccionario de sinónimos"""
        self.synonyms = {
            'equipo': ['escudería', 'escuderia', 'team', 'conjunto', 'escuadra'],
            'piloto': ['corredor', 'driver', 'conductor', 'piloteador'],
            'motor': ['propulsor', 'unidad de potencia', 'engine', 'powerunit'],
            'circuito': ['pista', 'trazado', 'autódromo', 'autodromo', 'circuit'],
            'ganó': ['venció', 'vencio', 'triunfó', 'triunfo', 'se impuso', 'ganador'],
            'corre': ['conduce', 'pilota', 'compite', 'está', 'esta'],
        }
    
    def _init_known_entities(self):
        """Define entidades conocidas (pilotos, equipos, circuitos)"""
        self.known_drivers = {
            'max verstappen': {'name': 'Max Verstappen', 'number': 1},
            'sergio perez': {'name': 'Sergio Pérez', 'number': 11},
            'lewis hamilton': {'name': 'Lewis Hamilton', 'number': 44},
            'george russell': {'name': 'George Russell', 'number': 63},
            'charles leclerc': {'name': 'Charles Leclerc', 'number': 16},
            'carlos sainz': {'name': 'Carlos Sainz', 'number': 55},
            'lando norris': {'name': 'Lando Norris', 'number': 4},
            'oscar piastri': {'name': 'Oscar Piastri', 'number': 81},
            'fernando alonso': {'name': 'Fernando Alonso', 'number': 14},
            'lance stroll': {'name': 'Lance Stroll', 'number': 18},
            'pierre gasly': {'name': 'Pierre Gasly', 'number': 10},
            'esteban ocon': {'name': 'Esteban Ocon', 'number': 31},
            'valtteri bottas': {'name': 'Valtteri Bottas', 'number': 77},
            'zhou guanyu': {'name': 'Zhou Guanyu', 'number': 24},
            'kevin magnussen': {'name': 'Kevin Magnussen', 'number': 20},
            'nico hulkenberg': {'name': 'Nico Hulkenberg', 'number': 27},
            'yuki tsunoda': {'name': 'Yuki Tsunoda', 'number': 22},
            'daniel ricciardo': {'name': 'Daniel Ricciardo', 'number': 3},
            'alexander albon': {'name': 'Alexander Albon', 'number': 23},
            'logan sargeant': {'name': 'Logan Sargeant', 'number': 2},
        }
        
        self.known_teams = {
            'red bull': 'Red Bull Racing',
            'redbull': 'Red Bull Racing',
            'mercedes': 'Mercedes-AMG Petronas',
            'ferrari': 'Scuderia Ferrari',
            'mclaren': 'McLaren Racing',
            'aston martin': 'Aston Martin Aramco',
            'alpine': 'Alpine F1 Team',
            'williams': 'Williams Racing',
            'alphatauri': 'Scuderia AlphaTauri',
            'rb': 'RB F1 Team',
            'alfa romeo': 'Alfa Romeo F1 Team',
            'sauber': 'Alfa Romeo F1 Team',
            'haas': 'Haas F1 Team',
        }
        
        self.known_circuits = {
            'bahrain': {'name': 'Bahrain International Circuit', 'country': 'Bahrain'},
            'jeddah': {'name': 'Jeddah Corniche Circuit', 'country': 'Saudi Arabia'},
            'melbourne': {'name': 'Albert Park Circuit', 'country': 'Australia'},
            'suzuka': {'name': 'Suzuka Circuit', 'country': 'Japan'},
            'shanghai': {'name': 'Shanghai International Circuit', 'country': 'China'},
            'miami': {'name': 'Miami International Autodrome', 'country': 'USA'},
            'imola': {'name': 'Autodromo Enzo e Dino Ferrari', 'country': 'Italy'},
            'monaco': {'name': 'Circuit de Monaco', 'country': 'Monaco'},
            'mónaco': {'name': 'Circuit de Monaco', 'country': 'Monaco'},
            'barcelona': {'name': 'Circuit de Barcelona-Catalunya', 'country': 'Spain'},
            'montreal': {'name': 'Circuit Gilles Villeneuve', 'country': 'Canada'},
            'silverstone': {'name': 'Silverstone Circuit', 'country': 'United Kingdom'},
            'austria': {'name': 'Red Bull Ring', 'country': 'Austria'},
            'spielberg': {'name': 'Red Bull Ring', 'country': 'Austria'},
            'paul ricard': {'name': 'Circuit Paul Ricard', 'country': 'France'},
            'hungaroring': {'name': 'Hungaroring', 'country': 'Hungary'},
            'spa': {'name': 'Circuit de Spa-Francorchamps', 'country': 'Belgium'},
            'zandvoort': {'name': 'Circuit Zandvoort', 'country': 'Netherlands'},
            'monza': {'name': 'Autodromo Nazionale di Monza', 'country': 'Italy'},
            'singapore': {'name': 'Marina Bay Street Circuit', 'country': 'Singapore'},
            'austin': {'name': 'Circuit of the Americas', 'country': 'USA'},
            'mexico': {'name': 'Mexico City', 'country': 'Mexico'},
            'méxico': {'name': 'Mexico City', 'country': 'Mexico'},
            'mexico city': {'name': 'Mexico City', 'country': 'Mexico'},
            'interlagos': {'name': 'Autódromo José Carlos Pace', 'country': 'Brazil'},
            'sao paulo': {'name': 'Autódromo José Carlos Pace', 'country': 'Brazil'},
            'las vegas': {'name': 'Las Vegas Street Circuit', 'country': 'USA'},
            'yas marina': {'name': 'Yas Marina Circuit', 'country': 'UAE'},
            'abu dhabi': {'name': 'Yas Marina Circuit', 'country': 'UAE'},
        }
    
    def normalize_text(self, text: str) -> str:
        """
        Normaliza texto removiendo acentos y convirtiendo a minúsculas
        
        Args:
            text: Texto a normalizar
            
        Returns:
            Texto normalizado
        """
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover acentos (pero mantener ñ)
        text_unaccented = unidecode(text)
        
        # Restaurar ñ si fue eliminada
        text_unaccented = text_unaccented.replace('n~', 'ñ')
        
        # Remover puntuación innecesaria pero mantener espacios
        text_clean = re.sub(r'[^\w\s]', ' ', text_unaccented)
        
        # Normalizar espacios múltiples
        text_clean = re.sub(r'\s+', ' ', text_clean).strip()
        
        return text_clean
    
    def fuzzy_match(self, text: str, candidates: Dict[str, Any], threshold: float = 0.75) -> Optional[str]:
        """
        Realiza búsqueda fuzzy (aproximada) para encontrar la mejor coincidencia
        
        Args:
            text: Texto a buscar
            candidates: Diccionario de candidatos {clave: valor}
            threshold: Umbral de similitud (0.0 a 1.0)
            
        Returns:
            Clave del mejor candidato o None si no hay coincidencias suficientes
        """
        best_match = None
        best_score = threshold
        
        text_normalized = self.normalize_text(text)
        
        for key in candidates.keys():
            key_normalized = self.normalize_text(key)
            
            # Calcular similitud usando SequenceMatcher
            similarity = SequenceMatcher(None, text_normalized, key_normalized).ratio()
            
            # También buscar si el texto está contenido en la clave
            if text_normalized in key_normalized or key_normalized in text_normalized:
                similarity = max(similarity, 0.85)
            
            if similarity > best_score:
                best_score = similarity
                best_match = key
        
        if best_match:
            logger.debug(f"Fuzzy match: '{text}' -> '{best_match}' (score: {best_score:.2f})")
        
        return best_match
    
    def extract_query_type(self, question: str) -> str:
        """
        Identifica el tipo de pregunta
        
        Args:
            question: Pregunta del usuario
            
        Returns:
            Tipo de consulta detectada
        """
        question_lower = question.lower()
        
        # Probar cada patrón
        for query_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, question, re.IGNORECASE):
                    logger.debug(f"Tipo de consulta detectado: {query_type}")
                    return query_type
        
        # Tipo por defecto si no se detecta ningún patrón específico
        logger.debug("No se detectó tipo de consulta específico, usando 'general'")
        return 'general'
    
    def extract_entities(self, question: str) -> Dict[str, List[str]]:
        """
        Extrae entidades nombradas de la pregunta
        
        Args:
            question: Pregunta del usuario
            
        Returns:
            Diccionario con entidades encontradas por tipo
        """
        entities: Dict[str, List[str]] = {
            'drivers': [],
            'teams': [],
            'circuits': [],
            'years': [],
            'numbers': []
        }
        
        question_normalized = self.normalize_text(question)
        
        # Buscar pilotos con coincidencia exacta primero
        found_drivers = False
        for driver_key, driver_info in self.known_drivers.items():
            if driver_key in question_normalized:
                entities['drivers'].append(driver_info['name'])
                found_drivers = True
        
        # Si no se encontró con coincidencia exacta, intentar fuzzy matching
        if not found_drivers:
            # Extraer nombres propios (palabras que empiezan con mayúscula)
            potential_names = re.findall(r'\b([A-ZÁ-Ú][a-záéíóúñ]+(?:\s+[A-ZÁ-Ú][a-záéíóúñ]+)*)\b', question)
            for name in potential_names:
                matched_key = self.fuzzy_match(name, self.known_drivers, threshold=0.70)
                if matched_key and self.known_drivers[matched_key]['name'] not in entities['drivers']:
                    entities['drivers'].append(self.known_drivers[matched_key]['name'])
                    logger.info(f"Fuzzy match encontrado para piloto: '{name}' -> '{self.known_drivers[matched_key]['name']}'")
        
        # Buscar equipos con coincidencia exacta primero
        found_teams = False
        for team_key, team_name in self.known_teams.items():
            if team_key in question_normalized:
                entities['teams'].append(team_name)
                found_teams = True
        
        # Si no se encontró con coincidencia exacta, intentar fuzzy matching para equipos
        if not found_teams:
            potential_teams = re.findall(r'\b([A-ZÁ-Ú][a-záéíóúñ]+(?:\s+[A-ZÁ-Ú][a-záéíóúñ]+)?)\b', question)
            for team in potential_teams:
                # Evitar palabras muy cortas (menos de 4 caracteres) que suelen ser falsos positivos
                if len(team) < 4:
                    continue
                matched_key = self.fuzzy_match(team, self.known_teams, threshold=0.75)
                if matched_key and self.known_teams[matched_key] not in entities['teams']:
                    entities['teams'].append(self.known_teams[matched_key])
                    logger.info(f"Fuzzy match encontrado para equipo: '{team}' -> '{self.known_teams[matched_key]}'")
        
        # Buscar circuitos con coincidencia exacta primero
        found_circuits = False
        for circuit_key, circuit_info in self.known_circuits.items():
            if circuit_key in question_normalized:
                entities['circuits'].append(circuit_info['name'])
                found_circuits = True
        
        # Si no se encontró con coincidencia exacta, intentar fuzzy matching para circuitos
        if not found_circuits:
            potential_circuits = re.findall(r'\b([A-ZÁ-Ú][a-záéíóúñ]+)\b', question)
            for circuit in potential_circuits:
                matched_key = self.fuzzy_match(circuit, self.known_circuits, threshold=0.75)
                if matched_key and self.known_circuits[matched_key]['name'] not in entities['circuits']:
                    entities['circuits'].append(self.known_circuits[matched_key]['name'])
                    logger.info(f"Fuzzy match encontrado para circuito: '{circuit}' -> '{self.known_circuits[matched_key]['name']}'")
        
        # Buscar años (formato 20XX)
        years = re.findall(r'\b(20\d{2})\b', question)
        entities['years'] = years
        
        # Buscar números (posibles números de piloto)
        numbers = re.findall(r'\b(\d{1,2})\b', question)
        entities['numbers'] = numbers
        
        logger.debug(f"Entidades extraídas: {entities}")
        return entities
    
    def extract_intent(self, question: str) -> Dict[str, Any]:
        """
        Extrae la intención completa de la pregunta
        
        Args:
            question: Pregunta del usuario
            
        Returns:
            Diccionario con tipo, entidades, filtros y acción
        """
        query_type = self.extract_query_type(question)
        entities = self.extract_entities(question)
        
        # Determinar acción según el tipo de consulta
        action_map = {
            'pilot_info': 'get_pilot_details',
            'team_info': 'get_team_of_pilot',
            'winner_info': 'get_race_winner',
            'motor_info': 'get_team_engine',
            'circuit_info': 'get_circuit_location',
            'session_info': 'get_session_details',
            'general': 'general_search'
        }
        
        action = action_map.get(query_type, 'general_search')
        
        # Construir filtros basados en las entidades
        filters = {}
        if entities['years']:
            filters['year'] = int(entities['years'][0])
        if entities['numbers']:
            filters['number'] = int(entities['numbers'][0])
        
        intent = {
            'type': query_type,
            'entities': entities,
            'filters': filters,
            'action': action,
            'original_question': question
        }
        
        logger.info(f"Intent extraído: {intent['type']}, acción: {action}")
        return intent

