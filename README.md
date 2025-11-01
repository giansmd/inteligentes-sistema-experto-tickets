# 🎫 Sistema Experto - Clasificador de Tickets de Soporte

MVP (Minimum Viable Product) de un sistema experto para clasificar automáticamente tickets de soporte técnico.

## 📋 Descripción

Este sistema experto analiza el texto de tickets de soporte y automáticamente:
- ✅ Clasifica en **4 categorías**: Hardware, Software, Redes, Seguridad
- ✅ Identifica el **tipo**: Incidencia o Solicitud  
- ✅ Asigna **prioridad**: Alta, Media o Baja
- ✅ Recomienda una **acción** específica

## 🏗️ Arquitectura

```
sistema-experto-tickets/
├── engine/                          # Motor de inferencia
│   ├── classification_engine.py    # Motor de clasificación con reglas
│   ├── rules_manager.py            # Gestor CRUD de reglas [NUEVO]
│   └── ticket_fact.py              # Definición de hechos
├── knowledge/                       # Base de conocimiento
│   ├── rules_data.json             # Reglas personalizadas en JSON [NUEVO]
│   ├── facts_storage.json          # Almacenamiento de tickets procesados
│   └── areas_empresa.json          # Áreas de la empresa
├── ui/                              # Interfaz de usuario
│   ├── app.py                      # Aplicación principal Streamlit
│   ├── main_app.py                 # Página de inicio
│   ├── gestion_reglas.py           # Interfaz de gestión de reglas [NUEVO]
│   ├── estadisticas.py             # Dashboard de estadísticas
│   └── test_app.py                 # Página de pruebas
├── tests/                           # Pruebas automatizadas
│   ├── test_rules.py               # Tests de reglas
│   ├── test_rules_manager.py       # Tests del gestor de reglas [NUEVO]
│   └── default_tickets.json        # Tickets de ejemplo
├── FEATURE_GESTION_REGLAS.md       # Documentación de gestión de reglas [NUEVO]
└── requirements.txt                # Dependencias
```

## 🚀 Instalación y Uso

### 1. Instalar dependencias

```bash
cd sistema-experto-tickets
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

### 3. Ejecutar pruebas

```bash
pytest tests/test_rules.py -v
```

## 📚 Las 10 Reglas Principales

El sistema implementa 10 reglas principales:

1. **Hardware Crítico**: Problema de hardware urgente → Prioridad ALTA
2. **Hardware Normal**: Problema de hardware → Prioridad MEDIA
3. **Solicitud Hardware**: Solicitud de equipo → Prioridad BAJA
4. **Software Urgente**: Problema software urgente → Prioridad ALTA
5. **Software Normal**: Problema de software → Prioridad MEDIA
6. **Consulta Software**: Pregunta sobre software → Prioridad BAJA
7. **Redes Críticas**: Problema de red urgente → Prioridad ALTA
8. **Redes Normal**: Problema de red → Prioridad MEDIA
9. **Seguridad Crítica**: Amenaza de seguridad → Prioridad ALTA
10. **Consulta Seguridad**: Pregunta de seguridad → Prioridad BAJA

## 🎯 Características Implementadas

### Categorías
- 🔧 **Hardware**: computadora, mouse, teclado, impresora, etc.
- 💻 **Software**: programa, aplicación, Office, navegador, etc.
- 🌐 **Redes**: internet, wifi, conexión, router, etc.
- 🔒 **Seguridad**: virus, contraseña, hackeo, antivirus, etc.
- 🖨️ **Equipos de Impresión/Escáner**: impresoras, escáneres, tóner

### Tipos
- 🚨 **Incidencia**: Problemas que requieren solución
- 📋 **Solicitud**: Consultas o requerimientos

### Prioridades
- 🔴 **Alta**: Requiere atención inmediata (palabras como "urgente", "crítico")
- 🟡 **Media**: Incidencias normales (24-48 horas)
- 🟢 **Baja**: Solicitudes de información (no urgente)

### 🆕 Sistema de Reglas Dinámicas (v2.0)
- ✅ **Gestión visual de reglas**: Crear, editar y eliminar reglas desde la interfaz
- ✅ **Reglas en JSON**: Sin necesidad de modificar código Python
- ✅ **Prioridad configurable**: Las reglas personalizadas tienen precedencia
- ✅ **Activación/Desactivación**: Control del estado de cada regla
- ✅ **Estadísticas y gráficos**: Visualización de distribución de reglas
- ✅ **Filtros avanzados**: Por estado, tipo y prioridad
- ✅ **Auditoría**: Fechas de creación y modificación

## 🧪 Casos de Prueba

El sistema incluye 8 casos de prueba predefinidos:

1. Hardware Urgente
2. Software Normal
3. Redes Crítico
4. Seguridad Alta
5. Consulta Software
6. Hardware Solicitud
7. Redes Lento
8. Seguridad Consulta

Puedes probarlos en la página de **Pruebas** de la aplicación.

## 📊 Funcionalidades

### Página Principal (Clasificador)
- Ingresar texto de ticket
- Ver clasificación automática
- Obtener acción recomendada
- Ver análisis de palabras clave
- Estadísticas de tickets procesados

### Página de Configuración ⚙️ **[NUEVO]**
- **Gestión Dinámica de Reglas**: Sistema completo para crear, editar y eliminar reglas sin modificar código
- **Ver Reglas**: Visualización con filtros por estado, tipo y prioridad
- **Agregar Reglas**: Formulario para crear reglas personalizadas con palabras clave
- **Editar Reglas**: Modificar reglas existentes
- **Estadísticas**: Gráficos de distribución de reglas
- **Activar/Desactivar**: Control del estado de cada regla

> 📖 **Documentación completa**: Ver [FEATURE_GESTION_REGLAS.md](FEATURE_GESTION_REGLAS.md) para detalles técnicos

### Página de Pruebas
- Probar con casos predefinidos
- Probar con texto personalizado
- Comparar con resultados esperados
- Ver todas las reglas del sistema
- Ver palabras clave por categoría

## 🔧 Cómo Funciona

1. **Análisis de Texto**: El sistema lee el texto del ticket
2. **Detección de Palabras Clave**: Busca palabras específicas de cada categoría
3. **Conteo**: Cuenta cuántas palabras clave de cada categoría encuentra
4. **Clasificación**: Asigna la categoría con más coincidencias
5. **Tipo e Incidencia**: Determina si es problema o consulta
6. **Prioridad**: Analiza palabras urgentes y tipo de problema
7. **Acción**: Recomienda acción según la regla aplicable

## 🧠 Motor de Inferencia

El motor de inferencia (`MotorInferencia`) es el cerebro del sistema:

```python
motor = MotorInferencia()
resultado = motor.procesar_ticket("Mi PC no funciona", "TKT-001")
```

**Resultado:**
```python
{
    "id_ticket": "TKT-001",
    "categoria": "hardware",
    "tipo": "incidencia", 
    "prioridad": "alta",
    "accion": "🚨 ACCIÓN INMEDIATA: Asignar a técnico...",
    "conteos": {"hardware": 2, "software": 0, ...}
}
```

## 📈 Estadísticas

El sistema mantiene estadísticas en tiempo real:
- Total de tickets procesados
- Distribución por categoría
- Distribución por tipo
- Distribución por prioridad

## 🧪 Tests

El proyecto incluye tests automatizados con pytest:

```bash
# Ejecutar todos los tests
pytest tests/test_rules.py -v

# Ejecutar un test específico
pytest tests/test_rules.py::TestReglas::test_clasificar_hardware_urgente -v
```

## 🎓 Aprendizajes Implementados

Este MVP demuestra:
- ✅ Arquitectura modular (engine/knowledge/ui/tests)
- ✅ Separación de responsabilidades
- ✅ Sistema basado en reglas
- ✅ Interfaz interactiva con Streamlit
- ✅ Pruebas automatizadas
- ✅ Documentación completa

## ✨ Novedades - Versión 2.0

### 🎉 Gestión Dinámica de Reglas
El sistema ahora permite gestionar reglas de clasificación sin modificar código:

```json
{
  "id_regla": "R01",
  "nombre": "Problemas de Impresora",
  "palabras_clave": ["impresora", "toner", "escaner"],
  "tipo": "EQUIPOS DE IMPRESIÓN/ESCÁNER",
  "prioridad": "Media",
  "asignado_a": "Equipo de Hardware - Impresoras",
  "activa": true
}
```

**Características:**
- 🔧 Crear reglas personalizadas desde la interfaz
- ✏️ Editar reglas existentes
- 🗑️ Eliminar reglas obsoletas  
- 🔄 Activar/desactivar reglas según necesidad
- 📊 Ver estadísticas con gráficos interactivos
- 🎯 Las reglas personalizadas tienen prioridad sobre las hardcodeadas

Ver documentación completa en [FEATURE_GESTION_REGLAS.md](FEATURE_GESTION_REGLAS.md)

## 🔮 Próximas Mejoras

- [ ] Importar/Exportar reglas en formato CSV
- [ ] Historial de cambios en reglas
- [ ] Reglas con condiciones múltiples (AND/OR)
- [ ] Machine Learning para sugerir nuevas reglas
- [ ] Validación de conflictos entre reglas
- [ ] API REST para gestión de reglas
- [ ] Integración con sistemas de tickets reales
- [ ] Múltiples idiomas

## 📝 Notas para Estudiantes

Este código está escrito siguiendo el estilo de los capítulos de OpenCV:
- Comentarios `[gians]` explican conceptos clave
- Código simple y legible, no profesional
- Buenas prácticas básicas
- Fácil de entender y modificar

## 🤝 Contribuir

Este es un proyecto educativo. Para agregar nuevas reglas o mejorar el sistema, modifica:
- `knowledge/rules.py` - Para agregar palabras clave o reglas
- `engine/inference_engine.py` - Para cambiar lógica de procesamiento
- `ui/*.py` - Para mejorar la interfaz

---

## 📚 Documentación Adicional

- **[FEATURE_GESTION_REGLAS.md](FEATURE_GESTION_REGLAS.md)**: Documentación técnica completa del sistema de gestión de reglas dinámicas
  - Arquitectura del módulo RulesManager
  - Guía de uso de la interfaz
  - Ejemplos de pruebas
  - Troubleshooting

---

**Versión:** 2.0  
**Autor:** Sistema experto educativo  
**Fecha:** Noviembre 2025  
**Rama actual:** `feature/gestion-reglas`