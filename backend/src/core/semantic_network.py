"""
Red Semántica usando NetworkX
"""
import networkx as nx
import logging
from typing import Dict, List, Optional, Any
from collections import defaultdict

logger = logging.getLogger(__name__)


class SemanticNetwork:
    """Red semántica para almacenar y consultar conocimiento sobre F1"""
    
    def __init__(self):
        """Inicializa la red semántica con un grafo dirigido múltiple"""
        self.graph = nx.MultiDiGraph()
        self.nodes_by_type: Dict[str, List[str]] = defaultdict(list)
        logger.info("Red semántica inicializada")
    
    def add_node(
        self, 
        node_id: str, 
        node_type: str, 
        attributes: Dict[str, Any]
    ) -> None:
        """
        Agrega un nodo a la red semántica
        
        Args:
            node_id: Identificador único del nodo
            node_type: Tipo del nodo (piloto, equipo, motor, circuito, sesion, etc.)
            attributes: Diccionario con los atributos del nodo
        """
        self.graph.add_node(
            node_id,
            node_type=node_type,
            **attributes
        )
        
        # Indexar por tipo para búsquedas rápidas
        if node_id not in self.nodes_by_type[node_type]:
            self.nodes_by_type[node_type].append(node_id)
        
        logger.debug(f"Nodo agregado: {node_id} (tipo: {node_type})")
    
    def add_edge(
        self, 
        source: str, 
        target: str, 
        relation: str, 
        attributes: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Agrega una arista (relación) entre dos nodos
        
        Args:
            source: ID del nodo origen
            target: ID del nodo destino
            relation: Tipo de relación
            attributes: Atributos opcionales de la relación
        """
        if attributes is None:
            attributes = {}
        
        # Verificar que ambos nodos existen
        if source not in self.graph:
            logger.warning(f"Nodo origen '{source}' no existe en el grafo")
            return
        
        if target not in self.graph:
            logger.warning(f"Nodo destino '{target}' no existe en el grafo")
            return
        
        self.graph.add_edge(
            source,
            target,
            relation=relation,
            **attributes
        )
        
        logger.debug(f"Arista agregada: {source} --[{relation}]--> {target}")
    
    def query_by_relation(
        self, 
        node_id: str, 
        relation: str, 
        direction: str = "outgoing"
    ) -> List[Dict[str, Any]]:
        """
        Busca nodos conectados por una relación específica
        
        Args:
            node_id: ID del nodo desde el cual buscar
            relation: Tipo de relación a buscar
            direction: "outgoing" (salientes) o "incoming" (entrantes)
            
        Returns:
            Lista de diccionarios con información de los nodos relacionados
        """
        if node_id not in self.graph:
            logger.warning(f"Nodo '{node_id}' no existe en el grafo")
            return []
        
        related_nodes = []
        
        if direction == "outgoing":
            # Buscar aristas salientes
            for _, target, data in self.graph.out_edges(node_id, data=True):
                if data.get('relation') == relation:
                    node_data = self.get_node_details(target)
                    if node_data:
                        related_nodes.append(node_data)
        
        elif direction == "incoming":
            # Buscar aristas entrantes
            for source, _, data in self.graph.in_edges(node_id, data=True):
                if data.get('relation') == relation:
                    node_data = self.get_node_details(source)
                    if node_data:
                        related_nodes.append(node_data)
        
        logger.debug(f"Encontrados {len(related_nodes)} nodos con relación '{relation}' ({direction})")
        return related_nodes
    
    def find_nodes_by_type(
        self, 
        node_type: str, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca todos los nodos de un tipo específico
        
        Args:
            node_type: Tipo de nodo a buscar
            filters: Filtros opcionales para aplicar a los atributos
            
        Returns:
            Lista de diccionarios con información de los nodos
        """
        node_ids = self.nodes_by_type.get(node_type, [])
        results = []
        
        for node_id in node_ids:
            node_data = self.get_node_details(node_id)
            if not node_data:
                continue
            
            # Aplicar filtros si existen
            if filters:
                match = True
                for key, value in filters.items():
                    node_value = node_data.get('attributes', {}).get(key)
                    if node_value is None:
                        match = False
                        break
                    
                    # Comparación flexible (case-insensitive para strings)
                    if isinstance(value, str) and isinstance(node_value, str):
                        if value.lower() not in node_value.lower():
                            match = False
                            break
                    elif node_value != value:
                        match = False
                        break
                
                if match:
                    results.append(node_data)
            else:
                results.append(node_data)
        
        logger.debug(f"Encontrados {len(results)} nodos de tipo '{node_type}'")
        return results
    
    def get_node_details(self, node_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene todos los detalles de un nodo
        
        Args:
            node_id: ID del nodo
            
        Returns:
            Diccionario con información del nodo o None si no existe
        """
        if node_id not in self.graph:
            return None
        
        node_attrs = dict(self.graph.nodes[node_id])
        node_type = node_attrs.pop('node_type', 'unknown')
        
        # Obtener relaciones salientes
        outgoing = []
        for _, target, data in self.graph.out_edges(node_id, data=True):
            outgoing.append({
                'target': target,
                'relation': data.get('relation', 'unknown'),
                'attributes': {k: v for k, v in data.items() if k != 'relation'}
            })
        
        # Obtener relaciones entrantes
        incoming = []
        for source, _, data in self.graph.in_edges(node_id, data=True):
            incoming.append({
                'source': source,
                'relation': data.get('relation', 'unknown'),
                'attributes': {k: v for k, v in data.items() if k != 'relation'}
            })
        
        return {
            'id': node_id,
            'type': node_type,
            'attributes': node_attrs,
            'outgoing_relations': outgoing,
            'incoming_relations': incoming
        }
    
    def find_path(
        self, 
        source: str, 
        target: str, 
        max_length: int = 5
    ) -> List[List[str]]:
        """
        Encuentra caminos entre dos nodos
        
        Args:
            source: Nodo origen
            target: Nodo destino
            max_length: Longitud máxima del camino
            
        Returns:
            Lista de caminos (cada camino es una lista de IDs de nodos)
        """
        if source not in self.graph or target not in self.graph:
            logger.warning(f"Uno o ambos nodos no existen: {source}, {target}")
            return []
        
        try:
            paths = list(nx.all_simple_paths(
                self.graph, 
                source, 
                target, 
                cutoff=max_length
            ))
            logger.debug(f"Encontrados {len(paths)} caminos entre {source} y {target}")
            return paths
        except nx.NetworkXNoPath:
            logger.debug(f"No hay camino entre {source} y {target}")
            return []
    
    def get_related_entities(
        self, 
        node_id: str, 
        max_depth: int = 2
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Explora el vecindario de un nodo hasta una profundidad máxima
        
        Args:
            node_id: ID del nodo central
            max_depth: Profundidad máxima de exploración
            
        Returns:
            Diccionario con entidades relacionadas agrupadas por tipo
        """
        if node_id not in self.graph:
            logger.warning(f"Nodo '{node_id}' no existe")
            return {}
        
        # Usar BFS para explorar vecindario
        visited = {node_id}
        current_level = {node_id}
        entities_by_type: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        
        for depth in range(max_depth):
            next_level = set()
            
            for current_node in current_level:
                # Nodos sucesores
                for neighbor in self.graph.successors(current_node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_level.add(neighbor)
                        node_data = self.get_node_details(neighbor)
                        if node_data:
                            node_type = node_data['type']
                            entities_by_type[node_type].append(node_data)
                
                # Nodos predecesores
                for neighbor in self.graph.predecessors(current_node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_level.add(neighbor)
                        node_data = self.get_node_details(neighbor)
                        if node_data:
                            node_type = node_data['type']
                            entities_by_type[node_type].append(node_data)
            
            current_level = next_level
            
            if not current_level:
                break
        
        # Convertir defaultdict a dict normal
        result = dict(entities_by_type)
        logger.debug(f"Encontradas {len(visited)-1} entidades relacionadas con {node_id}")
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de la red semántica
        
        Returns:
            Diccionario con estadísticas
        """
        stats = {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'nodes_by_type': {k: len(v) for k, v in self.nodes_by_type.items()}
        }
        
        logger.info(f"Estadísticas de red: {stats}")
        return stats

