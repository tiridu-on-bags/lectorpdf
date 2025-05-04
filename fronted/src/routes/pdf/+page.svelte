<!-- src/routes/pdf/+page.svelte -->
<script lang="ts">
  // Importamos el componente y el store
  import PdfJsViewer from '$lib/components/PdfJsViewer.svelte';
  // import { pdfStore } from '$lib/stores/pdf-state'; // Comentado - Archivo no encontrado
  
  let file: File | null = null;
  let isUploading = false;
  let uploadError = '';
  
  // Usar el store para obtener la URL
  // $: pdfUrl = $pdfStore.url; // Comentado - pdfStore no está definido
  let pdfUrl: string | null = null; // Usaremos una variable local en su lugar
  
  async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    const selectedFile = input.files?.[0] || null;
    
    if (!selectedFile || selectedFile.type !== 'application/pdf') {
      uploadError = 'Por favor selecciona un archivo PDF válido';
      return;
    }
    
    file = selectedFile;
    isUploading = true;
    uploadError = '';
    
    // Resetear el store al empezar una nueva carga
    // pdfStore.reset(); // Comentado - pdfStore no está definido
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      console.log('Iniciando subida de archivo...');
      console.log('Detalles del archivo:', {
        nombre: file.name,
        tamaño: file.size,
        tipo: file.type
      });
      
      // Usar la URL directa del backend
      const endpoint = 'http://localhost:8000/api/upload-pdf';
      console.log('Endpoint de subida:', endpoint);
      
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData
      });
      
      console.log('Estado de la respuesta:', response.status);
      console.log('Headers de la respuesta:', Object.fromEntries(response.headers.entries()));
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Error desconocido' }));
        console.error('Error detallado:', errorData);
        throw new Error(`Error al subir el archivo: ${response.status} - ${errorData.detail}`);
      }
      
      const data = await response.json();
      console.log('Respuesta completa del servidor:', data);
      
      if (!data.url) {
        throw new Error('No se recibió URL del archivo en la respuesta');
      }
      
      // Cargar el PDF en el store y notificar éxito
      const fullUrl = `http://localhost:8000${data.url}`;
      console.log('PDF cargado exitosamente:', fullUrl);
      isUploading = false;
      
      // Verificar URL y cargar PDF
      if (await checkUrl(fullUrl)) {
        // pdfStore.loadPdf(fullUrl); // Comentado - pdfStore no está definido
        pdfUrl = fullUrl; // Asignar a la variable local
      } else {
        throw new Error('La URL del PDF no es accesible');
      }
      
    } catch (error) {
      console.error('Error en la subida:', error);
      uploadError = error instanceof Error ? error.message : 'Error desconocido al subir el archivo';
      isUploading = false;
      file = null;
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
  
  <!-- Contenedor principal para el visor de PDF a pantalla completa -->
  <main class="flex-1 relative bg-gray-100 overflow-hidden">
    {#if pdfUrl}
      <div class="absolute inset-x-0 top-0 bg-white bg-opacity-80 p-1 text-xs text-blue-600 z-10 break-all">
        URL: {pdfUrl}
      </div>
      
      <div class="w-full h-full">
        <PdfJsViewer {pdfUrl} />
      </div>
    {:else}
      <div class="flex flex-col justify-center items-center h-full text-center p-5">
        <p class="text-2xl text-gray-700 mb-2.5">Selecciona un archivo PDF para comenzar</p>
        <p class="text-lg text-gray-500">Usa el Lápiz Inteligente para interactuar con el contenido</p>
      </div>
    {/if}
  </main>
</div>