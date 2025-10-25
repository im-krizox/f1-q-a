"""
Funciones de utilidad y helpers
"""
from typing import Any, Dict, List
import re
from datetime import datetime


def normalize_name(name: str) -> str:
    """
    Normaliza un nombre para usar como identificador
    
    Args:
        name: Nombre a normalizar
        
    Returns:
        Nombre normalizado
    """
    return re.sub(r'[^\w\s]', '', name.lower()).replace(' ', '_')


def format_date(date_str: str) -> str:
    """
    Formatea una fecha ISO a formato legible
    
    Args:
        date_str: Fecha en formato ISO
        
    Returns:
        Fecha formateada
    """
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime('%d/%m/%Y %H:%M')
    except:
        return date_str


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Trunca texto a una longitud máxima
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        
    Returns:
        Texto truncado
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'


def clean_dict(data: Dict[str, Any], remove_none: bool = True) -> Dict[str, Any]:
    """
    Limpia un diccionario removiendo valores None o vacíos
    
    Args:
        data: Diccionario a limpiar
        remove_none: Si remover valores None
        
    Returns:
        Diccionario limpio
    """
    cleaned = {}
    for key, value in data.items():
        if remove_none and value is None:
            continue
        if isinstance(value, str) and len(value) == 0:
            continue
        cleaned[key] = value
    return cleaned


def merge_dicts(*dicts: Dict) -> Dict:
    """
    Combina múltiples diccionarios
    
    Args:
        *dicts: Diccionarios a combinar
        
    Returns:
        Diccionario combinado
    """
    result = {}
    for d in dicts:
        result.update(d)
    return result


def flatten_list(nested_list: List[List[Any]]) -> List[Any]:
    """
    Aplana una lista anidada
    
    Args:
        nested_list: Lista anidada
        
    Returns:
        Lista aplanada
    """
    return [item for sublist in nested_list for item in sublist]


def deduplicate_list(items: List[Any], key: str = None) -> List[Any]:
    """
    Elimina duplicados de una lista
    
    Args:
        items: Lista de items
        key: Clave para comparación (si items son diccionarios)
        
    Returns:
        Lista sin duplicados
    """
    if not items:
        return []
    
    if key and isinstance(items[0], dict):
        seen = set()
        unique_items = []
        for item in items:
            value = item.get(key)
            if value not in seen:
                seen.add(value)
                unique_items.append(item)
        return unique_items
    else:
        return list(set(items))

