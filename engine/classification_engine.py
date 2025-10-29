# engine/classification_engine.py
# Motor de inferencia - aquí van las reglas del sistema experto

# Parche para compatibilidad con Python 3.12
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping

from experta import KnowledgeEngine, Rule
from engine.ticket_fact import Ticket

class TicketClassificationEngine(KnowledgeEngine):
    """
    Motor de clasificación de tickets usando encadenamiento hacia adelante.
    Cada regla evalúa los atributos del ticket y asigna categoría, prioridad y equipo.
    """
    
    def __init__(self):
        super().__init__()
        self.resultados = []  # Aquí guardamos los resultados de cada ticket
    
    @Rule(Ticket())
    def clasificar_ticket(self):
        """
        Regla principal que se activa cuando se declara un Ticket.
        Evalúa el contenido y aplica la clasificación correspondiente.
        """
        # Buscar el ticket en los facts
        contenido = ""
        for fact in self.facts.values():
            if isinstance(fact, Ticket):
                contenido = str(fact.get('contenido', '')).lower()
                break
        
        # Regla 9: Equipo lento - Prioridad Media (PRIORIDAD ALTA en el orden)
        if any(palabra in contenido for palabra in ['lento', 'lenta', 'lentos', 'lentas', 'demora', 'tarda', 'rendimiento', 'optimizar']):
            self.resultados.append({
                'regla': 'Regla 9: Equipo Lento',
                'tipo': 'PC/LAPTOP',
                'prioridad': 'Media',
                'asignado_a': 'Equipo de Mantenimiento'
            })
            return
        
        # Regla 6: Equipo no enciende - Prioridad Alta
        elif any(palabra in contenido for palabra in ['no enciende', 'no prende', 'pantalla negra', 'no inicia']):
            self.resultados.append({
                'regla': 'Regla 6: Equipo No Enciende',
                'tipo': 'PC/LAPTOP',
                'prioridad': 'Alta',
                'asignado_a': 'Equipo de Hardware - Emergencias'
            })
            return
        
        # Regla 1: Problemas con impresoras - Prioridad Media
        elif any(palabra in contenido for palabra in ['impresora', 'toner', 'impresion', 'escaner', 'atasco']):
            self.resultados.append({
                'regla': 'Regla 1: Problema de Impresora',
                'tipo': 'EQUIPOS DE IMPRESIÓN/ESCÁNER',
                'prioridad': 'Media',
                'asignado_a': 'Equipo de Hardware - Impresoras'
            })
            return
        
        # Regla 2: Problemas de red - Prioridad Alta
        elif any(palabra in contenido for palabra in ['red', 'internet', 'wifi', 'conexion', 'dominio']):
            self.resultados.append({
                'regla': 'Regla 2: Problema de Red',
                'tipo': 'PC/LAPTOP',
                'prioridad': 'Alta',
                'asignado_a': 'Equipo de Redes'
            })
            return
        
        # Regla 3: Instalación de software - Prioridad Baja
        elif any(palabra in contenido for palabra in ['instalacion', 'instalar', 'software', 'programa', 'aplicacion']):
            self.resultados.append({
                'regla': 'Regla 3: Instalación de Software',
                'tipo': 'PC/LAPTOP',
                'prioridad': 'Baja',
                'asignado_a': 'Equipo de Soporte - Software'
            })
            return
        
        # Regla 4: Problemas con sistemas corporativos - Prioridad Alta
        elif any(palabra in contenido for palabra in ['siga', 'siaf', 'sgd', 'sisper', 'sistema', 'intranet']):
            self.resultados.append({
                'regla': 'Regla 4: Problema de Sistema Corporativo',
                'tipo': 'SISTEMA',
                'prioridad': 'Alta',
                'asignado_a': 'Equipo de Sistemas Corporativos'
            })
            return
        
        # Regla 5: Problemas de contraseña - Prioridad Media
        elif any(palabra in contenido for palabra in ['contraseña', 'password', 'bloqueada', 'expirada', 'restablecimiento']):
            self.resultados.append({
                'regla': 'Regla 5: Problema de Contraseña',
                'tipo': 'SISTEMA',
                'prioridad': 'Media',
                'asignado_a': 'Equipo de Seguridad y Accesos'
            })
            return
        
        # Regla 7: Correo corporativo - Prioridad Media
        elif any(palabra in contenido for palabra in ['correo', 'email', 'gmail', 'outlook', 'corporativo']):
            self.resultados.append({
                'regla': 'Regla 7: Problema de Correo',
                'tipo': 'SISTEMA',
                'prioridad': 'Media',
                'asignado_a': 'Equipo de Correo y Comunicaciones'
            })
            return
        
        # Regla 8: Asesoría general - Prioridad Baja
        elif any(palabra in contenido for palabra in ['asesoria', 'ayuda', 'como', 'consulta', 'duda']):
            self.resultados.append({
                'regla': 'Regla 8: Asesoría General',
                'tipo': 'GENERAL',
                'prioridad': 'Baja',
                'asignado_a': 'Equipo de Asesoría General'
            })
            return
        
        # Regla 10: Habilitaciones y configuraciones - Prioridad Baja
        elif any(palabra in contenido for palabra in ['habilitar', 'configurar', 'activar', 'crear', 'backup']):
            self.resultados.append({
                'regla': 'Regla 10: Habilitación/Configuración',
                'tipo': 'GENERAL',
                'prioridad': 'Baja',
                'asignado_a': 'Equipo de Configuraciones'
            })
            return
        
        # Si no coincide con ninguna regla
        else:
            self.resultados.append({
                'regla': 'Sin clasificar',
                'tipo': 'GENERAL',
                'prioridad': 'Baja',
                'asignado_a': 'Revisar manualmente'
            })
    
    def reset_resultados(self):
        """Limpia los resultados para procesar un nuevo ticket"""
        self.resultados = []