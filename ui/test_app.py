"""
Interfaz de Pruebas del Sistema Experto
[gians] Aquí podemos probar el sistema con casos de ejemplo
"""

import streamlit as st
from engine.classification_engine import TicketClassificationEngine
from engine.ticket_fact import Ticket

def mostrar_pagina_pruebas():
    """Muestra la interfaz de pruebas con casos predefinidos"""
    
    st.subheader("🧪 Pruebas del Sistema Experto")
    st.markdown("*Prueba los diferentes test del sistema para comprobar su funcionalidad*")
    
    st.divider()

    motor = TicketClassificationEngine()
    
    # Tabs para organizar
    tab1, tab2, tab3 = st.tabs(["Test de inferencia correcta", "Test de caso borde", "Test de explicación de la inferencia"])
    
    # ==================== TAB 1: Test de inferencia correcta ====================
    with tab1:
        st.subheader("Test de inferencia correcta")
        
        st.info("""
        💡 **Instrucciones:**
        1. Presiona 'Probar'
        2. Compara el resultado con lo esperado
        """)
        
        # Mostrar el caso
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Datos del ticket:**")
            st.text_area(
                "Ticket:",
                value="Id ticket = TEST001 " +
                    "\nContenido = mi impresora no funciona" +
                    "\nCliente = Test User"+
                    "\nÁrea = Administración"+
                    "\nFecha = 2025-10-28",
                height=140,
                disabled=True,
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("**Resultado esperado:**")
            st.write(f"📝 Tipo: HARDWARE")
            st.write(f"⚡ Prioridad: Media")
            st.write(f"⚡ Asignado a: Equipo de Hardware")
        
        st.divider()
        
        if st.button("Realizar test", type="primary"):
            with st.spinner("Procesando..."):
                motor = TicketClassificationEngine()
                motor.reset()
                
                # Crear ticket con problema de impresora
                motor.declare(Ticket(
                    id_ticket="TEST001",
                    contenido="mi impresora no funciona",
                    cliente="Test User",
                    area="Administración",
                    fecha="2025-10-28"
                ))
                
                motor.run()
                
                resultado = motor.resultados
                
                st.markdown("### 📊 Resultado Obtenido")
                
                col1, col2, col3 = st.columns(3)

                if resultado:  # primero verifica que no esté vacío
                    correcto_tipo = resultado[0]["tipo"] == "HARDWARE"
                    correcto_prio = resultado[0]["prioridad"].lower() == "media"
                    correcto_asig = resultado[0]["asignado_a"] == "Equipo de Hardware"
                with col1:
                    emoji = "✅" if correcto_tipo else "❌"
                    st.metric(
                        "Tipo",
                        f"{emoji} {resultado[0]["tipo"]}",
                        delta="Correcto" if correcto_tipo else "Incorrecto"
                    )
                
                with col2:
                    emoji = "✅" if correcto_prio else "❌"
                    st.metric(
                        "Prioridad",
                        f"{emoji} {resultado[0]["prioridad"]}",
                        delta="Correcto" if correcto_prio else "Incorrecto"
                    )
                
                with col3:
                    emoji = "✅" if correcto_asig else "❌"
                    st.metric(
                        "Prioridad",
                        f"{emoji} {resultado[0]["asignado_a"]}",
                        delta="Correcto" if correcto_asig else "Incorrecto"
                    )

                # Verificar si todo está correcto
                todo_correcto = correcto_tipo and correcto_prio
                
                if todo_correcto:
                    st.success("🎉 ¡Clasificación 100% correcta!")
                else:
                    st.warning("⚠️ Hay diferencias con el resultado esperado")

    # ==================== TAB 2: Test de caso borde ====================
    with tab2:
        st.subheader("Test de caso borde (edge case)")
        
        st.info("""
        💡 **Instrucciones:**
        1. Presiona 'Probar'
        2. Observa cómo maneja el sistema un ticket sin contenido
        """)

        # Mostrar el caso
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Datos del ticket:**")
            st.text_area(
                "Ticket:",
                value="Id ticket = TEST002 " +
                    "\nContenido = " +
                    "\nCliente = Test User"+
                    "\nÁrea = Contabilidad"+
                    "\nFecha = 2025-10-28",
                height=140,
                disabled=True,
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("**Resultado esperado:**")
            st.write(f"Error: Contenido vacío")
        
        if st.button("Realizar test de caso borde", type="primary"):
            with st.spinner("Procesando..."):
                motor = TicketClassificationEngine()
                motor.reset()
                
                motor.declare(Ticket(
                    id_ticket="TEST002",
                    contenido="",
                    cliente="Test User",
                    area="Contabilidad",
                    fecha="2025-10-28"
                ))
                
                motor.run()
                
                resultado = motor.resultados
                
                st.markdown("### 📊 Resultado Obtenido")
                
                st.write(resultado[0]["regla"])
    
    # ==================== TAB 3: Test de explicación de la inferencia ====================
    with tab3:
        st.subheader("Test de explicación de la inferencia")
        
        st.info("""
        💡 **Instrucciones:**
        1. Presiona 'Probar'
        2. Revisa la explicación generada por el sistema
        """)

        st.markdown("**Datos del ticket:**")
        st.text_area(
            "Ticket:",
            value="Id ticket = TEST003 " +
                "\nContenido = necesito instalar un programa" +
                "\nCliente = Test User"+
                "\nÁrea = Recursos Humanos"+
                "\nFecha = 2025-10-28",
            height=140,
            disabled=True,
            label_visibility="collapsed"
        )
        
        if st.button("Realizar test de explicación", type="primary"):
            with st.spinner("Procesando..."):
                motor = TicketClassificationEngine()
                motor.reset()
                
                motor.declare(Ticket(
                    id_ticket="TEST003",
                    contenido="necesito instalar un programa",
                    cliente="Test User",
                    area="Recursos Humanos",
                    fecha="2025-10-28"
                ))
                
                motor.run()
                
                resultado = motor.resultados
                
                st.markdown("### 📊 Resultado Obtenido")
                
                if resultado:
                    st.write("El sistema clasificó el ticket como:")
                    st.json(resultado)
                    
                    st.markdown("### 🧐 Explicación de la Inferencia")
                    st.write("La regla aplicada fue: \n", resultado[0]['regla'])
                    st.caption("""
                    El sistema aplicó la regla correspondiente a instalación de software debido a que el contenido del ticket menciona la necesidad de instalar un programa. 
                    Según las reglas definidas, este tipo de solicitudes se clasifican con prioridad baja.
                    """)
                else:
                    st.warning("⚠️ No se pudo clasificar el ticket.")