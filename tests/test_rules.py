# tests/test_rules.py
# Pruebas unitarias para las 10 reglas del sistema experto

# Parche para compatibilidad con Python 3.12
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping

import pytest
from engine.classification_engine import TicketClassificationEngine
from engine.ticket_fact import Ticket

def test_regla_impresora():
    """Prueba para regla de problemas con impresora"""
    motor = TicketClassificationEngine()
    motor.reset()
    
    # Crear ticket con problema de impresora
    motor.declare(Ticket(
        id_ticket="TEST001",
        contenido="mi impresora no funciona",
        cliente="Test User",
        area="Test Area",
        fecha="2025-10-28"
    ))
    
    # Ejecutar motor
    motor.run()
    
    # Verificar resultado
    assert len(motor.resultados) > 0
    assert motor.resultados[0]['tipo'] == 'EQUIPOS DE IMPRESIÓN/ESCÁNER'
    assert motor.resultados[0]['prioridad'] == 'Media'
    print("✅ Test regla impresora: PASÓ")

def test_regla_red():
    """Prueba para regla de problemas de red"""
    motor = TicketClassificationEngine()
    motor.reset()
    
    motor.declare(Ticket(
        id_ticket="TEST002",
        contenido="no tengo internet",
        cliente="Test User",
        area="Test Area",
        fecha="2025-10-28"
    ))
    
    motor.run()
    
    assert len(motor.resultados) > 0
    assert motor.resultados[0]['tipo'] == 'PC/LAPTOP'
    assert motor.resultados[0]['prioridad'] == 'Alta'
    print("✅ Test regla red: PASÓ")

def test_regla_instalacion_software():
    """Prueba para regla de instalación de software"""
    motor = TicketClassificationEngine()
    motor.reset()
    
    motor.declare(Ticket(
        id_ticket="TEST003",
        contenido="necesito instalar un programa",
        cliente="Test User",
        area="Test Area",
        fecha="2025-10-28"
    ))
    
    motor.run()
    
    assert len(motor.resultados) > 0
    assert motor.resultados[0]['prioridad'] == 'Baja'
    print("✅ Test regla instalación software: PASÓ")

def test_regla_sistema_corporativo():
    """Prueba para regla de sistemas corporativos"""
    motor = TicketClassificationEngine()
    motor.reset()
    
    motor.declare(Ticket(
        id_ticket="TEST004",
        contenido="el sistema SIGA no funciona",
        cliente="Test User",
        area="Test Area",
        fecha="2025-10-28"
    ))
    
    motor.run()
    
    assert len(motor.resultados) > 0
    assert motor.resultados[0]['tipo'] == 'SISTEMA'
    assert motor.resultados[0]['prioridad'] == 'Alta'
    print("✅ Test regla sistema corporativo: PASÓ")

def test_regla_contrasena():
    """Prueba para regla de problemas de contraseña"""
    motor = TicketClassificationEngine()
    motor.reset()
    
    motor.declare(Ticket(
        id_ticket="TEST005",
        contenido="mi contraseña está bloqueada",
        cliente="Test User",
        area="Test Area",
        fecha="2025-10-28"
    ))
    
    motor.run()
    
    assert len(motor.resultados) > 0
    assert motor.resultados[0]['prioridad'] == 'Media'
    print("✅ Test regla contraseña: PASÓ")

def test_regla_equipo_no_enciende():
    """Prueba para regla de equipo que no enciende"""
    motor = TicketClassificationEngine()
    motor.reset()
    
    motor.declare(Ticket(
        id_ticket="TEST006",
        contenido="mi laptop no enciende",
        cliente="Test User",
        area="Test Area",
        fecha="2025-10-28"
    ))
    
    motor.run()
    
    assert len(motor.resultados) > 0
    assert motor.resultados[0]['prioridad'] == 'Alta'
    print("✅ Test regla equipo no enciende: PASÓ")

def test_regla_correo():
    """Prueba para regla de problemas de correo"""
    motor = TicketClassificationEngine()
    motor.reset()
    
    motor.declare(Ticket(
        id_ticket="TEST007",
        contenido="no puedo acceder a mi correo",
        cliente="Test User",
        area="Test Area",
        fecha="2025-10-28"
    ))
    
    motor.run()
    
    assert len(motor.resultados) > 0
    assert motor.resultados[0]['tipo'] == 'SISTEMA'
    print("✅ Test regla correo: PASÓ")

def test_regla_asesoria():
    """Prueba para regla de asesoría general"""
    motor = TicketClassificationEngine()
    motor.reset()
    
    motor.declare(Ticket(
        id_ticket="TEST008",
        contenido="necesito ayuda con algo",
        cliente="Test User",
        area="Test Area",
        fecha="2025-10-28"
    ))
    
    motor.run()
    
    assert len(motor.resultados) > 0
    assert motor.resultados[0]['tipo'] == 'GENERAL'
    print("✅ Test regla asesoría: PASÓ")

def test_regla_equipo_lento():
    """Prueba para regla de equipo lento"""
    motor = TicketClassificationEngine()
    motor.reset()
    
    motor.declare(Ticket(
        id_ticket="TEST009",
        contenido="mi computadora está muy lenta",
        cliente="Test User",
        area="Test Area",
        fecha="2025-10-28"
    ))
    
    motor.run()
    
    assert len(motor.resultados) > 0
    assert motor.resultados[0]['prioridad'] == 'Media'
    print("✅ Test regla equipo lento: PASÓ")

def test_regla_habilitacion():
    """Prueba para regla de habilitaciones"""
    motor = TicketClassificationEngine()
    motor.reset()
    
    motor.declare(Ticket(
        id_ticket="TEST010",
        contenido="necesito habilitar mi cuenta",
        cliente="Test User",
        area="Test Area",
        fecha="2025-10-28"
    ))
    
    motor.run()
    
    assert len(motor.resultados) > 0
    assert motor.resultados[0]['tipo'] == 'GENERAL'
    print("✅ Test regla habilitación: PASÓ")

# Ejecutar todas las pruebas
if __name__ == "__main__":
    print("\n🧪 Ejecutando pruebas del sistema experto...\n")
    
    test_regla_impresora()
    test_regla_red()
    test_regla_instalacion_software()
    test_regla_sistema_corporativo()
    test_regla_contrasena()
    test_regla_equipo_no_enciende()
    test_regla_correo()
    test_regla_asesoria()
    test_regla_equipo_lento()
    test_regla_habilitacion()
    
    print("\n✨ ¡Todas las pruebas pasaron exitosamente!")