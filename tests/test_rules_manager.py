# tests/test_rules_manager.py
# Script de prueba para el gestor de reglas

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.rules_manager import RulesManager
from engine.classification_engine import TicketClassificationEngine
from engine.ticket_fact import Ticket

def test_rules_manager():
    """Prueba las funcionalidades del gestor de reglas"""
    
    print("=" * 60)
    print("PRUEBAS DEL GESTOR DE REGLAS")
    print("=" * 60)
    
    # Crear instancia
    manager = RulesManager()
    
    # Test 1: Cargar reglas
    print("\n1. Cargando reglas existentes...")
    reglas = manager.get_all_rules()
    print(f"   ✓ Se cargaron {len(reglas)} reglas")
    
    # Test 2: Mostrar reglas activas
    print("\n2. Reglas activas:")
    activas = manager.get_active_rules()
    for regla in activas:
        print(f"   - {regla['id_regla']}: {regla['nombre']} ({regla['tipo']} - {regla['prioridad']})")
    
    # Test 3: Agregar nueva regla
    print("\n3. Agregando nueva regla de prueba...")
    resultado = manager.add_rule(
        nombre="Problemas de Audio TEST",
        palabras_clave=["audio", "sonido", "audífono", "parlante", "altavoz"],
        tipo="HARDWARE",
        prioridad="Media",
        asignado_a="Equipo de Hardware - Audio"
    )
    
    if resultado:
        print("   ✓ Regla agregada exitosamente")
        # Recargar reglas
        manager.load_rules()
        print(f"   ✓ Ahora hay {len(manager.get_all_rules())} reglas")
    else:
        print("   ✗ Error al agregar regla")
    
    # Test 4: Buscar regla por ID
    print("\n4. Buscando regla recién creada...")
    reglas = manager.get_all_rules()
    ultima_regla = reglas[-1] if reglas else None
    if ultima_regla:
        print(f"   ✓ Encontrada: {ultima_regla['id_regla']} - {ultima_regla['nombre']}")
        id_test = ultima_regla['id_regla']
    
    # Test 5: Desactivar regla
    if ultima_regla:
        print(f"\n5. Desactivando regla {id_test}...")
        if manager.toggle_rule_status(id_test):
            print("   ✓ Regla desactivada")
            manager.load_rules()
            regla_modificada = manager.get_rule_by_id(id_test)
            print(f"   ✓ Estado: {'Activa' if regla_modificada['activa'] else 'Inactiva'}")
    
    # Test 6: Actualizar regla
    if ultima_regla:
        print(f"\n6. Actualizando regla {id_test}...")
        if manager.update_rule(
            id_regla=id_test,
            nombre="Problemas de Audio TEST ACTUALIZADO",
            prioridad="Alta"
        ):
            print("   ✓ Regla actualizada")
            manager.load_rules()
            regla_actualizada = manager.get_rule_by_id(id_test)
            print(f"   ✓ Nuevo nombre: {regla_actualizada['nombre']}")
            print(f"   ✓ Nueva prioridad: {regla_actualizada['prioridad']}")
    
    # Test 7: Estadísticas
    print("\n7. Estadísticas del sistema:")
    stats = manager.get_statistics()
    print(f"   - Total: {stats['total']}")
    print(f"   - Activas: {stats['activas']}")
    print(f"   - Inactivas: {stats['inactivas']}")
    print(f"   - Por tipo: {stats['por_tipo']}")
    print(f"   - Por prioridad: {stats['por_prioridad']}")
    
    # Test 8: Eliminar regla de prueba
    if ultima_regla:
        print(f"\n8. Eliminando regla de prueba {id_test}...")
        if manager.delete_rule(id_test):
            print("   ✓ Regla eliminada exitosamente")
            manager.load_rules()
            print(f"   ✓ Ahora hay {len(manager.get_all_rules())} reglas")
    
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)


def test_classification_with_custom_rules():
    """Prueba el motor de clasificación con reglas personalizadas"""
    
    print("\n" + "=" * 60)
    print("PRUEBA DE CLASIFICACIÓN CON REGLAS PERSONALIZADAS")
    print("=" * 60)
    
    # Crear motor
    motor = TicketClassificationEngine()
    
    # Test 1: Ticket que coincide con regla personalizada
    print("\n1. Probando ticket que coincide con regla personalizada (impresora)...")
    motor.reset()
    motor.reset_resultados()
    motor.declare(Ticket(
        id_ticket="TEST001",
        contenido="La impresora no está funcionando, necesito cambiar el toner",
        cliente="Usuario Test",
        area="Área Test",
        fecha="2025-11-01"
    ))
    motor.run()
    
    if motor.resultados:
        resultado = motor.resultados[0]
        print(f"   ✓ Clasificado como: {resultado['tipo']}")
        print(f"   ✓ Prioridad: {resultado['prioridad']}")
        print(f"   ✓ Asignado a: {resultado['asignado_a']}")
        print(f"   ✓ Regla aplicada: {resultado['regla']}")
    
    # Test 2: Ticket que coincide con regla personalizada de red
    print("\n2. Probando ticket que coincide con regla personalizada (red)...")
    motor.reset()
    motor.reset_resultados()
    motor.declare(Ticket(
        id_ticket="TEST002",
        contenido="No tengo conexión a internet, el wifi no funciona",
        cliente="Usuario Test 2",
        area="Área Test",
        fecha="2025-11-01"
    ))
    motor.run()
    
    if motor.resultados:
        resultado = motor.resultados[0]
        print(f"   ✓ Clasificado como: {resultado['tipo']}")
        print(f"   ✓ Prioridad: {resultado['prioridad']}")
        print(f"   ✓ Asignado a: {resultado['asignado_a']}")
        print(f"   ✓ Regla aplicada: {resultado['regla']}")
    
    # Test 3: Ticket que NO coincide con reglas personalizadas (usa hardcoded)
    print("\n3. Probando ticket que usa regla hardcodeada (virus)...")
    motor.reset()
    motor.reset_resultados()
    motor.declare(Ticket(
        id_ticket="TEST003",
        contenido="Creo que mi computadora tiene un virus",
        cliente="Usuario Test 3",
        area="Área Test",
        fecha="2025-11-01"
    ))
    motor.run()
    
    if motor.resultados:
        resultado = motor.resultados[0]
        print(f"   ✓ Clasificado como: {resultado['tipo']}")
        print(f"   ✓ Prioridad: {resultado['prioridad']}")
        print(f"   ✓ Asignado a: {resultado['asignado_a']}")
        print(f"   ✓ Regla aplicada: {resultado['regla']}")
    
    # Test 4: Ticket que coincide con regla de licencias
    print("\n4. Probando ticket que coincide con regla personalizada (licencia)...")
    motor.reset()
    motor.reset_resultados()
    motor.declare(Ticket(
        id_ticket="TEST004",
        contenido="Mi licencia de Office está vencida, necesito activación",
        cliente="Usuario Test 4",
        area="Área Test",
        fecha="2025-11-01"
    ))
    motor.run()
    
    if motor.resultados:
        resultado = motor.resultados[0]
        print(f"   ✓ Clasificado como: {resultado['tipo']}")
        print(f"   ✓ Prioridad: {resultado['prioridad']}")
        print(f"   ✓ Asignado a: {resultado['asignado_a']}")
        print(f"   ✓ Regla aplicada: {resultado['regla']}")
    
    print("\n" + "=" * 60)
    print("PRUEBAS DE CLASIFICACIÓN COMPLETADAS")
    print("=" * 60)


if __name__ == "__main__":
    # Ejecutar pruebas
    test_rules_manager()
    test_classification_with_custom_rules()
    
    print("\n✅ TODAS LAS PRUEBAS COMPLETADAS")
