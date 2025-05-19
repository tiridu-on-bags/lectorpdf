<!-- src/routes/pdf/+page.svelte -->
<script lang="ts">
  // Importamos el componente y el store
  // import ContextualPdfViewer from '$lib/components/ContextualPdfViewer.svelte'; // Eliminar importación
  
  import PDFSlickViewer from '$lib/components/PDFSlickViewer.svelte'; // Importamos el componente visor
  
  let file: File | null = null;
  let isReadingFile = false;
  let readingError = '';
  
  // Variable para almacenar los datos binarios del PDF cargado localmente
  let pdfData: ArrayBuffer | null = null;
  
  // Variable para almacenar la URL del objeto para el visor PDFSlick
  let pdfObjectUrl: string | null = null;
  
  // Estado para el texto seleccionado
  let selectedText = '';
  let selectionPosition: {left: number; top: number; width: number; height: number} | null = null;
  
  // Función para manejar el evento de texto seleccionado (aún por implementar en PDFSlickViewer)
  function handleTextSelected(event: CustomEvent) {
    const { text, position } = event.detail;
    selectedText = text;
    selectionPosition = position;
    
    console.log('Texto seleccionado:', text);
    console.log('Posición:', position);
  }
  
  // Manejador de carga de archivos
  async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    const selectedFile = input.files?.[0] || null;
    
    if (!selectedFile) return;
    file = selectedFile;
    
    isReadingFile = true;
    readingError = '';
    
    // Limpiar datos anteriores y revocar URL de objeto si existe
    if (pdfObjectUrl) {
      URL.revokeObjectURL(pdfObjectUrl);
      pdfObjectUrl = null;
    }
    pdfData = null;
    
    try {
      // Leer el archivo como ArrayBuffer
      const arrayBuffer = await readFileAsArrayBuffer(selectedFile);
      pdfData = arrayBuffer;
      
      // Crear una URL de objeto a partir del ArrayBuffer
      const blob = new Blob([arrayBuffer], { type: 'application/pdf' });
      pdfObjectUrl = URL.createObjectURL(blob);
      
      console.log('PDF cargado como objeto URL:', pdfObjectUrl);
      isReadingFile = false;
    } catch (error) {
      console.error('Error al leer el archivo:', error);
      readingError = error instanceof Error ? error.message : 'Error al leer el archivo';
      isReadingFile = false;
    }
  }
  
  // Función para leer un archivo como ArrayBuffer usando Promise
  function readFileAsArrayBuffer(file: File): Promise<ArrayBuffer> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = () => {
        if (reader.result instanceof ArrayBuffer) {
          resolve(reader.result);
        } else {
          reject(new Error('Error al leer el archivo como ArrayBuffer'));
        }
      };
      
      reader.onerror = () => {
        reject(new Error('Error al leer el archivo'));
      };
      
      reader.readAsArrayBuffer(file);
    });
  }
  
  // Manejador para cuando el PDF se carga correctamente
  function handlePdfLoaded() {
    console.log('PDF cargado correctamente');
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
  
  // Revocar la URL de objeto cuando el componente se destruye
  onDestroy(() => {
    if (pdfObjectUrl) {
      URL.revokeObjectURL(pdfObjectUrl);
      pdfObjectUrl = null;
      console.log('PDF Object URL revoked.');
    }
  });
</script>

<div class="flex flex-col h-screen w-full overflow-hidden">
  <header class="p-2.5 bg-gray-100 border-b border-gray-200 flex justify-between items-center z-10">
    <h1 class="text-xl text-gray-800 m-0">Visor de PDF</h1>
    
    <div class="flex items-center gap-2.5">
      <input 
        type="file" 
        accept="application/pdf" 
        on:change={handleFileUpload}
        id="pdf-upload"
        class="hidden"
        disabled={isReadingFile}
      />
      <label for="pdf-upload" class="px-4 py-2 bg-blue-600 text-white rounded cursor-pointer font-medium text-sm">
        {#if isReadingFile}
          Leyendo archivo...
        {:else}
          Seleccionar PDF
        {/if}
      </label>
      
      {#if file}
        <span class="text-sm text-gray-700">{file.name}</span>
      {/if}
      
      {#if readingError}
        <div class="bg-red-50 text-red-700 px-3 py-1.5 rounded text-sm">{readingError}</div>
      {/if}
    </div>
  </header>
  
  <!-- Contenedor principal para el visor de PDF -->
  <main class="flex-1 relative">
    {#if pdfObjectUrl}
      <!-- Es importante que el div contenedor tenga posición RELATIVA para que el contenedor absoluto de PDFSlick funcione -->
      <div class="h-full w-full relative">
        <PDFSlickViewer 
          pdfUrl={pdfObjectUrl} 
          onLoad={handlePdfLoaded} 
          on:textselected={handleTextSelected} 
        />
      </div>
    {:else}
      <!-- Mostramos un placeholder si no hay PDF cargado -->
      <div class="flex items-center justify-center h-full w-full text-gray-500 text-xl bg-gray-100">
        <p>Selecciona un archivo PDF para visualizar.</p>
      </div>
    {/if}
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
  :global(.pdfSlickViewer) {
    position: absolute !important;
  }
  
  /* Estilos para resaltar el texto seleccionado */
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
  
  /* Estilos para el modo de selección precisa */
  /*
  :global(.precision-selection-mode) :global(.text-layer > span:hover) {
    background-color: rgba(59, 130, 246, 0.2) !important;
    outline: 1px solid rgba(59, 130, 246, 0.5);
    cursor: text;
  }
  */
  
  .pdf-view-container {
    /* Altura y ancho ya definidos arriba */
    position: relative;
  }
</style>
