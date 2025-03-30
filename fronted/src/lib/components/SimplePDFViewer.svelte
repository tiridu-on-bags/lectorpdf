<!-- src/lib/components/SimplePDFViewer.svelte -->
<script lang="ts">
  import { onMount, onDestroy, afterUpdate } from 'svelte';
  import type { PDFSlick as PDFSlickType } from '@pdfslick/core';
  
  // Para asegurar que los estilos estén disponibles
  import "@pdfslick/core/dist/pdf_viewer.css";
  
  export let pdfUrl: string | null = null;
  export let height: number = 600;
  
  let container: HTMLDivElement;
  let pdfSlick: PDFSlickType | null = null;
  let pageNumber = 1;
  let numPages = 0;
  let isLoading = false;
  let error = '';
  let unsubscribe: (() => void) | undefined;
  let pdfLoadAttempted = false;
  
  // Registro de cambios en pdfUrl para debugging
  $: if (pdfUrl) {
    console.log('SimplePDFViewer - URL recibida:', pdfUrl);
    pdfLoadAttempted = false; // Reset cuando cambia la URL
  }
  
  onMount(async () => {
    console.log('SimplePDFViewer - Componente montado');
  });
  
  afterUpdate(async () => {
    // Si tenemos URL, contenedor, y no hemos intentado cargar aún
    if (pdfUrl && container && !pdfLoadAttempted) {
      pdfLoadAttempted = true; // Marcar como intentado para evitar múltiples cargas
      console.log('SimplePDFViewer - Intentando cargar PDF después de actualización:', pdfUrl);
      await loadPDF(pdfUrl);
    }
  });
  
  async function loadPDF(url: string) {
    if (!url) {
      console.warn('SimplePDFViewer - URL vacía, no se puede cargar PDF');
      return;
    }
    
    if (!container) {
      console.warn('SimplePDFViewer - Contenedor no disponible, no se puede cargar PDF');
      return;
    }
    
    console.log('SimplePDFViewer - Iniciando carga de PDF:', url);
    isLoading = true;
    error = '';
    
    try {
      // Intentar verificar si la URL es accesible
      try {
        const response = await fetch(url, { method: 'HEAD' });
        if (!response.ok) {
          throw new Error(`URL no accesible: ${response.status}`);
        }
        console.log('SimplePDFViewer - URL verificada y accesible');
      } catch (e) {
        console.warn('SimplePDFViewer - No se pudo verificar URL, intentando cargar de todos modos:', e);
      }
      
      // Limpiar instancia anterior si existe
      if (pdfSlick && unsubscribe) {
        unsubscribe();
        pdfSlick = null;
      }
      
      // Verificar los estilos del contenedor
      const computedStyle = window.getComputedStyle(container);
      console.log('SimplePDFViewer - Estilos del contenedor:', {
        position: computedStyle.position,
        width: computedStyle.width,
        height: computedStyle.height,
        top: computedStyle.top,
        left: computedStyle.left
      });
      
      // Forzar posición absoluta en el contenedor si no la tiene
      if (computedStyle.position !== 'absolute') {
        console.warn('SimplePDFViewer - El contenedor no tiene posición absoluta, forzando...');
        container.style.position = 'absolute';
        container.style.top = '0';
        container.style.left = '0';
        container.style.right = '0';
        container.style.bottom = '0';
        container.style.width = '100%';
        container.style.height = '100%';
      }
      
      // Importar dinámicamente PDFSlick
      const { create, PDFSlick } = await import('@pdfslick/core');
      
      // Crear store y nueva instancia
      const store = create();
      
      pdfSlick = new PDFSlick({
        container,
        store,
        options: {
          scaleValue: 'page-fit'
        }
      });
      
      // Cargar documento con manejo explícito de promesa
      console.log('SimplePDFViewer - Cargando documento:', url);
      try {
        await pdfSlick.loadDocument(url);
        console.log('SimplePDFViewer - Documento cargado correctamente');
      } catch (loadError) {
        console.error('SimplePDFViewer - Error al cargar documento:', loadError);
        throw loadError;
      }
      
      store.setState({ pdfSlick });
      
      // Suscribirse a cambios de estado
      unsubscribe = store.subscribe((s: any) => {
        pageNumber = s.pageNumber;
        numPages = s.numPages;
      });
      
      console.log('SimplePDFViewer - PDF cargado correctamente:', { pageNumber, numPages });
    } catch (e) {
      console.error('SimplePDFViewer - Error al cargar PDF:', e);
      error = e.message || 'Error al cargar el PDF';
    } finally {
      isLoading = false;
    }
  }
  
  onDestroy(() => {
    if (unsubscribe) unsubscribe();
    console.log('SimplePDFViewer - Componente destruido');
  });
  
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

<div class="pdf-container" style="height: {height}px;">
  {#if isLoading}
    <div class="loading">Cargando PDF...</div>
  {:else if error}
    <div class="error">{error}</div>
  {:else if !pdfUrl}
    <div class="empty-state">
      <p>No hay PDF cargado</p>
    </div>
  {:else}
    <div class="viewer-wrapper">
      <!-- Contenedor con position: absolute -->
      <div class="pdfSlickContainer" bind:this={container}>
        <div class="pdfSlickViewer pdfViewer"></div>
      </div>
    </div>
    
    {#if numPages > 0}
      <div class="controls">
        <button on:click={prevPage} disabled={pageNumber <= 1}>
          Anterior
        </button>
        <span class="page-info">Página {pageNumber} de {numPages}</span>
        <button on:click={nextPage} disabled={pageNumber >= numPages}>
          Siguiente
        </button>
      </div>
    {/if}
  {/if}
</div>

<style>
  .pdf-container {
    width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    background-color: #f5f5f5;
  }
  
  .viewer-wrapper {
    position: relative;
    flex: 1;
    height: calc(100% - 50px);
  }
  
  /* CRÍTICO: El contenedor DEBE tener position: absolute */
  .pdfSlickContainer {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;
    width: 100% !important;
    height: 100% !important;
    overflow: auto;
  }
  
  .empty-state,
  .loading,
  .error {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    text-align: center;
    padding: 20px;
  }
  
  .loading {
    background: #f0f4f8;
    color: #0072e5;
  }
  
  .error {
    background: #fff3f3;
    color: #e53935;
  }
  
  .controls {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
    padding: 10px;
    background: #f0f4f8;
    border-top: 1px solid #ddd;
    height: 50px;
  }
  
  button {
    padding: 6px 12px;
    background: #0072e5;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
  }
  
  button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
  
  .page-info {
    font-size: 14px;
    color: #333;
  }
</style>