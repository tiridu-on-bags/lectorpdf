<!-- src/lib/components/SimplePDFViewer.svelte -->
<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import type { PDFSlick as PDFSlickType } from '@pdfslick/core';
    
    export let pdfUrl: string | null = null;
    export let height: number = 600;
    
    let container: HTMLDivElement;
    let pdfSlick: PDFSlickType;
    let pageNumber = 1;
    let numPages = 0;
    let isLoading = false;
    let error = '';
    let unsubscribe: () => void;
    
    // Para debug
    $: if (pdfUrl) {
      console.log('PDFSlick - URL recibida:', pdfUrl);
    }
    
    onMount(async () => {
      console.log('PDFSlick - Componente montado, URL inicial:', pdfUrl);
      
      // Importación dinámica de PDFSlick (solo en cliente)
      const { create, PDFSlick } = await import('@pdfslick/core');
      
      // Si ya hay una URL disponible al montar, cargar el PDF
      if (pdfUrl) {
        loadPDF(pdfUrl, create, PDFSlick);
      }
    });
    
    // Reaccionar a cambios en la URL del PDF
    $: if (pdfUrl && container) {
      console.log('PDFSlick - URL actualizada, intentando cargar PDF:', pdfUrl);
      
      // Usar Promise.resolve para asegurar que esto ocurra en el próximo ciclo
      Promise.resolve().then(async () => {
        const { create, PDFSlick } = await import('@pdfslick/core');
        loadPDF(pdfUrl, create, PDFSlick);
      });
    }
    
    async function loadPDF(url, create, PDFSlick) {
      if (!url || !container) {
        console.log('PDFSlick - No se puede cargar PDF, URL o contenedor faltante');
        return;
      }
      
      console.log('PDFSlick - Iniciando carga de PDF:', url);
      isLoading = true;
      error = '';
      
      try {
        // Limpiar instancia anterior si existe
        if (pdfSlick && unsubscribe) {
          unsubscribe();
          pdfSlick = null;
        }
        
        // Crear store y nueva instancia
        const store = create();
        
        pdfSlick = new PDFSlick({
          container,
          store,
          options: {
            scaleValue: 'page-fit'
          }
        });
        
        // Cargar documento
        console.log('PDFSlick - Cargando documento:', url);
        await pdfSlick.loadDocument(url);
        store.setState({ pdfSlick });
        
        // Suscribirse a cambios de estado
        unsubscribe = store.subscribe((s) => {
          pageNumber = s.pageNumber;
          numPages = s.numPages;
        });
        
        console.log('PDF cargado correctamente:', { pageNumber, numPages });
      } catch (e) {
        console.error('Error al cargar PDF:', e);
        error = e.message || 'Error al cargar el PDF';
      } finally {
        isLoading = false;
      }
    }
    
    onDestroy(() => {
      if (unsubscribe) unsubscribe();
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
      <div class="pdfSlickContainer" bind:this={container}>
        <div class="pdfSlickViewer pdfViewer"></div>
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
    }
    
    .pdfSlickContainer {
      flex: 1;
      overflow: auto;
      position: relative;
      height: calc(100% - 50px);
    }
    
    .empty-state, .loading, .error {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100%;
      width: 100%;
    }
    
    .loading {
      background: #f8f9fa;
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
      background: #f8f9fa;
      border-top: 1px solid #eee;
    }
    
    button {
      padding: 6px 12px;
      background: #0072e5;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
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