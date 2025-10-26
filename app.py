"""
Aplicación Principal del Sistema Experto
[gians] Este es el punto de entrada de la aplicación
"""

import streamlit as st
import sys
import os

# [gians] Agregar el directorio actual al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_app import mostrar_pagina_principal
from ui.test_app import mostrar_pagina_pruebas


# Configuración de la página
st.set_page_config(
    page_title="Sistema Experto - Tickets",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado simple
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Barra lateral con navegación
st.sidebar.title("🎫 Sistema Experto")
st.sidebar.markdown("**Clasificador de Tickets de Soporte**")
st.sidebar.markdown("---")

# Selector de página
pagina = st.sidebar.radio(
    "Navegación:",
    ["🏠 Clasificador", "🧪 Pruebas"],
    index=0
)

st.sidebar.markdown("---")

# Información del sistema
with st.sidebar.expander("ℹ️ Acerca del Sistema"):
    st.markdown("""
    **Sistema Experto v1.0**
    
    Clasifica tickets de soporte en:
    - 4 categorías
    - 2 tipos
    - 3 prioridades
    - 10 reglas principales
    
    **Desarrollado como MVP**
    
    Tecnologías:
    - Streamlit
    - durable_rules
    - Python 3.x
    """)

st.sidebar.markdown("---")

# Mostrar la página seleccionada
if pagina == "🏠 Clasificador":
    mostrar_pagina_principal()
elif pagina == "🧪 Pruebas":
    mostrar_pagina_pruebas()