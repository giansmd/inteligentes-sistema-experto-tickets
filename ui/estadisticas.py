# 📊 ui/estadisticas.py

#BIBLIOTECAS A UTILIZAR
import streamlit as st # Interfaz de usuario
import os, json # Manejo de archivos y JSON
import pandas as pd # Manipulación de datos
import plotly.express as px # Visualización de datos de forma más dinámica, este es el modulo simplificado de plotly

def mostrar_estadisticas():
    #PARTE 1
    try:
        os.environ["PATH"] += os.pathsep + "/usr/bin"
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

            # Contadores por categoría
            st.markdown("### 📊 Desglose por Categoría")
            categorias_sorted = sorted(categorias.items(), key=lambda x: x[1], reverse=True)
            
            for i in range(0, len(categorias_sorted), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(categorias_sorted):
                        cat, count = categorias_sorted[i + j]
                        with cols[j]:
                            st.markdown(f"""
                            <div style='background-color: rgba(150, 150, 171, 0.4); padding: 1rem; border-radius: 10px; text-align: center; margin-bottom: 1rem; animation: grow 1s ease-out;'>
                                <h4>{cat}</h4>
                                <div style='font-size: 2em; color: #00DED2;'>{count}</div>
                                <div style='font-size: 0.8em; color: #666;'>tickets</div>
                            </div>
                            """, unsafe_allow_html=True)
            # --- Selector de visualización ---
            st.markdown("### 📊 Visualización interactiva con filtros")

            # Convertir a DataFrame completo
            df_tickets = pd.DataFrame(tickets)

            # Convertir fechas
            df_tickets["fecha"] = pd.to_datetime(df_tickets["fecha"], errors="coerce")

            # --- FILTROS ---
            col1, col2, col3 = st.columns(3)

            with col1:
                opcion_grafico = st.selectbox(
                    "Selecciona qué deseas visualizar:",
                    ["Tipo", "Prioridad", "Asignado a", "Cliente", "Área", "Contenido"],
                    index=0
                )

            with col2:
                fecha_min = df_tickets["fecha"].min()
                fecha_max = df_tickets["fecha"].max()
                fecha_rango = st.date_input(
                    "Rango de fechas:",
                    value=(fecha_min if pd.notna(fecha_min) else None, fecha_max if pd.notna(fecha_max) else None)
                )

            with col3:
                filtro_secundario = st.selectbox(
                    "Filtrar por (opcional):",
                    ["Ninguno", "Prioridad", "Área", "Asignado a", "Cliente"],
                    index=0
                )

            # Aplicar filtro de fecha
            if isinstance(fecha_rango, tuple) and len(fecha_rango) == 2:
                inicio, fin = fecha_rango
                df_filtrado = df_tickets[
                    (df_tickets["fecha"] >= pd.to_datetime(inicio)) &
                    (df_tickets["fecha"] <= pd.to_datetime(fin))
                ]
            else:
                df_filtrado = df_tickets.copy()

            # Filtro secundario
            if filtro_secundario != "Ninguno":
                opciones_filtro = ["Todos"] + sorted(df_filtrado[filtro_secundario.lower().replace(" ", "_")].dropna().unique())
                seleccion_filtro = st.selectbox(f"Selecciona {filtro_secundario}:", opciones_filtro)
                if seleccion_filtro != "Todos":
                    df_filtrado = df_filtrado[df_filtrado[filtro_secundario.lower().replace(" ", "_")] == seleccion_filtro]

            # --- AGRUPACIÓN ---
            # Normalizar nombres de columnas sin tildes
            mapeo_columnas = {
                "tipo": "tipo",
                "prioridad": "prioridad",
                "asignado a": "asignado_a",
                "cliente": "cliente",
                "área": "area",
                "area": "area",
                "contenido": "contenido"
            }
            columna = mapeo_columnas.get(opcion_grafico.lower(), opcion_grafico.lower().replace(" ", "_"))

            if columna not in df_filtrado.columns:
                st.warning(f"No hay datos para la categoría '{opcion_grafico}'.")
            else:
                conteo = df_filtrado.groupby(columna).size().reset_index(name="Cantidad")

                # --- MOSTRAR ---
                if opcion_grafico == "Contenido":
                    # Tabla o gráfico horizontal
                    st.markdown("### 🧾 Tabla de Contenidos")
                    st.dataframe(conteo.sort_values("Cantidad", ascending=False).head(20), use_container_width=True)
                else:
                    # Gráfico dinámico
                    orientacion = "v" if opcion_grafico != "Cliente" else "h"
                    fig = px.bar(
                        conteo,
                        x=columna if orientacion == "v" else "Cantidad",
                        y="Cantidad" if orientacion == "v" else columna,
                        orientation=orientacion,
                        title=f"Distribución por {opcion_grafico}",
                        color="Cantidad",
                        color_continuous_scale="Viridis"
                    )
                    st.plotly_chart(fig, use_container_width=True, key=f"chart_{opcion_grafico}")
                
                # --- MÉTRICAS ---
                total = conteo["Cantidad"].sum()
                st.markdown(f"""
                <div style='background-color: rgba(150,150,171,0.2);
                            padding: 1rem; border-radius: 10px; text-align: center;
                            animation: grow 0.8s ease-out; margin-top: 1rem;'>
                    <h4>{opcion_grafico}</h4>
                    <h1 style='font-size: 2.5em; color: #00DED2;'>{total}</h1>
                    <p>Total en rango seleccionado</p>
                </div>
                """, unsafe_allow_html=True)
            if not df_filtrado.empty:
                st.markdown("### 📄 Generar Informe Ejecutivo Personalizado")

                # Seleccionar rango de fechas
                col1, col2 = st.columns(2)
                with col1:
                    inicio_pdf = st.date_input("Desde:", value=df_filtrado["fecha"].min().date())
                with col2:
                    fin_pdf = st.date_input("Hasta:", value=df_filtrado["fecha"].max().date())

                # Seleccionar gráficos a incluir
                opciones_graficos = ["Tipo", "Prioridad", "Área", "Cliente", "Asignado a", "Regla aplicada"]
                graficos_seleccionados = st.multiselect(
                    "Selecciona los gráficos que deseas incluir en el informe:",
                    opciones_graficos,
                    default=["Tipo", "Prioridad"]
                )

                # Generar PDF al hacer clic
                if st.button("📊 Generar Informe Ejecutivo (PDF)"):
                    df_informe = df_filtrado[
                        (df_filtrado["fecha"] >= pd.to_datetime(inicio_pdf)) &
                        (df_filtrado["fecha"] <= pd.to_datetime(fin_pdf))
                    ].copy()

                    if df_informe.empty:
                        st.warning("No hay tickets en el rango seleccionado.")
                    else:
                        pdf_buffer = generar_informe_pdf(df_informe, graficos_seleccionados, inicio_pdf, fin_pdf)
                        st.download_button(
                            label="⬇️ Descargar Informe PDF",
                            data=pdf_buffer,
                            file_name=f"informe_tickets_{inicio_pdf}_{fin_pdf}.pdf",
                            mime="application/pdf"
                        )

            # CSS animación
            st.markdown("""
            <style>
            @keyframes grow {
                from {transform: scale(0); opacity: 0;}
                to {transform: scale(1); opacity: 1;}
            }
            </style>
            """, unsafe_allow_html=True)

        else:
            st.info("No hay datos para mostrar estadísticas")
    
    except Exception as e:
        st.error(f"Error al cargar estadísticas: {e}")



# FUNCIONES AUXILIARES PARA INFORME PDF °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°


from reportlab.lib.pagesizes import letter # Tamaño carta
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
import tempfile
import textwrap
from reportlab.lib.styles import ParagraphStyle
def generar_informe_pdf(df_filtrado, graficos_seleccionados, inicio, fin):
    """Genera el informe ejecutivo PDF con los gráficos seleccionados y tabla completa"""
# Crea un estilo de texto más pequeño
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=30, leftMargin=30,
                            topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    elements = []
    estilo_celda = ParagraphStyle(
        name="TablaCelda",
        parent=styles["BodyText"],
        fontSize=7,        # 👈 aquí cambias el tamaño
        leading=9,         # separación entre líneas
        alignment=1,       # 0=izq, 1=centro, 2=der, 4=justificado
    )

    # --- ENCABEZADO ---
    elements.append(Paragraph("<b>Informe Ejecutivo de Tickets del Sistema</b>", styles['Title']))
    elements.append(Paragraph(
        f"Periodo analizado: {inicio.strftime('%Y-%m-%d')} a {fin.strftime('%Y-%m-%d')}",
        styles['Normal']
    ))
    elements.append(Spacer(1, 12))

    # --- RESUMEN PRINCIPAL ---
    total_tickets = len(df_filtrado)
    elementos_resumen = f"""
    Total de tickets analizados: <b>{total_tickets}</b><br/>
    Categorías incluidas: {', '.join(graficos_seleccionados)}
    """
    elements.append(Paragraph(elementos_resumen, styles['Normal']))
    elements.append(Spacer(1, 18))

    # --- GRÁFICOS SELECCIONADOS ---
    temp_files = []
    for categoria in graficos_seleccionados:
        columna = categoria.lower().replace(" ", "_").replace("área", "area")
        if columna not in df_filtrado.columns:
            continue

        conteo = df_filtrado.groupby(columna).size().reset_index(name="Cantidad")

        fig = px.bar(
            conteo,
            x=columna,
            y="Cantidad",
            title=f"Distribución por {categoria}",
            color="Cantidad",
            color_continuous_scale="Viridis"
        )

        # Guardar imagen temporal del gráfico
        temp_path = os.path.join(tempfile.gettempdir(), f"grafico_{columna}.png")
        fig.write_image(temp_path)
        temp_files.append(temp_path)

        elements.append(Paragraph(f"<b>Gráfico: {categoria}</b>", styles['Heading2']))
        elements.append(Image(temp_path, width=6*inch, height=3*inch))
        elements.append(Spacer(1, 12))

    # --- TABLA FINAL DE TICKETS ---
    elements.append(Paragraph("<b>📋 Detalle de Tickets Analizados</b>", styles['Heading2']))

    # Convertir DataFrame en lista de listas
    data = [list(df_filtrado.columns)] + df_filtrado.astype(str).values.tolist()

    # --- Ajustar texto largo ---
    def wrap_text(text, max_chars=35):
        if not isinstance(text, str):
            text = str(text)
        return "<br/>".join(textwrap.wrap(text, width=max_chars))

    # Aplicar a todas las celdas menos la cabecera
    for i in range(1, len(data)):
        for j in range(len(data[i])):
            data[i][j] = Paragraph(str(data[i][j]), estilo_celda)
    # --- Calcular ancho proporcional ---
    num_cols = len(data[0])
    total_width = 7.5 * inch  # ancho de página útil en letter
    col_widths = [total_width / num_cols for _ in range(num_cols)]

    tabla = Table(data, repeatRows=1, colWidths=col_widths)

    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#00DED2")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.25, colors.gray),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    elements.append(tabla)

    # --- GENERAR PDF ---
    doc.build(elements)
    buffer.seek(0)

    # Limpiar archivos temporales
    for f in temp_files:
        try:
            os.remove(f)
        except:
            pass

    return buffer
