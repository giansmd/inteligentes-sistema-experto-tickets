"""
Interfaz Principal del Sistema Experto
[gians] Aquí el usuario puede ingresar tickets y ver la clasificación
"""

import streamlit as st
from engine.inference_engine import MotorInferencia


def mostrar_pagina_principal():
    """Muestra la interfaz principal para clasificar tickets"""
    
    st.title("🎫 Sistema Experto - Clasificador de Tickets")
    st.markdown("*Clasifica automáticamente tickets de soporte técnico*")
    
    # Explicación del sistema
    with st.expander("📖 ¿Cómo funciona este sistema?"):
        st.markdown("""
        Este **Sistema Experto** usa reglas predefinidas para clasificar tickets de soporte técnico.
        
        **¿Qué hace?**
        - Lee el texto del ticket
        - Identifica palabras clave
        - Aplica reglas de clasificación
        - Asigna categoría, tipo y prioridad
        - Recomienda una acción
        
        **Categorías disponibles:**
        - 🔧 **Hardware**: Problemas con equipos físicos
        - 💻 **Software**: Problemas con programas y aplicaciones
        - 🌐 **Redes**: Problemas de conectividad
        - 🔒 **Seguridad**: Problemas de seguridad informática
        
        **Tipos de ticket:**
        - 🚨 **Incidencia**: Un problema que necesita resolverse
        - 📋 **Solicitud**: Una consulta o requerimiento
        
        **Prioridades:**
        - 🔴 **Alta**: Requiere atención inmediata
        - 🟡 **Media**: Atención en 24-48 horas
        - 🟢 **Baja**: Puede esperar, no urgente
        """)
    
    st.divider()
    
    # [gians] Inicializar el motor en session_state para mantenerlo entre recargas
    if "motor" not in st.session_state:
        st.session_state.motor = MotorInferencia()
    
    motor = st.session_state.motor
    
    # Área para ingresar el ticket
    st.subheader("📝 Ingresar Nuevo Ticket")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # [gians] Campo de texto para el ticket
        texto_ticket = st.text_area(
            "Describe el problema o solicitud:",
            height=150,
            placeholder="Ejemplo: Mi computadora no enciende y necesito urgentemente acceder a mis archivos...",
            help="Escribe el texto del ticket tal como lo enviaría el usuario"
        )
    
    with col2:
        st.write("**ID del Ticket:**")
        id_ticket = st.text_input(
            "ID (opcional):",
            placeholder="TKT-001",
            help="Deja en blanco para auto-generar"
        )
        
        st.write("")
        st.write("")
        clasificar_btn = st.button("🚀 Clasificar Ticket", type="primary", use_container_width=True)
    
    st.divider()
    
    # Procesar el ticket cuando se presiona el botón
    if clasificar_btn:
        if not texto_ticket or texto_ticket.strip() == "":
            st.warning("⚠️ Por favor, ingresa el texto del ticket")
        else:
            with st.spinner("Procesando ticket..."):
                # [gians] Procesar con el motor de inferencia
                resultado = motor.procesar_ticket(texto_ticket, id_ticket or None)
                
                if "error" in resultado and resultado["error"]:
                    st.error(f"❌ {resultado['error']}")
                else:
                    # Mostrar resultado exitoso
                    st.success("✅ ¡Ticket clasificado exitosamente!")
                    
                    # Mostrar la clasificación en tarjetas
                    st.markdown("### 📊 Resultado de la Clasificación")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "ID Ticket",
                            resultado["id_ticket"],
                            help="Identificador del ticket"
                        )
                    
                    with col2:
                        # [gians] Emoji según categoría
                        emojis_cat = {
                            "hardware": "🔧",
                            "software": "💻",
                            "redes": "🌐",
                            "seguridad": "🔒"
                        }
                        emoji = emojis_cat.get(resultado["categoria"], "📋")
                        
                        st.metric(
                            "Categoría",
                            f"{emoji} {resultado['categoria'].upper()}",
                            help="Área que debe atender el ticket"
                        )
                    
                    with col3:
                        # [gians] Emoji según tipo
                        emoji_tipo = "🚨" if resultado["tipo"] == "incidencia" else "📋"
                        
                        st.metric(
                            "Tipo",
                            f"{emoji_tipo} {resultado['tipo'].upper()}",
                            help="Si es un problema o una consulta"
                        )
                    
                    with col4:
                        # [gians] Color según prioridad
                        emojis_prio = {
                            "alta": "🔴",
                            "media": "🟡",
                            "baja": "🟢"
                        }
                        emoji_prio = emojis_prio.get(resultado["prioridad"], "⚪")
                        
                        st.metric(
                            "Prioridad",
                            f"{emoji_prio} {resultado['prioridad'].upper()}",
                            help="Urgencia del ticket"
                        )
                    
                    st.divider()
                    
                    # Mostrar la acción recomendada
                    st.markdown("### 🎯 Acción Recomendada")
                    st.info(resultado["accion"])
                    
                    # Mostrar análisis de palabras clave
                    with st.expander("🔍 Ver análisis detallado"):
                        st.markdown("**Palabras clave detectadas por categoría:**")
                        
                        conteos = resultado.get("conteos", {})
                        
                        for categoria, conteo in conteos.items():
                            if conteo > 0:
                                st.write(f"- **{categoria.capitalize()}**: {conteo} palabra(s) clave")
                        
                        st.markdown("---")
                        st.markdown("**Texto original del ticket:**")
                        st.code(resultado["texto_original"])
    
    # Mostrar estadísticas en la barra lateral
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Estadísticas")
    
    stats = motor.obtener_estadisticas()
    
    st.sidebar.metric("Total Procesados", stats["total"])
    
    if stats["total"] > 0:
        st.sidebar.markdown("**Por Categoría:**")
        for cat, count in stats["por_categoria"].items():
            st.sidebar.write(f"- {cat}: {count}")
        
        st.sidebar.markdown("**Por Prioridad:**")
        for prio, count in stats["por_prioridad"].items():
            st.sidebar.write(f"- {prio}: {count}")
        
        if st.sidebar.button("🗑️ Limpiar Historial"):
            motor.limpiar_historial()
            st.sidebar.success("Historial limpiado")
            st.rerun()