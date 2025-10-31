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
from datetime import datetime

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.classification_engine import TicketClassificationEngine
from engine.ticket_fact import Ticket

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

# Sidebar - Menú de navegación
st.sidebar.title("📋 Menú")
opcion = st.sidebar.radio(
    "Selecciona una opción:",
    ["🏠 Dashboard", "➕ Nuevo Ticket", "📊 Estadísticas", "⚙️ Configuración"]
)

# OPCIÓN 1: Dashboard
if opcion == "🏠 Dashboard":
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

            if contenido.strip() and cliente and area:
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
                st.error("Por favor completa todos los campos")

# OPCIÓN 3: Estadísticas
elif opcion == "📊 Estadísticas":
    st.header("Estadísticas del Sistema")
    
    try:
        ruta = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'facts_storage.json')
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            tickets = datos.get('tickets_procesados', [])
        
        if tickets:
            # Contar por categoría
            categorias = {}
            prioridades = {}
            equipos = {}
            
            for ticket in tickets:
                # Por tipo
                tipo = ticket.get('tipo', 'Sin clasificar')
                categorias[tipo] = categorias.get(tipo, 0) + 1
                
                # Por prioridad
                prioridad = ticket.get('prioridad', 'Sin prioridad')
                prioridades[prioridad] = prioridades.get(prioridad, 0) + 1
                
                # Por equipo
                equipo = ticket.get('asignado_a', 'Sin asignar')
                equipos[equipo] = equipos.get(equipo, 0) + 1
            
            # Mostrar estadísticas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Tickets", len(tickets))
            
            with col2:
                st.metric("Tickets Alta Prioridad", prioridades.get('Alta', 0))
            
            with col3:
                st.metric("Tipos de Categorías", len(categorias))
            
            st.markdown("---")
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Tickets por Tipo")
                for tipo, cantidad in categorias.items():
                    st.write(f"**{tipo}:** {cantidad} tickets")
            
            with col2:
                st.subheader("⚡ Tickets por Prioridad")
                for prioridad, cantidad in prioridades.items():
                    st.write(f"**{prioridad}:** {cantidad} tickets")
            
            st.markdown("---")
            st.subheader("👥 Tickets por Equipo Asignado")
            for equipo, cantidad in equipos.items():
                st.write(f"**{equipo}:** {cantidad} tickets")
        
        else:
            st.info("No hay datos para mostrar estadísticas")
    
    except Exception as e:
        st.error(f"Error al cargar estadísticas: {e}")

# OPCIÓN 4: Configuración
elif opcion == "⚙️ Configuración":
    st.header("Configuración del Sistema")
    
    st.subheader("🔧 Gestión de Reglas")
    
    # Mostrar reglas actuales
    try:
        ruta = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'rules_data.json')
        with open(ruta, 'r', encoding='utf-8') as f:
            reglas_data = json.load(f)
            reglas = reglas_data.get('reglas_personalizadas', [])
        
        for regla in reglas:
            with st.expander(f"📌 {regla['nombre']}"):
                st.write(f"**ID:** {regla['id_regla']}")
                st.write(f"**Palabras clave:** {', '.join(regla['palabras_clave'])}")
                st.write(f"**Tipo:** {regla['tipo']}")
                st.write(f"**Prioridad:** {regla['prioridad']}")
                st.write(f"**Asignar a:** {regla['asignado_a']}")
                st.write(f"**Estado:** {'✅ Activa' if regla['activa'] else '❌ Inactiva'}")
    
    except Exception as e:
        st.error(f"Error al cargar reglas: {e}")
    
    st.markdown("---")
    
    # Agregar nueva regla (simplificado)
    st.subheader("➕ Agregar Nueva Regla")
    st.info("Función en desarrollo - Próximamente podrás agregar reglas personalizadas")

# Footer
st.markdown("---")
st.markdown("**Sistema Experto de Service Desk** | Desarrollado con Experta + Streamlit")