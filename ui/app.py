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
# Agregar imports en la parte superior
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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


# Reemplazar la sección de estadísticas con:
elif opcion == "📊 Estadísticas":
    st.header("Estadísticas del Sistema")
    
    try:
        ruta = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'facts_storage.json')
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            tickets = datos.get('tickets_procesados', [])
        
        if tickets:
            # Contadores
            categorias = {}
            prioridades = {}
            equipos = {}
            
            for ticket in tickets:
                tipo = ticket.get('tipo', 'Sin clasificar')
                categorias[tipo] = categorias.get(tipo, 0) + 1
                prioridad = ticket.get('prioridad', 'Sin prioridad')
                prioridades[prioridad] = prioridades.get(prioridad, 0) + 1
                equipo = ticket.get('asignado_a', 'Sin asignar')
                equipos[equipo] = equipos.get(equipo, 0) + 1

            # KPIs principales con animación
            col1, col2, col3 = st.columns(3)
            
            with col1:
                cuenta = len(tickets)
                st.write("### 📊 Total Tickets")
                st.markdown(f"""
                <div style='text-align: center; animation: grow 1s ease-out;'>
                    <h1 style='font-size: 3em; color: #1f77b4;'>{cuenta}</h1>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                alta_prioridad = prioridades.get('Alta', 0)
                porcentaje = (alta_prioridad / cuenta) * 100
                st.write("### 🚨 Alta Prioridad")
                st.markdown(f"""
                <div style='text-align: center; animation: grow 1s ease-out;'>
                    <h1 style='font-size: 3em; color: #ff4b4b;'>{alta_prioridad}</h1>
                    <p>({porcentaje:.1f}%)</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.write("### 📑 Categorías")
                st.markdown(f"""
                <div style='text-align: center; animation: grow 1s ease-out;'>
                    <h1 style='font-size: 3em; color: #50af50;'>{len(categorias)}</h1>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Gráfico de barras para tipos de ticket
            df_tipos = pd.DataFrame(list(categorias.items()), columns=['Tipo', 'Cantidad'])
            fig_tipos = px.bar(df_tipos, x='Tipo', y='Cantidad',
                             title='Distribución por Tipo de Ticket',
                             color='Cantidad',
                             color_continuous_scale='Viridis')
            st.plotly_chart(fig_tipos, use_container_width=True)

            # Gráfico circular para prioridades
            df_prioridades = pd.DataFrame(list(prioridades.items()), columns=['Prioridad', 'Cantidad'])
            fig_prioridades = px.pie(df_prioridades, values='Cantidad', names='Prioridad',
                                   title='Distribución por Prioridad',
                                   hole=0.3,
                                   color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig_prioridades, use_container_width=True)

            # Contadores por categoría en grid de 3x3
            st.markdown("### 📊 Desglose por Categoría")
            categorias_sorted = sorted(categorias.items(), key=lambda x: x[1], reverse=True)
            
            for i in range(0, len(categorias_sorted), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(categorias_sorted):
                        cat, count = categorias_sorted[i + j]
                        with cols[j]:
                            st.markdown(f"""
                            <div style='background-color: #f0f2f8; padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 1rem; animation: grow 1s ease-out;'>
                                <h4>{cat}</h4>
                                <div style='font-size: 2em; color: #1f77b4;'>{count}</div>
                                <div style='font-size: 0.8em; color: #666;'>tickets</div>
                            </div>
                            """, unsafe_allow_html=True)

            # Agregar CSS para animaciones
            st.markdown("""
            <style>
            @keyframes grow {
                from {
                    transform: scale(0);
                    opacity: 0;
                }
                to {
                    transform: scale(1);
                    opacity: 1;
                }
            }
            </style>
            """, unsafe_allow_html=True)

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