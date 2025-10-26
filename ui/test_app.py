"""
Interfaz de Pruebas del Sistema Experto
[gians] Aquí podemos probar el sistema con casos de ejemplo
"""

import streamlit as st
from engine.inference_engine import MotorInferencia
from knowledge.rules import DESCRIPCION_REGLAS


# [gians] Casos de prueba predefinidos
CASOS_PRUEBA = {
    "Hardware Urgente": {
        "texto": "URGENTE: Mi computadora no enciende y tengo una presentación importante en 1 hora. Necesito ayuda inmediata.",
        "esperado": {"categoria": "hardware", "tipo": "incidencia", "prioridad": "alta"}
    },
    "Software Normal": {
        "texto": "Tengo un problema con Excel, no puedo abrir algunos archivos. ¿Podrían ayudarme?",
        "esperado": {"categoria": "software", "tipo": "incidencia", "prioridad": "media"}
    },
    "Redes Crítico": {
        "texto": "No tengo internet en toda la oficina. Es urgente porque no podemos trabajar sin conexión.",
        "esperado": {"categoria": "redes", "tipo": "incidencia", "prioridad": "alta"}
    },
    "Seguridad Alta": {
        "texto": "Creo que mi cuenta fue hackeada. Recibí emails extraños y mi contraseña no funciona. Necesito ayuda urgente.",
        "esperado": {"categoria": "seguridad", "tipo": "incidencia", "prioridad": "alta"}
    },
    "Consulta Software": {
        "texto": "Hola, me gustaría saber cómo puedo instalar Office en mi computadora nueva. ¿Tienen un tutorial?",
        "esperado": {"categoria": "software", "tipo": "solicitud", "prioridad": "baja"}
    },
    "Hardware Solicitud": {
        "texto": "Solicito un nuevo mouse porque el mío está fallando. No es urgente.",
        "esperado": {"categoria": "hardware", "tipo": "solicitud", "prioridad": "baja"}
    },
    "Redes Lento": {
        "texto": "El internet está muy lento desde esta mañana. Podrían revisar por favor?",
        "esperado": {"categoria": "redes", "tipo": "incidencia", "prioridad": "media"}
    },
    "Seguridad Consulta": {
        "texto": "Quisiera información sobre buenas prácticas de seguridad para contraseñas.",
        "esperado": {"categoria": "seguridad", "tipo": "solicitud", "prioridad": "baja"}
    }
}


def mostrar_pagina_pruebas():
    """Muestra la interfaz de pruebas con casos predefinidos"""
    
    st.title("🧪 Pruebas del Sistema Experto")
    st.markdown("*Prueba el sistema con casos de ejemplo o casos personalizados*")
    
    st.divider()
    
    # [gians] Inicializar motor
    if "motor_pruebas" not in st.session_state:
        st.session_state.motor_pruebas = MotorInferencia()
    
    motor = st.session_state.motor_pruebas
    
    # Tabs para organizar
    tab1, tab2, tab3 = st.tabs(["📋 Casos Predefinidos", "✏️ Prueba Manual", "📚 Reglas"])
    
    # ==================== TAB 1: CASOS PREDEFINIDOS ====================
    with tab1:
        st.subheader("Casos de Prueba Predefinidos")
        
        st.info("""
        💡 **Instrucciones:**
        1. Selecciona un caso de prueba
        2. Presiona 'Probar'
        3. Compara el resultado con lo esperado
        """)
        
        # Selector de caso
        caso_seleccionado = st.selectbox(
            "Selecciona un caso de prueba:",
            list(CASOS_PRUEBA.keys())
        )
        
        caso = CASOS_PRUEBA[caso_seleccionado]
        
        # Mostrar el caso
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Texto del ticket:**")
            st.text_area(
                "Ticket:",
                value=caso["texto"],
                height=100,
                disabled=True,
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("**Resultado esperado:**")
            st.write(f"📂 Categoría: **{caso['esperado']['categoria']}**")
            st.write(f"📝 Tipo: **{caso['esperado']['tipo']}**")
            st.write(f"⚡ Prioridad: **{caso['esperado']['prioridad']}**")
        
        st.divider()
        
        if st.button("🧪 Probar Caso", type="primary"):
            with st.spinner("Procesando..."):
                resultado = motor.procesar_ticket(caso["texto"], f"TEST-{caso_seleccionado}")
                
                st.markdown("### 📊 Resultado Obtenido")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    correcto_cat = resultado["categoria"] == caso["esperado"]["categoria"]
                    emoji = "✅" if correcto_cat else "❌"
                    st.metric(
                        "Categoría",
                        f"{emoji} {resultado['categoria']}",
                        delta="Correcto" if correcto_cat else "Incorrecto"
                    )
                
                with col2:
                    correcto_tipo = resultado["tipo"] == caso["esperado"]["tipo"]
                    emoji = "✅" if correcto_tipo else "❌"
                    st.metric(
                        "Tipo",
                        f"{emoji} {resultado['tipo']}",
                        delta="Correcto" if correcto_tipo else "Incorrecto"
                    )
                
                with col3:
                    correcto_prio = resultado["prioridad"] == caso["esperado"]["prioridad"]
                    emoji = "✅" if correcto_prio else "❌"
                    st.metric(
                        "Prioridad",
                        f"{emoji} {resultado['prioridad']}",
                        delta="Correcto" if correcto_prio else "Incorrecto"
                    )
                
                # Verificar si todo está correcto
                todo_correcto = correcto_cat and correcto_tipo and correcto_prio
                
                if todo_correcto:
                    st.success("🎉 ¡Clasificación 100% correcta!")
                else:
                    st.warning("⚠️ Hay diferencias con el resultado esperado")
                
                # Mostrar acción
                st.markdown("### 🎯 Acción Recomendada")
                st.info(resultado["accion"])
    
    # ==================== TAB 2: PRUEBA MANUAL ====================
    with tab2:
        st.subheader("Prueba con Texto Personalizado")
        
        st.info("Escribe cualquier texto para probar el sistema")
        
        texto_custom = st.text_area(
            "Tu ticket:",
            height=150,
            placeholder="Escribe aquí tu caso de prueba..."
        )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            id_custom = st.text_input("ID del ticket:", placeholder="TEST-CUSTOM")
        
        with col2:
            st.write("")
            st.write("")
            probar_btn = st.button("🚀 Clasificar", type="primary", use_container_width=True)
        
        if probar_btn:
            if not texto_custom:
                st.warning("⚠️ Escribe un texto primero")
            else:
                with st.spinner("Procesando..."):
                    resultado = motor.procesar_ticket(texto_custom, id_custom or "TEST-MANUAL")
                    
                    st.success("✅ Clasificación completada")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("ID", resultado["id_ticket"])
                    
                    with col2:
                        st.metric("Categoría", resultado["categoria"].upper())
                    
                    with col3:
                        st.metric("Tipo", resultado["tipo"].upper())
                    
                    with col4:
                        st.metric("Prioridad", resultado["prioridad"].upper())
                    
                    st.divider()
                    st.markdown("### 🎯 Acción")
                    st.info(resultado["accion"])
                    
                    with st.expander("🔍 Ver conteo de palabras clave"):
                        for cat, count in resultado["conteos"].items():
                            if count > 0:
                                st.write(f"- **{cat}**: {count} coincidencias")
    
    # ==================== TAB 3: REGLAS ====================
    with tab3:
        st.subheader("Reglas del Sistema")
        
        st.markdown(DESCRIPCION_REGLAS)
        
        st.divider()
        
        st.markdown("### 🔑 Palabras Clave por Categoría")
        
        from knowledge.rules import PALABRAS_CLAVE
        
        for categoria, palabras in PALABRAS_CLAVE.items():
            with st.expander(f"📂 {categoria.upper()} ({len(palabras)} palabras)"):
                # [gians] Mostrar en columnas para que sea más compacto
                num_cols = 3
                cols = st.columns(num_cols)
                
                for idx, palabra in enumerate(palabras):
                    col_idx = idx % num_cols
                    with cols[col_idx]:
                        st.write(f"• {palabra}")
    
    # Estadísticas en sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Estadísticas de Pruebas")
    
    stats = motor.obtener_estadisticas()
    st.sidebar.metric("Casos Probados", stats["total"])
    
    if stats["total"] > 0:
        st.sidebar.markdown("**Distribución:**")
        
        if stats["por_categoria"]:
            st.sidebar.write("Por categoría:")
            for cat, count in stats["por_categoria"].items():
                porcentaje = (count / stats["total"]) * 100
                st.sidebar.write(f"• {cat}: {count} ({porcentaje:.1f}%)")
        
        if st.sidebar.button("🗑️ Limpiar Pruebas"):
            motor.limpiar_historial()
            st.sidebar.success("Historial limpiado")
            st.rerun()