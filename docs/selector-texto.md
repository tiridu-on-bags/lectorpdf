# Implementación de visualización de PDF con selección de texto

Este documento describe la implementación de la funcionalidad de visualización de PDF con selección de texto en el proyecto LectorPDF.

## Tecnologías utilizadas

- **PDF.js**: Biblioteca de Mozilla para renderizar PDFs en el navegador
- **Svelte**: Framework para la interfaz de usuario
- **TypeScript**: Para tipado estático y mejor desarrollo

## Componente principal: PdfJsViewer

El componente `PdfJsViewer.svelte` implementa la visualización de PDF con capacidad de selección de texto.

### Características principales:

- Renderización de PDFs directamente en el navegador
- Soporte para selección de texto
- Navegación entre páginas
- Control de escala
- Manejo de errores robusto
- Eventos para interactuar con el texto seleccionado

## Desafíos técnicos y soluciones

### 1. Discrepancia de versiones entre API y Worker

**Problema**: 
```
The API version "5.2.133" does not match the Worker version "5.1.91".
```

**Solución**:
- Descargar versiones coincidentes de todos los archivos de PDF.js
- Asegurar que tanto la API como el Worker sean de la misma versión (5.2.133)

```bash
curl -o pdf.worker.mjs https://unpkg.com/pdfjs-dist@5.2.133/build/pdf.worker.mjs
curl -o pdf.mjs https://unpkg.com/pdfjs-dist@5.2.133/build/pdf.mjs
curl -o pdf.min.mjs https://unpkg.com/pdfjs-dist@5.2.133/build/pdf.min.mjs
curl -o web/pdf_viewer.mjs https://unpkg.com/pdfjs-dist@5.2.133/web/pdf_viewer.mjs
curl -o web/pdf_viewer.css https://unpkg.com/pdfjs-dist@5.2.133/web/pdf_viewer.css
```

### 2. Restricciones de Vite para importar archivos de /public

**Problema**:
```
Cannot import non-asset file /pdfjs/pdf.mjs which is inside /public. JS/CSS files inside /public are copied as-is on build and can only be referenced via <script src> or <link href> in html.
```

**Solución**:
- Implementar carga dinámica de scripts mediante `document.createElement('script')`
- Uso de variables globales para acceder a PDF.js
- Intentar primero importar desde módulos npm como fallback

```javascript
// Cargar scripts dinámicamente
async function loadScripts() {
  // Primero intentar cargar desde módulos npm
  try {
    const pdfJsModule = await import('pdfjs-dist');
    // Configuración...
  } catch (importError) {
    // Fallback: cargar dinámicamente con script tags
    const scriptPdf = document.createElement('script');
    scriptPdf.src = '/pdfjs/pdf.mjs';
    scriptPdf.type = 'text/javascript';
    // Configuración...
    document.head.appendChild(scriptPdf);
  }
}
```

### 3. Errores de renderizado en el mismo canvas

**Problema**:
```
Cannot use the same canvas during multiple render() operations. Use different canvas or ensure previous operations were cancelled or completed.
```

**Solución**:
- Recrear completamente el elemento canvas antes de cada renderizado
- Implementar una bandera para evitar renderizados simultáneos
- Cancelación adecuada de tareas de renderizado previas
- Separación de variables para evitar conflictos

```javascript
// Recrear el canvas para evitar problemas de reutilización
if (canvasEl && canvasEl.parentNode) {
  const newCanvas = document.createElement('canvas');
  newCanvas.className = canvasEl.className;
  canvasEl.parentNode.replaceChild(newCanvas, canvasEl);
  canvasEl = newCanvas;
}
```

### 4. Errores de cancelación de renderizado

**Problema**:
```
RenderingCancelledException {message: 'Rendering cancelled, page 1'...}
```

**Solución**:
- Manejo específico para este tipo de error
- Implementación de pausas entre cancelación y nuevo renderizado
- Mejor limpieza del canvas antes de renderizado

```javascript
// Ignorar errores específicos de cancelación
if (err && err.name === 'RenderingCancelledException') {
  console.log('Renderizado cancelado de forma controlada');
  return;
}
```

### 5. Problemas con la capa de texto

**Solución**:
- Implementación robusta de TextLayerBuilder
- Manejo de errores al añadir nodos de texto
- CSS específico para asegurar que el texto sea seleccionable

```css
.text-layer {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  opacity: 0.2;
  line-height: 1.0;
  pointer-events: all;
  user-select: text;
}
```

## Estructura final del componente

El componente final `PdfJsViewer.svelte` consta de estas partes principales:

1. **Carga dinámica de scripts**: Utiliza carga de scripts con fallback a npm
2. **Sistema de gestión de estado**: Controla página actual, escala, errores, etc.
3. **Renderizado de página**: Implementa un sistema robusto para renderizar PDF
4. **Capa de texto**: Implementa TextLayerBuilder para permitir selección
5. **Navegación**: Proporciona controles para navegar entre páginas
6. **Eventos**: Emite eventos como `textSelected` para interactuar con el texto

## Uso del componente

```svelte
<script>
  import PdfJsViewer from '$lib/components/PdfJsViewer.svelte';
  
  let pdfUrl = 'ruta/a/documento.pdf';
  let selectedText = '';
  
  function handleTextSelected(event) {
    selectedText = event.detail.text;
    console.log('Texto seleccionado:', selectedText);
  }
</script>

<PdfJsViewer {pdfUrl} scale={1.2} on:textSelected={handleTextSelected} />
```

## Lecciones aprendidas

1. **Compatibilidad de versiones**: Es crucial asegurar que todas las partes de PDF.js sean de la misma versión
2. **Consideraciones de bundler**: Vite tiene restricciones específicas para archivos en `/public`
3. **Manejo del canvas**: Las operaciones de renderizado en canvas requieren enfoques específicos para evitar conflictos
4. **Carga dinámica**: La carga dinámica de scripts puede ser una alternativa viable cuando hay restricciones del bundler
5. **Selección de texto**: Requiere configuración específica del CSS y capas adicionales sobre el canvas

## Referencias

- [Documentación de PDF.js](https://mozilla.github.io/pdf.js/getting_started/)
- [Documentación de Vite sobre /public](https://vitejs.dev/guide/assets.html#the-public-directory)
- [TextLayerBuilder API](https://github.com/mozilla/pdf.js/blob/master/src/display/text_layer.js)
