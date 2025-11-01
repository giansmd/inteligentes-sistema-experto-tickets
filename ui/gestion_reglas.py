# ui/gestion_reglas.py
# Interfaz para gestionar reglas personalizadas

import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.rules_manager import RulesManager

def mostrar_gestion_reglas():
    """
    Muestra la interfaz de gestión de reglas.
    Permite agregar, editar, eliminar y visualizar reglas.
    """
    
    st.header("🔧 Gestión de Reglas")
    
    # Inicializar el gestor de reglas
    rules_manager = RulesManager()
    
    # Crear pestañas
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Ver Reglas", 
        "➕ Agregar Regla", 
        "✏️ Editar Reglas",
        "📊 Estadísticas de Reglas"
    ])
    
    # TAB 1: Ver Reglas
    with tab1:
        st.subheader("📋 Reglas Actuales")
        
        reglas = rules_manager.get_all_rules()
        
        if not reglas:
            st.info("No hay reglas registradas. Agrega tu primera regla en la pestaña 'Agregar Regla'.")
        else:
            # Filtros
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filtro_estado = st.selectbox(
                    "Filtrar por estado:",
                    ["Todas", "Activas", "Inactivas"]
                )
            
            with col2:
                tipos_unicos = list(set([r.get('tipo', 'N/A') for r in reglas]))
                filtro_tipo = st.selectbox(
                    "Filtrar por tipo:",
                    ["Todos"] + tipos_unicos
                )
            
            with col3:
                prioridades_unicas = list(set([r.get('prioridad', 'N/A') for r in reglas]))
                filtro_prioridad = st.selectbox(
                    "Filtrar por prioridad:",
                    ["Todas"] + prioridades_unicas
                )
            
            # Aplicar filtros
            reglas_filtradas = reglas.copy()
            
            if filtro_estado == "Activas":
                reglas_filtradas = [r for r in reglas_filtradas if r.get('activa', True)]
            elif filtro_estado == "Inactivas":
                reglas_filtradas = [r for r in reglas_filtradas if not r.get('activa', True)]
            
            if filtro_tipo != "Todos":
                reglas_filtradas = [r for r in reglas_filtradas if r.get('tipo') == filtro_tipo]
            
            if filtro_prioridad != "Todas":
                reglas_filtradas = [r for r in reglas_filtradas if r.get('prioridad') == filtro_prioridad]
            
            st.write(f"Mostrando **{len(reglas_filtradas)}** de **{len(reglas)}** reglas")
            
            # Mostrar reglas en expandibles
            for regla in reglas_filtradas:
                estado_icon = "✅" if regla.get('activa', True) else "❌"
                
                with st.expander(f"{estado_icon} {regla['id_regla']} - {regla['nombre']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ID:** {regla['id_regla']}")
                        st.write(f"**Nombre:** {regla['nombre']}")
                        st.write(f"**Tipo:** {regla['tipo']}")
                        
                        # Color según prioridad
                        prioridad = regla['prioridad']
                        if prioridad == 'Alta':
                            st.error(f"**Prioridad:** {prioridad}")
                        elif prioridad == 'Media':
                            st.warning(f"**Prioridad:** {prioridad}")
                        else:
                            st.info(f"**Prioridad:** {prioridad}")
                    
                    with col2:
                        st.write(f"**Asignado a:** {regla['asignado_a']}")
                        st.write(f"**Estado:** {'Activa' if regla.get('activa', True) else 'Inactiva'}")
                        
                        if 'fecha_creacion' in regla:
                            st.write(f"**Fecha creación:** {regla['fecha_creacion']}")
                        if 'fecha_modificacion' in regla:
                            st.write(f"**Última modificación:** {regla['fecha_modificacion']}")
                    
                    st.write("**Palabras clave:**")
                    st.write(", ".join(regla['palabras_clave']))
                    
                    # Botones de acción
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        estado_actual = regla.get('activa', True)
                        nuevo_estado_texto = "Desactivar" if estado_actual else "Activar"
                        
                        if st.button(f"🔄 {nuevo_estado_texto}", key=f"toggle_{regla['id_regla']}"):
                            if rules_manager.toggle_rule_status(regla['id_regla']):
                                st.success(f"Regla {nuevo_estado_texto.lower()}da exitosamente")
                                st.rerun()
                            else:
                                st.error("Error al cambiar estado de la regla")
                    
                    with col_btn2:
                        if st.button("🗑️ Eliminar", key=f"delete_{regla['id_regla']}"):
                            if rules_manager.delete_rule(regla['id_regla']):
                                st.success("Regla eliminada exitosamente")
                                st.rerun()
                            else:
                                st.error("Error al eliminar la regla")
            
            # Mostrar tabla resumen
            st.markdown("---")
            st.subheader("📊 Vista de Tabla")
            
            df_reglas = pd.DataFrame([{
                'ID': r['id_regla'],
                'Nombre': r['nombre'],
                'Tipo': r['tipo'],
                'Prioridad': r['prioridad'],
                'Asignado a': r['asignado_a'],
                'Estado': '✅ Activa' if r.get('activa', True) else '❌ Inactiva',
                'Palabras Clave': len(r['palabras_clave'])
            } for r in reglas_filtradas])
            
            st.dataframe(df_reglas, use_container_width=True)
    
    # TAB 2: Agregar Regla
    with tab2:
        st.subheader("➕ Agregar Nueva Regla")
        
        with st.form("form_nueva_regla"):
            st.write("Complete los siguientes campos para crear una nueva regla:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input(
                    "Nombre de la regla *",
                    placeholder="Ej: Problemas de Conexión",
                    help="Nombre descriptivo para identificar la regla"
                )
                
                tipo = st.selectbox(
                    "Tipo de ticket *",
                    ["HARDWARE", "SOFTWARE", "REDES", "SEGURIDAD", "EQUIPOS DE IMPRESIÓN/ESCÁNER"],
                    help="Categoría del ticket"
                )
                
                prioridad = st.selectbox(
                    "Prioridad *",
                    ["Alta", "Media", "Baja"],
                    help="Nivel de urgencia del ticket"
                )
            
            with col2:
                asignado_a = st.text_input(
                    "Asignar a *",
                    placeholder="Ej: Equipo de Redes",
                    help="Equipo o persona responsable"
                )
                
                activa = st.checkbox(
                    "Regla activa",
                    value=True,
                    help="Si está desactivada, la regla no se aplicará"
                )
            
            st.write("**Palabras clave *:**")
            st.write("Ingrese las palabras clave separadas por comas. La regla se activará si el ticket contiene alguna de estas palabras.")
            
            palabras_clave_texto = st.text_area(
                "Palabras clave (separadas por comas)",
                placeholder="Ej: red, internet, wifi, conexión, desconectado",
                help="Palabras que activarán esta regla"
            )
            
            st.markdown("---")
            
            col_submit, col_reset = st.columns([1, 3])
            
            with col_submit:
                submitted = st.form_submit_button("✅ Crear Regla", use_container_width=True)
            
            if submitted:
                # Validar campos
                if not nombre or not palabras_clave_texto or not asignado_a:
                    st.error("❌ Por favor complete todos los campos obligatorios (*)")
                else:
                    # Procesar palabras clave
                    palabras_clave = [
                        palabra.strip().lower() 
                        for palabra in palabras_clave_texto.split(',') 
                        if palabra.strip()
                    ]
                    
                    if not palabras_clave:
                        st.error("❌ Debe ingresar al menos una palabra clave")
                    else:
                        # Agregar la regla
                        if rules_manager.add_rule(
                            nombre=nombre,
                            palabras_clave=palabras_clave,
                            tipo=tipo,
                            prioridad=prioridad,
                            asignado_a=asignado_a,
                            activa=activa
                        ):
                            st.success("✅ Regla creada exitosamente!")
                            st.balloons()
                            
                            # Mostrar resumen
                            st.info(f"""
                            **Resumen de la regla creada:**
                            - **Nombre:** {nombre}
                            - **Tipo:** {tipo}
                            - **Prioridad:** {prioridad}
                            - **Asignado a:** {asignado_a}
                            - **Palabras clave:** {', '.join(palabras_clave)}
                            - **Estado:** {'Activa' if activa else 'Inactiva'}
                            """)
                            
                            # Esperar un momento antes de recargar
                            import time
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Error al crear la regla. Por favor intente nuevamente.")
    
    # TAB 3: Editar Reglas
    with tab3:
        st.subheader("✏️ Editar Reglas Existentes")
        
        reglas = rules_manager.get_all_rules()
        
        if not reglas:
            st.info("No hay reglas para editar. Crea una regla primero.")
        else:
            # Seleccionar regla a editar
            opciones_reglas = [f"{r['id_regla']} - {r['nombre']}" for r in reglas]
            regla_seleccionada_texto = st.selectbox(
                "Selecciona la regla a editar:",
                opciones_reglas
            )
            
            # Obtener ID de la regla seleccionada
            id_regla_seleccionada = regla_seleccionada_texto.split(' - ')[0]
            regla_actual = rules_manager.get_rule_by_id(id_regla_seleccionada)
            
            if regla_actual:
                st.markdown("---")
                
                with st.form("form_editar_regla"):
                    st.write(f"Editando regla: **{regla_actual['nombre']}**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        nuevo_nombre = st.text_input(
                            "Nombre de la regla",
                            value=regla_actual['nombre']
                        )
                        
                        nuevo_tipo = st.selectbox(
                            "Tipo de ticket",
                            ["HARDWARE", "SOFTWARE", "REDES", "SEGURIDAD", "EQUIPOS DE IMPRESIÓN/ESCÁNER"],
                            index=["HARDWARE", "SOFTWARE", "REDES", "SEGURIDAD", "EQUIPOS DE IMPRESIÓN/ESCÁNER"].index(regla_actual['tipo']) if regla_actual['tipo'] in ["HARDWARE", "SOFTWARE", "REDES", "SEGURIDAD", "EQUIPOS DE IMPRESIÓN/ESCÁNER"] else 0
                        )
                        
                        nueva_prioridad = st.selectbox(
                            "Prioridad",
                            ["Alta", "Media", "Baja"],
                            index=["Alta", "Media", "Baja"].index(regla_actual['prioridad']) if regla_actual['prioridad'] in ["Alta", "Media", "Baja"] else 0
                        )
                    
                    with col2:
                        nuevo_asignado_a = st.text_input(
                            "Asignar a",
                            value=regla_actual['asignado_a']
                        )
                        
                        nueva_activa = st.checkbox(
                            "Regla activa",
                            value=regla_actual.get('activa', True)
                        )
                    
                    nuevas_palabras_clave_texto = st.text_area(
                        "Palabras clave (separadas por comas)",
                        value=", ".join(regla_actual['palabras_clave']),
                        height=100
                    )
                    
                    st.markdown("---")
                    
                    submitted = st.form_submit_button("💾 Guardar Cambios", use_container_width=True)
                    
                    if submitted:
                        # Procesar palabras clave
                        nuevas_palabras_clave = [
                            palabra.strip().lower() 
                            for palabra in nuevas_palabras_clave_texto.split(',') 
                            if palabra.strip()
                        ]
                        
                        # Actualizar la regla
                        if rules_manager.update_rule(
                            id_regla=id_regla_seleccionada,
                            nombre=nuevo_nombre,
                            palabras_clave=nuevas_palabras_clave,
                            tipo=nuevo_tipo,
                            prioridad=nueva_prioridad,
                            asignado_a=nuevo_asignado_a,
                            activa=nueva_activa
                        ):
                            st.success("✅ Regla actualizada exitosamente!")
                            st.rerun()
                        else:
                            st.error("❌ Error al actualizar la regla")
    
    # TAB 4: Estadísticas
    with tab4:
        st.subheader("📊 Estadísticas de Reglas")
        
        stats = rules_manager.get_statistics()
        
        # Métricas generales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Reglas", stats['total'])
        
        with col2:
            st.metric("Reglas Activas", stats['activas'], delta=f"{stats['activas']-stats['inactivas']}")
        
        with col3:
            st.metric("Reglas Inactivas", stats['inactivas'])
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribución por Tipo")
            if stats['por_tipo']:
                import plotly.express as px
                
                df_tipos = pd.DataFrame(list(stats['por_tipo'].items()), columns=['Tipo', 'Cantidad'])
                fig = px.pie(df_tipos, values='Cantidad', names='Tipo', hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos para mostrar")
        
        with col2:
            st.subheader("Distribución por Prioridad")
            if stats['por_prioridad']:
                df_prioridades = pd.DataFrame(list(stats['por_prioridad'].items()), columns=['Prioridad', 'Cantidad'])
                
                # Ordenar por prioridad
                orden_prioridad = {'Alta': 0, 'Media': 1, 'Baja': 2}
                df_prioridades['Orden'] = df_prioridades['Prioridad'].map(orden_prioridad)
                df_prioridades = df_prioridades.sort_values('Orden')
                
                # Colores personalizados
                colores = {'Alta': '#ff4b4b', 'Media': '#ffa500', 'Baja': '#4b9eff'}
                
                fig = px.bar(
                    df_prioridades, 
                    x='Prioridad', 
                    y='Cantidad',
                    color='Prioridad',
                    color_discrete_map=colores
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos para mostrar")
