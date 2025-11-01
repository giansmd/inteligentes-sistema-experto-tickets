# Nueva Funcionalidad: Gestión Dinámica de Reglas

## 📋 Descripción General

Se ha implementado un sistema completo de gestión de reglas que permite agregar, editar, eliminar y visualizar reglas de clasificación de tickets de forma dinámica, sin necesidad de modificar el código fuente.

## ✨ Características Nuevas

### 1. **Módulo de Gestión de Reglas** (`engine/rules_manager.py`)

Clase `RulesManager` que proporciona:
- ✅ Cargar reglas desde JSON
- ✅ Agregar nuevas reglas
- ✅ Actualizar reglas existentes
- ✅ Eliminar reglas
- ✅ Activar/Desactivar reglas
- ✅ Obtener estadísticas de reglas

### 2. **Interfaz Gráfica de Gestión** (`ui/gestion_reglas.py`)

Interfaz completa con 4 pestañas:

#### 📋 Ver Reglas
- Visualización de todas las reglas
- Filtros por estado (Activas/Inactivas)
- Filtros por tipo de ticket
- Filtros por prioridad
- Vista expandible con detalles completos
- Botones para activar/desactivar reglas
- Botones para eliminar reglas
- Tabla resumen con todas las reglas

#### ➕ Agregar Regla
- Formulario completo para crear nuevas reglas
- Campos:
  - Nombre de la regla
  - Tipo de ticket (HARDWARE, SOFTWARE, REDES, SEGURIDAD, EQUIPOS DE IMPRESIÓN/ESCÁNER)
  - Prioridad (Alta, Media, Baja)
  - Asignado a (equipo o persona)
  - Palabras clave (separadas por comas)
  - Estado (Activa/Inactiva)
- Validación de campos obligatorios
- Confirmación visual con resumen

#### ✏️ Editar Reglas
- Selector de regla a editar
- Formulario pre-poblado con valores actuales
- Modificación de cualquier campo
- Guardado de cambios con confirmación

#### 📊 Estadísticas
- Métricas generales:
  - Total de reglas
  - Reglas activas
  - Reglas inactivas
- Gráfico de distribución por tipo (gráfico de pastel)
- Gráfico de distribución por prioridad (gráfico de barras)

### 3. **Motor de Clasificación Mejorado** (`engine/classification_engine.py`)

El motor ahora:
1. ✅ Carga reglas personalizadas desde `rules_data.json`
2. ✅ Aplica primero las reglas personalizadas (activas)
3. ✅ Si no coincide, aplica las reglas hardcodeadas existentes
4. ✅ Prioridad a reglas personalizadas sobre hardcodeadas

### 4. **Integración en la Aplicación Principal**

La opción "⚙️ Configuración" ahora muestra la interfaz completa de gestión de reglas.

## 📁 Estructura de Reglas JSON

Las reglas se almacenan en `knowledge/rules_data.json`:

```json
{
  "reglas_personalizadas": [
    {
      "id_regla": "R01",
      "nombre": "Nombre descriptivo",
      "palabras_clave": ["palabra1", "palabra2", "palabra3"],
      "tipo": "TIPO_TICKET",
      "prioridad": "Alta/Media/Baja",
      "asignado_a": "Equipo responsable",
      "activa": true,
      "fecha_creacion": "2025-11-01 10:00:00",
      "fecha_modificacion": "2025-11-01 12:00:00"
    }
  ]
}
```

### Campos de una Regla

- **id_regla**: Identificador único (generado automáticamente)
- **nombre**: Nombre descriptivo de la regla
- **palabras_clave**: Array de palabras que activan la regla
- **tipo**: Categoría del ticket (HARDWARE, SOFTWARE, REDES, SEGURIDAD, etc.)
- **prioridad**: Nivel de urgencia (Alta, Media, Baja)
- **asignado_a**: Equipo o persona responsable
- **activa**: Estado de la regla (true/false)
- **fecha_creacion**: Timestamp de creación (opcional)
- **fecha_modificacion**: Timestamp de última modificación (opcional)

## 🚀 Cómo Usar

### Ver Reglas Existentes

1. Ir a "⚙️ Configuración" en el menú
2. En la pestaña "📋 Ver Reglas"
3. Usar filtros para buscar reglas específicas
4. Expandir reglas para ver detalles
5. Activar/Desactivar o Eliminar desde los botones

### Agregar Nueva Regla

1. Ir a "⚙️ Configuración"
2. Pestaña "➕ Agregar Regla"
3. Completar el formulario:
   - Nombre: Ej. "Problemas de Audio"
   - Tipo: Seleccionar de la lista
   - Prioridad: Alta, Media o Baja
   - Asignado a: Ej. "Equipo de Hardware"
   - Palabras clave: Ej. "audio, sonido, parlantes, microfono"
4. Click en "✅ Crear Regla"
5. Verificar confirmación

### Editar Regla Existente

1. Ir a "⚙️ Configuración"
2. Pestaña "✏️ Editar Reglas"
3. Seleccionar la regla del dropdown
4. Modificar los campos deseados
5. Click en "💾 Guardar Cambios"

### Ver Estadísticas

1. Ir a "⚙️ Configuración"
2. Pestaña "📊 Estadísticas de Reglas"
3. Visualizar métricas y gráficos

## 🔧 Funcionamiento Técnico

### Flujo de Clasificación

```
Ticket ingresado
    ↓
Motor de Clasificación
    ↓
1. Cargar reglas personalizadas activas
    ↓
2. ¿Coincide con regla personalizada?
    ├─ SÍ → Aplicar y terminar
    └─ NO → Continuar
         ↓
3. Evaluar reglas hardcodeadas
    ↓
4. ¿Coincide con regla hardcodeada?
    ├─ SÍ → Aplicar y terminar
    └─ NO → Aplicar regla por defecto
```

### Ventajas del Sistema

1. **Flexibilidad**: Agregar/modificar reglas sin tocar código
2. **Persistencia**: Reglas guardadas en JSON
3. **Prioridad**: Reglas personalizadas tienen precedencia
4. **Control**: Activar/desactivar reglas fácilmente
5. **Análisis**: Estadísticas y visualizaciones
6. **Auditoría**: Fechas de creación y modificación

## 🧪 Pruebas

### Probar Reglas Personalizadas

1. Crear una regla con palabras clave únicas
2. Ir a "➕ Nuevo Ticket"
3. Crear un ticket con esas palabras clave
4. Verificar que se clasifica con la regla personalizada
5. Desactivar la regla
6. Procesar otro ticket similar
7. Verificar que ahora usa reglas hardcodeadas

### Ejemplo de Prueba

**Regla**: 
- Nombre: "Problemas de Audio"
- Palabras: ["audio", "sonido", "audífono"]
- Tipo: HARDWARE
- Prioridad: Media

**Ticket de prueba**:
- Contenido: "No se escucha el audio en mi computadora"
- Resultado esperado: Clasificado con la regla "Problemas de Audio"

## 📝 Notas Importantes

- Las reglas se evalúan en orden de aparición en el JSON
- Las palabras clave NO distinguen mayúsculas/minúsculas
- La primera regla que coincida será aplicada
- Reglas inactivas son ignoradas por el motor
- Los IDs de reglas son generados automáticamente (R01, R02, etc.)

## 🐛 Troubleshooting

### Problema: Las reglas no se cargan
**Solución**: Verificar que `knowledge/rules_data.json` existe y tiene formato válido

### Problema: Regla personalizada no se aplica
**Solución**: 
1. Verificar que la regla está activa
2. Verificar que las palabras clave coinciden exactamente
3. Recordar que se busca coincidencia parcial (substring)

### Problema: Error al guardar regla
**Solución**: Verificar permisos de escritura en el archivo JSON

## 🎯 Próximas Mejoras (Ideas)

- [ ] Importar/Exportar reglas en formato CSV
- [ ] Historial de cambios en reglas
- [ ] Reglas con condiciones múltiples (AND/OR)
- [ ] Priorización de reglas (orden de evaluación)
- [ ] Validación de conflictos entre reglas
- [ ] Machine Learning para sugerir nuevas reglas
- [ ] API REST para gestión de reglas

## 👥 Contribuciones

Esta funcionalidad fue desarrollada en la rama `feature/gestion-reglas` y debe ser probada exhaustivamente antes de fusionar con `main`.

---
**Fecha de implementación**: 1 de Noviembre, 2025
**Versión**: 2.0.0
