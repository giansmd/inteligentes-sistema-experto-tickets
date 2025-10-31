# ui/main.py
import streamlit as st

def mostrar_inicio(session_state):
    # 🧠 Propósito del sistema
    st.markdown("""
    ### 🧠 Propósito del sistema  
    El **Sistema Experto de Service Desk** tiene como propósito **automatizar la clasificación de tickets de soporte técnico**.  
    A través de un motor de inferencia basado en reglas (usando la librería *Experta*), el sistema analiza el contenido de cada solicitud y determina automáticamente:

    - El **tipo de ticket** (incidente, requerimiento, consulta, etc.)  
    - La **prioridad** (alta, media, baja)  
    - El **personal o área asignada** para su atención  

    Esto permite **ahorrar tiempo**, **reducir errores humanos** y **mejorar la eficiencia** del servicio de soporte.
    """)

    # 🪜 Instrucciones
    st.markdown("""
    ### 🪜 Instrucciones para utilizar el sistema

    1. Dirígete a **"➕ Nuevo Ticket"** para registrar una solicitud.  
    2. Completa los campos requeridos.  
    3. Presiona **"Procesar Ticket"** para que el sistema lo analice.  
    4. Consulta los resultados en el **Dashboard** o en **Estadísticas**.
    """)

    # ⚡ Atajos rápidos
    st.markdown("### ⚡ Atajos rápidos")
    col1, col2, col3 = st.columns(3)

    # 👇 Botones dentro de columnas
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

    # Bloque inferior con fondo transparente
    st.markdown("""
    <div style='background-color: rgba(150,150,171,0.2);
                padding: 1rem;
                border-radius: 10px;
                margin-top: 2rem;
                text-align: center;'>
        <h4>💡 Consejo:</h4>
        <p>Puedes cambiar entre modo claro y oscuro desde 
        <b>☰ → Settings → Theme</b> en la esquina superior derecha.</p>
    </div>
    """, unsafe_allow_html=True)
