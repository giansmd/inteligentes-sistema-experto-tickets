# engine/classification_engine.py
# Motor de inferencia - aquí van las reglas del sistema experto

# Parche para compatibilidad con Python 3.12
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping

from experta import KnowledgeEngine, Rule
from engine.ticket_fact import Ticket
import json
import os

class TicketClassificationEngine(KnowledgeEngine):
    """
    Motor de clasificación de tickets usando encadenamiento hacia adelante.
    Cada regla evalúa los atributos del ticket y asigna categoría, prioridad y equipo.
    Ahora carga reglas personalizadas desde JSON.
    """
    
    def __init__(self):
        super().__init__()
        self.resultados = []  # Aquí guardamos los resultados de cada ticket
        self.reglas_personalizadas = self.cargar_reglas_personalizadas()
    
    def cargar_reglas_personalizadas(self):
        """Carga las reglas personalizadas desde JSON"""
        try:
            ruta = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'rules_data.json')
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Filtrar solo las reglas activas
                return [r for r in data.get('reglas_personalizadas', []) if r.get('activa', True)]
        except Exception as e:
            print(f"Error al cargar reglas personalizadas: {e}")
            return []
    
    @Rule(Ticket())
    def clasificar_ticket(self):
        """
        Regla principal que se activa cuando se declara un Ticket.
        Evalúa el contenido y aplica la clasificación correspondiente.
        Primero intenta aplicar reglas personalizadas desde JSON, 
        luego las reglas hardcodeadas.
        """
        # Buscar el ticket en los facts
        contenido = ""
        for fact in self.facts.values():
            if isinstance(fact, Ticket):
                contenido = str(fact.get('contenido', '')).lower()
                break

        # Verificar que el contenido no esté vacío
        if not contenido or contenido.isspace():
          self.resultados.append({
            'regla': 'Error: Contenido vacío',
            'tipo': 'ERROR',
            'prioridad': 'Baja',
            'asignado_a': 'Sin asignar'
          })
          return
        
        # Primero intentar con reglas personalizadas desde JSON
        for regla_json in self.reglas_personalizadas:
            palabras_clave = regla_json.get('palabras_clave', [])
            if any(palabra.lower() in contenido for palabra in palabras_clave):
                self.resultados.append({
                    'regla': f"Regla Personalizada: {regla_json['nombre']} ({regla_json['id_regla']})",
                    'tipo': regla_json.get('tipo', 'SOFTWARE'),
                    'prioridad': regla_json.get('prioridad', 'Media'),
                    'asignado_a': regla_json.get('asignado_a', 'Equipo de Software')
                })
                return
        
        # Si no coincide con reglas personalizadas, aplicar reglas hardcodeadas

        # Regla: Seguridad informática - Malware / Phishing (Prioridad Alta)
        if any(palabra in contenido for palabra in ['virus', 'malware', 'ransomware', 'phishing', 'phising', 'adjunto sospechoso', 'suplantación']):
            self.resultados.append({
              'regla': 'Regla: Incidente de Seguridad',
              'tipo': 'SEGURIDAD',
              'prioridad': 'Alta',
              'asignado_a': 'Equipo de Seguridad'
            })
            return

        # Regla: Pérdida de datos / Recuperación (Prioridad Alta)
        if any(palabra in contenido for palabra in ['perdí', 'perdida', 'archivo eliminado', 'no encuentro', 'restaurar', 'recuperar', 'backup perdido', 'datos borrados']):
            self.resultados.append({
              'regla': 'Regla: Recuperación de Datos',
              'tipo': 'SOFTWARE',
              'prioridad': 'Alta',
              'asignado_a': 'Equipo de Software'
            })
            return

        # Regla: ERP / Finanzas / Contabilidad (Prioridad Alta)
        if any(palabra in contenido for palabra in ['erp', 'contabilidad', 'facturación', 'finanzas', 'nomina', 'siga', 'siaf', 'sistema contable']):
            self.resultados.append({
              'regla': 'Regla: Sistema ERP/Finanzas',
              'tipo': 'SOFTWARE',
              'prioridad': 'Alta',
              'asignado_a': 'Equipo de Software'
            })
            return

        # Regla: VPN / Acceso remoto (Prioridad Alta)
        if any(palabra in contenido for palabra in ['vpn', 'acceso remoto', 'escritorio remoto', 'teamviewer', 'conexión remota', 'remote desktop']):
            self.resultados.append({
              'regla': 'Regla: Acceso Remoto / VPN',
              'tipo': 'REDES',
              'prioridad': 'Alta',
              'asignado_a': 'Equipo de Redes'
            })
            return

        # Regla: Equipo no enciende - Prioridad Alta
        if any(palabra in contenido for palabra in ['no enciende', 'no prende', 'pantalla negra', 'no inicia']):
            self.resultados.append({
                'regla': 'Regla: Equipo No Enciende',
                'tipo': 'HARDWARE',
                'prioridad': 'Alta',
                'asignado_a': 'Equipo de Hardware'
            })
            return
        
        # Regla: Problemas de red - Prioridad Alta
        if any(palabra in contenido for palabra in ['red', 'internet', 'wifi', 'conexion', 'dominio']):
            self.resultados.append({
                'regla': 'Regla: Problema de Red',
                'tipo': 'REDES',
                'prioridad': 'Alta',
                'asignado_a': 'Equipo de Redes'
            })
            return
            
        # Regla: Problemas con sistemas corporativos - Prioridad Alta
        if any(palabra in contenido for palabra in ['siga', 'siaf', 'sgd', 'sisper', 'sistema', 'intranet']):
            self.resultados.append({
                'regla': 'Regla: Problema de Sistema Corporativo',
                'tipo': 'SOFTWARE',
                'prioridad': 'Alta',
                'asignado_a': 'Equipo de Software'
            })
            return

        # Regla: Periféricos (mouse, teclado, monitor, webcam) - Prioridad Media
        if any(palabra in contenido for palabra in ['mouse', 'ratón', 'teclado', 'monitor', 'pantalla', 'webcam', 'microfono', 'altavoz', 'parlante']):
            self.resultados.append({
              'regla': 'Regla: Problema de Periféricos',
              'tipo': 'HARDWARE',
              'prioridad': 'Media',
              'asignado_a': 'Equipo de Hardware'
            })
            return

        # Regla: Equipo lento - Prioridad Media
        if any(palabra in contenido for palabra in ['lento', 'lenta', 'lentos', 'lentas', 'demora', 'tarda', 'rendimiento', 'optimizar']):
            self.resultados.append({
                'regla': 'Regla: Equipo Lento',
                'tipo': 'HARDWARE',
                'prioridad': 'Media',
                'asignado_a': 'Equipo de Hardware'
            })
            return
        
        # Regla: Problemas con impresoras - Prioridad Media
        if any(palabra in contenido for palabra in ['impresora', 'toner', 'impresion', 'escaner', 'atasco']):
            self.resultados.append({
                'regla': 'Regla: Problema de Impresora',
                'tipo': 'HARDWARE',
                'prioridad': 'Media',
                'asignado_a': 'Equipo de Hardware'
            })
            return
        
        # Regla: Problemas de contraseña - Prioridad Media
        if any(palabra in contenido for palabra in ['contraseña', 'password', 'bloqueada', 'expirada', 'restablecimiento']):
            self.resultados.append({
                'regla': 'Regla: Problema de Contraseña',
                'tipo': 'SEGURIDAD',
                'prioridad': 'Media',
                'asignado_a': 'Equipo de Seguridad'
            })
            return
        
        # Regla: Correo corporativo - Prioridad Media
        if any(palabra in contenido for palabra in ['correo', 'email', 'gmail', 'outlook', 'corporativo']):
            self.resultados.append({
                'regla': 'Regla: Problema de Correo',
                'tipo': 'SOFTWARE',
                'prioridad': 'Media',
                'asignado_a': 'Equipo de Software'
            })
            return
        
        # Regla: Asesoría general - Prioridad Baja
        if any(palabra in contenido for palabra in ['asesoria', 'ayuda', 'como', 'consulta', 'duda']):
            self.resultados.append({
                'regla': 'Regla: Asesoría General',
                'tipo': 'SOFTWARE',
                'prioridad': 'Baja',
                'asignado_a': 'Equipo de Software'
            })
            return
        
        # Regla: Habilitaciones y configuraciones - Prioridad Baja
        if any(palabra in contenido for palabra in ['habilitar', 'configurar', 'activar', 'crear', 'backup']):
            self.resultados.append({
                'regla': 'Regla: Habilitación/Configuración',
                'tipo': 'SOFTWARE',
                'prioridad': 'Baja',
                'asignado_a': 'Equipo de Software'
            })
            return
        
        # Regla: Instalación de software - Prioridad Baja
        if any(palabra in contenido for palabra in ['instalacion', 'instalar', 'software', 'programa', 'aplicacion']):
            self.resultados.append({
                'regla': 'Regla: Instalación de Software',
                'tipo': 'SOFTWARE',
                'prioridad': 'Baja',
                'asignado_a': 'Equipo de Software'
            })
            return
        
        # Si no coincide con ninguna regla - Fallback
        self.resultados.append({
            'regla': 'Sin clasificar',
            'tipo': 'SOFTWARE',
            'prioridad': 'Baja',
            'asignado_a': 'Equipo de Software'
        })
    
    def reset_resultados(self):
        """Limpia los resultados para procesar un nuevo ticket"""
        self.resultados = []
