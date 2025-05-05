<!-- src/routes/pdf/+page.svelte -->
<script lang="ts">
  // Importamos el componente y el store
  import PDFViewer from '$lib/components/PDFViewer.svelte';
  import { mousePosition } from '$lib/stores/mouse-position';
  import type { MousePosition } from '$lib/stores/mouse-position';
  import { pdfStore } from '$lib/stores/pdf-store';
  
  let file: File | null = null;
  let isUploading = false;
  let uploadError = '';
  
  // Usar el store para obtener la URL
  // $: pdfUrl = $pdfStore.url; // Comentado - pdfStore no está definido
  let pdfUrl: string | null = null; // Usaremos una variable local en su lugar
  
  // Estado para el texto seleccionado
  let selectedText = '';
  let selectionPosition: {left: number; top: number; width: number; height: number} | null = null;
  let showSelectionIndicator = false;
  
  // Inicializar el tracker de mouse
  let mouseTracker: { destroy: () => void } | null = null;
  let coords: MousePosition = { 
    x: 0, y: 0, 
    startX: 0, startY: 0, 
    relativeX: 0, relativeY: 0,
    relativeStartX: 0, relativeStartY: 0,
    targetElement: null,
    isSelecting: false,
    scrollX: 0, scrollY: 0
  };
  
  // Estado para la lupa de selección
  let magnifierActive = false;
  let magnifierPosition = { x: 0, y: 0 };
  let magnifierContent = '';
  
  // Manejar la selección de texto del PDF
  function handleTextSelected(event: CustomEvent) {
    const { text, position } = event.detail;
    selectedText = text;
    selectionPosition = position;
    showSelectionIndicator = true;
    
    // Ocultar el indicador después de 3 segundos
    setTimeout(() => {
      showSelectionIndicator = false;
    }, 3000);
    
    console.log('Texto seleccionado:', text);
    console.log('Posición:', position);
  }
  
  // Función para inicializar el rastreo del mouse cuando se carga la página
  function initMouseTracking() {
    if (typeof window === 'undefined') return;
    
    // Usar el store global de posición del mouse
    const unsubscribe = mousePosition.subscribe(value => {
      coords = value;
    });
    
    // Iniciar el rastreo del mouse
    mouseTracker = mousePosition.init();
    
    // Retornar función de limpieza
    return () => {
      unsubscribe();
      mouseTracker?.destroy();
    };
  }
  
  async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    const selectedFile = input.files?.[0] || null;
    
    if (!selectedFile) return;
    file = selectedFile;
    
    isUploading = true;
    uploadError = '';
    
    try {
      await pdfStore.uploadPDF(file);
      isUploading = false;
    } catch (error) {
      uploadError = error instanceof Error ? error.message : 'Error desconocido';
      isUploading = false;
    }
  }
  
  // Función para verificar si una URL es válida y accesible
  async function checkUrl(url: string): Promise<boolean> {
    try {
      const response = await fetch(url, { method: 'HEAD' });
      console.log('URL del PDF verificada:', response.ok);
      return response.ok;
    } catch (error) {
      console.error('Error verificando URL:', error);
      return false;
    }
  }
  
  // Iniciar el rastreador de mouse cuando el componente se monta
  import { onMount, onDestroy } from 'svelte';
  
  let cleanup: (() => void) | null = null;
  
  onMount(() => {
    cleanup = initMouseTracking();
  });
  
  onDestroy(() => {
    if (cleanup) cleanup();
  });
  
  // Función para activar/desactivar la lupa
  function toggleMagnifier() {
    magnifierActive = !magnifierActive;
  }
  
  // Función para actualizar la posición de la lupa
  function updateMagnifierPosition() {
    if (!magnifierActive) return;
    
    magnifierPosition = {
      x: coords.x,
      y: coords.y - 120 // Offset para que no tape el cursor
    };
    
    // Intentar obtener el texto cercano al cursor
    setTimeout(() => {
      const selection = window.getSelection();
      if (selection && selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const tempRange = range.cloneRange();
        
        // Expandir para capturar algo de contexto
        try {
          // Encontrar los límites de la palabra manualmente
          const startNode = tempRange.startContainer;
          let startOffset = tempRange.startOffset;
          let textContent = startNode.textContent || '';
          
          // Buscar hacia atrás hasta el espacio o inicio del texto
          while (startOffset > 0 && !/\s/.test(textContent.charAt(startOffset - 1))) {
            startOffset--;
          }
          
          // Moverse al final de la palabra
          const endNode = tempRange.endContainer;
          let endOffset = tempRange.endOffset;
          textContent = endNode.textContent || '';
          
          // Buscar hacia adelante hasta el espacio o final del texto
          while (endOffset < textContent.length && !/\s/.test(textContent.charAt(endOffset))) {
            endOffset++;
          }
          
          // Aplicar el nuevo rango expandido a palabras completas
          tempRange.setStart(startNode, startOffset);
          tempRange.setEnd(endNode, endOffset);
          
          magnifierContent = tempRange.toString().trim();
        } catch (e) {
          // Si expand falla, usar el texto bajo el cursor
          const element = document.elementFromPoint(coords.x, coords.y);
          if (element) magnifierContent = element.textContent?.substring(0, 50) || '';
        }
      }
    }, 50);
  }
  
  // Actualizar la lupa cuando el mouse se mueve
  $: if (magnifierActive && coords) {
    updateMagnifierPosition();
  }
</script>

<div class="flex flex-col h-full w-full overflow-hidden">
  <header class="p-2.5 bg-gray-100 border-b border-gray-200 flex justify-between items-center flex-shrink-0">
    <h1 class="text-xl text-gray-800 m-0">Visor de PDF con Lápiz Inteligente</h1>
    
    <div class="flex items-center gap-2.5">
      <input 
        type="file" 
        accept="application/pdf" 
        on:change={handleFileUpload}
        id="pdf-upload"
        class="hidden"
        disabled={isUploading}
      />
      <label for="pdf-upload" class="px-4 py-2 bg-blue-600 text-white rounded cursor-pointer font-medium text-sm">
        {#if isUploading}
          Procesando...
        {:else}
          Seleccionar PDF
        {/if}
      </label>
      
      {#if file}
        <span class="text-sm text-gray-700">{file.name}</span>
      {/if}
      
      {#if uploadError}
        <div class="bg-red-50 text-red-700 px-3 py-1.5 rounded text-sm">{uploadError}</div>
      {/if}
    </div>
  </header>
  
  <!-- Contenedor principal para el visor de PDF -->
  <main class="flex-1 relative bg-gray-100 overflow-hidden">
    {#if $pdfStore.url}
      <div class="absolute inset-x-0 top-0 bg-white bg-opacity-80 p-1 text-xs text-blue-600 z-10 break-all">
        URL: {$pdfStore.url}
      </div>
      
      <!-- Panel para mostrar texto seleccionado -->
      {#if selectedText}
        <div class="absolute bottom-0 left-0 right-0 bg-white bg-opacity-90 p-3 shadow-lg z-20 border-t border-gray-300">
          <h3 class="text-sm font-medium text-gray-700 mb-1">Texto seleccionado:</h3>
          <p class="text-sm text-gray-900 bg-blue-50 p-2 rounded border border-blue-200">{selectedText}</p>
          <button 
            class="absolute top-2 right-2 text-gray-500 hover:text-gray-700" 
            on:click={() => selectedText = ''}>
            ✕
          </button>
        </div>
      {/if}
      
      <!-- Indicador visual de selección -->
      {#if showSelectionIndicator && selectionPosition}
        <div 
          class="absolute z-20 bg-blue-500 bg-opacity-20 border-2 border-blue-500 pointer-events-none" 
          style="
            left: {selectionPosition.left}px; 
            top: {selectionPosition.top}px; 
            width: {selectionPosition.width}px; 
            height: {selectionPosition.height}px;
          ">
        </div>
      {/if}
      
      <!-- Indicador de mouse durante selección -->
      {#if coords.isSelecting}
        <div 
          class="mouse-selection-indicator absolute z-10 pointer-events-none"
          style="
            left: {coords.relativeStartX}px;
            top: {coords.relativeStartY}px;
            width: {Math.abs(coords.relativeX - coords.relativeStartX)}px;
            height: {Math.abs(coords.relativeY - coords.relativeStartY)}px;
            transform: translate({Math.min(0, coords.relativeX - coords.relativeStartX)}px, 
                                {Math.min(0, coords.relativeY - coords.relativeStartY)}px);
          "
        ></div>
      {/if}
      
      <div class="w-full h-full">
        <PDFViewer url={$pdfStore.url} />
      </div>
    {:else}
      <div class="flex flex-col justify-center items-center h-full text-center p-5">
        <p class="text-2xl text-gray-700 mb-2.5">Selecciona un archivo PDF para comenzar</p>
        <p class="text-lg text-gray-500">Usa el Lápiz Inteligente para interactuar con el contenido</p>
      </div>
    {/if}
  </main>

  <!-- Herramientas de selección precisas -->
  {#if $pdfStore.url}
    <div class="absolute top-16 right-4 z-20 bg-white shadow-lg rounded-lg overflow-hidden">
      <div class="p-2 flex flex-col space-y-2">
        <button 
          class="p-2 rounded hover:bg-blue-100 text-sm flex items-center space-x-2 {magnifierActive ? 'bg-blue-100 text-blue-700' : ''}"
          title="Activar lupa para selección más precisa"
          on:click={toggleMagnifier}
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
          </svg>
          <span>Lupa de precisión</span>
        </button>
      </div>
    </div>
  {/if}
  
  <!-- Lupa de selección -->
  {#if magnifierActive && coords.x > 0}
    <div 
      class="fixed z-50 bg-white rounded-lg shadow-lg p-3 pointer-events-none transform -translate-x-1/2 border-2 border-blue-400"
      style="
        left: {magnifierPosition.x}px;
        top: {magnifierPosition.y}px;
        max-width: 300px;
      "
    >
      <div class="text-lg font-medium text-gray-900">{magnifierContent || 'Posicione el cursor sobre el texto'}</div>
      <div class="text-xs text-gray-500 mt-1">Coordenadas: {Math.round(coords.relativeX)}, {Math.round(coords.relativeY)}</div>
    </div>
  {/if}

  <!-- Modo de debug (solo visible durante desarrollo) -->
  {#if import.meta.env.DEV && false}
    <div class="fixed bottom-0 right-0 bg-black bg-opacity-70 text-white p-2 text-xs font-mono z-50 pointer-events-none">
      Mouse: X:{Math.round(coords.x)}, Y:{Math.round(coords.y)}<br/>
      Rel: X:{Math.round(coords.relativeX)}, Y:{Math.round(coords.relativeY)}<br/>
      Start: X:{Math.round(coords.relativeStartX)}, Y:{Math.round(coords.relativeStartY)}<br/>
      Selecting: {coords.isSelecting ? 'Sí' : 'No'}<br/>
      Scroll: X:{coords.scrollX}, Y:{coords.scrollY}
    </div>
  {/if}
</div>

<style>
  /* Animación para hacer más visible la selección */
  @keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
    100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
  }
  
  :global(.highlight-selection) {
    animation: pulse 2s infinite;
    background-color: rgba(59, 130, 246, 0.3);
    border-radius: 3px;
  }
  
  :global(.text-layer .highlight) {
    background-color: rgba(59, 130, 246, 0.3) !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
    border-radius: 2px;
    opacity: 1 !important;
    color: transparent !important;
  }
  
  .mouse-selection-indicator {
    background-color: rgba(59, 130, 246, 0.2);
    border: 1px dashed rgba(59, 130, 246, 0.8);
    opacity: 0.7;
    mix-blend-mode: multiply;
  }
  
  /* Estilos para el modo de selección precisa */
  :global(.precision-selection-mode) :global(.text-layer > span:hover) {
    background-color: rgba(59, 130, 246, 0.2) !important;
    outline: 1px solid rgba(59, 130, 246, 0.5);
    cursor: text;
  }
</style>