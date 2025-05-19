```html
<!-- fronted/src/routes/pdf/+page.svelte -->
<script lang="ts">
  // Importamos el componente y el store
  import ContextualPdfViewer from '$lib/components/ContextualPdfViewer.svelte';
  
  let file: File | null = null;
  let isUploading = false;
  let uploadError = '';
  
  // Variable para almacenar los datos binarios del PDF cargado localmente
  let pdfData: ArrayBuffer | null = null;
  
  // Estado para el texto seleccionado
  let selectedText = '';
  let selectionPosition: {left: number; top: number; width: number; height: number} | null = null;
  let showSelectionIndicator = false;
  
  // Inicializar el tracker de mouse
  let mouseTracker: { destroy: () => void } | null = null;
  
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
    
    // Iniciar el rastreo del mouse
    // mouseTracker = mousePosition.init(); // Eliminado: depende de mousePosition
    
    // Retornar función de limpieza
    return () => {
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
    pdfData = null; // Limpiar datos anteriores
    
    const reader = new FileReader();

    reader.onload = (e) => {
        if (e.target?.result instanceof ArrayBuffer) {
            pdfData = e.target.result; // Almacenar los datos binarios
            isUploading = false; // Marcar como no cargando después de leer el archivo
        } else {
            uploadError = 'Error al leer el archivo como ArrayBuffer';
            isUploading = false;
        }
    };

    reader.onerror = () => {
        uploadError = 'Error al leer el archivo';
        isUploading = false;
    };

    reader.readAsArrayBuffer(selectedFile); // Leer como ArrayBuffer
    
    // La lógica original de subida al backend via pdfStore.uploadPDF(file) 
    // se remueve o comenta si solo nos enfocamos en la carga local por ahora.
    // Si necesitas subir también, esa lógica debería estar separada 
    // de la lectura local para visualización.
    // try {
    //   await pdfStore.uploadPDF(file);
    //   isUploading = false;
    // } catch (error) {
    //   uploadError = error instanceof Error ? error.message : 'Error desconocido';
    //   isUploading = false;
    // }
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
          Leyendo archivo...
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
    <div class="pdf-view-container">
      <ContextualPdfViewer pdfData={pdfData} on:textselected={handleTextSelected}/>
    </div>
  </main>

  <!-- Panel para mostrar texto seleccionado -->
  {#if selectedText && selectionPosition}
    <div 
      class="fixed z-50 bg-white rounded-lg shadow-lg p-3 pointer-events-none transform -translate-x-1/2 border-2 border-blue-400"
      style="
        left: {selectionPosition.left + selectionPosition.width / 2}px;
        top: {selectionPosition.top + selectionPosition.height}px;
        max-width: 300px;
      "
    >
      <div class="text-lg font-medium text-gray-900">{selectedText}</div>
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
  /*
  :global(.precision-selection-mode) :global(.text-layer > span:hover) {
    background-color: rgba(59, 130, 246, 0.2) !important;
    outline: 1px solid rgba(59, 130, 246, 0.5);
    cursor: text;
  }
  */
  
  .page-indicator {
    font-size: 14px;
    color: #555;
  }
</style>

