He revisado en detalle los tres “#doc” que enviaste:

1. #doc 1 (PSPDFKit for Web)  
   – Muestra cómo instalar `pspdfkit`, copiar sus assets a `static/pspdfkit-lib` y montar el visor con una acción Svelte.

2. #doc 2 (Nutrient vía `pspdfkit`)  
   – Una variante comercial (llamada Nutrient) que en la práctica usa la misma librería `pspdfkit` y copia el directorio `dist/pspdfkit-lib` a `public/`.

3. #doc 3 (Nutrient Web SDK desde CDN o paquete `@nutrient-sdk/viewer`)  
   – Permite usar el SDK desde un CDN (sin copiar archivos a `static/`) o bien instalar `@nutrient-sdk/viewer` y copiar con `rollup-plugin-copy`.

Tú quieres:

• Desechar **toda** la lógica de PDFSlick y PDF.js.  
• No añadir más código de “copias manuales” de assets si es posible.  
• Mantener tu flujo de subida de archivos y el resto de componentes (AI, menús, chats, etc.).  

Propongo este plan paso a paso:

1) Elegir la librería PDF a integrar  
   • **Opción A**: PSPDFKit puro (`npm install pspdfkit`).  
   • **Opción B**: Nutrient Web SDK vía CDN (sin copias estáticas).  
   • **Opción C**: Nutrient Web SDK local (`npm install @nutrient-sdk/viewer + rollup-plugin-copy`).  

   _Mi recomendación de mínimo esfuerzo es la **Opción B** (CDN). No tocas `static/`, basta con agregar un `<script>` al HTML y usar `window.NutrientViewer`._

2) Preparar el HTML base para cargar desde CDN  
   • Editar `src/app.html` (SvelteKit) e inyectar en `<head>`:  
     ```html
     <script defer src="https://cdn.cloud.pspdfkit.com/pspdfkit-web@VERSION/nutrient-viewer.js"></script>
     ```  
   • Reiniciar `npm run dev`.

3) Crear un nuevo componente Svelte “wrapper” (p. ej. `PdfViewer.svelte`)  
   – En `<script>` usar `onMount` / `onDestroy`.  
   – Hacer `use:handleViewer` o directamente en `onMount`:
     ```ts
     import { onMount, onDestroy } from 'svelte';
     export let pdfUrl: string;
     let container: HTMLDivElement;

     onMount(() => {
       if (window.NutrientViewer && container) {
         window.NutrientViewer.load({
           container,
           document: pdfUrl,
           /* opcional: baseUrl si lo necesitas */
         });
       }
     });
     onDestroy(() => {
       window.NutrientViewer?.unload(container);
     });
     ```
   – En el markup:
     ```html
     <div bind:this={container} class="h-full w-full" />
     ```

4) Integrar `PdfViewer.svelte` en tu `+page.svelte`  
   – Importarlo y pasarle `pdfUrl`:  
     ```svelte
     <script lang="ts">
       import PdfViewer from '$lib/components/PdfViewer.svelte';
       // ... tu lógica de subir archivos
     </script>

     {#if pdfUrl}
       <PdfViewer {pdfUrl} />
     {:else}
       <!-- placeholder -->
     {/if}
     ```
   – Elimina cualquier `<iframe>` o componentes PDFSlick/PDF.js que ya no uses.

5) Ajustar estilos y probar  
   – Asegúrate de que el contenedor tenga la altura total (`h-full` / `100vh`).  
   – Sube un PDF y comprueba en la consola de red que carga el script del CDN y el documento correctamente.  
   – Deberías ver la UI de Nutrient (PSPDFKit) en lugar de tu doble header 404.

6) Pulir  
   – (Opcional) Añade control de errores con `bind:errorMsg` si usas PSPDFKit directo.  
   – Quita dependencias de `@pdfslick` / `pdfjs-dist` de `package.json`.  
   – Ajusta tu layout global si necesitas margen cero.

---

Con este enfoque:  
- No copias manualmente assets en `static/`.  
- No dependes de PDF.js ni PDFSlick.  
- Conservas tu uploader y todo lo demás.

Dime si quieres seguir el **CDN** (Opción B) o prefieres montar PSPDFKit local (Opción A) o @nutrient-sdk/viewer (Opción C), y arrancamos implementando.
