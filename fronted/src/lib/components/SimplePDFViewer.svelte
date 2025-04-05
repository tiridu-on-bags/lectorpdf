<!-- src/lib/components/SimplePDFViewer.svelte -->
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';
  
  export let pdfUrl: string | null = null;
  export let height: number = 600;
  
  let container: HTMLDivElement;
  let pdfSlick: any;
  let unsubscribe: () => void;
  let pageNumber = 1;
  let numPages = 0;
  let loading = false;
  let error: string | null = null;

  onMount(async () => {
    // Solo cargar PDFSlick en el cliente
    if (!browser) return;
    
    try {
      console.log('SimplePDFViewer - Inicializando PDFSlick');
      // Importar dinámicamente para evitar errores SSR
      const { create, PDFSlick } = await import('@pdfslick/core');
      
      // Crear store de PDFSlick
      const store = create();
      
      console.log('SimplePDFViewer - Container:', container);
      
      pdfSlick = new PDFSlick({
        container,
        store,
        options: {
          scaleValue: 'page-fit'
        }
      });
      
      // Suscribirse para actualizar estado reactivo
      unsubscribe = store.subscribe((s) => {
        pageNumber = s.pageNumber;
        numPages = s.numPages;
      });
      
      // Cargar el documento si hay URL
      if (pdfUrl) {
        console.log('SimplePDFViewer - Cargando documento:', pdfUrl);
        loading = true;
        try {
          await pdfSlick.loadDocument(pdfUrl);
          console.log('SimplePDFViewer - Documento cargado correctamente');
        } catch (err) {
          console.error('SimplePDFViewer - Error al cargar documento:', err);
          error = err.message || 'Error al cargar el PDF';
        } finally {
          loading = false;
        }
      }
    } catch (err) {
      console.error('SimplePDFViewer - Error al inicializar:', err);
      error = err.message || 'Error al inicializar visor';
    }
  });

  onDestroy(() => {
    // Limpiar suscripción
    if (unsubscribe) unsubscribe();
    
    // Limpiar instancia PDFSlick
    if (pdfSlick && typeof pdfSlick.destroy === 'function') {
      pdfSlick.destroy();
    }
  });
  
  // Actualizar cuando cambia la URL
  $: if (browser && pdfSlick && pdfUrl) {
    console.log('SimplePDFViewer - URL actualizada:', pdfUrl);
    loading = true;
    error = null;
    pdfSlick.loadDocument(pdfUrl)
      .catch((err: Error) => {
        console.error('SimplePDFViewer - Error al cargar documento:', err);
        error = err.message;
      })
      .finally(() => {
        loading = false;
      });
  }
  
  // Funciones de navegación
  function prevPage() {
    if (pdfSlick && pageNumber > 1) {
      pdfSlick.gotoPage(pageNumber - 1);
    }
  }
  
  function nextPage() {
    if (pdfSlick && pageNumber < numPages) {
      pdfSlick.gotoPage(pageNumber + 1);
    }
  }
</script>

<div class="pdf-viewer-container" style="height: {height}px;">
  {#if loading}
    <div class="loading-indicator">
      <span class="spinner"></span>
      <p>Cargando documento...</p>
    </div>
  {/if}
  
  {#if error}
    <div class="pdf-error">
      <p>Error: {error}</p>
      <button on:click={() => pdfUrl && pdfSlick?.loadDocument(pdfUrl)}>
        Reintentar
      </button>
    </div>
  {/if}
  
  <!-- Importante: contenedor con posición absoluta -->
  <div class="pdfSlickContainer" bind:this={container}>
    <div class="pdfSlickViewer pdfViewer"></div>
  </div>
  
  {#if browser && pdfSlick && numPages > 0}
    <div class="pdf-controls">
      <button on:click={prevPage} disabled={pageNumber <= 1}>Anterior</button>
      <span>{pageNumber} / {numPages}</span>
      <button on:click={nextPage} disabled={pageNumber >= numPages}>Siguiente</button>
    </div>
  {/if}
</div>

<style>
  .pdf-viewer-container {
    position: relative;
    width: 100%;
    overflow: hidden;
    background-color: #f5f5f5;
    border-radius: 4px;
    border: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    min-height: 600px;
  }
  
  .pdfSlickContainer {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 40px; /* Espacio para los controles */
    overflow: auto;
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
    z-index: 10;
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
  
  .pdf-controls {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
    gap: 10px;
    background-color: #f0f0f0;
    border-top: 1px solid #e0e0e0;
    height: 40px;
  }
  
  button {
    padding: 5px 10px;
    background-color: #0072e5;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
</style>