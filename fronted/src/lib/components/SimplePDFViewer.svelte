<!-- src/lib/components/SimplePDFViewer.svelte -->
<script lang="ts">
  import { onMount, onDestroy, tick } from 'svelte';
  import { browser } from '$app/environment';
  import * as pdfjs from 'pdfjs-dist';
  
  export let pdfUrl: string | null = null;
  export let height: number = 600;
  
  let pdfContainer: HTMLElement | null = null;
  let loadingTask: any = null;
  let error: string | null = null;
  let renderState = {
    loading: false,
    initialized: false,
    error: null as string | null
  };
  
  // Configuración del worker PDF.js
  $: if (browser && !pdfjs.GlobalWorkerOptions.workerSrc) {
    pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;
  }
  
  onMount(() => {
    console.log('SimplePDFViewer - Componente montado');
    return () => {
      // Patrón Resource Management: Limpieza de recursos
      if (loadingTask) {
        loadingTask.destroy?.();
        loadingTask = null;
      }
    };
  });
  
  onDestroy(() => {
    console.log('SimplePDFViewer - Componente destruido');
  });
  
  // Aplicación del patrón Circuit Breaker para prevenir fallos en cascada
  async function loadPDF(url: string) {
    if (!url || !browser) return;
    
    // Prevenir múltiples cargas simultáneas (patrón Guard)
    if (renderState.loading) return;
    
    console.log('SimplePDFViewer - Iniciando carga de PDF:', url);
    renderState.loading = true;
    renderState.error = null;
    
    try {
      // Esperar a que el DOM se actualice antes de manipularlo (evita errores de referencia)
      await tick();
      
      // Verificar que el contenedor existe en el DOM
      if (!pdfContainer) {
        throw new Error('Contenedor PDF no disponible en el DOM');
      }
      
      // Implementación del patrón de Retry con backoff exponencial
      let retries = 0;
      const maxRetries = 3;
      
      while (retries < maxRetries) {
        try {
          // Cargar el documento (sin verificación previa por HEAD)
          loadingTask = pdfjs.getDocument(url);
          const pdf = await loadingTask.promise;
          
          // Renderizar la primera página
          const page = await pdf.getPage(1);
          const viewport = page.getViewport({ scale: 1.0 });
          
          // Ajustar contenedor
          const canvas = document.createElement('canvas');
          const context = canvas.getContext('2d');
          
          // Calcular escala para ajuste al contenedor 
          const containerWidth = pdfContainer.clientWidth;
          const scale = containerWidth / viewport.width;
          const scaledViewport = page.getViewport({ scale });
          
          canvas.height = scaledViewport.height;
          canvas.width = scaledViewport.width;
          
          // Limpiar contenedor y añadir canvas
          pdfContainer.innerHTML = '';
          pdfContainer.appendChild(canvas);
          
          // Renderizar el PDF
          await page.render({
            canvasContext: context,
            viewport: scaledViewport
          }).promise;
          
          renderState.initialized = true;
          console.log('SimplePDFViewer - PDF cargado exitosamente');
          break; // Salir del bucle de reintentos si es exitoso
          
        } catch (err) {
          retries++;
          if (retries >= maxRetries) throw err;
          
          // Backoff exponencial
          const delay = Math.pow(2, retries) * 100;
          await new Promise(resolve => setTimeout(resolve, delay));
          console.warn(`SimplePDFViewer - Reintento ${retries}/${maxRetries}`);
        }
      }
      
    } catch (err) {
      console.error('SimplePDFViewer - Error al cargar PDF:', err);
      renderState.error = err.message || 'Error al cargar el PDF';
      
      // Fallback visual
      if (pdfContainer) {
        pdfContainer.innerHTML = `
          <div class="pdf-error">
            <p>No se pudo cargar el PDF. ${renderState.error}</p>
            <button id="retry-pdf">Reintentar</button>
          </div>
        `;
        
        // Event binding seguro
        setTimeout(() => {
          const retryBtn = pdfContainer?.querySelector('#retry-pdf');
          retryBtn?.addEventListener('click', () => loadPDF(url));
        }, 0);
      }
    } finally {
      renderState.loading = false;
    }
  }
  
  // Efecto reactivo para cambios de URL
  $: if (pdfUrl) {
    console.log('SimplePDFViewer - URL recibida:', pdfUrl);
    loadPDF(pdfUrl);
  }
</script>

<div class="pdf-viewer-container" style="height: {height}px;">
  {#if renderState.loading}
    <div class="loading-indicator">
      <span class="spinner"></span>
      <p>Cargando documento...</p>
    </div>
  {/if}
  
  <!-- Contenedor de PDF con binding seguro -->
  <div class="pdf-container" bind:this={pdfContainer}></div>
</div>

<style>
  .pdf-viewer-container {
    position: relative;
    width: 100%;
    overflow: auto;
    background-color: #f5f5f5;
    border-radius: 4px;
    border: 1px solid #e0e0e0;
  }
  
  .pdf-container {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100%;
  }
  
  .loading-indicator {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #333;
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(0, 114, 229, 0.2);
    border-radius: 50%;
    border-top-color: #0072e5;
    animation: spin 1s ease-in-out infinite;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .pdf-error {
    padding: 20px;
    text-align: center;
    color: #d32f2f;
  }
</style>