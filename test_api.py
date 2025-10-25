#!/usr/bin/env python3
"""
Script de prueba para el API de F1 Q&A
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Imprime un título de sección"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """Prueba el endpoint de health"""
    print_section("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_stats():
    """Prueba el endpoint de estadísticas"""
    print_section("2. Estadísticas de la Red")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/stats")
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_question(question):
    """Prueba una pregunta"""
    print(f"\n💬 Pregunta: {question}")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/ask",
            json={"question": question},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📝 Respuesta: {data['answer']}")
            print(f"🎯 Confianza: {data['confidence']}")
            print(f"🔍 Tipo: {data['query_type']}")
            if data['related_entities']:
                print(f"🔗 Entidades relacionadas:")
                for entity in data['related_entities']:
                    print(f"   - {entity['type']}: {entity['name']}")
        else:
            print(f"❌ Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_entities(entity_type):
    """Prueba listar entidades"""
    print(f"\n📋 Listando {entity_type}...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/entities/{entity_type}?limit=5")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total: {data['count']}")
            for entity in data['entities'][:3]:
                print(f"  - {entity['id']}: {entity['attributes']}")
        else:
            print(f"❌ Error: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("\n🏎️  F1 Q&A System - Test Suite")
    print("="*60)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health()))
    
    # Test 2: Estadísticas
    results.append(("Estadísticas", test_stats()))
    
    # Test 3: Preguntas
    print_section("3. Preguntas de Prueba")
    
    questions = [
        "¿Quién es Max Verstappen?",
        "¿Para qué equipo corre Lewis Hamilton?",
        "¿Qué motor usa Red Bull?",
        "¿Dónde está el circuito de Spa?",
    ]
    
    for question in questions:
        results.append((f"Pregunta: {question}", test_question(question)))
    
    # Test 4: Entidades
    print_section("4. Listar Entidades")
    results.append(("Listar pilotos", test_entities("drivers")))
    results.append(("Listar equipos", test_entities("teams")))
    
    # Resumen
    print_section("Resumen de Pruebas")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n✅ Pasadas: {passed}/{total}")
    print(f"❌ Fallidas: {total - passed}/{total}")
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    print("\n" + "="*60)
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron!")
        return 0
    else:
        print("⚠️  Algunas pruebas fallaron")
        return 1

if __name__ == "__main__":
    sys.exit(main())

