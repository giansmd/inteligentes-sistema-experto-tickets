"""
Motor de Inferencia del Sistema Experto
[gians] Este archivo procesa los tickets y aplica las reglas
"""

from knowledge.rules import clasificar_ticket_simple


class MotorInferencia:
    """
    Motor de inferencia simple para clasificar tickets
    [gians] Esta clase es el "cerebro" que procesa los tickets
    """
    
    def __init__(self):
        """Inicializar el motor"""
        # [gians] Aquí podríamos inicializar cosas como historial, estadísticas, etc.
        self.tickets_procesados = 0
        self.historial = []
    
    def procesar_ticket(self, texto_ticket, id_ticket=None):
        """
        Procesa un ticket y devuelve la clasificación
        
        Args:
            texto_ticket (str): El texto del ticket a procesar
            id_ticket (str): ID opcional del ticket
        
        Returns:
            dict: Diccionario con la clasificación completa
        """
        # [gians] Validar que el texto no esté vacío
        if not texto_ticket or texto_ticket.strip() == "":
            return {
                "error": "El ticket está vacío",
                "categoria": None,
                "tipo": None,
                "prioridad": None,
                "accion": None
            }
        
        # [gians] Aplicar las reglas de clasificación
        resultado = clasificar_ticket_simple(texto_ticket)
        
        # [gians] Agregar información adicional
        resultado["id_ticket"] = id_ticket or f"TICKET-{self.tickets_procesados + 1:04d}"
        resultado["texto_original"] = texto_ticket
        
        # Guardar en historial
        self.historial.append(resultado)
        self.tickets_procesados += 1
        
        return resultado
    
    def obtener_estadisticas(self):
        """
        Devuelve estadísticas sobre los tickets procesados
        [gians] Útil para ver qué tipos de tickets son más comunes
        """
        if not self.historial:
            return {
                "total": 0,
                "por_categoria": {},
                "por_tipo": {},
                "por_prioridad": {}
            }
        
        # Contar por categoría
        categorias = {}
        tipos = {}
        prioridades = {}
        
        for ticket in self.historial:
            # Contar categorías
            cat = ticket.get("categoria", "desconocido")
            categorias[cat] = categorias.get(cat, 0) + 1
            
            # Contar tipos
            tipo = ticket.get("tipo", "desconocido")
            tipos[tipo] = tipos.get(tipo, 0) + 1
            
            # Contar prioridades
            prio = ticket.get("prioridad", "desconocido")
            prioridades[prio] = prioridades.get(prio, 0) + 1
        
        return {
            "total": len(self.historial),
            "por_categoria": categorias,
            "por_tipo": tipos,
            "por_prioridad": prioridades
        }
    
    def limpiar_historial(self):
        """Limpia el historial de tickets"""
        self.historial = []
        self.tickets_procesados = 0