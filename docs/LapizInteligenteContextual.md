# Lápiz Inteligente Contextual: Diseño e Implementación

## Concepto

El **Lápiz Inteligente Contextual** es una herramienta avanzada que permite la interacción directa con documentos PDF a través de selecciones de texto. Este enfoque proporciona una experiencia de usuario intuitiva al unificar acciones estándar con capacidades de IA directamente en el contexto de lectura.

### Principios de Diseño

1. **Interacción Contextual**: La selección de texto activa un menú flotante con herramientas estándar e inteligentes.
2. **No Intrusivo**: Los resultados aparecen cerca de la selección, sin interrumpir la lectura.
3. **Integración Natural**: La IA se presenta como una extensión de las herramientas habituales.
4. **Enfocado en el Contenido**: Mantiene al usuario centrado en el documento.

## Implementación Actual

### Arquitectura

```
┌─────────────────┐      ┌─────────────────┐
│    Frontend     │      │     Backend     │
│   (SvelteKit)   │◄────►│    (FastAPI)    │
└─────────────────┘      └─────────────────┘
        │                        │
┌─────────────────┐      ┌─────────────────┐
│    PDFSlick     │      │    Endpoints    │
│  (Visualización)│      │       IA        │
└─────────────────┘      └─────────────────┘
```

### Componentes Principales

#### Frontend

1. **ContextualPdfViewer.svelte**
   - Componente principal que integra PDFSlick
   - Gestiona la selección de texto y muestra menús contextuales
   - Coordina la interacción con el backend para funciones de IA

2. **ContextualMenu.svelte**
   - Menú flotante que aparece al seleccionar texto
   - Ofrece opciones estándar (resaltar, notas, copiar)
   - Ofrece acciones inteligentes (resumir, explicar, preguntar)

3. **AiTooltip.svelte**
   - Muestra resultados de la IA anclados a la selección
   - Proporciona controles para copiar o continuar la interacción
   - Diseño adaptable que evita solaparse con el contenido

#### Backend

1. **Endpoints de IA**
   - `/api/summarize`: Resume fragmentos de texto seleccionados
   - `/api/explain`: Proporciona explicaciones sobre términos o conceptos
   - `/api/ask-selected`: Responde preguntas específicas sobre el texto

### Flujo de Usuario

1. El usuario carga un PDF en la aplicación
2. El documento se visualiza en pantalla completa con PDFSlick
3. Al seleccionar texto, aparece el menú contextual
4. Al elegir una acción de IA (ej. Resumir), se envía el texto al backend
5. El resultado se muestra en un tooltip anclado cerca de la selección

## Funcionalidades Implementadas

### Acciones Estándar
- **Resaltar**: (Placeholder para implementación futura)
- **Añadir Nota**: (Placeholder para implementación futura)
- **Copiar**: Copia el texto seleccionado al portapapeles

### Acciones Inteligentes
- **Resumir**: Genera un resumen conciso del texto seleccionado
- **Explicar**: Proporciona una explicación de términos o conceptos
- **Preguntar**: Permite realizar consultas específicas sobre el contenido seleccionado

## Tecnologías Utilizadas

- **Frontend**: SvelteKit, PDFSlick, TypeScript
- **Backend**: FastAPI, Python
- **PDF Processing**: PyPDF2, fitz (PyMuPDF)
- **IA**: Simulación actual, preparado para integración con LLMs (OpenAI, etc.)

## Pasos Futuros

1. **Integración con LLMs Reales**
   - Conectar con OpenAI, Anthropic u otros proveedores
   - Implementar manejo de contexto para respuestas más precisas

2. **Características Avanzadas**
   - Resaltado persistente de texto
   - Sistema de notas ancladas al documento
   - Historia de consultas por documento

3. **Optimizaciones**
   - Caché de respuestas para preguntas frecuentes
   - Procesamiento en segundo plano para documentos grandes
   - Mejora de la experiencia móvil/táctil

4. **Rastreabilidad y Citas**
   - Integrar sistema de fuentes y referencias
   - Exportar notas y consultas con contexto

## Conclusión

El Lápiz Inteligente Contextual representa un enfoque novedoso para la interacción con documentos PDF, combinando la familiaridad de herramientas estándar con capacidades avanzadas de IA. La implementación actual establece las bases para un sistema robusto que puede mejorar significativamente la forma en que los usuarios consumen y comprenden documentos complejos.

La arquitectura modular permite una expansión gradual de las capacidades, mientras que el diseño centrado en la experiencia de usuario garantiza que la tecnología sea accesible y útil en escenarios prácticos. 