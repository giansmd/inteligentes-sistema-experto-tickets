"""
Pruebas automatizadas del Sistema Experto
[gians] Aquí probamos que las reglas funcionen correctamente
"""

import pytest
import sys
import os

# [gians] Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.inference_engine import MotorInferencia
from knowledge.rules import clasificar_ticket_simple


class TestMotorInferencia:
    """Pruebas del motor de inferencia"""
    
    def setup_method(self):
        """Configurar antes de cada test"""
        # [gians] Crear un motor nuevo para cada prueba
        self.motor = MotorInferencia()
    
    def test_motor_inicializa_correctamente(self):
        """Probar que el motor se inicializa bien"""
        assert self.motor.tickets_procesados == 0
        assert len(self.motor.historial) == 0
    
    def test_procesar_ticket_vacio_da_error(self):
        """Probar que un ticket vacío da error"""
        resultado = self.motor.procesar_ticket("")
        assert "error" in resultado
        assert resultado["categoria"] is None
    
    def test_procesar_ticket_incrementa_contador(self):
        """Probar que procesar tickets incrementa el contador"""
        self.motor.procesar_ticket("Mi computadora no funciona")
        assert self.motor.tickets_procesados == 1
        
        self.motor.procesar_ticket("El internet está lento")
        assert self.motor.tickets_procesados == 2
    
    def test_obtener_estadisticas_vacio(self):
        """Probar estadísticas cuando no hay tickets"""
        stats = self.motor.obtener_estadisticas()
        assert stats["total"] == 0
        assert stats["por_categoria"] == {}
    
    def test_limpiar_historial(self):
        """Probar que limpiar historial funciona"""
        self.motor.procesar_ticket("Test ticket")
        assert self.motor.tickets_procesados == 1
        
        self.motor.limpiar_historial()
        assert self.motor.tickets_procesados == 0
        assert len(self.motor.historial) == 0


class TestReglas:
    """Pruebas de las reglas de clasificación"""
    
    def test_clasificar_hardware_urgente(self):
        """Probar clasificación de hardware urgente"""
        texto = "URGENTE: Mi computadora no enciende"
        resultado = clasificar_ticket_simple(texto)
        
        assert resultado["categoria"] == "hardware"
        assert resultado["tipo"] == "incidencia"
        assert resultado["prioridad"] == "alta"
    
    def test_clasificar_software_normal(self):
        """Probar clasificación de software normal"""
        texto = "Tengo un problema con Excel, no abre archivos"
        resultado = clasificar_ticket_simple(texto)
        
        assert resultado["categoria"] == "software"
        assert resultado["tipo"] == "incidencia"
    
    def test_clasificar_redes_urgente(self):
        """Probar clasificación de redes urgente"""
        texto = "No hay internet en la oficina, es urgente"
        resultado = clasificar_ticket_simple(texto)
        
        assert resultado["categoria"] == "redes"
        assert resultado["prioridad"] == "alta"
    
    def test_clasificar_seguridad_critica(self):
        """Probar clasificación de seguridad crítica"""
        texto = "Creo que tengo un virus, es urgente"
        resultado = clasificar_ticket_simple(texto)
        
        assert resultado["categoria"] == "seguridad"
        assert resultado["prioridad"] == "alta"
    
    def test_clasificar_solicitud_software(self):
        """Probar clasificación de solicitud de software"""
        texto = "Me gustaría saber cómo instalar Office"
        resultado = clasificar_ticket_simple(texto)
        
        assert resultado["categoria"] == "software"
        assert resultado["tipo"] == "solicitud"
        assert resultado["prioridad"] == "baja"
    
    def test_clasificar_solicitud_hardware(self):
        """Probar clasificación de solicitud de hardware"""
        texto = "Necesito un mouse nuevo por favor"
        resultado = clasificar_ticket_simple(texto)
        
        assert resultado["categoria"] == "hardware"
        assert resultado["tipo"] == "solicitud"
    
    def test_resultado_tiene_accion(self):
        """Probar que siempre se genera una acción"""
        texto = "Mi computadora está lenta"
        resultado = clasificar_ticket_simple(texto)
        
        assert "accion" in resultado
        assert resultado["accion"] != ""
    
    def test_resultado_tiene_conteos(self):
        """Probar que se incluyen conteos de palabras"""
        texto = "La impresora no funciona"
        resultado = clasificar_ticket_simple(texto)
        
        assert "conteos" in resultado
        assert isinstance(resultado["conteos"], dict)
        assert resultado["conteos"]["hardware"] > 0


class TestIntegracion:
    """Pruebas de integración del sistema completo"""
    
    def test_flujo_completo_ticket(self):
        """Probar el flujo completo de procesamiento"""
        motor = MotorInferencia()
        
        # Procesar ticket
        resultado = motor.procesar_ticket(
            "URGENTE: Mi PC no enciende",
            "TKT-001"
        )
        
        # Verificar resultado
        assert resultado["id_ticket"] == "TKT-001"
        assert resultado["categoria"] == "hardware"
        assert resultado["prioridad"] == "alta"
        assert "accion" in resultado
        
        # Verificar estadísticas
        stats = motor.obtener_estadisticas()
        assert stats["total"] == 1
        assert "hardware" in stats["por_categoria"]
    
    def test_multiples_tickets(self):
        """Probar procesar múltiples tickets"""
        motor = MotorInferencia()
        
        tickets = [
            "Mi computadora no funciona",
            "El internet está lento",
            "Necesito instalar Office"
        ]
        
        for ticket in tickets:
            motor.procesar_ticket(ticket)
        
        stats = motor.obtener_estadisticas()
        assert stats["total"] == 3


# [gians] Ejecutar pruebas si se corre directamente este archivo
if __name__ == "__main__":
    pytest.main([__file__, "-v"])