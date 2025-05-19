<!-- src/lib/components/PDFSlickViewer.svelte -->
<script lang="ts">
    import { onMount, onDestroy, tick, createEventDispatcher } from 'svelte';
    // Eliminar importación estática
    // import { create, PDFSlick } from "@pdfslick/core";
    
    // Import only GlobalWorkerOptions needed
    import { GlobalWorkerOptions } from 'pdfjs-dist';
    import '@pdfslick/core/dist/pdf_viewer.css';
    
    export let pdfUrl: string | null = null;
    export let onLoad: () => void = () => {};
    
    // Event dispatcher para emitir eventos desde este componente
    const dispatch = createEventDispatcher();
    
    let container: HTMLDivElement; // Elemento contenedor principal
    let pdfSlick: any | null = null;
    let store: any;
    let pageNumber = 1;
    let numPages = 0;
    let scaleValue: string | undefined;
    
    let unsubscribe: (() => void) | undefined;
    let RO: ResizeObserver;
    
    // Función para manejar la selección de texto
    function setupTextSelectionHandling() {
        if (!container) return;
        
        // Manejador del evento mouseup para capturar texto seleccionado
        const handleTextSelection = () => {
            const selection = window.getSelection();
            if (!selection || selection.isCollapsed || !selection.toString().trim()) return;
            
            const text = selection.toString().trim();
            
            // Obtener la posición de la selección
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();
            
            // Calcular la posición relativa al visor
            const containerRect = container.getBoundingClientRect();
            const position = {
                left: rect.left - containerRect.left,
                top: rect.top - containerRect.top,
                width: rect.width,
                height: rect.height
            };
            
            // Despachar el evento con el texto seleccionado y su posición
            dispatch('textselected', { text, position });
            
            console.log('Texto seleccionado:', text, position);
        };
        
        // Agregar el event listener al contenedor
        container.addEventListener('mouseup', handleTextSelection);
        
        // Devolver una función para limpiar el event listener
        return () => {
            container.removeEventListener('mouseup', handleTextSelection);
        };
    }

    async function initializePdfViewer() {
        try {
            // Asegurar que el DOM esté actualizado
            await tick();

            // Importar dinámicamente PDFSlick
            const pdfSlickCore = await import('@pdfslick/core');
            const { create, PDFSlick } = pdfSlickCore;

            // Usar CDN para el worker
            GlobalWorkerOptions.workerSrc = 'https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.js';
            
            console.log("Worker URL set to:", GlobalWorkerOptions.workerSrc);

            // Crear el store si no existe
            if (!store) {
                store = create();
                unsubscribe = store.subscribe(state => {
                    pageNumber = state.pageNumber;
                    numPages = state.numPages;
                    scaleValue = state.scaleValue;
                    if (state.pdfSlick && state.pdfSlick !== pdfSlick) {
                        pdfSlick = state.pdfSlick;
                    }
                });
            }

            // Inicializar la instancia de PDFSlick
            if (container && store && !pdfSlick) {
                console.log("PDFSlickViewer: Initializing PDFSlick instance. Container:", container);
                console.log("PDFSlickViewer: Container position:", window.getComputedStyle(container).position);
                
                try {
                    pdfSlick = new PDFSlick({
                        container,
                        store,
                        options: {
                            scaleValue: 'page-fit',
                            textLayerMode: 2
                        }
                    });
                    
                    console.log("PDFSlickViewer: PDFSlick instance created.");
                    store.setState({ pdfSlick });
                    
                    // Configurar el observador de redimensionamiento
                    RO = new ResizeObserver(() => {
                        if (scaleValue && ['page-width', 'page-fit', 'auto'].includes(scaleValue)) {
                            pdfSlick.viewer.currentScaleValue = scaleValue;
                        }
                    });
                    RO.observe(container);
                    
                    // Configurar el manejo de selección de texto
                    const textSelectionCleanup = setupTextSelectionHandling();
                    
                    // Almacenar la función de limpieza
                    const originalCleanup = pdfSlick._cleanup || (() => {});
                    pdfSlick._cleanup = () => {
                        textSelectionCleanup();
                        originalCleanup();
                    };
                    
                } catch (error: any) {
                    console.error("PDFSlickViewer: Error creating PDFSlick instance:", error);
                    console.error("Error details:", error.stack);
                    alert(`Error initializing PDF viewer: ${error.message}`);
                    cleanupPdfViewer();
                }
            } else if (pdfSlick) {
                console.log("PDFSlickViewer: PDFSlick instance already exists.");
                if (store.getState().pdfSlick !== pdfSlick) {
                     store.setState({ pdfSlick });
                }
            } else {
                console.warn("PDFSlickViewer: DOM elements or store not available for initialization.", { container });
            }

        } catch (error: any) {
            console.error("PDFSlickViewer: Error in initializePdfViewer:", error);
            console.error("Error details:", error.stack);
            alert(`Error loading PDF viewer dependencies or during setup: ${error.message}`);
            cleanupPdfViewer();
        }
    }

    async function loadPdfDocument(url: string) {
        if (!pdfSlick) {
            console.warn("PDFSlickViewer: Attempted to load document before pdfSlick is initialized.");
            await initializePdfViewer();
            if (!pdfSlick) {
                console.error("PDFSlickViewer: Initialization failed, cannot load document.");
                return;
            }
        }

        console.log(`PDFSlickViewer: Loading document from ${url}`);
        try {
            await pdfSlick.loadDocument(url);
            console.log('PDFSlickViewer: Document loaded successfully.');
            onLoad();
        } catch (error: any) {
            console.error("PDFSlickViewer: Error loading PDF document:", error);
            console.error("Error details:", error.stack);
            alert(`Error loading PDF: ${error.message}`);
            cleanupPdfViewer();
            if (store) {
                store.setState({ pdfSlick: null, numPages: 0, pageNumber: 1 });
            }
        }
    }

    function cleanupPdfViewer() {
        console.log("PDFSlickViewer: Cleaning up.");
        if (pdfSlick) {
            pdfSlick._cleanup?.();
            pdfSlick = null;
        }
        if (RO) {
            RO.disconnect();
        }
        console.log("PDFSlickViewer: Cleanup finished.");
    }

    function prevPage() { 
        if (pdfSlick && pageNumber > 1) pdfSlick.gotoPage(pageNumber - 1); 
    }
    
    function nextPage() { 
        if (pdfSlick && pageNumber < numPages) pdfSlick.gotoPage(pageNumber + 1); 
    }
    
    function zoomOut() { 
        if (pdfSlick) pdfSlick.decreaseScale(); 
    }
    
    function zoomIn() { 
        if (pdfSlick) pdfSlick.increaseScale(); 
    }

    onMount(() => {
        console.log("PDFSlickViewer: Component mounted.");
        initializePdfViewer();
    });

    onDestroy(() => {
        console.log("PDFSlickViewer: Component will be destroyed.");
        cleanupPdfViewer();
        if (unsubscribe) {
            unsubscribe();
            unsubscribe = undefined;
        }
        console.log("PDFSlickViewer: Component cleanup complete.");
    });

    $: if (pdfUrl) {
        console.log("PDFSlickViewer: Reactive block: pdfUrl changed:", pdfUrl);
        loadPdfDocument(pdfUrl);
    } else {
        console.log("PDFSlickViewer: Reactive block: pdfUrl is null.");
        cleanupPdfViewer();
        if (store) {
            store.setState({ pdfSlick: null, numPages: 0, pageNumber: 1 });
        }
    }
</script>

<div class="absolute inset-0 bg-slate-200/70 pdfSlick">
  <div class="flex-1 relative h-full">
    <div id="viewerContainer" class="absolute inset-0 overflow-auto" bind:this={container}>
      <div id="viewer" class="pdfViewer"></div>
    </div>
  </div>

  <!-- Controles de paginación y zoom -->
  <div class="fixed w-full h-12 bottom-0 right-0 z-50 pointer-events-none flex justify-between items-center px-2">
    <div></div>
    <div class="flex justify-center">
      <div class="inline-flex rounded shadow-sm justify-center border border-slate-300 bg-white divide-x divide-x-slate-100">
        <button 
          on:click={prevPage} 
          disabled={pageNumber <= 1} 
          type="button"
          class="relative inline-flex items-center rounded-l px-2 py-2 text-slate-500 ring-0 ring-inset ring-slate-700 hover:bg-slate-50 enabled:hover:text-slate-900 transition-all focus:z-10 disabled:opacity-70 pointer-events-auto"
        >
          <span class="sr-only">Anterior</span>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="h-5 w-5">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M5.92803 7.97603L10.2853 12.3333L9.66662 12.9521L4.99995 8.28539V7.66667L9.66662 3L10.2853 3.61872L5.92803 7.97603Z" />
          </svg>
        </button>
        <button 
          on:click={zoomOut} 
          type="button"
          class="relative inline-flex items-center px-2 py-2 text-slate-500 ring-0 ring-inset ring-slate-700 hover:bg-slate-50 enabled:hover:text-slate-900 transition-all focus:z-10 pointer-events-auto disabled:opacity-70"
        >
          <span class="sr-only">Zoom Out</span>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="h-5 w-5">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M12.0275 6.14861C12.1231 7.56649 11.6682 8.96661 10.7575 10.0575L15.0175 14.3176L14.3176 15.0275L10.0575 10.7575C8.96661 11.6682 7.56649 12.1231 6.14861 12.0275C4.73072 11.9319 3.40437 11.2931 2.44561 10.2442C1.48684 9.19523 0.969494 7.81691 1.00139 6.39617C1.03329 4.97542 1.61188 3.62162 2.61675 2.61675C3.62162 1.61188 4.97542 1.03329 6.39617 1.00139C7.81691 0.969494 9.19523 1.48684 10.2442 2.44561C11.2931 3.40437 11.9319 4.73072 12.0275 6.14861ZM6.57756 11.0375C7.77042 11.0354 8.91377 10.5608 9.7575 9.71758L9.71758 9.7376C10.1447 9.32074 10.4849 8.82316 10.7183 8.27385C10.9518 7.72455 11.0739 7.13437 11.0776 6.53752C11.0776 5.64751 10.8136 4.77755 10.3191 4.03752C9.82467 3.2975 9.12188 2.72065 8.29961 2.38005C7.47734 2.03946 6.57255 1.95032 5.69963 2.12395C4.82672 2.29758 4.02489 2.72618 3.39556 3.35552C2.76622 3.98485 2.33762 4.78668 2.16399 5.6596C1.99036 6.53251 2.0795 7.4373 2.42009 8.25957C2.76069 9.08184 3.33742 9.78464 4.07744 10.2791C4.81746 10.7736 5.68755 11.0375 6.57756 11.0375ZM4.03748 6.0575H9.03748V7.0575H4.03748V6.0575Z" />
          </svg>
        </button>
        <div class="relative inline-flex items-center px-2 py-2 text-slate-500 pointer-events-auto">
          <span class="text-sm">Página {pageNumber} de {numPages}</span>
        </div>
        <button 
          on:click={zoomIn} 
          type="button"
          class="relative inline-flex items-center px-2 py-2 text-slate-500 ring-0 ring-inset ring-slate-700 hover:bg-slate-50 enabled:hover:text-slate-900 transition-all focus:z-10 pointer-events-auto disabled:opacity-70"
        >
          <span class="sr-only">Zoom In</span>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="h-5 w-5">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M12.0275 6.14861C12.1231 7.56649 11.6682 8.96661 10.7575 10.0575L15.0175 14.3176L14.3176 15.0275L10.0575 10.7575C8.96661 11.6682 7.56649 12.1231 6.14861 12.0275C4.73072 11.9319 3.40437 11.2931 2.44561 10.2442C1.48684 9.19523 0.969494 7.81691 1.00139 6.39617C1.03329 4.97542 1.61188 3.62162 2.61675 2.61675C3.62162 1.61188 4.97542 1.03329 6.39617 1.00139C7.81691 0.969494 9.19523 1.48684 10.2442 2.44561C11.2931 3.40437 11.9319 4.73072 12.0275 6.14861ZM6.57756 11.0375C7.77042 11.0354 8.91377 10.5608 9.7575 9.71758L9.71758 9.7376C10.1447 9.32074 10.4849 8.82316 10.7183 8.27385C10.9518 7.72455 11.0739 7.13437 11.0776 6.53752C11.0776 5.64751 10.8136 4.77755 10.3191 4.03752C9.82467 3.2975 9.12188 2.72065 8.29961 2.38005C7.47734 2.03946 6.57255 1.95032 5.69963 2.12395C4.82672 2.29758 4.02489 2.72618 3.39556 3.35552C2.76622 3.98485 2.33762 4.78668 2.16399 5.6596C1.99036 6.53251 2.0795 7.4373 2.42009 8.25957C2.76069 9.08184 3.33742 9.78464 4.07744 10.2791C4.81746 10.7736 5.68755 11.0375 6.57756 11.0375ZM9.01749 7.0376V6.0376H7.01749V4.0376H6.01749V6.0376H4.01749V7.0376H6.01749V9.0376H7.01749V7.0376H9.01749Z" />
          </svg>
        </button>
        <button 
          on:click={nextPage} 
          disabled={pageNumber >= numPages}
          type="button"
          class="relative inline-flex items-center rounded-r px-2 py-2 text-slate-500 ring-0 ring-inset ring-slate-700 hover:bg-slate-50 enabled:hover:text-slate-900 transition-all focus:z-10 disabled:opacity-70 pointer-events-auto"
        >
          <span class="sr-only">Siguiente</span>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" class="h-5 w-5">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M10.0718 8.02397L5.71454 3.66666L6.33326 3.04794L10.9999 7.71461V8.33333L6.33326 13L5.71454 12.3813L10.0718 8.02397Z" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</div>

<style>
  /* Estilos específicos solo si son necesarios */
</style>