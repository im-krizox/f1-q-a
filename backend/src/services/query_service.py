"""
Servicio de Consultas - Procesa preguntas y genera respuestas
"""
import logging
from typing import Dict, List, Any, Optional
from ..models.schemas import AnswerResponse
from .knowledge_base import KnowledgeBase
from .nlp_processor import NLPProcessor

logger = logging.getLogger(__name__)


class QueryService:
    """Servicio para procesar preguntas y generar respuestas"""
    
    def __init__(self, knowledge_base: KnowledgeBase, nlp_processor: NLPProcessor):
        """
        Inicializa el servicio de consultas
        
        Args:
            knowledge_base: Instancia de la base de conocimiento
            nlp_processor: Instancia del procesador NLP
        """
        self.knowledge_base = knowledge_base
        self.nlp_processor = nlp_processor
        self.network = knowledge_base.get_semantic_network()
        self.response_cache: Dict[str, AnswerResponse] = {}
        logger.info("QueryService inicializado")
    
    async def process_question(self, question: str) -> AnswerResponse:
        """
        Procesa una pregunta y genera una respuesta
        
        Args:
            question: Pregunta del usuario
            
        Returns:
            AnswerResponse con la respuesta generada
        """
        logger.info(f"Procesando pregunta: {question}")
        
        # Verificar caché
        if question in self.response_cache:
            logger.debug("Respuesta encontrada en caché")
            return self.response_cache[question]
        
        try:
            # Extraer intención de la pregunta
            intent = self.nlp_processor.extract_intent(question)
            query_type = intent['type']
            entities = intent['entities']
            filters = intent['filters']
            action = intent['action']
            
            # Ejecutar consulta según el tipo
            results = {}
            
            if action == 'get_pilot_details':
                results = self._query_pilot_info(entities, filters)
            elif action == 'get_team_of_pilot':
                results = self._query_team_info(entities, filters)
            elif action == 'get_race_winner':
                results = self._query_winner_info(entities, filters)
            elif action == 'get_team_engine':
                results = self._query_motor_info(entities, filters)
            elif action == 'get_circuit_location':
                results = self._query_circuit_info(entities, filters)
            elif action == 'get_session_details':
                results = self._query_session_info(entities, filters)
            else:
                results = self._query_general(entities, filters)
            
            # Calcular confianza
            confidence = self._calculate_confidence(results, intent)
            
            # Formatear respuesta
            answer = self._format_answer(results, query_type, entities)
            
            # Extraer entidades relacionadas
            related_entities = results.get('related_entities', [])
            
            # Crear respuesta
            response = AnswerResponse(
                answer=answer,
                confidence=confidence,
                related_entities=related_entities,
                query_type=query_type,
                metadata=results.get('metadata', {})
            )
            
            # Guardar en caché
            self.response_cache[question] = response
            
            logger.info(f"Respuesta generada con confianza: {confidence}")
            return response
            
        except Exception as e:
            logger.error(f"Error procesando pregunta: {e}", exc_info=True)
            
            # Respuesta de error
            return AnswerResponse(
                answer="Lo siento, tuve un problema al procesar tu pregunta. Por favor, intenta reformularla.",
                confidence=0.0,
                related_entities=[],
                query_type="error",
                metadata={"error": str(e)}
            )
    
    def _query_pilot_info(self, entities: Dict, filters: Dict) -> Dict[str, Any]:
        """
        Consulta información sobre un piloto
        
        Args:
            entities: Entidades extraídas de la pregunta
            filters: Filtros adicionales
            
        Returns:
            Diccionario con resultados
        """
        logger.debug("Ejecutando consulta de información de piloto")
        
        # Buscar piloto mencionado
        driver_name = entities['drivers'][0] if entities['drivers'] else None
        driver_number = filters.get('number')
        
        pilot_node = None
        
        # Buscar por nombre
        if driver_name:
            pilots = self.network.find_nodes_by_type('piloto', {'nombre': driver_name})
            if pilots:
                pilot_node = pilots[0]
        
        # Buscar por número
        elif driver_number:
            pilots = self.network.find_nodes_by_type('piloto', {'numero_piloto': driver_number})
            if pilots:
                pilot_node = pilots[0]
        
        if not pilot_node:
            return {
                'found': False,
                'message': 'No se encontró información del piloto',
                'related_entities': [],
                'metadata': {}
            }
        
        # Obtener equipo del piloto
        team_nodes = self.network.query_by_relation(
            pilot_node['id'],
            'conduce_para',
            direction='outgoing'
        )
        
        team_name = team_nodes[0]['attributes']['nombre_equipo'] if team_nodes else 'Desconocido'
        
        # Preparar entidades relacionadas
        related_entities = [
            {'type': 'piloto', 'name': pilot_node['attributes']['nombre'], 'id': pilot_node['id']},
        ]
        
        if team_nodes:
            related_entities.append({
                'type': 'equipo',
                'name': team_name,
                'id': team_nodes[0]['id']
            })
        
        return {
            'found': True,
            'pilot': pilot_node,
            'team': team_nodes[0] if team_nodes else None,
            'related_entities': related_entities,
            'metadata': {
                'pilot_name': pilot_node['attributes']['nombre'],
                'team_name': team_name,
                'nationality': pilot_node['attributes'].get('nacionalidad', '')
            }
        }
    
    def _query_team_info(self, entities: Dict, filters: Dict) -> Dict[str, Any]:
        """Consulta información sobre el equipo de un piloto"""
        logger.debug("Ejecutando consulta de equipo")
        
        # Primero obtener info del piloto
        pilot_info = self._query_pilot_info(entities, filters)
        
        if not pilot_info['found']:
            return pilot_info
        
        team = pilot_info.get('team')
        if not team:
            return {
                'found': False,
                'message': 'No se encontró el equipo del piloto',
                'related_entities': pilot_info['related_entities'],
                'metadata': {}
            }
        
        # Obtener motor del equipo
        motor_nodes = self.network.query_by_relation(
            team['id'],
            'usa_motor',
            direction='outgoing'
        )
        
        return {
            'found': True,
            'pilot': pilot_info['pilot'],
            'team': team,
            'motor': motor_nodes[0] if motor_nodes else None,
            'related_entities': pilot_info['related_entities'],
            'metadata': {
                'team_name': team['attributes']['nombre_equipo'],
                'team_principal': team['attributes'].get('jefe_equipo', ''),
                'motor': motor_nodes[0]['attributes']['fabricante'] if motor_nodes else 'Desconocido'
            }
        }
    
    def _query_motor_info(self, entities: Dict, filters: Dict) -> Dict[str, Any]:
        """Consulta información sobre el motor de un equipo"""
        logger.debug("Ejecutando consulta de motor")
        
        team_name = entities['teams'][0] if entities['teams'] else None
        
        if not team_name:
            return {
                'found': False,
                'message': 'No se especificó un equipo',
                'related_entities': [],
                'metadata': {}
            }
        
        # Buscar equipo
        teams = self.network.find_nodes_by_type('equipo', {'nombre_equipo': team_name})
        
        if not teams:
            return {
                'found': False,
                'message': f'No se encontró el equipo {team_name}',
                'related_entities': [],
                'metadata': {}
            }
        
        team = teams[0]
        
        # Obtener motor
        motor_nodes = self.network.query_by_relation(
            team['id'],
            'usa_motor',
            direction='outgoing'
        )
        
        if not motor_nodes:
            return {
                'found': False,
                'message': f'No se encontró información del motor de {team_name}',
                'related_entities': [],
                'metadata': {}
            }
        
        motor = motor_nodes[0]
        
        related_entities = [
            {'type': 'equipo', 'name': team['attributes']['nombre_equipo'], 'id': team['id']},
            {'type': 'motor', 'name': motor['attributes']['fabricante'], 'id': motor['id']}
        ]
        
        return {
            'found': True,
            'team': team,
            'motor': motor,
            'related_entities': related_entities,
            'metadata': {
                'team_name': team['attributes']['nombre_equipo'],
                'motor_fabricante': motor['attributes']['fabricante'],
                'proveedor_combustible': motor['attributes'].get('proveedor_combustible', '')
            }
        }
    
    def _query_circuit_info(self, entities: Dict, filters: Dict) -> Dict[str, Any]:
        """Consulta información sobre un circuito"""
        logger.debug("Ejecutando consulta de circuito")
        
        circuit_name = entities['circuits'][0] if entities['circuits'] else None
        
        if not circuit_name:
            return {
                'found': False,
                'message': 'No se especificó un circuito',
                'related_entities': [],
                'metadata': {}
            }
        
        # Buscar circuito
        circuits = self.network.find_nodes_by_type('circuito', {'nombre_oficial': circuit_name})
        
        if not circuits:
            # Intentar buscar por nombre corto
            circuits = self.network.find_nodes_by_type('circuito', {'circuit_short_name': circuit_name})
        
        if not circuits:
            return {
                'found': False,
                'message': f'No se encontró el circuito {circuit_name}',
                'related_entities': [],
                'metadata': {}
            }
        
        circuit = circuits[0]
        
        # Obtener país
        country_nodes = self.network.query_by_relation(
            circuit['id'],
            'esta_en',
            direction='outgoing'
        )
        
        country_name = country_nodes[0]['attributes']['nombre'] if country_nodes else 'Desconocido'
        
        related_entities = [
            {'type': 'circuito', 'name': circuit['attributes']['nombre_oficial'], 'id': circuit['id']},
        ]
        
        if country_nodes:
            related_entities.append({
                'type': 'pais',
                'name': country_name,
                'id': country_nodes[0]['id']
            })
        
        return {
            'found': True,
            'circuit': circuit,
            'country': country_nodes[0] if country_nodes else None,
            'related_entities': related_entities,
            'metadata': {
                'circuit_name': circuit['attributes']['nombre_oficial'],
                'country': country_name,
                'location': circuit['attributes'].get('location', '')
            }
        }
    
    def _query_winner_info(self, entities: Dict, filters: Dict) -> Dict[str, Any]:
        """Consulta información sobre el ganador de una carrera"""
        logger.debug("Ejecutando consulta de ganador")
        
        # Por ahora, sin datos de resultados específicos
        return {
            'found': False,
            'message': 'La información de ganadores requiere datos adicionales de resultados',
            'related_entities': [],
            'metadata': {}
        }
    
    def _query_session_info(self, entities: Dict, filters: Dict) -> Dict[str, Any]:
        """Consulta información sobre sesiones"""
        logger.debug("Ejecutando consulta de sesión")
        
        year = filters.get('year')
        circuit_name = entities['circuits'][0] if entities['circuits'] else None
        
        # Buscar sesiones
        sessions = self.network.find_nodes_by_type('sesion')
        
        # Filtrar por año si se especifica
        if year:
            sessions = [s for s in sessions if s['attributes'].get('year') == year]
        
        return {
            'found': len(sessions) > 0,
            'sessions': sessions[:10],  # Limitar a 10
            'count': len(sessions),
            'related_entities': [],
            'metadata': {'year': year, 'total_sessions': len(sessions)}
        }
    
    def _query_general(self, entities: Dict, filters: Dict) -> Dict[str, Any]:
        """Consulta general cuando no se detecta un tipo específico"""
        logger.debug("Ejecutando consulta general")
        
        # Buscar cualquier entidad mencionada
        all_entities = []
        pilot_info = None
        team_info = None
        
        # Si hay pilotos, intentar obtener su información completa
        if entities['drivers']:
            for driver_name in entities['drivers']:
                pilots = self.network.find_nodes_by_type('piloto', {'nombre': driver_name})
                if pilots:
                    pilot_node = pilots[0]
                    all_entities.append(pilot_node)
                    
                    # Obtener equipo del piloto
                    team_nodes = self.network.query_by_relation(
                        pilot_node['id'],
                        'conduce_para',
                        direction='outgoing'
                    )
                    
                    if team_nodes:
                        team_info = team_nodes[0]
                        all_entities.append(team_info)
                    
                    pilot_info = {
                        'pilot': pilot_node,
                        'team': team_nodes[0] if team_nodes else None
                    }
        
        if entities['teams']:
            for team_name in entities['teams']:
                teams = self.network.find_nodes_by_type('equipo', {'nombre_equipo': team_name})
                all_entities.extend(teams)
        
        if entities['circuits']:
            for circuit_name in entities['circuits']:
                circuits = self.network.find_nodes_by_type('circuito', {'nombre_oficial': circuit_name})
                all_entities.extend(circuits)
        
        # Preparar entidades relacionadas
        related_entities = []
        for e in all_entities[:5]:
            entity_data = {
                'type': e['type'],
                'id': e['id']
            }
            
            # Extraer el nombre apropiado según el tipo
            if e['type'] == 'piloto':
                entity_data['name'] = e['attributes'].get('nombre', 'Desconocido')
            elif e['type'] == 'equipo':
                entity_data['name'] = e['attributes'].get('nombre_equipo', 'Desconocido')
            elif e['type'] == 'circuito':
                entity_data['name'] = e['attributes'].get('nombre_oficial', 'Desconocido')
            else:
                entity_data['name'] = str(e['attributes'])
            
            related_entities.append(entity_data)
        
        return {
            'found': len(all_entities) > 0,
            'entities': all_entities,
            'pilot_info': pilot_info,
            'team_info': team_info,
            'related_entities': related_entities,
            'metadata': {}
        }
    
    def _calculate_confidence(self, results: Dict, intent: Dict) -> float:
        """
        Calcula el nivel de confianza de la respuesta
        
        Args:
            results: Resultados de la consulta
            intent: Intención extraída
            
        Returns:
            Valor entre 0.0 y 1.0
        """
        confidence = 0.5  # Base
        
        # Aumentar si se encontraron resultados
        if results.get('found'):
            confidence += 0.3
        
        # Aumentar si hay entidades relacionadas
        if results.get('related_entities'):
            confidence += 0.1 * min(len(results['related_entities']), 2)
        
        # Aumentar si hay metadata
        if results.get('metadata'):
            confidence += 0.1
        
        # Limitar a 1.0
        confidence = min(confidence, 1.0)
        
        return round(confidence, 2)
    
    def _format_answer(
        self, 
        results: Dict, 
        query_type: str, 
        entities: Dict
    ) -> str:
        """
        Formatea la respuesta en lenguaje natural
        
        Args:
            results: Resultados de la consulta
            query_type: Tipo de consulta
            entities: Entidades extraídas
            
        Returns:
            Respuesta formateada en español
        """
        if not results.get('found'):
            return results.get('message', 'No se encontró información sobre tu pregunta.')
        
        # Formatear según el tipo de consulta
        if query_type == 'pilot_info':
            pilot = results['pilot']
            team = results.get('team')
            name = pilot['attributes']['nombre']
            nationality = pilot['attributes'].get('nacionalidad', 'Desconocida')
            number = pilot['attributes'].get('numero_piloto', '')
            
            answer = f"{name} es un piloto de Fórmula 1 de nacionalidad {nationality}"
            if number:
                answer += f" con el número {number}"
            if team:
                team_name = team['attributes']['nombre_equipo']
                answer += f". Actualmente corre para {team_name}"
            answer += "."
            return answer
        
        elif query_type == 'team_info':
            team = results['team']
            pilot = results['pilot']
            team_name = team['attributes']['nombre_equipo']
            pilot_name = pilot['attributes']['nombre']
            
            return f"{pilot_name} corre para {team_name}."
        
        elif query_type == 'motor_info':
            team = results['team']
            motor = results['motor']
            team_name = team['attributes']['nombre_equipo']
            motor_name = motor['attributes']['fabricante']
            
            return f"{team_name} utiliza motores {motor_name}."
        
        elif query_type == 'circuit_info':
            circuit = results['circuit']
            country = results.get('country')
            circuit_name = circuit['attributes']['nombre_oficial']
            
            if country:
                country_name = country['attributes']['nombre']
                return f"El {circuit_name} está ubicado en {country_name}."
            else:
                return f"Se encontró información sobre {circuit_name}."
        
        elif query_type == 'session_info':
            count = results.get('count', 0)
            year = results.get('metadata', {}).get('year', '')
            
            if year:
                return f"Se encontraron {count} sesiones para el año {year}."
            else:
                return f"Se encontraron {count} sesiones en la base de datos."
        
        else:
            # Respuesta general - intentar dar información útil
            pilot_info = results.get('pilot_info')
            team_info = results.get('team_info')
            
            # Si hay información de piloto, mostrarla
            if pilot_info and pilot_info.get('pilot'):
                pilot = pilot_info['pilot']
                team = pilot_info.get('team')
                name = pilot['attributes'].get('nombre', 'Desconocido')
                nationality = pilot['attributes'].get('nacionalidad', 'Desconocida')
                number = pilot['attributes'].get('numero_piloto', '')
                
                answer = f"{name} es un piloto de Fórmula 1"
                if nationality != 'Desconocida':
                    answer += f" de nacionalidad {nationality}"
                if number:
                    answer += f" con el número {number}"
                if team:
                    team_name = team['attributes'].get('nombre_equipo', 'Desconocido')
                    answer += f". Actualmente corre para {team_name}"
                answer += "."
                return answer
            
            # Si solo hay entidades, dar respuesta genérica
            entities_found = results.get('entities', [])
            if entities_found:
                count = len(entities_found)
                return f"Se encontraron {count} entidades relacionadas con tu pregunta."
            else:
                return "Se encontró información sobre tu consulta."

