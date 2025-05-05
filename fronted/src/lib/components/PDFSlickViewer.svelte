<!-- src/lib/components/PDFSlickViewer.svelte -->
<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import { create, PDFSlick } from "@pdfslick/core";
    // Import only GlobalWorkerOptions needed
    import { GlobalWorkerOptions } from 'pdfjs-dist';
    
    export let pdfUrl: string | null = null;
    export let onLoad = () => {};
    
    let containerElement: HTMLDivElement; // Renamed for clarity (outer container)
    let pdfSlick: PDFSlick | null = null;
    let store = create(); // Create the store once
    let pageNumber = 1;
    let numPages = 0;
    
    onMount(() => {
      // Only set worker source on mount
      GlobalWorkerOptions.workerSrc = '/pdfjs/pdf.worker.mjs'; 
      
      // subscribe to store for page changes
      store.subscribe(state => {
        pageNumber = state.pageNumber;
        numPages = state.numPages;
      });

      return () => {
        // Cleanup PDFSlick instance on component destroy
        pdfSlick?._cleanup(); // Keep the cleanup method found previously
        pdfSlick = null;
      };
    });
    
    function prevPage() { if (pdfSlick && pageNumber > 1) pdfSlick.gotoPage(pageNumber - 1); }
    function nextPage() { if (pdfSlick && pageNumber < numPages) pdfSlick.gotoPage(pageNumber + 1); }

    // Reactive statement to initialize and load PDF
    $: {
      if (pdfUrl && containerElement) {
        if (!pdfSlick) {
          // Initialize PDFSlick only when url is available AND it's not already initialized
          console.log("PDFSlickViewer: Initializing PDFSlick instance.");
          const viewerElement = containerElement.querySelector('.pdfViewer') as HTMLDivElement;
          try {
            pdfSlick = new PDFSlick({
              container: containerElement,
              viewer: viewerElement,
              store,
              options: {
                scaleValue: "page-fit",
                textLayerMode: 2
              }
            });
            console.log("PDFSlickViewer: PDFSlick instance created.");
          } catch (error) {
             console.error("PDFSlickViewer: Error creating PDFSlick instance:", error);
          }
        }
        // Load or reload the document after ensuring instance exists
        if (pdfSlick) {
          loadPDF(pdfUrl);
        }
      } else if (!pdfUrl && pdfSlick) {
         // Optional: Clear viewer if URL becomes null
         // pdfSlick.close(); // or _cleanup/destroy? Let's leave it for now.
      }
    }
    
    async function loadPDF(url: string) {
       // Guard moved slightly, check pdfSlick exists before calling methods on it
      if (!url || !pdfSlick) {
          console.warn("PDFSlickViewer: loadPDF called with no URL or uninitialized pdfSlick.");
          return;
      }
      
      console.log(`PDFSlickViewer: Loading document from ${url}`);
      try {
        await pdfSlick.loadDocument(url); // Assumes loadDocument handles subsequent calls correctly
        console.log('PDFSlickViewer: Document loaded successfully.');
        onLoad(); // Call the passed onLoad callback
      } catch (error) {
        console.error("PDFSlickViewer: Error loading PDF:", error);
      }
    }
  </script>
  
  <!-- Outer container with binding -->
  <div class="pdfslick-container w-full h-full" bind:this={containerElement}>
    <!-- Inner div potentially REQUIRED by pdf.js PDFViewer -->
    <div class="pdfViewer"></div> 
  </div>
  
  <!-- Toolbar de paginación -->
  <div class="flex items-center gap-2 mb-2">
    <button on:click={prevPage} disabled={pageNumber <= 1} class="px-2 py-1 bg-gray-200 rounded disabled:opacity-50">Anterior</button>
    <span>Página {pageNumber} de {numPages}</span>
    <button on:click={nextPage} disabled={pageNumber >= numPages} class="px-2 py-1 bg-gray-200 rounded disabled:opacity-50">Siguiente</button>
  </div>
  
  <style>
    /* Import base pdfslick styles - adjust path if necessary */
    @import '@pdfslick/core/dist/pdf_viewer.css';

    .pdfslick-container {
      min-height: 500px;
      background-color: #f5f5f5;
      position: relative; /* Required by PDF.js */
      overflow: auto; /* Often needed with position relative/absolute */
    }

    /* Let PDFSlick/pdf.js manage the inner viewer's style */
    .pdfViewer {
       /* Usually empty, library styles might target this */
    }

    /* Deshabilita los eventos del canvas para que no bloqueen la selección */
    :global(.pdfslick-container .pdfViewer canvas) {
      pointer-events: none;
    }
    /* Asegura que la capa de texto esté encima y seleccionable */
    :global(.pdfslick-container .textLayer) {
      position: absolute;
      top: 0;
      left: 0;
      z-index: 10;
      pointer-events: all !important;
    }
    :global(.pdfslick-container .textLayer span) {
      user-select: text !important;
    }

    /* Ajustes CSS para capa de texto y canvas */
    :global(.pdfslick-container .pdfViewer) {
      position: relative;
    }
    :global(.pdfslick-container .pdfViewer canvas) {
      pointer-events: none;
    }
    :global(.pdfslick-container .textLayer) {
      /* PDF.js ya posiciona internamente cada página */
      pointer-events: all !important;
    }
    :global(.pdfslick-container .textLayer span) {
      user-select: text !important;
    }
  </style>