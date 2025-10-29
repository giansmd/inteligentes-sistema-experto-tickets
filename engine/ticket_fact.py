# engine/ticket_fact.py
# Este archivo define la estructura de un ticket (Hecho) que entra al sistema

from experta import Fact

class Ticket(Fact):
    """
    Representa un ticket de soporte con sus atributos
    
    Atributos que puede tener un ticket:
    - id_ticket: identificador único del ticket
    - contenido: descripción del problema
    - tipo: categoría general (EQUIPOS DE IMPRESIÓN/ESCÁNER, PC/LAPTOP, SISTEMA, GENERAL)
    - cliente: nombre del cliente
    - area: área del cliente
    - fecha: fecha de creación del ticket
    - prioridad: prioridad asignada (Alta, Media, Baja)
    - categoria: subcategoría específica del problema
    - asignado_a: equipo o técnico asignado
    """
    pass