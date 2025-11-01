# ui/gestion_areas.py
# Interfaz para gestionar áreas de la empresa

import streamlit as st
import sys
import os
import pandas as pd

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.areas_manager import AreasManager

def mostrar_gestion_areas():
    """
    Muestra la interfaz de gestión de áreas.
    Permite agregar, editar, eliminar y visualizar áreas.
    """
    
    st.header("🏢 Gestión de Áreas de la Empresa")
    
    # Inicializar el gestor de áreas
    areas_manager = AreasManager()
    
    # Crear pestañas
    tab1, tab2, tab3 = st.tabs([
        "📋 Ver Áreas", 
        "➕ Agregar Área", 
        "✏️ Editar Áreas"
    ])
    
    # TAB 1: Ver Áreas
    with tab1:
        st.subheader("📋 Áreas Registradas")
        
        areas = areas_manager.get_all_areas()
        
        if not areas:
            st.info("No hay áreas registradas. Agrega tu primera área en la pestaña 'Agregar Área'.")
        else:
            # Mostrar métricas
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total de Áreas", len(areas))
            with col2:
                st.metric("Última ID", areas[-1]['id_area'] if areas else "N/A")
            
            st.markdown("---")
            
            # Mostrar áreas en expandibles
            for area in areas:
                with st.expander(f"🏢 {area['id_area']} - {area['nombre']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ID:** {area['id_area']}")
                        st.write(f"**Nombre:** {area['nombre']}")
                        if 'descripcion' in area and area['descripcion']:
                            st.write(f"**Descripción:** {area['descripcion']}")
                    
                    with col2:
                        if 'fecha_creacion' in area:
                            st.write(f"**Fecha creación:** {area['fecha_creacion']}")
                        if 'fecha_modificacion' in area:
                            st.write(f"**Última modificación:** {area['fecha_modificacion']}")
                    
                    # Botón de eliminar
                    if st.button("🗑️ Eliminar", key=f"delete_{area['id_area']}"):
                        if areas_manager.delete_area(area['id_area']):
                            st.success("Área eliminada exitosamente")
                            st.rerun()
                        else:
                            st.error("Error al eliminar el área")
            
            # Mostrar tabla resumen
            st.markdown("---")
            st.subheader("📊 Vista de Tabla")
            
            df_areas = pd.DataFrame([{
                'ID': a['id_area'],
                'Nombre': a['nombre'],
                'Descripción': a.get('descripcion', 'Sin descripción')[:50] + '...' if a.get('descripcion', '') else 'Sin descripción'
            } for a in areas])
            
            st.dataframe(df_areas, use_container_width=True)
    
    # TAB 2: Agregar Área
    with tab2:
        st.subheader("➕ Agregar Nueva Área")
        
        with st.form("form_nueva_area"):
            st.write("Complete los siguientes campos para crear una nueva área:")
            
            nombre = st.text_input(
                "Nombre del área *",
                placeholder="Ej: Recursos Humanos",
                help="Nombre del área de la empresa"
            )
            
            descripcion = st.text_area(
                "Descripción (opcional)",
                placeholder="Ej: Área encargada de la gestión del talento humano",
                help="Descripción breve del área"
            )
            
            st.markdown("---")
            
            submitted = st.form_submit_button("✅ Crear Área", use_container_width=True)
            
            if submitted:
                # Validar campos
                if not nombre or nombre.isspace():
                    st.error("❌ El nombre del área es obligatorio")
                else:
                    # Agregar el área
                    if areas_manager.add_area(
                        nombre=nombre.strip(),
                        descripcion=descripcion.strip() if descripcion else ""
                    ):
                        st.success("✅ Área creada exitosamente!")
                        st.balloons()
                        
                        # Mostrar resumen
                        st.info(f"""
                        **Resumen del área creada:**
                        - **Nombre:** {nombre}
                        - **Descripción:** {descripcion if descripcion else 'Sin descripción'}
                        """)
                        
                        # Esperar un momento antes de recargar
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Error al crear el área. Puede que ya exista un área con ese nombre.")
    
    # TAB 3: Editar Áreas
    with tab3:
        st.subheader("✏️ Editar Áreas Existentes")
        
        areas = areas_manager.get_all_areas()
        
        if not areas:
            st.info("No hay áreas para editar. Crea un área primero.")
        else:
            # Seleccionar área a editar
            opciones_areas = [f"{a['id_area']} - {a['nombre']}" for a in areas]
            area_seleccionada_texto = st.selectbox(
                "Selecciona el área a editar:",
                opciones_areas
            )
            
            # Obtener ID del área seleccionada
            id_area_seleccionada = area_seleccionada_texto.split(' - ')[0]
            area_actual = areas_manager.get_area_by_id(id_area_seleccionada)
            
            if area_actual:
                st.markdown("---")
                
                with st.form("form_editar_area"):
                    st.write(f"Editando área: **{area_actual['nombre']}**")
                    
                    nuevo_nombre = st.text_input(
                        "Nombre del área",
                        value=area_actual['nombre']
                    )
                    
                    nueva_descripcion = st.text_area(
                        "Descripción",
                        value=area_actual.get('descripcion', '')
                    )
                    
                    st.markdown("---")
                    
                    submitted = st.form_submit_button("💾 Guardar Cambios", use_container_width=True)
                    
                    if submitted:
                        # Actualizar el área
                        if areas_manager.update_area(
                            id_area=id_area_seleccionada,
                            nombre=nuevo_nombre.strip() if nuevo_nombre else None,
                            descripcion=nueva_descripcion.strip() if nueva_descripcion else None
                        ):
                            st.success("✅ Área actualizada exitosamente!")
                            st.rerun()
                        else:
                            st.error("❌ Error al actualizar el área. Puede que ya exista un área con ese nombre.")
