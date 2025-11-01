# ui/app.py
# Aplicación principal con Streamlit - Dashboard del sistema experto

# Parche para compatibilidad con Python 3.12
import collections
import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping

import streamlit as st
import json
import os
import sys
import unicodedata
from datetime import datetime
# Agregar imports en la parte superior
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from estadisticas import mostrar_estadisticas


# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.classification_engine import TicketClassificationEngine
from engine.ticket_fact import Ticket

def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = texto.strip()
    return texto

# Configuración de la página
st.set_page_config(
    page_title="Sistema Experto - Service Desk",
    page_icon="🎫",
    layout="wide"
)

# Título principal
st.title("🎫 Sistema Experto Clasificador de Tickets")
st.markdown("---")

# Función para cargar tickets desde JSON
def cargar_tickets_desde_json(archivo):
    """Carga los tickets desde un archivo JSON"""
    try:
        ruta = os.path.join(os.path.dirname(__file__), '..', archivo)
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            return datos.get('tickets', [])
    except FileNotFoundError:
        st.error(f"No se encontró el archivo {archivo}")
        return []

# Función para guardar ticket procesado
def guardar_ticket_procesado(ticket_data, resultado):
    """Guarda el ticket procesado en facts_storage.json"""
    try:
        ruta = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'facts_storage.json')
        
        # Leer datos existentes
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        # Agregar nuevo ticket
        ticket_completo = {
            **ticket_data,
            **resultado,
            'fecha_procesamiento': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        datos['tickets_procesados'].append(ticket_completo)
        
        # Guardar
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        return False

# Función para clasificar un ticket
def clasificar_ticket(ticket_data):
    """Clasifica un ticket usando el motor de inferencia"""
    # Crear el motor
    motor = TicketClassificationEngine()
    motor.reset()
    
    # Declarar el hecho (ticket)
    motor.declare(Ticket(
        id_ticket=ticket_data.get('id_ticket', 'N/A'),
        contenido=ticket_data.get('contenido', '').lower(),  # Convertir a minúsculas
        cliente=ticket_data.get('cliente', ''),
        area=ticket_data.get('area', ''),
        fecha=ticket_data.get('fecha', '')
    ))
    
    # Ejecutar el motor
    motor.run()
    
    # Retornar resultados
    if motor.resultados:
        return motor.resultados[0]  # Devolver el primer resultado
    else:
        return {
            'regla': 'Sin clasificar',
            'tipo': 'GENERAL',
            'prioridad': 'Baja',
            'asignado_a': 'Revisar manualmente'
        }


# Sidebar - Menú de navegación sincronizado con session_state
st.sidebar.title("📋 Menú")

# Lista de opciones del menú
menu_opciones = ["🏠 Inicio", "📊 Dashboard", "➕ Nuevo Ticket", "📈 Estadísticas", "⚙️ Configuración", "🧐 Tests"]

# Inicializar session_state si no existe
if "opcion_menu" not in st.session_state:
    st.session_state["opcion_menu"] = "🏠 Inicio"

# Sincronizar el valor seleccionado en el sidebar
opcion = st.sidebar.radio(
    "Selecciona una opción:",
    menu_opciones,
    index=menu_opciones.index(st.session_state["opcion_menu"])
)

# Actualizar session_state al cambiar manualmente en el sidebar
if opcion != st.session_state["opcion_menu"]:
    st.session_state["opcion_menu"] = opcion
    st.rerun()

# Usar siempre la opción almacenada en session_state
opcion = st.session_state["opcion_menu"]

# OPCIÓN INICIO

if opcion == "🏠 Inicio":
    st.header("🧠 Propósito del Sistema")

    st.markdown("""
    El **Sistema Experto de Service Desk** tiene como propósito **automatizar la clasificación de tickets de soporte técnico**.  
    A través de un motor de inferencia basado en reglas (usando la librería *Experta*), el sistema analiza el contenido de cada solicitud y determina automáticamente:

    - El **tipo de ticket** (incidente, requerimiento, consulta, etc.)  
    - La **prioridad** (alta, media, baja)  
    - El **personal o área asignada** para su atención  

    Esto permite **ahorrar tiempo**, **reducir errores humanos** y **mejorar la eficiencia** del servicio de soporte.
    """)

    st.markdown("---")
    st.subheader("🪜 Instrucciones para utilizar el sistema")

    st.markdown("""
    1. Dirígete a **"➕ Nuevo Ticket"** para registrar una solicitud.  
    2. Completa los campos requeridos.  
    3. Presiona **"Procesar Ticket"** para que el sistema lo analice.  
    4. Consulta los resultados en el **Dashboard** o en **Estadísticas**.
    """)

    st.markdown("---")
    st.subheader("⚡ Atajos rápidos")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Ir al Dashboard"):
            st.session_state["opcion_menu"] = "📊 Dashboard"
            st.rerun()

    with col2:
        if st.button("➕ Crear un Nuevo Ticket"):
            st.session_state["opcion_menu"] = "➕ Nuevo Ticket"
            st.rerun()

    with col3:
        if st.button("📈 Ver Estadísticas"):
            st.session_state["opcion_menu"] = "📈 Estadísticas"
            st.rerun()

    st.markdown("""
    <div style='background-color: rgba(150,150,171,0.15);
                padding: 1rem;
                border-radius: 10px;
                margin-top: 2rem;
                text-align: center;'>
        <h4>💡 Consejo:</h4>
        <p>Puedes cambiar entre modo claro y oscuro desde 
        <b>☰ → Settings → Theme</b> en la esquina superior derecha.</p>
    </div>
    """, unsafe_allow_html=True)

# OPCIÓN 1: Dashboard
elif opcion == "📊 Dashboard":
    st.header("Dashboard de Tickets")
    
    # Botón para cargar tickets de ejemplo
    if st.button("🔄 Procesar Tickets de Ejemplo"):
        tickets = cargar_tickets_desde_json('tests/default_tickets.json')
        
        if tickets:
            st.success(f"✅ Se cargaron {len(tickets)} tickets")
            
            # Procesar cada ticket
            for ticket in tickets:
                resultado = clasificar_ticket(ticket)
                guardar_ticket_procesado(ticket, resultado)
            
            st.balloons()
            st.rerun()
    
    # Mostrar tickets procesados
    st.subheader("📋 Tickets Procesados")
    
    try:
        ruta = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'facts_storage.json')
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            tickets_procesados = datos.get('tickets_procesados', [])
        
        if tickets_procesados:
            # Mostrar en tabla
            for ticket in tickets_procesados:
                with st.expander(f"🎫 {ticket.get('id_ticket', 'N/A')} - {ticket.get('cliente', 'Sin nombre')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Contenido:** {ticket.get('contenido', 'N/A')}")
                        st.write(f"**Cliente:** {ticket.get('cliente', 'N/A')}")
                        st.write(f"**Área:** {ticket.get('area', 'N/A')}")
                        st.write(f"**Fecha:** {ticket.get('fecha', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Tipo:** {ticket.get('tipo', 'N/A')}")
                        
                        # Color según prioridad
                        prioridad = ticket.get('prioridad', 'Baja')
                        if prioridad == 'Alta':
                            st.error(f"**Prioridad:** {prioridad}")
                        elif prioridad == 'Media':
                            st.warning(f"**Prioridad:** {prioridad}")
                        else:
                            st.info(f"**Prioridad:** {prioridad}")
                        
                        st.write(f"**Asignado a:** {ticket.get('asignado_a', 'N/A')}")
                        st.write(f"**Regla aplicada:** {ticket.get('regla', 'N/A')}")
        else:
            st.info("No hay tickets procesados aún. Procesa algunos tickets de ejemplo o crea uno nuevo.")
    
    except Exception as e:
        st.error(f"Error al cargar tickets: {e}")

# OPCIÓN 2: Nuevo Ticket
elif opcion == "➕ Nuevo Ticket":
    st.header("Crear Nuevo Ticket")

    try:
        ruta_areas = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'areas_empresa.json')
        with open(ruta_areas, 'r', encoding='utf-8') as f:
            areas_data = json.load(f)
            json_areas = [area_obj['nombre'] for area_obj in areas_data.get('areas', [])]
    except Exception as e:
        st.error(f"Error al cargar áreas: {e}")
        json_areas = []
    
    with st.form("form_nuevo_ticket"):
        col1, col2 = st.columns(2)
        
        with col1:
            id_ticket = st.text_input("ID del Ticket", value=f"TK{datetime.now().strftime('%Y%m%d%H%M%S')}")
            cliente = st.text_input("Nombre del Cliente")
            area = st.text_input("Área del Cliente")
        
        with col2:
            fecha = st.date_input("Fecha", value=datetime.now())
            contenido = st.text_area("Descripción del Problema", height=150)
        
        submitted = st.form_submit_button("🚀 Procesar Ticket")

        if submitted:
            if contenido and cliente and area:
                if normalizar(area) in [normalizar(a) for a in json_areas]:
                    # Crear el ticket
                    nuevo_ticket = {
                        'id_ticket': id_ticket,
                        'contenido': contenido,
                        'cliente': cliente,
                        'area': area,
                        'fecha': fecha.strftime('%Y-%m-%d')
                    }
                    
                    # Clasificar
                    resultado = clasificar_ticket(nuevo_ticket)
                    
                    # Guardar
                    if guardar_ticket_procesado(nuevo_ticket, resultado):
                        st.success("✅ Ticket procesado y guardado exitosamente!")
                        
                        # Mostrar resultado
                        st.info(f"""
                        **Clasificación:**
                        - Tipo: {resultado['tipo']}
                        - Prioridad: {resultado['prioridad']}
                        - Asignado a: {resultado['asignado_a']}
                        - Regla aplicada: {resultado['regla']}
                        """)
                        
                        st.balloons()
                else:
                    st.error("Área no reconocida. Por favor ingrese un área dentro de la lista mostrada.")
            else:
                st.error("Por favor completa todos los campos")

    st.divider() 
    st.subheader("Áreas de la Empresa")
    st.text("   Las áreas disponibles son:")
    for i in range(len(json_areas)):
        st.write(f"{i + 1}. {json_areas[i]}")

# OPCIÓN 3: Estadísticas


# Reemplazar la sección de estadísticas con:
elif opcion == "📈 Estadísticas":
    st.header("Estadísticas del Sistema")
    mostrar_estadisticas()

# OPCIÓN 4: Configuración - Gestión de Reglas
elif opcion == "⚙️ Configuración":
    from ui.gestion_reglas import mostrar_gestion_reglas
    mostrar_gestion_reglas()

# OPCIÓN 5: Tests
elif opcion == "🧐 Tests":
    from ui.test_app import mostrar_pagina_pruebas
    mostrar_pagina_pruebas()

# Footer
st.markdown("---")
st.markdown("**Sistema Experto de Service Desk** | Desarrollado con Experta + Streamlit")
