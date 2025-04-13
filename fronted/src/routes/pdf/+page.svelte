<!-- src/routes/pdf/+page.svelte -->
<script lang="ts">
  // IMPORTANTE: Importar los estilos CSS de PDFSlick
  import "@pdfslick/core/dist/pdf_viewer.css";
  import { onMount } from 'svelte';
  import ContextualPdfViewer from '$lib/components/ContextualPdfViewer.svelte';
  
  let pdfUrl: string | null = null;
  let file: File | null = null;
  let isUploading = false;
  let uploadError = '';
  let documentId = '';
  let pdfLoaded = false;
  
  // Registrar cambios en pdfUrl para depuración
  $: if (pdfUrl) {
    console.log('pdfUrl actualizada:', pdfUrl);
  }
  
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
    pdfUrl = null;
    
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
      
      pdfUrl = `http://localhost:8000${data.url}`;
      documentId = data.document_id || '';
      pdfLoaded = true;
      isUploading = false;
      console.log('PDF cargado exitosamente:', pdfUrl);
      
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
      return response.ok;
    } catch (error) {
      console.error('Error verificando URL:', error);
      return false;
    }
  }
  
  // Verificar la URL del PDF cuando cambie
  $: if (pdfUrl) {
    checkUrl(pdfUrl).then(isValid => {
      if (!isValid) {
        console.error('La URL del PDF no es accesible:', pdfUrl);
      } else {
        console.log('URL del PDF verificada y accesible');
      }
    });
  }
</script>

<div class="container">
  <header class="header">
    <h1>Visor de PDF con Lápiz Inteligente</h1>
    
    <div class="upload-section">
      <input 
        type="file" 
        accept="application/pdf" 
        on:change={handleFileUpload}
        id="pdf-upload"
        class="file-input"
        disabled={isUploading}
      />
      <label for="pdf-upload" class="file-label">
        {#if isUploading}
          Procesando...
        {:else}
          Seleccionar PDF
        {/if}
      </label>
      
      {#if file}
        <span class="file-name">{file.name}</span>
      {/if}
      
      {#if uploadError}
        <div class="error-message">{uploadError}</div>
      {/if}
    </div>
  </header>
  
  <!-- Contenedor principal para el visor de PDF a pantalla completa -->
  <main class="pdf-container">
    {#if pdfUrl}
      <div class="debug-bar">
        URL: {pdfUrl}
      </div>
    {/if}
    
    <!-- Reemplazamos SimplePDFViewer por ContextualPdfViewer -->
    {#if pdfUrl}
      <ContextualPdfViewer 
        pdfUrl={pdfUrl} 
        documentId={documentId}
      />
    {:else}
      <div class="placeholder">
        <p class="info-text">Selecciona un archivo PDF para comenzar</p>
        <p class="feature-text">Usa el Lápiz Inteligente para interactuar con el contenido</p>
      </div>
    {/if}
  </main>
</div>

<style>
  /* Estilos globales para PDFSlick */
  :global(.pdfSlickViewer) {
    margin: 0 !important;
  }
  
  :global(.pdfSlickContainer) {
    position: absolute !important;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
  
  .container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    width: 100%;
    overflow: hidden;
  }
  
  .header {
    padding: 10px 20px;
    background-color: #f8f9fa;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
  }
  
  h1 {
    font-size: 1.4rem;
    margin: 0;
    color: #333;
  }
  
  .upload-section {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .file-input {
    display: none;
  }
  
  .file-label {
    padding: 8px 16px;
    background-color: #0072e5;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.9rem;
  }
  
  .file-name {
    font-size: 0.9em;
    color: #555;
  }
  
  .error-message {
    background-color: #ffebee;
    color: #c62828;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 0.9rem;
  }
  
  .pdf-container {
    flex: 1;
    position: relative;
    background-color: #f5f5f5;
    overflow: hidden;
  }
  
  .debug-bar {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    background-color: rgba(240, 248, 255, 0.8);
    padding: 4px 8px;
    font-size: 12px;
    color: #0066cc;
    z-index: 10;
    word-break: break-all;
  }
  
  .placeholder {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    text-align: center;
    padding: 20px;
  }
  
  .info-text {
    font-size: 1.5rem;
    color: #555;
    margin-bottom: 10px;
  }
  
  .feature-text {
    font-size: 1.1rem;
    color: #777;
  }
</style>