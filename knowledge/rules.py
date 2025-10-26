"""
Base de Conocimiento - Reglas del Sistema Experto
[gians] Aquí definimos las reglas que el sistema usará para clasificar tickets
"""

from durable.lang import *

# [gians] Constantes para las categorías y prioridades
CATEGORIAS = ["hardware", "software", "redes", "seguridad"]
TIPOS = ["incidencia", "solicitud"]
PRIORIDADES = ["alta", "media", "baja"]

# [gians] Palabras clave para identificar categorías
PALABRAS_CLAVE = {
    "hardware": [
        "computadora", "pc", "laptop", "mouse", "teclado", "monitor",
        "impresora", "disco", "ram", "memoria", "cpu", "pantalla",
        "dispositivo", "equipo", "hardware"
    ],
    "software": [
        "programa", "aplicación", "app", "software", "sistema", "windows",
        "office", "word", "excel", "correo", "email", "navegador",
        "chrome", "firefox", "instalar", "actualizar", "licencia"
    ],
    "redes": [
        "internet", "wifi", "red", "conexión", "conectar", "ethernet",
        "cable", "router", "modem", "vpn", "acceso", "servidor",
        "ip", "dns", "ping", "lento", "velocidad"
    ],
    "seguridad": [
        "virus", "malware", "contraseña", "password", "hackeo", "ataque",
        "antivirus", "firewall", "phishing", "spam", "bloqueo", "acceso",
        "permisos", "seguridad", "protección", "amenaza"
    ]
}

# [gians] Palabras que indican prioridad alta
PALABRAS_URGENTES = [
    "urgente", "crítico", "emergencia", "inmediato", "ahora",
    "bloqueado", "no funciona", "caído", "importante", "necesito ya"
]

# [gians] Palabras que indican solicitud vs incidencia
PALABRAS_SOLICITUD = [
    "solicito", "requiero", "necesito", "quiero", "podría",
    "me gustaría", "consulta", "información", "ayuda con",
    "cómo", "cuando", "pregunta"
]


def clasificar_ticket_simple(texto_ticket):
    """
    Función auxiliar para clasificar un ticket de forma básica
    [gians] Esta función analiza el texto y cuenta palabras clave
    """
    # Convertir a minúsculas para comparar mejor
    texto = texto_ticket.lower()
    
    # Inicializar contadores para cada categoría
    conteos = {categoria: 0 for categoria in CATEGORIAS}
    
    # Contar palabras clave de cada categoría
    for categoria, palabras in PALABRAS_CLAVE.items():
        for palabra in palabras:
            if palabra in texto:
                conteos[categoria] += 1
    
    # Determinar la categoría con más coincidencias
    categoria_detectada = max(conteos, key=conteos.get)
    
    # Si no hay coincidencias, categoría por defecto
    if conteos[categoria_detectada] == 0:
        categoria_detectada = "software"  # Por defecto
    
    # Determinar tipo (incidencia o solicitud)
    es_solicitud = any(palabra in texto for palabra in PALABRAS_SOLICITUD)
    tipo = "solicitud" if es_solicitud else "incidencia"
    
    # Determinar prioridad
    es_urgente = any(palabra in texto for palabra in PALABRAS_URGENTES)
    
    # [gians] Lógica simple de prioridad:
    # - Alta: si tiene palabras urgentes o es hardware crítico
    # - Media: incidencias normales
    # - Baja: solicitudes de información
    if es_urgente or (tipo == "incidencia" and categoria_detectada in ["hardware", "seguridad"]):
        prioridad = "alta"
    elif tipo == "incidencia":
        prioridad = "media"
    else:
        prioridad = "baja"
    
    # Determinar acción recomendada
    accion = generar_accion(categoria_detectada, tipo, prioridad)
    
    return {
        "categoria": categoria_detectada,
        "tipo": tipo,
        "prioridad": prioridad,
        "accion": accion,
        "conteos": conteos
    }


def generar_accion(categoria, tipo, prioridad):
    """
    Genera la acción recomendada según la clasificación
    [gians] Aquí definimos qué hacer con cada tipo de ticket
    """
    acciones = {
        # REGLA 1: Hardware crítico
        ("hardware", "incidencia", "alta"): 
            "🚨 ACCIÓN INMEDIATA: Asignar a técnico de hardware. Visita presencial urgente.",
        
        # REGLA 2: Hardware normal
        ("hardware", "incidencia", "media"): 
            "🔧 Asignar a técnico de hardware. Programar visita en 24-48 horas.",
        
        # REGLA 3: Solicitud de hardware
        ("hardware", "solicitud", "baja"): 
            "📋 Registrar solicitud de equipo. Evaluar disponibilidad en almacén.",
        
        # REGLA 4: Software urgente
        ("software", "incidencia", "alta"): 
            "💻 Asignar a soporte de software nivel 2. Resolver por acceso remoto.",
        
        # REGLA 5: Software normal
        ("software", "incidencia", "media"): 
            "💻 Asignar a soporte de software nivel 1. Contactar al usuario en 2 horas.",
        
        # REGLA 6: Consulta de software
        ("software", "solicitud", "baja"): 
            "📖 Enviar documentación o tutorial. Programar capacitación si es necesario.",
        
        # REGLA 7: Redes críticas
        ("redes", "incidencia", "alta"): 
            "🌐 URGENTE: Asignar a administrador de redes. Revisar conectividad inmediatamente.",
        
        # REGLA 8: Redes normal
        ("redes", "incidencia", "media"): 
            "🌐 Asignar a soporte de redes. Verificar configuración y cables.",
        
        # REGLA 9: Seguridad crítica
        ("seguridad", "incidencia", "alta"): 
            "🔒 ALERTA DE SEGURIDAD: Asignar a equipo de ciberseguridad. Aislar equipo si es necesario.",
        
        # REGLA 10: Consulta de seguridad
        ("seguridad", "solicitud", "baja"): 
            "🔐 Asignar a oficial de seguridad. Proporcionar guías de buenas prácticas.",
    }
    
    # Buscar la acción específica o dar una genérica
    clave = (categoria, tipo, prioridad)
    return acciones.get(clave, f"📋 Asignar a equipo de {categoria}. Evaluar caso específico.")


# [gians] Información adicional sobre las reglas
DESCRIPCION_REGLAS = """
📚 **REGLAS DEL SISTEMA EXPERTO** (10 reglas principales)

**REGLA 1 - Hardware Crítico:**
- SI: ticket menciona hardware + problema urgente
- ENTONCES: Prioridad ALTA → Técnico presencial inmediato

**REGLA 2 - Hardware Normal:**
- SI: ticket menciona hardware + problema normal
- ENTONCES: Prioridad MEDIA → Visita programada 24-48h

**REGLA 3 - Solicitud Hardware:**
- SI: ticket solicita hardware nuevo
- ENTONCES: Prioridad BAJA → Evaluar disponibilidad

**REGLA 4 - Software Urgente:**
- SI: ticket menciona software + urgente
- ENTONCES: Prioridad ALTA → Soporte remoto inmediato

**REGLA 5 - Software Normal:**
- SI: ticket menciona software + problema
- ENTONCES: Prioridad MEDIA → Contactar en 2 horas

**REGLA 6 - Consulta Software:**
- SI: ticket pregunta sobre software
- ENTONCES: Prioridad BAJA → Enviar documentación

**REGLA 7 - Redes Críticas:**
- SI: ticket menciona red + urgente
- ENTONCES: Prioridad ALTA → Admin de redes inmediato

**REGLA 8 - Redes Normal:**
- SI: ticket menciona red + problema
- ENTONCES: Prioridad MEDIA → Verificar configuración

**REGLA 9 - Seguridad Crítica:**
- SI: ticket menciona seguridad + amenaza
- ENTONCES: Prioridad ALTA → Equipo ciberseguridad

**REGLA 10 - Consulta Seguridad:**
- SI: ticket pregunta sobre seguridad
- ENTONCES: Prioridad BAJA → Guías de buenas prácticas
"""