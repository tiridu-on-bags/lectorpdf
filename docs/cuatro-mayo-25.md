# Documentación Implementación Visor PDF (25 de Mayo)

## Objetivo

Implementar un visor de PDF en la aplicación SvelteKit (`/routes/pdf`) utilizando la biblioteca PDF.js ubicada en `/static/pdfjs`.

## Pasos y Decisiones Clave

1.  **Identificación del Error Inicial:** Se detectó un error al intentar importar un componente Svelte inexistente (`$lib/components/PdfJsViewer.svelte`) en `src/routes/pdf/+page.svelte`.
2.  **Creación del Componente Visor:** Se creó el archivo `src/lib/components/PdfJsViewer.svelte` para encapsular la lógica del visor.
3.  **Carga de PDF.js:**
    *   **Intento Fallido:** El intento inicial de cargar `/static/pdfjs/pdf.mjs` mediante `await import()` fue bloqueado por Vite, ya que los assets en `static` no pueden ser importados como módulos directamente.
    *   **Solución:** Se implementó la carga dinámica de `/pdfjs/pdf.mjs` creando un elemento `<script type="module">` en `onMount`. Una vez cargado el script, se accede a la librería `pdfjsLib` (generalmente expuesta en el objeto `window`) y se configura la ruta del worker (`pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdfjs/pdf.worker.mjs'`).
4.  **Tipado TypeScript:**
    *   Para resolver el error `Cannot find module '/pdfjs/pdf.mjs'`, se añadió una declaración de módulo (`declare module '/pdfjs/pdf.mjs' { ... }`) en `src/app.d.ts`, definiendo la exportación por defecto como `unknown` para satisfacer las reglas del linter.
5.  **Manejo de Estado (PDF URL):**
    *   Se encontró un error relacionado con la importación de un store inexistente (`$lib/stores/pdf-state`).
    *   Se comentó temporalmente la importación y uso de este store en `src/routes/pdf/+page.svelte`. Se utilizó una variable local (`let pdfUrl: string | null = null;`) en la página para pasar la URL del PDF cargado al componente `PdfJsViewer`. *Nota: Queda pendiente definir la estrategia final de gestión de estado para la URL del PDF.*
6.  **Diseño y Layout:**
    *   **Ancho Completo:** Se eliminaron clases de padding y centrado (`p-4`, `flex`, `justify-center`, `items-start`) del `div` contenedor principal en `PdfJsViewer.svelte` para permitir que ocupe todo el ancho disponible.
    *   **Centrado Horizontal:** Se añadió CSS (`display: block; margin: 0 auto;`) a la regla `.pdf-canvas` para centrar el canvas horizontalmente dentro de su contenedor.
    *   **Ajuste al Ancho (Fit-to-Width) y Responsividad:**
        *   Se modificó la función `renderPage` para calcular dinámicamente la `scale` del PDF basándose en el ancho del `div` contenedor (`containerElement.clientWidth`).
        *   Se añadió un event listener para el evento `resize` de la ventana. Se utilizó `debounce` de `lodash-es` para optimizar la llamada a `renderPage` cuando cambia el tamaño, asegurando que el PDF se re-renderice con la escala adecuada.
        *   Se instalaron las dependencias `lodash-es` y `@types/lodash-es`.
        *   Se añadió lógica para cancelar tareas de renderizado previas al iniciar una nueva o al destruir el componente.

## Componentes Modificados/Creados

*   `fronted/src/lib/components/PdfJsViewer.svelte` (Creado y modificado)
*   `fronted/src/routes/pdf/+page.svelte` (Modificado)
*   `fronted/src/app.d.ts` (Modificado)
*   `fronted/package.json` y `fronted/package-lock.json` (Modificados por `npm install`)

## Próximos Pasos / Mejoras Posibles

*   Definir e implementar la gestión de estado final para `pdfUrl` (¿Store global o local?).
*   Añadir controles de paginación (página siguiente/anterior).
*   Añadir controles de zoom.
*   Mejorar el manejo de errores (mostrar mensajes más claros al usuario).
*   Verificar la correcta exposición de `pdfjsLib` en `window` para diferentes builds de PDF.js.
*   Considerar el uso de una biblioteca Svelte existente que envuelva PDF.js si la complejidad aumenta.
